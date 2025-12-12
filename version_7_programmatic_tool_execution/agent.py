# ------------------------------------------------------------------------------
# FILE: agent.py
# ------------------------------------------------------------------------------
# PURPOSE:
# Defines the AgentWrapper class that loads and constructs a Google ADK LLM Agent.
#
# NEW CAPABILITIES:
# - Includes a 'run_python_code' tool.
# - Dynamically fetches tools from MCP toolsets at runtime, wraps them as 
#   native Python async functions, and injects them into the script scope.
# - Enforces return values from the Python script back to the LLM.
# ------------------------------------------------------------------------------
# Sample query:  Can you write a python code that uses your MCP tools and run it 
# to first add two numbers 5 and 7, then multiply the sum by 2 then subtract 4 
# from the product and then divide the difference by 5

import asyncio
import textwrap
import traceback
from typing import Any, List, Dict, Callable, Optional, Union

from rich import print  # Used for colorful terminal logging

# ADK's built-in LLM agent class
from google.adk.agents.llm_agent import LlmAgent
# Tool wrapper to convert python func to ADK tool
from google.adk.tools import FunctionTool
# Type hint for ADK tools
from google.adk.tools import BaseTool

# Provides access to tools hosted on MCP servers
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset

# Connection settings for different types of MCP servers
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool import StdioConnectionParams

# Custom parameters for local STDIO-based MCP servers
from mcp import StdioServerParameters

# Utility function to read the config.json file
from utilities import read_config_json


# ------------------------------------------------------------------------------
# CLASS: AgentWrapper
# ------------------------------------------------------------------------------
class AgentWrapper:
    def __init__(self, tool_filter: Optional[List[str]] = None) -> None:
        """
        Initializes the wrapper but does NOT build the agent yet.
        Call `await self.build()` after this to complete setup.

        Args:
            tool_filter (Optional[List[str]]): Optional list of tool names to allow.
        """
        self.tool_filter: Optional[List[str]] = tool_filter
        self.agent: Optional[LlmAgent] = None          # Will hold the final LlmAgent after building
        self._toolsets: List[MCPToolset] = []          # Store all loaded toolsets for later cleanup


    async def build(self) -> None:
        """
        Builds the LlmAgent by:
        - Connecting to all MCP servers.
        - Defining the 'run_python_code' tool.
        - Initializing the ADK agent with strict instructions on using the Python tool.
        """
        # Load toolsets (connections are established here)
        self._toolsets = await self._load_toolsets()

        # --- Define the Python Execution Function Locally ---
        
        async def run_python_code(code: str) -> str:
            """
            Executes the provided Python code string asynchronously.
            
            IMPORTANT GUIDELINES:
            1. You have access to connected MCP tools as local async functions (e.g., `await read_file(path='...')`).
            2. Do NOT use standard Python APIs (like `open()`) if an MCP tool (like `read_file`) is available.
            3. Your code MUST end with a `return` statement. 
            4. The return value should be a descriptive string explaining what was done and the result.
            
            Args:
                code (str): Valid python code. Must include a 'return' statement at the end.
                
            Returns:
                str: The result of the execution or error message.
            """
            print(f"[bold blue]🐍 Executing Python Code:[/bold blue]\n{code}")
            
            # 1. Prepare the execution scope
            scope: Dict[str, Any] = {}

            # 2. Dynamic Tool Retrieval
            current_tools: List[BaseTool] = []
            
            for toolset in self._toolsets:
                try:
                    # fetch tools from the session
                    ts_tools: List[BaseTool] = await toolset.get_tools()
                    current_tools.extend(ts_tools)
                except Exception as e:
                    print(f"[yellow]⚠️ Warning: Could not fetch tools from a toolset during python exec:[/yellow] {e}")

            # 3. Helper to create a native python async function that calls the MCP tool
            def create_wrapper(tool_instance: BaseTool) -> Callable[..., Any]:
                async def wrapped_mcp_call(**kwargs: Any) -> Any:
                    # Log the call internally
                    print(f"[dim]  -> Calling tool: {tool_instance.name} with args: {kwargs}[/dim]")
                    # Execute the MCP tool
                    return await tool_instance.run_async(args=kwargs, tool_context=None)
                return wrapped_mcp_call

            # 4. Inject tools into scope
            for tool in current_tools:
                # Sanitize tool name for python variable (replace - with _)
                safe_name: str = tool.name.replace("-", "_")
                scope[safe_name] = create_wrapper(tool)

            # 5. Wrap the user's code in an async function to allow 'await'
            indented_code: str = textwrap.indent(code, "    ")
            wrapper_code: str = f"async def _main():\n{indented_code}"

            try:
                # Execute the definition of _main in the scope
                exec(wrapper_code, scope)
                
                # Retrieve and await the _main function
                if "_main" in scope:
                    result: Any = await scope["_main"]()
                    
                    # Handle cases where the agent forgot to return anything
                    if result is None:
                        return (
                            "Execution successful, but the Python script returned 'None'. "
                            "Did you forget to add a `return` statement at the end of your code? "
                            "Please rewrite the code to return a descriptive string."
                        )
                    return str(result)
                else:
                    return "Error: Could not define main execution block."

            except Exception:
                # Return the traceback so the Agent knows what went wrong and can retry
                err: str = traceback.format_exc()
                print(f"[red]❌ Python Execution Failed:[/red]\n{err}")
                return f"Python Execution Error:\n{err}"

        # --- Create the Tool ---
        python_tool: FunctionTool = FunctionTool(run_python_code)

        # Construct the ADK LLM Agent
        combined_tools: List[Union[MCPToolset, FunctionTool]] = self._toolsets + [python_tool] # type: ignore

        self.agent = LlmAgent(
            model="gemini-flash-latest",
            name="enterprise_assistant",
            instruction=(
                "Assist the user with filesystem and MCP server tasks. "
                "You have a powerful tool called 'run_python_code'. "
                "Use it when you need to chain multiple tools, perform logic/math, or process data. "
                "\n\n"
                "RULES FOR PYTHON CODE:\n"
                "1. All connected MCP tools are available as local async functions (e.g., `await read_file(path='...')`). "
                "   Use these instead of standard Python libraries where possible.\n"
                "2. Your generated Python script MUST end with a `return` statement.\n"
                "3. The returned string should summarize the action taken and the result obtained." \
                "4. Dont use default api or anything, just call tool like add_numbers with the required params"
            ),
            tools=combined_tools
        )


    async def _load_toolsets(self) -> List[MCPToolset]:
        """
        Reads config, connects to servers, and returns the list of Toolsets.

        Returns:
            List[MCPToolset]: A list of initialized MCP toolsets.
        """
        config: Dict[str, Any] = read_config_json()
        toolsets: List[MCPToolset] = []

        server_config: Dict[str, Any]
        for name, server_config in config.get("mcpServers", {}).items():
            try:
                conn: Union[StreamableHTTPServerParams, StdioConnectionParams]

                # Determine connection method
                if server_config.get("type") == "http":
                    conn = StreamableHTTPServerParams(url=server_config["url"])

                elif server_config.get("type") == "stdio":
                    conn = StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command=server_config["command"],
                            args=server_config["args"]
                        ),
                        timeout=5
                    )
                else:
                    raise ValueError(f"[red]❌ Unknown server type: '{server_config.get('type')}'[/red]")

                # Connect
                toolset = MCPToolset(
                    connection_params=conn,
                    tool_filter=self.tool_filter
                )

                # Fetch tools (activates the session and validates connection)
                tools: List[Any] = await toolset.get_tools()
                
                # Logging
                tool_names: List[str] = [tool.name for tool in tools]
                print(f"[bold green]✅ Tools loaded from [cyan]'{name}'[/cyan]:[/bold green] {tool_names}")

                toolsets.append(toolset)

            except Exception as e:
                print(f"[bold red]⚠️  Skipping server '{name}':[/bold red] {e}")

        return toolsets


    async def close(self) -> None:
        """
        Gracefully shuts down each loaded toolset.
        """
        for toolset in self._toolsets:
            try:
                await toolset.close()
            except Exception as e:
                print(f"[yellow]⚠️ Error closing toolset:[/yellow] {e}")

        await asyncio.sleep(1.0)