# Análisis de demanda del mercado laboral

*Generado el 2026-11-13 · muestra de **4239** vacantes sobre un corpus de **4239**.*

## Método

Cada vacante se clasifica en un perfil primario ponderando las señales del
título (peso 3) y de la descripción (peso 1). Los términos se detectan con
coincidencia por límite de palabra sobre alias explícitos, de modo que `sql`
no cuenta como aparición en `mysql` ni en `postgresql`.

El porcentaje indica en cuántas ofertas del perfil aparece el término.
El intervalo del 95% (método de Wilson) dice cuánta incertidumbre hay:
un término con 4% y un IC de 2–7% no es lo mismo que uno con 4% y 3.8–4.2%.

### Muestra por fuente

| Fuente | Vacantes en la muestra |
|---|---:|
| arbeitnow | 3576 |
| jobicy | 312 |
| himalayas | 240 |
| remoteok | 99 |
| remotive | 12 |

## Perfiles

| Perfil | Ofertas clasificadas |
|---|---:|
| OPS | 1129 |
| SUPPORT | 459 |
| IA | 303 |
| TURISMO | 216 |
| PM | 200 |
| ADMIN | 194 |
| UX | 134 |
| QA | 73 |

## OPS — 1129 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `stakeholder` | 482/1129 | 42.7% | 39.8–45.6% | arbeitnow (378), jobicy (70), himalayas (31) |
| `reporting` | 374/1129 | 33.1% | 30.4–35.9% | arbeitnow (283), jobicy (62), himalayas (23) |
| `logistics` | 282/1129 | 25.0% | 22.5–27.6% | arbeitnow (235), jobicy (27), himalayas (15) |
| `travel` | 271/1129 | 24.0% | 21.6–26.6% | arbeitnow (210), jobicy (43), himalayas (18) |
| `kpi` | 233/1129 | 20.6% | 18.4–23.1% | arbeitnow (150), jobicy (62), himalayas (20) |
| `process_improvement` | 214/1129 | 19.0% | 16.8–21.3% | arbeitnow (168), jobicy (31), himalayas (14) |
| `documentation` | 190/1129 | 16.8% | 14.8–19.1% | arbeitnow (125), jobicy (39), himalayas (22) |
| `roadmap` | 177/1129 | 15.7% | 13.7–17.9% | arbeitnow (117), jobicy (54), himalayas (5) |
| `onboarding` | 172/1129 | 15.2% | 13.3–17.4% | arbeitnow (137), jobicy (25), himalayas (7) |
| `customer_success` | 171/1129 | 15.1% | 13.2–17.4% | arbeitnow (130), jobicy (32), himalayas (8) |
| `python` | 145/1129 | 12.8% | 11.0–14.9% | arbeitnow (114), jobicy (20), himalayas (10) |
| `excel` | 135/1129 | 12.0% | 10.2–14.0% | arbeitnow (107), himalayas (16), jobicy (10) |
| `vendor_management` | 125/1129 | 11.1% | 9.4–13.0% | arbeitnow (106), jobicy (11), himalayas (7) |
| `sql` | 120/1129 | 10.6% | 9.0–12.6% | arbeitnow (92), jobicy (19), himalayas (7) |
| `project_management` | 119/1129 | 10.5% | 8.9–12.5% | arbeitnow (95), jobicy (14), himalayas (9) |
| `crm` | 113/1129 | 10.0% | 8.4–11.9% | arbeitnow (87), jobicy (15), himalayas (10) |
| `escalation` | 110/1129 | 9.7% | 8.1–11.6% | arbeitnow (71), jobicy (21), himalayas (16) |
| `inventory` | 106/1129 | 9.4% | 7.8–11.2% | arbeitnow (89), jobicy (7), himalayas (7) |
| `salesforce` | 103/1129 | 9.1% | 7.6–10.9% | arbeitnow (79), jobicy (15), himalayas (8) |
| `llm` | 97/1129 | 8.6% | 7.1–10.4% | arbeitnow (69), jobicy (26), himalayas (2) |
| `troubleshooting` | 92/1129 | 8.1% | 6.7–9.9% | arbeitnow (70), jobicy (14), himalayas (8) |
| `docker` | 91/1129 | 8.1% | 6.6–9.8% | arbeitnow (64), jobicy (19), himalayas (6) |
| `data_visualization` | 87/1129 | 7.7% | 6.3–9.4% | arbeitnow (64), jobicy (15), himalayas (7) |
| `agile` | 79/1129 | 7.0% | 5.7–8.6% | arbeitnow (51), jobicy (21), himalayas (7) |
| `prototyping` | 76/1129 | 6.7% | 5.4–8.3% | arbeitnow (46), jobicy (27), himalayas (3) |


## SUPPORT — 459 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `customer_success` | 271/459 | 59.0% | 54.5–63.4% | arbeitnow (191), jobicy (65), himalayas (8) |
| `stakeholder` | 146/459 | 31.8% | 27.7–36.2% | arbeitnow (85), jobicy (42), remoteok (12) |
| `onboarding` | 118/459 | 25.7% | 21.9–29.9% | arbeitnow (64), jobicy (38), remoteok (8) |
| `ticketing` | 106/459 | 23.1% | 19.5–27.2% | arbeitnow (81), jobicy (16), himalayas (5) |
| `travel` | 88/459 | 19.2% | 15.8–23.0% | arbeitnow (46), jobicy (29), remoteok (8) |
| `reporting` | 87/459 | 19.0% | 15.6–22.8% | arbeitnow (48), jobicy (27), remoteok (11) |
| `documentation` | 82/459 | 17.9% | 14.6–21.6% | arbeitnow (41), jobicy (22), remoteok (12) |
| `kpi` | 78/459 | 17.0% | 13.8–20.7% | arbeitnow (35), jobicy (30), remoteok (10) |
| `escalation` | 72/459 | 15.7% | 12.6–19.3% | jobicy (34), arbeitnow (29), himalayas (5) |
| `crm` | 67/459 | 14.6% | 11.7–18.1% | arbeitnow (42), jobicy (20), himalayas (4) |
| `roadmap` | 58/459 | 12.6% | 9.9–16.0% | arbeitnow (33), jobicy (19), remoteok (5) |
| `salesforce` | 54/459 | 11.8% | 9.1–15.0% | arbeitnow (28), jobicy (23), himalayas (2) |
| `troubleshooting` | 49/459 | 10.7% | 8.2–13.8% | jobicy (22), arbeitnow (18), himalayas (6) |
| `process_improvement` | 43/459 | 9.4% | 7.0–12.4% | arbeitnow (22), jobicy (14), remoteok (4) |
| `csat` | 41/459 | 8.9% | 6.7–11.9% | jobicy (19), arbeitnow (17), remoteok (3) |
| `upselling` | 41/459 | 8.9% | 6.7–11.9% | arbeitnow (28), jobicy (13) |
| `excel` | 35/459 | 7.6% | 5.5–10.4% | arbeitnow (16), jobicy (12), remoteok (5) |
| `project_management` | 29/459 | 6.3% | 4.4–8.9% | arbeitnow (13), jobicy (11), remoteok (5) |
| `sql` | 27/459 | 5.9% | 4.1–8.4% | arbeitnow (13), jobicy (10), remoteok (4) |
| `llm` | 26/459 | 5.7% | 3.9–8.2% | arbeitnow (11), jobicy (6), remoteok (5) |
| `python` | 25/459 | 5.4% | 3.7–7.9% | arbeitnow (10), remoteok (8), jobicy (7) |
| `agile` | 24/459 | 5.2% | 3.5–7.7% | arbeitnow (17), jobicy (4), remoteok (2) |
| `vendor_management` | 23/459 | 5.0% | 3.4–7.4% | arbeitnow (19), remoteok (2), jobicy (2) |
| `javascript` | 20/459 | 4.4% | 2.8–6.6% | remoteok (7), jobicy (7), arbeitnow (5) |
| `knowledge_base` | 20/459 | 4.4% | 2.8–6.6% | arbeitnow (10), jobicy (9), himalayas (1) |


## IA — 303 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `llm` | 196/303 | 64.7% | 59.2–69.9% | arbeitnow (171), jobicy (11), himalayas (8) |
| `python` | 127/303 | 41.9% | 36.5–47.5% | arbeitnow (113), jobicy (7), remoteok (4) |
| `stakeholder` | 85/303 | 28.1% | 23.3–33.4% | arbeitnow (78), jobicy (5), remoteok (1) |
| `sql` | 81/303 | 26.7% | 22.1–32.0% | arbeitnow (76), himalayas (2), remoteok (1) |
| `reporting` | 75/303 | 24.8% | 20.2–29.9% | arbeitnow (69), jobicy (4), remotive (1) |
| `javascript` | 73/303 | 24.1% | 19.6–29.2% | arbeitnow (67), remoteok (4), remotive (1) |
| `data_quality` | 67/303 | 22.1% | 17.8–27.1% | arbeitnow (58), himalayas (4), jobicy (3) |
| `documentation` | 60/303 | 19.8% | 15.7–24.7% | arbeitnow (53), himalayas (4), jobicy (2) |
| `roadmap` | 58/303 | 19.1% | 15.1–23.9% | arbeitnow (49), jobicy (6), himalayas (2) |
| `docker` | 56/303 | 18.5% | 14.5–23.2% | arbeitnow (50), jobicy (3), remoteok (2) |
| `process_improvement` | 51/303 | 16.8% | 13.0–21.5% | arbeitnow (41), jobicy (5), himalayas (3) |
| `ci_cd` | 50/303 | 16.5% | 12.7–21.1% | arbeitnow (45), jobicy (2), himalayas (2) |
| `kpi` | 46/303 | 15.2% | 11.6–19.7% | arbeitnow (43), remoteok (1), jobicy (1) |
| `logistics` | 45/303 | 14.9% | 11.3–19.3% | arbeitnow (39), remoteok (3), jobicy (2) |
| `etl` | 43/303 | 14.2% | 10.7–18.6% | arbeitnow (41), remoteok (1), jobicy (1) |
| `prototyping` | 41/303 | 13.5% | 10.1–17.8% | arbeitnow (34), jobicy (5), remoteok (2) |
| `ab_testing` | 40/303 | 13.2% | 9.8–17.5% | arbeitnow (36), jobicy (3), remotive (1) |
| `git` | 38/303 | 12.5% | 9.3–16.7% | arbeitnow (31), remoteok (3), himalayas (2) |
| `travel` | 38/303 | 12.5% | 9.3–16.7% | arbeitnow (30), jobicy (6), remoteok (2) |
| `data_visualization` | 37/303 | 12.2% | 9.0–16.4% | arbeitnow (34), himalayas (2), remoteok (1) |
| `onboarding` | 33/303 | 10.9% | 7.9–14.9% | arbeitnow (26), himalayas (4), jobicy (3) |
| `annotation` | 32/303 | 10.6% | 7.6–14.5% | arbeitnow (19), himalayas (9), remoteok (3) |
| `model_evaluation` | 32/303 | 10.6% | 7.6–14.5% | arbeitnow (27), remoteok (3), himalayas (2) |
| `prompt_engineering` | 31/303 | 10.2% | 7.3–14.2% | arbeitnow (28), remoteok (2), himalayas (1) |
| `excel` | 27/303 | 8.9% | 6.2–12.7% | arbeitnow (22), jobicy (2), himalayas (2) |


## TURISMO — 216 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `travel` | 175/216 | 81.0% | 75.3–85.7% | arbeitnow (137), jobicy (23), himalayas (10) |
| `stakeholder` | 76/216 | 35.2% | 29.1–41.8% | arbeitnow (61), jobicy (12), himalayas (2) |
| `hospitality` | 59/216 | 27.3% | 21.8–33.6% | arbeitnow (40), jobicy (10), himalayas (6) |
| `reporting` | 57/216 | 26.4% | 21.0–32.6% | arbeitnow (49), jobicy (4), himalayas (4) |
| `booking` | 38/216 | 17.6% | 13.1–23.2% | arbeitnow (20), jobicy (10), himalayas (5) |
| `kpi` | 38/216 | 17.6% | 13.1–23.2% | arbeitnow (23), jobicy (10), himalayas (4) |
| `onboarding` | 35/216 | 16.2% | 11.9–21.7% | arbeitnow (23), jobicy (6), himalayas (5) |
| `crm` | 31/216 | 14.4% | 10.3–19.7% | arbeitnow (22), jobicy (5), himalayas (4) |
| `roadmap` | 29/216 | 13.4% | 9.5–18.6% | arbeitnow (21), jobicy (6), remoteok (1) |
| `python` | 28/216 | 13.0% | 9.1–18.1% | arbeitnow (27), himalayas (1) |
| `customer_success` | 25/216 | 11.6% | 8.0–16.5% | arbeitnow (18), jobicy (4), himalayas (2) |
| `salesforce` | 23/216 | 10.6% | 7.2–15.5% | arbeitnow (14), jobicy (6), himalayas (3) |
| `documentation` | 23/216 | 10.6% | 7.2–15.5% | arbeitnow (20), himalayas (2), jobicy (1) |
| `process_improvement` | 22/216 | 10.2% | 6.8–14.9% | arbeitnow (16), jobicy (5), himalayas (1) |
| `docker` | 19/216 | 8.8% | 5.7–13.3% | arbeitnow (13), jobicy (4), himalayas (2) |
| `excel` | 19/216 | 8.8% | 5.7–13.3% | arbeitnow (17), himalayas (2) |
| `ci_cd` | 17/216 | 7.9% | 5.0–12.2% | arbeitnow (13), jobicy (3), himalayas (1) |
| `project_management` | 16/216 | 7.4% | 4.6–11.7% | arbeitnow (10), jobicy (5), himalayas (1) |
| `logistics` | 15/216 | 6.9% | 4.3–11.1% | arbeitnow (8), jobicy (5), remoteok (1) |
| `vendor_management` | 14/216 | 6.5% | 3.9–10.6% | arbeitnow (11), jobicy (2), remoteok (1) |
| `escalation` | 13/216 | 6.0% | 3.6–10.0% | arbeitnow (9), jobicy (3), himalayas (1) |
| `llm` | 13/216 | 6.0% | 3.6–10.0% | arbeitnow (11), jobicy (1), himalayas (1) |
| `git` | 13/216 | 6.0% | 3.6–10.0% | arbeitnow (12), himalayas (1) |
| `csat` | 12/216 | 5.6% | 3.2–9.5% | arbeitnow (6), jobicy (3), himalayas (3) |
| `agile` | 12/216 | 5.6% | 3.2–9.5% | arbeitnow (7), jobicy (5) |


## PM — 200 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `stakeholder` | 87/200 | 43.5% | 36.8–50.4% | arbeitnow (81), himalayas (3), remoteok (2) |
| `roadmap` | 75/200 | 37.5% | 31.1–44.4% | arbeitnow (70), remoteok (3), himalayas (2) |
| `project_management` | 57/200 | 28.5% | 22.7–35.1% | arbeitnow (51), himalayas (4), remoteok (2) |
| `kpi` | 52/200 | 26.0% | 20.4–32.5% | arbeitnow (47), remoteok (4), himalayas (1) |
| `reporting` | 52/200 | 26.0% | 20.4–32.5% | arbeitnow (50), remoteok (1), himalayas (1) |
| `agile` | 51/200 | 25.5% | 20.0–32.0% | arbeitnow (49), remoteok (1), himalayas (1) |
| `logistics` | 36/200 | 18.0% | 13.3–23.9% | arbeitnow (31), remoteok (4), himalayas (1) |
| `documentation` | 36/200 | 18.0% | 13.3–23.9% | arbeitnow (35), himalayas (1) |
| `travel` | 34/200 | 17.0% | 12.4–22.8% | arbeitnow (32), jobicy (1), himalayas (1) |
| `llm` | 31/200 | 15.5% | 11.1–21.2% | arbeitnow (29), remoteok (2) |
| `javascript` | 26/200 | 13.0% | 9.0–18.4% | arbeitnow (25), remoteok (1) |
| `onboarding` | 26/200 | 13.0% | 9.0–18.4% | arbeitnow (24), remoteok (1), himalayas (1) |
| `jira` | 25/200 | 12.5% | 8.6–17.8% | arbeitnow (24), remoteok (1) |
| `sql` | 25/200 | 12.5% | 8.6–17.8% | arbeitnow (23), remoteok (1), himalayas (1) |
| `bug_reporting` | 23/200 | 11.5% | 7.8–16.7% | arbeitnow (22), remoteok (1) |
| `ci_cd` | 23/200 | 11.5% | 7.8–16.7% | arbeitnow (21), jobicy (1), himalayas (1) |
| `python` | 23/200 | 11.5% | 7.8–16.7% | arbeitnow (23) |
| `requirements` | 22/200 | 11.0% | 7.4–16.1% | arbeitnow (21), himalayas (1) |
| `process_improvement` | 21/200 | 10.5% | 7.0–15.5% | arbeitnow (20), remoteok (1) |
| `docker` | 18/200 | 9.0% | 5.8–13.8% | arbeitnow (17), jobicy (1) |
| `customer_success` | 18/200 | 9.0% | 5.8–13.8% | arbeitnow (18) |
| `prototyping` | 17/200 | 8.5% | 5.4–13.2% | arbeitnow (15), remoteok (1), himalayas (1) |
| `escalation` | 15/200 | 7.5% | 4.6–12.0% | arbeitnow (14), remoteok (1) |
| `ticketing` | 14/200 | 7.0% | 4.2–11.4% | arbeitnow (14) |
| `data_visualization` | 13/200 | 6.5% | 3.8–10.8% | arbeitnow (12), remoteok (1) |


## ADMIN — 194 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `reporting` | 50/194 | 25.8% | 20.1–32.4% | arbeitnow (41), himalayas (7), remoteok (1) |
| `excel` | 44/194 | 22.7% | 17.4–29.1% | arbeitnow (36), himalayas (6), remoteok (1) |
| `llm` | 35/194 | 18.0% | 13.3–24.1% | arbeitnow (33), remoteok (1), himalayas (1) |
| `stakeholder` | 32/194 | 16.5% | 11.9–22.4% | arbeitnow (28), himalayas (4) |
| `python` | 27/194 | 13.9% | 9.7–19.5% | arbeitnow (27) |
| `documentation` | 24/194 | 12.4% | 8.5–17.7% | arbeitnow (18), himalayas (6) |
| `logistics` | 21/194 | 10.8% | 7.2–16.0% | arbeitnow (18), remoteok (2), himalayas (1) |
| `process_improvement` | 20/194 | 10.3% | 6.8–15.4% | arbeitnow (17), himalayas (2), remoteok (1) |
| `onboarding` | 20/194 | 10.3% | 6.8–15.4% | arbeitnow (18), himalayas (2) |
| `kpi` | 19/194 | 9.8% | 6.4–14.8% | arbeitnow (19) |
| `sql` | 19/194 | 9.8% | 6.4–14.8% | arbeitnow (19) |
| `travel` | 17/194 | 8.8% | 5.5–13.6% | arbeitnow (14), himalayas (2), remoteok (1) |
| `agile` | 17/194 | 8.8% | 5.5–13.6% | arbeitnow (16), himalayas (1) |
| `git` | 14/194 | 7.2% | 4.3–11.7% | arbeitnow (14) |
| `docker` | 13/194 | 6.7% | 4.0–11.1% | arbeitnow (12), remoteok (1) |
| `project_management` | 13/194 | 6.7% | 4.0–11.1% | arbeitnow (11), remoteok (1), himalayas (1) |
| `prototyping` | 13/194 | 6.7% | 4.0–11.1% | arbeitnow (11), remoteok (1), himalayas (1) |
| `javascript` | 13/194 | 6.7% | 4.0–11.1% | arbeitnow (12), remoteok (1) |
| `reconciliation` | 13/194 | 6.7% | 4.0–11.1% | arbeitnow (12), himalayas (1) |
| `vendor_management` | 12/194 | 6.2% | 3.6–10.5% | arbeitnow (10), remoteok (1), himalayas (1) |
| `roadmap` | 12/194 | 6.2% | 3.6–10.5% | arbeitnow (10), remoteok (1), himalayas (1) |
| `ci_cd` | 12/194 | 6.2% | 3.6–10.5% | arbeitnow (12) |
| `notion` | 11/194 | 5.7% | 3.2–9.9% | arbeitnow (10), remoteok (1) |
| `crm` | 11/194 | 5.7% | 3.2–9.9% | arbeitnow (10), himalayas (1) |
| `ticketing` | 11/194 | 5.7% | 3.2–9.9% | arbeitnow (11) |


## UX — 134 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `product_design` | 67/134 | 50.0% | 41.7–58.3% | arbeitnow (56), himalayas (7), remoteok (3) |
| `javascript` | 51/134 | 38.1% | 30.3–46.5% | arbeitnow (43), remoteok (3), himalayas (3) |
| `figma` | 38/134 | 28.4% | 21.4–36.5% | arbeitnow (35), himalayas (2), remoteok (1) |
| `stakeholder` | 36/134 | 26.9% | 20.1–34.9% | arbeitnow (30), himalayas (5), jobicy (1) |
| `prototyping` | 31/134 | 23.1% | 16.8–31.0% | arbeitnow (29), himalayas (2) |
| `design_system` | 31/134 | 23.1% | 16.8–31.0% | arbeitnow (28), himalayas (3) |
| `llm` | 23/134 | 17.2% | 11.7–24.4% | arbeitnow (17), remoteok (2), remotive (2) |
| `docker` | 22/134 | 16.4% | 11.1–23.6% | arbeitnow (17), remotive (2), himalayas (2) |
| `onboarding` | 22/134 | 16.4% | 11.1–23.6% | arbeitnow (21), himalayas (1) |
| `kpi` | 20/134 | 14.9% | 9.9–21.9% | arbeitnow (20) |
| `python` | 19/134 | 14.2% | 9.3–21.1% | arbeitnow (16), remoteok (2), remotive (1) |
| `ci_cd` | 19/134 | 14.2% | 9.3–21.1% | arbeitnow (18), remoteok (1) |
| `roadmap` | 18/134 | 13.4% | 8.7–20.2% | arbeitnow (17), himalayas (1) |
| `logistics` | 17/134 | 12.7% | 8.1–19.4% | arbeitnow (13), remoteok (2), remotive (1) |
| `html_css` | 17/134 | 12.7% | 8.1–19.4% | arbeitnow (15), remoteok (1), himalayas (1) |
| `documentation` | 17/134 | 12.7% | 8.1–19.4% | arbeitnow (13), himalayas (2), remotive (1) |
| `java` | 16/134 | 11.9% | 7.5–18.5% | arbeitnow (10), himalayas (3), remoteok (2) |
| `git` | 16/134 | 11.9% | 7.5–18.5% | arbeitnow (13), remoteok (1), remotive (1) |
| `reporting` | 16/134 | 11.9% | 7.5–18.5% | arbeitnow (15), remoteok (1) |
| `user_research` | 16/134 | 11.9% | 7.5–18.5% | arbeitnow (15), himalayas (1) |
| `sql` | 14/134 | 10.4% | 6.3–16.8% | arbeitnow (12), remoteok (1), himalayas (1) |
| `agile` | 14/134 | 10.4% | 6.3–16.8% | arbeitnow (14) |
| `accessibility` | 13/134 | 9.7% | 5.8–15.9% | arbeitnow (12), remoteok (1) |
| `process_improvement` | 12/134 | 9.0% | 5.2–15.0% | arbeitnow (10), jobicy (1), himalayas (1) |
| `user_flows` | 11/134 | 8.2% | 4.6–14.1% | arbeitnow (11) |


## QA — 73 ofertas

| Término | Ofertas | % | IC 95% | Fuentes |
|---|---:|---:|---|---|
| `qa` | 49/73 | 67.1% | 55.7–76.8% | arbeitnow (35), himalayas (8), remoteok (6) |
| `reporting` | 22/73 | 30.1% | 20.8–41.4% | arbeitnow (16), remoteok (4), himalayas (2) |
| `python` | 20/73 | 27.4% | 18.5–38.6% | arbeitnow (16), remoteok (3), himalayas (1) |
| `javascript` | 20/73 | 27.4% | 18.5–38.6% | arbeitnow (17), himalayas (2), remoteok (1) |
| `ci_cd` | 19/73 | 26.0% | 17.3–37.1% | arbeitnow (15), remoteok (2), himalayas (2) |
| `stakeholder` | 15/73 | 20.5% | 12.9–31.2% | arbeitnow (9), remoteok (4), himalayas (2) |
| `llm` | 14/73 | 19.2% | 11.8–29.7% | arbeitnow (10), himalayas (3), remoteok (1) |
| `bug_reporting` | 14/73 | 19.2% | 11.8–29.7% | arbeitnow (14) |
| `jira` | 14/73 | 19.2% | 11.8–29.7% | arbeitnow (13), himalayas (1) |
| `git` | 13/73 | 17.8% | 10.7–28.1% | arbeitnow (10), remoteok (2), himalayas (1) |
| `sql` | 13/73 | 17.8% | 10.7–28.1% | arbeitnow (10), remoteok (2), himalayas (1) |
| `documentation` | 13/73 | 17.8% | 10.7–28.1% | arbeitnow (10), himalayas (2), remoteok (1) |
| `test_plans` | 11/73 | 15.1% | 8.6–25.0% | arbeitnow (10), himalayas (1) |
| `kpi` | 10/73 | 13.7% | 7.6–23.4% | arbeitnow (9), remoteok (1) |
| `agile` | 10/73 | 13.7% | 7.6–23.4% | arbeitnow (9), himalayas (1) |
| `onboarding` | 9/73 | 12.3% | 6.6–21.8% | arbeitnow (7), remoteok (1), himalayas (1) |
| `test_cases` | 9/73 | 12.3% | 6.6–21.8% | arbeitnow (8), himalayas (1) |
| `docker` | 8/73 | 11.0% | 5.7–20.2% | arbeitnow (6), remoteok (2) |
| `crm` | 8/73 | 11.0% | 5.7–20.2% | arbeitnow (8) |
| `travel` | 8/73 | 11.0% | 5.7–20.2% | arbeitnow (7), himalayas (1) |
| `playwright` | 8/73 | 11.0% | 5.7–20.2% | arbeitnow (6), himalayas (2) |
| `linux` | 7/73 | 9.6% | 4.7–18.5% | arbeitnow (5), remoteok (1), himalayas (1) |
| `api_testing` | 7/73 | 9.6% | 4.7–18.5% | arbeitnow (4), himalayas (2), remoteok (1) |
| `excel` | 7/73 | 9.6% | 4.7–18.5% | arbeitnow (4), himalayas (2), remoteok (1) |
| `accessibility` | 7/73 | 9.6% | 4.7–18.5% | arbeitnow (7) |
