"""
Agent Collaboration System - Real inter-agent communication
Enables agents to share findings and build on each other's research
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from .research_engine import RealResearchEngine

class AgentCollaborationManager:
    """
    Manages real-time collaboration between research agents
    """

    def __init__(self):
        self.research_engine = RealResearchEngine()
        self.collaboration_sessions = {}
        self.agent_communications = []

    def start_collaboration_session(self, session_id: str, agents: List[str], query: str) -> Dict[str, Any]:
        """
        Start a new collaboration session with multiple agents

        Args:
            session_id: Unique session identifier
            agents: List of agent IDs participating
            query: Research query

        Returns:
            Session metadata
        """

        session_data = {
            "session_id": session_id,
            "agents": agents,
            "query": query,
            "start_time": datetime.now().isoformat(),
            "status": "active",
            "agent_results": {},
            "shared_context": {},
            "communications": [],
            "final_synthesis": None
        }

        self.collaboration_sessions[session_id] = session_data

        print(f"🤝 Started collaboration session: {session_id}")
        print(f"   Agents: {', '.join(agents)}")
        print(f"   Query: {query}")

        return session_data

    def execute_collaborative_research(self, session_id: str, mode: str = "parallel") -> Dict[str, Any]:
        """
        Execute collaborative research with real agent communication

        Args:
            session_id: Session identifier
            mode: "parallel" or "sequential"

        Returns:
            Complete collaboration results
        """

        if session_id not in self.collaboration_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.collaboration_sessions[session_id]
        agents = session["agents"]
        query = session["query"]

        print(f"🚀 Executing {mode} collaborative research...")

        if mode == "parallel":
            return self._execute_parallel_research(session)
        else:
            return self._execute_sequential_research(session)

    def _execute_parallel_research(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel research where agents work simultaneously"""

        agents = session["agents"]
        query = session["query"]
        session_id = session["session_id"]

        print(f"⚡ Parallel execution with {len(agents)} agents")

        # Step 1: All agents research simultaneously
        agent_results = {}

        for agent_id in agents:
            print(f"🤖 {agent_id.title()} agent starting research...")

            # Each agent does their specialized research
            agent_result = self.research_engine.comprehensive_research(query, agent_id)

            agent_results[agent_id] = agent_result

            # Store in session
            session["agent_results"][agent_id] = agent_result

            # Print agent contribution to terminal
            print(f"✅ {agent_id.title()} agent completed research")
            print(f"   📊 Sources found: {len(agent_result.get('sources', []))}")
            if agent_result.get('analysis'):
                print(f"   🧠 Analysis: {agent_result['analysis'][:150]}...")
            print(f"   ⏱️  Processing time: {agent_result.get('processing_time', 0):.1f}s")
            print("-" * 50)

        # Step 2: Agents share insights (post-processing collaboration)
        print(f"🔄 Agents sharing insights and collaborating...")

        shared_insights = self._extract_shared_insights(agent_results)
        session["shared_context"] = shared_insights

        # Step 3: Generate collaborative synthesis
        synthesis = self._synthesize_collaborative_results(agent_results, query, shared_insights)
        session["final_synthesis"] = synthesis

        # Step 4: Log collaboration communications
        self._log_collaboration_communications(session_id, agent_results, shared_insights)

        session["status"] = "completed"
        session["end_time"] = datetime.now().isoformat()

        return {
            "session_id": session_id,
            "mode": "parallel",
            "success": True,
            "individual_results": agent_results,
            "shared_insights": shared_insights,
            "synthesized_result": synthesis,
            "collaboration_log": session["communications"],
            "processing_time": self._calculate_session_time(session)
        }

    def _execute_sequential_research(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sequential research where agents build on each other's findings"""

        agents = session["agents"]
        query = session["query"]
        session_id = session["session_id"]

        print(f"🔄 Sequential execution with {len(agents)} agents")

        agent_results = {}
        cumulative_context = {}

        for i, agent_id in enumerate(agents):
            print(f"🤖 {agent_id.title()} agent starting research (step {i+1}/{len(agents)})...")

            # Create enhanced query with context from previous agents
            enhanced_query = self._create_enhanced_query(query, cumulative_context, agent_id)

            # Agent performs research with context
            agent_result = self.research_engine.comprehensive_research(enhanced_query, agent_id)

            # Add context information
            agent_result["context_used"] = len(cumulative_context) > 0
            agent_result["enhanced_query"] = enhanced_query

            agent_results[agent_id] = agent_result
            session["agent_results"][agent_id] = agent_result

            # Extract insights for next agents
            agent_insights = self._extract_agent_insights(agent_result, agent_id)
            cumulative_context[agent_id] = agent_insights

            # Log communication
            self._log_agent_communication(session_id, agent_id, agent_insights, cumulative_context)

            print(f"✅ {agent_id.title()} agent completed, sharing insights with remaining agents")

        # Final synthesis with all accumulated context
        print(f"🔄 Creating final collaborative synthesis...")

        synthesis = self._synthesize_collaborative_results(agent_results, query, cumulative_context)
        session["final_synthesis"] = synthesis
        session["shared_context"] = cumulative_context

        session["status"] = "completed"
        session["end_time"] = datetime.now().isoformat()

        return {
            "session_id": session_id,
            "mode": "sequential",
            "success": True,
            "individual_results": agent_results,
            "shared_context": cumulative_context,
            "synthesized_result": synthesis,
            "collaboration_log": session["communications"],
            "processing_time": self._calculate_session_time(session)
        }

    def _create_enhanced_query(self, original_query: str, context: Dict[str, Any], current_agent: str) -> str:
        """Create enhanced query with context from previous agents"""

        if not context:
            return original_query

        context_parts = [f"Original Query: {original_query}"]
        context_parts.append("\nPrevious Agent Findings:")

        for agent_id, insights in context.items():
            context_parts.append(f"\n{agent_id.title()} Agent Insights:")
            for insight in insights.get("key_points", []):
                context_parts.append(f"• {insight}")

        context_parts.append(f"\nAs the {current_agent} agent, provide your specialized analysis building on these findings.")

        return "\n".join(context_parts)

    def _extract_agent_insights(self, agent_result: Dict[str, Any], agent_id: str) -> Dict[str, Any]:
        """Extract key insights from an agent's research for sharing"""

        return {
            "agent_id": agent_id,
            "key_points": agent_result.get("key_insights", []),
            "summary": agent_result.get("executive_summary", ""),
            "confidence": agent_result.get("confidence", 0.7),
            "source_count": agent_result.get("source_count", 0),
            "specialist_findings": self._extract_specialist_findings(agent_result, agent_id)
        }

    def _extract_specialist_findings(self, agent_result: Dict[str, Any], agent_id: str) -> List[str]:
        """Extract specialist findings based on agent type"""

        analysis = agent_result.get("analysis", "")

        specialist_keywords = {
            "doctor": ["clinical", "medical", "treatment", "symptoms", "diagnosis", "therapy"],
            "financial": ["investment", "financial", "return", "risk", "valuation", "profit"],
            "market": ["market", "competitive", "industry", "trends", "share", "growth"],
            "research": ["study", "research", "evidence", "data", "findings", "analysis"],
            "developer": ["technical", "architecture", "implementation", "scalability", "performance"],
            "writer": ["content", "communication", "messaging", "audience", "strategy"],
            "analyst": ["metrics", "statistics", "patterns", "insights", "correlation"]
        }

        keywords = specialist_keywords.get(agent_id, [])
        findings = []

        # Extract sentences containing specialist keywords
        sentences = analysis.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in keywords) and len(sentence) > 20:
                findings.append(sentence)

        return findings[:3]  # Top 3 specialist findings

    def _extract_shared_insights(self, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract insights that can be shared between agents"""

        all_insights = []
        all_sources = []
        confidence_scores = []

        for agent_id, result in agent_results.items():
            all_insights.extend(result.get("key_insights", []))
            all_sources.extend(result.get("sources", []))
            confidence_scores.append(result.get("confidence", 0.7))

        # Find common themes and cross-references
        common_themes = self._identify_common_themes(agent_results)
        cross_references = self._find_cross_references(agent_results)

        return {
            "common_themes": common_themes,
            "cross_references": cross_references,
            "all_insights": all_insights,
            "unique_sources": list(set(all_sources)),
            "average_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.7,
            "agent_count": len(agent_results)
        }

    def _identify_common_themes(self, agent_results: Dict[str, Any]) -> List[str]:
        """Identify common themes across agent analyses"""

        # Simple keyword-based theme identification
        all_text = ""
        for result in agent_results.values():
            all_text += result.get("analysis", "") + " " + result.get("executive_summary", "")

        common_words = {}
        words = all_text.lower().split()

        # Count significant words (filter out common words)
        stop_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "must", "shall", "this", "that", "these", "those", "a", "an"}

        for word in words:
            word = word.strip('.,!?";()[]{}')
            if len(word) > 4 and word not in stop_words:
                common_words[word] = common_words.get(word, 0) + 1

        # Get most common themes
        sorted_themes = sorted(common_words.items(), key=lambda x: x[1], reverse=True)
        return [theme[0] for theme in sorted_themes[:5]]

    def _find_cross_references(self, agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find cross-references between agent findings"""

        cross_refs = []

        agents = list(agent_results.keys())

        for i, agent1 in enumerate(agents):
            for j, agent2 in enumerate(agents[i+1:], i+1):
                # Compare insights between agents
                agent1_insights = agent_results[agent1].get("key_insights", [])
                agent2_insights = agent_results[agent2].get("key_insights", [])

                # Simple similarity check
                for insight1 in agent1_insights:
                    for insight2 in agent2_insights:
                        similarity = self._calculate_text_similarity(insight1, insight2)
                        if similarity > 0.3:  # Threshold for related insights
                            cross_refs.append({
                                "agent1": agent1,
                                "agent2": agent2,
                                "insight1": insight1,
                                "insight2": insight2,
                                "similarity": similarity
                            })

        return cross_refs[:5]  # Top 5 cross-references

    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Simple text similarity calculation"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0

    def _synthesize_collaborative_results(self, agent_results: Dict[str, Any], original_query: str, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create final synthesis of all agent results"""

        print("🔄 Synthesizing collaborative results with AI...")

        # Compile all findings for synthesis
        synthesis_content = f"Original Query: {original_query}\n\n"

        synthesis_content += "Agent Findings Summary:\n"
        for agent_id, result in agent_results.items():
            synthesis_content += f"\n{agent_id.title()} Agent:\n"
            synthesis_content += f"Summary: {result.get('executive_summary', '')}\n"
            synthesis_content += f"Key Insights: {', '.join(result.get('key_insights', []))}\n"
            synthesis_content += f"Confidence: {result.get('confidence', 0.7):.1%}\n"

        if shared_context.get("common_themes"):
            synthesis_content += f"\nCommon Themes: {', '.join(shared_context['common_themes'])}\n"

        # Use AI to create professional synthesis
        synthesis_prompt = f"""
        Create a comprehensive research synthesis from multiple AI agents who analyzed WEB SEARCH RESULTS.

        IMPORTANT: Each agent analyzed real web search results from the internet. Focus on the web-based findings, data, and sources they discovered.

        Provide a comprehensive research report with:
        1. Executive Summary (3-4 sentences summarizing the web-based findings)
        2. Key Findings from Internet Sources (5-7 bullet points with specific data/facts from websites)
        3. Cross-Agent Insights (insights that emerged from combining different web sources)
        4. Source-Based Confidence Assessment
        5. Actionable Recommendations based on the web research
        6. Website and source references where applicable

        Multi-Agent Web Research Data:
        {synthesis_content}

        Remember: This synthesis should reflect comprehensive internet research findings, not general knowledge.
        """

        # Use Gemini for synthesis with fallback
        print("🤖 Starting AI synthesis...")
        ai_synthesis = self.research_engine.analyze_with_gemini(synthesis_prompt, "general")

        # Check if synthesis was successful
        if ai_synthesis.get("error") or not ai_synthesis.get("analysis"):
            print("⚠️ AI synthesis failed, creating manual synthesis...")
            # Create manual synthesis as fallback
            manual_synthesis = self._create_manual_synthesis(agent_results, original_query, shared_context)
            return manual_synthesis

        return {
            "executive_summary": ai_synthesis.get("summary", ""),
            "detailed_synthesis": ai_synthesis.get("analysis", ""),
            "key_findings": ai_synthesis.get("key_points", []),
            "cross_agent_insights": self._extract_cross_agent_insights(shared_context),
            "confidence_assessment": shared_context.get("average_confidence", 0.7),
            "recommendations": self._extract_recommendations(ai_synthesis.get("analysis", "")),
            "agents_involved": list(agent_results.keys()),
            "total_sources": len(shared_context.get("unique_sources", [])),
            "synthesis_timestamp": datetime.now().isoformat()
        }

    def _create_manual_synthesis(self, agent_results: Dict[str, Any], original_query: str, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create manual synthesis when AI synthesis fails"""

        print("🔧 Creating manual synthesis...")

        # Collect key findings from all agents
        all_findings = []
        all_sources = 0

        executive_parts = []
        for agent_id, result in agent_results.items():
            agent_name = agent_id.title()
            analysis = result.get('analysis', '')

            if analysis:
                # Extract first sentence as key finding
                sentences = analysis.split('. ')
                if sentences:
                    key_finding = sentences[0]
                    all_findings.append(f"{agent_name} Analysis: {key_finding}")
                    executive_parts.append(key_finding)

            # Count sources
            sources = result.get('sources', [])
            all_sources += len(sources)

        # Create executive summary
        executive_summary = f"Based on research from {len(agent_results)} specialized agents analyzing {all_sources} sources, "
        if executive_parts:
            executive_summary += executive_parts[0] + "."
        else:
            executive_summary += f"comprehensive analysis of '{original_query}' has been completed."

        # Create detailed synthesis
        detailed_synthesis = f"# Comprehensive Research Analysis\n\n"
        detailed_synthesis += f"**Query:** {original_query}\n\n"
        detailed_synthesis += f"**Research Summary:** This analysis combines insights from {len(agent_results)} specialized AI agents who analyzed {all_sources} web sources.\n\n"

        for agent_id, result in agent_results.items():
            agent_name = agent_id.title()
            analysis = result.get('analysis', '')
            if analysis:
                detailed_synthesis += f"## {agent_name} Agent Findings\n{analysis[:500]}...\n\n"

        return {
            "executive_summary": executive_summary,
            "detailed_synthesis": detailed_synthesis,
            "key_findings": all_findings[:7],  # Limit to 7 findings
            "cross_agent_insights": self._extract_cross_agent_insights(shared_context),
            "confidence_assessment": shared_context.get("average_confidence", 0.7),
            "recommendations": ["Review individual agent findings", "Consider multiple perspectives", "Verify information from sources"],
            "agents_involved": list(agent_results.keys()),
            "total_sources": all_sources,
            "synthesis_timestamp": datetime.now().isoformat(),
            "synthesis_method": "manual_fallback"
        }

    def _extract_cross_agent_insights(self, shared_context: Dict[str, Any]) -> List[str]:
        """Extract insights that emerged from agent collaboration"""

        insights = []

        # Add common themes as insights
        if shared_context.get("common_themes"):
            insights.append(f"Common research themes identified: {', '.join(shared_context['common_themes'][:3])}")

        # Add cross-references as insights
        for cross_ref in shared_context.get("cross_references", [])[:3]:
            insights.append(f"Correlation found between {cross_ref['agent1']} and {cross_ref['agent2']} findings")

        # Add collaboration quality insight
        agent_count = shared_context.get("agent_count", 0)
        if agent_count > 1:
            insights.append(f"Multi-agent analysis provides {agent_count}-perspective validation")

        return insights

    def _extract_recommendations(self, synthesis_text: str) -> List[str]:
        """Extract recommendations from synthesis text"""

        lines = synthesis_text.split('\n')
        recommendations = []

        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'should', 'consider', 'advise']):
                if len(line) > 20 and not line.startswith('#'):
                    recommendations.append(line)

        return recommendations[:5]

    def _log_agent_communication(self, session_id: str, agent_id: str, insights: Dict[str, Any], cumulative_context: Dict[str, Any]) -> None:
        """Log agent communication for transparency"""

        communication = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "agent_id": agent_id,
            "action": "shared_insights",
            "insights_shared": len(insights.get("key_points", [])),
            "context_received": len(cumulative_context) - 1,  # Exclude self
            "communication_summary": f"{agent_id} shared {len(insights.get('key_points', []))} insights"
        }

        self.agent_communications.append(communication)
        self.collaboration_sessions[session_id]["communications"].append(communication)

    def _log_collaboration_communications(self, session_id: str, agent_results: Dict[str, Any], shared_insights: Dict[str, Any]) -> None:
        """Log final collaboration communications"""

        communication = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "action": "collaboration_synthesis",
            "agents_involved": list(agent_results.keys()),
            "total_insights": len(shared_insights.get("all_insights", [])),
            "cross_references": len(shared_insights.get("cross_references", [])),
            "communication_summary": f"Final synthesis created from {len(agent_results)} agent analyses"
        }

        self.agent_communications.append(communication)
        self.collaboration_sessions[session_id]["communications"].append(communication)

    def _calculate_session_time(self, session: Dict[str, Any]) -> float:
        """Calculate total session processing time"""

        if "start_time" in session and "end_time" in session:
            start = datetime.fromisoformat(session["start_time"])
            end = datetime.fromisoformat(session["end_time"])
            return (end - start).total_seconds()

        return 0.0

    def get_collaboration_log(self, session_id: str) -> List[Dict[str, Any]]:
        """Get collaboration communication log for a session"""

        if session_id in self.collaboration_sessions:
            return self.collaboration_sessions[session_id].get("communications", [])

        return []