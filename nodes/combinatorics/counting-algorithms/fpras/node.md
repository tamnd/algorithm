---
tag: PDTQ1F
kind: definition
slug: fpras
name: Fully polynomial randomized approximation scheme (FPRAS)
aliases:
- FPRAS
- fully polynomial randomised approximation scheme
area: combinatorics/counting-algorithms
level: research
summary: A randomized algorithm giving a (1±ε) estimate in time polynomial in input size and 1/ε.
prereqs: [randomized-algorithm, monte-carlo-algorithm, hoeffding-inequality]
see_also: [approximate-counting, fptas, karp-luby-algorithm, jerrum-valiant-vazirani-theorem, median-trick, dnf-counting, rp, ptas]
sources:
  - paper: doi:10.1109/SFCS.1983.35
    title: Richard M. Karp and Michael Luby, Monte-Carlo algorithms for enumeration and reliability problems, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983), 56 to 64
    locator: the definition of a fully polynomial randomized approximation scheme and the scheme for DNF counting
  - paper: doi:10.1016/0304-3975(86)90174-X
    title: Mark R. Jerrum, Leslie G. Valiant and Vijay V. Vazirani, Random generation of combinatorial structures from a uniform distribution, Theoretical Computer Science 43, 169 to 188, 1986
    locator: the definitions of randomized approximate counting and almost uniform generation, and their equivalence for self-reducible problems
  - book: isbn:9783764369460
    title: Mark Jerrum, Counting, Sampling and Integrating, Algorithms and Complexity, Lectures in Mathematics ETH Zurich, Birkhauser, 2003
    locator: the chapter on sampling and counting (the definitions of FPRAS and FPAUS)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 11, Approximate Counting (randomized approximation schemes)
  - paper: doi:10.1145/1008731.1008738
    title: Mark Jerrum, Alistair Sinclair and Eric Vigoda, A polynomial-time approximation algorithm for the permanent of a matrix with nonnegative entries, Journal of the ACM 51(4), 671 to 697, 2004
    locator: the main theorem (an FPRAS for the permanent of a nonnegative matrix)
  - paper: doi:10.1007/s00453-003-1073-y
    title: Martin Dyer, Leslie Ann Goldberg, Catherine Greenhill and Mark Jerrum, The relative complexity of approximate counting problems, Algorithmica 38(3), 471 to 500, 2004
    locator: "the definition of approximation-preserving reductions and of the class #BIS"
  - paper: doi:10.1109/FOCS.2010.34
    title: Allan Sly, Computational transition at the uniqueness threshold, 51st Annual Symposium on Foundations of Computer Science (FOCS 2010), 287 to 296
    locator: the main theorem (no FPRAS for independent sets in graphs of maximum degree 6 unless NP = RP)
---

A fully polynomial randomized approximation scheme (FPRAS) for a counting function $f$ is a randomized algorithm that, given an input $x$ and an error bound $\varepsilon$, returns a number within a factor $1 \pm \varepsilon$ of $f(x)$ with probability at least $3/4$, in time polynomial in the size of $x$ and in $1/\varepsilon$. It is the standard notion of an efficient approximation for #P-hard counting problems, where exact polynomial algorithms are not expected. The error is relative, so an FPRAS must tell $f(x) = 0$ apart from $f(x) \ge 1$; this is why many counting problems whose decision version is NP-complete have no FPRAS unless NP = RP. The notion goes back to Karp and Luby (1983), whose [estimator for DNF counting](/karp-luby-algorithm/) is the first standard example.

## Definition

Let $f : \Sigma^* \to \mathbb{R}_{\ge 0}$ be a function, usually a count such as the number of solutions of an instance $x$.

A *randomized approximation scheme* for $f$ is a randomized algorithm that takes an input $x \in \Sigma^*$ and a rational $\varepsilon$ with $0 < \varepsilon < 1$, and returns a random number $Y$ such that

$$\Pr\big[(1 - \varepsilon) f(x) \le Y \le (1 + \varepsilon) f(x)\big] \ge \tfrac{3}{4}.$$

It is *fully polynomial* if its running time is bounded by a polynomial in $|x|$ and $1/\varepsilon$. A fully polynomial randomized approximation scheme is an FPRAS.

**The other form of the error.** Many authors, Jerrum among them, ask for $e^{-\varepsilon} f(x) \le Y \le e^{\varepsilon} f(x)$ instead. For $0 < \varepsilon < 1$, a result with $e^{\pm \varepsilon/2}$ error has $1 \pm \varepsilon$ error, and a result with $1 \pm \varepsilon/2$ error has $e^{\pm \varepsilon}$ error. So the two forms give the same class of functions, and only $\varepsilon$ changes by a factor of 2.

**The confidence.** The constant $3/4$ can be any constant above $1/2$. Given a target failure probability $\delta$, run the scheme $k$ times, with $k$ odd and $k \ge 8 \ln(1/\delta)$, and return the median of the $k$ results. The median is outside the interval only if at least $k/2$ runs fail. The number of failed runs is a sum of $k$ independent 0-1 variables, each with mean at most $1/4$, so by Hoeffding's inequality this has probability at most $e^{-2k(1/4)^2} = e^{-k/8} \le \delta$. For $\delta = 0.01$, $8 \ln 100 \approx 36.8$, so $k = 37$ runs are enough. This is the [median trick](/median-trick/), and the total running time is polynomial in $|x|$, $1/\varepsilon$ and $\log(1/\delta)$.

**Zero values.** If $f(x) = 0$, the interval is the single point 0, so an FPRAS must return exactly 0 with probability at least $3/4$.

## Examples and non-examples

- **DNF counting.** The [Karp-Luby estimator](/karp-luby-algorithm/) is an FPRAS for the number of satisfying assignments of a DNF formula, a #P-complete function. It uses $O(m \log(1/\delta)/\varepsilon^2)$ samples for $m$ clauses.
- **The permanent.** Jerrum, Sinclair and Vigoda (2004) gave an FPRAS for the [permanent](/permanent-computation/) of a matrix with nonnegative entries, and so for the number of perfect matchings of a bipartite graph. Exact computation is #P-complete.
- **Partition functions.** Jerrum and Sinclair gave an FPRAS for the partition function of the ferromagnetic Ising model, and for the number of all matchings of a graph, by Markov chain Monte Carlo with [rapid mixing](/rapid-mixing/).
- **Colorings.** For graphs of maximum degree $\Delta$ and $q > 2\Delta$ colors, Glauber dynamics mixes rapidly, and this gives an FPRAS for the number of proper [colorings](/counting-graph-colorings/).
- **Knapsack solutions.** Dyer (2003) gave an FPRAS for the number of 0-1 solutions of a knapsack inequality. Later work gave a deterministic FPTAS.
- **Every FPTAS.** A deterministic scheme with the same error and running time is an FPRAS that never fails. For example, Weitz (2006) gave a deterministic [FPTAS](/fptas/) for independent sets in graphs of maximum degree at most 5.
- **Non-example: CNF counting.** If #SAT had an FPRAS, then running it on a CNF formula and testing whether the result is nonzero would decide SAT with error at most $1/4$. This puts SAT in BPP, and NP $\subseteq$ BPP implies NP = [RP](/rp/). So #SAT has no FPRAS unless NP = RP. The same argument applies to every counting problem whose decision version is NP-complete.
- **Non-example: independent sets of large degree.** Sly (2010) showed that the number of independent sets in graphs of maximum degree 6 has no FPRAS unless NP = RP, although the decision problem is trivial.
- **Non-example: additive error.** Testing $t$ random assignments of a formula gives $2^n$ times the fraction that satisfy it. Its error is about $2^n/\sqrt{t}$, an additive error. When the true count is small, say 1, the relative error is huge, so this is not an FPRAS.
- **Non-example: a PRAS.** An algorithm with running time $|x|^{1/\varepsilon}$ is polynomial for each fixed $\varepsilon$ but not in $1/\varepsilon$. It is a polynomial randomized approximation scheme, not a fully polynomial one, in the same way that a [PTAS](/ptas/) need not be an FPTAS.

## Related definitions

- **[FPTAS](/fptas/).** The deterministic counterpart. For counting problems it is a deterministic algorithm with the same error and running time. Every FPTAS is an FPRAS.
- **FPAUS.** A fully polynomial almost uniform sampler draws a solution from a distribution within total variation distance $\delta$ of uniform, in time polynomial in $|x|$ and $\log(1/\delta)$. For self-reducible problems, an FPRAS exists if and only if an FPAUS exists; this is the [Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/), which also shows that a constant-factor approximation can be boosted to an FPRAS for [self-reducible](/self-reducibility/) problems.
- **Approximation-preserving reductions.** Dyer, Goldberg, Greenhill and Jerrum defined AP-reductions, under which the existence of an FPRAS is closed. Under them, #SAT is complete for all of #P, and counting independent sets in bipartite graphs (#BIS) is complete for a class of problems that are believed to have no FPRAS but are not known to be as hard as #SAT.
- **Approximate counting with an oracle.** Stockmeyer (1985) showed that every function in #P has a randomized approximation scheme that runs in polynomial time with an NP oracle.
- **[Approximate counting](/approximate-counting/).** The general problem of estimating a count within a relative error, and the methods used for it.
- **[Monte Carlo algorithm](/monte-carlo-algorithm/).** An FPRAS is a Monte Carlo algorithm: its running time is bounded, and its output can be wrong with small probability.

## References
