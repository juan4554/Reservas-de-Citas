// src/pages/slots.tsx
import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";
import { formatDate, formatTime } from "../lib/dates";
import { toast } from "../ui/useToast";
import Spinner from "../ui/Spinner";

type Facility = { id: number; nombre: string; tipo?: string };
type Slot = {
  id: number;
  instalacion_id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  capacidad: number;
  plazas_disponibles: number;
};

// Función para obtener los próximos 7 días
function getWeekDates(): string[] {
  const dates: string[] = [];
  const today = new Date();
  for (let i = 0; i < 7; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    dates.push(date.toISOString().slice(0, 10));
  }
  return dates;
}

// Agrupar slots por fecha
function groupSlotsByDate(slots: Slot[]): Record<string, Slot[]> {
  const grouped: Record<string, Slot[]> = {};
  slots.forEach(slot => {
    if (!grouped[slot.fecha]) {
      grouped[slot.fecha] = [];
    }
    grouped[slot.fecha].push(slot);
  });
  return grouped;
}

export default function Slots() {
  const [facilities, setFacilities] = useState<Facility[]>([]);
  const [facilityId, setFacilityId] = useState<number | null>(null);
  const [slots, setSlots] = useState<Slot[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [reservingId, setReservingId] = useState<number | null>(null);

  const weekDates = useMemo(() => getWeekDates(), []);

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

  // Cargar slots de toda la semana cuando se selecciona una instalación
  useEffect(() => {
    if (!facilityId) return;
    
    let alive = true;
    (async () => {
      try {
        setLoading(true);
        setErr(null);
        
        // Cargar slots de todos los días de la semana
        const allSlots: Slot[] = [];
        for (const date of weekDates) {
          try {
            const r = await api(`/slots/by-facility/${facilityId}?fecha=${date}&available_only=false`);
            const daySlots: Slot[] = await r.json();
            allSlots.push(...daySlots);
          } catch (e) {
            // Ignorar errores de días sin slots
          }
        }
        
        if (!alive) return;
        setSlots(allSlots);
      } catch (e: any) {
        if (alive) {
          setErr(e?.message ?? "Error al cargar franjas");
        }
      } finally {
        if (alive) {
          setLoading(false);
        }
      }
    })();
    
    return () => { alive = false; };
  }, [facilityId, weekDates]);

  async function reservar(slot: Slot) {
    setReservingId(slot.id);
    try {
      const body = JSON.stringify({ instalacion_id: slot.instalacion_id, franja_id: slot.id });
      await api("/reservations", { method: "POST", body });
      toast("Reserva creada exitosamente", "success");
      
      // Actualizar el slot reservado
      setSlots(prev => prev.map(s => 
        s.id === slot.id 
          ? { ...s, plazas_disponibles: s.plazas_disponibles - 1 }
          : s
      ));
    } catch (e: any) {
      toast(e?.message ?? "Error al reservar", "error");
    } finally {
      setReservingId(null);
    }
  }

  const facilityOptions = useMemo(
    () => facilities.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>),
    [facilities]
  );

  const selectedFacility = facilities.find(f => f.id === facilityId);
  const slotsByDate = useMemo(() => groupSlotsByDate(slots), [slots]);

  return (
    <div className="p-4 md:p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl md:text-3xl font-bold mb-2 text-gray-900">Reservar Clase</h1>
        <p className="text-gray-600">Selecciona una instalación y elige tu horario</p>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Instalación
        </label>
        <select
          className="w-full md:w-auto min-w-[250px] border-2 border-gray-300 rounded-lg px-4 py-2.5 text-base focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white"
          value={facilityId ?? ""}
          onChange={(e) => setFacilityId(Number(e.target.value))}
        >
          {facilityOptions}
        </select>
      </div>

      {err && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {err}
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Spinner />
          <span className="ml-3 text-gray-600">Cargando horarios disponibles...</span>
        </div>
      ) : facilityId && (
        <div className="space-y-6">
          {weekDates.map(date => {
            const daySlots = slotsByDate[date] || [];
            const dateObj = new Date(date);
            const isToday = date === new Date().toISOString().slice(0, 10);
            const dayName = dateObj.toLocaleDateString('es-ES', { weekday: 'long' });
            const dayNumber = dateObj.getDate();
            const monthName = dateObj.toLocaleDateString('es-ES', { month: 'short' });

            return (
              <div key={date} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className={`px-4 py-3 border-b ${isToday ? 'bg-orange-50 border-orange-200' : 'bg-gray-50 border-gray-200'}`}>
                  <div className="flex items-center gap-3">
                    <div className={`font-bold text-lg ${isToday ? 'text-orange-600' : 'text-gray-700'}`}>
                      {dayName.charAt(0).toUpperCase() + dayName.slice(1)}
                    </div>
                    <div className="text-sm text-gray-600">
                      {dayNumber} {monthName}
                    </div>
                    {isToday && (
                      <span className="ml-auto px-2 py-1 text-xs font-semibold bg-orange-500 text-white rounded-full">
                        Hoy
                      </span>
                    )}
                  </div>
                </div>
                
                {daySlots.length === 0 ? (
                  <div className="px-4 py-8 text-center text-gray-500">
                    No hay horarios disponibles este día
                  </div>
                ) : (
                  <div className="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                    {daySlots.map(slot => {
                      const isAvailable = slot.plazas_disponibles > 0;
                      const isReserving = reservingId === slot.id;
                      const availabilityPercent = (slot.plazas_disponibles / slot.capacidad) * 100;
                      
                      return (
                        <div
                          key={slot.id}
                          className={`relative p-4 rounded-lg border-2 transition-all duration-200 ${
                            isAvailable
                              ? 'border-gray-200 hover:border-orange-400 hover:shadow-md bg-white cursor-pointer'
                              : 'border-gray-100 bg-gray-50 opacity-60'
                          }`}
                        >
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex-1">
                              <div className="font-semibold text-lg text-gray-900">
                                {formatTime(slot.hora_inicio)} - {formatTime(slot.hora_fin)}
                              </div>
                            </div>
                            {isAvailable && (
                              <div className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                availabilityPercent > 50
                                  ? 'bg-green-100 text-green-700'
                                  : availabilityPercent > 25
                                  ? 'bg-yellow-100 text-yellow-700'
                                  : 'bg-red-100 text-red-700'
                              }`}>
                                {slot.plazas_disponibles} plazas
                              </div>
                            )}
                          </div>
                          
                          <div className="mb-3">
                            <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                              <span>Disponibilidad</span>
                              <span>{slot.plazas_disponibles}/{slot.capacidad}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full transition-all ${
                                  availabilityPercent > 50
                                    ? 'bg-green-500'
                                    : availabilityPercent > 25
                                    ? 'bg-yellow-500'
                                    : 'bg-red-500'
                                }`}
                                style={{ width: `${availabilityPercent}%` }}
                              />
                            </div>
                          </div>

                          <button
                            onClick={() => reservar(slot)}
                            disabled={!isAvailable || isReserving}
                            className={`w-full py-2.5 px-4 rounded-lg font-semibold text-sm transition-all duration-200 ${
                              isAvailable && !isReserving
                                ? 'bg-orange-500 hover:bg-orange-600 text-white shadow-md hover:shadow-lg transform hover:-translate-y-0.5'
                                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            }`}
                          >
                            {isReserving ? (
                              <span className="flex items-center justify-center gap-2">
                                <Spinner size={16} />
                                Reservando...
                              </span>
                            ) : isAvailable ? (
                              'Reservar'
                            ) : (
                              'Agotado'
                            )}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {!facilityId && !loading && (
        <div className="text-center py-12 text-gray-500">
          Selecciona una instalación para ver los horarios disponibles
        </div>
      )}
    </div>
  );
}
