#!/usr/bin/env python3
"""
AI Research Workspace - Unified Beautiful Interface
Real collaborative multi-agent research platform with stunning UI
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime
import json
import uuid
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'research_workspace'))

# Import the enhanced research system
from research_workspace.core.enhanced_research_engine import EnhancedResearchEngine
from research_workspace.core.agent_collaboration import AgentCollaborationManager
from research_workspace.agents import AVAILABLE_AGENTS

# Import enhanced display functions
from enhanced_display_functions import display_enhanced_research_results, generate_enhanced_pdf_report

# Page configuration
st.set_page_config(
    page_title="AI Research Workspace",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for stunning UI
st.markdown("""
<style>
    /* Main theme */
    .main {
        background: linear-gradient(135deg, #0D1117 0%, #161B22 100%);
        color: #F0F6FC;
    }

    .stApp {
        background: linear-gradient(135deg, #0D1117 0%, #161B22 100%);
    }

    /* Animated header orb */
    .research-orb {
        width: 160px;
        height: 160px;
        border-radius: 50%;
        background: radial-gradient(circle, #FF6B6B 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
        margin: 2rem auto;
        animation: researchGlow 5s ease-in-out infinite alternate;
        box-shadow: 0 0 50px rgba(255, 107, 107, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        position: relative;
    }

    .research-orb::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: radial-gradient(circle, transparent 30%, rgba(255, 107, 107, 0.3) 70%);
        animation: orbPulse 3s infinite;
    }

    @keyframes researchGlow {
        0% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.6), 0 0 60px rgba(78, 205, 196, 0.3); }
        25% { box-shadow: 0 0 40px rgba(78, 205, 196, 0.6), 0 0 70px rgba(69, 183, 209, 0.3); }
        50% { box-shadow: 0 0 45px rgba(69, 183, 209, 0.6), 0 0 80px rgba(150, 206, 180, 0.3); }
        75% { box-shadow: 0 0 40px rgba(150, 206, 180, 0.6), 0 0 70px rgba(255, 234, 167, 0.3); }
        100% { box-shadow: 0 0 35px rgba(255, 234, 167, 0.8), 0 0 60px rgba(255, 107, 107, 0.4); }
    }

    @keyframes orbPulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 0.4; }
    }

    /* Header text */
    .workspace-title {
        font-size: 3.2rem;
        font-weight: 900;
        color: #F0F6FC;
        margin: 1rem 0;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
    }

    .workspace-subtitle {
        font-size: 1.4rem;
        color: #8B949E;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 300;
    }

    /* Agent cards */
    .agent-card {
        background: linear-gradient(135deg, #21262D 0%, #30363D 100%);
        border: 2px solid #30363D;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        transition: all 0.4s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }

    .agent-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 107, 107, 0.1), transparent);
        transition: left 0.6s;
    }

    .agent-card:hover::before {
        left: 100%;
    }

    .agent-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.3);
        border-color: #FF6B6B;
    }

    .agent-card.selected {
        border-color: #4ECDC4;
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(69, 183, 209, 0.1) 100%);
        transform: translateY(-8px);
    }

    .agent-icon {
        font-size: 3.5rem;
        margin-bottom: 0.8rem;
        display: block;
    }

    .agent-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #F0F6FC;
        margin-bottom: 0.5rem;
    }

    .agent-specialty {
        font-size: 1rem;
        color: #4ECDC4;
        font-weight: 500;
    }

    /* Research interface */
    .research-interface {
        background: linear-gradient(135deg, #21262D 0%, #30363D 100%);
        border: 2px solid #30363D;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }

    /* Progress animations */
    .progress-container {
        background: linear-gradient(135deg, #21262D 0%, #30363D 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
    }

    .agent-working {
        display: inline-block;
        margin: 0.5rem;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        border-radius: 25px;
        color: white;
        font-weight: 600;
        animation: agentPulse 2s infinite;
    }

    @keyframes agentPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }

    /* Results container */
    .results-container {
        background: linear-gradient(135deg, #21262D 0%, #30363D 100%);
        border: 2px solid #30363D;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }

    /* Synthesis highlight */
    .synthesis-highlight {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(78, 205, 196, 0.15) 100%);
        border: 2px solid rgba(255, 107, 107, 0.4);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.6);
    }

    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
    }

    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, #21262D 0%, #30363D 100%);
        border: 1px solid #30363D;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin: 0.5rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #21262D 0%, #161B22 100%);
    }

    /* Collaboration log */
    .collaboration-message {
        background: linear-gradient(135deg, #30363D 0%, #21262D 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4ECDC4;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'collaboration_manager' not in st.session_state:
        st.session_state.collaboration_manager = AgentCollaborationManager()

    if 'research_engine' not in st.session_state:
        st.session_state.research_engine = EnhancedResearchEngine()

    if 'research_history' not in st.session_state:
        st.session_state.research_history = []

    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = str(uuid.uuid4())

    if 'selected_agents' not in st.session_state:
        st.session_state.selected_agents = []

def render_header():
    """Render the stunning header"""
    greeting, time_emoji = get_time_greeting()

    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <div class="research-orb">🤖</div>
        <div class="workspace-title">AI Research Workspace</div>
        <div class="workspace-subtitle">{greeting}! {time_emoji} Collaborative Intelligence at Work</div>
    </div>
    """, unsafe_allow_html=True)

def get_time_greeting():
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning", "🌅"
    elif 12 <= hour < 17:
        return "Good afternoon", "☀️"
    elif 17 <= hour < 22:
        return "Good evening", "🌆"
    else:
        return "Good night", "🌙"

def render_agent_selection():
    """Render the beautiful agent selection interface"""
    st.markdown("### 🎯 Choose Your Research Agents")

    # Create responsive grid
    cols = st.columns(4)

    for idx, (agent_id, agent_info) in enumerate(AVAILABLE_AGENTS.items()):
        with cols[idx % 4]:
            # Check if agent is selected
            is_selected = agent_id in st.session_state.selected_agents

            # Create clickable agent card
            card_class = "agent-card selected" if is_selected else "agent-card"

            st.markdown(f"""
            <div class="{card_class}" onclick="toggleAgent('{agent_id}')">
                <div class="agent-icon">{agent_info['icon']}</div>
                <div class="agent-name">{agent_info['name']}</div>
                <div class="agent-specialty">{agent_info['specialty']}</div>
            </div>
            """, unsafe_allow_html=True)

            # Agent selection checkbox
            if st.checkbox(f"Select {agent_info['name']}", key=f"select_{agent_id}", value=is_selected):
                if agent_id not in st.session_state.selected_agents:
                    st.session_state.selected_agents.append(agent_id)
            else:
                if agent_id in st.session_state.selected_agents:
                    st.session_state.selected_agents.remove(agent_id)

            # Agent details in expander
            with st.expander(f"🔍 {agent_info['name']} Details"):
                st.markdown(f"**Description:** {agent_info['description']}")
                st.markdown("**Capabilities:**")
                for capability in agent_info['use_cases'][:3]:
                    st.markdown(f"• {capability}")
                st.markdown(f"**Keywords:** {', '.join(agent_info['keywords'][:5])}")

def render_query_interface():
    """Render the research query interface"""
    st.markdown('<div class="research-interface">', unsafe_allow_html=True)

    st.markdown("### 💬 Enter Your Research Query")

    # Query input
    query = st.text_area(
        "What would you like to research?",
        placeholder="Example: 'Should I invest in renewable energy companies?' or 'Latest treatments for Type 2 diabetes?'",
        height=120
    )

    # Auto-suggest agents based on query
    if query and len(query) > 10:
        suggested_agents = suggest_agents_for_query(query)
        if suggested_agents:
            st.markdown("**💡 Suggested Agents:**")
            suggestion_cols = st.columns(len(suggested_agents))

            for idx, agent_id in enumerate(suggested_agents):
                with suggestion_cols[idx]:
                    agent_info = AVAILABLE_AGENTS[agent_id]
                    if st.button(f"{agent_info['icon']} {agent_info['name']}", key=f"suggest_{agent_id}"):
                        if agent_id not in st.session_state.selected_agents:
                            st.session_state.selected_agents.append(agent_id)
                            st.rerun()

    # Collaboration mode
    if len(st.session_state.selected_agents) > 1:
        st.markdown("### ⚙️ Collaboration Mode")
        collaboration_mode = st.radio(
            "How should the agents work together?",
            ["parallel", "sequential"],
            help="Parallel: Agents work simultaneously. Sequential: Agents build on each other's findings.",
            horizontal=True
        )
    else:
        collaboration_mode = "parallel"

    # Execute button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button(
            "🚀 START RESEARCH",
            type="primary",
            disabled=not query or not st.session_state.selected_agents,
            use_container_width=True
        ):
            execute_research(query, st.session_state.selected_agents, collaboration_mode)

    st.markdown('</div>', unsafe_allow_html=True)

def suggest_agents_for_query(query: str) -> List[str]:
    """Suggest relevant agents based on query analysis"""
    query_lower = query.lower()
    agent_scores = {}

    for agent_id, agent_info in AVAILABLE_AGENTS.items():
        score = 0

        # Check keywords
        for keyword in agent_info['keywords']:
            if keyword in query_lower:
                score += 1

        # Check use cases
        for use_case in agent_info['use_cases']:
            use_case_words = use_case.lower().split()
            for word in use_case_words:
                if word in query_lower and len(word) > 3:
                    score += 0.5

        agent_scores[agent_id] = score

    # Return top 3 agents with score > 0
    sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
    return [agent_id for agent_id, score in sorted_agents if score > 0][:3]

def execute_research(query: str, selected_agents: List[str], collaboration_mode: str):
    """Execute the research with real agent collaboration"""

    # Create session
    session_id = str(uuid.uuid4())

    # Progress container
    progress_container = st.container()

    with progress_container:
        st.markdown('<div class="progress-container">', unsafe_allow_html=True)
        st.markdown("### 🔄 AI Research in Progress...")

        # Show working agents
        agent_pills = ""
        for agent_id in selected_agents:
            agent_info = AVAILABLE_AGENTS[agent_id]
            agent_pills += f'<span class="agent-working">{agent_info["icon"]} {agent_info["name"]}</span>'

        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <p style="color: #8B949E; text-align: center;">Agents working on your research:</p>
            <div style="text-align: center;">{agent_pills}</div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Step 1: Initialize collaboration
            status_text.text("🚀 Initializing agent collaboration...")
            time.sleep(1)
            progress_bar.progress(0.1)

            session = st.session_state.collaboration_manager.start_collaboration_session(
                session_id, selected_agents, query
            )

            # Step 2: Execute collaborative research
            status_text.text("🔍 Agents performing research...")
            progress_bar.progress(0.3)

            result = st.session_state.collaboration_manager.execute_collaborative_research(
                session_id, collaboration_mode
            )

            # Progress updates
            for i, agent_id in enumerate(selected_agents):
                agent_info = AVAILABLE_AGENTS[agent_id]
                status_text.text(f"🤖 {agent_info['name']} completed research...")
                progress_bar.progress(0.4 + (i + 1) * 0.4 / len(selected_agents))
                time.sleep(0.8)

            # Execute comprehensive research using Enhanced engine (optimized for speed)
            result = st.session_state.research_engine.comprehensive_research(query, num_sub_questions=2)

            if not result['success']:
                st.error(f"Research failed: {result.get('error', 'Unknown error')}")
                return

            progress_bar.progress(1.0)
            status_text.text("✅ Enhanced research completed successfully!")
            time.sleep(1)

            # Store results
            st.session_state.research_history.append({
                'query': query,
                'agents': ['enhanced_galileo'],
                'result': result,
                'timestamp': datetime.now(),
                'enhanced_mode': True
            })

            st.markdown('</div>', unsafe_allow_html=True)

            # Clear progress and show results
            progress_container.empty()
            display_enhanced_research_results(result, query)

        except Exception as e:
            st.error(f"❌ Research failed: {str(e)}")
            print(f"Research error: {e}")

def display_research_results(result: Dict[str, Any], query: str, agents: List[str]):
    """Display comprehensive research results"""

    st.markdown("## 📊 Research Results")

    # Main comprehensive report - check for collaborative synthesis
    synthesis_text = ""
    if result.get('synthesized_result', {}).get('detailed_synthesis'):
        synthesis_text = result['synthesized_result']['detailed_synthesis']
    elif result.get('individual_results') and len(agents) == 1:
        # Single agent result
        agent_id = agents[0]
        agent_result = result['individual_results'][agent_id]
        synthesis_text = agent_result.get('analysis', '')
    elif result.get('synthesis'):
        synthesis_text = result['synthesis']
    elif result.get('analysis'):
        synthesis_text = result['analysis']

    if synthesis_text:
        st.markdown("### 📋 Comprehensive Report")
        # Add source links directly in the report
        if result.get('individual_results'):
            all_sources = []
            for agent_id in agents:
                agent_result = result['individual_results'].get(agent_id, {})
                agent_sources = agent_result.get('sources', [])
                all_sources.extend(agent_sources)

            # Add sources at the end of the report
            synthesis_with_sources = synthesis_text + "\n\n## 📚 Sources\n\n"
            for i, source in enumerate(all_sources[:50], 1):
                title = source.get('title', 'Source')
                url = source.get('link', source.get('url', '#'))
                synthesis_with_sources += f"{i}. [{title}]({url})\n"

            st.markdown(synthesis_with_sources)
        else:
            st.markdown(synthesis_text)


    # Simple analytics
    render_analytics_dashboard(result, agents)

    # Export options
    render_export_options(result, query, agents)


def render_analytics_dashboard(result: Dict[str, Any], agents: List[str]):
    """Render simplified analytics dashboard"""
    col1, col2, col3 = st.columns(3)

    # Count total sources from all agents
    total_sources = 0
    if result.get('individual_results'):
        for agent_id in agents:
            agent_result = result['individual_results'].get(agent_id, {})
            agent_sources = agent_result.get('sources', [])
            total_sources += len(agent_sources)

    with col1:
        st.metric("📊 Total Sources", total_sources)

    with col2:
        # Get confidence from synthesis or average from agents
        confidence = 0.8  # default
        if result.get('synthesized_result', {}).get('confidence_assessment'):
            confidence = result['synthesized_result']['confidence_assessment']
        elif result.get('individual_results'):
            confidences = []
            for agent_id in agents:
                agent_result = result['individual_results'].get(agent_id, {})
                confidences.append(agent_result.get('confidence', 0.8))
            confidence = sum(confidences) / len(confidences) if confidences else 0.8

        st.metric("🎯 Confidence", f"{confidence * 100:.1f}%")

    with col3:
        processing_time = result.get('processing_time', 0)
        st.metric("⚡ Processing Time", f"{processing_time:.1f}s")

def render_export_options(result: Dict[str, Any], query: str, agents: List[str]):
    """Render export options including Google Docs"""

    st.markdown("### 📤 Export Research Results")

    col1, col2, col3 = st.columns(3)

    # Create unique keys based on session state
    if 'button_counter' not in st.session_state:
        st.session_state.button_counter = 0

    st.session_state.button_counter += 1
    unique_id = st.session_state.button_counter

    with col1:
        # Generate comprehensive PDF report
        pdf_data = generate_comprehensive_pdf_report(result, query, agents)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_data,
            file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            key=f"download_pdf_report_{unique_id}"
        )

    with col2:
        # Generate JSON data
        json_data = json.dumps(result, indent=2, default=str)
        st.download_button(
            label="📊 Download JSON Data",
            data=json_data,
            file_name=f"research_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key=f"download_json_data_{unique_id}"
        )

    # Remove the export button since we now have direct PDF download

def generate_comprehensive_pdf_report(result: Dict[str, Any], query: str, agents: List[str]) -> bytes:
    """Export research results to professional PDF"""
    st.write("🚀 Starting PDF export...")
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
        from datetime import datetime
        import io

        # Get synthesis
        synthesis_text = ""
        if result.get('synthesized_result', {}).get('detailed_synthesis'):
            synthesis_text = result['synthesized_result']['detailed_synthesis']
        elif result.get('individual_results') and len(agents) == 1:
            agent_id = agents[0]
            agent_result = result['individual_results'][agent_id]
            synthesis_text = agent_result.get('analysis', '')

        # Get all sources
        all_sources = []
        if result.get('individual_results'):
            for agent_id in agents:
                agent_result = result['individual_results'].get(agent_id, {})
                agent_sources = agent_result.get('sources', [])
                all_sources.extend(agent_sources)

        # Create PDF buffer
        buffer = io.BytesIO()

        # Create PDF document
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1f4e79'),
            alignment=1  # Center alignment
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#2c5282'),
            spaceBefore=20
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            leading=14
        )

        # Build PDF content
        story = []

        # Title
        story.append(Paragraph(f"AI Research Report: {query}", title_style))
        story.append(Spacer(1, 20))

        # Metadata
        agents_names = [AVAILABLE_AGENTS[agent_id]['name'] for agent_id in agents]
        story.append(Paragraph(f"<b>Research Agents:</b> {', '.join(agents_names)}", normal_style))
        story.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
        story.append(Paragraph(f"<b>Sources Analyzed:</b> {len(all_sources)} sources", normal_style))
        story.append(Spacer(1, 30))

        # Executive Summary Section
        story.append(Paragraph("Executive Summary", heading_style))
        if synthesis_text:
            summary_lines = synthesis_text.split('\n')[:5]  # First 5 lines as summary
            summary = ' '.join([line.strip() for line in summary_lines if line.strip()])
            story.append(Paragraph(summary, normal_style))
        story.append(Spacer(1, 20))

        # Individual Agent Analysis
        if result.get('individual_results'):
            story.append(Paragraph("Detailed Agent Analysis", heading_style))

            for agent_id in agents:
                agent_result = result['individual_results'].get(agent_id, {})
                agent_name = AVAILABLE_AGENTS[agent_id]['name']

                story.append(Paragraph(f"{agent_name} Analysis",
                    ParagraphStyle('AgentHeading', parent=heading_style, fontSize=14, spaceAfter=8)))

                agent_analysis = agent_result.get('analysis', '')
                if agent_analysis:
                    # Split into paragraphs and format
                    paragraphs = agent_analysis.split('\n')
                    for para in paragraphs:
                        if para.strip():
                            if para.startswith('#'):
                                clean_para = para.replace('#', '').strip()
                                story.append(Paragraph(clean_para,
                                    ParagraphStyle('SubHeading', parent=normal_style, fontSize=12, fontWeight='bold')))
                            else:
                                story.append(Paragraph(para.strip(), normal_style))

                # Agent-specific sources
                agent_sources = agent_result.get('sources', [])
                if agent_sources:
                    story.append(Paragraph(f"{agent_name} Sources:",
                        ParagraphStyle('SourceHeading', parent=normal_style, fontSize=10, fontWeight='bold')))
                    for i, source in enumerate(agent_sources[:10], 1):
                        source_title = source.get('title', 'Unknown Source')
                        source_url = source.get('link', source.get('url', ''))
                        story.append(Paragraph(f"{i}. {source_title}<br/><font size='8'>{source_url}</font>",
                            ParagraphStyle('SourceText', parent=normal_style, fontSize=9, leftIndent=20)))

                story.append(Spacer(1, 15))

        # Comprehensive Sources section
        if all_sources:
            story.append(PageBreak())
            story.append(Paragraph("Complete Source Bibliography", heading_style))
            story.append(Paragraph(f"Total sources analyzed: {len(all_sources)}", normal_style))
            story.append(Spacer(1, 10))

            # Group sources by domain
            domain_sources = {}
            for source in all_sources:
                url = source.get('link', source.get('url', ''))
                if url:
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(url).netloc
                        if domain not in domain_sources:
                            domain_sources[domain] = []
                        domain_sources[domain].append(source)
                    except:
                        pass

            for domain, sources in domain_sources.items():
                story.append(Paragraph(f"<b>{domain}</b> ({len(sources)} sources)",
                    ParagraphStyle('DomainHeading', parent=normal_style, fontSize=11, fontWeight='bold', spaceAfter=5)))

                for i, source in enumerate(sources, 1):
                    source_title = source.get('title', 'Unknown Source')
                    source_url = source.get('link', source.get('url', ''))
                    story.append(Paragraph(f"{i}. {source_title}<br/><font size='8'>{source_url}</font>",
                        ParagraphStyle('DomainSourceText', parent=normal_style, fontSize=9, leftIndent=15, spaceAfter=3)))

                story.append(Spacer(1, 10))

        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("Generated by AI Research Workspace",
                               ParagraphStyle('Footer', parent=normal_style, fontSize=9, textColor=HexColor('#666666'), alignment=1)))

        # Build PDF
        doc.build(story)

        # Get PDF data
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        return pdf_data

    except Exception as e:
        st.error(f"❌ PDF generation failed: {str(e)}")
        st.info("💡 Make sure reportlab is installed: `pip install reportlab`")
        return b""

def generate_markdown_report(result: Dict[str, Any], query: str, agents: List[str]) -> str:
    """Generate professional markdown report"""

    report_lines = [
        f"# AI Research Report",
        f"",
        f"**Query:** {query}",
        f"**Date:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}",
        f"**Agents Used:** {', '.join([AVAILABLE_AGENTS[agent_id]['name'] for agent_id in agents])}",
        f"**Processing Time:** {result.get('processing_time', 0):.2f} seconds",
        f"",
        f"---",
        f""
    ]

    # Executive summary
    if result.get('synthesized_result', {}).get('executive_summary'):
        report_lines.extend([
            f"## Executive Summary",
            f"",
            f"{result['synthesized_result']['executive_summary']}",
            f""
        ])

    # Key findings
    if result.get('synthesized_result', {}).get('key_findings'):
        report_lines.extend([
            f"## Key Findings",
            f""
        ])
        for finding in result['synthesized_result']['key_findings']:
            report_lines.append(f"• {finding}")
        report_lines.append("")

    # Individual agent analyses
    report_lines.extend([
        f"## Individual Agent Analyses",
        f""
    ])

    for agent_id in agents:
        agent_info = AVAILABLE_AGENTS[agent_id]
        agent_result = result.get('individual_results', {}).get(agent_id, {})

        report_lines.extend([
            f"### {agent_info['icon']} {agent_info['name']}",
            f"",
            f"**Confidence:** {agent_result.get('confidence', 0.7):.1%}",
            f"**Sources Found:** {len(agent_result.get('sources', []))}",
            f"",
            f"**Summary:**",
            f"{agent_result.get('executive_summary', 'No summary available')}",
            f""
        ])

        if agent_result.get('key_insights'):
            report_lines.extend([
                f"**Key Insights:**",
                f""
            ])
            for insight in agent_result['key_insights']:
                report_lines.append(f"• {insight}")
            report_lines.append("")

    # Sources
    all_sources = set()
    for agent_id in agents:
        agent_result = result.get('individual_results', {}).get(agent_id, {})
        all_sources.update(agent_result.get('sources', []))

    if all_sources:
        report_lines.extend([
            f"## Sources",
            f""
        ])
        for idx, source in enumerate(sorted(all_sources), 1):
            report_lines.append(f"{idx}. {source}")

    report_lines.extend([
        f"",
        f"---",
        f"*Generated by AI Research Workspace - Collaborative Intelligence*"
    ])

    return "\n".join(report_lines)

def render_sidebar():
    """Render enhanced sidebar"""
    with st.sidebar:
        st.markdown("### 🔧 Workspace Controls")

        # Current session info
        st.markdown(f"**Session:** {st.session_state.current_session_id[:8]}...")

        # Research history
        st.markdown("#### 📜 Recent Research")

        if st.session_state.research_history:
            for idx, entry in enumerate(reversed(st.session_state.research_history[-3:])):
                with st.expander(f"Query {len(st.session_state.research_history) - idx}"):
                    st.markdown(f"**Query:** {entry['query'][:50]}...")
                    # Handle enhanced_galileo agent display
                    if entry.get('enhanced_mode'):
                        st.markdown(f"**Agents:** Enhanced Research Engine (Planner + Scout + Analyst + Writer)")
                    else:
                        agent_names = []
                        for agent_id in entry['agents']:
                            if agent_id in AVAILABLE_AGENTS:
                                agent_names.append(AVAILABLE_AGENTS[agent_id]['name'])
                            else:
                                agent_names.append(agent_id.replace('_', ' ').title())
                        st.markdown(f"**Agents:** {', '.join(agent_names)}")
                    st.markdown(f"**Time:** {entry['timestamp'].strftime('%H:%M:%S')}")
        else:
            st.info("No research history yet")

        # Quick actions
        st.markdown("#### ⚡ Quick Actions")

        if st.button("🆕 New Session"):
            st.session_state.current_session_id = str(uuid.uuid4())
            st.session_state.selected_agents = []
            st.success("New session started!")

        if st.button("🧹 Clear Selection"):
            st.session_state.selected_agents = []
            st.success("Agent selection cleared!")

        # System stats
        st.markdown("#### 📊 System Stats")
        st.metric("Available Agents", len(AVAILABLE_AGENTS))
        st.metric("Research Sessions", len(st.session_state.research_history))

def main():
    """Main application"""
    initialize_session_state()

    # Header
    render_header()


    # Agent selection
    render_agent_selection()

    # Query interface
    render_query_interface()

    # Display latest results if available
    if st.session_state.research_history:
        latest = st.session_state.research_history[-1]
        st.markdown("---")

        # Check if it's enhanced mode or legacy mode
        if latest.get('enhanced_mode'):
            display_enhanced_research_results(latest['result'], latest['query'])
        else:
            display_research_results(
                latest['result'],
                latest['query'],
                latest['agents']
            )

    # Sidebar
    render_sidebar()

    # Footer
    st.markdown("---")
    st.markdown("*AI Research Workspace - Where Collaborative Intelligence Meets Beautiful Design* ✨")

if __name__ == "__main__":
    main()