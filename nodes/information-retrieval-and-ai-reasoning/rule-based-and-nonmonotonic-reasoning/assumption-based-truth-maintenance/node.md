---
tag: D3V9DW
kind: algorithm
slug: assumption-based-truth-maintenance
name: Assumption-based truth maintenance
aliases:
- ATMS
- de Kleer ATMS
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Labels each node with the minimal consistent sets of assumptions from which it follows, so a reasoner can work in all contexts at once; the labels can be exponential.
model: word-ram
complexity:
  vars: {a: the number of assumptions, n: the number of nodes, k: the largest number of antecedents of a justification, s: the number of justifications}
  time: {worst: 2^O(a k) s}
  space: {extra: O(a n 2^a)}
properties: {deterministic: true, incremental: true, monotone: true}
history:
  year: 1986
  people: [Johan de Kleer]
  note: De Kleer introduced the ATMS at Xerox PARC to let a problem solver explore many sets of assumptions at once, without the relabelling and backtracking of a justification-based TMS.
prereqs: [justification-based-truth-maintenance, horn-clause, forward-chaining]
see_also: [consistency-based-diagnosis, reiter-hs-tree, hitting-set, abductive-reasoning, prime-implicant, nonmonotonic-reasoning, horn-sat]
sources:
  - paper: doi:10.1016/0004-3702(86)90080-9
    title: "Johan de Kleer, An assumption-based TMS, Artificial Intelligence 28(2), 127 to 162 (1986)"
    locator: the definitions of assumptions, environments, nogoods and labels, the four label properties, and the label update algorithm
  - paper: "Johan de Kleer, Extending the ATMS, Artificial Intelligence 28(2), 163 to 196 (1986)"
    locator: disjunctions of assumptions and other extensions of the basic ATMS
  - paper: "Raymond Reiter and Johan de Kleer, Foundations of assumption-based truth maintenance systems: preliminary report, Proceedings of the Sixth National Conference on Artificial Intelligence (AAAI-87), 183 to 188 (1987)"
    locator: the characterization of ATMS labels and of the clause management system by prime implicates
  - book: isbn:9780262061575
    title: Kenneth D. Forbus and Johan de Kleer, Building Problem Solvers, MIT Press (1993)
    locator: the chapters on the ATMS, its implementation and its use in problem solvers
  - paper: "Bart Selman and Hector J. Levesque, Abductive and default reasoning: a computational core, Proceedings of the Eighth National Conference on Artificial Intelligence (AAAI-90), 343 to 348 (1990)"
    locator: the hardness of finding an assumption-based explanation over Horn clauses
---

An assumption-based truth maintenance system (ATMS) records, for each node, every minimal set of assumptions under which the node holds. A [justification-based TMS](/justification-based-truth-maintenance/) keeps one set of beliefs and relabels it when an assumption changes. The ATMS keeps all contexts at once: the *label* of a node is the list of its minimal consistent *environments*, sets of assumptions from which the node follows by the Horn justifications. A *nogood* is a minimal set of assumptions that derives a contradiction, and no label holds a superset of one. The reasoner can then ask whether a node holds in any context by one subset test, and switch contexts for free. The price is that labels can be exponential in the number of assumptions.

## In plain words

Suppose a reasoner works with guesses and wants to compare many combinations of guesses. In place of keeping one combination at a time, the ATMS writes next to each conclusion the smallest combinations of guesses that are enough to reach it. It also keeps a list of the combinations that lead to a contradiction, and drops every entry that contains one of them. To know whether a conclusion holds for some set of guesses, check whether one of its entries is part of that set. Nothing is ever retracted: a new rule only adds entries, and a new contradiction only removes the entries that contain it. The lists can be very long, because each choice between two guesses can double them.

## The problem

There is a set $A$ of *assumptions*, a set of nodes that contains $A$ and a contradiction node $\bot$, and a set $J$ of *justifications*, Horn clauses

$$x \leftarrow a_1, \ldots, a_k$$

over nodes. For an environment $E \subseteq A$, the closure $\mathrm{Cl}(E)$ is the least set that contains $E$ and is closed under $J$, which [forward chaining](/forward-chaining/) computes. $E$ is *inconsistent* when $\bot \in \mathrm{Cl}(E)$; the *nogoods* are the minimal inconsistent environments. The label of a node $x$ must be

- *sound*: each environment in it derives $x$;
- *consistent*: each environment in it is consistent;
- *minimal*: no environment in it is a superset of another;
- *complete*: each consistent environment that derives $x$ is a superset of one of them.

So $L(x)$ is the set of minimal consistent environments $E$ with $x \in \mathrm{Cl}(E)$. In logical terms, $E \in L(x)$ when $J \cup E \models x$ and $J \cup E \not\models \bot$. Reiter and de Kleer (1987) characterized the labels by the prime implicates of the justifications, the clauses of the form $\neg a_1 \vee \cdots \vee \neg a_m \vee x$ that follow from $J$ and are minimal. The task is incremental: keep all labels and the nogood list correct while assumptions and justifications are added.

## The algorithm

A queue holds pairs (node, environments) that wait to enter a label. Adding an assumption $a$ queues $(a, \{\{a\}\})$. Adding a justification $x \leftarrow a_1, \ldots, a_k$ queues $x$ with the minimal consistent unions of one environment from each antecedent label, and runs PROPAGATE.

```pseudo id=main
PROPAGATE(Q)
L1  while Q is not empty do
L2      (x, E) ← remove the first pair of Q; drop the environments of E that contain a nogood
L3      N ← the minimal environments of E that have no subset in L(x)
L4      if N is empty then continue with the next pair at L1
L5      if x = ⊥ then NOGOOD(e) for each e in N; continue at L1
L6      remove from L(x) every environment that has a subset in N; add N to L(x)
L7      for each justification y ← b_1, …, b_k that has x among its antecedents do
L8          append (y, COMBINE(the justification, x, N)) to Q

COMBINE(y ← b_1, …, b_k, x, N)
L9  for each position i with b_i = x, choose an environment of N at i and one of L(b_l) at each other position l
L10 take the union of each choice, and keep the unions that contain no nogood
L11 return the minimal ones among them

NOGOOD(e)
L12 if no nogood is a subset of e then add e to the nogoods and remove the nogoods that contain e
L13 remove from every label the environments that contain e
```

Only the new environments $N$ of a node travel on to its consumers (lines L7 to L9). Labels never lose an environment except to a smaller one or to a nogood, so the ATMS is monotone: there is no retraction and no relabelling.

## Example

The assumptions are $A, B, C$, and the justifications are added in this order.

| step | justification | effect |
|---|---|---|
| 1 | $x \leftarrow A, B$ | $L(x) = \{\{A, B\}\}$ |
| 2 | $y \leftarrow B$ | $L(y) = \{\{B\}\}$ |
| 3 | $y \leftarrow C$ | $L(y) = \{\{B\}, \{C\}\}$ |
| 4 | $z \leftarrow x, y$ | the unions are $\{A, B\} \cup \{B\} = \{A, B\}$ and $\{A, B, C\}$; the minimal one gives $L(z) = \{\{A, B\}\}$ |
| 5 | $z \leftarrow y$ | $\{B\}$ and $\{C\}$ enter, and $\{A, B\}$ leaves because $\{B\}$ is a subset: $L(z) = \{\{B\}, \{C\}\}$ |
| 6 | $\bot \leftarrow A, B$ | $\{A, B\}$ becomes a nogood; it leaves $L(x)$, so $L(x)$ is empty; $L(z)$ does not change |

Now $z$ holds in the context $\{B, C\}$, because $\{B\}$ is a subset of it, and in no context that contains both $A$ and $B$, because such a context is inconsistent.

## Correctness

The [correctness proof](proofs/correctness.md) shows that every environment that enters a label derives its node (soundness), that lines L2, L3, L6, L12 and L13 keep labels minimal and free of nogoods, and a quiescence lemma: when the queue is empty, for every justification and every choice of label environments of its antecedents, the union contains a nogood or has a subset in the label of the consequent. The reason is that the antecedent environment that entered its label last sent this union, or a subset of it, down the queue. Completeness then follows by induction on a forward chaining derivation, and the same argument shows that the nogoods are exactly the minimal inconsistent environments. Labels with these four properties are unique, so the result does not depend on the order of the additions.

## Complexity

Labels can be exponential. With assumptions $A_1, B_1, \ldots, A_n, B_n$ and justifications $x_i \leftarrow A_i$, $x_i \leftarrow B_i$ and $g \leftarrow x_1, \ldots, x_n$, the label of $g$ holds all $2^n$ choices of one assumption from each pair, and no choice contains another. So any procedure that writes out the labels takes exponential time on an input of size $O(n)$; the proof page gives the details. In general each label has at most $2^a$ environments, a combination step over $k$ antecedents forms at most $2^{a k}$ unions, and each node gets new environments at most $2^a$ times, which gives a bound of the form $2^{O(a k)} s$ on the time and $O(a\, n\, 2^a)$ on the space. The cost is not only in the size of the output: deciding whether a node has any consistent environment is NP-complete when nogoods are present (Selman and Levesque 1990). To see the hardness, take assumptions $p^+$ and $p^-$ for each variable $p$ of a CNF formula, the justification $\bot \leftarrow p^+, p^-$, a justification $c \leftarrow p^+$ for each positive literal $p$ of a clause $c$ and $c \leftarrow p^-$ for each negative one, and $g \leftarrow c_1, \ldots, c_m$; then $g$ has a consistent environment exactly when the formula is satisfiable. In practice the labels stay small when the assumptions are few or the nogoods cut the products early, and ATMS implementations use bit vectors for environments and a table of all environments, so that a subset test is a few machine operations.

## Properties

- **Multiple contexts.** All consistent sets of assumptions are represented at once; a query in a context is a subset test against the label.
- **Monotone.** Justifications and assumptions are only added. Inconsistency removes environments, but no node is ever relabelled because a premise was withdrawn.
- **Unique result.** The labels and nogoods depend only on the justifications, not on the order in which they were added.
- **Horn only.** The basic ATMS handles Horn justifications. Disjunctions of assumptions need the extensions of de Kleer's second paper.
- **Exponential labels.** The size of a label can be $2^{a/2}$ even with no nogoods.

## Variants and improvements

- **Focusing.** Restrict the labels to environments inside a set of contexts of interest, to avoid the exponential growth outside them.
- **Disjunctions and the CMS.** De Kleer's extensions add choose-sets of assumptions; Reiter and de Kleer's clause management system accepts arbitrary clauses and answers with prime implicates.
- **Diagnosis.** In [consistency-based diagnosis](/consistency-based-diagnosis/), the assumptions say that components work, the nogoods are the conflict sets, and the diagnoses are the minimal [hitting sets](/hitting-set/) of the nogoods, as in [Reiter's HS-tree](/reiter-hs-tree/) and de Kleer and Williams's GDE.
- **Abduction.** The label of an observation lists its minimal consistent explanations by assumptions, the Horn case of [abductive reasoning](/abductive-reasoning/).
- **Lazy labels.** Compute the label of a node only when it is asked for, with backward search from the node.

## When to use it

Use an ATMS when a problem solver must compare many alternative sets of assumptions, as in model-based diagnosis, qualitative physics and design spaces, and when switching between contexts must be cheap. Use a [JTMS](/justification-based-truth-maintenance/) when one context is active at a time, when the justifications need nonmonotonic out-lists, or when the number of assumptions is large and unfocused.

## Pitfalls

- **Label explosion.** A few independent binary choices multiply the label size. Focus the labels or keep the number of assumptions per problem small.
- **Forgetting minimality.** If supersets are not removed from labels and from the nogood list, they grow fast and the subset tests slow down.
- **Late nogoods.** A nogood that arrives late must remove environments from every label, not only from the nodes near the contradiction.
- **Treating the label as a probability.** A label says under which assumptions a node holds, not how likely the node is.

## Implementations

## History

De Kleer (1986) introduced the ATMS in three papers in one issue of Artificial Intelligence: the basic system, its extensions, and its use in problem solving. It grew from his work with Brown on qualitative physics and with Williams on diagnosis, where the GDE of de Kleer and Williams (1987) used it to find conflict sets. Reiter and de Kleer (1987) gave the logical foundations through prime implicates. Forbus and de Kleer (1993) gave the standard implementation in their textbook.

## References
