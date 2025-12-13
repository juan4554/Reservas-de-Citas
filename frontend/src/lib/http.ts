// src/lib/http.ts
const API = (import.meta as any).env?.VITE_API_URL ?? "http://127.0.0.1:8000";

function getToken() {
  return localStorage.getItem("access_token");
}

async function handle<T>(res: Response): Promise<T> {
  if (res.status === 401) {
    // token inválido/expirado → limpiar y a login
    localStorage.removeItem("access_token");
    // opcional: señal para toaster
    window.dispatchEvent(new CustomEvent("toast", { detail: { type: "error", msg: "Sesión caducada. Vuelve a iniciar sesión." }}));
    location.replace("/login");
    throw new Error("No autorizado (401)");
  }
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`${res.status} ${res.statusText} – ${txt}`);
  }
  // si no hay contenido (204), devolver undefined
  if (res.status === 204) return undefined as unknown as T;
  return res.json() as Promise<T>;
}

export async function get<T>(path: string, init?: RequestInit) {
  const token = getToken();
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      "Accept": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers || {}),
    },
  });
  return handle<T>(res);
}

export async function post<T>(path: string, body?: any, init?: RequestInit) {
  const token = getToken();
  const res = await fetch(`${API}${path}`, {
    method: "POST",
    body: body instanceof FormData ? body : JSON.stringify(body ?? {}),
    headers: {
      ...(body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      "Accept": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers || {}),
    },
    ...init,
  });
  return handle<T>(res);
}

export async function del<T>(path: string, init?: RequestInit) {
  const token = getToken();
  const res = await fetch(`${API}${path}`, {
    method: "DELETE",
    headers: {
      "Accept": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers || {}),
    },
    ...init,
  });
  return handle<T>(res);
}
