import streamlit as st
import pandas as pd
import spacy
import re
import random
import fitz
import networkx as nx
import matplotlib.pyplot as plt
import os

from spacy.training.example import Example
from spacy.scorer import Scorer
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Drug NER + KG", layout="wide")

st.title("💊 Drug NER + Knowledge Graph")

# =========================
# CACHE MODEL
# =========================
@st.cache_resource
def load_model(path):
    return spacy.load(path)

# =========================
# STEP 1: DATASET
# =========================
st.header("1️⃣ Upload Dataset")

uploaded_excel = st.file_uploader("Upload Excel Dataset", type=["xlsx"])

if uploaded_excel:
    df = pd.read_excel(uploaded_excel, engine="openpyxl")
    st.dataframe(df.head())

    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

    st.success(f"Train: {len(df_train)} | Test: {len(df_test)}")

    def split_semicolon(x):
        if pd.isna(x):
            return []
        return [t.strip() for t in str(x).split(";") if t.strip()]

    TEMPLATES = [
        "{DRUG} is used to treat {CANCERS} cancer and may cause {SIDEFX}.",
        "{DRUG} is indicated in {CANCERS} and can lead to {SIDEFX}.",
        "{DRUG} therapy in {CANCERS} patients may result in {SIDEFX}.",
        "In {CANCERS}, {DRUG} may cause adverse effects such as {SIDEFX}.",
    ]

    def build_training_data(df_in):
        data = []
        for _, row in df_in.iterrows():
            drug = str(row.get("Drug_Name", "")).strip()
            cancers = split_semicolon(row.get("Common_Cancers"))
            sidefx = split_semicolon(row.get("Major_Side_Effects"))

            if not drug:
                continue

            text = random.choice(TEMPLATES)\
                .replace("{DRUG}", drug)\
                .replace("{CANCERS}", ", ".join(cancers) if cancers else "cancer")\
                .replace("{SIDEFX}", "; ".join(sidefx) if sidefx else "side effects")

            entities = []

            for m in re.finditer(re.escape(drug), text):
                entities.append((m.start(), m.end(), "DRUG"))

            for c in cancers:
                for m in re.finditer(re.escape(c), text):
                    entities.append((m.start(), m.end(), "CANCER"))

            for s in sidefx:
                for m in re.finditer(re.escape(s), text):
                    entities.append((m.start(), m.end(), "SIDE_EFFECT"))

            if entities:
                data.append((text, {"entities": entities}))

        return data

    if st.button("🚀 Train Model"):

        train_data = build_training_data(df_train)
        test_data = build_training_data(df_test)

        nlp = spacy.load("en_core_web_sm")
        ner = nlp.get_pipe("ner")

        for label in ["DRUG", "CANCER", "SIDE_EFFECT"]:
            ner.add_label(label)

        optimizer = nlp.resume_training()

        with st.spinner("Training model..."):
            for epoch in range(10):
                random.shuffle(train_data)
                losses = {}

                for text, ann in train_data:
                    example = Example.from_dict(nlp.make_doc(text), ann)
                    nlp.update([example], drop=0.3, sgd=optimizer, losses=losses)

                st.write(f"Epoch {epoch+1} Loss: {losses.get('ner')}")

        MODEL_DIR = "drug_ner_model"
        nlp.to_disk(MODEL_DIR)

        st.success("✅ Model Trained & Saved")

        def evaluate(nlp, data):
            scorer = Scorer()
            examples = []
            for text, ann in data:
                doc = nlp(text)
                examples.append(Example.from_dict(doc, ann))
            return scorer.score(examples)

        scores = evaluate(nlp, test_data)

        st.subheader("📊 Evaluation")
        st.json(scores)

# =========================
# STEP 2: PDF
# =========================
st.header("2️⃣ Upload PDF")

uploaded_pdf = st.file_uploader("Upload PDF File", type=["pdf"])

if uploaded_pdf:
    pdf_path = "temp.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    def extract_text(pdf_path):
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    text = extract_text(pdf_path)
    text = re.sub(r"\n+", "\n", text)

    st.text_area("📄 Extracted Text Preview", text[:1000], height=200)

    if os.path.exists("drug_ner_model"):
        nlp = load_model("drug_ner_model")
        doc = nlp(text)

        drugs = sorted(set([e.text for e in doc.ents if e.label_ == "DRUG"]))
        cancers = sorted(set([e.text for e in doc.ents if e.label_ == "CANCER"]))
        sidefx = sorted(set([e.text for e in doc.ents if e.label_ == "SIDE_EFFECT"]))

        st.subheader("🔍 Extracted Entities")
        st.write("Drugs:", drugs)
        st.write("Cancers:", cancers)
        st.write("Side Effects:", sidefx)

        # =========================
        # BUILD KG
        # =========================
        def build_kg(doc):
            G = nx.Graph()

            for sent in doc.sents:
                ents = [(e.text, e.label_) for e in sent.ents]

                d = [t for t, l in ents if l == "DRUG"]
                c = [t for t, l in ents if l == "CANCER"]
                s = [t for t, l in ents if l == "SIDE_EFFECT"]

                for x in d:
                    for y in c:
                        if G.has_edge(x, y):
                            G[x][y]["weight"] += 1
                        else:
                            G.add_edge(x, y, relation="TREATS", weight=1)

                for x in d:
                    for y in s:
                        if G.has_edge(x, y):
                            G[x][y]["weight"] += 1
                        else:
                            G.add_edge(x, y, relation="CAUSES", weight=1)

            return G

        G = build_kg(doc)

        # =========================
        # CLEAN GRAPH VISUALIZATION
        # =========================
        st.subheader("📈 Knowledge Graph")

        if G.number_of_edges() > 0:

            st.info("Reduce relations if graph looks crowded")

            top_n = st.slider("Select number of relations", 5, 40, 20)

            edges_sorted = sorted(
                G.edges(data=True),
                key=lambda x: x[2].get("weight", 1),
                reverse=True
            )[:top_n]

            H = nx.Graph()
            for u, v, data in edges_sorted:
                H.add_edge(u, v, **data)

            pos = nx.spring_layout(H, k=2.2, iterations=100, seed=42)

            plt.figure(figsize=(16, 12))

            color_map = []
            for node in H.nodes():
                if node in drugs:
                    color_map.append("#4e79a7")
                elif node in cancers:
                    color_map.append("#e15759")
                else:
                    color_map.append("#f28e2b")

            nx.draw_networkx_nodes(H, pos, node_size=1800, node_color=color_map, alpha=0.95)

            widths = [1 + 0.8 * H[u][v].get("weight", 1) for u, v in H.edges()]
            nx.draw_networkx_edges(H, pos, width=widths, alpha=0.3)

            nx.draw_networkx_labels(
                H, pos,
                font_size=10,
                font_weight="bold",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1)
            )

            plt.title("Drug–Cancer–Side Effect Relations", fontsize=16)
            plt.axis("off")

            st.pyplot(plt)

        else:
            st.warning("❌ No relations found")

    else:
        st.error("⚠️ Train the model first!")
