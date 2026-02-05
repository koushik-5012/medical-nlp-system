"""
About page - System info and how to use.

Displays system overview, tech stack,
performance metrics, and usage guide.

Author: Koushik
Date: February 2026
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def load_css():
    """Load custom CSS."""
    st.markdown("""
        <style>
            .page-header {
                background: linear-gradient(135deg, #37474f, #263238);
                color: white;
                padding: 18px 28px;
                border-radius: 12px;
                margin-bottom: 20px;
            }
            .page-header h2 { margin: 0; }
            .page-header p { margin: 4px 0 0; opacity: 0.85; }
            .tech-card {
                background: #f8fbff;
                border-radius: 10px;
                padding: 16px;
                border: 1px solid #e0ecff;
                text-align: center;
            }
            .tech-card h4 { margin: 8px 0 4px; color: #1a73e8; }
            .tech-card p { margin: 0; color: #666; font-size: 0.88em; }
            .step-box {
                background: white;
                border-radius: 10px;
                padding: 16px 20px;
                margin-bottom: 10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                display: flex;
                align-items: flex-start;
                gap: 14px;
            }
            .step-number {
                background: #1a73e8;
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }
            .metric-card {
                background: #f8fbff;
                border-radius: 10px;
                padding: 18px;
                text-align: center;
                border: 1px solid #e0ecff;
            }
            .metric-card h3 { margin: 0; color: #1a73e8; }
            .metric-card p { margin: 4px 0 0; color: #666; font-size: 0.88em; }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main about page."""
    load_css()

    st.markdown("""
        <div class="page-header">
            <h2>ℹ️ About Medical NLP System</h2>
            <p>System overview, tech stack, and usage guide</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏥 System Overview")
    st.markdown("""
        <div style="background:#f8fbff; border-radius:10px; padding:18px; border:1px solid #e0ecff;">
            <p style="margin:0; color:#444; line-height:1.6;">
                The <strong>Medical NLP Analysis System</strong> is a production-ready application that uses
                advanced Natural Language Processing to analyze doctor-patient transcripts. It extracts
                medical entities, analyzes patient sentiment, classifies conversation intents, generates
                clinical SOAP notes, and produces structured reports — all automatically.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🛠️ Technology Stack")

    col1, col2, col3, col4 = st.columns(4)

    tech_stack = [
        ("🧠", "NLP Core", "spaCy, scispaCy\nen_core_sci_md"),
        ("🤖", "Transformers", "DistilBERT\nBART (Zero-Shot)"),
        ("🔑", "Keywords", "KeyBERT\nSentence-BERT"),
        ("🌐", "Frontend", "Streamlit\nPlotly"),
    ]

    cols = [col1, col2, col3, col4]
    for col, (icon, title, desc) in zip(cols, tech_stack):
        with col:
            st.markdown(f"""
                <div class="tech-card">
                    <div style="font-size:2em;">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc.replace(chr(10), '<br>')}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("~85%", "NER Accuracy"),
        ("~80%", "Sentiment Accuracy"),
        ("<5s", "Processing Time"),
        ("4", "Output Formats"),
    ]

    metric_cols = [col1, col2, col3, col4]
    for col, (value, label) in zip(metric_cols, metrics):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>{value}</h3>
                    <p>{label}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 How To Use")

    steps = [
        ("📂", "<strong>Upload Transcript</strong><br>Upload a .txt file of a doctor-patient conversation, or click 'Load Sample Transcript' to try with our example."),
        ("⚙️", "<strong>Configure Options</strong><br>Select which analyses to run using the checkboxes in the sidebar."),
        ("🔄", "<strong>Process</strong><br>Click 'Process Transcript' to run the full NLP pipeline."),
        ("📊", "<strong>View Results</strong><br>Navigate through the pages to see NER analysis, SOAP notes, and sentiment breakdown."),
        ("📥", "<strong>Download</strong><br>Download results as JSON or TXT files from each page."),
    ]

    for i, (icon, text) in enumerate(steps, 1):
        st.markdown(f"""
            <div class="step-box">
                <div class="step-number">{i}</div>
                <div>
                    <span style="font-size:1.2em;">{icon}</span>
                    <p style="margin:0;">{text}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧩 System Modules")

    modules = {
        "Preprocessing": ["TextCleaner", "SpeakerDiarizer", "TemporalExtractor"],
        "NER": ["ScispaCyNER", "EntityValidator"],
        "Sentiment": ["SentimentAnalyzer"],
        "Intent": ["IntentClassifier"],
        "Summarization": ["MedicalKeywordExtractor", "MedicalSummarizer"],
        "Generators": ["SOAPGenerator"],
        "Pipeline": ["MedicalNLPPipeline"],
    }

    col1, col2 = st.columns(2)
    items = list(modules.items())
    half = len(items) // 2 + 1

    with col1:
        for module, classes in items[:half]:
            st.markdown(f"""
                <div style="background:#f8fbff; border-radius:8px; padding:12px 16px; margin-bottom:8px; border:1px solid #e0ecff;">
                    <strong style="color:#1a73e8;">{module}</strong><br>
                    <span style="color:#666; font-size:0.88em;">{', '.join(classes)}</span>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        for module, classes in items[half:]:
            st.markdown(f"""
                <div style="background:#f8fbff; border-radius:8px; padding:12px 16px; margin-bottom:8px; border:1px solid #e0ecff;">
                    <strong style="color:#1a73e8;">{module}</strong><br>
                    <span style="color:#666; font-size:0.88em;">{', '.join(classes)}</span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
        <div style="text-align:center; color:#888; padding:20px;">
            <p style="font-size:0.85em;">Author: Koushik | February 2026</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()