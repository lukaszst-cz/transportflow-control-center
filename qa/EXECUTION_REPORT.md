# Raport wykonania testów

Data wykonania: 2026-09-27  
Zakres: bieżący `main` / przygotowanie demonstracji portfolio  
Klasyfikacja danych: wyłącznie syntetyczne

## Wynik automatyczny

- `python app.py --check` — PASS
- `python -m unittest discover -s tests -v` — 13/13 PASS
- inicjalizacja tymczasowej bazy SQLite — PASS
- endpoint dashboardu — PASS
- endpoint zleceń i filtrowanie po statusie — PASS
- obsługa nieistniejącego endpointu 404 — PASS
- powtarzalny seed bez duplikatów — PASS
- kontrola syntetycznego zestawu danych — PASS
- kontrola marży i wymaganych dokumentów — PASS\n- podział kierowców 24 podstawowych + 2 rezerwowych — PASS
- reguły odczytów 28/90 dni — PASS
- zgodność rozkładu floty z `workflow.json` — PASS
- zgodność reguł blokujących z kontraktem procesu — PASS

## Zakres danych demo

- 20 zestawów,
- 26 kierowców,
- 3 scenariusze zleceń,
- dokumenty firmowe, pojazdów i kierowców,
- scenariusz blokady wyjazdu przez brak dokumentu specjalistycznego.

## Ograniczenia

Wynik potwierdza spójność demonstracyjnego modelu operacyjnego, API i danych testowych. Nie jest audytem bezpieczeństwa systemu produkcyjnego.

Publiczna wersja nie zawiera produkcyjnego systemu tożsamości, serwerowego RBAC, szyfrowania danych operacyjnych, kopii zapasowych, pełnego dziennika audytowego ani rzeczywistej integracji GPS/telematycznej.

Frontend/PWA i skoroszyt procesu są utrzymywane w osobnym repozytorium `transportflow-360` i mają własną kontrolę jakości.
