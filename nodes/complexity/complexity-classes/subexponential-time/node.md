---
tag: FBHRTC
kind: definition
slug: subexponential-time
name: Subexponential time
aliases:
- SUBEXP
area: complexity/complexity-classes
level: advanced
summary: Two related notions. The class SUBEXP of problems solvable in time 2^(n^e) for every e > 0, and the wider set of running times 2^(o(n)) used by the exponential time hypothesis.
prereqs: [quasi-polynomial-time, exptime]
see_also: [quasi-polynomial-time, exptime, strong-exponential-time-hypothesis, integer-factorization, planar-separator-theorem, hardness-versus-randomness, unique-games-subexponential-algorithm, subexponential-parameterized-algorithm]
sources:
  - paper: doi:10.1006/jcss.2000.1727
    title: Russell Impagliazzo and Ramamohan Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 367 to 375 (2001)
    locator: the statement of the exponential time hypothesis
  - paper: doi:10.1006/jcss.2001.1774
    title: Russell Impagliazzo, Ramamohan Paturi and Francis Zane, Which problems have strongly exponential complexity?, Journal of Computer and System Sciences 63(4), 512 to 530 (2001)
    locator: the sparsification lemma and subexponential reduction families
  - paper: doi:10.1007/BF01275486
    title: László Babai, Lance Fortnow, Noam Nisan and Avi Wigderson, BPP has subexponential time simulations unless EXPTIME has publishable proofs, Computational Complexity 3(4), 307 to 318 (1993)
    locator: the main theorem
  - paper: doi:10.1145/800061.808746
    title: László Babai and Eugene M. Luks, Canonical labeling of graphs, 15th ACM Symposium on Theory of Computing, 171 to 183 (1983)
    locator: the 2^(O(sqrt(n log n))) bound for graph isomorphism
  - paper: doi:10.1137/0209046
    title: Richard J. Lipton and Robert Endre Tarjan, Applications of a planar separator theorem, SIAM Journal on Computing 9(3), 615 to 627 (1980)
    locator: the 2^(O(sqrt n)) algorithms for NP-complete problems on planar graphs
  - paper: doi:10.1090/S0894-0347-1992-1137100-0
    title: Hendrik W. Lenstra Jr. and Carl Pomerance, A rigorous time bound for factoring integers, Journal of the American Mathematical Society 5(3), 483 to 516 (1992)
    locator: the main theorem
---

Subexponential time means running time that grows more slowly than any exponential $2^{cn}$ in the input size $n$. The phrase has two meanings in use. In structural complexity, the class SUBEXP contains the problems solvable in time $2^{n^\varepsilon}$ for every $\varepsilon > 0$. In the study of exact algorithms and of the exponential time hypothesis, "subexponential" means time $2^{o(n)}$, where $n$ is often a natural parameter such as the number of variables rather than the input length. The second notion is weaker: $2^{\sqrt{n}}$ and $2^{n / \log n}$ are subexponential in the second sense, but neither bound alone puts a problem in SUBEXP. Both notions sit between [quasi-polynomial time](/quasi-polynomial-time/) and [EXP](/exptime/), and whether NP-complete problems have subexponential algorithms is open.

## Definition

**The class SUBEXP.**

$$\mathsf{SUBEXP} = \bigcap_{\varepsilon > 0} \mathsf{DTIME}\big(2^{n^\varepsilon}\big),$$

where $n$ is the input length and $\mathsf{DTIME}(t(n))$ is deterministic time $O(t(n))$ on a multitape Turing machine. A language is in SUBEXP if for each $\varepsilon > 0$ there is some algorithm, which may depend on $\varepsilon$, running in time $2^{n^\varepsilon}$. By the [time hierarchy theorem](/time-hierarchy-theorem/),

$$\mathsf{P} \subsetneq \mathsf{QP} \subsetneq \mathsf{SUBEXP} \subsetneq \mathsf{EXP}.$$

The class is closed under polynomial-time many-one reductions, since $2^{(n^k)^{\varepsilon}} = 2^{n^{k\varepsilon}}$ and $\varepsilon$ is arbitrary. The variant i.o.-SUBEXP asks only that the algorithm be correct for infinitely many input lengths.

**Time $2^{o(n)}$.** A problem with a size parameter $n$ is solvable in subexponential time in the second sense if it has an algorithm with running time $2^{f(n)} \cdot \mathrm{poly}(N)$ for some function $f(n) = o(n)$, where $N$ is the input length. For 3-SAT the parameter is the number of variables $n$. The exponential time hypothesis (ETH) of Impagliazzo and Paturi states that 3-SAT has no algorithm with time $2^{o(n)}$. Impagliazzo, Paturi and Zane (2001) introduced reductions that preserve this notion, and with their sparsification lemma ETH also rules out time $2^{o(m)}$ for $m$ clauses.

**How the two notions relate.** A 3-CNF formula over $n$ variables has at most $8 \binom{n}{3}$ distinct clauses, so its length is $N = O(n^3 \log n)$. If 3-SAT were in SUBEXP, take $\varepsilon = 1/6$: the time would be $2^{N^{1/6}} = 2^{O(n^{1/2} (\log n)^{1/6})} = 2^{o(n)}$. So ETH implies that 3-SAT is not in SUBEXP, and that $\mathsf{NP} \not\subseteq \mathsf{SUBEXP}$. The converse fails: an algorithm with time $2^{n / \log n}$ would refute ETH but would not put 3-SAT in SUBEXP.

## Examples and non-examples

**The measure of size matters.** The clique problem on a graph with $n$ vertices has an input of $N = n(n-1)/2$ bits. Trying all vertex subsets takes time about $2^n$, which is $2^{c \sqrt{N}}$ with $c = n / \sqrt{N}$:

| $n$ | $N$ | $c$ |
|---|---|---|
| $20$ | $190$ | $1.451$ |
| $40$ | $780$ | $1.432$ |
| $80$ | $3160$ | $1.423$ |

The constant tends to $\sqrt{2}$. So brute force is subexponential in the input length in the second sense, while ETH implies that no algorithm runs in time $2^{o(n)}$ in the number of vertices. Statements about subexponential time must name the parameter.

**Graph isomorphism.** Babai and Luks (1983) decided graph isomorphism in time $2^{O(\sqrt{n \log n})}$ for $n$ vertices. This is subexponential in the second sense, and in the input length $N \approx n^2$ it is $2^{O(N^{1/4} \sqrt{\log N})}$, which is below $2^{N^\varepsilon}$ only for $\varepsilon > 1/4$. Babai (2016) improved the bound to [quasi-polynomial time](/quasi-polynomial-time/), which puts graph isomorphism in SUBEXP.

**Planar graphs.** Lipton and Tarjan (1980) used the [planar separator theorem](/planar-separator-theorem/) to solve NP-complete problems on [planar graphs](/planar-graph/), such as [maximum independent set](/maximum-independent-set/), in time $2^{O(\sqrt{n})}$. Under ETH, many of these bounds cannot be improved to $2^{o(\sqrt{n})}$. [Bidimensionality theory](/bidimensionality-theory/) extends the method to parameterized problems, see [subexponential parameterized algorithms](/subexponential-parameterized-algorithm/).

**Integer factoring.** Let $N$ be the integer to factor and $n = \log_2 N$ its length in bits. Write $L_N[\alpha, c] = \exp\big(c (\ln N)^\alpha (\ln \ln N)^{1-\alpha}\big)$. Lenstra and Pomerance (1992) proved a randomized bound of $L_N[1/2, 1 + o(1)]$. The [general number field sieve](/general-number-field-sieve/) runs in time $L_N[1/3, (64/9)^{1/3} + o(1)]$, where $(64/9)^{1/3} \approx 1.923$, under heuristic assumptions. Both are $2^{o(n)}$, but neither is $2^{n^\varepsilon}$ for every $\varepsilon$, so [factoring](/integer-factorization/) is not known to be in SUBEXP. The table gives $\log_2$ of the two bounds with the $o(1)$ terms set to zero:

| bits $n$ | $L_N[1/2, 1]$ | $L_N[1/3, 1.923]$ |
|---|---|---|
| $512$ | $65.9$ | $63.9$ |
| $1024$ | $98.5$ | $86.8$ |
| $2048$ | $146.4$ | $116.9$ |

**Derandomization.** Babai, Fortnow, Nisan and Wigderson (1993) proved that $\mathsf{BPP} \subseteq \text{i.o.-}\mathsf{SUBEXP}$ unless $\mathsf{EXP} = \mathsf{MA}$. This is one of the results that trade [hardness for randomness](/hardness-versus-randomness/).

**Unique games.** Arora, Barak and Steurer gave a [subexponential algorithm for unique games](/unique-games-subexponential-algorithm/): for instances in which a $1 - \varepsilon$ fraction of the constraints can be satisfied, its time is $2^{n^{\delta}}$ with $\delta$ tending to $0$ as $\varepsilon$ does. So a reduction from 3-SAT to unique games, if one exists, must enlarge the instance by a polynomial whose degree grows as $\varepsilon$ shrinks, unless 3-SAT has algorithms with time $2^{o(n)}$.

**Non-examples.** The best known algorithms for [3-SAT](/3-sat/), such as [Schöning's algorithm](/schoning-algorithm/) and the [PPSZ algorithm](/ppsz-algorithm/), run in time $c^n$ for constants $c > 1$, which is exponential. The [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) states that the base for [k-SAT](/k-sat/) tends to $2$ as $k$ grows. Problems complete for EXP are not in SUBEXP, by the hierarchy theorem.

## Related definitions

- [Quasi-polynomial time](/quasi-polynomial-time/): time $2^{(\log n)^{O(1)}}$, a smaller class inside SUBEXP.
- [EXP](/exptime/): time $2^{n^{O(1)}}$, which strictly contains SUBEXP.
- The exponential time hypothesis and the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/): lower bounds for k-SAT in the $2^{o(n)}$ sense. The [Gap-ETH](/gap-eth/) variant adds an approximation gap.
- [Subexponential parameterized algorithms](/subexponential-parameterized-algorithm/): time $2^{o(k)} \cdot \mathrm{poly}(n)$ in a parameter $k$.

## References
