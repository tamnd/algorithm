---
tag: VDGQFJ
kind: definition
slug: dimacs-cnf-format
name: DIMACS CNF format
aliases:
- DIMACS
- DIMACS CNF
- .cnf file
area: logic-and-constraints/sat-solving
level: intro
summary: The standard text format for CNF formulas. A header line p cnf n m, then each clause as signed integers ended by 0. Nearly every SAT solver reads it.
prereqs: [conjunctive-normal-form, literal]
see_also: [sat, clause, drat-proof, max-sat, qbf, model-counting, incremental-sat]
sources:
  - paper: "David S. Johnson and Michael A. Trick (eds.), Cliques, Coloring, and Satisfiability, Second DIMACS Implementation Challenge, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 26, American Mathematical Society, 1996"
    locator: the challenge input formats, among them the CNF format of the satisfiability track, first circulated in 1993 as "Satisfiability suggested format"
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 15, Proofs of Unsatisfiability, by Marijn Heule (the DRAT format, which reuses the DIMACS conventions for clauses)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (the benchmark formulas, and the input conventions of the SAT programs)
---

The DIMACS CNF format is the plain text format in which SAT solvers read a formula in [conjunctive normal form](/conjunctive-normal-form/). A header line `p cnf n m` gives the number of variables and clauses, and each [clause](/clause/) follows as a list of nonzero integers ended by `0`, where $i$ is the [literal](/literal/) $x_i$ and $-i$ is $\neg x_i$. It comes from the Second DIMACS Implementation Challenge of 1992 and 1993, and the SAT Competitions, the solver libraries and the proof formats such as [DRAT](/drat-proof/) all use it or extend it.

## Definition

A DIMACS CNF file is a text file of whitespace-separated tokens with three kinds of content.

**Comment lines.** A line that starts with `c` is a comment and is ignored. Comments may appear before the header; most parsers also accept them between clauses.

**Problem line.** Exactly one line of the form `p cnf n m`, before the first clause, where $n \ge 0$ is the number of variables and $m \ge 0$ the number of clauses. The variables are $x_1, \ldots, x_n$.

**Clauses.** After the problem line comes a sequence of nonzero integers in the range $-n$ to $n$, split into clauses by the token `0`. The clause $\ell_1 \ldots \ell_k$ `0` is $\{\ell_1, \ldots, \ell_k\}$, with $i$ for $x_i$ and $-i$ for $\neg x_i$. A clause may span several lines, and a line may hold several clauses: only the `0` ends a clause. A `0` with no literal before it is the empty clause. There should be exactly $m$ clauses.

**Solver output.** The SAT Competition rules fix the answer of a solver. A line `s SATISFIABLE` is followed by one or more lines `v` with the literals that are true in a model, ended by `0`. Otherwise the line is `s UNSATISFIABLE` or `s UNKNOWN`. The exit code is 10 for satisfiable and 20 for unsatisfiable.

**Extensions.** Several formats keep the clause syntax and change the header:

- `p wcnf` for weighted [MaxSAT](/max-sat/), with a weight before each clause; the newer form drops the header and marks hard clauses with `h`.
- QDIMACS for [QBF](/qbf/), with lines `e` and `a` that list the existential and universal variables of each quantifier block.
- `c ind` or `c p show` comment lines in some [model counting](/model-counting/) tracks, which name the variables to project on.
- The incremental IPASIR interface, which takes the same signed integers ended by 0 through function calls instead of a file, see [incremental SAT](/incremental-sat/).
- [DRAT](/drat-proof/) and LRAT proofs, which list added and deleted clauses in the same style.

## Examples and non-examples

This file is valid:

```text
c a small example: 3 variables, 4 clauses
p cnf 3 4
1 -2 0
2 3 0
-1 -3 0
-2
3 0
```

It is the formula $\{x_1, \neg x_2\}, \{x_2, x_3\}, \{\neg x_1, \neg x_3\}, \{\neg x_2, x_3\}$; the last clause spans two lines. A check of all 8 assignments shows one model, $x_1 = 0, x_2 = 0, x_3 = 1$. If $x_2$ were true, the first and last clauses would force $x_1$ and $x_3$, and the third clause would be false. So $x_2$ is false, the second clause forces $x_3$, and the third forces $\neg x_1$. A solver prints:

```text
s SATISFIABLE
v -1 -2 3 0
```

Files that break the format, and what common parsers do with them:

| file content | problem | usual behaviour |
|---|---|---|
| `p cnf 3 2`, then `1 2 0` and `-3` | the last clause has no `0` | most parsers accept it at the end of the file; strict ones reject it |
| `p cnf 2 1`, then `1 -3 0` | variable 3 is above $n = 2$ | rejected by strict parsers; others grow $n$ |
| `p cnf 3 5` with only 4 clauses | wrong clause count | many solvers warn and go on |
| `p cnf 3 1`, then `1 -1 2 0` | a tautology | valid; solvers remove it |
| `p cnf 2 1`, then `1 1 2 0` | a repeated literal | valid; solvers must remove the repeat before they watch the clause |
| `p cnf 1 1`, then `0` | the empty clause | valid; the formula is unsatisfiable |
| `p cnf 0 0` | no clauses | valid; the formula is satisfiable |
| clauses before the `p` line | missing header | rejected |

Some old benchmark files, such as the uniform random 3-SAT sets of SATLIB, end with a line `%` and a line `0`. Parsers that do not stop at `%` read a spurious empty clause and report the formula unsatisfiable.

## Related definitions

- **[Conjunctive normal form](/conjunctive-normal-form/).** The formulas that the format writes down.
- **[Literal](/literal/).** Its signed integer coding is the coding of the format; solvers convert $\pm i$ to an internal code such as $2i$ or $2i + 1$.
- **[Boolean satisfiability problem](/sat/).** The question a solver answers on a DIMACS file.
- **[DRAT proof](/drat-proof/).** The certificate of an `s UNSATISFIABLE` answer, written as a list of clauses in the same syntax.
- **[MaxSAT](/max-sat/) and [QBF](/qbf/).** The WCNF and QDIMACS variants.

## References
