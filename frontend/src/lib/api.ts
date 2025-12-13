
const API = (import.meta as any).env?.VITE_API_URL ?? "http://127.0.0.1:8000";

export function getToken() {
  return localStorage.getItem("access_token");
}

export async function api(path: string, init: RequestInit = {}) {
  const headers = new Headers(init.headers || {});
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (!headers.has("Content-Type") && init.body && !(init.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }
  const res = await fetch(`${API}${path}`, { ...init, headers });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText} – ${text}`);
  }
  return res;
}

// Wrapper compatible con axios para auth.ts
const apiClient = {
  async get<T = any>(path: string, config?: any) {
    const res = await api(path, {
      method: "GET",
      headers: config?.headers,
    });
    const data = res.status === 204 ? undefined : await res.json();
    return { data: data as T };
  },
  async post<T = any>(path: string, body?: any, config?: any) {
    const headers = new Headers(config?.headers || {});
    if (!headers.has("Content-Type") && body && !(body instanceof FormData)) {
      headers.set("Content-Type", "application/json");
    }
    const res = await api(path, {
      method: "POST",
      body: body instanceof FormData ? body : JSON.stringify(body),
      headers,
    });
    const data = res.status === 204 ? undefined : await res.json();
    return { data: data as T };
  },
};

// Exportar el cliente como default para auth.ts
export default apiClient;
export { API };
