---
tag: 71EN86
kind: algorithm
slug: tarjan-offline-lca
name: Tarjan's offline LCA algorithm
aliases:
- union-find LCA
area: graphs/tree-algorithms
level: advanced
summary: Answer a batch of LCA queries offline in near-linear time using DFS and union-find.
solves: [lowest-common-ancestor]
model: word-ram
complexity:
  vars: {n: the number of vertices, q: the number of queries, α: the inverse Ackermann function}
  time: {worst: O((n + q) α(n)), average: O((n + q) α(n)), best: Θ(n + q)}
  space: {extra: Θ(n + q)}
properties: {deterministic: true, online: false, recursive: false}
prereqs: [lowest-common-ancestor, disjoint-set-forest, depth-first-search, postorder-traversal]
see_also: [lca-binary-lifting, euler-tour-lca, rmq-lca-equivalence, static-tree-set-union, gabow-tarjan-union-find, offline-query-processing, inverse-ackermann-function, virtual-tree]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 21 (Data Structures for Disjoint Sets), Problem 21-3 (Tarjan's off-line least-common-ancestors algorithm)
  - paper: doi:10.1145/322154.322161
    title: Robert E. Tarjan, Applications of path compression on balanced trees, Journal of the ACM 26(4), 690 to 715 (1979)
    locator: the off-line least common ancestors problem, solved with path compression during a depth-first search
  - paper: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, On finding lowest common ancestors in trees, SIAM Journal on Computing 5(1), 115 to 132 (1976)
    locator: the off-line version of the problem and its solution with set union
  - paper: Harold N. Gabow and Robert E. Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2), 209 to 221 (1985)
    locator: the static tree set union and its use for off-line least common ancestors in linear time
---

Tarjan's offline LCA algorithm answers a batch of $q$ [lowest common ancestor](/lowest-common-ancestor/) queries on a rooted tree with $n$ vertices in one depth-first search. When a vertex is finished, the algorithm merges it into the set of its parent in a [disjoint-set forest](/disjoint-set-forest/), and each set remembers the lowest vertex of the search path above it. A query $(u, v)$ is answered when the second of its two vertices is finished: the answer is the vertex remembered by the set of the first one. With union by rank and path compression, the time is $O((n + q)\,\alpha(n))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). All queries must be known in advance, so the method is offline.

## In plain words

You have a family tree and a list of questions: for two people, who is their closest shared ancestor? Walk the tree in depth-first order, and finish a person when you are done with all of their descendants.

Keep groups of finished people. When a person is finished, their group joins the group of their parent, and the joined group is labelled with the parent's name. So at any moment, the label of a finished person's group is the nearest of their ancestors that the walk has not yet finished.

Now take a question about two people. When the second of them is finished, look up the group of the first one. Its label is the answer: the walk is still inside that ancestor, which is the point where the paths to the two people split.

## The problem

The input is a tree with the vertices $0, \ldots, n-1$, $n \ge 1$, given as $n - 1$ edges, a root $r$, and a list of $q$ queries $(u_i, v_i)$. The tree is rooted at $r$ and not weighted. The output, for each $i$, is $\mathrm{lca}(u_i, v_i)$, the deepest vertex that is an ancestor of both $u_i$ and $v_i$, where each vertex is an ancestor of itself. The queries are all given before the work starts. This is the offline form of the [lowest common ancestor](/lowest-common-ancestor/) problem.

## The algorithm

The [disjoint-set forest](/disjoint-set-forest/) has the operations FIND and UNION with union by rank and path compression. Each set has a label $\mathit{anc}$, stored at its representative. A vertex is *done* when the search has left it for good.

```pseudo id=main
TARJAN-OFFLINE-LCA(adj, r, Q)          ▷ Q: the queries (u_i, v_i)
L1  for each vertex v do MAKE-SET(v); anc[v] ← v; done[v] ← false
L2  for each query i = (u, v) do add (v, i) to qs[u]; add (u, i) to qs[v]
L3  S ← a stack holding the pair (r, −1)
L4  while S is not empty do
L5      (v, p) ← the top of S             ▷ p is the parent of v, or −1
L6      if v has a neighbour c ≠ p not yet taken then push (c, v) on S
L7      else
L8          pop S; done[v] ← true
L9          for each (w, i) in qs[v] with done[w] do ans[i] ← anc[FIND(w)]
L10         if p ≠ −1 then UNION(p, v); anc[FIND(p)] ← p
L11 return ans
```

The stack holds the path from $r$ to the current vertex, so the vertices on it are exactly the vertices that are started and not done. Line L8 finishes the vertices in [postorder](/postorder-traversal/). Line L9 answers the queries of $v$ whose other vertex is already done; this includes a query $(v, v)$, since $v$ is marked done first. Line L10 merges the set of $v$, which by then holds the whole subtree of $v$, into the set of its parent, and labels the result with the parent. A query with $u \ne v$ is answered once, at the second of its two vertices to finish.

## Example

Take the tree with the edges $01, 02, 13, 14, 25, 46, 47$, rooted at $0$, with the neighbours of each vertex in increasing order. The vertices finish in the order $3, 6, 7, 4, 1, 5, 2, 0$. The queries are $Q_0 = (6, 3)$, $Q_1 = (7, 5)$, $Q_2 = (6, 7)$, $Q_3 = (4, 6)$, $Q_4 = (2, 2)$ and $Q_5 = (3, 0)$.

```
          0
        /   \
       1     2
      / \     \
     3   4     5
        / \
       6   7
```

| finished | answers at L9 | sets of done vertices after L10, with labels |
|---|---|---|
| 3 | none | $\{1, 3\}$: 1 |
| 6 | $Q_0$: $\mathit{anc}$ of the set of 3 is $1$ | $\{1, 3\}$: 1, $\{4, 6\}$: 4 |
| 7 | $Q_2$: set of 6, label $4$ | $\{1, 3\}$: 1, $\{4, 6, 7\}$: 4 |
| 4 | $Q_3$: set of 6, label $4$ | $\{1, 3, 4, 6, 7\}$: 1 |
| 1 | none | $\{0, 1, 3, 4, 6, 7\}$: 0 |
| 5 | $Q_1$: set of 7, label $0$ | $\{0, 1, 3, 4, 6, 7\}$: 0, $\{2, 5\}$: 2 |
| 2 | $Q_4$: set of 2, label $2$ | $\{0, \ldots, 7\}$: 0 |
| 0 | $Q_5$: set of 3, label $0$ | no change (root) |

The answers are $1, 0, 4, 4, 2, 0$. The sets contain $0$, $1$ and $4$ before these are done, because UNION$(p, v)$ also puts the parent $p$ in the set; the label stays $p$ until $p$ itself is done.

The small cases: on a single vertex, the only query $(0, 0)$ gives $0$. On the path $0, 1, \ldots, n-1$ rooted at $0$, $\mathrm{lca}(u, v) = \min(u, v)$, and the stack grows to $n$ entries, which an explicit stack handles for $n = 10^5$. On the star rooted at its centre $0$, the answer is $0$ for two different vertices.

## Correctness

The full proof is in the [proof page](proofs/correctness). In short: at each moment, for each done vertex $w$, the set of $w$ is labelled with the lowest ancestor of $w$ that is on the stack, or with $v$ itself while line L9 runs for $v$ and $w$ is in the subtree of $v$. When line L9 runs at $v$ for a done $w$, the lowest common ancestor of $v$ and $w$ is exactly that vertex: either $w$ is in the subtree of $v$, and the answer is $v$, or the paths from the root to $v$ and to $w$ split at the lowest vertex of the stack that is an ancestor of $w$.

## Complexity

The cost is in the [word RAM](/word-ram/) model with adjacency lists.

- The search pushes and pops each vertex once and reads each adjacency list once, $O(n)$ steps, by the [tree edge count](/tree-edge-count/).
- Line L2 stores each query twice, and line L9 reads each stored entry once, so there are at most $2q$ FIND operations there, plus $2(n - 1)$ FIND operations in line L10 and $n - 1$ UNION operations.
- With union by rank and path compression, $m$ operations on $n$ elements take $O(m\,\alpha(n))$ time. Here $m = O(n + q)$.

So the time is $O((n + q)\,\alpha(n))$ in the worst case, and the extra space is $\Theta(n + q)$ for the forest, the labels, the query lists and the stack. Since $\alpha(n) \le 4$ for every practical $n$, the time is linear in practice.

## Properties

- **Offline.** All queries must be known before the search. The answers come in the order in which the vertices finish, not the order of the queries, and are stored by index.
- **Rooted.** The answer depends on the root $r$. The same tree with another root gives other answers.
- **No preprocessing structure is kept.** After the search the union-find forest is useless for new queries, unlike [binary lifting](/lca-binary-lifting/) or the [Euler tour method](/euler-tour-lca/).
- **Not recursive.** The explicit stack of line L3 keeps the depth of the Python call stack constant, which matters on a path of $10^5$ vertices.

## Variants and improvements

- **Linear time.** The unions follow the fixed tree, so they form a [static tree set union](/static-tree-set-union/). Gabow and Tarjan solve it in $O(n + q)$ time on a word RAM with [microsets](/gabow-tarjan-union-find/), which makes the offline problem linear.
- **Recursive form.** The textbook form is a recursive procedure LCA$(u)$ that, after the call on each child $v$, does UNION$(u, v)$ and sets the label to $u$, then marks $u$ and answers the queries of $u$. It is the same algorithm, with the call stack in place of $S$.
- **Distances.** With the depth of each vertex, $d(u, v) = \mathrm{depth}(u) + \mathrm{depth}(v) - 2\,\mathrm{depth}(\mathrm{lca}(u, v))$, so the same pass answers distance queries, and path sums with prefix sums from the root.
- **Online alternatives.** If the queries arrive one by one, use [binary lifting](/lca-binary-lifting/) with $O(n \log n)$ preprocessing and $O(\log n)$ per query, or the [Euler tour with range minimum queries](/euler-tour-lca/) with $O(1)$ per query, see [RMQ and LCA](/rmq-lca-equivalence/).

## When to use it

Use it when the tree and all queries are known at once, as in many [offline query](/offline-query-processing/) settings: path queries computed in one batch, building a [virtual tree](/virtual-tree/) for a fixed set of vertices, or many distances in a fixed tree. It needs only a union-find structure and a stack, and its memory is linear in $n + q$. When queries arrive online or the tree is queried many times, an online structure is better.

## Pitfalls

- **Setting the label on the wrong set.** After UNION$(p, v)$, the representative can be $v$'s old representative. The label must be written at FIND$(p)$ after the union, not at $p$.
- **Answering too early.** Line L9 must test that the other vertex is done. If it answers when the other vertex is only started, the label can be a vertex below the true answer.
- **Queries $(v, v)$.** Mark $v$ done before line L9, or the query is never answered.
- **Deep recursion.** The recursive form needs a call stack of depth $n$ on a path. In Python, use an explicit stack as above.
- **Forgetting path compression or union by rank.** Without them, a path can make FIND take $\Theta(n)$ time, and the total becomes $\Theta(nq)$.

## Implementations

## History

Aho, Hopcroft and Ullman studied the lowest common ancestor problem in 1976 and solved the offline form with set union. Tarjan, in his 1979 paper on path compression on balanced trees, gave the form with a depth-first search and labelled sets that is now called by his name, with the bound $O((n + q)\,\alpha(n))$. Gabow and Tarjan made it linear in 1985 by a special union-find structure for unions that follow a known tree. The form in the problem section of the disjoint-set chapter of Cormen, Leiserson, Rivest and Stein spread the algorithm as a classic exercise.

## References
