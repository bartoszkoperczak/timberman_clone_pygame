# TimbermanClone

TimbermanClone to zręcznościowa gra 2D napisana w Pythonie z użyciem biblioteki Pygame. Gracz wciela się w drwala, którego zadaniem jest ścinanie drzewa i unikanie gałęzi. Gra oferuje tryb singleplayer, multiplayer (1vs1) oraz pojedynek z botem.

## Spis treści
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Uruchomienie](#uruchomienie)
- [Tryby gry](#tryby-gry)
- [Sterowanie](#sterowanie)
- [Struktura projektu](#struktura-projektu)
- [Opis najważniejszych klas](#opis-najważniejszych-klas)
- [Zapis postępów i ustawień](#zapis-postępów-i-ustawień)
- [Testy](#testy)
- [Autorzy](#autorzy)

## Wymagania
- Python 3.12+ (zalecany)
- Pygame
- Pozostałe zależności znajdują się w pliku `requirements.txt`

## Instalacja
1. Sklonuj repozytorium lub pobierz projekt.
2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

## Uruchomienie
Aby uruchomić grę, wykonaj:
```bash
python run.py
```

## Tryby gry
- **Singleplayer** – klasyczna rozgrywka dla jednego gracza.
- **1vs1** – dwóch graczy na podzielonym ekranie.
- **1vsBot** – pojedynek z komputerowym przeciwnikiem.

## Sterowanie
Sterowanie można zmieniać w menu ustawień. Domyślnie:
- Gracz 1: Z (lewo) X (cios) C (prawo)
- Gracz 2: J (lewo) K (cios) L (prawo)

## Struktura projektu
- `run.py` – główny plik uruchamiający grę.
- `requirements.txt` – zależności projektu.
- `assets/` – grafiki, muzyka, czcionki:
  - `background*.jpg` – tła gry
  - `character_*.png` – postacie
  - `tree.jpg`, `branch.png`, `golden_tree.jpg`, `golden_branch.png` – elementy drzewa
  - `ui/` – grafiki przycisków i interfejsu
  - `fonts/` – czcionki
- `data/` – pliki z historią gier i konfiguracją sterowania:
  - `history.json` – historia gier
  - `config.json` – ustawienia sterowania
- `src/` – kod źródłowy gry:
  - `assets_manager.py` – ładowanie i zarządzanie zasobami
  - `DEFAULTS.py` – stałe i domyślne wartości
  - `event_manager.py` – obsługa zdarzeń
  - `game_window.py` – główne okno gry i pętla aplikacji
  - `storage_service.py` – zapis i odczyt historii oraz ustawień
  - `ui_manager.py` – obsługa interfejsu użytkownika
  - `view_manager.py` – zarządzanie widokami
  - `components/` – komponenty UI (np. przyciski)
  - `enums/` – typy wyliczeniowe (tryby gry, sterowanie, power-upy)
  - `game/` – logika gry:
    - `Game.py` – główna klasa rozgrywki
    - `GameEngine.py` – silnik gry dla pojedynczego gracza
    - `Character.py` – postać gracza
    - `Tree.py`, `Log.py` – drzewo i kłody
    - `HUD.py` – wyświetlanie wyników, timerów, komunikatów
    - `IceShard.py` – obsługa przeszkód
  - `interfaces/` – interfejsy do rysowania i obsługi zdarzeń
- `tests/` – testy jednostkowe

## Opis najważniejszych klas

- **GameWindow** – główne okno gry, pętla zdarzeń, inicjalizacja UI i muzyki.
- **UIManager** – zarządza ekranami menu, ustawień, historii gier, obsługuje przyciski i slider głośności.
- **Game** – zarządza rozgrywką, silnikami graczy, HUDem, czasem gry i zapisuje historię.
- **GameEngine** – logika gry dla jednego gracza (ruch, kolizje, punkty, power-upy).
- **HUD** – wyświetlanie wyników, timerów, komunikatów o przegranej/wygranej, obsługa powrotu do menu.
- **StorageService** – zapis i odczyt historii gier oraz ustawień sterowania.
- **ViewManager** – przełączanie widoków (menu, gra, ustawienia).
- **Button** – komponent przycisku UI.

## Zapis postępów i ustawień
- Historia gier zapisywana jest w pliku `data/history.json`.
- Ustawienia sterowania i inne konfiguracje w `data/config.json`.
- W menu ustawień można przeglądać historię gier oraz zmieniać sterowanie.

## Testy
Testy jednostkowe znajdują się w katalogu `tests/`. Aby je uruchomić:
```bash
pytest tests/
```

## Autorzy
Projekt stworzony przez Michał Kozak/Bartosz Koperczak.

