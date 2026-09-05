# 6\. Product Backlog [Ejemplos de secciones 6 y 7](https://docs.google.com/document/d/1MAFFBYM7f6k-g1Y6h7f4p1EyhNIhBa7qE5Zeu-yYHtk/edit?tab=t.0)

El Product Backlog debe organizarse en torno a cuatro épicas principales del proyecto, entendidas como bloques funcionales relevantes. Cada épica debe contener al menos dos historias de usuario (HU). Esta sección reemplaza a la tradicional de “Requerimientos” y tiene carácter orientador para la planificación de entregas.

Las historias de usuario deben especificarse siguiendo el formato:  
“Como \[rol\], quiero \[necesidad\] para \[finalidad\]”.

Deben:

* Ser breves, claras y sin ambigüedades.  
* Representar funcionalidades concretas del sistema desde la perspectiva del usuario.  
* Incluir una prioridad clara y si corresponde, marcar si alguna HU es opcional.  
* Cada historia debe ser acompañada por su asignación de Story Points, calculados en base a:

* Dificultad: cantidad de trabajo involucrado.  
* Complejidad: nivel técnico o sofisticación.  
* Incertidumbre: nivel de riesgo o novedad.

La suma de estos valores se redondea hacia el número superior más cercano de la serie de Fibonacci: 1, 2, 3, 5, 8, 13, 21, 34...

Ejemplo: si una historia suma 9 puntos → se asignan 13 Story Points.

Los Story Points no deben equipararse a horas de trabajo. Deben reflejar la carga relativa de la HU respecto de otras.

7\. Criterios de aceptación

Esta sección reemplaza a la sección tradicional de “Historias de usuario”. Aquí se detallan los criterios de aceptación de las historias definidas en el Product Backlog.

Los criterios de aceptación indican claramente cuándo una historia puede considerarse terminada. Deben ser:

* Objetivos, verificables y medibles.  
* Claramente relacionados con la HU correspondiente.  
* Cada HU debe contar con al menos tres criterios de aceptación, que pueden abarcar:

* Funcionalidad esperada.  
* Comportamiento visual/interfaz.  
* Validación técnica o normativa.

Se recomienda redactarlos como condiciones simples, sin ambigüedad, que permitan a cualquier evaluador confirmar si la historia fue efectivamente resuelta.

Sugerencias de corrección:

* Verificar que todas las HU estén bien redactadas y representen funcionalidades clave.  
* Evaluar que las épicas estén claramente diferenciadas y cubran áreas fundamentales del proyecto.  
* Controlar que los Story Points estén asignados según el criterio establecido.  
* Confirmar que los criterios de aceptación permitan evaluar de manera clara y objetiva cada HU.  
* Verificar si el alumno descompuso correctamente cada historia de usuario (HU) en tareas técnicas concretas, claras y estimables.

8\. Fases de CRISP-DM  
[Ejemplos sección 8](https://docs.google.com/document/d/1OJbJduw1h5YJNUCtxDRDnlq3TmF6HsZ4qzkahumXTzk/edit?tab=t.0)

CRISP-DM es una metodología orientada a proyectos de minería de datos que se basa en 6 fases bien definidas y secuenciales:

1. Comprensión del negocio: se debe definir el objetivo que se persigue con la implementación del producto o servicio que utiliza IA. Además, se debe definir el impacto que generaría y, en lo posible, también definir una “métrica de éxito” que ayude a medir este impacto.  
     
2. Comprensión de los datos: se debe definir con qué tipo de datos se va a trabajar (tabulares, imágenes, sonido, texto, etc.) y cuáles son las fuentes (sensores, cámaras web, registros, etc.). En lo posible, también estimar la cantidad de datos (cantidad de imágenes, filas, archivos de texto). Se considera como un plus comentarios acerca de la calidad de los datos (equipos descalibrados, sensores que fallan, filas con valores nulos, etc.).  
     
3. Preparación de los datos: esta es la sección más complicada a definir ya que se deben conocer muy bien los datos para saber qué tratamiento darle al dataset. Se pueden mencionar técnicas como normalización, eliminación o imputación de valores faltantes, transformaciones, etc. La definición de cada técnica debería estar acompañada de una breve justificación.  
     
4. Modelado: se debe explicitar el tipo de problema a abordar (clasificación, regresión, predicción, detección de anomalías, etc.). Se pueden mencionar algoritmos de machine learning o arquitecturas de deep learning que podrían utilizarse.  
     
5. Evaluación del modelo: se deben mencionar las posibles métricas a utilizar para evaluar el desempeño del modelo (f1-score si es un problema de clasificación, MSE si es un problema de regresión, etc.).   
     
6. Despliegue del modelo: esta fase es completamente opcional. En caso de completarse, se debería definir la estrategia de puesta en producción del modelo (online, local, mediante una API, en batch, etc.) y las herramientas a utilizar (Docker, AWS, Azure, Google Cloud, etc.).

9\. Desglose de trabajo en tareas a partir de las Historias de usuario

[Ejemplos secciones 9, 10, 11 y 12](https://docs.google.com/document/d/1asxDz4DFfGr3TMd47Mbd4tVQjEnyeVxZsaWXEEufPxI/edit?tab=t.0)

**Criterios a evaluar:**

* Que cada HU tenga al menos **dos tareas** claramente asociadas.  
* Que las tareas estén redactadas con **verbos de acción**, sean específicas y medibles.  
* Que las tareas reflejan una **implementación técnica realista**.  
* Que cada tarea incluya **una estimación horaria (2 a 8 h)** y una **prioridad asignada**.  
* Si alguna HU incluye tareas no técnicas (documentación, pruebas, entrega), estas estén bien justificadas.  
* No deben incluirse tareas genéricas como “implementar HU”.

10\. Diagrama de Gantt del proyecto (a partir del Product Backlog y otras tareas)

**Criterios a evaluar:**

* Que el Gantt incluya tareas tanto **técnicas** (HU) como **no técnicas** (planificación, escritura, defensa, etc.).  
* Que las tareas están **ordenadas cronológicamente**.  
* Que el eje vertical muestre claramente las tareas y el eje horizontal representa **fechas o semanas**.  
* Que el cronograma abarque **desde el inicio de la asignatura Gestión de Proyectos hasta la defensa**.  
* Que se utilicen **colores diferenciados** para distinguir tipos de tareas (opcional pero recomendable).  
* Que el cronograma sea **realista** y contemple las **600 horas de trabajo**, distribuidas entre:  
  	480–500 h para actividades técnicas.  
  	100–120 h para actividades generales (planificación, memoria, defensa).

### 11\. Planificación de Sprints

**Criterios a evaluar:**

* Que la planificación esté estructurada por **sprints (Sprint 0, Sprint 1, etc.)**. Se recomendaron de 10 a 12 sprints.  
* Que cada sprint tenga una duración razonable (**1 a 3 semanas**).  
* Que las tareas estén claramente asociadas a las HU o fases del proyecto.  
* Que se indique la **estimación en horas por tarea**, el **responsable** y un campo de **% de avance**.  
* Que incluya sprints específicos para tareas como:  
  	Reuniones iniciales / planificación.  
  	Redacción de la memoria técnica.  
  	Preparación de entregables y defensa.  
* Que la planificación total sume aproximadamente **600 horas**, distribuidas de forma coherente.

### 12\. Normativa y cumplimiento de datos (gobernanza)

**Criterios a evaluar:**

* Que se hayan enumerado las normativas aplicables al proyecto. Por ejemplo:  
    
  * Si se trata de un proyecto del rubro médico, es altamente probable que deban aplicarse las normas [HIPAA](https://www.safetica.com/es/recursos/blogs/que-es-hipaa-el-alcance-proposito-y-como-cumplir) o la [Ley 26.529 de Derechos del Paciente en su Relación con los Profesionales e Instituciones de la Salud](https://www.argentina.gob.ar/normativa/nacional/ley-26529-160432/texto) en Argentina.  
  * Si se trabajan con datos personales, es altamente probable que deban aplicarse las normas [GDPR](https://es.wikipedia.org/wiki/Reglamento_General_de_Protecci%C3%B3n_de_Datos) o la [Ley 25.326 de Protección de Datos Personales](https://www.argentina.gob.ar/sites/default/files/arg_ley25326.pdf) en Argentina.  
  * Si se trabajan con datos protegidos por derechos de autor, es altamente probable que deban aplicarse las normas [WIPO Copyright Treaty (WCT)](https://www.wipo.int/treaties/en/ip/wct/)  o la [Ley 11.723 de Propiedad Intelectual](https://servicios.infoleg.gob.ar/infolegInternet/anexos/40000-44999/42755/texact.htm) en Argentina.  
  * Si se trabajan con datos financieros, es posible que deban aplicarse las normas [PCI DSS](https://es.wikipedia.org/wiki/PCI_DSS) o la [Comunicación A 6354 del Banco Central de la República Argentina](https://www.bcra.gob.ar/Pdfs/comytexord/A6354.pdf) en Argentina.


* Es posible que el proyecto no esté obligado a cumplir ninguna norma. En este caso, se debe explicitar y argumentar de manera razonable.  
* El alumno también debe explicitar si el dataset a utilizar está licenciado, si es de libre disponibilidad o si existen restricciones para su uso. Por ejemplo:  
    
  * Una licencia muy común es la [MIT](https://mit-license.org/). Esta licencia es de las más libres en cuanto a permisividad de uso.  
  * La licencia [CC BY-NC](https://creativecommons.org/licenses/by-nc/4.0/) permite el uso de los datos únicamente para fines no comerciales.  
  * Es posible que, si el proyecto es impulsado por una empresa, los datos sean confidenciales. Esto debe mencionarse.

### 13\. Sigue igual que la plantilla original

### 14\. Sprint Review

[Ejemplos secciones 14 y 15](https://docs.google.com/document/d/1oPDbhEwklamtySZMiYT-OlSSrk5qYXTIA5u1ks8vpYo/edit?tab=t.0)

**Pautas para la corrección:**

* Se deben presentar al menos 4 revisiones de sprint técnico. No deben incluirse tareas no técnicas en esta sección.  
* En cada revisión debe indicarse la historia de usuario asociada y las tareas relacionadas.  
* Debe indicarse cómo se sabrá si la historia está cumplida (por ejemplo, mediante pruebas, visualizaciones, outputs validados, etc).  
* Deben incluirse observaciones o riesgos si corresponde

### 15\. Sprint Retrospective

Confirmar que se haya aplicado el formato sugerido (estrella de la retrospectiva), incluyendo los siguientes cinco ejes:

* ¿Qué hacer más?  
* ¿Qué hacer menos?  
* ¿Qué mantener?  
* ¿Qué empezar a hacer?  
* ¿Qué dejar de hacer?

* Comprobar que haya al menos una retrospectiva de un sprint no técnico (por ejemplo, defensa, escritura de memoria o reuniones con el cliente).  
* Verificar que estén desarrolladas al menos tres retrospectivas técnicas distintas, con tareas específicas y no repetidas entre sí.  
* Evaluar si las reflexiones presentadas son pertinentes, realistas y evidencian una comprensión del proceso de mejora continua.  
  