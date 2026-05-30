# Guion Demo Day — Comercial

**Audiencia:** gerencia, planificadores de compras y stakeholders de negocio. **NO** técnicos.
**Duración:** 10 minutos.
**Lenguaje:** pesos, días, porcentajes. Cero jerga técnica (sin "MLflow", "Docker", "FastAPI", "MAPE", "R²").
**Versión técnica del guion:** [docs/DEMO_DAY.md](DEMO_DAY.md).

> Lee este guion tal cual durante el pitch. Cada bloque tiene **qué decir**,
> **qué mostrar** y **frases listas para usar**. Si algo falla, ver Plan B.

---

## Pre-flight (5 min antes)

```powershell
docker compose up -d
Start-Sleep 30
1..10 | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body '{"days":30,"series":"valor_neto"}' -ContentType "application/json" | Out-Null }
```

(Eso último genera tráfico de muestra para que la app y los gráficos tengan datos visibles.)

**Pestañas abiertas en navegador, EN ESTE ORDEN:**

1. **Streamlit** — http://localhost:8501 *(la estrella del pitch comercial)*
2. **Una hoja de Excel real** del cliente (para contraste visual).
3. *(opcional, si te queda tiempo)* Grafana — http://localhost:3000

Cierra todas las pestañas técnicas (MLflow, API docs, Prometheus). El cliente comercial **no necesita verlas**.

---

## 0:00 – 1:30 · El problema cuesta plata (90 s)

**Qué decir** (lectura directa):

> "Imaginen que mañana abren su supermercado en Cali y, en sólo una sede, una
> de cada cuatro neveras tiene un producto vencido y, al mismo tiempo, una de
> cada diez perchas de productos populares está vacía. **Eso pasa hoy en la
> cadena**. Cada quiebre es una venta perdida; cada vencimiento es plata
> tirada a la basura.
>
> El proceso actual depende de Excel, intuición y reportes que llegan tarde.
> Cuando el planificador ve un dato, ya tomó la decisión de compra. Y nadie
> puede auditar **por qué** compró lo que compró."

**Qué mostrar:** una hoja de Excel real del cliente (o la captura de una). Cambia entre 2-3 pestañas para enfatizar la complejidad.

**Cierre del bloque:**

> "El problema no es que falte data. El problema es que la data **no llega
> convertida en decisión**."

---

## 1:30 – 3:00 · La solución es **una pantalla** (90 s)

**Qué decir:**

> "Diseñamos Forescast: una herramienta que toma todo el histórico de ventas
> y, en una sola pantalla, le dice al planificador **cuánto vender en los
> próximos 7, 15 o 30 días**, qué día va a ser el más fuerte y cuánto
> ingresar en promedio.
>
> No es un reporte que llega por correo a las 8 a.m. Es una pantalla que el
> equipo de compras consulta cuando va a tomar la decisión, con la
> información del cierre de ayer.
>
> Lo que reemplaza:
>
> - Cinco hojas de Excel consolidando data.
> - Reportes manuales por sede.
> - Reuniones de 2 horas para acordar "cuánto pido al proveedor".
> - Decisiones por intuición sin registro.
>
> Lo que **no** cambia:
>
> - El criterio del experto sigue mandando. La pantalla **propone**; el
>   planificador **decide**."

**Qué mostrar:** Streamlit abierto en la página inicial (http://localhost:8501).

> Tono: vendiéndoles tranquilidad, no disrupción.

---

## 3:00 – 7:30 · Demo: el día de un planificador (4:30 min)

### 3:00 – 4:00 · Selección y pronóstico

**Qué hacer en pantalla:**

1. Abrir Streamlit en http://localhost:8501.
2. En la barra lateral izquierda, seleccionar **Serie a pronosticar:**
   *"Ventas (valor neto)"*.
3. Mover el slider a **30 días**.
4. Click en **Generar pronóstico**.

**Qué decir mientras carga:**

> "Marta, jefa de compras, llega un lunes a planear las compras del próximo
> mes. Selecciona 'Ventas' y el horizonte que necesita: 30 días. Un click."

### 4:00 – 5:30 · Los KPIs que el negocio necesita

**Qué señalar en pantalla** (las 4 tarjetas superiores):

1. **Total esperado de los próximos 30 días.**
   > "En menos de 5 segundos, Marta ya sabe que se esperan X mil millones de
   > pesos en venta neta. Sin abrir Excel, sin pedir un reporte."

2. **Promedio diario.**
   > "El promedio diario le da una base de comparación: ¿qué día estoy por
   > encima, qué día por debajo del esperado?"

3. **Día con mayor pronóstico.**
   > "Saber con anticipación el día pico le permite **negociar entregas con
   > proveedores**, programar más personal en caja y asegurar que las
   > góndolas estén llenas el día que importa."

4. **Fuente del dato.**
   > "Esto es importante: cada pronóstico queda registrado y dice qué motor
   > lo generó. Trazabilidad total para auditoría."

### 5:30 – 6:30 · El gráfico — historia + futuro juntos

**Qué señalar:** el gráfico azul (histórico) + naranja (pronóstico).

**Qué decir:**

> "En azul ven el comportamiento real del último año. En naranja, lo que el
> sistema espera del próximo mes. Los picos de fin de quincena, los valles
> de los lunes, todo lo que el equipo ya intuía, ahora está **cuantificado y
> proyectado**.
>
> Esto no reemplaza al experto: lo **arma** con un cañón."

### 6:30 – 7:30 · Tabla detallada — el aterrizaje operativo

**Qué hacer:** clic en *Detalle del pronóstico* para mostrar la tabla día por día.

**Qué decir:**

> "Cuando Marta va a hacer la orden al proveedor, no necesita promedios:
> necesita el valor exacto del día. Esta tabla es la **conexión directa
> entre el modelo y la orden de compra**.
>
> Lo descarga en CSV, lo cruza con su catálogo, y en 15 minutos tiene la
> orden lista. Antes le tomaba media mañana."

---

## 7:30 – 9:00 · Caso de negocio (90 s)

**Qué decir:**

> "Hablemos de impacto. Estos son los compromisos del proyecto, definidos en
> nuestro tablero de innovación de datos junto con la cadena:"

**Mostrar (puede ser una diapositiva impresa o el README sección §6.1):**

| Indicador | Compromiso | Significado para el negocio |
|---|---|---|
| **Error promedio del pronóstico** | ≤ 10 % | Cada peso pronosticado se desvía menos de 10 centavos del real |
| **Calidad del ajuste** | R² ≥ 0,80 | El modelo explica al menos el 80 % del comportamiento de la serie |
| **Tiempo del reporte de ventas** | De medio día a < 1 min | Decisiones de compra el mismo día del cierre |
| **Trazabilidad de decisiones** | 100 % | Cada pronóstico queda registrado con su modelo y fecha |

**Beneficios cualitativos del piloto:**

> "Para esta primera versión, basada sólo en el histórico crudo, ya logramos
> el menor error de los 7 modelos comparados. Para llegar a la meta del 10 %,
> el roadmap incluye:
>
> - **Calendario de festivos** de Cali y Colombia.
> - **Promociones y descuentos** del cliente.
> - **Eventos macro** (inflación, clima, fin de quincena ampliada).
> - **Detalle por categoría o sede**, no sólo total agregado.
>
> Cada una de esas inversiones cierra una porción de la brecha. La
> plataforma está lista para incorporarlas **sin reescribir nada**."

---

## 9:00 – 10:00 · Cierre y llamada a la acción (60 s)

**Qué decir:**

> "Resumiendo: **Forescast convierte el histórico de ventas en decisiones
> auditables en minutos**, en una pantalla, con trazabilidad total. La
> arquitectura es lo suficientemente robusta para soportar la operación
> diaria de la cadena, y lo suficientemente flexible para crecer con ella.
>
> **Lo que proponemos:**
>
> 1. Un **piloto de 4–6 semanas** con dos categorías reales suyas. Sin
>    integración al ERP todavía. El equipo de compras valida los pronósticos
>    en paralelo a su proceso actual.
> 2. Al final del piloto, comparamos: aciertos, ahorros y horas-hombre.
> 3. Si los números cierran, **fase 2**: integración con el ERP y monitoreo
>    24/7 con alertas automáticas.
>
> **Lo que necesitamos del cliente:**
>
> - Acceso a un histórico de ventas de al menos un año (formato CSV o
>   conexión directa).
> - Un punto de contacto del equipo de compras para validar los resultados.
> - 2 horas semanales del planificador durante el piloto.
>
> Gracias. ¿Preguntas?"

---

## Frases de transición (entre bloques)

Si necesitas relleno o el público se queda callado, usa estas:

- "Esto que ven aquí es exactamente lo que el planificador va a ver mañana."
- "Quiero que noten algo clave..."
- "Pongamos esto en contexto de negocio."
- "Volvamos al problema que les planteé al inicio."
- "Hagamos las cuentas en pesos."

---

## Preguntas frecuentes (FAQ comercial)

| Si te preguntan… | Respondes (1-2 frases) |
|---|---|
| **¿Cuánto cuesta?** | "Lo definimos según el alcance del piloto. La plataforma es open-source; el costo es el equipo que la implementa y mantiene. Te paso una propuesta detallada en 48 h." |
| **¿En cuánto tiempo lo tenemos?** | "Piloto: 4–6 semanas. Integración con ERP: 2–3 meses adicionales. Producción estable: 6 meses." |
| **¿Y la seguridad de los datos?** | "Todo corre en el perímetro del cliente, on-premise o en su cloud privada. Los datos nunca salen de su infraestructura." |
| **¿Qué pasa si me equivoco con el modelo?** | "El sistema guarda historial de todos los pronósticos y su exactitud real. Si un modelo se degrada, se cambia a otro registrado sin tocar la integración con el ERP." |
| **¿Necesito un científico de datos en mi equipo?** | "Para usarlo, no. Para evolucionarlo, idealmente uno externo o consultor en fase 2. La plataforma está pensada para que IT del cliente la opere con poco entrenamiento." |
| **¿Por qué Cali y no otras ciudades?** | "Empezamos aquí por proximidad académica con UAO y porque tenemos un caso real validado. La solución es replicable en cualquier ciudad o cadena de LATAM." |
| **¿Esto reemplaza al planificador?** | "No. **Le quita el trabajo de consolidación de Excel** y le devuelve tiempo para negociar con proveedores, gestionar excepciones y mejorar márgenes. Su criterio sigue siendo el que decide." |
| **¿Y si el modelo se equivoca y compro de más?** | "La pantalla muestra **siempre** el rango de incertidumbre. El planificador siempre tiene la decisión final con visibilidad del riesgo." |
| **¿Funciona con mi ERP actual?** | "Sí. La API es estándar REST; cualquier ERP moderno (SAP, Oracle, locales) la consume con un conector simple." |
| **¿Por qué confiar en estudiantes de maestría?** | "Esto no es un trabajo de clase: es un proyecto con un equipo industrial validado por la UAO, código abierto, métricas verificables, y un product ready para piloto. La diferencia con un POC es que **ya corre**." |

---

## Plan B — qué hacer si algo falla en vivo

| Falla | Acción inmediata |
|---|---|
| **Streamlit no carga** | Mostrar capturas del proceso desde celular o slides. Continuar narrativa. |
| **El pronóstico tarda mucho** | "Está procesando un año de data en tiempo real" — esperar 10 s. Si no responde, pasar a las capturas. |
| **El público pregunta algo muy técnico** | "Esa es una excelente pregunta para nuestro equipo técnico, te la respondo en detalle por correo después de la sesión. Para mantener el tiempo, sigamos con [siguiente bloque]." |
| **Te preguntan por costo y no quieres comprometerte** | "Eso lo cerramos en una segunda conversación con tu equipo de IT y compras, donde te paso la propuesta formal." |
| **Te quedaste sin tiempo** | Saltar directo al **§9:00 cierre y llamada a la acción**. Es lo más importante: pedir la próxima reunión. |
| **El público parece desinteresado** | Volver a frases de impacto: "Esto les ahorra X horas por semana de su equipo de compras". |

---

## Métricas que vas a usar

Memoriza estos 5 datos para citarlos sin papel:

1. **17 GB** de histórico de ventas procesado.
2. **365 días** de horizonte hacia atrás.
3. **30 días** de horizonte hacia adelante.
4. **20,96 % de error promedio** en el modelo actual (mejora con más datos).
5. **Meta: 10 % de error** según el tablero de innovación acordado.

> Nota: nunca cites MAPE o R² ante audiencia comercial. Traduce siempre:
> "error promedio del pronóstico", "calidad del ajuste".

---

## Repartición del equipo (sugerencia comercial)

- **Juan M. Velásquez** — abre el pitch (problema y solución, slides 0:00–3:00).
- **Jenn Ramos** — demo en vivo de Streamlit (3:00–7:30).
- **Frank Daza** — caso de negocio y KPIs (7:30–9:00).
- **Yancarlos Cuarán** — cierre, ask y manejo de preguntas (9:00–10:00).

Si presenta una sola persona, mantener el guion. Si son dos, dividir 3:00 (demo) + 7:30 (cierre).

---

## Materiales complementarios para llevar

- Impresión del **§7:30 tabla de compromisos** (1 hoja, formato vertical).
- Impresión del gráfico principal de Streamlit (captura del día anterior).
- Tarjetas con QR al repositorio y al README.
- Hoja con los pasos del piloto (4–6 semanas) ya estructurados.

---

*Forescast_Project · UAO · 2026 · Versión comercial del guion Demo Day*
