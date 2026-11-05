---
tag: 4N9BC2
kind: technique
slug: parse-table-compression
name: Parse table compression
aliases:
- default reductions
- row displacement
- table packing
area: automata-and-parsing/parser-generators
level: advanced
summary: Reducing the space of LR or LL parse tables by default reductions, row sharing and displacement packing.
prereqs: [parsing-table, lr-parsing]
see_also: [lr-parse-table, ll-parse-table, yacc, parser-generator, parser-table-construction, parser-error-recovery, lalr-parsing, lalr-lookahead-computation]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition
    locator: Section 4.7.6, Compaction of LR Parsing Tables (default reductions in ACTION rows, shared rows, GOTO stored by columns with defaults)
  - paper: doi:10.1145/359168.359175
    title: Robert Endre Tarjan and Andrew Chi-Chih Yao, Storing a sparse table, Communications of the ACM 22(11) (1979)
    locator: pp. 606 to 611 (row displacement with a first-fit packing of the rows into one array)
  - paper: "Peter Dencker, Karl Dürre and Johannes Heuft, Optimization of parser tables for portable compilers, ACM Transactions on Programming Languages and Systems 6(4) (1984)"
    locator: the merging of compatible rows and columns by graph colouring, and the comparison of compression methods on real grammars
  - url: https://www.gnu.org/software/bison/manual/
    title: GNU Bison manual
    locator: section Default Reductions (the lr.default-reduction setting and its effect on error detection)
---

## In plain words

A parser generator produces a table with one row per parser state and one column per token or rule name. For a real language the table has hundreds or thousands of rows, and most cells are empty, meaning "syntax error", or repeat the same entry along a row. Compression stores only what matters.

Three ideas do most of the work. First, a row that mostly says "reduce by rule 5" keeps that as a single default and lists only the other entries. Second, rows that end up the same are stored once. Third, the short rows left over are slid along one long array until their entries fall into free slots, and a small check array records which row owns each slot, so lookups stay fast. The parser accepts the same inputs; it may notice an error a few steps later, but never after reading a wrong token.

## When it applies

The technique applies to any table indexed by (state, symbol) whose cells are mostly empty or repeat a value per row or per column: LR(0), [SLR](/slr-parsing/), [LALR](/lalr-parsing/) and canonical LR action and goto tables, [LL parse tables](/ll-parse-table/), and the transition tables of scanners. It pays off when the table is large, as for the grammars of programming languages, and when it must be shipped inside the generated parser. It needs three facts about the table:

- **Error cells are interchangeable with some actions.** Replacing an error cell in the ACTION part by a reduction changes only when an error is noticed, not whether it is: see the template, step 2.
- **GOTO lookups never hit an error cell.** After a reduction by $A \to \alpha$ an LR parser looks up $\mathrm{GOTO}(p, A)$ only for a state $p$ that has a move on $A$, so the empty GOTO cells can hold anything.
- **Lookups dominate.** The compressed table must answer a lookup in constant time, which rules out searching a list per row for large rows but allows an index computation and one comparison.

## The template

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$. The table has $N$ states, the ACTION part has a column for each terminal and the end marker $\$$, each numbered by a code $c(a)$, and the GOTO part has a column for each nonterminal.

1. **Build the dense table** and check it for conflicts; the compressed table must reproduce every non-error cell.
2. **Default reduction per row.** In each ACTION row, pick the reduction that occurs most often, if any, as the row's default $D[s]$. Delete the cells equal to it, and treat every error cell of the row as $D[s]$ too. In a state with no reduction the default is "error".
3. **Share rows.** Rows that are now equal are stored once; each state keeps the number $R[s]$ of its row.
4. **Pack the rows by displacement.** Give each stored row $r$ an offset $\mathit{base}[r]$ such that the slots $\mathit{base}[r] + c(a)$ of all its entries are free, place each entry in $\mathit{next}[\mathit{base}[r] + c(a)]$ and write $r$ in $\mathit{check}$ at the same slot. Taking the rows from the fullest to the emptiest and each at the smallest free offset is the first-fit decreasing rule of Tarjan and Yao.
5. **GOTO by columns.** For each nonterminal $A$, store the most frequent target as the column default and list the other pairs (state, target).
6. **Lookup.** $\mathrm{ACTION}(s, a)$: let $i = \mathit{base}[R[s]] + c(a)$; if $i$ is inside the array and $\mathit{check}[i] = R[s]$, return $\mathit{next}[i]$, else return $D[s]$. $\mathrm{GOTO}(p, A)$: return the listed target for $p$ if there is one, else the column default.

**Why the parser still works.** For a table without conflicts, step 2 changes only error cells, and only into reductions. Take an input on which the dense parser stops with an error in state $s$ on token $a$. The compressed parser does the same moves up to that point. In $s$ it may now reduce instead; reductions do not read input, the GOTO lookups that follow are of cells that exist, and they lead to states where the same token $a$ is still next. A canonical LR(1) or LALR(1) parser never shifts a token unless the input read so far, with that token, is a prefix of a sentence: shifting $a$ there would mean the dense parser could have parsed it too. So the compressed parser ends in an error before shifting $a$, after at most a few extra reductions, and accepts exactly the same inputs. A script checked this on the example below and on 624 random conflict-free LALR(1) tables, including grammars with ε-productions and left recursion, over all inputs up to length 4: acceptance and the number of tokens shifted before the error were the same in every case.

## Classic examples

**The expression grammar.** Take $E \to E + T \mid T$, $T \to T * F \mid F$, $F \to (\,E\,) \mid \mathit{id}$ as productions 1 to 6. Its LALR(1) table has 12 states, ACTION columns $+, *, (, ), \mathit{id}, \$$ with codes 0 to 5, and GOTO columns $E, T, F$: 72 ACTION cells of which 36 are filled, and 36 GOTO cells of which 9 are filled. The states, numbered in the order a breadth-first construction finds them, have the kernels

| state | kernel items | row after step 2 | default |
|---|---|---|---|
| 0 | $E' \to \cdot E$ | $( \mapsto$ shift 4, $\mathit{id} \mapsto$ shift 5 | error |
| 1 | $E' \to E \cdot$, $E \to E \cdot + T$ | $+ \mapsto$ shift 6, $\$ \mapsto$ accept | error |
| 2 | $E \to T \cdot$, $T \to T \cdot * F$ | $* \mapsto$ shift 7 | reduce 2 |
| 3 | $T \to F \cdot$ | empty | reduce 4 |
| 4 | $F \to ( \cdot E )$ | as state 0 | error |
| 5 | $F \to \mathit{id} \cdot$ | empty | reduce 6 |
| 6 | $E \to E + \cdot T$ | as state 0 | error |
| 7 | $T \to T * \cdot F$ | as state 0 | error |
| 8 | $E \to E \cdot + T$, $F \to ( E \cdot )$ | $+ \mapsto$ shift 6, $) \mapsto$ shift 11 | error |
| 9 | $E \to E + T \cdot$, $T \to T \cdot * F$ | $* \mapsto$ shift 7 | reduce 1 |
| 10 | $T \to T * F \cdot$ | empty | reduce 3 |
| 11 | $F \to ( E ) \cdot$ | empty | reduce 5 |

After step 2, 16 entries are left, and step 3 leaves five distinct rows: $r_0$ for states 0, 4, 6 and 7, $r_1$ for state 1, $r_2$ for states 2 and 9, $r_3$ (empty) for states 3, 5, 10 and 11, and $r_4$ for state 8. First fit, fullest rows first, gives $\mathit{base} = 0$ for $r_0$, $r_1$, $r_2$ and $r_3$ and $\mathit{base} = 3$ for $r_4$, and an array of 7 slots:

| slot | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| next | shift 6 | shift 7 | shift 4 | shift 6 | shift 5 | accept | shift 11 |
| check | $r_1$ | $r_2$ | $r_0$ | $r_4$ | $r_0$ | $r_1$ | $r_4$ |

The GOTO columns have defaults $E \mapsto 1$, $T \mapsto 2$, $F \mapsto 3$, with the exceptions $(4, E) \mapsto 8$, $(6, T) \mapsto 9$ and $(7, F) \mapsto 10$. A lookup of $\mathrm{ACTION}(9, ))$ computes $i = 0 + 3$, finds $\mathit{check}[3] = r_4 \ne r_2$, and returns the default, reduce 1, which is the dense entry. $\mathrm{ACTION}(8, \$)$ computes $i = 3 + 5 = 8$, outside the array, and returns the default of state 8, error. The 108 dense cells become 12 defaults, 12 row numbers, 5 offsets, 14 array cells and 9 GOTO numbers, 52 in all; on tables with hundreds of states and terminals the proportion saved is much larger, since most rows are short. The tables and lookups were produced and checked by a script, which also ran the dense and the compressed parser on every input of up to six tokens and found the same outcome and error position every time.

**LL(1) tables.** In an [LL parse table](/ll-parse-table/), a nonterminal with an ε-production can use it as the row default. The parser then expands $A \to \varepsilon$ on a token that cannot follow, and the error appears at the next terminal match instead, still before the wrong token is consumed.

**Scanners.** The same displacement layout with base, next and check arrays, and a default per state, stores the transition tables of generated scanners, where most states have transitions on few characters.

## Variations

- **Choice of defaults.** Some generators make a reduction the default only when it is the only action of the state, a *consistent* state, so that the error cells of other rows stay errors. Bison chooses among these policies with `%define lr.default-reduction`, and documents that more default reductions mean later error detection (Bison manual, Default Reductions).
- **Row and column merging.** Rows that agree wherever both are defined can be merged even if they are not equal, when the error cells do not matter; finding few merged rows is a graph colouring problem on the conflict graph of rows, and Dencker, Dürre and Heuft apply it to rows and columns of parser tables.
- **Bit matrices.** Some generators keep a separate bit matrix marks the significant cells, so that a merged or default-filled table still detect errors at the same point as the dense one.
- **Lists per row.** Small rows can be stored as lists of (token, action) pairs searched linearly, which is simple and often fast enough; the displacement layout gives constant time for large rows.
- **Displacement order.** First fit with rows sorted by decreasing size is the classic heuristic; Tarjan and Yao bound the size of the packed array it produces under a condition on the distribution of the entries among the rows.

## Pitfalls

- **Forgetting the check array.** Without $\mathit{check}$, a lookup that lands in a slot owned by another row returns that row's entry: in the example, $\mathrm{ACTION}(9, ))$ would return shift 6 instead of reduce 1.
- **Default reductions and error recovery.** Extra reductions before an error is found pop the states that a recovery would have used and can make error messages list fewer expected tokens; see [parser error recovery](/parser-error-recovery/). Generators that care keep defaults to consistent states, or check the token before reducing, as Bison's lookahead correction does.
- **Tables with conflicts.** The argument above needs a table without conflicts. On tables whose conflicts were settled by the default rules of [yacc](/yacc/), the script found random grammars, most of them with a cycle $A \Rightarrow^+ A$, where default reductions made the compressed parser loop on inputs that the dense parser rejected.
- **Compressing GOTO with ACTION rules.** GOTO defaults by column are safe because the parser never asks for an undefined GOTO cell; ACTION defaults must be chosen per row, since error cells there are asked for.
- **Measuring the wrong thing.** The saving depends on the number of distinct rows and on the packing; small example tables can grow under compression because of the index arrays.

## Exercises

1. Show that if a state of an LR(0) automaton contains a completed item and no other item, replacing all of its error cells by that reduction never changes the set of accepted inputs. *Hint: the dense parser reduces there on every token that can follow, and the GOTO it reaches is the same.*
2. In the example, pack the nonempty rows in the order $r_4, r_2, r_1, r_0$ with first fit and compare the length of the array with the 7 slots above. *Answer: 8 slots. Over all 24 orders of these four rows first fit gives between 7 and 11 slots, and 7 is optimal, since the rows have 7 entries.*
3. Give a grammar and an input on which an LALR(1) parser with default reductions performs more reductions before reporting the error than the dense parser. *Answer: the expression grammar with input $\mathit{id}\,($. The dense parser shifts $\mathit{id}$ and stops in state 5; the compressed one reduces by $F \to \mathit{id}$, $T \to F$ and $E \to T$ and stops in state 1, after the same single shift.*
4. Explain why the GOTO part can be stored as column defaults with exceptions and no check, while the ACTION entries packed by displacement need the check array.
5. For an LL(1) table, show that using an ε-production as the default of its row never lets the parser match a terminal that is not a prefix continuation of the input. *Hint: after the ε-expansion the parser either expands another nonterminal or matches a terminal, and the terminal match is exact.*

## References
