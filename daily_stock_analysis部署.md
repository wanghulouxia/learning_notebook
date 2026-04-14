步骤 1 — 克隆并配置：
从github下载daily_stock_analysis到本地。

cd daily_stock_analysis
cp .env.example .env
配置环境变量参数如下：
# Gemini（https://aistudio.google.com）
#GEMINI_API_KEY=     #没有账号，先注释掉
#TUSHARE_TOKEN=   # #没有账号，先注释掉
# Ollama 本地模型（无需 API Key，推荐）
OLLAMA_API_BASE=http://192.168.0.187:11434
LITELLM_MODEL=ollama/qwen3:8b

#ANSPIRE_API_KEYS=   #没有账号，先注释掉

# Tavily API Keys（支持多个，逗号分隔）
#TAVILY_API_KEYS=            #没有账号，先注释掉
# SerpAPI Keys（支持多个，逗号分隔）
#SERPAPI_API_KEYS=            #没有账号，先注释掉

SEARXNG_BASE_URLS=http://192.168.0.187:12369
SEARXNG_PUBLIC_INSTANCES_ENABLED=true

AGENT_SKILLS=bull_trend

# 【方式二】飞书机器人
# 在飞书群 -> 设置 -> 群机器人 -> 添加机器人 -> 自定义机器人 -> 复制 Webhook 地址
#
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_key_here


步骤 2 — 启动服务：
# 同时启动调度器和 Web 服务器（推荐）
docker-compose -f ./docker/docker-compose.yml up -d












