# LinkedIn Scraper

This project is a LinkedIn hashtag scraper that uses [Playwright](https://playwright.dev/python/) to automate the process of fetching post data from LinkedIn hashtags. The script can extract author names, reactions, reposts, comments, and more for a given keyword and save the results to a CSV file.

## Features

- Scrapes posts from LinkedIn hashtags for a given keyword.
- Extracts author names, number of reactions, comments, reposts, and more.
- Saves extracted data into a CSV file.
- Uses cookies to avoid re-logging in on every run.

## Requirements

- Python 3.11 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- LinkedIn account credentials for login (set in the script for automated login).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MostofaMohiuddin/linkedin-scraper.git
   cd linkedin-scraper
   ```

2. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Install Playwright browser dependencies:

   ```bash
   poetry run playwright install
   ```

## Usage

1. Set your LinkedIn credentials in the `login` function:

   ```python
   await page.fill('input[name="session_key"]', "<your-email>")
   await page.fill('input[name="session_password"]', "<your-password>")
   ```

2. Run the script:

   ```bash
   poetry run python scrape.py
   ```

### Script Flow

- The script will first check if a `cookies.json` file exists. If the file exists, it will use the cookies to avoid re-logging in.
- If no cookies are found, it will log in using your credentials and save the cookies for future use.
- The script will scrape data for the specified keyword and extract post data from the hashtag feed.
- The data is stored in a CSV file called `data.csv`.

## Customization

- **Changing the Keyword**: Update the `QUERY_KEYWORD` variable to scrape for a different hashtag.

  ```python
  QUERY_KEYWORD = "your-keyword"
  ```

- **Number of Scrolls**: Modify `MAX_SCROLLS` to control how much content the script scrolls through.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
