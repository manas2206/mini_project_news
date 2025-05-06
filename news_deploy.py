import streamlit as st
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import webbrowser

# NewsAPI Key
API_KEY = '1b32428f7e804339b9ffe14969da7877'

# Default fallback image URL
DEFAULT_IMAGE_URL = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'

# Fetch news articles
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []

# Load image safely with fallback
def load_image(url):
    try:
        response = requests.get(url, timeout=5)
        image = Image.open(BytesIO(response.content))
        return image
    except (requests.exceptions.RequestException, UnidentifiedImageError, OSError):
        # Try loading the default image
        try:
            fallback_response = requests.get(DEFAULT_IMAGE_URL)
            return Image.open(BytesIO(fallback_response.content))
        except:
            return None

# Streamlit page config
st.set_page_config(page_title="Mera News App", layout="centered")
st.markdown("<h1 style='text-align: center;'>🗞️ Mera News App</h1>", unsafe_allow_html=True)
st.markdown("---")

# Loading spinner
with st.spinner("Fetching the latest news..."):
    articles = get_news()

# Display news articles
for index, article in enumerate(articles):
    st.markdown(f"### {article.get('title', 'No Title')}")

    # Image display with fallback
    image_url = article.get('urlToImage') or DEFAULT_IMAGE_URL
    image = load_image(image_url)
    if image:
        st.image(image, use_container_width=True)
    else:
        st.warning("⚠️ Image could not be loaded.")

    # Description
    st.write(article.get('description', 'No description available.'))

    # Button to read more
    if st.button(f"🔗 Read Full Article {index + 1}"):
        webbrowser.open_new_tab(article.get('url', '#'))

    st.markdown("---")

# Footer
st.markdown("<footer style='text-align: center; padding-top: 20px;'>Made By: Manas Pandey </footer>", unsafe_allow_html=True)
