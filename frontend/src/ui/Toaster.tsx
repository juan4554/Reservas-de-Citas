// src/ui/Toaster.tsx
import React from "react";

type Toast = { id: number; msg: string; type?: "info"|"success"|"error" };
let nextId = 1;

export default function Toaster() {
  const [toasts, setToasts] = React.useState<Toast[]>([]);

  React.useEffect(() => {
    function onToast(e: Event) {
      const detail = (e as CustomEvent).detail as { msg: string; type?: Toast["type"] };
      const t: Toast = { id: nextId++, msg: detail.msg, type: detail.type || "info" };
      setToasts((curr) => [...curr, t]);
      setTimeout(() => setToasts((curr) => curr.filter(x => x.id !== t.id)), 3000);
    }
    window.addEventListener("toast", onToast as any);
    return () => window.removeEventListener("toast", onToast as any);
  }, []);

  return (
    <div className="fixed right-4 top-4 z-50 space-y-2">
      {toasts.map(t => (
        <div
          key={t.id}
          className={
            "px-3 py-2 rounded shadow text-sm text-white " +
            (t.type === "success" ? "bg-green-600" :
             t.type === "error" ? "bg-red-600" : "bg-gray-800")
          }
        >
          {t.msg}
        </div>
      ))}
    </div>
  );
}
