import requests
import time

BASE  = "http://localhost:8000"
EMAIL = f"test_{int(time.time())}@fitness.com"  # único por ejecución

VERDE = "\033[92m"
ROJO  = "\033[91m"
RESET = "\033[0m"
BOLD  = "\033[1m"

def body(r):
    try:
        return r.json()
    except Exception:
        return r.text or f"<sin cuerpo, status={r.status_code}>"

def ok(label, r, esperado=200):
    paso    = r.status_code == esperado
    simbolo = f"{VERDE}✓{RESET}" if paso else f"{ROJO}✗{RESET}"
    estado  = f"{VERDE}{r.status_code}{RESET}" if paso else f"{ROJO}{r.status_code}{RESET}"
    print(f"  {simbolo} {label:<45} {estado}  {body(r)}")

def seccion(nombre):
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}  {nombre}{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

# ── Raíz ──────────────────────────────────────────────────────
seccion("RAÍZ")
ok("GET /", requests.get(f"{BASE}/"))

# ── Auth ──────────────────────────────────────────────────────
seccion("AUTH")
r = requests.post(f"{BASE}/api/register", json={
    "nombre": "Usuario Test",
    "email": EMAIL,
    "password": "password123"
})
ok("POST /api/register  (nuevo usuario)", r)

r = requests.post(f"{BASE}/api/register", json={
    "nombre": "Usuario Test",
    "email": EMAIL,
    "password": "password123"
})
ok("POST /api/register  (email duplicado → 400)", r, esperado=400)

r = requests.post(f"{BASE}/api/login", json={"email": EMAIL, "password": "password123"})
ok("POST /api/login     (credenciales OK)", r)
login_data  = r.json()
TOKEN       = login_data["access_token"]
USUARIO_ID  = login_data["usuario"]["id"]

r = requests.post(f"{BASE}/api/login", json={"email": EMAIL, "password": "mal_password"})
ok("POST /api/login     (clave incorrecta → 401)", r, esperado=401)

# ── Deportes ──────────────────────────────────────────────────
seccion("DEPORTES")
r = requests.post(f"{BASE}/api/deportes/", json={"nombre": "Gym", "icono": "💪"})
ok("POST /api/deportes/  (Gym)", r)
GYM_ID = r.json()["id"]

r = requests.post(f"{BASE}/api/deportes/", json={"nombre": "Natación", "icono": "🏊"})
ok("POST /api/deportes/  (Natación)", r)
NATACION_ID = r.json()["id"]

r = requests.get(f"{BASE}/api/deportes/")
ok("GET  /api/deportes/", r)

r = requests.get(f"{BASE}/api/deportes/{GYM_ID}")
ok(f"GET  /api/deportes/{GYM_ID}", r)

r = requests.put(f"{BASE}/api/deportes/{GYM_ID}", json={"nombre": "Gimnasio", "icono": "🏋️"})
ok(f"PUT  /api/deportes/{GYM_ID}", r)

r = requests.get(f"{BASE}/api/deportes/9999")
ok("GET  /api/deportes/9999  (no existe → 404)", r, esperado=404)

# ── Ejercicios ────────────────────────────────────────────────
seccion("EJERCICIOS")
r = requests.post(f"{BASE}/api/ejercicios/", json={
    "nombre": "Press de banca",
    "grupo_muscular": "Pecho",
    "descripcion": "Empuje horizontal con barra",
    "deporte_id": GYM_ID
})
ok("POST /api/ejercicios/  (Press banca)", r)
EJ_ID = r.json()["id"]

r = requests.post(f"{BASE}/api/ejercicios/", json={
    "nombre": "Sentadilla",
    "grupo_muscular": "Piernas",
    "descripcion": "Movimiento de empuje con piernas",
    "deporte_id": GYM_ID
})
ok("POST /api/ejercicios/  (Sentadilla)", r)

r = requests.get(f"{BASE}/api/ejercicios/")
ok("GET  /api/ejercicios/", r)

r = requests.get(f"{BASE}/api/ejercicios/deporte/{GYM_ID}")
ok(f"GET  /api/ejercicios/deporte/{GYM_ID}", r)

r = requests.put(f"{BASE}/api/ejercicios/{EJ_ID}", json={
    "nombre": "Press de banca con barra",
    "grupo_muscular": "Pecho",
    "descripcion": "Empuje horizontal con barra olímpica",
    "deporte_id": GYM_ID
})
ok(f"PUT  /api/ejercicios/{EJ_ID}", r)

# ── Rutinas ───────────────────────────────────────────────────
seccion("RUTINAS")
r = requests.post(f"{BASE}/api/rutinas/", params={"usuario_id": USUARIO_ID}, json={
    "nombre": "Rutina Pecho y Tríceps",
    "descripcion": "Entrenamiento de empuje",
    "deporte_id": GYM_ID
})
ok("POST /api/rutinas/", r)
RUTINA_ID = r.json()["id"]

r = requests.get(f"{BASE}/api/rutinas/")
ok("GET  /api/rutinas/", r)

r = requests.get(f"{BASE}/api/rutinas/{RUTINA_ID}")
ok(f"GET  /api/rutinas/{RUTINA_ID}", r)

r = requests.put(f"{BASE}/api/rutinas/{RUTINA_ID}", json={
    "nombre": "Rutina Pecho, Hombro y Tríceps",
    "descripcion": "Entrenamiento de empuje completo",
    "deporte_id": GYM_ID
})
ok(f"PUT  /api/rutinas/{RUTINA_ID}", r)

# ── Sesiones ──────────────────────────────────────────────────
seccion("SESIONES")
r = requests.post(f"{BASE}/api/sesiones/", params={"usuario_id": USUARIO_ID}, json={
    "duracion": 60,
    "notas": "Buena sesión, aumenté peso",
    "rutina_id": RUTINA_ID
})
ok("POST /api/sesiones/", r)
SESION_ID = r.json()["id"]

r = requests.get(f"{BASE}/api/sesiones/")
ok("GET  /api/sesiones/", r)

r = requests.get(f"{BASE}/api/sesiones/{SESION_ID}")
ok(f"GET  /api/sesiones/{SESION_ID}", r)

r = requests.put(f"{BASE}/api/sesiones/{SESION_ID}", json={
    "duracion": 75,
    "notas": "Actualizado: muy buena sesión",
    "rutina_id": RUTINA_ID
})
ok(f"PUT  /api/sesiones/{SESION_ID}", r)

# ── DELETE (respetando FK: sesión → rutina → ejercicio → deporte)
seccion("DELETE")
r = requests.delete(f"{BASE}/api/sesiones/{SESION_ID}")
ok(f"DELETE /api/sesiones/{SESION_ID}", r)

r = requests.delete(f"{BASE}/api/rutinas/{RUTINA_ID}")
ok(f"DELETE /api/rutinas/{RUTINA_ID}", r)

r = requests.delete(f"{BASE}/api/ejercicios/{EJ_ID}")
ok(f"DELETE /api/ejercicios/{EJ_ID}", r)

r = requests.delete(f"{BASE}/api/deportes/{GYM_ID}")
ok(f"DELETE /api/deportes/{GYM_ID}", r)

r = requests.delete(f"{BASE}/api/deportes/{NATACION_ID}")
ok(f"DELETE /api/deportes/{NATACION_ID}", r)

r = requests.delete(f"{BASE}/api/deportes/9999")
ok("DELETE /api/deportes/9999  (no existe → 404)", r, esperado=404)

# ── Resumen ───────────────────────────────────────────────────
print(f"\n{BOLD}{'─'*60}{RESET}")
print(f"  Usuario de prueba: {EMAIL}")
print(f"{BOLD}{'─'*60}{RESET}\n")
