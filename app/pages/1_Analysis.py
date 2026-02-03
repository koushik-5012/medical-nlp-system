"""
Analysis page - NER results and medical summary.

Displays extracted entities, diagnosis, prognosis,
temporal info, and medical keywords.

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
                background: linear-gradient(135deg, #1a73e8, #0d47a1);
                color: white;
                padding: 18px 28px;
                border-radius: 12px;
                margin-bottom: 20px;
            }
            .page-header h2 { margin: 0; }
            .page-header p { margin: 4px 0 0; opacity: 0.85; }
            .entity-tag { display: inline-block; padding: 5px 14px; border-radius: 20px; font-size: 0.88em; margin: 3px; }
            .tag-symptom { background: #ffcdd2; color: #c62828; }
            .tag-treatment { background: #c8e6c9; color: #2e7d32; }
            .tag-diagnosis { background: #bbdefb; color: #1565c0; }
            .tag-keyword { background: #e1bee5; color: #6a1b9a; }
            .tag-anatomy { background: #fff9c4; color: #f57f17; }
            .info-card {
                background: #f8fbff;
                border-radius: 10px;
                padding: 18px;
                border: 1px solid #e0ecff;
                margin-bottom: 12px;
            }
            .info-card h4 { margin: 0 0 8px; color: #1a73e8; }
            .confidence-high { color: #2e7d32; font-weight: bold; }
            .confidence-mid { color: #f57c00; font-weight: bold; }
            .confidence-low { color: #c62828; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)


def render_entity_tags(entities, tag_class):
    """Render entities as colored tags."""
    if not entities:
        return "<p style='color:#888; font-style:italic;'>None found</p>"
    tags = ''.join([f'<span class="entity-tag {tag_class}">{e}</span>' for e in entities])
    return tags


def main():
    """Main analysis page."""
    load_css()

    st.markdown("""
        <div class="page-header">
            <h2>📊 Medical Entity Analysis</h2>
            <p>Extracted entities, diagnosis, prognosis, and keywords</p>
        </div>
    """, unsafe_allow_html=True)

    if 'pipeline_output' not in st.session_state:
        st.warning("⚠️ No results yet. Please go to the **Home** page, upload a transcript, and click **Process Transcript** first.")
        return

    output = st.session_state['pipeline_output']
    summary = output.get('summary', {})
    entities = output.get('entities', {})
    temporal = output.get('temporal_info', {})
    keywords = output.get('keywords', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="info-card">
                <h4>👤 Patient Information</h4>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Name:** {summary.get('patient_name', 'Unknown')}")
        st.markdown(f"**Incident Date:** {temporal.get('dates', ['Not specified'])[0] if temporal.get('dates') else 'Not specified'}")
        st.markdown(f"**Times:** {', '.join(temporal.get('times', ['Not specified']))}")

    with col2:
        st.markdown("""
            <div class="info-card">
                <h4>🏥 Diagnosis & Prognosis</h4>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"**Diagnosis:** {summary.get('diagnosis', 'Not identified')}")
        st.markdown(f"**Prognosis:** {summary.get('prognosis', 'Not specified')}")

    st.markdown("---")

    st.markdown("### 🔴 Symptoms")
    symptoms = entities.get('symptoms', [])
    st.markdown(render_entity_tags(symptoms, 'tag-symptom'), unsafe_allow_html=True)

    st.markdown("### 💊 Treatments")
    treatments = entities.get('treatments', [])
    st.markdown(render_entity_tags(treatments, 'tag-treatment'), unsafe_allow_html=True)

    st.markdown("### 🧬 Anatomy")
    anatomy = entities.get('anatomy', [])
    st.markdown(render_entity_tags(anatomy, 'tag-anatomy'), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📋 Current Status")
    st.markdown(f"""
        <div class="info-card">
            <p>{summary.get('current_status', 'Not specified')}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.markdown("### 📅 Temporal Information")
        st.markdown(f"""
            <div class="info-card">
                <h4>📅 Dates</h4>
                <p>{', '.join(temporal.get('dates', ['None found']))}</p>
                <h4>⏱️ Durations</h4>
                <p>{', '.join(temporal.get('durations', ['None found']))}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown("### 🔑 Medical Keywords")
        medical_phrases = keywords.get('medical_phrases', [])
        st.markdown(render_entity_tags(medical_phrases, 'tag-keyword'), unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Top Keywords with Scores")
    top_keywords = keywords.get('top_keywords', [])

    if top_keywords:
        import plotly.graph_objects as go

        labels = [kw['keyword'] for kw in top_keywords[:10]]
        scores = [kw['score'] for kw in top_keywords[:10]]

        fig = go.Figure(go.Bar(
            x=scores,
            y=labels,
            orientation='h',
            marker_color=['#1a73e8' if s > 0.3 else '#90caf9' for s in scores]
        ))

        fig.update_layout(
            title="Keyword Relevance Scores",
            xaxis_title="Score",
            height=350,
            margin=dict(l=150, r=30, t=40, b=30),
            plot_bgcolor='white',
            paper_bgcolor='white',
        )
        fig.update_xaxes(showgrid=True, gridcolor='#eee')

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    with st.expander("📥 Download Full Analysis (JSON)"):
        import json
        st.download_button(
            label="📥 Download JSON",
            data=json.dumps(output, indent=2, default=str),
            file_name="analysis_results.json",
            mime="application/json"
        )


if __name__ == "__main__":
    main()