import api from "./api";

export type LoginResponse = {
  access_token: string;
  token_type: "bearer";
};

export async function login(username: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", username);
  body.set("password", password);
  body.set("grant_type", "password");
  const { data } = await api.post<LoginResponse>("/auth/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  localStorage.setItem("access_token", data.access_token);
  return data;
}

export async function register(
  nombre: string,
  email: string,
  password: string
) {
  const { data } = await api.post("/auth/register", { nombre, email, password });
  return data;
}

export async function me() {
  const { data } = await api.get("/auth/me");
  return data; // {id, nombre, email, rol}
}

export function logout() {
  localStorage.removeItem("access_token");
}
