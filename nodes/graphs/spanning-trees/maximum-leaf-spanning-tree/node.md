---
tag: ZTZK8Y
kind: problem
slug: maximum-leaf-spanning-tree
name: Maximum leaf spanning tree problem
aliases:
- Maximum leaf spanning tree
- max-leaf spanning tree
area: graphs/spanning-trees
level: advanced
summary: Find a spanning tree with the largest number of leaves; NP-hard.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Ω(n + m)}
prereqs: [spanning-tree, dominating-set, np-hard, degree-constrained-spanning-tree]
see_also: [spanning-tree, dominating-set, degree-constrained-spanning-tree, hamiltonian-path-problem, kernelization, set-cover, np-hard]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman (1979)
    locator: Appendix A2.1, problem ND2, Maximum Leaf Spanning Tree
  - paper: doi:10.1006/jagm.1998.0944
    title: "Hsueh-I Lu and R. Ravi, Approximating maximum leaf spanning trees in almost linear time, Journal of Algorithms 29(1) (1998), 132-141"
    locator: the whole paper (the greedy 3-approximation in O((m + n) α(m, n)) time, with a tight example)
  - paper: doi:10.1007/3-540-68530-8_37
    title: "Roberto Solis-Oba, 2-approximation algorithm for finding a spanning tree with maximum number of leaves, Algorithms ESA 1998, Lecture Notes in Computer Science 1461, 441-452"
    locator: the whole paper (the linear-time 2-approximation by expansion rules)
  - paper: doi:10.1137/0404010
    title: "Daniel J. Kleitman and Douglas B. West, Spanning trees with many leaves, SIAM Journal on Discrete Mathematics 4(1) (1991), 99-106"
    locator: the whole paper (every connected graph with minimum degree at least 3 has a spanning tree with at least n/4 + 2 leaves)
---

The maximum leaf spanning tree problem asks, for a connected undirected graph, for a [spanning tree](/spanning-tree/) with as many leaves, vertices of degree 1, as possible. It is the opposite of keeping degrees low, as in the [degree-constrained spanning tree](/degree-constrained-spanning-tree/) problem: a tree with many leaves is bushy, with a small connected core. That core is exactly a connected [dominating set](/dominating-set/), so the problem is equivalent to finding a smallest connected dominating set. It is [NP-hard](/np-hard/) (Garey and Johnson, problem ND2) and hard to approximate within some constant, but a greedy algorithm gives a factor 3 in almost linear time, and a refined one a factor 2 in linear time.

## In plain words

Picture a network that must stay connected through a tree of links. Points inside the tree pass messages along; points at the ends of branches only listen. You want as many listeners as possible, so that the core of relaying points is small.

Every listener must sit next to some relay, and the relays must form one connected group. So the question is the same as asking for the smallest connected group of points that touches every other point. That question is hard in general, but simple greedy rules come within a factor of two or three of the best answer.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. There are no weights, so ties between edges do not arise; many trees can be optimal. Parallel edges and self-loops do not matter and can be dropped.

**Output.** A spanning tree $T$ of $G$ with the largest number $\ell(T)$ of leaves. The optimum is written $\ell(G)$.

**Decision version** (Garey and Johnson, ND2). Given $G$ and an integer $K$, does $G$ have a spanning tree with at least $K$ leaves? It is NP-complete.

**Disconnected graphs.** A graph that is not connected has no spanning tree. The natural extension is a spanning forest with the most leaves, which is a maximum leaf spanning tree of each component; count an isolated vertex as having no leaf.

**Small cases.** For $n = 1$ the only tree has no edge, and for $n = 2$ both vertices are leaves. From here on, $n \ge 3$, so every spanning tree has an internal vertex.

**The equivalence with connected dominating sets.** A set $D \subseteq V$ is a *connected dominating set* when $D$ induces a connected subgraph and every vertex outside $D$ has a neighbour in $D$. Let $\gamma_c(G)$ be the smallest size of such a set. For a connected graph with $n \ge 3$,

$$\ell(G) = n - \gamma_c(G).$$

*Proof.* Let $T$ be a spanning tree, and $D$ its set of internal vertices, which is not empty since $n \ge 3$. Deleting the leaves of a tree leaves a tree, so $D$ induces a connected subgraph, and each leaf is joined in $T$ to an internal vertex, so $D$ dominates. Hence $\gamma_c(G) \le n - \ell(T)$. Conversely, let $D$ be a connected dominating set. Take a spanning tree of the subgraph induced by $D$ and join each vertex outside $D$ to one neighbour in $D$. This is a spanning tree of $G$ in which every vertex outside $D$ is a leaf, so $\ell(G) \ge n - |D|$. $\square$

## Variants

- **Connected dominating set.** The equivalent minimization problem above. The two have the same optimal solutions but different approximation behaviour, since a constant factor on $\ell$ does not translate into a constant factor on $n - \ell$.
- **Minimum leaf spanning tree.** Ask for the fewest leaves instead. A spanning tree with 2 leaves is a Hamiltonian path, so this version contains the [Hamiltonian path problem](/hamiltonian-path-problem/) and is NP-hard too.
- **Directed version.** A spanning out-tree from a root with the most leaves, studied as the maximum leaf out-branching problem.
- **Weighted leaves.** Each vertex has a profit for being a leaf; maximize the total profit.
- **Parameterized version (k-leaf spanning tree).** Given $k$, decide whether $\ell(G) \ge k$. It is fixed-parameter tractable, and it has a [kernel](/kernelization/) with $O(k)$ vertices.

## Examples

**The graph with six vertices.** Take the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$, with the weights ignored. The graph has 55 spanning trees. Counted by their number of leaves, the best have 4 leaves, and there are 8 of them, for example $\{ab, bc, bd, de, df\}$, whose internal vertices are $b$ and $d$, and $\{ac, bc, cd, ce, ef\}$, whose internal vertices are $c$ and $e$. No tree has 5 leaves: that would be a star, and no vertex is adjacent to all five others. So $\ell(G) = 4$, and $\gamma_c(G) = 2$: the set $\{b, d\}$ is connected, and $b$ dominates $a$ and $c$ while $d$ dominates $c$, $e$ and $f$.

**Families.**

| graph | $\ell(G)$ | an optimal tree |
|---|---|---|
| complete graph $K_n$ | $n - 1$ | a star |
| path $P_n$, $n \ge 2$ | 2 | the path |
| cycle $C_n$ | 2 | the cycle minus an edge |
| complete bipartite $K_{p,q}$, $2 \le p \le q$ | $p + q - 2$ | an edge $uv$, with the other vertices of each side joined to the opposite end |
| wheel with $k$ rim vertices | $k$ | the star from the hub |

For $K_{p,q}$ with $p, q \ge 2$, no vertex dominates the graph, so $\gamma_c \ge 2$, and an edge is a connected dominating set.

**A lower bound from degrees.** Kleitman and West proved that every connected graph with minimum degree at least 3 has a spanning tree with at least $n/4 + 2$ leaves, and that this is tight. Such general bounds give fast certificates that $\ell(G)$ is large.

## Known algorithms

| algorithm | guarantee | time |
|---|---|---|
| brute force over vertex sets as connected dominating sets | exact | $O(2^n (n + m))$ |
| exact exponential algorithms with branching | exact | $O(c^n)$ with $c < 2$ |
| fixed-parameter algorithms for $\ell(G) \ge k$ | exact | $O(c^k \operatorname{poly}(n))$, with a linear kernel |
| Lu and Ravi, greedy growth (1998) | $\ell(T) \ge \ell(G)/3$ | $O((m + n)\, \alpha(m, n))$ |
| Solis-Oba, expansion rules (1998) | $\ell(T) \ge \ell(G)/2$ | $O(m + n)$ |

**The greedy idea.** Lu and Ravi grow a forest by repeatedly picking a vertex with many neighbours not yet in the forest and adding it with all of them as leaves. Each such step makes the vertex internal but adds several leaves, so it pays for itself; then the trees of the forest are joined into one tree at a small loss. Solis-Oba's rules also expand vertices that have only two new neighbours when that prepares a larger expansion, which sharpens the count to a factor 2. A spanning tree built by any search that makes each expanded vertex adopt all its free neighbours is a natural baseline.

## Bounds

- **Hardness.** The decision version is NP-complete (Garey and Johnson, ND2), so no polynomial algorithm is known. The problem is also MAX SNP-hard (Galbiati, Maffioli and Morzenti, 1994), so it has no polynomial-time approximation scheme unless P = NP.
- **Best ratio.** Factor 2 in linear time (Solis-Oba). Whether a ratio below 2 is possible in polynomial time is open, as far as the sources here say.
- **Trivial lower bound.** Any algorithm must read the graph, so $\Omega(n + m)$ time.
- **Connected dominating set.** For the minimization version, a factor of about $\ln \Delta$ is possible, where $\Delta$ is the maximum degree, by a greedy method in the style of [set cover](/set-cover/), and the reduction from set cover below shows that a factor $(1 - \varepsilon) \ln n$ is not possible unless P = NP, as for set cover.

## Reductions

- **To and from connected dominating set.** $\ell(G) = n - \gamma_c(G)$ for $n \ge 3$, with the conversions between trees and sets in the proof above, each in $O(n + m)$ time.
- **From set cover.** Take a [set cover](/set-cover/) instance with a nonempty universe $U$ and sets $S_1, \ldots, S_k$ that together cover $U$. Build a graph with a vertex for each element and each set, a vertex $r$ joined to every set vertex, a pendant vertex $r'$ joined only to $r$, and an edge from each set to each of its elements. Then $\gamma_c = c + 1$, where $c$ is the size of a smallest cover. A cover $C$ gives the connected dominating set $C \cup \{r\}$. Conversely, a connected dominating set $D$ must contain $r$, to dominate $r'$ and stay connected, and replacing each element vertex of $D$ by a set that contains it turns the set vertices of $D$ into a cover of size at most $|D| - 1$. So the problem is NP-hard, and since $n - \ell(G) = c + 1$, an exact algorithm for the maximum leaf spanning tree finds a minimum set cover.
- **To the minimum leaf problem.** None simple: the two objectives behave differently, and only the minimum version contains Hamiltonian path directly.

## Applications

- **Wireless and ad hoc networks.** A small connected dominating set is a *virtual backbone*: only its nodes relay traffic, and every other node is one hop from it. The maximum leaf spanning tree gives such a backbone.
- **Broadcasting.** In a broadcast tree, only internal nodes forward, so many leaves mean few forwarding nodes.
- **Network design and circuit layout.** Trees with few internal nodes keep the number of switching or branching points low.
- **Graph theory.** The number of leaves is studied as a graph invariant, with bounds in terms of the minimum degree such as the Kleitman-West bound.

## References
