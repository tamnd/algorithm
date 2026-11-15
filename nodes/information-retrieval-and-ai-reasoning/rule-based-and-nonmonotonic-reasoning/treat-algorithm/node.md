---
tag: YM9BB7
kind: algorithm
slug: treat-algorithm
name: TREAT algorithm
aliases:
- Miranker TREAT
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: A production system matcher that keeps only the matches of single conditions and the conflict set, joins each new element with the other conditions, and deletes by a scan of the conflict set.
model: word-ram
complexity:
  vars: {n: the number of elements in working memory, r: the number of rules, m: the largest number of conditions in a rule, a: the largest arity of an element, k: the number of instantiations in the conflict set}
  time: {worst: O(r m a n^(m-1))}
  space: {extra: O(r m n + k)}
properties: {deterministic: true, incremental: true}
history:
  year: 1987
  people: [Daniel P. Miranker]
  note: Miranker proposed TREAT in his Columbia University thesis work on the DADO parallel machine, and reported that it ran faster than Rete on a set of OPS5 programs.
prereqs: [rete-algorithm, production-system]
see_also: [forward-chaining, conflict-resolution-strategy, incremental-view-maintenance, semi-naive-evaluation, nested-loop-join]
sources:
  - paper: "Daniel P. Miranker, TREAT: A better match algorithm for AI production systems, Proceedings of the Sixth National Conference on Artificial Intelligence (AAAI-87), volume 1, 42 to 47 (1987)"
    locator: the description of the algorithm, condition membership, and the comparison with Rete on five OPS5 programs
  - paper: doi:10.1016/0004-3702(82)90020-0
    title: "Charles L. Forgy, Rete: A fast algorithm for the many pattern/many object pattern match problem, Artificial Intelligence 19(1), 17 to 37 (1982)"
    locator: the network that TREAT is compared with
  - paper: "Robert B. Doorenbos, Production Matching for Large Learning Systems, PhD thesis, Carnegie Mellon University, technical report CMU-CS-95-113 (1995)"
    locator: the discussion of TREAT and of the trade-off between storing and recomputing partial matches
---

TREAT is a match algorithm for [production systems](/production-system/), proposed by Miranker as an alternative to the [Rete algorithm](/rete-algorithm/). Both keep the conflict set up to date while the working memory changes. Rete stores every partial match of every prefix of the conditions of a rule in *beta memories*. TREAT stores only the *alpha memories*, the elements that match each single condition, and the conflict set itself. When an element is inserted, TREAT joins it with the alpha memories of the other conditions of each rule that it touches. When an element is deleted, TREAT removes the instantiations that hold it from the conflict set, with no join at all. So TREAT does more work on inserts and less on deletes, and it uses much less memory.

## In plain words

A rule system needs to know, after every change to its facts, which rules can fire with which facts. TREAT keeps two things: for each condition of each rule, the list of facts that fit that condition alone, and the list of complete matches. When a new fact arrives, it is put in the lists of the conditions it fits. Then, for each rule and each such condition, TREAT looks for complete matches that use the new fact there, by pairing it with facts from the lists of the other conditions. When a fact is removed, TREAT takes it out of the lists and drops every complete match that uses it. Nothing in between is saved, so nothing in between has to be cleaned up.

## The problem

The setting is the same as for [Rete](/rete-algorithm/). A working memory element (WME) is a ground tuple. A rule is $\rho: c_1, \ldots, c_m \Rightarrow \text{actions}$ with condition patterns $c_k$. An instantiation of $\rho$ in the working memory $W$ is a tuple $(w_1, \ldots, w_m)$ of elements of $W$ with one binding $\theta$ such that $c_k\theta = w_k$ for every $k$. The conflict set is the set of pairs $(\rho, (w_1, \ldots, w_m))$ over all rules. The task is to keep the conflict set correct after each insert or delete of one element. This page treats positive conditions only.

## The algorithm

Each condition has an alpha memory, keyed by the condition with its variables renamed by first occurrence, so that equal conditions of different rules share it. It holds the elements that pass the constant tests and the equality tests within the condition.

```pseudo id=main
INSERT(w)
L1  for each alpha memory α whose tests w passes do
L2      add w to α
L3  for each rule ρ with the conditions c_1, …, c_m do
L4      for each i such that the alpha memory of c_i received w do
L5          for each binding θ with c_i θ = w and, for each j ≠ i, c_j θ = w_j for an element w_j of the alpha memory of c_j, where w_j ≠ w for j < i do
L6              add (ρ, (w_1, …, w_m)) to the conflict set, with w_i = w

DELETE(w)
L7  remove w from every alpha memory
L8  for each instantiation in the conflict set that holds w do
L9      remove it from the conflict set
```

Line L5 is a *seeded join*: it starts from the binding that $w$ gives at position $i$ and binds the other conditions one at a time, as a [nested loop join](/nested-loop-join/) does. The rule $w_j \ne w$ for $j < i$ makes each new instantiation come from the first position where $w$ occurs, so an element that matches two conditions of one rule does not make the same instantiation twice. Miranker's *condition membership* adds a flag for each rule that says whether every alpha memory of the rule is non-empty; line L4 can skip a rule whose flag is off.

## Example

Take the two rules of the Rete example,

$$\begin{aligned} R_1 &: \mathit{goal}(g), \mathit{block}(b, \mathit{red}), \mathit{on}(b, t) \Rightarrow \ldots \\ R_2 &: \mathit{goal}(g), \mathit{block}(b, \mathit{red}), \mathit{clear}(b) \Rightarrow \ldots \end{aligned}$$

and the elements $\mathit{goal}(g_1)$, $\mathit{block}(b_1, \mathit{red})$, $\mathit{block}(b_2, \mathit{red})$, $\mathit{block}(b_3, \mathit{blue})$ and $\mathit{on}(b_1, \mathit{table})$, inserted in this order. TREAT has the same 4 alpha memories as Rete, and the conflict set holds $(R_1, (\mathit{goal}(g_1), \mathit{block}(b_1, \mathit{red}), \mathit{on}(b_1, \mathit{table})))$.

| change | seeds | join work | conflict set change |
|---|---|---|---|
| insert $\mathit{clear}(b_2)$ | $R_2$ at position 3, binding $b = b_2$ | goal memory: $g_1$; block memory: $b_1$ fails the test $b = b_2$, $b_2$ passes | add the instantiation of $R_2$ |
| delete $\mathit{block}(b_1, \mathit{red})$ | none | none | remove the instantiation of $R_1$ |
| insert $\mathit{block}(b_1, \mathit{red})$ | $R_1$ and $R_2$ at position 2, binding $b = b_1$ | $R_1$: goal $g_1$, then on: $\mathit{on}(b_1, \mathit{table})$ passes; $R_2$: goal $g_1$, then clear: $\mathit{clear}(b_2)$ fails | add the instantiation of $R_1$ again |

Rete would answer the first insert from its stored tokens for $\mathit{goal}, \mathit{block}$, and would answer the delete by removing two tokens. TREAT recomputes the join of the goal and block memories, and needs no tokens at all.

## Correctness

The [correctness proof](proofs/correctness.md) keeps the invariant that each alpha memory holds exactly the elements that pass its tests and that the conflict set holds exactly the instantiations, each once. After an insert, the new instantiations are those that contain $w$. Each has a first position $p$ where $w$ occurs; the seeded join at $p$ produces it once, and the seeded join at any later position $i$ with $w_i = w$ rejects it, because $w_p = w$ with $p < i$. A delete removes exactly the instantiations that hold $w$.

## Complexity

An insert runs, for each rule and each position whose alpha memory received $w$, a join over the $m - 1$ other alpha memories. The search tree of one join has $O(n^{m-1})$ nodes and each test costs $O(a)$, so an insert costs $O(r\, m\, a\, n^{m-1})$ time in the worst case. A delete scans the conflict set in $O(k\, m)$ time, or takes time proportional to the instantiations it removes when each element keeps a list of its instantiations. The extra space is the alpha memories, $O(r\, m\, n)$, plus the conflict set, $O(k)$. Rete in the worst case stores $O(r\, m\, n^m)$ tokens.

As for Rete, these are combined complexity bounds, and the match problem is NP-complete when the rules are part of the input. The speed comparison with Rete is a measurement: Miranker (1987) ran both on five OPS5 programs and found TREAT faster, often by more than half. The result depends on the programs, on how often they delete elements, and on the two implementations; Doorenbos (1995) argued, from his own measurements, that on very large learned rule sets the stored state of Rete is worth its cost.

## Properties

- **Incremental.** The conflict set is kept between changes; only alpha memories are kept besides it.
- **Little state.** The memory is linear in the working memory, plus the conflict set.
- **Cheap deletes.** A delete needs no join, only the removal of the instantiations that hold the element.
- **Repeated joins.** The same partial match is computed again on each insert that needs it.
- **Exact.** The conflict set equals the result of a full rematch after each change, with no duplicates.

## Variants and improvements

- **Condition membership.** Skip the joins of a rule while one of its alpha memories is empty. Miranker describes this as a part of TREAT; the implementation here does without it, since its join stops at the first empty memory.
- **Join order.** Order the other conditions of a seeded join by the size of their alpha memories, or by the variables they share with the seed, to keep the search tree small.
- **Negated conditions.** An insert that matches a negated condition removes the instantiations that it blocks; a delete that matches a negated condition needs a seeded join for the instantiations that it unblocks.
- **Gator networks.** Hanson and Hasan generalized Rete and TREAT to networks that store an optimized choice of partial matches.
- **Lazy matching.** LEAPS computes only the instantiation that conflict resolution would pick next, not the whole conflict set.

## When to use it

Use TREAT when memory is limited, when facts are often deleted or modified, or when the rules have conditions with large alpha memories that would make large beta memories in Rete. Use [Rete](/rete-algorithm/) when the same partial matches are needed in many cycles and memory is not the limit. Both give the same conflict set, so the choice affects only the cost.

## Pitfalls

- **Double counting.** When an element matches two conditions of one rule, only the first position may seed the instantiation; without the rule $w_j \ne w$ for $j < i$ the conflict set gets duplicates.
- **Join order.** A seeded join that binds an unrelated condition first makes a cross product.
- **Delete cost.** Without an index from elements to instantiations, each delete scans the whole conflict set.
- **Reading the speed claim as a bound.** TREAT is faster on the programs that Miranker measured; on programs that reuse long partial matches, Rete can be faster.

## Implementations

## History

Miranker developed TREAT at Columbia University in the mid-1980s, as part of the DADO project on parallel production systems, and presented it at AAAI-87 with measurements on five OPS5 programs. His thesis appeared as a book in 1990. Later work combined the two ideas: Gator networks (Hanson and Hasan, 1993) choose which partial matches to store, and LEAPS (Miranker and others, 1990) matches lazily.

## References
