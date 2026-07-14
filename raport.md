# Pracownia Problemowa – Raport z wykonania projektu<br>„Information Set Decoding jako technika ataku na kryptosystemy kodowe – przegląd metod i demonstrator ataku”

**Autor:** Piotr Sielchanowicz

**Data:** 13 lipca 2026 r.

---

## 1. Kryptosystem McEliece

Kryptosystem McEliece (zaproponowany w 1978 r.) to asymetryczny algorytm oparty na teorii kodów korekcyjnych (binarnych kodach Goppy). Stanowi on jeden z kluczowych i najbardziej stabilnych filarów kryptografii postkwantowej, wykazując pełną odporność na kwantowy algorytm Shora. Bezpieczeństwo systemu opiera się na fakcie, że dekodowanie losowego kodu liniowego bez znajomości jego struktury (odzyskanie oryginalnego słowa kodowego) jest problemem NP-trudnym.

* **Generowanie kluczy:** Wybierany jest kod Goppy o parametrach $[n, k]$, zdolny do korekcji $t$ błędów, reprezentowany przez binarną macierz generującą $G$. Klucz prywatny stanowi trójka $(S, G, P)$, gdzie $S \in \mathbb{F}_2^{k \times k}$ to losowa macierz odwracalna maskująca strukturę kodu, a $P \in \mathbb{F}_2^{n \times n}$ to losowa macierz permutacji. Kluczem publicznym jest zamaskowana macierz generująca $G' = SGP$ oraz parametr zdolności korekcyjnej $t$.


* **Szyfrowanie i deszyfrowanie:** Szyfrowanie wiadomości $m \in \mathbb{F}_2^k$ polega na obliczeniu szyfrogramu $c = mG' + e$, gdzie $e$ to losowy wektor błędu o wadze Hamminga dokładnie $\text{wt}(e) = t$. Odbiorca posiadający klucz prywatny zdejmuje permutację za pomocą macierzy odwrotnej ($cP^{-1} = (mS)G + eP^{-1}$), co zachowuje wagę błędu ($e' = eP^{-1}$, $\text{wt}(e') = t$). Następnie szybki algorytm dekodowania kodu Goppy usuwa błąd, odzyskując słowo $m' = mS$, które po pomnożeniu przez $S^{-1}$ daje tekst jawny $m$. Główną wadą systemu pozostaje bardzo duży rozmiar klucza publicznego.



---

## 2. Atak Information Set Decoding (ISD) i Algorytm Prange'a

Algorytmy z rodziny Information Set Decoding stanowią najskuteczniejszą znaną klasę ataków typu message-recovery na McEliece'a. Ich działanie opiera się na koncepcji zbioru informacyjnego $I \subseteq \{1, \dots, n\}$ o rozmiarze $k$, dla którego podmacierz publiczna $G'_I$ jest odwracalna.

* **Główna idea:** Jeżeli na pozycjach należących do zbioru $I$ w wektorze błędu $e$ nie wystąpiły żadne przekłamania ($e_I = 0$), wiadomość można odzyskać wprost z szyfrogramu: $m = c_I (G'_I)^{-1}$.


* **Algorytm Prange'a:** Najstarszy wariant ISD (1962 r.) – wyszukuje podzbiór całkowicie wolny od błędów. Złożoność algorytmu jest wykładnicza i zależy od prawdopodobieństwa sukcesu w pojedynczej próbie: $P = \binom{n-t}{k}/\binom{n}{k}$. Odporność na te ataki decyduje o doborze bezpiecznych parametrów współczesnych instancji McEliece'a.



---

## 3. Demonstrator Ataku (Opis Implementacji)

W ramach projektu zaprojektowano i zaimplementowano funkcjonalny demonstrator ataku Prange'a w języku Python przy użyciu biblioteki `galois`. Demonstrator realizuje pełen scenariusz kryptograficzny na małym ciele Galois $\mathbb{F}_{16}$ (GF($2^4$)) dla kodu Goppy o parametrach $n=16$, $t=2$ oraz dynamicznie wyznaczanym wymiarze $k=8$:

1. **Generowanie struktur:** Program losuje wielomian Goppy $g(x)$ stopnia $t=2$ nad $\mathbb{F}_{16}$, tworzy binarną macierz weryfikacji parzystości $H_{bin}$, wyznacza jej jądro jako binarną macierz generującą $G$ oraz generuje losowe macierze maskujące $S$ i permutacji $P$ w celu wyznaczenia klucza publicznego $G_{pub}$.


2. **Szyfrowanie i deszyfrowanie:** Wiadomość $m$ zostaje zaszyfrowana za pomocą $G_{pub}$ z dodaniem losowego wektora błędu o wadze $t$. Prawidłowość implementacji kodu Goppy potwierdzono pomyślnym testem dekodowania kluczem prywatnym przez przeszukanie przestrzeni syndromów.


3. **Atak Prange'a:** W pętli losuje podzbiór indeksów o długości $k$, weryfikuje odwracalność podmacierzy $G_I$, oblicza kandydata na wiadomość $m^* = c_I (G_I)^{-1}$ oraz testuje wagę wektora błędu $e^* = c - m^* G_{pub}$. Atak kończy się sukcesem w momencie odnalezienia błędu o wadze dokładnie równej $t$.



Demonstrator pomyślnie i bezbłędnie odzyskuje oryginalną wiadomość w czasie ułamka sekundy, ilustrując praktyczną wykonalność oraz mechanizm działania algorytmów ISD na mniejszych systemach kodowych.