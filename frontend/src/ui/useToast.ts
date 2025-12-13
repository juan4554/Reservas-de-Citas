// src/ui/useToast.ts
export function toast(msg: string, type: "info"|"success"|"error" = "info") {
  window.dispatchEvent(new CustomEvent("toast", { detail: { msg, type } }));
}
