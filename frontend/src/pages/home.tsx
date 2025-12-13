import { Link } from "react-router-dom";
import { useAuth } from "../context/authContext";

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-fitness-primary via-fitness-primary-dark to-fitness-secondary text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-4 font-display">
              💪 Reserva tu Entrenamiento
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-orange-100">
              Encuentra y reserva tu clase de Crossfit o Fitness favorita
            </p>
            {!user && (
              <Link
                to="/login"
                className="inline-block px-8 py-4 bg-white text-fitness-primary font-bold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
              >
                Comenzar Ahora
              </Link>
            )}
            {user && (
              <div className="flex gap-4 justify-center">
                <Link
                  to="/slots"
                  className="inline-block px-8 py-4 bg-white text-fitness-primary font-bold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
                >
                  Ver Horarios
                </Link>
                <Link
                  to="/my"
                  className="inline-block px-8 py-4 bg-transparent border-2 border-white text-white font-bold rounded-lg hover:bg-white hover:text-fitness-primary transition-all duration-200"
                >
                  Mis Reservas
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8">
          <div className="text-center p-6 rounded-xl bg-white border-2 border-gray-200 hover:border-fitness-primary transition-colors">
            <div className="text-4xl mb-4">📅</div>
            <h3 className="font-bold text-lg mb-2">Reserva Fácil</h3>
            <p className="text-gray-600 text-sm">
              Selecciona tu horario preferido en segundos
            </p>
          </div>
          
          <div className="text-center p-6 rounded-xl bg-white border-2 border-gray-200 hover:border-fitness-primary transition-colors">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="font-bold text-lg mb-2">Disponibilidad en Tiempo Real</h3>
            <p className="text-gray-600 text-sm">
              Ve las plazas disponibles al instante
            </p>
          </div>
          
          <div className="text-center p-6 rounded-xl bg-white border-2 border-gray-200 hover:border-fitness-primary transition-colors">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="font-bold text-lg mb-2">Gestiona tus Clases</h3>
            <p className="text-gray-600 text-sm">
              Cancela o modifica cuando necesites
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
