Proceso de las ZKP
=====================================
Para explicar las ZKP (pruebas de cero conocimiento) se utilizará una analogía con Bob y Alice dónde se explicará a profuncidad el funcionamiento del algoritmo que hemos implementado. En este ejemplo se plantea la existencia de una cueva circular en la que hay una puerta cerrada con llave. La prueba de cero conocimiento consiste en que Alice entra en la cueva mientras Bob espera fuera. Una vez Alice ha entrado en la cueva Bob se acerca a la bifurcación y grita una salida derecha o izquierda que deberá tomar Alice. Si Alice conoce el secreto (posee la llave) podrá salir siempre por la salida que indique Bob. De esta manera se Alice ha demostrado a Bob que conoce el secreto sin enseñar la llave.

Paso 1: Bob elige los siguientes 4 parametros
-------------------------------------------------
- Un primo P largo de tal forma que la descomposición de ese primo sea intratable
- Saca también un parámetro de seguridad T, de tal forma que P >= 2^t. Normalmente con t = 40 es una seguridad adecuada
- Bob establece una firma segura con un algortimo secreto de firma que es Firma(Bob) y un algoritmo de verificaión SHA2
- Una función segura de Hash para hashear el mensaje antes de firmarlo


Paso 2: Entrega del mensaje a Alicia
------------------------------------------
- Bob establece la identidad de Alice como el certificado de nacimiento o el pasaporte, y crea un String IDAlice
- Alicia elige un exponente random A. De tal forma que 0<=A<=P-2
- Alicia calcula V que es congrunte con el generador V=ALFA-A mod P
- Devuelve V a Bob
- Bob genera una firma (S = IDAlice, V). Y le da el certificado que es Cert=(IDAlice, V, S)


Paso 3: Verificación
-----------------------------
    - Alica elige un número random R en el mismo rango que A, y prueba que el máximo común divisor(R, P-1) = 1. Que es lo mismo que X               congruente con A^R mod P
    - Alice devuelve el certificado que ella crea CertAlice = (IDAlice, V, S)
    - Alice manda X a Bob
    - Bob verifica la firma de Alice y envia TRUE si lo es. Además, elige un número random E en el rango 1 < E < 2. Y se lo manda a Alice
    - Alicia calcula Y congruente con A*E+R mod P-1.
    - Alicia envía Y a Bob
    - Bob calcula Z congruente con ALFA^Y * V^E mod P
    - Bob acepta que es verdadero si Z = X
