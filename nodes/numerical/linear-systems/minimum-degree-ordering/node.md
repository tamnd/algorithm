---
tag: 3FDE64
kind: algorithm
slug: minimum-degree-ordering
name: Minimum degree ordering
aliases:
- approximate minimum degree
- AMD
- minimum degree algorithm
- Tinney scheme 2
area: numerical/linear-systems
level: research
summary: Greedily eliminate the vertex of smallest degree to limit fill-in.
solves: [fill-reducing-ordering]
model: word-ram
complexity:
  vars: {n: "the number of vertices (unknowns)", m: "the number of edges (off-diagonal pairs of A)"}
  time: {worst: O(n^2 m), best: O((n + m) log n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [fill-in, priority-queue]
see_also: [fill-reducing-ordering, nested-dissection, reverse-cuthill-mckee, elimination-tree, multifrontal-method, cholesky-decomposition, perfect-elimination-ordering, sparse-linear-systems]
sources:
  - paper: doi:10.1137/1031001
    title: Alan George and Joseph W. H. Liu, The evolution of the minimum degree ordering algorithm, SIAM Review 31(1), 1989
    locator: the elimination and quotient graph models, multiple elimination, mass elimination and external degree
  - paper: doi:10.1137/S0895479894278952
    title: Patrick R. Amestoy, Timothy A. Davis and Iain S. Duff, An approximate minimum degree ordering algorithm, SIAM Journal on Matrix Analysis and Applications 17(4), 1996
    locator: the approximate degree bound and element absorption
  - paper: doi:10.1109/PROC.1967.6011
    title: W. F. Tinney and J. W. Walker, Direct solutions of sparse network equations by optimally ordered triangular factorization, Proceedings of the IEEE 55(11), 1967
    locator: scheme 2, the minimum degree rule
  - paper: doi:10.1137/0602010
    title: Mihalis Yannakakis, Computing the minimum fill-in is NP-complete, SIAM Journal on Algebraic and Discrete Methods 2(1), 1981
    locator: the NP-completeness of minimum fill
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 7, Fill-reducing orderings (minimum degree and the quotient graph)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (the backward error bound, which does not depend on the symmetric ordering)
---

Minimum degree orders the unknowns of a sparse symmetric matrix for [Cholesky factorization](/cholesky-decomposition/) by always eliminating next the unknown with the fewest remaining neighbours in the elimination graph, since eliminating a vertex of degree $d$ can create at most $d(d - 1)/2$ fill entries and costs about $d^2$ flops. It is greedy, does not minimize fill (that problem is NP-hard), and has no approximation guarantee, but on most practical matrices it gives far less [fill](/fill-in/) than bandwidth orderings. The production form, approximate minimum degree (AMD), runs on a quotient graph that never needs more memory than the matrix and replaces exact degrees by cheap upper bounds; it is the default fill-reducing ordering in MATLAB, SuiteSparse and many direct solvers.

## In plain words

Solving a sparse system by elimination fills in some of the zero entries, and the order of elimination decides how many. Removing an unknown that is connected to only a few others links those few to each other and nothing more. So pick, at every step, the unknown with the fewest current connections, remove it, connect its neighbours, and repeat. The rule is short-sighted and can be beaten, but it is fast and usually good. Clever bookkeeping lets it run without ever writing down the new connections explicitly.

## The problem

**Notation.** $A \in \mathbb{R}^{n \times n}$ is symmetric positive definite with graph $G = (V, E)$, one vertex per row and an edge $\{i, j\}$ for each $a_{ij} \ne 0$, $i \ne j$, and $m = |E|$. An ordering $\sigma$ eliminates vertex $\sigma_k$ at step $k$; $P$ is the corresponding permutation, and $L$ is the Cholesky factor of $P A P^T = L L^T$. The elimination graphs are $G_0 = G$ and $G_k$, obtained by deleting $\sigma_k$ from $G_{k-1}$ and joining its neighbours into a clique; $d_{k-1}(v)$ is the degree of $v$ in $G_{k-1}$, and $c_k = d_{k-1}(\sigma_k)$ is the number of off-diagonal nonzeros in column $k$ of $L$. For the factorization in floating point: $u = 2^{-53}$, $\gamma_k = k u/(1 - k u)$, $\hat x$ is the computed solution and $\kappa_2(A) = \|A\|_2\|A^{-1}\|_2$.

**Input.** The pattern of $A$ as the graph $G$; values are not used.

**Output.** An ordering $\sigma$ with small $|L| = \sum_k c_k$ (memory of the factor) and small $\sum_k c_k^2$ (leading term of the flops of [sparse Cholesky](/cholesky-decomposition/), which is $\sum_k c_k^2 + O(|L|)$). Minimizing either exactly is NP-hard (Yannakakis, 1981). This page counts $\sum_k c_k^2$ as "flops".

## The algorithm

```pseudo id=main
MINIMUM-DEGREE(G)
L1  G_0 ← G;  put every vertex in a priority queue keyed by its degree
L2  for k ← 1 to n do
L3      v ← an uneliminated vertex of least degree in G_{k-1}       ▷ ties: smallest index
L4      append v to order
L5      N ← the neighbours of v in G_{k-1}
L6      G_k ← G_{k-1} with v deleted and N joined into a clique     ▷ the fill of step k
L7      update the keys of the vertices of N                          ▷ only their degrees change
L8  return order
```

The implementation keeps a binary heap with lazy deletion: line L7 pushes new pairs and stale pairs are skipped when popped. Writing the clique at line L6 explicitly costs time and memory proportional to the fill. The **quotient graph** avoids this: an eliminated vertex $p$ becomes an *element* with a variable list $L_p$ (the clique), and each remaining variable $i$ keeps a list $A_i$ of variable neighbours and a list $E_i$ of adjacent elements. Then the neighbours of $i$ in $G_k$ are $A_i \cup \bigcup_{e \in E_i} L_e$ minus $i$. When $p$ is eliminated, the elements adjacent to $p$ are *absorbed* into $L_p$, and the lists $A_i$ of the variables in $L_p$ are pruned. The storage never exceeds that of $G$ (proved). **AMD** replaces the exact degree of each $i \in L_p$, which needs a set union, by the bound
$$\bar d_i = \min\Big(r - 1,\ \bar d_i^{\,\mathrm{old}} + |L_p \setminus \{i\}|,\ |A_i| + |L_p \setminus \{i\}| + \sum_{e \in E_i \setminus \{p\}} |L_e \setminus L_p|\Big),$$
with $r$ the number of remaining variables. This value is never below the true degree and equals it when $i$ is adjacent to at most two elements. The sizes $|L_e \setminus L_p|$ for all $e$ can be computed in one pass over the lists of $L_p$.

## Example

**The $3 \times 3$ grid** (the 5-point Laplacian, vertices $0, \ldots, 8$ row by row). The corners have degree 2 and are eliminated first, $0, 2, 6, 8$, each joining its two neighbours (fill edges $\{1,3\}, \{1,5\}, \{3,7\}, \{5,7\}$). The edge midpoints now have degree 3 and the centre 4, so $1$ goes next (fill $\{3, 5\}$), then $3, 4, 5, 7$ with no further fill. The order $(0, 2, 6, 8, 1, 3, 4, 5, 7)$ has 5 fill entries, $|L| = 17$ off-diagonal nonzeros and $\sum c_k^2 = 39$. The natural row-by-row order gives 8 fill entries.

**Grids and a mesh.** Off-diagonal nonzeros of $L$ and flops $\sum_k c_k^2$, from the implementation; RCM is [reverse Cuthill-McKee](/reverse-cuthill-mckee/), AMD is the approximate degree version on the quotient graph. The last row is 400 random points in the unit square joined when closer than $0.0775$ ($m = 1391$).

| graph | natural | RCM | minimum degree | AMD |
|---|---|---|---|---|
| grid $8 \times 8$ | 455, 3479 | 364, 2324 | 295, 1629 | 296, 1638 |
| grid $16 \times 16$ | 3855, 60335 | 2840, 35240 | 1923, 21193 | 1893, 20203 |
| grid $24 \times 24$ | 13271, 313927 | 9476, 174524 | 5539, 91827 | 5443, 87783 |
| grid $32 \times 32$ | 31775, 1005919 | 22320, 545104 | 11308, 235950 | 11323, 240127 |
| random mesh, $n = 400$ | 14060, 949044 | 4446, 66062 | 2443, 19633 | 2443, 19633 |

On the $32 \times 32$ grid minimum degree has half the fill and less than half the flops of RCM, and the ratio grows with $k$: bandwidth orderings give $\Theta(n^{3/2})$ fill and $\Theta(n^2)$ flops on 2D grids, while minimum degree, observed, comes close to the $O(n \log n)$ and $O(n^{3/2})$ of [nested dissection](/nested-dissection/). The approximate degree changes the fill by less than 2 percent here.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Fill model.** By the result of Parter and Rose, column $k$ of $L$ has its nonzeros at the neighbours of $\sigma_k$ in $G_{k-1}$, barring exact cancellation. So $|L| = \sum_k c_k$, and line L6 adds exactly the fill. The tests compare the symbolic pattern with an exact rational $LDL^T$.
- **Output.** Every vertex is appended once. At each step the chosen vertex has least current degree.
- **Quotient graph.** Under the invariants of George and Liu, the reach sets equal the elimination-graph neighbourhoods. So the exact quotient version returns the same order as the explicit one with the same tie-breaking. Its storage $\sum |A_i| + \sum |L_e|$ never exceeds $2m$.
- **AMD bound.** The approximate degree is an upper bound, exact when at most two elements are adjacent.
- **Forests.** On a forest the rule produces no fill.
- **Not optimal.** Two 4-cliques joined through a vertex of degree 2 give fill 1 under minimum degree, while the graph is chordal with minimum fill 0.

**Numerical stability.** The ordering does not affect stability for symmetric positive definite $A$:
- Cholesky of $P A P^T$ runs to completion for every $P$ when $20 n^{3/2}\kappa_2(A) u \le 1$, a sufficient condition (Higham, Chapter 10).
- The computed solution then satisfies $(A + \Delta A)\hat x = b$ with $|\Delta A| \le \gamma_{3n+1} P^T|\hat R^T||\hat R|P$ (Higham, Chapter 10).
- So $\|x - \hat x\|_2/\|x\|_2 \lesssim c_n \kappa_2(A) u$ with a modest $c_n$.
- Fewer nonzeros also means shorter inner products: the constant depends on the longest column count rather than on $n$, and there are fewer rounding errors in total.

For unsymmetric $A$, minimum degree is applied to the pattern of $A^T A$ (COLAMD) or combined with pivoting by the Markowitz rule. The pivoting there is threshold partial pivoting: a pivot is accepted if it is at least $\tau$ times the largest entry in its column, with $0 < \tau \le 1$. Then $|l_{ij}| \le 1/\tau$, and the same argument as for partial pivoting bounds the growth factor by $\rho_n \le (1 + 1/\tau)^{n-1}$, a worst-case bound. Lowering $\tau$ buys sparsity with stability.

## Complexity

- **Explicit elimination graph.** Writing the cliques costs time proportional to $\sum_k c_k^2$, the flop count of the factorization itself, plus $O((n + |L|)\log n)$ for the heap. Memory is $O(m + |L|)$. On a forest, or any matrix with no fill, this is $O((n + m)\log n)$.
- **Quotient graph, exact degree.** Storage is $O(n + m)$, proved above. Recomputing exact degrees can cost $O(n^2 m)$ in the worst case (Heggernes, Eisenstat, Kumfert and Pothen, 2001).
- **AMD.** Its degree updates cost $O(|A_i| + |E_i|)$ per variable, and its worst case is $O(n m)$ (the same authors). In practice AMD runs in time close to $O(|L|)$ and is usually much cheaper than the numerical factorization.
- **Accelerations.** The large constant factors are cut by three devices: supervariables (indistinguishable vertices handled together), mass and multiple elimination, and element absorption.

The orderings then decide the factorization cost. That cost is often limited by memory traffic rather than flops, which is why the elimination is then reorganized into dense blocks by [multifrontal](/multifrontal-method/) or supernodal methods. On the $k \times k$ grid, no ordering beats $\Omega(n \log n)$ fill and $\Omega(n^{3/2})$ flops (Hoffman, Martin and Rose). Nested dissection attains both orders. Minimum degree has no such guarantee, and there are graph families where it is far from optimal.

## Properties

- **Greedy and local.** Each step minimizes the immediate fill bound $c_k(c_k - 1)/2$ and the step cost $c_k^2$, not the total.
- **Structural.** It uses only the pattern, so it is computed once per pattern and reused for every factorization with that pattern.
- **Tie-breaking matters.** Different tie rules can change fill noticeably; the initial numbering acts as the tie-breaker.
- **Exact on forests**, and observed to be optimal on most tiny random graphs in the tests, but not always.
- **Approximate degree** is an upper bound, exact with at most two adjacent elements, and gives fill within a few percent of exact degrees in practice.

## Variants and improvements

- **Markowitz criterion** (1957). For unsymmetric matrices, choose the pivot minimizing $(r_i - 1)(c_j - 1)$, the product of its row and column counts, subject to a threshold pivoting test.
- **Multiple minimum degree** (Liu, 1985). Eliminate an independent set of vertices of minimum degree before updating degrees; much faster, slightly different fill.
- **External degree and supervariables.** Count the degree of a supervariable excluding itself, and merge indistinguishable vertices; both are standard in MMD and AMD.
- **AMD and COLAMD** (Amestoy, Davis and Duff, 1996; Davis, Gilbert, Larimore and Ng, 2004). The approximate degree, and its column version for $A^T A$ in LU and QR.
- **Minimum deficiency (minimum fill).** Choose the vertex whose elimination adds the fewest fill edges. Often less fill, but much more expensive; approximate versions (AMF) exist.
- **Hybrids.** Nested dissection on the top levels and minimum degree on the small subgraphs (as in METIS), or constrained minimum degree on the separators.

## When to use it

Use AMD as the default ordering for sparse Cholesky and $LDL^T$ of small and medium 2D problems, circuit and network matrices, and matrices without geometric structure. Use COLAMD for sparse LU or QR. For large 3D meshes, nested dissection usually gives less fill and much better parallelism. For banded or envelope solvers, or for locality in iterative methods, use [RCM](/reverse-cuthill-mckee/).

## Pitfalls

- **Explicit cliques.** Implementing line L6 literally needs memory proportional to the fill. Production codes use the quotient graph.
- **Exact degree updates.** Recomputing exact degrees after every elimination is the main cost of naive codes. Use approximate or external degrees and multiple elimination.
- **Dense rows.** A few dense rows make every neighbour's degree large and slow the algorithm. Remove rows with more than about $10\sqrt n$ entries, order them last, and order the rest.
- **Expecting optimality.** It is a heuristic with no approximation bound. On large 3D problems nested dissection is often much better.
- **Unsymmetric pivoting.** For LU, a fill-reducing column order can be destroyed by row pivoting. Use threshold partial pivoting and accept some loss of sparsity.

## Implementations

## History

Markowitz (1957) introduced the pivot rule that bears his name for sparse LU in linear programming. Tinney and Walker (1967) proposed the symmetric minimum degree rule (their "scheme 2") for power network equations. Rose (1972) gave the graph model of elimination, after Parter (1961). George and Liu developed the quotient graph and the efficient implementations of the late 1970s and 1980s, including Liu's multiple minimum degree (1985), and surveyed the field in 1989. Amestoy, Davis and Duff (1996) introduced the approximate degree, which made AMD the standard. Yannakakis (1981) proved that minimum fill is NP-complete.

## References
