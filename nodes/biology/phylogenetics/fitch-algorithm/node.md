---
tag: NYTSYT
kind: algorithm
slug: fitch-algorithm
name: Fitch's algorithm
aliases:
- Fitch parsimony
area: biology/phylogenetics
level: core
summary: Two passes over a rooted binary tree that find the least number of state changes for one character, by set intersection or union at each node, in O(nk) time.
solves: [small-parsimony]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, k: the number of states, m: the number of sites}
  time: {worst: Θ(m n k), average: Θ(m n k), best: Θ(m n k)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1971
  people: [Walter M. Fitch]
  note: Fitch published the intersection and union rules in 1971 for the least number of changes on a given tree topology. Hartigan (1973) proved that they are optimal and extended them to trees of any degree.
prereqs: [small-parsimony, postorder-traversal, tree-dynamic-programming]
see_also: [hartigan-algorithm, sankoff-algorithm, maximum-parsimony, ancestral-sequence-reconstruction, parsimony-informative-site, felsenstein-pruning, preorder-traversal, binary-tree]
sources:
  - paper: doi:10.2307/2412116
    title: Walter M. Fitch, Toward defining the course of evolution, minimum change for a specific tree topology, Systematic Zoology 20(4), 1971, 406-416
    locator: the rules of intersection and union on a binary tree, and the count of the unions as the number of changes
  - paper: doi:10.2307/2529676
    title: J. A. Hartigan, Minimum mutation fits to a given tree, Biometrics 29(1), 1973, 53-65
    locator: the proof that the method gives the least number of mutations, for trees of any degree
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 2, Counting evolutionary changes, the section on the Fitch algorithm
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Section 10.10, Small Parsimony Problem
---

Fitch's algorithm solves the [small parsimony problem](/small-parsimony/) with unit costs on a rooted binary tree. For one character, such as one column of an alignment, it finds the least number of changes along the edges that explains the states at the leaves, and one assignment of states to the internal nodes that reaches it. A [postorder](/postorder-traversal/) pass gives each node a set of states: the intersection of the sets of its two children if it is not empty, and their union otherwise, with one change counted for each union. A [preorder](/preorder-traversal/) pass then picks the states. Both passes do $O(k)$ work per node, so one site takes $O(nk)$ time for $n$ nodes and $k$ states. The sets of the first pass give the score, but they are not the sets of all optimal states.

## In plain words

Think of a family tree with a letter at each living species. Go up from the tips. At each ancestor, look at the letter sets of its two children. If they share a letter, keep only the shared letters: the ancestor can agree with both children for free. If they share nothing, keep all letters of both and count one change, because one of the two children must differ from the ancestor.

At the top, the count is the least number of changes for the whole tree. To get the ancestors, go back down. The top node takes any letter of its set. Each child keeps the letter of its parent if that letter is in its own set, and takes a letter of its own set if not.

## The problem

**Input.** A rooted binary tree $T$ with $n$ nodes and a state $x(\ell)$ from a set $\Sigma$ of $k$ states at each leaf $\ell$.

**Output.** The least number of edges $(u, v)$ with $\lambda(u) \ne \lambda(v)$ over all labelings $\lambda$ of the nodes that agree with $x$ at the leaves, and one labeling that reaches it. For aligned sequences, run the algorithm on each site and add the scores. See [small parsimony](/small-parsimony/) for the general problem.

## The algorithm

Write $S_v$ for the set of node $v$ in the first pass.

```pseudo id=main
FITCH(T, x)
L1  score ← 0
L2  for each node v of T in postorder do
L3      if v is a leaf then S_v ← {x(v)}
L4      else let l and r be the two children of v
L5          if S_l ∩ S_r ≠ ∅ then S_v ← S_l ∩ S_r
L6          else S_v ← S_l ∪ S_r, score ← score + 1
L7  λ(root) ← any state of S_root
L8  for each node v in preorder, and each child w of v do
L9      if λ(v) ∈ S_w then λ(w) ← λ(v)                 ▷ no change on the edge
L10     else λ(w) ← any state of S_w                     ▷ one change on the edge
L11 return score, λ
```

Lines L1 to L6 are the first pass. The [postorder](/postorder-traversal/) puts both children before their parent, so lines L5 and L6 read sets that are already known. Line L6 is the only place where the score grows.

Lines L7 to L11 are the second pass. A leaf has a set with one state, so line L9 or L10 gives each leaf its own state. The implementation picks the smallest state at lines L7 and L10, so its output is the same on each run.

## Example

Take the tree $((t_1, t_2), (t_3, (t_4, t_5)))$ with the leaf states A, C, C, G, A, the same instance as in [small parsimony](/small-parsimony/). The internal nodes are $u = (t_1, t_2)$, $w = (t_4, t_5)$, $v = (t_3, w)$ and the root $r = (u, v)$.

The first pass, in postorder:

| node | children's sets | line | set | score |
|---|---|---|---|---|
| $u$ | $\{$A$\}$, $\{$C$\}$ | L6 | $\{$A, C$\}$ | 1 |
| $w$ | $\{$G$\}$, $\{$A$\}$ | L6 | $\{$A, G$\}$ | 2 |
| $v$ | $\{$C$\}$, $\{$A, G$\}$ | L6 | $\{$A, C, G$\}$ | 3 |
| $r$ | $\{$A, C$\}$, $\{$A, C, G$\}$ | L5 | $\{$A, C$\}$ | 3 |

The score is 3. The second pass sets $\lambda(r) = $ A at line L7. Then A is in $S_u$, $S_v$ and $S_w$, so line L9 gives A to $u$, $v$ and $w$. The leaves get their own states. The changes are on the edges $u \to t_2$, $v \to t_3$ and $w \to t_4$: three changes, as the score says.

**The first pass alone is not enough.** All optimal labelings of this site are (A, A, A, A) and (C, C, C, $s$) for $s \in \{$A, C, G$\}$, where the order is $(r, u, v, w)$. So the true sets of optimal states are $\{$A, C$\}$ at $v$ and $\{$A, C, G$\}$ at $w$. The first pass gave $S_v = \{$A, C, G$\}$, which holds G, a state that is not optimal at $v$, and $S_w = \{$A, G$\}$, which misses C. Only the root set is exact. To get every optimal state at every node, use the top-down pass of [Hartigan's algorithm](/hartigan-algorithm/).

## Correctness

For a node $w$, let $s_w$ be the least number of changes inside its subtree, and let $g_w(a)$ be the least number of changes inside the subtree plus on the edge above $w$, when the parent of $w$ has state $a$. The key claim is that $g_w(a) = s_w + [a \notin S_w]$ for every state $a$, and that $S_w$ is the set of states of $w$ that reach $s_w$. It holds at a leaf. At a node with children $l$ and $r$, a state $a$ costs $s_l + s_r + [a \notin S_l] + [a \notin S_r]$. If the two sets meet, the least value is $s_l + s_r$, reached exactly on the intersection. If not, every state is outside at least one set, so the least value is $s_l + s_r + 1$, reached exactly on the union. This is line L5 or L6, and line L6 counts the extra change. At the root the claim gives the score and the set of optimal root states. The second pass picks, at each child, a state that reaches $g_w(\lambda(\text{parent}))$, so the labeling costs exactly the score. The full proof is below.

## Complexity

- **Time.** The first pass does one intersection, and at most one union, per internal node. With sets of $k$ states each, this takes $O(k)$ time, so the pass takes $O(nk)$ time. The second pass does one membership test and one choice per edge, $O(nk)$ time in total. Each set operation reads its sets whatever they hold, so the time is $\Theta(nk)$ per site, and $\Theta(mnk)$ for $m$ sites, in the best, the average and the worst case.
- **Bit sets.** For DNA, $k = 4$ and a set is a 4-bit mask. Intersection, union and the test for the empty set are single machine instructions, so a site takes $\Theta(n)$ time. Programs pack many sites into one word and process them at the same time.
- **Space.** The sets take $O(nk)$ space for one site, or $O(n)$ words with bit sets. The postorder needs an explicit stack of $O(n)$ entries.

## Properties

- **Exact.** It returns the least number of changes and one labeling that reaches it.
- **Deterministic.** With a fixed rule at lines L7 and L10, the output is the same on each run.
- **Binary trees only.** The rules of lines L5 and L6 compare exactly two sets. A node with three or more children needs [Hartigan's algorithm](/hartigan-algorithm/).
- **Unit costs only.** Every change costs 1. For a cost table, use the [Sankoff algorithm](/sankoff-algorithm/).
- **Root independent.** The score does not depend on where an unrooted tree is rooted, because the unit cost is symmetric and obeys the triangle inequality ([small parsimony](/small-parsimony/)).
- **Not online.** The second pass needs the whole first pass.

## Variants and improvements

- **Any degree.** [Hartigan's algorithm](/hartigan-algorithm/) counts, for each state, how many children have it in their sets. With two children it gives the same sets and score as Fitch.
- **Weighted costs.** The [Sankoff algorithm](/sankoff-algorithm/) replaces each set by a table of $k$ costs, at $O(nk^2)$ time.
- **All optimal states.** A top-down pass with the lower sets of Hartigan gives, for each node, the set of states that it takes in at least one optimal labeling.
- **Ambiguous and missing data.** A leaf with an ambiguity code, such as R for A or G, starts with the set of its possible states, and a missing state starts with all of $\Sigma$. The proof above holds without change, since a leaf with set $S$ costs $[a \notin S]$ for a parent in state $a$.
- **Faster tree search.** In a search for [maximum parsimony](/maximum-parsimony/), a local change of the tree changes only the sets on the path from the change to the root. Programs keep the first-pass sets and recompute only that path.
- **Uninformative sites.** A site that is not [parsimony-informative](/parsimony-informative-site/) has the same score on every tree, so a tree search can skip it and add its constant score at the end.

## When to use it

Use Fitch's algorithm to score a given binary tree under unit costs, which is the inner loop of most searches for maximum parsimony. It is the fastest exact method for this case, in particular with bit sets for DNA. If some changes should cost more than others, for example transversions more than transitions, use the [Sankoff algorithm](/sankoff-algorithm/). If the tree has nodes with more than two children, use [Hartigan's algorithm](/hartigan-algorithm/). If you need all optimal ancestral states, not one labeling, add Hartigan's top-down pass.

## Pitfalls

- **The first-pass sets are not ancestral states.** As the example shows, a set of the first pass can hold a state that is in no optimal labeling, and miss a state that is in one. Only the root set is exact. Report ancestral states from the second pass, or from Hartigan's final sets.
- **Folding the rule over many children.** On a node with more than two children, applying lines L5 and L6 to the children one after another scores a binary resolution of the node, not the node itself. For a star with leaves A, A, C, C and G, the fold gives 2, but the star needs 3 changes.
- **Choosing a free state at line L10 without the test.** Line L9 must keep the parent's state when it is in the child's set. A child that takes any state of its set can add a change that the score does not count.
- **Gaps.** Treating a gap as a fifth state counts each gap column as a change, so a long insertion counts as many changes. Treating it as missing data ignores it. The two choices give different trees, and the page or the program should say which one it uses.

## Implementations

## History

Walter Fitch published the method in 1971 in Systematic Zoology, to count the least number of nucleotide replacements on a given tree topology. His rules are the intersection and the union of this page, and the count of the unions. In 1973 John Hartigan gave a proof that the rules give the least number of changes, and extended them to trees whose nodes have any number of children, with the upper and lower sets that also give all optimal labelings. Kluge and Farris (1969) and Farris (1970) had given a similar pass for ordered characters, with intervals in place of sets. Sankoff (1975) gave the dynamic program for any cost table, of which Fitch's algorithm is the case of unit costs.

## References
