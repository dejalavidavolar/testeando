# RA Signatures - GitHub Actions Edition

Genera firmas RetroAchievements automáticamente usando GitHub Actions + GitHub Pages.

## Setup

### 1. Crear secrets

En GitHub:

Settings → Secrets and variables → Actions

Agregar:

- RA_USERNAME
- RA_API_KEY

---

### 2. Editar usuarios

Modificar en app.py:

```python
USERS = [
    "TU_USUARIO"
]
```

Puedes agregar varios usuarios.

---

### 3. Activar GitHub Pages

Settings → Pages

Seleccionar:

- Deploy from branch
- main
- /(root)

---

### 4. Ejecutar workflow

Actions → Generate RA Signatures → Run workflow

---

## URLs finales

```text
https://TUUSUARIO.github.io/REPO/users/usuario.png
```

---

## Actualización automática

El workflow corre cada 30 minutos.

---

## Stack

- Python
- Pillow
- GitHub Actions
- GitHub Pages