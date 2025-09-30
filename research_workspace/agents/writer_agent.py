"""
Writer Agent - Content creation and documentation specialist
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class WriterAgent:
    def __init__(self):
        self.agent_id = "writer"
        self.name = "Writer Agent"
        self.icon = "✍️"
        self.specialty = "Content creation and documentation"
        self.description = "Specializes in content creation, technical writing, and communication strategies"

        self.capabilities = [
            "Technical documentation", "Content strategy development",
            "Writing optimization", "Communication planning", "Editorial guidance"
        ]

        self.keywords = [
            "writing", "content", "documentation", "communication", "editorial", "copy", "text"
        ]

        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        print(f"✍️ Writer Agent analyzing: {query}")

        # Enhance for writing focus
        writing_query = f"{query} writing content creation documentation communication strategy"

        result = self.research_engine.comprehensive_research(writing_query, "writer")

        # Add writing-specific analysis
        result.update({
            "agent_type": "writer",
            "writing_insights": self._extract_writing_insights(result)
        })

        self.research_history.append({
            "query": query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def _extract_writing_insights(self, result: Dict[str, Any]) -> List[str]:
        insights = []
        analysis = result.get("analysis", "").lower()

        if any(term in analysis for term in ["audience", "reader", "target", "user"]):
            insights.append("Audience analysis and targeting considerations")
        if any(term in analysis for term in ["style", "tone", "voice", "brand"]):
            insights.append("Style and tone recommendations available")
        if any(term in analysis for term in ["structure", "format", "template", "layout"]):
            insights.append("Content structure and formatting guidance")

        return insights

    def get_info(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "icon": self.icon,
            "specialty": self.specialty,
            "description": self.description,
            "capabilities": self.capabilities,
            "keywords": self.keywords,
            "research_count": len(self.research_history),
            "status": "🟢 Ready"
        }