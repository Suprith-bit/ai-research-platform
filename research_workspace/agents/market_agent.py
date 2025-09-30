"""
Market Agent - Business intelligence and market analysis specialist
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class MarketAgent:
    def __init__(self):
        self.agent_id = "market"
        self.name = "Market Agent"
        self.icon = "💼"
        self.specialty = "Business intelligence and market analysis"
        self.description = "Analyzes market trends, competitive intelligence, and business opportunities"

        self.capabilities = [
            "Market trend analysis", "Competitive intelligence", "Industry reports",
            "Business opportunity assessment", "Market sizing and segmentation"
        ]

        self.keywords = [
            "market", "business", "industry", "competitive", "trends", "analysis", "intelligence"
        ]

        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        print(f"💼 Market Agent analyzing: {query}")

        # Enhance for market focus
        market_query = f"{query} market analysis business intelligence industry trends"

        result = self.research_engine.comprehensive_research(market_query, "market")

        # Add market-specific analysis
        result.update({
            "agent_type": "market",
            "market_insights": self._extract_market_insights(result)
        })

        self.research_history.append({
            "query": query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def _extract_market_insights(self, result: Dict[str, Any]) -> List[str]:
        insights = []
        analysis = result.get("analysis", "").lower()

        if any(term in analysis for term in ["growth", "market size", "revenue"]):
            insights.append("Market growth and size data identified")
        if any(term in analysis for term in ["competitor", "competitive", "market share"]):
            insights.append("Competitive landscape analysis available")
        if any(term in analysis for term in ["trend", "emerging", "future"]):
            insights.append("Market trends and future outlook discussed")

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