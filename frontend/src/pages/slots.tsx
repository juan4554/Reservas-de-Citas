// src/pages/slots.tsx
import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";

type Facility = { id: number; nombre: string };
type Slot = {
  id: number;
  instalacion_id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  plazas_totales: number;
  plazas_disponibles: number;
};

export default function Slots() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [facilityId, setFacilityId] = useState<number | null>(null);
  const [date, setDate] = useState<string>(() => new Date().toISOString().slice(0, 10));
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const r = await api("/facilities");
        const data: Facility[] = await r.json();
        setFacilities(data);
        if (data.length && facilityId === null) setFacilityId(data[0].id);
      } catch (e: any) {
        setErr(e?.message ?? "Error");
      }
    })();
  }, []);

  useEffect(() => {
    if (!facilityId || !date) return;
    let alive = true;
    (async () => {
      try {
        setLoading(true);
        const r = await api(`/slots/by-facility/${facilityId}?fecha=${date}&available_only=false`);
        const data: Slot[] = await r.json();
        if (!alive) return;
        setSlots(data ?? []);
      } catch (e: any) {
        setErr(e?.message ?? "Error");
      } finally {
        setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [facilityId, date]);

  async function reservar(slot: Slot) {
    try {
      const body = JSON.stringify({ instalacion_id: slot.instalacion_id, franja_id: slot.id });
      await api("/reservations", { method: "POST", body });
      alert("Reserva creada");
      // refresca listado
      const r = await api(`/slots/by-facility/${facilityId}?fecha=${date}&available_only=false`);
      setSlots(await r.json());
    } catch (e: any) {
      alert(e?.message ?? "Error al reservar");
    }
  }

  const facilityOptions = useMemo(
    () => facilities.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>),
    [facilities]
  );

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-semibold">Reservar</h1>

      <div className="flex gap-3 items-center">
        <select
          className="border rounded px-2 py-1"
          value={facilityId ?? ""}
          onChange={(e) => setFacilityId(Number(e.target.value))}
        >
          {facilityOptions}
        </select>
        <input
          type="date"
          className="border rounded px-2 py-1"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      {err && <p className="text-red-600">{err}</p>}
      {loading ? (
        <p>Cargando franjas…</p>
      ) : (
        <ul className="grid gap-3">
          {slots.map(s => (
            <li key={s.id} className="p-3 rounded border bg-white flex items-center justify-between">
              <div>
                <div className="font-medium">{s.fecha} · {s.hora_inicio}–{s.hora_fin}</div>
                <div className="text-sm text-gray-600">
                  Plazas: {s.plazas_disponibles}/{s.plazas_totales}
                </div>
              </div>
              <button
                onClick={() => reservar(s)}
                disabled={s.plazas_disponibles <= 0}
                className="px-3 py-1 rounded text-sm bg-indigo-600 text-white disabled:opacity-50"
              >
                Reservar
              </button>
            </li>
          ))}
          {slots.length === 0 && <p>No hay franjas para ese día.</p>}
        </ul>
      )}
    </div>
  );
}
