import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_proxies(file_path):
    """
    Load proxies from a text file.

    :param file_path: Path to the file containing proxies, one per line.
    :return: A list of proxies.
    """
    try:
        with open(file_path, 'r') as file:
            proxy_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Proxy file not found at {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred while loading proxies: {e}")
        return []

    return proxy_list


def test_proxy(proxy):
    """
    Test if a proxy can successfully connect to TikTok.

    :param proxy: A proxy URL to test.
    :return: The proxy URL if successful, otherwise None.
    """
    url = "https://www.tiktok.com/"
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working")
            return proxy
        else:
            print(f"Proxy {proxy} failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Proxy {proxy} failed: {e}")
    return None


def test_proxies_concurrently(proxy_list, max_workers=10):
    """
    Test proxies concurrently to improve performance.

    :param proxy_list: A list of proxies to test.
    :param max_workers: The maximum number of threads to use.
    :return: A list of working proxies.
    """
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(test_proxy, proxy): proxy for proxy in proxy_list}
        for future in as_completed(futures):
            proxy = future.result()
            if proxy:
                valid_proxies.append(proxy)
    return valid_proxies


# Example usage: Load and test proxies from a file
if __name__ == "__main__":
    proxy_file_path = 'proxies.txt'
    proxies = load_proxies(proxy_file_path)
    if proxies:
        working_proxies = test_proxies_concurrently(proxies)
        print(f"Working proxies: {working_proxies}")
