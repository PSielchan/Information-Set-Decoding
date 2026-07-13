# Sprawozdanie: Kryptosystem McEliece i Information Set Decoding

## 1. Kryptosystem McEliece

### 1.1. Historia i podstawy matematyczne

Kryptosystem McEliece został zaproponowany w 1978 roku przez Roberta McEliece'a. Jego konstrukcja wykorzystuje teorię kodów korekcyjnych, a dokładniej binarne kody Goppy.

System jest asymetryczny (wykorzystuje asymetrię klucza):

* **Klucz publiczny** służy do szyfrowania wiadomości.
* **Klucz prywatny** służy do deszyfrowania (odszyfrowywania) wiadomości.

Bezpieczeństwo systemu opiera się na fakcie, że dekodowanie losowego kodu liniowego (czyli odzyskanie oryginalnego słowa kodowego przy braku znajomości struktury kodu) jest problemem **NP-trudnym**.


### 1.2. Podstawy matematyczne

Niech $C \subseteq \mathbb{F}_2^n$ będzie binarnym kodem liniowym o długości $n$ oraz wymiarze $k$.

Macierz generująca ten kod ma postać:


$$G \in \mathbb{F}_2^{k \times n}$$

Dla wiadomości reprezentowanej jako wektor:


$$m \in \mathbb{F}_2^k$$

proces kodowania (bez szumu) odbywa się według wzoru:


$$c = mG$$

Podczas transmisji przez kanał z zakłóceniami dodawany jest wektor błędów:


$$e = (e_1, e_2, \dots, e_n)$$

Otrzymany szyfrogram (odebrany ciąg) $r$ definiuje równanie:


$$r = c + e = mG + e$$

gdzie:

* $c$ – poprawne słowo kodowe,
* $e$ – wektor błędów o wadze Hamminga $\text{wt}(e) \le t$ (gdzie $t$ to zdolność korekcyjna kodu),
* $r$ – odebrany ciąg (szyfrogram).


### 1.3. Generowanie kluczy

Generowanie pary kluczy przebiega następująco:

1. Wybierany jest konkretny binarny kod Goppy o parametrach $[n, k]$, zdolny do poprawienia $t$ błędów, reprezentowany przez macierz generującą $G$.
2. Generowane są dwie losowe macierze pomocnicze:
* $S \in \mathbb{F}_2^{k \times k}$ – losowa macierz odwracalna (nieosobliwa), służąca jako maskowanie (scrambler),
* $P \in \mathbb{F}_2^{n \times n}$ – losowa macierz permutacji.


3. Obliczana jest **publiczna macierz generująca** $G'$:

$$G' = SGP$$


* **Klucz publiczny:** $(G', t)$
* **Klucz prywatny:** $(S, G, P)$ wraz z wydajnym algorytmem dekodowania dla kodu $G$.


### 1.4. Proces szyfrowania

Szyfrowanie wiadomości $m \in \mathbb{F}_2^k$ za pomocą klucza publicznego polega na wykonaniu operacji:


$$c = mG' + e$$

gdzie:

* $m$ – tekst jawny (wiadomość),
* $G'$ – publiczna macierz generująca,
* $e$ – losowo wygenerowany wektor błędu o wadze Hamminga dokładnie $\text{wt}(e) = t$.

```
         Wiadomość (m)
               |
               v
     Pomnożenie przez G'
               |
               v
    Dodanie wektora błędu (e)
               |
               v
         Szyfrogram (c)

```


### 1.5. Proces odszyfrowywania

Odbiorca posiadający klucz prywatny $(S, G, P)$ wykonuje następujące kroki:

1. **Usuwanie permutacji:**
Odbiorca mnoży szyfrogram $c$ z prawej strony przez macierz odwrotną do permutacji $P^{-1}$:

$$r' = cP^{-1} = (mG' + e)P^{-1} = (mSGP + e)P^{-1} = (mS)G + eP^{-1}$$



Ponieważ $P$ jest macierzą permutacji, wektor błędu $e' = eP^{-1}$ ma dokładnie taką samą wagę Hamminga jak $e$ (czyli $\text{wt}(e') = t$).

2. **Dekodowanie:**
Odbiorca stosuje szybki algorytm dekodowania kodu Goppy (np. algorytm Pattersona) do wektora $r'$, usuwając błąd $e'$ i odzyskując słowo:

$$m' = mS$$


3. **Odzyskanie wiadomości:**
Odbiorca mnoży wynik przez $S^{-1}$, aby usunąć maskowanie:

$$m = m'S^{-1}$$



```
         Szyfrogram (c)
               |
               v
      Pomnożenie przez P⁻¹
               |
               v
  Dekodowanie kodu Goppy (usuwanie e')
               |
               v
    Otrzymanie zamaskowanego mS
               |
               v
      Pomnożenie przez S⁻¹
               |
               v
         Wiadomość (m)

```


## 2. Information Set Decoding (ISD)

### 2.1. Problem dekodowania kodów liniowych

Problem dekodowania syndromowego (lub ogólnego dekodowania kodów liniowych) można sformułować następująco:

Dany jest wektor $r \in \mathbb{F}_2^n$ oraz macierz parzystości $H$ (lub macierz generatora $G$). Należy znaleźć wektor błędu $e$ o wadze Hamminga:


$$\text{wt}(e) = t$$


taki, że:


$$r = c + e$$

W ogólnym przypadku (dla losowego kodu liniowego) problem ten jest **NP-trudny**, co stanowi podstawę bezpieczeństwa kryptosystemu McEliece.


### 2.2. Idea Information Set Decoding

Algorytmy z rodziny **Information Set Decoding (ISD)** stanowią najskuteczniejszą klasę ataków na kryptosystemy oparte na kodach. Ich działanie opiera się na koncepcji **zbioru informacyjnego** (ang. *information set*).

Zbiór informacyjny $I \subseteq \{1, 2, \dots, n\}$ o rozmiarze $k$ to taki zestaw indeksów kolumn macierzy $G'$, dla którego podmacierz $G'_I$ jest odwracalna.

> **Główna idea:** Jeśli wybierzemy zbiór $I$ o rozmiarze $k$ i okaże się, że na tych pozycjach w wektorze błędu $e$ nie ma żadnych błędów ($e_I = 0$), to możemy odzyskać wiadomość bezpośrednio z szyfrogramu:
> 
> $$m = c_I (G'_I)^{-1}$$
> 
> 

```
                Losowanie zbioru informacyjnego I
                               |
                               v
               Sprawdzenie, czy e_I zawiera błędy
                               |
                +--------------+--------------+
                |                             |
          [ Brak błędów ]                  [ Błędy ]
                |                             |
                v                             v
      Odzyskanie wiadomości              Kolejna próba
         (Koniec ataku)                (Nowa iteracja)

```


### 2.3. Algorytm Prange'a

Zaproponowany w 1962 roku przez Eugene'a Prange'a, jest najprostszą i pierwotną wersją algorytmu ISD. Zakłada on najbardziej restrykcyjny scenariusz – poszukuje zbioru informacyjnego całkowicie wolnego od błędów.

Prawdopodobieństwo sukcesu w pojedynczej iteracji wynosi:


$$P = \frac{\binom{n-t}{k}}{\binom{n}{k}}$$

Średnia liczba wymaganych iteracji do znalezienia poprawnego zbioru to:


$$N = \frac{1}{P}$$

**Kroki algorytmu:**

1. Wylosuj zbiór $I \subset \{1, \dots, n\}$ o rozmiarze $k$.
2. Sprawdź, czy podmacierz $G'_I$ jest odwracalna. Jeśli nie, wróć do kroku 1.
3. Wyznacz potencjalną wiadomość $m^* = r_I (G'_I)^{-1}$.
4. Oblicz wektor błędu $e^* = r - m^* G'$.
5. Jeśli $\text{wt}(e^*) = t$, to $m = m^*$ (sukces). W przeciwnym wypadku wróć do kroku 1.


### 2.4. Złożoność obliczeniowa

Koszt klasycznego algorytmu ISD można oszacować asymptotycznie jako:


$$T(n) \approx \frac{\binom{n}{t}}{\binom{n-k}{t}}$$

Algorytmy ISD charakteryzują się **wykładniczą złożonością obliczeniową**. Do dziś nie istnieje żaden algorytm wielomianowy zdolny rozwiązać problem dekodowania losowych kodów liniowych.


## 3. Znaczenie ISD dla bezpieczeństwa McEliece

Algorytmy ISD stanowią kluczowy punkt odniesienia przy wyznaczaniu parametrów kryptosystemu McEliece. Ponieważ nie znamy skuteczniejszych ataków strukturalnych na binarne kody Goppy, o bezpieczeństwie systemu decyduje odporność na ataki typu message-recovery realizowane za pomocą ISD.

## 4. Zalety i wady kryptosystemu McEliece

### Zalety

* **Odporność postkwantowa:** Brak podatności na algorytm Shora.
* **Szybkie szyfrowanie i deszyfrowanie:** Operacje opierają się na prostym mnożeniu macierzy i wektorów w ciele dwuelementowym, co jest niezwykle wydajne obliczeniowo.
* **Długoletnia historia badań:** Od 1978 roku konstrukcja oparta na binarnych kodach Goppy nie została złamana.

### Wady

* **Ogromny rozmiar klucza publicznego:** Wymaga przechowywania od kilkuset kilobajtów do ponad megabajta danych, co obciąża pasmo sieciowe i pamięć.

---

## 5. Podsumowanie

Kryptosystem McEliece pozostaje jednym z najbardziej stabilnych i bezpiecznych filarów kryptografii postkwantowej. Algorytmy Information Set Decoding (ISD) są najważniejszym narzędziem służącym do weryfikacji tej odporności. Każda nowa optymalizacja w rodzinie algorytmów ISD bezpośrednio wpływa na konieczność korekty parametrów i rozmiarów kluczy w standardach McEliece.

---

## Bibliografia

* **[1]** R. J. McEliece, "A public-key cryptosystem based on algebraic coding theory," *Deep Space Network Progress Report*, vol. 44, pp. 114–116, Jan. 1978.
* **[2]** E. Prange, "The use of information sets in decoding cyclic codes," *IRE Transactions on Information Theory*, vol. 8, no. 5, pp. 5–9, Sep. 1962.
* **[3]** D. J. Bernstein, T. Chou, and P. Schwabe, "Classic McEliece: Conservative code-based cryptography," *NIST Post-Quantum Cryptography Standardization Project*, Round 3 Submission, Oct. 2020.