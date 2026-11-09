---
tag: BWG1RS
kind: algorithm
slug: input-resolution
name: Input resolution
aliases:
- input refutation
- input strategy
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Resolution in which every step has an input clause as one parent. Complete for Horn clauses but not in general, and it refutes exactly the sets that unit resolution refutes (Chang 1970).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {n: the number of distinct atoms of a ground input}
  time: {worst: O(n^3 9^n)}
  space: {extra: O(n 4^n)}
properties: {deterministic: true, exact: false, online: false, recursive: false, in_place: false}
history:
  year: 1970
  people: [Chin-Liang Chang]
  note: Chang proved that a set of clauses has an input refutation if and only if it has a unit refutation.
prereqs: [binary-resolution, robinson-resolution, horn-clause]
see_also: [unit-resolution, linear-resolution, sld-resolution, set-of-support, logic-programming]
sources:
  - paper: "Chin-Liang Chang, The unit proof and the input proof in theorem proving, Journal of the ACM 17(4), 698-707, 1970"
    locator: the main theorem, a set of clauses has a unit refutation if and only if it has an input refutation
  - paper: "Lawrence J. Henschen and Lawrence Wos, Unit refutations and Horn sets, Journal of the ACM 21(4), 590-605, 1974"
    locator: unit resolution is refutation complete for Horn sets, and so input resolution is too
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 7, unit resolution and input resolution
  - book: isbn:9783540181999
    title: John W. Lloyd, Foundations of Logic Programming, second edition, Springer, 1987
    locator: Chapter 2, soundness and completeness of SLD resolution
---

Input resolution is the restriction of [Robinson's resolution principle](/robinson-resolution/) in which every resolution step has an input clause, or a [factor](/factoring/) of one, as one of its parents. The other parent can be any clause derived so far. Chang (1970) proved that a set of clauses has an input refutation if and only if it has a [unit refutation](/unit-resolution/), so the two restrictions have the same power: both are complete for [Horn clauses](/horn-clause/) and both fail on some unsatisfiable sets that are not Horn. For Horn clauses, the linear form of input resolution is [SLD resolution](/sld-resolution/), the proof procedure of Prolog.

## In plain words

You have a fixed list of rules, each an "or" of facts, and you want to show that they cannot all hold. You may combine two rules that clash on a fact, but one of the two must always come from your first list. The new rules you make can be combined with first-list rules, but never with each other.

This keeps the search small, because one side of every step comes from a short, fixed list. It works whenever each rule has at most one positive fact. But it can get stuck on other rules: if no rule on the first list is a single fact, the very last step, which must give the empty rule, can never happen.

## The problem

The input is a finite set $S$ of first-order clauses, and the question is whether $S$ is unsatisfiable. The answers are UNSAT with a refutation, SATURATED when no new input step is possible, or UNKNOWN at a limit. UNSAT is always right. SATURATED means that $S$ is satisfiable when $S$ is a Horn set, and nothing in general.

An **input resolvent** is a [binary resolvent](/binary-resolution/) of two clauses, one of which is an **input clause**: a clause of $S$ or a factor of an input clause. An **input refutation** is a derivation of $\square$ in which every resolution step is an input step.

## The algorithm

The loop is the given-clause loop of [Robinson's resolution principle](/robinson-resolution/). Each clause carries a mark that says whether it is an input clause, and two lines change.

```pseudo id=main
INPUT-RESOLUTION(S, limit, k)
L1  passive ← S with every clause marked as input, active ← ∅
L2  while passive ≠ ∅
L3      G ← the lightest clause of passive, but the oldest one at every k-th pick; remove G from passive
L4      if G = □ then return UNSAT
L5      if G is a tautology, or a clause A of active subsumes G where A is marked or G is not, then continue
L6      remove from active every clause A that G subsumes, except a marked A when G is not marked
L7      active ← active ∪ {G}
L8      N ← the factors of G, marked when G is marked
L9      for each clause A of active, if G or A is marked, add to N the binary resolvents of G and A, not marked
L10     passive ← passive ∪ (N minus the clauses that were stored before with the same mark)
L11     if more than limit clauses were stored then return UNKNOWN
L12 return SATURATED
```

Line L9 is the restriction. Lines L5 and L6 protect the marked clauses: a derived clause may not delete an input clause by subsumption, because only an input clause may be a side parent at line L9. If an unmarked clause deleted an input clause, a step that the input clause could make would be lost. Line L10 compares a clause together with its mark, so the same clause can be stored once as an input and once as derived.

## Example

Take the Horn set of the [unit resolution](/unit-resolution/) page:

$$0: \neg p \vee \neg q \vee r, \quad 1: \neg r \vee s, \quad 2: p, \quad 3: q, \quad 4: \neg s.$$

The run uses $k = 5$. Clauses 0 to 4 are marked; all new clauses are not.

| pick | G | why picked | input resolvents | new clauses |
|---|---|---|---|---|
| 1 | 2: $p$ | lightest | none | none |
| 2 | 3: $q$ | lightest | none | none |
| 3 | 4: $\neg s$ | lightest | none | none |
| 4 | 1: $\neg r \vee s$ | lightest | with 4 | 5: $\neg r$ |
| 5 | 0: $\neg p \vee \neg q \vee r$ | oldest | with 2, 3 and 1 | 6: $\neg q \vee r$, 7: $\neg p \vee r$, 8: $\neg p \vee \neg q \vee s$ |
| 6 | 5: $\neg r$ | lightest | with 0 | 9: $\neg p \vee \neg q$ |
| 7 | 6: $\neg q \vee r$ | lightest | with 3 and 1; not with 5, as neither is input | 10: $r$, 11: $\neg q \vee s$ |
| 8 | 10: $r$ | lightest | with 1; not with 5 | 12: $s$ |
| 9 | 12: $s$ | lightest | with 4 | 13: $\square$ |
| 10 | 7: $\neg p \vee r$ | oldest | subsumed by 10, deleted at L5 | none |
| 11 | 13: $\square$ | weight 0 | return UNSAT | |

The refutation is $6 = 0 \otimes 2$, $10 = 6 \otimes 3$, $12 = 10 \otimes 1$ and $13 = 12 \otimes 4$. Each step uses one of the clauses 0 to 4, and each step also uses the clause made by the step before. So this is also a [linear](/linear-resolution/) input refutation, which is the shape of an [SLD](/sld-resolution/) derivation. The unit run on the same set resolves $r$ with the derived unit $\neg r$ at its last step, which input resolution may not do.

## Correctness

Each input resolvent is a binary resolvent, so it follows from its parents, and UNSAT is always right.

**Complete for Horn sets.** Let $S$ be an unsatisfiable set of Horn clauses. Take a finite unsatisfiable set $T$ of ground instances ([Herbrand's theorem](/herbrand-theorem/)). Its definite clauses have a least model $M$, and some negative clause of $T$ is false in $M$, so all of its atoms are in $M$. Replace one atom of this negative clause by the body of a definite clause that put the atom into $M$ first. The result is again negative, and the stages at which its atoms entered $M$ form a smaller multiset. So the replacements end in $\square$. Each replacement is an input step, and the lifting argument turns the ground derivation into an input derivation from $S$.

**Not complete in general.** The last step of an input refutation resolves two units, one of which is an input clause or a factor of one. The set $\{p \vee q,\ \neg p \vee q,\ p \vee \neg q,\ \neg p \vee \neg q\}$ is unsatisfiable, but no input clause has one literal, so it has no input refutation.

The full proof, with the marks at lines L5 and L6, is in the proof file. Chang's equivalence with unit resolution is not proved there; see Chang (1970) or Chapter 7 of Chang and Lee.

## Complexity

On first-order input the loop need not stop: $\{P(a),\ \neg P(x) \vee P(f(x))\}$ gives $P(f(a)), P(f(f(a))), \ldots$ forever.

On ground input with $n$ atoms, the count is the one of [Robinson's resolution principle](/robinson-resolution/), doubled by the mark. There are at most $4^n$ clauses over $n$ atoms, so at most $2 \cdot 4^n$ stored pairs of a clause and a mark, and at most $2 \cdot 3^n$ of them are not tautologies. Only these reach line L7. Each of them meets at most $2 \cdot 3^n$ active clauses at lines L5, L6 and L9, at $O(n^2)$ for a subsumption test and $O(n \log n)$ for each of at most $n$ resolvents. The total time is $O(n^3\, 9^n)$, and the stored clauses take $O(n\, 4^n)$ space. Input resolution does not make the ground worst case polynomial: unlike a unit resolvent, an input resolvent can be longer than both parents.

## Properties

- **Sound.** Every UNSAT answer comes with a refutation in which each step has an input parent.
- **Complete for Horn sets.** With no limit and a fair line L3, an unsatisfiable Horn set gives UNSAT.
- **Not complete in general.** A set with no unit input clause and no unit factor of one has no input refutation.
- **Same power as unit resolution.** A set has an input refutation if and only if it has a unit refutation (Chang 1970). On ground sets, the tests check this on 600 random sets.
- **Not exact.** SATURATED proves satisfiability only for Horn input.

## Variants and improvements

- **Linear input resolution.** If each step must also use the clause made by the step before, the refutations are chains. This is still complete for Horn sets when the chain starts from a negative clause, and it is [SLD resolution](/sld-resolution/) when a selection rule picks the literal to resolve.
- **Linear resolution.** If the side parent may also be an earlier clause of the chain, not only an input clause, the restriction becomes complete for all clause sets. That is [linear resolution](/linear-resolution/) (Loveland 1970, Luckham 1970).
- **Set of support.** Requiring one parent to come from a chosen support set, instead of from the input, gives the [set-of-support strategy](/set-of-support/), which is complete when the clauses outside the support are satisfiable.
- **Unit resolution.** The dual restriction, where one parent must have one literal, refutes the same sets; see [unit resolution](/unit-resolution/).

## When to use it

Use input resolution, in its linear form, for Horn clauses with a goal, as Prolog and Datalog engines do. The small fixed set of side parents makes indexing easy and memory small. Do not use it as the whole prover for clauses that are not Horn: it will report SATURATED on unsatisfiable sets.

## Pitfalls

- **Subsumption deletes an input clause.** If line L5 or L6 lets a derived clause delete an input clause, the run can lose its only side parent. For example, a derived unit $r$ subsumes the input clause $r \vee s$, but only $r \vee s$ may be the side parent of later steps. Keep the mark test in lines L5 and L6.
- **Factors lose the mark.** If line L8 does not mark the factors of marked clauses, the set $\{P(x) \vee P(y),\ \neg P(u) \vee \neg P(v)\}$ has no input refutation, because the last step needs the unit factors $P(x)$ and $\neg P(u)$ as input clauses. Mark them.
- **Reading SATURATED as satisfiable.** For the four clauses over $p$ and $q$ above, line L12 returns SATURATED on an unsatisfiable set. Trust it only for Horn input.
- **Counting a derived clause as input.** If line L10 drops the mark when it finds the same clause stored as an input, or the other way round, the run can make steps that are not input steps. Compare clauses together with their marks.

## Implementations

## History

Input resolution grew out of the strategies that the Argonne group tried in the 1960s. Chin-Liang Chang (1970) defined unit proofs and input proofs and proved that a set has one if and only if it has the other. Chang and Lee's book (1973) presented the result together with linear resolution. Henschen and Wos (1974) proved that unit refutations exist for all unsatisfiable Horn sets, so input refutations do too. Robert Kowalski and Donald Kuehner (1971) restricted linear resolution further with a selection function, and Kowalski (1974) used its Horn case as the basis of logic programming, which became SLD resolution.

## References
