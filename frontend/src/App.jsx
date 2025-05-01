import React, { useState } from 'react'

export default function App() {
  const [query, setQuery] = useState('')
  const [target, setTarget] = useState('')
  const [reportTitle, setReportTitle] = useState('')
  const [reportBody, setReportBody] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setReportTitle('')
    setReportBody('')

    try {
      const res = await fetch('http://localhost:8080/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, target_solution: target })
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const data = await res.json()

      const raw = data.report?.raw
      if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
        // Extrae clave y valor cuando raw es un objeto con título dinámico
        const [key] = Object.keys(raw)
        setReportTitle(key)
        setReportBody(raw[key])
      } else {
        setReportTitle('Recomendación Final')
        setReportBody(typeof raw === 'string' ? raw : '')
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center p-4 min-h-screen">
      <div className="w-full max-w-2xl bg-white bg-opacity-90 backdrop-blur-md p-8 rounded-3xl shadow-lg">
        <h1 className="text-4xl font-extrabold text-primary text-center mb-2">
          Digital Adoption Agents
        </h1>
        <p className="text-center text-gray-700 mb-6">
          Un conjunto de agentes inteligentes que te guían en tu proceso de adopción digital.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-lg font-medium text-gray-800 mb-2">
              Describe tu desafío digital (Query)
            </label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              rows={3}
              className="w-full border border-gray-300 rounded-lg p-3 focus:border-primary focus:ring focus:ring-primary/50"
              placeholder="¿En qué parte de tu ecosistema digital necesitas ayuda?"
              required
            />
          </div>

          <div>
            <label className="block text-lg font-medium text-gray-800 mb-2">
              Solución actual a reemplazar (Target Solution)
            </label>
            <input
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              className="w-full border border-gray-300 rounded-lg p-3 focus:border-primary focus:ring focus:ring-primary/50"
              placeholder="Ej: IBM ESB, Front, SAP, etc."
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white py-3 rounded-full font-semibold hover:bg-primary/90 transition"
          >
            {loading ? 'Procesando...' : 'Obtener Recomendación'}
          </button>
        </form>

        {error && (
          <div className="mt-6 text-red-600 font-medium text-center">
            Error: {error}
          </div>
        )}

        {reportBody && (
          <div className="mt-6">
            <h2 className="text-2xl font-bold text-primary mb-4 text-center">
              {reportTitle}
            </h2>
            <div className="bg-gray-100 p-6 rounded-lg text-gray-800 whitespace-pre-line">
              {reportBody}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
