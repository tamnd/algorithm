---
tag: ZG9QWA
kind: algorithm
slug: micali-vazirani-algorithm
name: Micali-Vazirani algorithm
aliases:
- MV algorithm
area: graphs/matching
level: research
summary: Finds maximum matchings in general graphs in O(E√V) time.
solves: [maximum-matching]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: "O(m n^(1/2))"}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1980
  people: [Silvio Micali, Vijay Vazirani]
  note: Micali and Vazirani presented the algorithm at FOCS 1980; a complete proof of its correctness took until Vazirani's simplified account of 2012 and 2013.
prereqs: [hopcroft-karp, edmonds-blossom, blossom]
see_also: [edmonds-blossom, hopcroft-karp, maximum-matching, augmenting-path, berge-lemma, tutte-berge-formula, gallai-edmonds-decomposition, disjoint-set-forest]
sources:
  - paper: "Silvio Micali and Vijay V. Vazirani, An O(sqrt(|V|) |E|) algorithm for finding maximum matching in general graphs, 21st Annual Symposium on Foundations of Computer Science, 17 to 27 (1980)"
    locator: the whole paper (the algorithm, its phases, double depth-first search and the time bound)
  - url: https://arxiv.org/abs/1210.4594
    title: Vijay V. Vazirani, A simplification of the MV matching algorithm and its proof, arXiv:1210.4594 (version 5, 2013)
    locator: Section 6 (double depth-first search and Theorem 28), Section 7 (procedures MIN and MAX, petals and buds, finding a maximal set of paths and removing vertices), Section 8 (Lemma 33 and Theorems 34 and 35)
  - paper: "Vijay V. Vazirani, A theory of alternating paths and blossoms for proving correctness of the O(sqrt(V) E) general graph maximum matching algorithm, Combinatorica 14(1), 71 to 109 (1994)"
    locator: the whole paper (tenacity, blossoms defined by minimum alternating paths, and the first published proof attempt)
  - paper: doi:10.1137/0202019
    title: John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 225 to 231 (1973)
    locator: the whole paper (the phase method and the bound of O(n^(1/2)) phases, which the MV algorithm reuses)
---

The Micali-Vazirani (MV) algorithm finds a [maximum matching](/maximum-matching/) in a general graph without weights in $O(m\sqrt n)$ time. Like [Hopcroft-Karp](/hopcroft-karp/) for bipartite graphs, it works in phases, and each phase augments the matching along a maximal set of vertex-disjoint shortest [augmenting paths](/augmenting-path/). The graph may have odd cycles, so shortest alternating paths can enter a [blossom](/blossom/) and must leave it the long way round. MV handles this without shrinking blossoms: an alternating [breadth-first search](/breadth-first-search/) gives each vertex an even and an odd level, and a *double depth-first search* from each *bridge* finds either two free vertices or the *bud* of a new petal. It is the fastest known deterministic algorithm for sparse general graphs, and it is known for being hard to prove and to implement.

## In plain words

In a graph without odd cycles, a vertex is reached either by paths of even length or by paths of odd length, never both. With odd cycles, a vertex can have a short path of one kind and a longer path of the other kind. The long path goes up through an edge called a bridge and then comes back down.

The algorithm first labels the vertices with their shortest path lengths, layer by layer, as in a breadth-first search. At each layer, it takes the bridges found so far and runs two searches downward from the two ends of each bridge. If the two searches reach two different free vertices, they have found a shortest augmenting path. If both are forced through one vertex, the vertices they visited form a petal, and each of them now knows its longer path length too. Petals are later skipped in one jump.

## The problem

The input is a finite undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. It is general (odd cycles are allowed) and has no weights. The output is a [matching](/maximum-matching/) of largest size. The empty graph and a graph with no edges give the empty matching; an odd cycle $C_{2k+1}$ gives $k$ edges and no perfect matching.

Fix a matching $M$. An *alternating path* starts at a free vertex and alternates between edges outside $M$ and edges in $M$. The *evenlevel* and *oddlevel* of $v$ are the lengths of the shortest even and odd alternating paths to $v$ ($\infty$ if there are none). Their minimum is the *minlevel*, their maximum the *maxlevel*, and their sum the *tenacity* of $v$. An edge $uv$ is a *prop* if it is the last edge of a shortest path to one of its ends; otherwise it is a *bridge*. The tenacity of a bridge $uv$ is $\text{evenlevel}(u) + \text{evenlevel}(v) + 1$ if $uv \notin M$ and $\text{oddlevel}(u) + \text{oddlevel}(v) + 1$ if $uv \in M$. A shortest augmenting path has length $2i + 1$, where $i$ is the first search level at which a bridge of tenacity $2i + 1$ leads to two free vertices.

## The algorithm

```pseudo id=main
MICALI-VAZIRANI(G)
L1  repeat                                                    ▷ one phase per pass
L2      give every free vertex evenlevel 0; every other level is ∞
L3      for i = 0, 1, 2, …
L4          MIN(i): from each vertex with a level equal to i, scan the edges of the right parity
               (unmatched if i is even, matched if i is odd); an edge to a vertex v with minlevel(v) ≥ i + 1 is a prop:
               set the level of v to i + 1 and add the scanning vertex to pred(v); any other edge is a bridge
L5          MAX(i): for each bridge (u, v) of tenacity 2i + 1 with u and v not erased, run DDFS from bud*(u) and bud*(v)
L6              if DDFS ends at a bottleneck b: the visited vertices form a petal with bud b;
                   set maxlevel(w) = 2i + 1 − minlevel(w) for each w in it
L7              if DDFS ends at two free vertices: open the petals on the two DFS paths to get an augmenting path P
L8                  augment M along P; erase P, and then every vertex all of whose predecessors are erased
L9          if a path was found at level i then end the phase
L10 until a phase finds no augmenting path; return M
```

**Double depth-first search (DDFS).** The red DFS starts at $\text{bud}^*(u)$ and the green DFS at $\text{bud}^*(v)$. From its current vertex $c$, a DFS looks at a predecessor $p$ of $c$ and moves to $\text{bud}^*(p)$, the outermost bud of the petals that contain $p$ (or $p$ itself), if that vertex is not yet visited. The DFS whose vertex has the higher minlevel moves; at equal levels red moves. If a DFS reaches the current vertex $w$ of the other DFS, the two meet: green backtracks from $w$ and tries to reach another vertex at level at most $\text{level}(w)$; if it succeeds, red takes $w$. Otherwise red backtracks and tries the same, and if it succeeds, green takes $w$. If both fail, $w$ is the bottleneck. If the two DFSs stand on two different free vertices, DDFS returns them.

**bud\*.** Each vertex in a petal points to its bud. $\text{bud}^*$ follows these pointers to the end, so a [disjoint-set forest](/disjoint-set-forest/) with [path compression](/path-compression/) computes it.

**Opening a petal.** To continue a path from a vertex $x$ of a petal down to its bud $b$ with a given parity: if the parity is that of $\text{minlevel}(x)$, follow predecessors down to $b$, opening inner petals on the way. Otherwise $x$ needs its maxlevel path, which goes up its own DFS tree to its end of the petal's bridge, across the bridge, and down the other tree to $b$.

## Example

Take the vertices $0, \ldots, 5$ with edges $01, 02, 12, 23, 34, 45$ and the matching $M = \{12, 34\}$. The free vertices are $0$ and $5$. The triangle $0, 1, 2$ is a blossom with base $0$.

| level $i$ | MIN | MAX |
|---|---|---|
| 0 | from 0: oddlevel(1) = oddlevel(2) = 1; from 5: oddlevel(4) = 1 | no bridge of tenacity 1 |
| 1 | from 1 along $12 \in M$: 2 has minlevel 1, so $12$ is a bridge of tenacity $1 + 1 + 1 = 3$; from 4: evenlevel(3) = 2 | DDFS on $(1, 2)$: both DFSs step to 0 and meet; neither finds another vertex, so 0 is the bottleneck. Petal $\{1, 2\}$ with bud 0, evenlevel(1) = evenlevel(2) = $3 - 1 = 2$ |
| 2 | from 2 along $23 \notin M$: 3 has minlevel 2, so $23$ is a bridge of tenacity $2 + 2 + 1 = 5$ | DDFS on $(2, 3)$: red starts at $\text{bud}^*(2) = 0$, which is free; green goes $3 \to 4 \to 5$. Two free vertices. |

To build the path, vertex 2 needs an even path to the bud 0. Its minlevel is odd, so it uses its maxlevel path through the petal's bridge: $2, 1, 0$. The augmenting path is $0, 1, 2, 3, 4, 5$ of length 5, and the new matching $\{01, 23, 45\}$ is perfect. In the next phase there are no free vertices, so the algorithm stops.

For the triangle alone, the first phase matches one edge, and the second phase finds no augmenting path, since the single free vertex has no partner.

## Correctness

The full proof is below. It has three parts.

1. **Each augmentation is valid.** The path built in line L7 is a simple alternating path between two free vertices, and line L8 erases its vertices, so the paths of one phase are vertex-disjoint. Flipping each path increases $|M|$ by one.
2. **The search is complete.** This is the hard part, and the proof cites Vazirani (2013). MIN and MAX give every vertex of tenacity at most $l_m$ its correct minlevel and maxlevel, where $l_m$ is the length of a shortest augmenting path; every bridge of tenacity $2i + 1$ is known by the end of MIN at level $i$; and DDFS finds the highest bottleneck or two disjoint paths to free vertices. Erasing vertices with no predecessors left removes only vertices that lie on no shortest augmenting path disjoint from the paths found. So each phase finds a maximal set of disjoint shortest augmenting paths, and a phase finds none only if none exists.
3. **Maximality and phases.** When a phase finds no augmenting path, $M$ is maximum by [Berge's lemma](/berge-lemma/). The argument of Hopcroft and Karp, which does not use bipartiteness, shows that the shortest augmenting length grows after each phase, so there are $O(\sqrt n)$ phases.

## Complexity

- **One phase.** MIN scans each edge a constant number of times. Each DDFS that ends at a bottleneck only searches edges of its petal, and each vertex joins at most one petal. Each DDFS that ends at free vertices only searches edges that lie on paths from its two start vertices to the two free vertices it finds (Theorem 28 of Vazirani 2013). Opening petals and erasing vertices each look at an edge a constant number of times. With a linear-time special case of set union for $\text{bud}^*$, a phase costs $O(m)$ on the RAM; with a general disjoint-set forest it costs $O(m\,\alpha(m, n))$.
- **Number of phases.** At most $O(\sqrt n)$, by the bound of Hopcroft and Karp. Total $O(m\sqrt n)$ time, and $\Theta(n + m)$ space for levels, predecessor lists, petals and bridges.
- **Python version.** It uses path compression alone for $\text{bud}^*$ and starts each DDFS with fresh visited marks, so it does not meet the bound exactly. It is meant to show the method on small graphs.

## Properties

- **General graphs, unweighted.** Odd cycles are handled by levels and petals, not by contraction.
- **Shortest paths only.** Every augmentation in a phase has the same length, and the length grows from phase to phase. This is checked in the tests.
- **Deterministic.** The order of bridges and of predecessor lists changes which maximum matching is returned, but not its size.
- **No contraction.** Petals are recorded by bud pointers; the graph itself is never changed during a phase.

## Variants and improvements

- **Bipartite case.** On bipartite graphs, [Hopcroft-Karp](/hopcroft-karp/) reaches the same bound with a much simpler search, a breadth-first search followed by depth-first searches without petals.
- **Edmonds' algorithm.** [Edmonds' blossom algorithm](/edmonds-blossom/) contracts blossoms and needs $O(n^3)$ time in its usual form. It is much simpler to write and to prove.
- **Greedy start.** Starting from a greedy [maximal matching](/maximal-matching/) instead of the empty matching saves early phases and does not change the bounds.
- **Algebraic algorithms.** Randomized algebraic methods find maximum matchings in $O(n^{\omega})$ time, which is better for dense graphs; see the [randomized parallel perfect matching](/rnc-perfect-matching/) for the method behind them.

## When to use it

Use it when the graph is large and sparse, has odd cycles, and the worst-case $O(m\sqrt n)$ bound matters, for example as a subroutine in a theoretical bound. For graphs with up to a few thousand vertices, Edmonds' algorithm or a library implementation is easier and fast enough. For bipartite graphs use Hopcroft-Karp.

## Pitfalls

- **Synchronization.** A bridge of tenacity $2i + 1$ must wait until level $i$, even if its tenacity is known earlier. A DDFS run too early can visit vertices whose own, smaller tenacity is not yet known and give them wrong maxlevels (Vazirani 2013, Figures 19 and 20).
- **Bridge tenacity not known yet.** When MIN declares a bridge, one level of an end may still be $\infty$. Keep the bridge waiting on that vertex and insert it once the level is set by MAX.
- **Stopping at the first meeting.** When the two DFSs meet at $w$, $w$ is a bottleneck only if neither DFS can reach another vertex at level at most $\text{level}(w)$. Stopping at the first meeting gives petals that are too small and maxlevels that are wrong.
- **Parities when opening petals.** A vertex in a petal has two paths to the bud, and the path through the bridge is needed exactly when the required parity is not that of its minlevel. Mixing them up gives paths that are not alternating.
- **Erasing.** After an augmentation, all vertices of the path and then all vertices with no predecessors left must be erased. Otherwise later paths in the same phase can cross the path just used.
- **Trusting old proofs.** Several published descriptions and proofs of the algorithm had gaps. Test any implementation against a brute force on many small graphs with odd cycles.

## Implementations

The Python version takes the number of vertices and a list of edges and returns the mate of each vertex, or -1. It follows Vazirani's 2013 description: levels and props from MIN, bridges inserted once their tenacity is known, DDFS with the meeting rules, petals with bud pointers, path opening through petals, and erasure by predecessor counts. It checks every path before it augments. The tests compare the size with a brute force on 600 random graphs, and check on 300 more that the path lengths in one phase are equal and grow from phase to phase.

## History

Micali and Vazirani presented the algorithm at FOCS in 1980, extending the $O(m\sqrt n)$ bound of Hopcroft and Karp from bipartite graphs to general graphs. The conference paper gave no complete proof. Vazirani published a theory of alternating paths and blossoms for this purpose in Combinatorica in 1994, and later found gaps in it. In 2012 and 2013 he gave a simpler description of the algorithm with a new, recursive definition of blossoms and a complete proof. The 1980 paper had claimed without proof that path compression alone computes $\text{bud}^*$ in linear time per phase; a 2013 result showed that it does not, which is why the RAM bound uses a special linear-time set union.

## References
