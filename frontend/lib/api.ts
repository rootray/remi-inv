const BASE = "/api";

// ── Types ────────────────────────────────────────────────────────────────────

export type RuleAction = "reinvest_all" | "threshold" | "target_symbol";
export type ReinvestmentStatus = "pending" | "filled" | "failed";

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface CredentialStatus {
  has_credentials: boolean;
  base_url: string | null;
  updated_at: string | null;
}

export interface Position {
  symbol: string;
  qty: string;
  market_value: string;
  unrealized_pl: string;
  current_price: string;
}

export interface Dividend {
  symbol: string;
  net_amount: string;
  date: string;
}

export interface ReinvestmentLog {
  id: number;
  source_symbol: string;
  target_symbol: string;
  dividend_amount: string;
  shares_purchased: string | null;
  alpaca_order_id: string | null;
  status: ReinvestmentStatus;
  error_message: string | null;
  executed_at: string;
}

export interface Rule {
  id: number;
  name: string;
  action: RuleAction;
  threshold_amount: number | null;
  target_symbol: string | null;
  is_active: boolean;
}

export interface RuleCreate {
  name: string;
  action: RuleAction;
  threshold_amount?: number;
  target_symbol?: string;
  is_active?: boolean;
}

export interface RuleUpdate {
  name?: string;
  action?: RuleAction;
  threshold_amount?: number;
  target_symbol?: string;
  is_active?: boolean;
}

// ── Token helpers ─────────────────────────────────────────────────────────────

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("drip_token");
}

export function setToken(token: string): void {
  localStorage.setItem("drip_token", token);
}

export function clearToken(): void {
  localStorage.removeItem("drip_token");
}

// ── Fetch wrapper ─────────────────────────────────────────────────────────────

async function request<T>(
  path: string,
  options: RequestInit = {},
  auth = true,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    clearToken();
    window.location.href = "/login";
    throw new Error("Unauthorised");
  }

  if (res.status === 204) return undefined as T;

  const data = await res.json();
  if (!res.ok) throw new Error(data?.detail ?? `HTTP ${res.status}`);
  return data as T;
}

// ── Auth ──────────────────────────────────────────────────────────────────────

export async function register(email: string, password: string): Promise<User> {
  return request<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }, false);
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  return request<TokenResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }, false);
}

// ── Users ─────────────────────────────────────────────────────────────────────

export async function getMe(): Promise<User> {
  return request<User>("/users/me");
}

export async function upsertCredentials(
  api_key: string,
  secret_key: string,
  base_url: string,
): Promise<void> {
  return request<void>("/users/me/credentials", {
    method: "PUT",
    body: JSON.stringify({ api_key, secret_key, base_url }),
  });
}

export async function getCredentialStatus(): Promise<CredentialStatus> {
  return request<CredentialStatus>("/users/me/credentials");
}

// ── Portfolio ─────────────────────────────────────────────────────────────────

export async function getPositions(): Promise<Position[]> {
  return request<Position[]>("/portfolio/positions");
}

export async function getDividends(since?: string): Promise<Dividend[]> {
  const qs = since ? `?since=${encodeURIComponent(since)}` : "";
  return request<Dividend[]>(`/portfolio/dividends${qs}`);
}

export async function getReinvestmentLog(limit = 50, offset = 0): Promise<ReinvestmentLog[]> {
  return request<ReinvestmentLog[]>(`/portfolio/reinvestment-log?limit=${limit}&offset=${offset}`);
}

// ── Rules ─────────────────────────────────────────────────────────────────────

export async function listRules(): Promise<Rule[]> {
  return request<Rule[]>("/rules");
}

export async function createRule(body: RuleCreate): Promise<Rule> {
  return request<Rule>("/rules", { method: "POST", body: JSON.stringify(body) });
}

export async function updateRule(id: number, body: RuleUpdate): Promise<Rule> {
  return request<Rule>(`/rules/${id}`, { method: "PATCH", body: JSON.stringify(body) });
}

export async function deleteRule(id: number): Promise<void> {
  return request<void>(`/rules/${id}`, { method: "DELETE" });
}
