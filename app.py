# app.py

#%% Imports y configuración inicial
from typing import List
import os
from pathlib import Path

# CrewAI y sus herramientas
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
from tools.calculator_tool import CalculatorTool
from tools.github_search_tool import GitHubSearchTool

# FastAPI para exponer la API
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Carga variables de entorno desde un archivo .env (si existe)
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

#%% Configuración de la clave de OpenAI pública (cuenta personal)
# Asegúrate de tener en tu .env: OPENAI_API_KEY=sk-...
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("❌ No se encontró la variable OPENAI_API_KEY")

# Para que embedchain y CrewAI lo detecten:
os.environ["OPENAI_API_KEY"] = openai_key

# Instancia el LLM usando tu cuenta de OpenAI.com
# No se especifica api_base, ni api_version, ni deployment (solo openai.api_key)
llm = LLM(
    model="gpt-4o-mini",    # O el modelo que prefieras: "gpt-3.5-turbo", etc.
    api_key=openai_key
)

#%% Definición del Crew con agentes y tareas
@CrewBase
class TechSolutionsCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def solution_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['solution_researcher'],
            verbose=True,
            llm=llm,
            tools=[
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
            ]
        )
    
    @agent
    def opensource_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['opensource_expert'],
            verbose=True,
            llm=llm,
            tools=[
                GitHubSearchTool(),
                CalculatorTool()
            ]
        )
    
    @agent
    def enterprise_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['enterprise_advisor'],
            verbose=True,
            llm=llm,
            tools=[
                WebsiteSearchTool(),
                ScrapeWebsiteTool(),
                CalculatorTool()
            ]
        )
    
    @task
    def solution_search(self) -> Task:
        return Task(
            config=self.tasks_config['solution_search'],
            agent=self.solution_researcher(),
        )
    
    @task
    def opensource_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['opensource_analysis'],
            agent=self.opensource_expert(),
        )
    
    @task
    def enterprise_recommendation(self) -> Task:
        return Task(
            config=self.tasks_config['enterprise_recommendation'],
            agent=self.enterprise_advisor(),
        )
    
    @crew
    def crew(self) -> Crew:
        """Construye el Crew y programa las tareas en secuencia."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

#%% Punto de entrada para ejecución directa
def run():
    inputs = {
        'query': 'What is the target_solution you would like to replace?',
        'target_solution': 'IBM ESB',
    }
    return TechSolutionsCrew().crew().kickoff(inputs=inputs)

#%% Configuración de FastAPI
app = FastAPI(
    title="Tech Solutions Crew",
    description="API para lanzar tus tasks de CrewAI",
)

# Permitir peticiones CORS desde localhost:3000 (tu frontend)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para la petición /run
class RunRequest(BaseModel):
    query: str
    target_solution: str

@app.post("/run")
async def run_crew(body: RunRequest):
    """
    Endpoint POST /run
    Recibe JSON con 'query' y 'target_solution', ejecuta el Crew y devuelve el reporte.
    """
    result = TechSolutionsCrew().crew().kickoff(inputs=body.dict())
    return {"report": result}

#%% Para ejecución como script
if __name__ == "__main__":
    print("## Tech Solutions Crew - Ejecución directa")
    report = run()
    print("\n=== Report ===\n")
    print(report)
    # Alternativamente, lanzar uvicorn:
    # uvicorn.run(app, host="0.0.0.0", port=8000)
