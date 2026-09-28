# Macierz śledzenia wymagań

| Wymaganie | Strona / aplikacja | Excel | Python / test |
|---|---|---|---|
| Proces RFQ → zapłata | `proces.html` | `RACI`, `Faktury` | `workflow.json` |
| 20 zestawów 12/4/4 | `flota.html` | `Flota_Ciezka` | `test_fleet_and_drivers` |
| 26 kierowców: 24 podstawowych + 2 rezerwowych | portal, zgodność | `Kierowcy` | `test_fleet_and_drivers`, `test_driver_employment_distribution` |
| Odczyty 28/90 dni | `flota.html`, artykuł | `Kierowcy`, `Czas_Pracy`, `Flota_Ciezka` | `test_workflow_download_periods` |
| Koszt i stawka za km | `kalkulator.html` | `Kalkulator_km` | `test_margin_is_positive_and_below_one` |
| Dokumenty i blokady | `dokumenty.html` | `Dokumenty`, `Checki` | `test_required_documents_and_blocking_scenario` |
| Chłodnie / cysterny | `flota.html` | `Chlodnie_ATP`, `Cysterny_ADR` | dane startowe SQLite |
| Taxi i kontenery osobno | `taxi-kontenery.html` | `Najem_Taxi`, `Kontenery_UDT` | konfiguracja modułów |
| Dostęp według ról | `portal/`, `dokumenty.html` | `Start`, `RACI`, `Slownik` | strategia wdrożenia RBAC |
| Widok klienta | `portal/` | dane tylko zbiorcze | API zleceń |
| Anonimizacja | wszystkie strony | wszystkie arkusze | `--check` |
