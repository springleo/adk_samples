# Intelligent Research-Driven Website Builder Agent (v3)

This project demonstrates an advanced multi-agent system using the Agent Development Kit (ADK). It uses a team of six specialized agents that combine intelligent research capabilities with parallel processing and sequential workflow to build complete HTML+CSS+JS web pages from a single topic input. This version significantly enhances the previous approach by incorporating comprehensive topic research through question generation, parallel research execution, and intelligent query synthesis before proceeding with requirements writing, design, and development.

The system transforms a simple topic (e.g., "artificial intelligence", "renewable energy") into a fully researched, comprehensive webpage through an intelligent 6-stage pipeline.

The generated web page is saved to a timestamped `.html` file in the `output/` directory.

---

## 📦 Features

- ✅ **Intelligent Research Pipeline:** A sophisticated 6-agent workflow that researches topics before building:
    1.  `questions_generator`: Generates 5 important questions about the topic using Google search
    2.  `questions_researcher`: 5 parallel agents research each question simultaneously 
    3.  `query_generator`: Synthesizes all research into a comprehensive web development query
    4.  `requirements_writer`: Converts the research-backed query into detailed requirements
    5.  `designer`: Creates visual design specifications from requirements
    6.  `code_writer`: Generates the final HTML/CSS/JS code
- ✅ **Parallel Processing:** Question research happens concurrently for maximum efficiency
- ✅ **Google Search Integration:** All research agents use Google search for current, accurate information
- ✅ **Research-Driven Development:** Every webpage is built on comprehensive topic research
- ✅ Gemini 2.0/2.5 Flash powered LLM agents using Google ADK
- ✅ Takes a simple topic input (e.g., "machine learning", "sustainable architecture")
- ✅ Generates research-backed, comprehensive HTML pages with inline CSS/JS
- ✅ Saves the final output as a timestamped `.html` file
- ✅ Highly modular and easily extendable architecture

---

## 📂 Project Structure

```text
version_3_parallel_research_agent/
├── agents/
│   ├── root_website_builder/      # Orchestrator: Manages the 6-agent sequence
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── questions_generator/       # Agent 1: Generates 5 research questions about the topic
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── questions_researcher/      # Agent 2: 5 parallel agents research each question
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── query_generator/           # Agent 3: Synthesizes research into web development query
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── requirements_writer/       # Agent 4: Converts query into detailed requirements
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   ├── designer/                  # Agent 5: Creates visual design specifications
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── instructions.txt
│   │   └── description.txt
│   └── code_writer/               # Agent 6: Generates final HTML/CSS/JS code
│       ├── __init__.py
│       ├── agent.py
│       ├── instructions.txt
│       └── description.txt
├── tools/
│   └── file_writer_tool.py        # Tool for saving the final webpage to disk
├── utils/
│   └── file_loader.py             # Utility for reading instruction files
├── output/                        # Auto-generated folder with timestamped HTML outputs
│   └── 250801_113507_generated_page.html # Example output file
├── agent_runner.py                # Python script for programmatic agent execution
├── main.py                        # Entry point for the ADK application
├── pyproject.toml                 # Project dependencies and configuration
├── uv.lock                        # Dependency lock file
└── README.md                      # This documentation file
```

---

## 🚀 Quickstart

### 1. Clone the Repo

```bash
git clone https://github.com/theailanguage/adk_samples.git
```

### 2. Set Up Python Environment
**Required:** Python 3.11+, uv, VS Code, and Git.

```bash
cd adk_samples/intelligent_research_website_builder
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate.bat on Windows
uv sync --all-groups
```

### 3. Add Your API Key

Create a `.env` file in the `intelligent_research_website_builder` project root:

```env
GOOGLE_API_KEY=your-google-api-key
GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

You can get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

---

### 4. Run the Agent UI

```bash
cd adk_samples/intelligent_research_website_builder
adk web ./agents
```

Then open `http://localhost:8000` in your browser. From the agent dropdown list, select **`root_website_builder`**. This is the main entry point that will run the entire 6-agent research and development pipeline.

---

### **Four Ways to Run Your ADK Agent**

| S.No. | Method & Command | Description | When to Use |
|------:|------------------|-------------|-------------|
| 1 | **ADK Web**  <br>`adk web ./agents` | - Launches a browser-based UI | - Ideal for debugging or quick demos |
| 2 | **ADK API Server** <br>`adk api_server ./agents` | - Starts an HTTP API server | - Useful for REST API-based automation. |
| 3 | **Programmatic Python Script** <br>`uv run python3 -m agent_runner` | - Fully code-driven interaction using Python and the ADK SDK | - Ideal for building your own CLI tools or backend pipelines |
| 4 | **ADK CLI Run** <br>`adk run agents/root_website_builder` | - Command-line way to run a specific agent directly | - Great for quick runs or testing |

---

## 💬 Example Topics

Provide a simple topic to the `root_website_builder` agent. The system will research the topic comprehensively and build an informative webpage:

**Technology Topics:**
```
artificial intelligence
blockchain technology
quantum computing
```

**Science Topics:**
```
renewable energy
climate change solutions
space exploration
```

**Business Topics:**
```
sustainable agriculture
digital marketing trends
remote work productivity
```

The agent system will research your topic thoroughly, generate relevant questions, find current information, and create a comprehensive webpage in the `output/` folder.

---

## 🧠 How It Works

This project demonstrates an intelligent research-driven workflow using six specialized agents orchestrated by a root agent. The system transforms a simple topic into a comprehensive, research-backed webpage through the following pipeline:

### Phase 1: Research & Intelligence Gathering
1. **Topic Input**: You provide a simple topic (e.g., "machine learning") to the **`root_website_builder`** agent
2. **Question Generation**: The **`questions_generator`** agent researches the topic using Google search and generates 5 important questions that help understand the topic comprehensively
3. **Parallel Research**: The **`questions_researcher`** agent runs 5 specialized sub-agents in parallel, each researching one specific question using Google search to gather current, authoritative information

### Phase 2: Synthesis & Planning  
4. **Query Synthesis**: The **`query_generator`** agent analyzes all research outputs and synthesizes them into a single, comprehensive web development query that incorporates all research insights
5. **Requirements Writing**: The **`requirements_writer`** agent converts the research-backed query into detailed, structured webpage requirements

### Phase 3: Design & Development
6. **Design Specification**: The **`designer`** agent creates comprehensive visual design specifications with exact colors, typography, and layout details
7. **Code Generation**: The **`code_writer`** agent implements the design specifications into clean HTML, CSS, and JavaScript code
8. **File Output**: The final webpage is saved as a timestamped `.html` file in the `output/` directory

### Key Advantages:
- **Research-Driven**: Every webpage is built on comprehensive, current research
- **Parallel Efficiency**: Question research happens simultaneously, reducing total execution time
- **Comprehensive Coverage**: 5 different research angles ensure thorough topic understanding
- **Current Information**: Google search integration provides up-to-date, accurate content

---

## 🛠️ Extending the Project

The modular, research-driven design makes this project highly extensible:

### Research Extensions:
-   **Add More Research Agents:** Increase from 5 to 10 parallel researchers for even more comprehensive coverage
-   **Specialized Research Tools:** Add domain-specific research tools (academic papers, industry reports, social media trends)
-   **Multi-Language Research:** Extend research capabilities to non-English sources

### Pipeline Extensions:
-   **Add a QA Agent:** Insert a `qa_testing_agent` after the `code_writer` to validate generated HTML
-   **Add SEO Optimization:** Include an `seo_optimizer_agent` to enhance search engine optimization
-   **Add Accessibility Checker:** Insert an `accessibility_agent` to ensure WCAG compliance

### Output Extensions:
-   **Multi-Format Output:** Replace `code_writer` with specialized agents for React, Vue, or other frameworks
-   **CMS Integration:** Add agents that can publish directly to WordPress, Webflow, or other platforms
-   **Multi-Page Sites:** Extend to generate complete multi-page websites instead of single pages

### Intelligence Extensions:
-   **User Feedback Loop:** Add agents that can incorporate user feedback to refine outputs
-   **A/B Testing:** Generate multiple variations for testing different approaches
-   **Analytics Integration:** Add tracking and performance monitoring capabilities

---

## 📜 License

This repository is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for full details.

---

Happy building with ADK! 🛠