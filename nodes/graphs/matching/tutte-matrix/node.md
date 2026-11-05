---
tag: WVHG9P
kind: definition
slug: tutte-matrix
name: Tutte matrix
aliases:
- skew-symmetric matching matrix
area: graphs/matching
level: advanced
summary: Skew-symmetric matrix with random variables whose determinant is nonzero iff a perfect matching exists.
prereqs: [determinant, perfect-matching]
see_also: [schwartz-zippel-lemma, rnc-perfect-matching, tutte-theorem, polynomial-identity-testing, counting-perfect-matchings, rank, maximum-matching, matrix-multiplication-exponent]
sources:
  - paper: doi:10.1112/jlms/s1-22.2.107
    title: William T. Tutte, The factorization of linear graphs, Journal of the London Mathematical Society 22(2), 107 to 111 (1947)
    locator: the whole paper (the matrix and its Pfaffian)
  - paper: "László Lovász, On determinants, matchings, and random algorithms, Fundamentals of Computation Theory (FCT 1979), Akademie-Verlag Berlin, 565 to 574 (1979)"
    locator: the whole paper (random substitution, and the rank of the matrix equals twice the matching number)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press
    locator: Chapter 7, Algebraic Techniques (the Tutte matrix and the randomized test for perfect matchings)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing
    locator: Chapter 8, Determinants and matchings
---

The Tutte matrix of a graph is a skew-symmetric matrix with one variable for each edge. Its [determinant](/determinant/) is a [polynomial](/polynomial/) that is not identically zero if and only if the graph has a [perfect matching](/perfect-matching/). If random numbers replace the variables, the determinant is nonzero with high probability exactly when a perfect matching exists. This gives a simple randomized test, and it is the basis of the [randomized parallel algorithm](/rnc-perfect-matching/) for perfect matching.

## Definition

Let $G = (V, E)$ be a finite undirected graph, general and without weights, with vertices $1, \ldots, n$ and no self-loops. For each edge $ij$ with $i < j$, take an independent variable $x_{ij}$. The **Tutte matrix** $T = T(G)$ is the $n \times n$ matrix with entries
$$T_{ij} = \begin{cases} x_{ij} & \text{if } ij \in E \text{ and } i < j, \\ -x_{ji} & \text{if } ij \in E \text{ and } i > j, \\ 0 & \text{otherwise.} \end{cases}$$
So $T^{\mathsf T} = -T$: the matrix is skew-symmetric, with zeros on the diagonal. Parallel edges give the same entry as one edge.

**Theorem (Tutte, 1947).** $\det T$ is not the zero polynomial if and only if $G$ has a perfect matching.

*Proof sketch.* Write $\det T = \sum_{\sigma} \operatorname{sgn}(\sigma) \prod_{i} T_{i \sigma(i)}$ over the permutations $\sigma$ of $V$. A term is nonzero only if $i\sigma(i) \in E$ for each $i$, so $\sigma$ is a cover of $V$ by directed cycles along edges. Pair each $\sigma$ that has an odd cycle with the permutation $\sigma'$ that reverses the odd cycle containing the least vertex among the vertices on odd cycles. Reversing an odd cycle keeps the sign of $\sigma$ and changes the sign of an odd number of entries, so the two terms cancel. The terms that remain have only even cycles. If $G$ has no perfect matching, no cover by even cycles and 2-cycles exists, since each even cycle splits into two matchings; so $\det T = 0$. If $G$ has a perfect matching $M$, the permutation that swaps the ends of each edge of $M$ gives the monomial $\prod_{ij \in M} x_{ij}^2$ with coefficient 1. No other surviving permutation gives this monomial, so it does not cancel. $\square$

**Pfaffian.** For a skew-symmetric matrix of even order, $\det T = \operatorname{Pf}(T)^2$, where
$$\operatorname{Pf}(T) = \sum_{M} \pm \prod_{ij \in M} x_{ij}$$
is a sum over the perfect matchings $M$ of $G$, each with a sign. The monomials of different matchings differ, so $\operatorname{Pf}(T) \ne 0$ exactly when a perfect matching exists. For $n$ odd, $\det T = \det T^{\mathsf T} = (-1)^n \det T$, so $\det T = 0$.

**Rank.** Lovász proved that the [rank](/rank/) of $T$ over the field of rational functions is $2\nu(G)$, where $\nu(G)$ is the size of a [maximum matching](/maximum-matching/).

**Random substitution.** $\det T$ has degree $n$. Replace each variable by an element chosen uniformly from a set $X$ of field elements. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), if $\det T$ is not zero as a polynomial, the value is 0 with probability at most $n / |X|$. If $G$ has no perfect matching, the value is always 0. So a computation of one numeric determinant, in $O(n^{\omega})$ field operations, decides the existence of a perfect matching with one-sided error. Over a prime field $\mathbb{Z}_p$ with $p \ge 2n$, the error is at most $1/2$ per trial, and independent trials make it as small as needed.

## Examples and non-examples

**One edge.** For $V = \{1, 2\}$ and $E = \{12\}$,
$$T = \begin{pmatrix} 0 & x_{12} \\ -x_{12} & 0 \end{pmatrix}, \qquad \det T = x_{12}^2, \qquad \operatorname{Pf}(T) = x_{12}.$$

**The 4-cycle.** For the cycle $1 - 2 - 3 - 4 - 1$,
$$T = \begin{pmatrix} 0 & x_{12} & 0 & x_{14} \\ -x_{12} & 0 & x_{23} & 0 \\ 0 & -x_{23} & 0 & x_{34} \\ -x_{14} & 0 & -x_{34} & 0 \end{pmatrix}.$$
The Pfaffian of a $4 \times 4$ skew-symmetric matrix is $T_{12} T_{34} - T_{13} T_{24} + T_{14} T_{23}$, which here is $x_{12} x_{34} + x_{14} x_{23}$, one term for each of the two perfect matchings $\{12, 34\}$ and $\{14, 23\}$. So $\det T = (x_{12} x_{34} + x_{14} x_{23})^2 \ne 0$.

**The path $1 - 2 - 3 - 4$.** The entries $T_{13}$, $T_{24}$ and $T_{14}$ are 0, so $\operatorname{Pf}(T) = x_{12} x_{34}$: the only perfect matching.

**Graphs with no perfect matching.**

- The star with center 1 and leaves 2, 3, 4: every term of the Pfaffian $T_{12} T_{34} - T_{13} T_{24} + T_{14} T_{23}$ has a factor between two leaves, which is 0. So $\det T = 0$.
- An odd cycle, or any graph with an odd number of vertices: $\det T = 0$, since $T$ is skew-symmetric of odd order.
- The graph with no vertices: $T$ is the empty matrix, its determinant is 1, and the empty matching is perfect.

**Non-example: substituting 1 for every variable.** Then the Pfaffian counts the perfect matchings with signs, and the signs can cancel. Number the 4-cycle as $1 - 2 - 4 - 3 - 1$, so its edges are $12$, $24$, $34$ and $13$. With every variable equal to 1, $\operatorname{Pf} = T_{12} T_{34} - T_{13} T_{24} + T_{14} T_{23} = 1 - 1 + 0 = 0$, although the graph has the two perfect matchings $\{12, 34\}$ and $\{13, 24\}$. In the bipartite version below, the 4-cycle with all entries 1 gives the matrix $\begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$ with determinant 0 as well. This is why the variables, or random values, are needed.

**Non-example: the adjacency matrix.** The adjacency matrix is symmetric, not skew-symmetric, and its determinant does not detect perfect matchings: for the 4-cycle it is 0.

## Related definitions

- **Edmonds matrix.** For a [bipartite graph](/bipartite-graph/) with sides $L = \{u_1, \ldots, u_k\}$ and $R = \{w_1, \ldots, w_k\}$, the $k \times k$ matrix $A$ with $A_{ij} = x_{ij}$ if $u_i w_j \in E$ and 0 otherwise. Its determinant is $\sum_{M} \pm \prod_{u_i w_j \in M} x_{ij}$ over the perfect matchings, so it is nonzero exactly when a perfect matching exists. The Tutte matrix of a bipartite graph is $\begin{pmatrix} 0 & A \\ -A^{\mathsf T} & 0 \end{pmatrix}$ up to the order of the vertices.
- **Permanent.** The same sum without signs, $\operatorname{per}(A)$ for the 0-1 biadjacency matrix, counts the perfect matchings of a bipartite graph. It is #P-complete to compute; see [counting perfect matchings](/counting-perfect-matchings/).
- **Pfaffian orientations.** For a [planar graph](/planar-graph/), Kasteleyn showed how to choose the signs of the entries so that all terms of the Pfaffian have the same sign. Then the Pfaffian of a numeric matrix counts the perfect matchings in polynomial time.
- **Weighted version.** Replacing $x_{ij}$ by $2^{w_{ij}}$ for edge weights $w_{ij}$ makes the largest power of 2 that divides $\det T$ equal to $2^{2W}$, where $W$ is the weight of a minimum-weight perfect matching, when that matching is unique. With random weights, the isolation lemma makes it unique with probability at least $1/2$; this is the [algorithm of Mulmuley, Vazirani and Vazirani](/rnc-perfect-matching/).
- **[Polynomial identity testing](/polynomial-identity-testing/).** Deciding whether $\det T$ is the zero polynomial is an instance of this problem. Matching algorithms decide it in deterministic polynomial time, but a deterministic algorithm in [NC](/nc/) for it is open. Fenner, Gurjar and Thierauf for bipartite graphs, and Svensson and Tarnawski for general graphs, gave deterministic algorithms with quasi-polynomially many processors.

## References
