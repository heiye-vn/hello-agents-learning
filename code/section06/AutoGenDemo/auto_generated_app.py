import streamlit as st
import requests
import logging
import concurrent.futures
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 页面配置
st.set_page_config(page_title="比特币实时价格", page_icon="₿", layout="centered")

# 自定义高对比度暗黑模式 CSS
st.markdown("""
<style>
    .main, .stApp {
        background-color: #0e1117;
    }
    .main, p {
        color: #c9d1d9;
    }
    .btc-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        margin-top: 50px;
    }
    .btc-title {
        font-size: 24px;
        color: #8b949e;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .btc-price {
        font-size: 48px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 15px;
    }
    .btc-change {
        font-size: 20px;
        font-weight: 500;
        margin-bottom: 20px;
    }
    .up {
        color: #3fb950;
    }
    .down {
        color: #f85149;
    }
    .error-text {
        color: #f85149;
        font-size: 18px;
        margin-bottom: 20px;
    }
    .stButton > button {
        width: 100%;
        background-color: #238636;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #2ea043;
        color: #ffffff;
    }
    .stButton > button:disabled {
        background-color: #21262d;
        color: #8b949e;
    }
    .spinner {
        border: 4px solid #30363d;
        border-top: 4px solid #ffffff;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# 全局 Session 复用连接池与标头，提高性能与防拦截
session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BTCStreamlitApp/1.0"}

def fetch_from_coingecko() -> Optional[Dict[str, Any]]:
    """主数据源: CoinGecko"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
    try:
        resp = session.get(url, timeout=(3, 5), headers=headers)
        if resp.status_code == 451:
            raise requests.exceptions.HTTPError("451 Unavailable For Legal Reasons")
        resp.raise_for_status()
        data = resp.json()
        price = float(data['bitcoin']['usd'])
        change_pct = float(data['bitcoin'].get('usd_24h_change', 0.0))
        change_abs = price * (change_pct / 100) if change_pct else 0.0
        return {
            'price': price,
            'change_pct': change_pct,
            'change_abs': change_abs
        }
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        logger.warning(f"CoinGecko 请求失败: {e}")
        return None

def fetch_from_binance() -> Optional[Dict[str, Any]]:
    """备用数据源1: Binance"""
    url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
    try:
        resp = session.get(url, timeout=(3, 5), headers=headers)
        resp.raise_for_status()
        data = resp.json()
        price = float(data['lastPrice'])
        open_price = float(data['openPrice'])
        change_abs = price - open_price
        change_pct = (change_abs / open_price) * 100 if open_price else 0.0
        return {
            'price': price,
            'change_pct': change_pct,
            'change_abs': change_abs
        }
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        logger.warning(f"Binance 请求失败: {e}")
        return None

def fetch_from_coinbase() -> Optional[Dict[str, Any]]:
    """备用数据源2: Coinbase"""
    url = "https://api.coinbase.com/v2/prices/BTC-USD/stats"
    try:
        resp = session.get(url, timeout=(3, 5), headers=headers)
        resp.raise_for_status()
        data = resp.json()['data']
        price = float(data['last'])
        open_price = float(data['open'])
        change_abs = price - open_price
        change_pct = (change_abs / open_price) * 100 if open_price else 0.0
        return {
            'price': price,
            'change_pct': change_pct,
            'change_abs': change_abs
        }
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        logger.warning(f"Coinbase 请求失败: {e}")
        return None

def get_btc_data() -> Optional[Dict[str, Any]]:
    """多源并发容错获取数据，大幅减少顺序请求带来的阻塞时间"""
    sources = [fetch_from_coingecko, fetch_from_binance, fetch_from_coinbase]
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    futures = {executor.submit(src): src.__name__ for src in sources}
    
    try:
        # as_completed 会在任意一个完成时返回，最多等待 5 秒
        for future in concurrent.futures.as_completed(futures, timeout=5):
            try:
                data = future.result()
                if data:
                    # 获取到有效数据后，非阻塞关闭线程池并取消未完成的任务
                    executor.shutdown(wait=False, cancel_futures=True)
                    return data
            except Exception as e:
                logger.warning(f"Data source {futures[future]} failed: {e}")
        
        executor.shutdown(wait=False)
        return None
    except concurrent.futures.TimeoutError:
        logger.error("所有数据源获取超时")
        executor.shutdown(wait=False, cancel_futures=True)
        return None

# 初始化 Session State
if 'btc_data' not in st.session_state:
    st.session_state.btc_data = None
if 'is_error' not in st.session_state:
    st.session_state.is_error = False
if 'is_loading' not in st.session_state:
    # 初次加载直接进入 loading 状态
    st.session_state.is_loading = True

if st.session_state.is_loading:
    # 先渲染加载 UI，再执行获取请求，避免 UI 卡死无反馈
    st.markdown('<div class="btc-card">', unsafe_allow_html=True)
    st.markdown('<div class="btc-title">比特币 (BTC) / USD</div>', unsafe_allow_html=True)
    st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#8b949e;">正在获取最新数据...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 后台执行获取逻辑
    new_data = get_btc_data()
    if new_data:
        st.session_state.btc_data = new_data
        st.session_state.is_error = False
    else:
        st.session_state.is_error = True
    st.session_state.is_loading = False
    st.rerun()

elif st.session_state.is_error or st.session_state.btc_data is None:
    st.markdown('<div class="btc-card">', unsafe_allow_html=True)
    st.markdown('<div class="btc-title">数据获取失败</div>', unsafe_allow_html=True)
    st.markdown('<div class="error-text">网络异常或数据源受限，请稍后重试</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("重试", key="retry_btn"):
        st.session_state.is_loading = True
        st.rerun()

else:
    data = st.session_state.btc_data
    # 显式转换为 float 防止类型异常或 XSS 注入
    price = float(data['price'])
    change_pct = float(data['change_pct'])
    change_abs = float(data['change_abs'])
    
    color_class = "up" if change_pct >= 0 else "down"
    arrow = "▲" if change_pct >= 0 else "▼"
    
    st.markdown('<div class="btc-card">', unsafe_allow_html=True)
    st.markdown('<div class="btc-title">比特币 (BTC) / USD</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="btc-price">${price:,.2f}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="btc-change {color_class}">'
        f'{arrow} ${abs(change_abs):,.2f} ({change_pct:+.2f}%) 24h'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("刷新数据", key="refresh_btn"):
        st.session_state.is_loading = True
        st.rerun()