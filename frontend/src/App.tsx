import { Routes, Route, Link, Navigate, useNavigate } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "./context/authContext";
import Home from "./pages/home";
import Login from "./pages/login";
import Facilities from "./pages/facilities";
import Slots from "./pages/slots";
import MyReservations from "./pages/my-reservations";


function PrivateRoute({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const { user, logout } = useAuth();
  const nav = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <nav className="bg-fitness-secondary text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
              <span className="text-xl font-bold font-display">💪 FitReserve</span>
            </Link>
            <div className="flex items-center gap-4">
              <Link 
                to="/facilities" 
                className="text-sm font-medium hover:text-fitness-primary transition-colors px-3 py-2 rounded-md"
              >
                Instalaciones
              </Link>
              <Link 
                to="/slots" 
                className="text-sm font-medium hover:text-fitness-primary transition-colors px-3 py-2 rounded-md"
              >
                Reservar
              </Link>
              <Link 
                to="/my" 
                className="text-sm font-medium hover:text-fitness-primary transition-colors px-3 py-2 rounded-md"
              >
                Mis Reservas
              </Link>
              {user ? (
                <div className="flex items-center gap-3 ml-4 pl-4 border-l border-gray-600">
                  <span className="text-sm font-medium">
                    {user.nombre}
                    {user.rol === 'admin' && (
                      <span className="ml-2 px-2 py-0.5 text-xs bg-fitness-primary rounded-full">Admin</span>
                    )}
                  </span>
                  <button
                    onClick={() => { logout(); nav("/login"); }}
                    className="px-4 py-2 rounded-lg bg-fitness-primary hover:bg-fitness-primary-dark text-white text-sm font-medium transition-colors"
                  >
                    Salir
                  </button>
                </div>
              ) : (
                <Link 
                  className="px-4 py-2 rounded-lg bg-fitness-primary hover:bg-fitness-primary-dark text-white text-sm font-medium transition-colors" 
                  to="/login"
                >
                  Entrar
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="min-h-[calc(100vh-4rem)]">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/facilities" element={<PrivateRoute><Facilities /></PrivateRoute>} />
          <Route path="/slots" element={<PrivateRoute><Slots /></PrivateRoute>} />
          <Route path="/my" element={<PrivateRoute><MyReservations /></PrivateRoute>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
