# AI Powered MSME Smart Decision Support System

A complete production-quality prototype of an AI-powered decision support system for MSMEs (Micro, Small, and Medium Enterprises). This application enables factory owners to securely manage factory data, predict future profits, assess business health, clean and upload historical data via CSV, visualize key analytics, and receive dynamic, data-driven AI recommendations.

## Tech Stack
- **Programming Language**: Python 3.8+
- **Frontend**: Streamlit
- **Backend API**: FastAPI
- **Database**: SQLite (ORM via SQLAlchemy)
- **Machine Learning**: Scikit-learn
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib

## Project Features
1. **Secure Authentication**: Register and log in securely. Uses JWT token-based authentication on the FastAPI backend and persistent session state in the Streamlit frontend.
2. **Interactive Dashboard**: Track sales, production volume, profit margins, inventory status, utility expenses, machine operating hours, and downtime.
3. **Data Entry Form**: Manually record daily factory metrics.
4. **CSV Bulk Upload**: Upload csv data with automatic cleaning logic powered by Pandas.
5. **Predictive Analytics**: Machine learning regression models predicting future factory profits.
6. **Business Health Assessment**: Rule-based scoring architecture ready to be substituted with a Scikit-learn Decision Tree Classifier.
7. **Dynamic AI Recommendation Engine**: Custom recommendations based on machine performance, inventory status, profit margins, and costs.
8. **Reports & Exports**: Compile and download monthly performance reports in PDF format.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher installed on your machine.
- Streamlit and FastAPI requirements.

### Installation
1. Navigate to the project root directory:
   ```bash
   cd msme_decision_support
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (Command Prompt)**:
     ```cmd
     venv\Scripts\activate.bat
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the FastAPI Backend**:
   Run the backend wrapper script:
   ```bash
   python backend/run.py
   ```
   Or manually:
   ```bash
   uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The interactive API docs will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

2. **Start the Streamlit Frontend**:
   In a separate terminal (with the virtual environment activated):
   ```bash
   streamlit run frontend/app.py
   ```
   The web portal will open at [http://localhost:8501](http://localhost:8501).

## Folder Structure
```
msme_decision_support/
├── requirements.txt            # Python dependencies
├── README.md                   # Installation and usage instructions
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI routing and application initialization
│   │   ├── database.py         # SQLite connection config
│   │   ├── models.py           # SQLAlchemy database tables
│   │   ├── schemas.py          # Pydantic validation schemas
│   │   ├── crud.py             # Data handling and database queries
│   │   └── auth.py             # Security, password hashing, and JWT creation
│   └── run.py                  # API launch script
├── frontend/
│   ├── app.py                  # Main Streamlit dashboard code
│   └── api_client.py           # HTTP interface connecting Streamlit to FastAPI
├── ml/
│   ├── models/
│   │   ├── profit_predictor.py # Linear regression profit predictor
│   │   ├── health_scorer.py    # Factory health evaluator
│   │   └── recommendation.py   # Rule-based dynamic feedback generator
│   └── train.py                # Script to fit model parameters
└── utils/
    ├── data_cleaner.py         # Preprocessing data functions using Pandas
    └── report_generator.py     # PDF monthly reports compilation
```
