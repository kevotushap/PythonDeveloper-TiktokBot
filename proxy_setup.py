import requests

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines() if line.strip()]
    return proxies

def test_proxy(proxy):
    url = "https://www.tiktok.com/"
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working")
        else:
            print(f"Proxy {proxy} failed with status code {response.status_code}")
    except Exception as e:
        print(f"Proxy {proxy} failed: {e}")

# Example usage: Test proxies from a file
if __name__ == "__main__":
    proxy_file_path = 'proxies.txt'
    proxies = load_proxies(proxy_file_path)
    for proxy in proxies:
        test_proxy(proxy)
