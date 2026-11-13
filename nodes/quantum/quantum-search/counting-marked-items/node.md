---
tag: 2AHMAA
kind: problem
slug: counting-marked-items
name: Counting marked items
aliases:
- quantum counting problem
area: quantum/quantum-search
level: core
summary: Given an oracle for f on N items, find or estimate the number M of items with f(x) = 1. A quantum computer gets relative error ε with O(√(N/M)/ε) queries.
prereqs: [unstructured-search, quantum-query-model]
see_also: [quantum-counting, grover-search, bbht-search, approximate-counting, counting-problem, dnf-counting, polynomial-method, monte-carlo-integration]
sources:
  - paper: doi:10.1007/BFb0055105
    title: "Gilles Brassard, Peter Høyer and Alain Tapp, Quantum counting, Proceedings of ICALP 1998, Lecture Notes in Computer Science 1443, Springer, 1998, pages 820-831 (arXiv:quant-ph/9805082)"
    locator: the whole paper (the counting problem, and its solution by the Fourier transform of the Grover iteration)
  - paper: arxiv:quant-ph/0005055
    title: "Gilles Brassard, Peter Høyer, Michele Mosca and Alain Tapp, Quantum amplitude amplification and estimation, in Quantum Computation and Information, Contemporary Mathematics 305, American Mathematical Society, 2002"
    locator: the counting results (Theorem 13 on additive error, Corollary 14, Theorem 15 on relative error, Theorem 16 on deciding t = 0 or t = t0, and Theorem 17 on exact counting with Theta(sqrt((t+1)(N-t+1))) queries)
  - paper: doi:10.1145/502090.502097
    title: "Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4), 2001, pages 778-797"
    locator: Section 2, Table 1 (THRESHOLD_t needs Theta(sqrt(t(N-t+1))) queries with bounded error; PARITY needs N/2 queries)
  - paper: arxiv:quant-ph/9605034
    title: "Michel Boyer, Gilles Brassard, Peter Høyer and Alain Tapp, Tight bounds on quantum searching, Fortschritte der Physik 46(4-5), 1998, pages 493-505"
    locator: Section 5 (the first sketch of quantum counting, with the error bound (2 pi/P) sqrt(tN) + pi^2 N/P^2)
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Chapter 6, Section 6.3 (quantum counting)
  - book: isbn:9780198570493
    title: Phillip Kaye, Raymond Laflamme and Michele Mosca, An Introduction to Quantum Computing, Oxford University Press, 2007
    locator: Chapter 8, Section 8.3 (quantum amplitude estimation and quantum counting)
---

Counting marked items is the problem of finding, or estimating, the number $M$ of items $x \in \{0, 1, \ldots, N-1\}$ with $f(x) = 1$, when $f$ is given only as an oracle. It is the counting version of [unstructured search](/unstructured-search/), which asks for one marked item. This page is the problem; the algorithm that solves it with a quadratic speedup is [quantum counting](/quantum-counting/), which applies phase estimation to the Grover iteration. With bounded error, $O(\sqrt{N/M}/\varepsilon)$ quantum queries give $M$ within a factor $1 \pm \varepsilon$, against $O(N/(\varepsilon^2 M))$ classical samples.

## In plain words

A box answers yes or no about each of many items. You want to know how many items get a yes. A normal computer can ask about every item, or ask about a random sample and scale up. A small sample is enough for a rough answer when yes items are common, but a rare yes needs many questions.

A quantum computer can ask about many items at once. It cannot read out all answers, but it can measure how fast the search method of Grover turns. That speed depends only on the share of yes items. So it learns the count with about the square root of the questions a sample needs. An exact count is much harder, and a few questions such as "is the count even?" get almost no help.

## Definition

**Input.** A number $N$ and a function $f : \{0, 1, \ldots, N-1\} \to \{0, 1\}$, given as a [quantum oracle](/quantum-oracle/): the bit oracle $|x\rangle|b\rangle \mapsto |x\rangle|b \oplus f(x)\rangle$ or the phase oracle $|x\rangle \mapsto (-1)^{f(x)}|x\rangle$. Let $M = |\{x : f(x) = 1\}|$.

**Output.** One of the following, as the variant asks:

- *Exact count.* $M$ itself.
- *Additive estimate.* A number $\tilde M$ with $|\tilde M - M| \le \Delta$.
- *Relative estimate.* A number $\tilde M$ with $|\tilde M - M| \le \varepsilon M$. For $M = 0$ this asks for $\tilde M = 0$.
- *Decision.* Is $M = 0$? Or is $M \ge t$ for a given $t$ (the threshold function)?

**Cost.** The number of oracle queries, in the [quantum query model](/quantum-query-model/). A randomized or quantum algorithm may fail with probability at most $1/3$; repetition and a median make this smaller.

## Variants

- **Exact counting.** Output $M$ with bounded error.
- **Approximate counting.** Additive error $\Delta$, or relative error $\varepsilon$. A relative estimate also decides whether $M = 0$, so it is at least as hard as the decision version of search.
- **Threshold.** Decide whether $M \ge t$. For $t = 1$ this is $\mathrm{OR}_N$, the decision version of search.
- **Parity.** Decide whether $M$ is even. This is the hardest case for quantum speedup.
- **Weighted counting.** Estimate the mean of a function $g : \{0, \ldots, N-1\} \to [0, 1]$. Amplitude estimation solves this with the same methods; [Monte Carlo integration](/monte-carlo-integration/) is the classical version.

## Examples

**A small table.** $N = 8$ and $f$ is 1 at $x \in \{1, 4, 6\}$. Then $M = 3$ and $M/N = 0.375$.

**Satisfying assignments.** Let $\phi$ be a Boolean formula on $n$ variables, and $f(x) = 1$ if the assignment $x$ satisfies $\phi$. Then $N = 2^n$ and $M$ is the number of satisfying assignments: the classic [counting problem](/counting-problem/) #SAT, here in the oracle setting. For an $n = 40$ formula with about a thousand solutions, a relative estimate within $10\%$ takes about $\sqrt{2^{40}/1000}/0.1 \approx 3.3 \cdot 10^5$ quantum queries, up to a constant, against about $2^{40}/(0.01 \cdot 1000) \approx 1.1 \cdot 10^{11}$ classical samples.

**Number of solutions before a search.** To run [Grover's search](/grover-search/) with the right number of iterations, one needs $M$ within a constant factor. A relative estimate with $\varepsilon = 1/2$ is enough.

## Known algorithms

| algorithm | output | queries | notes |
|---|---|---|---|
| query every item | exact $M$ | $N$ | deterministic, classical |
| random sampling | relative error $\varepsilon$ | $O(N/(\varepsilon^2 M))$ expected | classical, by a [Chernoff bound](/chernoff-bound/) |
| [quantum counting](/quantum-counting/), $P$ steps | additive error $O(\sqrt{M(N-M)}/P + N/P^2)$ | $O(P)$ | Brassard, Høyer and Tapp; Brassard, Høyer, Mosca and Tapp, Theorem 13 |
| quantum counting with a doubling $P$ | relative error $\varepsilon$ | $O(\sqrt{N/M}/\varepsilon)$ expected | Theorem 15 |
| quantum counting, exact version | exact $M$ | $O(\sqrt{(M+1)(N-M+1)})$ expected | Theorem 17 |
| [BBHT search](/bbht-search/) with a time-out | decide $M = 0$ | $O(\sqrt{N})$ | one-sided error |

## Bounds

| question | classical randomized | quantum (bounded error) |
|---|---|---|
| is $M = 0$? | $\Theta(N)$ | $\Theta(\sqrt{N})$ |
| is $M \ge t$? | $\Theta(N)$ in the worst case | $\Theta(\sqrt{t(N-t+1)})$ |
| exact $M$ | $\Theta(N)$ | $\Theta(\sqrt{(M+1)(N-M+1)})$ on inputs with $M$ marked items |
| relative error $\varepsilon$ | $O(N/(\varepsilon^2 M))$ | $O(\sqrt{N/M}/\varepsilon)$ |
| parity of $M$ | $N$ | $N/2$ |

The quantum lower bounds come from the [polynomial method](/polynomial-method/). Beals, Buhrman, Cleve, Mosca and de Wolf show that the threshold function $\mathrm{Th}_t$ needs $\Theta(\sqrt{t(N-t+1)})$ queries and parity needs $N/2$. An exact count decides $\mathrm{Th}_M$, so on inputs near $M$ marked items it needs $\Omega(\sqrt{M(N-M+1)})$ queries, which the exact version of quantum counting meets up to a constant. A relative estimate decides whether $M = 0$, so it needs $\Omega(\sqrt{N/M})$ queries by the [optimality of Grover's search](/grover-optimality/). The parity bound shows that a quantum computer cannot count exactly much faster than a classical one in the worst case $M \approx N/2$.

## Reductions

- **Search to counting.** A relative estimate of $M$ fixes the iteration count of Grover's search, so search with an unknown $M$ reduces to approximate counting plus one Grover run. [BBHT search](/bbht-search/) avoids the count and is cheaper.
- **Decision to counting.** "Is $M = 0$?" is $\mathrm{OR}_N$, and each relative estimate answers it. So counting with relative error is at least as hard as [unstructured search](/unstructured-search/).
- **Counting to phase estimation.** The Grover iteration has eigenvalues $e^{\pm 2i\theta}$ with $\sin^2\theta = M/N$. So estimating $M$ reduces to [phase estimation](/phase-estimation-problem/) of a unitary that costs one query per application. This is the idea of [quantum counting](/quantum-counting/).
- **Classical counting.** For #SAT and other #P-complete counting problems, the oracle bounds above give a quadratic speedup over classical sampling, not a polynomial algorithm. Classical [approximate counting](/approximate-counting/) uses the structure of the problem, as in [DNF counting](/dnf-counting/).

## Applications

- **Tuning a search.** Estimate $M$ first, then run Grover's search with $\lfloor \pi/(4\theta) \rfloor$ iterations.
- **Model counting.** Estimate the number of solutions of a formula or a constraint system, given as a reversible circuit.
- **Estimating a mean.** With amplitude estimation, the mean of a bounded function, and so Monte Carlo estimates of expected values, cost $O(1/\varepsilon)$ evaluations in place of $O(1/\varepsilon^2)$.
- **Deciding existence.** The decision version tells whether any solution exists, with $O(\sqrt{N})$ queries.

## References
