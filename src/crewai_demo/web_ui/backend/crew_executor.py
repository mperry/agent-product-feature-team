"""
Enhanced crew executor with detailed output capture and real-time logging
"""

import asyncio
import time
import json
from typing import Dict, Any, Optional
from datetime import datetime

from crewai import Crew
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_path))

from crewai_demo.crew_product_feature import CrewFeatureDevelopment
from .custom_logger import AgentOutputLogger
from .models import CrewExecutionResult, AgentOutput


class EnhancedCrewExecutor:
    """Enhanced crew executor with detailed output capture"""
    
    def __init__(self, logger: AgentOutputLogger):
        self.logger = logger
        self.crew_instance = None
        self.is_running = False
        
    async def execute_crew(self, feature_request: str) -> CrewExecutionResult:
        """Execute the crew with detailed logging"""
        start_time = time.time()
        self.is_running = True
        
        print("\n" + "="*80)
        print("🚀 CREW EXECUTION STARTED")
        print("="*80)
        print(f"📋 Feature Request: {feature_request[:100]}...")
        print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*80)
        
        try:
            # Initialize crew
            print("🔧 Initializing crew agents...")
            self.crew_instance = CrewFeatureDevelopment()
            crew = self.crew_instance.product_feature_crew()
            print("✅ Crew initialized successfully")
            
            # Prepare inputs
            inputs = {
                'feature_request': feature_request
            }
            
            # Execute crew with custom logging
            result = await self._execute_with_logging(crew, inputs)
            
            execution_time = time.time() - start_time
            
            # Get all outputs
            outputs = self._extract_outputs()
            
            # Get generated files
            generated_files = self._get_generated_files()
            
            print(f"\n{'='*80}")
            print("✅ CREW EXECUTION COMPLETED SUCCESSFULLY")
            print(f"{'='*80}")
            print(f"⏱️  Total Execution Time: {execution_time:.2f} seconds ({execution_time/60:.2f} minutes)")
            print(f"📊 Total Outputs Captured: {len(outputs)}")
            print(f"📁 Generated Files: {len(generated_files)}")
            if generated_files:
                print(f"   Files: {', '.join(generated_files)}")
            print(f"{'='*80}\n")
            
            # Log crew completion with final result (update execution time in the message)
            await self.logger.log_crew_complete(True, execution_time, str(result))
            
            return CrewExecutionResult(
                success=True,
                outputs=outputs,
                execution_time=execution_time,
                generated_files=generated_files,
                final_result=str(result)
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_message = str(e)
            
            print(f"\n{'='*80}")
            print("❌ CREW EXECUTION FAILED")
            print(f"{'='*80}")
            print(f"⏱️  Execution Time Before Failure: {execution_time:.2f} seconds")
            print(f"❌ Error: {error_message}")
            print(f"{'='*80}\n")
            import traceback
            traceback.print_exc()
            
            await self.logger.log_error(error_message)
            await self.logger.log_crew_complete(False, execution_time, error_message)
            
            return CrewExecutionResult(
                success=False,
                outputs=[],
                error_message=error_message,
                execution_time=execution_time
            )
        finally:
            self.is_running = False
            
    async def _execute_with_logging(self, crew: Crew, inputs: Dict[str, Any]):
        """Execute crew with detailed logging for each task"""
        
        # Define task sequence with expected outputs
        task_sequence = [
            {
                "name": "product_design_task",
                "agent": "Product Manager",
                "output_type": "product_spec"
            },
            {
                "name": "uiux_design_task", 
                "agent": "UI/UX Designer",
                "output_type": "wireframe"
            },
            {
                "name": "backend_development_task",
                "agent": "Backend Engineer", 
                "output_type": "backend_api"
            },
            {
                "name": "frontend_development_task",
                "agent": "Frontend Engineer",
                "output_type": "html"
            }
        ]
        
        # Log crew start and send initial progress
        print("\n📊 Starting sequential task execution...")
        print("   Task sequence: Product Manager → UI/UX Designer → Backend Engineer → Frontend Engineer")
        await self.logger.log_agent_start("Crew", "product_feature_crew")
        await self.logger.log_agent_thinking("Crew", "Starting sequential task execution...")
        await asyncio.sleep(0.1)  # Brief pause to ensure message is sent
        
        # Send initial progress update (0%)
        await self.logger.log_task_complete("crew_start", "Crew", 0)
        
        # Send progress updates during execution
        async def send_progress_updates():
            """Send periodic progress updates during execution"""
            # Simulate progress updates as tasks are being worked on
            progress_steps = [5, 12, 25, 35, 50, 60, 75, 85, 95]
            for progress in progress_steps:
                await asyncio.sleep(10)  # Wait 10 seconds between updates
                if self.is_running:  # Only send if still running
                    await self.logger.log_agent_thinking("Crew", f"Execution in progress... ({progress}% estimated)")
                    await self.logger.log_task_complete("crew_progress", "Crew", progress)
        
        # Execute crew in a thread to avoid blocking
        import concurrent.futures
        
        def run_crew():
            print(f"\n{'='*80}")
            print("🔥 CREWAI EXECUTION STARTING (this may take several minutes)")
            print(f"{'='*80}\n")
            try:
                # CrewAI will print verbose output here since verbose=True
                result = crew.kickoff(inputs=inputs)
                print(f"\n{'='*80}")
                print("✅ CREWAI EXECUTION COMPLETED")
                print(f"{'='*80}\n")
                return result
            except Exception as e:
                print(f"\n{'='*80}")
                print(f"❌ CREWAI EXECUTION FAILED: {e}")
                print(f"{'='*80}")
                import traceback
                traceback.print_exc()
                raise
        
        # Start progress update task (don't await, let it run in background)
        progress_task = asyncio.create_task(send_progress_updates())
        
        # Start crew execution in thread pool
        loop = asyncio.get_event_loop()
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = await loop.run_in_executor(executor, run_crew)
            # Cancel progress updates since execution is done
            progress_task.cancel()
        except Exception as e:
            progress_task.cancel()
            print(f"DEBUG: Exception during crew execution: {e}")
            await self.logger.log_error(f"Crew execution failed: {str(e)}")
            raise
        
        # Parse the actual crew result to extract task outputs
        print(f"\n📦 Parsing crew execution results...")
        print(f"   Result type: {type(result).__name__}")
        
        # Debug: Inspect result structure
        print(f"   Result attributes: {dir(result)}")
        if hasattr(result, 'tasks_output'):
            print(f"   ✅ Has tasks_output: {len(result.tasks_output) if result.tasks_output else 0} tasks")
            for i, task_out in enumerate(result.tasks_output):
                print(f"      Task {i}: {type(task_out).__name__}, has 'output': {hasattr(task_out, 'output')}")
        if hasattr(result, 'raw'):
            print(f"   ✅ Has raw: {type(result.raw).__name__}")
        if hasattr(result, 'tasks'):
            print(f"   ✅ Has tasks: {len(result.tasks) if result.tasks else 0} tasks")
        
        result_preview = str(result)[:300] if result else "No result"
        print(f"   Result preview: {result_preview}...")
        
        # Extract individual task outputs from the result
        task_outputs = {}
        
        # Method 1: Try tasks_output attribute (CrewAI standard)
        if hasattr(result, 'tasks_output') and result.tasks_output:
            print(f"   📋 Extracting from tasks_output ({len(result.tasks_output)} tasks)...")
            for i, task_output in enumerate(result.tasks_output):
                if i < len(task_sequence):
                    task_info = task_sequence[i]
                    # Try different ways to get the output
                    output_text = None
                    if hasattr(task_output, 'output'):
                        output_text = str(task_output.output)
                    elif hasattr(task_output, 'raw'):
                        output_text = str(task_output.raw)
                    elif isinstance(task_output, str):
                        output_text = task_output
                    else:
                        output_text = str(task_output)
                    
                    if output_text and len(output_text.strip()) > 0:
                        task_outputs[task_info["name"]] = output_text
                        print(f"      ✓ Extracted output for {task_info['agent']}: {len(output_text)} chars")
                    else:
                        print(f"      ⚠ Empty output for {task_info['agent']}")
        
        # Method 2: Try raw attribute
        elif hasattr(result, 'raw'):
            print(f"   📋 Extracting from raw attribute...")
            try:
                import json
                raw_data = result.raw
                if isinstance(raw_data, dict):
                    # Try to match keys to task names
                    for key, value in raw_data.items():
                        for task_info in task_sequence:
                            if (task_info["name"] in key.lower() or 
                                task_info["agent"].lower() in key.lower() or
                                task_info["output_type"] in key.lower()):
                                task_outputs[task_info["name"]] = str(value)
                                print(f"      ✓ Matched '{key}' to {task_info['agent']}")
                                break
                elif isinstance(raw_data, str) and len(raw_data) > 0:
                    # If raw is a string, might be the final output
                    task_outputs[task_sequence[-1]["name"]] = raw_data
                    print(f"      ✓ Using raw string as final output")
            except Exception as e:
                print(f"      ❌ Error parsing raw: {e}")
        
        # Method 3: Try direct string conversion
        if not task_outputs:
            result_str = str(result)
            if result_str and len(result_str.strip()) > 50:  # Only if substantial content
                print(f"   📋 Using string representation as fallback...")
                # Split by common delimiters or use as final output
                task_outputs[task_sequence[-1]["name"]] = result_str
                print(f"      ✓ Using full result for final task ({len(result_str)} chars)")
        
        # Report what we extracted
        print(f"\n   📊 Extraction Summary:")
        for task_info in task_sequence:
            if task_info["name"] in task_outputs:
                output_len = len(task_outputs[task_info["name"]])
                print(f"      ✅ {task_info['agent']}: {output_len} chars")
            else:
                print(f"      ❌ {task_info['agent']}: NO OUTPUT EXTRACTED")
        
        # Log task progression with actual or placeholder outputs
        # Send updates with realistic delays to show incremental progress
        print(f"\n📋 Processing task outputs and sending updates to UI...")
        for i, task_info in enumerate(task_sequence):
            # Calculate progress: 25%, 50%, 75%, 100%
            base_progress = i * 25
            progress = base_progress + 25
            
            print(f"\n   [{i+1}/4] {task_info['agent']} - {task_info['name']}")
            
            # Send task start (with base progress)
            await self.logger.log_agent_start(
                task_info["agent"], 
                task_info["name"]
            )
            
            # Send initial progress for this task starting
            await self.logger.log_task_complete(
                task_info["name"] + "_start",
                task_info["agent"],
                base_progress
            )
            
            await asyncio.sleep(0.5)  # Small delay to show task starting
            
            # Send thinking status
            await self.logger.log_agent_thinking(
                task_info["agent"],
                f"Working on {task_info['output_type']} generation..."
            )
            
            # Send intermediate progress (task in progress)
            intermediate_progress = base_progress + 10
            await self.logger.log_task_complete(
                task_info["name"] + "_progress",
                task_info["agent"],
                intermediate_progress
            )
            
            await asyncio.sleep(1.0)  # Delay to show intermediate progress
            
            # Get the actual output for this task
            task_output = task_outputs.get(task_info["name"])
            
            if task_output and len(task_output.strip()) > 0:
                # Show output preview in terminal
                output_preview = task_output[:150] + "..." if len(task_output) > 150 else task_output
                print(f"      Output: {output_preview}")
                print(f"      Progress: {progress}%")
                
                # Log completion with actual output
                await self.logger.log_agent_output(
                    task_info["agent"],
                    task_info["name"], 
                    task_output,
                    task_info["output_type"]
                )
            else:
                # No output extracted - this might indicate the task didn't complete or output wasn't captured
                warning_msg = f"⚠️  WARNING: No output extracted for {task_info['agent']}. Task may have failed or output structure is unexpected."
                print(f"      {warning_msg}")
                
                # Try to get output from the full result string as a fallback
                result_str = str(result)
                if task_info["output_type"] in result_str.lower() or task_info["agent"].lower() in result_str.lower():
                    # Extract a portion of the result that might contain this task's output
                    task_output = f"[Output not individually captured - may be in full result]\n\nFull crew result:\n{result_str[:500]}..."
                else:
                    task_output = f"⚠️ Output not captured for {task_info['agent']}. The task may have completed but the output format is not recognized. Check CrewAI execution logs above for details."
                
                await self.logger.log_agent_output(
                    task_info["agent"],
                    task_info["name"], 
                    task_output,
                    task_info["output_type"]
                )
            
            # Send final completion for this task
            await self.logger.log_task_complete(
                task_info["name"],
                task_info["agent"],
                progress
            )
            
            # Longer delay between tasks to show progression
            await asyncio.sleep(1.5)
        
        # Note: Final completion message will be sent in execute_crew with correct execution time
        print("DEBUG: Crew execution finished, parsing results...")
            
        return result
        
    def _extract_task_output(self, result: Any, task_name: str) -> str:
        """Extract output from crew result for a specific task"""
        # This is a simplified extraction. In practice, you might need
        # to modify the crew execution to capture individual task outputs
        
        if hasattr(result, 'tasks_output'):
            # Try to get task output
            for task in result.tasks_output:
                if hasattr(task, 'output'):
                    return str(task.output)
                    
        # Fallback to a generic message
        return f"Output generated for {task_name}"
        
    def _extract_outputs(self) -> list[AgentOutput]:
        """Extract all agent outputs from the logger"""
        outputs = []
        
        for task_name, task_outputs in self.logger.get_all_outputs().items():
            for agent_name, output_data in task_outputs.items():
                outputs.append(AgentOutput(
                    agent_name=agent_name,
                    task_name=task_name,
                    output=output_data["output"],
                    timestamp=output_data["timestamp"],
                    output_type=output_data["output_type"]
                ))
                
        return outputs
        
    def _get_generated_files(self) -> list[str]:
        """Get list of generated files"""
        files = []
        
        # Check for common output files
        import os
        if os.path.exists("frontend_code.html"):
            # Clean the frontend code file to remove any dots at beginning/end
            self._clean_frontend_output_file("frontend_code.html")
            files.append("frontend_code.html")
            
        return files
        
    def _clean_frontend_output_file(self, file_path: str):
        """Clean the frontend output file to remove dots at beginning and end"""
        try:
            import os
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove dots/periods from the beginning and end
                content = content.strip()
                while content.startswith('.'):
                    content = content[1:].strip()
                while content.endswith('.'):
                    content = content[:-1].strip()
                
                # Ensure it starts with DOCTYPE and ends with </html>
                if not content.startswith('<!DOCTYPE html>'):
                    # Find the first occurrence of DOCTYPE
                    doctype_pos = content.find('<!DOCTYPE html>')
                    if doctype_pos != -1:
                        content = content[doctype_pos:]
                
                if not content.endswith('</html>'):
                    # Find the last occurrence of </html>
                    html_end_pos = content.rfind('</html>')
                    if html_end_pos != -1:
                        content = content[:html_end_pos + 7]
                
                # Write the cleaned content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"DEBUG: Cleaned frontend output file: {file_path}")
                
        except Exception as e:
            print(f"Warning: Could not clean frontend output file {file_path}: {e}")
        
    def stop_execution(self):
        """Stop the crew execution"""
        self.is_running = False
        # Note: CrewAI doesn't have a built-in stop mechanism
        # This would need to be implemented based on your specific needs
        
    def get_status(self) -> Dict[str, Any]:
        """Get current execution status"""
        return {
            "is_running": self.is_running,
            "current_agent": self.logger.current_agent,
            "current_task": self.logger.current_task,
            "outputs_count": len(self.logger.get_all_outputs())
        }
