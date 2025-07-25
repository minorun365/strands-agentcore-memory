import streamlit as st
import uuid
from datetime import datetime
from memory_manager import get_session_history


def initialize_session_state():
    """セッション状態の初期化"""
    if 'threads' not in st.session_state:
        st.session_state.threads = {}
    
    # ユーザーID（固定）
    if 'user_id' not in st.session_state:
        st.session_state.user_id = "user_1"  # 固定ユーザー
    
    # セッションID（可変：新しい会話ごとに生成）
    if 'current_thread_id' not in st.session_state:
        # リロード後は常に新規セッションで開始
        # 新しいセッションIDを生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:12]
        st.session_state.current_thread_id = f"session_{timestamp}_{unique_id}"
        
        # 初期の「現在の会話」をサイドバーに表示するため、threadsに追加
        st.session_state.threads[st.session_state.current_thread_id] = {
            'title': '現在の会話',
            'messages': []
        }
    
    if 'current_thread_title' not in st.session_state:
        st.session_state.current_thread_title = "現在の会話"
    
    # メモリキャッシュをクリア（リロード時の履歴復元を確実にするため）
    if 'cache_cleared' not in st.session_state:
        try:
            st.cache_data.clear()
        except Exception:
            pass
        st.session_state.cache_cleared = True
    
    # メモリから履歴を復元（初回のみ）
    if 'memory_restored' not in st.session_state:
        restore_session_from_memory()
        st.session_state.memory_restored = True

def create_new_thread():
    """新しいスレッド（セッション）を作成"""
    # 現在のスレッドが未発話の場合、新しいスレッドを作成しない
    if (st.session_state.current_thread_title == "現在の会話" and 
        st.session_state.current_thread_id in st.session_state.threads and
        len(st.session_state.threads[st.session_state.current_thread_id]['messages']) == 0):
        return st.session_state.current_thread_id
    
    # 新しいセッションIDを生成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:12]
    new_session_id = f"session_{timestamp}_{unique_id}"
    st.session_state.current_thread_id = new_session_id
    st.session_state.current_thread_title = "現在の会話"
    
    # 新しいスレッドを一番上に追加（既存の辞書を再構築）
    if hasattr(st.session_state, 'threads') and st.session_state.threads:
        from collections import OrderedDict
        new_threads = OrderedDict()
        new_threads[new_session_id] = {
            'title': '現在の会話',
            'messages': []
        }
        for thread_id, thread_data in st.session_state.threads.items():
            new_threads[thread_id] = thread_data
        st.session_state.threads = dict(new_threads)
    else:
        st.session_state.threads = {
            new_session_id: {
                'title': '現在の会話',
                'messages': []
            }
        }
    
    return new_session_id


def add_message_to_thread(thread_id, role, content):
    """スレッドにメッセージを追加"""
    if thread_id not in st.session_state.threads:
        st.session_state.threads[thread_id] = {
            'title': '現在の会話',
            'messages': []
        }
    
    st.session_state.threads[thread_id]['messages'].append({
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    })
    
    # ユーザーの最初のメッセージでタイトル候補を準備（即座にcurrent_thread_titleを更新）
    if role == 'user' and st.session_state.threads[thread_id]['title'] == '現在の会話':
        title = content[:47] + "..." if len(content) > 50 else content
        # サイドバーでのリアルタイム表示用にcurrent_thread_titleを即座に更新
        if thread_id == st.session_state.current_thread_id:
            st.session_state.current_thread_title = title
        # threads辞書も更新
        st.session_state.threads[thread_id]['title'] = title

def update_thread_title(thread_id, title):
    """スレッドのタイトルを更新"""
    if thread_id in st.session_state.threads:
        st.session_state.threads[thread_id]['title'] = title
        if thread_id == st.session_state.current_thread_id:
            st.session_state.current_thread_title = title

def get_thread_messages(thread_id):
    """指定されたスレッドのメッセージを取得"""
    if thread_id in st.session_state.threads:
        return st.session_state.threads[thread_id].get('messages', [])
    return []

def render_sidebar():
    """サイドバーのレンダリング"""
    with st.sidebar:
        # 新しい会話を始めるボタン
        if st.button("新しい会話を始める", use_container_width=True):
            create_new_thread()
            st.rerun()
        
        # スレッド一覧の表示
        if st.session_state.threads:
            st.subheader("会話履歴")
            
            # スレッド一覧を表示
            
            for thread_id, thread_data in st.session_state.threads.items():
                # 現在のスレッドかどうかでスタイルを変更
                is_current = thread_id == st.session_state.current_thread_id
                
                # 現在のスレッドの場合、リアルタイムでタイトルを反映
                if is_current:
                    display_title = st.session_state.current_thread_title
                else:
                    display_title = thread_data['title']
                
                if st.button(
                    f"{display_title[:30]}{'...' if len(display_title) > 30 else ''}",
                    key=f"thread_{thread_id}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    # スレッド切り替え
                    st.session_state.current_thread_id = thread_id
                    st.session_state.current_thread_title = thread_data['title']
                    st.rerun()

def render_chat_history():
    """チャット履歴の表示"""
    messages = get_thread_messages(st.session_state.current_thread_id)
    
    if messages:
        for message in messages:
            role = message['role']
            content = message['content']
            
            if role == 'user':
                with st.chat_message("user"):
                    st.markdown(content)
            elif role == 'assistant':
                with st.chat_message("assistant"):
                    st.markdown(content)

def restore_session_from_memory():
    """AgentCore Memoryから過去の全セッション履歴を復元"""
    try:
        from memory_manager import get_available_sessions
        
        available_sessions = get_available_sessions()
        if not available_sessions:
            return
        
        # 現在の「現在の会話」を保持
        current_new_thread_id = st.session_state.current_thread_id
        current_new_thread = st.session_state.threads.get(current_new_thread_id, {
            'title': '現在の会話',
            'messages': []
        })
        
        # 各セッションを復元
        temp_threads = {current_new_thread_id: current_new_thread}
        
        for session_id in available_sessions:
            try:
                session_history = get_session_history(session_id, k=20)
                
                if session_history and len(session_history) > 0:
                    thread_id = f"session_{session_id}"
                    
                    # 重複回避
                    if thread_id == current_new_thread_id:
                        continue
                    
                    # タイトルを最初のユーザーメッセージから生成
                    thread_title = f"セッション {session_id[:8]}..."
                    for msg in session_history:
                        if msg['role'] == 'user':
                            # タイトル自動生成
                            thread_title = msg['content'][:47] + "..." if len(msg['content']) > 50 else msg['content']
                            break
                    
                    temp_threads[thread_id] = {
                        'title': thread_title,
                        'messages': session_history
                    }
                    
            except Exception:
                continue
        
        st.session_state.threads = temp_threads
        
    except Exception:
        pass

