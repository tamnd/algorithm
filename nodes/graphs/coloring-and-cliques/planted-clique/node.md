---
tag: FEQAM2
kind: problem
slug: planted-clique
name: Planted clique problem
aliases:
- hidden clique
area: graphs/coloring-and-cliques
level: research
summary: Recover a clique planted in a random graph; a hardness assumption in average-case complexity.
prereqs: [maximum-clique, erdos-renyi-model]
see_also: [average-case-analysis, computational-hardness-assumption, spectral-methods, sparse-pca, stochastic-block-model, tomita-maximum-clique, lovasz-theta-function, eigenvector]
sources:
  - paper: doi:10.1002/rsa.3240030402
    title: Mark Jerrum, Large cliques elude the Metropolis process, Random Structures and Algorithms 3(4), 347 to 359 (1992)
    locator: the definition of the hidden clique model and the lower bound for the Metropolis process
  - paper: doi:10.1016/0166-218X(94)00103-K
    title: Luděk Kučera, Expected complexity of graph partitioning problems, Discrete Applied Mathematics 57(2 to 3), 193 to 212 (1995)
    locator: recovery of a planted clique of size about the square root of n log n from the vertex degrees
  - paper: "N. Alon, M. Krivelevich and B. Sudakov, Finding a large hidden clique in a random graph, Random Structures and Algorithms 13(3 to 4), 457 to 466 (1998)"
    locator: the spectral algorithm for cliques of size c times the square root of n
  - paper: doi:10.1137/17M1138236
    title: Boaz Barak, Samuel Hopkins, Jonathan Kelner, Pravesh K. Kothari, Ankur Moitra and Aaron Potechin, A nearly tight sum-of-squares lower bound for the planted clique problem, SIAM Journal on Computing 48(2), 687 to 735 (2019)
    locator: the main theorem (degree-d sum-of-squares fails below about n^(1/2) for constant d)
---

In the planted clique problem, a random graph $G(n, \frac12)$ is given, except that a hidden set of $k$ vertices has been made into a [clique](/clique/), and the task is to find it. A random graph has no clique larger than about $2\log_2 n$, so for $k$ a bit above that the planted clique is the unique largest one and can be found by search in time $n^{O(\log n)}$. Polynomial-time algorithms are known only for $k \ge c\sqrt{n}$. The belief that nothing efficient works for $k = n^{1/2 - \varepsilon}$ is the planted clique hypothesis, a standard assumption in [average-case](/average-case-analysis/) complexity.

## In plain words

Take a large crowd where each pair of people are friends by a coin flip. Secretly pick a small group and make them all friends with each other. Now hand someone the friendship list and ask them to find the secret group.

If the group is large, its members have noticeably more friends than average, and simple counting finds them. If the group is small, but still larger than any group that would form by chance, it can be found by checking every possible group, which takes far too long. Between those sizes, nobody knows a fast method, and many believe none exists.

## Definition

**Distribution $G(n, \frac12, k)$.** Draw a graph from the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, \frac12)$: each of the $\binom n2$ edges is present independently with probability $\frac12$. Choose a set $K$ of $k$ vertices uniformly at random and add all edges inside $K$.

**Search version.** Given a sample from $G(n, \frac12, k)$, output $K$, with probability tending to 1 as $n \to \infty$.

**Decision version.** Given a graph drawn either from $G(n, \frac12)$ or from $G(n, \frac12, k)$, each with probability $\frac12$, decide which, with success probability at least $\frac12 + \delta$ for a constant $\delta > 0$.

**Planted clique hypothesis.** For every $\varepsilon > 0$, no polynomial-time algorithm solves the decision version for $k = n^{1/2 - \varepsilon}$.

## Variants

- **Edge density.** Use $G(n, p)$ for other constant $p$; the threshold for efficient algorithms is still of order $\sqrt n$.
- **Planted dense subgraph.** Raise the edge probability inside $K$ to $q > p$ instead of to 1; this is a model of community detection and close to the [stochastic block model](/stochastic-block-model/).
- **Planted independent set, planted coloring.** The complement problem, and its generalization where the vertices are split into hidden color classes.
- **Hypergraphs and tensors.** Planted cliques in random $r$-uniform hypergraphs, related to tensor PCA.
- **Semi-random models.** An adversary may delete edges outside $K$ after the random draw; this defeats degree counting but not methods based on semidefinite programming such as the [Lovász theta function](/lovasz-theta-function/).

## Examples

One instance for each $k$, with $n = 2000$ (so $\sqrt n \approx 44.7$), random seed fixed. "Degree" keeps the $k$ vertices of largest degree; "spectral" keeps the $k$ largest entries, in absolute value, of the top [eigenvector](/eigenvector/) of the $\pm 1$ adjacency matrix. The table counts how many of the $k$ chosen vertices lie in $K$.

| $k$ | degree | spectral |
|---|---|---|
| 40 | 2 | 1 |
| 90 | 39 | 90 |
| 150 | 128 | 150 |

At $k = 40$, below $\sqrt n$, both methods see only noise. At $k = 90 \approx 2\sqrt n$ the spectral method already finds the whole clique, while degrees need $k$ of order $\sqrt{n \log n}$ to separate. The largest clique of $G(2000, \frac12)$ itself has fewer than $2 \log_2 2000 \approx 22$ vertices, so for every $k$ in the table the planted clique is the unique maximum clique.

## Known algorithms

- **Exhaustive search.** For $k \ge (2 + \varepsilon)\log_2 n$, the planted clique is with high probability the only clique of its size. Try every set $S$ of $\lceil 3 \log_2 n \rceil$ vertices; for the right $S \subseteq K$, the common neighbors of $S$ are exactly $K \setminus S$ plus few others, which are then removed. This takes $n^{O(\log n)}$ time, quasi-polynomial but not polynomial. Exact solvers such as [Tomita's branch and bound](/tomita-maximum-clique/) follow the same limit.
- **Degrees (Kučera 1995).** A vertex of $K$ has expected degree $\frac{n}{2} + \frac{k}{2}$, while the degree fluctuations are of order $\sqrt{n}$, and the maximum over $n$ vertices of order $\sqrt{n \log n}$. So for $k \ge c\sqrt{n \log n}$ the $k$ vertices of largest degree are exactly $K$.
- **Spectral (Alon, Krivelevich and Sudakov 1998).** For $k \ge c\sqrt{n}$, the second eigenvector of the adjacency matrix is concentrated on $K$; take its $k$ largest entries, then clean up by keeping the vertices with at least $\frac34 k$ neighbors in that set. Running time is polynomial; with a brute-force guess of a few clique vertices, any constant $c > 0$ works in time $n^{O(\log(1/c))}$. See [spectral methods](/spectral-methods/).
- **Message passing and linear time.** Later algorithms reach $k \ge 1.261\sqrt{n}$ in linear time (Dekel, Gurel-Gurevich and Peres) and $k \ge (1 + \varepsilon)\sqrt{n/e}$ by approximate message passing (Deshpande and Montanari).
- **Lovász theta.** Feige and Krauthgamer showed that the theta function of the graph reveals $K$ for $k \ge c\sqrt n$, also in the semi-random model.

## Bounds

- **Information-theoretic.** For $k \le (2 - \varepsilon)\log_2 n$ the planted clique cannot be told apart from cliques that occur by chance; for $k \ge (2 + \varepsilon)\log_2 n$ it is determined, and found in quasi-polynomial time.
- **Metropolis process (Jerrum 1992).** A natural Markov chain that grows and shrinks a clique needs superpolynomial expected time to find a clique of size $(1 + \varepsilon)\log_2 n$ in $G(n, \frac12)$, from most starting states, and this remains true when a clique of size $n^{\beta}$ with $\beta < \frac12$ is planted.
- **Sum of squares (Barak et al. 2019).** The degree-$d$ sum-of-squares relaxation of maximum clique has value much larger than $k$ on $G(n, \frac12)$ itself when $k \le n^{1/2 - c\sqrt{d / \log n}}$, so it cannot distinguish the two distributions. For constant $d$ this is $n^{1/2 - o(1)}$.
- **Statistical queries and low-degree polynomials.** Statistical query algorithms (Feldman et al.) and low-degree polynomial tests also fail below $n^{1/2 - \varepsilon}$, matching the spectral threshold up to the exponent.
- **No reduction from worst case.** No reduction from an NP-hard problem is known, and none is expected, since the problem is solvable in quasi-polynomial time.

## Reductions

- **Source of average-case hardness.** Assuming the hypothesis, the following are hard on average: finding an approximate Nash equilibrium of maximum social welfare (Hazan and Krauthgamer), detecting sparse principal components ([sparse PCA](/sparse-pca/), Berthet and Rigollet), testing $k$-wise independence (Alon et al.), and community detection with a small planted community.
- **To worst-case approximation.** A polynomial algorithm that found, in every graph, a clique of size at least $\omega / n^{1/2 - \varepsilon}$ would find a clique larger than $2\log_2 n$ in $G(n, \frac12, k)$ for $k = n^{1/2 - \varepsilon/2}$, which tells the two distributions apart. So the hypothesis implies that [maximum clique](/maximum-clique/) has no such approximation, a weaker conclusion than the known worst-case NP-hardness of approximation within $n^{1 - \varepsilon}$.
- **Within the family.** Planted dense subgraph and planted clique reduce to each other in parts of their parameter space, which lets one hypothesis cover many problems; see [computational hardness assumptions](/computational-hardness-assumption/).

## Applications

- **Cryptography.** Juels and Peinado proposed a hidden clique as a one-way function: planting is easy, finding is believed hard.
- **Statistics.** It is the reference problem for computational-statistical gaps, where an estimator exists but no efficient one is known.
- **Biology and networks.** Finding dense groups of genes, proteins or users in noisy networks, where the clean model explains why simple degree and spectral filters stop working at a size near $\sqrt n$.
- **Benchmarks.** Planted instances, with known answers, test heuristics and exact clique solvers.

## References
