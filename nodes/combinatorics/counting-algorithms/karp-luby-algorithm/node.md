---
tag: 68D09K
kind: algorithm
slug: karp-luby-algorithm
name: Karp-Luby estimator
aliases:
- Karp-Luby Monte Carlo counting
- Karp-Luby DNF counting
area: combinatorics/counting-algorithms
level: advanced
summary: Estimates the number of satisfying assignments of a DNF with polynomially many samples, by sampling (clause, assignment) pairs and keeping a pair only if its clause is the first one satisfied.
solves: [dnf-counting]
model: word-ram
complexity:
  vars: {m: the number of clauses, n: the number of variables, L: the total number of literals in the formula, ε: the relative error (0 < ε < 1), δ: the failure probability (0 < δ < 1)}
  time: {worst: "O(m (n + L) log(1/δ) / ε^2)"}
  space: {extra: "O(m + n)"}
properties: {deterministic: false, recursive: false}
history:
  year: 1983
  people: [Richard M. Karp, Michael Luby]
  note: Karp and Luby gave the estimator at FOCS 1983 for DNF counting and network reliability. The journal version with Neal Madras in 1989 put it in a general framework for the size of a union of sets and added a faster self-adjusting variant.
prereqs: [dnf-counting, chernoff-bound, importance-sampling]
see_also: [fpras, approximate-counting, karp-luby-estimator, monte-carlo-algorithm, model-counting, inclusion-exclusion-principle, union-bound, median-trick]
sources:
  - paper: doi:10.1109/SFCS.1983.35
    title: Richard M. Karp and Michael Luby, Monte-Carlo algorithms for enumeration and reliability problems, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983), 56 to 64
    locator: the DNF counting algorithm and its analysis
  - paper: doi:10.1016/0196-6774(89)90038-2
    title: Richard M. Karp, Michael Luby and Neal Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10(3), 429 to 448, 1989
    locator: the union of sets problem (the coverage algorithm and the self-adjusting coverage algorithm)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 11, Approximate Counting (the DNF counting problem)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: the chapter The Monte Carlo Method (the DNF counting problem), and Chapter 4 (Chernoff bounds)
---

The Karp-Luby estimator approximates the number $|S|$ of truth assignments that satisfy a formula $F = C_1 \lor \cdots \lor C_m$ in disjunctive normal form over $n$ variables. Exact [DNF counting](/dnf-counting/) is #P-complete, and the plain [Monte Carlo](/monte-carlo-algorithm/) method of testing random assignments fails when $|S|$ is a tiny fraction of $2^n$. Karp and Luby sample from a smaller space instead: the pairs $(i, a)$ where the assignment $a$ satisfies the clause $C_i$. There are $W = \sum_i 2^{n - |C_i|}$ such pairs, $W$ is easy to compute, and at least one pair in $m$ is "first", that is, $C_i$ is the first clause that $a$ satisfies. The first pairs are in one-to-one correspondence with $S$. So $W$ times the fraction of first pairs among $N = \lceil 3m \ln(2/\delta)/\varepsilon^2 \rceil$ samples is within a factor $1 \pm \varepsilon$ of $|S|$ with probability at least $1 - \delta$. The running time is polynomial in $n$, $m$, $1/\varepsilon$ and $\log(1/\delta)$, so this is an [FPRAS](/fpras/) for #DNF.

## In plain words

Think of each clause as a club, and of each assignment that makes the clause true as a member of that club. A person can be a member of many clubs. We want the number of different people, not the total size of all the clubs.

The total size of the clubs is easy to compute, but it counts a person once for each club that person is in. To fix this, give each person a home club: the first club on the list that the person belongs to. Now pick a random club membership, with each membership equally likely, and ask whether it is the person's home club. The fraction of yes answers, times the total size of the clubs, is the number of people. No person has more memberships than there are clubs, so the yes answers are never too rare.

## The problem

Input: a DNF formula $F = C_1 \lor \cdots \lor C_m$ over the variables $x_1, \ldots, x_n$, where each clause $C_i$ is a conjunction of literals; an accuracy $0 < \varepsilon < 1$; a confidence $0 < \delta < 1$. Let $S_i$ be the set of assignments that satisfy $C_i$ and $S = S_1 \cup \cdots \cup S_m$. Output: a number $Y$ such that

$$\Pr\big[(1 - \varepsilon)|S| \le Y \le (1 + \varepsilon)|S|\big] \ge 1 - \delta.$$

A clause with $k$ different literals and no complementary pair fixes $k$ variables and leaves the other $n - k$ free, so $|S_i| = 2^{n - k}$, and a uniform element of $S_i$ is easy to draw. A clause that contains both $x_v$ and $\lnot x_v$ has $S_i = \emptyset$.

## The algorithm

The weight of clause $C_i$ is $w_i = |S_i| = 2^{n - |C_i|}$, where $|C_i|$ is the number of different literals of $C_i$, and $W = \sum_i w_i$. A trial draws a uniform pair $(i, a)$ with $a \in S_i$, in two steps, and scores 1 if $C_i$ is the first clause that $a$ satisfies.

```pseudo id=main
KARP-LUBY(C_1, …, C_m, n, ε, δ)                 ▷ returns an estimate of |S_1 ∪ ⋯ ∪ S_m|
L1  drop every clause that has a literal and its negation; let m be the number left; if m = 0 then return 0
L2  w_i ← 2^(n − |C_i|) for i = 1, …, m;  W ← w_1 + ⋯ + w_m
L3  N ← ⌈3 m ln(2/δ) / ε²⌉;  s ← 0
L4  repeat N times
L5      pick i ∈ {1, …, m} with probability w_i / W
L6      pick a uniformly from S_i: set the literals of C_i true, and every other variable by a fair coin
L7      if no clause C_j with j < i is satisfied by a then s ← s + 1
L8  return W · s / N
```

Line L5 takes a uniform integer $r$ in $[0, W)$ and finds the first prefix sum $w_1 + \cdots + w_i$ above $r$ by binary search.

## Example

Let $n = 3$ and $F = (x_1 \land x_2) \lor (x_2 \land x_3) \lor \lnot x_1$, so $C_1 = x_1 x_2$, $C_2 = x_2 x_3$ and $C_3 = \lnot x_1$. Write an assignment as the bits $x_1 x_2 x_3$. Line L2 gives $w_1 = 2$, $w_2 = 2$, $w_3 = 4$ and $W = 8$. The 8 pairs are:

| clause $i$ | assignments $a \in S_i$ | first clause of $a$ | first pairs |
|---|---|---|---|
| 1 | 110, 111 | $C_1$, $C_1$ | 2 |
| 2 | 011, 111 | $C_2$, $C_1$ | 1 |
| 3 | 000, 001, 010, 011 | $C_3$, $C_3$, $C_3$, $C_2$ | 3 |

So 6 of the 8 pairs are first, and $|S| = 6$: the assignments are 000, 001, 010, 011, 110 and 111. The success probability of one trial is $6/8$.

For $\varepsilon = 0.5$ and $\delta = 0.25$, line L3 gives $N = \lceil 9 \ln 8 / 0.25 \rceil = 75$. To keep the table short, here are the first 8 trials of one run, with the state after each trial:

| trial | $i$ (L5) | $a$ (L6) | first clause of $a$ | success (L7) | $s$ |
|---|---|---|---|---|---|
| 1 | 3 | 001 | $C_3$ | yes | 1 |
| 2 | 3 | 010 | $C_3$ | yes | 2 |
| 3 | 2 | 111 | $C_1$ | no | 2 |
| 4 | 1 | 110 | $C_1$ | yes | 3 |
| 5 | 3 | 011 | $C_2$ | no | 3 |
| 6 | 1 | 110 | $C_1$ | yes | 4 |
| 7 | 1 | 111 | $C_1$ | yes | 5 |
| 8 | 3 | 000 | $C_3$ | yes | 6 |

If the run stopped here, line L8 would return $8 \cdot 6 / 8 = 6$. With so few trials an exact hit is luck: the value $8 s / 8 = s$ can be any integer from 0 to 8. With all 75 trials, the result lies in $[3, 9]$ with probability at least $0.75$.

## Correctness

The full proof is in `proofs/correctness.md`. It has three steps.

- **Uniform pairs.** Line L5 picks $i$ with probability $w_i / W$, and line L6 picks each $a \in S_i$ with probability $1/w_i$. So each pair $(i, a)$ with $a \in S_i$ comes up with probability $1/W$.
- **The mean.** Each $a \in S$ has exactly one first pair, the pair with the least $i$ such that $a \in S_i$. So exactly $|S|$ of the $W$ pairs succeed, and each trial succeeds with probability $p = |S|/W$. Each $a \in S$ lies in at most $m$ sets $S_i$, so $W \le m |S|$ and $p \ge 1/m$.
- **The guarantee.** The count $s$ is a sum of $N$ independent 0-1 variables with mean $\mu = Np \ge N/m \ge 3 \ln(2/\delta)/\varepsilon^2$. By the [Chernoff bound](/chernoff-bound/), $\Pr[|s - \mu| > \varepsilon \mu] \le 2 e^{-\varepsilon^2 \mu / 3} \le \delta$. Since $Y = W s / N$ and $W \mu / N = |S|$, this is the claim.

Clauses dropped by line L1 have $S_i = \emptyset$, so they change neither $S$ nor the answer.

## Complexity

- **Time.** Line L1 and line L2 take $O(L + m)$ time. One trial takes $O(\log m)$ for line L5, $O(n)$ random bits for line L6, and $O(L)$ for line L7, which reads each earlier clause once. So the total is $O(N (n + L)) = O(m (n + L) \log(1/\delta) / \varepsilon^2)$. This counts an operation on a number of $n + \log m$ bits, such as $W$, as one step.
- **Space.** The prefix sums of the weights take $m$ numbers, and the assignment takes $n$ bits: $O(m + n)$ beyond the input.
- **Samples.** The number of trials $N = O(m \log(1/\delta)/\varepsilon^2)$ does not depend on $n$ or on $|S|$. It depends on $m$ only through the bound $p \ge 1/m$.

## Properties

- **Randomized, with relative error.** The output is random. The guarantee is multiplicative, $(1 \pm \varepsilon)|S|$, with failure probability at most $\delta$. The algorithm never returns a nonzero value when $S$ is empty, because then $m = 0$ after line L1.
- **Unbiased.** $\mathbb{E}[Y] = |S|$ for every $N$, by the uniform pair argument.
- **Bounded relative variance.** One trial has variance $p(1 - p)$, so $W \cdot (\text{success})$ has relative variance $(1 - p)/p \le m - 1$. This is the source of the factor $m$ in $N$. Plain Monte Carlo over all $2^n$ assignments has relative variance $2^n/|S| - 1$, which can be exponential.
- **Exact in easy cases.** If one clause is left after line L1, every trial succeeds and $Y = W = |S|$.
- **Not recursive.** The trials are independent and can run in parallel; only the count $s$ is shared.

## Variants and improvements

- **Union of sets.** The same method estimates $|S_1 \cup \cdots \cup S_m|$ for any family of sets where one can compute each $|S_i|$, draw a uniform element of $S_i$, and test whether an element lies in $S_j$. Karp, Luby and Madras state the method in this form.
- **Probabilities instead of counts.** If each variable $x_v$ is true with its own probability $q_v$, take $w_i = \Pr[C_i]$ and draw $a$ from the product distribution conditioned on $C_i$. The output then estimates $\Pr[F]$. This is the form used for network reliability, where $F$ is the event that the network fails.
- **Coverage estimator.** Instead of the first-clause test, score a trial by $1/c(a)$, where $c(a)$ is the number of clauses that $a$ satisfies. This is also unbiased, since each $a \in S$ appears in $c(a)$ pairs, and its variance is at most that of the 0-1 score.
- **Self-adjusting coverage.** Karp, Luby and Madras test random clauses against $a$ until one is satisfied, instead of scanning all earlier clauses, and stop after a fixed number of steps. This removes most of the factor $L$ per trial and runs in time about $O(n m \log(1/\delta)/\varepsilon^2)$.
- **The median trick.** Running the algorithm with $\delta = 1/4$ a total of $O(\log(1/\delta))$ times and taking the [median](/median-trick/) gives the same dependence on $\delta$. Here the direct choice of $N$ in line L3 is simpler.

## When to use it

Use the Karp-Luby estimator to approximate the number of solutions, or the probability, of a DNF, or of any union of sets with the three operations above, when both $n$ and $m$ are too large for exact methods. If $n$ is at most about 25, enumerate all assignments. If $m$ is at most about 20, use [inclusion-exclusion](/inclusion-exclusion-principle/) over the $2^m$ subsets of clauses, which is exact. Do not try to use it for CNF formulas by complementation: $|S_{\text{CNF}}| = 2^n - |S_{\text{DNF}}|$, and a relative error on the DNF count gives no relative error on a small CNF count. Approximate #SAT for CNF has no [FPRAS](/fpras/) unless NP = RP.

## Pitfalls

- **The first-clause test of line L7.** The test must compare $i$ with one fixed clause chosen by $a$ alone, such as the first one. Scoring 1 only when $a$ satisfies no clause other than $C_i$ counts only the assignments in exactly one $S_i$. In the example this scores 4 pairs (000, 001, 010 with $C_3$ and 110 with $C_1$), and the estimate tends to 4 instead of 6.
- **No test at all.** Dropping line L7 and always adding 1 returns $W = \sum_i |S_i|$, which counts each assignment once per clause it satisfies: 8 in the example instead of 6.
- **The clause weights of line L5.** Picking $i$ uniformly instead of with probability $w_i / W$ biases the result. For $n = 3$, $C_1 = x_1$ and $C_2 = x_1 x_2 x_3$, the answer is $|S| = 4$ and $W = 5$, but a uniform $i$ gives $\mathbb{E}[Y] = 5 \cdot \tfrac{1}{2} = 2.5$.
- **The number of trials of line L3.** $N$ must grow with $m$. With $m$ copies of the same clause, $p = 1/m$, and a fixed number of trials sees no success at all for large $m$, so the output is 0 with high probability.
- **Contradictory clauses.** Without line L1, a clause with both $x_v$ and $\lnot x_v$ gets the weight $2^{n - |C_i|}$ of assignments that do not exist, and line L6 cannot sample from it.
- **Floating point weights.** For $n$ above about 1000, $2^{n - |C_i|}$ overflows a double. Use exact integers, or scale all weights by $2^{-n + \min_i |C_i|}$.

## Implementations

## History

Richard Karp and Michael Luby presented the estimator at FOCS 1983 in a paper on Monte Carlo algorithms for enumeration and reliability problems, with DNF counting and the failure probability of a network as the main examples. The journal paper of Karp, Luby and Neal Madras in 1989 stated the method for a general union of sets and gave the self-adjusting coverage algorithm. The algorithm became the standard first example of an FPRAS for a #P-complete problem, in textbooks such as Motwani and Raghavan (1995) and Mitzenmacher and Upfal.

## References
