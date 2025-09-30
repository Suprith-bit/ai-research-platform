"""
Real Research Engine - Integrates Serper API and Google Gemini
This engine performs actual web searches and AI analysis
"""

import os
import sys
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

# Add paths for configuration
sys.path.append(os.path.join(os.path.dirname(__file__), '../../shared'))
from config import Config

class RealResearchEngine:
    """
    Core research engine that performs real web searches and AI analysis
    """

    def __init__(self):
        """Initialize the research engine with real API connections"""
        self.serper_api_key = Config.SERPER_API_KEY
        self.use_openai = Config.USE_OPENAI

        if self.use_openai:
            self.openai_api_key = Config.OPENAI_API_KEY
            if not self.serper_api_key or not self.openai_api_key:
                raise ValueError("OpenAI and Serper API keys not configured. Check your .env file.")
            print("✅ Real Research Engine initialized with OpenAI API")
        else:
            self.gemini_api_key = Config.GEMINI_API_KEY
            if not self.serper_api_key or not self.gemini_api_key:
                raise ValueError("Gemini and Serper API keys not configured. Check your .env file.")
            print("✅ Real Research Engine initialized with Gemini API")

    def search_web(self, query: str, num_results: int = 20) -> Dict[str, Any]:
        """
        Perform real web search using Serper API

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            Dictionary containing search results and metadata
        """

        url = "https://google.serper.dev/search"

        payload = json.dumps({
            "q": query,
            "num": num_results,
            "tbs": "qdr:y",  # Recent results (past year)
            "location": "United States",
            "gl": "us",
            "hl": "en"
        })

        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }

        try:
            print(f"🔍 Searching web for: {query}")
            response = requests.post(url, headers=headers, data=payload, timeout=30)
            response.raise_for_status()

            search_data = response.json()

            # Extract and format results
            results = {
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "total_results": search_data.get("searchInformation", {}).get("totalResults", "0"),
                "search_time": search_data.get("searchInformation", {}).get("searchTime", 0),
                "organic_results": [],
                "news_results": [],
                "knowledge_graph": search_data.get("knowledgeGraph", {}),
                "answer_box": search_data.get("answerBox", {}),
                "raw_data": search_data
            }

            # Process organic results
            for item in search_data.get("organic", []):
                results["organic_results"].append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "displayed_link": item.get("displayedLink", ""),
                    "position": item.get("position", 0)
                })

            # Process news results if available
            for item in search_data.get("news", []):
                results["news_results"].append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "date": item.get("date", ""),
                    "source": item.get("source", "")
                })

            print(f"✅ Found {len(results['organic_results'])} organic results")
            return results

        except requests.exceptions.RequestException as e:
            print(f"❌ Serper API error: {str(e)}")
            return {
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "organic_results": [],
                "news_results": []
            }

    def analyze_with_ai(self, content: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze content using configured AI API (OpenAI or Gemini)

        Args:
            content: Content to analyze
            analysis_type: Type of analysis (general, medical, financial, technical, etc.)

        Returns:
            Dictionary containing AI analysis results
        """

        if self.use_openai:
            return self.analyze_with_openai(content, analysis_type)
        else:
            return self.analyze_with_gemini(content, analysis_type)

    def analyze_with_openai(self, content: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze content using OpenAI API

        Args:
            content: Content to analyze
            analysis_type: Type of analysis (general, medical, financial, technical, etc.)

        Returns:
            Dictionary containing AI analysis results
        """

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)

        except ImportError:
            print("❌ OpenAI library not installed")
            return {"error": "OpenAI library not available", "analysis": ""}
        except Exception as e:
            print(f"❌ OpenAI configuration error: {str(e)}")
            return {"error": str(e), "analysis": ""}

        # Create detailed analysis prompts for comprehensive reports
        prompts = {
            "general": f"""
            Create a comprehensive research report with proper formatting and source citations.

            FORMAT THE REPORT AS FOLLOWS:

            # Executive Summary
            [4-5 sentences synthesizing key findings with specific data points and source citations]

            # Market Overview
            [Detailed analysis with statistics, percentages, and growth rates from sources]
            - Include specific numbers from research
            - Quote expert opinions and statements
            - Reference companies and organizations mentioned

            # Current Trends and Patterns
            [Analysis of trends with data backing each claim]
            - Cite specific sources for each trend
            - Include dates and timeframes
            - Provide statistical evidence

            # Key Players and Competitive Landscape
            [Analysis of major players with financial data]
            - Market share percentages
            - Revenue figures
            - Company valuations and metrics

            # Financial Data and Projections
            [All financial metrics found in sources]
            - Market size data
            - Growth projections
            - Investment figures
            - Revenue forecasts

            # Risk Analysis
            [Potential challenges identified in research]

            # Actionable Recommendations
            [Data-backed specific recommendations]

            # Source Citations
            Throughout the report, cite sources as [Source: Website Name - URL].
            Include ALL the URLs and website names from the research data below.

            RESEARCH DATA TO ANALYZE:
            {content}

            CRITICAL: Include direct quotes, specific numbers, dates, and statistics from the sources. Reference the actual website names and URLs throughout the analysis.
            """,

            "medical": f"""
            As a medical research analyst, analyze the following WEB SEARCH RESULTS and provide:

            IMPORTANT: Base your analysis on the specific medical information found in these web sources.

            1. Clinical Summary (based on the search results)
            2. Evidence Quality Assessment from the sources
            3. Safety and Efficacy Findings from the web data
            4. Regulatory Status (if mentioned in sources)
            5. Clinical Implications from the research
            6. Specific source citations and medical websites referenced

            Medical content:
            {content}
            """,

            "financial": f"""
            As a financial analyst, analyze this content and provide:
            1. Investment Thesis Summary
            2. Financial Metrics and Performance
            3. Risk Assessment
            4. Market Opportunities and Threats
            5. Recommendations

            Content: {content}
            """
        }

        try:
            response = client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert research analyst providing comprehensive analysis with proper source citations."},
                    {"role": "user", "content": prompts.get(analysis_type, prompts["general"])}
                ],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )

            analysis_result = response.choices[0].message.content

            return {
                "analysis": analysis_result,
                "model_used": Config.MODEL_NAME,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else 0,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ OpenAI analysis error: {str(e)}")
            return {"error": str(e), "analysis": "Analysis failed due to API error"}

    def analyze_with_gemini(self, content: str, analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze content using Google Gemini API

        Args:
            content: Content to analyze
            analysis_type: Type of analysis (general, medical, financial, technical, etc.)

        Returns:
            Dictionary containing AI analysis results
        """

        # Import Gemini here to avoid import errors if not installed
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_api_key)

            # Use Gemini 2.5 Flash for fast analysis
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

        except ImportError:
            print("❌ Google GenerativeAI library not installed")
            return {"error": "Gemini library not available", "analysis": ""}
        except Exception as e:
            print(f"❌ Gemini configuration error: {str(e)}")
            return {"error": str(e), "analysis": ""}

        # Create detailed analysis prompts for comprehensive reports
        prompts = {
            "general": f"""
            Create a comprehensive research report with proper formatting and source citations.

            FORMAT THE REPORT AS FOLLOWS:

            # Executive Summary
            [4-5 sentences synthesizing key findings with specific data points and source citations]

            # Market Overview
            [Detailed analysis with statistics, percentages, and growth rates from sources]
            - Include specific numbers from research
            - Quote expert opinions and statements
            - Reference companies and organizations mentioned

            # Current Trends and Patterns
            [Analysis of trends with data backing each claim]
            - Cite specific sources for each trend
            - Include dates and timeframes
            - Provide statistical evidence

            # Key Players and Competitive Landscape
            [Analysis of major players with financial data]
            - Market share percentages
            - Revenue figures
            - Company valuations and metrics

            # Financial Data and Projections
            [All financial metrics found in sources]
            - Market size data
            - Growth projections
            - Investment figures
            - Revenue forecasts

            # Risk Analysis
            [Potential challenges identified in research]

            # Actionable Recommendations
            [Data-backed specific recommendations]

            # Source Citations
            Throughout the report, cite sources as [Source: Website Name - URL].
            Include ALL the URLs and website names from the research data below.

            RESEARCH DATA TO ANALYZE:
            {content}

            CRITICAL: Include direct quotes, specific numbers, dates, and statistics from the sources. Reference the actual website names and URLs throughout the analysis.
            """,

            "medical": f"""
            As a medical research analyst, analyze the following WEB SEARCH RESULTS and provide:

            IMPORTANT: Base your analysis on the specific medical information found in these web sources.

            1. Clinical Summary (based on the search results)
            2. Evidence Quality Assessment from the sources
            3. Safety and Efficacy Findings from the web data
            4. Regulatory Status (if mentioned in sources)
            5. Clinical Implications from the research
            6. Specific source citations and medical websites referenced

            Medical content:
            {content}
            """,

            "financial": f"""
            As a financial analyst, analyze this content and provide:
            1. Investment Thesis Summary
            2. Financial Metrics and Performance
            3. Risk Assessment
            4. Market Opportunities and Threats
            5. Valuation Insights
            6. Investment Recommendation (if applicable)

            Financial content:
            {content}
            """,

            "technical": f"""
            As a technical architect, analyze this content and provide:
            1. Technical Summary
            2. Architecture and Design Patterns
            3. Performance Considerations
            4. Security Implications
            5. Scalability Assessment
            6. Implementation Recommendations

            Technical content:
            {content}
            """,

            "market": f"""
            As a market intelligence analyst, analyze this content and provide:
            1. Market Overview
            2. Competitive Landscape
            3. Industry Trends and Drivers
            4. Market Size and Growth Potential
            5. Key Players and Market Share
            6. Strategic Recommendations

            Market content:
            {content}
            """
        }

        prompt = prompts.get(analysis_type, prompts["general"])

        try:
            print(f"🤖 Analyzing content with Gemini ({analysis_type} analysis)")

            # Add generation config for better control
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 4096,
            }

            # Simple timeout using threading
            import threading
            import time

            result_container = {}
            error_container = {}

            def generate_with_timeout():
                try:
                    response = model.generate_content(prompt, generation_config=generation_config)
                    result_container['response'] = response
                except Exception as e:
                    error_container['error'] = e

            # Start generation in thread
            thread = threading.Thread(target=generate_with_timeout)
            thread.daemon = True
            thread.start()

            # Wait for completion with longer timeout for detailed analysis
            thread.join(timeout=180)  # 3 minute timeout for comprehensive reports

            if thread.is_alive():
                print("⏰ Gemini analysis timed out, generating fallback response")
                return {
                    "analysis_type": analysis_type,
                    "error": "Analysis timed out",
                    "timestamp": datetime.now().isoformat(),
                    "analysis": "Analysis timed out. The query was too complex or the service is busy. Please try again with a simpler query.",
                    "confidence": 0.3,
                    "key_points": ["Analysis timed out", "Please try a simpler query"],
                    "summary": "Analysis timed out"
                }

            if 'error' in error_container:
                raise error_container['error']

            if 'response' not in result_container:
                raise Exception("No response received")

            response = result_container['response']

            # Extract the analysis text
            analysis_text = response.text if hasattr(response, 'text') else str(response)

            # Parse the structured response
            analysis_result = {
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "content_length": len(content),
                "analysis": analysis_text,
                "confidence": self._extract_confidence(analysis_text),
                "key_points": self._extract_key_points(analysis_text),
                "summary": self._extract_summary(analysis_text)
            }

            print(f"✅ Gemini analysis completed ({len(analysis_text)} characters)")
            return analysis_result

        except Exception as e:
            print(f"❌ Gemini analysis error: {str(e)}")
            return {
                "analysis_type": analysis_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "analysis": f"Analysis failed: {str(e)}. Please try again.",
                "confidence": 0.0,
                "key_points": [f"Error: {str(e)}"],
                "summary": f"Analysis failed: {str(e)}"
            }

    def deep_web_research(self, query: str) -> Dict[str, Any]:
        """Perform DEEP web research with 50-100+ sources for extraordinary reports"""

        print(f"🚀 DEEP WEB RESEARCH INITIATED for: {query}")
        print("🔍 Searching 50-100+ websites for comprehensive analysis...")

        all_results = {
            "organic_results": [],
            "news_results": [],
            "academic_results": [],
            "data_sources": [],
            "chart_sources": [],
            "government_sources": [],
            "financial_sources": []
        }

        # 1. PRIMARY SEARCH - Multiple rounds with different parameters
        search_rounds = [
            {"q": query, "num": 20, "tbs": None},  # Current results
            {"q": query, "num": 20, "tbs": "qdr:m"},  # Past month
            {"q": query, "num": 20, "tbs": "qdr:y"},  # Past year
            {"q": f"{query} analysis report", "num": 15, "tbs": None},  # Analysis focus
            {"q": f"{query} data statistics", "num": 15, "tbs": None},  # Data focus
            {"q": f"{query} trends forecast", "num": 15, "tbs": None},  # Trends focus
        ]

        for i, search_params in enumerate(search_rounds, 1):
            print(f"   Round {i}: Searching with parameters {search_params['q'][:50]}...")
            try:
                search_result = self._perform_search(search_params)
                if search_result.get("organic_results"):
                    all_results["organic_results"].extend(search_result["organic_results"])
                    print(f"   ✅ Round {i}: Found {len(search_result['organic_results'])} sources")
            except Exception as e:
                print(f"   ⚠️ Round {i} failed: {e}")

        # 2. SPECIALIZED SEARCHES
        specialized_searches = {
            "news": f"{query} latest news updates",
            "academic": f"{query} research study findings",
            "government": f"{query} site:gov OR site:edu",
            "financial": f"{query} market analysis investment",
            "data": f"{query} chart graph data visualization",
            "reports": f"{query} industry report whitepaper"
        }

        for search_type, search_query in specialized_searches.items():
            print(f"   🎯 Specialized {search_type} search...")
            try:
                if search_type == "news":
                    results = self._search_news(search_query, num=20)
                    all_results["news_results"].extend(results)
                elif search_type == "data":
                    results = self._search_data_sources(search_query)
                    all_results["data_sources"].extend(results)
                    all_results["chart_sources"].extend(results)
                else:
                    results = self._perform_search({"q": search_query, "num": 15, "tbs": None})
                    if results.get("organic_results"):
                        category_key = f"{search_type}_sources" if f"{search_type}_sources" in all_results else "organic_results"
                        all_results[category_key].extend(results["organic_results"])

                print(f"   ✅ {search_type.title()}: Found {len(results) if isinstance(results, list) else len(results.get('organic_results', []))} sources")

            except Exception as e:
                print(f"   ⚠️ {search_type} search failed: {e}")

        # 3. REMOVE DUPLICATES AND RANK BY RELEVANCE
        all_sources = []
        seen_urls = set()

        # Combine all results
        for category, results in all_results.items():
            for result in results:
                url = result.get('link', result.get('url', ''))
                if url and url not in seen_urls:
                    result['category'] = category
                    result['relevance_score'] = self._calculate_relevance_score(result, query)
                    all_sources.append(result)
                    seen_urls.add(url)

        # Sort by relevance score
        all_sources.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)

        # Take top 100 most relevant sources
        top_sources = all_sources[:100]

        final_results = {
            "organic_results": [s for s in top_sources if s.get('category') == 'organic_results'],
            "news_results": [s for s in top_sources if s.get('category') == 'news_results'],
            "academic_results": [s for s in top_sources if s.get('category') == 'academic_results'],
            "data_sources": [s for s in top_sources if s.get('category') == 'data_sources'],
            "government_sources": [s for s in top_sources if s.get('category') == 'government_sources'],
            "financial_sources": [s for s in top_sources if s.get('category') == 'financial_sources'],
            "all_sources": top_sources,
            "total_sources": len(top_sources),
            "search_coverage": "comprehensive"
        }

        print(f"🎉 DEEP RESEARCH COMPLETED: {final_results['total_sources']} premium sources found!")
        print(f"   📊 Data/Chart sources: {len(final_results['data_sources'])}")
        print(f"   📰 News sources: {len(final_results['news_results'])}")
        print(f"   🎓 Academic sources: {len(final_results['academic_results'])}")
        print(f"   🏛️ Government sources: {len(final_results['government_sources'])}")
        print(f"   💰 Financial sources: {len(final_results['financial_sources'])}")

        return final_results

    def _perform_search(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform individual search with parameters"""
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "q": search_params["q"],
            "num": search_params.get("num", 20),
            "tbs": search_params.get("tbs"),
            "location": "United States",
            "gl": "us",
            "hl": "en"
        })

        response = requests.post(url, headers=headers, data=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return {"organic_results": []}

    def _search_news(self, query: str, num: int = 20) -> List[Dict[str, Any]]:
        """Search for news articles"""
        try:
            news_url = "https://google.serper.dev/news"
            news_payload = json.dumps({
                "q": query,
                "num": num,
                "location": "United States"
            })

            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }

            news_response = requests.post(news_url, headers=headers, data=news_payload, timeout=15)
            if news_response.status_code == 200:
                news_data = news_response.json()
                return news_data.get("news", [])
            return []

        except Exception as e:
            print(f"News search error: {e}")
            return []

    def _search_data_sources(self, query: str) -> List[Dict[str, Any]]:
        """Search for data visualization and chart sources"""
        data_query = f"{query} chart graph visualization data site:statista.com OR site:ourworldindata.org OR site:kaggle.com OR site:data.gov"

        search_result = self._perform_search({"q": data_query, "num": 15, "tbs": None})
        return search_result.get("organic_results", [])

    def _calculate_relevance_score(self, result: Dict[str, Any], query: str) -> float:
        """Calculate relevance score for ranking sources"""
        score = 0.0

        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        url = result.get('link', result.get('url', '')).lower()
        query_terms = query.lower().split()

        # Title relevance (highest weight)
        for term in query_terms:
            if term in title:
                score += 3.0

        # Snippet relevance
        for term in query_terms:
            if term in snippet:
                score += 1.5

        # URL quality bonus
        quality_domains = ['gov', 'edu', 'org', 'statista', 'bloomberg', 'reuters', 'wsj', 'forbes', 'harvard', 'mit', 'stanford']
        for domain in quality_domains:
            if domain in url:
                score += 2.0

        # Recency bonus (if available)
        if result.get('date') or 'recent' in snippet or '2024' in snippet or '2025' in snippet:
            score += 1.0

        return score

    def comprehensive_research(self, query: str, agent_type: str = "general") -> Dict[str, Any]:
        """
        Perform comprehensive research: web search + AI analysis

        Args:
            query: Research query
            agent_type: Type of agent (research, doctor, market, etc.)

        Returns:
            Complete research results with search data and AI analysis
        """

        print(f"🚀 Starting comprehensive research for: {query}")
        start_time = time.time()

        # Step 1: Deep web search with multiple sources
        search_results = self.deep_web_research(query)

        if search_results.get("error"):
            return {
                "query": query,
                "agent_type": agent_type,
                "success": False,
                "error": search_results["error"],
                "timestamp": datetime.now().isoformat()
            }

        # Step 2: Compile MASSIVE content for extraordinary analysis
        content_for_analysis = self._compile_deep_research_content(search_results)

        # Step 3: AI analysis based on agent type
        analysis_type_map = {
            "research": "general",
            "doctor": "medical",
            "market": "market",
            "financial": "financial",
            "developer": "technical",
            "writer": "general",
            "analyst": "general"
        }

        analysis_type = analysis_type_map.get(agent_type, "general")
        ai_analysis = self.analyze_with_ai(content_for_analysis, analysis_type)

        # Step 4: Compile final results
        processing_time = time.time() - start_time

        final_results = {
            "query": query,
            "agent_type": agent_type,
            "success": True,
            "processing_time": processing_time,
            "timestamp": datetime.now().isoformat(),

            # Search data
            "search_results": search_results,
            "sources": [result["link"] for result in search_results.get("organic_results", [])],
            "source_count": len(search_results.get("organic_results", [])),

            # AI analysis
            "ai_analysis": ai_analysis,
            "executive_summary": ai_analysis.get("summary", ""),
            "analysis": ai_analysis.get("analysis", ""),
            "confidence": ai_analysis.get("confidence", 0.7),
            "key_insights": ai_analysis.get("key_points", []),

            # Metadata
            "total_results_found": search_results.get("total_results", "0"),
            "search_time": search_results.get("search_time", 0)
        }

        print(f"✅ Comprehensive research completed in {processing_time:.2f}s")
        return final_results

    def _compile_deep_research_content(self, search_results: Dict) -> str:
        """Compile MASSIVE search results into extraordinary content for AI analysis"""

        content_parts = []

        # Header with research scope
        total_sources = search_results.get('total_sources', 0)
        content_parts.append(f"🎯 COMPREHENSIVE RESEARCH ANALYSIS")
        content_parts.append(f"📊 Sources Analyzed: {total_sources} premium websites")
        content_parts.append(f"🔍 Research Coverage: {search_results.get('search_coverage', 'comprehensive')}")
        content_parts.append("=" * 100)

        # Add answer box if available
        if search_results.get("answer_box"):
            answer_box = search_results["answer_box"]
            if answer_box.get("answer"):
                content_parts.append(f"🎯 QUICK ANSWER: {answer_box['answer']}")
                content_parts.append("---")

        # Add knowledge graph if available
        if search_results.get("knowledge_graph"):
            kg = search_results["knowledge_graph"]
            if kg.get("description"):
                content_parts.append(f"📚 KNOWLEDGE BASE: {kg['description']}")
                content_parts.append("---")

        # HIGH-PRIORITY SOURCES (Top 20 organic results)
        organic_results = search_results.get("organic_results", [])
        if organic_results:
            content_parts.append("🏆 TOP-TIER WEB SOURCES:")
            for i, result in enumerate(organic_results[:20], 1):
                score = result.get('relevance_score', 0)
                content_parts.append(f"Source #{i} (Relevance: {score:.1f}): {result['title']}")
                content_parts.append(f"URL: {result.get('link', result.get('url', ''))}")
                content_parts.append(f"Content: {result['snippet']}")
                content_parts.append("---")

        # FINANCIAL SOURCES (if available)
        financial_sources = search_results.get("financial_sources", [])
        if financial_sources:
            content_parts.append("💰 FINANCIAL & MARKET SOURCES:")
            for i, result in enumerate(financial_sources[:10], 1):
                content_parts.append(f"Financial Source {i}: {result['title']}")
                content_parts.append(f"URL: {result.get('link', result.get('url', ''))}")
                content_parts.append(f"Content: {result['snippet']}")
                content_parts.append("---")

        # DATA & VISUALIZATION SOURCES
        data_sources = search_results.get("data_sources", [])
        if data_sources:
            content_parts.append("📊 DATA & VISUALIZATION SOURCES:")
            for i, result in enumerate(data_sources[:8], 1):
                content_parts.append(f"Data Source {i}: {result['title']}")
                content_parts.append(f"URL: {result.get('link', result.get('url', ''))}")
                content_parts.append(f"Charts/Data: {result['snippet']}")
                content_parts.append("---")

        # GOVERNMENT & ACADEMIC SOURCES
        govt_sources = search_results.get("government_sources", [])
        academic_sources = search_results.get("academic_results", [])

        if govt_sources:
            content_parts.append("🏛️ GOVERNMENT & OFFICIAL SOURCES:")
            for i, result in enumerate(govt_sources[:5], 1):
                content_parts.append(f"Official Source {i}: {result['title']}")
                content_parts.append(f"URL: {result.get('link', result.get('url', ''))}")
                content_parts.append(f"Official Data: {result['snippet']}")
                content_parts.append("---")

        if academic_sources:
            content_parts.append("🎓 ACADEMIC & RESEARCH SOURCES:")
            for i, result in enumerate(academic_sources[:8], 1):
                content_parts.append(f"Academic Source {i}: {result['title']}")
                content_parts.append(f"URL: {result.get('link', result.get('url', ''))}")
                content_parts.append(f"Research: {result['snippet']}")
                content_parts.append("---")

        # RECENT NEWS & UPDATES
        news_results = search_results.get("news_results", [])
        if news_results:
            content_parts.append("📰 LATEST NEWS & UPDATES:")
            for i, result in enumerate(news_results[:10], 1):
                content_parts.append(f"News {i}: {result['title']}")
                content_parts.append(f"Source: {result.get('source', 'News Source')}")
                content_parts.append(f"Date: {result.get('date', 'Recent')}")
                content_parts.append(f"Content: {result.get('snippet', result.get('description', ''))}")
                content_parts.append("---")

        content_parts.append("=" * 100)
        content_parts.append(f"📋 TOTAL RESEARCH BASE: {total_sources} sources analyzed")

        return "\n".join(content_parts)

    def _extract_confidence(self, analysis_text: str) -> float:
        """Extract confidence level from analysis text"""
        text_lower = analysis_text.lower()

        if "high confidence" in text_lower or "high certainty" in text_lower:
            return 0.9
        elif "medium confidence" in text_lower or "moderate confidence" in text_lower:
            return 0.7
        elif "low confidence" in text_lower or "uncertain" in text_lower:
            return 0.5
        else:
            return 0.7  # Default confidence

    def _extract_key_points(self, analysis_text: str) -> List[str]:
        """Extract key points from analysis text"""
        lines = analysis_text.split('\n')
        key_points = []

        for line in lines:
            line = line.strip()
            # Look for bullet points or numbered lists
            if line.startswith(('•', '-', '*')) or (len(line) > 0 and line[0].isdigit() and '.' in line):
                # Clean up the bullet point
                cleaned = line.lstrip('•-*0123456789. ').strip()
                if len(cleaned) > 10:  # Meaningful content
                    key_points.append(cleaned)

        return key_points[:5]  # Return top 5 key points

    def _extract_summary(self, analysis_text: str) -> str:
        """Extract executive summary from analysis text"""
        lines = analysis_text.split('\n')

        # Look for summary section
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['summary', 'executive', 'conclusion', 'overview']):
                # Get the next few lines as summary
                summary_lines = []
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip() and not lines[j].startswith('#'):
                        summary_lines.append(lines[j].strip())

                if summary_lines:
                    return ' '.join(summary_lines)

        # If no summary section found, return first paragraph
        paragraphs = analysis_text.split('\n\n')
        if paragraphs:
            return paragraphs[0].strip()

        return "Summary not available"