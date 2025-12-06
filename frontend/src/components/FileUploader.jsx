"use client"

import { useRef } from "react"

export default function FileUploader({ onComplete, onError, onLoadingChange, isLoading }) {
  const fileInputRef = useRef(null)

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    if (!file.name.endsWith(".pdf")) {
      onError("Please select a PDF file")
      return
    }

    onLoadingChange(true)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`)
      }

      const data = await response.json()
      onComplete(data)
    } catch (err) {
      onError(err.message || "Failed to process invoice")
    }
  }

  return (
    <div className="bg-slate-700/50 border-2 border-dashed border-slate-600 rounded-lg p-8">
      <div className="text-center">
        <div className="mx-auto w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center mb-4">
          <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
        </div>
        <h2 className="text-xl font-semibold text-white mb-2">Upload Invoice</h2>
        <p className="text-slate-300 text-sm mb-6">Select a PDF file to analyze and validate</p>

        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isLoading}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-semibold py-2 px-6 rounded-lg transition-colors"
        >
          {isLoading ? "Processing..." : "Choose PDF"}
        </button>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          disabled={isLoading}
          className="hidden"
        />

        <p className="text-slate-400 text-xs mt-4">PDF files only • Max 10 MB</p>
      </div>
    </div>
  )
}
