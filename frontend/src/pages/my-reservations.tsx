// src/pages/my-reservations.tsx
import { useEffect, useState } from "react";
import { api } from "../lib/api";

type Reserva = {
  id: number;
  instalacion_id?: number;
  fecha?: string;
  hora_inicio?: string;
  hora_fin?: string;
  estado?: string;
};
type Facility = { id: number; nombre: string };

export default function MyReservations() {
  const [items, setItems] = useState<Reserva[]>([]);
  const [facMap, setFacMap] = useState<Map<number, Facility>>(new Map());
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [rRes, rFac] = await Promise.all([
          api("/reservations/my"),
          api("/facilities"),
        ]);
        const reservas: Reserva[] = await rRes.json();
        const facs: Facility[] = await rFac.json();
        if (!alive) return;
        setItems(reservas ?? []);
        setFacMap(new Map(facs.map(f => [f.id, f])));
      } catch (e: any) {
        setErr(e?.message ?? "Error");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  async function cancelar(id: number) {
    if (!confirm("¿Cancelar la reserva?")) return;
    try {
      await api(`/reservations/${id}`, { method: "DELETE" });
      setItems(prev => prev.filter(x => x.id !== id));
    } catch (e: any) {
      alert(e?.message ?? "Error al cancelar");
    }
  }

  if (loading) return <p className="p-4">Cargando…</p>;
  if (err) return <p className="p-4 text-red-600">Error: {err}</p>;
  if (items.length === 0) return <p className="p-4">No tienes reservas.</p>;

  return (
    <div className="space-y-3 p-4">
      <h1 className="text-xl font-semibold">Mis reservas</h1>
      <ul className="grid gap-3">
        {items.map((r) => {
          const fac = r.instalacion_id ? facMap.get(r.instalacion_id)?.nombre : "-";
          return (
            <li key={r.id} className="p-3 rounded border bg-white flex items-center justify-between">
              <div>
                <div className="font-medium">{fac ?? "-"}</div>
                <div className="text-sm text-gray-600">
                  {r.fecha ?? "—"} · {r.hora_inicio ?? "—"}–{r.hora_fin ?? "—"} · {r.estado ?? "activa"}
                </div>
              </div>
              <button
                onClick={() => cancelar(r.id)}
                className="px-3 py-1 rounded text-sm bg-red-600 text-white hover:bg-red-700"
              >
                Cancelar
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
