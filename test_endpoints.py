import requests
import time

BASE  = "http://localhost:8000"
TS    = int(time.time())
EMAIL = f"test_{TS}@fitness.com"
EMAIL2 = f"test2_{TS}@fitness.com"

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
    print(f"  {simbolo} {label:<50} {estado}  {body(r)}")

def seccion(nombre):
    print(f"\n{BOLD}{'─'*60}{RESET}")
    print(f"{BOLD}  {nombre}{RESET}")
    print(f"{BOLD}{'─'*60}{RESET}")

def auth_headers(token):
    return {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

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
TOKEN      = r.json()["access_token"]
USUARIO_ID = r.json()["usuario"]["id"]
HEADERS    = auth_headers(TOKEN)

r = requests.post(f"{BASE}/api/login", json={"email": EMAIL, "password": "mal_password"})
ok("POST /api/login     (clave incorrecta → 401)", r, esperado=401)

# Registrar segundo usuario
r = requests.post(f"{BASE}/api/register", json={
    "nombre": "Usuario 2",
    "email": EMAIL2,
    "password": "password123"
})
ok("POST /api/register  (segundo usuario)", r)
r = requests.post(f"{BASE}/api/login", json={"email": EMAIL2, "password": "password123"})
ok("POST /api/login     (segundo usuario)", r)
TOKEN2   = r.json()["access_token"]
HEADERS2 = auth_headers(TOKEN2)

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

# Sin token → 401
r = requests.get(f"{BASE}/api/rutinas/")
ok("GET  /api/rutinas/  (sin token → 401)", r, esperado=401)

r = requests.post(f"{BASE}/api/rutinas/", headers=HEADERS, json={
    "nombre": "Rutina Pecho y Tríceps",
    "descripcion": "Entrenamiento de empuje",
    "deporte_id": GYM_ID
})
ok("POST /api/rutinas/  (usuario 1)", r)
RUTINA_ID = r.json()["id"]

r = requests.get(f"{BASE}/api/rutinas/", headers=HEADERS)
ok("GET  /api/rutinas/  (usuario 1 ve sus rutinas)", r)

r = requests.get(f"{BASE}/api/rutinas/{RUTINA_ID}", headers=HEADERS)
ok(f"GET  /api/rutinas/{RUTINA_ID}  (usuario 1)", r)

r = requests.put(f"{BASE}/api/rutinas/{RUTINA_ID}", headers=HEADERS, json={
    "nombre": "Rutina Pecho, Hombro y Tríceps",
    "descripcion": "Entrenamiento de empuje completo",
    "deporte_id": GYM_ID
})
ok(f"PUT  /api/rutinas/{RUTINA_ID}  (usuario 1)", r)

# Usuario 2 no puede ver ni modificar la rutina del usuario 1
r = requests.get(f"{BASE}/api/rutinas/", headers=HEADERS2)
lista_u2 = r.json()
ok("GET  /api/rutinas/  (usuario 2 ve lista vacía)", r)
ids_u2 = [x["id"] for x in lista_u2] if isinstance(lista_u2, list) else []
cross_get = ids_u2 and RUTINA_ID in ids_u2
print(f"    {'✗ FUGA' if cross_get else '✓'} La rutina del usuario 1 {'SÍ' if cross_get else 'NO'} aparece en la lista del usuario 2")

r = requests.get(f"{BASE}/api/rutinas/{RUTINA_ID}", headers=HEADERS2)
ok(f"GET  /api/rutinas/{RUTINA_ID}  (usuario 2 → 404)", r, esperado=404)

r = requests.delete(f"{BASE}/api/rutinas/{RUTINA_ID}", headers=HEADERS2)
ok(f"DELETE /api/rutinas/{RUTINA_ID}  (usuario 2 no puede → 404)", r, esperado=404)

# ── Sesiones ──────────────────────────────────────────────────
seccion("SESIONES")

# Sin token → 401
r = requests.get(f"{BASE}/api/sesiones/")
ok("GET  /api/sesiones/  (sin token → 401)", r, esperado=401)

r = requests.post(f"{BASE}/api/sesiones/", headers=HEADERS, json={
    "duracion": 60,
    "notas": "Buena sesión, aumenté peso",
    "rutina_id": RUTINA_ID
})
ok("POST /api/sesiones/  (usuario 1)", r)
SESION_ID = r.json()["id"]

r = requests.get(f"{BASE}/api/sesiones/", headers=HEADERS)
ok("GET  /api/sesiones/  (usuario 1 ve sus sesiones)", r)

r = requests.get(f"{BASE}/api/sesiones/{SESION_ID}", headers=HEADERS)
ok(f"GET  /api/sesiones/{SESION_ID}  (usuario 1)", r)

r = requests.put(f"{BASE}/api/sesiones/{SESION_ID}", headers=HEADERS, json={
    "duracion": 75,
    "notas": "Actualizado: muy buena sesión",
    "rutina_id": RUTINA_ID
})
ok(f"PUT  /api/sesiones/{SESION_ID}  (usuario 1)", r)

# Usuario 2 no puede ver ni modificar la sesión del usuario 1
r = requests.get(f"{BASE}/api/sesiones/", headers=HEADERS2)
lista_s2 = r.json()
ok("GET  /api/sesiones/  (usuario 2 ve lista vacía)", r)
ids_s2 = [x["id"] for x in lista_s2] if isinstance(lista_s2, list) else []
cross_ses = ids_s2 and SESION_ID in ids_s2
print(f"    {'✗ FUGA' if cross_ses else '✓'} La sesión del usuario 1 {'SÍ' if cross_ses else 'NO'} aparece en la lista del usuario 2")

r = requests.get(f"{BASE}/api/sesiones/{SESION_ID}", headers=HEADERS2)
ok(f"GET  /api/sesiones/{SESION_ID}  (usuario 2 → 404)", r, esperado=404)

r = requests.delete(f"{BASE}/api/sesiones/{SESION_ID}", headers=HEADERS2)
ok(f"DELETE /api/sesiones/{SESION_ID}  (usuario 2 no puede → 404)", r, esperado=404)

# ── DELETE (respetando FK: sesión → rutina → ejercicio → deporte)
seccion("DELETE")
r = requests.delete(f"{BASE}/api/sesiones/{SESION_ID}", headers=HEADERS)
ok(f"DELETE /api/sesiones/{SESION_ID}  (usuario 1)", r)

r = requests.delete(f"{BASE}/api/rutinas/{RUTINA_ID}", headers=HEADERS)
ok(f"DELETE /api/rutinas/{RUTINA_ID}  (usuario 1)", r)

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
print(f"  Usuario 1: {EMAIL}  (id={USUARIO_ID})")
print(f"  Usuario 2: {EMAIL2}")
print(f"{BOLD}{'─'*60}{RESET}\n")
