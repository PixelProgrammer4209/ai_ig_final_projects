TripSmith 🌴

TripSmith is an AI-powered, feasibility-first travel planner focused initially on Kerala. Unlike standard AI itineraries, TripSmith actively evaluates your budget and constraints using a multi-agent AI workflow and local RAG (Retrieval-Augmented Generation) database to determine if your trip is actually practical.

Features

Sequential Multi-Agent AI: Powered by CrewAI (Researcher -> Planner -> Analyst).

Local RAG Database: Uses ChromaDB and Sentence Transformers for accurate local tourism data.

Feasibility Analysis: Actively calculates expected costs against user budgets.

Minimalist UI: Clean, responsive React frontend with Markdown rendering.

Prerequisites

Python 3.12+

Node.js 18+

A free Groq API Key

Setup & Installation

1. Backend Setup

Navigate to the backend directory and set up your Python environment:

cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt


Create a .env file in the backend directory and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here


Initialize the local database (only needed once):

python rag_manager.py


Start the FastAPI server:

uvicorn main:app --reload


2. Frontend Setup

Open a new terminal and navigate to the frontend directory:

cd frontend
npm install


Start the Vite development server:

npm run dev


Usage

Open your browser to http://localhost:5173.

Enter your starting location, destination (e.g., Munnar), days, travelers, and total budget.

Add any specific travel preferences (e.g., "Tea Gardens, Relaxing").

Click "Plan My Trip". The AI agents will take ~30-60 seconds to research, plan, and analyze your trip.

Tech Stack

Frontend: React, Vite, React-Markdown

Backend: FastAPI, Pydantic

AI & ML: CrewAI, ChromaDB, SentenceTransformers, Groq (LLM)