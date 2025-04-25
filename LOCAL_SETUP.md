# Local Setup Guide

This guide provides comprehensive instructions for setting up and running the application locally.

## Prerequisites

1. **Python**: Version 3.8 or higher
2. **pip**: Python package manager
3. **Git**: For version control
4. **Excel**: For viewing the data file (optional)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Create a Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Copy the `.env.example` file to create your `.env` file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and update the following variables:
     - `GEMINI_API_KEY`: Your Google Gemini API key
     - `EXCEL_FILE_PATH`: Path to your Excel data file
     - Other settings can be left as default for local development

## Data Preparation

1. Ensure your Excel file (`Kemet_Data.xlsx`) is placed in the project root directory
2. The Excel file should contain the following sheets:
   - Product data
   - Specifications
   - Categories

## Running the Application

1. **Start the Flask Server**
   ```bash
   # Windows
   python app.py

   # macOS/Linux
   python3 app.py
   ```
2. The application will be available at `http://localhost:5000`



