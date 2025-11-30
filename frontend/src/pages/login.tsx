// src/pages/login.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/authContext";
import { API_URL } from "../api/client";

export default function Login() {
  const nav = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("admin@test.local.es");
  const [password, setPassword] = useState("Admin1234");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string>("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");
    setLoading(true);
    try {
      const form = new URLSearchParams();
      form.set("username", email);
      form.set("password", password);
      form.set("grant_type", "password");

      const r = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: form,
      });
      if (!r.ok) throw new Error(await r.text());
      const { access_token } = await r.json();
      if (!access_token) throw new Error("Login sin token");

      localStorage.setItem("access_token", access_token);
      

      const me = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      if (!me.ok) throw new Error(await me.text());
      const u = await me.json(); // { id, nombre, rol }
      login({ id: u.id, nombre: u.nombre, rol: u.rol });

      nav("/facilities", { replace: true });
    } catch (e: any) {
      setErr(e.message || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-lg font-semibold mb-4">Entrar</h1>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="email"
          className="border rounded px-3 py-2 w-full"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="email"
        />
        <input
          type="password"
          className="border rounded px-3 py-2 w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
        />
        {err && <div className="text-sm text-red-600">{err}</div>}
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 rounded bg-indigo-600 text-white disabled:opacity-60"
        >
          {loading ? "Accediendo…" : "Acceder"}
        </button>
      </form>
    </div>
  );
}
