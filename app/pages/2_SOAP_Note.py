"""
SOAP Note page - Clinical note display.

Displays the generated SOAP note in formatted
and JSON views with download options.

Author: Koushik
Date: February 2026
"""

import streamlit as st
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def load_css():
    """Load custom CSS."""
    st.markdown("""
        <style>
            .page-header {
                background: linear-gradient(135deg, #4caf50, #2e7d32);
                color: white;
                padding: 18px 28px;
                border-radius: 12px;
                margin-bottom: 20px;
            }
            .page-header h2 { margin: 0; }
            .page-header p { margin: 4px 0 0; opacity: 0.85; }
            .soap-section {
                border-radius: 10px;
                padding: 18px 22px;
                margin-bottom: 16px;
            }
            .soap-S { background: #e3f2fd; border-left: 5px solid #1a73e8; }
            .soap-O { background: #e8f5e9; border-left: 5px solid #4caf50; }
            .soap-A { background: #fff3e0; border-left: 5px solid #ff9800; }
            .soap-P { background: #f3e5f5; border-left: 5px solid #9c27b0; }
            .soap-section h3 { margin: 0 0 10px; }
            .soap-section p { margin: 6px 0; color: #444; }
            .soap-label { font-weight: bold; color: #333; }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main SOAP page."""
    load_css()

    st.markdown("""
        <div class="page-header">
            <h2>📋 SOAP Clinical Note</h2>
            <p>Subjective • Objective • Assessment • Plan</p>
        </div>
    """, unsafe_allow_html=True)

    if 'pipeline_output' not in st.session_state:
        st.warning("⚠️ No results yet. Please go to the **Home** page, upload a transcript, and click **Process Transcript** first.")
        return

    view_mode = st.radio(
        "📄 View Mode",
        ["Formatted View", "JSON View"],
        horizontal=True
    )

    output = st.session_state['pipeline_output']
    transcript = st.session_state.get('raw_transcript', '')

    from src.generators.soap_generator import SOAPGenerator
    generator = SOAPGenerator()
    dialogues = generator.diarizer.parse_transcript(transcript)
    soap = generator.generate(transcript, dialogues)

    if view_mode == "Formatted View":
        st.markdown("""
            <div class="soap-section soap-S">
                <h3>📝 S — Subjective</h3>
                <p><span class="soap-label">Chief Complaint:</span><br>{chief_complaint}</p>
                <p><span class="soap-label">History of Present Illness:</span><br>{history}</p>
                <p><span class="soap-label">Review of Systems:</span><br>{ros}</p>
            </div>
        """.format(
            chief_complaint=soap['subjective']['chief_complaint'],
            history=soap['subjective']['history_of_present_illness'],
            ros=soap['subjective']['review_of_systems']
        ), unsafe_allow_html=True)

        st.markdown("""
            <div class="soap-section soap-O">
                <h3>🔬 O — Objective</h3>
                <p><span class="soap-label">Physical Examination:</span><br>{exam}</p>
                <p><span class="soap-label">Vital Signs:</span><br>{vitals}</p>
                <p><span class="soap-label">Observations:</span><br>{obs}</p>
            </div>
        """.format(
            exam=soap['objective']['physical_examination'],
            vitals=soap['objective']['vital_signs'],
            obs='<br>'.join([f'• {o}' for o in soap['objective']['observations']])
        ), unsafe_allow_html=True)

        st.markdown("""
            <div class="soap-section soap-A">
                <h3>📊 A — Assessment</h3>
                <p><span class="soap-label">Primary Diagnosis:</span> {diagnosis}</p>
                <p><span class="soap-label">Severity:</span> {severity}</p>
                <p><span class="soap-label">Prognosis:</span> {prognosis}</p>
            </div>
        """.format(
            diagnosis=soap['assessment']['primary_diagnosis'],
            severity=soap['assessment']['severity'],
            prognosis=soap['assessment']['prognosis']
        ), unsafe_allow_html=True)

        st.markdown("""
            <div class="soap-section soap-P">
                <h3>📝 P — Plan</h3>
                <p><span class="soap-label">Treatment Plan:</span><br>{treatment}</p>
                <p><span class="soap-label">Medications:</span><br>{meds}</p>
                <p><span class="soap-label">Follow-up:</span><br>{followup}</p>
                <p><span class="soap-label">Patient Education:</span><br>{edu}</p>
            </div>
        """.format(
            treatment=soap['plan']['treatment_plan'],
            meds='<br>'.join([f'• {m}' for m in soap['plan']['medications']]),
            followup=soap['plan']['follow_up'],
            edu='<br>'.join([f'• {e}' for e in soap['plan']['patient_education']])
        ), unsafe_allow_html=True)

    else:
        st.json(soap)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📥 Download SOAP (JSON)",
            data=json.dumps(soap, indent=2),
            file_name="soap_note.json",
            mime="application/json"
        )

    with col2:
        formatted_text = generator.to_formatted_text(soap)
        st.download_button(
            label="📥 Download SOAP (TXT)",
            data=formatted_text,
            file_name="soap_note.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()