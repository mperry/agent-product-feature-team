from crewai import Agent, Task, Crew, Process
# from crewai.tools import SerperDevTool, ScrapeWebsiteTool


class CrewFeatureDevelopment():

    # search_tool = SerperDevTool()
    # scrape_tool = ScrapeWebsiteTool()

    def product_manager_agent(self) -> Agent:
        return Agent(
        role="Product Manager",
        goal="Translate vague feature requests into clear, actionable product specifications with acceptance criteria.",
        backstory=" You are an experienced product manager who bridges the gap between customer needs" 
                    "and the engineering team. You excel at gathering high-level ideas and shaping them into structured,"
                    "prioritized tasks that align with business objectives. "
                    "You always consider usability, feasibility, and value when writing requirements.",
        verbose=True,
        allow_delegation=True,
        # tools = [self.scrape_tool, self.search_tool]
    )

    def uiux_designer_agent(self) -> Agent:
        return Agent(
            role="UI/UX Designer",
            goal="Design user-friendly interfaces and provide wireframe-style briefs that balance aesthetics, accessibility, and usability.",
            backstory=" You are a creative designer with years of experience making digital products simple and intuitive. "
                    "You take product requirements and transform them into user journeys, wireframes, and style notes that engineers "
                    "can build upon. You think like the end-user and aim to maximize clarity and engagement in your designs.",
            verbose=True,
            allow_delegation=True,
            # tools = [self.scrape_tool, self.search_tool]
        )
    def backend_engineer_agent(self) -> Agent:
        return Agent(
            role="Backend Engineer",
            goal="Define scalable APIs, database schemas, and server-side logic needed to support new product features.",
            backstory="You are a backend engineer who cares deeply about performance, security, and clean architecture."
                    "You design reliable APIs and efficient data models that ensure features can scale and integrate smoothly "
                    "with existing systems. You anticipate potential bottlenecks and provide developers with clear implementation plans.",
               
            verbose=True,
            allow_delegation=True,
            # tools = [self.scrape_tool, self.search_tool]
        )

    def frontend_engineer_agent(self) -> Agent:
        return Agent(
            role="Frontend Engineer",
            goal="Build interactive, responsive, and accessible UI components that connect seamlessly with backend APIs.",
            backstory="You are a frontend engineer passionate about creating smooth user experiences. "
                        "You translate design briefs into working code, ensuring it adheres "
                        "to modern standards (HTML, CSS, JS, or frameworks like React). "
                        "You pay close attention to detail, accessibility, and performance while integrating backend logic into the UI.",
            verbose=True,
            allow_delegation=True,
            # tools = [self.scrape_tool, self.search_tool]
        )

    def product_design_task(self) -> Task:
        return Task(
            description="Take the raw feature request {feature_request} and break it into a structured product specification with goals, "
                        "requirements, and acceptance criteria.",
            expected_output="A JSON specification with fields: feature, goals, requirements, acceptance_criteria.",
            agent=self.product_manager_agent()
        )            

    def uiux_design_task(self) -> Task:
        return Task(
            description="Based on the product spec, propose a wireframe/design brief with layout, elements, and style notes.",
            expected_output="A JSON wireframe spec with fields: layout, elements, style_notes.",
            agent=self.uiux_designer_agent()
        )

    def backend_development_task(self) -> Task:
        return Task(
            description="From the product spec, define API endpoints, database schema, and backend logic needed.",
            expected_output="A JSON spec with fields: api_endpoints, database_schema.",
            agent=self.backend_engineer_agent()
        )

    def frontend_development_task(self) -> Task:
        return Task(
            description="Using the design brief and backend API plan, generate working frontend code (HTML, CSS, JS).",
            expected_output="Code snippets that implement the login page UI connected to backend endpoints.",
            agent=self.frontend_engineer_agent(),
            output_file="frontend_code.html"
        )

    def product_feature_crew(self) -> Crew:
        return Crew(
            agents=[self.product_manager_agent(), 
                    self.uiux_designer_agent(),
                    self.backend_engineer_agent(),
                    self.frontend_engineer_agent()],
            tasks=[self.product_design_task(), 
                    self.uiux_design_task(), 
                    self.backend_development_task(), 
                    self.frontend_development_task()],
            process=Process.sequential,
            verbose=True
        )