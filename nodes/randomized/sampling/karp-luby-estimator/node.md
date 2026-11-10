---
tag: KKHPVT
kind: algorithm
slug: karp-luby-estimator
name: Karp-Luby estimator for the size of a union
aliases:
- Karp-Luby-Madras estimator
- coverage estimator
- union-of-sets estimator
- Karp-Luby union estimator
area: randomized/sampling
level: advanced
summary: Estimates the size of a union of m sets from their sizes, uniform samples and membership tests, within a factor 1 ± ε with probability 1 - δ, using O(m log(1/δ)/ε²) samples.
solves: [approximate-counting]
model: word-ram
complexity:
  vars: {m: the number of sets, ε: the relative error (0 < ε < 1), δ: the failure probability (0 < δ < 1)}
  time: {worst: "O(m^2 log(1/δ) / ε^2)"}
  space: {extra: O(m)}
properties: {deterministic: false, recursive: false}
history:
  year: 1989
  people: [Richard M. Karp, Michael Luby, Neal Madras]
  note: Karp and Luby gave the method at FOCS 1983 for DNF counting and network reliability; with Madras, in the Journal of Algorithms in 1989, they stated it for the union of sets and added the coverage and self-adjusting coverage algorithms.
prereqs: [importance-sampling, chernoff-bound, linearity-of-expectation]
see_also: [karp-luby-algorithm, dnf-counting, fpras, approximate-counting, jerrum-valiant-vazirani-theorem, inclusion-exclusion-principle, monte-carlo-algorithm, klee-measure-problem]
sources:
  - paper: doi:10.1016/0196-6774(89)90038-2
    title: Richard M. Karp, Michael Luby and Neal Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10(3), 429 to 448, 1989
    locator: the union of sets problem, the coverage algorithm, and the self-adjusting coverage algorithm with its running time
  - paper: doi:10.1109/SFCS.1983.35
    title: Richard M. Karp and Michael Luby, Monte-Carlo algorithms for enumeration and reliability problems, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983), 56 to 64
    locator: the first form of the estimator, for DNF counting and reliability
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: the chapter The Monte Carlo Method (DNF counting and the union of sets), and Chapter 4 (Chernoff bounds for variables in [0, 1])
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 11, Approximate Counting (the DNF counting problem and the estimator theorem)
---

The Karp-Luby estimator approximates the size of a union $U = A_1 \cup \cdots \cup A_m$ of sets that are too large to list, when three things are easy for each set: its size $|A_i|$, a uniform random element of it, and a test of whether a given element belongs to it. It samples a pair $(i, x)$, a set chosen with probability proportional to its size and a uniform element of that set, so that the pair is uniform among all $W = \sum_i |A_i|$ pairs. Then $W$ times an indicator, "is $i$ the first set that holds $x$?", or the ratio $W/c(x)$, where $c(x)$ is the number of sets holding $x$, is an unbiased estimate of $|U|$ whose relative variance is below $m$. The mean of $N = \lceil 3m \ln(2/\delta)/\varepsilon^2 \rceil$ samples is within a factor $1 \pm \varepsilon$ of $|U|$ with probability at least $1 - \delta$. This page treats the general union estimator of Karp, Luby and Madras (1989). Its first and main use, counting the solutions of a DNF formula, has its own page: the [Karp-Luby algorithm for DNF counting](/karp-luby-algorithm/).

## In plain words

You want to know how many different people are on a set of club lists. You know the length of each list, you can pick a random name from any list, and you can check whether a name is on a list. People can be on many lists, so adding up the lengths counts some people many times.

Pick a list with chance in proportion to its length, then a random name on it. This is the same as picking a random line from all the lists together. Then ask: is this the first list on which this person appears? Each person has exactly one first list, so the share of "yes" answers, times the total length, is the number of different people. Since each person is on at most all the lists, at least one answer in that many is "yes", which makes the share easy to measure.

## The problem

The input is $m$ sets $A_1, \ldots, A_m$ from some universe, given by three oracles: SIZE$(i)$ returns $|A_i|$, SAMPLE$(i)$ returns a uniform element of $A_i$, and MEMBER$(j, x)$ tells whether $x \in A_j$. Also given are an accuracy $0 < \varepsilon < 1$ and a confidence $0 < \delta < 1$. The output is a number $\hat u$ with $\Pr[(1 - \varepsilon)|U| \le \hat u \le (1 + \varepsilon)|U|] \ge 1 - \delta$, for $U = \bigcup_i A_i$. This is an [approximate counting](/approximate-counting/) problem, and an algorithm for it that runs in time polynomial in $m$, $1/\varepsilon$ and $\log(1/\delta)$ is an [FPRAS](/fpras/) for the union size.

The [inclusion-exclusion principle](/inclusion-exclusion-principle/) gives $|U|$ exactly, but it needs the sizes of up to $2^m - 1$ intersections. Plain Monte Carlo, testing random elements of the universe, fails when $U$ is a tiny part of the universe.

## The algorithm

```pseudo id=main
KARP-LUBY(A_1, ..., A_m, ε, δ)
L1  W ← |A_1| + ... + |A_m|; N ← ⌈3m ln(2/δ) / ε²⌉; Y ← 0
L2  repeat N times
L3      pick i with probability |A_i| / W
L4      x ← a uniform random element of A_i
L5      if x ∉ A_j for every j < i then Y ← Y + 1     ▷ i is the first set holding x
L6  return W · Y / N
```

The *coverage* form replaces line L5 by "$Y \leftarrow Y + 1/c(x)$", where $c(x)$ is the number of sets $j$ with $x \in A_j$. Both forms use the same pairs and the same $N$.

## Example

Take the DNF formula $(x_1 \land x_2) \lor (\lnot x_1 \land x_3) \lor (x_2 \land x_3)$ over three variables. Let $A_i$ be the set of assignments, written $x_1 x_2 x_3$, that satisfy clause $i$:

| $i$ | clause | $A_i$ | elements whose first set is $i$ |
|---|---|---|---|
| 1 | $x_1 \land x_2$ | 110, 111 | 110, 111 |
| 2 | $\lnot x_1 \land x_3$ | 001, 011 | 001, 011 |
| 3 | $x_2 \land x_3$ | 011, 111 | none |

Here $W = 6$ and $|U| = 4$. Of the 6 equally likely pairs, 4 pass the test of line L5, so $E[Y \text{ per sample}] = 4/6$ and $E[W Y/N] = 4$. The relative variance of one 0-1 sample is $W/|U| - 1 = 0.5$. With the coverage form, the elements $110$ and $001$ have $c = 1$ and give $6$, and $111$ and $011$ have $c = 2$ and give $3$. The mean over the six pairs is $(6 + 3 + 6 + 3 + 3 + 3)/6 = 4$, and the relative variance is $18/16 - 1 = 0.125$. For $\varepsilon = 0.1$ and $\delta = 0.01$, line L1 sets $N = \lceil 9 \ln 200 / 0.01 \rceil = 4769$.

## Correctness

**Theorem (Karp, Luby and Madras 1989).** Each 0-1 sample $WY$ and each coverage sample $W/c(x)$ has mean $|U|$ and relative variance at most $W/|U| - 1 \le m - 1$. With $N \ge 3m\ln(2/\delta)/\varepsilon^2$ samples, the output is within a factor $1 \pm \varepsilon$ of $|U|$ with probability at least $1 - \delta$.

The pair $(i, x)$ is uniform over the $W$ pairs with $x \in A_i$. Each element of $U$ has exactly one first set, so $|U|$ of the $W$ pairs pass line L5, and also $\sum_{(i,x)} 1/c(x) = |U|$. Since each element lies in at most $m$ sets, $W \le m|U|$, so the success rate per sample is at least $1/m$. The [Chernoff bound](/chernoff-bound/) for a sum of $N$ independent variables in $[0, 1]$ with mean at least $N/m$ then gives the sample bound. The full proof is below.

## Complexity

- **Samples.** $N = \lceil 3m \ln(2/\delta)/\varepsilon^2 \rceil = O(m \log(1/\delta)/\varepsilon^2)$.
- **Oracle calls.** Each sample uses one SAMPLE call and up to $i - 1 < m$ MEMBER calls in the 0-1 form, or $m$ in the coverage form. So the total is $O(m^2 \log(1/\delta)/\varepsilon^2)$ oracle calls, plus $O(m)$ SIZE calls. Line L3 takes $O(\log m)$ time with prefix sums of the sizes.
- **Self-adjusting coverage.** Karp, Luby and Madras remove one factor of $m$. To estimate $1/c(x)$, test random sets $j$, uniform among the $m$, until one holds $x$. The number of tests $G$ is geometric with mean $m/c(x)$, so $W G/m$ is an unbiased estimate of $W/c(x)$, and its expected cost is small exactly when $c(x)$ is large. Their self-adjusting algorithm stops after a fixed budget of $O(m \log(1/\delta)/\varepsilon^2)$ membership tests in total.
- **Space.** $O(m)$ for the sizes and their prefix sums.

## Properties

- **Unbiased.** Each sample has mean exactly $|U|$, for every instance.
- **Relative variance at most m.** This is what makes a polynomial number of samples enough, however small $|U|$ is compared with the universe.
- **Only three oracles.** The sets can be implicit and exponentially large. For a DNF clause with $\ell$ literals over $n$ variables, the size is $2^{n - \ell}$, a uniform element fixes the $\ell$ literals and flips coins for the rest, and membership is evaluation.
- **Also for weights and measures.** The same argument works when the sets carry a measure, for example the volume of a union of boxes, with "uniform element" replaced by "a point drawn from the measure".

## Variants and improvements

- **DNF counting.** The [Karp-Luby algorithm](/karp-luby-algorithm/) is this estimator applied to the satisfying sets of the clauses. It gives an FPRAS for #DNF, whose exact version is #P-complete.
- **Network reliability.** Karp and Luby applied the method to the probability that a network with random edge failures is disconnected, written as a union of events.
- **The median trick.** Running $O(\log(1/\delta))$ independent copies with failure probability $1/4$ each and taking the median also gives confidence $1 - \delta$, with any estimator of bounded relative variance. See the [median trick](/median-trick/).
- **From counting to sampling.** By the [Jerrum-Valiant-Vazirani theorem](/jerrum-valiant-vazirani-theorem/), for self-reducible problems an FPRAS such as this one gives an almost uniform sampler, and back.

## When to use it

Use the Karp-Luby estimator when a quantity is the size or the measure of a union of sets that each have a known size, a uniform sampler and a membership test, but whose overlaps are complex: the number of models of a DNF formula, the probability that at least one of $m$ failure events happens, or the volume of a union of boxes in high dimension. If the union is a large part of a universe you can sample from directly, plain Monte Carlo is simpler. If $m$ is small, inclusion-exclusion is exact.

## Pitfalls

- **Sampling sets uniformly instead of by size.** Line L3 must pick set $i$ with probability $|A_i|/W$. Picking $i$ uniformly makes the pair non-uniform and biases the estimate unless all sets have the same size.
- **Testing all other sets in line L5.** The test is "no *earlier* set holds $x$". Testing all $j \ne i$ counts only elements that lie in a single set, which underestimates $|U|$.
- **Empty sets.** A DNF clause with both $x$ and $\lnot x$ has an empty set. It must get size 0, or SAMPLE fails.
- **Plain Monte Carlo instead.** Testing uniform random elements of the whole universe needs about $|\text{universe}|/|U|$ samples to see even one element of $U$. For a DNF with 2 models over 40 variables that is about $5 \cdot 10^{11}$, while the Karp-Luby estimator needs a few thousand.

## Implementations

## History

Richard Karp and Michael Luby gave the method at FOCS 1983, for counting the satisfying assignments of DNF formulas and for network reliability. In the 1989 journal version, with Neal Madras, the method is stated for the general union of sets problem, with the coverage algorithm and the self-adjusting coverage algorithm that removes a factor of $m$ from the running time. The estimator became the standard example of an FPRAS for a #P-complete problem, and appears in the textbooks of Motwani and Raghavan and of Mitzenmacher and Upfal.

## References
