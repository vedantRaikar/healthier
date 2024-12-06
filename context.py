import concurrent.futures
import requests
import tiktoken  # Install via `pip install tiktoken` if using OpenAI models
def fetch_wikipedia_context(keys, max_tokens = 128000 , max_workers=5, timeout=5):
    """
    Fetches Wikipedia article data for a list of search keys using multithreading,
    and ensures the combined context does not exceed the specified token limit.

    Args:
        keys (list): List of search terms (keys) for fetching Wikipedia articles.
        max_tokens (int): Maximum number of tokens allowed in the combined context.
        max_workers (int): Number of threads to use for concurrent processing.
        timeout (int): Timeout for each HTTP request in seconds.

    Returns:
        str: Truncated combined context within the specified token limit.
    """
    def get_wikipedia_articles(key):
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": key,
            "srlimit": 1
        }
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles for key '{key}': {e}")
            return None

    # Initialize the tokenizer for token counting
    tokenizer = tiktoken.get_encoding("cl100k_base")  # Use a tokenizer appropriate for your LLM

    # Container for article summaries
    summaries = []

    # Multithreading to process keys
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_key = {executor.submit(get_wikipedia_articles, key): key for key in keys}
        for future in concurrent.futures.as_completed(future_to_key):
            try:
                data = future.result()
                if data and "query" in data and "search" in data["query"]:
                    for article in data["query"]["search"]:
                        snippet = article.get("snippet", "").replace("<span class='searchmatch'>", "").replace("</span>", "")
                        summaries.append(snippet)
            except Exception as e:
                key = future_to_key[future]
                print(f"Error processing key '{key}': {e}")

    # Combine all summaries into a single context string
    combined_context = " ".join(summaries)

    # Count tokens and truncate if necessary
    tokens = tokenizer.encode(combined_context)
    if len(tokens) > max_tokens:
        truncated_context = tokenizer.decode(tokens[:max_tokens])  # Truncate to fit within max_tokens
    else:
        truncated_context = combined_context

    return truncated_context


