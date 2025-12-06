export default function ValidationResults({ validation }) {
  return (
    <div className="space-y-4">
      {validation.errors.length === 0 && validation.warnings.length === 0 ? (
        <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
          <p className="text-green-200 font-semibold">No validation issues found</p>
        </div>
      ) : (
        <>
          {/* Errors */}
          {validation.errors.length > 0 && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <p className="text-red-200 font-semibold mb-3">Errors ({validation.errors.length})</p>
              <ul className="space-y-2">
                {validation.errors.map((error, idx) => (
                  <li key={idx} className="text-red-100 text-sm flex items-start gap-2">
                    <span className="text-red-400 mt-0.5">•</span>
                    <div>
                      <span className="font-semibold">{error.field}:</span>
                      <p className="text-red-200/80">{error.message}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Warnings */}
          {validation.warnings.length > 0 && (
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
              <p className="text-yellow-200 font-semibold mb-3">Warnings ({validation.warnings.length})</p>
              <ul className="space-y-2">
                {validation.warnings.map((warning, idx) => (
                  <li key={idx} className="text-yellow-100 text-sm flex items-start gap-2">
                    <span className="text-yellow-400 mt-0.5">•</span>
                    <div>
                      <span className="font-semibold">{warning.field}:</span>
                      <p className="text-yellow-200/80">{warning.message}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  )
}
