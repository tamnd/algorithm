---
tag: 36W80E
kind: algorithm
slug: reverse-cuthill-mckee
name: Reverse Cuthill-McKee algorithm
aliases:
- RCM
- reverse Cuthill-McKee ordering
area: numerical/linear-systems
level: advanced
summary: Cuthill-McKee with the order reversed, which often reduces fill-in as well.
solves: [bandwidth-reduction]
model: word-ram
complexity:
  vars: {n: "the number of vertices (unknowns)", m: "the number of edges (off-diagonal pairs)", d: "the largest degree"}
  time: {worst: O(n (n + m)), best: O(n + m log d)}
  space: {extra: Θ(n)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [cuthill-mckee, fill-in]
see_also: [bandwidth-reduction, banded-matrix, fill-reducing-ordering, minimum-degree-ordering, nested-dissection, cholesky-decomposition, incomplete-cholesky-factorization, sparse-linear-systems]
sources:
  - paper: doi:10.1137/0713020
    title: Wai-Hung Liu and Andrew H. Sherman, Comparative analysis of the Cuthill-McKee and the reverse Cuthill-McKee ordering algorithms for sparse matrices, SIAM Journal on Numerical Analysis 13(2), 1976
    locator: the theorem that the reversed ordering never has a larger envelope or envelope factorization cost
  - paper: doi:10.1145/800195.805928
    title: E. Cuthill and J. McKee, Reducing the bandwidth of sparse symmetric matrices, Proceedings of the 24th ACM National Conference, 1969
    locator: the level-structure ordering that RCM reverses
  - paper: doi:10.1145/355841.355845
    title: Alan George and Joseph W. H. Liu, An implementation of a pseudoperipheral node finder, ACM Transactions on Mathematical Software 5(3), 1979
    locator: the start vertex heuristic used at line L4
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 7, Fill-reducing orderings (the section on bandwidth and profile reduction)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 3.3, Permutations and Reorderings (level-set orderings, Cuthill-McKee and reverse Cuthill-McKee)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (the backward error bound, which does not depend on the symmetric ordering)
---

Reverse Cuthill-McKee (RCM) reorders the unknowns of a sparse symmetric matrix by a breadth-first search from a pseudo-peripheral vertex, numbering the neighbours of each vertex by increasing degree as in [Cuthill-McKee](/cuthill-mckee/), and then reverses the list. Reversal keeps the bandwidth, which is less than twice the widest BFS level, but makes the envelope never larger and usually much smaller (Liu and Sherman, 1976), so a banded or envelope [Cholesky](/cholesky-decomposition/) of the reordered matrix stores fewer entries and does fewer flops. It runs in nearly linear time, is the default bandwidth ordering in MATLAB, SciPy and Boost, and is a cheap ordering for incomplete factorizations and for the memory locality of sparse products.

## In plain words

Number the unknowns in waves spreading out from one end of the problem, so that connected unknowns get close numbers and the matrix entries hug the diagonal. Then turn the numbering around, so the last wave becomes the first. The band stays exactly as narrow, but the shape inside it changes: the rows that reach far back now come late, where they cause less work. When the matrix is factored, fewer zeros turn into nonzeros, and the factorization takes less memory and time.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ has a symmetric pattern; its graph $G = (V, E)$ has a vertex per row and an edge $\{i, j\}$ for each $a_{ij} \ne 0$, $i \ne j$, with $m = |E|$ edges and largest degree $d$. An ordering $\sigma$ gives vertex $\sigma_k$ the new number $k$; the reordered matrix is $P A P^T$ with $(P A P^T)_{kl} = a_{\sigma_k \sigma_l}$. For row $i$ of $P A P^T$, $\phi_i$ is the column of its first nonzero, $\rho_i = i - \phi_i$, the bandwidth is $\beta = \max_i \rho_i$, and the envelope is $\mathrm{Env} = \sum_i \rho_i$. For the numerical factorization: $u = 2^{-53}$, $\gamma_k = k u/(1 - k u)$, and $\hat R$ is the computed Cholesky factor.

**Input.** The graph $G$ (the pattern of $A$; values are not used).

**Output.** An ordering $\sigma$ with small bandwidth and envelope, to be used for $P A P^T$. The goal is cheap factorization: [fill](/fill-in/) of the Cholesky factor lies inside the envelope (proved below), so an envelope solver needs $\mathrm{Env} + n$ words and about $\sum_i \rho_i^2$ flops. Minimizing the bandwidth or the envelope exactly is NP-hard (see [bandwidth reduction](/bandwidth-reduction/)), so RCM is a heuristic.

## The algorithm

```pseudo id=main
REVERSE-CUTHILL-MCKEE(G)
L1  order ← empty list;  all vertices unnumbered
L2  for each vertex s in order of increasing degree do      ▷ one pass per component
L3      if s is numbered then continue
L4      r ← PSEUDO-PERIPHERAL(G, s)                           ▷ George and Liu: repeated BFS
L5      append r to order;  number r
L6      for each vertex v of order, from r on, in order do      ▷ order doubles as the BFS queue
L7          N ← the unnumbered neighbours of v, by increasing degree
L8          append N to order;  number each vertex of N
L9  reverse order
L10 return order                                             ▷ vertex order[k] gets number k
```

Lines L1 to L8 are the Cuthill-McKee algorithm; only line L9 is new. PSEUDO-PERIPHERAL starts a breadth-first search at $s$, moves to a vertex of least degree in the last level, and repeats while the number of levels grows; it ends at a vertex of nearly maximal eccentricity, which makes the levels many and narrow.

## Example

**A star.** Let vertex 0 be joined to vertices 1 to 5 (an arrow matrix). Cuthill-McKee starts at the leaf 1, a pseudo-peripheral vertex, and gives $\pi = (1, 0, 2, 3, 4, 5)$; RCM gives $\pi^R = (5, 4, 3, 2, 0, 1)$. Both have bandwidth 4.

| ordering | bandwidth | envelope | nonzeros of $L$ below the diagonal | Cholesky flops $\sum_k c_k^2$ |
|---|---|---|---|---|
| natural, centre first | 5 | 15 | 15 | 55 |
| Cuthill-McKee | 4 | 11 | 11 | 31 |
| reverse Cuthill-McKee | 4 | 5 | 5 | 5 |

In the CM order the centre is eliminated second and joins the four remaining leaves into a clique, 6 new entries. In the RCM order the leaves go first, each has a single later neighbour, and there is no fill at all.

**A mesh-like graph.** 400 random points in the unit square, joined when closer than $0.0775$ ($m = 1391$ edges), numbered at random:

| ordering | bandwidth | envelope | nonzeros of $L$ | Cholesky flops |
|---|---|---|---|---|
| random numbering | 393 | 61454 | 14060 | 949044 |
| Cuthill-McKee | 40 | 8491 | 8491 | 217363 |
| reverse Cuthill-McKee | 40 | 6571 | 4446 | 66062 |

Same bandwidth, a 23 percent smaller envelope, and half the nonzeros and less than a third of the flops of CM. In the CM order every envelope entry fills; in the RCM order many stay zero. On the $k \times k$ grid started from a corner, CM and RCM coincide up to the symmetry of the grid (bandwidth $k$; for $k = 8$, envelope 364 against 455 for the row-by-row order).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Every vertex is appended exactly once, so the result is a permutation. Breadth-first search numbers each component level by level, and each edge joins the same or adjacent levels, so the bandwidth is at most $2w - 1$ for the largest level width $w$; reversal maps $k \mapsto n - 1 - k$ and preserves all differences, hence the bandwidth. For every ordering, the Cholesky factor has $l_{ij} = 0$ for $j < \phi_i$, so fill stays in the envelope (George). Liu and Sherman (1976) proved that $\mathrm{Env}(\pi^R) \le \mathrm{Env}(\pi)$ for every Cuthill-McKee ordering $\pi$, with the same inequality for the cost of envelope factorization; the proof file cites this result, and the tests check it on 300 random graphs.

**Numerical stability.** RCM changes only the order of elimination. For symmetric positive definite $A$, Cholesky of $P A P^T$ is backward stable for every $P$: if it runs to completion, $(P A P^T + \Delta A)\hat x' = P b$ with $|\Delta A| \le \gamma_{3n+1}|\hat R^T||\hat R|$ (Higham, Chapter 10), and $\kappa_2(P A P^T) = \kappa_2(A)$. In a band or envelope factorization each inner product has at most $\beta + 1$ terms, and the same proof then gives the bound with a constant depending on $\beta$ instead of $n$. For nonsymmetric $A$ with partial pivoting, row interchanges can widen the upper band of $U$ up to the sum of the lower and upper bandwidths.

## Complexity

One breadth-first search with sorting of each neighbour list costs $O(n + m\log d)$, or $O(n + m)$ with bucket sorting by degree. The pseudo-peripheral search repeats breadth-first searches while the eccentricity grows, at most $n$ times in theory and usually two to five times in practice, so the total is $O(n(n + m))$ in the worst case and $O(n + m\log d)$ when the start search ends quickly. Extra space is $O(n)$ for the order, the marks and one level structure. Reversal costs $O(n)$.

The orderings feed the factorization costs above: envelope Cholesky needs $\mathrm{Env} + n$ words and about $\sum_i \rho_i^2$ flops, band Cholesky $n(\beta + 1)$ words and about $n\beta^2$ flops. On the $k \times k$ grid ($n = k^2$) RCM reaches $\beta = k$ and $\mathrm{Env} \approx n^{3/2}$, so about $n^2$ flops, which is far from the $O(n^{3/2})$ of [nested dissection](/nested-dissection/); bandwidth orderings are not the right tool when the factorization cost dominates on large 2D or 3D meshes.

## Properties

- **Same bandwidth as CM, envelope never larger** (Liu and Sherman), and nonzeros and flops of the general sparse factorization usually much smaller.
- **Purely structural.** It uses only the pattern, not the values, so it is computed once per pattern.
- **Fast.** Close to linear time; much cheaper than [minimum degree](/minimum-degree-ordering/) or nested dissection orderings.
- **Locality.** Neighbouring unknowns get nearby numbers, which improves cache reuse in sparse matrix-vector products and in Gauss-Seidel sweeps.
- **No guarantee.** There is no approximation bound for bandwidth or envelope; it can be far from optimal on graphs without a long, narrow level structure.

## Variants and improvements

- **Gibbs-Poole-Stockmeyer and Gibbs-King.** Build a level structure from both ends of a pseudo-diameter and combine them, often narrowing the levels; good for profile and band solvers.
- **Sloan's algorithm.** A priority-based numbering that balances distance from the end vertex against the current front size, usually giving smaller envelopes than RCM.
- **Spectral ordering.** Sort vertices by the Fiedler vector of the graph Laplacian; often a smaller envelope on meshes, at the cost of an eigenvector computation.
- **Unsymmetric matrices.** Apply RCM to the pattern of $A + A^T$, or to the bipartite graph of $A$ for a two-sided permutation.
- **Fill-reducing orderings.** For general sparse Cholesky, [minimum degree](/minimum-degree-ordering/) and [nested dissection](/nested-dissection/) give much less fill than any bandwidth ordering; see [fill-reducing ordering](/fill-reducing-ordering/).

## When to use it

Use RCM to prepare a matrix for a banded or envelope solver, to order unknowns for [incomplete Cholesky](/incomplete-cholesky-factorization/) or ILU preconditioners, where it often gives better preconditioners than the natural order, or to improve memory locality of iterative solvers. It is also a reasonable ordering for small and medium problems with a long, thin structure (beams, pipes, strips), where a band is natural. For large 2D or 3D problems solved by sparse direct methods, use minimum degree or nested dissection instead.

## Pitfalls

- **Using CM instead of RCM.** CM's envelope can be much larger; the star example shows 11 against 5, and fill 6 against 0.
- **A poor start vertex.** Starting in the middle of the graph gives fewer, wider levels and roughly doubles the bandwidth; use a pseudo-peripheral vertex.
- **Ignoring components.** Each component needs its own start; the loop at line L2 handles them, but code that does a single BFS misses vertices.
- **Unsymmetric patterns.** RCM needs a symmetric pattern; use $A + A^T$, and remember that partial pivoting can widen the band again.
- **Expecting optimal fill.** On large meshes, bandwidth orderings give $\Theta(n^2)$ Cholesky flops in 2D where nested dissection gives $\Theta(n^{3/2})$.

## Implementations

## History

Cuthill and McKee (1969) proposed the level-structure ordering to reduce bandwidth in structural analysis. Alan George, in his 1971 Stanford thesis, observed that reversing the Cuthill-McKee order gave much better envelope storage and factorization cost for finite element matrices. Liu and Sherman (1976) proved that the reversed ordering is never worse in envelope and envelope work. Gibbs, Poole and Stockmeyer (1976) gave an improved start vertex and level structure, and George and Liu (1979) the pseudo-peripheral vertex finder used today. The book of George and Liu (1981) made RCM the standard profile ordering.

## References
