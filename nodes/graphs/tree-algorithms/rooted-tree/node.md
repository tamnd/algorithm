---
tag: Y1TMKB
kind: definition
slug: rooted-tree
name: Rooted tree
aliases:
- tree
area: graphs/tree-algorithms
level: intro
summary: A connected acyclic graph with a distinguished root, giving parent and child relations.
prereqs: [tree, connected-graph, acyclic-graph]
see_also: [tree-edge-count, arborescence, binary-tree, rooted-tree-representation, parent-pointer-tree, tree-rooting, tree-traversal, lowest-common-ancestor]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5 (Trees), the parts on free trees and on rooted and ordered trees (ancestor, descendant, parent, child, depth, height)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3 (Trees), the recursive definition of a tree, of an ordered tree and of a forest, and the terms level, degree and leaf
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.5 (Trees and forests), rooted trees and the tree-order
---

A rooted tree is a [tree](/tree/), that is, a [connected](/connected-graph/) [acyclic](/acyclic-graph/) undirected graph, with one vertex chosen as the *root*. The choice of the root gives each edge a direction, away from the root, and so defines the parent, the children, the ancestors, the descendants, the depth and the height of each vertex. Almost every tree algorithm on this site works on a rooted tree, and a free tree is rooted first, at a fixed vertex or at a vertex the algorithm chooses.

## Definition

Let $T = (V, E)$ be a tree with a finite, non-empty vertex set $V$, and let $r \in V$. The pair $(T, r)$ is a *rooted tree* with root $r$. In a tree, there is exactly one simple path between two vertices, so for each $v \in V$ there is one path $P(v)$ from $r$ to $v$. All terms below come from these paths.

- **Ancestor and descendant.** A vertex $u$ is an *ancestor* of $v$, and $v$ is a *descendant* of $u$, if $u$ lies on $P(v)$. Each vertex is an ancestor and a descendant of itself. A *proper* ancestor or descendant is one that is not equal to the vertex.
- **Parent and child.** For $v \ne r$, the *parent* $p(v)$ is the vertex just before $v$ on $P(v)$. Then $v$ is a *child* of $p(v)$. The root has no parent. Each edge $\{u, v\}$ of $T$ joins a vertex to its parent, because $u$ is on $P(v)$ or $v$ is on $P(u)$.
- **Leaf and internal vertex.** A vertex with no children is a *leaf*. A vertex with at least one child is *internal*. In the rooted sense, the *degree* of a vertex is its number of children. This differs from its degree in the graph by one for each vertex other than the root.
- **Siblings.** Two vertices with the same parent are *siblings*.
- **Depth and level.** The *depth* $d(v)$ is the number of edges of $P(v)$. So $d(r) = 0$, and $d(v) = d(p(v)) + 1$ for $v \ne r$. The vertices of depth $k$ form *level* $k$.
- **Height.** The *height* of $v$ is the number of edges of a longest path from $v$ down to a leaf. The height of the tree is the height of $r$, which is also the largest depth.
- **Subtree.** The *subtree* $T_v$ of $v$ is the tree on the descendants of $v$, rooted at $v$. Its number of vertices is the subtree size of $v$, which [one traversal computes for all vertices](/subtree-sizes/).
- **Ordered tree.** A rooted tree is *ordered* if the children of each vertex are in a fixed linear order: first child, second child, and so on. A [binary tree](/binary-tree/) is not only ordered: each child is a *left* or a *right* child, so a vertex with one child has two different possible shapes.

### Equivalent forms

Three descriptions give the same objects, up to the naming of the vertices.

1. **A tree with a chosen vertex**, as above.
2. **A parent function.** A map $p : V \setminus \{r\} \to V$ such that from each vertex, the sequence $v, p(v), p(p(v)), \ldots$ reaches $r$. The edges $\{v, p(v)\}$ form a tree with $|V| - 1$ edges. This is the [parent-pointer tree](/parent-pointer-tree/) representation.
3. **Knuth's recursive form.** A rooted tree is a vertex $r$ together with a finite (possibly empty) set of disjoint rooted trees, the subtrees of $r$, whose roots are the children of $r$. For an ordered tree, the set is a sequence.

Directing each edge from the parent to the child gives an [arborescence](/arborescence/): a directed graph in which the root has in-degree 0, each other vertex has in-degree 1, and each vertex can be reached from the root.

### Conventions on this site

The tree pages state three things about their input. *Rooted*: whether a root is given. *Weighted*: whether edges carry lengths; when they do not, the length of a path is its number of edges. *Numbering*: the vertices are $0, 1, \ldots, n-1$ unless the page says otherwise, the root is vertex $0$ when the input does not name it, and the tree comes as a list of $n - 1$ edges or as a parent array with $p(r) = -1$. A tree with $n$ vertices has $n - 1$ edges, by the [tree edge count](/tree-edge-count/).

## Examples and non-examples

Take the tree on $\{0, \ldots, 7\}$ with the edges $01, 02, 13, 14, 25, 46, 47$, rooted at $0$.

```
          0
        /   \
       1     2
      / \     \
     3   4     5
        / \
       6   7
```

- The parent array is $p = [-1, 0, 0, 1, 1, 2, 4, 4]$.
- The depths are $[0, 1, 1, 2, 2, 2, 3, 3]$, so the height of the tree is $3$.
- The leaves are $3, 5, 6, 7$. The internal vertices are $0, 1, 2, 4$.
- The ancestors of $7$ are $7, 4, 1, 0$. The subtree $T_1$ has the vertices $1, 3, 4, 6, 7$.
- The vertices $6$ and $7$ are siblings. The vertices $3$ and $4$ are siblings, and $3$ and $5$ are not, although they have the same depth.

The same tree rooted at $6$ has height $5$ (the path $6, 4, 1, 0, 2, 5$), and now $4$ is the parent of $1$. The edges do not change, but each relation that depends on the root does.

Three small cases show the extremes.

- **Single vertex.** $V = \{r\}$. The root is a leaf, its depth and height are $0$, and the parent function is empty.
- **Path.** The path $0, 1, \ldots, n-1$ rooted at $0$ has height $n - 1$ and one leaf. Rooted at its middle vertex $\lfloor (n-1)/2 \rfloor$, for $n \ge 3$, it has height $\lceil (n-1)/2 \rceil$ and two leaves.
- **Star.** The star with centre $0$ and leaves $1, \ldots, n-1$, for $n \ge 3$, rooted at $0$ has height $1$ and $n - 1$ leaves. Rooted at the leaf $1$, it has height $2$, the root has one child, and there are $n - 2$ leaves.

Non-examples:

- A graph with a cycle, such as the triangle on $\{0, 1, 2\}$ with root $0$. The vertex $2$ has two simple paths from $0$, so it has no well-defined parent.
- A disconnected acyclic graph. It is a *forest*. A rooted forest has one root in each component, and it is not a rooted tree.
- A directed acyclic graph in which a vertex has two incoming edges, such as $0 \to 2$ and $1 \to 2$. Each vertex of a rooted tree, other than the root, has exactly one parent.
- A free tree with no chosen root. It has a [centre](/tree-center/) and a [centroid](/centroid/), but no parent relation until a root is fixed. A free tree on $n$ vertices gives $n$ rooted trees, one for each choice of root, and some of these can be isomorphic.

## Related definitions

- [Tree](/tree/): the free tree and the abstract type with `parent` and `children`.
- [Arborescence](/arborescence/): the directed form, with each edge from parent to child.
- [Binary tree](/binary-tree/) and [complete binary tree](/complete-binary-tree/): ordered trees with at most two positional children.
- [Rooted tree representation](/rooted-tree-representation/), [parent-pointer tree](/parent-pointer-tree/) and [left-child right-sibling](/left-child-right-sibling/): ways to store a rooted tree.
- [Tree rooting](/tree-rooting/): how to turn a free tree, given by its edges, into a parent array.
- [Tree traversal](/tree-traversal/): the orders in which algorithms visit a rooted tree.
- [Lowest common ancestor](/lowest-common-ancestor/): the deepest common ancestor of two vertices.

## References
