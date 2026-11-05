---
tag: 4RNDJE
kind: definition
slug: nice-tree-decomposition
name: Nice tree decomposition
aliases:
- normalized tree decomposition
area: graphs/tree-algorithms
level: advanced
summary: Normalized tree decomposition with introduce, forget and join nodes, convenient for DP.
prereqs: [tree-decomposition, rooted-tree]
see_also: [tree-decomposition, path-decomposition, treewidth, dp-on-tree-decompositions, tree-decomposition-construction, independent-set-on-trees, binary-tree, postorder-traversal]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the definition of nice tree decompositions with leaf, introduce, forget and join nodes, the variant with introduce edge nodes, and the lemma that turns any tree decomposition into a nice one of the same width
  - paper: Ton Kloks, Treewidth, Computations and Approximations, Lecture Notes in Computer Science 842, Springer, 1994
    locator: the normalized form of tree decompositions with nodes of a few fixed kinds, used to make dynamic programming uniform
---

## Definition

Let $G = (V, E)$ be a graph and $(T, \{X_t\})$ a [tree decomposition](/tree-decomposition/) of $G$ whose tree $T$ is rooted at a node $r$. The decomposition is *nice* if $X_r = \emptyset$, $X_\ell = \emptyset$ for every leaf $\ell$ of $T$, and every other node $t$ is of one of three kinds:

- **Introduce node.** $t$ has one child $t'$, and $X_t = X_{t'} \cup \{v\}$ for a vertex $v \notin X_{t'}$. We say that $t$ introduces $v$.
- **Forget node.** $t$ has one child $t'$, and $X_t = X_{t'} \setminus \{w\}$ for a vertex $w \in X_{t'}$. We say that $t$ forgets $w$.
- **Join node.** $t$ has exactly two children $t_1$ and $t_2$, and $X_t = X_{t_1} = X_{t_2}$.

The leaves are called *leaf nodes*. The graph is not weighted, and the nodes of $T$ are numbered apart from the vertices $0, \ldots, n-1$ of $G$. A nice decomposition with no join node is a nice [path decomposition](/path-decomposition/).

Two consequences follow from the definition and the subtree condition. Each vertex $v$ is forgotten exactly once: the bags that hold $v$ form a subtree whose top node is not the root, since $X_r = \emptyset$, and the parent of that top node forgets $v$. A vertex $v$ can be introduced several times: every lowest node of the subtree of bags that hold $v$ is an introduce node of $v$, because its children, empty leaves or not, do not hold $v$. And if $G$ has $n$ vertices and a tree decomposition of width $k$, it has a nice one of width $k$ with $O(kn)$ nodes, which can be found in time polynomial in $k$ and linear in $n$ and in the size of the given decomposition: root it, merge bags that are subsets of a neighbour, put a chain of introduce or forget nodes on each edge to change one vertex at a time, and replace each node with $d \ge 2$ children by $d - 1$ join nodes with copies of its bag.

## Examples and non-examples

**A nice path decomposition.** The strip of triangles with the vertices $0, \ldots, 5$ and the edges $01, 02, 12, 13, 23, 24, 34, 35, 45$ has the path decomposition $\{0,1,2\}, \{1,2,3\}, \{2,3,4\}, \{3,4,5\}$ of width 2. Read from the leaf up to the root, a nice version is:

$$\emptyset \xrightarrow{+0} \{0\} \xrightarrow{+1} \{0,1\} \xrightarrow{+2} \{0,1,2\} \xrightarrow{-0} \{1,2\} \xrightarrow{+3} \{1,2,3\} \xrightarrow{-1} \{2,3\} \xrightarrow{+4} \{2,3,4\} \xrightarrow{-2} \{3,4\} \xrightarrow{+5} \{3,4,5\} \xrightarrow{-3} \{4,5\} \xrightarrow{-4} \{5\} \xrightarrow{-5} \emptyset$$

Here $+v$ is an introduce node and $-w$ a forget node. There are $1 + 6 + 6 = 13$ nodes: a nice path decomposition has $2n + 1$ nodes, since each vertex is introduced once and forgotten once. The width is still 2.

**A join node.** Take the star with centre $0$ and leaves $1$ and $2$. A nice decomposition of width 1, rooted at $r$:

- $r$: $\emptyset$, forgets $0$ from its child $j$;
- $j$: $\{0\}$, a join node with the children $a$ and $b$;
- $a$: $\{0\}$, forgets $1$ from $\{0, 1\}$, which introduces $1$ into $\{0\}$, which introduces $0$ into a leaf $\emptyset$;
- $b$: the same with $2$ in place of $1$.

The vertex $0$ is introduced twice, once below $a$ and once below $b$, and forgotten once, at $r$.

**Small cases.** The single vertex $0$ has the nice decomposition $\emptyset \xrightarrow{+0} \{0\} \xrightarrow{-0} \emptyset$ with three nodes. The path $0, \ldots, n-1$ has the nice path decomposition $+0, +1, -0, +2, -1, \ldots, +(n-1), -(n-2), -(n-1)$ of width 1.

**Non-examples.**

- A node with bag $\{0, 1, 2\}$ whose only child has bag $\{0\}$: two vertices are added at once, so the node is neither an introduce nor a forget node. Inserting the bag $\{0, 1\}$ between them fixes it.
- A node with two children whose bags are $\{0, 1\}$ and $\{0, 2\}$: a join node needs equal bags. Placing forget and introduce nodes on each branch, up to the common bag $\{0\}$, fixes it.
- A node with three children: a join node has exactly two. Two join nodes with the same bag fix it.
- The path decomposition $\{0, 1\}, \{1, 2\}$ of the path $0, 1, 2$, rooted at either end: it is a valid tree decomposition, but its leaf and root bags are not empty, and each step changes two vertices.

## Related definitions

- **Tree decomposition.** The general notion, with any tree and any bags; see [tree decomposition](/tree-decomposition/). A nice one is a normal form of it with the same width.
- **Introduce edge nodes.** A common variant adds nodes with one child and the same bag that mark one edge $uv$ of $G$, with $u, v$ in the bag; each edge is introduced exactly once. Dynamic programs then handle each edge at one place, which matters for problems such as [Hamiltonian cycle](/hamiltonian-cycle/) or counting.
- **Relaxed forms.** Some texts allow leaf bags with one vertex, or a nonempty root bag. These change the counts by a constant per leaf and do not change the width.
- **Nice path decomposition.** A nice decomposition with only introduce and forget nodes; its tree is a path.
- **Use in dynamic programming.** A [dynamic program over a tree decomposition](/dp-on-tree-decompositions/) defines one rule for each of the four node kinds and evaluates them bottom-up, for example in [postorder](/postorder-traversal/). It is the generalization of the program for [independent sets on trees](/independent-set-on-trees/).

## References
