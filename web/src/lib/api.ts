const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function throwApiError(response: Response): Promise<never> {
  const raw = await response.text();
  throw new Error(raw || "Request failed");
}

async function request<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    return throwApiError(res);
  }
  return res.json();
}

export async function createPlan(body: { query: string; preferences: string }) {
  return request<{ summary: string; score: number; items: Array<{ title: string; detail: string; score: number }> }>(
    "/api/plan",
    body,
  );
}

export async function createInsights(body: { selection: string; context: string }) {
  return request<{ insights: string[]; next_actions: string[]; highlights: string[] }>("/api/insights", body);
}
