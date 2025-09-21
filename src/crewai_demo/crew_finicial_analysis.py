from crewai import Agent, Task, Crew, task
from crewai.project import CrewBase, agent
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai.tools import SerperDevTool, ScrapeWebsiteTool

@CrewBase
class CrewFinancialAnalysis():

    agents: List[BaseAgent]
    tasks: List[Task]
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    @agent
    def data_analyst_agent(self) -> Agent:
        return Agent(
        role="Data Analyst",
        goal="Monitor and analyze market data in real-time "
            "to identify trends and predict market movements.",
        backstory="Specializing in financial markets, this agent "
                "uses statistical modeling and machine learning "
                "to provide crucial insights. With a knack for data, "
                "the Data Analyst Agent is the cornerstone for "
                "informing trading decisions.",
        verbose=True,
        allow_delegation=True,
        tools = [scrape_tool, search_tool]
    )

    @agent
    def trading_strategy_agent(self) -> Agent:
        return Agent(
            role="Trading Strategy Developer",
            goal="Develop and test various trading strategies based "
            "on insights from the Data Analyst Agent.",

            backstory="Equipped with a deep understanding of financial "
                "markets and quantitative analysis, this agent "
                "devises and refines trading strategies. It evaluates "
                "the performance of different approaches to determine "
                "the most profitable and risk-averse options.",
            verbose=True,
            allow_delegation=True,
            tools = [scrape_tool, search_tool]
        )
    @agent
    def risk_management_agent(self) -> Agent:
        return Agent(
            role="Risk Advisor",
            goal="Evaluate and provide insights on the risks "
            "associated with potential trading activities.",
                backstory="Armed with a deep understanding of risk assessment models "
                "and market dynamics, this agent scrutinizes the potential "
                "risks of proposed trades. It offers a detailed analysis of "
                "risk exposure and suggests safeguards to ensure that "
                "trading activities align with the firm’s risk tolerance.",
            verbose=True,
            allow_delegation=True,
            tools = [scrape_tool, search_tool]
        )

    @agent
    def execution_agent(self) -> Agent:
        return Agent(
            role="Trade Advisor",
            goal="Suggest optimal trade execution strategies "
            "based on approved trading strategies.",
            backstory="Equipped with a deep understanding of financial "
                "markets and quantitative analysis, this agent "
                "devises and refines trading strategies. It evaluates "
                "the performance of different approaches to determine "
                "the most profitable and risk-averse options.",
        verbose=True,
        allow_delegation=True,
        tools = [scrape_tool, search_tool]
    )

    @task
    def data_analysis_task(self) -> Task:
        return Task(
            description=(
            "Continuously monitor and analyze market data for "
            "the selected stock ({stock_selection}). "
            "Use statistical modeling and machine learning to "
            "identify trends and predict market movements."
            ),
            expected_output=(
                "Insights and alerts about significant market "
                "opportunities or threats for {stock_selection}."
        ),
        agent=data_analyst_agent,
    )

    @task
    def trading_strategy_task(self) -> Task:
        return Task(
            description=(
            "Develop and refine trading strategies based on "
            "the insights from the Data Analyst and "
            "user-defined risk tolerance ({risk_tolerance}). "
            "Consider trading preferences ({trading_strategy_preference})."
                        ),
            expected_output=(
                "A set of potential trading strategies for {stock_selection} "
                "that align with the user's risk tolerance."
            ),
            agent=trading_strategy_agent,
        )

    @task
    def execution_task(self) -> Task:
        return Task(
            description=(
            "Analyze approved trading strategies to determine the "
            "best execution methods for {stock_selection}, "
            "considering current market conditions and optimal pricing."
            ),
            expected_output=(
                "Detailed execution plans suggesting how and when to "
                "execute trades for {stock_selection}."
            ),
            agent=execution_agent,
        )

    @task
    def risk_management_task(self) -> Task:
        return Task(
            description=(
                "Evaluate the risks associated with the proposed trading "
                "strategies and execution plans for {stock_selection}. "
                "Provide a detailed analysis of potential risks "
                "and suggest mitigation strategies."
            ),
            expected_output=(
                "A comprehensive risk analysis report detailing potential "
                "risks and mitigation recommendations for {stock_selection}."
            ),
            agent=risk_management_agent,
        )

    @crew
    def financial_trading_crew(self) -> Crew:
        return Crew(
            agents=[data_analyst_agent, 
                    trading_strategy_agent, 
                    execution_agent, 
                    risk_management_agent],
            tasks=[data_analysis_task, 
                    strategy_development_task, 
                    execution_planning_task, 
                    risk_assessment_task],
            process=ChatOpenAI(model="gpt-3.5-turbo", 
                           temperature=0.7),
            verbose=True
        )