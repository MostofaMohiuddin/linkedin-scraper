import asyncio
import csv
import json
import os
from playwright.async_api import async_playwright

MAX_SCROLLS = 5
QUERY_KEYWORD = "ceo" # Change this to the keyword you want to search for
LINKEDIN_USERNAME = "bexepe1823@sgatra.com"
LINKEDIN_PASSWORD = "9MHxv*pK5iu_$_p"

async def extract_post_data(page):
    await page.wait_for_selector("#fie-impression-container")
    posts = await page.query_selector_all("#fie-impression-container")
    all_posts_data = []

    for post in posts:
        try:
            # Extract author name, likes, reposts, comments, and post link
            await post.wait_for_selector(".update-components-actor__name .visually-hidden")
            author = await post.query_selector(".update-components-actor__name .visually-hidden")
            reaction_count = await post.query_selector(".social-details-social-counts__reactions-count")
            comment_and_repost_buttons = await post.query_selector_all(".social-details-social-counts__item ")
            comments = 0
            reposts = 0
            for button in comment_and_repost_buttons:
                text = await button.inner_text()
                if "comments" in text:
                    comments = text[:-9]
                elif "reposts" in text:
                    reposts = text[:-7]
            post_data = {
                "author": await author.inner_text(),
                "reactions": await reaction_count.inner_text() if reaction_count else 0,
                "reposts": reposts,
                "comments": comments,
            }

            all_posts_data.append(post_data)
        except Exception as e:
            print(f"Error extracting data for a post: {e}")
    
    return all_posts_data


async def save_cookies(page):
    cookies = await page.context.cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)

async def load_cookies(context):
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
        await context.add_cookies(cookies)

async def login(context):
    page = await context.new_page()
    await page.goto('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    await page.wait_for_selector('input[name="session_key"]')
    await page.fill('input[name="session_key"]', LINKEDIN_USERNAME)
    await page.fill('input[name="session_password"]', LINKEDIN_PASSWORD)
    await page.click('button[type="submit"]')
    await page.wait_for_timeout(2000)
    await save_cookies(page)
    await page.close()

async def initialize(pw):
    browser = await pw.chromium.launch(headless=True)
    context = await browser.new_context(viewport=None, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0")
    if os.path.exists('cookies.json'):
        await load_cookies(context)
    else:
        await login(context) 
    return context, browser


def write_to_csv(data):
    csv_file_path = "data.csv"
    # Check if the list is not empty
    if len(data) == 0:
        print("No data to write.")
        return

    # Writing the list of dictionaries to a CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        # Extract fieldnames from the keys of the first dictionary
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header (keys of the dictionary)
        writer.writeheader()
        
        # Write each dictionary as a row in the CSV
        writer.writerows(data)
    
    print(f"Data has been written to {csv_file_path}")


async def scrape_website():
    try:
        async with async_playwright() as p:
            context, browser = await initialize(p)
            page = await context.new_page()
        
            await page.goto(f"https://www.linkedin.com/feed/hashtag/?keywords={QUERY_KEYWORD}")
            await page.wait_for_timeout(2000)

            data = []
            for _ in range(MAX_SCROLLS):
                page_data = await extract_post_data(page)
                data.append(page_data)
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                
            print(data)
            print(len(data))

            await context.close()
            await browser.close()
        if data:
            write_to_csv(data)
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(scrape_website())


