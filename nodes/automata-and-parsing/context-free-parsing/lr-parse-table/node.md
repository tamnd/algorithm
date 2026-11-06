---
tag: B3QKMP
kind: data-structure
slug: lr-parse-table
name: LR parse table
aliases:
- ACTION and GOTO tables
area: automata-and-parsing/context-free-parsing
level: core
summary: Action and goto tables that drive a shift-reduce LR parser.
model: word-ram
complexity:
  vars: {N: the number of states, σ: the number of terminals plus one for the end marker, v: the number of nonterminals, g: the size of the grammar}
  time: {build: O(N g (g + σ)), lookup: O(1)}
  space: {total: Θ(N (σ + v))}
history:
  year: 1965
  people: [Donald E. Knuth]
  note: Knuth's LR(k) parser chooses each move from the current state and the next k symbols; the split into an ACTION table for terminals and a GOTO table for nonterminals is the form used by the parser generators that followed.
prereqs: [lr-item, shift-reduce-parsing, first-and-follow-sets]
see_also: [lr0-parsing, slr-parsing, lalr-parsing, canonical-lr-parsing, parse-table-compression, ll-parse-table, shift-reduce-conflict, yacc]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.6.3, The LR-Parsing Algorithm (the ACTION and GOTO functions); Section 4.6.4, Constructing SLR-Parsing Tables (Algorithm 4.46 and Figure 4.37); Section 4.7.3, Canonical LR(1) Parsing Tables; Section 4.7.7, Compaction of LR Parsing Tables
  - paper: doi:10.1016/S0019-9958(65)90426-2
    title: Donald E. Knuth, On the translation of languages from left to right, Information and Control 8(6) (1965)
    locator: pp. 607 to 639
  - paper: doi:10.1145/362619.362625
    title: Frank L. DeRemer, Simple LR(k) grammars, Communications of the ACM 14(7) (1971)
    locator: pp. 453 to 460
  - book: isbn:9780521820608
    title: Andrew W. Appel and Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Section 3.3, LR Parsing (the parsing table with shift, reduce, goto and accept entries)
---

An LR parse table is the pair of tables that drives a [shift-reduce](/shift-reduce-parsing/) LR parser: $\mathrm{ACTION}[q, a]$ tells the parser in state $q$ with next token $a$ to shift and go to a state, to reduce by a production, to accept, or to report an error, and $\mathrm{GOTO}[q, A]$ gives the state to enter after a reduction to the nonterminal $A$. The states are the item sets of an LR automaton, and the methods [LR(0)](/lr0-parsing/), [SLR](/slr-parsing/), [LALR](/lalr-parsing/) and [canonical LR(1)](/canonical-lr-parsing/) differ only in the automaton and in the tokens on which they put a reduction. A cell that gets two actions is a conflict, and a grammar suits a method exactly when its table has none.

## In plain words

An LR parser reads tokens onto a stack and, every so often, replaces the top of the stack by the name of a grammar rule. The table tells it what to do. Each row is a state of the parser, which sums up what is on the stack. Each column is a possible next token, or the name of a rule.

To decide the next move, the parser looks in the row of its state and the column of the next token. The box says "read the token and go to state 7", or "replace the top three symbols by an expression", or "done", or it is empty, which means the input has an error here. After a replacement, the parser looks up the box for the rule's name in the second part of the table to know its new state.

## The abstract type

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area. The grammar is augmented with $S' \to S$, and $\$ \notin \Sigma$ marks the end of the input.

An LR parse table over a set $Q$ of states is a pair of partial maps

$$\mathrm{ACTION} : Q \times (\Sigma \cup \{\$\}) \to \{\text{shift } j, \text{reduce } A \to \beta, \text{accept}\}, \qquad \mathrm{GOTO} : Q \times V \to Q,$$

with a start state $q_0$. An undefined ACTION entry means error. A *conflict* is a cell to which the construction assigns two different actions: shift and reduce (a [shift-reduce conflict](/shift-reduce-conflict/)) or two reductions (a [reduce-reduce conflict](/reduce-reduce-conflict/)). The operations are LOOKUP-ACTION, LOOKUP-GOTO and the construction FILL from an LR automaton. The table holds everything the parser needs; the grammar is used only to know the length and the left side of each production to reduce by.

## Representation

- **Dense arrays.** ACTION is an $N \times \sigma$ array and GOTO an $N \times v$ array, each entry a small integer: for example $+j$ for shift $j$, $-p$ for reduce by production $p$, a special value for accept and 0 for error. Lookup is one array access.
- **Rows as maps.** The implementation on this page stores each row as a hash map from symbols to actions, which keeps only the nonempty cells.
- **Compressed.** Real parser generators store the tables in compressed form, since most cells are empty or repeat a default reduction. The usual tricks are a default reduction per row, sharing of equal rows, and packing the rows into one array with offsets. See [parse table compression](/parse-table-compression/).

A reduction needs the production's length and left side, kept in a separate array indexed by production number.

## Operations

FILL turns an automaton, a list $C$ of item sets with the transition function GOTO, into the two tables. The lookahead set $\mathrm{LA}(q, A \to \alpha)$ of a complete item is all of $\Sigma \cup \{\$\}$ for LR(0), $\mathrm{FOLLOW}(A)$ for SLR, and the lookahead terminal of the item for canonical LR(1) and LALR.

```pseudo id=main
FILL(C, GOTO)                                  ▷ C the item sets, GOTO the automaton's transitions
L1  for each state q and each item in C[q] do
L2      if the item is A → α·aβ with a ∈ Σ then SET(q, a, shift GOTO(q, a))
L3      else if the item is S' → S· then SET(q, $, accept)
L4      else if the item is A → α· then
L5          for each b ∈ LA(q, A → α) do SET(q, b, reduce A → α)
L6  for each state q and nonterminal A with GOTO(q, A) defined do GOTO-TABLE[q, A] ← GOTO(q, A)

SET(q, a, x)
L7  if ACTION[q, a] is empty or equals x then ACTION[q, a] ← x
L8  else record a conflict at (q, a)

LOOKUP-ACTION(q, a)
L9  return ACTION[q, a], or error if the cell is empty

LR-DRIVE(w)                                    ▷ the table has no conflict
L10 push q0; loop: act ← LOOKUP-ACTION(top state, next token of w$)
L11     if act is error then report an error at the next token
L12     if act = shift j then push j and advance the input
L13     else if act = reduce A → β then pop |β| states; push GOTO-TABLE[top state, A]; output A → β
L14     else return accept
```

## Example

The SLR table of the expression grammar, with the productions numbered (1) $E \to E + T$, (2) $E \to T$, (3) $T \to T * F$, (4) $T \to F$, (5) $F \to ( E )$, (6) $F \to id$. In the ACTION part, s$j$ is shift $j$ and r$p$ is reduce by production $p$; empty cells are errors.

| state | $id$ | $+$ | $*$ | $($ | $)$ | $\$$ | $E$ | $T$ | $F$ |
|---|---|---|---|---|---|---|---|---|---|
| 0 | s3 | | | s2 | | | 4 | 5 | 1 |
| 1 | | r4 | r4 | | r4 | r4 | | | |
| 2 | s3 | | | s2 | | | 6 | 5 | 1 |
| 3 | | r6 | r6 | | r6 | r6 | | | |
| 4 | | s7 | | | | acc | | | |
| 5 | | r2 | s8 | | r2 | r2 | | | |
| 6 | | s7 | | | s9 | | | | |
| 7 | s3 | | | s2 | | | | 10 | 1 |
| 8 | s3 | | | s2 | | | | | 11 |
| 9 | | r5 | r5 | | r5 | r5 | | | |
| 10 | | r1 | s8 | | r1 | r1 | | | |
| 11 | | r3 | r3 | | r3 | r3 | | | |

Of the $12 \times 6 = 72$ ACTION cells, 36 are filled; GOTO has 9 entries. State 5 holds the items $E \to T \cdot$ and $T \to T \cdot * F$. LR(0) would put r2 in all six columns and clash with s8 under $*$; SLR puts r2 only under $\mathrm{FOLLOW}(E) = \{+, ), \$\}$, and the conflict disappears. The parse of $id * id + id$ takes 14 steps:

| states | symbols | input | action |
|---|---|---|---|
| 0 | | $id * id + id \$$ | s3 |
| 0 3 | $id$ | $* id + id \$$ | r6 |
| 0 1 | $F$ | $* id + id \$$ | r4 |
| 0 5 | $T$ | $* id + id \$$ | s8 |
| 0 5 8 | $T *$ | $id + id \$$ | s3 |
| 0 5 8 3 | $T * id$ | $+ id \$$ | r6 |
| 0 5 8 11 | $T * F$ | $+ id \$$ | r3 |
| 0 5 | $T$ | $+ id \$$ | r2 |
| 0 4 | $E$ | $+ id \$$ | s7 |
| 0 4 7 | $E +$ | $id \$$ | s3 |
| 0 4 7 3 | $E + id$ | $\$$ | r6 |
| 0 4 7 1 | $E + F$ | $\$$ | r4 |
| 0 4 7 10 | $E + T$ | $\$$ | r1 |
| 0 4 | $E$ | $\$$ | acc |

In state 5 with $+$ next, the parser reduces $T$ to $E$, because $*$ has already been handled; under $*$ it would shift. This is how the table encodes that $*$ binds more tightly than $+$. The canonical LR(1) automaton of the same grammar has 22 states, and its table has no conflict either.

## Correctness

FILL puts an action into a cell exactly when an item of the state calls for it, so the table without conflicts is a function that agrees with all the items. Two facts about it give a correct parser. A reduction by $A \to \beta$ is placed only in a state with the complete item $A \to \beta \cdot$, so the top of the stack is $\beta$ whenever the parser reduces, and every tree node it builds is correct. For every rightmost derivation of a sentence, the reduction at each handle is in the cell of the next token: for LR(1) items this is the item's lookahead, for SLR the token is in FOLLOW of the left side, and for LR(0) it is in every column. Without conflicts the parser therefore follows the derivation and accepts. Errors are reported before the first token that no sentence allows. The full proof is below.

## Complexity

- **Space.** The dense table has $N \sigma$ ACTION and $N v$ GOTO cells, so $\Theta(N (\sigma + v))$ space. The expression grammar gives $12 \times 9$ cells for SLR and $22 \times 9$ for canonical LR(1). For a programming language, $N$ is a few hundred to a few thousand LALR states, and compression saves most of the space.
- **Lookup.** One array access, $O(1)$; with hash maps, $O(1)$ expected.
- **FILL.** Each item of each state is handled once. Shift and accept entries cost $O(1)$, and a complete item costs $O(|\mathrm{LA}|) \le O(\sigma)$. A state has at most $|G|$ items for LR(0) and SLR, and at most $|G| \sigma$ for LR(1), so FILL takes $O(N |G| \sigma)$ time plus $O(N v)$ for GOTO. Building the automaton itself, with closures of $O(|G|)$ cost for each of at most $|G|$ successors per state, takes $O(N |G|^2)$ for LR(0) and SLR.
- **Parsing.** Each step is one lookup plus the pops of a reduction.

## Variants

- **LR(0), SLR, LALR, LR(1).** The same two tables, with different automata and lookahead sets. LR(0) and SLR use the LR(0) automaton; LALR uses it too, with exact lookaheads; canonical LR(1) uses a larger automaton.
- **Default reductions.** If a state has only one reduction, the cell of every token not shifted can hold that reduction. This shrinks the table and delays error detection by some reductions, but never past a shift: the parser still stops before it shifts a wrong token. [yacc](/yacc/) and Bison do this.
- **Conflict resolution by precedence.** Parser generators fill a conflicting cell with one action chosen by the declared precedence and associativity of the operators, which lets an ambiguous expression grammar such as $E \to E + E \mid E * E \mid id$ give a usable table.
- **LR(k) for $k > 1$.** The columns become strings of up to $k$ tokens. The table grows with $\sigma^k$ and is rarely used.
- **GLR tables.** A [GLR](/glr-parsing/) parser keeps the conflicts and lets each cell hold a set of actions.

## When to use it

Use a table-driven LR parser when the grammar is LR or LALR and comes from a parser generator: the table is built once, the driver is short, and parsing is linear. Prefer an [LL parse table](/ll-parse-table/) or a hand-written recursive descent parser when the grammar is LL(1) and readable error messages matter more than grammar coverage.

## Pitfalls

- **Off-by-one in reductions.** A reduction pops $|\beta|$ states, zero for $A \to \varepsilon$, and then reads GOTO from the newly exposed top state, not from the state before the pop.
- **Accept versus reduce.** The item $S' \to S \cdot$ means accept on $\$$ only; treating it as an ordinary reduction leaves the parser looking for a GOTO entry that does not exist.
- **Silent conflict resolution.** Generators that resolve conflicts by default, shift over reduce, can hide a real grammar error. Read the conflict report.
- **Comparing state numbers.** State numbers depend on the order in which the automaton is built, so two tables for the same grammar can look different and still be the same up to renaming of states.

## Implementations

## History

Knuth (1965) described the LR(k) parser as a machine that chooses its move from its state and the next $k$ symbols. DeRemer (1969, 1971) made the method practical with SLR and LALR tables built from the LR(0) automaton. Aho and Johnson (1974) described the table form with shift, reduce, accept, error and goto entries used by yacc, and Johnson's yacc made it the standard way to build parsers in the 1970s.

## References
