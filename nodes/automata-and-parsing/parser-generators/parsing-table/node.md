---
tag: JQ131J
kind: data-structure
slug: parsing-table
name: Parsing table
aliases:
- action and goto table
- predictive parse table
area: automata-and-parsing/parser-generators
level: core
summary: The table that maps a parser state and lookahead symbol to a shift, reduce, goto, accept or error action.
model: word-ram
complexity:
  vars: {N: the number of rows, σ: the number of columns, a: the number of actions already in the cell, k: the number of conflicting cells}
  time: {add: O(a), lookup: O(1), resolve: O(k log k)}
  space: {total: Θ(N σ)}
history:
  year: 1965
  people: [Donald E. Knuth]
  note: Knuth's LR(k) parser chooses each move from its state and the next k symbols; the generators that followed, yacc among them, store these choices as a table over states and symbols, and LL(1) generators use the same kind of table over nonterminals and tokens.
prereqs: [context-free-grammar, shift-reduce-parsing, first-and-follow-sets]
see_also: [lr-parse-table, ll-parse-table, parser-table-construction, parse-table-compression, yacc, shift-reduce-conflict, reduce-reduce-conflict, glr-parsing]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.4.4, Nonrecursive Predictive Parsing (the table M and its driver); Section 4.6.3, The LR-Parsing Algorithm (the ACTION and GOTO functions); Section 4.8, Using Ambiguous Grammars (resolving conflicts in the table)
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639 (the LR(k) parser that chooses its move from its state and the next k symbols)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition
    locator: Chapter 8, Deterministic Top-Down Parsing, and Chapter 9, Deterministic Bottom-Up Parsing (the parse tables of LL(1) and LR parsers)
---

A parsing table is the two-dimensional table that a table-driven parser consults at every step: a row for each parser state, or for each nonterminal in a top-down parser, a column for each lookahead symbol, and in each cell the action to take. One fixed driver loop runs every language; the grammar enters only through the table. While a [parser generator](/parser-generator/) fills the table, a cell can receive two different actions, and the table records this as a *conflict*, which the generator reports or resolves. This page treats the structure common to [LR parse tables](/lr-parse-table/) and [LL parse tables](/ll-parse-table/): its cells, its conflict record, and the drivers that read it.

## In plain words

Think of a grid. The parser always knows which row it is in, because the row is its current state, and it knows which column to look at, because the column is the next token. The box where the two meet says what to do: read the token and move to another row, replace some symbols by a rule's name, stop with success, or, if the box is empty, report an error.

The builder fills the boxes from the grammar. If it ever wants to write two different things into one box, the grammar is unclear for this kind of parser, and the box is marked. Before the parser can run, every marked box must be settled, by changing the grammar or by a rule that keeps one of the two.

## The abstract type

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The end marker is $\$$. For LR tables the grammar is augmented with $S' \to S$ as production 0.

A parsing table has a set $R$ of rows, a list $C$ of column symbols, and for each cell $(r, c)$ a finite set $T[r, c]$ of actions; the empty set means error. The actions are:

- in an LR table, $\mathrm{shift}\ q$ and $\mathrm{reduce}\ p$ in terminal columns, $\mathrm{accept}$ in the column of $\$$, and $\mathrm{goto}\ q$ in nonterminal columns, with rows the states of an LR automaton;
- in an LL(1) table, $\mathrm{predict}\ p$, with rows the nonterminals.

A cell with two or more actions is a *conflict*: a [shift-reduce conflict](/shift-reduce-conflict/), a [reduce-reduce conflict](/reduce-reduce-conflict/), or two predictions. The operations are:

- $\mathrm{ADD}(r, c, x)$: add action $x$ to the cell $(r, c)$;
- $\mathrm{LOOKUP}(r, c)$: return $T[r, c]$;
- $\mathrm{CONFLICTS}()$: list the cells with two or more actions;
- $\mathrm{RESOLVE}(\mathit{choose})$: replace each conflicting cell by the single action, or none, that a policy picks;
- the driver, which reads the table, defined for LR tables below and for LL tables on the [LL(1) parsing](/ll1-parsing/) page.

A table is *deterministic* when it has no conflicts; only then does the driver have exactly one move at each step.

## Representation

- **Dense grid.** An array of $N$ rows by $\sigma$ columns, with symbols mapped to column numbers once. A cell holds an empty tuple, one action, or a short tuple of actions in a conflict. A set of conflicting positions is kept beside the grid so that CONFLICTS and RESOLVE do not scan all cells. The implementation on this page uses this form.
- **Encoded integers.** Real generators store each deterministic cell as one small integer, for example $+q$ for shift $q$, $-p$ for reduce by $p$, and 0 for error, and keep production lengths and left sides in two separate arrays.
- **Compressed.** Most cells are empty or repeat a default reduction, so production tables are stored with default actions, shared rows and rows packed into one array with offsets; see [parse table compression](/parse-table-compression/).
- **Sets kept.** A [GLR](/glr-parsing/) parser keeps the conflicting cells as they are and follows all their actions.

## Operations

```pseudo id=main
ADD(T, r, c, x)
L1  if T[r, c] is empty then T[r, c] ← (x)
L2  else if x is not in T[r, c] then append x to T[r, c]; add (r, c) to T.conflicts
LOOKUP(T, r, c)
L3  return T[r, c]                                   ▷ empty means error
RESOLVE(T, choose)
L4  for each (r, c) in T.conflicts, in order do
L5      T[r, c] ← (choose(r, c, T[r, c]))            ▷ or empty, if choose gives none
L6  T.conflicts ← ∅
DRIVE-LR(T, tokens)                                   ▷ T deterministic; tokens followed by $
L7  stack ← (0); a ← the first token
L8  loop: x ← the action in LOOKUP(T, top of stack, a); if none then return reject
L9      if x = shift q then push q; a ← the next token
L10     if x = reduce A → β then pop |β| states; push the q of goto q in LOOKUP(T, top of stack, A)
L11     if x = accept then return accept
```

ADD never loses an action: it either fills an empty cell or extends a cell and marks it. A filling procedure, such as the SLR(1) or LALR(1) construction, calls ADD once for each action that its rules assign; the table it leaves behind records every disagreement of those rules. The LL(1) driver keeps a stack of grammar symbols instead of states: with a nonterminal $A$ on top it replaces $A$ by the right side of the predicted production, and with a terminal on top it matches it against the input.

## Example

**An LR table.** For $E \to E + n \mid n$, augmented with $S' \to E$ as production 0, so that $E \to E + n$ is production 1 and $E \to n$ is production 2, the SLR(1) construction fills 9 cells of a table with 5 rows and the columns $+$, $n$, $\$$, $E$:

| state | $+$ | $n$ | $\$$ | $E$ |
|---|---|---|---|---|
| 0 | | shift 2 | | goto 1 |
| 1 | shift 3 | | accept | |
| 2 | reduce 2 | | reduce 2 | |
| 3 | | shift 4 | | |
| 4 | reduce 1 | | reduce 1 | |

DRIVE-LR on $n + n$:

| stack | input | action |
|---|---|---|
| 0 | $n + n\ \$$ | shift 2 |
| 0 2 | $+ n\ \$$ | reduce 2 ($E \to n$), goto 1 |
| 0 1 | $+ n\ \$$ | shift 3 |
| 0 1 3 | $n\ \$$ | shift 4 |
| 0 1 3 4 | $\$$ | reduce 1 ($E \to E + n$), pop 3 states, goto 1 |
| 0 1 | $\$$ | accept |

**An LL table for the same language.** $E \to n\,E'$ (production 0), $E' \to + n\,E'$ (1), $E' \to \varepsilon$ (2) gives a table with rows $E$ and $E'$ and three filled cells: $T[E, n] = \mathrm{predict}\ 0$, $T[E', +] = \mathrm{predict}\ 1$, $T[E', \$] = \mathrm{predict}\ 2$.

**A conflict and its resolution.** For the ambiguous $E \to E + E \mid n$ the SLR(1) construction calls ADD twice on the cell of state 4, which holds $E \to E + E \cdot$ and $E \to E \cdot + E$, and the column $+$: first with shift 3, then with reduce 1. CONFLICTS returns that one cell. RESOLVE with the policy "keep the reduction" makes $+$ left-associative, and the driver then accepts $n + n + n$ by reducing the first $n + n$ before it reads the second $+$.

## Correctness

The proof in [correctness](proofs/correctness.md) shows two things. First, the cell contents and the conflict record are exact: after any sequence of ADD calls, $T[r, c]$ is the list of distinct actions added to the cell in the order of their first addition, and the conflict set is the set of cells that received two or more distinct actions; after RESOLVE no cell has more than one action. Second, the LR driver is sound for every deterministic table filled from the LR(0) automaton of the grammar, whatever the lookaheads and whatever the resolution policy: if it accepts $w$ then $w \in L(G)$. The converse needs the lookaheads of a correct construction and is proved on the pages of [SLR](/slr-parsing/), [LALR](/lalr-parsing/) and [canonical LR](/canonical-lr-parsing/) parsing.

## Complexity

- **ADD** costs $O(a)$, where $a$ is the number of actions already in the cell, which is 0 or 1 except in a conflict; with symbols mapped to column numbers once, this is $O(1)$ for a deterministic table.
- **LOOKUP** is one array access, $O(1)$.
- **RESOLVE** sorts the $k$ conflicting positions for a deterministic report order and calls the policy once per cell: $O(k \log k)$ plus the cost of the policy.
- **Space** is $\Theta(N \sigma)$ for the dense grid, where $\sigma = |\Sigma| + 1 + |V|$ for an LR table and $|\Sigma| + 1$ for an LL(1) table. For the expression grammar $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$ the SLR(1) table has 12 rows and 9 columns, of which 45 cells are filled.
- **The drivers** run in $O(n)$ table lookups on a deterministic table built by a correct LR or LL(1) construction, since such a table admits no cycle of moves that consumes no input.

## Variants

- **Precedence resolution.** RESOLVE with a policy based on declared operator precedence and associativity is how [yacc](/yacc/) turns an ambiguous expression grammar into a deterministic table.
- **Default reductions.** A state whose only reduction is $A \to \alpha$ can hold that reduction in every empty terminal cell; the table shrinks and errors are found a few reductions later, never after a wrong shift.
- **LR(k) and LL(k) tables.** The columns become strings of up to $k$ tokens; the grid grows as $(|\Sigma| + 1)^k$ and is rarely used for $k > 1$.
- **Operator precedence tables.** Rows and columns are both terminals and the cells hold precedence relations; see [operator precedence grammars](/operator-precedence-grammar/).

## When to use it

Use a parsing table when the parser is generated: the table is built once from the grammar, and the driver is a short loop that is easy to trust. Keep the conflict record and print it; every conflict is either an ambiguity in the grammar or a place where the method looks too little ahead. Prefer hand-written [recursive descent](/recursive-descent-parsing/) when the grammar is small and LL(1) and the error messages matter more than coverage.

## Pitfalls

- **Overwriting a cell.** A table stored as a plain map from cells to one action loses the first action when a second arrives, and the generator then reports no conflict at all. Keep the set, or at least a flag.
- **Silent resolution.** A builder that resolves every conflict by a fixed rule, such as shift over reduce, hides real ambiguities. Count the conflicts and compare them with the number the author expects.
- **Goto after the pop.** After a reduction by $A \to \beta$, the goto entry is read from the state exposed by popping $|\beta|$ states, not from the state that was on top before.
- **Loops after resolution.** A table that came from a correct construction cannot loop, but a hand-edited or arbitrarily resolved table can, for example a top-down table that predicts a left-recursive production. A driver used on such tables needs a step limit.

## Implementations

## History

Knuth (1965) defined LR(k) parsing as a machine that chooses its move from its state and the next $k$ symbols. The practical LR methods that followed, SLR and LALR, store those moves as a table of shift, reduce, accept, error and goto entries over the states of the LR(0) automaton, and yacc made such tables, with conflict reports and precedence resolution, the standard output of a parser generator. Top-down parser generators use the same structure with nonterminals as rows.

## References
