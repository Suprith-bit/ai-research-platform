"""
Enhanced display functions for research results
"""

import streamlit as st
import re
from datetime import datetime
from typing import Dict, Any
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor


def display_enhanced_research_results(result: Dict[str, Any], query: str):
    """Display enhanced research results in horizontal layout"""

    if not result.get('success'):
        st.error(f"Research failed: {result.get('error', 'Unknown error')}")
        return

    # Get the enhanced report
    markdown_report = result.get('markdown_report', '')
    metadata = result.get('metadata', {})
    source_citation_map = result.get('source_citation_map', {})

    # Create unique session keys to avoid duplicate key errors
    import time
    import hashlib
    query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
    session_key = f"{int(time.time())}_{query_hash}"

    # HORIZONTAL LAYOUT - Fixed columns with clear separation
    left_col, right_col = st.columns([7, 3], gap="large")

    with left_col:
        st.markdown("## 📊 Research Results")

        # Statistics in horizontal row
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        with metrics_col1:
            st.metric("Words", metadata.get('word_count', 0))
        with metrics_col2:
            st.metric("Citations", metadata.get('citation_count', 0))
        with metrics_col3:
            st.metric("Sources", metadata.get('sources_analyzed', 0))
        with metrics_col4:
            st.metric("Sub-questions", metadata.get('sub_questions_covered', 0))

        st.markdown("---")

        # Main report content
        if markdown_report:
            enhanced_report = process_citations_for_streamlit(markdown_report)
            st.markdown(enhanced_report, unsafe_allow_html=True)
        else:
            st.warning("No report content generated")

    with right_col:
        st.markdown("### 📥 Export Options")

        # PDF Download
        try:
            pdf_data = generate_enhanced_pdf_report(result, query)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"research_report_{timestamp}.pdf"

            st.download_button(
                label="📄 Download PDF",
                data=pdf_data,
                file_name=pdf_filename,
                mime="application/pdf",
                key=f"pdf_download_{session_key}",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")

        # Add space between buttons
        st.markdown("")

        # Show source count
        source_count = len(source_citation_map)
        if source_count > 0:
            st.info(f"📚 {source_count} sources referenced")

            # Show top sources in sidebar
            st.markdown("**Top Sources:**")
            for url, data in list(source_citation_map.items())[:5]:
                title = data.get('title', 'Unknown Source')[:50] + "..."
                st.markdown(f"• [{title}]({url})")

            if source_count > 5:
                st.markdown(f"*...and {source_count - 5} more sources*")
        else:
            st.warning("No sources found")

    return


def process_citations_for_streamlit(markdown_text: str) -> str:
    """Process inline citations to work better with Streamlit"""

    # Convert markdown citations to HTML links for better display
    citation_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

    def replace_citation(match):
        title = match.group(1)
        url = match.group(2)
        return f'<a href="{url}" target="_blank" style="color: #0066cc; text-decoration: none;">[{title}]</a>'

    processed_text = re.sub(citation_pattern, replace_citation, markdown_text)

    return processed_text


def generate_enhanced_pdf_report(result: Dict[str, Any], query: str) -> bytes:
    """Generate enhanced PDF report with proper citations and links"""

    try:
        # Create PDF buffer
        buffer = io.BytesIO()

        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Enhanced styles
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'EnhancedTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1f4e79'),
            alignment=1,  # Center
            fontName='Helvetica-Bold'
        )

        heading_style = ParagraphStyle(
            'EnhancedHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#2c5282'),
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )

        normal_style = ParagraphStyle(
            'EnhancedNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            leading=14,
            fontName='Helvetica'
        )

        citation_style = ParagraphStyle(
            'CitationStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leading=12,
            leftIndent=20,
            fontName='Helvetica',
            textColor=HexColor('#666666')
        )

        # Build PDF content
        story = []

        # Get data
        markdown_report = result.get('markdown_report', '')
        metadata = result.get('metadata', {})
        source_citation_map = result.get('source_citation_map', {})

        # Title page
        story.append(Paragraph(f"AI Research Report", title_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"{query}",
            ParagraphStyle('QueryStyle', parent=normal_style, fontSize=14,
                          textColor=HexColor('#4a5568'), alignment=1)))
        story.append(Spacer(1, 30))

        # Metadata section
        story.append(Paragraph("Report Metadata", heading_style))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
        story.append(Paragraph(f"<b>Research Engine:</b> Enhanced AI Research System", normal_style))
        story.append(Paragraph(f"<b>Word Count:</b> {metadata.get('word_count', 0)} words", normal_style))
        story.append(Paragraph(f"<b>Citations:</b> {metadata.get('citation_count', 0)} inline citations", normal_style))
        story.append(Paragraph(f"<b>Sources Analyzed:</b> {metadata.get('sources_analyzed', 0)} sources", normal_style))
        story.append(Spacer(1, 30))

        # Main report content
        if markdown_report:
            # Convert markdown to PDF-friendly format
            pdf_content = convert_markdown_to_pdf_content(markdown_report, heading_style, normal_style)
            story.extend(pdf_content)

        # Comprehensive source listing
        story.append(PageBreak())
        story.append(Paragraph("Complete Source Bibliography", heading_style))

        if source_citation_map:
            story.append(Paragraph(f"Total sources with inline citations: {len(source_citation_map)}", normal_style))
            story.append(Spacer(1, 15))

            # Group sources by domain for better organization
            domain_sources = {}
            for url, data in source_citation_map.items():
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(url).netloc
                    if domain not in domain_sources:
                        domain_sources[domain] = []
                    domain_sources[domain].append((url, data))
                except:
                    pass

            for domain, sources in domain_sources.items():
                story.append(Paragraph(f"<b>{domain}</b> ({len(sources)} sources)", heading_style))

                for j, (url, data) in enumerate(sources, 1):
                    title = data.get('title', 'Unknown Source')
                    # Create clickable link in PDF
                    story.append(Paragraph(
                        f"{j}. <link href=\"{url}\">{title}</link><br/>"
                        f"<font size=\"9\" color=\"#666666\">{url}</font>",
                        citation_style
                    ))

                story.append(Spacer(1, 10))

        # Footer
        story.append(PageBreak())
        story.append(Paragraph("Generated by Enhanced AI Research Engine",
            ParagraphStyle('Footer', parent=normal_style, fontSize=10,
                          textColor=HexColor('#888888'), alignment=1)))

        # Build PDF
        doc.build(story)

        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()

        return pdf_data

    except Exception as e:
        raise Exception(f"Enhanced PDF generation failed: {str(e)}")


def convert_markdown_to_pdf_content(markdown_text: str, heading_style, normal_style):
    """Convert markdown text to PDF-friendly content with proper formatting"""

    story = []
    lines = markdown_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Handle headers
        if line.startswith('# '):
            story.append(Paragraph(line[2:], heading_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:],
                ParagraphStyle('SubHeading', parent=heading_style, fontSize=14)))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:],
                ParagraphStyle('SubSubHeading', parent=heading_style, fontSize=12)))

        # Handle lists
        elif line.startswith('- ') or line.startswith('* '):
            story.append(Paragraph(f"• {line[2:]}",
                ParagraphStyle('ListItem', parent=normal_style, leftIndent=20)))

        # Handle numbered lists
        elif re.match(r'^\d+\.', line):
            story.append(Paragraph(line,
                ParagraphStyle('NumberedItem', parent=normal_style, leftIndent=20)))

        # Regular paragraphs with citation support
        else:
            # Convert inline citations to proper links
            citation_pattern = r'\[([^\]]+)\]\(([^)]+)\)'

            def replace_citation(match):
                title = match.group(1)
                url = match.group(2)
                return f'<link href="{url}">[{title}]</link>'

            processed_line = re.sub(citation_pattern, replace_citation, line)
            story.append(Paragraph(processed_line, normal_style))

        story.append(Spacer(1, 6))

    return story