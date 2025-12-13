import { useEffect, useState } from "react";
import { get, del } from "../lib/http";
import { formatDate, formatTime } from "../lib/dates";
import { toast } from "../ui/useToast";
import Spinner from "../ui/Spinner";

type Reserva = {
  id: number;
  usuario_id: number;
  usuario_nombre: string;
  usuario_email: string;
  instalacion_id: number;
  instalacion_nombre: string;
  franja_id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  estado: string;
};

type ReservasPorUsuario = {
  usuario_id: number;
  usuario_nombre: string;
  usuario_email: string;
  reservas: Reserva[];
};

export default function AdminReservations() {
  const [reservasPorUsuario, setReservasPorUsuario] = useState<ReservasPorUsuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [busyId, setBusyId] = useState<number | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [filtroEstado, setFiltroEstado] = useState<string>("");
  const [filtroUsuario, setFiltroUsuario] = useState<string>("");

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const params = new URLSearchParams();
        if (filtroEstado) {
          params.append("estado", filtroEstado);
        }
        params.append("limit", "1000"); // Obtener todas las reservas
        
        const data = await get<{ items: Reserva[]; total: number }>(`/admin/reservations?${params.toString()}`);
        if (!alive) return;
        
        const reservas = data.items || [];
        
        // Agrupar por usuario
        const agrupadas = reservas.reduce((acc, reserva) => {
          const key = reserva.usuario_id;
          if (!acc[key]) {
            acc[key] = {
              usuario_id: reserva.usuario_id,
              usuario_nombre: reserva.usuario_nombre,
              usuario_email: reserva.usuario_email,
              reservas: [],
            };
          }
          acc[key].reservas.push(reserva);
          return acc;
        }, {} as Record<number, ReservasPorUsuario>);
        
        // Convertir a array y ordenar por nombre de usuario
        const resultado = Object.values(agrupadas).sort((a, b) =>
          a.usuario_nombre.localeCompare(b.usuario_nombre)
        );
        
        // Filtrar por búsqueda de usuario si existe
        const filtrado = filtroUsuario
          ? resultado.filter(
              (grupo) =>
                grupo.usuario_nombre.toLowerCase().includes(filtroUsuario.toLowerCase()) ||
                grupo.usuario_email.toLowerCase().includes(filtroUsuario.toLowerCase())
            )
          : resultado;
        
        setReservasPorUsuario(filtrado);
      } catch (e: any) {
        setErr(e?.message ?? "No se pudieron cargar las reservas");
      } finally {
        setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, [filtroEstado, filtroUsuario]);

  async function cancel(id: number) {
    setBusyId(id);
    try {
      await del(`/admin/reservations/${id}`);
      // Actualizar estado local
      setReservasPorUsuario((curr) =>
        curr.map((grupo) => ({
          ...grupo,
          reservas: grupo.reservas.map((r) =>
            r.id === id ? { ...r, estado: "cancelada" } : r
          ),
        }))
      );
      toast("Reserva cancelada", "success");
    } catch (e: any) {
      toast(e?.message ?? "No se pudo cancelar", "error");
    } finally {
      setBusyId(null);
    }
  }

  if (loading) {
    return (
      <div className="p-4 flex items-center gap-2">
        <Spinner /> Cargando reservas...
      </div>
    );
  }

  if (err) {
    return <p className="p-4 text-red-600">Error: {err}</p>;
  }

  const totalReservas = reservasPorUsuario.reduce((sum, grupo) => sum + grupo.reservas.length, 0);

  return (
    <div className="p-4 md:p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl md:text-3xl font-bold mb-2 text-gray-900">
          Administración de Reservas
        </h1>
        <p className="text-gray-600">
          Gestiona todas las reservas del sistema agrupadas por usuario
        </p>
      </div>

      {/* Filtros */}
      <div className="mb-6 p-4 bg-white rounded-lg shadow-md border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filtrar por estado
            </label>
            <select
              value={filtroEstado}
              onChange={(e) => setFiltroEstado(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fitness-primary focus:border-transparent"
            >
              <option value="">Todas</option>
              <option value="activa">Activas</option>
              <option value="cancelada">Canceladas</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Buscar usuario
            </label>
            <input
              type="text"
              value={filtroUsuario}
              onChange={(e) => setFiltroUsuario(e.target.value)}
              placeholder="Nombre o email..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fitness-primary focus:border-transparent"
            />
          </div>
        </div>
        <div className="mt-4 text-sm text-gray-600">
          Total: {totalReservas} reservas en {reservasPorUsuario.length} usuarios
        </div>
      </div>

      {reservasPorUsuario.length === 0 ? (
        <div className="p-8 text-center bg-white rounded-lg shadow-md border border-gray-200">
          <p className="text-gray-600 mb-2">No se encontraron reservas.</p>
          <p className="text-sm text-gray-500">
            {filtroEstado || filtroUsuario
              ? "Intenta ajustar los filtros."
              : "Aún no hay reservas en el sistema."}
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {reservasPorUsuario.map((grupo) => (
            <div
              key={grupo.usuario_id}
              className="bg-white rounded-xl shadow-lg border-2 border-gray-200 overflow-hidden"
            >
              {/* Encabezado del usuario */}
              <div className="bg-gradient-to-r from-fitness-primary to-fitness-secondary text-white p-4 md:p-6">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <div>
                    <h2 className="text-xl md:text-2xl font-bold">{grupo.usuario_nombre}</h2>
                    <p className="text-sm text-gray-200 mt-1">{grupo.usuario_email}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">{grupo.reservas.length}</div>
                    <div className="text-sm text-gray-200">
                      {grupo.reservas.length === 1 ? "reserva" : "reservas"}
                    </div>
                  </div>
                </div>
              </div>

              {/* Lista de reservas del usuario */}
              <div className="p-4 md:p-6">
                <ul className="space-y-3">
                  {grupo.reservas
                    .sort((a, b) => {
                      // Ordenar por fecha y hora
                      const fechaA = new Date(`${a.fecha}T${a.hora_inicio}`);
                      const fechaB = new Date(`${b.fecha}T${b.hora_inicio}`);
                      return fechaB.getTime() - fechaA.getTime();
                    })
                    .map((reserva) => {
                      const fecha = formatDate(reserva.fecha);
                      const ini = formatTime(reserva.hora_inicio);
                      const fin = formatTime(reserva.hora_fin);
                      const fechaObj = new Date(reserva.fecha);
                      const isToday =
                        fechaObj.toDateString() === new Date().toDateString();
                      const isPast = fechaObj < new Date() && !isToday;
                      const isCancelada = reserva.estado === "cancelada";

                      return (
                        <li
                          key={reserva.id}
                          className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                            isCancelada
                              ? "bg-gray-100 border-gray-300 opacity-75"
                              : isPast
                              ? "bg-gray-50 border-gray-200"
                              : "bg-white border-gray-200 hover:shadow-md"
                          }`}
                        >
                          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                            <div className="flex-1">
                              <div className="flex items-center gap-3 mb-2 flex-wrap">
                                <h3 className="font-bold text-lg text-gray-900">
                                  {reserva.instalacion_nombre}
                                </h3>
                                {isCancelada && (
                                  <span className="px-2 py-1 text-xs font-semibold bg-gray-500 text-white rounded-full">
                                    Cancelada
                                  </span>
                                )}
                                {!isCancelada && isToday && (
                                  <span className="px-2 py-1 text-xs font-semibold bg-fitness-primary text-white rounded-full">
                                    Hoy
                                  </span>
                                )}
                                {!isCancelada && isPast && (
                                  <span className="px-2 py-1 text-xs font-semibold bg-gray-400 text-white rounded-full">
                                    Pasada
                                  </span>
                                )}
                                {!isCancelada && !isPast && !isToday && (
                                  <span className="px-2 py-1 text-xs font-semibold bg-green-500 text-white rounded-full">
                                    Futura
                                  </span>
                                )}
                              </div>
                              <div className="flex items-center gap-4 text-sm text-gray-600 flex-wrap">
                                <span className="flex items-center gap-1">
                                  📅 {fecha}
                                </span>
                                <span className="flex items-center gap-1">
                                  ⏰ {ini} - {fin}
                                </span>
                                <span className="text-xs text-gray-500">
                                  ID: {reserva.id}
                                </span>
                              </div>
                            </div>
                            {!isCancelada && (
                              <button
                                onClick={() => cancel(reserva.id)}
                                disabled={busyId === reserva.id}
                                className={`px-4 py-2.5 rounded-lg font-semibold text-sm flex items-center gap-2 transition-all duration-200 whitespace-nowrap ${
                                  busyId === reserva.id
                                    ? "bg-gray-400 text-white cursor-not-allowed"
                                    : "bg-red-500 hover:bg-red-600 text-white shadow-md hover:shadow-lg"
                                }`}
                              >
                                {busyId === reserva.id && <Spinner size={14} />}
                                Cancelar
                              </button>
                            )}
                          </div>
                        </li>
                      );
                    })}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

