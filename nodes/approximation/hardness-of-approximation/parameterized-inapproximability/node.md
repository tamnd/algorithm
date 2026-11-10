---
tag: QXS8RT
kind: concept
slug: parameterized-inapproximability
name: Parameterized inapproximability
aliases:
- W[1]-hardness of approximation
- FPT-inapproximability
- hardness of FPT approximation
area: approximation/hardness-of-approximation
level: research
summary: Showing that no algorithm in time f(k) n^O(1) approximates a parameterized problem within a given ratio, under W[1] ≠ FPT, ETH or Gap-ETH. Clique and dominating set are the main cases.
prereqs: [fpt-approximation, fixed-parameter-tractable, parameterized-reduction, clique-w1-completeness, gap-eth]
see_also: [parameterized-clique, parameterized-dominating-set, clique-inapproximability, dominating-set-inapproximability, k-center-inapproximability, k-median-inapproximability, label-cover, gap-preserving-reduction]
sources:
  - paper: doi:10.1109/FOCS.2017.74
    title: P. Chalermsook, M. Cygan, G. Kortsarz, B. Laekhanukit, P. Manurangsi, D. Nanongkai and L. Trevisan, From Gap-ETH to FPT-inapproximability, clique, dominating set, and more, FOCS 2017
    locator: under Gap-ETH, no FPT algorithm with ratio o(k) for clique and none with any ratio f(k) for dominating set
  - paper: doi:10.1145/3406325.3451016
    title: Bingkai Lin, Constant approximating k-clique is W[1]-hard, STOC 2021
    locator: no FPT algorithm with a constant ratio for clique unless W[1] = FPT
  - paper: doi:10.1145/3188745.3188896
    title: Karthik C. S., B. Laekhanukit and P. Manurangsi, On the parameterized complexity of approximating dominating set, STOC 2018
    locator: no FPT algorithm with any ratio f(k) for dominating set unless W[1] = FPT, and running-time bounds under ETH and SETH
  - paper: "Y. Chen and B. Lin, The constant inapproximability of the parameterized dominating set problem, FOCS 2016"
    locator: no FPT algorithm with a constant ratio for dominating set unless W[1] = FPT
  - paper: "D. Marx, Parameterized complexity and approximation algorithms, The Computer Journal 51(1), 2008"
    locator: the definitions of FPT approximation for minimization and maximization problems
  - paper: "A. E. Feldmann, Karthik C. S., E. Lee and P. Manurangsi, A survey on approximation in parameterized complexity, hardness and algorithms, Algorithms 13(6), 2020"
    locator: the survey of results and hypotheses, including the parameterized inapproximability hypothesis
  - book: isbn:9783319212746
    title: M. Cygan, F. V. Fomin, Ł. Kowalik, D. Lokshtanov, D. Marx, M. Pilipczuk, M. Pilipczuk and S. Saurabh, Parameterized Algorithms
    locator: Chapters 13 and 14 (W[1]-hardness, and lower bounds from the exponential time hypothesis)
---

Parameterized inapproximability is the study of lower bounds for [FPT approximation](/fpt-approximation/): algorithms that run in time $f(k) \cdot n^{O(1)}$, for a computable $f$ and a parameter $k$, and return a solution within some ratio that may depend on $k$. Many problems that are hard to approximate in polynomial time, such as [clique](/clique-inapproximability/), become hard to solve exactly but easy to approximate when extra time $f(k)$ is allowed, and the question is when the extra time helps. The main results are that clique has no FPT algorithm with ratio $o(k)$ and dominating set none with any ratio $g(k)$, under [Gap-ETH](/gap-eth/) (Chalermsook et al. 2017), and that both have no constant ratio unless W[1] = FPT (Chen and Lin 2016, Karthik, Laekhanukit and Manurangsi 2018, Lin 2021).

## In plain words

Some hard problems become easier when one number in the input is small. A method may take time that grows very fast with that number, as long as it grows only slowly with the size of the input. Finding a group of $k$ people who all know each other is the usual example: nobody knows such a method for it.

A natural hope is that approximation helps here. Perhaps, with time that grows fast in $k$, one can at least find a group of $k / 2$ people who all know each other. Parameterized inapproximability shows that this hope fails for some problems. For the group problem, finding even a group of size $k / c$ for a fixed $c$ is as hard as the exact problem. For the problem of picking $k$ people who together know everybody, no ratio at all is possible.

## The idea

**FPT approximation.** Let $k$ be the parameter, usually the size of the wanted solution. For a minimization problem such as [dominating set](/parameterized-dominating-set/), an FPT algorithm with ratio $\rho(k)$ gets a graph and $k$ with $\mathrm{OPT} \le k$, runs in time $f(k) \cdot n^{O(1)}$, and returns a solution of size at most $\rho(k) \cdot k$. For a maximization problem such as [clique](/parameterized-clique/), it gets $k$ with $\mathrm{OPT} \ge k$ and returns a solution of size at least $k / \rho(k)$. A problem with no FPT algorithm for any computable ratio $\rho$ is called **totally FPT-inapproximable**. For clique, returning one vertex is a ratio $k$, so the strongest possible statement is that no ratio $o(k)$ is possible.

**Three kinds of assumption.** The lower bounds use the same three assumptions as exact parameterized lower bounds, in increasing strength.

- **W[1] $\ne$ FPT.** This is the standard assumption that $k$-clique has no algorithm in time $f(k) \cdot n^{O(1)}$; see [clique W[1]-completeness](/clique-w1-completeness/). It is the weakest, and the hardest to use: the reduction must create the gap itself, since $k$-clique has no gap.
- **ETH.** 3-SAT needs time $2^{\Omega(n)}$. It implies W[1] $\ne$ FPT and gives bounds on the exponent, such as no $n^{o(k)}$ time.
- **Gap-ETH.** A constant gap for 3-SAT needs time $2^{\Omega(n)}$. Here the gap comes from the assumption, and the reductions only have to keep it while moving it to a problem with parameter $k$.

**The integer gap.** Some bounds come for free from exact hardness. Let a minimization problem have integer values, and let deciding $\mathrm{OPT} \le k$ be W[1]-hard. If an FPT algorithm has ratio $\rho < \frac{k + 1}{k}$, then on an instance with $\mathrm{OPT} \le k$ it returns a value below $k + 1$, so at most $k$, and on an instance with $\mathrm{OPT} \ge k + 1$ it returns at least $k + 1$. So it decides the W[1]-hard question. This bound tends to 1 as $k$ grows, so it says almost nothing. A real gap needs either a reduction that makes one or an assumption that has one.

**How the Gap-ETH proofs work.** Chalermsook et al. start from a gap 3-SAT formula on $n$ variables, split the variables into $k$ blocks, and make a 2-CSP with one variable per block and alphabet size $N = 2^{n / k}$. An algorithm in time $N^{o(k)}$ for its gap version would run in time $2^{o(n)}$, against Gap-ETH. Then each problem gets its own reduction. The two items below are an outline; the full proofs are in the paper.

- For clique, the vertices of the new graph are the pairs (block, assignment of that block), and edges join consistent pairs. A $k$-clique is a full satisfying assignment. A large clique in a graph from an unsatisfiable formula would give a partial assignment that satisfies too many constraints, and a careful choice of the blocks rules this out for cliques of size $k / \rho(k)$ when $\rho = o(k)$.
- For dominating set, the 2-CSP gap is moved to a set cover instance with $k$ parts, in the style of the [label cover](/label-cover/) reduction to set cover. A small dominating set gives a labeling with many satisfied constraints, and the gap of the CSP becomes a gap of any size $g(k)$ in the dominating set.

**How the W[1] proofs work.** Without a gap in the assumption, the reduction has to make one from exact $k$-clique, in time $f(k) \cdot n^{O(1)}$ and with the new parameter bounded by a function of $k$. Chen and Lin (2016) did this for dominating set with a constant gap. Karthik, Laekhanukit and Manurangsi (2018) extended it to every ratio $g(k)$ with a construction they call threshold graph composition, which uses error-correcting codes. For clique, the gap step was found only by Lin (2021), with a new combinatorial construction.

**Pitfalls.**

- The ratio may depend on $k$, so "no constant ratio" and "no $g(k)$ ratio for any $g$" are different results.
- The reduction must keep the new parameter bounded by a function of $k$ alone. A reduction from clique that makes the parameter grow with $n$, as in the polynomial-time proofs, does not give a parameterized bound.
- A problem may be both W[1]-hard to solve exactly and easy to approximate in FPT time. So W[1]-hardness of the exact problem says nothing about its FPT approximations, beyond the integer gap above.

## Examples

**The integer gap for dominating set.** For $k = 5$, the bound is $\frac{6}{5} = 1.2$: an algorithm in time $f(5) \cdot n^{O(1)}$ that returns a dominating set of size at most $1.19 \cdot \mathrm{OPT}$ returns one of size at most $\lfloor 1.19 \cdot 5 \rfloor = 5$ whenever one of size 5 exists. So it solves 5-dominating set, which is W[2]-hard. The real results are much stronger: by Karthik, Laekhanukit and Manurangsi, no ratio such as $2^{2^{k}}$ is possible either, unless W[1] = FPT.

**$k$-center.** With distances 1 and 2 taken from a graph, $k$ centers of radius 1 exist if and only if the graph has a dominating set of size $k$. So an FPT algorithm with ratio below 2 for $k$-center would solve $k$-dominating set. The integer gap here is 2 and does not shrink with $k$, because the values are only 1 and 2. This reduction is on the [k-center inapproximability](/k-center-inapproximability/) page.

**Clique with a trivial ratio.** For clique, a single vertex is a solution of size $1 = k / k$, so the ratio $k$ is always reached. By Lin (2021), a ratio of any constant $c$, for example finding a clique of size $k / 2$ in a graph with a $k$-clique, is W[1]-hard. Under Gap-ETH, Chalermsook et al. rule out every ratio $o(k)$, so even a clique of size $\log k$ cannot be found in FPT time. A ratio such as $\log k$ is ruled out under Gap-ETH, but not by Lin's constant bound alone.

## Where it is used

- **Lower bounds for clustering.** Under Gap-ETH, $k$-median has no FPT algorithm with ratio below $1 + \frac{2}{e}$, which matches the known FPT algorithm with ratio $1 + \frac{2}{e} + \varepsilon$ (Cohen-Addad et al. 2019); see [k-median inapproximability](/k-median-inapproximability/).
- **Set cover with few sets.** Dominating set and set cover are the same problem here; see [dominating set inapproximability](/dominating-set-inapproximability/). So set cover with parameter $k$, the number of sets, has no FPT algorithm with any ratio $g(k)$ unless W[1] = FPT.
- **Hypotheses for gap CSPs.** The parameterized inapproximability hypothesis (PIH) says that a constant gap for 2-CSPs with $k$ variables is W[1]-hard. It plays the role of the PCP theorem in parameterized complexity. Guruswami, Lin, Ren, Sun and Wu (2024) proved it under ETH.
- **Choosing which problems to approximate.** Results of this kind show where FPT approximation is worth trying. For $k$-cut, which is W[1]-hard to solve exactly, Gupta, Lee and Li (2018) gave an FPT algorithm with a ratio below 2, the best polynomial ratio, so here the extra time does help.

## References
