import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "../context/authContext";

export default function AdminRoute({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  if (user.rol !== "admin") {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
}

