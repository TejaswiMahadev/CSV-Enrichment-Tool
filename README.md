# AI-Powered CSV Analysis & Enrichment Tool

## Overview
The **AI-Powered CSV Analysis & Enrichment Tool** is a web application built with Streamlit that helps users analyze, enrich, and interact with CSV data. This tool leverages AI models for generating insights, making enrichment suggestions, and providing a chat interface for data-specific queries. Additionally, it incorporates a web search feature for external data enrichment using SerpAPI.

## Features
- **Data Overview**: Display basic statistics and missing values in the dataset.
- **AI Analysis**: Generate insights and visualizations using AI models.
- **Enrichment Suggestions**: AI-powered suggestions for improving and enriching the dataset.
- **Visualizations**: Create scatter plots, bar charts, line charts, and box plots dynamically.
- **Chat with CSV**: Interact with your data using natural language questions.
- **Web Search**: Perform real-time web searches for additional context and information.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Streamlit
- **APIs and SDKs**:
  - **Google Generative AI (Gemini) SDK**
  - **SerpAPI** for web search
- **Libraries**:
  - `pandas` for data manipulation
  - `plotly` for visualizations
  - `dotenv` for environment variable management

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/TejaswiMahadev/CSV-Enrichment-Tool.git
    cd CSV-Enrichment-Tool
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
   - Create a `.env` file and add your API keys:
     ```ini
     GOOGLE_API_KEY=your_google_api_key_here
     SERPAPI_KEY=your_serpapi_key_here
     ```

## How to Run

1. **Run the Streamlit app**:
    ```bash
    streamlit run main.py
    ```

2. **Navigate to** `http://localhost:8501` in your web browser.

## Deployment
The app can be deployed on platforms like [Render](https://render.com/) or [Heroku](https://www.heroku.com/). Make sure to include environment variables as part of the deployment configuration.

## Usage
1. **Upload CSV**: Upload a CSV file to start analyzing.
2. **Navigate Using Sidebar**: Use the sidebar to explore different sections like data overview, AI analysis, visualizations, etc.
3. **Interact with Data**: Ask questions or run a web search to enrich your dataset.

## Example Screenshots
![Data Overview](screenshots/data_overview.png)
*Screenshot of the Data Overview page.*

![AI Analysis](screenshots/ai_analysis.png)
*Screenshot of the AI Analysis page.*

## Known Issues
- Ensure the API keys are correctly set up in the environment for proper functionality.
- Some features may depend on the availability of external APIs.

## License
This project is licensed under the MIT License.

## Contact
**Author**: Tejaswi Mahadev  
**Email**: [your-email@example.com](mailto:your-email@example.com)  
**LinkedIn**: [Your LinkedIn](https://www.linkedin.com/in/your-profile)

---

Feel free to customize the README further to suit your project's needs, including adding more screenshots or sections as required.
