---
tag: AZ0KEP
kind: algorithm
slug: sankoff-algorithm
name: Sankoff algorithm
aliases:
- weighted parsimony dynamic program
area: biology/phylogenetics
level: advanced
summary: Dynamic program over a fixed rooted tree that finds the least total cost of state changes for any cost table, with a table of k costs per node, in O(nk^2) time.
solves: [small-parsimony]
model: word-ram
complexity:
  vars: {n: the number of nodes of the tree, k: the number of states, m: the number of sites}
  time: {worst: Θ(m n k^2), average: Θ(m n k^2), best: Θ(m n k^2)}
  space: {extra: Θ(n k)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1975
  people: [David Sankoff, Pascale Rousseau]
  note: Sankoff published the labeling of the internal nodes of a given tree with sequences of least mutation cost in 1975. The same year, Sankoff and Rousseau gave the dynamic program over the tree for one character in a metric space.
prereqs: [small-parsimony, tree-dynamic-programming, fitch-algorithm]
see_also: [hartigan-algorithm, wagner-parsimony, camin-sokal-parsimony, maximum-parsimony, ancestral-sequence-reconstruction, felsenstein-pruning, steiner-tree-problem, traceback]
sources:
  - paper: doi:10.1137/0128004
    title: David Sankoff, Minimal mutation trees of sequences, SIAM Journal on Applied Mathematics 28(1), 1975, 35-42
    locator: the reconstruction of the sequences at the internal nodes of a given tree with the least total mutation cost
  - paper: doi:10.1007/BF01681346
    title: David Sankoff and Pascale Rousseau, Locating the vertices of a Steiner tree in an arbitrary metric space, Mathematical Programming 9, 1975, 240-246
    locator: the dynamic program that places the internal vertices of a tree of given shape in a metric space, one coordinate at a time
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 2, Counting evolutionary changes, the section on Sankoff's algorithm
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Section 10.10, Small Parsimony Problem (the weighted version)
---

The Sankoff algorithm solves the weighted [small parsimony problem](/small-parsimony/): given a rooted tree, a state at each leaf, and a cost $\delta(a, b)$ for each change from state $a$ to state $b$, it finds states for the internal nodes with the least total cost along the edges. It keeps, for each node $v$ and each state $a$, the value $C_v(a)$: the least cost of the subtree of $v$ when $v$ has state $a$. A [postorder](/postorder-traversal/) pass fills these tables, and a [traceback](/traceback/) from the root picks the states. Each edge does $k^2$ work for $k$ states, so one site takes $O(nk^2)$ time on a tree with $n$ nodes. The tree may have nodes of any degree, and the cost table may be asymmetric or forbid some changes with an infinite cost. With the unit cost it gives the same score as [Fitch's algorithm](/fitch-algorithm/).

## In plain words

Some changes are more likely than others. In DNA, a change between A and G, or between C and T, is more common than the other changes, so it can cost less. Fitch's sets cannot count such costs, so keep a price list at each node.

The price list of a node says, for each letter, how cheap the part of the tree below the node can be if the node has that letter. At a tip, its own letter costs 0 and every other letter is impossible. Going up, a node asks each child: if I have this letter, what is your best price, with the change on our edge? It adds the answers.

At the root, the cheapest entry is the answer. To find the ancestors, go back down and give each child the letter that gave the best price for its parent's letter.

## The problem

**Input.** A rooted tree $T$ with $n$ nodes, a set $\Sigma$ of $k$ states in a fixed order, a state $x(\ell)$ at each leaf $\ell$, and a cost $\delta : \Sigma \times \Sigma \to \mathbb{R}_{\ge 0} \cup \{\infty\}$. The value $\delta(a, b)$ is the cost of an edge from a parent in state $a$ to a child in state $b$.

**Output.** The least value of $\sum_{(u, w) \in E(T)} \delta(\lambda(u), \lambda(w))$ over all labelings $\lambda$ that agree with $x$ at the leaves, and one labeling that reaches it. See [small parsimony](/small-parsimony/).

## The algorithm

For a node $v$ and a state $a$, let $C_v(a)$ be the least cost of the edges below $v$ when $v$ has state $a$. Once $v$ has a state, its children's subtrees are independent, so

$$C_v(a) = \sum_{w \text{ child of } v} \min_{b \in \Sigma} \bigl(\delta(a, b) + C_w(b)\bigr).$$

```pseudo id=main
SANKOFF(T, x, Σ, δ)
L1  for each node v of T in postorder do
L2      if v is a leaf then for each state a: C_v(a) ← 0 if a = x(v), else ∞
L3      else for each state a do
L4          C_v(a) ← Σ over the children w of v of min over b of (δ(a, b) + C_w(b))
L5  score ← min over a of C_root(a)
L6  λ(root) ← the first state a with C_root(a) = score
L7  for each node v in preorder, and each child w of v do
L8      λ(w) ← the first state b that minimizes δ(λ(v), b) + C_w(b)
L9  return score, λ
```

Lines L1 to L4 fill the tables. The postorder puts the children of $v$ before $v$, so line L4 reads tables that are full. Lines L5 to L8 are the traceback. Line L8 picks, for the child $w$, the same state $b$ that gave the minimum for $\lambda(v)$ in line L4. At a leaf, $C_w(b)$ is finite only for $b = x(w)$, so line L8 keeps the observed state whenever the score is finite.

## Example

Take the tree $((t_1, t_2), (t_3, (t_4, t_5)))$ with the leaf states A, C, T, G, A. Let a transition (A and G, or C and T) cost 1, and let a transversion (any other change) cost 2. The internal nodes are $u = (t_1, t_2)$, $w = (t_4, t_5)$, $v = (t_3, w)$ and the root $r = (u, v)$. The tables, in the order A, C, G, T:

| node | children | $C(\text{A})$ | $C(\text{C})$ | $C(\text{G})$ | $C(\text{T})$ |
|---|---|---|---|---|---|
| $u$ | A, C | 2 | 2 | 3 | 3 |
| $w$ | G, A | 1 | 4 | 1 | 4 |
| $v$ | T, $w$ | 3 | 4 | 3 | 3 |
| $r$ | $u$, $v$ | 5 | 6 | 6 | 6 |

For example, $C_u(\text{G}) = \delta(\text{G}, \text{A}) + \delta(\text{G}, \text{C}) = 1 + 2 = 3$. For $v$ in state A, the leaf $t_3$ costs $\delta(\text{A}, \text{T}) = 2$, and the child $w$ costs $\min(0 + 1, 2 + 4, 1 + 1, 2 + 4) = 1$, so $C_v(\text{A}) = 3$. At the root, $C_r(\text{A}) = \min_b (\delta(\text{A}, b) + C_u(b)) + \min_b (\delta(\text{A}, b) + C_v(b)) = 2 + 3 = 5$.

The score is 5, at the root state A. In the traceback, $u$ gets A because $\delta(\text{A}, b) + C_u(b)$ is $2, 4, 4, 5$ for $b = $ A, C, G, T. In the same way $v$ gets A (values $3, 6, 4, 5$) and $w$ gets A (values $1, 6, 2, 6$). The changes are A to C on the edge to $t_2$ (cost 2), A to T on the edge to $t_3$ (cost 2) and A to G on the edge to $t_4$ (cost 1), in total 5. Each minimum is reached by one state only, so this labeling is the only optimal one.

With the unit cost, the same tree with the states A, C, C, G, A gives the score 3, as in [Fitch's algorithm](/fitch-algorithm/).

## Correctness

The proof has two parts. First, by induction in postorder, $C_v(a)$ is the least cost of the subtree of $v$ when $v$ has state $a$. At a leaf the only labeling gives $v$ its own state, at cost 0. At an internal node, a labeling of the subtree with $v$ in state $a$ is a choice of a state $b$ for each child $w$ and a labeling of the subtree of $w$ with $w$ in state $b$. The cost is the sum over the children of $\delta(a, b) + $ the cost below $w$, and the children's choices are independent, so the least cost is the sum of the separate minimums. Second, the traceback keeps the invariant that the subtree of each node $w$ gets a labeling of cost $C_w(\lambda(w))$: line L8 picks for each child the state that reaches its term in line L4. At the root this cost is the score. The full proof is below.

## Complexity

- **Time.** Line L4 computes, for each of the $k$ states $a$ of $v$ and each child $w$, a minimum over $k$ states. Each edge of the tree is the edge to one child, so the first pass does $k^2$ steps per edge, $\Theta(nk^2)$ in total. The traceback does $k$ steps per edge. So one site takes $\Theta(nk^2)$ time in every case, and $m$ sites take $\Theta(mnk^2)$.
- **Space.** The tables take $\Theta(nk)$ numbers for one site.
- **Special costs.** For the unit cost, the minimum of line L4 is $\min(C_w(a), \min_b C_w(b) + 1)$, which takes $O(1)$ time after one pass over the table, so a site takes $O(nk)$ time. For the ordered cost $|a - b|$ of [Wagner parsimony](/wagner-parsimony/), two sweeps over the states, one up and one down, compute all $k$ minimums in $O(k)$ time.

## Properties

- **Exact.** It returns the least cost for any table $\delta$ with values in $\mathbb{R}_{\ge 0} \cup \{\infty\}$. The table need not be symmetric, and it need not obey the triangle inequality.
- **Deterministic.** The order of $\Sigma$ breaks the ties in lines L6 and L8.
- **Any degree.** A node can have any number of children, including one.
- **Root.** For a symmetric $\delta$, the cost does not depend on the direction of the edges, so the score of an unrooted tree is the same for every node chosen as the root. For an asymmetric $\delta$, as in [Camin-Sokal parsimony](/camin-sokal-parsimony/), the root matters.
- **All optimal states.** The tables hold all the information for every optimal labeling. A second pass from the root computes for each node the least cost of the whole tree with that node in each state, and so the set of its optimal states.

## Variants and improvements

- **Fixed root state.** If the ancestral state is known, as in Camin-Sokal parsimony, replace line L5 by the value at that state, or add an edge above the root from a node in that state.
- **Forbidden changes.** An infinite cost forbids a change. This gives [Camin-Sokal parsimony](/camin-sokal-parsimony/) with $\delta(a, b) = \infty$ for $b < a$.
- **Ambiguous data.** A leaf whose state is only known to lie in a set $S$ starts with 0 on $S$ and $\infty$ elsewhere.
- **Sequences.** For aligned sequences, run the algorithm on each site and add the scores. Sites with the same pattern of leaf states have the same score and can be computed once.
- **Counting.** Storing, next to $C_v(a)$, the number of labelings that reach it gives the number of optimal labelings at the same cost.
- **Probabilities.** Replacing min by sum and plus by product turns the algorithm into the [Felsenstein pruning algorithm](/felsenstein-pruning/) for the likelihood of a tree.

## When to use it

Use the Sankoff algorithm when changes between states should have different costs: transitions and transversions in DNA, a cost table for amino acids, ordered or irreversible morphological characters, or a cost of $\infty$ for changes that cannot happen. Use it also on trees with nodes of high degree. For unit costs on binary trees, [Fitch's algorithm](/fitch-algorithm/) gives the same score with less work, and for unit costs on any tree, [Hartigan's algorithm](/hartigan-algorithm/) does. For ordered states, the interval pass of [Wagner parsimony](/wagner-parsimony/) is faster.

## Pitfalls

- **Infinite costs everywhere.** If every labeling has an infinite cost, the score is $\infty$, every entry of line L8 ties at $\infty$, and the returned labeling can even give a leaf a wrong state. Test the score before using the labeling.
- **Direction of the cost.** Line L4 must use $\delta(a, b)$ with $a$ the parent state and $b$ the child state. For an asymmetric table, swapping the two gives the score of the reversed process.
- **Floating-point costs.** Line L8 compares sums for the least value. With real costs, use the same expression as line L4, or store the minimizing state of line L4, so that rounding does not pick a state that is not optimal.
- **Tables as ancestral states.** The state with the least $C_v(a)$ at an internal node is the best state for its subtree alone, not for the whole tree. Use the traceback, or the second pass of the properties above.

## Implementations

## History

In 1975 David Sankoff published a method to reconstruct the sequences at the internal nodes of a given tree with the least total mutation cost, in the SIAM Journal on Applied Mathematics. In the same year, Sankoff and Pascale Rousseau showed in Mathematical Programming how to place the internal vertices of a tree of given shape in any metric space so that the total length is least, one coordinate at a time. That dynamic program over the tree, with a table of costs per state, is what is now called the Sankoff algorithm. It contains the unit-cost rules of Fitch (1971) and Hartigan (1973) as special cases.

## References
