---
tag: 1EV788
kind: algorithm
slug: davis-putnam-elimination
name: Davis-Putnam procedure
aliases:
- DP procedure
- resolution-based DP
- Davis-Putnam variable elimination
- directional resolution
area: logic-and-constraints/sat-solving
level: core
summary: Decide SAT with no search. Apply the unit and pure literal rules, and remove one variable at a time by replacing its clauses with all their resolvents on it.
solves: [sat]
model: word-ram
complexity:
  vars: {n: the number of variables}
  time: {worst: O(n^2 9^n)}
  space: {extra: O(n 3^n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1960
  people: [Martin Davis, Hilary Putnam]
  note: Published as part of a proof procedure for first-order logic, where the propositional part had to test sets of ground clauses for satisfiability.
prereqs: [binary-resolution, unit-propagation, pure-literal-elimination]
see_also: [dpll, bounded-variable-elimination, ordered-resolution, haken-resolution-lower-bound, robinson-resolution, cdcl]
sources:
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960
    locator: pages 201 to 215 (the rules for one-literal clauses, for literals of one sign, and the rule for eliminating atomic formulas)
  - paper: doi:10.1145/368273.368557
    title: Martin Davis, George Logemann and Donald Loveland, A machine program for theorem-proving, Communications of the ACM 5(7), 1962
    locator: pages 394 to 397 (the report that elimination used too much memory, and its replacement by splitting)
  - paper: "Irina Rish and Rina Dechter, Resolution versus search, two strategies for SAT, Journal of Automated Reasoning 24(1-2), 2000, pages 225 to 275"
    locator: directional resolution, its bound in terms of the induced width of the ordering, and the comparison with DPLL
  - paper: "Niklas Eén and Armin Biere, Effective preprocessing in SAT through variable and clause elimination, SAT 2005, Lecture Notes in Computer Science 3569, pages 61 to 75"
    locator: variable elimination by clause distribution, applied only when the formula does not grow
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 3, Complete Algorithms, by Adnan Darwiche and Knot Pipatsrisawat (resolution-based methods and variable elimination)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (the part on resolution and the elimination of variables)
---

The Davis-Putnam procedure decides the [SAT problem](/sat/) for a formula in [conjunctive normal form](/conjunctive-normal-form/) without search. It applies the unit rule and the [pure literal rule](/pure-literal-elimination/) while they apply, and otherwise it removes one variable $x$: it replaces all clauses that contain $x$ or $\neg x$ by all their [resolvents](/binary-resolution/) on $x$. The formula is unsatisfiable exactly when the empty clause appears. The number of clauses can grow exponentially, so the procedure is used today in a bounded form, as [bounded variable elimination](/bounded-variable-elimination/) in preprocessing.

## In plain words

Take one switch and look at the rules that mention it. Some rules need it on, and some need it off. Whatever position it gets, one group is happy through it, and each rule of the other group must be met by its other switches. So for each pair, one rule of each group, write a new rule that joins their other switches. Then throw away the switch and all the rules that mention it. The new set of rules can be met exactly when the old one can.

Do this for every variable, one by one. If you ever get a rule with no switches, it can never be met, and there is no answer. If no rules are left, there is an answer, and you can find the switch values by going back through the steps.

## The problem

The input is a formula $F$ over $x_1, \ldots, x_n$ with $m$ [clauses](/clause/). A clause is a set of [literals](/literal/), and $|F|$ is the total number of literal occurrences. The output is a model of $F$ or UNSAT. This is the [SAT problem](/sat/).

## The algorithm

For a variable $x$ of $F$, let $P$ be the clauses of $F$ that contain $x$ and $N$ the clauses that contain $\neg x$. The *resolvent* on $x$ of $C \in P$ and $D \in N$ is $(C \setminus \{x\}) \cup (D \setminus \{\neg x\})$. A resolvent is a *tautology* when it holds a literal and its negation. For a literal $\ell$, $F|\ell$ is $F$ with the clauses that contain $\ell$ removed and $\neg\ell$ removed from the others.

```pseudo id=main
DP(F)
L1  loop
L2      if F has the empty clause then return UNSAT
L3      if F = ∅ then return SAT and the model rebuilt from the record
L4      if F has a unit clause {ℓ} then record ℓ, F ← F|ℓ, continue
L5      if F has a pure literal ℓ then record ℓ, F ← F|ℓ, continue
L6      x ← a variable of F with the smallest |P| · |N|
L7      P ← the clauses with x, N ← the clauses with ¬x
L8      R ← the resolvents on x of all pairs in P × N that are not tautologies
L9      F ← (F \ (P ∪ N)) ∪ R, record (x, P)
```

To rebuild a model, start with every variable false, and go through the record from the last step to the first. For a recorded literal $\ell$, make $\ell$ true. For a recorded $(x, P)$, set $x$ to false if every clause of $P$ has a true literal other than $x$, and to true otherwise.

The rule of line L6 is a common choice; Davis and Putnam left the order open. Line L5 removes clauses and line L4 shortens them, so both only make $F$ smaller. Only line L9 can make $F$ grow: it removes $|P| + |N|$ clauses and adds up to $|P| \cdot |N|$.

## Example

Take the 5 clauses $\{x_1, x_2\}, \{\neg x_1, x_3\}, \{\neg x_2, x_3\}, \{\neg x_3, x_4\}, \{\neg x_3, \neg x_4\}$. No clause is unit, and no literal is pure. The products $|P| \cdot |N|$ are 1 for $x_1$, $x_2$ and $x_4$, and 4 for $x_3$, so the procedure eliminates $x_1$.

| step | rule | variable or literal | formula after the step |
|---|---|---|---|
| 1 | eliminate (L9) | $x_1$ | $\{x_2, x_3\}, \{\neg x_2, x_3\}, \{\neg x_3, x_4\}, \{\neg x_3, \neg x_4\}$ |
| 2 | eliminate (L9) | $x_2$ | $\{x_3\}, \{\neg x_3, x_4\}, \{\neg x_3, \neg x_4\}$ |
| 3 | unit (L4) | $x_3$ | $\{x_4\}, \{\neg x_4\}$ |
| 4 | unit (L4) | $\neg x_4$ | the empty clause |

Line L2 then returns UNSAT. The steps form a resolution refutation: $\{x_2, x_3\}$ from the first two clauses, $\{x_3\}$ from it and the third, and the empty clause from $\{x_3\}$ and the last two.

A satisfiable case shows the rebuilding. For $\{x_1, x_2\}, \{\neg x_1, x_2\}, \{x_1, \neg x_2\}, \{\neg x_1, \neg x_2, x_3\}, \{x_3, x_4\}$, the procedure makes the pure literal $x_3$ true, which leaves the first three clauses. Then it eliminates $x_1$ with $P = \{\{x_1, x_2\}, \{x_1, \neg x_2\}\}$: the only resolvent that is not a tautology is $\{x_2\}$, and the unit rule makes $x_2$ true and leaves $F = \emptyset$. In reverse, $x_2$ becomes true. The clause $\{x_1, \neg x_2\}$ of $P$ has no true literal other than $x_1$, so $x_1$ becomes true. Then $x_3$ becomes true, and $x_4$ keeps the value false. The result $x_1 x_2 x_3 \neg x_4$ satisfies all five clauses.

## Correctness

Elimination keeps satisfiability. In one direction, each resolvent follows from its two parent clauses, so a model of $F$ is a model of the new formula. In the other direction, take a model $\beta$ of the new formula. If every clause of $P$ is true in $\beta$ without $x$, set $x$ false, which makes every clause of $N$ true. Otherwise some $C \in P$ has only $x$ true, so set $x$ true. For each $D \in N$, the resolvent of $C$ and $D$ is true in $\beta$ (or it is a tautology), and since $C \setminus \{x\}$ is false, $D \setminus \{\neg x\}$ has a true literal. So the extended assignment satisfies $F$. The unit and pure rules keep satisfiability too, and each step removes a variable, so there are at most $n$ steps. The rebuilding applies the extension step by step in reverse. The full proof is below.

## Complexity

Each step removes a variable, so there are at most $n$ steps. The cost of a step depends on the size of the formula, which can grow fast. With duplicate clauses merged, a formula over $j$ variables has at most $3^j$ clauses, which gives the crude bounds of $O(n^2\, 9^n)$ time and $O(n\, 3^n)$ space.

The growth is real. An UNSAT run gives a resolution refutation of $F$ (an [ordered resolution](/ordered-resolution/) refutation in the elimination order), so [Haken's lower bound](/haken-resolution-lower-bound/) for the pigeonhole formulas and the bounds of Chvátal and Szemerédi for random formulas apply: on these formulas every run has exponential size, with every elimination order. In the other direction, Rish and Dechter showed that with a fixed order, the cost is bounded by $n$ times a function exponential in the *induced width* $w$ of the order: the largest number of earlier neighbours of a variable in the interaction graph, after the edges added by elimination. So the procedure is fast on formulas with small treewidth, for example on chains and trees of clauses.

## Properties

- **No search.** The procedure never guesses and never backtracks. Each step is forced.
- **Sound and complete.** It returns UNSAT only for unsatisfiable formulas, and it returns a model otherwise.
- **A proof of UNSAT.** The resolvents form a resolution refutation that a checker can verify.
- **Order dependent.** The size of the intermediate formulas depends strongly on the order of elimination. The smallest induced width over all orders is the [treewidth](/treewidth/) of the interaction graph, and computing it is NP-hard. Directional resolution is the [bucket elimination](/bucket-elimination/) scheme applied to clauses.
- **Memory bound.** The procedure keeps the whole formula, and the formula may grow at each step. This is its main weakness.

## Variants and improvements

- **Splitting instead of elimination.** [DPLL](/dpll/) replaces line L9 by a split on $x$. This uses little memory, at the cost of a search.
- **Bounded variable elimination.** Eliminate $x$ only when $|R|$ is at most $|P| + |N|$, after removing subsumed resolvents. This is a standard preprocessing step of [CDCL](/cdcl/) solvers ([bounded variable elimination](/bounded-variable-elimination/)).
- **Directional resolution.** Fix the order in advance, and keep the resolvents in buckets, one per variable. Rish and Dechter analysed this form and showed that it compiles the formula: after the run, a model can be found without backtracking.
- **Subsumption.** Remove each clause that contains another clause. This keeps the formula small and does not change its models ([clause subsumption](/clause-subsumption/)).

## When to use it

Use full elimination for formulas with small induced width, where the formula stays small for a good order. Use bounded elimination as preprocessing before a CDCL solver. For general formulas, the full procedure runs out of memory, and [DPLL](/dpll/) or [CDCL](/cdcl/) is better.

## Pitfalls

- **Keeping tautologies.** A resolvent with $y$ and $\neg y$ is always true. Keeping it makes the formula larger and changes nothing.
- **Forgetting the record.** The final formula is empty and says nothing about the eliminated variables. Keep the clauses of $P$ for each step, or the model cannot be rebuilt.
- **Rebuilding in the wrong order.** Go from the last step to the first. The value of an eliminated variable depends on the values of the variables that were eliminated after it.
- **Duplicates.** Without merging duplicate clauses, the formula grows faster than it needs to.

## Implementations

## History

Davis and Putnam (1960) gave the procedure as the propositional part of a proof procedure for first-order logic based on Herbrand's theorem. Their rules were the one-literal rule, the affirmative-negative rule (pure literals) and the rule for eliminating atomic formulas, which is variable elimination by resolution. Davis, Logemann and Loveland (1962) found that elimination needed too much memory, and replaced it with splitting, which gave [DPLL](/dpll/). Dechter and Rish revived elimination in 1994 as directional resolution, with an analysis in terms of induced width. Eén and Biere (2005) made bounded variable elimination a standard preprocessing step in the SatELite preprocessor.

## References
