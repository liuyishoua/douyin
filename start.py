"""Create an isolated environment and launch the standalone console."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import shutil
import sys
import threading
import urllib.request
import venv
import webbrowser

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="抖音控制台一键启动（默认演示模式）")
    parser.add_argument("--real", action="store_true", help="使用真实账号模式")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--setup-only", action="store_true", help="仅安装依赖")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("请安装 Python 3.10 或更新版本")
    if not 1 <= args.port <= 65535:
        parser.error("端口必须在 1～65535 之间")
    directory = ROOT / ".venv"
    python = directory / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        print("正在创建独立 Python 环境……", flush=True)
        venv.EnvBuilder(with_pip=True).create(directory)
    requirements = ROOT / "requirements-web.txt"
    digest = hashlib.sha256(requirements.read_bytes()).hexdigest()
    marker = directory / ".douyin-requirements"
    if not marker.exists() or marker.read_text().strip() != digest:
        print("正在安装控制台依赖（首次启动需要联网）……", flush=True)
        subprocess.run([str(python), "-m", "pip", "install", "-r", str(requirements)], check=True, cwd=ROOT)
        marker.write_text(digest)
    if args.setup_only:
        print("依赖安装完成。")
        return 0
    if args.real and not shutil.which("node"):
        parser.error("真实扫码登录需要 Node.js，请安装 Node.js 后重试")
    command = [str(python), "-m", "web", "--port", str(args.port)]
    if not args.real:
        command.append("--demo")
    if args.data_dir:
        command.extend(["--data-dir", str(args.data_dir.resolve())])
    url = f"http://127.0.0.1:{args.port}"
    process = subprocess.Popen(command, cwd=ROOT)
    stop = threading.Event()

    def open_when_ready():
        for _ in range(60):
            if stop.is_set() or process.poll() is not None:
                return
            try:
                with urllib.request.urlopen(url + "/.well-known/bifrost/ready", timeout=1) as response:
                    ready = response.status == 200
                if ready and not stop.is_set():
                    webbrowser.open(url)
                    return
            except OSError:
                pass
            stop.wait(0.5)

    if not args.no_browser:
        threading.Thread(target=open_when_ready, daemon=True).start()
    try:
        return process.wait()
    except KeyboardInterrupt:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        return 0
    finally:
        stop.set()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError, OSError) as error:
        print(f"启动失败：{error}。检查 Python、网络和端口后重试。", file=sys.stderr)
        raise SystemExit(1)
