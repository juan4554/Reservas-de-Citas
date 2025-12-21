# Guía para Imágenes de Instalaciones

## Páginas Recomendadas para Obtener Imágenes Gratuitas

### 1. **Unsplash** (Recomendado)
- **URL:** https://unsplash.com
- **Ventajas:** 
  - Fotos de alta calidad
  - Uso comercial libre
  - API disponible
  - Búsqueda fácil por palabras clave
- **Cómo usar:**
  1. Busca términos como: "crossfit", "kettlebell", "mma", "boxing", "weightlifting", "gym"
  2. Selecciona una imagen
  3. Haz clic en "Download free"
  4. O usa directamente la URL de Unsplash con parámetros de tamaño

**Ejemplo de URL de Unsplash:**
```
https://images.unsplash.com/photo-[ID]?w=400&h=300&fit=crop
```

**Búsquedas recomendadas:**
- CrossFit: https://unsplash.com/s/photos/crossfit-kettlebell
- MMA: https://unsplash.com/s/photos/mma-boxing
- Weightlifting: https://unsplash.com/s/photos/weightlifting
- Hyrox: https://unsplash.com/s/photos/running-track
- Gymnastics: https://unsplash.com/s/photos/gymnastics
- Pista Central: https://unsplash.com/s/photos/stadium

---

### 2. **Pexels**
- **URL:** https://www.pexels.com
- **Ventajas:**
  - Fotos y videos gratuitos
  - Buena calidad
  - Fácil de descargar
- **Cómo usar:**
  1. Busca términos similares
  2. Descarga la imagen
  3. Colócala en `frontend/public/images/facilities/`
  4. Usa la ruta: `/images/facilities/nombre.jpg`

---

### 3. **Pixabay**
- **URL:** https://pixabay.com
- **Ventajas:**
  - Imágenes, vectores e ilustraciones
  - Buena opción para iconos
  - Sin atribución requerida
- **Cómo usar:**
  1. Busca y descarga
  2. Coloca en `frontend/public/images/facilities/`

---

### 4. **Freepik** (con atribución)
- **URL:** https://www.freepik.com
- **Ventajas:**
  - Gran variedad de recursos
  - Ilustraciones y vectores
- **Nota:** Requiere atribución en algunos casos

---

## Opción 1: Usar URLs de Unsplash (Más Fácil)

Edita el archivo `frontend/src/pages/facilities.tsx` y cambia las URLs en la función `getFacilityImage()`:

```typescript
if (nameLower.includes("crossfit")) {
  return "https://images.unsplash.com/photo-[TU-ID-AQUI]?w=400&h=300&fit=crop";
}
```

**Para obtener el ID de una foto de Unsplash:**
1. Ve a la foto en Unsplash
2. Haz clic derecho → "Copiar dirección de la imagen"
3. O usa el botón "Share" → "Copy link to photo"
4. El ID está en la URL: `unsplash.com/photos/[ID]`

---

## Opción 2: Usar Imágenes Locales (Recomendado para Producción)

1. **Crea la carpeta:**
   ```bash
   mkdir -p frontend/public/images/facilities
   ```

2. **Descarga las imágenes** desde Unsplash, Pexels, etc.

3. **Nombra las imágenes** según la instalación:
   - `crossfit.jpg`
   - `mma.jpg`
   - `weightlifting.jpg`
   - `hyrox.jpg`
   - `gymnastics.jpg`
   - `pista.jpg`
   - `default.jpg`

4. **Colócalas en:** `frontend/public/images/facilities/`

5. **Actualiza el código** en `facilities.tsx`:
   ```typescript
   if (nameLower.includes("crossfit")) {
     return "/images/facilities/crossfit.jpg";
   }
   ```

---

## Tamaños Recomendados

- **Ancho:** 400-800px
- **Alto:** 300-400px
- **Formato:** JPG o WebP (mejor compresión)
- **Peso:** < 200KB por imagen

---

## Ejemplo de Búsquedas Específicas

### CrossFit
- Búsquedas: "crossfit kettlebell", "crossfit workout", "functional training"
- Estilo: Intenso, dinámico, pesas, kettlebells

### MMA
- Búsquedas: "mma boxing", "martial arts", "boxing gloves", "fighting"
- Estilo: Acción, guantes, ring de boxeo

### Weightlifting
- Búsquedas: "weightlifting", "barbell", "powerlifting", "olympic lifting"
- Estilo: Pesas, barras, levantamiento

### Hyrox
- Búsquedas: "running track", "athlete running", "endurance training"
- Estilo: Corredor, pista, atletismo

### Gymnastics
- Búsquedas: "gymnastics", "gymnast", "acrobatics"
- Estilo: Flexibilidad, barras, anillas

### Pista Central
- Búsquedas: "stadium", "sports field", "track field"
- Estilo: Estadio, campo deportivo

---

## Notas Importantes

1. **Derechos de autor:** Todas las páginas mencionadas ofrecen imágenes con licencia libre para uso comercial
2. **Optimización:** Comprime las imágenes antes de usarlas (usa herramientas como TinyPNG)
3. **Fallback:** El código ya incluye un fallback a emoji si la imagen no carga
4. **Responsive:** Las imágenes se ajustan automáticamente al tamaño de la card

