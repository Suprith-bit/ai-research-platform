"""
Developer Agent - Technical architecture and software development specialist
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class DeveloperAgent:
    def __init__(self):
        self.agent_id = "developer"
        self.name = "Developer Agent"
        self.icon = "💻"
        self.specialty = "Technical architecture and software development"
        self.description = "Focuses on software architecture, coding solutions, and technical implementation"

        self.capabilities = [
            "Software architecture design", "Technology stack recommendations",
            "Code optimization strategies", "Technical feasibility analysis", "Development best practices"
        ]

        self.keywords = [
            "code", "programming", "software", "technical", "development", "architecture", "technology"
        ]

        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        print(f"💻 Developer Agent analyzing: {query}")

        # Enhance for technical focus
        technical_query = f"{query} software development programming architecture technical implementation"

        result = self.research_engine.comprehensive_research(technical_query, "developer")

        # Add technical-specific analysis
        result.update({
            "agent_type": "developer",
            "technical_insights": self._extract_technical_insights(result)
        })

        self.research_history.append({
            "query": query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def _extract_technical_insights(self, result: Dict[str, Any]) -> List[str]:
        insights = []
        analysis = result.get("analysis", "").lower()

        if any(term in analysis for term in ["architecture", "design", "pattern", "framework"]):
            insights.append("Architecture and design patterns discussed")
        if any(term in analysis for term in ["performance", "scalability", "optimization"]):
            insights.append("Performance and scalability considerations")
        if any(term in analysis for term in ["security", "authentication", "encryption"]):
            insights.append("Security implementation guidelines")

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