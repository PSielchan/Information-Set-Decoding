# McEliece Cryptosystem & Prange ISD Attack Demonstrator

Krótka demonstracja działania ataku kryptoanalitycznego Prange ISD (Information Set Decoding) wraz z implementacją systemu kryptograficznego McEliece opartego na binarnych kodach Goppy.

## Wymagania systemowe

Kod został napisany w języku Python (.py) i wymaga zainstalowania dwóch zewnętrznych bibliotek do obsługi macierzy oraz ciał skończonych.

Wymagany Python: **wersja 3.8 lub nowsza**

### Instalacja zależności

Zainstaluj wymagane pakiety za pomocą menedżera pakietów `pip`:

```bash
pip install numpy galois
```

## Jak uruchomić program?

Uruchom w terminalu:

```bash
python Prange_ISD_Demonstrator.py
```

## Co robi ten skrypt?

Po uruchomieniu program automatycznie przeprowadzi pełną demonstrację:

1. **Generowanie kluczy:** Tworzy losowy wielomian Goppy stopnia $t=2$ nad ciałem $GF(16)$ oraz wyznacza binarną macierz generującą $G$ i kontrolną $H$. Maskuje klucz prywatny losowymi macierzami $S$ oraz $P$, dając klucz publiczny $G_{pub}$.
2. **Szyfrowanie:** Koduje losową wiadomość i nakłada na nią dokładnie $t=2$ błędy.
3. **Kryptoanaliza:** Uruchamia atak Prange ISD, który bez znajomości klucza prywatnego (metodą próbkowania zbiorów informacyjnych) łamie szyfrogram i odzyskuje treść wiadomości.
