Micut Andrei-Ion
Grupa 331CB

LFA Tema 2 - Subset Construction - AFN -> AFD



Pentru realizarea temei s-a aplicat algoritmul Subset Construction prezentat la curs.

Pentru reprezentarea structurilor de AFN si AFD s-au folosit modulele (cu clasele)

deja existente, fiind utilizate doar atributele aflate in cele 2 clase.



Pentru generarea structurii de AFN pornind de la un text se foloseste functia textToNFA.

Aceasta functie parseaza textul si pe baza structurii oferite in cerinta creaza si

populeaza atributele necesare unui AFN (alfabet, tranzitii, stari, stare initiala, stari

finale).



Pentru transformarea unei structuri de AFD in text se foloseste functia DFAtoText care

construieste intr-un buffered string StringIO descrierea text a AFD-ului conform cerintei.



Functia care realizeaza conversia si aplica algoritmul Subset Construction se numeste

NFAtoDFA. Pornind de la starea initiala, pentru obtinerea multimii de stari ce va

reprezenta o stare in AFD se aplica EpsilonClosure pe starea initiala a AFN-ului.

Pentru a mentine o mapare intre un set de stari si un numar de stare (ID-ul starii ce va

fi folosit de AFD) se foloseste un dictionar ce are ca si cheie frozenset si returneaza

ca valoare un intreg. Pe masura ce noi seturi distincte sunt descoperite, li se atribuie

un unic numar de stare (un intreg).

Functia porneste din starea initiala, expandeaza cu ajutorul EpsilonClosure, iar apoi

genereaza noi stari in functie de tranzitiile disponibile din acele stari. Starile

noi generate sunt salvate intr-o coada (lista din care se insereaza si extrage ordonat)

pentru a fi procesate (expandate la randul lor). Se verifica tot timpul ca nu cumva sa

se intalneasca o stare deja, moment in care nu se va adauga in coada deoarece acea cale

a fost deja expandata.

La final, dupa terminarea tuturor cailor, se creaza un SINK_STATE si se adauga toate

tranzitiile necesare pentru a face DELTA totala.



Functia EpsilonClosure realizeaza inchiderea epsilon (obtine multimea starilor la care se

poate ajunge prin tranzitii pe "eps"). Functia primeste:

- states = starile pe care se doreste sa se faca expandarea

- nfa = nfa-ul din care fac parte starile

- known = starile care au fost intalnite la un moment dat pentru a nu incerca o noua expandare a unei stari, daca aceasta a fost expandata anterior.

Functia itereaza prin setul de stari, si pentru fiecare stare se cauta starile in care

se poate ajunge dintr-o tranzitie pe "eps". Se verifica cate din starile obtinute sunt

noi (nu sunt cunoscute) si se apeleaza recursiv EpsilonClosure pentru starile care sunt

noi.





Fluxul principal al programului citeste NFA-ul din fisierul text, face conversia apeland DFAtoText, iar apoi scrie DFA-ul obtinut in fisierul de iesire cu ajutorul

DFAtoText.