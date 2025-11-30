import { useEffect, useState } from "react";

const API = "http://localhost:8000";

type Facility = { id: number; nombre: string; tipo?: string; aforo?: string  };

export default function Facilities() {
  const [items, setItems] = useState<Facility[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const r = await fetch(`${API}/facilities`);
      const data = await r.json();
      setItems(data);
      setLoading(false);
    })();
  }, []);

  if (loading) return <p>Cargando instalaciones…</p>;

  return (
    <div className="space-y-3">
      <h1 className="text-xl font-semibold">Servicios ofrecidos</h1>
      <ul className="grid gap-3">
        {items.map((f) => (
          <li key={f.id} className="p-3 rounded border bg-white">
            <div className="font-medium">{f.nombre}</div>
            <div className="text-sm text-gray-600">{f.tipo ?? "—"}</div>
            <div className="text-sm text-gray-600">{f.aforo ?? "—"}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
