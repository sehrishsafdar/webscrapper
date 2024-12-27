import requests

def load_latest_posts(offset, tag=0):
    # Define the URL and data to send in the POST request
    url = 'https://www.geo.tv/category/geo-fact-check/more_news'
    data = {
        'offset': offset,  
        'tag': tag         
    }

    # Send the POST request
    try:
        response = requests.post(url, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            response_text = response.text  
            if response_text.strip():  
                return response_text, True  
            else:
                return "", False  
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return "", False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "", False


def scrape_all_pages():
    """
    Crawls and collects posts from all pages.
    """
    offset = 2 
    tag = 0  
    all_pages_posts = []

    while True:
        print(f"Fetching posts for offset: {offset}...")
        html_response, has_more = load_latest_posts(offset, tag)

        if html_response:
            # Append the raw HTML response to the list (process it later as needed)
            all_pages_posts.append(html_response)
            print(f"Offset {offset} extracted successfully!")
        else:
            print("No more posts to fetch.")
            break

        offset += 1
        break
    print('--- Data crawled from all pages! ---')
    return all_pages_posts

'''
# Example usage
if _name_ == "_main_":
    all_posts = scrape_all_pages()
    print(f"Total pages fetched: {len(all_posts)}")
'''