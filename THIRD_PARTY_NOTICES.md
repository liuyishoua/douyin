# 第三方来源与许可范围

## 本仓库代码

本项目从 [liuyishoua/bifrost](https://github.com/liuyishoua/bifrost) 的 `applications/douyin` 提取，
来源提交：`dc984f1b1eca7978bf54677e2a9eafd62685d9e6`。本仓库中版权所有者拥有权利的代码沿用
[PolyForm Noncommercial License 1.0.0](LICENSE)，保留原 Required Notice。
该声明不替代第三方代码、素材及依赖自己的许可条件，也不表示对第三方代码重新授权。

## 原抖音接口项目

原接口代码、协议资源和部分素材来源于
[cv-cat/DouYin_Spider](https://github.com/cv-cat/DouYin_Spider)。
原作者说明保存在 [docs/upstream-readme.md](docs/upstream-readme.md)，
原 `author/` 素材和代码中已有来源标注继续保留。
涉及目录主要为 `dy_apis/`、`builder/`、`utils/`、`static/`、`dy_live/`、`author/` 及原示例脚本；
这些目录也包含后续修改，不能仅按目录认定每段代码的权利归属。

截至 2026-10-05，提取的源码及上游当前仓库根目录未见独立 LICENSE 文件；
上游 README 声明仅供学习与技术研究使用。此处记录该事实，不将其认定为 MIT、Apache 等标准许可，
也不以本仓库的 PolyForm 声明替代上游授权。

## 运行依赖

Flask、cryptography、qrcode / Pillow、Beautiful Soup、curl_cffi、ecdsa、loguru、protobuf、
python-dotenv、requests 及其传递依赖均按各自分发包的许可证使用。
这些依赖通过 `requirements-web.txt` 安装，未将其安装目录纳入本仓库。
原 `requirements.txt` 中媒体、直播等扩展依赖同样保留其各自许可。

## README 截图

`docs/images/` 中图片由本仓库 Web 控制台在独立演示环境运行时截取，
账号、用户、文案及任务均为模拟数据，不代表真实账号发送结果。
