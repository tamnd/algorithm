---
tag: SCNB37
kind: definition
slug: two-sided-error
name: Two-sided error
aliases:
- bounded error
- BPP-type error
area: randomized/monte-carlo-and-las-vegas
level: core
summary: Error allowed on both answers, bounded by a constant below one half.
prereqs: [monte-carlo-algorithm, one-sided-error, chernoff-bound]
see_also: [one-sided-error, error-amplification, bpp, pp, hoeffding-inequality, median-trick, adleman-theorem, monte-carlo-algorithm]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Chapter 7, Randomized computation (the definition of BPP, error reduction by majority with a Chernoff bound, BPP in P/poly, BPP in the polynomial hierarchy); Chapter 20, Derandomization
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.5 (the classes PP and BPP, and why a gap from one half is needed)
  - paper: doi:10.1137/0206049
    title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing 6(4), 1977
    locator: pages 675 to 695 (the classes PP and BPP)
---

A [Monte Carlo algorithm](/monte-carlo-algorithm/) for a decision problem has two-sided error when both of its answers can be wrong, each with probability at most $\delta$, and $\delta$ is below $1/2$ by a fixed gap. With the gap, a majority vote over independent runs makes the error exponentially small. Without the gap, as in the class [PP](/pp/), the error can be so close to $1/2$ that no polynomial number of runs helps. Polynomial-time algorithms with two-sided error $\delta \le 1/3$ define the class [BPP](/bpp/).

## Definition

Notation on this page: $n = |x|$ is the input size, $\delta$ is the error probability, $\gamma$ is the gap $1/2 - \delta$, and $\Pr$ is over the random bits of the algorithm for one fixed input.

Let $L$ be a language and $A$ a randomized algorithm that stops on every input and every random string with the answer "yes" or "no". $A$ has **two-sided error $\delta$** if for every input $x$:

$$x \in L \implies \Pr[A(x) = \text{yes}] \ge 1 - \delta, \qquad x \notin L \implies \Pr[A(x) = \text{yes}] \le \delta,$$

with $\delta \le 1/2 - \gamma$ for a gap $\gamma > 0$. The gap is a constant, or at least $1/q(n)$ for a polynomial $q$. Equivalently, $\Pr[A(x) \text{ is correct}] \ge 1/2 + \gamma$ on every input.

- [BPP](/bpp/) is the class of languages with a polynomial-time algorithm of two-sided error at most $1/3$. Any constant gap gives the same class, by the majority vote below.
- [PP](/pp/) asks only $\Pr[A(x) \text{ is correct}] > 1/2$, with no bound on the gap.
- The definition is symmetric in "yes" and "no", so BPP is closed under complement. RP is not known to be.

### Facts

**Majority vote.** Run $A$ $k$ times with independent bits, $k$ odd, and output the majority answer. If each run is correct with probability at least $1/2 + \gamma$, the majority is wrong with probability at most $(1 - 4\gamma^2)^{k/2} \le e^{-2\gamma^2 k}$. So $k = \lceil \ln(1/\delta')/(2\gamma^2) \rceil$, made odd, reaches error $\delta'$. The proof and the exact numbers are on the page [error amplification](/error-amplification/). For $\gamma = 1/6$ (error $1/3$) and $\delta' = 10^{-6}$, the bound asks for 249 runs, and the exact binomial tail shows that 193 runs are enough.

**An OR does not work.** The OR of $k$ runs, the method for [one-sided error](/one-sided-error/), says "yes" on $x \notin L$ with probability up to $1 - (1 - \delta)^k$, which tends to 1. Two-sided error needs a vote.

**Why the gap is needed.** Without a gap, the error can be exponentially close to $1/2$. For example, SAT has an algorithm that is correct with probability more than $1/2$ on each formula $\varphi$ with $m$ variables: pick a uniform assignment; if it satisfies $\varphi$, say "yes"; else say "yes" with probability $1/2 - 2^{-m-1}$. An unsatisfiable $\varphi$ gets "yes" with probability $1/2 - 2^{-m-1} < 1/2$. A satisfiable one gets "yes" with probability at least $2^{-m} + (1 - 2^{-m})(1/2 - 2^{-m-1}) = 1/2 + 2^{-2m-1}$. The gap $2^{-2m-1}$ is so small that the majority vote needs about $2^{4m}$ runs. This is why SAT is in PP while it is not known to be in BPP.

**Known containments.** RP $\subseteq$ BPP, because one-sided error $1/2$ becomes $1/4$ after two runs. BPP $\subseteq$ P/poly ([Adleman's theorem](/adleman-theorem/) and its extension to two-sided error), and BPP is in the second level of the polynomial hierarchy. Whether BPP $=$ P is open; it follows from strong enough circuit lower bounds, see [pseudorandom generator](/pseudorandom-generator/).

## Examples and non-examples

- **Majority of a large array, a promise problem.** An array of $N$ bits is promised to have a fraction of ones at least $2/3$ ("yes") or at most $1/3$ ("no"). Read $s = 100$ uniform random positions and say "yes" if more than 50 of them are 1. On a "yes" array, the number of ones seen has the binomial distribution with mean at least $66.7$, and the answer is wrong with probability at most $0.00042$; a "no" array is symmetric. Both answers can be wrong, and the time does not depend on $N$. [Hoeffding's inequality](/hoeffding-inequality/) gives the weaker bound $e^{-2 \cdot 100 / 36} \approx 0.0039$.
- **An intersection of one-sided problems.** Let $L_1$ have an algorithm with RP-type error and $L_2$ one with co-RP-type error, each at most $1/4$ after two runs. To decide $L_1 \cap L_2$, answer "yes" when both say "yes". The answer can be wrong on both sides: a wrong "no" from the first test, or a wrong "yes" from the second. The error is at most $1/4 + 1/4 = 1/2$, so run each test three times first to bring each error to $1/8$ and the total to $1/4$.
- **Estimation with a tolerance.** A [Monte Carlo estimator](/monte-carlo-integration/) that must be within $\varepsilon$ of the true value can be too high or too low. With a threshold, it decides a promise problem with two-sided error. The [median trick](/median-trick/) is the majority vote for numerical answers.
- **Non-example: Miller-Rabin.** Its answer "composite" is never wrong, so its error is [one-sided](/one-sided-error/). One-sided error is a special case of two-sided error, but calling it two-sided wastes the simpler amplification.
- **Non-example: error exactly $1/2$.** An algorithm that ignores its input and flips a fair coin has $\Pr[\text{correct}] = 1/2$ on every input. It has no gap, and no number of runs helps.
- **Non-example: the PP algorithm for SAT above.** It has a gap, but the gap $2^{-2m-1}$ is not bounded below by an inverse polynomial, so it is not two-sided error in the sense of BPP.

## Related definitions

- **[One-sided error](/one-sided-error/).** Only one answer can be wrong; any error below 1 can be amplified with an OR.
- **[Error amplification](/error-amplification/).** The majority vote with a Chernoff bound, and the number of rounds for a target error.
- **[BPP](/bpp/)** and **[PP](/pp/).** Two-sided error with and without a gap, in polynomial time.
- **[Chernoff bound](/chernoff-bound/)** and **[Hoeffding's inequality](/hoeffding-inequality/).** The tail bounds behind the majority vote.
- **[Median trick](/median-trick/).** Amplification for algorithms that output numbers instead of yes or no.
- **[Monte Carlo algorithm](/monte-carlo-algorithm/).** Two-sided error is the most general error of a Monte Carlo algorithm for a decision problem.

## References
