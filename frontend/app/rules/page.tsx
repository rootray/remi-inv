"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
  getToken,
  listRules,
  createRule,
  updateRule,
  deleteRule,
  type Rule,
  type RuleAction,
} from "@/lib/api";

const ACTION_LABELS: Record<RuleAction, string> = {
  reinvest_all: "Reinvest all dividends",
  threshold: "Reinvest if amount ≥ threshold",
  target_symbol: "Reinvest into a specific symbol",
};

export default function RulesPage() {
  const router = useRouter();
  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // New rule form state
  const [name, setName] = useState("");
  const [action, setAction] = useState<RuleAction>("reinvest_all");
  const [thresholdAmount, setThresholdAmount] = useState("");
  const [targetSymbol, setTargetSymbol] = useState("");
  const [creating, setCreating] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    listRules()
      .then(setRules)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load rules"))
      .finally(() => setLoading(false));
  }, [router]);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setFormError(null);
    setCreating(true);
    try {
      const body: Parameters<typeof createRule>[0] = { name, action };
      if (action === "threshold") body.threshold_amount = parseFloat(thresholdAmount);
      if (action === "target_symbol") body.target_symbol = targetSymbol.toUpperCase();
      const created = await createRule(body);
      setRules((prev) => [...prev, created]);
      setName("");
      setThresholdAmount("");
      setTargetSymbol("");
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Failed to create rule");
    } finally {
      setCreating(false);
    }
  }

  async function handleToggle(rule: Rule) {
    // Optimistic update
    setRules((prev) => prev.map((r) => r.id === rule.id ? { ...r, is_active: !r.is_active } : r));
    try {
      await updateRule(rule.id, { is_active: !rule.is_active });
    } catch {
      // Revert on failure
      setRules((prev) => prev.map((r) => r.id === rule.id ? { ...r, is_active: rule.is_active } : r));
    }
  }

  async function handleDelete(id: number) {
    // Optimistic update
    setRules((prev) => prev.filter((r) => r.id !== id));
    try {
      await deleteRule(id);
    } catch (err) {
      // Refetch on failure
      listRules().then(setRules);
    }
  }

  if (loading) return <div className="p-8 text-sm text-gray-500">Loading…</div>;
  if (error) return <div className="p-8 text-sm text-red-600">{error}</div>;

  return (
    <div className="min-h-screen">
      <header className="border-b border-gray-200 bg-white px-6 py-4 flex items-center justify-between">
        <h1 className="text-lg font-semibold">DRIP Investing</h1>
        <nav className="flex items-center gap-4 text-sm">
          <a href="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</a>
        </nav>
      </header>

      <main className="mx-auto max-w-2xl px-6 py-8 space-y-8">

        {/* Create rule form */}
        <section>
          <h2 className="text-base font-semibold mb-4">New Rule</h2>
          <form onSubmit={handleCreate} className="space-y-4 rounded-lg border border-gray-200 bg-white p-5">
            <div>
              <label className="block text-sm font-medium mb-1">Rule name</label>
              <input
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Reinvest all dividends"
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Action</label>
              <select
                value={action}
                onChange={(e) => setAction(e.target.value as RuleAction)}
                className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {(Object.entries(ACTION_LABELS) as [RuleAction, string][]).map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </div>
            {action === "threshold" && (
              <div>
                <label className="block text-sm font-medium mb-1">Minimum dividend amount ($)</label>
                <input
                  required
                  type="number"
                  min="0.01"
                  step="0.01"
                  value={thresholdAmount}
                  onChange={(e) => setThresholdAmount(e.target.value)}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}
            {action === "target_symbol" && (
              <div>
                <label className="block text-sm font-medium mb-1">Target symbol</label>
                <input
                  required
                  value={targetSymbol}
                  onChange={(e) => setTargetSymbol(e.target.value)}
                  placeholder="e.g. VTI"
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm uppercase focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}
            {formError && <p className="text-sm text-red-600">{formError}</p>}
            <button
              type="submit"
              disabled={creating}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
            >
              {creating ? "Creating…" : "Create rule"}
            </button>
          </form>
        </section>

        {/* Rules list */}
        <section>
          <h2 className="text-base font-semibold mb-4">Your Rules</h2>
          {rules.length === 0 ? (
            <p className="text-sm text-gray-500">No rules yet. Create one above.</p>
          ) : (
            <ul className="space-y-3">
              {rules.map((rule) => (
                <li
                  key={rule.id}
                  className="flex items-start justify-between rounded-lg border border-gray-200 bg-white px-5 py-4"
                >
                  <div className="space-y-0.5">
                    <p className={`text-sm font-medium ${!rule.is_active ? "text-gray-400 line-through" : ""}`}>
                      {rule.name}
                    </p>
                    <p className="text-xs text-gray-500">{ACTION_LABELS[rule.action]}</p>
                    {rule.threshold_amount != null && (
                      <p className="text-xs text-gray-400">Threshold: ${rule.threshold_amount}</p>
                    )}
                    {rule.target_symbol && (
                      <p className="text-xs text-gray-400">Target: {rule.target_symbol}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-3 ml-4 shrink-0">
                    <button
                      onClick={() => handleToggle(rule)}
                      className={`text-xs font-medium px-2 py-1 rounded-full ${
                        rule.is_active
                          ? "bg-green-100 text-green-700 hover:bg-green-200"
                          : "bg-gray-100 text-gray-500 hover:bg-gray-200"
                      }`}
                    >
                      {rule.is_active ? "Active" : "Inactive"}
                    </button>
                    <button
                      onClick={() => handleDelete(rule.id)}
                      className="text-xs text-red-500 hover:text-red-700"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

      </main>
    </div>
  );
}
