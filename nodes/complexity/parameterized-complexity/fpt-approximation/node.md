---
tag: FH1JZF
kind: concept
slug: fpt-approximation
name: FPT approximation
aliases:
- parameterized approximation
area: complexity/parameterized-complexity
level: research
summary: "An algorithm in time f(k) n^O(1) that returns a solution within a factor rho(k) of the target k, or proves that none of size k exists. An EPTAS or FPTAS gives an FPT algorithm."
prereqs: [fixed-parameter-tractable, approximation-ratio]
see_also: [parameterized-inapproximability, gap-eth, lossy-kernelization, eptas, fptas, treewidth-computation, parameterized-bandwidth, max-coverage]
sources:
  - paper: doi:10.1093/comjnl/bxm048
    title: "Daniel Marx, Parameterized complexity and approximation algorithms, The Computer Journal 51(1), 60-78 (2008)"
    locator: the definitions of FPT approximation algorithms and FPT approximation schemes, and the scheme for partial vertex cover
  - paper: doi:10.3390/a13060146
    title: "Andreas Emil Feldmann, Karthik C. S., Euiwoong Lee and Pasin Manurangsi, A survey on approximation in parameterized complexity: hardness and algorithms, Algorithms 13(6), article 146 (2020)"
    locator: the survey, the definitions and the list of FPT approximation algorithms and hardness results
  - paper: doi:10.1006/jcss.1997.1490
    title: "Liming Cai and Jianer Chen, On fixed-parameter tractability and approximability of NP optimization problems, Journal of Computer and System Sciences 54(3), 465-474 (1997)"
    locator: a fully polynomial-time approximation scheme implies that the standard parameterization is FPT
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 7.6.2, An FPT approximation algorithm for treewidth"
  - paper: doi:10.1137/22M147551X
    title: "Tuukka Korhonen, A single-exponential time 2-approximation algorithm for treewidth, SIAM Journal on Computing (2023)"
    locator: "the main theorem, a tree decomposition of width at most 2k + 1 or a proof that the treewidth exceeds k, in time 2^O(k) n (conference version FOCS 2021)"
---

An FPT approximation algorithm combines the two ways of coping with NP-hard problems. With the solution size $k$ as the parameter, it runs in time $f(k) \cdot n^{O(1)}$, and it either returns a solution whose value is within a factor $\rho(k)$ of $k$, or proves that no solution of value $k$ exists. It is useful for problems that are W[1]-hard to solve exactly and also hard to approximate in polynomial time. This page covers the algorithms and the link to approximation schemes; the lower bounds are on [parameterized inapproximability](/parameterized-inapproximability/).

## In plain words

Some problems are too hard to solve exactly even when the answer is small, and too hard to approximate well in polynomial time. FPT approximation allows both relaxations at once. The algorithm may spend time that grows fast with the size of the wanted answer, as long as it grows only polynomially with the size of the input. In return it only has to find an answer that is close to the target, not exactly on it, or show that the target is out of reach. The idea also runs in the other direction: a very good polynomial-time approximation for a problem whose answers are whole numbers can be used to solve the exact problem when the answer is small.

## The idea

**Definition (Marx 2008).** Let $\Pi$ be a minimization problem with integer optimum $\mathrm{OPT}(x)$, and let $\rho \ge 1$ be a computable function. An *FPT approximation algorithm with ratio $\rho$* takes $(x, k)$ and, in time $f(k) \cdot |x|^{O(1)}$:

- returns a solution of value at most $\rho(k) \cdot k$, or
- correctly reports that $\mathrm{OPT}(x) > k$.

If $\mathrm{OPT}(x) \le k$, it must return a solution. For a maximization problem, it returns a solution of value at least $k / \rho(k)$ or reports that $\mathrm{OPT}(x) < k$. The parameter is $k$, the target value. An *FPT approximation scheme* takes $\varepsilon > 0$ as well, has ratio $1 + \varepsilon$ (or $1 - \varepsilon$ for maximization), and runs in time $f(k, \varepsilon) \cdot |x|^{O(1)}$.

Every FPT algorithm for the exact problem is an FPT approximation algorithm with ratio 1. So the notion is useful for problems that are not FPT, such as W[1]-hard problems.

**Proposition (approximation schemes give FPT algorithms).** Let $\Pi$ be a minimization problem with integer values. If $\Pi$ has an [EPTAS](/eptas/) with time $g(1/\varepsilon) \cdot n^{c}$, then "is $\mathrm{OPT}(x) \le k$?" is solvable in time $g(k + 1) \cdot n^{c}$, so it is FPT in $k$. An [FPTAS](/fptas/) gives time polynomial in $k$ and $n$.

*Proof.* Run the scheme with $\varepsilon = 1/(k+1)$, and let $s$ be the value of the solution it returns. If $\mathrm{OPT}(x) \le k$, then $s \le (1 + \frac{1}{k+1}) \cdot k = k + \frac{k}{k+1} < k + 1$, so $s \le k$ because $s$ is an integer. If $\mathrm{OPT}(x) > k$, every solution has value greater than $k$, so $s > k$. So the answer is yes exactly when $s \le k$. The time is $g(1/\varepsilon) \cdot n^c = g(k+1) \cdot n^c$. For maximization, use ratio $1 - \frac{1}{k+1}$: if $\mathrm{OPT}(x) \ge k$, then $s \ge k - \frac{k}{k+1} > k - 1$, so $s \ge k$. $\square$

Cai and Chen (1997) proved this for fully polynomial-time approximation schemes. The contrapositive is a tool: if the standard parameterization of $\Pi$ is [W[1]-hard](/w-hardness/), then $\Pi$ has no EPTAS unless $\mathsf{FPT} = \mathsf{W}[1]$.

## Examples

**Partial vertex cover.** Given a graph and $k$, choose $k$ vertices that cover the largest number of edges. This is a special case of [maximum coverage](/max-coverage/). Marx (2008) gave an FPT approximation scheme with parameter $k$. The idea fits in two cases. Let $D$ be the sum of the $k$ largest degrees. The $k$ vertices of largest degree cover at least $D - \binom{k}{2}$ edges, since at most $\binom{k}{2}$ edges join two of them, and no $k$ vertices cover more than $D$ edges. So if $\binom{k}{2} \le \varepsilon D$, the top $k$ vertices are a $(1 - \varepsilon)$-approximation. Otherwise $D < k^2/(2\varepsilon)$, every degree is bounded by a function of $k$ and $\varepsilon$, and the exact problem can be solved in FPT time on such graphs (this part is left out here).

On a random graph with 14 vertices, edge probability 0.3 and seed 6 (Python `random.Random(6)`, 22 edges), the numbers are:

| $k$ | top $k$ degrees | $D - \binom{k}{2}$ | top-$k$ value | optimum | $D$ |
|---|---|---|---|---|---|
| 2 | 6, 5 | 10 | 10 | 10 | 11 |
| 3 | 6, 5, 4 | 12 | 14 | 14 | 15 |
| 4 | 6, 5, 4, 4 | 13 | 16 | 17 | 19 |

At $k = 4$ the top-degree choice is not optimal, but it stays between the two bounds, as the argument says.

**Treewidth.** Computing the treewidth is FPT, but the exact algorithms are slow. Many algorithms only need a tree decomposition of width $O(k)$. Cygan et al., Section 7.6.2, give an FPT approximation algorithm for treewidth. Korhonen (2021) gives time $2^{O(k)} \cdot n$ and width at most $2k + 1$, or a proof that the treewidth exceeds $k$. See [treewidth computation](/treewidth-computation/).

**Bandwidth on trees.** [Bandwidth](/parameterized-bandwidth/) is W[t]-hard for every $t$, even on trees. Dregi and Lokshtanov (2014) give a polynomial-time algorithm on trees that either proves that the bandwidth is greater than $b$ or returns a layout of bandwidth $b^{O(b)}$. The ratio is a function of $b$ alone.

## Where it is used

- **W[1]-hard problems with good approximations.** Clustering problems such as [k-median](/k-median-problem/) and coverage problems are W[1]-hard with $k$ as parameter and hard to approximate in polynomial time beyond fixed ratios. FPT time often allows better ratios. The survey of Feldmann, Karthik, Lee and Manurangsi (2020) lists these results.
- **Subroutines.** Many FPT algorithms first need an approximate structure, such as a tree decomposition of width $O(k)$, and then solve the problem exactly on it. An FPT approximation is enough for this step.
- **Approximate kernels.** [Lossy kernelization](/lossy-kernelization/) is the kernel form of the same idea: a small instance from which a good approximate solution can be lifted.
- **Ruling out schemes.** By the proposition above, W[1]-hardness of the exact problem rules out an EPTAS unless $\mathsf{FPT} = \mathsf{W}[1]$.
- **Limits.** For some problems, no FPT approximation with any ratio $\rho(k)$ exists under standard assumptions. Dominating set and clique are the main cases. These results use [Gap-ETH](/gap-eth/) and are on [parameterized inapproximability](/parameterized-inapproximability/).

## References
