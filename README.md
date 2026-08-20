# 💊 Drug NER + Knowledge Graph

> An AI-powered application for extracting drug-related entities from medical documents and building a knowledge graph connecting drugs, drug classes, cancers, and major side effects.

## 📌 Overview

**Drug NER + Knowledge Graph** is an NLP-based healthcare research application designed to extract and organize information about drugs and their relationships with cancers and side effects.

The application allows users to upload structured datasets and medical PDF documents, train a Named Entity Recognition (NER) model, extract relevant drug information, and represent relationships between entities through a knowledge graph.

The goal is to make complex drug–cancer–side-effect relationships easier to explore and analyze.

## ✨ Features

* 📊 **Excel Dataset Upload**

  * Upload `.xlsx` datasets containing drug information.
  * Preview uploaded records directly in the application.
  * Automatically split data into training and testing sets.

* 🧠 **Drug Named Entity Recognition (NER)**

  * Train an NLP model using the uploaded dataset.
  * Identify drug-related entities from text.
  * Extract important medical entities from documents.

* 📄 **PDF Document Processing**

  * Upload medical/research PDF documents.
  * Extract text for NLP processing.
  * Identify drug-related information from unstructured text.

* 🕸️ **Knowledge Graph**

  * Represent relationships between:

    * Drugs
    * Drug Classes
    * Cancers
    * Side Effects
  * Convert extracted information into connected entities and relationships.

* 🔎 **Drug Relationship Analysis**

  * Explore which cancers are associated with specific drugs.
  * Identify major side effects associated with drugs.
  * Analyze relationships between drug classes and treatments.

* 📈 **Dataset Visualization**

  * Preview uploaded datasets.
  * Display training/testing split information.
  * Present extracted entities and relationships in an organized interface.

## 🗂️ Example Dataset

The application supports datasets containing fields such as:

| Column               | Description                      |
| -------------------- | -------------------------------- |
| `ID`                 | Unique identifier                |
| `Drug_Name`          | Name of the drug                 |
| `Drug_Class`         | Drug classification              |
| `Common_Cancers`     | Cancers associated with the drug |
| `Major_Side_Effects` | Major reported side effects      |

Example:

| Drug        | Class                 | Common Cancers         | Major Side Effects                   |
| ----------- | --------------------- | ---------------------- | ------------------------------------ |
| Cisplatin   | Platinum Chemotherapy | Lung, Ovarian, Bladder | Nephrotoxicity, Nausea, Hearing loss |
| Carboplatin | Platinum Chemotherapy | Ovarian, Lung          | Bone marrow suppression, Nausea      |
| Oxaliplatin | Platinum Chemotherapy | Colorectal             | Peripheral neuropathy, Nausea        |
| Paclitaxel  | Taxane Chemotherapy   | Breast, Ovarian, Lung  | Hair loss, Neuropathy                |
| Docetaxel   | Taxane Chemotherapy   | Breast, Prostate       | Fluid retention, Fatigue             |

> **Note:** The dataset is intended for NLP/research demonstration and should not be used as a substitute for professional medical advice.

## 🏗️ System Workflow

```text
              ┌─────────────────────┐
              │   Upload Dataset    │
              │       (.xlsx)       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Data Preprocessing  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Train NER Model   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Upload PDF/Text   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │    Drug NER         │
              │ Entity Extraction   │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Knowledge Graph     │
              │ Construction         │
              └──────────┬──────────┘
                         │
                         ▼
       ┌──────────────────────────────────┐
       │ Drug ↔ Cancer ↔ Side Effect      │
       │          Relationships            │
       └──────────────────────────────────┘
```

## 🛠️ Tech Stack

* **Python**
* **Natural Language Processing (NLP)**
* **Named Entity Recognition (NER)**
* **Machine Learning**
* **Knowledge Graphs**
* **Pandas**
* **Excel/XLSX Processing**
* **PDF Text Extraction**
* **Streamlit** / Web-based UI

## 📁 Project Structure

```text
Drug-NER-Knowledge-Graph/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── cancer_drugs_side_effects_dataset.xlsx
│
├── models/
│   └── ner_model/
│
├── utils/
│   ├── preprocessing.py
│   ├── pdf_processing.py
│   └── knowledge_graph.py
│
├── assets/
│   └── screenshot.png
│
└── notebooks/
    └── model_training.ipynb
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Drug-NER-Knowledge-Graph
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

If the project uses Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧪 How to Use

### Step 1 — Upload Dataset

Upload an Excel file containing drug information.

The application displays a preview of the dataset and prepares the data for model training.

### Step 2 — Train the NER Model

Click **Train Model** to train the NER model using the uploaded dataset.

The dataset is divided into training and testing portions.

### Step 3 — Upload PDF

Upload a medical or research PDF containing drug-related information.

### Step 4 — Extract Entities

The trained NER model processes the extracted PDF text and identifies relevant drug-related entities.

### Step 5 — Build the Knowledge Graph

Extracted information is transformed into relationships between entities such as:

```text
Drug
 │
 ├── belongs to → Drug Class
 │
 ├── associated with → Cancer
 │
 └── has → Side Effect
```

## 🧠 Knowledge Graph Example

```text
Cisplatin
    │
    ├──────────────► Platinum Chemotherapy
    │
    ├──────────────► Lung Cancer
    │
    ├──────────────► Ovarian Cancer
    │
    ├──────────────► Bladder Cancer
    │
    ├──────────────► Nephrotoxicity
    │
    └──────────────► Nausea
```

This representation makes it easier to query and visualize relationships between medical entities.

## 📊 Dataset Split

The application provides a training/testing split for model development.

Example:

```text
Training Data : 80%
Testing Data  : 20%
```

The exact split may vary depending on the uploaded dataset and configuration.

## 🔬 Applications

This project can be useful for:

* Medical NLP research
* Drug information extraction
* Biomedical knowledge discovery
* Healthcare information systems
* Knowledge graph research
* NLP model experimentation
* Academic/research projects

## ⚠️ Limitations

* Model performance depends on the quality and size of the training dataset.
* Extracted entities may require validation.
* Medical terminology can be ambiguous and context-dependent.
* The knowledge graph represents information extracted from the provided data and documents.
* This project is intended for **research and educational purposes**, not clinical decision-making.

## 🔮 Future Enhancements

* [ ] Add advanced biomedical NER models
* [ ] Integrate transformer-based models such as BERT
* [ ] Improve entity normalization
* [ ] Add interactive knowledge graph visualization
* [ ] Add Neo4j integration
* [ ] Support additional document formats
* [ ] Add semantic search over extracted entities
* [ ] Add drug–drug relationship extraction
* [ ] Add confidence scores for extracted entities
* [ ] Add a question-answering interface over the knowledge graph

## 👩‍💻 Author

**Ananya Das**

B.Tech Computer Science & Engineering — AI/ML

### 🔗 Connect

* GitHub: [@ananya348](https://github.com/ananya348)
* LinkedIn: [Ananya Das](https://linkedin.com/in/ananyadas)

## 📄 License

This project is intended for educational and research purposes. Add the appropriate open-source license to the repository if you plan to distribute the project publicly.
