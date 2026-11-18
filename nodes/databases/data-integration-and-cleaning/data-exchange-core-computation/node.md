---
tag: 6E0XMM
kind: algorithm
slug: data-exchange-core-computation
name: Core computation for data exchange
aliases:
- core of a universal solution
area: databases/data-integration-and-cleaning
level: research
summary: "Compute the core, the smallest universal solution: chase, then retract blocks of nulls. Polynomial in data complexity for s-t tgds, and for weakly acyclic target tgds with egds."
solves: [data-exchange-problem]
model: word-ram
complexity:
  vars: {m: the number of facts of the canonical universal solution, w: the largest number of existential variables in one tgd}
  time: {worst: O(m^(w+2))}
  space: {extra: O(m)}
properties: {deterministic: true, exact: true, online: false, in_place: false, recursive: false}
history:
  year: 2005
  people: [Ronald Fagin, Phokion G. Kolaitis, Lucian Popa]
  note: "Fagin, Kolaitis and Popa showed that all universal solutions share one core and gave polynomial algorithms for it under broad conditions. Gottlob and Nash extended this to weakly acyclic target tgds in 2008."
prereqs: [chase-algorithm, data-exchange-problem, universal-solution]
see_also: [weak-acyclicity, certain-answers, conjunctive-query-minimization, chandra-merlin-theorem, tuple-generating-dependency, equality-generating-dependency, schema-mapping]
sources:
  - paper: doi:10.1145/1061318.1061323
    title: "Ronald Fagin, Phokion G. Kolaitis and Lucian Popa, Data exchange: getting to the core, ACM TODS 30(1), 2005"
    locator: pages 174-210
  - paper: doi:10.1145/1346330.1346334
    title: "Georg Gottlob and Alan Nash, Efficient core computation in data exchange, Journal of the ACM 55(2), 2008"
    locator: the polynomial algorithm for weakly acyclic target dependencies
  - book: isbn:9781107016163
    title: "Marcelo Arenas, Pablo Barceló, Leonid Libkin and Filip Murlak, Foundations of Data Exchange, Cambridge University Press, 2014"
    locator: "Chapter 6, Good solutions"
  - paper: doi:10.1016/j.tcs.2004.10.033
    title: "Ronald Fagin, Phokion G. Kolaitis, Renée J. Miller and Lucian Popa, Data exchange: semantics and query answering, Theoretical Computer Science 336(1), 2005"
    locator: universal solutions and the chase
---

This algorithm computes the core of the universal solutions of a [data exchange problem](/data-exchange-problem/): the smallest target instance that is still a [universal solution](/universal-solution/). The page on universal solutions defines the notion and shows that many universal solutions exist. This page gives the method that picks the best one. For source-to-target tgds, it runs the chase and then folds away the redundant facts one small block of nulls at a time.

## In plain words

The chase fills the target with facts that have unknown values, called labeled nulls. It is careful but wasteful. If one rule says "each flight leaves its origin to some place" and another rule says the same in more detail, the chase writes both facts, and the short one adds nothing.

A fact is redundant when you can rename some unknown values into values that are already there and still stay inside the instance. The core is what is left when no renaming removes anything. The method takes each group of unknowns that occur together, tries all renamings of that group, and removes the facts that a renaming makes redundant. Each group is small, because each rule makes only a few unknowns. So the work stays polynomial in the size of the data.

## The problem

The input is a source instance $I$ and a finite set $\Sigma$ of source-to-target [tgds](/tuple-generating-dependency/) $\forall x\, (\varphi(x) \to \exists y\, \psi(x, y))$. Set semantics holds throughout. Values are constants or labeled nulls $\bot_1, \bot_2, \ldots$ (written N1, N2 in the code).

- A **homomorphism** $h : K \to L$ maps values to values, is the identity on constants and maps each fact of $K$ to a fact of $L$.
- An instance $C$ is a **core** if no homomorphism maps $C$ to a proper subset of $C$. A **core of** $K$ is a subset $C \subseteq K$ that is a core with a homomorphism $K \to C$.
- A **block** of $K$ is a connected part of the graph on the nulls of $K$ in which two nulls are joined when they occur in one fact.

The output is a core of the universal solutions. It is unique up to a renaming of nulls (see Correctness), so "the core" is well defined.

## The algorithm

```pseudo id=main
CORE-SOLUTION(I, Sigma)
L1  J <- CHASE(I, Sigma)                     ▷ the canonical universal solution
L2  for each block B of J, in a fixed order do
L3      F <- the facts of J that hold a null of B
L4      while some map h on the nulls of F has h(F) ⊆ J and h(F) ≠ F do
L5          J <- J minus (F minus h(F))
L6          F <- F ∩ J
L7  return J

CHASE(I, Sigma)
L8  J <- the empty instance
L9  for each tgd and each assignment of its body variables that maps the body into I do
L10     add the head to J, with fresh nulls for the existential variables
L11 return J
```

CHASE is the oblivious [chase](/chase-algorithm/) for source-to-target tgds: each trigger fires one time, even when its head already holds. The result is the canonical universal solution. In line L4, $h$ is the identity on constants and on all nulls outside $F$. The search for $h$ is a backtracking match of the facts of $F$ into $J$, with the nulls of $F$ as the variables, the same as evaluating a [conjunctive query](/conjunctive-query/) with $|F|$ atoms. Line L5 replaces $F$ by its image $h(F)$, which is already in $J$. This is the image of $J$ under the map that is $h$ on $F$ and the identity elsewhere.

## Example

The mapping has two tgds, $d_1 : \forall x, y\, (\text{Flight}(x, y) \to \exists z\, (\text{Leg}(x, z) \wedge \text{Leg}(z, y)))$ and $d_2 : \forall x, y\, (\text{Flight}(x, y) \to \exists u\, \text{Leg}(x, u))$. The source is $I = \{\text{Flight}(a, b), \text{Flight}(b, c)\}$. The chase fires four triggers and gives

$$J = \{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c), \text{Leg}(a, \bot_3), \text{Leg}(b, \bot_4)\}.$$

Each null is its own block.

| block | $F$ | a map $h$ with $h(F) \subseteq J$, $h(F) \neq F$ | facts removed |
|---|---|---|---|
| $\bot_1$ | Leg$(a, \bot_1)$, Leg$(\bot_1, b)$ | none: only $\bot_1$ has both a Leg from $a$ and a Leg to $b$ | none |
| $\bot_2$ | Leg$(b, \bot_2)$, Leg$(\bot_2, c)$ | none, for the same reason | none |
| $\bot_3$ | Leg$(a, \bot_3)$ | $\bot_3 \mapsto \bot_1$ | Leg$(a, \bot_3)$ |
| $\bot_4$ | Leg$(b, \bot_4)$ | $\bot_4 \mapsto \bot_2$ | Leg$(b, \bot_4)$ |

The core is $\{\text{Leg}(a, \bot_1), \text{Leg}(\bot_1, b), \text{Leg}(b, \bot_2), \text{Leg}(\bot_2, c)\}$. The trigger of $d_2$ adds nothing that $d_1$ does not already give. A query $Q(x, y) \text{ :- } \text{Leg}(x, z), \text{Leg}(z, y)$ gives the same null-free answers $\{(a, b), (b, c)\}$ on $J$ and on the core, because the two instances have homomorphisms each way.

## Correctness

The [proof file](proofs/correctness.md) proves the theorem below in full.

**Theorem.** For source-to-target tgds, CORE-SOLUTION stops and returns a subset $C$ of the canonical universal solution $J$ such that $C$ is a core, $J$ maps homomorphically to $C$, and $C$ is a universal solution.

The proof has four parts.

1. The chase result $J$ is a universal solution. Each trigger has a witness, and the fresh nulls of each trigger can be mapped to the witness values of that trigger in any other solution.
2. Each fact of $J$ holds nulls of one trigger only, so a block has at most $w$ nulls.
3. An instance is a core if and only if no group of nulls has a map $h$ as in line L4. If such an $h$ exists, it removes a fact. If the instance is not a core, a homomorphism onto a proper subset must move the facts of some group, and its restriction to that group is such an $h$.
4. Work on one block removes only facts of that block, and the instance only shrinks. So a block that has no map left at the end of its loop has none at the end of the run.

All universal solutions have the same core, up to a renaming of nulls, and no universal solution is smaller. Fagin, Kolaitis and Popa proved this. The proof file gives the short argument: two cores with homomorphisms each way are isomorphic.

## Complexity

Fix $\Sigma$. Let $m$ be the number of facts of $J$ and $w$ the largest number of existential variables in one tgd. Line L4 succeeds at most $m$ times, since each success removes a fact, and fails at most once per block, so it runs at most $2m$ times. One search tries the partial maps of at most $w$ nulls to the $O(m)$ values of $J$, and each step scans one relation.

- **Time.** $O(m^{w+1})$ for one search, and $O(m^{w+2})$ in total. For a fixed $\Sigma$, $m$ is polynomial in $|I|$, so the run takes polynomial time in data complexity.
- **Space.** $O(m)$ for the instance and its index, plus the recursion of one search, which is bounded by the number of facts in a block.

In combined complexity, where $\Sigma$ is part of the input, the exponent $w$ grows with the mapping. Core problems are hard in general: Fagin, Kolaitis and Popa showed that deciding whether a graph $H$ is the core of a graph $G$ is DP-complete.

## Properties

- **Exact.** It returns the core, not an approximation.
- **Deterministic.** The order of the blocks fixes which isomorphic copy of the core is returned.
- **Polynomial in data complexity.** The degree of the polynomial depends on the mapping through $w$.
- **Monotone shrinking.** Each step removes facts and never adds one, so each prefix of the run is a universal solution between $J$ and the core.
- **No new values.** The core uses only values that occur in $J$.

## Variants and improvements

- **Target egds.** With [egds](/equality-generating-dependency/) on the target, the chase can merge nulls, so the blocks are no longer bounded by one trigger. Fagin, Kolaitis and Popa gave polynomial algorithms under broad conditions of this kind.
- **Weakly acyclic target tgds.** Gottlob and Nash gave a polynomial algorithm in data complexity when the source-to-target dependencies are arbitrary tgds and the target dependencies are a [weakly acyclic](/weak-acyclicity/) set of tgds with egds. They also proved a fixed-parameter intractability result, and they showed that with a predicate that tells nulls from constants the problem becomes NP-complete.
- **Query minimization.** The same retraction idea applied to the canonical database of a conjunctive query gives [conjunctive query minimization](/conjunctive-query-minimization/), by the [Chandra-Merlin theorem](/chandra-merlin-theorem/).

## When to use it

Use the core when you must store the target instance, since it is the smallest universal solution and has no redundant facts. It gives the same [certain answers](/certain-answers/) to unions of conjunctive queries as any other universal solution. When the target is only used to answer such queries and size does not matter, the canonical universal solution is enough and saves the extra pass.

## Pitfalls

- **Nulls must not map to fresh values.** The map $h$ of line L4 is the identity on constants and maps into values that already occur in $J$. A map that may invent values does not give a subset.
- **Blocks grow with target dependencies.** The bound of $w$ nulls per block holds for source-to-target tgds. With target tgds or egds, a block can hold nulls from many triggers, and the simple search can become exponential in the data.
- **Termination of the chase.** With target tgds, the chase may not stop. [Weak acyclicity](/weak-acyclicity/) is a sufficient condition for it to stop, not a necessary one.
- **Queries with negation.** The core and $J$ can give different naive answers to a query with negation. In the example, "some $x$ has Leg$(a, x)$ and no Leg$(x, b)$" is true on $J$, with $x = \bot_3$, but false on the core. Neither answer is the certain answer in general.

## Implementations

## History

Fagin, Kolaitis, Miller and Popa defined universal solutions and the canonical universal solution in their work on data exchange, which appeared at ICDT 2003 and in Theoretical Computer Science in 2005. Fagin, Kolaitis and Popa then showed in ACM TODS in 2005 that all universal solutions share one core, that it is the smallest universal solution, and that it can be computed in polynomial time under broad conditions. Gottlob and Nash answered an open problem from that work in the Journal of the ACM in 2008, with a polynomial algorithm for weakly acyclic target tgds and egds.

## References
