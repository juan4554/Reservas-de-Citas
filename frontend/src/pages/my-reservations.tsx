import { useEffect, useState } from "react";
import { get, del } from "../lib/http";
import { formatDate, formatTime } from "../lib/dates";
import { toast } from "../ui/useToast";
import Spinner from "../ui/Spinner";

type Reserva = {
  id: number;
  fecha?: string;
  hora_inicio?: string;
  hora_fin?: string;
  instalacion?: { id: number; nombre: string };
};

export default function MyReservations() {
  const [items, setItems] = useState<Reserva[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const data = await get<Reserva[]>("/reservations/my");
        if (!alive) return;
        
        // Filtrar solo reservas activas (futuras)
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        const activeReservations = (Array.isArray(data) ? data : []).filter((r) => {
          if (!r.fecha) return false;
          const reservationDate = new Date(r.fecha);
          reservationDate.setHours(0, 0, 0, 0);
          return reservationDate >= today;
        });
        
        setItems(activeReservations);
      } catch (e: any) {
        setErr(e?.message ?? "No se pudieron cargar las reservas");
      } finally {
        setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  async function cancel(id: number) {
    setBusyId(id);
    try {
      await del(`/reservations/${id}`);
      setItems((curr) => curr.filter(r => r.id !== id));
      toast("Reserva cancelada", "success");
    } catch (e: any) {
      toast(e?.message ?? "No se pudo cancelar", "error");
    } finally {
      setBusyId(null);
    }
  }

  if (loading) return <div className="p-4 flex items-center gap-2"><Spinner /> Cargando mis reservas…</div>;
  if (err) return <p className="p-4 text-red-600">Error: {err}</p>;
  if (items.length === 0) return (
    <div className="p-4 text-center">
      <p className="text-gray-600 mb-2">No tienes reservas activas.</p>
      <p className="text-sm text-gray-500">Las reservas pasadas no se muestran aquí.</p>
    </div>
  );

  return (
    <div className="p-4 md:p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl md:text-3xl font-bold mb-2 text-gray-900">Mis Reservas Activas</h1>
        <p className="text-gray-600">Gestiona tus próximas clases y entrenamientos</p>
      </div>

      <ul className="grid gap-4">
        {items.map((r) => {
          const fecha = formatDate(r.fecha);
          const ini = formatTime(r.hora_inicio);
          const fin = formatTime(r.hora_fin);
          const fac = r.instalacion?.nombre ?? "Instalación";
          const fechaObj = r.fecha ? new Date(r.fecha) : null;
          const isToday = fechaObj && fechaObj.toDateString() === new Date().toDateString();
          const isTomorrow = fechaObj && fechaObj.toDateString() === new Date(Date.now() + 86400000).toDateString();

          return (
            <li 
              key={r.id} 
              className="p-4 md:p-6 rounded-xl border-2 border-gray-200 bg-white hover:shadow-lg transition-all duration-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
            >
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="font-bold text-lg text-gray-900">{fac}</h3>
                  {isToday && (
                    <span className="px-2 py-1 text-xs font-semibold bg-fitness-primary text-white rounded-full">
                      Hoy
                    </span>
                  )}
                  {isTomorrow && (
                    <span className="px-2 py-1 text-xs font-semibold bg-fitness-accent text-gray-900 rounded-full">
                      Mañana
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span className="flex items-center gap-1">
                    📅 {fecha}
                  </span>
                  <span className="flex items-center gap-1">
                    ⏰ {ini} - {fin}
                  </span>
                </div>
              </div>
              <button
                onClick={() => cancel(r.id)}
                disabled={busyId === r.id}
                className={`px-4 py-2.5 rounded-lg font-semibold text-sm flex items-center gap-2 transition-all duration-200 ${
                  busyId === r.id 
                    ? "bg-gray-400 text-white cursor-not-allowed" 
                    : "bg-red-500 hover:bg-red-600 text-white shadow-md hover:shadow-lg"
                }`}
              >
                {busyId === r.id && <Spinner size={14} />} 
                Cancelar
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
