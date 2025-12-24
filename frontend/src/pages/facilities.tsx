import { useEffect, useState } from "react";
import { get } from "../lib/http";
import Spinner from "../ui/Spinner";

type Facility = { id: number; nombre: string; tipo?: string; aforo?: number };

function getFacilityImage(nombre: string): string {
  const nameLower = nombre.toLowerCase();
  
  if (nameLower.includes("crossfit") || nameLower.includes("cross fit")) {
    return "https://images.unsplash.com/photo-1549060279-7e168fcee0c2?w=400&h=300&fit=crop";
  }
  
  if (nameLower.includes("mma") || nameLower.includes("artes marciales")) {
    return "https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=400&h=300&fit=crop";
  }
  
  if (nameLower.includes("weightlifting") || nameLower.includes("pesas") || nameLower.includes("halterofilia")) {
    return "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop";
  }
  
  if (nameLower.includes("hyrox")) {
    return "https://images.unsplash.com/photo-1571008887538-b36bb32f4571?w=400&h=300&fit=crop";
  }
  
  if (nameLower.includes("gymnastics") || nameLower.includes("gimnasia")) {
    return "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop";
  }
  
  if (nameLower.includes("pista") || nameLower.includes("central")) {
    return "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop";
  }
  
  return "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=300&fit=crop";
}

export default function Facilities() {
  const [items, setItems] = useState<Facility[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await get<Facility[]>("/facilities");
        setItems(Array.isArray(data) ? data : []);
      } catch (e: any) {
        setErr(e?.message ?? "Error al cargar instalaciones");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <div className="p-4 md:p-6 flex items-center justify-center min-h-[400px]">
        <div className="flex items-center gap-3">
          <Spinner />
          <span className="text-gray-600">Cargando instalaciones...</span>
        </div>
      </div>
    );
  }

  if (err) {
    return (
      <div className="p-4 md:p-6">
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {err}
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl md:text-3xl font-bold mb-2 text-gray-900">Nuestras Instalaciones</h1>
        <p className="text-gray-600">Descubre todos los espacios disponibles para entrenar</p>
      </div>

      <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        {items.map((f) => (
          <li 
            key={f.id} 
            className="group relative overflow-hidden rounded-xl border-2 border-gray-200 bg-white hover:border-fitness-primary hover:shadow-lg transition-all duration-200"
          >
            <div className="h-32 bg-gradient-to-br from-fitness-primary to-fitness-primary-dark flex items-center justify-center overflow-hidden relative">
              <img 
                src={getFacilityImage(f.nombre)} 
                alt={f.nombre}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  const parent = target.parentElement;
                  if (parent && !parent.querySelector('span')) {
                    const fallback = document.createElement('span');
                    fallback.className = 'text-4xl';
                    fallback.textContent = '💪';
                    parent.appendChild(fallback);
                  }
                }}
              />
            </div>
            <div className="p-4 md:p-5">
              <h3 className="font-bold text-lg text-gray-900 mb-2">{f.nombre}</h3>
              {f.tipo && (
                <div className="flex items-center gap-2 text-sm text-gray-600 mb-2">
                  <span>🏋️</span>
                  <span>{f.tipo}</span>
                </div>
              )}
              {f.aforo && (
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <span>👥</span>
                  <span>Capacidad: {f.aforo} personas</span>
                </div>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
