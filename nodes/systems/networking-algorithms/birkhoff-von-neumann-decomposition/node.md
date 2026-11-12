---
tag: YCNDFQ
kind: theorem
slug: birkhoff-von-neumann-decomposition
name: Birkhoff-von Neumann decomposition
aliases:
- Birkhoff-von Neumann theorem
- Birkhoff theorem on doubly stochastic matrices
area: systems/networking-algorithms
level: advanced
summary: "Every doubly stochastic matrix is a convex combination of at most (N-1)^2+1 permutation matrices. A switch can serve any admissible rate matrix by a schedule of matchings."
prereqs: [hall-theorem, perfect-matching, convex-polytope]
see_also: [switch-scheduling, konig-theorem, edge-coloring, matching-polytope, caratheodory-theorem, assignment-problem, kuhn-algorithm, islip]
sources:
  - paper: "Garrett Birkhoff, Tres observaciones sobre el álgebra lineal, Universidad Nacional de Tucumán, Revista, Serie A 5 (1946), 147-151"
    locator: the theorem that the doubly stochastic matrices are the convex hull of the permutation matrices
  - paper: "John von Neumann, A certain zero-sum two-person game equivalent to the optimal assignment problem, in H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press (1953), 5-12"
    locator: an independent proof, used to show that the assignment problem has an optimal solution at a permutation
  - paper: "Marvin Marcus and Rimhak Ree, Diagonals of doubly stochastic matrices, Quarterly Journal of Mathematics 10 (1959), 296-302"
    locator: the bound N^2 - 2N + 2 on the number of permutation matrices that are needed
  - paper: "Cheng-Shang Chang, Wen-Jyh Chen and Hsiang-Yi Huang, Birkhoff-von Neumann input buffered crossbar switches, Proceedings of IEEE INFOCOM 2000, 1614-1623"
    locator: the BvN switch, which completes the rate matrix to a doubly stochastic matrix, decomposes it, and schedules the permutations with rate guarantees and no speedup
  - paper: "Fanny Dufossé and Bora Uçar, Notes on Birkhoff-von Neumann decomposition of doubly stochastic matrices, Linear Algebra and its Applications 497 (2016), 108-115"
    locator: the NP-hardness of finding a decomposition with the fewest permutation matrices, and greedy heuristics
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer, 2003
    locator: Chapter 18, Bipartite matching polytope (Birkhoff's theorem as the perfect matching polytope of the complete bipartite graph)
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 13, switching (input-queued crossbars and their schedulers)
---

The Birkhoff-von Neumann theorem says that every doubly stochastic matrix, a square matrix with nonnegative entries whose rows and columns each sum to 1, is a weighted average of permutation matrices. The proof is an algorithm: by [Hall's theorem](/hall-theorem/) the positive entries always contain a [perfect matching](/perfect-matching/), so we can subtract a multiple of a permutation matrix and repeat. At most $(N-1)^2 + 1$ permutations are needed, and that number is needed for most matrices. In [switch scheduling](/switch-scheduling/), the theorem shows that a crossbar can serve any admissible rate matrix with no speedup: decompose the rates and use each matching for its share of the time slots.

## Statement

An $N \times N$ real matrix $M$ is **doubly stochastic** if $m_{ij} \ge 0$ for all $i, j$, and $\sum_j m_{ij} = 1$ for each row $i$ and $\sum_i m_{ij} = 1$ for each column $j$. A **permutation matrix** $P_\sigma$, for a permutation $\sigma$ of $\{1, \ldots, N\}$, has a 1 in entry $(i, \sigma(i))$ for each $i$ and 0 elsewhere. The set of doubly stochastic matrices is the **Birkhoff polytope** $B_N$.

**Theorem (Birkhoff 1946, von Neumann 1953).** Every doubly stochastic matrix $M$ is a convex combination of permutation matrices:

$$M = \sum_{k=1}^{K} w_k P_{\sigma_k}, \qquad w_k > 0, \qquad \sum_{k=1}^{K} w_k = 1.$$

Equivalently, $B_N$ is the convex hull of the $N!$ permutation matrices, and these are its vertices.

**Bound (Marcus and Ree 1959).** One can take $K \le (N-1)^2 + 1 = N^2 - 2N + 2$. The algorithm in the proof below gives a decomposition with this many terms or fewer, whichever perfect matching it picks in each step.

**Corollary (substochastic matrices).** If $R \ge 0$ has all row sums and column sums at most 1, there is a doubly stochastic $M$ with $M \ge R$ entrywise, and $M$ differs from $R$ in at most $2N - 1$ entries.

## In plain words

Think of a matrix as a plan of how to share time. Row $i$ is an input of a switch, column $j$ is an output, and the entry says what part of the time input $i$ should send to output $j$. Each input and each output is busy all the time, so each row and each column adds up to 1.

The theorem says that any such plan can be made from a list of simple plans, where each simple plan pairs every input with a different output. You use each simple plan for some part of the time, and the parts add up to the whole. You find the list by taking one pairing that uses only entries that are still above zero, using it for as long as the smallest of its entries allows, and repeating.

## Proof

**Step 1 (a perfect matching on the support).** Let $A \ge 0$ be an $N \times N$ matrix whose rows and columns all sum to the same number $s > 0$. Let $G$ be the bipartite graph with rows on one side, columns on the other, and an edge $(i, j)$ when $a_{ij} > 0$. Then $G$ has a perfect matching.

Take a set $S$ of rows, and let $T$ be the set of columns that have an edge to $S$. The rows in $S$ carry total mass $s|S|$, and all of it is in the columns of $T$, because every positive entry of a row in $S$ is in such a column. The columns of $T$ carry total mass $s|T|$, which includes that mass. So $s|S| \le s|T|$, and $|T| \ge |S|$. This is Hall's condition, so by [Hall's theorem](/hall-theorem/) $G$ has a perfect matching.

**Step 2 (one subtraction).** Let $A$ be as in Step 1 with common sum $s$, let $\sigma$ be a perfect matching of $G$, and let $w = \min_i a_{i \sigma(i)} > 0$. Then $A' = A - w P_\sigma$ has nonnegative entries, since $a_{i\sigma(i)} \ge w$, and all of its rows and columns sum to $s - w$, since $P_\sigma$ has exactly one 1 in each row and each column. At least one entry that is positive in $A$ is zero in $A'$, namely an entry $(i, \sigma(i))$ where the minimum is reached. No zero entry of $A$ becomes positive.

**Step 3 (existence).** Start with $A_0 = M$ and $s_0 = 1$. While $s_t > 0$, apply Step 2 to $A_t$ to get $\sigma_t$, $w_t$, and $A_{t+1} = A_t - w_t P_{\sigma_t}$ with $s_{t+1} = s_t - w_t$. The support shrinks in each step, so the process stops after at most $N^2$ steps. It can only stop at $s_t = 0$: if $s_t > 0$, the rows of $A_t$ sum to $s_t$, so $A_t$ has a positive entry and Step 2 applies. At $s_K = 0$ the rows of $A_K$ sum to 0 and the entries are nonnegative, so $A_K = 0$. Then $M = \sum_{t < K} w_t P_{\sigma_t}$, each $w_t > 0$, and $\sum_t w_t = s_0 - s_K = 1$.

Each permutation matrix is doubly stochastic, and a convex combination of doubly stochastic matrices is doubly stochastic, because the conditions are linear equations and nonnegativity. So $B_N$ is exactly the convex hull of the permutation matrices. A permutation matrix $P$ is a vertex: if $P = \lambda X + (1 - \lambda) Y$ with $X, Y \in B_N$ and $0 < \lambda < 1$, then $X$ and $Y$ are 0 wherever $P$ is 0, so each row of $X$ has only one possibly nonzero entry, which must be 1, and $X = Y = P$.

**Step 4 (the bound $(N-1)^2 + 1$).** For a matrix $X \in B_N$, let $F(X) = \{Y \in B_N : y_{ij} = 0 \text{ whenever } x_{ij} = 0\}$. This set is a face of $B_N$, because it is the set of points of $B_N$ where the valid inequality $\sum_{x_{ij} = 0} y_{ij} \ge 0$ holds with equality.

First, $\dim B_N \le (N-1)^2$. The polytope lies in the affine space cut out by the $2N$ row and column equations. Among these, the equations of all $N$ rows and of the columns $1, \ldots, N-1$ are linearly independent: in a linear relation $\sum_i \alpha_i (\text{row } i) + \sum_{j < N} \beta_j (\text{column } j) = 0$, the coefficient of $y_{iN}$ is $\alpha_i$, so every $\alpha_i = 0$, and then the coefficient of $y_{1j}$ is $\beta_j$, so every $\beta_j = 0$. So the affine space has dimension at most $N^2 - (2N - 1) = (N-1)^2$.

In Step 3, scale $A_t$ to $X_t = A_t / s_t \in B_N$ for each $t < K$. Since the support of $A_{t+1}$ is a proper subset of the support of $A_t$, the face $F(X_{t+1})$ is contained in $F(X_t)$ and does not contain $X_t$. So it is a proper face of $F(X_t)$, and a proper face of a polytope has a smaller dimension. The dimensions $\dim F(X_0) > \dim F(X_1) > \cdots > \dim F(X_{K-1}) \ge 0$ are $K$ distinct integers in $[0, (N-1)^2]$, so $K \le (N-1)^2 + 1$.

**Step 5 (the corollary).** Let $R$ have row deficits $d_i = 1 - \sum_j r_{ij} \ge 0$ and column deficits $e_j = 1 - \sum_i r_{ij} \ge 0$. Both kinds of deficit sum to $N - \sum_{ij} r_{ij}$, so a row has a deficit exactly when some column has one. While this is so, pick a row $i$ and a column $j$ with positive deficits, and add $\min(d_i, e_j)$ to $r_{ij}$. Entries only grow, and each step makes $d_i$ or $e_j$ zero, and the zero stays. There are $2N$ deficits, and the last step zeroes two of them, because the two totals are equal. So there are at most $2N - 1$ steps, and the result is doubly stochastic. $\blacksquare$

## Consequences

**Schedules for an input-queued switch.** Let $R$ be the rate matrix of an $N \times N$ crossbar, with $r_{ij}$ the arrival rate of cells from input $i$ to output $j$. It is admissible when all row and column sums are at most 1. Complete $R$ to a doubly stochastic $M \ge R$ (Step 5) and decompose $M = \sum_k w_k P_{\sigma_k}$. A schedule that uses matching $\sigma_k$ in a fraction $w_k$ of the slots gives each pair $(i, j)$ a service rate of $m_{ij} \ge r_{ij}$. Chang, Chen and Huang (2000) built the Birkhoff-von Neumann switch on this idea; it gives rate guarantees with no speedup and no scheduling work in each slot. The weak point is that the rates must be known and the decomposition must be recomputed when they change.

For example, take $N = 3$ and

$$R = \begin{pmatrix} 0.3 & 0.2 & 0 \\ 0.1 & 0.3 & 0.2 \\ 0.2 & 0 & 0.4 \end{pmatrix}.$$

The row deficits are $(0.5, 0.4, 0.4)$ and the column deficits are $(0.4, 0.5, 0.4)$. Step 5 adds 0.4 at $(1,1)$, 0.1 at $(1,2)$, 0.4 at $(2,2)$ and 0.4 at $(3,3)$, which is 4 changed entries, at most $2N - 1 = 5$. The proof algorithm of the implementation then finds

$$M = \begin{pmatrix} 0.7 & 0.3 & 0 \\ 0.1 & 0.7 & 0.2 \\ 0.2 & 0 & 0.8 \end{pmatrix} = 0.7\, I + 0.1\, P_{(2,1,3)} + 0.2\, P_{(2,3,1)},$$

where $P_{(a,b,c)}$ sends row 1 to column $a$, row 2 to column $b$ and row 3 to column $c$. In a frame of 10 slots the switch uses the identity 7 times, $(2,1,3)$ once and $(2,3,1)$ twice, and each pair gets at least $10 r_{ij}$ slots.

**Integer form and edge coloring.** If $K$ is a nonnegative integer matrix with all row and column sums equal to $D$, then $K$ is the sum of $D$ permutation matrices. This is the matrix form of [Kőnig's](/konig-theorem/) theorem that a $D$-regular bipartite multigraph has a proper [edge coloring](/edge-coloring/) with $D$ colors. It follows from the theorem: in the proof applied to $K / D$, every entry is a multiple of $1/D$ at each step, so every weight $w_t$ is a multiple of $1/D$. A frame-based switch with integer cell counts per frame uses this form.

**The assignment problem.** A linear function $\sum_{ij} c_{ij} x_{ij}$ over $B_N$ has its minimum at a vertex, which is a permutation matrix. So the linear programming relaxation of the [assignment problem](/assignment-problem/) has an integral optimum. This was von Neumann's use of the theorem. In the language of polytopes, $B_N$ is the perfect [matching polytope](/matching-polytope/) of the complete bipartite graph $K_{N,N}$.

**A small worked case.** The circulant matrix with rows $(\frac12, \frac13, \frac16)$, $(\frac16, \frac12, \frac13)$ and $(\frac13, \frac16, \frac12)$ decomposes as $\frac12 I + \frac13 P_{(2,3,1)} + \frac16 P_{(3,1,2)}$. Three terms are enough here, fewer than the bound of 5.

## Tightness

**The bound $(N-1)^2 + 1$ is tight.** First, $\dim B_N = (N-1)^2$ exactly. Let $J$ be the all-ones matrix. Any matrix $E$ with all row and column sums 0 and all entries at most $1/N$ in absolute value gives $J/N + E \in B_N$. These $E$ form a ball in the $(N-1)^2$-dimensional space of matrices with zero row and column sums. So $B_N$ contains a ball of that dimension. A convex combination of $(N-1)^2$ permutation matrices lies in an affine set of dimension at most $(N-1)^2 - 1$. There are finitely many such sets, so their union has measure zero in $B_N$. So almost every doubly stochastic matrix needs $(N-1)^2 + 1$ terms. This is also the upper bound that [Carathéodory's theorem](/caratheodory-theorem/) gives for a polytope of this dimension.

For $N = 3$, the bound is 5. Weight the six permutation matrices of size 3 by $1, 2, \ldots, 6$ over 21. The test of the implementation checks, by exact linear algebra on all 15 sets of 4 permutations, that no 4 of them give this matrix, so it needs 5. For random dense matrices built from 40 random permutations (seed 5, 200 matrices for each size), the largest number of terms that the algorithm used was exactly $(N-1)^2 + 1$ for $N = 3, 4, 5, 6$: 5, 10, 17 and 26.

**The choice of matchings changes the count.** For the circulant matrix above, the proof algorithm can also end with 5 terms: $\frac16$ each for $(3,2,1)$, $(1,3,2)$, $(2,3,1)$ and $(2,1,3)$, and $\frac13$ for $I$, when it picks the matchings in this order. The best choice needs only 3. Finding a decomposition with the fewest terms is NP-hard (Dufossé and Uçar 2016), so in practice one uses heuristics such as taking the matching whose smallest entry is largest.

**The hypotheses are needed.** A nonnegative matrix whose row sums are 1 but whose column sums are not is not a combination of permutation matrices, since every such combination has equal column sums. Negative entries also break Step 1: $\begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$ has all sums 1 but is not in the convex hull.

## History

Dénes Kőnig proved in 1916 that a regular bipartite multigraph has a perfect matching, which already gives the theorem for matrices with rational entries. Garrett Birkhoff stated and proved the theorem for real doubly stochastic matrices in 1946, in a short Spanish note in a journal of the National University of Tucumán in Argentina. John von Neumann gave an independent proof in 1953, as a tool for the optimal assignment problem viewed as a game. Marcus and Ree (1959) proved the bound $N^2 - 2N + 2$ on the number of permutation matrices. In networking, Chang, Chen and Huang (2000) used the decomposition to build input-queued switches with rate guarantees, and the decomposition has since been used for the scheduling of optical and data-center switches, where each reconfiguration of the fabric is costly and fewer terms are better.

## References
