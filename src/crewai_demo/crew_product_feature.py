from crewai import Agent, Task, Crew, Process


class CrewFeatureDevelopment():


    def product_manager_agent(self) -> Agent:
        return Agent(
        role="Product Manager",
        goal="Translate vague feature requests into clear, actionable product specifications with acceptance criteria.",
        backstory=" You are an experienced product manager who bridges the gap between customer needs" 
                    "and the engineering team. You excel at gathering high-level ideas and shaping them into structured,"
                    "prioritized tasks that align with business objectives. "
                    "You always consider usability, feasibility, and value when writing requirements.",
        verbose=True,
        max_iter=2,  
    )

    def uiux_designer_agent(self) -> Agent:
        return Agent(
            role="UI/UX Designer",
            goal="Design user-friendly interfaces and provide wireframe-style briefs that balance aesthetics, accessibility, and usability.",
            backstory=" You are a creative designer with years of experience making digital products simple and intuitive. "
                    "You take product requirements and transform them into user journeys, wireframes, and style notes that engineers "
                    "can build upon. You think like the end-user and aim to maximize clarity and engagement in your designs.",
            verbose=True,
            max_iter=2,  
        )
    def backend_engineer_agent(self) -> Agent:
        return Agent(
            role="Backend Engineer",
            goal="Define scalable APIs, database schemas, and server-side logic needed to support new product features.",
            backstory="You are a backend engineer who cares deeply about performance, security, and clean architecture."
                    "You design reliable APIs and efficient data models that ensure features can scale and integrate smoothly "
                    "with existing systems. You anticipate potential bottlenecks and provide developers with clear implementation plans.",
            verbose=True,
            max_iter=2,  
        )

    def frontend_engineer_agent(self) -> Agent:
        return Agent(
            role="HTML Code Generator",
            goal="Output ONLY valid HTML code with complete CSS styling. Never explain, never use markdown, never add comments or explanations. Never add dots or periods at the beginning or end of the output.",
            backstory="You are a strict HTML code generator with expertise in CSS styling. Your ONLY job is to output valid HTML code with complete CSS. "
                        "You NEVER write explanations, comments, or use markdown formatting. "
                        "You NEVER add dots, periods, or any punctuation at the beginning or end of your output. "
                        "You ALWAYS start with <!DOCTYPE html> and end with </html>. "
                        "You ALWAYS embed CSS in <style> tags and JavaScript in <script> tags. "
                        "You ALWAYS include CSS reset and style ALL HTML elements used in the page. "
                        "You ALWAYS create modern, responsive designs with proper styling for every element. "
                        "Your output is ALWAYS a complete, working HTML file with no extra characters.",
            verbose=True,
            max_iter=1,  
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
            description="Based on the product spec from the previous task, propose a wireframe/design brief with layout, elements, and style notes.",
            expected_output="A JSON wireframe spec with fields: layout, elements, style_notes.",
            agent=self.uiux_designer_agent(),
            context=[self.product_design_task()]
        )

    def backend_development_task(self) -> Task:
        return Task(
            description="Based on the product spec from the first task, define API endpoints, database schema, and backend logic needed.",
            expected_output="A JSON backend API spec with fields: api_endpoints, database_schema.",
            agent=self.backend_engineer_agent(),
            context=[self.product_design_task()]
        )

    def frontend_development_task(self) -> Task:
        return Task(
            description="""CRITICAL: You MUST generate ONLY a complete HTML file with embedded CSS and JavaScript.
                            Based on the product spec and UI/UX design from previous tasks, create a functional login page.
                            Requirements:
                            1. Start with <!DOCTYPE html> and end with </html>
                            2. Include all CSS in <style> tags within <head>
                            3. Include all JavaScript in <script> tags before </body>
                            4. Create a functional login page with username/password fields
                            5. Connect to backend API endpoints from the backend task
                            6. NO explanatory text, NO markdown, NO code blocks
                            7. NO dots, periods, or punctuation at the beginning or end
                            8. ONLY the raw HTML code
                            
                            CSS Requirements:
                            - Include CSS reset (* { margin: 0; padding: 0; box-sizing: border-box; })
                            - Style ALL HTML elements used (header, nav, ul, li, a, main, section, form, input, label, etc.)
                            - Use modern CSS with proper selectors
                            - Include hover effects and transitions
                            - Make the design responsive and visually appealing
                            - Use proper color scheme and typography

                            Example structure:
                            <!DOCTYPE html>
                            <html>
                            <head>
                            <style>
                            * { margin: 0; padding: 0; box-sizing: border-box; }
                            body { font-family: system fonts; }
                            /* Complete CSS for all elements */
                            </style>
                            </head>
                            <body>
                            <!-- HTML content here -->
                            <script>
                            // JavaScript here
                            </script>
                            </body>
                            </html>""",
            expected_output="A complete, valid HTML file that starts with <!DOCTYPE html> and contains all CSS and JavaScript inline. The CSS must style ALL HTML elements used in the page. No markdown formatting, no explanatory text, no dots or periods at the beginning or end, just pure HTML code.",
            agent=self.frontend_engineer_agent(),
            context=[self.product_design_task(), self.uiux_design_task(), self.backend_development_task()],
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