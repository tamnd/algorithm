---
tag: HBJAYD
kind: algorithm
slug: hartigan-algorithm
name: Hartigan's algorithm
aliases:
- Hartigan parsimony
area: biology/phylogenetics
level: advanced
summary: Unit-cost small parsimony on a rooted tree of any degree. Upper and lower state sets give the score and, in a second pass, every state that each node takes in some optimal labeling.
solves: [small-parsimony]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, k: the number of states, m: the number of sites}
  time: {worst: Θ(m n k), average: Θ(m n k), best: Θ(m n k)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1973
  people: [John A. Hartigan]
  note: Hartigan published a method for the minimum mutation fits of a character to a given tree in 1973. It works for nodes of any degree, proves the optimality of Fitch's rules, and gives all optimal fits.
prereqs: [fitch-algorithm, small-parsimony]
see_also: [sankoff-algorithm, maximum-parsimony, ancestral-sequence-reconstruction, tree-dynamic-programming, postorder-traversal, preorder-traversal]
sources:
  - paper: doi:10.2307/2529676
    title: J. A. Hartigan, Minimum mutation fits to a given tree, Biometrics 29(1), 1973, 53-65
    locator: the fits of least mutation to a given tree with nodes of any degree, the proof of their optimality, and the generation of all such fits
  - paper: doi:10.2307/2412116
    title: Walter M. Fitch, Toward defining the course of evolution, minimum change for a specific tree topology, Systematic Zoology 20(4), 1971, 406-416
    locator: the case of binary trees, which this algorithm extends
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 2, Counting evolutionary changes, and Chapter 6, Ancestral states and branch lengths
---

Hartigan's algorithm solves the [small parsimony problem](/small-parsimony/) with unit costs on a rooted tree whose nodes may have any number of children. In a [postorder](/postorder-traversal/) pass, each node counts, for each state, how many of its children allow that state. The states with the highest count form the upper set of the node, and the states with one less form its lower set. The score grows by the number of children minus the highest count. A [preorder](/preorder-traversal/) pass then gives each node its final set: the set of all states that the node has in at least one most parsimonious labeling. Both passes take $O(nk)$ time for $n$ nodes and $k$ states. On a binary tree, the upper sets and the score are those of [Fitch's algorithm](/fitch-algorithm/), so the method also proves Fitch's rules and corrects the sets of Fitch's first pass.

## In plain words

Suppose an ancestor has many children. Each child has a set of letters that suit it best. For each letter, count how many children would be happy with it. A letter that suits the most children is a best choice for the ancestor. Each child that it does not suit needs one change on its branch, so the count of changes grows by the number of unhappy children.

Keep also the letters that are one vote short. They are almost as good: if the ancestor's own parent has such a letter, taking it costs the same as taking a best letter.

Then go down from the top. The top node can take any of its best letters. Each lower node looks at the letters its parent can take and finds the letters it can take in a best solution. At the end, each node knows all its best letters.

## The problem

**Input.** A rooted tree $T$ with $n$ nodes, in which an internal node may have any number $d \ge 1$ of children, and a state $x(\ell)$ at each leaf $\ell$.

**Output.** The least number of edges $(u, w)$ with $\lambda(u) \ne \lambda(w)$ over all labelings $\lambda$ that agree with $x$ at the leaves, and for each node $v$ the set $F_v$ of the states $\lambda(v)$ over all labelings $\lambda$ that reach this least number. See [small parsimony](/small-parsimony/).

## The algorithm

Here a state means a state that occurs at some leaf. Other states are never optimal, and leaving them out keeps the sets small. Write $n_v(a)$ for the number of children of $v$ whose upper set holds $a$.

```pseudo id=main
HARTIGAN(T, x)
L1  score ← 0
L2  for each node v of T in postorder do
L3      if v is a leaf then U_v ← {x(v)}, L_v ← ∅
L4      else for each state a: n_v(a) ← number of children w of v with a ∈ U_w
L5          M ← max over a of n_v(a)
L6          U_v ← {a : n_v(a) = M}, L_v ← {a : n_v(a) = M − 1}
L7          score ← score + (number of children of v) − M
L8  F_root ← U_root
L9  for each node v in preorder, and each child w of v do
L10     if w is a leaf then F_w ← U_w
L11     else F_w ← F_v ∩ (U_w ∪ L_w)
L12         if F_v ⊄ U_w then F_w ← F_w ∪ U_w
L13 return score, U, L, F
```

Lines L1 to L7 are the first pass. The upper set $U_v$ holds the best states of $v$ for its own subtree, and the lower set $L_v$ holds the states that cost exactly one change more. Line L7 counts one change for each child that cannot share the best state of $v$.

Lines L8 to L12 are the second pass. If the parent can take a state $a$ of $U_w$, then $w$ can take $a$ (line L11). If the parent can take a state $a$ of $L_w$, then $w$ can take $a$, at one change inside its subtree, or a state of $U_w$, at one change on its edge; both cost the same. If the parent can take a state outside $U_w$, then a state of $U_w$ is optimal for $w$ (line L12). To get one labeling from the final sets, give the root any state of $F_{\text{root}}$, and give each child the parent's state if it is in the child's upper set, and a state of its upper set if not.

## Example

Take seven leaves with the states A, G, G, C, A, G, C. Let $u$ be the parent of the first three, $w$ the parent of the next two, and let the root $r$ have the children $u$, $w$, $t_6$ and $t_7$. So $r$ has four children and $u$ has three. The states are A, C and G.

| node | children's upper sets | counts | $U$ | $L$ | changes added |
|---|---|---|---|---|---|
| $u$ | $\{$A$\}$, $\{$G$\}$, $\{$G$\}$ | A 1, G 2, C 0 | $\{$G$\}$ | $\{$A$\}$ | $3 - 2 = 1$ |
| $w$ | $\{$C$\}$, $\{$A$\}$ | A 1, C 1, G 0 | $\{$A, C$\}$ | $\{$G$\}$ | $2 - 1 = 1$ |
| $r$ | $\{$G$\}$, $\{$A, C$\}$, $\{$G$\}$, $\{$C$\}$ | A 1, C 2, G 2 | $\{$C, G$\}$ | $\{$A$\}$ | $4 - 2 = 2$ |

The score is $1 + 1 + 2 = 4$. The second pass gives:

- $F_r = U_r = \{$C, G$\}$.
- At $u$: $F_r \cap (U_u \cup L_u) = \{$C, G$\} \cap \{$A, G$\} = \{$G$\}$. C is in $F_r$ but not in $U_u$, so line L12 adds $U_u = \{$G$\}$. So $F_u = \{$G$\}$.
- At $w$: $F_r \cap (U_w \cup L_w) = \{$C, G$\}$. G is in $F_r$ but not in $U_w$, so line L12 adds $\{$A, C$\}$. So $F_w = \{$A, C, G$\}$.

The site has exactly four most parsimonious labelings of $(r, u, w)$: (C, G, C), and (G, G, $s$) for $s \in \{$A, C, G$\}$. For example, (G, G, G) has changes on the edges to $t_1$, $t_4$, $t_5$ and $t_7$. So G is optimal at $w$ although it is not in $U_w$: the upper sets alone do not give the ancestral states, and the lower set $L_w$ is what brings G back.

On a binary tree, line L6 gives the intersection of the two children's sets when it is not empty ($M = 2$) and their union when it is ($M = 1$), and line L7 adds 0 or 1. These are Fitch's rules.

## Correctness

For a node $w$, let $c_w(a)$ be the least number of changes in the subtree of $w$ when $w$ has state $a$, and $s_w = \min_a c_w(a)$. The first pass keeps the invariant that $U_w$ is the set of states with $c_w(a) = s_w$, and that a parent in state $a$ pays $s_w + [a \notin U_w]$ for the subtree of $w$ and the edge above it. Then a node $v$ with $d$ children pays $c_v(a) = \sum_w s_w + d - n_v(a)$, which is least for the states of highest count, and $L_v$ is the set of states with $c_v(a) = s_v + 1$. For the second pass, given the state $a$ of its parent, the optimal states of $w$ are $\{a\}$ if $a \in U_w$, $\{a\} \cup U_w$ if $a \in L_w$, and $U_w$ otherwise. A state is optimal at $w$ in the whole tree exactly when it is optimal given some optimal state of the parent, because the subtree of $w$ can be solved again once the parent's state is fixed. Lines L11 and L12 are the union of the three cases over the parent's final set. The full proof is below.

## Complexity

- **Time.** At a node with $d$ children, line L4 reads the $d$ upper sets, each of at most $k$ states, and lines L5 and L6 scan the $k$ counts. Summed over all nodes, this is $O(nk)$, because each node is the child of one node. Lines L11 and L12 take $O(k)$ time per edge. So a site takes $\Theta(nk)$ time and $m$ sites take $\Theta(mnk)$.
- **Space.** Three sets per node, $\Theta(nk)$.
- **Bit sets.** For DNA, the sets are 4-bit masks and the counts are small, so each node takes $O(d)$ word operations.

## Properties

- **Exact.** It gives the least number of changes and, for each node, the exact set of its states in optimal labelings.
- **Deterministic.** It returns sets, not one labeling, so it makes no choice between ties.
- **Any degree.** It treats a node with many children as one node: it does not resolve it into a binary tree. A binary resolution can have a lower score, so the two are different problems.
- **Unit costs only.** For a cost table, use the [Sankoff algorithm](/sankoff-algorithm/).
- **Agrees with Fitch.** On binary trees, the score and the upper sets equal those of [Fitch's algorithm](/fitch-algorithm/).

## Variants and improvements

- **One labeling.** Pick a state of $F_{\text{root}}$, then go down with the rule of the algorithm section. This is Fitch's second pass with the upper sets.
- **All labelings.** The rule of the second pass, given the parent's state, lists the options for each child. A depth-first walk over these options lists every most parsimonious labeling.
- **Counting labelings.** Count, for each node and parent state, the number of optimal labelings of its subtree, by multiplying over the children.
- **Unrooted trees.** Root the tree at any internal node. The score and the final sets do not depend on the choice, because the unit cost is symmetric.
- **Weighted costs.** The [Sankoff algorithm](/sankoff-algorithm/) and its second pass from the root generalize the final sets to any cost table, at $O(nk^2)$ time.

## When to use it

Use Hartigan's algorithm for unit-cost parsimony on trees with polytomies, such as a consensus tree or a tree with unresolved groups, and whenever you need every optimal ancestral state, not only one labeling, for example to report ambiguous reconstructions. On a binary tree, if you need only the score, [Fitch's algorithm](/fitch-algorithm/) does the same work with simpler code.

## Pitfalls

- **Using Fitch's rules on a polytomy.** Folding the intersection and union over the children one at a time scores a binary resolution of the node. On a star with leaves A, A, C, C and G, the fold gives 2, while the star needs 3 changes. Line L7 gives $5 - 2 = 3$.
- **Forgetting the lower sets.** Without line L11's use of $L_w$, the second pass misses states such as G at $w$ in the example.
- **Upper sets as ancestral states.** As in Fitch's algorithm, $U_v$ is optimal for the subtree of $v$ only. Only $U_{\text{root}}$ is a final set.
- **Leaves in the second pass.** A leaf has its observed state and nothing else. Line L10 must not apply the rule of lines L11 and L12 to a leaf, because its lower set is empty and its upper set is fixed by the data.

## Implementations

## History

John Hartigan published the method in Biometrics in 1973, two years after Fitch. Fitch's rules work on binary trees. Hartigan's counts work on trees with nodes of any degree, and he proved that the method gives the least number of mutations, which also proves Fitch's rules. His paper also generates all the fits of least mutation, which on this page are the final sets of the second pass. Sankoff (1975) and Sankoff and Rousseau (1975) then gave the dynamic program for any cost table.

## References
