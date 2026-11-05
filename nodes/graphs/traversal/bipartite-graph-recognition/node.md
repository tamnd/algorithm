---
tag: 62CY51
kind: problem
slug: bipartite-graph-recognition
name: Bipartite graph recognition
aliases:
- certifying bipartiteness
area: graphs/traversal
level: intro
summary: Decides whether the vertices of a graph can be split into two sets with every edge crossing, using a graph traversal with two colors.
prereqs: [bipartite-graph, bipartiteness-check]
see_also: [bipartiteness-check, bipartite-testing, certifying-algorithms, bipartite-odd-cycle-theorem, bfs-tree, lowest-common-ancestor, dynamic-bipartiteness, bipartite-double-cover]
sources:
  - paper: doi:10.1016/j.cosrev.2010.09.009
    title: Ross M. McConnell, Kurt Mehlhorn, Stefan Näher and Pascal Schweitzer, Certifying algorithms, Computer Science Review 5(2), 119 to 161 (2011)
    locator: the introduction and the example of bipartiteness with a 2-coloring or an odd cycle as witness
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness (the odd cycle through the lowest common ancestor in the BFS tree)
  - paper: doi:10.1016/j.tcs.2005.09.013
    title: Joan Feigenbaum, Sampath Kannan, Andrew McGregor, Siddharth Suri and Jian Zhang, On graph problems in a semi-streaming model, Theoretical Computer Science 348(2-3), 207 to 216 (2005)
    locator: the one-pass semi-streaming algorithm for bipartiteness
  - paper: doi:10.1145/285055.285060
    title: Oded Goldreich, Shafi Goldwasser and Dana Ron, Property testing and its connection to learning and approximation, Journal of the ACM 45(4), 653 to 750 (1998)
    locator: the tester for bipartiteness in the dense graph model
---

Bipartite graph recognition asks whether a given graph is [bipartite](/bipartite-graph/), and asks the answer to come with a proof that anyone can check quickly. For YES the proof is the bipartition, two sets of vertices with no edge inside either set. For NO the proof is a cycle of odd length, which no bipartition can split, by the [odd cycle theorem](/bipartite-odd-cycle-theorem/). A [breadth-first search](/breadth-first-search/) finds one of the two proofs in $\Theta(n + m)$ time, and each proof is checked in linear time. Recognition with witnesses is the standard first example of a [certifying algorithm](/certifying-algorithms/). This page treats the witnesses and the other models of computation in which the problem is studied. The basic search is on [bipartiteness checking](/bipartiteness-check/).

## In plain words

Someone gives you a network and says "it splits into two teams, with every link going between the teams". You should not have to trust them.

If the answer is yes, they can show you the two teams. You look at each link and see that it joins the two teams.

If the answer is no, they can show you a loop of links with an odd number of steps. Going round the loop, the teams would have to switch at every step, and after an odd number of switches you cannot be back on the team you started with. So no split exists.

Either proof is easy to check. A good algorithm gives you one of the two, and not only a yes or a no.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges.

**Output.** One of:

- a *bipartition*: a set $A \subseteq V$ such that each edge has exactly one end in $A$, which certifies YES;
- an *odd cycle*: a sequence of distinct vertices $u_0, u_1, \ldots, u_{2k}$ with $\{u_i, u_{i+1}\} \in E$ for each $i$ and $\{u_{2k}, u_0\} \in E$, which certifies NO. A self-loop is the case $k = 0$.

**Checking.** A bipartition is checked by one pass over the edges, with a Boolean array for $A$, in $O(n + m)$ time. An odd cycle is checked by testing that its length is odd, that its vertices are distinct, and that each of its consecutive pairs is an edge. With a hash set of the edges, or after sorting each adjacency list, this is $O(n + m)$ time. The two kinds of output cannot both exist for one graph: going round an odd cycle, the side changes an odd number of times, so the start vertex would be on both sides.

## Variants

- **Decision only.** Answer YES or NO without a proof. See [bipartiteness checking](/bipartiteness-check/).
- **Shortest odd cycle.** Find an odd cycle of the smallest length, the odd girth. A BFS from every vertex finds it in $O(nm)$ time. The odd cycle from a single BFS is not always the shortest one.
- **Online and dynamic.** Keep the answer while edges arrive, or while edges arrive and leave. See [dynamic bipartiteness](/dynamic-bipartiteness/).
- **Streaming.** The edges arrive in one pass and the memory is small compared with $m$. Feigenbaum, Kannan, McGregor, Suri and Zhang gave a one-pass algorithm with $O(n \log n)$ bits, the semi-streaming model, by keeping a spanning forest together with parity information.
- **Property testing.** Decide with few queries whether the graph is bipartite or far from bipartite, that is, needs many edge deletions to become bipartite. In the dense graph model, where a query asks whether two given vertices are adjacent, Goldreich, Goldwasser and Ron gave a tester whose number of queries depends only on the distance parameter $\varepsilon$, and not on $n$.

## Examples

Take the vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$.

- **YES with a witness.** BFS from 0 and from 7 gives the colours of the parities of the [BFS layers](/bfs-layers/). The witness is $A = \{0, 3, 4, 6, 7\}$. Each of the 8 edges has one end in $A$: for example $\{3, 5\}$ has 3 in $A$ and 5 outside.
- **NO with a witness.** Add the edge $\{3, 4\}$. BFS from 0 gives the layers $\{0\}$, $\{1, 2\}$, $\{3, 4\}$, $\{5\}$, $\{6\}$, with the parents $\pi[3] = 1$ and $\pi[4] = 2$. The new edge lies inside the layer $\{3, 4\}$. The tree paths go up from 3 to 1 to 0 and from 4 to 2 to 0, so the lowest common ancestor is 0. The witness is the cycle $0, 1, 3, 4, 2$ of length 5. Its consecutive pairs $\{0,1\}$, $\{1,3\}$, $\{3,4\}$, $\{4,2\}$, $\{2,0\}$ are all edges, and 5 is odd.
- **A shorter odd cycle exists.** The same graph also has the triangle $2, 3, 4$, through the edges $\{2,3\}$, $\{3,4\}$, $\{2,4\}$. The BFS witness from 0 has length 5, which is valid but not the shortest.

## Known algorithms

**Certifying BFS.** Run the BFS check of [bipartiteness checking](/bipartiteness-check/) on each component, with the parents $\pi$ and the distances.

1. If no edge joins two vertices of the same colour, return $A = \{v : \mathrm{dist}[v] \text{ is even}\}$.
2. Otherwise let $\{u, v\}$ be such an edge. Both ends are in one layer. Walk up from $u$ and from $v$ in the [BFS tree](/bfs-tree/), one step from each at a time, until the two walks meet at a vertex $z$, the [lowest common ancestor](/lowest-common-ancestor/). Return the path from $u$ up to $z$, followed by the path from $z$ down to $v$.

The two walks have the same length $i - j$ at each moment, where $i$ is the layer of $u$ and $v$ and $j$ that of $z$, so they meet at the same time. The cycle has $2(i - j) + 1$ edges, and its vertices are distinct because the two tree paths meet only at $z$. Step 2 takes $O(n)$ extra time.

**Certifying DFS.** Colour by the parity of DFS depth. A back edge $\{u, v\}$, with $v$ an ancestor of $u$ and the same parity, gives the odd cycle of the tree path from $v$ to $u$ plus the edge. Reading the cycle takes time proportional to its length.

| method | time | witness for NO |
|---|---|---|
| certifying BFS | $\Theta(n + m)$ | odd cycle through the BFS tree and one edge inside a layer |
| certifying DFS | $\Theta(n + m)$ | odd cycle of a tree path and one back edge |
| [union-find with parity](/dsu-with-parity/) | $O(n + m\,\alpha(n))$ | the edge that closes the first odd cycle; the cycle itself needs the forest |

## Bounds

- **Time.** $\Theta(n + m)$ for the decision, and the witnesses cost no more. The lower bound argument is on [bipartiteness checking](/bipartiteness-check/).
- **Size of the witness.** A bipartition has $n$ bits. An odd cycle has at most $n$ vertices, and the shortest odd cycle can have $\Theta(n)$ vertices, as in an odd cycle $C_n$.
- **Space.** On a read-only input, recognition is in deterministic logspace, through the reduction to connectivity in the [bipartite double cover](/bipartite-double-cover/) and Reingold's theorem. The witness itself is written on a write-only output.
- **Streaming.** One pass with $O(n \log n)$ bits suffices, by the semi-streaming algorithm above.

## Reductions

- **To connectivity.** $G$ is bipartite exactly when, in the [bipartite double cover](/bipartite-double-cover/), no vertex $v$ has its two copies in one component. A path from $(v, 0)$ to $(v, 1)$ in the cover projects to a closed walk of odd length through $v$ in $G$, and a closed walk of odd length always contains an odd cycle.
- **Checking a claimed bipartition.** This is a single scan of the edges, so recognition with a YES witness is in the class of problems whose answers are checkable in linear time.
- **Witness extraction from a closed walk.** If a closed walk of odd length is known, an odd cycle can be cut out of it in linear time: if a vertex repeats, the walk splits at the repeat into two closed walks, one of which has odd length, and the process continues on that one.

## Applications

- **Trustworthy software.** A certifying program can be checked on every run, by a short checker, instead of being trusted. Libraries of graph algorithms, such as LEDA, return witnesses for this reason, and bipartiteness is a standard first example.
- **Diagnosis.** When a model should be bipartite, for example a conflict graph that should split into two groups, the odd cycle shows where the model is wrong. It points to a small set of conflicts that cannot be met together.
- **Recognition of graph classes.** Many recognition algorithms for graph classes return a witness for NO, such as a forbidden subgraph. Bipartite graphs are the class whose forbidden subgraphs are the odd cycles.

## References
