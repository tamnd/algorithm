---
tag: HCBMN4
kind: data-structure
slug: pq-tree
name: PQ-tree
aliases:
- Permutation-equivalence tree
area: sequences/interval-problems
level: research
summary: A tree that represents all permutations satisfying a consecutive-ones constraint family.
model: pointer-machine
complexity:
  vars: {n: the number of leaves (the time is per REDUCE in the simple form; Booth and Lueker do m reductions of total size f in O(n + m + f))}
  time: {worst: O(n)}
  space: {extra: Θ(n)}
prereqs: [consecutive-ones-property, rooted-tree, permutation]
see_also: [planarity-testing, st-numbering, lexicographic-bfs, chordal-graph, hypergraph, partition-refinement, amortized-cost, k-colorable-interval-subgraph]
sources:
  - paper: doi:10.1016/S0022-0000(76)80045-1
    title: "Kellogg S. Booth and George S. Lueker, Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms, Journal of Computer and System Sciences 13(3) (1976), pages 335 to 379"
    locator: the definition of PQ-trees and their equivalence, the REDUCE operation with its templates, the linear time bound, and the applications to the consecutive ones property, interval graphs and planarity
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 8, Interval Graphs (the consecutive ones property of the clique matrix, and the recognition of interval graphs that the PQ-tree supports)
---

A PQ-tree stores a set of permutations of a finite set $U$: its leaves are the elements of $U$, and its inner nodes are P-nodes, whose children may be put in any order, and Q-nodes, whose children may only be kept in order or reversed. The permutations it stores are the leaf orders that these choices give. Booth and Lueker introduced it in 1976 with one main operation, REDUCE$(T, S)$, which keeps exactly the stored permutations in which the set $S$ is consecutive. Reducing the universal tree by every row of a 0-1 matrix gives the tree of all [consecutive ones](/consecutive-ones-property/) orders, or shows that there are none, in $O(n + m + f)$ time in total.

## In plain words

Think of a mobile that hangs from the ceiling. Each item of the set hangs at the bottom. Some joints of the mobile spin freely, so the parts below them can come in any order. Other joints are stiff bars, which you can only turn round, so their parts come in the given order or backward.

Read the items from left to right. Each way to set the joints gives one order of the items. The mobile is a short way to write down a large number of orders.

When you learn that some items must stand side by side, you rebuild a few joints near those items. Afterwards the mobile gives exactly the old orders in which those items are side by side. If no such order is left, the rebuild fails, and you know the rules cannot all hold.

## The abstract type

Let $U$ be a finite set with $n \ge 1$ elements. A *PQ-tree over $U$* is a rooted ordered tree with these parts:

- The leaves are the elements of $U$, one leaf for each element.
- Each inner node is a *P-node* with at least 2 children or a *Q-node* with at least 3 children.

The *frontier* of $T$ is the sequence of its leaves from left to right. Two trees are *equivalent* when one turns into the other by a sequence of two moves: put the children of a P-node in any order, or reverse the children of a Q-node. Write $\mathrm{Fr}(T)$ for the set of frontiers of the trees equivalent to $T$. Equivalently, define $\mathrm{Fr}$ by recursion on the tree:

- For a leaf $u$, $\mathrm{Fr}(u) = \{u\}$.
- For a P-node with children $c_1, \ldots, c_d$, $\mathrm{Fr}$ is the set of concatenations $f_{\sigma(1)} \cdots f_{\sigma(d)}$ for every permutation $\sigma$ and every choice of $f_i \in \mathrm{Fr}(c_i)$.
- For a Q-node, the same set, but only for the identity and the reversal of $1, \ldots, d$.

These are the operations:

- **UNIVERSAL$(U)$.** Return a P-node whose children are the leaves of $U$, or the one leaf if $n = 1$. Then $\mathrm{Fr}$ is all $n!$ permutations of $U$.
- **REDUCE$(T, S)$** for $S \subseteq U$. Return a tree $T'$ such that $\mathrm{Fr}(T') = \{\, \pi \in \mathrm{Fr}(T) : \text{the elements of } S \text{ are consecutive in } \pi \,\}$, or fail when this set is empty.
- **FRONTIER$(T)$.** Return the frontier of $T$ itself, one of the stored permutations, in $O(n)$ time.

Every set of permutations that has the form "all orders of $U$ in which each of $S_1, \ldots, S_m$ is consecutive" is $\mathrm{Fr}(T)$ for a PQ-tree $T$: start from UNIVERSAL$(U)$ and reduce by $S_1, \ldots, S_m$ in turn. The order of the sets does not matter for the result, since REDUCE intersects with one condition at a time.

The two node rules on the number of children lose nothing. A P-node or Q-node with one child allows only that child's orders, and a Q-node with two children allows both orders of the two, the same as a P-node, so such nodes are rewritten at once.

## Representation

Each node stores its kind, P, Q or leaf, and the list of its children in the current order; a leaf stores its element. The implementation on this page uses Python tuples `("leaf", x)`, `("P", [children])` and `("Q", [children])`. Since every inner node has at least 2 children, a tree with $n$ leaves has at most $n - 1$ inner nodes, so the tree takes $\Theta(n)$ space.

REDUCE needs, for each node $x$, the number $k(x)$ of its leaves in $S$ and the number $\lvert x \rvert$ of all its leaves. They give the *label* of $x$: *empty* if $k(x) = 0$, *full* if $k(x) = \lvert x \rvert$, and *partial* otherwise. The *pertinent root* is the deepest node whose leaves include all of $S$.

The structure of Booth and Lueker adds parent pointers, and for the children of a Q-node it keeps parent pointers only at the two end children, with sibling pointers between neighbours. This lets a reduction work bottom up from the leaves of $S$ and touch only the pertinent part of the tree, which is the source of the linear total bound.

## Operations

REDUCE first labels the nodes, then walks down to the pertinent root, and there rebuilds the tree by *templates*, one for each pattern of child labels. The sequence form SINGLY$(x)$ of a partial node lists trees whose frontiers, concatenated, give exactly the frontiers of $x$ in which the full leaves come last.

```pseudo id=main
REDUCE(T, S)                      ▷ result: the frontiers of T in which S is consecutive
L1  if |S| ≤ 1 then return T
L2  label each node empty, full or partial by counting its leaves in S
L3  x ← root; while x has one non-empty child c and c is partial do x ← c
L4  replace x by ROOT(x) and return T    ▷ x is the pertinent root; any failure fails REDUCE

ROOT(x)                           ▷ make the full leaves below x consecutive
L5  if x is a P-node then fail if x has more than 2 partial children
L6      Z ← SINGLY(p₁) · P(full children) · reverse(SINGLY(p₂))   ▷ for the partial children p₁, p₂ present
L7      return P(empty children, Q(Z)), or P(empty children, P(full children)) if no child is partial
L8  if x is a Q-node then fail unless the non-empty children are adjacent and only the two outer ones may be partial
L9      return Q(children, with the left partial one replaced by SINGLY and the right one by reverse(SINGLY))

SINGLY(x)                         ▷ x partial, not the pertinent root: empty part first, full part last
L10 if x is a P-node then fail if x has more than 1 partial child
L11     return P(empty children) · SINGLY(partial child) · P(full children)   ▷ leave out the empty parts
L12 if x is a Q-node then fail unless in one direction the labels read empty*, at most one partial, full*
L13     return the children in that direction, with the partial one replaced by SINGLY of it
```

Here $Z \cdot Z'$ joins two sequences, $P(\ldots)$ and $Q(\ldots)$ build a node over a list of trees, and every new node is normalized: a node with one child is replaced by the child, and a Q-node with two children becomes a P-node. Every tree that SINGLY lists is empty or full, and the empty ones come first.

Line L3 stops at the pertinent root: if $x$ has two or more non-empty children, or one full child, then no child contains all of $S$. Lines L5 to L7 are the templates of Booth and Lueker for a P-node at the root, called P2, P4 and P6 in their paper, and lines L10 and L11 the templates P3 and P5 for a P-node lower down. Lines L8, L9, L12 and L13 are the Q-node templates. The page [consecutive ones property](/consecutive-ones-property/) explains why the sets must be consecutive in this way.

## Example

Take $U = \{1, 2, 3, 4, 5\}$ and the sets $S_1 = \{1, 3\}$, $S_2 = \{2, 3, 4\}$, $S_3 = \{4, 5\}$, $S_4 = \{2, 4\}$ of the example on the [consecutive ones property](/consecutive-ones-property/) page, reduced in the order $S_2, S_3, S_4, S_1$. Write $P(\ldots)$ and $Q(\ldots)$ for the nodes.

| step | tree | frontiers |
|---|---|---|
| UNIVERSAL | $P(1, 2, 3, 4, 5)$ | 120 |
| REDUCE by $\{2, 3, 4\}$ | $P(1, 5, P(2, 3, 4))$ | 36 |
| REDUCE by $\{4, 5\}$ | $P(1, Q(P(2, 3), 4, 5))$ | 8 |
| REDUCE by $\{2, 4\}$ | $P(1, Q(3, 2, 4, 5))$ | 4 |
| REDUCE by $\{1, 3\}$ | $Q(5, 4, 2, 3, 1)$ | 2 |

*Step 1.* The root is the pertinent root, with 3 full leaves and 2 empty ones, and no partial child. Line L7 groups the full children under a new P-node: $3! \cdot 3! = 36$ frontiers.

*Step 2.* The root is the pertinent root: its children $1$, $5$, $P(2, 3, 4)$ are empty, full and partial. SINGLY of $P(2, 3, 4)$ is $P(2, 3), 4$, by line L11, and line L6 appends the full child: $Z = P(2, 3), 4, 5$. Line L7 returns $P(1, Q(Z))$. The Q-node forces 4 between the block $\{2, 3\}$ and 5: $2 \cdot 2 \cdot 2 = 8$ frontiers.

*Step 3.* Line L3 walks from the root to the Q-node, since it is the only non-empty child and it is partial. Its children $P(2, 3)$, $4$, $5$ are partial, full and empty: the non-empty ones are adjacent and the partial one is outside, so line L9 replaces $P(2, 3)$ by its SINGLY form $3, 2$, with the full leaf 2 toward 4. Now 3 is fixed next to 2: 4 frontiers.

*Step 4.* At the root, $1$ is full and the Q-node is partial. Its labels $3, 2, 4, 5$ read full, empty, empty, empty, so line L12 takes the reverse direction, $5, 4, 2, 3$. Line L6 appends the full child 1, and line L7 gives a P-node with no empty children over $Q(5, 4, 2, 3, 1)$, which is normalized to the Q-node itself. The 2 frontiers are $1, 3, 2, 4, 5$ and its reverse, the only consecutive ones orders.

**A failure.** The sets $\{a, b\}, \{b, c\}, \{a, c\}$ over $\{a, b, c\}$ have no common consecutive order. REDUCE by $\{a, b\}$ gives $P(c, P(a, b))$, and REDUCE by $\{b, c\}$ gives $Q(a, b, c)$. For $\{a, c\}$ the root is the Q-node with labels full, empty, full: the non-empty children are not adjacent, and line L8 fails. In the same way, the star $\{a, b\}, \{a, c\}, \{a, d\}$ gives $P(d, Q(b, a, c))$ after two steps and then fails at line L8, since $d$ and $a$ are not neighbours.

**Edge cases.** A set with 0 or 1 elements, or the set of all leaves, leaves the tree unchanged, by line L1 or because the root is full. A set equal to the leaves of one node $y$ also keeps every frontier: the walk of line L3 stops at the parent of $y$, where $y$ is the only non-empty child and is full, and line L7 or line L9 rebuilds a tree with the same frontiers.

## Correctness

The [proof](proofs/correctness.md) shows that REDUCE returns a tree with exactly the frontiers of $T$ in which $S$ is consecutive, and fails exactly when there are none. Its core is a statement on SINGLY, proved by induction on the height: for a partial node $x$ that is not the pertinent root, the trees that SINGLY$(x)$ lists give, concatenated, exactly the frontiers of $x$ in which the leaves of $S$ come last, and SINGLY fails exactly when no frontier of $x$ has this form. At a P-node this forces at most one partial child, all empty children first and all full children last; at a Q-node it forces the labels to read empty, partial, full in one of the two directions. At the pertinent root, the block of $S$ in a frontier has two ends, and only a child that crosses one of the ends can be partial, which gives lines L5 and L8. The proof also shows that each REDUCE stops after a number of steps bounded by the number of nodes.

## Complexity

- **The simple form.** The form above labels the whole tree on line L2, in $O(n)$ time, and then visits each node at most once on lines L3 to L13, so one REDUCE takes $O(n)$ time, and $m$ reductions take $O(mn)$ time. This is the form of the implementation on this page.
- **The form of Booth and Lueker.** Their REDUCE works from the leaves of $S$ upward, in two passes: the first finds the pertinent subtree, the second applies the templates to it from the bottom. With the pointer scheme of the Representation section, they show that $m$ reductions by sets of total size $f$ take $O(n + m + f)$ time, by an [amortized](/amortized-cost/) argument over the whole sequence. The consecutive ones test of an $m \times n$ matrix with $f$ ones is then linear in its size.
- **Space.** $\Theta(n)$ for the tree and the labels.
- **Output.** Counting the frontiers of a tree is a product of $d!$ for each P-node with $d$ children and 2 for each Q-node, so it takes $O(n)$ time, but listing them takes time proportional to their number, which can be $n!$.

## Variants

- **PC-trees.** A variant with C-nodes, whose children lie on a circle, which represents circular orders. It handles the circular ones property and is used for planarity testing.
- **Interval graph recognition.** Booth and Lueker list the [maximal cliques](/maximal-clique/) of a [chordal graph](/chordal-graph/) and reduce by the set of cliques that contain each vertex. The graph is an interval graph if and only if every reduction succeeds, and the final frontier orders the cliques. Later methods replace the PQ-tree by [lexicographic BFS](/lexicographic-bfs/) sweeps.
- **Planarity testing.** In the vertex addition method, the vertices are added in the order of an [st-numbering](/st-numbering/), and a PQ-tree holds the possible orders of the edges that wait to be embedded; each step is a REDUCE by the edges of the new vertex. This gives the linear time [planarity test](/planarity-testing/) of Booth and Lueker.
- **Hypergraphs.** The [hypergraph](/hypergraph/) whose edges are the sets $S_i$ is an interval hypergraph if and only if all reductions succeed.
- **Partition refinement.** [Partition refinement](/partition-refinement/) splits the elements step by step and gives other ways to find one consecutive ones order without building the tree.

## When to use it

Use a PQ-tree when constraints of the form "these elements must be next to each other" arrive one by one and you must keep all orders that satisfy them, or report at once when they conflict: the consecutive ones test, the arrangement of probes in physical maps of DNA, interval models of graphs, and the vertex addition step of planarity tests. If only one valid order is needed and all sets are known in advance, a partition refinement method can be simpler to write. If the sets are few, a search over the tree of the simple form is fast enough and much easier to get right than the full bottom-up version.

## Pitfalls

- **Forgetting to normalize.** A Q-node with two children must become a P-node, and a node with one child must be removed. Otherwise a later Q-node test reads two directions as valid, or a single child hides a partial node, and the result is wrong.
- **The wrong side of a partial child.** At the pertinent root, the left partial child must have its full part on the right, toward the block, and the right one on the left, which is why line L6 and line L9 reverse SINGLY for the second one. Getting this wrong keeps frontiers in which $S$ has a gap.
- **Stopping above the pertinent root.** The root templates assume that no child contains all of $S$. Applied to an ancestor whose only non-empty child is partial, line L6 would call SINGLY on that child and push the block of $S$ to one end of it, which loses every frontier in which the block lies inside.
- **Partial children inside the block.** At a Q-node root, a partial child strictly between the two outer non-empty children leaves empty leaves inside the block, so line L8 must fail.
- **The cost of the simple form.** Labelling the whole tree costs $\Theta(n)$ even for a small set, so $m$ reductions cost $\Theta(mn)$, not linear time. The linear bound needs the bottom-up scheme, and its main difficulty is that the children of a Q-node do not know their parent.

## Implementations

## History

Booth and Lueker introduced PQ-trees in 1976, with the templates, the linear time bound and three applications: the consecutive ones property, the recognition of interval graphs through the clique matrix theorem of Fulkerson and Gross, and planarity testing by the vertex addition method of Lempel, Even and Cederbaum. Their planarity algorithm was the second linear time planarity test, after the path addition algorithm of Hopcroft and Tarjan. The full template system was long regarded as hard to implement, which led to the simpler later methods based on lexicographic BFS for interval graphs and on PC-trees for planarity.

## References
