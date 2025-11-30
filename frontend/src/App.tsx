// src/App.tsx
import { Routes, Route, Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "./context/authContext";
import Home from "./pages/home";
import Login from "./pages/login";
import Facilities from "./pages/facilities";
import Slots from "./pages/slots";
import MyReservations from "./pages/my-reservations";

function PrivateRoute({ children }: { children: JSX.Element }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

export default function App() {
  const { user, logout } = useAuth();
  const nav = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <nav className="flex items-center justify-between px-4 py-3 shadow bg-white">
        <Link to="/" className="font-semibold">Reserva Sport</Link>
        <div className="flex items-center gap-3">
          <Link to="/facilities" className="text-sm underline">Instalaciones</Link>
          <Link to="/slots?facilityId=1" className="text-sm underline">Reservar</Link>
          <Link to="/my" className="text-sm underline">Mis reservas</Link>
          {user ? (
            <>
              <span className="text-sm">Hola, {user.nombre} ({user.rol})</span>
              <button
                onClick={() => { logout(); nav("/login"); }}
                className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 text-sm"
              >Salir</button>
            </>
          ) : (
            <Link className="px-3 py-1 rounded bg-indigo-600 text-white text-sm" to="/login">
              Entrar
            </Link>
          )}
        </div>
      </nav>

      <main className="p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/facilities" element={<PrivateRoute><Facilities /></PrivateRoute>} />
          <Route path="/slots" element={<PrivateRoute><Slots /></PrivateRoute>} />
          <Route path="/my" element={<PrivateRoute><MyReservations /></PrivateRoute>} /> {/* <- RUTA */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
