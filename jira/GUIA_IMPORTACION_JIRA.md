# Guía: llevar la planificación del GdP V4 a Jira

> Nota de terminología: desde fines de 2025 Atlassian renombró "Projects" a
> "Spaces" en toda la interfaz de Jira. Es un cambio de nombre únicamente —
> la distinción Team-managed/Company-managed, el importador CSV, los
> sprints y la jerarquía Epic → Story → Subtask funcionan exactamente
> igual que antes, solo que el contenedor se llama "Space" en vez de
> "Project". Esta guía ya usa esa terminología.

Archivos en esta carpeta (`jira/` del repo):

- `build_import.py` — script que genera `jira_import.csv` (fuente de verdad; si corregís algo, editá este script y volvé a correrlo).
- `jira_import.csv` — 101 filas: 5 épicas, 10 historias de usuario, 86 tareas (sub-tareas + tareas de gestión), con las columnas `Issue ID`/`Parent` que arman la jerarquía Epic → Story → Subtask en una sola importación. La referencia de "cuándo" es el sprint de cada ítem; solo las épicas y las tareas sin sprint traen **Start date** y **Due date** (no se usa time tracking). **Todo el contenido de los tickets (Summary, Description) está en inglés**, como corresponde a los tickets del proyecto.
- `sprint_dates.csv` — fechas de inicio/fin aproximadas de los 12 sprints + receso ("Break") + contingencia ("Contingency").

## 0. Por qué no lo hago yo directamente

Existe un conector MCP de Atlassian disponible, pero:

1. Requiere autorización OAuth interactiva (`/mcp` en una sesión interactiva de Claude Code), que no está disponible aquí.
2. El import de CSV con jerarquía completa (ver sección 2) requiere permisos de administrador del sitio Jira, que tu cuenta no tiene (lo confirmaste: "You do not have access to Jira settings or Atlassian admin").

Si más adelante querés que yo cree o actualice issues directamente vía API, corré `/mcp` en una sesión interactiva de Claude Code y autorizá el conector de Atlassian; en la próxima conversación podré leer y escribir issues de Jira con ese conector (igual va a necesitar que alguien con los permisos correspondientes lo autorice contra la cuenta corporativa).

## 1. El Space (ya creado)

El Space `NLoS Detection (UWB)` (clave `NLOS`), Scrum, team-managed, ya está creado. En `Space settings → Work types`, confirmá que cada tipo tenga en *Context fields* los campos que usa el CSV. Si falta alguno, arrastralo desde el panel derecho y tocá **Save changes**:

| Work type | Campos necesarios (además de Summary y Description) |
|---|---|
| Epic | Start date, Due date |
| Story | Parent, Priority, Story point estimate, Sprint |
| Subtask | Parent, Priority |
| Task | Parent, Priority, Sprint, Labels, Start date, Due date |

Las Subtasks no llevan Sprint: Jira siempre las mantiene en el sprint de su Story. Por eso el sprint va cargado en la Story. HU6 abarca los sprints 6 y 7: se importa en el Sprint 6, y al cerrarlo Jira ofrece pasar lo pendiente al Sprint 7.

## 2. Importar el CSV

Hay **dos importadores de CSV distintos** en Jira Cloud, y arman jerarquías de forma muy distinta:

- **"Import work items from CSV"** (Filtros → Search work items → ••• → Import work items from CSV): lo puede usar cualquier usuario con permiso para crear issues, pero **no arma jerarquías** (Epic → Story → Subtask). Sirve solo para cargar issues sueltos.
- **"External System Import"** (ícono de engranaje → **System** → **External System Import** → **CSV**): el único que arma la jerarquía completa en una sola pasada, usando un par de columnas `Issue ID`/`Parent` ([documentado por Atlassian](https://support.atlassian.com/jira/kb/keep-issue-parent-child-mapping-during-csv-import-to-jira-cloud/)). **Requiere ser administrador del sitio o de la organización** — vos no lo sos (lo vimos en tu menú de configuración, que solo muestra "Personal Jira settings").

`jira_import.csv` está armado para el segundo importador. Como no tenés ese permiso, la opción real es:

### Opción A (recomendada): que el administrador de Jira lo corra por vos

Mandale al administrador de Jira de MobileKnowledge el archivo `jira_import.csv` y estos pasos:

1. Ícono de engranaje → **System** → **External System Import** → **CSV**.
2. Elegir el Space `NLOS` existente como destino, subir `jira_import.csv`.
3. En la pantalla de mapeo, estas columnas van tal cual (incluido el formato de fecha `yyyy-MM-dd`):

   | Columna del CSV | Campo de Jira |
   |---|---|
   | `Issue ID` | **Issue ID** (campo especial del importador) |
   | `Parent` | **Parent** |
   | `Issue Type` | Issue Type |
   | `Summary` | Summary |
   | `Description` | Description |
   | `Priority` | Priority |
   | `Story Points` | Story point estimate |
   | `Sprint` | Sprint |
   | `Start date` | Start date |
   | `Due date` | Due date |
   | `Labels` | Labels |

4. Revisar el preview (Jira arma un resumen antes de confirmar) y lanzar la importación.

Es un único archivo, una sola pasada: el par `Issue ID`/`Parent` le dice a Jira qué fila es hija de cuál, y Jira resuelve sola si esa relación es el padre de una Epic o el padre de una Subtask, según el tipo de cada fila.

### Opción B: si no conseguís que un admin lo corra

Si no hay nadie con ese permiso disponible, se puede cargar todo a mano con el importador que sí tenés (**Import work items from CSV**), en 3 tandas, fijando el Parent de cada issue manualmente después de crearlo (ese importador no arma jerarquías, y Jira Cloud tampoco permite reasignar el Parent de muchos issues a la vez en un Space team-managed):

1. Creá primero las 5 épicas a mano (son pocas, no vale la pena por CSV): `Create` → Epic, usando los Summary y fechas de las primeras 5 filas de `jira_import.csv`.
2. Importá las 10 Stories con **Import work items from CSV** (filtrando el CSV a esas filas), sin la columna Parent. Después abrí cada una y asignale su épica a mano en el campo Parent (son 10).
3. Importá las 86 Subtasks/Tasks de la misma forma, sin Parent. Después asignale a cada una su Story o la épica E5 a mano (son 86 — tedioso, pero cada una es un solo clic en un desplegable).

Esta opción no necesita admin, pero es mucho más lenta. Avisame si llegás a necesitarla y te preparo los 3 CSV filtrados (sin la columna Parent, lista para este importador).

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

### Cómo se maneja el "cuándo"

El sprint es la referencia de cuándo se hace cada cosa, no una fecha fija por ítem:

- **Stories, Subtasks y Tasks de los sprints 0 y 11**: sin Start date ni Due date. Si algo se atrasa, al cerrar el sprint Jira ofrece mover lo pendiente al siguiente, sin fechas que corregir a mano. Cada Subtask guarda en la descripción el sprint en que estaba planificada (`Planned effort: 8 h (Sprint 7)`).
- **Epics**: con Start date y Due date (desde el inicio de su primer sprint hasta el fin del último), para que el Timeline muestre las 5 barras del plan. Si el cronograma se corre, se ajustan arrastrando la barra en el Timeline.
- **Tasks sin sprint** (label `cross-cutting`): las reuniones de seguimiento abarcan todo el proyecto, y el informe de avance vence el 2027-07-12, antes del inicio del TTFA. Son las únicas tareas con fechas, porque no tienen sprint que les dé un vencimiento.

### Labels

- `optional`: en HU10, la única historia opcional del backlog (sección 6 del documento).
- `ttfa` / `ttfb`: en las 8 tareas de redacción de la memoria y defensa del Sprint 11, para poder filtrarlas por separado aunque compartan sprint.
- `cross-cutting`: en las 2 tareas sin sprint (reuniones de seguimiento, informe de avance).

La línea base original, para comparar lo planificado con lo real, queda en el documento del plan y en `sprint_dates.csv`.

## 4. Checklist de verificación

Después de importar, confirmá:

- [ ] 5 épicas: E1 a E4 (el backlog real) + E5 (gestión/cierre, no es backlog).
- [ ] 10 historias de usuario, Story Points sumando **89** en total (HU1=5, HU2=5, HU3=8, HU4=8, HU5=8, HU6=13, HU7=13, HU8=13, HU9=8, HU10=8).
- [ ] 86 tareas (sub-tareas bajo las HU + tareas sueltas bajo E5), cada una con su esfuerzo planificado en la descripción (`Planned effort: 8 h`), que en total suman **600 h**.
- [ ] Las 5 épicas con Start date y Due date; la vista Timeline va de 2026-08-25 a 2027-11-15.
- [ ] Cada Story en su sprint (HU6 en el Sprint 6), con sus Subtasks adentro.
- [ ] HU10 marcada como prioridad Low/opcional, bajo la épica E4.
- [ ] Cada HU tiene al menos 3 criterios de aceptación en su descripción (ya vienen cargados desde la sección 7 del documento, traducidos al inglés).
- [ ] 12 sprints visibles en el Backlog con las fechas de la tabla anterior.

## 5. Para más adelante: Atlassian MCP

Si querés que en futuras conversaciones yo pueda leer el estado del tablero, actualizar el % de avance de las tareas, o crear nuevos issues directamente (por ejemplo, al cerrar cada sprint real):

1. En una sesión **interactiva** de Claude Code (no en este modo), corré `/mcp`.
2. Autorizá el conector `plugin:product-management:atlassian` contra tu cuenta corporativa (tu administrador de Jira debe permitir apps/conectores OAuth de terceros — si no podés autorizarlo vos mismo, es por política de la organización).
3. En la próxima conversación yo podré usar ese conector sobre el Space que ya creaste con esta guía.
