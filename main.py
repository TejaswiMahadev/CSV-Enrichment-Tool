import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from google import genai
from google.genai import types
from typing import List, Dict
import plotly.express as px
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

# Load environment variables
load_dotenv()

# Get API key from environment or Streamlit secrets
def get_api_key():
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        if 'GOOGLE_API_KEY' in st.secrets:
            api_key = st.secrets['GOOGLE_API_KEY']

    serp_api_key = os.getenv('SERP_API_KEY')
    if not serp_api_key:
        if 'SERP_API_KEY' in st.secrets:
            serp_api_key = st.secrets['SERP_API_KEY']
    return api_key , serp_api_key
    

class CSVEnrichmentAgent:
    def __init__(self):
        google_key, serp_key = get_api_keys()

        if not google_key:
            st.error("Google API Key not found")
            st.stop()

        self.client = genai.Client(api_key=google_key)
        self.serp_key = serp_key

    def analyze_columns(self, columns: List[str]) -> str:
        prompt = f"""
        Analyze these dataset columns:
        {columns}

        Respond with:
        1. Data Overview
        2. Key Insights
        3. Suggested Visualizations
        """

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=600
            )
        )
        return response.text

    def suggest_enrichments(self, columns: List[str], sample_data: str) -> str:
        prompt = f"""
        Dataset Columns:
        {columns}

        Sample Rows:
        {sample_data}

        Suggest valuable enrichment opportunities.
        """

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=600
            )
        )
        return response.text

    def chat_with_csv(self, query: str, df: pd.DataFrame) -> str:
        prompt = f"""
        You are a data analyst.

        Sample Data:
        {df.head().to_string()}

        Question:
        {query}
        """

        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=500
            )
        )
        return response.text

    def generate_insights(self, df: pd.DataFrame) -> Dict:
        return {
            "statistics": df.describe(include="all"),
            "missing_values": df.isnull().sum(),
            "row_count": len(df),
            "column_count": len(df.columns)
        }

    def web_search(self, query: str):
        if not self.serp_key:
            return []

        search = GoogleSearch({
            "q": query,
            "api_key": self.serp_key
        })

        results = search.get_dict()
        return [
            {
                "title": r.get("title"),
                "snippet": r.get("snippet"),
                "link": r.get("link")
            }
            for r in results.get("organic_results", [])
        ]


def main():
    st.set_page_config(page_title="AI CSV Enrichment Tool", layout="wide")
    st.title("🤖 AI-Powered CSV Analysis & Enrichment")
    
    # API Key input in sidebar if not found in environment
    if not get_api_key():
        with st.sidebar:
            api_key = st.text_input("Enter your Google API Key", type="password")
            if api_key:
                os.environ['GOOGLE_API_KEY'] = api_key
            else:
                st.error("Please enter your Google API Key to continue")
                st.stop()
    
    try:
        # Initialize agent
        agent = CSVEnrichmentAgent()
        
        # File upload
        uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
        
        if uploaded_file is not None:
            # Read and display data
            df = pd.read_csv(uploaded_file)
            
            # Sidebar for navigation
            with st.sidebar:
                page =  option_menu(
                    "Navigation",
                    ["Data Overview", "AI Analysis", "Enrichment Suggestions", "Visualizations", "Chat with CSV", "Web Search"],
                    icons=["bar-chart", "robot", "stars", "pie-chart", "chat-left-dots", "search"],
                    menu_icon="menu-app",
                    default_index=0,
                    styles={
                        "container": {"padding": "5px", "background-color": "#000000"},
                        "icon": {"color": "white", "font-size": "18px"},
                        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                        "nav-link-selected": {"background-color": "blue"},
                    }
                )
            
            if page == "Data Overview":
                st.header("📊 Data Overview")
                st.write("First few rows of your data:")
                st.dataframe(df.head())
                
                # Display basic insights
                insights = agent.generate_insights(df)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Rows", insights["row_count"])
                    st.metric("Total Columns", insights["column_count"])
                
                st.subheader("Missing Values Analysis")
                st.bar_chart(insights["missing_values"])
                
            elif page == "AI Analysis":
                st.header("🧠 AI Analysis")
                
                # Get AI analysis of columns
                with st.spinner("Generating AI analysis..."):
                    analysis = agent.analyze_columns(df.columns.tolist())
                    st.write(analysis)
                
            elif page == "Enrichment Suggestions":
                st.header("✨ Enrichment Suggestions")
                
                # Get enrichment suggestions
                with st.spinner("Generating enrichment suggestions..."):
                    sample_data = df.head().to_string()
                    suggestions = agent.suggest_enrichments(df.columns.tolist(), sample_data)
                    st.write(suggestions)
                
            elif page == "Visualizations":
                st.header("📈 Visualizations")
                
                # Dynamic visualization options based on data types
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                categorical_cols = df.select_dtypes(include=['object']).columns
                
                # Visualization type selector
                viz_type = st.selectbox(
                    "Choose visualization type",
                    ["Scatter Plot", "Bar Chart", "Line Chart", "Box Plot"]
                )
                
                if viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
                    x_col = st.selectbox("Select X axis", numeric_cols, key="scatter_x")
                    y_col = st.selectbox("Select Y axis", numeric_cols, key="scatter_y")
                    fig = px.scatter(df, x=x_col, y=y_col)
                    st.plotly_chart(fig)
                    
                elif viz_type == "Bar Chart" and len(categorical_cols) > 0:
                    x_col = st.selectbox("Select category", categorical_cols)
                    if len(numeric_cols) > 0:
                        y_col = st.selectbox("Select value", numeric_cols)
                        fig = px.bar(df, x=x_col, y=y_col)
                        st.plotly_chart(fig)
                        
                elif viz_type == "Line Chart" and len(numeric_cols) > 0:
                    y_col = st.selectbox("Select value", numeric_cols)
                    fig = px.line(df, y=y_col)
                    st.plotly_chart(fig)
                    
                elif viz_type == "Box Plot" and len(numeric_cols) > 0:
                    y_col = st.selectbox("Select value", numeric_cols)
                    if len(categorical_cols) > 0:
                        x_col = st.selectbox("Select category (optional)", categorical_cols)
                        fig = px.box(df, x=x_col, y=y_col)
                    else:
                        fig = px.box(df, y=y_col)
                    st.plotly_chart(fig)
                    
            elif page == "Chat with CSV":
                st.header("💬 Chat with CSV")
                
                # Allow user to enter a question
                query = st.text_input("Ask a question about your data:")
                
                if query:
                    # Get response from AI model
                    with st.spinner("Generating response..."):
                        response = agent.chat_with_csv(query, df)
                        st.write(response)
            
            elif page == "Web Search":
                st.header("🔍 Dynamic Web Search")
                
                # Input prompt for web search
                query = st.text_input("Enter your search query:")
                
                if query:
                    st.write(f"Searching for: {query}")
                    with st.spinner("Searching..."):
                        results = agent.web_search(query)
                        if results:
                            st.subheader("Search Results:")
                            for result in results:
                                st.markdown(f"**Title:** {result['title']}")
                                st.markdown(f"**Snippet:** {result['snippet']}")
                                st.markdown(f"[Link]({result['link']})")
                        else:
                            st.write("No results found.")
                    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your API keys and file format.")

if __name__ == "__main__":
    main()
