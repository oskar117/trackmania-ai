# Trackmania AI

Jest to program, który ma za zadanie nauczyć się grać w grę Trackmania 2020. 
Na początku obraz z gry przetwarzany jest za pomocą OpenCV, aby wykryć krawędzię trasy
(na chwilę obecną obsługuje tylko zwykłą asfaltową nawierzchnię). Resztę danych pozyskuje 
z obrazu za pomocą Tesseract (wymaga kilku modów z OpenPlanet), bądź czytając dane z adresów pamięci
(wymaga CheatEngine albo innego narzędzia aby znaleźć manualnie odpowiednie adresy). Wszystkie dane wrzucane są
do algorytmu genetycznego NEAT. Po zakończeniu nauki program zapisuje sieć neuronową do pliku,
aby można było później uruchomić ją w trybie gry.

### Uruchamianie

Dostępne są 3 główne tryby programu:
* **learn** - program przeprowadzający naukę
* **play** - program odtwarzający sieć neuronową
* **help** - wyświetla ekran pomocy

Dla trybów learn i play dostępne są następujące podejścia do pozyskiwania danych:
* **visual** - używa tesseract do pozyskiwania danych o grze
```bash
    python main.py [learn|play] visual [nazwa_pliku_z_najlepszym_wynikiem] [ścieżka do instalacji tesseract]
```
* **memory** - czyta dane po adresach w pamięci
```bash
    python main.py [learn|play] memory [nazwa_pliku_z_najlepszym_wynikiem] [pid_gry] [adres_prędkości] [adres_biegu]
     [adres_zaliczonych_checkpointów] [adres_czasu_na_ostatnim_checkpoincie] [adres_ostatniego_ukonczonego_okrążenia]
```