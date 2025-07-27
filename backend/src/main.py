from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from dotenv import load_dotenv
from typing import AsyncGenerator, Any, Dict
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 各モジュールからインポート
from .aws_knowledge_agent import aws_knowledge_agent, set_parent_stream_queue as set_knowledge_queue
from .japanese_holiday_agent import japanese_holiday_agent, set_parent_stream_queue as set_holiday_queue
from .memory_manager import UnifiedMemoryManager

# 環境変数を読み込む（ローカル開発用）
load_dotenv()

class AgentManager:
    """エージェントとメモリ関連機能を管理するクラス（改善版）"""
    
    def __init__(self):
        self.memory_manager = UnifiedMemoryManager()
        # Strands Agents 1.0.1の新機能を活用した効率的なエージェント設定
        self.agent = Agent(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            tools=[aws_knowledge_agent, japanese_holiday_agent],
            system_prompt="""あなたは2つの専門サブエージェントを活用するAWSエキスパートです：

1. AWSナレッジエージェント: AWS公式ドキュメントから一般的な情報を検索
2. 祝日APIエージェント: 日本の祝日情報を提供（デモ用シンプルAPI）

効率的にサブエージェントを使い分けて、正確で実用的な回答を提供してください。""",
            # Strands 1.0.1の新機能：メモリプロバイダー統合
            callback_handler=None  # ストリーミングはコールバックではなく直接処理
        )
    
    def get_conversation_history_with_context(self, session_id: str, k: int = 3) -> str:
        """会話履歴を取得してコンテキスト文字列として返す（改善版）"""
        return self.memory_manager.get_conversation_history_as_context(session_id, k=k)
    
    def save_conversation(self, session_id: str, user_message: str, response: str):
        """会話をメモリに保存"""
        self.memory_manager.save_conversation(session_id, user_message, response)

# AgentCoreを初期化
app = BedrockAgentCoreApp()

# エージェントマネージャーのインスタンスを作成
agent_manager = AgentManager()


# AgentCoreのエントリーポイント関数を定義
@app.entrypoint
async def invoke(payload: Dict[str, Any]) -> AsyncGenerator[Any, None]:
    # AgentCore Runtime形式でのペイロード取得
    input_data = payload.get("input", {})
    user_message = input_data.get("prompt", "")
    session_id = input_data.get("session_id", "default_session")
    
    # 過去の会話履歴を取得してコンテキストに追加
    logger.info(f"セッション {session_id} の履歴取得開始")
    context = agent_manager.get_conversation_history_with_context(session_id, k=5)
    logger.info(f"履歴取得完了: {len(context)} 文字")
    if context:
        user_message = context + user_message
    
    # ストリームキューを初期化
    parent_stream_queue = asyncio.Queue()
    
    # サブエージェントにストリームキューを設定
    logger.info("サブエージェント用ストリームキューを設定")
    set_knowledge_queue(parent_stream_queue)
    set_holiday_queue(parent_stream_queue)
    logger.info("ストリームキュー設定完了")
    
    try:
        # Strands Agents 1.0.1の改善されたストリーミング処理
        accumulated_response = ""
        original_prompt = input_data.get("prompt", "")
        
        # リアルタイムストリーミングを実現する改善版merged_stream
        agent_stream = agent_manager.agent.stream_async(user_message)
        
        async def improved_merged_stream():
            """元の設計意図を保持しつつ改善されたストリーム統合"""
            # 初期タスクセットアップ
            agent_task = asyncio.create_task(anext(agent_stream, None))
            queue_task = asyncio.create_task(parent_stream_queue.get()) if parent_stream_queue else None
            
            # アクティブタスクセット
            pending_tasks = {agent_task}
            if queue_task:
                pending_tasks.add(queue_task)
            
            # 並行処理ループ：どちらのストリームからでもイベントが来次第即座に処理
            while pending_tasks:
                # FIRST_COMPLETED: 最初に完了したタスクを優先処理（リアルタイム性確保）
                completed_tasks, pending_tasks = await asyncio.wait(
                    pending_tasks, 
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                for completed_task in completed_tasks:
                    if completed_task == agent_task:
                        # メインエージェントイベント処理
                        event = completed_task.result()
                        if event is not None:
                            # テキスト蓄積処理
                            if isinstance(event, dict) and "event" in event:
                                event_data = event["event"]
                                if "contentBlockDelta" in event_data:
                                    delta = event_data["contentBlockDelta"].get("delta", {})
                                    if "text" in delta:
                                        nonlocal accumulated_response
                                        accumulated_response += delta["text"]
                            
                            yield event
                            
                            # 次のエージェントイベントを待機
                            agent_task = asyncio.create_task(anext(agent_stream, None))
                            pending_tasks.add(agent_task)
                        else:
                            # エージェントストリーム終了
                            agent_task = None
                    
                    elif completed_task == queue_task:
                        # サブエージェントイベント処理
                        try:
                            sub_event = completed_task.result()
                            logger.info(f"リアルタイムサブエージェントイベント: {sub_event}")
                            
                            # サブエージェントイベントをそのまま出力（AgentCore Runtime形式）
                            yield sub_event
                            
                            # 次のキューイベントを待機（キューが存在する場合）
                            if parent_stream_queue:
                                queue_task = asyncio.create_task(parent_stream_queue.get())
                                pending_tasks.add(queue_task)
                            else:
                                queue_task = None
                        except Exception as e:
                            logger.warning(f"サブエージェントキュー処理エラー: {e}")
                            queue_task = None
                
                # 終了条件: エージェントストリーム終了 && キューが空またはNone
                if (agent_task is None and 
                    (parent_stream_queue is None or parent_stream_queue.empty())):
                    break
        
        # 改善されたストリーム統合を実行
        async for event in improved_merged_stream():
            yield event
            
        # 会話をメモリに保存
        if accumulated_response:
            agent_manager.save_conversation(session_id, original_prompt, accumulated_response)
            
    except Exception:
        raise
    finally:
        set_knowledge_queue(None)
        set_holiday_queue(None)

# AgentCore Runtimeサーバーを起動
if __name__ == "__main__":
    app.run()