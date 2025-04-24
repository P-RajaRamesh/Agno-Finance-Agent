from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from textwrap import dedent
import streamlit as st
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state if needed
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False
if 'valid_api_key' not in st.session_state:
    st.session_state.valid_api_key = None

# Function to validate Gemini API key format
def is_valid_gemini_api_key(key):
    # Typical Gemini API keys start with "AI" followed by alphanumeric characters
    # This is a basic validation - adjust pattern as needed
    pattern = r'^[A-Za-z0-9_-]{25,}$'
    return bool(re.match(pattern, key))

# Function to test if the API key works
def verify_api_key(key):
    try:
        # Create a minimal test to verify the key works
        test_model = Gemini(id="gemini-2.0-flash-exp", api_key=key)
        # You might want to add a minimal test query here
        return True
    except Exception:
        return False

# Streamlit UI setup - only title is shown before API key validation
st.title("Financial Analysis Assistant")

# API key validation flow
api_key = os.getenv("GOOGLE_API_KEY")
needs_key = True

# Check if we have a valid key in session state
if st.session_state.valid_api_key:
    api_key = st.session_state.valid_api_key
    needs_key = False

# If key exists in environment but hasn't been verified
elif api_key and not st.session_state.api_key_set:
    if is_valid_gemini_api_key(api_key):
        st.session_state.valid_api_key = api_key
        st.session_state.api_key_set = True
        needs_key = False
    else:
        st.error("API key found in environment variables is invalid.")
        api_key = None

# If we need an API key, show the input form
if needs_key:
    st.warning("Valid Google Gemini API Key required to use this application.")
    
    with st.form("api_key_form"):
        user_api_key = st.text_input("Enter your Google Gemini API Key:", type="password", 
                                     help="Your API key should be at least 25 characters long.")
        submit_button = st.form_submit_button("Validate & Set API Key")
        
        if submit_button:
            if not user_api_key:
                st.error("Please enter an API key.")
            elif not is_valid_gemini_api_key(user_api_key):
                st.error("Invalid API key format. Please check your API key.")
            else:
                # Format looks valid, now test if it works
                with st.spinner("Validating API key..."):
                    if verify_api_key(user_api_key):
                        os.environ["GOOGLE_API_KEY"] = user_api_key
                        st.session_state.valid_api_key = user_api_key
                        st.session_state.api_key_set = True
                        st.success("API Key validated and set successfully!")
                        st.rerun()
                    else:
                        st.error("API key validation failed. Please check your key.")
    
    # Stop execution until a valid API key is provided
    st.stop()

# Only show the main app if API key is set and valid
# Sidebar content for user guidance
with st.sidebar:
    st.header("📘 How to Use")
    st.markdown(
        """
        This AI-powered **Financial Analysis Assistant** helps you analyze stocks using live market data.  
        Simply:
        1. Enter a **stock ticker symbol** (e.g., `AAPL`, `GOOGL`, `TSLA`)
        2. Click **"Analyze"**
        3. Get a detailed report with 📈 trends, 🧾 financials, and 🔍 analyst insights.

        ---
        """
    )

    st.subheader("💡 Examples")
    st.markdown(
        """
        - `AAPL` – Apple Inc.  
        - `MSFT` – Microsoft Corp  
        - `GOOGL` – Alphabet Inc  
        - `TSLA` – Tesla Inc  
        - `NFLX` – Netflix Inc  
        """
    )

    st.subheader("🔐 Notes")
    st.markdown(
        """
        - Data is pulled live using [Yahoo Finance](https://finance.yahoo.com).
        - Powered by **Gemini** via AGNO Agent framework.
        - Analysis may take a moment to complete.
        """
    )

    # Add option to reset/change API key if needed
    if st.button("Change API Key"):
        st.session_state.api_key_set = False
        st.session_state.valid_api_key = None
        st.rerun()

    st.markdown("---")

# Inject custom CSS to create a scrollable area
st.markdown("""
    <style>
    .scrollable {
        height: 400px;
        overflow-y: scroll;
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# Define the financial analysis agent using the validated API key
finance_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", api_key=st.session_state.valid_api_key),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=dedent("""\
        You are a seasoned Wall Street analyst with deep expertise in market analysis! 📊
        Follow these steps for comprehensive financial analysis:
        1. Market Overview
           - Latest stock price
           - 52-week high and low
        2. Financial Deep Dive
           - Key metrics (P/E, Market Cap, EPS)
        3. Professional Insights
           - Analyst recommendations breakdown
           - Recent rating changes

        4. Market Context
           - Industry trends and positioning
           - Competitive analysis
           - Market sentiment indicators

        Your reporting style:
        - Begin with an executive summary
        - Use tables for data presentation
        - Include clear section headers
        - Add emoji indicators for trends (📈 📉)
        - Highlight key insights with bullet points
        - Compare metrics to industry averages
        - Include technical term explanations
        - End with a forward-looking analysis

        Risk Disclosure:
        - Always highlight potential risk factors
        - Note market uncertainties
        - Mention relevant regulatory concerns
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

# Input field for the stock ticker
ticker = st.text_input("Enter the stock ticker symbol (e.g., AAPL):")

# Button for triggering analysis
if st.button("Analyze"):
    if ticker:
        query = f"What's the latest news and financial performance of {ticker}?"
        try:
            with st.spinner("Analyzing..."):
                response = finance_agent.run(query, stream=False)
            if response and response.content:
                st.subheader("Analysis Report:")
                # Use custom scrollable div for the response content
                st.markdown(f'<div class="scrollable">{response.content}</div>', unsafe_allow_html=True)
            else:
                st.error("No response received from the agent.")
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            # If the error might be related to an invalid API key, offer to reset
            if "authentication" in str(e).lower() or "api key" in str(e).lower() or "unauthorized" in str(e).lower():
                st.error("This may be an API key issue. Please try resetting your API key.")
                if st.button("Reset API Key"):
                    st.session_state.api_key_set = False
                    st.session_state.valid_api_key = None
                    st.rerun()
    else:
        st.error("Please enter a stock ticker symbol.")
