// src/pages/slots.tsx
import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { apiFetch } from "../api/client";

type Facility = { id: number; nombre: string };
type Slot = {
  id: number;
  instalacion_id: number;
  fecha: string;        // "YYYY-MM-DD"
  hora_inicio: string;  // "HH:MM"
  hora_fin: string;     // "HH:MM"
  plazas_disponibles: number;
};

export default function Slots() {
  const [params, setParams] = useSearchParams();
  const facilityId = Number(params.get("facilityId") || 1);

  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);
  const [date, setDate] = useState(params.get("date") || today);

  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    apiFetch<Facility[]>("/facilities").then(setFacilities).catch(() => {});
  }, []);

  useEffect(() => {
    setParams({ facilityId: String(facilityId), date });
    setLoading(true);
    setErr("");
    apiFetch<Slot[]>(
      `/slots/by-facility/${facilityId}?fecha=${date}&available_only=false`
    )
      .then(setSlots)
      .catch((e) => setErr(e.message || "Error cargando franjas"))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [facilityId, date]);

  async function reservar(slot: Slot) {
    try {
      await apiFetch("/reservations", {
        method: "POST",
        body: JSON.stringify({ instalacion_id: slot.instalacion_id, franja_id: slot.id }),
      });
      // refresca
      const fresh = await apiFetch<Slot[]>(
        `/slots/by-facility/${facilityId}?fecha=${date}&available_only=false`
      );
      setSlots(fresh);
      alert("Reserva creada ✅");
    } catch (e: any) {
      alert(e.message || "No se pudo reservar");
    }
  }

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Reservar</h1>

      <div className="flex gap-3 items-center">
        <select
          className="border rounded px-2 py-1"
          value={facilityId}
          onChange={(e) => setParams({ facilityId: e.target.value, date })}
        >
          {facilities.map((f) => (
            <option key={f.id} value={f.id}>{f.nombre}</option>
          ))}
        </select>

        <input
          type="date"
          className="border rounded px-2 py-1"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      {loading && <div>Cargando franjas…</div>}
      {err && <div className="text-red-600">{err}</div>}

      <ul className="divide-y rounded border bg-white">
        {slots.map((s) => (
          <li key={s.id} className="p-3 flex items-center justify-between">
            <div>
              <div className="font-medium">
                {s.fecha} · {s.hora_inicio}–{s.hora_fin}
              </div>
              <div className="text-sm text-gray-600">
                Plazas: {s.plazas_disponibles}
              </div>
            </div>
            <button
              disabled={s.plazas_disponibles <= 0}
              onClick={() => reservar(s)}
              className="px-3 py-1 rounded bg-indigo-600 text-white disabled:opacity-50"
            >
              Reservar
            </button>
          </li>
        ))}
        {slots.length === 0 && !loading && <li className="p-3 text-sm">Sin franjas.</li>}
      </ul>
    </div>
  );
}
