"""
Medical NLP Analysis System - Main Streamlit Application.

This is the main entry point for the web application.
Handles file upload, processing, and stores results
for other pages to access.

Author: Koushik
Date: February 2026
"""

import streamlit as st
import json
import os
import sys
import warnings
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Medical NLP Analysis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Medical NLP Transcription Analysis System v1.0"
    }
)


def load_css():
    """Load custom CSS styles."""
    st.markdown("""
        <style>
            .main-header {
                background: linear-gradient(135deg, #1a73e8, #0d47a1);
                color: white;
                padding: 20px 30px;
                border-radius: 12px;
                margin-bottom: 20px;
                text-align: center;
            }
            .main-header h1 {
                margin: 0;
                font-size: 2.2em;
            }
            .main-header p {
                margin: 5px 0 0 0;
                opacity: 0.85;
                font-size: 1em;
            }
            .stat-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-top: 4px solid #1a73e8;
            }
            .stat-card h3 {
                margin: 0;
                color: #1a73e8;
                font-size: 1.8em;
            }
            .stat-card p {
                margin: 5px 0 0 0;
                color: #555;
                font-size: 0.9em;
            }
            .section-box {
                background: #f8fbff;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                border: 1px solid #e0ecff;
            }
            .success-box {
                background: #e8f5e9;
                border-radius: 10px;
                padding: 15px 20px;
                border: 1px solid #c8e6c9;
                color: #2e7d32;
            }
            .warning-box {
                background: #fff3e0;
                border-radius: 10px;
                padding: 15px 20px;
                border: 1px solid #ffe0b2;
                color: #e65100;
            }
            .entity-tag {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                margin: 3px;
            }
            .tag-symptom { background: #ffcdd2; color: #c62828; }
            .tag-treatment { background: #c8e6c9; color: #2e7d32; }
            .tag-diagnosis { background: #bbdefb; color: #1565c0; }
            .tag-keyword { background: #e1bee5; color: #6a1b9a; }
            .stButton button {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                width: 100%;
            }
            .stButton button:hover {
                background-color: #1558b0;
            }
            sidebar .stButton button {
                background-color: #0d47a1;
            }
        </style>
    """, unsafe_allow_html=True)


def load_sample_transcript():
    """Load the sample transcript from data/raw/."""
    sample_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data', 'raw', 'sample_transcript.txt'
    )
    if os.path.exists(sample_path):
        with open(sample_path, 'r') as f:
            return f.read()
    return None


def initialize_pipeline():
    """Initialize the NLP pipeline (cached)."""
    if 'pipeline' not in st.session_state:
        with st.spinner("🔄 Loading NLP models... (first time only)"):
            from src.pipeline.medical_nlp_pipeline import MedicalNLPPipeline
            st.session_state['pipeline'] = MedicalNLPPipeline()
    return st.session_state['pipeline']


def main():
    """Main application layout and logic."""
    load_css()

    st.markdown("""
        <div class="main-header">
            <h1>🏥 Medical NLP Analysis System</h1>
            <p>AI-Powered Medical Transcription Analysis & Report Generation</p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 📂 Upload Transcript")
        uploaded_file = st.file_uploader(
            "Upload a medical transcript (.txt)",
            type=["txt"],
            help="Upload a doctor-patient conversation transcript"
        )

        st.markdown("---")
        st.markdown("### 📋 Or Use Sample")
        load_sample = st.button("📄 Load Sample Transcript")

        st.markdown("---")
        st.markdown("### ⚙️ Analysis Options")
        run_ner = st.checkbox("Named Entity Recognition", value=True)
        run_sentiment = st.checkbox("Sentiment Analysis", value=True)
        run_intent = st.checkbox("Intent Classification", value=True)
        run_soap = st.checkbox("SOAP Note Generation", value=True)

        st.markdown("---")
        st.markdown("### 📊 Navigation")
        st.markdown("""
            - 🏠 **Home** - Upload & Process
            - 📊 **Analysis** - NER & Summary
            - 📋 **SOAP Note** - Clinical Notes
            - 😊 **Sentiment** - Emotion Analysis
            - ℹ️ **About** - System Info
        """)

    transcript_text = None

    if uploaded_file is not None:
        transcript_text = uploaded_file.getvalue().decode("utf-8")
        st.session_state['raw_transcript'] = transcript_text
        st.markdown('<div class="success-box">✅ File uploaded successfully!</div>', unsafe_allow_html=True)

    elif load_sample:
        transcript_text = load_sample_transcript()
        if transcript_text:
            st.session_state['raw_transcript'] = transcript_text
            st.markdown('<div class="success-box">✅ Sample transcript loaded!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ Sample file not found.</div>', unsafe_allow_html=True)

    elif 'raw_transcript' in st.session_state:
        transcript_text = st.session_state['raw_transcript']

    if transcript_text:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 📝 Transcript Preview")
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            preview = transcript_text[:500] + "\n..." if len(transcript_text) > 500 else transcript_text
            st.text(preview)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown("### 📊 Quick Stats")
            lines = transcript_text.strip().split('\n')
            non_empty_lines = [l for l in lines if l.strip()]
            doctor_lines = [l for l in non_empty_lines if l.strip().lower().startswith(('physician', 'doctor'))]
            patient_lines = [l for l in non_empty_lines if l.strip().lower().startswith('patient')]
            word_count = len(transcript_text.split())

            st.markdown(f"""
                <div class="stat-card" style="margin-bottom:10px;">
                    <h3>{word_count}</h3><p>Total Words</p>
                </div>
                <div class="stat-card" style="margin-bottom:10px; border-top-color:#4caf50;">
                    <h3>{len(doctor_lines)}</h3><p>Doctor Turns</p>
                </div>
                <div class="stat-card" style="margin-bottom:10px; border-top-color:#ff9800;">
                    <h3>{len(patient_lines)}</h3><p>Patient Turns</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            process_btn = st.button("🔄 Process Transcript", key="process_btn")

        with col_btn2:
            if 'pipeline_output' in st.session_state:
                output_json = json.dumps(st.session_state['pipeline_output'], indent=2, default=str)
                st.download_button(
                    label="📥 Download Results (JSON)",
                    data=output_json,
                    file_name="medical_nlp_results.json",
                    mime="application/json"
                )

        if process_btn:
            pipeline = initialize_pipeline()

            with st.spinner("🧠 Analyzing transcript... This may take a moment."):
                progress_text = st.empty()
                progress_text.markdown("🔄 Starting analysis...")
                time.sleep(0.5)

                progress_text.markdown("🔍 Extracting entities...")
                time.sleep(0.3)

                progress_text.markdown("😊 Analyzing sentiment...")
                time.sleep(0.3)

                progress_text.markdown("🎯 Classifying intents...")
                time.sleep(0.3)

                progress_text.markdown("📝 Generating reports...")

                output = pipeline.process(transcript_text)
                st.session_state['pipeline_output'] = output

                progress_text.empty()

            st.markdown('<div class="success-box">✅ Analysis complete! Navigate to the pages on the left to see results.</div>', unsafe_allow_html=True)

            col_s1, col_s2, col_s3, col_s4 = st.columns(4)

            with col_s1:
                entity_count = sum(len(v) for v in output.get('entities', {}).values())
                st.markdown(f"""
                    <div class="stat-card">
                        <h3 style="color:#e53935;">{entity_count}</h3>
                        <p>Entities Found</p>
                    </div>
                """, unsafe_allow_html=True)

            with col_s2:
                st.markdown(f"""
                    <div class="stat-card">
                        <h3 style="color:#7b1fa2;">{output['sentiment_analysis']['overall']['dominant_sentiment']}</h3>
                        <p>Overall Sentiment</p>
                    </div>
                """, unsafe_allow_html=True)

            with col_s3:
                keyword_count = len(output.get('keywords', {}).get('medical_phrases', []))
                st.markdown(f"""
                    <div class="stat-card">
                        <h3 style="color:#1565c0;">{keyword_count}</h3>
                        <p>Medical Phrases</p>
                    </div>
                """, unsafe_allow_html=True)

            with col_s4:
                st.markdown(f"""
                    <div class="stat-card">
                        <h3 style="color:#2e7d32;">✓</h3>
                        <p>SOAP Note Ready</p>
                    </div>
                """, unsafe_allow_html=True)

    else:
        st.markdown("""
            <div class="section-box" style="text-align:center; padding:60px 20px;">
                <h2>👋 Welcome to Medical NLP Analysis</h2>
                <p style="color:#555; font-size:1.1em;">
                    Upload a medical transcript or load our sample to get started.
                </p>
                <br>
                <p style="color:#888;">
                    📂 Use the sidebar to upload a file<br>
                    📄 Or click "Load Sample Transcript"<br>
                    🔄 Then click "Process Transcript"
                </p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()