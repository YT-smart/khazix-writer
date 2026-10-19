# Khazix Writer

卡兹克风格的公众号文章创作 Skill。

## 它是什么

这个 Skill 将卡兹克的公开文章、人物判断方式、写作框架和公众号排版经验整合在一起，用来学习他的观察方式和内容工作流。

它不是简单复制口头禅，也不是让模型冒充卡兹克本人。

知识库包含 46 篇有效公众号原文，以及人物框架、主题资料和实体资料。原文已经移除了微信阅读器附加的扫码、授权、分析、点赞、分享等无关内容。

## 安装

### Windows PowerShell

```powershell
git clone https://github.com/YT-smart/khazix-writer.git "$env:USERPROFILE\.codex\skills\khazix-writer"
```

### macOS / Linux

```bash
git clone https://github.com/YT-smart/khazix-writer.git ~/.codex/skills/khazix-writer
```

如果已经安装过：

```bash
git -C ~/.codex/skills/khazix-writer pull --ff-only
```

Windows PowerShell 使用：

```powershell
git -C "$env:USERPROFILE\.codex\skills\khazix-writer" pull --ff-only
```

安装后重新打开 Codex，或者开启一个新的对话即可使用。

## 怎么用

直接在 Codex 里提出请求：

> 用 Khazix Writer 写一篇关于 AI 知识库的公众号文章。

或者：

> 按卡兹克的观察方式，分析这个 AI 产品对普通人有什么意义。

也可以提供主题、新闻链接、产品资料、个人经历或已有草稿：

> 用卡兹克的公众号写作方式，把下面的产品资料写成一篇文章。我的亲身体验是……

Skill 会先理解主题和读者，再从知识库查找相关资料，选择合适的判断框架，最后组织成公众号文章。

默认流程是：

1. 先根据你的要求写正文，并给出配图建议
2. 你确认正文后，再生成公众号排版内容
3. 有图片时，先确认来源和用途，再处理成 base64 图片，方便复制到公众号

涉及最新的产品、价格、版本、排名或开放资格时，仍然需要核对当前资料。知识库里的旧文章只代表卡兹克当时的判断。

## 五个核心判断框架

1. 从用户卡住的地方反推方案
2. 把能力宣传翻译成具体任务，并保留失败边界
3. 按目标、成本和效果选择人机组合
4. 除了能力，还要看入口、工作流和迁移成本
5. 沿着技术动作，追到它改变了谁的生活

这些框架是基于公开文章的分析归纳，不是卡兹克本人发布的官方方法论。

## 使用边界

这个 Skill 只供学习卡兹克的观察方式、写作框架和内容工作流。

请保留自己的经历、判断和表达方式，不要把卡兹克的购买、测试、采访或现场经历写成自己的亲历，也不要让文章冒充卡兹克本人发布。

学习一个人的最终目的，是形成自己的风格。
