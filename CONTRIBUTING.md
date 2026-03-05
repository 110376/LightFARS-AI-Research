# 贡献指南

感谢你考虑为 LightFARS 做出贡献！

## 🤔 如何贡献

### 报告 Bug

如果你发现了 Bug，请：

1. 检查 [Issues](https://github.com/你的用户名/lightfars/issues) 是否已有人报告
2. 如果没有，创建一个新的 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤
   - 期望的行为
   - 实际的行为
   - 环境信息（Python 版本、操作系统等）

### 提出新功能

如果你有新功能的想法：

1. 先在 [Issues](https://github.com/你的用户名/lightfars/issues) 中讨论
2. 说明功能的用途和实现思路
3. 等待维护者反馈后再开始开发

### 提交代码

#### 1. Fork 项目

点击 GitHub 页面右上角的 Fork 按钮

#### 2. 克隆你的 Fork

```bash
git clone https://github.com/你的用户名/lightfars.git
cd lightfars
```

#### 3. 创建特性分支

```bash
git checkout -b feature/你的功能名
```

#### 4. 进行修改

- 遵循现有代码风格
- 添加必要的注释和文档
- 确保代码通过测试

#### 5. 提交更改

```bash
git add .
git commit -m "feat: 添加 xxx 功能"
```

#### 6. 推送到你的 Fork

```bash
git push origin feature/你的功能名
```

#### 7. 创建 Pull Request

1. 访问你 Fork 的 GitHub 页面
2. 点击 "New Pull Request"
3. 填写 PR 描述：
   - 说明修改了什么
   - 为什么这样修改
   - 相关的 Issue 链接

---

## 📝 代码规范

### Python 代码风格

- 遵循 PEP 8 规范
- 使用有意义的变量和函数名
- 添加类型提示（Type Hints）
- 编写文档字符串（Docstrings）

### 示例

```python
from typing import List, Dict
from langchain_core.tools import tool

@tool
def search_papers(query: str, max_results: int = 10) -> str:
    """搜索学术论文。

    Args:
        query: 搜索关键词
        max_results: 最大返回结果数

    Returns:
        JSON 格式的论文列表
    """
    # 实现代码
    pass
```

---

## 🧪 测试

提交前请确保：

1. 代码没有语法错误
2. 功能正常工作
3. 不影响现有功能

```bash
# 运行测试
python -m pytest tests/

# 代码格式检查
python -m black src/
python -m flake8 src/
```

---

## 📖 文档

如果修改了功能，请同步更新：

- README.md（如果是用户可见的功能）
- 代码注释
- 相关文档

---

## 🎯 提交信息规范

使用语义化提交信息：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式调整 |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具链相关 |

示例：
```
feat: 添加新闻摘要 Agent
fix: 修复 arXiv 搜索参数问题
docs: 更新 README 安装说明
```

---

## ⚖️ 行为准则

- 尊重所有贡献者
- 欢迎不同意见，友好讨论
- 关注问题本身，而非个人

---

## 📮 联系方式

如有疑问，请：
- 提交 [Issue](https://github.com/你的用户名/lightfars/issues)
- 发起 [Discussion](https://github.com/你的用户名/lightfars/discussions)

---

**再次感谢你的贡献！** 🎉
