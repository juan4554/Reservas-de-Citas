
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

export { API };
