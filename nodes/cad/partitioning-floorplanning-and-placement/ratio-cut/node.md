---
tag: 95PDKQ
kind: definition
slug: ratio-cut
name: Ratio cut
aliases:
- Wei-Cheng ratio cut
area: cad/partitioning-floorplanning-and-placement
level: core
summary: The cut size of a bipartition divided by the product of the part sizes, minimized to find natural clusters without a fixed balance.
prereqs: [cut, laplacian-matrix, hypergraph-partitioning]
see_also: [normalized-cut, sparsest-cut-problem, spectral-partitioning, graph-partitioning-problem, cheeger-inequality, hypergraph-partitioning, rayleigh-quotient, spectral-clustering]
sources:
  - paper: doi:10.1109/43.87601
    title: Yen-Chuen Wei and Chung-Kuan Cheng, Ratio cut partitioning for hierarchical designs, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 10(7), 911 to 921, 1991
    locator: the definition of the ratio cut for netlists, the statement that finding the optimal ratio cut is NP-complete, and the iterative shifting heuristic
  - paper: "Yen-Chuen Wei and Chung-Kuan Cheng, Towards efficient hierarchical designs by ratio cut partitioning, IEEE International Conference on Computer-Aided Design (ICCAD), 298 to 301, 1989"
    locator: the conference version of the ratio cut objective
  - paper: doi:10.1109/43.159993
    title: Lars Hagen and Andrew B. Kahng, New spectral methods for ratio cut partitioning and clustering, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 11(9), 1074 to 1085, 1992
    locator: the lower bound of the minimum ratio cut by the second smallest Laplacian eigenvalue divided by n, and the EIG1 sweep over the sorted eigenvector
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (general locator)
---

The ratio cut of a split of a graph or a netlist into two nonempty parts $A$ and $B$ is the weight of the cut divided by $|A| \cdot |B|$. Wei and Cheng introduced it in 1989 for circuit partitioning: instead of forcing two parts of equal size, it lets the parts have any sizes, but makes a cut cheaper per crossing net the more balanced it is. So a minimum ratio cut finds a natural split, such as a loosely joined cluster, even when the cluster is small. Finding a minimum ratio cut is NP-hard (Wei and Cheng, 1991), and the second smallest Laplacian eigenvalue divided by $n$ is a lower bound on it (Hagen and Kahng, 1992). The [normalized cut](/normalized-cut/) is the same idea with volumes instead of vertex counts.

## Definition

Let $G = (V, E)$ be a graph with $n = |V| \ge 2$ vertices and edge weights $w \ge 0$. For a set $A$ with $\emptyset \ne A \subsetneq V$ and $B = V \setminus A$, let $\mathrm{cut}(A, B)$ be the total weight of the edges between $A$ and $B$. The *ratio cut* of $(A, B)$ is

$$ R(A, B) = \frac{\mathrm{cut}(A, B)}{|A| \cdot |B|}. $$

The *minimum ratio cut* of $G$ is $R^* = \min_{A} R(A, B)$ over all such $A$. For a netlist, a [hypergraph](/hypergraph/), $\mathrm{cut}(A, B)$ is the weight of the nets with pins in both parts, as in [hypergraph partitioning](/hypergraph-partitioning/), and $|A|$, $|B|$ may be replaced by the total cell areas. The formula is defined only when both parts are nonempty.

**Other normalizations.** Several quantities with the same name differ by a constant factor:

- In spectral clustering (for example in von Luxburg's tutorial), $\mathrm{RatioCut}(A, B) = \mathrm{cut}(A, B) \, (1/|A| + 1/|B|) = n \, R(A, B)$.
- The uniform [sparsest cut](/sparsest-cut-problem/), with demand 1 between every pair of vertices, is $\mathrm{cut}(A, B) / (|A| |B|)$, which is exactly $R$.
- The edge expansion $\mathrm{cut}(A, B) / \min(|A|, |B|)$ lies between $R \cdot n/2$ and $R \cdot n$, since $\max(|A|, |B|)$ lies between $n/2$ and $n$.
- The [normalized cut](/normalized-cut/) divides by the volumes (sums of degrees) of the parts instead of the vertex counts.

A bound on any of them gives a bound on the others, but only after the factor is fixed. A statement about "the ratio cut" must say which one it uses. This page uses $R$.

**Lower bound by $\lambda_2$ (Hagen and Kahng).** Let $L$ be the [Laplacian](/laplacian-matrix/) of $G$ with eigenvalues $0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n$. Then

$$ R^* \ge \frac{\lambda_2}{n}. $$

*Proof.* Take any split $(A, B)$ and define $x_v = |B|$ for $v \in A$ and $x_v = -|A|$ for $v \in B$. Then $\sum_v x_v = |A| |B| - |B| |A| = 0$, so $x$ is orthogonal to the all-ones vector. Each cut edge has $|x_u - x_v| = |A| + |B| = n$, and every other edge has $x_u = x_v$, so $x^{\top} L x = \sum_{\{u,v\} \in E} w(u,v) (x_u - x_v)^2 = n^2 \, \mathrm{cut}(A, B)$. Also $x^{\top} x = |A| \, |B|^2 + |B| \, |A|^2 = n \, |A| \, |B|$. By the [Courant-Fischer theorem](/courant-fischer-theorem/), $\lambda_2$ is the least [Rayleigh quotient](/rayleigh-quotient/) over nonzero vectors orthogonal to the all-ones vector, so

$$ \lambda_2 \le \frac{x^{\top} L x}{x^{\top} x} = \frac{n^2 \, \mathrm{cut}(A, B)}{n \, |A| \, |B|} = n \, R(A, B). $$

This holds for every split, so $R^* \ge \lambda_2 / n$. $\square$

The vector $x$ takes only two values. Allowing any real values is the relaxation that the spectral method solves: the eigenvector of $\lambda_2$ minimizes the quotient, and [spectral partitioning](/spectral-partitioning/) rounds it back to a split by a sweep. The bound has no matching upper bound by a constant factor: on a path of $n$ vertices, $R^* = 1/(\lfloor n/2 \rfloor \lceil n/2 \rceil) \approx 4/n^2$ while $\lambda_2 / n \approx \pi^2 / n^3$. A two-sided estimate in terms of $\lambda_2$ holds for the edge expansion and the conductance, by the [Cheeger inequality](/cheeger-inequality/), not with a constant factor for $R$.

**Basic properties.**

- For fixed sizes $|A| = a$, minimizing $R$ is minimizing the cut, so the bisection with $a = n/2$ minimizes $R$ among all bisections.
- The denominator $a (n - a)$ grows from $n - 1$ at $a = 1$ to $\lfloor n^2/4 \rfloor$ at $a = \lfloor n/2 \rfloor$. A cut of a large part must be more than $\lfloor n^2/4 \rfloor / (n - 1) \approx n/4$ times smaller than a cut of a single vertex to win.
- $R^* = 0$ if and only if $G$ is disconnected, as $\lambda_2 = 0$ in the same case.
- The minimum bisection width $b$ gives $R^* \le b / \lfloor n^2/4 \rfloor$.

## Examples and non-examples

- **Two triangles.** On the graph of the [graph partitioning](/graph-partitioning-problem/) page (two triangles $a, b, c$ and $d, e, f$ joined by the edges $cd$ and $be$), the split $\{a, b, c\} \mid \{d, e, f\}$ has $R = 2/9$. A single vertex of degree 2 gives $2/5$, and the other splits are worse, so $R^* = 2/9$. Here $\lambda_2 = 1$, and the bound gives $R^* \ge 1/6$.
- **A clique with a pendant vertex.** Take $K_4$ on $a, b, c, d$ and add a vertex $e$ joined only to $d$. Cutting off $e$ gives $R = 1/(1 \cdot 4) = 1/4$. The split $\{d, e\} \mid \{a, b, c\}$ cuts 3 edges and gives $3/6 = 1/2$, and every split of the clique is worse still. So $R^* = 1/4$ with parts of size 1 and 4: the ratio cut does not force balance, it finds the loose vertex. The Laplacian has $\lambda_2 = 1$, and the bound gives $1/5$. A bisection rule would instead have to cut the clique.
- **A path.** On a path with $n$ vertices, every split cuts at least one edge, and one edge gives $1/(a(n - a))$, least at $a = \lfloor n/2 \rfloor$. For $n = 6$ this is $1/9$, and $\lambda_2/n = (2 - 2\cos(\pi/6))/6 \approx 0.0447$.
- **A netlist.** Cells $a, b, c, d, e$ and nets $\{a, b, c\}$, $\{c, d\}$, $\{d, e\}$, $\{a, e\}$. The split $\{a, b, c\} \mid \{d, e\}$ cuts the nets $\{c, d\}$ and $\{a, e\}$, so $R = 2/6 = 1/3$. The split $\{b\} \mid \{a, c, d, e\}$ cuts only $\{a, b, c\}$, so $R = 1/4$, which is smaller. In the netlist form, cutting off a cell that has a single net is cheap.
- **Non-example: an empty part.** $A = V$ or $A = \emptyset$ is not a ratio cut: the formula divides by zero. A minimum ratio cut is always over two nonempty parts.
- **Non-example: the bisection width.** The ratio cut is not the bisection width divided by a constant, since its best split need not be balanced, as the pendant example shows.

## Related definitions

- **[Sparsest cut](/sparsest-cut-problem/).** The general form with demands. With unit demands it is the ratio cut, and its approximation algorithms (Leighton and Rao; Arora, Rao and Vazirani) apply to $R^*$.
- **[Normalized cut](/normalized-cut/).** Divides by the volumes of the parts. It is the objective of [spectral clustering](/spectral-clustering/) with the normalized Laplacian, while the ratio cut goes with the unnormalized Laplacian.
- **[Graph partitioning](/graph-partitioning-problem/) and [hypergraph partitioning](/hypergraph-partitioning/).** These fix the sizes by a balance condition and minimize the cut alone.
- **[Spectral partitioning](/spectral-partitioning/).** Hagen and Kahng's EIG1 sorts the vertices by the eigenvector of $\lambda_2$ and takes the prefix of least ratio cut.
- **[Cheeger inequality](/cheeger-inequality/).** Relates $\lambda_2$ to conductance and expansion from both sides.

## References
