"""
Research Agent - Academic research and scientific literature specialist
Clean, simple implementation focused on academic research
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# Add path for core components
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class ResearchAgent:
    """
    Specialized agent for academic research and scientific literature
    """

    def __init__(self):
        self.agent_id = "research"
        self.name = "Research Agent"
        self.icon = "🔬"
        self.specialty = "Academic research and scientific literature"
        self.description = "Specializes in academic research, scientific papers, literature reviews, and theoretical analysis"

        self.capabilities = [
            "Literature reviews and systematic reviews",
            "Scientific paper analysis and evaluation",
            "Research methodology guidance",
            "Academic source verification",
            "Theoretical framework development",
            "Evidence synthesis and meta-analysis",
            "Peer review quality assessment",
            "Citation and impact analysis"
        ]

        self.keywords = [
            "research", "academic", "study", "literature", "science",
            "paper", "journal", "theory", "methodology", "evidence",
            "analysis", "systematic", "meta", "peer-reviewed"
        ]

        self.example_queries = [
            "What does recent research say about climate change effects?",
            "Systematic review of AI in healthcare applications",
            "Literature review on renewable energy technologies",
            "Research methodology for machine learning studies"
        ]

        # Initialize research engine
        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform academic research with scientific focus

        Args:
            query: Research question
            context: Optional context from other agents

        Returns:
            Comprehensive research results
        """

        print(f"🔬 Research Agent analyzing: {query}")

        # Enhance query for academic focus
        academic_query = self._enhance_for_academic_research(query, context)

        # Perform comprehensive research
        result = self.research_engine.comprehensive_research(academic_query, "research")

        # Add academic-specific post-processing
        enhanced_result = self._add_academic_analysis(result, query)

        # Store in history
        self.research_history.append({
            "query": query,
            "result": enhanced_result,
            "timestamp": datetime.now().isoformat()
        })

        return enhanced_result

    def _enhance_for_academic_research(self, query: str, context: Optional[Dict] = None) -> str:
        """Enhance query with academic research focus"""

        enhanced_parts = []

        # Add academic search terms
        enhanced_parts.append(f"{query} academic research scientific study")

        # Add context if available
        if context:
            enhanced_parts.append("\nContext from other research agents:")
            for agent_id, insights in context.items():
                if isinstance(insights, dict) and insights.get("key_points"):
                    enhanced_parts.append(f"{agent_id}: {', '.join(insights['key_points'][:2])}")

        # Add academic focus
        enhanced_parts.append("\nFocus on: peer-reviewed sources, academic journals, research studies, scientific evidence")

        return "\n".join(enhanced_parts)

    def _add_academic_analysis(self, result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Add academic-specific analysis to research results"""

        # Enhanced academic metrics
        academic_metrics = self._calculate_academic_metrics(result)

        # Add academic-specific fields
        result.update({
            "agent_type": "research",
            "academic_metrics": academic_metrics,
            "research_quality": self._assess_research_quality(result),
            "source_credibility": self._assess_source_credibility(result),
            "evidence_strength": self._assess_evidence_strength(result),
            "academic_insights": self._extract_academic_insights(result)
        })

        return result

    def _calculate_academic_metrics(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate academic-specific metrics"""

        sources = result.get("sources", [])
        analysis = result.get("analysis", "")

        # Count academic sources
        academic_domains = [
            ".edu", ".org", "pubmed", "scholar.google", "researchgate",
            "arxiv", "jstor", "springer", "elsevier", "wiley", "nature",
            "science", "cell", "lancet", "nejm"
        ]

        academic_source_count = 0
        for source in sources:
            if any(domain in source.lower() for domain in academic_domains):
                academic_source_count += 1

        # Count research-specific terms
        research_terms = [
            "study", "research", "analysis", "evidence", "data", "findings",
            "methodology", "systematic", "meta-analysis", "peer-reviewed"
        ]

        research_term_count = sum(analysis.lower().count(term) for term in research_terms)

        return {
            "total_sources": len(sources),
            "academic_sources": academic_source_count,
            "academic_source_ratio": academic_source_count / len(sources) if sources else 0,
            "research_term_density": research_term_count / len(analysis.split()) if analysis else 0,
            "evidence_indicators": research_term_count
        }

    def _assess_research_quality(self, result: Dict[str, Any]) -> str:
        """Assess the quality of research sources and evidence"""

        metrics = result.get("academic_metrics", {})
        academic_ratio = metrics.get("academic_source_ratio", 0)
        evidence_indicators = metrics.get("evidence_indicators", 0)

        if academic_ratio > 0.7 and evidence_indicators > 10:
            return "High - Strong academic sources and evidence base"
        elif academic_ratio > 0.4 and evidence_indicators > 5:
            return "Medium - Moderate academic coverage"
        else:
            return "Low - Limited academic sources available"

    def _assess_source_credibility(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess credibility of sources"""

        sources = result.get("sources", [])

        credibility_tiers = {
            "tier1": [".edu", "pubmed", "scholar.google", "nature", "science", "cell"],
            "tier2": [".org", "researchgate", "arxiv", "springer", "elsevier"],
            "tier3": [".gov", "who.int", "cdc.gov", "nih.gov"]
        }

        tier_counts = {tier: 0 for tier in credibility_tiers}

        for source in sources:
            source_lower = source.lower()
            for tier, domains in credibility_tiers.items():
                if any(domain in source_lower for domain in domains):
                    tier_counts[tier] += 1
                    break

        return {
            "tier1_sources": tier_counts["tier1"],  # Highest credibility
            "tier2_sources": tier_counts["tier2"],  # Good credibility
            "tier3_sources": tier_counts["tier3"],  # Official sources
            "total_credible": sum(tier_counts.values()),
            "credibility_score": self._calculate_credibility_score(tier_counts, len(sources))
        }

    def _calculate_credibility_score(self, tier_counts: Dict[str, int], total_sources: int) -> float:
        """Calculate overall credibility score"""

        if total_sources == 0:
            return 0.0

        # Weighted scoring
        score = (tier_counts["tier1"] * 1.0 +
                tier_counts["tier2"] * 0.8 +
                tier_counts["tier3"] * 0.6) / total_sources

        return min(score, 1.0)

    def _assess_evidence_strength(self, result: Dict[str, Any]) -> str:
        """Assess strength of evidence based on content analysis"""

        analysis = result.get("analysis", "").lower()

        strong_indicators = ["systematic review", "meta-analysis", "randomized controlled", "peer-reviewed", "longitudinal study"]
        moderate_indicators = ["cohort study", "case-control", "cross-sectional", "observational"]
        weak_indicators = ["case report", "expert opinion", "editorial", "commentary"]

        strong_count = sum(1 for indicator in strong_indicators if indicator in analysis)
        moderate_count = sum(1 for indicator in moderate_indicators if indicator in analysis)
        weak_count = sum(1 for indicator in weak_indicators if indicator in analysis)

        if strong_count >= 2:
            return "Strong - Multiple high-quality study types identified"
        elif strong_count >= 1 or moderate_count >= 2:
            return "Moderate - Some quality research evidence found"
        else:
            return "Limited - Primarily observational or opinion-based sources"

    def _extract_academic_insights(self, result: Dict[str, Any]) -> List[str]:
        """Extract academic-specific insights"""

        insights = []
        analysis = result.get("analysis", "")

        # Look for research gaps
        if any(term in analysis.lower() for term in ["gap", "limitation", "future research", "further study"]):
            insights.append("Research gaps and future directions identified")

        # Look for methodology discussions
        if any(term in analysis.lower() for term in ["methodology", "method", "approach", "design"]):
            insights.append("Methodological considerations discussed")

        # Look for evidence quality
        metrics = result.get("academic_metrics", {})
        if metrics.get("academic_source_ratio", 0) > 0.5:
            insights.append("High proportion of academic sources found")

        # Look for consensus or controversy
        if any(term in analysis.lower() for term in ["consensus", "agreement", "widely accepted"]):
            insights.append("Scientific consensus indicators found")
        elif any(term in analysis.lower() for term in ["controversy", "debate", "conflicting", "disputed"]):
            insights.append("Scientific debate or controversy noted")

        return insights

    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "icon": self.icon,
            "specialty": self.specialty,
            "description": self.description,
            "capabilities": self.capabilities,
            "keywords": self.keywords,
            "example_queries": self.example_queries,
            "research_count": len(self.research_history),
            "status": "🟢 Ready"
        }

    def get_research_history(self) -> List[Dict[str, Any]]:
        """Get research history"""
        return self.research_history[-10:]  # Last 10 research queries