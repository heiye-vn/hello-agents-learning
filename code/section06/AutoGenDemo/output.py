import streamlit as st
import requests
from datetime import datetime

# 设置页面配置
st.set_page_config(page_title="BTC Price Tracker", page_icon="₿", layout="centered")

# 隐藏 Streamlit 默认菜单并优化暗黑模式卡片高对比度外观
custom_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stMetric {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                padding: 18px 20px !important;
                border-radius: 12px !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            }
            .stMetric label {
                color: #a0aec0 !important;
                font-weight: 500 !important;
            }
            .stMetric [data-testid="stMetricValue"] {
                color: #f7fafc !important;
                font-weight: 700 !important;
            }
            </style>
            """
st.markdown(custom_style, unsafe_allow_html=True)


def get_btc_data():
    """
    获取比特币对美元的实时行情数据。
    支持多数据源备用降级（CoinCap / CoinGecko / OKX / Binance），规避地区 HTTP 451 限制。
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # 1. 尝试 CoinCap API
    try:
        url = "https://api.coincap.io/v2/assets/bitcoin"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            price = float(data.get("priceUsd", 0))
            change_percent = float(data.get("changePercent24Hr", 0))
            change = price - (price / (1 + change_percent / 100))
            return {
                "success": True,
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "source": "CoinCap API",
            }
    except Exception:
        pass

    # 2. 尝试 CoinGecko API
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json().get("bitcoin", {})
            price = float(data.get("usd", 0))
            change_percent = float(data.get("usd_24h_change", 0))
            change = price - (price / (1 + change_percent / 100))
            return {
                "success": True,
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "source": "CoinGecko API",
            }
    except Exception:
        pass

    # 3. 尝试 OKX API
    try:
        url = "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            ticker = resp.json().get("data", [{}])[0]
            price = float(ticker.get("last", 0))
            open_price = float(ticker.get("open24h", price))
            change = price - open_price
            change_percent = (change / open_price * 100) if open_price else 0
            return {
                "success": True,
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "source": "OKX API",
            }
    except Exception:
        pass

    # 4. 尝试 Binance API (保底)
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            price = float(data["lastPrice"])
            change = float(data["priceChange"])
            change_percent = float(data["priceChangePercent"])
            return {
                "success": True,
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "source": "Binance API",
            }
    except Exception as e:
        return {"success": False, "error": f"多数据源请求均受限或超时 ({str(e)})"}

    return {"success": False, "error": "无法连接到行情服务器，请检查网络设置。"}


# ================= UI 布局 =================

st.title("₿ 比特币实时价格监控")
st.markdown("### USD / Tether 现货行情")

# 刷新按钮
if st.button("🔄 刷新数据", use_container_width=True):
    # Streamlit 按钮点击会自动重新运行脚本，这里不需要写具体逻辑
    pass

# 加载状态与数据获取
with st.spinner("正在获取最新行情数据..."):
    btc_data = get_btc_data()

# 数据展示与异常处理
if btc_data["success"]:
    price = btc_data["price"]
    change = btc_data["change"]
    change_percent = btc_data["change_percent"]

    # 格式化显示字符串，价格保留两位小数并加千分符
    price_str = f"${price:,.2f}"
    change_str = f"${change:,.2f}"
    delta_str = f"{change_percent:.2f}%"

    # 使用列布局展示核心指标
    col1, col2 = st.columns([2, 1])

    with col1:
        # st.metric 组件原生支持根据 delta 的正负自动变色（正绿负红）
        st.metric(label="当前价格 (USD)", value=price_str)

    with col2:
        st.metric(
            label="24小时涨跌",
            value=change_str,
            delta=delta_str,
            help="展示 24 小时内的价格涨跌额及对应百分比",
        )

    # 底部显示数据更新时间及来源
    source_name = btc_data.get("source", "网络行情")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"⏱️ 更新时间: {current_time}  |  📡 数据来源: {source_name}")

else:
    # 展示友好的错误提示
    st.error(f"❌ 获取数据失败！")
    st.warning(f"错误详情：{btc_data['error']}")
    st.info("💡 建议：请检查网络连接或稍后点击上方按钮重试。")
