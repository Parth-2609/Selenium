# Web Scraping with Selenium

This project demonstrates web scraping using Selenium in Python to extract data from a website employing both infinite scroll and pagination. The scraped data includes information about 2,535 companies, such as their **Name**, **Industry**, **Number of Employees**, and **Certification Period**, all stored in an Excel file.

## Project Overview

### Problem Statement
The website presented two challenges:
- It used **infinite scroll** and **pagination**, making it harder to locate all data.
- Clicking the "Next Page" button did not change the website URL, as it relied on **JavaScript rendering** to simulate a multi-page structure.

### Solution
Using **Selenium**, a powerful tool for browser automation, I navigated the website, triggered JavaScript events, and successfully extracted all required data.

## Features
- Automates navigation through infinite scroll and JavaScript-based pagination.
- Scrapes detailed information about companies.
- Stores the extracted data into an Excel file for easy access and analysis.

## Technology Stack
- **Programming Language:** Python
- **Web Scraping Tool:** Selenium
- **Data Storage:** Excel (using pandas)
- **Browser:** Chrome (with ChromeDriver)

## Setup and Installation

### Prerequisites
1. Install Python (>= 3.7).
2. Install Google Chrome and download the matching version of [ChromeDriver](https://chromedriver.chromium.org/downloads).
3. Install the following Python packages:
   ```
   pip install selenium pandas
   ```

### Clone the Repository
```
git clone <repository-link>
cd <repository-folder>
```

## Challenges Faced
- **Infinite Scroll and Pagination:** Handling dynamic content loading required a combination of JavaScript execution and scroll simulation.
- **Static URL:** The lack of URL changes forced reliance on Selenium's DOM manipulation capabilities.
- **Trial and Error:** As a beginner, I faced multiple hurdles, but persistence and debugging led to success.

## Data Extracted
- **Company Name**
- **Industry**
- **Number of Employees**
- **Certification Period**

### Sample Output
| Name             | Industry       | Employees | Certification Period |
|------------------|----------------|-----------|-----------------------|
| Company A        | Technology     | 500       | Jan 2024 - Dec 2024   |
| Company B        | Healthcare     | 200       | Apr 2023 - Mar 2024   |
| ...              | ...            | ...       | ...                   |

## Lessons Learned
- **Understanding Selenium:** Starting from scratch, I learned how to interact with web elements, handle JavaScript, and navigate complex web structures.
- **Problem-Solving:** Tackling infinite scroll and pagination deepened my understanding of dynamic web scraping.

#### Contributions are welcome! If you have ideas for improvement or encounter any issues, feel free to open a pull request or create an issue.
