---
tag: Q53SNA
kind: data-structure
slug: virtual-tree
name: Virtual tree
area: graphs/tree-algorithms
level: advanced
summary: A compressed tree built on a chosen set of key vertices and their pairwise lowest common ancestors, so queries touch only O(k) nodes.
model: word-ram
complexity:
  vars: {n: the number of vertices of the tree, k: the number of key vertices}
  time: {preprocess: Θ(n log n), build: O(k (log k + log n))}
  space: {extra: Θ(n log n), per_tree: Θ(k)}
prereqs: [lowest-common-ancestor, preorder-traversal, rooted-tree, lca-binary-lifting]
see_also: [tree-dynamic-programming, euler-tour-lca, tarjan-offline-lca, steiner-tree-problem, centroid-decomposition, subtree-sizes, bender-farach-colton-rmq, tree-path-queries]
sources:
  - url: https://oi-wiki.org/graph/virtual-tree/
    title: OI Wiki, Virtual tree
    locator: the construction by sorting the key vertices by DFS order, adding the LCAs of adjacent keys, and linking with a stack, and its use for tree dynamic programming over many query sets
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 22.3 (Depth-first search), the parenthesis theorem on discovery and finishing times, which gives the interval form of ancestry used here
---

A virtual tree, also called an auxiliary tree, is a small tree that keeps only a chosen set $K$ of $k$ key vertices of a large rooted tree, together with the [lowest common ancestors](/lowest-common-ancestor/) of pairs of them. Each of its edges stands for a path of the original tree, and its length is the number of edges of that path. It has at most $2k - 1$ vertices, and it is built in $O(k (\log k + \log n))$ time after a single preprocessing of the tree: sort the keys by [preorder](/preorder-traversal/) position, add the LCA of each adjacent pair, sort again, and link each vertex to the LCA of it and its predecessor. A [tree dynamic program](/tree-dynamic-programming/) that only cares about the keys can then run on the virtual tree, so many query sets with a total of $\sum k$ keys cost $O(\sum k \log n)$ time and not $O(n)$ per set.

## In plain words

You have a huge family tree, and today's question only concerns a few people. Most of the tree is irrelevant: long chains of ancestors that just lead from one person to another, and whole branches with nobody of interest.

The virtual tree throws all that away. It keeps the people you care about, and also each point where the lines of two of them meet, because those meeting points decide how the people relate. Each long chain becomes a single link, labelled with its length.

To build it, list the people in the order of a walk through the tree. Each neighbour pair in that list adds its meeting point. With these added, each person's link goes up to the meeting point of that person and the one just before in the list.

## The abstract type

A virtual tree structure is built once for a fixed rooted tree $T$ and then answers:

- $\mathrm{build}(K)$ for a non-empty set $K$ of vertices: return the virtual tree $V(K)$, as its vertices and, for each vertex but its root, the virtual parent and the length of the virtual edge.
- $\mathrm{lca}(u, v)$, which the build needs and which callers often use too.

Let $\overline{K}$ be $K$ together with $\mathrm{lca}(x, y)$ for all $x, y \in K$. The *virtual tree* $V(K)$ has the vertex set $\overline{K}$, and the parent of $v \in \overline{K}$ is the nearest proper ancestor of $v$ that is in $\overline{K}$; the vertex $\mathrm{lca}(K)$ has no parent and is the root. The length of the edge from $v$ to its parent $u$ is $\mathrm{depth}(v) - \mathrm{depth}(u)$. So the ancestor relation of $T$ restricted to $\overline{K}$ is the ancestor relation of $V(K)$, and the distance in $T$ between two vertices of $\overline{K}$ is their distance in $V(K)$ with these lengths.

## Representation

The tree $T$ has the vertices $0, \ldots, n-1$, is rooted at $r$, and is not weighted; with edge weights, replace the depth by the weighted depth for the lengths. Preprocessing stores four things:

- $\mathrm{tin}(v)$, the position of $v$ in a [preorder](/preorder-traversal/) from $r$;
- $\mathrm{depth}(v)$;
- a table for [LCA queries](/lowest-common-ancestor/), here [binary lifting](/lca-binary-lifting/), with $\lceil \log_2 n \rceil$ ancestors per vertex;
- nothing more for the build: each virtual tree is returned as a list of its vertices in preorder and an array of parent positions.

**Ancestry by intervals.** The subtree of $v$ is the block of preorder positions from $\mathrm{tin}(v)$ to $\mathrm{tin}(v) + s(v) - 1$, where $s(v)$ is the [subtree size](/subtree-sizes/). So if $u$ is an ancestor of $v$, then $\mathrm{tin}(u) \le \mathrm{tin}(v)$; and if $u$ is an ancestor of $w$ and $\mathrm{tin}(u) \le \mathrm{tin}(v) \le \mathrm{tin}(w)$, then $u$ is an ancestor of $v$.

## Operations

```pseudo id=main
BUILD-VIRTUAL-TREE(K)                    ▷ tin, depth and lca from preprocessing
L1  B ← K sorted by tin, without repeats; b ← |B|
L2  A ← a copy of B
L3  for i ← 1 to b − 1 do append lca(B[i − 1], B[i]) to A
L4  A ← A sorted by tin, without repeats; m ← |A|
L5  par[0] ← NIL                          ▷ A[0] = lca(K) is the root
L6  for i ← 1 to m − 1 do
L7      par[i] ← the position of lca(A[i − 1], A[i]) in A
L8  return A, par
```

Line L3 adds only $b - 1$ LCAs, of adjacent keys, and still gets all of $\overline{K}$: for keys sorted by preorder, the LCA of any two is the shallowest LCA of the adjacent pairs between them. Line L7 links each vertex to the LCA of it and the vertex just before it in preorder, which is its nearest proper ancestor in the set.

**Stack form.** A common equivalent build walks $B$ in order with a stack that holds the current root path of the virtual tree. For a new key $x$, let $\ell = \mathrm{lca}(\mathrm{top}, x)$; while the vertex below the top is at least as deep as $\ell$, link the top to the vertex below it and pop it. Then, if the top is not $\ell$, link the top to $\ell$, pop it and push $\ell$. Push $x$. At the end, link each vertex left on the stack to the one below it. It needs one sort and $k$ LCA queries.

## Example

Take the tree with the edges $01, 02, 13, 14, 25, 46, 47$, rooted at $0$. Its preorder is $0, 1, 3, 4, 6, 7, 2, 5$, so $\mathrm{tin} = [0, 1, 6, 2, 3, 7, 4, 5]$, and the depths are $[0, 1, 1, 2, 2, 2, 3, 3]$.

```
          0
        /   \
       1     2
      / \     \
     3   4     5
        / \
       6   7
```

Let $K = \{5, 3, 6\}$.

| step | result |
|---|---|
| L1, sort by tin | $B = 3, 6, 5$ (tin $2, 4, 7$) |
| L3, adjacent LCAs | $\mathrm{lca}(3, 6) = 1$, $\mathrm{lca}(6, 5) = 0$ |
| L4, sort again | $A = 0, 1, 3, 6, 5$ |
| L7, $i = 1$ | $\mathrm{lca}(0, 1) = 0$: parent of $1$ is $0$, length $1$ |
| L7, $i = 2$ | $\mathrm{lca}(1, 3) = 1$: parent of $3$ is $1$, length $1$ |
| L7, $i = 3$ | $\mathrm{lca}(3, 6) = 1$: parent of $6$ is $1$, length $2$ |
| L7, $i = 4$ | $\mathrm{lca}(6, 5) = 0$: parent of $5$ is $0$, length $2$ |

The virtual tree has $5 = 2 \cdot 3 - 1$ vertices: the root $0$ with the children $1$ and $5$, and $1$ with the children $3$ and $6$. The vertices $2$, $4$ and $7$ are gone; the edge $6$ to $1$ stands for the path $6, 4, 1$. The sum of the lengths, $6$, is the number of edges of the smallest subtree of $T$ that joins $3$, $6$ and $5$. For $K = \{6, 7\}$ the virtual tree is $4$ with the children $6$ and $7$.

The small cases: in a single vertex tree, $V(\{0\})$ is that vertex. On the path $0, 1, \ldots, n-1$ rooted at $0$, every LCA is a key, and $V(K)$ is the path of the keys in increasing order. On the star rooted at its centre $0$, two or more leaves give the centre with the leaves as its children, and a single key gives a tree with one vertex.

## Correctness

The full proof is in the [proof page](proofs/correctness). It uses two facts. First, if $x_1, \ldots, x_b$ are sorted by $\mathrm{tin}$, the LCA of $x_i$ and $x_j$ for $i < j$ is the shallowest of $\mathrm{lca}(x_t, x_{t+1})$ for $i \le t < j$, so the set $A$ of line L4 is $\overline{K}$, and $\overline{K}$ is closed under LCA. Second, in a set closed under LCA and sorted by $\mathrm{tin}$, the nearest proper ancestor of $A[i]$ in the set is $\mathrm{lca}(A[i-1], A[i])$: a deeper ancestor in the set would come before $A[i]$ and at or before $A[i-1]$ in preorder, and by the interval property it would also be an ancestor of $A[i-1]$.

**Size.** $|A| \le b + (b - 1) = 2b - 1 \le 2k - 1$, because line L3 adds $b - 1$ vertices.

## Complexity

- **Preprocessing.** The preorder and the depths take $\Theta(n)$ time with an explicit stack; the binary lifting table takes $\Theta(n \log n)$ time and space.
- **Build.** Lines L1 and L4 sort at most $2k - 1$ vertices, $O(k \log k)$ time. Lines L3 and L7 make at most $2k - 2$ LCA queries, $O(\log n)$ each with binary lifting. The total is $O(k (\log k + \log n))$, and the virtual tree takes $\Theta(k)$ space.
- **Faster LCA.** With [Euler tour LCA](/euler-tour-lca/) and a sparse table, each query takes $O(1)$ time, so the build takes $O(k \log k)$ time, or $O(k)$ when the keys come already sorted by preorder.

## Variants

- **Stack construction.** The form described under Operations, with one sort and $k$ LCA queries. It is often used in contest code.
- **Keeping the global root.** Some uses add $r$ to $K$, so that the virtual tree is always rooted at $r$. The bound becomes $2k + 1$ vertices.
- **Weighted trees.** With edge lengths, store the weighted depth, and each virtual edge gets the length of its path. To keep the minimum or maximum edge on a path, use binary lifting with path aggregates, as in [tree path queries](/tree-path-queries/).
- **Offline LCA.** When all key sets are known in advance, the LCA queries of all builds can be answered in one batch with [Tarjan's offline algorithm](/tarjan-offline-lca/).

## When to use it

Use a virtual tree when there are many query sets on one fixed tree, each set is small, and the answer for a set depends only on the paths between its vertices: the total length of the subtree that joins them (a [Steiner tree](/steiner-tree-problem/) in a tree), the cheapest set of edges to cut that separates the keys from the root, or a sum over the pairs of keys. If $\sum k$ over all sets is $S$, the total time is $O(n \log n + S \log n)$, while running the dynamic program on all of $T$ for each set costs $O(n)$ per set. For one set, or when the sets are large, work on $T$ directly.

## Pitfalls

- **Only the adjacent LCAs.** Adding the LCA of each adjacent pair is enough, but only when the keys are sorted by preorder. In any other order, needed LCAs can be missing.
- **Repeats.** Without the removal of repeats in line L4, a vertex appears twice and gets two parents. A key that is also an LCA, such as $1$ in $K = \{1, 3\}$, is the usual case.
- **The root.** $A[0]$ is $\mathrm{lca}(K)$, not $r$. A dynamic program that needs the global root must add it.
- **Cost per query.** Resetting arrays of size $n$ for each query set destroys the gain. Clear only the entries of the vertices of the virtual tree.
- **Deep recursion.** The preprocessing DFS and the dynamic program on the virtual tree should use explicit stacks or the preorder list, since a path of $10^5$ vertices overflows the Python call stack.

## Implementations

## History

The virtual tree is folklore of programming contests, also known as the auxiliary tree or the compressed tree. It rests on two older facts: the parenthesis structure of the discovery times of a [depth-first search](/depth-first-search/), as in Cormen, Leiserson, Rivest and Stein, and fast LCA queries. Contest editorials and OI Wiki describe the build by preorder sorting and adjacent LCAs, and its use for dynamic programming over many small query sets.

## References
