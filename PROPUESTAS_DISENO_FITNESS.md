# Propuestas de Diseño - App Fitness/Crossfit

## Análisis de la Interfaz Actual

### Estado Actual
- Diseño básico con colores neutros (grises, índigo)
- Navegación simple pero poco atractiva
- Falta de identidad visual relacionada con fitness
- Componentes funcionales pero sin personalidad

## Propuestas de Mejora

### 1. Paleta de Colores Fitness/Crossfit

#### Opción A: Energético y Dinámico
- **Primario**: Naranja (#FF6B35) / Rojo Coral (#FF6B6B)
- **Secundario**: Negro (#1A1A1A) / Gris Oscuro (#2D2D2D)
- **Acento**: Amarillo Energético (#FFD93D)
- **Fondo**: Blanco / Gris Muy Claro (#F8F9FA)
- **Éxito**: Verde (#10B981)
- **Advertencia**: Amarillo (#F59E0B)
- **Error**: Rojo (#EF4444)

#### Opción B: Moderno y Profesional
- **Primario**: Azul Oscuro (#1E3A5F) / Azul Acero (#2C5282)
- **Secundario**: Naranja (#F97316)
- **Acento**: Turquesa (#14B8A6)
- **Fondo**: Blanco / Gris Claro (#F1F5F9)
- **Éxito**: Verde Esmeralda (#059669)
- **Advertencia**: Ámbar (#D97706)
- **Error**: Rojo (#DC2626)

**Recomendación**: Opción A (Energético) para Crossfit, Opción B para Fitness general

### 2. Tipografía

- **Títulos**: Font Bold, Sans-serif moderna (Inter, Poppins, Montserrat)
- **Cuerpo**: Font Regular/Medium, legible
- **Tamaños**: Jerarquía clara (2xl, xl, lg, base, sm)
- **Pesos**: Bold para títulos, Medium para subtítulos, Regular para texto

### 3. Componentes Mejorados

#### Navbar
- Fondo oscuro (negro/gris oscuro) con logo/icono de fitness
- Botones con efecto hover destacado
- Badge de notificaciones si hay reservas próximas
- Avatar del usuario con dropdown

#### Cards de Instalaciones
- Imágenes de fondo (placeholders con gradientes)
- Iconos representativos (pesas, cinta, etc.)
- Badge de estado (Disponible, Lleno, Mantenimiento)
- Hover effect con elevación

#### Cards de Slots/Horarios
- Diseño tipo "ticket" o "badge"
- Indicador visual de disponibilidad (barra de progreso)
- Color coding: Verde (muchas plazas), Amarillo (pocas), Rojo (agotado)
- Animación al reservar

#### Mis Reservas
- Cards con información destacada
- Badge de "Próxima" para la reserva más cercana
- Botón de cancelar con confirmación
- Filtros: Próximas, Pasadas, Todas

### 4. Iconografía

- Usar iconos relacionados con fitness:
  - Pesas para instalaciones
  - Calendario para reservas
  - Reloj para horarios
  - Usuario/Perfil para cuenta
  - Salida para logout

### 5. Microinteracciones

- Animaciones suaves en hover
- Feedback visual al hacer clic
- Transiciones entre páginas
- Loading states atractivos
- Toast notifications con iconos

### 6. Layout y Espaciado

- Máximo ancho de contenido: 1280px (max-w-7xl)
- Padding consistente: 16px móvil, 24px desktop
- Grid responsivo: 1 col móvil, 2-3 tablet, 4 desktop
- Espaciado generoso entre secciones

### 7. Elementos Específicos Fitness

#### Home Page
- Hero section con call-to-action
- Estadísticas rápidas (reservas esta semana, clases disponibles)
- Accesos rápidos a acciones principales

#### Página de Reservas
- Vista semanal con días destacados
- Indicadores de popularidad (clases más reservadas)
- Filtros por tipo de clase/horario

#### Perfil de Usuario
- Estadísticas personales (reservas totales, asistencia)
- Historial de reservas
- Preferencias (horarios favoritos, instalaciones)

### 8. Responsive Design

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Navegación adaptativa (hamburger menu en móvil)
- Cards apilables en móvil, grid en desktop

### 9. Accesibilidad

- Contraste adecuado (WCAG AA mínimo)
- Tamaños de click targets (mínimo 44x44px)
- Navegación por teclado
- Labels descriptivos
- Estados focus visibles

### 10. Mejoras de UX

- Búsqueda rápida de instalaciones
- Filtros avanzados (horario, tipo, disponibilidad)
- Recordatorios de reservas próximas
- Sistema de favoritos
- Historial de búsquedas

## Implementación Prioritaria

### Fase 1 (Inmediata)
1. ✅ Filtrar reservas activas
2. ✅ Cards de slots de la semana
3. Cambiar paleta de colores a naranja/negro
4. Mejorar tipografía y espaciado
5. Añadir iconos a navegación

### Fase 2 (Corto plazo)
1. Mejorar cards de instalaciones con imágenes
2. Añadir animaciones y transiciones
3. Mejorar página de inicio
4. Sistema de notificaciones toast mejorado

### Fase 3 (Medio plazo)
1. Estadísticas y dashboard
2. Sistema de favoritos
3. Búsqueda y filtros avanzados
4. Modo oscuro (opcional)

## Referencias de Diseño

- **Crossfit**: Colores vibrantes, diseño bold, tipografía fuerte
- **Fitness Apps**: Clean, moderno, con buen uso del espacio blanco
- **Booking Apps**: UX clara, proceso de reserva intuitivo
- **Sports Apps**: Energía, movimiento, dinamismo

