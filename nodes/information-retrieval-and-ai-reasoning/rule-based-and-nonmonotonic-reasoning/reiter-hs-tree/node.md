---
tag: PCV2A8
kind: algorithm
slug: reiter-hs-tree
name: Reiter's hitting set tree
aliases:
- HS-tree
- Greiner HS-DAG
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: advanced
summary: Finds all minimal diagnoses as the minimal hitting sets of the conflict sets, with a breadth-first search tree whose edges are elements of conflicts.
model: word-ram
complexity:
  vars: {k: the number of nodes that the search creates, u: the number of components, m: the number of distinct labels}
  time: {worst: O(k · (k + m) · u)}
  space: {extra: Θ(k · u)}
properties: {deterministic: true}
history:
  year: 1987
  people: [Raymond Reiter, Russell Greiner, Barbara A. Smith, Ralph W. Wilkerson]
  note: Reiter gave the pruned HS-tree in his 1987 theory of diagnosis. In 1989 Greiner, Smith and Wilkerson showed that its pruning can lose diagnoses and gave the corrected HS-DAG with a proof.
prereqs: [hitting-set, consistency-based-diagnosis, breadth-first-search]
see_also: [minimal-transversal-enumeration, assumption-based-truth-maintenance, minimal-unsatisfiable-subset, minimal-correction-subset, directed-acyclic-graph, sat]
sources:
  - paper: doi:10.1016/0004-3702(87)90062-2
    title: Raymond Reiter, A theory of diagnosis from first principles, Artificial Intelligence 32(1), 57 to 95 (1987)
    locator: Theorem 4.4 (diagnoses are the minimal hitting sets of the conflict sets) and Section 4 (the HS-tree and its pruning rules)
  - paper: doi:10.1016/0004-3702(89)90079-9
    title: Russell Greiner, Barbara A. Smith and Ralph W. Wilkerson, A correction to the algorithm in Reiter's theory of diagnosis, Artificial Intelligence 41(1), 79 to 88 (1989)
    locator: Figures 1 and 2 (the lost diagnoses), the HS-DAG algorithm, Theorem 4.1 and Lemma 4.2
  - paper: doi:10.1016/0004-3702(87)90063-4
    title: Johan de Kleer and Brian C. Williams, Diagnosing multiple faults, Artificial Intelligence 32(1), 97 to 130 (1987)
    locator: the polybox example, and conflicts found with an assumption-based truth maintenance system
  - paper: doi:10.1016/S0020-0190(00)00166-6
    title: Franz Wotawa, A variant of Reiter's hitting-set algorithm, Information Processing Letters 79(1), 45 to 51 (2001)
    locator: the variant of the tree construction
---

This page is the diagnosis search tree. In [consistency-based diagnosis](/consistency-based-diagnosis/), a diagnosis is a minimal set of components that, when assumed faulty, makes the observations consistent with the system description. Reiter (1987, Theorem 4.4) proved that the diagnoses are exactly the minimal [hitting sets](/hitting-set/) of the conflict sets. The hitting set page covers the set problem itself. This page covers the search that Reiter built on the theorem: a [breadth-first](/breadth-first-search/) tree that asks a consistency checker for one conflict at a time, never needs the whole list of conflicts, and stops at the minimal hitting sets. Reiter's rules for pruning the tree are wrong in some cases. Greiner, Smith and Wilkerson (1989) gave two examples where a diagnosis is lost, and replaced the tree by a [directed acyclic graph](/directed-acyclic-graph/), the HS-DAG, which they proved correct.

## In plain words

A machine misbehaves, and a checker can tell you a group of parts that cannot all be working, called a conflict. The search starts with no suspects. It asks for a conflict and branches on each part in it: "suppose this part is broken". On each branch it asks again for a conflict that avoids the parts already suspected, and branches again. A branch ends when the suspects explain everything, and then they form a diagnosis. The search goes level by level, so small diagnoses come first, and a branch that contains a diagnosis already found is dropped. When the checker gives a large conflict and later a smaller one inside it, the search can cut the branches for the extra parts. The correction is about doing this cut safely.

## The problem

The input is a finite set $U$ of components and a label oracle $\mathrm{next}$. For a set $h \subseteq U$ of suspected components, $\mathrm{next}(h)$ returns nothing if $h$ hits every conflict, and otherwise a conflict $L \subseteq U$ with $L \cap h = \emptyset$. In diagnosis, a conflict is a set $C$ of components such that the system description, the observations and the statements "$c$ is not abnormal" for all $c \in C$ are inconsistent together. The oracle needs only a consistency checker: $\mathrm{next}(h)$ tests the components outside $h$, and if they are inconsistent, it deletes components one at a time while the rest stays inconsistent. A conflict need not be minimal. For an explicit collection $F$ of sets, the oracle returns the first member of $F$ that is disjoint from $h$.

The output is the set of all minimal hitting sets of the conflicts, that is, all minimal diagnoses. If the observations alone contradict the system description, the empty set is a conflict and there is no diagnosis. If nothing is wrong, the answer is the single empty diagnosis.

## The algorithm

Each node $n$ stands for the set $H(n)$ of the labels on the path from the root. A node is identified by $H(n)$, so two paths with the same edge labels in a different order end at the same node. This is what makes the structure a DAG.

```pseudo id=main
HS-DAG(next)                       ▷ next(h): a conflict disjoint from h, or nothing
L1  create the root with H = ∅; labels ← an empty list
L2  level ← [root]
L3  while level is not empty do
L4      following ← []
L5      for each node n of level that still exists and has no status do
L6          if some checked node m has H(m) ⊊ H(n) then mark n closed; continue
L7          L ← the first S in labels with S ∩ H(n) = ∅, or nothing    ▷ reuse a known conflict
L8          if L is nothing then
L9              L ← next(H(n))
L10             if L is nothing then mark n checked; continue    ▷ H(n) is a diagnosis
L11             PRUNE(L); append L to labels
L12             if n was deleted by PRUNE then continue
L13         mark n labeled with L
L14         for each σ in L do
L15             c ← H(n) ∪ {σ}
L16             if no node has H = c then
L17                 create the node c
L18                 append c to following
L19             add an edge marked σ from n to c
L20     level ← following
L21 return the sets H(n) of the checked nodes

PRUNE(Σ)
L22 for each node n' with a label S' ⊋ Σ do: relabel n' with Σ, remove its edges for the elements of S' ∖ Σ, and remove S' from labels
L23 delete every node that the root no longer reaches
```

Line L7 is Reiter's label reuse: a known conflict that avoids $H(n)$ saves a call of the oracle, which is often a theorem prover. Line L6 is the closing rule: a node above a known diagnosis cannot lead to a minimal one. Lines L22 and L23 are the pruning step of Greiner, Smith and Wilkerson. In their version the collection $F$ is ordered and $S'$ is swapped with $\Sigma$ in $F$; removing $S'$ from the list of labels has the same effect.

## Example

This is the example in Figure 1 of Greiner, Smith and Wilkerson. The conflicts, in this order, are $F = \{a,b\}, \{b,c\}, \{a,c\}, \{b,d\}, \{b\}$. The minimal hitting sets must contain $b$, and then one of $a$ or $c$, so they are $\{a,b\}$ and $\{b,c\}$.

| level | node $H$ | result | why |
|---|---|---|---|
| 0 | $\emptyset$ | label $\{a,b\}$ | the first conflict |
| 1 | $\{a\}$ | label $\{b,c\}$ | the first conflict that avoids $a$ |
| 1 | $\{b\}$ | label $\{a,c\}$ | its $a$ edge goes to the node $\{a,b\}$, which already exists |
| 2 | $\{a,b\}$ | checked | it meets every conflict |
| 2 | $\{a,c\}$ | label $\{b,d\}$ | |
| 2 | $\{b,c\}$ | checked | it meets every conflict |
| 3 | $\{a,b,c\}$ | closed | it contains the diagnosis $\{a,b\}$ |
| 3 | $\{a,c,d\}$ | label $\{b\}$, deleted | the new conflict $\{b\}$ prunes |

The new label $\{b\}$ is a proper subset of the labels of the root, of $\{a\}$ and of $\{a,c\}$. PRUNE gives all three the label $\{b\}$ and removes the edges for $a$, $c$ and $d$ respectively. The root now reaches only $\{b\}$, and through it $\{a,b\}$ and $\{b,c\}$. The nodes $\{a\}$, $\{a,c\}$, $\{a,b,c\}$ and $\{a,c,d\}$ are deleted. The node $\{a,b\}$ stays, because its other parent $\{b\}$ stays. The result is $\{a,b\}$ and $\{b,c\}$.

Reiter's original tree makes a separate node for each path. It closes the path $b, a$ because the path $a, b$ already gave the same set. Then the label $\{b\}$ cuts the $a$ edge of the root, and the path $a, b$ goes with it, so $\{a,b\}$ is lost. Figure 2 of the same paper shows a second error: with $F = \{a,b\}, \{a\}, \{b\}$, the root keeps its label $\{a,b\}$, the label $\{b\}$ cuts its $a$ edge, and later the label $\{a\}$ cuts its $b$ edge. The tree returns nothing, but $\{a,b\}$ is a hitting set.

## Correctness

The [correctness proof](proofs/correctness.md) has the details. Call a label valid if it contains a conflict, and note that a set hits every valid label exactly when it hits every conflict. The proof shows three invariants: every label is valid, every labeled node has an edge for each element of its current label, and every node is reachable from the root. PRUNE keeps them, because $\Sigma \subsetneq S'$ is valid, avoids $H(n')$, and its edges were already there. For completeness, take a minimal hitting set $M$ and walk from the root, always along an edge in $M \cap L$. The walk cannot stop at a closed node, because then a smaller hitting set would lie inside $M$, so it ends at a checked node with $H = M$. For soundness, a checked node $n$ whose $H(n)$ is not minimal contains some minimal $M$, and the node for $M$ is on an earlier level, so it was already checked when $n$ was tested at line L6. Reiter's tree breaks the invariants: a node closed in favour of a node that is later cut has no valid reason to be closed, and a node that keeps its old label after a cut no longer has an edge for each element of it.

## Complexity

Let $k$ be the number of nodes that the search creates, $u = |U|$ and $m$ the number of distinct labels. Each node is processed once. The closing test at line L6 scans the nodes in $O(k \cdot u)$ time, and the reuse test at line L7 scans the labels in $O(m \cdot u)$ time. Each call of PRUNE costs $O(k \cdot u)$, and there is at most one per node. So the work outside the oracle is $O(k \cdot (k + m) \cdot u)$, and the oracle is called at most $k$ times. The space is $\Theta(k \cdot u)$. In diagnosis the oracle calls dominate: the deletion method makes up to $u + 1$ consistency checks per conflict, and for a propositional system description each check is a [SAT](/sat/) call.

The number of nodes $k$ is at least the number of minimal diagnoses, and that can be exponential: $r$ disjoint conflicts $\{a_i, b_i\}$ have $2^r$ minimal hitting sets. Enumerating minimal hitting sets with good bounds in terms of the output size is the [minimal transversal enumeration](/minimal-transversal-enumeration/) problem. The HS-DAG is not built for that bound. Its strength is that it needs no list of conflicts in advance and calls the oracle only on the nodes it visits.

## Properties

- **Sound and complete.** The checked nodes are exactly the minimal hitting sets, also when the oracle returns conflicts that are not minimal.
- **Smallest first.** The search goes level by level, so all diagnoses of size $j$ are found before any of size $j + 1$. Stopping after level $j$ gives the diagnoses of size at most $j$.
- **Lazy conflicts.** Only the conflicts that the search asks for are computed, and each known conflict is reused when it avoids the current node.
- **Deterministic.** With a deterministic oracle and a fixed order of the elements at line L14, the run is fixed.
- **Pruning is optional.** Without lines L22 and L23 the algorithm is the basic HS-DAG and is still correct. Pruning only removes work when a later conflict is a proper subset of an earlier one. With minimal conflicts it never applies.

## Variants and improvements

- **Basic HS-DAG.** Drop the pruning step. Greiner, Smith and Wilkerson proved this version first (their Lemma 4.2); Reiter had stated the property without proof.
- **Minimal conflicts.** If the oracle always returns minimal conflicts, no label is a proper subset of another, pruning never applies, and Reiter's tree and the HS-DAG give the same answer. In SAT terms, a minimal conflict is a [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/) of the health assumptions, and a minimal diagnosis is the complement of a maximal satisfiable subset, that is, a [minimal correction subset](/minimal-correction-subset/).
- **Bounded search.** Stop after a fixed level, or keep only diagnoses up to a given size, which is common when single and double faults are the main concern.
- **Wotawa's variant.** Wotawa (2001) changed the way the tree is built to reduce the work for nodes that the HS-DAG would merge or close.
- **Conflicts from an ATMS.** De Kleer and Williams (1987) computed the conflicts with an [assumption-based truth maintenance system](/assumption-based-truth-maintenance/) and generated the candidates from them in their General Diagnostic Engine.

## When to use it

Use the HS-DAG when the conflicts are not given in advance but can be found by a consistency checker, and when you want the diagnoses in increasing size. This is the usual case in model-based diagnosis of circuits and of configuration or software models. If the full collection of sets is given and only one smallest hitting set is needed, an exact or approximate [hitting set](/hitting-set/) method fits better. If all minimal hitting sets of a large explicit collection are needed, look at [minimal transversal enumeration](/minimal-transversal-enumeration/).

## Pitfalls

- **Reiter's pruning without relabeling.** Cutting the extra edges of a node but keeping its old label can lose diagnoses, as in Figure 2. Relabel the node with the smaller conflict.
- **Closing on a duplicate in a tree.** In a tree, closing a node because another node has the same set is safe only if that other node is never cut later. Merging the two into one node, as in the DAG, removes the problem.
- **Closing on equal sets.** The closing test must use a proper subset. A node equal to a checked node is that node.
- **Depth-first search.** The closing test relies on all smaller diagnoses being found first. A depth-first order can mark a non-minimal set as checked.
- **Inconsistent observations.** If the system description and the observations are already inconsistent, the oracle returns the empty conflict, and the correct answer is "no diagnosis". Code that assumes every label has at least one element can loop or crash here.

## Implementations

## History

Reiter (1987) set out the consistency-based theory of diagnosis, proved that diagnoses are minimal hitting sets of the conflict sets, and gave the HS-tree with label reuse, closing and pruning. In the same issue of Artificial Intelligence, de Kleer and Williams (1987) described the General Diagnostic Engine, which finds conflicts with an ATMS. Greiner, Smith and Wilkerson (1989) showed that Reiter's pruning can lose diagnoses, gave the HS-DAG with relabeling, and proved it correct. Wotawa (2001) published a later variant of the construction.

## References
