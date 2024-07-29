from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from bs4 import BeautifulSoup

# Function to summarize article


def summarize_article(article_text, max_length=150):
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer.encode("summarize: " + article_text,
                              return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_length, min_length=50,
                                 length_penalty=2.0, num_beams=4, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to scrape content of the aricle


def scrape_webpage(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text(separator='\n', strip=True)
        return all_text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    # Sample URL for Testing The Script
    webpage_url = "https://medium.com/pythoneers/17-mindblowing-python-automation-scripts-i-use-everyday-523fb1eb9284"
    webpage_text = scrape_webpage(webpage_url)

    if webpage_text:
        summary = summarize_article(webpage_text)
        print("\nSummarized Article:")
        print(summary)
    else:
        print("Webpage scraping failed.")
