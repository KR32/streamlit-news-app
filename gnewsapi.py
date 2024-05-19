import requests
import streamlit as st
from PIL import Image

BASE_URL = "https://gnews.io/api/v4"
API_KEY = "<your API_KEY here>"

# Fetch tech news using GNews API
def fetch_tech_news(search_query, language, page):
    url = f"{BASE_URL}/search?q={search_query.strip()}&lang={language}&token={API_KEY}&page={page}"
    response = requests.get(url)

    if response.status_code != 200:
        print(response.json())
        st.error("Error fetching news. Please try again later.")
        return [], 0

    try:
        news_data = response.json()
    except ValueError:
        st.error("Error parsing news data. Please try again later.")
        return [], 0

    articles = news_data.get("articles", [])
    total_articles = news_data.get("totalArticles", 0)

    tech_news = []
    for article in articles:
        title = article.get("title", "")
        url = article.get("url", "")
        image_url = article.get("image", "")

        tech_news.append((title, url, image_url))

    return tech_news, total_articles

# Display tech news with thumbnails and usage information
def display_tech_news(tech_news, total_articles):
    st.title("Tech News")
    st.write(f"Total Articles: {total_articles}")

    for i, (title, url, image_url) in enumerate(tech_news, start=1):
        st.markdown(f"## Article {i}")
        st.write(f"[{title}]({url})")

        if image_url:
            try:
                image = Image.open(requests.get(image_url, stream=True).raw)
                st.image(image, use_column_width=True)
            except Exception as e:
                st.write("Image unavailable.")
        else:
            st.write("No image available.")

        st.write("---")

# Streamlit app
def main():
    st.header("Tech News App")

    col1, col2, col3 = st.columns(3)

    with col1:
        search_query = st.text_input("Search for tech news:")
        if not search_query:
            search_query = "Technology"

    with col2:
        language = st.selectbox("Select language:", ["en", "de", "fr", "es", "it"])

    with col3:
        page = st.number_input("Page number:", min_value=1, step=1, value=1, format="%d")

    with st.spinner("Fetching news..."):
        tech_news, total_articles = fetch_tech_news(search_query, language, page)

    display_tech_news(tech_news, total_articles)

if __name__ == "__main__":
    main()
