# 📝 Gestor de Notas API

API REST desarrollada con Flask y SQLite para gestionar notas de forma eficiente.

---

## 🚀 Características

* Crear, leer, editar y eliminar notas (CRUD)
* Filtrar por estado (completadas / no completadas)
* Búsqueda por texto en título y contenido
* Paginación de resultados
* Orden dinámico por diferentes campos

---

## 🧱 Tecnologías utilizadas

* Python
* Flask
* SQLite

---

## ⚙️ Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/Lev-w/gestor-tareas-sqlite
cd gestor-tareas-sqlite
```

2. Crear entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```bash
python run.py
```

---

## 📌 Endpoints principales

### 🔹 Obtener notas

```http
GET /notas
```

### 🔹 Filtros y búsqueda

```http
GET /notas?completadas=true
GET /notas?buscar=python
GET /notas?completadas=false&buscar=api
```

---

### 🔹 Paginación

```http
GET /notas?page=1&limit=5
```

---

### 🔹 Orden dinámico

```http
GET /notas?orden=titulo
GET /notas?orden=fecha_creacion
```

---

### 🔹 Crear nota

```http
POST /notas
```

Body JSON:

```json
{
  "titulo": "Mi nota",
  "contenido": "Contenido de ejemplo"
}
```

---

### 🔹 Editar nota

```http
PUT /notas/<id>
```

---

### 🔹 Eliminar nota

```http
DELETE /notas/<id>
```

---

## 📦 Estructura del proyecto

```
app/
├── __init__.py
├── routes.py
├── services.py
├── db.py

run.py
```

---

## 🧠 Aprendizajes

Este proyecto incluye conceptos clave de backend:

* Arquitectura por capas (routes, services, db)
* Manejo de bases de datos con SQLite
* Construcción de queries dinámicas
* Validación de parámetros en APIs
* Paginación y filtrado de datos

---
