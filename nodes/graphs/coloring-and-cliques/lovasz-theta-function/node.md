---
tag: 9VSGYP
kind: concept
slug: lovasz-theta-function
name: Lovász theta function
aliases:
- theta(G)
area: graphs/coloring-and-cliques
level: research
summary: Semidefinite programming bound that lies between the independence number and the chromatic number of the complement.
prereqs: [semidefinite-programming, independence-number, chromatic-number]
see_also: [perfect-graph, perfect-graph-theorem, ellipsoid-method, channel-capacity, eigenvalue, motzkin-straus-theorem, planted-clique, graph-coloring-inapproximability]
sources:
  - paper: doi:10.1109/TIT.1979.1055985
    title: László Lovász, On the Shannon capacity of a graph, IEEE Transactions on Information Theory 25(1), 1 to 7 (1979)
    locator: the definition of theta, the bound on the Shannon capacity, the value for the pentagon, and the formula for edge-transitive graphs
  - paper: doi:10.1007/BF02579273
    title: M. Grötschel, L. Lovász and A. Schrijver, The ellipsoid method and its consequences in combinatorial optimization, Combinatorica 1(2), 169 to 197 (1981)
    locator: the polynomial-time computation of theta and the algorithms for perfect graphs
  - paper: doi:10.37236/1193
    title: Donald E. Knuth, The sandwich theorem, Electronic Journal of Combinatorics 1, Article A1 (1994)
    locator: the equivalent definitions of theta and the sandwich inequalities
---

The Lovász theta function $\vartheta(G)$ is a number attached to a graph that is computable in polynomial time, by [semidefinite programming](/semidefinite-programming/), and is squeezed between two NP-hard quantities: $\alpha(G) \le \vartheta(G) \le \chi(\overline{G})$, the [independence number](/independence-number/) and the least number of cliques that cover the vertices. Lovász introduced it in 1979 to prove that the Shannon capacity of the 5-cycle is $\sqrt 5$. On [perfect graphs](/perfect-graph/) both ends of the sandwich are equal, which makes maximum clique, maximum independent set and coloring solvable in polynomial time there.

## In plain words

Some questions about networks, like the largest set of points with no links between them, are very hard to answer exactly. The theta number is a quantity that a computer can find quickly and that is guaranteed to be at least that answer and at most a second hard answer, the fewest linked groups that cover all points.

When those two hard answers agree, the theta number pins both down. Many important families of networks have this property. For others, the theta number is still a useful estimate, and it has solved some questions that no other method could.

## The idea

Let $G$ have vertices $1, \ldots, n$ and edge set $E$. The theta function is the optimum of the semidefinite program

$$\vartheta(G) = \max\Big\{ \sum_{i,j} X_{ij} \;:\; X \succeq 0,\ \operatorname{tr} X = 1,\ X_{ij} = 0 \text{ for all } ij \in E \Big\}.$$

By semidefinite duality it also equals $\min \lambda_{\max}(A)$ over symmetric matrices $A$ with $A_{ij} = 1$ whenever $i = j$ or $ij \notin E$, and Lovász's original definition through orthonormal representations: assign unit vectors $u_i$ with $u_i \perp u_j$ whenever $i \ne j$ are non-adjacent, and a unit vector $c$; then $\vartheta(G) = \min \max_i 1/(c^{\mathsf T} u_i)^2$ over all such choices. Knuth's survey collects these and other equivalent forms.

**Sandwich theorem.** $\alpha(G) \le \vartheta(G) \le \chi(\overline{G})$.

*Lower bound.* For an independent set $S$, let $X = \frac{1}{|S|}\mathbf{1}_S \mathbf{1}_S^{\mathsf T}$. It is positive semidefinite with trace 1, it is 0 on every edge because $S$ has no edges, and $\sum_{i,j} X_{ij} = |S|$.

*Upper bound.* Let $C_1, \ldots, C_k$ be cliques of $G$ that partition $V$, with $k = \chi(\overline{G})$, and let $M = k \sum_t \mathbf{1}_{C_t}\mathbf{1}_{C_t}^{\mathsf T} - J$, where $J$ is the all-ones matrix. For any vector $y$, with $s_t = \sum_{i \in C_t} y_i$, we get $y^{\mathsf T} M y = k \sum_t s_t^2 - (\sum_t s_t)^2 \ge 0$ by the Cauchy-Schwarz inequality, so $M \succeq 0$. For a feasible $X$, the inner product of two positive semidefinite matrices is nonnegative, so $0 \le \langle M, X\rangle = k \sum_t \sum_{i, j \in C_t} X_{ij} - \sum_{i,j} X_{ij}$. Two distinct vertices of a clique are adjacent, so $X_{ij} = 0$ there, and the first sum is $k \operatorname{tr} X = k$. Hence $\sum_{i,j} X_{ij} \le k$. $\square$

Applied to the complement, the same theorem reads $\omega(G) \le \vartheta(\overline{G}) \le \chi(G)$.

**Computation.** The program can be solved to any accuracy $\varepsilon$ in time polynomial in $n$ and $\log(1/\varepsilon)$, by the [ellipsoid method](/ellipsoid-method/) (Grötschel, Lovász and Schrijver 1981) or by interior-point methods.

**Further properties.**

- $\vartheta(G)\, \vartheta(\overline{G}) \ge n$, with equality when $G$ is vertex-transitive.
- $\vartheta$ is multiplicative on the strong product: $\vartheta(G \boxtimes H) = \vartheta(G)\vartheta(H)$.
- For a regular edge-transitive graph with adjacency [eigenvalues](/eigenvalue/) $\lambda_{\max}$ and $\lambda_{\min}$, $\vartheta(G) = \dfrac{-n\, \lambda_{\min}}{\lambda_{\max} - \lambda_{\min}}$, the Hoffman ratio. In general $\vartheta$ is at most this ratio for regular graphs.

## Examples

| graph | $\alpha(G)$ | $\vartheta(G)$ | $\chi(\overline{G})$ |
|---|---|---|---|
| complete graph $K_n$ | 1 | 1 | 1 |
| $n$ isolated vertices | $n$ | $n$ | $n$ |
| $C_4$ | 2 | 2 | 2 |
| $C_5$ | 2 | $\sqrt 5 \approx 2.236$ | 3 |
| $C_7$ | 3 | $\dfrac{7\cos(\pi/7)}{1 + \cos(\pi/7)} \approx 3.318$ | 4 |
| Petersen graph | 4 | 4 | 5 |

The values for cycles and the Petersen graph come from the eigenvalue formula, since these graphs are edge-transitive: $C_5$ has $\lambda_{\max} = 2$ and $\lambda_{\min} = -\frac{1 + \sqrt 5}{2}$, which gives $\frac{5(1 + \sqrt 5)/2}{2 + (1 + \sqrt5)/2} = \sqrt 5$, and the Petersen graph has eigenvalues $3$ and $-2$, which gives $\frac{10 \cdot 2}{5} = 4$. The Petersen graph has no triangles, so its cliques are edges and single vertices, and covering 10 vertices needs 5 of them.

For odd cycles $C_{2k+1}$ with $k \ge 2$ the theta value is strictly between the two ends, which reflects that they are not perfect. For $C_5$, $\vartheta(C_5)\vartheta(\overline{C_5}) = 5$, as the vertex-transitive equality predicts, since $\overline{C_5} \cong C_5$.

## Where it is used

- **Shannon capacity.** The zero-error capacity of a noisy [channel](/channel-capacity/) whose confusable symbols form $G$ is $\Theta(G) = \lim_k \alpha(G^{\boxtimes k})^{1/k}$. Since $\alpha(G^{\boxtimes k}) \le \vartheta(G)^k$, we get $\Theta(G) \le \vartheta(G)$. For the pentagon, the 5 words $(i, 2i \bmod 5)$ are pairwise distinguishable in $C_5^{\boxtimes 2}$, so $\Theta(C_5) \ge \sqrt 5$, and Lovász's bound shows equality. This answered Shannon's question from 1956.
- **Perfect graphs.** If $G$ is perfect, $\alpha(G) = \chi(\overline{G})$, so $\vartheta(G)$ equals both and rounding it gives $\alpha$ exactly. With self-reduction this yields polynomial-time algorithms for maximum weight independent set, maximum clique, minimum coloring and minimum clique cover on perfect graphs (Grötschel, Lovász and Schrijver). No combinatorial polynomial algorithm is known for coloring perfect graphs in general. See also the [perfect graph theorem](/perfect-graph-theorem/).
- **Coloring with vectors.** $\vartheta(\overline{G})$ equals the strict vector chromatic number of $G$. Karger, Motwani and Sudan rounded vector colorings to color 3-colorable graphs with fewer colors than combinatorial methods gave; the [inapproximability of coloring](/graph-coloring-inapproximability/) limits how far such rounding can go.
- **Average-case and semi-random instances.** Theta finds a [planted clique](/planted-clique/) of size $c\sqrt n$ and certifies it, even when an adversary removes edges outside the clique.
- **Bounds on codes and sphere packings.** Delsarte's linear programming bound for codes is a variant of theta for graphs with a group structure, and Schrijver strengthened it with semidefinite constraints.
- **Relation to quadratic programs.** Like the [Motzkin-Straus theorem](/motzkin-straus-theorem/), theta turns a clique question into a continuous optimization, but a convex one, which is why it can be solved in polynomial time while only bounding $\alpha$.

## References
