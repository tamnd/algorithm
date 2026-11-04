---
tag: V0NDZZ
kind: definition
slug: bipartite-double-cover
name: Bipartite double cover
aliases:
- bipartite double graph
- Kronecker cover
area: techniques/reductions-and-transforms
level: intro
summary: A bipartite graph with two copies of each vertex and an edge between copies for each edge of the original graph.
prereqs: [undirected-graph, bipartite-graph, walk, breadth-first-search]
see_also: [bipartite-testing, bipartite-odd-cycle-theorem, connected-graph, kronecker-product, girth, odd-cycle-transversal, graph-isomorphism-definition]
sources:
  - book: isbn:9781439813041
    title: Richard Hammack, Wilfried Imrich and Sandi Klavzar, Handbook of Product Graphs, second edition, CRC Press, 2011
    locator: Chapter 5, Direct products (Theorem 5.9, Weichsel's theorem on the connectivity of direct products)
  - paper: doi:10.1090/S0002-9939-1962-0133816-6
    title: "Paul M. Weichsel, The Kronecker product of graphs, Proceedings of the American Mathematical Society 13(1) (1962)"
    locator: the main theorem (a Kronecker product of connected graphs is connected exactly when one factor has an odd cycle; with two bipartite factors it has two components)
  - paper: doi:10.1002/jgt.3190040107
    title: "Richard A. Brualdi, Frank Harary and Zevi Miller, Bigraphs versus digraphs via matrices, Journal of Graph Theory 4(1) (1980), 51-73"
    locator: the bipartite graph with two copies of the vertex set associated with a digraph and its adjacency matrix
---

The bipartite double cover of a graph $G$ is the graph $G \times K_2$: it has two copies $(v, 0)$ and $(v, 1)$ of each vertex $v$, and each edge $uv$ of $G$ gives the two edges $(u, 0)(v, 1)$ and $(u, 1)(v, 0)$. It is always a [bipartite graph](/bipartite-graph/), and a [walk](/walk/) in it records a walk of $G$ together with the parity of its length. This makes it a standard tool for questions about odd and even walks: [breadth-first search](/breadth-first-search/) on the double cover finds shortest odd walks, tests [bipartiteness](/bipartite-testing/) and finds a shortest odd cycle.

## Definition

Let $G = (V, E)$ be a simple [undirected graph](/undirected-graph/) with $n \ge 1$ vertices and $m$ edges. The *bipartite double cover* of $G$ is the graph $B(G)$ with

$$V(B(G)) = V \times \{0, 1\}, \qquad E(B(G)) = \bigl\{ \{(u, i), (v, 1 - i)\} : \{u, v\} \in E,\ i \in \{0, 1\} \bigr\}.$$

So $(u, i)$ and $(v, j)$ are adjacent exactly when $\{u, v\} \in E$ and $i \ne j$. This is the direct (tensor, Kronecker, categorical) product $G \times K_2$, in which $(u, i)$ and $(v, j)$ are adjacent when $u v$ is an edge of $G$ and $i j$ is an edge of $K_2$. If $A$ is the [adjacency matrix](/adjacency-matrix/) of $G$ and the vertices of $B(G)$ are listed as all $(v, 0)$ and then all $(v, 1)$, the adjacency matrix of $B(G)$ is

$$\begin{pmatrix} 0 & A \\ A & 0 \end{pmatrix} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} \otimes A,$$

the [Kronecker product](/kronecker-product/) of the adjacency matrices of $K_2$ and $G$.

The name *cover* comes from the projection $\pi(v, i) = v$. Every vertex of $G$ has exactly two preimages, and $\pi$ maps the neighbours of $(v, i)$ one to one onto the neighbours of $v$, since $(v, i)$ has the neighbours $(u, 1 - i)$ for $u \in N(v)$. So $B(G)$ is a 2-fold covering graph of $G$, and $(v, i)$ has the same degree as $v$.

### Basic facts

**Fact 1.** $B(G)$ is bipartite, with parts $V \times \{0\}$ and $V \times \{1\}$. *Proof.* Every edge joins a vertex with second coordinate $i$ to one with $1 - i$. $\square$

**Fact 2.** $B(G)$ has $2n$ vertices and $2m$ edges. *Proof.* The vertex count is $|V \times \{0, 1\}|$. Each edge $\{u, v\}$ of $G$ gives the edges $\{(u, 0), (v, 1)\}$ and $\{(u, 1), (v, 0)\}$; the choice $i$ for the pair written as $(v, u)$ gives the same two edges. They are distinct because $u \ne v$, and edges from different edges of $G$ are distinct because $\pi$ maps them to different edges. $\square$

**Fact 3 (walks and parity).** For $u, v \in V$, $i \in \{0, 1\}$ and $k \ge 0$: $G$ has a walk of length $k$ from $u$ to $v$ if and only if $B(G)$ has a walk of length $k$ from $(u, i)$ to $(v, (i + k) \bmod 2)$. *Proof.* A walk $u = w_0, w_1, \ldots, w_k = v$ in $G$ lifts to $(w_t, (i + t) \bmod 2)$ for $t = 0, \ldots, k$; each step is an edge of $B(G)$ because $w_t w_{t+1} \in E$ and the second coordinate changes. Conversely, $\pi$ maps a walk of $B(G)$ to a walk of $G$ of the same length, and the second coordinate changes at each step, so after $k$ steps it is $(i + k) \bmod 2$. $\square$

So the distance from $(u, 0)$ to $(v, 1)$ in $B(G)$ is the length of a shortest odd walk from $u$ to $v$ in $G$, and the distance from $(u, 0)$ to $(v, 0)$ is the length of a shortest even walk ($\infty$ when there is none).

**Fact 4 (connectivity).** $B(G)$ is [connected](/connected-graph/) if and only if $G$ is connected and not bipartite. This is the case $H = K_2$ of Weichsel's theorem on direct products. *Proof.* Suppose $G$ is connected and has an odd cycle through a vertex $w$, of length $\ell$. Take two vertices $(u, i)$ and $(v, j)$ of $B(G)$, and a walk $P$ from $u$ to $v$ in $G$ of length $L$. If $L \equiv j - i \pmod 2$, the lift of $P$ from $(u, i)$ ends at $(v, j)$ by Fact 3. Otherwise go from $u$ to $w$ along a walk $Q$, around the odd cycle, back along $Q$ reversed, and then along $P$. This walk has length $2|Q| + \ell + L$, of the other parity, and its lift from $(u, i)$ ends at $(v, j)$. Conversely, if $G$ is not connected, take $u$ and $v$ in different components; no walk of $G$ joins them, so by Fact 3 no walk of $B(G)$ joins $(u, 0)$ and $(v, 0)$. If $G$ is bipartite, every closed walk of $G$ has even length, so by Fact 3 no walk of $B(G)$ joins $(u, 0)$ and $(u, 1)$. $\square$

**Fact 5 (bipartite input).** If $G$ is bipartite, then $B(G)$ is isomorphic to two disjoint copies of $G$. *Proof.* Let $X, Y$ be the parts of $G$. Define $\varphi_0(x) = (x, 0)$ and $\varphi_1(x) = (x, 1)$ for $x \in X$, and $\varphi_0(y) = (y, 1)$ and $\varphi_1(y) = (y, 0)$ for $y \in Y$. Each $\varphi_a$ is one to one, their images are disjoint and cover $V \times \{0, 1\}$. Every edge of $G$ joins some $x \in X$ to some $y \in Y$, and the two edges of $B(G)$ that it gives are $\{(x, 0), (y, 1)\} = \varphi_0(\{x, y\})$ and $\{(x, 1), (y, 0)\} = \varphi_1(\{x, y\})$. So the edges of $B(G)$ are exactly the images of the edges of $G$ under $\varphi_0$ and under $\varphi_1$, and no edge joins the two images. $\square$

**Fact 6 (spectrum).** The eigenvalues of $B(G)$ are $\lambda_1, \ldots, \lambda_n, -\lambda_1, \ldots, -\lambda_n$, where $\lambda_1, \ldots, \lambda_n$ are the [eigenvalues](/eigenvalue/) of $A$. *Proof.* $A$ is real and symmetric, so it has an orthonormal basis of eigenvectors $x_1, \ldots, x_n$ with $A x_r = \lambda_r x_r$. Then $(x_r, x_r)$ is an eigenvector of the block matrix with eigenvalue $\lambda_r$, and $(x_r, -x_r)$ one with eigenvalue $-\lambda_r$. These $2n$ vectors are orthogonal, so they are a basis, and the list is complete. $\square$

### The algorithmic use

To find, for a source $s$, the shortest odd walk and the shortest even walk from $s$ to every vertex, run BFS on $B(G)$ from $(s, 0)$. $B(G)$ is never built explicitly: a BFS state is a pair $(v, \text{parity})$, and the neighbours of $(v, i)$ are $(u, 1 - i)$ for $u \in N(v)$. The time is $O(n + m)$ by Fact 2. Three uses follow:

- **Bipartiteness.** A connected $G$ is bipartite if and only if $(s, 1)$ is unreachable from $(s, 0)$, by Fact 4. This is the parity argument of the [odd cycle theorem](/bipartite-odd-cycle-theorem/) in another form.
- **Shortest odd closed walk through $s$.** Its length is $\operatorname{dist}_{B(G)}((s, 0), (s, 1))$.
- **Shortest odd cycle.** Let $L$ be the minimum of $\operatorname{dist}_{B(G)}((s, 0), (s, 1))$ over all $s$. Then $L$ is the length of a shortest odd cycle of $G$, found in $O(n(n + m))$ time. *Proof.* Every odd cycle is an odd closed walk, so $L$ is at most the shortest odd cycle. Conversely, take an odd closed walk of length $L$. If it visits some vertex twice (other than at its two ends), cut it there into two closed walks whose lengths add up to $L$; one of them is odd and shorter, which contradicts the minimality of $L$. So the walk is a cycle. $\square$

## Examples and non-examples

- **Triangle.** $B(K_3)$ is the 6-cycle $C_6$: the walk $(0,0), (1,1), (2,0), (0,1), (1,0), (2,1), (0,0)$ visits all 6 vertices along its 6 edges. More generally, for odd $k \ge 3$, $B(C_k) = C_{2k}$, since $C_k$ is connected, not bipartite and 2-regular, so $B(C_k)$ is connected and 2-regular with $2k$ vertices.
- **Even cycle.** $B(C_4)$ is two disjoint copies of $C_4$ (Fact 5). In the same way $B(P_3)$, for the path with 3 vertices, has 2 components.
- **Complete graph $K_4$.** $B(K_4)$ is the cube graph $Q_3$: 8 vertices, 12 edges, 3-regular. In general $B(K_n)$ is $K_{n,n}$ with a perfect matching removed, since $(u, 0)$ and $(v, 1)$ are adjacent exactly when $u \ne v$.
- **Petersen graph.** The bipartite double cover of the Petersen graph (10 vertices, 15 edges, 3-regular) is the Desargues graph, the generalized Petersen graph $GP(10, 3)$: 20 vertices, 30 edges, 3-regular, connected.
- **An odd walk that is not a path.** Let $G$ be the 5-cycle $0, 1, 2, 3, 4$ with one more vertex $5$ joined to $0$. In $B(G)$ the distance from $(5, 0)$ to $(5, 1)$ is $7$, along $(5,0), (0,1), (4,0), (3,1), (2,0), (1,1), (0,0), (5,1)$. Its projection $5, 0, 4, 3, 2, 1, 0, 5$ is the shortest odd closed walk through $5$, and it repeats the vertices $0$ and $5$. The minimum over all start vertices is $5$, the length of the 5-cycle.
- **Non-example: $C_8$.** No graph has $C_8$ as its bipartite double cover. Such a graph would have 4 vertices, 4 edges and all degrees $2$ (degrees are kept by the cover), so it would be $C_4$; but $B(C_4)$ is disconnected.
- **Non-example: the prism.** The Cartesian product $K_3 \square K_2$ (the triangular prism) also has two copies of each vertex of $K_3$, but it joins $(v, 0)$ to $(v, 1)$ and keeps the triangles inside each copy. It contains triangles, so it is not bipartite and is not $B(K_3)$.

### Common errors

- Confusing $G \times K_2$ with $G \square K_2$. In the double cover, edges always change the copy, and there is no edge between $(v, 0)$ and $(v, 1)$ unless $G$ has a loop at $v$.
- Reading a shortest path of $B(G)$ as a path of $G$. Its projection is a walk and can repeat vertices, as in the example with the pendant vertex.
- Assuming that $B(G)$ is connected whenever $G$ is. For a connected bipartite $G$ it has two components (Fact 4 and Fact 5).

## Related definitions

- [Bipartite graph](/bipartite-graph/): $B(G)$ is always one, and the [odd cycle theorem](/bipartite-odd-cycle-theorem/) says when $G$ is one.
- [Kronecker product](/kronecker-product/) of matrices: the adjacency matrix of $B(G)$ is a Kronecker product.
- [Walk](/walk/), [girth](/girth/): the double cover turns questions about odd walks and odd cycles into distance questions.
- [Bipartite testing](/bipartite-testing/), [odd cycle transversal](/odd-cycle-transversal/): problems about the odd cycles of a graph.
- [Graph isomorphism](/graph-isomorphism-definition/): non-isomorphic graphs can have isomorphic double covers. For example $B(K_3 \sqcup K_3)$ and $B(C_6)$ are both two disjoint copies of $C_6$.
- Brualdi, Harary and Miller (1980) use the same construction for a directed graph $D$: the bipartite graph with an edge $(u, 0)(v, 1)$ for each arc $u \to v$. Its biadjacency matrix is the adjacency matrix of $D$.

### History

Weichsel (1962) proved the connectivity theorem for Kronecker (direct) products of graphs, of which Fact 4 is a special case.

## References
