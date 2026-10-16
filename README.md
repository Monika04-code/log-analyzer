# Log Analyzer

Nástroj v Pythone, ktorý prečíta prístupový log webservera (formát Common Log Format) a vytvorí prehľadný súhrn. Nepotrebuje žiadne ďalšie knižnice, stačí Python 3.

## Čo robí
- Spočíta všetky požiadavky a množstvo prenesených dát
- Rozdelí požiadavky podľa stavových kódov (2xx, 3xx, 4xx, 5xx)
- Ukáže najaktívnejšie IP adresy a najčastejšie požadované adresy URL
- Zobrazí chyby (4xx a 5xx) podľa hodín, aby bolo vidieť, kedy sa problémy stávajú
- Preskočí neplatné riadky a povie, koľko ich bolo
- Voliteľne uloží rovnaký report ako súbor JSON

## Ako ho použiť
```
python log_analyzer.py sample_data/access.log
```

Voľby:
- `--top N` koľko najčastejších položiek zobraziť (predvolene 5)
- `--json report.json` uloží report aj do súboru JSON

Príklad:
```
python log_analyzer.py sample_data/access.log --top 3 --json report.json
```

## Ukážkový výstup
```
Total requests:   60
Invalid lines:    1
Data transferred: 1.24 MB

Status classes:
  2xx: 34
  3xx: 6
  4xx: 16
  5xx: 4

Top IP addresses:
  203.0.113.8       16
  192.0.2.10        12
  198.51.100.23     10
  192.0.2.11        9
  198.51.100.5      7

Top URLs:
  /                     21
  /produkty             9
  /admin                7
  /cennik               7
  /api/objednavky       6

Errors (4xx/5xx) by hour:
  08:00  ### 3
  09:00  ###### 6
  10:00  #### 4
  13:00  ## 2
  14:00  ## 2
  22:00  ### 3
```

## Na čo sa hodí
- Rýchly prehľad, ktoré stránky vracajú chyby
- Odhalenie podozrivej aktivity (veľa požiadaviek z jednej IP adresy alebo pokusy o prístup na `/admin`)
- Podklad pre správcu webu alebo pre report klientovi

## Poznámky
- Ukážkový log obsahuje vymyslené dáta. IP adresy patria do rozsahov vyhradených pre dokumentáciu.
- Nástroj očakáva štandardný formát logu (Apache, Nginx). Iné formáty by si vyžiadali úpravu regulárneho výrazu v `log_analyzer.py`.

## Autorka
Monika. Projekt je ukážkou mojej práce so spracovaním dát a textových súborov v Pythone.
