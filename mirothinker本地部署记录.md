1. 下载代码到本地
git clone https://github.com/MiroMindAI/MiroThinker
cd MiroThinker
2. 环境配置
cd apps/miroflow-agent
uv sync
3. Configure API keys
cp .env.example .env

4. 启动web ui界面
cd apps/gradio-demo
uv sync
5. 启动LM Studio
- 打开 LM Studio，下载模型（如 google/gemma-4-e4b）
- 点击 "Start Server"，默认 http://localhost:1234/v1
6. 环境配置
在 apps/gradio-demo/main.py 第 70-81 行 可以看到读取逻辑：
# 第 73-81 行
llm_provider = os.getenv(
    "DEFAULT_LLM_PROVIDER", "qwen"
)  # 默认 qwen
model_name = os.getenv(
    "DEFAULT_MODEL_NAME", "MiroThinker"
)  # 默认 MiroThinker
agent_set = os.getenv("DEFAULT_AGENT_SET", "demo")
base_url = os.getenv("BASE_URL", "http://localhost:11434")  # 默认 11434
api_key = os.getenv("API_KEY", "")

解决方案
方式一：在 apps/gradio-demo/ 创建 .env
在 apps/gradio-demo/ 新建 .env 文件：
# apps/gradio-demo/.env
# Gradio Web UI 主模型配置（本地 LM Studio）
BASE_URL=http://192.168.0.187:1234/v1
API_KEY=any
DEFAULT_MODEL_NAME=mirothinker-1.7-mini
DEFAULT_LLM_PROVIDER=qwen

# 如果需要切换模型，按需修改上方 DEFAULT_MODEL_NAME
# LM Studio 启动后默认端口 1234

DEFAULT_LLM_PROVIDER 只影响加载哪个 yaml 配置文件（temperature、max_tokens 等参数），改为 openai，使用 gpt-5.yaml 配置


7. 启动UI界面
uv run main.py


8. 重点改造成本地searcng搜索

项目中为实现 SearXNG 兼容性，进行了以下具体修订：
1. 新增 SearXNG MCP Server
文件: libs/miroflow-tools/src/miroflow_tools/mcp_servers/searxng_mcp_server.py
- 实现 searxng_search 工具函数
- 配置 SearXNG 使用 Google 引擎
- 返回标准化 JSON 格式（title, url, snippet）
2. 添加 SearXNG Fallback 支持
文件: libs/miroflow-tools/src/miroflow_tools/dev_mcp_servers/search_and_scrape_webpage.py
- 在 google_search 工具中添加 _fallback_to_searxng() 函数
- 当 Serper API 不可用或失败时，自动切换到本地 SearXNG
- 转换 SearXNG 格式为 Serper 兼容格式
3. 配置注册
文件: apps/miroflow-agent/src/config/settings.py
- 添加 SEARXNG_BASE_URL 和 SEARXNG_API_KEY 环境变量
- 在 create_mcp_server_parameters() 中注册 searxng_search 工具
- 在 get_env_info() 中添加 SearXNG 信息收集
4. Agent 配置
文件: apps/miroflow-agent/conf/agent/demo.yaml
main_agent:
  tools:
    - searxng_search          # 新增 SearXNG 搜索工具
    - search_and_scrape_webpage
  tool_blacklist:
    - [ "search_and_scrape_webpage", "sogou_search" ]
5. 环境配置
文件: .env
SEARXNG_BASE_URL=http://localhost:12369

不过原生模型采用google search训练的，天然提出google search工具调用，失败后，才fall back到searxng上。

6. 日志分析
每个任务运行后，存放一个json日志，比如D:\MiroThinker-main\MiroThinker-main\apps\gradio-demo\logs\api-server。我们可以使用D:\MiroThinker-main\MiroThinker-main\apps\visualize-trace\run.py进行可视化阅读。具体运行参考D:\MiroThinker-main\MiroThinker-main\apps\visualize-trace\README.md文件。操作如下：
PS D:\MiroThinker-main\MiroThinker-main> cd .\apps\visualize-trace\
PS D:\MiroThinker-main\MiroThinker-main\apps\visualize-trace> python run.py
PS D:\MiroThinker-main\MiroThinker-main\apps\visualize-trace> uv run run.py
Application will run at http://localhost:5000
然后把日志path复制到directory里，然后再自己加载特定的日志内容，然后点击load既可以。
