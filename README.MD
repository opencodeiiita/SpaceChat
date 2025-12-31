# SpaceChat

A modular, space-focused chatbot scaffold built with Groq LLMs, LangGraph/LangChain orchestration, and a Streamlit front end. The code is intentionally small and composable so you can study or reuse individual pieces in other projects.

## What this project does
- Captures user prompts from a Streamlit chat UI.
- Routes prompts through a LangGraph execution graph with a planner and tool nodes.
- Fetches space data (e.g., NASA imagery or mission facts) via simple utilities.
- Generates final answers with a Groq-backed LLM agent.
- Returns concise, conversational responses to the browser.

## Tech stack
- Python 3.10+
- Groq `ChatGroq` models
- LangChain + LangGraph for orchestration
- Streamlit for the UI shell
- `requests` for lightweight API calls

## Project structure
- `src/ui/app.py`: Streamlit shell for the chat experience.
- `src/agents/graph.py`: LangGraph scaffold that wires the conversation flow.
- `src/agents/planner.py`: Planner that decides when to call tools vs. the LLM.
- `src/agents/llm_agent.py`: Groq-backed LLM agent interface.
- `src/agents/research_tool.py`: Research helpers (NASA image search, mission lookups).
- `src/utils/space_apis.py`: Space API accessors (extend with more endpoints).
- `src/utils/helpers.py`: Formatting/validation utilities.
- `src/data/`: Placeholder for cached responses or local assets.

## Directory structure
```
SpaceChat/                  # Root of repo
├── README.MD               # Project documentation
├── CONTRIBUTING.MD         # Comprehensive guide for contributing
├── src/
│ ├── agents/               # LangGraph agent nodes & orchestration
│ │ ├── graph.py            # LangGraph engine that coordinates conversation flow
│ │ ├── llm_agent.py        # Groq LLM agent interface for response generation
│ │ ├── planner.py          # Decides which tool to call and when
│ │ └── research_tool.py    # Research helpers
│ ├── ui/
│ │ └── app.py              # Streamlit app entrypoint
│ └── utils/
│   └── helpers.py          # Reusable utility modules
├── participants/           # Contributor submissions (Design folders + intros)
│ ├── 24CS0160/             # Design folders (logo files)
│ ├── IEC2024059/           # Design folders (logo files)
│ ├── ...                   # Individual contributor folders
│ └── *.txt                 # Intro files for Issue #1
└── architecture_diagrams/  # Contributor architecture diagrams
  ├── .gitignore            # Untrack sensitive files
  ├── *.png                 # Architecture diagrams
  ├── *.svg                 # Vector diagrams
  └── *.txt                 # Links to diagrams
```

## Architecture at a glance
The core flow connects the Streamlit UI to the LangGraph execution graph, which routes messages through the planner, research tools, and LLM agent. Utilities support the agents and tools, while future memory hooks sit alongside the graph.
flowchart TD
    User --> UI["Streamlit UI"]
    UI --> Graph["LangGraph Execution Flow"]

    Graph --> Planner["Planner"]
    Planner --> LLM["LLM Agent"]
    Planner --> Research["NASA Research Tool"]

    Research --> Utils["Space APIs & Utils"]
    LLM --> Graph
    Research --> Graph

    Graph --> UI
    Graph --- Memory["State / Memory"]

## How a request flows
1) **Capture**: The UI receives the prompt from the browser chat box.  
2) **Route**: The execution graph hands the prompt to the planner.  
3) **Plan**: The planner decides whether to invoke research tools, the LLM, or both.  
4) **Research**: Tools call space APIs through `space_apis.py` helpers.  
5) **Generate**: The LLM agent drafts a final answer using tool outputs.  
6) **Respond**: The graph returns the response to the UI.  
7) **(Future)** **Memory**: State is persisted to improve follow-up turns.

## Extending and customizing
- **Swap the model**: Point the LLM agent at a different Groq model or provider.
- **Add tools**: Register new nodes in `src/agents/graph.py` and wire them through the planner.
- **Enhance planning**: Implement heuristics or structured outputs in `Planner.plan`.
- **Improve research**: Extend `src/utils/space_apis.py` with more endpoints and error handling.
- **UI tweaks**: Adjust layout, theming, and prompt hints in `src/ui/app.py`.

## Configuration
- `GROQ_API_KEY`: Required for Groq LLM access.
- Optional NASA or other API keys: add corresponding env vars and wiring in `space_apis.py`.

## Development status
- The execution graph, planner, LLM agent, and research tools are scaffolded with placeholders ready to be filled in.
- Memory support is stubbed for future work.
- Tests are not yet added; add lightweight unit tests around planner logic and tool calls as you implement them.

## Contributing
- Keep modules small and composable; maintain clear boundaries between UI, graph, agents, and utilities.
- Prefer adding tool nodes over expanding prompts when external data is needed.
- Document new endpoints, models, or configuration in this README and code docstrings.
