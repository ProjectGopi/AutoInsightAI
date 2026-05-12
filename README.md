# AutoInsight AI

AutoInsight AI is a full-stack web application designed to help users upload datasets, manage them, and perform automated analytics and insights generation. 

## Features
- **Dashboard**: Overview of your active datasets and analytics results.
- **Dataset Management**: Upload, view, and manage datasets via the web interface.
- **Analytics Engine**: Powered by Pandas and Scikit-learn to extract insights from your data.
- **Dark Mode Support**: Toggleable dark mode for better user experience.
- **Docker Ready**: Easy deployment with Docker.

## Tech Stack

### Frontend
- **Framework**: React.js 18
- **Styling**: Tailwind CSS & PostCSS
- **Routing**: React Router DOM v7
- **Charts**: Recharts
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI
- **Database ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Data Processing**: Pandas & NumPy
- **Machine Learning**: Scikit-Learn

## Project Structure

```text
autoinsight-ai/
│
├── backend/          # FastAPI backend application
│   ├── app/          # API routes, models, and core logic
│   ├── venv/         # Python virtual environment
│   ├── uploaded_files/ # Directory for user uploaded datasets
│   └── requirements.txt
│
├── frontend/         # React frontend application
│   ├── public/       # Static assets
│   ├── src/          # React components, pages, and services
│   ├── package.json  # NPM dependencies
│   └── tailwind.config.js
│
└── docker/           # Docker configuration files
```

## Getting Started

### Prerequisites
- Node.js & npm (for the frontend)
- Python 3.8+ (for the backend)
- PostgreSQL (if running locally without Docker)

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```
   The app will be available at `http://localhost:3000`.

## Running with Docker

*(Instructions to be updated based on your specific docker-compose setup)*
```bash
docker-compose up -d --build
```

## Author Details

**Pokala Gopi Lakshman**
- Email: pokala.gopilakshman@gmail.com
- GitHub: [github.com/pokala-gopi-lakshman](https://github.com/22BCE0585)
