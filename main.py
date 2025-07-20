import streamlit as st
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_ollama
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

st.set_page_config(layout="wide")
st.title("AI Web Scraper and Parser (Basic Proxy)")

st.markdown(
    """
    This application allows you to scrape content from a website using a basic Selenium setup
    (optional basic proxy support) and then extract specific information from the scraped content
    using an Ollama LLM.
    """
)

url = st.text_input("Enter a Website URL to Scrape:", help="e.g., https://example.com")

if st.button("Scrape Site", key="scrape_button"): # Added unique key
    if not url:
        st.error("Please enter a URL to scrape.")
    else:
        with st.spinner("Scraping the website... This may take a moment due to browser launch."):
            scraped_html = scrape_website(url)

        if scraped_html:
            body_content = extract_body_content(scraped_html)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content
            st.success("Website scraped successfully!")

            with st.expander("View Cleaned DOM Content"):
                st.text_area("Cleaned DOM Content", cleaned_content, height=300, disabled=True)
        else:
            st.error("Failed to scrape the website. Please check the URL or try again. Note: Authenticated proxies are not supported in this version.")

if "dom_content" in st.session_state and st.session_state.dom_content:
    st.subheader("Parse Scraped Content")
    parse_description = st.text_area(
        "Describe what specific information you want to parse from the content (e.g., 'the main article title', 'all product names and their prices'):",
        help="Be as specific as possible for better results."
    )

    # Use a single button and handle the logic for parse_description inside the if block
    if st.button("Parse Content", key="parse_button"): # Added unique key
        if not parse_description:
            st.error("Please provide a description of what you want to parse.")
        else:
            with st.spinner("Parsing the content with Ollama..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)

                if parsed_result.strip():
                    st.success("Content parsed successfully!")
                    st.text_area("Parsed Result", parsed_result, height=200, disabled=True)
                else:
                    st.warning("Ollama did not return any specific information based on your description. Try refining your description.")

elif "dom_content" in st.session_state and not st.session_state.dom_content:
    st.info("Scraping resulted in no content or an error. Please re-scrape with a valid URL.")
