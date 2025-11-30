import { createContext, useContext } from "react";

export type User = { id: number; nombre: string; rol: "admin" | "cliente" } | null;

export type AuthCtx = {
  user: User;
  loading: boolean;
  login: (u: NonNullable<User>) => void;
  logout: () => void;
};

export const AuthContext = createContext<AuthCtx | undefined>(undefined);

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de <AuthProvider>");
  return ctx;
}
