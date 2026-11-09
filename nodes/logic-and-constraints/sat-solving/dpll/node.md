---
tag: V4WR4Y
kind: algorithm
slug: dpll
name: DPLL algorithm
aliases:
- Davis-Putnam-Logemann-Loveland
- DPLL procedure
- DLL procedure
area: logic-and-constraints/sat-solving
level: core
summary: Backtracking search for SAT that simplifies the formula at each node with unit propagation and the pure literal rule, then splits on one literal.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of clauses, k: the largest clause width}
  time: {worst: O(2^n n m k), best: O(n m k)}
  space: {extra: O(n m k)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1962
  people: [Martin Davis, George Logemann, Donald W. Loveland]
  note: They replaced the elimination rule of the Davis-Putnam procedure (1960) by splitting on a variable, because elimination used too much memory on the computers of the time.
prereqs: [dpll-backtracking-sat, unit-propagation, pure-literal-elimination]
see_also: [davis-putnam-elimination, cdcl, lookahead-sat, chronological-backtracking, haken-resolution-lower-bound, schoning-algorithm, model-counting, dpll-t]
sources:
  - paper: doi:10.1145/368273.368557
    title: Martin Davis, George Logemann and Donald Loveland, A machine program for theorem-proving, Communications of the ACM 5(7), 1962
    locator: pages 394 to 397 (the splitting rule that replaces elimination, with the one-literal and affirmative-negative rules kept)
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960
    locator: pages 201 to 215 (the rules for one-literal clauses and for literals of one sign)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 3, Complete Algorithms, by Adnan Darwiche and Knot Pipatsrisawat
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 2, Section 2.2 (DPLL and its extension to CDCL)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (Algorithm D, satisfiability by cyclic DPLL)
  - paper: "Paul Beame, Henry Kautz and Ashish Sabharwal, Towards understanding and harnessing the potential of clause learning, Journal of Artificial Intelligence Research 22, 2004, pages 319 to 351"
    locator: the correspondence between DPLL runs on unsatisfiable formulas and tree-like resolution refutations
  - paper: "Burkhard Monien and Ewald Speckenmeyer, Solving satisfiability in less than 2^n steps, Discrete Applied Mathematics 10, 1985, pages 287 to 295"
    locator: the branching on a shortest clause and its bound for 3-SAT
  - paper: doi:10.1016/0304-3975(85)90144-6
    title: Armin Haken, The intractability of resolution, Theoretical Computer Science 39, 1985
    locator: pages 297 to 308 (exponential lower bound for resolution refutations of the pigeonhole formulas)
---

The DPLL algorithm decides the [SAT problem](/sat/) for a formula in [conjunctive normal form](/conjunctive-normal-form/) by depth-first search, with two simplification rules at each node. It first applies [unit propagation](/unit-propagation/) and the [pure literal rule](/pure-literal-elimination/) until neither applies, then it splits on one literal: it tries the formula with the literal true, and if that fails, with the literal false. It is sound and complete, and its worst case is $2^n$ times a polynomial. [CDCL](/cdcl/), the base of modern solvers, is DPLL with clause learning and non-chronological backtracking.

## In plain words

You have a list of rules, and each rule asks for at least one of a few switch positions. At each step, you first do the forced work. If a rule has only one way left to be satisfied, you set that switch. If a switch position appears in some rules and the opposite position appears in no rule, you set it that way, because it can only help. You remove each rule that is now satisfied.

If a rule has no way left, this path fails. If no rules are left, you are done. Otherwise you pick one switch, set it, and go on. If that fails, you come back and set the switch the other way. If both ways fail, the path above fails too.

## The problem

The input is a formula $F$ over $x_1, \ldots, x_n$ with $m$ [clauses](/clause/) of width at most $k$. A clause is a set of [literals](/literal/), and $|F| \le mk$ is the total number of literal occurrences. The output is a model of $F$ or UNSAT. This is the [SAT problem](/sat/), which is [NP-complete](/np-complete/).

## The algorithm

For a literal $\ell$, the formula $F|\ell$ is $F$ with $\ell$ made true: remove every clause that contains $\ell$, and remove $\neg\ell$ from every other clause. A clause $\{\ell\}$ with one literal is a [unit clause](/unit-clause/). A literal is *pure* in $F$ when it occurs in $F$ and its negation does not. The call DPLL$(F, \emptyset)$ decides $F$.

```pseudo id=main
DPLL(F, α)                                 ▷ α: the literals set so far
L1  while F has a unit clause {ℓ} do       ▷ unit propagation
L2      α ← α ∪ {ℓ}, F ← F|ℓ
L3  if F has the empty clause then return UNSAT
L4  while F has a pure literal ℓ do        ▷ pure literal rule
L5      α ← α ∪ {ℓ}, F ← F|ℓ
L6  if F = ∅ then return SAT and α        ▷ each free variable can take either value
L7  ℓ ← a literal of F                     ▷ the branching heuristic
L8  if DPLL(F|ℓ, α ∪ {ℓ}) returns SAT and β then return SAT and β
L9  return DPLL(F|¬ℓ, α ∪ {¬ℓ})
```

The implementation picks $\ell$ as the literal of smallest index in a shortest clause, which is close to the rule of Monien and Speckenmeyer. It runs the recursion with an explicit stack: line L9 pushes the second branch, line L8 pushes the first branch on top of it, and a branch that ends in UNSAT pops the next one.

This page and [backtracking for SAT](/dpll-backtracking-sat/) have distinct jobs. Backtracking for SAT is the bare search: a fixed variable order, no simplification, and a test of the clauses that just became fully assigned. DPLL adds lines L1 to L5, which fix the forced and the safe literals before each split, and it picks the split literal freely. On $\{\{x_n\}, \{\neg x_n\}\}$ the bare search makes $2^{n+1} - 2$ tests, and DPLL stops after one unit step.

## Example

The formula has 6 variables and 7 clauses:

$$C_1 = \{x_1, x_2\},\ C_2 = \{\neg x_1, x_3\},\ C_3 = \{\neg x_1, \neg x_3\},\ C_4 = \{\neg x_2, x_4, x_5\},\ C_5 = \{\neg x_4, x_6\},\ C_6 = \{\neg x_5, x_6\},\ C_7 = \{\neg x_4, \neg x_5\}.$$

| step | rule | literal | clauses left after the step |
|---|---|---|---|
| 1 | pure (L4) | $x_6$ | $C_1, C_2, C_3, C_4, C_7$ |
| 2 | split (L8) | $x_1$ | $\{x_3\}, \{\neg x_3\}, C_4, C_7$ |
| 3 | unit (L1) | $x_3$ | the empty clause from $C_3$: UNSAT (L3) |
| 4 | split (L9) | $\neg x_1$ | $\{x_2\}, C_4, C_7$ |
| 5 | unit (L1) | $x_2$ | $\{x_4, x_5\}, C_7$ |
| 6 | split (L8) | $x_4$ | $\{\neg x_5\}$ |
| 7 | unit (L1) | $\neg x_5$ | none: SAT (L6) |

At the start no clause is unit, and $x_6$ is the only pure literal, so it is set and removes $C_5$ and $C_6$. The first split on $x_1$ fails after one unit step, and the second branch succeeds after one more split. The result is $\alpha = \{x_6, \neg x_1, x_2, x_4, \neg x_5\}$. The variable $x_3$ is free, and the implementation sets it to false, which gives the model $\neg x_1, x_2, \neg x_3, x_4, \neg x_5, x_6$.

## Correctness

Three facts about simplification give the proof. If $\{\ell\}$ is a clause, every model makes $\ell$ true, so $F$ and $F|\ell$ are both satisfiable or both not. If $\ell$ is pure, a model of $F$ stays a model when $\ell$ is made true, because no clause contains $\neg\ell$, so again $F$ and $F|\ell$ agree. A split is complete, because each model makes $\ell$ true or false. Each step removes at least one variable from $F$, so an induction on the number of variables shows that DPLL returns a model of $F$ when one exists and UNSAT otherwise. The calls form a binary tree of depth at most $n$, so the procedure terminates. The full proof is below.

## Complexity

The calls form a binary tree of depth at most $n$, so there are at most $2^{n+1} - 1$ calls. A call does at most $n$ simplification steps, and each costs $O(|F|)$, so the worst-case time is $O(2^n \cdot n \cdot |F|)$. The stack holds at most $n$ pending branches, each with a copy of the formula, so the space is $O(n |F|)$. Solvers avoid the copies with a trail of assignments that is undone on backtracking, as in [CDCL](/cdcl/).

No worst-case bound better than $2^n$ times a polynomial is proved for DPLL on general CNF. Lower bounds come from proof complexity. When DPLL answers UNSAT, its search tree is a tree-like [resolution](/binary-resolution/) refutation of $F$, with one resolution step for each internal node, so the size of the smallest tree-like refutation is a lower bound on the number of calls (Beame, Kautz and Sabharwal, 2004). [Haken's theorem](/haken-resolution-lower-bound/) gives refutations of size $2^{\Omega(h)}$ for the pigeonhole formula with $h + 1$ pigeons and $h$ holes, even in general resolution, so DPLL takes exponential time on it with every branching rule. For 3-SAT, Monien and Speckenmeyer (1985) proved that branching on a shortest clause, with a refinement, takes $O(\alpha^n)$ time for $\alpha \approx 1.618$, the golden ratio. Better bounds for 3-SAT come from other methods, for example [Schöning's algorithm](/schoning-algorithm/) and [PPSZ](/ppsz-algorithm/).

## Properties

- **Sound and complete.** A SAT answer comes with a model, and UNSAT is returned only when no model exists.
- **Recursive.** The textbook form recurses on the formula. The implementation uses an explicit stack, with at most $n$ pending branches.
- **Deterministic.** With a fixed branching rule, the run is the same on each input. Some solvers break ties at random.
- **Chronological.** A failed branch returns to the most recent split, as in [chronological backtracking](/chronological-backtracking/).
- **A proof of UNSAT.** The search tree of an UNSAT run is a tree-like resolution refutation.

## Variants and improvements

- **Branching heuristics.** MOMS picks a variable with the most occurrences in the shortest clauses, and Jeroslow-Wang weights each clause by $2^{-|C|}$. [Lookahead solvers](/lookahead-sat/) test each candidate literal by propagation before they choose.
- **CDCL.** [Clause learning](/clause-learning/), [non-chronological backtracking](/non-chronological-backtracking/), [two watched literals](/two-watched-literals/) and [restarts](/restarts/) turn DPLL into [CDCL](/cdcl/).
- **Model counting.** Do not stop at the first model: add the counts of both branches, and count $2^f$ models when $F$ is empty with $f$ free variables. Component caching makes this practical ([model counting](/model-counting/)).
- **DPLL(T).** [DPLL(T)](/dpll-t/) runs the same search on the Boolean skeleton of a formula and checks the theory atoms with a theory solver.
- **Without the pure literal rule.** Most CDCL solvers drop the pure literal rule during search, because it is costly to maintain and helps little on large formulas. They use it, if at all, in preprocessing.

## When to use it

Use DPLL when you need a short complete solver, or a base for model counting or for a solver with a special branching rule. For large structured formulas, use [CDCL](/cdcl/), which is DPLL plus learning and is much faster in practice. For 2-CNF and Horn formulas, use the linear-time [2-SAT algorithm](/two-sat-algorithm/) or [Horn-SAT](/horn-sat/).

## Pitfalls

- **Copying the formula at each node.** Building $F|\ell$ costs $O(|F|)$ per step. A real solver keeps one formula and a trail of assignments.
- **Testing for SAT too early.** The formula is satisfied only when no clause is left, not when no unit clause is left.
- **Pure literals and models.** A pure literal is set without a split, so the result is one model, not a list of all models. For counting or for enumeration, turn the pure literal rule off.
- **Tautologies.** A clause with $x$ and $\neg x$ is always true, but it hides the purity of other literals. Remove such clauses at the start.

## Implementations

## History

Davis and Putnam (1960) gave a procedure with three rules: one-literal clauses, literals of one sign, and the elimination of a variable by resolution ([Davis-Putnam elimination](/davis-putnam-elimination/)). Davis, Logemann and Loveland (1962) ran it on an IBM 704 and found that elimination used too much memory, so they replaced it with splitting. The new procedure kept the first two rules and is now called DPLL. It was the base of most complete SAT solvers until GRASP (1996) and Chaff (2001) added clause learning, which led to [CDCL](/cdcl/).

## References
