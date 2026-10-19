# 从粘贴HTML复原的微信排版

证据：[原始HTML](../raw/layout/wechat-reference.html)，[提取正文](../raw/layout/wechat-reference.txt)。可运行`python scripts/inspect_layout.py`查看属性频次。样本无标题与发表日期，包含28张图片；未在本次逐图阅读，文中的产品参数不能视为独立核验。

## 保留的设计

| 项目 | 样本证据 | 成稿处理 |
|---|---|---|
| 背景/正文 | 白底、rgba(0,0,0,0.9) | 白底近黑，取消装饰卡片 |
| 字号 | 外层17px，113个内层16px覆盖 | 正文最终16px，保留易读字号 |
| 字体 | PingFang SC、system-ui、微软雅黑等 | 系统中文无衬线字体栈 |
| 行距/字距 | line-height 1.6；letter-spacing .034em | 原样保留 |
| 段落 | 127次margin:0px 8px 24px | 左右8px，段后24px，短段不首行缩进 |
| 重点 | 11处16px bold内层样式 | 用局部加粗承接核心结论，不整篇加粗 |
| 图片 | 实际截图/效果图穿插，宽度有661px等页面残留 | width:100%;max-width:100%;height:auto，说明文字可选 |
| 结尾 | CTA约15px；作者/联系行12px灰色 | 用户提供才加，不能移植作者邮箱与身份 |

样本以正文串联过程，几乎没有装饰标题，不把它做成模板卡片、彩色模块或大段编号目录。教程需要层级时可以使用简洁粗体段或小标题；这属于可读性适配，不冒称为样本固有组件。

## 清理

不带`data-layout-id`、`data-pm-slice`、`leaf`、`textstyle`、`js_*`类名、`mp-style-type`、懒加载占位SVG、固定661px宽度、编辑器重复嵌套span。最终HTML的图片使用base64 `data:` URI，缺素材时用清晰文字占位。远程URL只能作为素材线索，不能直接成为可复制到公众号的最终图片地址。原文远程图片没有下载进本包，原链接可能失效；不默认复用它们作为新文章证据。

输出`article.html`是可嵌入正文的纯片段，样式全部内联；`article.preview.html`是带doctype、viewport和手机宽度外框的预览页。把预览页浏览器显示的正文复制到微信编辑器；最终编辑器对图片上传和粘贴样式的保留仍需现场确认，本包没有声称已经发布或验证微信后台行为。

## 渲染输入

`python scripts/render_wechat.py article.json --output-dir output`

JSON顶层字段：`title`（用于预览标题，不自动插入正文）、`author`、`contact`、`cta`（后三者均可省略）、`blocks`。

块支持`paragraph`、`heading`、`quote`、`image`、`list`。普通文本用`text`；局部粗体/链接用`spans:[{"text":"…","bold":true},{"text":"…","href":"https://…"}]`，不会把输入text当HTML执行。图片用`src`、`alt`、`caption`，src缺失时用`alt`渲染待补图说明；本地图片会在渲染阶段转成base64 `data:` URI，已有data URI可原样保留。远程URL只作线索，不作为最终图片地址。只输出原样文字，不替作者润色或杜撰截图。输入示例见[排版演示](../assets/layout-demo.json)。

成稿JSON由Markdown逐段转换，保留段序、措辞与强调；输出后核对两种格式内容。图片位置按“此处需要看什么证据”决定，不按固定段数插图。
