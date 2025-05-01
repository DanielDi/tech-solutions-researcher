import requests
from crewai.tools import BaseTool

class GitHubSearchTool(BaseTool):
    name: str = "GitHub Search Tool"
    description: str = (
        "Herramienta para buscar proyectos open source en GitHub utilizando palabras clave. "
        "Devuelve los repositorios más populares y relevantes."
    )

    def _run(self, query: str) -> str:
        url = "https://api.github.com/search/repositories"
        params = {"q": query, "sort": "stars", "order": "desc"}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = []
            for repo in data.get("items", [])[:3]:
                results.append(f"{repo['full_name']}: {repo['description']}")
            return "\n".join(results)
        else:
            return f"Error en la búsqueda: {response.status_code}"