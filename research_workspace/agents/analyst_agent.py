"""
Analyst Agent - Data analysis and insights extraction specialist
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class AnalystAgent:
    def __init__(self):
        self.agent_id = "analyst"
        self.name = "Analyst Agent"
        self.icon = "📊"
        self.specialty = "Data analysis and insights extraction"
        self.description = "Performs statistical analysis, data insights, and trend identification"

        self.capabilities = [
            "Statistical analysis", "Data trend identification",
            "Performance metrics analysis", "Predictive insights", "Data visualization recommendations"
        ]

        self.keywords = [
            "data", "analysis", "statistics", "metrics", "trends", "insights", "analytics"
        ]

        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        print(f"📊 Analyst Agent analyzing: {query}")

        # Enhance for data analysis focus
        analyst_query = f"{query} data analysis statistics metrics trends insights"

        result = self.research_engine.comprehensive_research(analyst_query, "analyst")

        # Add analyst-specific analysis
        result.update({
            "agent_type": "analyst",
            "analytical_insights": self._extract_analytical_insights(result)
        })

        self.research_history.append({
            "query": query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def _extract_analytical_insights(self, result: Dict[str, Any]) -> List[str]:
        insights = []
        analysis = result.get("analysis", "").lower()

        if any(term in analysis for term in ["data", "statistics", "metrics", "numbers"]):
            insights.append("Quantitative data and metrics available")
        if any(term in analysis for term in ["trend", "pattern", "correlation", "relationship"]):
            insights.append("Trends and patterns identified in data")
        if any(term in analysis for term in ["prediction", "forecast", "future", "projection"]):
            insights.append("Predictive insights and forecasting data")

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