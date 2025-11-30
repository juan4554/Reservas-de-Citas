// src/pages/my-reservations.tsx
import { useEffect, useState } from "react";

const API = (import.meta as any).env?.VITE_API_URL ?? "http://127.0.0.1:8000";

type Reserva = {
  id: number;
  usuario_id?: number;
  instalacion_id?: number;            // <-- la necesitamos para resolver el nombre
  fecha?: string;
  hora_inicio?: string;
  hora_fin?: string;
  estado?: string;
};

type Facility = { id: number; nombre: string; tipo?: string; aforo?: number };

export default function MyReservations() {
  const [items, setItems] = useState<Reserva[]>([]);
  const [facMap, setFacMap] = useState<Map<number, Facility>>(new Map());
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          setErr("No hay token. Inicia sesión.");
          return;
        }

        // Pide reservas + instalaciones en paralelo
        const [resRes, facRes] = await Promise.all([
          fetch(`${API}/reservations/my`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch(`${API}/facilities`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        if (!resRes.ok) {
          const txt = await resRes.text();
          throw new Error(`${resRes.status} ${resRes.statusText} – ${txt}`);
        }
        if (!facRes.ok) {
          const txt = await facRes.text();
          throw new Error(`${facRes.status} ${facRes.statusText} – ${txt}`);
        }

        const reservas: Reserva[] = await resRes.json();
        const facilities: Facility[] = await facRes.json();

        if (!alive) return;

        setItems(Array.isArray(reservas) ? reservas : []);
        setFacMap(new Map(facilities.map((f) => [f.id, f])));
      } catch (e: any) {
        setErr(e?.message ?? "Error desconocido");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  if (loading) return <p className="p-4">Cargando mis reservas…</p>;
  if (err) return <p className="p-4 text-red-600">Error: {err}</p>;
  if (items.length === 0) return <p className="p-4">No tienes reservas.</p>;

  return (
    <div className="space-y-3 p-4">
      <h1 className="text-xl font-semibold">Mis reservas</h1>
      <ul className="grid gap-3">
        {items.map((r) => {
          const fecha = r.fecha ?? "—";
          const ini = r.hora_inicio ?? "—";
          const fin = r.hora_fin ?? "—";
          const facilityName =
            (r.instalacion_id && facMap.get(r.instalacion_id)?.nombre) ?? "-";
          const estado = r.estado ?? "activa";

          return (
            <li key={r.id} className="p-3 rounded border bg-white">
              <div className="font-medium">{facilityName}</div>
              <div className="text-sm text-gray-600">
                {fecha} · {ini}–{fin} · {estado}
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
