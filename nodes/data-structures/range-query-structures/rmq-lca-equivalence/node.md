---
tag: Y3ZV50
kind: theorem
slug: rmq-lca-equivalence
name: RMQ-LCA equivalence
aliases:
- RMQ and LCA reduction
area: data-structures/range-query-structures
level: advanced
summary: Range minimum and lowest common ancestor queries reduce to each other up to linear overhead.
prereqs: [range-minimum-query, lowest-common-ancestor, cartesian-tree, euler-tour-technique]
see_also: [bender-farach-colton-rmq, fischer-heun-rmq, euler-tour-lca, monotonic-stack, sparse-table, lcp-array, catalan-numbers, tarjan-offline-lca]
sources:
  - paper: "Michael A. Bender and Martin Farach-Colton, The LCA problem revisited, LATIN 2000: Theoretical Informatics, Lecture Notes in Computer Science 1776, Springer, 2000"
    locator: the reduction from LCA to plus-minus-one RMQ by the Euler tour, the reduction from RMQ to LCA by the Cartesian tree, and the linear-time plus-minus-one RMQ
  - paper: "Harold N. Gabow, Jon L. Bentley and Robert E. Tarjan, Scaling and related techniques for geometry problems, Proceedings of the 16th Annual ACM Symposium on Theory of Computing (STOC 1984), 135-143"
    locator: the Cartesian tree and the reduction of range minimum to nearest common ancestors
  - paper: doi:10.1145/358841.358852
    title: "Jean Vuillemin, A unifying look at data structures, Communications of the ACM 23(4) (1980), 229-239"
    locator: the definition of the Cartesian tree
  - paper: "Dov Harel and Robert E. Tarjan, Fast algorithms for finding nearest common ancestors, SIAM Journal on Computing 13(2) (1984), 338-355"
    locator: the linear-time preprocessing and constant-time query for nearest common ancestors
---

The [range minimum query](/range-minimum-query/) problem and the [lowest common ancestor](/lowest-common-ancestor/) problem reduce to each other in linear time, with $O(1)$ extra time per query. From an array, the [Cartesian tree](/cartesian-tree/) gives a tree in which the leftmost minimum of $A[l \ldots r]$ is the lowest common ancestor of the nodes $l$ and $r$. From a tree, the [Euler tour](/euler-tour-technique/) gives an array of depths in which the lowest common ancestor of two nodes is the item of least depth between their first visits. The second array has the special form in which adjacent items differ by exactly 1, so general RMQ reduces to this easy special case, which is the route of the [Bender-Farach-Colton](/bender-farach-colton-rmq/) structure to $O(n)$ preprocessing and $O(1)$ query time.

## Statement

For an array $A[0 \ldots n-1]$ over a total order, let $\mathrm{RMQ}_A(l, r)$ be the leftmost index of a minimum of $A[l \ldots r]$. For a rooted tree $T$, let $\mathrm{LCA}_T(u, v)$ be the deepest node that is an ancestor of both $u$ and $v$, where each node is an ancestor of itself.

The *Cartesian tree* $C(A)$ is the binary tree on the nodes $0, \ldots, n - 1$ defined by recursion: if $n = 0$ it is empty; otherwise its root is $m = \mathrm{RMQ}_A(0, n - 1)$, its left subtree is the Cartesian tree of $A[0 \ldots m - 1]$, and its right subtree is the Cartesian tree of $A[m + 1 \ldots n - 1]$, with the indices kept.

The *Euler tour* of a rooted tree $T$ with $n$ nodes is the sequence $E[0 \ldots 2n - 2]$ written by a [depth-first search](/depth-first-search/) that writes the current node when it enters it and again each time it comes back to it from a child. Let $D[i]$ be the depth of $E[i]$, and let $\mathrm{first}(u)$ be the least $i$ with $E[i] = u$.

**Theorem.**

1. **RMQ to LCA.** $C(A)$ can be built in $O(n)$ time, and $\mathrm{RMQ}_A(l, r) = \mathrm{LCA}_{C(A)}(l, r)$ for all $0 \le l \le r \le n - 1$.
2. **LCA to $\pm 1$ RMQ.** $E$ and $D$ can be built in $O(n)$ time, $|D[i + 1] - D[i]| = 1$ for all $i$, and for any nodes $u, v$ with $\mathrm{first}(u) \le \mathrm{first}(v)$, the node $E[i]$ is $\mathrm{LCA}_T(u, v)$ for every index $i$ of a minimum of $D[\mathrm{first}(u) \ldots \mathrm{first}(v)]$.

So a structure for RMQ with preprocessing $p(n)$ and query time $q(n)$ gives one for LCA with $O(n) + p(2n - 1)$ and $q(2n - 1) + O(1)$, and the reverse holds with $O(n) + p(n)$ and $q(n) + O(1)$. Both directions together reduce general RMQ to $\pm 1$ RMQ on $2n - 1$ items.

## In plain words

Take a list of numbers. Put the smallest number at the top of a family tree. The numbers to its left form its left branch, built the same way, and the numbers to its right form its right branch. Now the smallest number of any stretch of the list is the closest shared ancestor, in this tree, of the two ends of the stretch.

The other way round, walk around a tree and write down each place you stand on, and how deep it is, every time you arrive there. Between your first visits to two places, the highest point you pass is their closest shared ancestor. So the question on trees becomes a "lowest number in a stretch" question, on a list in which each number is one more or one less than the one before it.

## Proof

**Part 1.** We first show a property of $C(A)$ by [induction](/induction/) on $n$.

*Claim.* For each node $w$, the indices of the subtree of $w$ form a contiguous range $[a_w, b_w]$, the left subtree of $w$ holds exactly $[a_w, w - 1]$, the right subtree holds exactly $[w + 1, b_w]$, and $w = \mathrm{RMQ}_A(a_w, b_w)$.

For the root $m$, the subtree is $[0, n - 1]$ and $m = \mathrm{RMQ}_A(0, n - 1)$ by definition. Its left and right subtrees are the Cartesian trees of $A[0 \ldots m - 1]$ and of $A[m + 1 \ldots n - 1]$, which are shorter, so by the hypothesis the claim holds inside them, and their index sets are $[0, m - 1]$ and $[m + 1, n - 1]$. This proves the claim.

Now let $0 \le l \le r \le n - 1$ and $w = \mathrm{LCA}(l, r)$. The subtree of $w$ holds $l$ and $r$, so $a_w \le l \le r \le b_w$. If $l$ and $r$ were both in the left subtree of $w$, the root of that subtree would be a deeper common ancestor, and the same holds for the right subtree. So $l$ is $w$ or in its left subtree, and $r$ is $w$ or in its right subtree, which gives $l \le w \le r$ by the claim. Since $w$ is the leftmost minimum of $[a_w, b_w] \supseteq [l, r]$, we get $A[w] \le A[j]$ for each $j \in [l, r]$, and $A[w] < A[j]$ for each $j \in [l, w - 1]$. So $w$ is the leftmost minimum of $[l, r]$, that is, $w = \mathrm{RMQ}_A(l, r)$.

*Linear-time build.* Scan $i = 0, 1, \ldots, n - 1$ with a stack of indices, the right spine of the tree built so far. At step $i$, pop every index $j$ with $A[j] > A[i]$; the last popped index becomes the left child of $i$; if the stack is not empty, $i$ becomes the right child of its top; then push $i$. After step $i$, the tree is $C(A[0 \ldots i])$ and the stack holds its right spine from the root down. This holds for $i = 0$. For the step to $i$: the new item is the last index, so in $C(A[0 \ldots i])$ it lies on the right spine. Its ancestors on the spine are exactly the spine nodes $j$ with $A[j] \le A[i]$, because a spine node $j$ is the leftmost minimum of $[j, i - 1]$ and stays the leftmost minimum of $[j, i]$ exactly when $A[j] \le A[i]$, the strict test keeping an equal earlier item above. The popped part of the spine, with its left subtrees, is all of $A[j' \ldots i - 1]$ for the first popped $j'$, and it becomes the left subtree of $i$ unchanged. Each index is pushed once and popped at most once, so the build takes $O(n)$ time. This is the [monotonic stack](/monotonic-stack/) method.

**Part 2.** The search writes one entry when it enters a node and one when it returns over each of the $n - 1$ edges, so $E$ has $n + (n - 1) = 2n - 1$ entries and takes $O(n)$ time. Two adjacent entries are a node and its child, in one order or the other, so their depths differ by exactly 1.

The search enters a node $u$ at $\mathrm{first}(u)$, writes only nodes of the subtree of $u$ until it leaves $u$ for the last time at an index $\mathrm{last}(u)$, and never comes back. So the entries $E[\mathrm{first}(u) \ldots \mathrm{last}(u)]$ are exactly the visits inside the subtree of $u$.

Let $u, v$ have $\mathrm{first}(u) \le \mathrm{first}(v)$ and let $w = \mathrm{LCA}(u, v)$. Both $u$ and $v$ lie in the subtree of $w$, so $\mathrm{first}(w) \le \mathrm{first}(u) \le \mathrm{first}(v) \le \mathrm{last}(w)$, and every entry of $E[\mathrm{first}(u) \ldots \mathrm{first}(v)]$ is a node of the subtree of $w$, of depth at least $\mathrm{depth}(w)$, with equality only for $w$ itself. It remains to show that $w$ occurs in this range. If $u = w$, then $E[\mathrm{first}(u)] = w$. Otherwise $u \ne w$, and $v \ne w$ as well, since $\mathrm{first}(w) < \mathrm{first}(u) \le \mathrm{first}(v)$ when $w$ is a proper ancestor of $u$. Then $u$ and $v$ lie in the subtrees of two different children $c_1$ and $c_2$ of $w$, since a common child would be a deeper common ancestor. Because $\mathrm{first}(u) < \mathrm{first}(v)$, the search visits $c_1$ before $c_2$. After it returns from $c_1$, at an index after $\mathrm{first}(u)$, it writes $w$, and only later enters $c_2$ and then $v$. So $w$ occurs in the range, the least depth in $D[\mathrm{first}(u) \ldots \mathrm{first}(v)]$ is $\mathrm{depth}(w)$, and every index of a minimum holds $w$.

**The cost bounds.** For LCA, build $E$, $D$ and $\mathrm{first}$ in $O(n)$ time and an RMQ structure on $D$, of length $2n - 1$; a query is two lookups of $\mathrm{first}$, one RMQ and one lookup in $E$. For RMQ, build $C(A)$ in $O(n)$ time and an LCA structure on it; by Part 1 a query is one LCA query. $\blacksquare$

### A worked example

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$. The stack build gives these spines after each step: $[0]$, $[1]$, $[1, 2]$, $[3]$, $[3, 4]$, $[3, 5]$, $[3, 5, 6]$, $[3, 5, 7]$. The tree has the root 3; node 3 has the children 1 and 5; node 1 has the children 0 and 2; node 5 has the children 4 and 7; node 7 has the left child 6.

The query $\mathrm{RMQ}(4, 7)$ asks for the minimum of 9, 3, 7, 4. Node 4 is the left child of 5 and node 7 its right child, so $\mathrm{LCA}(4, 7) = 5$, and $A[5] = 3$ is the minimum.

The Euler tour of this tree, left child first, is

$$E = 3, 1, 0, 1, 2, 1, 3, 5, 4, 5, 7, 6, 7, 5, 3,$$

with the depths $D = 0, 1, 2, 1, 2, 1, 0, 1, 2, 1, 2, 3, 2, 1, 0$, 15 entries for 8 nodes. Then $\mathrm{first}(4) = 8$ and $\mathrm{first}(6) = 11$, and the least depth in $D[8 \ldots 11] = 2, 1, 2, 3$ is at index 9, where $E[9] = 5$. So $\mathrm{LCA}(4, 6) = 5$, which is also $\mathrm{RMQ}_A(4, 6)$, the minimum 3 of 9, 3, 7.

## Consequences

- **Optimal static RMQ.** General RMQ reduces to LCA on the Cartesian tree, and LCA reduces to $\pm 1$ RMQ on $2n - 1$ depths. The $\pm 1$ case has only $2^{b - 1}$ different blocks of length $b$ up to an additive shift, so with $b = \frac12 \lg n$ a table of all blocks, a [sparse table](/sparse-table/) over the block minimums and the reduction give $\langle O(n), O(1) \rangle$; this is the [Bender-Farach-Colton RMQ](/bender-farach-colton-rmq/).
- **Optimal static LCA.** In the same way, LCA has a $\langle O(n), O(1) \rangle$ solution, the result of Harel and Tarjan with a simpler proof; see [Euler tour LCA](/euler-tour-lca/).
- **Encodings.** By Part 1, the answers of all index queries depend only on the shape of $C(A)$. Two arrays have the same answers exactly when their Cartesian trees have the same shape, so there are $C_n$ answer functions, the $n$-th [Catalan number](/catalan-numbers/). This is the base of the $2n + o(n)$ bit structure of [Fischer and Heun](/fischer-heun-rmq/).
- **String queries.** With a [suffix array](/suffix-array/) and its [LCP array](/lcp-array/), the longest common prefix of two suffixes is a range minimum, so it is also an LCA query in the suffix tree, and both views give $O(1)$ time.
- **Offline queries.** Offline RMQ can use [Tarjan's offline LCA](/tarjan-offline-lca/) on the Cartesian tree.

## Tightness

- **Linear overhead is needed.** Each reduction reads its whole input, so $\Theta(n)$ is the least possible cost of building it. The query overhead is $O(1)$, so the two problems have the same complexity up to constant factors in both measures.
- **The size grows by less than a factor of 2.** The array of the second reduction has $2n - 1$ items, and this is necessary for the Euler tour, since it must return over each of the $n - 1$ edges.
- **The leftmost rule matters.** With repeated values and a Cartesian tree whose root is some other minimum, Part 1 still returns an index of a minimum, but not always the leftmost one. For $A = [1, 1]$ with the root 1, the query $(0, 1)$ returns 1.
- **The $\pm 1$ case is not easier asymptotically.** General RMQ reduces to $\pm 1$ RMQ, and $\pm 1$ RMQ is a special case of general RMQ, so all three problems are equivalent up to linear overhead.

## History

Vuillemin defined the Cartesian tree in 1980. Gabow, Bentley and Tarjan used it in 1984 to reduce range minimum queries to nearest common ancestor queries, and Harel and Tarjan gave the first LCA structure with linear preprocessing and constant query time in the same year. The reduction of LCA to the $\pm 1$ case through the Euler tour, together with a simple table method for that case, became widely known through Bender and Farach-Colton in 2000, who presented both directions as one simple route to optimal RMQ and LCA.

## References
