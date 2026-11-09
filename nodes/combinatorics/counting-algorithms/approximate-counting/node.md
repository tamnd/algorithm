---
tag: 07J65C
kind: problem
slug: approximate-counting
name: Approximate counting
aliases:
- approximate counting of combinatorial objects
- randomized approximate counting
area: combinatorics/counting-algorithms
level: research
summary: Estimating a count to within a multiplicative error, often via sampling.
prereqs: [fpras, monte-carlo-algorithm, chernoff-bound]
see_also: [karp-luby-algorithm, dnf-counting, jerrum-valiant-vazirani-theorem, rapid-mixing, model-counting, fptas, permanent-computation, approximate-counting-problem]
sources:
  - paper: doi:10.1016/0304-3975(86)90174-X
    title: Mark R. Jerrum, Leslie G. Valiant and Vijay V. Vazirani, Random generation of combinatorial structures from a uniform distribution, Theoretical Computer Science 43, 169 to 188, 1986
    locator: the reduction between approximate counting and almost uniform generation for self-reducible relations
  - paper: doi:10.1016/0196-6774(89)90038-2
    title: Richard M. Karp, Michael Luby and Neal Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10(3), 429 to 448, 1989
    locator: the union of sets problem and DNF counting
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Lectures in Mathematics ETH Zurich, Birkhauser, 2003
    locator: the chapters on sampling and counting, on coupling, and on canonical paths
  - paper: doi:10.1137/0222066
    title: Mark Jerrum and Alistair Sinclair, Polynomial-time approximation algorithms for the Ising model, SIAM Journal on Computing 22(5), 1087 to 1116, 1993
    locator: the main theorem (an FPRAS for the ferromagnetic Ising partition function)
  - paper: doi:10.1137/0214060
    title: Larry Stockmeyer, On approximation algorithms for #P, SIAM Journal on Computing 14(4), 849 to 861, 1985
    locator: the main theorem (approximate counting with an NP oracle)
  - paper: doi:10.1145/1132516.1132538
    title: Dror Weitz, Counting independent sets up to the tree threshold, 38th Annual ACM Symposium on Theory of Computing (STOC 2006), 140 to 149
    locator: the main theorem (a deterministic FPTAS by correlation decay)
  - paper: doi:10.1137/S0097539797315306
    title: Paul Dagum, Richard Karp, Michael Luby and Sheldon Ross, An optimal algorithm for Monte Carlo estimation, SIAM Journal on Computing 29(5), 1484 to 1496, 2000
    locator: the main theorems (the number of samples needed for a relative error estimate of a mean)
  - paper: doi:10.1137/S0097539796298340
    title: David R. Karger, A randomized fully polynomial time approximation scheme for the all-terminal network reliability problem, SIAM Journal on Computing 29(2), 492 to 514, 1999
    locator: the main theorem (an FPRAS for all-terminal network unreliability)
  - url: https://oeis.org/A000045
    title: OEIS A000045, Fibonacci numbers
    locator: the comment that F(n+2) is the number of independent vertex sets of the path with n vertices
---

Approximate counting asks for an estimate of the number of objects of a given kind, such as the satisfying assignments of a formula or the perfect matchings of a graph, within a small relative error. Exact counting is #P-hard for most interesting problems, even for many whose decision version is easy, such as perfect matchings in bipartite graphs. Approximate counting is often much easier: a polynomial-time randomized algorithm with relative error $\varepsilon$, an [FPRAS](/fpras/), is known for the number of satisfying assignments of a DNF, the permanent of a nonnegative matrix, the Ising model partition function, and many more. The main tools are random sampling, Markov chains that mix rapidly, and the equivalence of counting and sampling for self-reducible problems. This page is about counting combinatorial objects; the streaming problem of counting many events with a small counter is [a different problem with the same name](/approximate-counting-problem/).

## In plain words

Sometimes we need to know how many ways there are to do something, and the exact number is too hard to compute. Often a number that is almost right is enough, for example one that is off by at most one percent.

The simplest idea is to try many random candidates and see what fraction of them work. This is fine when many candidates work, but it fails when the good ones are very rare. Better methods use smarter random choices: they sample only from places where good objects are common, or they break the count into many steps, where each step is a ratio that is easy to estimate. The answer is random, but it is close to the truth with high probability, and the work grows only slowly as we ask for more accuracy.

## Definition

Let $R$ be a relation, so that $R(x) = \{ y : (x, y) \in R \}$ is the set of solutions of an instance $x$, and let $f(x) = |R(x)|$. Usually $R$ is an NP relation: solutions have length polynomial in $|x|$ and can be checked in polynomial time, so $f$ is in #P. More generally $f(x)$ can be a nonnegative weighted sum, such as a partition function.

**Input.** An instance $x$, an error bound $0 < \varepsilon < 1$ and a failure probability $0 < \delta < 1$.

**Output.** A number $Y$ such that

$$\Pr\big[(1 - \varepsilon) f(x) \le Y \le (1 + \varepsilon) f(x)\big] \ge 1 - \delta.$$

The goal is a running time polynomial in $|x|$, $1/\varepsilon$ and $\log(1/\delta)$, which is an [FPRAS](/fpras/). The [median trick](/median-trick/) turns any algorithm that meets the bound with probability $3/4$ into one that meets it with probability $1 - \delta$, at a cost of a factor $O(\log(1/\delta))$.

## Variants

- **Deterministic approximation.** The same error bound with $\delta = 0$, by a deterministic algorithm: an [FPTAS](/fptas/) for counting.
- **Additive error.** Asking only for $|Y - f(x)| \le \varepsilon N$ for a known upper bound $N$, such as $2^n$. Plain random sampling solves this, but it says nothing useful when $f(x)$ is much smaller than $N$.
- **Rough approximation.** Asking for a factor $c$ or a factor polynomial in $|x|$. For self-reducible problems, Sinclair and Jerrum showed that any such approximation can be boosted to an FPRAS.
- **Almost uniform sampling.** Drawing a solution from a distribution close to uniform on $R(x)$. For self-reducible problems this is equivalent to approximate counting, by the [Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/).
- **Weighted counting.** Estimating a sum of nonnegative weights, such as a partition function of statistical physics, or the probability of an event, as in network reliability.
- **Counting with an oracle.** Approximate counting with access to an NP oracle, which Stockmeyer showed is possible for every function in #P.

## Examples

- **Rare solutions.** The formula $x_1 \land x_2 \land \cdots \land x_n$ has one satisfying assignment among $2^n$. Plain Monte Carlo sees no solution in fewer than about $2^n$ samples, so it returns 0 with high probability, a relative error of 100 percent. The [Karp-Luby estimator](/karp-luby-algorithm/) samples only among assignments that satisfy some clause, and returns the exact count 1 here.
- **The product estimator.** Let $Z(G)$ be the number of independent sets of a graph $G$, and let $G_k$ be the graph induced by the first $k$ vertices $v_1, \ldots, v_k$. Then

  $$Z(G_n) = \prod_{k=1}^{n} \frac{Z(G_k)}{Z(G_{k-1})}, \qquad \frac{Z(G_{k-1})}{Z(G_k)} = \Pr_{I}[v_k \notin I],$$

  where $I$ is a uniform independent set of $G_k$. Removing $v_k$ from the sets that contain it is one to one, so each ratio $\Pr[v_k \notin I]$ is at least $1/2$, and $O(n/\varepsilon^2)$ samples per ratio estimate the product within $1 \pm \varepsilon$ with constant probability. For the path with 4 vertices, the counts $Z(G_0), \ldots, Z(G_4)$ are $1, 2, 3, 5, 8$, Fibonacci numbers (OEIS A000045), and the ratios are $1/2$, $2/3$, $3/5$ and $5/8$. The product of their inverses is $2 \cdot \tfrac{3}{2} \cdot \tfrac{5}{3} \cdot \tfrac{8}{5} = 8$.
- **Perfect matchings.** The number of perfect matchings of a bipartite graph is the [permanent](/permanent-computation/) of its 0-1 biadjacency matrix. Exact computation is #P-complete, while the FPRAS of Jerrum, Sinclair and Vigoda approximates it in polynomial time.

## Known algorithms

- **Plain Monte Carlo.** Sample uniformly from a larger set $U \supseteq R(x)$ whose size is known, and multiply $|U|$ by the fraction of samples in $R(x)$. This needs about $|U|/(\varepsilon^2 f(x))$ samples, so it works only when $f(x)/|U|$ is at least an inverse polynomial. See [rejection sampling](/rejection-sampling/).
- **Karp-Luby and union of sets.** For a union of sets with known sizes, uniform sampling and membership tests, the [Karp-Luby estimator](/karp-luby-algorithm/) uses [importance sampling](/importance-sampling/) over pairs (set, element). It gives an FPRAS for [DNF counting](/dnf-counting/) and is the basis of FPRAS results for network reliability.
- **Markov chain Monte Carlo.** For self-reducible problems, write the count as a product of ratios, as in the product estimator, and estimate each ratio by sampling with a [Markov chain](/markov-chain/). The algorithm is polynomial when the chain has [rapid mixing](/rapid-mixing/), which is proved by [canonical paths](/canonical-paths/), [conductance](/conductance/), [coupling](/coupling-method/) or [path coupling](/path-coupling/). This gives the FPRAS results for matchings, the permanent, the Ising model, colorings with many colors, and the volume of a convex body.
- **Simulated annealing.** Instead of removing one vertex at a time, change a temperature or weight parameter in a sequence of steps from an easy value to the target value. Good cooling schedules reduce the number of steps, and so the number of samples.
- **Correlation decay.** For some spin systems, the probability that a vertex is occupied depends only weakly on far away parts of the graph. Weitz used this, through a tree of self-avoiding walks, to give a deterministic FPTAS for independent sets in graphs of maximum degree at most 5.
- **Dynamic programming with rounding.** Dyer gave an FPRAS for the number of solutions of a knapsack inequality, by rounding the weights, counting the rounded problem exactly with [dynamic programming](/knapsack-dynamic-programming/), and correcting by rejection sampling. Later work turned this into a deterministic FPTAS.
- **Hashing.** Random hash functions cut the solution set into cells of about equal size. With a SAT solver or an NP oracle to test whether a cell is empty, the number of cells needed to make them empty gives a constant-factor estimate, which can then be refined. This is Stockmeyer's method, and the basis of practical approximate [model counting](/model-counting/) tools.

## Bounds

- **Sample complexity.** For a random variable in $[0, 1]$ with mean $\mu$ and variance $\sigma^2$, Dagum, Karp, Luby and Ross gave an algorithm that estimates $\mu$ within $1 \pm \varepsilon$ with probability $1 - \delta$, using a number of samples within a constant factor of the least possible, about $\max(\sigma^2, \varepsilon \mu) \ln(1/\delta) / (\varepsilon^2 \mu^2)$. The algorithm does not need to know $\mu$ or $\sigma^2$ in advance.
- **Hardness from decision.** If the problem "is $f(x) > 0$" is NP-complete, there is no FPRAS for $f$ unless NP = RP, because an FPRAS decides it with bounded error. So #SAT and the number of Hamiltonian cycles have no FPRAS unless NP = RP.
- **Hardness with an easy decision problem.** Sly showed that the number of independent sets in graphs of maximum degree 6 has no FPRAS unless NP = RP, although every graph has an independent set. Together with Weitz's algorithm for maximum degree 5, this places the threshold exactly between degrees 5 and 6.
- **An upper bound.** By Stockmeyer, every function in #P has a randomized approximation scheme that runs in polynomial time with an NP oracle. So approximate counting is in the polynomial hierarchy, while by [Toda's theorem](/toda-theorem/) every problem in the hierarchy reduces to exact counting.

## Reductions

- **Counting and sampling.** For self-reducible relations, an FPRAS gives an almost uniform sampler and the other way round. The sampler is built by fixing the solution one piece at a time, with probabilities given by estimated counts; the counter is the product estimator.
- **Approximation-preserving reductions.** Dyer, Goldberg, Greenhill and Jerrum defined AP-reductions, which keep the existence of an FPRAS. Under them #SAT is complete for #P, and the number of independent sets of a bipartite graph (#BIS) is complete for an intermediate class.
- **Parsimonious reductions.** A [parsimonious reduction](/parsimonious-reduction/) preserves the number of solutions exactly, so it transfers both exact and approximate counting results.
- **Complementation does not work.** The count of a CNF is $2^n$ minus the count of the DNF of its negation, but a relative error on the DNF count gives no relative error on the CNF count when the latter is small. This is why DNF counting has an FPRAS and CNF counting does not, unless NP = RP.

## Applications

- **Network reliability.** The probability that a network with random edge failures becomes disconnected. Karger gave an FPRAS for all-terminal unreliability, using the Karp-Luby method on the small cuts of the graph.
- **Probabilistic databases.** The probability that a query is true in a database with independent uncertain tuples is the probability of a DNF formula of the tuples, which the Karp-Luby method estimates.
- **Statistical physics.** Partition functions of the Ising model, the hard-core model and the monomer-dimer model, from which free energies and other quantities follow.
- **Probabilistic inference and verification.** Approximate [model counting](/model-counting/) of CNF formulas with hashing and SAT solvers, used for inference in graphical models and for the amount of information that a program leaks.
- **Volume and integration.** The volume of a convex body given by a membership oracle has an FPRAS by random walks, while deterministic algorithms need an exponential number of oracle calls for a good approximation.

## References
