# Parsing per belief statements

## Descrizione del Progetto

Questo progetto si occupa del parsing e della trasformazione di assegnamenti probabilistici in formato ASP. Ha l'obiettivo di elaborare un input che contiene assegnamenti probabilistici, verificarne la correttezza sintattica, che rispetti il formato, e infine trasformarlo in un formato ASP. 

 - **Parsing**: Per parsing intendiamo un processo di analisi e scomposizione di un input, in una struttura organizzata, seguendo regole precise definite da una grammatica. Nel caso in oggetto è stato scelto Lark.
 - **Lark**: Libreria python progettata per creare parser. Permette di trasformare l'albero sintattico (struttura organizzata) in oggetti python, mediante strumenti che permettono di definire grammatiche.
 - **ASP**: Il parsing in ASP traduce il programma in una rappresentazione interna per il solver ASP che utilizza per calcolare gli answer set
 - **Answer set**: Soluzioni che soddisfano le regole e i vincoli del programma

### Tecnologie Utilizzate
- **Lark**: Per la definizione della grammatica e il parsing dell' input.
- **Moduli Personalizzati**: Implementano trasformazione, gestione degli assegnamenti, e la logica ASP.
- **Python**: Linguaggio utilizzato per sviluppare il progetto.

---

## Struttura del File `grammar.lark`

Il file `grammar.lark` definisce la grammatica utilizzata per il parsing degli assegnamenti probabilistici. 
Descrizione:

### Regole Principali
- **`start`**: Punto di ingresso principale della grammatica.
  ```
  ?start: assignment_list

- **`assignment_list`**: Una lista di assegnamenti separati da **`;`**.
  ```
  assignment_list: assignment (";" assignment)*

- **`assignment`**: Un singolo assegnamento con una lista di fatti e un valore di probabilità.
  ```
  assignment: "{" fact_list "}" ":" FLOAT

- **`fact_list`**: Una lista di fatti separati da **`,`**.
  ```
  fact_list: fact ("," fact)*

- **`fact`**:  Un fatto che può essere semplice o con argomenti.
  ```
  ?fact: atom ("(" argument_list ")")?

- **`atom`**:  Un identificatore che rappresenta un nome o un numero intero.
  ```
  atom: NAME | INT

- **`FLOAT`**: Un numero decimale che rappresenta un valore di probabilità compreso tra 0 e 1.
  ```
  FLOAT: DIGIT+ ("." DIGIT+)?

- Regole di Ignoranza: La grammatica ignora spazi, tabulazioni e nuove righe.
  ```
  %ignore " "
  %ignore "\\t"
  %ignore "\\n"
  
## Funzionalità dei singoli file
#### **`file_processor.py`**
- Legge i file input, normalizza le righe, effettua il parsing, trasforma i risultati in fatti probabilistici e regole ASP. Salva l'output in output.txt

#### **`belief_parser.py`**
-  Definisce la logica per il parsing usando la grammatica definita in **`grammar.lark`**. Converte i segmenti validi in oggetti Python come **`assignment`** e **`fact`**
 
#### **`transformer_module.py`**
- Implementa la logica per trasformare gli oggetti **`assignment`** in fatti probabilistici e regole ASP. Gestisce calcoli di probabilità condizionali e genera output che segue la sintassi ASP.

#### **`assignment.py`**
- Rappresenta un singolo assegnamento probabilistico e comprende metodi per validare e rappresentare l'assegnamento.

#### **`assignment_list.py`**
- Gestisce una lista di assegnamenti. Fornisce metodi per verificare se la lista è vuota e per iterare sugli assegnamenti.

#### **`fact.py`**
- Definisce la struttura di un fatto, con supporto per fatti semplici e composti. Include metodi per la rappresentazione testuale e normalizzata.

#### **`parser_module.py`**
- Contiene funzioni di supporto per il parsing e la trasformazione dei dati. Fa l'intermediario fra il parsing e le trasformazioni ASP.

#### **`main.py`**
- Punto di ingresso del programma. Inizializza il **`FileProcessor`** e avvia il processo di elaborazione dei file di input e output.

  ---

## Esempio di parsing
 - Per l'input **`{red}:0.3`**, la grammatica produce il seguente albero sintattico:
  ```
 assignment_list
  assignment
    fact_list
      fact
        atom: "red"
    FLOAT: "0.3"


```

## Processo Dettagliato 
#### Input di esempio
``` {red}:0.3 ; {blue}:0.1 ; {blue,yellow}:0.6. ```

### Passo 1:
#### File Coinvolto: **`file_processor.py`**
 1. L'input viene letto e vengono rimossi gli spazi superflui
 2. Controllo che l'input termini con **`.`**

### Passo 2:
#### File Coinvolti:
 - **`belief_parser.py`**
 - **`grammar.lark`**

1. L'input viene diviso in assegnamenti separtai da **`;`**
2. Gli assegnamenti vengono analizzati da una grammatica specifica che viene definita in **`grammar.lark`**
3. Vengono identificati i segmenti validi e trasformati in oggetti python (es . **`fact`**)
4. Infine, vengono registrati gli errori sintattici

#### Output Intermentio:
 ```
Segmenti validi:
- {red}:0.3
- {blue}:0.1
- {blue,yellow}:0.6

Nessun segmento non valido.
  ```

### Passo 3: Trasformazione in fatti probabilistici
#### File coinvolto: **`transformer_module.py`**
 1. Ogni singolo assegnamento, se valido, viene trasformato in un fatto probabilistico, con successivo calcolo della probabilità condizionale
- **`{red}:0.3`**:
  ```
   0.3 / 1.0 = 0.300000000
  ```
- **`{blue}:0.1`**:
  ```
   0.1 / (1 - 0.3) = 0.142857143
  ```
- **`{blue,yellow}:0.6`**:
  ```
   0.6 / (1 - 0.3 - 0.1) = 1.000000000
  ```
2. Vengono generati i fatti probabilistici
```
  0.300000000::redf.
  0.142857143::bluef.
  1.000000000::blue_yellowf.
```
#### Output Intermedio:
```
0.300000000::redf.
0.142857143::bluef.
1.000000000::blue_yellowf
```

### Passo 4: Generazione delle regole ASP
#### File coinvolto: **`transformer_module.py`**
 1. Vengono generate le regole ASP per modellare le relazioni logiche fra i fatti
 2. Come da esempio:
- **`{red}`**:
  ```
   red:- redf.
  ```
- **`{blue}`**:
  ```
   blue:- not redf, bluef.
  ```
- **`{blue,yellow}`**:
  ```
   blue_yellow:- not redf, not bluef.
  ```

3. Si creano le regole combinate:
```
   blue;yellow:- blue_yellow.
```
#### Output Intermedio:
```
red:- redf.
blue:- not redf, bluef.
blue_yellow:- not redf, not bluef.
blue;yellow:- blue_yellow.
```

### Passo 5: Output finale:

```
Output riga 1:
0.300000000::redf.
0.142857143::bluef.
1.000000000::blue_yellowf.
red:- redf.
blue:- not redf, bluef.
blue_yellow:- not redf, not bluef.
blue;yellow:- blue_yellow.
```

## Esempi di Input e Output
### Input:

 ```
{red}:0.3; {blue}:0.1; {blue,yellow}:0.6.
{a}:0.5; {a,b}:0.3; {a,b,c}:0.2.
{red}:0.3; {blue}:0.1; {invalid_input}.
{red}:1.2; {blue}:0.8.
{alpha}:0.333; {beta}:0.666.
{f(x)}:0.5; {f(x,y)}:0.3; {f(f(x))}:0.2.
{a}:0.2; {b}:0.3; {c}:0.1; {d}:0.2; {e}:0.2.
{f(x)}:0.2; {f(y)}:0.3; {f(z)}:0.1; {f(x,y)}:0.2; {f(x,z)}:0.2.
{f(a)}:0.2; {f(b)}:0.2; {f(c)}:0.2; {f(a,b)}:0.2; {f(a,b,c)}:0.2.
```

### Output:
 ```
Output riga 1:
0.300000000::redf.
0.142857143::bluef.
1.000000000::blue_yellowf.
red:- redf.
blue:- not redf, bluef.
blue_yellow:- not redf, not bluef.
blue;yellow:- blue_yellow.

Output riga 2:
0.500000000::af.
0.600000000::a_bf.
1.000000000::a_b_cf.
a:- af.
a_b:- not af, a_bf.
a_b_c:- not af, not a_bf.
a;b;c:- a_b_c.

Output riga 3:
0.300000000::redf.
0.142857143::bluef.
red:- redf.
blue:- not redf.
blue:- blue.
% La riga '{invalid_input}.' non rispetta la grammatica.

Output riga 4:
0.800000000::bluef.
blue:- bluef.
blue:- blue.
% La riga '{red}:1.2.' non rispetta la grammatica.

Output riga 5:
0.333000000::alphaf.
0.998500750::betaf.
alpha:- alphaf.
beta:- not alphaf.
beta:- beta.

Output riga 6:
0.500000000::f_xf.
0.600000000::f_x_yf.
1.000000000::f_f_xf.
f_x:- f_xf.
f_x_y:- not f_xf, f_x_yf.
f_f_x:- not f_xf, not f_x_yf.
f;f;x:- f_f_x.

Output riga 7:
0.200000000::af.
0.375000000::bf.
0.200000000::cf.
0.500000000::df.
1.000000000::ef.
a:- af.
b:- not af, bf.
c:- not af, not bf, cf.
d:- not af, not bf, not cf, df.
e:- not af, not bf, not cf, not df.
e:- e.

Output riga 8:
0.200000000::f_xf.
0.375000000::f_yf.
0.200000000::f_zf.
0.500000000::f_x_yf.
1.000000000::f_x_zf.
f_x:- f_xf.
f_y:- not f_xf, f_yf.
f_z:- not f_xf, not f_yf, f_zf.
f_x_y:- not f_xf, not f_yf, not f_zf, f_x_yf.
f_x_z:- not f_xf, not f_yf, not f_zf, not f_x_yf.
f;x;z:- f_x_z.

Output riga 9:
0.200000000::f_af.
0.250000000::f_bf.
0.333333333::f_cf.
0.500000000::f_a_bf.
1.000000000::f_a_b_cf.
f_a:- f_af.
f_b:- not f_af, f_bf.
f_c:- not f_af, not f_bf, f_cf.
f_a_b:- not f_af, not f_bf, not f_cf, f_a_bf.
f_a_b_c:- not f_af, not f_bf, not f_cf, not f_a_bf.
f;a;b;c:- f_a_b_c.
```


