"""
Sentiment & Intent analysis page.

Displays sentiment distribution, intent classification,
timeline visualization, and per-statement breakdown.

Author: Koushik
Date: February 2026
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


def load_css():
    """Load custom CSS."""
    st.markdown("""
        <style>
            .page-header {
                background: linear-gradient(135deg, #9c27b0, #6a1b9a);
                color: white;
                padding: 18px 28px;
                border-radius: 12px;
                margin-bottom: 20px;
            }
            .page-header h2 { margin: 0; }
            .page-header p { margin: 4px 0 0; opacity: 0.85; }
            .sentiment-card {
                border-radius: 10px;
                padding: 14px 18px;
                margin-bottom: 10px;
            }
            .sent-anxious { background: #ffebee; border-left: 4px solid #f44336; }
            .sent-neutral { background: #f5f5f5; border-left: 4px solid #9e9e9e; }
            .sent-reassured { background: #e8f5e9; border-left: 4px solid #4caf50; }
            .sentiment-card .statement { color: #444; font-style: italic; margin: 6px 0 0; }
            .sentiment-card .meta { font-size: 0.82em; color: #777; margin-top: 4px; }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Main sentiment page."""
    load_css()

    st.markdown("""
        <div class="page-header">
            <h2>😊 Sentiment & Intent Analysis</h2>
            <p>Patient emotion tracking and conversation intent classification</p>
        </div>
    """, unsafe_allow_html=True)

    if 'pipeline_output' not in st.session_state:
        st.warning("⚠️ No results yet. Please go to the **Home** page, upload a transcript, and click **Process Transcript** first.")
        return

    output = st.session_state['pipeline_output']
    sentiment_data = output.get('sentiment_analysis', {})
    intent_data = output.get('intent_analysis', {})

    overall = sentiment_data.get('overall', {})
    distribution = overall.get('distribution', {})
    per_statement = sentiment_data.get('per_statement', [])
    timeline = sentiment_data.get('timeline', [])
    intent_dist = intent_data.get('distribution', {})
    intent_statements = intent_data.get('per_statement', [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="background:#ffebee; border-radius:10px; padding:16px; text-align:center;">
                <h3 style="margin:0; color:#f44336;">😰 Anxious</h3>
                <h2 style="margin:8px 0; color:#f44336;">{distribution.get('Anxious', 0)}</h2>
                <p style="margin:0; color:#777;">statements</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background:#f5f5f5; border-radius:10px; padding:16px; text-align:center;">
                <h3 style="margin:0; color:#757575;">😐 Neutral</h3>
                <h2 style="margin:8px 0; color:#757575;">{distribution.get('Neutral', 0)}</h2>
                <p style="margin:0; color:#777;">statements</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="background:#e8f5e9; border-radius:10px; padding:16px; text-align:center;">
                <h3 style="margin:0; color:#4caf50;">😊 Reassured</h3>
                <h2 style="margin:8px 0; color:#4caf50;">{distribution.get('Reassured', 0)}</h2>
                <p style="margin:0; color:#777;">statements</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("### 📊 Sentiment Distribution")
        labels = list(distribution.keys())
        values = list(distribution.values())
        colors = ['#f44336', '#9e9e9e', '#4caf50']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent'
        )])

        fig_pie.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=30, b=10),
            paper_bgcolor='white',
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col_chart2:
        st.markdown("### 🎯 Intent Distribution")
        intent_labels = [k for k, v in intent_dist.items() if v > 0]
        intent_values = [v for v in intent_dist.values() if v > 0]

        if intent_labels:
            fig_intent = go.Figure(go.Bar(
                x=intent_values,
                y=intent_labels,
                orientation='h',
                marker_color='#7c4dff'
            ))

            fig_intent.update_layout(
                height=300,
                margin=dict(l=160, r=30, t=30, b=30),
                plot_bgcolor='white',
                paper_bgcolor='white',
            )
            fig_intent.update_xaxes(showgrid=True, gridcolor='#eee')

            st.plotly_chart(fig_intent, use_container_width=True)

    st.markdown("---")

    st.markdown("### 📈 Sentiment Journey Timeline")
    if timeline:
        positions = [t['position'] for t in timeline]
        scores = [t['score'] for t in timeline]
        sentiments = [t['sentiment'] for t in timeline]
        colors_map = {'Anxious': '#f44336', 'Neutral': '#9e9e9e', 'Reassured': '#4caf50'}
        marker_colors = [colors_map.get(s, '#888') for s in sentiments]

        fig_timeline = go.Figure()

        fig_timeline.add_trace(go.Scatter(
            x=positions,
            y=scores,
            mode='lines+markers',
            marker=dict(
                size=14,
                color=marker_colors,
                line=dict(width=2, color='white')
            ),
            line=dict(color='#aaa', width=2),
            text=sentiments,
            hovertemplate='Statement %{x}<br>Sentiment: %{text}<extra></extra>'
        ))

        fig_timeline.update_layout(
            height=280,
            yaxis=dict(
                tickvals=[-1, 0, 1],
                ticktext=['😰 Anxious', '😐 Neutral', '😊 Reassured'],
                range=[-1.5, 1.5]
            ),
            xaxis_title="Statement Order",
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=120, r=30, t=30, b=40),
        )
        fig_timeline.update_xaxes(showgrid=True, gridcolor='#eee')
        fig_timeline.update_yaxes(showgrid=True, gridcolor='#eee')

        st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("---")

    st.markdown("### 💬 Statement-by-Statement Breakdown")

    sentiment_class_map = {
        'Anxious': 'sent-anxious',
        'Neutral': 'sent-neutral',
        'Reassured': 'sent-reassured',
    }

    sentiment_icon_map = {
        'Anxious': '😰',
        'Neutral': '😐',
        'Reassured': '😊',
    }

    for i, stmt in enumerate(per_statement):
        sent = stmt.get('sentiment', 'Neutral')
        css_class = sentiment_class_map.get(sent, 'sent-neutral')
        icon = sentiment_icon_map.get(sent, '😐')
        confidence = stmt.get('confidence', 0)

        intent_text = ""
        if i < len(intent_statements):
            intent_text = intent_statements[i].get('intent', '')

        st.markdown(f"""
            <div class="sentiment-card {css_class}">
                <strong>{icon} {sent}</strong>
                <span style="color:#888; font-size:0.85em;"> confidence: {confidence}</span>
                {f'<span style="background:#ede7f6; color:#5e35b1; padding:2px 10px; border-radius:12px; font-size:0.82em; margin-left:8px;">🎯 {intent_text}</span>' if intent_text else ''}
                <p class="statement">"{stmt.get('text', '')}"</p>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()