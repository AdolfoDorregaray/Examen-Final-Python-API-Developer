# Examen Final - Python API Developer

## III. PARTE TEÓRICA

1. **Si te piden desarrollar una aplicación muy pequeña que solo debe saludar al usuario y no necesita base de datos ni panel de administración, ¿por qué elegir Flask en lugar de Django sería una decisión más inteligente? Argumenta basándote en la simplicidad del código inicial.** ... "Elegir Flask es más inteligente porque es un micro-framework. Mientras que Django crea una estructura pesada con archivos que no usaríamos (admin, auth, settings complejos), Flask permite crear un saludo con apenas 5 líneas de código en un solo archivo. Menos código significa menor consumo de recursos y mayor velocidad de despliegue para tareas simples."
2. **Imagina que el menú de un restaurante es una API. El cliente (Client) pide un plato al mesero (Interface) y la cocina (Server) lo prepara. Siguiendo esta analogía, ¿por qué el cliente no entra directamente a la cocina a cocinar su comida? Relaciona tu respuesta con la seguridad y el orden en el intercambio de datos en una API.** ... "El cliente no entra a la cocina porque el mesero (API) actúa como una capa de abstracción y seguridad. Si el cliente entra, podría causar desorden, ver recetas secretas o manipular ingredientes indebidamente. En una API, esto evita que el usuario acceda directamente a la base de datos, garantizando que solo se entreguen los datos permitidos bajo reglas estrictas."
3. **Imagina que REST es como hacer una llamada telefónica para preguntar algo y colgar, mientras que WebSockets es dejar la llamada abierta todo el día para hablar en cualquier momento. ¿En qué situación de una aplicación real (ejemplo: un banco o un juego online) crees que es mejor dejar la 'llamada abierta' y por qué?** ... "Para un juego online, es mejor dejar la 'llamada abierta' (WebSockets). En un juego, la posición de los jugadores cambia cada milisegundo; si usáramos REST, el dispositivo tendría que preguntar '¿dónde están los demás?' miles de veces por minuto, saturando el servidor. Con WebSockets, el servidor empuja la información en tiempo real apenas ocurre un cambio."

## IV. EVIDENCIAS (Capturas de Postman)
GET /estudiantes: Devolver la lista completa de alumnos.
![Lista General](https://github.com/user-attachments/assets/267a0dce-2b91-4ffc-9f72-44b415076bbe)

GET /estudiantes/<id>: Devolver la información de un estudiante por su ID.
![Detalle Individual](https://github.com/user-attachments/assets/5f800ee6-f3a2-41e5-b0df-ecc55fbcbfe0)

POST /estudiantes: Crear un nuevo registro de estudiante.
![Nuevo Registro](https://github.com/user-attachments/assets/df22d155-48c4-4126-b794-d98727e274cd)
![Lista Actualizada](https://github.com/user-attachments/assets/fda202b0-2a5b-404e-b288-475aa6232d6b)

PUT /estudiantes/<id>: Actualizar la información de un estudiante existente.
![Actualizar Datos](https://github.com/user-attachments/assets/90da183c-4585-4363-bd94-51fda8751324)
![Lista Actualizada 3](https://github.com/user-attachments/assets/05491a00-c4ff-430a-8d91-136a70f8c314)

DELETE /estudiantes/<id>: Eliminar un estudiante de la base de datos.
![Eliminar Registro](https://github.com/user-attachments/assets/3690e42c-7eb0-4f24-9cde-45b249f75226)
![Lista Actualizada 2](https://github.com/user-attachments/assets/42514c3d-f42f-4dee-ac49-379122e6387f)

GET/estudiantes/buscar por nombre y apellido (Debe ser insensible a mayúsculas/minúsculas).
![Búsqueda](https://github.com/user-attachments/assets/274a7fde-487f-4311-b641-4a598560110c)

GET/estudiantes/filtrar por los alumnos que aprobaron.
![Visualizar Aprobados](https://github.com/user-attachments/assets/0e50266d-c967-4852-a986-e47fa5bbf049)
