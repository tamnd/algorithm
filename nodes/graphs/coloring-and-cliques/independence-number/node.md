---
tag: Q8G1WX
kind: concept
slug: independence-number
name: Independence number
aliases:
- alpha(G)
- stability number
area: graphs/coloring-and-cliques
level: intro
summary: Size of a largest independent set in a graph.
prereqs: [independent-set]
see_also: [maximum-independent-set, clique-number, chromatic-number, vertex-cover, ramsey-theorem, turan-theorem, lovasz-theta-function, konig-theorem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.5, Perfect graphs (α(G), ω(G) and the bound χ(G) ≥ n/α(G)); Chapter 9, Ramsey theory
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 3.1 (independent sets and covers, Gallai's identity and the König-Egerváry theorem); Section 5.1 (the bound χ(G) ≥ n(G)/α(G))
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: The Probabilistic Lens, Turán's theorem (the random-order proof of α(G) ≥ Σ 1/(d(v) + 1))
  - paper: doi:10.1007/BF02392825
    title: Johan Håstad, Clique is hard to approximate within n^(1-ε), Acta Mathematica 182(1), 105 to 142 (1999)
    locator: the main theorem (also for independent sets, by complementation)
---

The independence number $\alpha(G)$ of a graph $G$ is the number of vertices in a largest [independent set](/independent-set/) of $G$. It is the [clique number](/clique-number/) of the [complement graph](/complement-graph/), and with the [chromatic number](/chromatic-number/) it gives the bound $\chi(G) \ge n / \alpha(G)$. Computing it is the [maximum independent set problem](/maximum-independent-set/), which is NP-hard and hard to approximate. Simple degree bounds and the [Lovász theta function](/lovasz-theta-function/) give bounds that are cheap to compute.

## In plain words

Some pairs of people in a group do not get along. You want to invite as many people as you can to a party so that no two guests are in such a pair. The largest number of guests you can invite is the independence number of the "do not get along" graph.

This number is easy to define and hard to compute: no known fast method finds it for every graph. But it is easy to get a guaranteed lower value. If each person has only a few enemies, you can always invite a large group. Each guest you invite rules out only that guest's enemies.

## The idea

Let $G = (V, E)$ be a finite simple undirected graph with $n = |V|$ vertices. Then

$$\alpha(G) = \max \{\, |S| : S \subseteq V,\ S \text{ is independent in } G \,\},$$

with $\alpha(G) = 0$ when $V = \emptyset$. The main identities and bounds are below. Write $\omega$ for the clique number, $\chi$ for the chromatic number, $\beta$ for the size of a smallest [vertex cover](/vertex-cover/), $\nu$ for the size of a [maximum matching](/maximum-matching/), and $d(v)$ for the [degree](/degree/) of $v$.

- **Complement.** $\alpha(G) = \omega(\overline{G})$, because a set is independent in $G$ exactly when it is a clique in $\overline{G}$.
- **Gallai's identity.** $\alpha(G) + \beta(G) = n$, because $S$ is independent exactly when $V \setminus S$ is a vertex cover.
- **Bipartite graphs.** If $G$ is bipartite, $\beta(G) = \nu(G)$ by [König's theorem](/konig-theorem/), so $\alpha(G) = n - \nu(G)$. This makes $\alpha$ computable in polynomial time for bipartite graphs; see [bipartite maximum independent set](/bipartite-maximum-independent-set/).
- **Coloring.** Each color class of a proper coloring is independent, so $n \le \chi(G)\,\alpha(G)$.
- **Caro-Wei bound.** $\alpha(G) \ge \sum_{v \in V} \frac{1}{d(v) + 1}$.
- **Turán form.** With the average degree $\bar d = 2|E|/n$, $\alpha(G) \ge \frac{n}{\bar d + 1}$. In particular $\alpha(G) \ge \frac{n}{\Delta + 1}$ for the maximum degree $\Delta$.
- **Theta sandwich.** $\alpha(G) \le \vartheta(G) \le \chi(\overline{G})$, where $\vartheta$ is the [Lovász theta function](/lovasz-theta-function/), which is computable to any precision in polynomial time.
- **Ramsey.** Each graph on at least $R(s, t)$ vertices has $\omega \ge s$ or $\alpha \ge t$; see [Ramsey's theorem](/ramsey-theorem/).

**Proof of the Caro-Wei bound.** Take a uniform random order of $V$. Let $S$ be the set of vertices that come before all of their neighbors in the order. Two adjacent vertices cannot both come before each other, so $S$ is independent. A vertex $v$ is in $S$ exactly when it is first among the $d(v) + 1$ vertices of $\{v\} \cup N(v)$. Each of these is equally likely to be first, so $\Pr[v \in S] = 1/(d(v) + 1)$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}|S| = \sum_v 1/(d(v) + 1)$. Some order gives a set at least as large as the mean, so $\alpha(G)$ is at least this sum. $\square$

**Proof of the Turán form.** The function $x \mapsto 1/(x + 1)$ is convex for $x > -1$. By Jensen's inequality, $\frac{1}{n}\sum_v \frac{1}{d(v) + 1} \ge \frac{1}{\bar d + 1}$. Multiply by $n$ and use the Caro-Wei bound. $\square$

The Turán form is the complement form of [Turán's theorem](/turan-theorem/): a graph with $n$ vertices and fewer edges than the Turán bound has a large independent set.

**Hardness.** Deciding whether $\alpha(G) \ge k$ is NP-complete; it is [Karp's](/karps-21-np-complete-problems/) problem *Independent set*, the same as *Clique* in the complement. Håstad proved that for each $\varepsilon > 0$, $\alpha$ cannot be approximated within a factor $n^{1 - \varepsilon}$ in polynomial time unless $\mathrm{NP} = \mathrm{ZPP}$, and Zuckerman (2007) made the hypothesis $\mathrm{P} \ne \mathrm{NP}$. The exact algorithms are on the page of the [maximum independent set problem](/maximum-independent-set/).

## Examples

| graph | $n$ | $\alpha$ | $\chi$ | Caro-Wei bound | reason for $\alpha$ |
|---|---|---|---|---|---|
| $K_4$ | 4 | 1 | 4 | 1 | all pairs adjacent |
| $C_5$ | 5 | 2 | 3 | 5/3 | $\lfloor 5/2 \rfloor$ |
| $C_7$ | 7 | 3 | 3 | 7/3 | $\lfloor 7/2 \rfloor$ |
| $K_{3,3}$ | 6 | 3 | 2 | 3/2 | one side |
| star $K_{1,5}$ | 6 | 5 | 2 | 8/3 | the 5 leaves |
| Petersen graph | 10 | 4 | 3 | 5/2 | see below |

- **Petersen graph.** It is 3-regular, so Caro-Wei gives $\alpha \ge 10/4$, that is $\alpha \ge 3$. Its adjacency eigenvalues are $3$, $1$ and $-2$. The Hoffman ratio bound for a $d$-regular graph, $\alpha \le n \cdot \frac{-\lambda_{\min}}{d - \lambda_{\min}}$, gives $\alpha \le 10 \cdot 2/5 = 4$, and the set $\{0, 2, 8, 9\}$ of the [independent set](/independent-set/) page reaches it.
- **The coloring bound can be strict.** $C_5$ has $n/\alpha = 5/2$, so $\chi \ge 3$, which is exact. The star $K_{1,5}$ has $n/\alpha = 6/5$ and $\chi = 2$.
- **Caro-Wei can be far off.** For the star $K_{1,5}$, the bound is $8/3$ and $\alpha = 5$. For a disjoint union of cliques the bound is exact: each clique $K_r$ adds $r \cdot \frac{1}{r} = 1$.
- **Random graphs.** In the [Erdős-Rényi graph](/erdos-renyi-model/) $G(n, 1/2)$, $\alpha$ is about $2 \log_2 n$ with high probability, while the greedy algorithm finds an independent set of only about $\log_2 n$ vertices.

## Where it is used

- **Coloring lower bounds.** $\chi(G) \ge n / \alpha(G)$ and its fractional version are standard lower bounds in [graph coloring](/graph-coloring/).
- **Perfect graphs.** A graph is [perfect](/perfect-graph/) when $\chi = \omega$ for all induced subgraphs. Lovász proved that this holds if and only if $\alpha(H)\,\omega(H) \ge |V(H)|$ for every induced subgraph $H$, which gives the [perfect graph theorem](/perfect-graph-theorem/).
- **Ramsey and extremal theory.** [Ramsey's theorem](/ramsey-theorem/) bounds $\alpha$ and $\omega$ together, and [Turán's theorem](/turan-theorem/) is a lower bound on $\alpha$ of a sparse graph.
- **Information theory.** The Shannon capacity of a graph is the limit of $\alpha(G^{\boxtimes k})^{1/k}$ over strong powers. Lovász introduced $\vartheta$ to prove that the capacity of $C_5$ is $\sqrt 5$.
- **Scheduling and coding.** A set of tasks with pairwise conflicts that can run at the same time is an independent set of the [conflict graph](/conflict-graph/). A code with minimum distance $d$ is an independent set in the graph that joins words at distance less than $d$.

## References
