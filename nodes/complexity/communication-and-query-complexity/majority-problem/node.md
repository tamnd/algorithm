---
tag: 2WZJSX
kind: problem
slug: majority-problem
name: Majority problem
aliases:
- MAJORITY
area: complexity/communication-and-query-complexity
level: intro
summary: "Decide whether more than half of n input bits are 1. Deterministic, randomized and quantum query algorithms all need a constant fraction of n queries, and AC0 circuits cannot compute it."
prereqs: [query-model]
see_also: [parity-problem, majority-element-problem, boyer-moore-majority, approximate-degree, sensitivity, tc0, sorting-network, quantum-counting]
sources:
  - paper: doi:10.1145/129712.129758
    title: Ramamohan Paturi, On the degree of polynomials that approximate symmetric Boolean functions, 24th ACM Symposium on Theory of Computing (STOC 1992)
    locator: pp. 468 to 474 (approximate degree of a symmetric function is Theta(sqrt(n (n - Gamma(f)))))
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.4 (approximate degree), Section 6.1 (symmetric functions and Paturi's theorem)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (Q(f) at least half the approximate degree; quantum complexity of symmetric functions)
  - paper: doi:10.1137/0220062
    title: Noam Nisan, CREW PRAMs and decision trees, SIAM Journal on Computing 20(6) (1991)
    locator: pp. 999 to 1007 (bs(f) at most 3 R(f))
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 12, Decision trees; Chapter 14, Circuit lower bounds (PARITY is not in AC0)
---

The majority problem asks whether more than half of $n$ input bits are 1. It is the standard example of a symmetric threshold function in [query complexity](/query-complexity/): a single bit can decide the answer only on inputs near the middle weight, but those inputs force every model, deterministic, randomized or quantum, to make $\Theta(n)$ queries. In circuit complexity it defines the gates of [TC0](/tc0/). This page is about the Boolean function. Finding an element that fills more than half of an array is the different [majority element problem](/majority-element-problem/), solved by the [Boyer-Moore majority vote](/boyer-moore-majority/).

## In plain words

You have a row of hidden bits and must say whether ones are more than half of them. A single look tells you little. Near a tie, every unseen bit could still change the answer, so a careful algorithm must look at nearly all bits. Coin flips do not save much here, and neither does a quantum computer: both still need a fixed fraction of the bits. This is different from asking "is there any one?", where a quantum computer needs far fewer looks. If you only need the answer when the vote is clearly one-sided, a small random sample is enough.

## Definition

For $x \in \{0,1\}^n$ let $|x| = x_1 + \cdots + x_n$. The majority function is $\mathrm{MAJ}_n(x) = 1$ if $|x| > n/2$ and $0$ otherwise. For even $n$ a tie gives 0; some sources define majority only for odd $n$, where there are no ties.

**Instance.** A string $x \in \{0,1\}^n$, available through queries "what is $x_i$?" in the [query model](/query-model/).

**Question.** Is $|x| > n/2$?

The measure is the number of queries in a named model: deterministic ($D^{dt}$), randomized with error $1/3$ ($R$) or quantum with error $1/3$ ($Q$). In circuit complexity the input is on $n$ wires, and the measures are size and depth.

$\mathrm{MAJ}_n$ is **symmetric**: its value depends only on $|x|$. It is **monotone**: turning a 0 into a 1 never changes the value from 1 to 0. And it is a **threshold function**: $\mathrm{MAJ}_n(x) = 1$ exactly when the linear form $x_1 + \cdots + x_n - n/2$ is positive, as for a [perceptron](/perceptron/) with all weights equal.

## Variants

- **Threshold functions.** $\mathrm{Th}_k^n(x) = 1$ when $|x| \ge k$. OR is $\mathrm{Th}_1^n$, AND is $\mathrm{Th}_n^n$, and $\mathrm{MAJ}_n$ is $\mathrm{Th}_{\lfloor n/2 \rfloor + 1}^n$.
- **Gap majority.** A promise problem: either $|x| \le (1/2 - \varepsilon) n$ or $|x| \ge (1/2 + \varepsilon) n$. The promise removes the hard inputs near the middle, and the cost no longer depends on $n$.
- **Majority of values.** Given $n$ items from any set, find a value that appears more than $n/2$ times, if one exists. This is the [majority element problem](/majority-element-problem/), measured by comparisons or time, not by bit queries.
## Examples

**Three bits.** As a real polynomial, $\mathrm{MAJ}_3(x) = x_1 x_2 + x_1 x_3 + x_2 x_3 - 2 x_1 x_2 x_3$. At $x = 110$ it gives $1$, and at $x = 111$ it gives $3 - 2 = 1$. It has degree 3.

**Sensitivity at $n = 6$.** At an input with $|x| = 3$ the value is 0, and flipping any of the three zeros gives weight 4 and value 1, so the 0-sensitivity is 3. At an input with $|x| = 4$ the value is 1, and flipping any of the four ones gives value 0, so the 1-sensitivity is 4. In general $\mathrm{s}(\mathrm{MAJ}_n) = \lfloor n/2 \rfloor + 1$.

**Approximate degree.** The best error of a polynomial of degree $d$ was computed exactly by a rational minimax search over the symmetric values. The table gives $\widetilde{\deg}(\mathrm{MAJ}_n)$, the least degree with error at most $1/3$.

| $n$ | 1 to 5 | 6 to 11 | 12 | 20 | 30 | 40 | 60 | 80 |
|---|---|---|---|---|---|---|---|---|
| $\widetilde{\deg}(\mathrm{MAJ}_n)$ | 1 | 3 | 4 | 6 | 9 | 11 | 16 | 21 |

For $n = 5$, the linear polynomial $q(k) = k/3 - 1/3$ in the weight $k$ has error exactly $1/3$: it gives $-1/3, 0, 1/3$ at $k = 0, 1, 2$ and $2/3, 1, 4/3$ at $k = 3, 4, 5$. At $n = 6$ the best error with degree 3 is $0.2407$, and at $n = 12$ the best error with degree 4 is $0.3259$. The degree grows about as $n/4$ in this range, which matches the linear bound below.

## Known algorithms

- **Deterministic.** Count the ones, and stop when either count passes $n/2$: at most $n$ queries in the [query model](/query-model/), and this is optimal.
- **Quantum.** For exact majority no quantum algorithm beats $\Theta(n)$ queries, by the [polynomial method](/polynomial-method/). For gap majority, [quantum counting](/quantum-counting/) with $P - 1$ queries estimates $|x|$ within about $\pi n / P$, so $O(1/\varepsilon)$ queries are enough.
- **Randomized, gap version.** Sample $k$ random positions and output the majority of the sample: by Hoeffding's form of the [Chernoff bound](/chernoff-bound/), $k = \lceil \ln 3 / (2 \varepsilon^2) \rceil$ samples give error at most $1/3$, independent of $n$.
- **Circuits.** A [sorting network](/sorting-network/) on the bits moves the ones to the top, and its output at position $\lfloor n/2 \rfloor + 1$ from the top is $\mathrm{MAJ}_n$; with the [AKS network](/aks-sorting-network/) the depth is $O(\log n)$. With one MAJORITY gate the depth is 1, which is the base of [TC0](/tc0/).

## Bounds

| measure | value | reason |
|---|---|---|
| $\mathrm{s}$, $\mathrm{bs}$, $C$ | $\lfloor n/2 \rfloor + 1$ | monotone, so the three are equal |
| $D^{dt}$ | $n$ | adversary, below |
| $R_0$, $R$ | $\Theta(n)$ | $R \ge \mathrm{bs}/3$ |
| $\deg$ | $n$ | finite difference, below |
| $\widetilde{\deg}$ | $\Theta(n)$ | Paturi |
| $Q$ | $\Theta(n)$ | $Q \ge \widetilde{\deg}/2$ |

**Deterministic lower bound.** An adversary answers 1 until it has given $\lfloor n/2 \rfloor$ ones, and 0 after that. After $n - 1$ queries the bits seen hold exactly $\lfloor n/2 \rfloor$ ones and $n - 1 - \lfloor n/2 \rfloor$ zeros, so the last bit decides the value. Any algorithm must query it, and $D^{dt}(\mathrm{MAJ}_n) = n$. A full search over decision trees confirms this for $n = 1, \ldots, 7$.

**Randomized lower bound.** Since $\mathrm{MAJ}_n$ is monotone, $\mathrm{bs} = \mathrm{s} = \lfloor n/2 \rfloor + 1$ (see [certificate complexity](/certificate-complexity/)). The block argument of Nisan gives $R \ge \mathrm{bs}/3 \ge (n + 1)/6$; see [randomized query complexity](/randomized-query-complexity/).

**Exact degree.** A symmetric function has the degree of the polynomial of one variable that interpolates its values at $k = 0, \ldots, n$. That degree is $n$ exactly when the $n$-th finite difference $\sum_k (-1)^{n-k} \binom{n}{k} \mathrm{MAJ}_n(k)$ is not zero. For majority this sum is $\pm \binom{n-1}{\lfloor n/2 \rfloor}$, and a direct computation gives $1, 1, -2, -3, 6, 10, -20, -35, 70, 126, -252, -462$ for $n = 1, \ldots, 12$. So $\deg(\mathrm{MAJ}_n) = n$.

**Approximate degree and quantum queries.** Paturi's theorem says that a symmetric $f$ has $\widetilde{\deg}(f) = \Theta(\sqrt{n (n - \Gamma(f))})$, where $\Gamma(f) = \min \{ |2k - n + 1| : f(k) \ne f(k+1) \}$ measures how far from the middle weight the value changes. For majority the change is at the middle, so $\Gamma = 0$ for odd $n$ and $\Gamma = 1$ for even $n$, and $\widetilde{\deg}(\mathrm{MAJ}_n) = \Theta(n)$. By Beals et al., $Q(f) \ge \widetilde{\deg}(f)/2$, so $Q(\mathrm{MAJ}_n) = \Theta(n)$. Compare OR, where the change is at weight 0, $\Gamma = n - 1$, and both measures are $\Theta(\sqrt n)$.

**Sign degree.** The sign of the linear polynomial $|x| - n/2$ equals the sign pattern of majority, so majority is computed by a single threshold gate. Its approximate degree is $\Theta(n)$, but its sign degree is 1. This contrast is why majority is easy for threshold circuits and perceptrons but hard for query algorithms and for small-degree approximation.

**Circuits.** $\mathrm{MAJ}_n$ is not in [AC0](/ac0/), by the reduction from PARITY below.

## Reductions

- **PARITY to MAJORITY.** $\mathrm{PARITY}_n(x) = 1$ when $|x| = k$ for some odd $k$, and $[|x| = k] = \mathrm{Th}_k(x) \wedge \neg \mathrm{Th}_{k+1}(x)$. Each threshold is a majority with some inputs fixed, as in the next item, so PARITY has circuits of constant depth and polynomial size with MAJORITY, AND and OR gates. Since PARITY is not in AC0, MAJORITY is not in AC0 either; see the [parity problem](/parity-problem/).
- **Threshold to MAJORITY.** Any $\mathrm{Th}_k^n$ is a majority on at most $2n + 1$ bits with some bits fixed. If $k \le (n+1)/2$, add $n + 1 - 2k$ ones: then $\mathrm{Th}_k^n(x) = \mathrm{MAJ}_{2n+1-2k}(x, 1, \ldots, 1)$. If $k > (n+1)/2$, add $2k - 1 - n$ zeros instead. In particular $\mathrm{MAJ}_n(x) = \mathrm{MAJ}_{n+1}(x, 0)$ for even $n$.
- **Majority element.** For an array over $\{0, 1\}$, the [majority element problem](/majority-element-problem/) asks for the value with more than $n/2$ copies, which is the bit $\mathrm{MAJ}_n(x)$ when it exists.

## Applications

- **Error reduction.** Running a [Monte Carlo algorithm](/monte-carlo-algorithm/) many times and taking the majority answer reduces its error exponentially; the analysis is a [Chernoff bound](/chernoff-bound/) on the number of wrong runs.
- **Decoding.** The [repetition code](/repetition-code/) decodes each bit by the majority of its copies.
- **Threshold circuits and learning.** Majority gates define [TC0](/tc0/), and a [perceptron](/perceptron/) is a weighted majority.
- **Lower bound test cases.** Majority is the standard symmetric function whose change point is at the middle, the opposite case to OR; together they show the two ends of Paturi's theorem.

## References
