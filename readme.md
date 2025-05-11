# LLM-Based RAG System

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system using a Large Language Model (LLM). The system retrieves content from the internet based on user queries, processes it to extract meaningful text, and generates contextual responses using an LLM. It consists of a Flask backend for handling API calls, content retrieval, and LLM integration, and a Streamlit front-end for user interaction. LangChain is used to add conversational memory, enabling follow-up questions (bonus feature).

**Note**: Only packages listed in `requirements.txt` or similar alternatives with equivalent functionality are used.

## Process Overview

1. **User Input via Streamlit Interface**:

    - Users input queries through a Streamlit-based front-end interface.

2. **Query Sent to Flask Backend**:

    - The query is sent to the Flask backend via a POST API call.

3. **Internet Search and Article Scraping**:

    - The backend uses SerpAPI to search the internet and retrieve the top 5 relevant web pages.
    - Content (headings and paragraphs) is scraped using WebBaseLoader, excluding non-essential elements like images and advertisements.

4. **Content Processing**:

    - Scraped content is cleaned and formatted into a coherent input for the LLM, combining the user query and extracted text.

5. **LLM Response Generation**:

    - The processed content is passed to a simulated ChatGoogleGenerativeAI LLM via LangChain, which maintains conversational context.
    - The LLM generates a response based on the query and context.

6. **Response Sent Back to Streamlit Interface**:
    - The Flask backend returns the LLM-generated response to the Streamlit front-end, where it is displayed to the user.

## What We Expect

We expect you to:

-   Understand and implement the system components (web search, scraping, LLM integration, and front-end).
-   Demonstrate proficiency with the provided tools (Flask, Streamlit, LangChain, etc.).
-   Deliver a functional solution that meets the requirements.
-   Bonus: Implement conversational memory using LangChain for a chatbot-like experience.

## Prerequisites

-   Python 3.8 or higher
-   SerpAPI key (sign up at [serpapi.com](https://serpapi.com))
-   GOOGLE API key (simulated here; replace with actual key from [google/api](https://ai.google.dev/gemini-api/docs/api-key))

## Setup Instructions

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/AkashKoley012/RAG-Search.git
cd RAG-Search
```

Or download and extract the project zip file.

### Step 2: Set Up a Virtual Environment

Use `venv` or `conda` to create an isolated environment.

#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

#### Using `conda`

```bash
conda create --name rag_env python=3.8
conda activate rag_env
```

### Step 3: Install Requirements

Install dependencies from the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```
SERPAPI_KEY=your_serpapi_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

**Note**: Do not include `.env` in version control. Replace `your_serpapi_key_here` with a valid SerpAPI key and `your_grok_api_key_here` with a Grok 3 API key (simulated for this project).

### Step 5: Run the Flask Backend

Navigate to the `flask_app` directory and start the Flask server:

```bash
cd flask_app
python app.py
```

The backend will run at `http://localhost:5000`.

### Step 6: Run the Streamlit Frontend

In a new terminal, navigate to the `streamlit_app` directory and start the Streamlit app:

```bash
cd streamlit_app
streamlit run app.py
```

### Step 7: Open the Application

Open a web browser and go to `http://localhost:8501`. Enter a query (e.g., "What is the capital of France?") and verify the response. Test conversational memory by asking follow-up questions (e.g., "Tell me more about it").

## Project Structure

-   **flask_app/**: Backend Flask API and utility functions.
    -   `app.py`: Main Flask application with endpoints for query processing, web search, scraping, and LLM integration.
-   **streamlit_app/**: Streamlit front-end code.
    -   `app.py`: Streamlit application for user query input and response display.
-   **.env**: Stores API keys (not tracked in version control).
-   **requirements.txt**: Lists project dependencies.
-   **README.md**: This documentation.

## Task Instructions for Candidates

You are required to:

1. Implement functionality to fetch web content, process it, and generate LLM responses using the provided APIs.
2. Integrate SerpAPI for web search and BeautifulSoup for content scraping in the Flask backend.
3. Use LangChain for conversational memory and response generation.
4. Display results in the Streamlit front-end in a user-friendly manner.
5. Ensure the system handles errors gracefully (e.g., invalid queries or failed API calls).

**Bonus**: Conversational memory is implemented using LangChain, allowing the system to maintain context across multiple queries.

## Notes

-   The Google 3 API is simulated in this project due to limited public access. In production, replace the simulated LLM with actual API calls to Google API (see [google/api](https://ai.google.dev/gemini-api/docs/api-key)).
-   Ensure the SerpAPI key is valid and websites allow scraping.
-   The system uses packages from `requirements.txt` or equivalent alternatives (e.g., `requests`, `WebBaseLoader`, `langchain`).
-   Test the system thoroughly to verify content retrieval, processing, and response generation.

## Troubleshooting

-   **Backend Errors**: Verify API keys in `.env` and ensure all dependencies are installed.
-   **Frontend Errors**: Ensure the Flask backend is running at `http://localhost:5000` before starting Streamlit.
-   **Search/Scraping Issues**: Check SerpAPI key validity and handle potential website access restrictions.
-   **LLM Issues**: If using a real Google API, ensure proper authentication and quota availability.

## Submission

Submit the entire `RAG-Search/` directory as a zip file or via a Git repository. Include all files (including `requirements.txt` and `.env` template without sensitive keys) and ensure this `README.md` is updated with any setup-specific notes.

Good luck!
