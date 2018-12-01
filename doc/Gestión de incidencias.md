# Gestión de incidencias
## Formato de incidencias
Existen incidencias de dos tipos, utilizando para ambas la plantilla estándar que ofrece Github:
* **Feature request:** petición de una característica para añadir al proyecto.
* **Bug report:** informe de un error detectado durante el desarrollo del proyecto.

Se pueden omitir campos de la plantilla si se considera necesario siempre que la descripción siga siendo correcta.

**Ejemplo:**
```
Titulo: "Feature request: ley d'Hondt"

**Is your feature request related to a problem? Please describe.**
Implementación de la ley d'Hondt para los tipos de votación que lo permitan.

**Describe the solution you'd like**
Es necesaria una solución con un formato limpio y un rendimiento aceptable.
```
## Apertura de incidencias
Se considerará aceptable crear una incidencia en los siguientes casos:
* Antes de empezar el desarrollo, cuando se quiere especificar una característica general del proyecto. Estas características tienen una rama asignada y se deciden por consenso.
* Cuando se encuentra un fallo en tu rama relacionado con la parte de implementación de otra rama.
* Cuando se encuentra un fallo en la rama master.
## Asignación de incidencias
Las incidencias de características se asignarán por consenso al comienzo del proyecto antes de empezar la construcción del código. Por otro lado, las incidencias relativas a fallos se le asignarán al encargado de la funcionalidad más cercana a la semántica del fallo. En el caso de que ningún colaborador tenga una funcionalidad asignada cercana al fallo se asignará de manera arbitraria por consenso.   
## Cierre de incidencias
La incidencia se considera cerrada cuando existe un commit en el que se especifica explícitamente que la incidencia queda solucionada y el que la abrió y un tercero (cualquier colaborador del proyecto) están de acuerdo.
