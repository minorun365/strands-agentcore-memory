from strands import Agent, tool
from mcp.client.streamable_http import streamablehttp_client
from strands.tools.mcp.mcp_client import MCPClient
from typing import Optional
import asyncio
import logging

from .stream_processor import StreamProcessor

logger = logging.getLogger(__name__)


class AWSKnowledgeAgentManager:
    """AWS Knowledge エージェントのクラス化管理"""
    
    def __init__(self):
        self.mcp_client: Optional[MCPClient] = None
        self.stream_processor = StreamProcessor("AWSナレッジ")
        self._initialize_mcp_client()
    
    def _initialize_mcp_client(self) -> None:
        """MCP クライアントを初期化"""
        try:
            self.mcp_client = MCPClient(
                lambda: streamablehttp_client("https://knowledge-mcp.global.api.aws")
            )
            logger.info("AWS Knowledge MCP クライアント初期化成功")
        except Exception as e:
            logger.error(f"AWS Knowledge MCP クライアント初期化失敗: {e}")
            self.mcp_client = None
    
    def set_parent_stream_queue(self, queue: Optional[asyncio.Queue]) -> None:
        """親エージェントのストリームキューを設定"""
        self.stream_processor.set_parent_queue(queue)
    
    def create_agent(self) -> Agent:
        """AWSナレッジエージェントを作成（MCPコンテキスト内で呼び出される）"""
        if not self.mcp_client:
            raise RuntimeError("AWS Knowledge MCP client is not available")
        
        available_tools = self.mcp_client.list_tools_sync()
        return Agent(
            model="anthropic.claude-3-5-sonnet-20241022-v2:0",
            tools=available_tools
        )
    
    async def process_query(self, query: str) -> str:
        """クエリを処理してレスポンスを返す"""
        if not self.mcp_client:
            return "AWS Knowledge MCP client is not available"
        
        try:
            return await self.stream_processor.process_query_with_context(
                query, 
                self.mcp_client, 
                self.create_agent
            )
        except Exception as e:
            logger.error(f"AWS Knowledge エージェント処理エラー: {e}")
            return "AWS Knowledge MCP client is not available"
    
    @property
    def is_available(self) -> bool:
        """MCPクライアントが利用可能かどうか"""
        return self.mcp_client is not None


# グローバルインスタンス（シングルトンパターン）
_knowledge_manager = AWSKnowledgeAgentManager()

def set_parent_stream_queue(queue: Optional[asyncio.Queue]) -> None:
    """後方互換性のための関数"""
    _knowledge_manager.set_parent_stream_queue(queue)

@tool
async def aws_knowledge_agent(query: str) -> str:
    """AWS知識ベースエージェント（改善版）"""
    return await _knowledge_manager.process_query(query)