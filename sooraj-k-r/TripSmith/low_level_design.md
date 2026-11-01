TripSmith: Low-Level Workflow Design

This document maps the exact operational workflow of the TripSmith application using sequence and architecture flow diagrams.

1. Sequence Diagram (Data Flow)

This diagram illustrates the step-by-step communication between the user, the FastAPI backend, the CrewAI Agents, and the local Vector Database.

sequenceDiagram
    autonumber
    actor User
    participant React UI (Frontend)
    participant FastAPI (Backend)
    participant CrewAI Orchestrator
    participant RAG Tool (ChromaDB)
    participant Groq LLM API
    
    User->>React UI: Submits Form (Location, Budget, Preferences)
    React UI->>FastAPI: POST /api/plan-trip (JSON Payload)
    FastAPI->>CrewAI Orchestrator: Initialize TripCrew with Inputs
    
    rect rgb(240, 248, 255)
        Note right of CrewAI Orchestrator: Agent 1: Destination Researcher
        CrewAI Orchestrator->>RAG Tool (ChromaDB): Query Vector DB (Destination + Preferences)
        RAG Tool (ChromaDB)-->>CrewAI Orchestrator: Returns top matching context (Factual Data)
        CrewAI Orchestrator->>Groq LLM API: Generate Research Summary based on Context
        Groq LLM API-->>CrewAI Orchestrator: Research Report
    end

    rect rgb(240, 255, 240)
        Note right of CrewAI Orchestrator: Agent 2: Itinerary Planner
        CrewAI Orchestrator->>Groq LLM API: Prompt: Build itinerary using Research Report
        Groq LLM API-->>CrewAI Orchestrator: Draft Itinerary (Markdown)
    end

    rect rgb(255, 240, 245)
        Note right of CrewAI Orchestrator: Agent 3: Budget Analyst
        CrewAI Orchestrator->>Groq LLM API: Prompt: Compare Itinerary costs vs User Budget
        Groq LLM API-->>CrewAI Orchestrator: Final Feasibility Report & Warnings
    end

    CrewAI Orchestrator-->>FastAPI: Raw String Output (Markdown)
    FastAPI->>FastAPI: Parse Feasibility Status & Warnings from Output
    FastAPI-->>React UI: Return JSON (TripResponse Schema)
    React UI-->>User: Renders Markdown Tables & Feasibility UI


2. RAG (Retrieval-Augmented Generation) Ingestion Workflow

This illustrates how the knowledge base is built before the user ever makes a request.

flowchart TD
    A[Raw Data Files (kerala_guide.txt)] --> B[PdfReader / File IO]
    B --> C[Text Chunker (Size: 200 words)]
    C --> D[SentenceTransformers Model]
    D -->|all-MiniLM-L6-v2| E[Generate Vector Embeddings]
    E --> F[(ChromaDB Persistent Storage)]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
