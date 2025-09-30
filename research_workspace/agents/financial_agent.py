"""
Financial Agent - Investment analysis and financial research specialist
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class FinancialAgent:
    def __init__(self):
        self.agent_id = "financial"
        self.name = "Financial Agent"
        self.icon = "💰"
        self.specialty = "Investment analysis and financial research"
        self.description = "Provides investment analysis, financial metrics, and economic research"

        self.capabilities = [
            "Investment opportunity analysis", "Financial performance evaluation",
            "Risk assessment", "Economic trend analysis", "Portfolio optimization"
        ]

        self.keywords = [
            "investment", "financial", "money", "stock", "economic", "finance", "portfolio", "risk"
        ]

        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        print(f"💰 Financial Agent analyzing: {query}")

        # Enhance for financial focus
        financial_query = f"{query} financial analysis investment risk return valuation"

        result = self.research_engine.comprehensive_research(financial_query, "financial")

        # Add financial-specific analysis
        result.update({
            "agent_type": "financial",
            "financial_insights": self._extract_financial_insights(result)
        })

        self.research_history.append({
            "query": query,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return result

    def _extract_financial_insights(self, result: Dict[str, Any]) -> List[str]:
        insights = []
        analysis = result.get("analysis", "").lower()

        if any(term in analysis for term in ["valuation", "price", "earnings", "revenue"]):
            insights.append("Financial valuation metrics available")
        if any(term in analysis for term in ["risk", "volatility", "uncertainty"]):
            insights.append("Risk factors and considerations identified")
        if any(term in analysis for term in ["return", "profit", "gain", "yield"]):
            insights.append("Return potential and profitability analysis")

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