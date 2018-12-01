# Gestión de código
## Gestión de repositorio
### Finalidad del repositorio
Decide-Europa-Postproc es un fork del repositorio Decide-Europa que tiene como finalidad principal desarrollar un incremento de funcionalidad sobre el subsistema de postprocesado. Para esto será necesario hacer una selección personal de funcionalidades y coordinarse con el resto de grupos.
### Pull requests
Los pull requests se harán sobre el repositorio una vez se hayan completado y comprobado todas los incrementos que se querían realizar y se encuentren sobre la rama master.
## Gestión de ramas
### Creación de ramas
En este repositorio se crearán ramas por funcionalidad, pudiendo estas ser subdivididas en el caso de que sea necesaria mayor granularidad. Cada una de estas ramas estará asignada principalmente a uno de los colaboradores del proyecto, aunque podría darse el caso de que una funcionalidad concreta estuviese asignada a varios colaboradores debido a su complejidad.

Toda rama que se cree en este repositorio deberá ser con el consentimiento de todo el equipo de proyecto, habiéndose decidido previamente que la funcionalidad es suficiente como para subdividirse.
### Cierre de ramas
En este repositorio se cerrará una rama cuando se considere por consenso que una funcionalidad está completamente implementada y probada. El encargado de hacer el merge con master es el jefe de proyecto, previa integración con la rama realizada por el encargado de la funcionalidad.

Toda rama que se cierre en este repositorio deberá ser con el consentimiento de todo el equipo de proyecto, habiendo validado todos los colaboradores que no existen conflictos que no se puedan arreglar.
## Gestión de commits
### Formato de los commits
El formato utilizado en los mensajes de los commits será una versión simplificada de los utilizados en Karma-Runner 3.0:
```
<type>: <subject> [; <issue>]

<body>
```
Siendo cada uno de estos campos:
* **Type:** grupo de cambios al que pertenece el commit. Puede ser de varios tipos:
  - **Fix:** corrección de un error.
  - **Feature:** nueva funcionalidad en el sistema.
  - **Doc:** cambios en la documentación.
  - **Refactor:** refactorización de código.
  - **Test:** creación o actualización de tests.
* **Subject:** asunto concreto del commit. Se debe utilizar el participio.
* **Issue:** campo opcional. Incidencia a la que hace referencia.
* **Body:** descripción del contenido del commit. Formato libre. Se debe utilizar la tercera persona en pretérito perfecto.

**Ejemplo:**
```
Feature: implementada ley d'Hondt; #124

Se ha implementado la ley d'Hondt en todos los tipos de votaciones que lo permitan.
```

### Semántica de los commits
Todos los commits deben afectar unicamente a una funcionalidad concreta de una rama en particular. Queda explícitamente prohibido hacer commit de una funcionalidad fuera de su rama correspondiente.
