import requests
import streamlit as st
from PIL import Image
from newsapi import NewsApiClient

# Initialize News API client
newsapi = NewsApiClient(api_key="<your API_KEY here>")

# Fetch news articles by topic and page
def fetch_news_articles(topic, page):
    if topic:
        articles = newsapi.get_everything(q=topic, language='en', sort_by='relevancy', page=page, page_size=10)
    else:
        companies = ['OpenAI', 'Microsoft', 'Apple', 'Google', 'Tesla', 'Amazon', 'Facebook']
        all_articles = []
        for company in companies:
            articles = newsapi.get_everything(q=company, language='en', sort_by='publishedAt', page=page, page_size=2)
            all_articles.extend(articles['articles'])
        articles = {'articles': all_articles}

    return articles['articles']

# Display news articles
def display_news_articles(articles):
    st.title("News Articles")

    if not articles:
        st.write("No articles found.")
        return

    for i, article in enumerate(articles, start=1):
        st.markdown(f"##  {i}) {article['title']}")

        if article['urlToImage']:
            try:
                image = Image.open(requests.get(article['urlToImage'], stream=True).raw)
                st.image(image, use_column_width=True, caption=f"Image source: {article['source']['name']}")
                st.markdown(f"[Open Article]({article['url']})")
            except Exception as e:
                st.write("Image unavailable.")
        else:
            st.write("No image available.")

        st.write(f"Source: [{article['source']['name']}]({article['url']})")
        st.write(f"Published At: {article['publishedAt']}")
        st.write("---")

# Streamlit app
def main():

    # Static Header
    with st.container():
        st.title("News App")
        st.markdown("---")

    # Fancy search bar in the sidebar
    st.sidebar.subheader("Search News")
    search_topic = st.sidebar.text_input("Enter a topic")

    # Pagination button
    page_no = st.sidebar.number_input("Page number:", min_value=1, step=1, value=1, format="%d")

    # search_topic = st.text_input("Search for news by topic:")
    # page_no = st.number_input("Page number:", min_value=1, step=1, value=1, format="%d")

    news_articles = fetch_news_articles(search_topic, page_no)
    display_news_articles(news_articles)

if __name__ == "__main__":
    main()
