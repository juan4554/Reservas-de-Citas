const fmtDate = new Intl.DateTimeFormat("es-ES", { dateStyle: "medium" });
const fmtTime = new Intl.DateTimeFormat("es-ES", { timeStyle: "short" });

export function formatDate(iso?: string) {
  if (!iso) return "—";
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso : fmtDate.format(d);
}

export function formatTime(iso?: string) {
  if (!iso) return "—";
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso : fmtTime.format(d);
}
