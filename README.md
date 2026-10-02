# TransportFlow Control Center

[![Test](https://github.com/lukaszst-cz/transportflow-control-center/actions/workflows/test.yml/badge.svg)](https://github.com/lukaszst-cz/transportflow-control-center/actions/workflows/test.yml)

Backendowa część demonstracji **TransportFlow 360**: lokalny model operacyjny Python + SQLite dla floty, zleceń, dokumentów i zgodności.

Frontend/PWA i skoroszyt procesu: https://github.com/lukaszst-cz/transportflow-360

Działające demo frontowe: https://lukaszst-cz.github.io/transportflow-360/

Lokalna aplikacja demonstracyjna Python + SQLite pokazująca:

- 20 zestawów: 12 chłodni, 4 cysterny i 4 plandeki;
- 26 kierowców: 24 podstawowych i 2 rezerwowych;
- zlecenia kontraktowe i giełdowe;
- koszty, ceny i marżę;
- dokumenty, terminy oraz blokady procesu;
- terminy odczytu kart kierowców i danych pojazdów;
- API JSON do odczytu dashboardu i zleceń.
- powiązanie z publicznym frontendem, który rozdziela widoki klienta, handlu, dyspozycji, kierowcy, floty, zgodności, finansów, najmu i właściciela.

Wszystkie dane są syntetyczne. Aplikacja nie jest produkcyjnym TMS-em.

Publiczna wersja portfolio demonstruje role na przełączniku, ale nie udaje produkcyjnego zabezpieczenia. Rzeczywiste wdrożenie wymaga logowania, RBAC po stronie serwera, szyfrowania, kopii zapasowych, dziennika audytowego i integracji z telematyką/GPS. Klient powinien widzieć lokalizację pojazdu realizującego jego zlecenie, a nie prywatną lokalizację kierowcy.

## Uruchomienie

```powershell
python app.py
```

Następnie otwórz `http://127.0.0.1:8025`.

## API demonstracyjne

Po uruchomieniu lokalnym dostępne są:
- `GET /api/health` — stan aplikacji i informacja, że zestaw danych jest syntetyczny;
- `GET /api/dashboard` — podsumowanie floty, kierowców, zleceń i dokumentów;
- `GET /api/orders` — lista demonstracyjnych zleceń;
- `GET /api/orders?status=W%20trasie` — filtrowanie zleceń po statusie.

API jest częścią demonstracji lokalnej. Nie zawiera logowania ani produkcyjnego RBAC.

## Kontrola danych

```powershell
python app.py --check
```

## Kontrola jakości

Automatyczne testy korzystają z osobnej tymczasowej bazy SQLite i obejmują:
- spójność floty i kierowców;
- marżę i dane operacyjne zleceń;
- wymagane dokumenty oraz scenariusz blokady wyjazdu;
- okresy odczytów 28/90 dni;
- zgodność rozkładu floty i reguł blokujących z `workflow.json`;
- endpointy dashboardu i zleceń;
- filtrowanie po statusie i obsługę 404;
- kontrolę syntetycznego zestawu danych;
- powtarzalne inicjalizowanie bazy bez duplikatów.

[Strategia testów](qa/TEST_STRATEGY.md) · [Przypadki testowe](qa/TEST_CASES.md) · [Macierz śledzenia](qa/TRACEABILITY_MATRIX.md) · [Raport wykonania](qa/EXECUTION_REPORT.md)

## Testy

```powershell
python -m unittest discover -s tests -v
```

Dokumentacja QA znajduje się w katalogu `qa/`.

## Autor, darmowe projekty i wsparcie

Projekt jest udostępniany bezpłatnie jako demonstracja i portfolio. Jeśli jest przydatny, można dobrowolnie wesprzeć dalszy rozwój: **[Postaw Naleśnikowi++ kawę ☕](https://buymeacoffee.com/nalesnik_plus_plus)**.

Potrzebujesz własnej strony WWW, formularza wyceny albo prostego systemu dla firmy? **[Zobacz Zielona Marka →](https://zielona-marka.pl)**.

