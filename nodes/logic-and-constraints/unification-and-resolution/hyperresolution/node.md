---
tag: BHQ7B0
kind: algorithm
slug: hyperresolution
name: Hyperresolution
aliases:
- hyper-resolution
- positive hyperresolution
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Resolves all negative literals of a nucleus at once with positive electron clauses under one unifier, so every derived clause is positive. Refutation complete with factoring (Robinson 1965).
solves: [first-order-theorem-proving]
model: word-ram
complexity:
  vars: {n: the number of distinct atoms of a ground input, m: the number of input clauses, k: the largest number of negative literals in an input clause}
  time: {worst: O(k m (n 2^n)^(k+1))}
  space: {extra: O(n (m + 2^n))}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1965
  people: [John Alan Robinson]
  note: Robinson introduced hyperresolution in the same year as the resolution principle, as a way to skip the mixed clauses that binary resolution builds.
prereqs: [binary-resolution, robinson-resolution, most-general-unifier]
see_also: [ordered-resolution, set-of-support, unit-resolution, horn-sat-forward-chaining, robinson-completeness-theorem, lifting-lemma]
sources:
  - paper: "John Alan Robinson, Automatic deduction with hyper-resolution, International Journal of Computer Mathematics 1, 227-234, 1965"
    locator: the definition of hyperresolution and its completeness
  - paper: "James R. Slagle, Automatic theorem proving with renamable and semantic resolution, Journal of the ACM 14(4), 687-697, 1967"
    locator: semantic resolution, of which positive hyperresolution is the case of the interpretation that makes every atom false
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 6, semantic resolution and hyperresolution
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (hyperresolution as ordered resolution with selection of all negative literals)
---

Hyperresolution is a restriction of [Robinson's resolution principle](/robinson-resolution/) that does many [binary resolution](/binary-resolution/) steps as one. A **nucleus** is a clause with at least one negative literal. **Electrons** are positive clauses, clauses with no negative literal. One hyperresolution step resolves every negative literal of a nucleus, each with a literal of an electron, under one simultaneous most general unifier. The result, the **hyperresolvent**, has only positive literals, so it is an electron again. Robinson introduced the rule in 1965 and proved that hyperresolution with factoring of electrons is refutation complete. For Horn clauses it is forward chaining.

## In plain words

Think of a rule like "if $A$ and $B$ then $C$ or $D$". The "if" part lists conditions, and the "then" part lists outcomes. Hyperresolution waits until it has facts for every condition of a rule. Then it fires the rule once and writes down the outcome, together with the leftover outcomes of the facts it used.

So it only ever writes down positive facts or lists of positive possibilities. It never stores a half-used rule, as plain resolution does. Rules are used only as rules, and facts only as facts.

If a rule has only conditions and no outcome, firing it gives the empty statement. That means the conditions cannot all hold, and the whole set of rules is contradictory.

## The problem

The input is a finite set $S$ of first-order clauses, and the question is whether $S$ is unsatisfiable. The answers are UNSAT with a refutation, SATURATED, which means that $S$ is satisfiable, and UNKNOWN at a limit.

Let $N = \neg A_1 \vee \cdots \vee \neg A_k \vee B$ be a nucleus, where $B$ is the positive part, and let $E_1 \vee L_1, \ldots, E_k \vee L_k$ be electrons, all renamed apart, with $L_i$ a positive literal. If $\sigma$ is a most general simultaneous unifier of the pairs $(A_1, L_1), \ldots, (A_k, L_k)$, the **hyperresolvent** is

$$(B \vee E_1 \vee \cdots \vee E_k)\sigma.$$

It is positive. The same electron may fill several slots, each time with fresh variables. Only the nuclei of $S$ are used, because every derived clause is positive. The page's code finds $\sigma$ as one most general unifier of the two terms $\mathrm{tuple}(A_1, \ldots, A_k)$ and $\mathrm{tuple}(L_1, \ldots, L_k)$.

## The algorithm

The loop is the given-clause loop of [Robinson's resolution principle](/robinson-resolution/) on the electrons only. The nuclei stay outside the loop.

```pseudo id=main
HYPERRESOLUTION(S, limit, k)
L1  nuclei ← the clauses of S with a negative literal; passive ← the positive clauses of S; active ← ∅
L2  while passive ≠ ∅
L3      G ← the lightest clause of passive, but the oldest one at every k-th pick; remove G from passive
L4      if G = □ then return UNSAT
L5      if a clause of active subsumes G then continue
L6      remove from active every clause that G subsumes
L7      active ← active ∪ {G}
L8      N ← the factors of G, and every hyperresolvent of a nucleus with electrons from active, at least one of them G
L9      passive ← passive ∪ (N minus the clauses that were stored before)
L10     if more than limit clauses were stored then return UNKNOWN
L11 return SATURATED
```

Line L8 requires $G$ among the electrons, because the steps with older electrons only were done when the last of them was picked. A positive clause is never a tautology, so line L5 has no tautology test. Factoring is applied to electrons only. A nucleus needs no factors, because one electron may fill two slots.

## Example

Take the transitivity nucleus and four clauses:

$$0: \neg L(x, y) \vee \neg L(y, z) \vee L(x, z), \quad 1: L(a,b), \quad 2: L(b,c), \quad 3: L(c,d), \quad 4: \neg L(a,d).$$

The nuclei are 0 and 4. The electrons 1, 2 and 3 go to passive. The run uses $k = 5$.

| pick | G | why picked | hyperresolvents with G | new clauses |
|---|---|---|---|---|
| 1 | 1: $L(a,b)$ | lightest | none: nucleus 0 needs a chain of two | none |
| 2 | 2: $L(b,c)$ | lightest | nucleus 0 with 1 and 2, $\sigma = \{x \mapsto a, y \mapsto b, z \mapsto c\}$ | 5: $L(a,c)$ |
| 3 | 3: $L(c,d)$ | lightest | nucleus 0 with 2 and 3 | 6: $L(b,d)$ |
| 4 | 5: $L(a,c)$ | lightest | nucleus 0 with 5 and 3 | 7: $L(a,d)$ |
| 5 | 6: $L(b,d)$ | oldest | nucleus 0 with 1 and 6 gives $L(a,d)$ again | none (stored before) |
| 6 | 7: $L(a,d)$ | lightest | nucleus 4 with 7, $\sigma = \{\}$ | 8: $\square$ |
| 7 | 8: $\square$ | weight 0 | return UNSAT | |

The refutation is $5 = \mathrm{hyper}(0; 1, 2)$, $7 = \mathrm{hyper}(0; 5, 3)$ and $8 = \mathrm{hyper}(4; 7)$. Binary resolution would also build mixed clauses such as $\neg L(b, z) \vee L(a, z)$; hyperresolution never stores them.

## Correctness

A hyperresolvent is the result of $k$ binary resolution steps, so it follows from its parents, and UNSAT is always right.

For completeness, suppose that the loop never finds $\square$. The ground argument builds a model. Order the ground atoms in any well-founded total order, and go through the derived ground electrons from small to large. An electron that is false so far makes its largest atom true. Every electron is then true. A ground nucleus $\neg A_1 \vee \cdots \vee \neg A_k \vee B$ with all $A_i$ true and $B$ false is impossible: each $A_i$ was made true by an electron $A_i \vee E_i$ with $E_i$ false, and the hyperresolvent $B \vee E_1 \vee \cdots \vee E_k$ would be a false electron. So the ground instances have a model. The [lifting lemma](/lifting-lemma/) turns each ground hyperresolution step into a step between clauses of the run, with factors of electrons for merged literals. The full proof, with subsumption and the fair choice at line L3, is in the proof file.

## Complexity

On first-order input the loop need not stop: $\{P(a),\ \neg P(x) \vee P(f(x))\}$ gives $P(f(a)), P(f(f(a))), \ldots$ forever.

On a ground input with $n$ atoms, $m$ clauses and at most $k$ negative literals in a clause, every stored electron is a set of positive literals, so there are at most $2^n$ of them, and at most $2^n$ picks. In one pick, line L8 tries, for each of at most $m$ nuclei, every choice of an electron and a literal position for each of at most $k$ slots, at most $(n 2^n)^k$ choices, and each choice costs $O(k n)$ to unify and to build. Lines L5 and L6 cost $O(n^2 2^n)$, which is less. The total is $O(2^n \cdot m \cdot (n 2^n)^k \cdot k n) = O(k m (n 2^n)^{k+1})$. The stored clauses take $O(n (m + 2^n))$ space.

For a ground Horn set the electrons are single atoms, there are at most $n$ of them, and hyperresolution is [forward chaining](/horn-sat-forward-chaining/), which needs only linear time with counters.

## Properties

- **Sound.** Every UNSAT answer comes with a refutation of hyperresolution and factoring steps.
- **Refutation complete.** With no limit and a fair line L3, an unsatisfiable set gives UNSAT (Robinson 1965).
- **A decision procedure for some classes.** A SATURATED answer proves satisfiability. The loop always stops on ground input. It also stops on function-free input in which every variable of a clause occurs in a negative literal of that clause, such as disjunctive Datalog, because then every electron is ground and built from the finitely many constants.
- **Positive clauses only.** All derived clauses are electrons. The nuclei are the input clauses with negative literals and never change.
- **A model on SATURATED.** For ground input, the atoms that the construction in the proof makes true form a model of the input.

## Variants and improvements

- **Negative hyperresolution.** Swap the signs: nuclei have a positive literal, electrons are negative clauses, and every derived clause is negative. It is the dual and is complete too.
- **Semantic resolution.** Slagle (1967) generalized both: fix an interpretation $I$, let electrons be clauses false in $I$, and resolve all literals of a nucleus that are true in $I$. Positive hyperresolution is the case where $I$ makes every atom false.
- **Ordered hyperresolution.** Bachmair and Ganzinger describe hyperresolution as [ordered resolution](/ordered-resolution/) with a selection function that selects all negative literals of a clause. Adding an atom ordering then restricts which literal of each electron may be used.
- **UR-resolution.** Unit-resulting resolution resolves a nucleus with units until one literal is left. It is the unit counterpart of hyperresolution, and it is incomplete in general.
- **Set of support.** Choosing the positive input clauses as the support is related, but [set of support](/set-of-support/) still forms mixed clauses.

## When to use it

Use hyperresolution when the input has many rules with several conditions, as in problems from algebra, geometry and planning, or in Datalog-like reasoning, and when you want derived clauses to stay positive. It is also a good model builder: on SATURATED, the electrons describe a model. It is weak when the goal clause is long and the electrons are many, because the number of electron choices grows as a power of the number of conditions. Provers such as Otter and Prover9 offer it as a rule, next to binary resolution and UR-resolution.

## Pitfalls

- **No factors of electrons.** If line L8 forms no factors, the set $\{P(x) \vee P(y),\ \neg P(u) \vee \neg P(v)\}$ gives only $P(y) \vee P(y')$, a variant of the electron, and the loop returns SATURATED on an unsatisfiable set. With the factor $P(x)$ at line L8, the nucleus with $P(x)$ in both slots gives $\square$.
- **The same electron in two slots.** If line L8 lets each electron fill at most one slot, the set $\{P(a),\ \neg P(x) \vee \neg P(y)\}$ has no refutation. Allow repeats, with a fresh renaming for each slot.
- **Skipping G.** If line L8 does not require $G$ among the electrons, it repeats all old steps at every pick. If it requires $G$ in one fixed slot, it misses steps. Require $G$ in at least one slot.
- **Treating derived clauses as nuclei.** Every derived clause is positive, so only the clauses of $S$ are nuclei. A loop that adds derived clauses to the nuclei wastes work and can lose the clean model reading of SATURATED.

## Implementations

## History

John Alan Robinson introduced hyperresolution in 1965, in a paper that followed his resolution paper in the same year. James Slagle (1967) generalized it to semantic resolution, with any interpretation in place of "all atoms false". Hyperresolution became a standard rule of the Argonne provers, including Otter and Prover9 by William McCune. Bachmair and Ganzinger, in their chapter of the Handbook of Automated Reasoning (2001), describe it as ordered resolution with selection, which also gives completeness with redundancy deletion.

## References
