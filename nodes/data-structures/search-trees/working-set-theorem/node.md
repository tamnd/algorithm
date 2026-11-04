---
tag: 37FBMK
kind: theorem
slug: working-set-theorem
name: Working set theorem
aliases:
- splay tree working set bound
area: data-structures/search-trees
level: advanced
summary: Splay tree access cost is bounded by the logarithm of the working set size of each access.
prereqs: [splay-tree, splaying, potential-method]
see_also: [static-optimality-theorem, dynamic-optimality-conjecture, move-to-front, locality-of-reference, lru-cache, paging-problem, finger-search-tree, amortized-cost]
sources:
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: Section 2, Lemma 1 (Access Lemma) and Theorem 4 (Working Set Theorem)
---

The working set theorem of Sleator and Tarjan (1985, Theorem 4) says that in a [splay tree](/splay-tree/), an access to an item costs $O(\log(t + 1))$ amortized time, where $t$ is the number of distinct items accessed since the last access to that item. A small set of items in active use is therefore cheap to access, however large the tree is. The bound expresses [locality of reference](/locality-of-reference/) in time, as a [least recently used](/lru-cache/) cache does, and it implies the [static optimality theorem](/static-optimality-theorem/) up to the constant factor.

## Statement

Let a splay tree hold $n$ keys, in any initial shape, and let $i_1, \ldots, i_m$ be a sequence of accesses, each a successful search followed by a splay. The cost of an access is the number of nodes on its search path. For access $j$, let $t(j)$ be the number of distinct items accessed after the previous access to $i_j$ and before access $j$. If access $j$ is the first access to $i_j$, let $t(j) = n$.

**Theorem.** The total cost of the sequence is at most
$$\sum_{j=1}^{m} \bigl(6 \lg(t(j) + 1) + 3 \lg W + 2\bigr) + n \lg W + 2 n \lg n, \qquad W = \sum_{k=1}^{n} \frac{1}{k^2} < \frac{\pi^2}{6},$$
which is $O(m + n \log n + \sum_j \log(t(j) + 1))$. Since $3 \lg W < 2.16$, each access costs at most $6 \lg(t(j) + 1) + 4.16$ amortized.

## In plain words

Think of the items you have used most recently as your working set. If you keep coming back to the same few items, the theorem says the splay tree handles each of them almost as fast as if the tree held only those few.

The cost of looking up an item depends on how many other different items you looked at since you last looked at it. Ten different items in between cost about as much as a lookup in a tree of ten items. An item you have not touched for a long time costs as much as a lookup in the whole tree. Nobody tells the tree which items are in the working set; it finds out by moving each item it finds to the top.

## Proof

**The Access Lemma** (Sleator and Tarjan, Lemma 1; proved in [the complexity proof of splaying](/splaying/proofs/complexity.md)). Give each node $x$ a weight $w(x) > 0$, let $s(x)$ be the total weight of the subtree of $x$, $r(x) = \lg s(x)$ and $\Phi = \sum_x r(x)$. The number of rotations of a splay of $x$ in a tree with root $t$, or 1 if there are none, plus the change of $\Phi$, is at most $3(r(t) - r(x)) + 1$. The lemma holds for each fixed choice of weights, and the weights may change between splays, provided the change of $\Phi$ caused by the change of weights is counted.

**Weights from a move-to-front list.** Keep a list $L$ of all $n$ items, at first in any order. After each access, move the accessed item to the front of $L$, as in the [move-to-front](/move-to-front/) rule. Give the item at position $k$ of $L$ the weight $1/k^2$. The positions are always $1, \ldots, n$, so the total weight is always $W$.

**The position of the accessed item.** Before access $j$, the items in front of $i_j$ in $L$ are exactly the distinct items accessed since the last access to $i_j$, because each of them was moved in front of $i_j$ and no move takes an item behind $i_j$ except a move of $i_j$ itself. So $i_j$ is at position $t(j) + 1$. For a first access, its position is at most $n \le t(j) + 1$.

**Amortized cost of one access.** By the Access Lemma with $r(t) = \lg W$ and $r(x) \ge \lg w(x) \ge \lg (t(j) + 1)^{-2}$, the splay of access $j$ has amortized cost at most
$$3\bigl(\lg W + 2 \lg(t(j) + 1)\bigr) + 1.$$

**The change of weights does not increase $\Phi$.** After the splay, $i_j$ is the root. The move to the front gives $i_j$ the weight 1 and moves each item that was in front of it one place back, which decreases its weight; all other weights stay. The root's rank is $\lg W$ before and after. Each other node $y$ has $i_j$ outside its subtree, so $s(y)$ is a sum of weights that did not increase. So $\Phi$ does not increase.

**Initial and final potential.** For each node, $\lg (1/n^2) \le r(x) \le \lg W$, so $\Phi_0 - \Phi_m \le n(\lg W + 2 \lg n)$.

**Sum.** An access to a node at depth $d$ visits $d + 1$ nodes and makes $d$ rotations, so its cost is at most $\max(d, 1) + 1$. Summing the amortized costs and adding the potential drop:
$$\text{total cost} \le \sum_{j=1}^{m}\bigl(3 \lg W + 6 \lg(t(j) + 1) + 1 + 1\bigr) + n \lg W + 2 n \lg n. \qquad \blacksquare$$

## Consequences

- **Static optimality.** Group the accesses by item. For an item with $q$ accesses in a sequence of length $m$, the sum of $\lg(t(j) + 1)$ over its accesses is at most about $q \lg(m/q)$, by concavity of $\lg$ and because the gaps between its accesses add up to at most $m$. So the working set bound implies the [static optimality theorem](/static-optimality-theorem/) up to the constants.
- **Small working sets.** If each access goes to one of $k$ items that are used in turn, then after the first access to each, $t(j) \le k - 1$, and each access costs $O(\log k)$ amortized, independent of $n$.
- **Example.** In a splay tree of $n = 1024$ keys built in random order, 8000 accesses that cycle through 8 keys chosen at random cost 35083 nodes visited in total. After the first 80 accesses, the average cost was 4.375 nodes and the largest cost 5 nodes, while a balanced tree of 1024 keys has paths of about 10 nodes. Here $t(j) = 7$ for the late accesses, so the theorem gives at most $6 \lg 8 + 4.16 \approx 22$ amortized.
- **Caching view.** A splay tree behaves like an LRU cache with a logarithmic cost: the recently used items sit near the root, and the cost grows with the logarithm of the time since last use, measured in distinct items.

## Tightness

- **The logarithm is necessary.** On a sequence that cycles through $k$ items with equal frequencies, each static BST costs at least $\lg k / \lg 3$ per access on average, by the entropy bound in the proof of the [static optimality theorem](/static-optimality-theorem/), while $t(j) = k - 1$. So a bound in terms of $t(j)$ alone cannot drop the logarithm for static trees.
- **The additive terms.** The term $2 n \lg n$ pays for the initial tree, which can be a chain, and the term $O(1)$ per access pays for accesses to the root. Neither can be removed: a single access to the deepest node of a chain costs $n$.
- **Amortized, not per access.** One access can cost $\Theta(n)$ even when $t(j)$ is small, if earlier accesses left the tree badly shaped; the bound holds only for the total.
- **Not the strongest bound.** The working set bound does not imply the dynamic finger bound, and sequences such as sequential access cost $O(m)$ in a splay tree but have $t(j) = n - 1$ for each access after the first round. Iacono's unified bound and the [dynamic optimality conjecture](/dynamic-optimality-conjecture/) are stronger statements.

## History

Sleator and Tarjan stated and proved the working set theorem in 1985 as Theorem 4 of the paper that introduced splay trees. The proof by move-to-front weights $1/k^2$ is theirs. The bound has become one of the standard measures of how well a self-adjusting search structure adapts to an access sequence.

## References
