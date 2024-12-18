import requests
from utils import string_util
def load_latest_posts(page):
    # Define the URL and data to send in the POST request
    url = 'https://www.sochfactcheck.com/wp-admin/admin-ajax.php'
    data = {
        'action': 'load_latest_posts',
        'page': page
    }

    # Send the POST request
    try:
        response = requests.post(url, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()  # Parse the response JSON

            # Check if the response indicates success
            if response_data.get('success'):
                # Process the posts and handle the button (in a script context this would be UI interaction)
                posts = response_data.get('data', {}).get('posts', [])
                has_more = response_data.get('data', {}).get('has_more', False)

                return posts, has_more
                
            else:
                print("Error: Response does not indicate success.")
                return False
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


def scrape_all_pages():
    
    page = 1
    
    all_pages_posts = []

    while True:
        posts, has_more = load_latest_posts(page)

        all_pages_posts.append(posts)

        if not has_more:
            break

        print(f'Page {page} extracted successfully!')

        page += 1
        #if page == 30:
        break

    print('--- Data crawled from all pages! ---')
    return all_pages_posts