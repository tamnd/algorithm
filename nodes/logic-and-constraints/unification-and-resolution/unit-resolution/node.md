---
tag: HX313Y
kind: algorithm
slug: unit-resolution
name: Unit resolution
aliases:
- unit propagation resolution
- unit-resulting resolution restriction
- unit refutation
area: logic-and-constraints/unification-and-resolution
level: intro
summary: Restricted resolution in which one parent is always a unit clause. It is refutation complete for Horn clauses, not in general, and it refutes the same sets as input resolution (Chang 1970).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {n: the number of distinct atoms of a ground input, m: the number of input clauses}
  time: {worst: O(n^2 m^2 4^n)}
  space: {extra: O(n m 2^n)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: false}
history:
  year: 1964
  people: [Lawrence Wos, Daniel Carson, George Robinson]
  note: The Argonne group used unit preference in its provers; Chang (1970) showed that unit and input refutations exist for the same sets, and Henschen and Wos (1974) showed completeness for Horn sets.
prereqs: [binary-resolution, robinson-resolution, unit-clause, horn-clause]
see_also: [input-resolution, unit-propagation, horn-sat-forward-chaining, sld-resolution, set-of-support, linear-resolution]
sources:
  - paper: "Chin-Liang Chang, The unit proof and the input proof in theorem proving, Journal of the ACM 17(4), 698-707, 1970"
    locator: the main theorem, a set of clauses has a unit refutation if and only if it has an input refutation
  - paper: "Lawrence J. Henschen and Lawrence Wos, Unit refutations and Horn sets, Journal of the ACM 21(4), 590-605, 1974"
    locator: unit resolution is refutation complete for Horn sets
  - paper: "Lawrence Wos, Daniel Carson and George A. Robinson, The unit preference strategy in theorem proving, AFIPS Conference Proceedings 26 (Fall Joint Computer Conference), 615-621, 1964"
    locator: the unit preference strategy, which picks unit clauses first without restricting resolution
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 1984
    locator: the linear-time algorithm with a counter for each clause
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 7, unit resolution and input resolution
---

Unit resolution is the restriction of [Robinson's resolution principle](/robinson-resolution/) in which every resolution step has a [unit clause](/unit-clause/), a clause with one literal, as one of its parents. Each step makes the other parent shorter by one literal, so the procedure is fast and its clauses stay small. The price is completeness: unit resolution refutes every unsatisfiable set of [Horn clauses](/horn-clause/), but some unsatisfiable sets with no unit clause have no unit refutation at all. Chang (1970) proved that unit resolution and [input resolution](/input-resolution/) refute exactly the same sets.

## In plain words

You have a list of rules, each an "or" of facts, and you want to show that they cannot all hold. A rule with one fact is a plain claim. Use only plain claims to cut other rules: if a claim says that a fact holds, remove the denial of that fact from every rule that has it. Each cut gives a shorter rule, and a rule that drops to one fact becomes a new claim. If a claim and its denial both appear, the rules are contradictory.

This is fast, because rules only get shorter. But it can get stuck. If every rule has two or more facts, there is nothing to cut with, even when the rules do clash. For rules with at most one positive fact, the method never gets stuck.

## The problem

The input is a finite set $S$ of first-order clauses, and the question is whether $S$ is unsatisfiable. The procedure answers UNSAT with a refutation, SATURATED when no new unit step is possible, or UNKNOWN at a limit. UNSAT is always right. SATURATED means that $S$ is satisfiable when $S$ is a Horn set, and nothing in general.

A **unit resolvent** is a [binary resolvent](/binary-resolution/) of two clauses one of which has exactly one literal. If $\{L\}$ and $D \vee \neg L'$ are renamed apart and $\sigma$ is a most general unifier of the atoms $L$ and $L'$, the unit resolvent is $D\sigma$. A **Horn clause** has at most one positive literal.

## The algorithm

The loop is the given-clause loop of [Robinson's resolution principle](/robinson-resolution/), with one test added at line L9.

```pseudo id=main
UNIT-RESOLUTION(S, limit, k)
L1  passive ← S, active ← ∅
L2  while passive ≠ ∅
L3      G ← the lightest clause of passive, but the oldest one at every k-th pick; remove G from passive
L4      if G = □ then return UNSAT
L5      if G is a tautology or a clause of active subsumes G then continue
L6      remove from active every clause that G subsumes
L7      active ← active ∪ {G}; N ← the factors of G
L8      for each clause A of active
L9          if G or A is a unit clause then N ← N ∪ the binary resolvents of G and A
L10     passive ← passive ∪ (N minus the clauses that were stored before)
L11     if more than limit clauses were stored then return UNKNOWN
L12 return SATURATED
```

Line L9 is the only change: a resolvent is formed only when one parent has one literal. Factors are still formed at line L7. For first-order Horn sets factoring is not needed, but for a set such as $\{P(x),\ \neg P(u) \vee \neg P(v)\}$ it gives the unit $\neg P(u)$ at once.

## Example

Take the propositional set

$$0: \neg p \vee \neg q \vee r, \quad 1: \neg r \vee s, \quad 2: p, \quad 3: q, \quad 4: \neg s.$$

It is a Horn set, and it is unsatisfiable: $p$ and $q$ force $r$, then $s$, which clashes with $\neg s$. The run uses $k = 5$.

| pick | G | why picked | unit resolvents | new clauses |
|---|---|---|---|---|
| 1 | 2: $p$ | lightest | none: no clause of active has $\neg p$ | none |
| 2 | 3: $q$ | lightest | none | none |
| 3 | 4: $\neg s$ | lightest | none | none |
| 4 | 1: $\neg r \vee s$ | lightest | with 4 | 5: $\neg r$ |
| 5 | 0: $\neg p \vee \neg q \vee r$ | oldest (5th pick) | with 2, with 3 | 6: $\neg q \vee r$, 7: $\neg p \vee r$ |
| 6 | 5: $\neg r$ | lightest | with 0 | 8: $\neg p \vee \neg q$ |
| 7 | 6: $\neg q \vee r$ | lightest, then smallest number | with 3, with 5 | 9: $r$, 10: $\neg q$ |
| 8 | 9: $r$ | lightest | with 5 | 11: $\square$ |
| 9 | 11: $\square$ | weight 0 | return UNSAT | |

The refutation is $6 = 0 \otimes 2$, $9 = 6 \otimes 3$, $5 = 1 \otimes 4$ and $11 = 9 \otimes 5$, where $\otimes$ marks a resolution step. In every step one parent is a unit.

Now take the four clauses $p \vee q$, $\neg p \vee q$, $p \vee \neg q$ and $\neg p \vee \neg q$. They are unsatisfiable, because each of the four assignments of $p$ and $q$ makes one clause false. There is no unit clause and no factor, so line L9 never fires and the loop returns SATURATED after four picks. Full resolution refutes the set in three steps: $q$ from the first two clauses, $\neg q$ from the last two, and then $\square$.

## Correctness

Each unit resolvent is a binary resolvent, so it follows from its parents, and UNSAT is always right. For completeness, suppose $S$ is an unsatisfiable set of Horn clauses. By [Herbrand's theorem](/herbrand-theorem/), a finite set $T$ of ground instances is unsatisfiable. The atoms that the definite clauses of $T$ force, by repeated unit steps from the positive units, form the least model of the definite part. If no unit step reached $\square$, this set of atoms would satisfy every clause of $T$, so some unit step reaches $\square$. Each such ground unit step lifts to a unit step between clauses of $S$ or their factors, as in the [lifting lemma](/lifting-lemma/), because a ground unit is an instance of a clause that becomes a unit after factoring. With a fair line L3 the loop finds the lifted refutation. The full proof, with the deletion of subsumed clauses, is in the proof file.

## Complexity

On first-order input the loop need not stop: $\{P(a),\ \neg P(x) \vee P(f(x))\}$ gives $P(f(a)), P(f(f(a))), \ldots$ forever.

On a ground input with $n$ atoms and $m$ clauses, each unit resolvent of a unit $\{L\}$ and a clause $D$ is $D$ minus one literal, or $\square$. So every stored clause is a subset of an input clause, and there are at most $m\,2^n$ stored clauses and picks. In one pick, lines L5 and L6 compare $G$ with at most $m\,2^n$ active clauses at $O(n^2)$ each, and lines L8 and L9 make at most $n$ resolvents for each active clause at $O(n \log n)$ each. All picks cost $O(n^2 m^2 4^n)$ time, and the stored clauses take $O(n m\, 2^n)$ space. This bound is loose. For propositional input the same inferences are [unit propagation](/unit-propagation/), and with a counter for each clause, [forward chaining](/horn-sat-forward-chaining/) does them in time linear in the total size of the clauses (Dowling and Gallier 1984).

## Properties

- **Sound.** Every UNSAT answer comes with a refutation.
- **Complete for Horn sets.** With no limit and a fair line L3, an unsatisfiable Horn set gives UNSAT (Henschen and Wos 1974).
- **Not complete in general.** The four clauses over $p$ and $q$ above are unsatisfiable and have no unit refutation.
- **Same power as input resolution.** A set has a unit refutation if and only if it has an [input refutation](/input-resolution/) (Chang 1970).
- **Clauses only shrink.** Each unit resolvent of a unit and a clause $D$ has fewer literals than $D$ in the ground case.
- **Not exact.** SATURATED does not mean satisfiable unless the input is a Horn set, so the front matter marks the procedure as not exact.

## Variants and improvements

- **Unit preference.** Wos, Carson and Robinson (1964) did not restrict resolution to units; they only picked unit clauses first. This keeps completeness, and it is what the weight order at line L3 does in a general prover.
- **Unit-resulting resolution.** A clause with $k + 1$ literals is resolved at once with $k$ units, and the result is a new unit. Otter and Prover9 offer it as a rule, called UR-resolution.
- **Unit propagation.** For propositional clauses, unit resolution is [unit propagation](/unit-propagation/), the inner loop of [DPLL](/dpll/) and [CDCL](/cdcl/). There it is a deduction step inside a search, not a full prover.
- **Renamable Horn sets.** If flipping the sign of some predicate symbols in all clauses gives a Horn set, unit resolution is still complete, because flipping a sign in every clause does not change which unit steps exist.
- **SLD resolution.** For Horn clauses with one negative goal, [SLD resolution](/sld-resolution/) is also complete. It is linear input resolution, and Chang's theorem links it to unit resolution.

## When to use it

Use unit resolution as a fast first pass, or as the whole prover for Horn problems such as Datalog rules, type rules and many verification conditions. For non-Horn input, use it as a preference, not a restriction: pick units first and still allow all resolvents. For propositional Horn satisfiability, use the linear-time [Horn-SAT forward chaining](/horn-sat-forward-chaining/) instead of this loop.

## Pitfalls

- **Reading SATURATED as satisfiable.** Line L12 proves satisfiability only for Horn input. For the four clauses over $p$ and $q$ it returns SATURATED on an unsatisfiable set. Check that the input is Horn before you trust the answer.
- **Forgetting factors.** If line L7 does not form factors, the set $\{P(x) \vee P(y),\ \neg P(u) \vee \neg P(v)\}$ has no unit clause, and the loop stops with SATURATED. With line L7, the factors $P(x)$ and $\neg P(u)$ are units, and they resolve to $\square$. Keep line L7, even though Horn sets do not need it.
- **Unit by count, not by size.** In line L9 a "unit" is a clause with one literal after duplicates are merged. A clause such as $P(x) \vee P(x)$ is a unit only when it is stored as a set. Build clauses as sets, as line L10 does.
- **Subsumption across the restriction.** Line L6 may delete a non-unit clause that a new unit subsumes. That is safe here, because a unit that subsumes a clause can do every unit step that the clause can do.

## Implementations

## History

The Argonne group of Lawrence Wos, Daniel Carson and George Robinson introduced the unit preference strategy in 1964, in the first years of resolution provers. Chin-Liang Chang (1970) proved that unit refutations and input refutations exist for the same sets of clauses. Lawrence Henschen and Lawrence Wos (1974) proved that unit resolution is complete for Horn sets. Dowling and Gallier (1984) gave the linear-time algorithm for propositional Horn satisfiability, which is unit resolution with counters.

## References
