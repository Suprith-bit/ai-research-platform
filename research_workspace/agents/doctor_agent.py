"""
Doctor Agent - Medical and healthcare research specialist
Clean, simple implementation focused on medical research
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# Add path for core components
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.research_engine import RealResearchEngine

class DoctorAgent:
    """
    Specialized agent for medical and healthcare research
    """

    def __init__(self):
        self.agent_id = "doctor"
        self.name = "Doctor Agent"
        self.icon = "🏥"
        self.specialty = "Medical and healthcare research"
        self.description = "Focuses on medical research, clinical studies, healthcare trends, and medical analysis"

        self.capabilities = [
            "Medical condition research and analysis",
            "Treatment option evaluation",
            "Clinical study interpretation",
            "Drug and therapy research",
            "Healthcare trend analysis",
            "Medical guideline review",
            "Symptom and diagnosis research",
            "Medical safety and efficacy assessment"
        ]

        self.keywords = [
            "medical", "health", "doctor", "clinical", "treatment", "disease",
            "medicine", "therapy", "patient", "diagnosis", "symptoms", "drug",
            "healthcare", "hospital", "physician", "nursing"
        ]

        self.example_queries = [
            "Latest treatments for Type 2 diabetes",
            "Clinical evidence for new cancer therapies",
            "Side effects of common blood pressure medications",
            "Best practices for mental health treatment"
        ]

        # Initialize research engine
        self.research_engine = RealResearchEngine()
        self.research_history = []

    def research(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform medical research with clinical focus

        Args:
            query: Medical research question
            context: Optional context from other agents

        Returns:
            Comprehensive medical research results
        """

        print(f"🏥 Doctor Agent analyzing: {query}")

        # Enhance query for medical focus
        medical_query = self._enhance_for_medical_research(query, context)

        # Perform comprehensive research with medical analysis
        result = self.research_engine.comprehensive_research(medical_query, "doctor")

        # Add medical-specific post-processing
        enhanced_result = self._add_medical_analysis(result, query)

        # Store in history
        self.research_history.append({
            "query": query,
            "result": enhanced_result,
            "timestamp": datetime.now().isoformat()
        })

        return enhanced_result

    def _enhance_for_medical_research(self, query: str, context: Optional[Dict] = None) -> str:
        """Enhance query with medical research focus"""

        enhanced_parts = []

        # Add medical search terms
        enhanced_parts.append(f"{query} medical research clinical study treatment")

        # Add context if available
        if context:
            enhanced_parts.append("\nContext from other research agents:")
            for agent_id, insights in context.items():
                if isinstance(insights, dict) and insights.get("key_points"):
                    enhanced_parts.append(f"{agent_id}: {', '.join(insights['key_points'][:2])}")

        # Add medical focus
        enhanced_parts.append("\nFocus on: clinical evidence, medical journals, treatment guidelines, safety data, efficacy studies")

        return "\n".join(enhanced_parts)

    def _add_medical_analysis(self, result: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Add medical-specific analysis to research results"""

        # Enhanced medical metrics
        medical_metrics = self._calculate_medical_metrics(result)

        # Add medical-specific fields
        result.update({
            "agent_type": "doctor",
            "medical_metrics": medical_metrics,
            "clinical_evidence": self._assess_clinical_evidence(result),
            "safety_profile": self._assess_safety_profile(result),
            "efficacy_data": self._assess_efficacy_data(result),
            "regulatory_status": self._assess_regulatory_status(result),
            "medical_insights": self._extract_medical_insights(result)
        })

        return result

    def _calculate_medical_metrics(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate medical-specific metrics"""

        sources = result.get("sources", [])
        analysis = result.get("analysis", "")

        # Count medical sources
        medical_domains = [
            "pubmed", "nejm", "bmj", "lancet", "jama", "mayo", "who.int",
            "cdc.gov", "nih.gov", "fda.gov", "medscape", "uptodate",
            "cochrane", "clinicaltrials.gov"
        ]

        medical_source_count = 0
        for source in sources:
            if any(domain in source.lower() for domain in medical_domains):
                medical_source_count += 1

        # Count medical-specific terms
        medical_terms = [
            "clinical", "patient", "treatment", "therapy", "drug", "medication",
            "diagnosis", "symptom", "efficacy", "safety", "side effect", "adverse"
        ]

        medical_term_count = sum(analysis.lower().count(term) for term in medical_terms)

        return {
            "total_sources": len(sources),
            "medical_sources": medical_source_count,
            "medical_source_ratio": medical_source_count / len(sources) if sources else 0,
            "medical_term_density": medical_term_count / len(analysis.split()) if analysis else 0,
            "clinical_indicators": medical_term_count
        }

    def _assess_clinical_evidence(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess quality of clinical evidence"""

        analysis = result.get("analysis", "").lower()

        evidence_levels = {
            "level_1": ["systematic review", "meta-analysis", "cochrane"],
            "level_2": ["randomized controlled trial", "rct", "double-blind"],
            "level_3": ["cohort study", "case-control", "observational"],
            "level_4": ["case series", "case report", "expert opinion"]
        }

        evidence_counts = {level: 0 for level in evidence_levels}

        for level, terms in evidence_levels.items():
            for term in terms:
                if term in analysis:
                    evidence_counts[level] += 1

        evidence_quality = "High" if evidence_counts["level_1"] > 0 else \
                          "Good" if evidence_counts["level_2"] > 0 else \
                          "Moderate" if evidence_counts["level_3"] > 0 else \
                          "Limited"

        return {
            "evidence_levels": evidence_counts,
            "evidence_quality": evidence_quality,
            "has_systematic_review": evidence_counts["level_1"] > 0,
            "has_rct_data": evidence_counts["level_2"] > 0
        }

    def _assess_safety_profile(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess safety information from research"""

        analysis = result.get("analysis", "").lower()

        safety_indicators = [
            "side effect", "adverse event", "contraindication", "warning",
            "precaution", "risk", "safety", "toxicity", "allergic reaction"
        ]

        safety_mentions = sum(1 for indicator in safety_indicators if indicator in analysis)

        safety_concerns = []
        if "side effect" in analysis or "adverse" in analysis:
            safety_concerns.append("Side effects documented")
        if "contraindication" in analysis:
            safety_concerns.append("Contraindications noted")
        if "warning" in analysis or "risk" in analysis:
            safety_concerns.append("Safety warnings identified")

        return {
            "safety_mentions": safety_mentions,
            "safety_concerns": safety_concerns,
            "safety_data_available": safety_mentions > 0,
            "safety_assessment": "Comprehensive" if safety_mentions > 3 else
                                "Moderate" if safety_mentions > 1 else
                                "Limited"
        }

    def _assess_efficacy_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess efficacy information from research"""

        analysis = result.get("analysis", "").lower()

        efficacy_indicators = [
            "efficacy", "effective", "improvement", "benefit", "outcome",
            "response rate", "success rate", "cure", "remission"
        ]

        efficacy_mentions = sum(1 for indicator in efficacy_indicators if indicator in analysis)

        efficacy_findings = []
        if "efficacy" in analysis or "effective" in analysis:
            efficacy_findings.append("Efficacy data available")
        if "improvement" in analysis or "benefit" in analysis:
            efficacy_findings.append("Clinical benefits documented")
        if "response rate" in analysis or "success rate" in analysis:
            efficacy_findings.append("Response rates reported")

        return {
            "efficacy_mentions": efficacy_mentions,
            "efficacy_findings": efficacy_findings,
            "efficacy_data_available": efficacy_mentions > 0,
            "efficacy_assessment": "Strong" if efficacy_mentions > 3 else
                                  "Moderate" if efficacy_mentions > 1 else
                                  "Limited"
        }

    def _assess_regulatory_status(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess regulatory and approval status"""

        analysis = result.get("analysis", "").lower()

        regulatory_terms = [
            "fda approved", "fda approval", "approved by", "licensed",
            "regulatory", "clinical trial", "phase", "investigational"
        ]

        regulatory_mentions = sum(1 for term in regulatory_terms if term in analysis)

        status_indicators = []
        if "fda approved" in analysis or "fda approval" in analysis:
            status_indicators.append("FDA approved")
        if "clinical trial" in analysis:
            status_indicators.append("In clinical trials")
        if "investigational" in analysis:
            status_indicators.append("Investigational status")

        return {
            "regulatory_mentions": regulatory_mentions,
            "status_indicators": status_indicators,
            "regulatory_info_available": regulatory_mentions > 0
        }

    def _extract_medical_insights(self, result: Dict[str, Any]) -> List[str]:
        """Extract medical-specific insights"""

        insights = []
        analysis = result.get("analysis", "")

        # Clinical evidence insights
        clinical_evidence = result.get("clinical_evidence", {})
        if clinical_evidence.get("has_systematic_review"):
            insights.append("High-quality systematic review evidence available")

        # Safety insights
        safety_profile = result.get("safety_profile", {})
        if safety_profile.get("safety_data_available"):
            insights.append("Safety data and side effect information documented")

        # Efficacy insights
        efficacy_data = result.get("efficacy_data", {})
        if efficacy_data.get("efficacy_assessment") == "Strong":
            insights.append("Strong efficacy evidence from clinical studies")

        # Source quality insights
        metrics = result.get("medical_metrics", {})
        if metrics.get("medical_source_ratio", 0) > 0.6:
            insights.append("High proportion of medical and clinical sources")

        # Look for treatment guidelines
        if any(term in analysis.lower() for term in ["guideline", "recommendation", "standard of care"]):
            insights.append("Treatment guidelines and recommendations identified")

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