# Parsing for Belief Statements

## Project Description

This project focuses on the parsing and transformation of probabilistic assignments into ASP format. The goal is to process an input containing probabilistic assignments, verify its syntactic correctness according to a predefined format, and finally transform it into an ASP-compliant format.

- **Parsing**: Parsing refers to the process of analyzing and breaking down an input into an organized structure following precise rules defined by a grammar. In this project, the Lark library is used.
- **Lark**: A Python library designed to create parsers. It allows transforming the syntax tree (organized structure) into Python objects through tools for defining grammars.
- **ASP**: Parsing into ASP translates the program into an internal representation for the ASP solver, which is used to compute the answer sets.
- **Answer set**: Solutions that satisfy the rules and constraints of the program.

### Technologies Used
- **Lark**: For grammar definition and input parsing.
- **Custom Modules**: For transformations, assignment handling, and ASP logic.
- **Python**: Programming language used to develop the project.

---

## `grammar.lark` File Structure

The `grammar.lark` file defines the grammar used for parsing probabilistic assignments. 
Details:

### Main Rules
- **`start`**: The main entry point of the grammar.
  ```
  ?start: assignment_list
- **`assignment_list`**: A list of assignments separated by **`;`**.
  ```
  assignment_list: assignment (";" assignment)*
- **`assignment`**: A single assignment with a list of facts and a probability value.
  ```
  assignment: "{" fact_list "}" ":" FLOAT
- **`fact_list`**: A list of facts separated by **`,`**.
  ```
  fact_list: fact ("," fact)*
- **`fact`**:  A fact that can be simple or with arguments.
  ```
  ?fact: atom ("(" argument_list ")")?
- **`atom`**:  An identifier representing a name or an integer.
  ```
  atom: NAME | INT
- **`FLOAT`**: A decimal number representing a probability value between 0 and 1.
  ```
  FLOAT: DIGIT+ ("." DIGIT+)?
- Ignored rules: The grammar ignores spaces, tabs, and newlines.
  ```
  %ignore " "
  %ignore "\\t"
  %ignore "\\n"  
## File Functionalities
#### **`file_processor.py`**
- Reads input files, normalizes the lines, parses them, transforms the results into probabilistic facts and ASP rules, and saves the output to `output.txt`.

#### **`belief_parser.py`**
- Defines the logic for parsing using the grammar specified in **`grammar.lark`**. Converts valid segments into Python objects like **`assignment`** and **`fact`**.

#### **`transformer_module.py`**
- Implements the logic for transforming **`assignment`** objects into probabilistic facts and ASP rules. Manages conditional probability calculations and generates output following ASP syntax.

#### **`assignment.py`**
- Represents a single probabilistic assignment and includes methods for validating and representing the assignment.

#### **`assignment_list.py`**
- Manages a list of assignments. Provides methods to check if the list is empty and to iterate over the assignments.

#### **`fact.py`**
- Defines the structure of a fact, supporting both simple and composite facts. Includes methods for textual and normalized representation.

#### **`parser_module.py`**
- Contains helper functions for parsing and data transformation. Acts as an intermediary between parsing and ASP transformations.

#### **`main.py`**
- The program's entry point. Initializes the **`FileProcessor`** and starts the process of handling input and output files.

---

## Parsing Example
- For the input **`{red}:0.3`**, the grammar produces the following syntax tree:
  ```plaintext
  assignment_list
    assignment
      fact_list
        fact
          atom: "red"
      FLOAT: "0.3"
  ```

## Detailed Process 
#### Example Input
``` {red}:0.3 ; {blue}:0.1 ; {blue,yellow}:0.6. ```

### Step 1:
#### File Involved: **`file_processor.py`**
1. The input is read, and unnecessary spaces are removed.
2. The input is checked to ensure it ends with **`.`**.

### Step 2:
#### Files Involved:
- **`belief_parser.py`**
- **`grammar.lark`**

1. The input is split into assignments separated by **`;`**.
2. The assignments are analyzed using a specific grammar defined in **`grammar.lark`**.
3. Valid segments are identified and transformed into Python objects (e.g., **`fact`**).
4. Syntax errors are recorded.

#### Intermediate Output:
 ```
Valid segments:
- {red}:0.3
- {blue}:0.1
- {blue,yellow}:0.6

No invalid segments found.
  ```

### Step 3: Transformation into Probabilistic Facts
#### File Involved: **`transformer_module.py`**
1. Each valid assignment is transformed into a probabilistic fact, with conditional probability calculations:
   
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
2. Probabilistic facts are generated:
```
  0.300000000::redf.
  0.142857143::bluef.
  1.000000000::blue_yellowf.
```
#### Intermediate Output:
```
0.300000000::redf.
0.142857143::bluef.
1.000000000::blue_yellowf
```

### Step 4: Generation of ASP Rules
#### File Involved: **`transformer_module.py`**
1. ASP rules are generated to model logical relationships between facts.
2. Example rules:
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

3. Combined rules are created:
```
   blue;yellow:- blue_yellow.
```
#### Intermediate Output:
```
red:- redf.
blue:- not redf, bluef.
blue_yellow:- not redf, not bluef.
blue;yellow:- blue_yellow.
```

### Passo 5: Final Output:

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

## Examples of Input and Output
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
red:- redf.
blue:- not redf, bluef.
blue_yellow:- not redf, not bluef.
blue;yellow:- blue_yellow.

Output riga 2:
0.500000000::af.
0.600000000::a_bf.
a:- af.
a_b:- not af, a_bf.
a;b :- a_b.
a_b_c:- not af, not a_bf.
a;b;c:- a_b_c.

Output riga 3:
0.300000000::redf.
0.142857143::bluef.
red:- redf.
blue:- not redf, bluef.
% La riga '{invalid_input}.' non rispetta la grammatica.

Output riga 4:
0.800000000::bluef.
blue:- bluef.
% La riga '{red}:1.2.' non rispetta la grammatica.

Output riga 5:
0.333000000::alphaf.
0.998500750::betaf.
alpha:- alphaf.
beta:- not alphaf, betaf.

Output riga 6:
0.500000000::f_xf.
0.600000000::f_x_yf.
f_x:- f_xf.
f_x_y:- not f_xf, f_x_yf.
f_f_x:- not f_xf, not f_x_yf.
f;f;x:- f_f_x.

Output riga 7:
0.200000000::af.
0.375000000::bf.
0.200000000::cf.
0.500000000::df.
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
f_a:- f_af.
f_b:- not f_af, f_bf.
f_c:- not f_af, not f_bf, f_cf.
f_a_b:- not f_af, not f_bf, not f_cf, f_a_bf.
f_a_b_c:- not f_af, not f_bf, not f_cf, not f_a_bf.
f;a;b;c:- f_a_b_c.
```


