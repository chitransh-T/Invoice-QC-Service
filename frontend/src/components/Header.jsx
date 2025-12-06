export default function Header() {
  return (
    <header className="bg-slate-950/80 backdrop-blur border-b border-slate-700">
      <div className="container mx-auto px-4 py-6 max-w-6xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Invoice QC Service</h1>
            <p className="text-slate-400 mt-1">Extract & Validate B2B Invoices</p>
          </div>
          <div className="text-right text-sm text-slate-400">
            <p>FastAPI Backend</p>
            <p>React Frontend</p>
          </div>
        </div>
      </div>
    </header>
  )
}
