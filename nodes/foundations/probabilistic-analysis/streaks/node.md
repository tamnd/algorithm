---
tag: T3G4YQ
kind: problem
slug: streaks
name: Longest streak in random coin flips
aliases:
- Streaks
area: foundations/probabilistic-analysis
level: core
summary: The question of how long a run of identical outcomes is expected in a sequence of random coin flips, with a logarithmic answer.
prereqs: [bernoulli-trials, independent-events, union-bound, expected-value]
see_also: [birthday-paradox, balls-into-bins, coupon-collector-problem, hiring-problem, run-length-encoding, high-probability-bounds, geometric-distribution]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 5, Section 5.4 (Streaks, the bounds O(lg n) and Ω(lg n) on the expected longest streak of heads)
  - paper: doi:10.1080/07468342.1990.11973306
    title: Mark F. Schilling, The longest run of heads, The College Mathematics Journal 21(3), 1990
    locator: pp. 196 to 207, the recursion for the distribution and the approximation of the mean
  - paper: "Paul Erdős and Alfréd Rényi, On a new law of large numbers, Journal d'Analyse Mathématique 23 (1970)"
    locator: pp. 103 to 111, the longest run of heads divided by lg n tends to 1 almost surely
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 1 and Chapter 2 (the union bound and indicator variables used in the proof)
---

The streaks problem asks for the length $R_n$ of the longest run of consecutive heads in $n$ independent flips of a fair coin, or, in a second form, of the longest run of identical outcomes. The answer is logarithmic: $\mathbb{E}[R_n] = \Theta(\lg n)$, and more precisely $\mathbb{E}[R_n] \approx \lg n - 2/3$, with an error below 0.002 for $10^3 \le n \le 10^6$, and $R_n / \lg n \to 1$ in probability. CLRS uses it as a third example of [indicator random variables](/indicator-random-variable/) and the [union bound](/union-bound/), after the [birthday paradox](/birthday-paradox/) and [balls into bins](/balls-into-bins/).

## In plain words

Flip a fair coin many times and write down the results. Look for the longest block of heads in a row. People who invent a random sequence by hand almost always make this block too short. In two hundred real flips, the longest block of heads is usually six to eight long.

The reason is that each position can start a block. A block of a given length is rare at one position, but there are many positions. Each extra head in the block halves its chance. So doubling the number of flips adds only about one to the longest block. The longest block grows like the number of times you can halve the number of flips.

## Definition

**Input.** An integer $n \ge 1$. Flips $c_1, \ldots, c_n$ are independent, each heads with probability $1/2$.

**Head runs.** A *run of heads of length $k$ at position $i$* means $c_i = c_{i+1} = \cdots = c_{i+k-1} = $ heads, with $1 \le i \le n - k + 1$. Let $R_n$ be the largest $k$ such that a run of heads of length $k$ exists, and $R_n = 0$ if all flips are tails.

**Streaks of identical outcomes.** Let $S_n$ be the largest $k$ such that $k$ consecutive flips are all equal, heads or tails. For $n \ge 1$, $S_n$ has the same distribution as $1 + R_{n-1}$. Indeed, the indicators $b_i = [c_i = c_{i-1}]$ for $i = 2, \ldots, n$ are independent fair bits, since $c_i$ is a fresh fair flip, and a streak of $k$ equal flips is a run of $k - 1$ ones among the $b_i$.

**Questions.** The distribution of $R_n$, its mean, and how sharply it concentrates.

## Variants

- **A biased coin.** With heads probability $p$, the longest head run is about $\log_{1/p} n$. The same proofs work with $2$ replaced by $1/p$.
- **Runs of identical outcomes.** $S_n$, as defined above. Its mean is $1 + \mathbb{E}[R_{n-1}] \approx \lg n + 1/3$.
- **Runs with a few errors.** The longest stretch with at most $r$ tails. It is also logarithmic, with a larger constant.
- **Runs in other alphabets.** For $n$ uniform letters from an alphabet of size $a$, the longest run of one fixed letter is about $\log_a n$.

## Examples

**Exact means.** The table gives $\mathbb{E}[R_n]$ computed exactly from the recurrence under Known algorithms, the value $\lg n - 2/3$, and the gap $\mathbb{E}[R_n] - \lg n$. The last column is the mean of a simulation with numpy (seed 5; 100000, 5000 and 200 runs).

| $n$ | $\lg n$ | $\mathbb{E}[R_n]$ | $\lg n - 2/3$ | $\mathbb{E}[R_n] - \lg n$ | simulated mean |
| --- | --- | --- | --- | --- | --- |
| 10 | 3.322 | 2.799 | 2.655 | $-0.523$ | |
| 100 | 6.644 | 5.992 | 5.977 | $-0.652$ | |
| 200 | 7.644 | 6.984 | 6.977 | $-0.660$ | 6.977 |
| 1000 | 9.966 | 9.300 | 9.299 | $-0.666$ | |
| $10^4$ | 13.288 | 12.621 | 12.621 | $-0.667$ | 12.596 |
| $10^5$ | 16.610 | 15.942 | 15.943 | $-0.667$ | |
| $10^6$ | 19.932 | 19.264 | 19.265 | $-0.667$ | 19.470 |

**The distribution for 200 flips.** $\Pr[R_{200} = k]$ for the likely values:

| $k$ | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\Pr[R_{200} = k]$ | 0.0334 | 0.1650 | 0.2572 | 0.2240 | 0.1465 | 0.0833 | 0.0442 | 0.0227 |

So $\Pr[R_{200} \ge 6] = 0.80$ and $\Pr[R_{200} \le 4] = 0.034$. A sequence of 200 "random" flips with no run of five heads is suspect. The streak of identical outcomes in 200 flips has mean $1 + \mathbb{E}[R_{199}] = 7.977$.

## Known algorithms

**Computing $R$ of a given sequence.** One pass with a counter of the current run and the best run so far takes $\Theta(n)$ time and $O(1)$ space. This is [run-length encoding](/run-length-encoding/) that keeps only the longest run.

**The exact distribution.** Let $a_m = \Pr[R_m < k]$ for a fixed $k \ge 1$. Then $a_m = 1$ for $0 \le m < k$, and for $m \ge k$,
$$ a_m = \sum_{j=1}^{k} 2^{-j} a_{m-j}. $$
To see this, condition on the first tail. If it is at position $j \le k$, which has probability $2^{-j}$, the first $j - 1$ heads form a run shorter than $k$ and the rest is a fresh sequence of $m - j$ flips. If the first $k$ flips are all heads, then $R_m \ge k$. Subtracting the equation for $m - 1$ from the one for $m$ (valid for $m \ge k + 1$) gives the shorter form $a_m = a_{m-1} - 2^{-(k+1)}a_{m-k-1}$. So $\Pr[R_n < k]$ costs $O(n)$ arithmetic operations for each $k$, and $\mathbb{E}[R_n] = \sum_{k \ge 1}\Pr[R_n \ge k]$ costs $O(n\log n)$, since $\Pr[R_n \ge k] \le n2^{-k}$ is negligible for $k > \lg n + 60$.

## Bounds

**Upper bound: $\Pr[R_n \ge k] \le n 2^{-k}$, and $\mathbb{E}[R_n] \le \lceil\lg n\rceil + 1$.** A run of length $k$ starts at one of $n - k + 1$ positions, and a given position starts one with probability $2^{-k}$. By the union bound, $\Pr[R_n \ge k] \le (n - k + 1)2^{-k} \le n2^{-k}$. With $r = \lceil \lg n\rceil$,
$$ \mathbb{E}[R_n] = \sum_{k \ge 1}\Pr[R_n \ge k] \le \sum_{k=1}^{r} 1 + \sum_{k > r} n 2^{-k} = r + n2^{-r} \le \lceil\lg n\rceil + 1. $$
In particular $\Pr[R_n \ge 2\lceil\lg n\rceil] \le n \cdot n^{-2} = 1/n$, which is the form in CLRS, and $\Pr[R_n \ge \lg n + t] \le 2^{-t}$ for each $t \ge 0$.

**Lower bound: $\Pr[R_n < s] \le 1/n$ with $s = \lfloor (\lg n)/2 \rfloor$, for $n \ge 1498$.** Cut the flips into $b = \lfloor n/s\rfloor$ disjoint blocks of $s$ flips. A block is all heads with probability $2^{-s} \ge n^{-1/2}$, and the blocks are independent. If no run of length $s$ exists, then no block is all heads, so
$$ \Pr[R_n < s] \le (1 - 2^{-s})^{b} \le e^{-b2^{-s}} \le e^{-b/\sqrt n}. $$
Since $s \le (\lg n)/2$, $b \ge n/s - 1 \ge 2n/\lg n - 1$, so the exponent is at least $2\sqrt n/\lg n - 1/\sqrt n$. This is at least $\ln n$ for each $n \ge 1498$: it holds at $n = 1498$, and beyond it the derivative of $2\sqrt n/\lg n$ exceeds that of $\ln n$. Hence $\Pr[R_n < s] \le 1/n$, and $\mathbb{E}[R_n] \ge s\Pr[R_n \ge s] \ge \lfloor(\lg n)/2\rfloor(1 - 1/n)$. With the upper bound, $\mathbb{E}[R_n] = \Theta(\lg n)$.

**A sharper lower bound.** For $n \ge 256$, let $k = \lfloor \lg n - 2\lg\lg n\rfloor \ge 2$. Then $2^{-k} \ge (\lg n)^2/n$ and $\lfloor n/k\rfloor \ge n/\lg n - 1$, so the same block argument gives an exponent of at least $\lg n - (\lg n)^2/n \ge \lg n - 1$ and
$$ \Pr[R_n < k] \le e^{1 - \lg n} = e\,n^{-1/\ln 2} \le e\,n^{-1.44}. $$
Together with $\Pr[R_n \ge \lg n + t] \le 2^{-t}$, this shows $\lg n - 2\lg\lg n - 1 \le R_n \le \lg n + t$ with probability at least $1 - e\,n^{-1.44} - 2^{-t}$. So $R_n / \lg n \to 1$ in probability.

**The exact asymptotics.** Erdős and Rényi proved in 1970 that $R_n / \lg n \to 1$ almost surely. Schilling gives the approximation $\mathbb{E}[R_n] \approx \log_{1/p}(n(1-p)) + \gamma/\ln(1/p) - 1/2$ for heads probability $p$; for $p = 1/2$ this is $\lg n - 1 + 0.8327 - 0.5 = \lg n - 0.667$, which the table confirms to three decimals for $n \ge 1000$. The distribution of $R_n - \lg n$ does not converge: it oscillates slowly with $\lg n$, but its spread stays bounded: the exact variance of $R_n$ is 3.46 at $n = 1000$ and 3.51 at $n = 10^5$.

## Reductions

- **Streaks to head runs.** As shown in the Definition, $S_n$ has the distribution of $1 + R_{n-1}$, so every bound for $R$ gives a bound for $S$.
- **Balls into bins.** Both problems bound a maximum of many dependent counts by a union bound for the upper side and by independent blocks or a second moment for the lower side. The maximum load is $\Theta(\ln n/\ln\ln n)$ there and the longest run is $\Theta(\lg n)$ here.

## Applications

- **Testing randomness.** The longest-run test of the NIST randomness test suite compares the longest run of ones in blocks with its known distribution. Classroom versions tell real coin flips from invented ones by the length of the longest run.
- **Compression.** The longest run sets the largest count that run-length encoding of random bits must store, about $\lg n$.
- **Sports and finance.** "Hot hand" claims are judged against the long streaks that chance alone produces.

## References
