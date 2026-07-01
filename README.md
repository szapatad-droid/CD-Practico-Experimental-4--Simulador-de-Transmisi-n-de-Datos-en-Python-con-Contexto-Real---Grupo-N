# Simulador de Transmisión de Datos en Python con Contexto Real

## Descripción

Este proyecto desarrolla un simulador interactivo de transmisión de datos basado en conceptos de Comunicación de Datos y el Modelo OSI. La aplicación permite visualizar el proceso completo de envío y recepción de información utilizando modulación ASK (Amplitude Shift Keying), detección de errores mediante bits de paridad y simulación de ruido en el canal de comunicación.

El sistema fue desarrollado en Python utilizando Tkinter para la interfaz gráfica y Matplotlib para la visualización de señales.

## Objetivos

* Simular la transmisión de datos digitales a través de un canal de comunicación.
* Representar gráficamente la conversión de datos digitales a señales analógicas.
* Aplicar conceptos del Modelo OSI.
* Implementar detección de errores mediante paridad.
* Analizar el efecto del ruido sobre la calidad de la transmisión.
* Relacionar la teoría con escenarios reales de comunicación.

## Tecnologías Utilizadas

* Python 3.x
* Tkinter
* NumPy
* Matplotlib

## Características Principales

### Modelo OSI

El simulador muestra el recorrido de los datos a través de las siguientes capas:

1. Aplicación
2. Presentación
3. Sesión
4. Transporte
5. Red
6. Enlace de Datos
7. Física

### Codificación y Transmisión

* Conversión de caracteres a código ASCII.
* Generación de tramas de 8 bits más un bit de paridad.
* Modulación ASK (Amplitude Shift Keying).
* Simulación de transmisión por canal físico.

### Detección de Errores

* Verificación mediante paridad par.
* Cálculo de tasa de error de bits (BER).
* Simulación de errores causados por ruido.

### Visualización Gráfica

El sistema muestra tres etapas de la comunicación:

1. Bits digitales transmitidos.
2. Señal analógica modulada (ASK).
3. Señal recibida y bits demodulados.

## Escenarios Reales Simulados

El proyecto relaciona la teoría con ejemplos reales como:

* WhatsApp mediante Wi-Fi.
* Netflix por fibra óptica.
* Llamadas celulares.
* Controles remotos infrarrojos.
* Transacciones bancarias en cajeros automáticos.

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
```

2. Ingresar al directorio:

```bash
cd TU-REPOSITORIO
```

3. Instalar dependencias:

```bash
pip install numpy matplotlib
```

4. Ejecutar el programa:

```bash
python "Practico Experimental 4 Simulador de Transmisión de Datos en Python con Contexto Real.py"
```

## Conceptos Implementados

* Comunicación de Datos
* Señales Digitales y Analógicas
* Modulación ASK
* Teorema de Nyquist
* Relación Señal/Ruido (SNR)
* Tasa de Error de Bits (BER)
* Modelo OSI
* Detección de Errores por Paridad

## Autor

Desarrollado como proyecto académico del GRUPO N para la asignatura de Comunicación de Datos.

Universidad Estatal de Milagro (UNEMI)

## 📄 Licencia

Este proyecto se distribuye con fines educativos y académicos.
