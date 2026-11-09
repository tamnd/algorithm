---
tag: EPST33
kind: algorithm
slug: dpll-backtracking-sat
name: Backtracking for SAT
aliases:
- plain backtracking for SAT
- backtracking search for satisfiability
area: logic-and-constraints/sat-solving
level: core
summary: Decide SAT by assigning the variables one at a time in a fixed order and undoing the last choice as soon as a clause is false. No unit propagation; DPLL adds it.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause width}
  time: {worst: O(2^n (m k + 1)), best: O(n + m k)}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1962
  people: [Martin Davis, George Logemann, Donald W. Loveland]
  note: The splitting rule of the DLL paper is this backtracking search. Golomb and Baumert described backtrack programming in general in 1965.
prereqs: [sat, conjunctive-normal-form, chronological-backtracking]
see_also: [dpll, cdcl, generic-backtracking-algorithm, depth-first-search, exact-exponential-algorithms]
sources:
  - paper: doi:10.1145/368273.368557
    title: Martin Davis, George Logemann and Donald Loveland, A machine program for theorem-proving, Communications of the ACM 5(7), 1962
    locator: pages 394 to 397 (the splitting of the formula on one variable, with the search kept in a list instead of a tree)
  - paper: "Solomon W. Golomb and Leonard D. Baumert, Backtrack programming, Journal of the ACM 12(4), 1965, pages 516 to 524"
    locator: the general backtrack method, with a partial solution extended one coordinate at a time and cut off when it cannot be extended
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (the first backtracking algorithms of the section)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 3, Complete Algorithms, by Adnan Darwiche and Knot Pipatsrisawat
---

Backtracking for SAT decides the [SAT problem](/sat/) by depth-first search over partial assignments. It assigns $x_1, x_2, \ldots, x_n$ in this order, tries false before true, and undoes the last open choice as soon as a clause has all its variables assigned and is false. It is the plain search that [DPLL](/dpll/) improves with [unit propagation](/unit-propagation/) and the [pure literal rule](/pure-literal-elimination/). Its worst case is $2^n$ times a polynomial, and it can reach that bound on formulas that DPLL solves at once.

## In plain words

You have a row of switches, each on or off, and a list of rules. Each rule says that at least one of some switches must be in a given position. You set the switches from left to right, off first. After each switch, you check only the rules whose last switch you just set, because only their result is now fixed. If such a rule fails, you change the last switch that is still off to on, and you reset the switches after it. If the last switch is set and no rule failed, you have an answer. If every switch you could change is already on, there is no answer.

## The problem

The input is a formula $F$ in [conjunctive normal form](/conjunctive-normal-form/) over $x_1, \ldots, x_n$, with $m$ [clauses](/clause/) of width at most $k$. A clause is a set of [literals](/literal/), and $|F|$ is the total number of literal occurrences, so $|F| \le mk$. The output is a model of $F$, or UNSAT. This is the [SAT problem](/sat/).

## The algorithm

For a clause $C$, let $\max(C)$ be the largest index of a variable in $C$. The array $\alpha[1 \ldots n]$ holds the current values, and $i$ is the depth of the search.

```pseudo id=main
BACKTRACK-SAT(F)                           ▷ F over x1 .. xn
L1  if F has the empty clause then return UNSAT
L2  if n = 0 then return SAT with the empty assignment
L3  i ← 1, α[1] ← false
L4  loop
L5      if no clause C with max(C) = i is false under α[1 .. i] then
L6          if i = n then return SAT and α
L7          i ← i + 1, α[i] ← false
L8      else
L9          while i ≥ 1 and α[i] = true do i ← i − 1          ▷ both values failed
L10         if i = 0 then return UNSAT
L11         α[i] ← true
```

The search keeps no stack of frames. The prefix $\alpha[1 \ldots i]$ is the stack: a value false means that true is still to be tried, and a value true means that both values are used. Line L5 tests only the clauses whose largest variable is $x_i$. A clause with a smaller largest variable was tested when that variable got its current value, and the values before $x_i$ have not changed since.

This page is the plain search. [DPLL](/dpll/) is the same search plus two rules that run before each choice: unit propagation assigns the literal of each clause that has only one free literal left, and the pure literal rule assigns a literal whose negation does not occur. DPLL also simplifies the formula, and it picks the next variable freely instead of in the fixed order.

## Example

Take $n = 3$ and the four clauses

$$C_1 = \{x_1, x_2\},\quad C_2 = \{x_1, \neg x_2\},\quad C_3 = \{\neg x_1, x_3\},\quad C_4 = \{\neg x_2, \neg x_3\}.$$

The values of $\max$ are 2, 2, 3 and 3. Each row is one test of line L5.

| test | prefix $\alpha[1 \ldots i]$ | clauses tested | result | next step |
|---|---|---|---|---|
| 1 | 0 | none | pass | go to $x_2$ |
| 2 | 0 0 | $C_1, C_2$ | $C_1$ false | set $x_2$ true |
| 3 | 0 1 | $C_1, C_2$ | $C_2$ false | back to $x_1$, set it true |
| 4 | 1 | none | pass | go to $x_2$ |
| 5 | 1 0 | $C_1, C_2$ | pass | go to $x_3$ |
| 6 | 1 0 0 | $C_3, C_4$ | $C_3$ false | set $x_3$ true |
| 7 | 1 0 1 | $C_3, C_4$ | pass | return the model |

The answer is $x_1 = 1, x_2 = 0, x_3 = 1$. Tests 2 and 3 show the weakness of the plain search. Under $x_1 = 0$, the clauses $C_1$ and $C_2$ are both unit, with opposite literals, and unit propagation would find the conflict without trying $x_2$. On the formula $\{\{x_n\}, \{\neg x_n\}\}$ the plain search makes $2^{n+1} - 2$ tests, and DPLL stops after one round of unit propagation.

## Correctness

The proof uses an invariant of line L5. No assignment that comes before the current prefix in the lexicographic order, with false before true, is a model. And each clause whose largest variable is before $x_i$ is true under the current values. A failed test shows that no extension of the prefix is a model, and line L9 moves to the next prefix after all extensions of the failed one. When the test passes at $i = n$, every clause has been tested with its final values, so $\alpha$ is a model. So the algorithm returns the first model in this order, or UNSAT when there is none. The full proof is below.

## Complexity

The tested prefixes come in strictly increasing preorder in the binary tree of all prefixes, so there are at most $2 + 4 + \cdots + 2^n = 2^{n+1} - 2$ tests. Let $F_i$ be the set of clauses $C$ with $\max(C) = i$. There are at most $2^i$ tests at depth $i$, and each reads the clauses of $F_i$, so the total time is

$$O\Big(2^{n+1} + \sum_{i=1}^{n} 2^i\, |F_i|\Big) \subseteq O\big(2^n (|F| + 1)\big),$$

where $|F_i|$ is the number of literal occurrences in $F_i$. The steps of line L9 are paid by the tests that set those values. The bound is tight up to the factor $|F|$: the formula $\{\{x_n\}, \{\neg x_n\}\}$ takes $2^{n+1} - 2$ tests. The best case is a formula with a model that starts with false on each variable, which takes $n$ tests and time $O(n + |F|)$. The extra space is $O(n)$ for $\alpha$ and $O(m)$ for the lists $F_i$.

No algorithm for SAT is known with a worst-case bound of $O(c^n)$ for a constant $c < 2$ on general CNF, and SAT is [NP-complete](/np-complete/) ([Cook-Levin theorem](/cook-levin-theorem/)). For 3-SAT, better exponential bounds are proved, for example by [Schöning's algorithm](/schoning-algorithm/) and [PPSZ](/ppsz-algorithm/).

## Properties

- **Deterministic and exact.** The order of variables and values is fixed, and the answer is always correct.
- **Lexicographically first model.** With false before true, the model it returns is the first one in lexicographic order. No other SAT algorithm on these pages promises this.
- **Iterative and small.** It needs only the array $\alpha$ and the lists $F_i$, with no recursion and no copy of the formula.
- **Chronological.** It always undoes the most recent open choice, even when that choice has nothing to do with the false clause. This is [chronological backtracking](/chronological-backtracking/).

## Variants and improvements

- **[DPLL](/dpll/).** Add unit propagation, the pure literal rule and a free choice of the next variable.
- **[Backjumping](/non-chronological-backtracking/).** On a failure, jump back to the latest variable that occurs in the false clause, not to the latest open choice.
- **[CDCL](/cdcl/).** Learn a clause from each conflict, and jump back to the level where it becomes unit.
- **Counting and enumeration.** Do not stop at the first model. Record it and continue as if the test of line L5 had failed. This enumerates all models in lexicographic order, which is a simple form of [model counting](/model-counting/).

## When to use it

Use it as a reference solver in tests, for very small formulas, and for teaching. It is short enough to check by hand, and its answer is the first model in lexicographic order, which makes it a good oracle. For any real formula, use [DPLL](/dpll/) or [CDCL](/cdcl/).

## Pitfalls

- **Testing all clauses at each step.** Testing every clause at every node costs $O(|F|)$ per node. Group the clauses by their largest variable and test only one group.
- **Testing too early.** A clause with an unassigned variable can still become true. Only a clause whose variables all have values can fail.
- **Recursion depth.** A recursive version needs depth $n$. In Python, use the array $\alpha$ as the stack, as here.
- **The empty clause.** An empty clause has no largest variable. Handle it before the search, as line L1 does.

## Implementations

## History

Davis, Logemann and Loveland (1962) replaced the elimination rule of the [Davis-Putnam procedure](/davis-putnam-elimination/) by splitting on one variable, which is this search with unit propagation and the pure literal rule added. Golomb and Baumert (1965) described backtrack programming as a general method for search problems. The plain search on this page is the first algorithm in most treatments of SAT solving, for example at the start of Knuth's Section 7.2.2.2.

## References
