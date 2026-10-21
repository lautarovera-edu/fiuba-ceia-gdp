# Guía: llevar la planificación del GdP V4 a Jira

> Nota de terminología: desde fines de 2025 Atlassian renombró "Projects" a
> "Spaces" en toda la interfaz de Jira. Es un cambio de nombre únicamente —
> la distinción Team-managed/Company-managed, el importador CSV, los
> sprints y la jerarquía Epic → Story → Sub-task funcionan exactamente
> igual que antes, solo que el contenedor se llama "Space" en vez de
> "Project". Esta guía ya usa esa terminología.

Archivos en esta carpeta (`jira/` del repo):

- `build_import.py` — script que genera los dos CSV de abajo (fuente de verdad; si corregís algo, editá este script y volvé a correrlo).
- `jira_import.csv` — 101 filas: 5 épicas, 10 historias de usuario, 86 tareas (sub-tareas + tareas de gestión). **Todo el contenido de los tickets (Summary, Description, Epic Name) está en inglés**, como corresponde a los tickets del proyecto. Las claves internas (`HU1`, `E1`, nombres de Sprint, `Priority: High/Medium/Low`) y las fechas usan convenciones en inglés también.
- `sprint_dates.csv` — fechas de inicio/fin aproximadas de los 12 sprints + receso ("Break") + contingencia ("Contingency").

## 0. Por qué no lo hago yo directamente

Existe un conector MCP de Atlassian disponible, pero:

1. Requiere autorización OAuth interactiva (`/mcp` en una sesión interactiva de Claude Code), que no está disponible aquí.
2. Crear un **Space** nuevo en Jira normalmente exige permisos de administrador del sitio, que una cuenta corporativa individual suele no tener.

Si más adelante querés que yo cree o actualice issues directamente vía API (una vez que el Space ya exista), corré `/mcp` en una sesión interactiva de Claude Code y autorizá el conector de Atlassian; en la próxima conversación podré leer y escribir issues de Jira con ese conector.

## 1. Crear el Space

1. En Jira, `Create space` → plantilla **Scrum** → tipo **Team-managed** (ícono de personas, no "Company-managed"; esta distinción no cambió con el rename a Spaces).
2. Nombre sugerido: `NLoS Detection (UWB)`. Clave sugerida: `NLOS`.
3. En `Space settings → Features`, confirmá que estén activos: **Sprints**, **Epics** y **Story points**. Si vas a usar la columna `Original Estimate`, activá también **Time tracking**.

## 2. Importar el CSV

Jira → ícono de engranaje (arriba a la derecha) → **System** → **External System Import** → **CSV**. Subí `jira_import.csv`.

En la pantalla de mapeo de columnas:

| Columna del CSV | Campo de Jira |
|---|---|
| `Issue Id` | **Issue id** (campo especial del importador, no es un campo real de Jira) |
| `Parent Id` | **Parent id** |
| `Issue Type` | Issue Type |
| `Summary` | Summary |
| `Description` | Description |
| `Epic Name` | Epic Name |
| `Priority` | Priority |
| `Story Points` | Story point estimate |
| `Sprint` | Sprint |
| `Original Estimate` | Original Estimate |
| `Labels` | Labels |

El par **Issue id / Parent id** es la clave: le dice a Jira "esta fila es hija de aquella otra fila del mismo archivo", y Jira infiere automáticamente si esa relación es *Epic Link* (cuando el padre es una Epic) o *parent de sub-tarea* (cuando el padre es una Story). No son campos reales de Jira — existen solo para resolver la jerarquía durante la importación, así que no vas a verlos después en los issues creados.

Revisá el preview (Jira te muestra una tabla antes de confirmar) y lanzá la importación.

### Si tu instancia no soporta Issue id/Parent id

Algunas instancias con el importador CSV restringido (o configuraciones de administrador distintas) no resuelven bien esta jerarquía en una sola pasada. Si después de importar ves las Stories o Sub-tareas sueltas, sin padre:

1. Filtrá el CSV para quedarte solo con las filas `Epic` + `Story` (quitá las de `Issue Type = Sub-task/Task`) e importá primero esa versión reducida.
2. Anotá las claves reales que Jira asignó a cada HU (p. ej. `NLOS-6` para HU1, `NLOS-7` para HU2, etc.).
3. En el CSV completo, hacé buscar-y-reemplazar de cada `HU1`, `HU2`... (columna `Parent Id`) por la clave real (`NLOS-6`, `NLOS-7`...), y de `E1`...`E5` por las claves reales de las épicas.
4. Importá de nuevo, ahora solo las filas `Sub-task`/`Task`.

## 3. Crear los 12 sprints y fecharlos

El importador de Jira crea los sprints por nombre (`Sprint 0`...`Sprint 11`) pero **no puede fijarles fecha de inicio/fin**. Después de importar:

1. Andá al **Backlog** del Space. Vas a ver los 12 sprints creados (vacíos de fecha) con sus issues ya adentro.
2. Para cada uno, abrí el menú `⋯ → Edit sprint` y cargá las fechas de `sprint_dates.csv`:

| Sprint | Inicio | Fin |
|---|---|---|
| Sprint 0 | 2026-08-25 | 2026-11-02 |
| Sprint 1 | 2026-11-03 | 2026-11-23 |
| Sprint 2 | 2026-11-24 | 2026-12-14 |
| *(Break: 2026-12-15 a 2027-01-11, sin sprint)* | | |
| Sprint 3 | 2027-01-12 | 2027-02-01 |
| Sprint 4 | 2027-02-02 | 2027-02-22 |
| Sprint 5 | 2027-02-23 | 2027-03-15 |
| Sprint 6 | 2027-03-16 | 2027-04-05 |
| Sprint 7 | 2027-04-06 | 2027-04-26 |
| Sprint 8 | 2027-04-27 | 2027-05-17 |
| Sprint 9 | 2027-05-18 | 2027-06-07 |
| Sprint 10 | 2027-06-08 | 2027-06-28 |
| *(Contingency: 2027-06-29 a 2027-07-12, sin sprint)* | | |
| Sprint 11 | 2027-07-13 | 2027-11-15 |

Son fechas calculadas a partir de las duraciones del cuadro 5 del documento (inicio 25/ago/2026, fin con la defensa el 15/nov/2027 — coincide exacto con la fecha de defensa del acta, lo que confirma que el cálculo es consistente). Ajustalas si tu Gantt real difiere en algún punto.

Las 2 tareas con label `cross-cutting` (reuniones de seguimiento, informe de avance) quedan **sin sprint asignado** a propósito, porque el documento las describe como actividades que atraviesan todo el proyecto, no ligadas a un sprint puntual. Podés dejarlas en el Backlog y moverlas manualmente al sprint donde correspondan, o crear para ellas un sprint "Cross-cutting" ficticio si preferís verlas en el tablero.

## 4. Checklist de verificación

Después de importar, confirmá:

- [ ] 5 épicas: E1 a E4 (el backlog real) + E5 (gestión/cierre, no es backlog).
- [ ] 10 historias de usuario, Story Points sumando **89** en total (HU1=5, HU2=5, HU3=8, HU4=8, HU5=8, HU6=13, HU7=13, HU8=13, HU9=8, HU10=8).
- [ ] 86 tareas (sub-tareas bajo las HU + tareas sueltas bajo E5), con horas sumando **600 h** en total.
- [ ] HU10 marcada como prioridad Low/opcional, bajo la épica E4.
- [ ] Cada HU tiene al menos 3 criterios de aceptación en su descripción (ya vienen cargados desde la sección 7 del documento, traducidos al inglés).
- [ ] 12 sprints visibles en el Backlog con las fechas de la tabla anterior.

## 5. Para más adelante: Atlassian MCP

Si querés que en futuras conversaciones yo pueda leer el estado del tablero, actualizar el % de avance de las tareas, o crear nuevos issues directamente (por ejemplo, al cerrar cada sprint real):

1. En una sesión **interactiva** de Claude Code (no en este modo), corré `/mcp`.
2. Autorizá el conector `plugin:product-management:atlassian` contra tu cuenta corporativa (tu administrador de Jira debe permitir apps/conectores OAuth de terceros — si no podés autorizarlo vos mismo, es por política de la organización).
3. En la próxima conversación yo podré usar ese conector sobre el Space que ya creaste con esta guía.
