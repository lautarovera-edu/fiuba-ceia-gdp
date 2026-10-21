# Guía: conectar el repositorio de código y un espacio de Confluence al Space NLOS

Requisito previo: el Space `NLOS` ya está creado (ver `GUIA_IMPORTACION_JIRA.md`).

## 1. Crear el repositorio en la organización de MobileKnowledge

El scaffold ya existe localmente en `/home/lautaro/ceia/4b2026/trabajo-final/nlos-uwb-detection`
(rama `main`, todavía sin commits). Contiene una carpeta por épica del backlog
y un README con la convención para enlazar commits a Jira.

1. En GitHub, dentro de la organización de MobileKnowledge, creá un repositorio
   **privado** y **vacío** (sin README, sin `.gitignore`, sin licencia, para que
   no choque con el scaffold). Nombre sugerido: `nlos-uwb-detection`.
2. Hacé el primer commit y el push:

   ```bash
   cd /home/lautaro/ceia/4b2026/trabajo-final/nlos-uwb-detection
   git add .
   git commit -m "chore: add repository scaffold"
   git remote add origin git@github.com:<org-mobileknowledge>/nlos-uwb-detection.git
   git push -u origin main
   ```

   Si tu clave SSH personal no tiene acceso a la organización, usá la URL HTTPS
   o la clave que usás para los repos de la empresa.

## 2. Conectar GitHub con Jira (app "GitHub for Jira")

Se necesitan dos permisos que probablemente no tengas vos: **administrador del
sitio Jira** para instalar la app, y **owner de la organización de GitHub**
para autorizarla. Primero revisá si la empresa ya la tiene instalada:

- En el Space `NLOS`, abrí la vista **Development**. Si te ofrece conectar
  GitHub o ya muestra repositorios, la app está instalada.

Si ya está instalada:

1. Jira → **Apps** → **Manage your apps** → **GitHub for Jira** → **Configure**.
2. En la organización de MobileKnowledge, si el acceso es a repositorios
   seleccionados, agregá `nlos-uwb-detection`. Los repositorios nuevos **no** se
   agregan solos cuando la conexión está en "Only select repositories".

Si no está instalada, pedíselo al administrador de Jira y al owner de la
organización de GitHub: instalar **GitHub for Jira** (de Atlassian) desde
Atlassian Marketplace, conectar la organización y dar acceso al repositorio.

**Cómo verificarlo:** creá una rama `NLOS-1-test` y pusheala. En unos minutos
tiene que aparecer en el panel **Development** del ticket `NLOS-1`. Después
borrá la rama.

A partir de ahí, cualquier rama, commit o título de PR que contenga una clave
(`NLOS-12`) queda enlazado al ticket. La convención está en el README del repo.

## 3. Crear el espacio de Confluence

Confluence es un producto aparte. Tiene que estar habilitado en el mismo sitio
de Atlassian de la empresa (lo ves en el selector de apps, arriba a la izquierda).

1. Confluence → **Spaces** → **Create space** → plantilla en blanco (o
   **Documentation** si querés páginas de ejemplo).
2. Nombre: `NLoS Detection (UWB)`. Clave: `NLOS` (si está tomada, `NLOSUWB`).
3. Dejalo vacío o creá solo estas páginas raíz como esqueleto:
   - `Design decisions`
   - `Experiments log`
   - `Model datasheet` (entregable de HU9)
   - `Firmware integration guide` (entregable de HU8)
   - `Meeting notes` (las 6 reuniones de seguimiento)

Crear espacios puede requerir el permiso **Create space** de Confluence. Si no
lo tenés, se lo pedís al administrador.

## 4. Vincular Confluence con el Space de Jira

1. En el Space `NLOS` de Jira, abrí la vista **Docs** (aparecía en la lista de
   vistas al crear el Space).
2. Elegí **Connect** / **Link a space** y seleccioná el espacio de Confluence
   recién creado.
3. Las páginas del espacio quedan visibles desde la pestaña Docs de Jira, y
   podés enlazar páginas puntuales a una épica desde el propio ticket.

Atlassian avisa que esta parte de la interfaz se está actualizando, así que
los nombres de los botones pueden variar un poco.

Finalmente, agregá la URL del espacio de Confluence en `docs/README.md` del
repositorio de código.
