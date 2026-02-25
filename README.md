
# **Non-Flow Thermodynamic Process Visualizer**

*A FastAPI + Streamlit Web App for T–s & P–v Diagrams Using CoolProp*

---

## **📌 Project Description**

This project visualizes **non-flow thermodynamic processes** by generating **Temperature–Entropy (T–s)** and **Pressure–Volume (P–v)** diagrams using accurate steam properties from **CoolProp**.

It implements the five major non-flow processes:

1. **Constant Volume (Isochoric)**
2. **Constant Pressure (Isobaric)**
3. **Isothermal**
4. **Adiabatic (Isentropic)**
5. **Polytropic**

The system accepts initial conditions, uses CoolProp to compute thermodynamic properties along the process path, stores retrieved values, and displays interactive plots.

This work is based on the guidelines from the course instructions referencing:

* **Building APIs in Python (Datacamp)**
* **SQL Server Fundamentals (Datacamp)**

---

## **🧱 Project Architecture**

```
nonflow_webapp/
│
├── backend/
│   ├── main.py            # FastAPI backend API
│   ├── utils.py           # Thermodynamic calculations using CoolProp
│   ├── database.py        # SQLAlchemy DB engine & session
│   ├── models.py          # Database tables (ProcessPoints)
│   └── crud.py            # Save/fetch computed points
│
├── frontend/
│   └── app.py             # Streamlit frontend for UI & plotting
│
├── data/
│   └── steam_table.csv    # (Optional) raw steam table for reference
│
├── requirements.txt       # Dependencies
└── README.md
```

---

## **⚙️ Features**

### **Frontend (Streamlit)**

* Clean and simple interface
* Process selector
* User inputs initial P, T, n (polytropic index), etc.
* **Calculate button**
* Real-time T–s and P–v plots
* Download results as CSV

### **Backend (FastAPI)**

* `/compute` endpoint for thermodynamic calculations
* Returns JSON with full process curve
* Uses CoolProp for property accuracy

### **Database (SQLAlchemy + SQLite)**

* Stores process data for record-keeping
* Each calculation is logged
* Useful for debugging or lecturer demonstration

### **Thermodynamics**

* Accurate steam/water properties via **CoolProp**
* Handles saturated, superheated, and compressed regions
* Supports 5 non-flow processes

---

## **📥 Installation**

### 1. Clone or download the project:

```bash
git clone <your-repo-url>
cd nonflow_webapp
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Run FastAPI backend:

```bash
uvicorn backend.main:app --reload
```

### 4. Run Streamlit frontend:

```bash
streamlit run frontend/app.py
```

---

## **🧪 How It Works**

1. User selects process type.
2. User enters initial conditions (P, T, etc.).
3. Streamlit sends request → FastAPI (`/compute`).
4. Backend computes values using CoolProp for:

   * Temperature
   * Pressure
   * Specific Volume
   * Entropy
5. Backend returns 50+ computed points.
6. Streamlit plots T–s and P–v graphs.
7. User can download the generated dataset as CSV.

---

## **📊 Example Output**

### T–s Diagram

(Shows entropy changes vs temperature)

### P–v Diagram

(Shows pressure vs specific volume for process path)

---

## **📚 Dependencies**

* Python 3.10+
* Streamlit
* FastAPI
* CoolProp
* SQLAlchemy
* Uvicorn
* Pandas
* Matplotlib

---

## **📝 Acknowledgment**

This project follows the instruction of **Assignment 3: Data Visualization of Non-Flow Processes**, covering:

* Constant Volume
* Constant Pressure
* Polytropic
* Adiabatic
* Isothermal

Using API development (FastAPI) and SQL fundamentals as referenced from Datacamp training.

