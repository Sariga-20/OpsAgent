# 🤖 OpsAgent — Autonomous Business Operations Agent

OpsAgent is an AI-powered business operations investigation system that combines **business data analysis, machine learning, RAG-based policy retrieval, LLM reasoning, deterministic policy evaluation, and human approval** into one operational workflow.

The system investigates an e-commerce order, retrieves operational data from PostgreSQL, generates a late-delivery risk prediction using the **OpsPredict XGBoost model**, retrieves relevant delivery-policy evidence using RAG, evaluates deterministic policy indicators, generates an evidence-based analysis with **Groq**, and requires explicit human approval before executing an operational action.

## 🚀 Live Demo

**Streamlit:** https://opsagent-3bnmvb23ipfxfgdauzg7q8.streamlit.app

> The live application uses Streamlit Community Cloud, Neon PostgreSQL, and Groq. Database credentials and API keys are stored as deployment secrets and are not committed to the repository.

---

## 🎯 Project Objective

OpsAgent demonstrates how an AI agent can combine multiple business intelligence and AI capabilities into a controlled operational workflow.

Instead of relying on an LLM alone, OpsAgent uses specialized components to:

1. Investigate an order using PostgreSQL business data
2. Generate a machine-learning late-delivery prediction
3. Retrieve relevant operational policy evidence using RAG
4. Evaluate deterministic business-policy indicators
5. Generate an evidence-based LLM analysis
6. Request explicit human approval
7. Execute an operational action only after approval

---

## 🏗️ Architecture

```text
                         User
                          │
                          ▼
                ┌──────────────────┐
                │    Streamlit     │
                │    Dashboard     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     OpsAgent     │
                │   Investigation  │
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   Business Data     ML Prediction     RAG
       Tool              Tool          Tool
          │              │              │
          ▼              ▼              ▼
   Neon PostgreSQL   OpsPredict       ChromaDB
                     XGBoost        + Hugging Face
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                Policy Evaluation
                         │
                         ▼
                      Groq LLM
                         │
                         ▼
                Evidence-Based Analysis
                         │
                         ▼
                 Human Approval
                    /                         Reject      Approve
                   │           │
                   ▼           ▼
                  Stop      Operational
                              Action
```

---

## 🧠 Key Capabilities

### 1. Business Data Investigation

OpsAgent retrieves order information and operational features from PostgreSQL.

The project uses **Neon PostgreSQL** for the deployed application.

### 2. Machine Learning Risk Prediction

The system integrates the **OpsPredict XGBoost model** to estimate the probability of late delivery.

The prediction workflow uses operational features such as:

- Seller historical performance
- Estimated delivery time
- Freight cost
- Number of items
- Number of sellers
- Seller/customer geographic relationship
- Product characteristics
- Historical seller orders

### 3. RAG-Based Policy Retrieval

Operational delivery policies are stored as documents and indexed for semantic retrieval using:

- ChromaDB
- Hugging Face sentence-transformer embeddings
- LangChain
- `all-MiniLM-L6-v2`

OpsAgent retrieves relevant policy evidence before generating its analysis.

The deployed RAG tool can create the local Chroma vector store from the delivery policy document when a usable vector store is not already present.

### 4. Deterministic Policy Evaluation

Business-policy indicators are evaluated using deterministic Python rules rather than allowing the LLM to invent thresholds.

The implementation evaluates indicators such as:

- Seller historical late-delivery activity
- Short estimated delivery time
- High freight cost
- Multiple items
- Multiple sellers
- Cross-state seller/customer location

> **Note:** Numeric thresholds used by the implementation are operational heuristics defined in code. They are not claimed to be official thresholds from the policy document.

### 5. Evidence-Based LLM Analysis

OpsAgent uses **Groq** with the `openai/gpt-oss-20b` model to generate a structured investigation summary.

The analysis is based on:

- Investigation facts
- ML prediction
- Deterministic policy evaluation
- Retrieved policy evidence

The LLM is instructed to use the supplied evidence, avoid inventing policy rules, and not execute operational actions.

### 6. Human-in-the-Loop Approval

OpsAgent does not independently execute consequential operational actions.

A human must explicitly approve the action before execution.

```text
Investigation
      ↓
Policy Evaluation
      ↓
LLM Analysis
      ↓
Human Approval
    ↙       ↘
 Reject     Approve
   ↓          ↓
 Stop       Execute
```

The deployed application has been tested with both approval paths:

- **Approve → operational action executed**
- **Reject → no operational action executed**

---

## 🛠️ Technology Stack

### Programming

- Python
- SQL

### AI / LLM

- Groq
- `openai/gpt-oss-20b`
- LangChain
- LangGraph
- Hugging Face
- Sentence Transformers

### Retrieval / RAG

- ChromaDB
- LangChain Chroma
- Hugging Face Embeddings
- `all-MiniLM-L6-v2`

### Data / Database

- PostgreSQL
- Neon PostgreSQL
- Pandas
- NumPy
- Psycopg2

### Machine Learning

- XGBoost
- Scikit-learn

### Application / Deployment

- Streamlit
- Streamlit Community Cloud
- Docker

### Development

- Git
- GitHub
- VS Code
- Python virtual environment

---

## 📂 Project Structure

```text
OpsAgent/
│
├── app/
│   └── streamlit_app.py
│
├── documents/
│   └── delivery_policy.txt
│
├── models/
│   ├── model_metadata.json
│   └── ops_predict_xgboost.pkl
│
├── rag/
│   ├── document_loader.py
│   ├── vector_store.py
│   └── test_retriever.py
│
├── src/
│   ├── actions.py
│   ├── agent.py
│   ├── agent_graph.py
│   ├── approval.py
│   ├── config.py
│   ├── database.py
│   ├── graph_nodes.py
│   ├── graph_state.py
│   ├── investigation.py
│   ├── policy_evaluator.py
│   └── workflow.py
│
├── tools/
│   ├── business_data_tool.py
│   ├── order_data_tool.py
│   ├── order_prediction_data.py
│   ├── order_risk_tool.py
│   ├── opspredict_tool.py
│   └── rag_tool.py
│
├── .gitignore
├── Dockerfile
├── requirements.txt
├── runtime.txt
└── README.md
```

> `data/chroma/`, `.env`, Python virtual environments, logs, and database dump files are excluded from Git using `.gitignore`.

---

## 🔄 Investigation Workflow

For each order, OpsAgent follows this workflow:

### Step 1 — Order Investigation

The application receives an order ID and retrieves the required business and operational data.

### Step 2 — Risk Prediction

The OpsPredict XGBoost model generates a late-delivery probability and prediction result.

### Step 3 — Policy Retrieval

The RAG system searches the delivery operations policy for relevant evidence.

### Step 4 — Policy Evaluation

Deterministic Python rules evaluate the configured operational policy indicators.

### Step 5 — LLM Analysis

Groq generates a structured analysis using the investigation facts, model prediction, policy evaluation, and retrieved policy evidence.

### Step 6 — Human Approval

The workflow pauses and requires explicit human approval.

### Step 7 — Action

If approved, OpsAgent creates the operational review action.

If rejected, no operational action is executed.

---

## 🖥️ Streamlit Interface

The Streamlit application provides an interactive interface for investigating orders.

The dashboard displays:

- Order ID
- Late-delivery probability
- Risk classification
- Prediction features
- Policy indicator evaluation
- LLM analysis
- Retrieved policy evidence
- Human approval controls
- Action result

Run locally with:

```bash
streamlit run app/streamlit_app.py
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sariga-20/OpsAgent.git
cd OpsAgent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scriptsctivate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DB_HOST=your_neon_host
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password

GROQ_API_KEY=your_groq_api_key
GROQ_TEMPERATURE=0
```

> **Important:** Never commit `.env` or API keys to GitHub.

### 5. Run the application

```bash
streamlit run app/streamlit_app.py
```

---

## 🗄️ Database

OpsAgent uses PostgreSQL for business and operational data.

The deployed application uses **Neon PostgreSQL**.

The project reads data from tables including:

- `orders`
- `order_items`
- `customers`
- `sellers`
- `products`
- `order_payments`
- `order_reviews`

Database connection details are supplied through environment variables.

---

## 🔎 RAG Pipeline

The delivery policy is stored in:

```text
documents/delivery_policy.txt
```

The RAG pipeline:

```text
Delivery Policy
      ↓
Document Loader
      ↓
Text Splitting
      ↓
Hugging Face Embeddings
      ↓
ChromaDB
      ↓
Similarity Search
      ↓
Retrieved Policy Evidence
      ↓
LLM Analysis
```

The deployed application was tested successfully with retrieved delivery-policy evidence.

---

## 🤖 ML Prediction Pipeline

The OpsPredict component provides the late-delivery prediction:

```text
Order ID
   ↓
Retrieve Business Data
   ↓
Generate Prediction Features
   ↓
OpsPredict XGBoost Model
   ↓
Late-Delivery Probability
   ↓
Prediction Result
```

The prediction is presented separately from deterministic policy evaluation so that model output is not treated as a business-policy rule.

---

## 🔐 Human Approval & Safety

OpsAgent follows a human-in-the-loop design.

The AI system can:

- Investigate
- Retrieve evidence
- Predict risk
- Evaluate policy indicators
- Generate analysis
- Prepare an operational review

But it does not independently execute the operational action.

The final action requires explicit human approval.

```text
AI Investigation
       ↓
Evidence + Analysis
       ↓
Human Decision
    ↙       ↘
 Reject     Approve
   ↓          ↓
 Stop       Action
```

---

## 🐳 Docker

The project includes a Dockerfile for containerized deployment.

Build the image:

```bash
docker build -t opsagent .
```

Run it locally:

```bash
docker run -p 8501:8501 --env-file .env opsagent
```

Docker is not required for the current Streamlit Community Cloud deployment, but the project remains container-ready.

---

## ☁️ Deployment

### Current Deployment

The live application is deployed using:

**Streamlit Community Cloud**

The application connects to:

- Neon PostgreSQL
- Groq API
- RAG policy documents
- OpsPredict model

Secrets are configured through the deployment platform and are not stored in the repository.

### Docker / Render

The application was also containerized and tested with Docker.

A Render deployment was tested, but the free Render service reached its **512 MB memory limit** while running the application. The live application therefore uses Streamlit Community Cloud instead.

---

## 🧪 Testing

Run the available tests with:

```bash
pytest -v
```

The RAG retriever can also be tested separately:

```bash
python rag/test_retriever.py
```

The deployed application has been manually tested for:

- Order investigation
- ML prediction
- Policy retrieval
- Policy indicator evaluation
- Groq analysis
- Human approval
- Approved operational action
- Rejected operational action

---

## 📌 Example Use Case

A business operations user enters an order ID.

OpsAgent follows this process:

```text
Order ID
   ↓
Retrieve order data
   ↓
Generate operational features
   ↓
Predict late-delivery probability
   ↓
Retrieve delivery policy
   ↓
Evaluate policy indicators
   ↓
Generate evidence-based LLM analysis
   ↓
Request human approval
   ↓
Execute or reject operational review
```

This demonstrates an agentic workflow where an LLM works together with business data, machine learning, retrieval systems, deterministic rules, and human oversight.

---

## 🚀 Future Improvements

Potential future improvements include:

- More business investigation tools
- Automated root-cause analysis across multiple orders
- Additional company policy documents
- Advanced LangGraph human-in-the-loop interrupts
- Agent memory
- More operational actions
- API-based deployment
- Authentication
- Production monitoring
- Automated evaluation of agent responses
- Expanded observability and logging

---

## 👩‍💻 Author

**Sariga C**

Computer Science & Engineering

**Aspiring AI / ML Engineer | Data Analyst | Agentic AI Engineer**
