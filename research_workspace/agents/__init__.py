"""
AI Research Workspace - Specialized Research Agents
Clean, simple agent names for professional research collaboration
"""

from .research_agent import ResearchAgent
from .doctor_agent import DoctorAgent
from .market_agent import MarketAgent
from .financial_agent import FinancialAgent
from .developer_agent import DeveloperAgent
from .writer_agent import WriterAgent
from .analyst_agent import AnalystAgent

# Clean agent registry with simple names
AVAILABLE_AGENTS = {
    "research": {
        "name": "Research Agent",
        "icon": "🔬",
        "class": ResearchAgent,
        "specialty": "Academic research and scientific literature",
        "description": "Specializes in academic research, scientific papers, literature reviews, and theoretical analysis",
        "use_cases": [
            "Literature reviews and academic research",
            "Scientific paper analysis",
            "Theoretical framework development",
            "Research methodology guidance",
            "Academic source verification"
        ],
        "keywords": ["research", "academic", "study", "literature", "science", "paper", "journal", "theory"]
    },
    "doctor": {
        "name": "Doctor Agent",
        "icon": "🏥",
        "class": DoctorAgent,
        "specialty": "Medical and healthcare research",
        "description": "Focuses on medical research, clinical studies, healthcare trends, and medical analysis",
        "use_cases": [
            "Medical condition research",
            "Treatment option analysis",
            "Clinical study reviews",
            "Healthcare trend analysis",
            "Drug and therapy research"
        ],
        "keywords": ["medical", "health", "doctor", "clinical", "treatment", "disease", "medicine", "therapy"]
    },
    "market": {
        "name": "Market Agent",
        "icon": "💼",
        "class": MarketAgent,
        "specialty": "Business intelligence and market analysis",
        "description": "Analyzes market trends, competitive intelligence, and business opportunities",
        "use_cases": [
            "Market trend analysis",
            "Competitive intelligence",
            "Industry reports",
            "Business opportunity assessment",
            "Market sizing and segmentation"
        ],
        "keywords": ["market", "business", "industry", "competitive", "trends", "analysis", "intelligence"]
    },
    "financial": {
        "name": "Financial Agent",
        "icon": "💰",
        "class": FinancialAgent,
        "specialty": "Investment analysis and financial research",
        "description": "Provides investment analysis, financial metrics, and economic research",
        "use_cases": [
            "Investment opportunity analysis",
            "Financial performance evaluation",
            "Risk assessment",
            "Economic trend analysis",
            "Portfolio optimization"
        ],
        "keywords": ["investment", "financial", "money", "stock", "economic", "finance", "portfolio", "risk"]
    },
    "developer": {
        "name": "Developer Agent",
        "icon": "💻",
        "class": DeveloperAgent,
        "specialty": "Technical architecture and software development",
        "description": "Focuses on software architecture, coding solutions, and technical implementation",
        "use_cases": [
            "Software architecture design",
            "Technology stack recommendations",
            "Code optimization strategies",
            "Technical feasibility analysis",
            "Development best practices"
        ],
        "keywords": ["code", "programming", "software", "technical", "development", "architecture", "technology"]
    },
    "writer": {
        "name": "Writer Agent",
        "icon": "✍️",
        "class": WriterAgent,
        "specialty": "Content creation and documentation",
        "description": "Specializes in content creation, technical writing, and communication strategies",
        "use_cases": [
            "Technical documentation",
            "Content strategy development",
            "Writing optimization",
            "Communication planning",
            "Editorial guidance"
        ],
        "keywords": ["writing", "content", "documentation", "communication", "editorial", "copy", "text"]
    },
    "analyst": {
        "name": "Analyst Agent",
        "icon": "📊",
        "class": AnalystAgent,
        "specialty": "Data analysis and insights extraction",
        "description": "Performs statistical analysis, data insights, and trend identification",
        "use_cases": [
            "Statistical analysis",
            "Data trend identification",
            "Performance metrics analysis",
            "Predictive insights",
            "Data visualization recommendations"
        ],
        "keywords": ["data", "analysis", "statistics", "metrics", "trends", "insights", "analytics"]
    }
}