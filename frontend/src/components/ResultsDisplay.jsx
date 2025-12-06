"use client"

import { useState } from "react"
import ExtractedDataTable from "./ExtractedDataTable"
import ValidationResults from "./ValidationResults"

export default function ResultsDisplay({ result }) {
  const [activeTab, setActiveTab] = useState("validation")

  if (!result.success) {
    return (
      <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-6 text-red-200">
        <p className="font-semibold">Failed to process invoice</p>
      </div>
    )
  }

  const validation = result.validation
  const isValid = validation.is_valid

  return (
    <div className="space-y-4">
      {/* Status Badge */}
      <div className="flex items-center gap-3">
        <div
          className={`px-4 py-2 rounded-lg font-semibold text-white flex items-center gap-2 ${
            isValid ? "bg-green-600" : "bg-red-600"
          }`}
        >
          {isValid ? (
            <>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              Valid Invoice
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              Invalid Invoice
            </>
          )}
        </div>
        <span className="text-slate-300">
          Invoice: <span className="font-semibold text-white">{validation.invoice_number || "N/A"}</span>
        </span>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-slate-700">
        <button
          onClick={() => setActiveTab("validation")}
          className={`px-4 py-2 font-semibold transition-colors ${
            activeTab === "validation"
              ? "text-blue-400 border-b-2 border-blue-400"
              : "text-slate-400 hover:text-slate-200"
          }`}
        >
          Validation Results
        </button>
        <button
          onClick={() => setActiveTab("extracted")}
          className={`px-4 py-2 font-semibold transition-colors ${
            activeTab === "extracted"
              ? "text-blue-400 border-b-2 border-blue-400"
              : "text-slate-400 hover:text-slate-200"
          }`}
        >
          Extracted Data
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === "validation" && <ValidationResults validation={validation} />}
      {activeTab === "extracted" && <ExtractedDataTable data={result.extracted} />}
    </div>
  )
}
