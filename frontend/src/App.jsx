import { useState } from "react"
import FileUploader from "./components/FileUploader"
import ResultsDisplay from "./components/ResultsDisplay"
import Header from "./components/Header"

export default function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleUploadComplete = (analysisResult) => {
    setResult(analysisResult)
    setLoading(false)
    setError(null)
  }

  const handleError = (errorMessage) => {
    setError(errorMessage)
    setLoading(false)
  }

  const handleLoadingChange = (isLoading) => {
    setLoading(isLoading)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="lg:sticky lg:top-8 lg:h-fit">
            <FileUploader
              onComplete={handleUploadComplete}
              onError={handleError}
              onLoadingChange={handleLoadingChange}
              isLoading={loading}
            />
          </div>

          {/* Results Section */}
          <div>
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 text-red-200 mb-4">
                <p className="font-semibold">Error</p>
                <p className="text-sm mt-1">{error}</p>
              </div>
            )}

            {loading && (
              <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-8 text-center">
                <div className="inline-block">
                  <div className="animate-spin rounded-full h-8 w-8 border border-blue-400 border-t-blue-200"></div>
                </div>
                <p className="text-blue-200 mt-4">Processing invoice...</p>
              </div>
            )}

            {result && !loading && <ResultsDisplay result={result} />}

            {!result && !loading && !error && (
              <div className="bg-slate-700/50 border border-slate-600 rounded-lg p-8 text-center text-slate-300">
                <p>Upload an invoice PDF to get started</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
