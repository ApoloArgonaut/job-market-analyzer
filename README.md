# jobmarket

**Qué piden realmente las ofertas de trabajo remotas — medido, no supuesto.**

Una herramienta de línea de comandos que descarga ofertas de cinco bolsas de
empleo públicas, las clasifica por perfil profesional y mide qué habilidades
aparecen en cada una, con intervalos de confianza.

```
$ jobmarket fetch
$ jobmarket analyze
→ reports/informe-mercado.md
```

---

## Por qué existe

Cuando buscas trabajo, alguien te dice «aprende SQL» o «aprende Docker». Casi
nunca te dice **en qué porcentaje de las ofertas de tu perfil aparece eso**, ni
con qué incertidumbre. Este proyecto lo mide sobre datos reales y publica el
método para que cualquiera pueda discutirlo.

Ejemplo real del informe, perfil QA (73 ofertas):

| Término | Ofertas | % | IC 95% |
|---|---:|---:|---|
| `qa` | 49/73 | 67.1% | 55.7–76.8% |
| `python` | 20/73 | 27.4% | 18.5–38.6% |
| `ci_cd` | 19/73 | 26.0% | 17.3–37.1% |
| `bug_reporting` | 14/73 | 19.2% | 11.8–29.7% |
| `sql` | 13/73 | 17.8% | 10.7–28.1% |

El intervalo importa: 17.8% con un IC de 10.7–28.1% significa «en algún lugar
entre una de cada seis y una de cada cuatro ofertas». Reportar solo el 17.8%
sería inventar precisión.

---

## Instalación

```bash
git clone https://github.com/ApoloArgonaut/job-market-analyzer
cd job-market-analyzer
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

Requiere Python 3.11 o superior. Sin dependencias de runtime: solo la
biblioteca estándar.

---

## Uso

### 1. Descargar ofertas

```bash
jobmarket fetch                              # las cinco fuentes
jobmarket fetch --sources remoteok himalayas # solo algunas
```

Escribe `data/vacantes.csv` y `data/vacantes.db` (SQLite con índices por perfil
y por fuente).

### 2. Generar el informe

```bash
jobmarket analyze
jobmarket analyze --json reports/terminos.json   # salida para máquinas
jobmarket analyze --per-source 400               # muestreo estratificado
```

Por defecto analiza el corpus completo. Con `--per-source N` toma hasta N
ofertas de cada fuente, con semilla fija para que el resultado sea reproducible.

### 3. Ver el reparto por perfil

```bash
jobmarket stats
```

---

## Método

### Clasificación

Cada oferta se asigna a **un** perfil primario. Las señales del título pesan 3
y las de la descripción pesan 1, porque una mención suelta en un párrafo de
4.000 caracteres no equivale a un puesto que se llama «QA Engineer».

Si ninguna señal supera el umbral, la oferta queda **sin clasificar**. Es
deliberado: forzar una etiqueta produce datos que parecen completos y no lo
están. En el corpus de referencia, el 63.9% se clasifica.

### Detección de términos

Cada término canónico tiene alias explícitos y se compara con **límites de
palabra**, nunca por subcadena:

```python
"sql" in "mysql"        # True  ← el error de la versión anterior
contains("mysql", "sql") # False ← aquí
```

Además se suprimen los términos contenidos en otro más largo: una oferta que
dice «bug reporting» no cuenta también como «reporting».

### Muestreo

El muestreo es **estratificado por fuente**. Sin eso, una bolsa que devuelve
4.000 ofertas aplasta a las demás y el informe termina describiendo un solo
mercado sin decirlo.

### Incertidumbre

Toda proporción lleva su intervalo de Wilson al 95%. Se prefiere a la
aproximación normal porque funciona con proporciones pequeñas y extremas, que
es justo el caso de «X% de las ofertas pide esto».

---

## Fuentes

| Fuente | Cobertura | Notas |
|---|---|---|
| RemoteOK | Global | API pública, sin clave |
| Remotive | Global | Filtrado por categoría |
| Jobicy | Global | Filtrado por industria |
| Arbeitnow | Principalmente Alemania | API paginada |
| Himalayas | Global | API paginada |

Ninguna requiere credenciales. Si una fuente cae, el resto continúa y el error
se reporta al final.

**Sesgo conocido:** las cinco son bolsas de empleo *remoto*. El informe describe
ese mercado, no el mercado presencial. Está declarado en el propio informe.

---

## Tests

```bash
.venv/bin/pytest                    # 85 tests
.venv/bin/pytest --cov=jobmarket    # con cobertura
```

Los tests cubren los cuatro bugs que motivaron la reescritura:

1. `sql` no debe coincidir dentro de `mysql` ni `postgresql`.
2. Una oferta pertenece a un solo perfil, no a varios.
3. El muestreo no puede dejar que una fuente domine la muestra.
4. Las proporciones deben llevar intervalo de confianza.

---

## Estructura

```
src/jobmarket/
├── normalize.py   # normalización, límites de palabra, supresión de solapamientos
├── lexicon.py     # términos canónicos, alias y perfiles
├── classify.py    # clasificación ponderada, con umbral y evidencia
├── sampling.py    # muestreo estratificado e intervalos de Wilson
├── fetch.py       # conectores con reintentos
├── analysis.py    # frecuencia por perfil, brechas y fortalezas
├── report.py      # informe en Markdown
├── store.py       # CSV canónico y SQLite
└── cli.py         # interfaz de línea de comandos
```

---

## Licencia

MIT — ver [LICENSE](LICENSE).

## Autor

**Ezra Gonzalez** — [LinkedIn](https://www.linkedin.com/in/ezra-gonzalez-studio) · [GitHub](https://github.com/ApoloArgonaut)
