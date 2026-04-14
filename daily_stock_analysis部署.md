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
# 高级：模型路由 YAML 配置（可选，参考 litellm_config.example.yaml）
LITELLM_CONFIG=./litellm_config.yaml

我们还要修改D:\daily_stock_analysis-main\litellm_config.yaml，这个复制来自D:\daily_stock_analysis-main\litellm_config.example.yaml
model_list:
  # --- siliconflow (OpenAI 兼容，一个 Key 使用多种模型) ---
  # 这是一个自定义 OpenAI 兼容模型渠道的示例
  - model_name: ollama/qwen3:8b
    litellm_params:
      model: ollama/qwen3:8b
      #api_key: "os.environ/LITELLM_API_KEY" # 从环境变量读取 Key，安全防泄漏   # 本地模型ollama没有key
      api_base: http://192.168.0.187:11434
      # 以下配置是表示如何启用Qwen模型的enable_thinking开关
      extra_body:
        chat_template_kwargs:
          enable_thinking: true

修改D:\daily_stock_analysis-main\docker\docker-compose.yml文件
  volumes:
    - ../data:/app/data
    - ../logs:/app/logs
    - ../reports:/app/reports
    - ../.env:/app/.env
    - ../strategies:/app/strategies:ro
    - ../litellm_config.yaml:/app/litellm_config.yaml:ro   #新增这个
    # 如需覆盖前端静态资源，可挂载本地 static 目录
    # - ../static:/app/static:ro


步骤 2 — 启动服务：
# 同时启动调度器和 Web 服务器（推荐）
docker-compose -f ./docker/docker-compose.yml up -d   这会启用sever和analyzer两个容器
docker-compose -f ./docker/docker-compose.yml up -d sever 只启用sever，可以通过localhost:8000打开
docker-compose -f ./docker/docker-compose.yml up -d analyzer 启用analyzer  ， 定时分析




其他修订：
文件: D:\daily_stock_analysis-main\src\search_service.py
第2114-2115行:
NEWS_OVERSAMPLE_FACTOR = 2
NEWS_OVERSAMPLE_MAX = 10
方案B: 同时增加倍数和上限
NEWS_OVERSAMPLE_FACTOR = 3  # 从2改为3
NEWS_OVERSAMPLE_MAX = 20    # 从10改为20
这样可以获得更多原始搜索结果，减少过滤后的数据不足问题。

# Agent 执行超时预算（秒，0 表示关闭；single-agent 用作整体循环预算，multi-agent 用作协作编排预算；默认 600）
AGENT_ORCHESTRATOR_TIMEOUT_S=1200#600




