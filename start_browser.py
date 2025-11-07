"""
Helper script to automatically open the browser when the app starts
"""
import time
import webbrowser
import requests
import sys

def wait_for_server(url, timeout=30, check_interval=0.5):
    """Wait for the server to be ready"""
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url + '/api/health', timeout=1)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass

        time.sleep(check_interval)

    return False


def open_browser():
    """Open the browser to the app URL"""
    url = "http://localhost:5000"

    print("Waiting for server to start...")

    if wait_for_server(url):
        print("Server is ready! Opening browser...")
        time.sleep(0.5)  # Small delay to ensure server is fully ready
        webbrowser.open(url)
        print(f"Browser opened to {url}")
    else:
        print("Server did not start in time. Please open your browser manually to:")
        print(url)


if __name__ == "__main__":
    open_browser()
