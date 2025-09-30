"""
Enhanced Research Engine - Implements advanced Galileo agent techniques
Combines sophisticated planning, deep web extraction, cross-source analysis, and evidence-backed writing
"""

import os
import sys
import requests
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import time
import concurrent.futures
from threading import Lock
import re
from bs4 import BeautifulSoup
import urllib.parse
from collections import defaultdict
import hashlib

# Add paths for configuration
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
from config import Config

class QueryPlanner:
    """Advanced query decomposition using Galileo planner techniques"""

    def __init__(self, use_openai: bool = False):
        self.use_openai = use_openai
        if use_openai:
            import openai
            openai.api_key = Config.OPENAI_API_KEY
            self.client = openai
        else:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_focused_sub_questions(self, user_query: str, num_questions: int = 6) -> List[str]:
        """Generate focused, web-searchable sub-questions using Galileo planning techniques"""

        planning_prompt = f"""
        TASK: Break down this research query into {num_questions} focused, web-searchable sub-questions.

        USER QUERY: "{user_query}"

        Generate sub-questions that are:
        1. SPECIFIC and FOCUSED (not broad or vague)
        2. WEB-SEARCHABLE (will find concrete information online)
        3. COMPLEMENTARY (cover different aspects without overlap)
        4. ACTIONABLE (lead to factual, citable information)
        5. COMPREHENSIVE (together cover the full scope)

        Each sub-question should target specific information that can be found through web search.
        Avoid questions that are too philosophical or opinion-based.
        Focus on factual, data-driven aspects.

        FORMAT: Return as a JSON array of strings:
        ["specific sub-question 1", "specific sub-question 2", ...]

        EXAMPLES of GOOD sub-questions:
        - "What are the current market statistics for [specific technology]?"
        - "Which companies are leading in [specific field] and what are their key products?"
        - "What are the recent technical developments in [specific area] in 2024?"
        - "What challenges and limitations exist with [specific technology]?"

        EXAMPLES of BAD sub-questions:
        - "What is the future of [broad topic]?" (too vague)
        - "Should people use [technology]?" (opinion-based)
        - "How does [technology] make people feel?" (subjective)

        Generate {num_questions} focused sub-questions for: "{user_query}"
        """

        try:
            if self.use_openai:
                response = self.client.chat.completions.create(
                    model=Config.MODEL_NAME,
                    messages=[{"role": "user", "content": planning_prompt}],
                    max_tokens=1500,
                    temperature=0.2
                )
                response_text = response.choices[0].message.content
            else:
                response = self.model.generate_content(planning_prompt)
                response_text = response.text

            # Extract JSON from response
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                sub_questions = json.loads(json_match.group(0))
                return sub_questions[:num_questions]

            # Fallback parsing
            lines = [line.strip() for line in response_text.split('\n') if line.strip()]
            questions = []
            for line in lines:
                if line.startswith('"') and line.endswith('"'):
                    questions.append(line[1:-1])
                elif line.startswith('- '):
                    questions.append(line[2:].strip('"'))

            return questions[:num_questions]

        except Exception as e:
            print(f"❌ Planning error: {e}")
            # Fallback decomposition
            return self._fallback_decomposition(user_query, num_questions)

    def _fallback_decomposition(self, user_query: str, num_questions: int) -> List[str]:
        """Fallback decomposition when AI fails"""

        base_aspects = [
            f"What is {user_query} and how does it work?",
            f"What are the current applications and use cases of {user_query}?",
            f"What are the advantages and benefits of {user_query}?",
            f"What are the challenges and limitations of {user_query}?",
            f"What are the recent developments in {user_query}?",
            f"What is the market outlook for {user_query}?"
        ]

        return base_aspects[:num_questions]


class WebScout:
    """Deep web extraction using Galileo scout techniques"""

    def __init__(self):
        self.serper_api_key = Config.SERPER_API_KEY
        self.serper_url = "https://google.serper.dev/search"
        self.min_sources_per_query = 5
        self.target_sources_per_query = 3  # Reduced for speed
        self.max_search_results = 12
        self.rate_limit_lock = Lock()

        self.scraping_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

    def deep_search_all_questions(self, sub_questions: List[str]) -> Dict[str, List[Dict]]:
        """Deep search with content extraction for all sub-questions"""

        print(f"\n🔍 SCOUT: Starting deep web extraction for {len(sub_questions)} queries")

        all_sources_data = {}

        for i, question in enumerate(sub_questions, 1):
            print(f"\n📍 [{i}/{len(sub_questions)}] Extracting: {question[:60]}...")

            try:
                # Deep search with content extraction
                question_sources = self._deep_search_with_extraction(question)

                # Ensure minimum sources
                if len(question_sources) < self.min_sources_per_query:
                    additional_sources = self._search_deeper(question, len(question_sources))
                    question_sources.extend(additional_sources)

                # Rank by relevance and take top sources
                ranked_sources = self._rank_by_relevance(question, question_sources)
                final_sources = ranked_sources[:self.target_sources_per_query]

                all_sources_data[question] = final_sources

                print(f"   ✅ Extracted {len(final_sources)} high-quality sources")

                # Rate limiting
                time.sleep(2)

            except Exception as e:
                print(f"   ❌ Extraction error: {e}")
                all_sources_data[question] = []

        total_sources = sum(len(sources) for sources in all_sources_data.values())
        print(f"\n🔍 Deep extraction completed: {total_sources} sources with content extracted")

        return all_sources_data

    def _deep_search_with_extraction(self, query: str) -> List[Dict]:
        """Deep search with immediate content extraction"""

        # Multiple search strategies
        direct_results = self._serper_search(query)
        expanded_results = self._serper_search(f"{query} guide examples")

        # Combine and deduplicate
        all_results = direct_results + expanded_results
        unique_results = self._remove_duplicates(all_results)

        # Extract content in parallel
        results_with_content = self._extract_content_parallel(unique_results)

        return results_with_content

    def _serper_search(self, query: str) -> List[Dict]:
        """Search using Serper API"""

        # Clean query
        if len(query.split()) > 12:
            query = ' '.join(query.split()[:12])
        query = query.replace('"', '').replace('(', '').replace(')', '')

        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }

        payload = {
            'q': query,
            'num': self.max_search_results,
            'gl': 'us',
            'hl': 'en'
        }

        try:
            with self.rate_limit_lock:
                response = requests.post(
                    self.serper_url,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=15
                )
                response.raise_for_status()

            data = response.json()
            results = []

            if 'organic' in data:
                for item in data['organic']:
                    result = {
                        'title': item.get('title', 'No title'),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', 'No snippet'),
                        'query': query,
                        'search_position': len(results) + 1
                    }
                    results.append(result)

            return results

        except Exception as e:
            print(f"   Serper error: {e}")
            return []

    def _search_deeper(self, query: str, current_count: int) -> List[Dict]:
        """Search deeper when not enough sources found"""

        needed = self.min_sources_per_query - current_count
        deeper_terms = [
            f"{query} research analysis",
            f"{query} technical details",
            f"{query} case studies examples"
        ]

        deeper_results = []
        for term in deeper_terms:
            if len(deeper_results) >= needed:
                break
            results = self._serper_search(term)
            deeper_results.extend(results[:3])
            time.sleep(1)

        return deeper_results[:needed]

    def _remove_duplicates(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicate URLs"""

        seen_urls = set()
        unique_results = []

        for result in results:
            url = result.get('url', '').lower()
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        return unique_results

    def _extract_content_parallel(self, results: List[Dict]) -> List[Dict]:
        """Extract content from URLs in parallel"""

        def extract_single_url(result):
            try:
                url = result.get('url', '')
                if not url:
                    return None

                response = requests.get(url, headers=self.scraping_headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Remove unwanted elements
                for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    element.decompose()

                content = soup.get_text(separator=' ', strip=True)
                cleaned_content = re.sub(r'\s+', ' ', content).strip()

                result.update({
                    'extracted_content': cleaned_content[:1200],  # Limit content
                    'content_length': len(cleaned_content),
                    'extraction_success': True
                })

                return result

            except Exception as e:
                result.update({
                    'extracted_content': result.get('snippet', ''),
                    'content_length': len(result.get('snippet', '')),
                    'extraction_success': False,
                    'extraction_error': str(e)
                })
                return result

        results_with_content = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_result = {
                executor.submit(extract_single_url, result): result
                for result in results
            }

            for future in concurrent.futures.as_completed(future_to_result):
                try:
                    result_with_content = future.result(timeout=15)
                    if result_with_content:
                        results_with_content.append(result_with_content)
                except Exception as e:
                    print(f"   Content extraction failed: {e}")

        return results_with_content

    def _rank_by_relevance(self, query: str, sources: List[Dict]) -> List[Dict]:
        """Rank sources by relevance using Galileo techniques"""

        for source in sources:
            relevance = self._calculate_relevance_score(query, source)
            source['relevance_score'] = relevance

        return sorted(sources, key=lambda x: x['relevance_score'], reverse=True)

    def _calculate_relevance_score(self, query: str, source: Dict) -> float:
        """Calculate relevance score using multiple factors"""

        title = source.get('title', '').lower()
        snippet = source.get('snippet', '').lower()
        content = source.get('extracted_content', '').lower()
        url = source.get('url', '').lower()

        query_words = set(word.strip() for word in query.lower().split() if len(word.strip()) > 2)

        if not query_words:
            return 0.0

        # Title relevance (30%)
        title_words = set(word.strip() for word in title.split() if len(word.strip()) > 2)
        title_overlap = len(query_words.intersection(title_words))
        title_score = (title_overlap / len(query_words)) * 0.30

        # Content relevance (40%)
        content_words = set(word.strip() for word in content.split() if len(word.strip()) > 2)
        content_overlap = len(query_words.intersection(content_words))
        content_score = (content_overlap / len(query_words)) * 0.40

        # Snippet relevance (20%)
        snippet_words = set(word.strip() for word in snippet.split() if len(word.strip()) > 2)
        snippet_overlap = len(query_words.intersection(snippet_words))
        snippet_score = (snippet_overlap / len(query_words)) * 0.20

        # Quality indicators (10%)
        quality_score = 0.0
        if source.get('extraction_success', False):
            quality_score += 0.05
        if any(domain in url for domain in ['edu', 'org', 'gov']):
            quality_score += 0.05

        total_score = title_score + content_score + snippet_score + quality_score
        return min(total_score, 1.0)


class InformationAnalyst:
    """Cross-source synthesis using Galileo analyst techniques"""

    def __init__(self, use_openai: bool = False):
        self.use_openai = use_openai
        if use_openai:
            import openai
            openai.api_key = Config.OPENAI_API_KEY
            self.client = openai
        else:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.5-flash")

    def analyze_and_synthesize(self, sources_data: Dict[str, List[Dict]]) -> Dict:
        """Analyze and synthesize information across sources using Galileo techniques"""

        print(f"\n🔬 ANALYST: Starting cross-source synthesis...")

        analysis_results = {
            'sub_question_answers': {},
            'synthesized_insights': {},
            'source_quality_analysis': {},
            'cross_source_validation': {},
            'metadata': {
                'total_sources_analyzed': 0,
                'high_quality_sources': 0
            }
        }

        total_sources = 0

        for sub_question, sources in sources_data.items():
            if not sources:
                continue

            print(f"\n📍 Analyzing: {sub_question[:60]}...")

            try:
                # Filter quality sources
                quality_sources = self._assess_source_quality(sources)

                # Extract information from each source
                source_extractions = self._extract_information_from_sources(quality_sources, sub_question)

                # Synthesize across sources
                synthesized_answer = self._synthesize_information(source_extractions, sub_question)

                # Store results
                analysis_results['sub_question_answers'][sub_question] = synthesized_answer
                analysis_results['source_quality_analysis'][sub_question] = {
                    'total_sources': len(sources),
                    'quality_sources': len(quality_sources)
                }

                total_sources += len(sources)

                print(f"   ✅ Synthesized from {len(quality_sources)} quality sources")

            except Exception as e:
                print(f"   ❌ Analysis error: {e}")
                analysis_results['sub_question_answers'][sub_question] = {
                    'answer': f"Analysis failed: {str(e)}",
                    'source_urls': [],
                    'confidence_score': 0.0
                }

        # Generate overall insights
        analysis_results['synthesized_insights'] = self._generate_overall_insights(
            analysis_results['sub_question_answers']
        )

        analysis_results['metadata']['total_sources_analyzed'] = total_sources

        print(f"🔬 Analysis completed: {total_sources} sources analyzed")

        return analysis_results

    def _assess_source_quality(self, sources: List[Dict]) -> List[Dict]:
        """Assess source quality using multiple indicators"""

        quality_sources = []

        for source in sources:
            content_length = len(source.get('extracted_content', ''))
            relevance_score = source.get('relevance_score', 0)
            extraction_success = source.get('extraction_success', False)

            # Quality scoring
            quality_score = 0.0

            if content_length >= 500:
                quality_score += 0.3
            elif content_length >= 200:
                quality_score += 0.2
            elif content_length >= 100:
                quality_score += 0.1

            quality_score += min(relevance_score * 0.4, 0.4)

            if extraction_success:
                quality_score += 0.2

            url = source.get('url', '').lower()
            if any(domain in url for domain in ['edu', 'org', 'gov']):
                quality_score += 0.1

            source['quality_score'] = quality_score

            # Filter based on minimum thresholds
            if content_length >= 100 and relevance_score >= 0.2:
                quality_sources.append(source)

        # Sort by quality and take top sources
        quality_sources.sort(key=lambda x: x['quality_score'], reverse=True)
        return quality_sources[:3]  # Top 3 sources per question (reduced for speed)

    def _extract_information_from_sources(self, sources: List[Dict], sub_question: str) -> List[Dict]:
        """Extract key information from each source"""

        extractions = []

        for source in sources:
            try:
                content = source.get('extracted_content', '')
                if len(content) < 50:
                    continue

                extraction_result = self._ai_extract_information(content, sub_question, source)

                if extraction_result and extraction_result.get('key_information'):
                    extractions.append(extraction_result)

            except Exception as e:
                print(f"   ⚠️ Extraction failed for {source.get('url', 'unknown')}: {e}")

        return extractions

    def _ai_extract_information(self, content: str, sub_question: str, source: Dict) -> Dict:
        """Use AI to extract key information from source content"""

        extraction_prompt = f"""
        Extract specific, factual information from this content to answer the sub-question.

        SUB-QUESTION: "{sub_question}"
        SOURCE: {source.get('url', 'unknown')}

        CONTENT:
        {content[:1500]}

        Extract key facts that directly answer the sub-question. Return as JSON:
        {{
            "key_information": [
                {{
                    "fact": "specific factual statement",
                    "relevance": "how this answers the question",
                    "confidence": 0.9
                }}
            ],
            "main_points": ["key point 1", "key point 2"],
            "source_authority": {{
                "appears_reliable": true/false,
                "reasoning": "why reliable or not"
            }}
        }}

        Only extract factual, specific information directly relevant to the sub-question.
        """

        try:
            if self.use_openai:
                response = self.client.chat.completions.create(
                    model=Config.MODEL_NAME,
                    messages=[{"role": "user", "content": extraction_prompt}],
                    max_tokens=1000,
                    temperature=0.2
                )
                response_text = response.choices[0].message.content
            else:
                response = self.model.generate_content(extraction_prompt)
                response_text = response.text

            # Clean and parse JSON
            cleaned_response = self._clean_json_response(response_text)
            extraction_data = json.loads(cleaned_response)

            # Add source metadata
            if 'key_information' in extraction_data:
                for fact in extraction_data['key_information']:
                    fact['source_url'] = source.get('url')
                    fact['source_title'] = source.get('title')

            extraction_data['source_metadata'] = {
                'url': source.get('url'),
                'title': source.get('title'),
                'quality_score': source.get('quality_score', 0),
                'relevance_score': source.get('relevance_score', 0)
            }

            return extraction_data

        except Exception as e:
            print(f"AI extraction error: {e}")
            return {}

    def _synthesize_information(self, extractions: List[Dict], sub_question: str) -> Dict:
        """Synthesize information from multiple sources"""

        if not extractions:
            return {
                'answer': f"No sufficient information found for: {sub_question}",
                'source_urls': [],
                'confidence_score': 0.0
            }

        # Prepare synthesis data
        all_facts = []
        all_sources = []

        for extraction in extractions:
            if 'key_information' in extraction:
                all_facts.extend(extraction['key_information'])
            if 'source_metadata' in extraction:
                all_sources.append(extraction['source_metadata'])

        synthesis_prompt = f"""
        Synthesize information from multiple sources to comprehensively answer this question.

        QUESTION: "{sub_question}"

        EXTRACTED FACTS:
        {json.dumps(all_facts, indent=2)[:2500]}

        SOURCES: {len(all_sources)} analyzed

        Create a comprehensive answer by:
        1. Combining complementary information
        2. Identifying most reliable facts
        3. Resolving contradictions
        4. Providing complete coverage

        Return as JSON:
        {{
            "synthesized_answer": "comprehensive answer",
            "key_points": [
                {{
                    "point": "main point",
                    "supporting_sources": ["url1", "url2"],
                    "confidence": 0.9
                }}
            ],
            "overall_confidence": 0.85,
            "information_completeness": 0.8
        }}
        """

        try:
            if self.use_openai:
                response = self.client.chat.completions.create(
                    model=Config.MODEL_NAME,
                    messages=[{"role": "user", "content": synthesis_prompt}],
                    max_tokens=1500,
                    temperature=0.2
                )
                response_text = response.choices[0].message.content
            else:
                response = self.model.generate_content(synthesis_prompt)
                response_text = response.text

            cleaned_response = self._clean_json_response(response_text)
            synthesis_result = json.loads(cleaned_response)

            source_urls = [s['url'] for s in all_sources if s.get('url')]

            return {
                'answer': synthesis_result.get('synthesized_answer', ''),
                'key_points': synthesis_result.get('key_points', []),
                'source_urls': source_urls,
                'confidence_score': synthesis_result.get('overall_confidence', 0.0),
                'completeness_score': synthesis_result.get('information_completeness', 0.0),
                'sources_count': len(all_sources)
            }

        except Exception as e:
            print(f"Synthesis error: {e}")
            return self._fallback_synthesis(all_facts, all_sources, sub_question)

    def _generate_overall_insights(self, sub_question_answers: Dict) -> Dict:
        """Generate overall insights connecting information across sub-questions"""

        insights_prompt = f"""
        Generate overall insights by connecting information across all sub-questions.

        SUB-QUESTION ANSWERS:
        {json.dumps({q: a.get('answer', '') for q, a in sub_question_answers.items()}, indent=2)[:2500]}

        Identify:
        1. Common themes across sub-questions
        2. Connections between different aspects
        3. Overarching insights

        Return as JSON:
        {{
            "key_insights": ["insight 1", "insight 2"],
            "thematic_connections": {{
                "theme_1": ["sub-question 1", "sub-question 3"]
            }},
            "knowledge_synthesis": "high-level synthesis"
        }}
        """

        try:
            if self.use_openai:
                response = self.client.chat.completions.create(
                    model=Config.MODEL_NAME,
                    messages=[{"role": "user", "content": insights_prompt}],
                    max_tokens=1000,
                    temperature=0.3
                )
                response_text = response.choices[0].message.content
            else:
                response = self.model.generate_content(insights_prompt)
                response_text = response.text

            cleaned_response = self._clean_json_response(response_text)
            return json.loads(cleaned_response)
        except:
            return {
                "key_insights": ["Analysis completed across multiple sources"],
                "knowledge_synthesis": "Information synthesized from multiple sources"
            }

    def _fallback_synthesis(self, all_facts: List[Dict], all_sources: List[Dict], sub_question: str) -> Dict:
        """Fallback synthesis when AI fails"""

        if not all_facts:
            return {
                'answer': f"Unable to find sufficient information for: {sub_question}",
                'source_urls': [],
                'confidence_score': 0.0
            }

        high_conf_facts = [f for f in all_facts if f.get('confidence', 0) >= 0.7]

        if high_conf_facts:
            answer = ". ".join([f['fact'] for f in high_conf_facts[:3]])
        else:
            answer = ". ".join([f['fact'] for f in all_facts[:3]])

        source_urls = [s['url'] for s in all_sources if s.get('url')]

        return {
            'answer': answer,
            'source_urls': source_urls,
            'confidence_score': 0.6,
            'sources_count': len(all_sources)
        }

    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response"""
        try:
            cleaned = re.sub(r'```json\s*', '', response_text)
            cleaned = re.sub(r'```\s*$', '', cleaned)

            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                return json_match.group(0)

            return cleaned.strip()
        except:
            return response_text


class ReportWriter:
    """Evidence-backed report generation using Galileo writer techniques"""

    def __init__(self, use_openai: bool = False):
        self.use_openai = use_openai
        if use_openai:
            import openai
            openai.api_key = Config.OPENAI_API_KEY
            self.client = openai
        else:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_comprehensive_report(self, user_topic: str, analysis_results: Dict) -> Dict:
        """Generate comprehensive report with inline citations using Galileo techniques"""

        print(f"\n✍️ WRITER: Generating evidence-backed report...")

        sub_question_answers = analysis_results.get('sub_question_answers', {})
        synthesized_insights = analysis_results.get('synthesized_insights', {})

        # Build source citation map
        source_citation_map = self._build_source_citation_map(sub_question_answers)

        try:
            # Generate markdown report
            markdown_report = self._generate_markdown_report(
                user_topic, sub_question_answers, synthesized_insights, source_citation_map
            )

            # Validate and format
            validated_report = self._validate_and_format_report(markdown_report, source_citation_map)

            # Generate metadata
            report_metadata = self._generate_report_metadata(user_topic, validated_report, analysis_results)

            print(f"✅ Generated {len(validated_report.split())} word report")
            print(f"🔗 Citations included: {report_metadata['citation_count']}")

            return {
                'markdown_report': validated_report,
                'metadata': report_metadata,
                'source_citation_map': source_citation_map
            }

        except Exception as e:
            print(f"❌ Report generation error: {e}")
            return self._generate_fallback_report(user_topic, analysis_results)

    def _build_source_citation_map(self, sub_question_answers: Dict) -> Dict:
        """Build comprehensive source citation map"""

        citation_map = {}

        for question, answer_data in sub_question_answers.items():
            source_urls = answer_data.get('source_urls', [])

            for url in source_urls:
                if url not in citation_map:
                    source_title = self._generate_source_title_from_url(url)
                    citation_map[url] = {
                        'title': source_title,
                        'url': url,
                        'question_context': question
                    }

        return citation_map

    def _generate_source_title_from_url(self, url: str) -> str:
        """Generate readable source title from URL"""

        if not url:
            return "Source"

        try:
            domain = url.split('/')[2].replace('www.', '')

            domain_titles = {
                'arxiv.org': 'ArXiv Research Paper',
                'github.com': 'GitHub Repository',
                'stackoverflow.com': 'Stack Overflow',
                'medium.com': 'Medium Article',
                'towardsdatascience.com': 'Towards Data Science',
                'pytorch.org': 'PyTorch Documentation',
                'tensorflow.org': 'TensorFlow Documentation',
                'wikipedia.org': 'Wikipedia',
                'nature.com': 'Nature Journal',
                'sciencedirect.com': 'ScienceDirect'
            }

            for known_domain, title in domain_titles.items():
                if known_domain in domain:
                    return title

            return domain.replace('.com', '').replace('.org', '').replace('.edu', '').title()

        except:
            return "Source"

    def _generate_markdown_report(self, user_topic: str, sub_question_answers: Dict,
                                  synthesized_insights: Dict, source_citation_map: Dict) -> str:
        """Generate comprehensive markdown report with inline citations"""

        report_prompt = f"""
        Generate a comprehensive, evidence-backed research report in Markdown format.

        TOPIC: "{user_topic}"

        RESEARCH DATA:
        {json.dumps({q: a.get('answer', '') for q, a in sub_question_answers.items()}, indent=2)[:3000]}

        INSIGHTS:
        {json.dumps(synthesized_insights, indent=2)[:1000]}

        CITATION MAP:
        {json.dumps(source_citation_map, indent=2)[:1500]}

        CRITICAL REQUIREMENTS:
        1. **MANDATORY INLINE CITATIONS**: Every factual statement MUST be followed by [Source Title](URL)
        2. **NO NUMBERED CITATIONS**: Use inline format: [Title](URL)
        3. **Comprehensive Coverage**: Address all aspects from research
        4. **Professional Structure**: Use proper markdown headers and formatting
        5. **Evidence-Based**: Every claim must have source attribution

        STRUCTURE:

        # {user_topic}

        ## Executive Summary
        [Key findings with citations]

        ## Introduction
        [Context and scope with citations]

        ## Key Findings
        [Main discoveries with heavy citations]

        ## Detailed Analysis
        [In-depth examination with citations for every claim]

        ## Insights and Implications
        [Cross-cutting insights with supporting citations]

        ## Conclusion
        [Summary with key source citations]

        ## Sources
        [Complete list of sources with URLs]

        CITATION EXAMPLES:
        - "BERT uses bidirectional training [Understanding BERT](https://example.com/bert)."
        - "Performance reached 80.5% accuracy [BERT Analysis](https://research.com/bert)."

        Generate a complete, professional report with comprehensive inline citations.
        EVERY factual statement must have a source citation.
        """

        try:
            if self.use_openai:
                response = self.client.chat.completions.create(
                    model=Config.MODEL_NAME,
                    messages=[{"role": "user", "content": report_prompt}],
                    max_tokens=4000,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            else:
                response = self.model.generate_content(report_prompt)
                return response.text.strip()

        except Exception as e:
            print(f"AI report generation error: {e}")
            raise

    def _validate_and_format_report(self, markdown_report: str, source_citation_map: Dict) -> str:
        """Validate citations and format report"""

        # Count citations
        citation_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        citations = re.findall(citation_pattern, markdown_report)

        print(f"🔍 Found {len(citations)} citations in report")

        # Ensure proper formatting
        formatted_report = self._ensure_markdown_formatting(markdown_report)

        # Add report header
        final_report = self._add_report_header(formatted_report)

        return final_report

    def _ensure_markdown_formatting(self, report: str) -> str:
        """Ensure proper markdown formatting"""

        formatted = report

        # Fix header spacing
        formatted = re.sub(r'\n(#{1,6})', r'\n\n\1', formatted)
        formatted = re.sub(r'(#{1,6}.*?)\n([^\n#])', r'\1\n\n\2', formatted)

        # Fix list spacing
        formatted = re.sub(r'\n(\s*[-*+])', r'\n\n\1', formatted)

        # Clean multiple newlines
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)

        return formatted.strip()

    def _add_report_header(self, report: str) -> str:
        """Add metadata header"""

        header = f"""---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generator: Enhanced AI Research Engine
Format: Evidence-Backed Research Report
---

"""
        return header + report

    def _generate_report_metadata(self, user_topic: str, report: str, analysis_results: Dict) -> Dict:
        """Generate comprehensive report metadata"""

        word_count = len(report.split())
        citation_count = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', report))
        section_count = len(re.findall(r'^#+', report, re.MULTILINE))

        total_sources = analysis_results.get('metadata', {}).get('total_sources_analyzed', 0)

        return {
            'generation_timestamp': datetime.now().isoformat(),
            'user_topic': user_topic,
            'word_count': word_count,
            'citation_count': citation_count,
            'section_count': section_count,
            'sources_analyzed': total_sources,
            'report_quality_score': min(citation_count * 0.1, 1.0),
            'sub_questions_covered': len(analysis_results.get('sub_question_answers', {}))
        }

    def _generate_fallback_report(self, user_topic: str, analysis_results: Dict) -> Dict:
        """Generate fallback report when main generation fails"""

        fallback_report = f"""---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Generator: Enhanced AI Research Engine (Fallback Mode)
---

# {user_topic}

## Report Generation Notice

This report was generated in fallback mode due to technical issues.

## Research Summary

Research was completed with {len(analysis_results.get('sub_question_answers', {}))} sub-questions analyzed.

## Recommendations

For complete analysis:
1. Review saved research data
2. Re-run report generation
"""

        return {
            'markdown_report': fallback_report,
            'metadata': {
                'generation_timestamp': datetime.now().isoformat(),
                'user_topic': user_topic,
                'fallback_mode': True,
                'word_count': len(fallback_report.split()),
                'citation_count': 0
            }
        }


class EnhancedResearchEngine:
    """
    Enhanced research engine implementing Galileo agent techniques:
    - Advanced query decomposition and planning
    - Deep web extraction with content analysis
    - Cross-source synthesis and validation
    - Evidence-backed report generation with inline citations
    """

    def __init__(self):
        """Initialize enhanced research engine with Galileo-style components"""
        self.serper_api_key = Config.SERPER_API_KEY
        self.use_openai = Config.USE_OPENAI

        if self.use_openai:
            self.openai_api_key = Config.OPENAI_API_KEY
            if not self.serper_api_key or not self.openai_api_key:
                raise ValueError("OpenAI and Serper API keys not configured. Check your .env file.")
            print("✅ Enhanced Research Engine initialized with OpenAI API")
        else:
            self.gemini_api_key = Config.GEMINI_API_KEY
            if not self.serper_api_key or not self.gemini_api_key:
                raise ValueError("Gemini and Serper API keys not configured. Check your .env file.")
            print("✅ Enhanced Research Engine initialized with Gemini API")

        # Initialize Galileo-style agent components
        self.planner = QueryPlanner(self.use_openai)
        self.scout = WebScout()
        self.analyst = InformationAnalyst(self.use_openai)
        self.writer = ReportWriter(self.use_openai)

    def comprehensive_research(self, user_query: str, num_sub_questions: int = 3) -> Dict[str, Any]:  # Reduced to 3 for speed
        """
        Perform comprehensive research using Galileo agent workflow:
        1. Planning: Break down query into focused sub-questions
        2. Scouting: Deep web extraction with content analysis
        3. Analysis: Cross-source synthesis and validation
        4. Writing: Evidence-backed report generation
        """

        print(f"\n🚀 Starting comprehensive research for: {user_query}")
        print(f"🎯 Target sub-questions: {num_sub_questions}")

        research_context = {
            'user_query': user_query,
            'start_time': datetime.now(),
            'agents_used': ['planner', 'scout', 'analyst', 'writer']
        }

        try:
            # PHASE 1: PLANNING - Generate focused sub-questions
            print(f"\n📋 PHASE 1: Query decomposition and planning")
            sub_questions = self.planner.generate_focused_sub_questions(user_query, num_sub_questions)

            print(f"✅ Generated {len(sub_questions)} focused sub-questions:")
            for i, q in enumerate(sub_questions, 1):
                print(f"   {i}. {q}")

            research_context['sub_questions'] = sub_questions

            # PHASE 2: SCOUTING - Deep web extraction
            print(f"\n🔍 PHASE 2: Deep web extraction and content analysis")
            sources_data = self.scout.deep_search_all_questions(sub_questions)
            research_context['sources_data'] = sources_data

            # PHASE 3: ANALYSIS - Cross-source synthesis
            print(f"\n🔬 PHASE 3: Cross-source analysis and synthesis")
            analysis_results = self.analyst.analyze_and_synthesize(sources_data)
            research_context['analysis_results'] = analysis_results

            # PHASE 4: WRITING - Evidence-backed report generation
            print(f"\n✍️ PHASE 4: Evidence-backed report generation")
            report_results = self.writer.generate_comprehensive_report(user_query, analysis_results)
            research_context['report_results'] = report_results

            # Compile final results
            research_context['end_time'] = datetime.now()
            research_context['duration'] = (research_context['end_time'] - research_context['start_time']).total_seconds()

            print(f"\n🎉 Research completed in {research_context['duration']:.1f} seconds")
            print(f"📊 Total sources analyzed: {analysis_results['metadata']['total_sources_analyzed']}")
            print(f"📝 Report word count: {report_results['metadata']['word_count']}")
            print(f"🔗 Citations included: {report_results['metadata']['citation_count']}")

            return {
                'success': True,
                'research_context': research_context,
                'markdown_report': report_results['markdown_report'],
                'metadata': report_results['metadata'],
                'source_citation_map': report_results.get('source_citation_map', {}),
                'analysis_results': analysis_results
            }

        except Exception as e:
            print(f"❌ Research failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'research_context': research_context
            }

    # Legacy method compatibility
    def analyze_with_ai(self, sources_text: str, user_query: str, timeout: int = 180) -> str:
        """Legacy compatibility method - redirects to comprehensive research"""

        print("⚠️  Using legacy analyze_with_ai method - redirecting to enhanced research")

        result = self.comprehensive_research(user_query)

        if result['success']:
            return result['markdown_report']
        else:
            return f"Research failed: {result.get('error', 'Unknown error')}"

    def search_web(self, query: str, num_results: int = 20) -> Dict[str, Any]:
        """Legacy compatibility method"""

        print("⚠️  Using legacy search_web method - use comprehensive_research instead")

        # Use scout for web search
        results = self.scout._serper_search(query)

        return {
            'success': True,
            'results': results[:num_results],
            'total_results': len(results),
            'query': query
        }