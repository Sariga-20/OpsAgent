# 🤖 OpsAgent — Autonomous Business Operations Agent

OpsAgent is an AI-powered business operations investigation system that combines **LLM reasoning, business data analysis, machine learning predictions, RAG-based policy retrieval, and human approval** to investigate operational risks.

The system can investigate an e-commerce order, retrieve relevant business data, generate a late-delivery risk prediction using the OpsPredict ML model, retrieve operational policy evidence, identify deterministic policy indicators, generate an evidence-based analysis, and require human approval before executing an operational action.

---

## 🎯 Project Objective

The goal of OpsAgent is to demonstrate how an AI agent can combine multiple business intelligence and AI capabilities into a single operational workflow.

Instead of only generating an LLM response, OpsAgent uses specialized tools to:

1. Investigate an order using PostgreSQL data
2. Generate a machine-learning risk prediction
3. Retrieve relevant operational policies using RAG
4. Evaluate deterministic business-policy indicators
5. Generate an evidence-based LLM analysis
6. Request human approval
7. Execute an operational action only after approval

---

## 🏗️ Architecture

```text
                    User / Business Question
                              │
                              ▼
                       ┌─────────────┐
                       │  OpsAgent   │
                       └──────┬──────┘
                              │
                              ▼
                         LLM - Ollama
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Business Data     ML Prediction       RAG
            Tool              Tool             Tool
              │               │               │
              ▼               ▼               ▼
        PostgreSQL        OpsPredict        ChromaDB
                                           + Hugging Face
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                       Investigation
                              │
                              ▼
                    Policy Evaluation
                              │
                              ▼
                       LLM Analysis
                              │
                              ▼
                      Human Approval
                         │          │
                       Reject     Approve
                         │          │
                         ▼          ▼
                      Stop       Action

```
---
## 🧠 Key Capabilities

### 1. Business Data Investigation

OpsAgent retrieves order information and operational features from PostgreSQL.

### 2. Machine Learning Risk Prediction

The system integrates the **OpsPredict XGBoost model** to estimate the probability of late delivery.

The model uses features such as:

- Seller historical performance
- Estimated delivery time
- Freight cost
- Number of items
- Number of sellers
- Seller/customer geographic relationship
- Product characteristics
- Historical seller orders

### 3. RAG-Based Policy Retrieval

Operational policies are stored as documents and indexed using:

- ChromaDB
- Hugging Face sentence-transformer embeddings
- LangChain

OpsAgent retrieves relevant policy evidence before generating its analysis.

### 4. Deterministic Policy Evaluation

Business-policy indicators are evaluated using deterministic Python rules rather than allowing the LLM to invent thresholds.

The implementation evaluates indicators such as:

- Seller historical late-delivery activity
- Short estimated delivery time
- High freight cost
- Multiple items
- Multiple sellers
- Cross-state seller/customer location

> **Note:** The numeric thresholds used by the implementation are operational heuristics defined in code. They are not claimed to be official thresholds from the policy document.

### 5. LLM Analysis

Ollama with **Llama 3.2:3b** generates an evidence-based investigation summary using:

- Investigation data
- ML prediction
- Deterministic policy evaluation
- Retrieved policy evidence

The LLM is instructed not to invent policy conclusions or override deterministic results.

### 6. Human-in-the-Loop Approval

OpsAgent does not independently execute consequential operational actions.

A human must approve the proposed action before execution.

```text
Investigation
      ↓
LLM Analysis
      ↓
Human Approval
   ↙       ↘
Reject    Approve
  ↓          ↓
Stop       Execute
```

---

## 🛠️ Technology Stack

### Programming

- Python
- SQL

### AI / LLM

- Ollama
- Llama 3.2:3b
- LangChain
- LangGraph
- Hugging Face
- Sentence Transformers

### Retrieval / RAG

- ChromaDB
- LangChain Chroma
- Hugging Face Embeddings

### Data / Database

- PostgreSQL
- Pandas
- NumPy
- Psycopg2

### Machine Learning

- XGBoost
- Scikit-learn

### Application

- FastAPI
- Streamlit

### Testing / Development

- Pytest
- Git
- GitHub

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
└── README.md
```

---

## 🔄 Investigation Workflow

For each order, OpsAgent follows this workflow:

### Step 1 — Order Investigation

The agent retrieves the order and calculates the required operational features.

### Step 2 — Risk Prediction

The OpsPredict XGBoost model generates a late-delivery probability.

### Step 3 — Policy Retrieval

The RAG system searches the operational delivery policy for relevant guidance.

### Step 4 — Policy Evaluation

Deterministic Python rules evaluate operational risk indicators.

### Step 5 — LLM Analysis

The LLM combines the investigation facts, model prediction, policy evaluation, and retrieved policy evidence into a structured analysis.

### Step 6 — Human Approval

The system pauses before executing an operational action.

### Step 7 — Action

If approved, OpsAgent creates the operational review action.

If rejected, no operational action is executed.

---

## 🖥️ Streamlit Interface

The Streamlit application provides an interactive interface for investigating orders.

The interface displays:

- Order ID
- Late-delivery probability
- Risk classification
- Prediction features
- Policy indicator evaluation
- LLM analysis
- Retrieved policy evidence
- Human approval controls
- Action result

Run the application with:

```bash
streamlit run app/streamlit_app.py
```

---

## ⚙️ Setup

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
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and run Ollama

Install Ollama and pull the required model:

```bash
ollama pull llama3.2:3b
```

Verify it:

```bash
ollama run llama3.2:3b
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_TEMPERATURE=0

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=businesspulse
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

> **Important:** Do not commit the `.env` file to GitHub.

---

## 🗄️ Database

OpsAgent uses the PostgreSQL database created for the BusinessPulse project.

The application reads operational data from tables such as:

- `orders`
- `order_items`
- `customers`
- `sellers`
- `products`
- `order_payments`
- `order_reviews`

The database connection is configured through environment variables.

---

## 🧪 Testing

Run the available tests using:

```bash
pytest -v
```

Individual components can also be tested separately.

Example:

```bash
python rag/test_retriever.py
```

---

## 🔐 Human Approval & Safety

OpsAgent follows a human-in-the-loop design.

The AI system can:

- Investigate
- Retrieve evidence
- Predict risk
- Analyze information
- Recommend an operational review

But it does not independently execute consequential operational actions.

The final action requires explicit human approval.

---

## 📌 Example Use Case

A business operations user enters an order ID.

OpsAgent follows this process:

```text
Order ID
   ↓
Retrieve order data
   ↓
Calculate operational features
   ↓
Predict late-delivery probability
   ↓
Retrieve delivery policy
   ↓
Evaluate policy indicators
   ↓
Generate LLM investigation
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
- Cloud deployment
- Automated evaluation of agent responses

---

## 👩‍💻 Author

**Sariga C**

Computer Science & Engineering

Aspiring AI / ML Engineer | Data Analyst | Agentic AI Engineer