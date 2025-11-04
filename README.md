# Project 3: AI & Big Data System for Student Mental Health Warning

This is the final product for Project 3, specializing in Cyber Security & IoT, at VNU-International School.

**Student:** Nguyễn Duy Hùng
**ID:** 22071098

## Project Overview

This project develops an interactive dashboard designed to analyze and provide early warnings for student mental health issues. The system leverages data analysis and AI to identify potential risk factors and behavioral patterns.

The dashboard presents a comprehensive narrative through three analytical sections:
1.  **Evidence from Real-world Survey Data:** Utilizes a public dataset from Kaggle to establish a correlation between academic performance (GPA) and mental health status.
2.  **In-depth Analysis of Risk Factors:** Employs a custom-simulated dataset to explore underlying risk factors, such as academic load and social support.
3.  **Behavioral Monitoring & AI-powered Alerts:** Demonstrates a proof-of-concept AI system that analyzes simulated text data for sentiment and monitors behavioral patterns (e.g., late-night activity) to flag at-risk individuals.

## Installation and Usage Guide

### Prerequisites
- Python 3.8+
- Git

### Setup Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/hunghhhh/vnuis-project3-mental-health.git
    cd vnuis-project3-mental-health
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Generate the necessary datasets:**
    *   First, run the behavioral data simulator:
        ```bash
        python scripts/data_simulator.py
        ```
    *   Then, create the student profiles:
        ```bash
        python scripts/create_profiles.py
        ```
5.  **Train the AI model (only needs to be run once):**
    ```bash
    python scripts/train_model.py
    ```
6.  **Run the Streamlit dashboard:**
    ```bash
    streamlit run app/dashboard.py
    ```
    The application will open in your web browser.