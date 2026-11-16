---
tag: R1A503
kind: definition
slug: subexponential-parameterized-algorithm
name: Subexponential parameterized algorithm
aliases:
- subexponential FPT
area: complexity/parameterized-complexity
level: advanced
summary: "An algorithm for a parameterized problem with running time 2^(o(k)) n^O(1). Planar vertex cover and feedback arc set in tournaments have one; vertex cover in general graphs has none under ETH."
prereqs: [fixed-parameter-tractable, subexponential-time]
see_also: [bidimensionality-theory, grid-minor-theorem, planar-separator-theorem, parameterized-vertex-cover, kemeny-rank-aggregation, cluster-editing, edge-clique-cover, strong-exponential-time-hypothesis]
sources:
  - paper: doi:10.1016/S0022-0000(03)00074-6
    title: "Liming Cai and David Juedes, On the existence of subexponential parameterized algorithms, Journal of Computer and System Sciences 67(4), 789-807 (2003)"
    locator: no 2^(o(k)) algorithms for vertex cover and related problems, and no 2^(o(sqrt k)) algorithms for their planar versions, unless 3-SAT has subexponential algorithms
  - paper: doi:10.1145/1101821.1101823
    title: "Erik D. Demaine, Fedor V. Fomin, MohammadTaghi Hajiaghayi and Dimitrios M. Thilikos, Subexponential parameterized algorithms on bounded-genus graphs and H-minor-free graphs, Journal of the ACM 52(6), 866-893 (2005)"
    locator: 2^(O(sqrt k)) n^O(1) algorithms for bidimensional problems such as planar vertex cover and dominating set
  - paper: doi:10.1007/978-3-642-02927-1_6
    title: "Noga Alon, Daniel Lokshtanov and Saket Saurabh, Fast FAST, ICALP 2009, LNCS 5555, 49-58"
    locator: feedback arc set in tournaments in 2^(O(sqrt k log k)) n^O(1)
  - paper: doi:10.1007/978-3-642-17517-6_3
    title: "Marek Karpinski and Warren Schudy, Faster algorithms for feedback arc set tournament, Kemeny rank aggregation and betweenness tournament, ISAAC 2010, LNCS 6506, 3-14"
    locator: 2^(O(sqrt k)) + n^O(1) for feedback arc set in tournaments and Kemeny rank aggregation
  - book: isbn:9783540299523
    title: Jörg Flum and Martin Grohe, Parameterized Complexity Theory, Springer, 2006
    locator: the chapter on subexponential fixed-parameter tractability (the class SUBEPT)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7, Treewidth (bidimensionality); Chapter 14, Lower bounds based on the exponential time hypothesis
---

A subexponential parameterized algorithm solves a parameterized problem in time $2^{o(k)} n^{O(1)}$, where $k$ is the [parameter](/parameter/) and $n$ the input size. It is a stronger goal than [fixed-parameter tractability](/fixed-parameter-tractable/), which allows any computable $f(k)$ in $f(k) n^{O(1)}$. Typical bounds are $2^{O(\sqrt k)} n^{O(1)}$ and $2^{O(\sqrt k \log k)} n^{O(1)}$. Such algorithms exist for many problems on planar graphs, by [bidimensionality](/bidimensionality-theory/), and for some problems on tournaments and dense graphs. For many other problems, such as vertex cover in general graphs, none exists unless the exponential time hypothesis (ETH) fails.

## Definition

Let $(L, \kappa)$ be a parameterized problem, with parameter $k = \kappa(x)$ for an input $x$ of size $n$.

- An algorithm for $(L, \kappa)$ is a *subexponential parameterized algorithm* if its running time is at most $2^{s(k)} n^{c}$ for a constant $c$ and a computable function $s$ with $s(k) = o(k)$, that is, $s(k)/k \to 0$.
- The problem is *subexponential fixed-parameter tractable* if it has such an algorithm. Flum and Grohe call this class SUBEPT. They require the $o(k)$ to be *effective*: a computable function must bound how fast $s(k)/k$ goes to 0.
- The bound is often written as an additive bound $2^{o(k)} + n^{O(1)}$, which is stronger. It holds when a polynomial kernel is computed first and the subexponential algorithm runs on the kernel.

The word *subexponential* refers to the parameter only. The dependence on $n$ stays polynomial. A $2^{o(n)}$ algorithm for an NP-hard problem, without a parameter, is a different notion; see [subexponential time](/subexponential-time/).

A scratch computation shows the size of the gap for a few values of $k$:

| $k$ | $2^k$ | $2^{\sqrt k}$ | $2^{\sqrt k \log_2 k}$ |
|---|---|---|---|
| 64 | $1.84 \times 10^{19}$ | 256 | $2.81 \times 10^{14}$ |
| 100 | $1.27 \times 10^{30}$ | 1024 | $1.0 \times 10^{20}$ |
| 400 | $2.58 \times 10^{120}$ | 1048576 | $1.1 \times 10^{52}$ |

## Examples and non-examples

**Examples.**

- *Planar vertex cover, planar dominating set, and other bidimensional problems.* Demaine, Fomin, Hajiaghayi and Thilikos gave $2^{O(\sqrt k)} n^{O(1)}$ algorithms on planar graphs, and more generally on graphs of bounded genus and $H$-minor-free graphs. For planar vertex cover the idea is short. A planar graph that contains an $r \times r$ grid as a minor has no vertex cover of size less than about $r^2 / 2$. By the planar [grid minor theorem](/grid-minor-theorem/), a planar graph with a vertex cover of size $k$ has treewidth $O(\sqrt k)$. Dynamic programming over a tree decomposition then takes $2^{O(\sqrt k)} n$ time.
- *Feedback arc set in tournaments.* Delete at most $k$ arcs of a tournament to make it acyclic. Alon, Lokshtanov and Saurabh gave $2^{O(\sqrt k \log k)} n^{O(1)}$ time. Karpinski and Schudy, and independently Feige, improved it to $2^{O(\sqrt k)} + n^{O(1)}$. The same holds for [Kemeny rank aggregation](/kemeny-rank-aggregation/) with $k$ the cost of the solution.
- *Cluster editing with at most $p$ clusters.* Time $2^{O(\sqrt{pk})} + n^{O(1)}$. For a fixed $p$ this is subexponential in $k$. See [cluster editing](/cluster-editing/).

**Non-examples.**

- *Vertex cover in general graphs.* It is FPT in $O^\ast(1.2738^k)$ time, where $O^\ast$ hides polynomial factors, but it has no $2^{o(k)} n^{O(1)}$ algorithm unless ETH fails (Cai and Juedes). The reason is that 3-SAT reduces to vertex cover with $k$ linear in the number of variables and clauses. See [parameterized vertex cover](/parameterized-vertex-cover/).
- *Planar vertex cover below $\sqrt k$.* The same argument with planar reductions shows that planar vertex cover has no $2^{o(\sqrt k)} n^{O(1)}$ algorithm unless ETH fails. So $2^{O(\sqrt k)}$ is optimal for it.
- *Cluster editing in general.* No $2^{o(k)} n^{O(1)}$ algorithm unless ETH fails, although it is subexponential with a bounded number of clusters.
- *Edge clique cover.* It is FPT, but even $2^{2^{o(k)}} n^{O(1)}$ is impossible unless ETH fails. See [edge clique cover](/edge-clique-cover/).
- *Problems that are not FPT.* A problem that is W[1]-hard, such as $k$-clique, has no $f(k) n^{O(1)}$ algorithm at all unless FPT = W[1], so in particular no subexponential one.

## Related definitions

- **Fixed-parameter tractable.** Time $f(k) n^{O(1)}$ for a computable $f$. Every subexponential parameterized algorithm is an FPT algorithm.
- **Exponential time hypothesis.** 3-SAT with $n$ variables has no $2^{o(n)}$ algorithm. It is the usual assumption behind lower bounds of the form "no $2^{o(k)} n^{O(1)}$ algorithm". A *linear parameter* reduction from 3-SAT, where $k$ is $O(n + m)$, transfers the lower bound. The [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) gives sharper bounds on the base of an exponential.
- **Bidimensionality.** A theory that gives subexponential algorithms for problems whose solution size grows with the size of a grid minor. See [bidimensionality theory](/bidimensionality-theory/).
- **Planar separators.** Another source of $2^{O(\sqrt k)}$ algorithms: a planar graph with $n$ vertices has a balanced separator of size $O(\sqrt n)$, and after a linear kernel this gives subexponential algorithms in $k$. See the [planar separator theorem](/planar-separator-theorem/).

## References
