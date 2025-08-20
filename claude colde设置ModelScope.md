# Claude Code × 魔搭免费 API 配置笔记

> 来源：微信公众号「鲲鹏Talk」  
> 原文链接：https://mp.weixin.qq.com/s/x-vSg8RqtPvpRgfA1iWVPQ  
> 日期：2025-08-17

---

## 1. 免费额度速览
| 项目 | 额度 |
| --- | --- |
| 每日总调用 | 2000 次 |
| Qwen3-Coder 专属 | 500 次 |
| 并发限制 | 以平台实时提示为准 |
| 状态 | Beta 测试，随时可能调整 |

---

## 2. 准备工作（一次性）
1. **注册 / 登录**：https://modelscope.cn  
2. **绑定阿里云账号**（必须）：  
   个人中心 → 阿里云账号 → 立即绑定  
3. **获取 Access Token**  
   个人中心 → **我的 AccessToken** → 生成 → 复制  
   ⚠️ **在 Claude Code 中使用时去掉 `ms-` 前缀**  
   例：`ms-abcdef123456` → 只保留 `abcdef123456`

---

## 3. Claude Code 配置
### 3.1 找到配置文件
- **Windows**  
  `C:\Users\<你的用户名>\.claude\settings.json`  
- **Linux / macOS**  
  `~/.claude/settings.json`

> 若文件不存在，手动创建即可。

### 3.2 写入配置
```json
{
  "env": {
    "ANTHROPIC_API_KEY":  "你的Token（去掉ms-前缀）",
    "ANTHROPIC_BASE_URL": "https://api-inference.modelscope.cn",
    "ANTHROPIC_MODEL": "Qwen/Qwen3-Coder-480B-A35B-Instruct",
    "ANTHROPIC_SMALL_FAST_MODEL": "Qwen/Qwen3-Coder-480B-A35B-Instruct"
  },
  "permissions": {
    "allow": [],
    "deny": []
  }
}