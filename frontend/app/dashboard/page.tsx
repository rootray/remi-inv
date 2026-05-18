"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getToken,
  clearToken,
  getPositions,
  getDividends,
  getReinvestmentLog,
  type Position,
  type Dividend,
  type ReinvestmentLog,
} from "@/lib/api";

export default function DashboardPage() {
  const router = useRouter();
  const [positions, setPositions] = useState<Position[]>([]);
  const [dividends, setDividends] = useState<Dividend[]>([]);
  const [logs, setLogs] = useState<ReinvestmentLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    Promise.all([getPositions(), getDividends(), getReinvestmentLog()])
      .then(([p, d, l]) => {
        setPositions(p);
        setDividends(d);
        setLogs(l);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, [router]);

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  if (loading) return <div className="p-8 text-sm text-gray-500">Loading…</div>;
  if (error) return <div className="p-8 text-sm text-red-600">{error}</div>;

  return (
    <div className="min-h-screen">
      <header className="border-b border-gray-200 bg-white px-6 py-4 flex items-center justify-between">
        <h1 className="text-lg font-semibold">DRIP Investing</h1>
        <nav className="flex items-center gap-4 text-sm">
          <a href="/rules" className="text-gray-600 hover:text-gray-900">Rules</a>
          <button onClick={handleLogout} className="text-gray-500 hover:text-gray-900">Sign out</button>
        </nav>
      </header>

      <main className="mx-auto max-w-5xl px-6 py-8 space-y-10">

        {/* Positions */}
        <section>
          <h2 className="text-base font-semibold mb-3">Positions</h2>
          {positions.length === 0 ? (
            <p className="text-sm text-gray-500">No positions found.</p>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-left text-xs text-gray-500 uppercase">
                  <tr>
                    <th className="px-4 py-2">Symbol</th>
                    <th className="px-4 py-2">Qty</th>
                    <th className="px-4 py-2">Market Value</th>
                    <th className="px-4 py-2">Current Price</th>
                    <th className="px-4 py-2">Unrealised P&L</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {positions.map((p) => (
                    <tr key={p.symbol} className="bg-white">
                      <td className="px-4 py-2 font-medium">{p.symbol}</td>
                      <td className="px-4 py-2">{p.qty}</td>
                      <td className="px-4 py-2">${p.market_value}</td>
                      <td className="px-4 py-2">${p.current_price}</td>
                      <td className={`px-4 py-2 ${parseFloat(p.unrealized_pl) >= 0 ? "text-green-600" : "text-red-600"}`}>
                        ${p.unrealized_pl}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Recent dividends */}
        <section>
          <h2 className="text-base font-semibold mb-3">Dividends (last 30 days)</h2>
          {dividends.length === 0 ? (
            <p className="text-sm text-gray-500">No dividend activity in the last 30 days.</p>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-left text-xs text-gray-500 uppercase">
                  <tr>
                    <th className="px-4 py-2">Symbol</th>
                    <th className="px-4 py-2">Net Amount</th>
                    <th className="px-4 py-2">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {dividends.map((d, i) => (
                    <tr key={i} className="bg-white">
                      <td className="px-4 py-2 font-medium">{d.symbol}</td>
                      <td className="px-4 py-2">${d.net_amount}</td>
                      <td className="px-4 py-2">{d.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Reinvestment log */}
        <section>
          <h2 className="text-base font-semibold mb-3">Reinvestment Log</h2>
          {logs.length === 0 ? (
            <p className="text-sm text-gray-500">No reinvestments recorded yet.</p>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 text-left text-xs text-gray-500 uppercase">
                  <tr>
                    <th className="px-4 py-2">Source</th>
                    <th className="px-4 py-2">Target</th>
                    <th className="px-4 py-2">Amount</th>
                    <th className="px-4 py-2">Status</th>
                    <th className="px-4 py-2">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {logs.map((log) => (
                    <tr key={log.id} className="bg-white">
                      <td className="px-4 py-2 font-medium">{log.source_symbol}</td>
                      <td className="px-4 py-2">{log.target_symbol}</td>
                      <td className="px-4 py-2">${log.dividend_amount}</td>
                      <td className="px-4 py-2">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                          log.status === "filled" ? "bg-green-100 text-green-700"
                          : log.status === "failed" ? "bg-red-100 text-red-700"
                          : "bg-yellow-100 text-yellow-700"
                        }`}>
                          {log.status}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-gray-500">
                        {new Date(log.executed_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

      </main>
    </div>
  );
}
