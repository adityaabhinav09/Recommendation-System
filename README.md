# Movie Recommendation App

A Streamlit-based movie recommendation app built with Python and TMDB integration.

## Overview

This app lets users select a movie and view the top 5 recommended films along with their posters and direct TMDB links.

## Features

- Movie similarity-based recommendations
- Poster fetch using TMDB API
- Clean Streamlit UI with responsive recommendation cards
- Direct links to TMDB movie pages

## Project Structure

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `movies.pkl` - Saved movies data
- `similarity_index.pkl` - Precomputed similarity matrix
- `Data/` - Raw dataset files
- `.env` - Environment variables (not checked in)
- `.gitignore` - Files ignored by Git

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Recommendation\ System
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your TMDB API key in a `.env` file:
   ```bash
   TMDB_API=your_tmdb_api_key_here
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment

Deploy with Streamlit Cloud, Heroku, or any platform that supports Python web apps.

### Live Demo

- Deployed project: https://recommendation-system-movie02.streamlit.app/

### Streamlit Cloud

1. Push this project to GitHub.
2. Connect the repo to Streamlit Cloud.
3. Add the `TMDB_API` secret in Streamlit Cloud settings.
4. Deploy.

## Author

Aditya Abhinav

## Notes

- Do not commit `.env` or virtual environment files.
- If you want, you can exclude the `Data/` directory and model files from GitHub and store them separately.
