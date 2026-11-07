---
tag: 9BQFTQ
kind: algorithm
slug: cuthill-mckee
name: Cuthill-McKee algorithm
aliases:
- Cuthill-McKee ordering
- CM ordering
area: numerical/linear-systems
level: advanced
summary: Breadth-first ordering that reduces the bandwidth of a sparse symmetric matrix.
solves: [bandwidth-reduction]
model: word-ram
complexity:
  vars: {n: "the number of vertices (unknowns)", m: "the number of edges (off-diagonal pairs)", Δ: "the largest degree"}
  time: {worst: O(n (n + m))}
  space: {extra: Θ(n)}
  numbering: {worst: "O(n log n + m log Δ)"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [breadth-first-search, sparse-matrix, banded-matrix]
see_also: [reverse-cuthill-mckee, bandwidth-reduction, fill-reducing-ordering, banded-matrix, fill-in, minimum-degree-ordering, nested-dissection, sparse-linear-systems]
sources:
  - paper: doi:10.1145/800195.805928
    title: E. Cuthill and J. McKee, Reducing the bandwidth of sparse symmetric matrices, Proceedings of the 24th ACM National Conference, 1969
    locator: pp. 157 to 172 (level structures from a start vertex, neighbours numbered by increasing degree)
  - paper: doi:10.1137/0713020
    title: Wai-Hung Liu and Andrew H. Sherman, Comparative analysis of the Cuthill-McKee and the reverse Cuthill-McKee ordering algorithms for sparse matrices, SIAM Journal on Numerical Analysis 13(2), 1976
    locator: pp. 198 to 213 (the envelope of the reversed ordering is never larger)
  - paper: doi:10.1145/355841.355845
    title: Alan George and Joseph W. H. Liu, An implementation of a pseudoperipheral node finder, ACM Transactions on Mathematical Software 5(3), 1979
    locator: pp. 284 to 295 (the shrinking last level heuristic for the start vertex)
  - book: "Alan George and Joseph W. H. Liu, Computer Solution of Large Sparse Positive Definite Systems, Prentice-Hall, 1981"
    title: Computer Solution of Large Sparse Positive Definite Systems
    locator: Chapter 4, Band and envelope methods (Section 4.3, the reverse Cuthill-McKee algorithm; Section 4.3.2, finding a starting node)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 7, Fill-reducing orderings (the section on bandwidth and profile reduction)
  - paper: doi:10.1137/0713023
    title: Norman E. Gibbs, William G. Poole and Paul K. Stockmeyer, An algorithm for reducing the bandwidth and profile of a sparse matrix, SIAM Journal on Numerical Analysis 13(2), 1976
    locator: pp. 236 to 250
---

The Cuthill-McKee algorithm renumbers the unknowns of a sparse symmetric matrix so that its nonzeros lie in a narrow band around the diagonal. It runs a [breadth-first search](/breadth-first-search/) on the graph of the matrix from a carefully chosen start vertex and numbers the vertices in the order the search discovers them, taking the unvisited neighbours of each vertex in order of increasing degree. Because every edge joins two vertices in the same or adjacent BFS levels, the bandwidth of the reordered matrix is less than twice the width of the widest level. The numbering takes $O(n \log n + m \log \Delta)$ time, and finding a good start vertex takes a few more searches. Reversing the order gives [reverse Cuthill-McKee](/reverse-cuthill-mckee/), which has the same bandwidth and never a larger envelope, and is the variant used in practice. It is a heuristic for the NP-hard [bandwidth reduction](/bandwidth-reduction/) problem, with no approximation guarantee.

## In plain words

Pick an unknown at the edge of the problem and give it number one. Then number all its neighbours, then all their new neighbours, and so on, like ripples spreading from a stone dropped in a pond. Unknowns that are connected end up with numbers that are close, because they are in the same ripple or in neighbouring ripples. Close numbers mean the nonzeros of the matrix sit close to the diagonal, so a banded solver can factor it cheaply. Starting at the edge makes the ripples many and thin, which keeps the band narrow.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ has a symmetric pattern, and $G = (V, E)$ is its graph: $V = \{0, \ldots, n - 1\}$ and $\{i, j\} \in E$ for each $a_{ij} \ne 0$, $i \ne j$, with $m = |E|$ and degrees $d(v)$. An ordering is a list $\pi$ of the vertices; vertex $\pi_k$ gets the new number $f(\pi_k) = k$, and the reordered matrix is $P A P^T$ with $(P A P^T)_{kl} = a_{\pi_k \pi_l}$. The bandwidth is $\beta_f = \max_{\{v, w\} \in E} |f(v) - f(w)|$, and the envelope (profile) is $\sum_v (f(v) - \min(\{f(v)\} \cup \{f(w) : w \sim v\}))$.

The goal is an ordering with small $\beta_f$ and small envelope, so that a banded or envelope [Cholesky](/cholesky-decomposition/) of $P A P^T$, which creates [fill](/fill-in/) only inside the band, is cheap.

A level structure rooted at $r$ is the partition of the component of $r$ into $L_0 = \{r\}, L_1, \ldots, L_e$, where $L_i$ is the set of vertices at distance $i$ from $r$; $e$ is the eccentricity of $r$ and $w = \max_i |L_i|$ the width.

## The algorithm

```pseudo id=main
CUTHILL-MCKEE(G)
L1  seen[v] ← false for all v; π ← empty list
L2  for each vertex s with seen[s] = false, in order of increasing (d(s), s) do
L3      r ← PSEUDO-PERIPHERAL(G, s)
L4      seen[r] ← true; append r to π
L5      head ← |π| − 1
L6      while head < |π| do
L7          v ← π[head]; head ← head + 1
L8          N ← the unseen neighbours of v, sorted by (d(w), w)
L9          for w in N do seen[w] ← true; append w to π
L10 return π
```

PSEUDO-PERIPHERAL$(G, s)$ is the George-Liu (1979) heuristic: build the level structure from $r = s$; take $x$ of minimum degree in the last level; if the level structure from $x$ has more levels than that of $r$, set $r \leftarrow x$ and repeat; otherwise return $r$. It returns a vertex of nearly maximum eccentricity, which tends to give many narrow levels. Lines L2 to L9 process the components one after another, so each component gets a contiguous block of numbers.

## Example

Take the 6-cycle with edges $\{0, 3\}, \{3, 4\}, \{4, 1\}, \{1, 2\}, \{2, 5\}, \{5, 0\}$. In the given numbering the edge $\{0, 5\}$ gives bandwidth $5$, so the matrix has entries in its corners. Every degree is $2$, so line L2 starts at $s = 0$. From $0$ the levels are $\{0\}, \{3, 5\}, \{4, 2\}, \{1\}$; from the last level's vertex $1$ there are also $4$ levels, so the pseudo-peripheral search returns $r = 0$.

| step | $v$ | unseen neighbours, sorted | $\pi$ |
|---|---|---|---|
| L4 | | | $0$ |
| 1 | $0$ | $3, 5$ | $0, 3, 5$ |
| 2 | $3$ | $4$ | $0, 3, 5, 4$ |
| 3 | $5$ | $2$ | $0, 3, 5, 4, 2$ |
| 4 | $4$ | $1$ | $0, 3, 5, 4, 2, 1$ |
| 5, 6 | $2, 1$ | none | |

The new numbers are $f(0) = 0, f(3) = 1, f(5) = 2, f(4) = 3, f(2) = 4, f(1) = 5$, and the edges now have differences $1, 2, 2, 1, 2, 2$: bandwidth $2$, which is optimal for a cycle. The level widths are $1, 2, 2, 1$, and the bound of Theorem 3 below is $2 + 2 - 1 = 3$.

## Correctness

The full proofs are in `proofs/correctness.md`. The statements:

1. **Permutation and termination.** The output lists every vertex exactly once, and the pseudo-peripheral search stops after at most $n$ searches.
2. **Characterization.** Within each component, the numbering follows the level structure from its root $r$ (all of $L_i$ before any of $L_{i+1}$), and after $r$ the vertices appear in increasing order of the key $(f(\text{first numbered neighbour}), d(v), v)$. This determines the ordering uniquely given the roots.
3. **Bandwidth bound.** $\beta_f \le \max_i (|L_i| + |L_{i+1}|) - 1 \le 2 w - 1$ for each component's level structure.

The bound uses only the level structure, which is why a root with many narrow levels helps. The degree rule at line L8 has no effect on the bound; it is a heuristic that numbers low degree vertices first so that later levels are not widened by their many neighbours.

## Complexity

With adjacency lists, lines L6 to L9 visit each vertex once and each edge twice, and the sort at line L8 costs $O(d(v) \log d(v))$ per vertex, so $O(m \log \Delta)$ in total; the sort at line L2 adds $O(n \log n)$. A counting sort by degree reduces the numbering to $O(n + m)$. Each search in PSEUDO-PERIPHERAL costs $O(n + m)$ on the component, and the number of levels strictly increases with each accepted move, so there are at most $e + 1 \le n$ searches: $O(n(n + m))$ in the worst case. In practice the search stops after two to five passes, and the whole ordering costs a small multiple of one BFS. The extra space is $\Theta(n)$ for the flags, the queue (which is $\pi$ itself) and one level structure. Proofs are in `proofs/complexity.md`.

## Properties

- **Deterministic** with the tie rules stated (degree, then index).
- **Bandwidth is preserved by reversal**: $f$ and $n - 1 - f$ give the same $\beta$, but the envelope changes, and Liu and Sherman (1976) proved the reversed one is never larger.
- **No approximation guarantee.** On a star $K_{1, n-1}$ the algorithm starts at a leaf, numbers the centre $1$, and gets bandwidth $n - 2$, while placing the centre in the middle gives $\lceil (n - 1)/2 \rceil$.
- **Exact on paths and cycles**: bandwidth $1$ and $2$, from any labelling.
- **On a $k \times k$ grid** started at a corner it numbers by anti-diagonals: bandwidth $k$ (optimal) and a smaller profile than the row by row order (for $k = 8$, $364$ against $455$).
- **Fill stays in the envelope**: Cholesky of the reordered matrix has no nonzero to the left of the first nonzero of each row, a property of every ordering that the tests check exactly.

## Variants and improvements

- **[Reverse Cuthill-McKee](/reverse-cuthill-mckee/)** (George 1971). Reverse $\pi$. Same bandwidth, envelope never larger, and usually much smaller; the default in MATLAB's `symrcm`, SciPy's `reverse_cuthill_mckee` and Boost.
- **Gibbs-Poole-Stockmeyer** (1976). Finds both ends of a pseudo-diameter and merges the two level structures into one of smaller width, giving similar or smaller bandwidth with less time in the root search.
- **King's algorithm and Sloan's algorithm.** Number vertices to minimize the growth of the active front (wavefront) rather than in pure BFS order; better for profile and frontal solvers.
- **Spectral orderings.** Sort the vertices by the entries of the Fiedler vector of the graph Laplacian; often smaller envelopes for mesh problems (Barnard, Pothen and Simon 1995).
- **Unsymmetric patterns.** Apply the algorithm to the pattern of $A + A^T$, or to the bipartite graph of $A$ to get separate row and column orders.

## When to use it

Use RCM (not plain CM) when the matrix will be factored by a banded or envelope solver, when you want a cheap ordering for an [incomplete factorization](/incomplete-cholesky-factorization/) preconditioner, or to improve cache locality of sparse matrix-vector products in Krylov methods. For a general sparse direct solve, [minimum degree](/minimum-degree-ordering/) or [nested dissection](/nested-dissection/) give much less fill on 2D and 3D meshes (on a $k \times k$ grid, $\Theta(n^{3/2})$ entries in $L$ for any band ordering against $\Theta(n \log n)$ for nested dissection). For thin domains, such as long strips or 1D-like meshes, band orderings are close to optimal.

## Pitfalls

- **Bad start vertex.** Starting at a central vertex gives fewer, wider levels and usually a larger bandwidth. Always use a pseudo-peripheral root.
- **Using CM instead of RCM for factorization.** CM can have a much larger envelope, and envelope solvers pay for every entry in it. Reverse the order.
- **Disconnected graphs.** A single BFS numbers only one component. Loop over components, as line L2 does, or isolated vertices are lost.
- **Applying it to an unsymmetric pattern directly.** The BFS needs undirected edges; symmetrize the pattern first.
- **Expecting optimal bandwidth.** The problem is NP-hard and CM has bad cases (stars, and graphs with a few high degree hubs). Check the result against the lower bound $\lceil \Delta/2 \rceil$ when it matters.
- **Confusing new and old indices.** $\pi_k$ is the old index of new number $k$; the permuted matrix is `A[π][:, π]`, and its inverse permutation is $f$.

## Implementations

## History

Elizabeth Cuthill and James McKee, working on structural analysis at the David Taylor Model Basin, published the method at the 1969 ACM National Conference. Alan George, in his 1971 Stanford thesis on the finite element method, observed that reversing the ordering gives a much smaller envelope, and Liu and Sherman (1976) proved that the reversal never increases it. George and Liu (1979) gave the pseudo-peripheral node finder used in most implementations, and their 1981 book made RCM the standard envelope ordering. Gibbs, Poole and Stockmeyer (1976) gave the main alternative. The bandwidth problem itself was shown NP-complete by Papadimitriou in 1976.

## References
