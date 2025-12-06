export default function ExtractedDataTable({ data }) {
  return (
    <div className="space-y-4">
      {/* Basic Info */}
      <div className="bg-slate-700/50 rounded-lg p-4 space-y-3">
        <h3 className="font-semibold text-white">Invoice Details</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-slate-400">Invoice Number</p>
            <p className="text-white font-semibold">{data.invoice_number || "—"}</p>
          </div>
          <div>
            <p className="text-slate-400">Date</p>
            <p className="text-white font-semibold">{data.invoice_date || "—"}</p>
          </div>
          <div>
            <p className="text-slate-400">Due Date</p>
            <p className="text-white font-semibold">{data.due_date || "—"}</p>
          </div>
          <div>
            <p className="text-slate-400">Currency</p>
            <p className="text-white font-semibold">{data.currency || "—"}</p>
          </div>
        </div>
      </div>

      {/* Party Info */}
      <div className="bg-slate-700/50 rounded-lg p-4 space-y-3">
        <h3 className="font-semibold text-white">Parties</h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="text-sm">
            <p className="text-slate-400 mb-1">Seller</p>
            <p className="text-white font-semibold">{data.seller_name || "—"}</p>
            <p className="text-slate-300 text-xs mt-1">{data.seller_address || "N/A"}</p>
          </div>
          <div className="text-sm">
            <p className="text-slate-400 mb-1">Buyer</p>
            <p className="text-white font-semibold">{data.buyer_name || "—"}</p>
            <p className="text-slate-300 text-xs mt-1">{data.buyer_address || "N/A"}</p>
          </div>
        </div>
      </div>

      {/* Amounts */}
      <div className="bg-slate-700/50 rounded-lg p-4 space-y-3">
        <h3 className="font-semibold text-white">Amounts</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-slate-400">Net Total</span>
            <span className="text-white font-semibold">
              {data.net_total ? `${data.net_total.toFixed(2)} ${data.currency}` : "—"}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Tax ({data.tax_percentage}%)</span>
            <span className="text-white font-semibold">
              {data.tax_amount ? `${data.tax_amount.toFixed(2)} ${data.currency}` : "—"}
            </span>
          </div>
          <div className="border-t border-slate-600 pt-2 mt-2 flex justify-between">
            <span className="text-slate-300 font-semibold">Gross Total</span>
            <span className="text-blue-400 font-bold text-lg">
              {data.gross_total ? `${data.gross_total.toFixed(2)} ${data.currency}` : "—"}
            </span>
          </div>
        </div>
      </div>

      {/* Line Items */}
      {data.line_items && data.line_items.length > 0 && (
        <div className="bg-slate-700/50 rounded-lg p-4 space-y-3">
          <h3 className="font-semibold text-white">Line Items</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-600">
                  <th className="text-left text-slate-400 py-2 px-2">Description</th>
                  <th className="text-right text-slate-400 py-2 px-2">Qty</th>
                  <th className="text-right text-slate-400 py-2 px-2">Unit Price</th>
                  <th className="text-right text-slate-400 py-2 px-2">Total</th>
                </tr>
              </thead>
              <tbody>
                {data.line_items.map((item, idx) => (
                  <tr key={idx} className="border-b border-slate-700 hover:bg-slate-600/30">
                    <td className="text-white py-2 px-2">{item.description}</td>
                    <td className="text-right text-slate-300 py-2 px-2">{item.quantity}</td>
                    <td className="text-right text-slate-300 py-2 px-2">{item.unit_price.toFixed(2)}</td>
                    <td className="text-right text-white py-2 px-2 font-semibold">{item.line_total.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
