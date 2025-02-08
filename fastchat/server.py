import subprocess
import threading
import argparse
import time
import os

def run_controller():
    """Chạy controller để điều khiển hệ thống"""
    subprocess.run(["python3", "-m", "fastchat.serve.controller", "--host", "127.0.0.1"])

def run_model_worker():
    """Chạy model worker để xử lý các tác vụ của mô hình"""
    subprocess.run(["python3", "-m", "fastchat.serve.model_worker", "--host", "127.0.0.1", "--controller-address", "http://127.0.0.1:21001", "--model-path", "lmsys/vicuna-7b-v1.5"])

def run_api_server(api_port):

    subprocess.run(["python3", "-m", "fastchat.serve.openai_api_server", "--host", "127.0.0.1", "--controller-address", "http://127.0.0.1:21001", "--port", str(api_port)])


def start_fastchat_server(api_port=8000):
    """Khởi động server với các dịch vụ cần thiết"""
    try:
        # Start controller thread
        controller_thread = threading.Thread(target=run_controller, daemon=True)
        controller_thread.start()
        time.sleep(2)  # Wait for the controller to start

        # Start model worker thread
        model_worker_thread = threading.Thread(target=run_model_worker, daemon=True)
        model_worker_thread.start()
        time.sleep(2)  # Wait for the model worker to start

        # Start API server thread
        api_server_thread = threading.Thread(target=run_api_server, args=(api_port,), daemon=True)
        api_server_thread.start()

        # Giữ chương trình chính tiếp tục chạy
        api_server_thread.join()
    except Exception as e:
        print(f"Lỗi khi khởi động FastChat server: {e}")

def main():
    """Chạy server với các tham số đầu vào từ dòng lệnh"""
    parser = argparse.ArgumentParser(description="FastChat Server")
    parser.add_argument("--api-port", type=int, default=8000, help="API server port")

    args = parser.parse_args()


    # Start server 
    start_fastchat_server(api_port=args.api_port)

if __name__ == "__main__":
    main()
