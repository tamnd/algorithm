---
tag: YA1S1T
kind: algorithm
slug: bogosort
name: Bogosort
aliases:
- permutation sort
- stupid sort
- monkey sort
area: sorting/comparison-sorts
level: intro
summary: Randomly permutes the array until sorted; expected factorial time, included as a pedagogical counterexample.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {expected: Θ(n · n!), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: false, comparison: true, recursive: false}
prereqs: [fisher-yates-shuffle, geometric-distribution, las-vegas-algorithm]
see_also: [sorting-problem, random-permutation, expected-running-time, stooge-sort, next-permutation, comparison-sort-lower-bound]
sources:
  - paper: "Hermann Gruber, Markus Holzer and Oliver Ruepp, Sorting the slow way: an analysis of perversely awful randomized sorting algorithms, Fun with Algorithms (FUN 2007), Lecture Notes in Computer Science 4475"
    locator: pp. 183 to 197 (the expected numbers of comparisons and swaps of bogosort)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 5.3, Randomized algorithms (RANDOMLY-PERMUTE and the proof that it gives a uniform random permutation)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.4, The geometric distribution (its expectation) and the chapter on martingales (Wald's equation)
---

Bogosort sorts an array by putting it in a random order again and again until the order is sorted. It is a [Las Vegas algorithm](/las-vegas-algorithm/): its output is always correct, and it stops with probability 1, but on $n$ distinct keys it needs $n!$ shuffles on average, and $\Theta(n \cdot n!)$ expected time. Nobody uses it to sort. It is a standard example of how to compute an expected running time with the [geometric distribution](/geometric-distribution/), and of a correct algorithm that is useless.

## In plain words

Throw a deck of cards in the air, pick them up in whatever order they land, and look whether they are in order. If they are not, throw them again. Sooner or later they will land in order, and then you stop.

The check is quick: walk along the row and stop at the first pair that is in the wrong order. The throws are the problem. With ten cards there are more than three million orders, and only one of them is sorted, so you expect to throw more than three million times.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm has access to a source of uniform random integers.

## The algorithm

```pseudo id=main
BOGOSORT(A)
L1  while not IS-SORTED(A) do
L2      SHUFFLE(A)

IS-SORTED(A)
L3  for i ← 1 to n − 1 do
L4      if A[i − 1] > A[i] then return false
L5  return true

SHUFFLE(A)                                 ▷ the Fisher-Yates shuffle
L6  for i ← n − 1 downto 1 do
L7      j ← a uniform random integer in [0, i]
L8      exchange A[i] and A[j]
```

IS-SORTED compares neighbours from the left and stops at the first pair out of order. SHUFFLE is the [Fisher-Yates shuffle](/fisher-yates-shuffle/): it puts the array in each of its $n!$ orders with probability $1/n!$, with $n - 1$ exchanges. The loop of line L1 stops at the first check that sees a sorted array.

## Example

Sort $A = [3, 1, 2]$. The check of the input stops at the first pair, after 1 comparison. Each shuffle gives one of the 6 orders with probability $1/6$. One run, with the shuffle of the Python code below and the seed 16, went like this:

| shuffle | the array after the shuffle | comparisons of the check | sorted? |
|---|---|---|---|
| 0 (input) | 3 1 2 | 1 | no |
| 1 | 3 2 1 | 1 | no |
| 2 | 3 1 2 | 1 | no |
| 3 | 2 3 1 | 2 | no |
| 4 | 1 2 3 | 2 | yes |

Shuffle 2 gave the input order again: the shuffles have no memory. The number of shuffles is random. Its mean is 6 for this input, and the mean total number of comparisons is $1 + 6 \cdot (1 + 1/2) = 10$.

## Correctness

If BOGOSORT returns, the test of line L1 has just found that $A$ is sorted, and each shuffle only exchanges items, so $A$ holds the input items in sorted order. It returns with probability 1, because each shuffle gives a sorted order with probability at least $1/n!$, independently of the earlier shuffles, so the probability that the first $k$ shuffles all fail is at most $(1 - 1/n!)^k$, which tends to 0. There is no bound on the number of shuffles that holds for every run. The full proof is below.

## Complexity

Let the keys be distinct, and let the input not be sorted. Let $N$ be the number of shuffles.

**Shuffles.** Each shuffle is sorted with probability $p = 1/n!$, independently of the others. So $N$ has the [geometric distribution](/geometric-distribution/) with parameter $p$, and

$$\mathbb{E}[N] = \frac{1}{p} = n!, \qquad \Pr[N > k] = (1 - p)^k.$$

**Exchanges.** Each shuffle makes $n - 1$ exchanges, so the expected number of exchanges is $(n-1) \cdot n!$.

**Comparisons.** On a uniformly random order, the check makes more than $k$ comparisons exactly when the first $k + 1$ items are in increasing order, which has probability $1/(k+1)!$. So the expected number of comparisons of one check is

$$\sum_{k=0}^{n-2} \Pr[\text{more than } k] = \sum_{j=1}^{n-1} \frac{1}{j!} < e - 1 \approx 1.718.$$

The checks after the shuffles are independent and have the same distribution, and $N$ is decided by them, so by Wald's equation the expected number of comparisons after the shuffles is $\mathbb{E}[N]$ times this mean. With the check of the input, the expected total is

$$C_0 + n! \sum_{j=1}^{n-1} \frac{1}{j!} \;\sim\; (e - 1)\, n!,$$

where $C_0 \le n - 1$ is the cost of the first check. This agrees with Gruber, Holzer and Ruepp (2007).

**Time.** Each shuffle costs $\Theta(n)$, so the expected time is $\Theta(n \cdot n!)$. The best case is a sorted input: one check of $n - 1$ comparisons, and $\Theta(n)$ time. The worst case is unbounded: for each $k$, some runs take more than $k$ shuffles.

| $n$ | $n!$ | expected comparisons | at $10^9$ comparisons per second |
|---|---|---|---|
| 5 | 120 | about 205 | instant |
| 10 | 3,628,800 | about $6.2 \times 10^6$ | 6 ms |
| 15 | $1.3 \times 10^{12}$ | about $2.2 \times 10^{12}$ | 37 minutes |
| 20 | $2.4 \times 10^{18}$ | about $4.2 \times 10^{18}$ | 132 years |

**Space.** $\Theta(1)$ extra, besides the random number source.

**Equal keys.** If the key values occur $m_1, \dots, m_r$ times, then $m_1! \cdots m_r!$ of the $n!$ orders are sorted, and $\mathbb{E}[N] = n! / (m_1! \cdots m_r!)$.

## Properties

- **Not stable.** The shuffle mixes equal items. The output order of equal items is random.
- **In place.** It uses $O(1)$ extra words.
- **Randomized, Las Vegas.** The answer is always correct. Only the running time is random.
- **Comparison-based.** It touches the keys only in IS-SORTED. Its expected $\Theta(n!)$ comparisons are far above the [comparison sort lower bound](/comparison-sort-lower-bound/) of $\lg(n!)$, because the shuffles ignore what the checks learned.

## Variants and improvements

- **Deterministic bogosort, or permutation sort.** Go through the $n!$ orders in a fixed sequence, for example with [next permutation](/next-permutation/), and stop at the sorted one. It always stops, after at most $n!$ orders, in $O(n \cdot n!)$ time.
- **Bozosort.** Exchange two random items instead of a full shuffle, and check again. Gruber, Holzer and Ruepp (2007) analyse it too.
- **[Stooge sort](/stooge-sort/).** A deterministic sort that is slow for a different reason: it sorts overlapping two-thirds of the array again and again, in $\Theta(n^{\lg 3/\lg 1.5}) \approx \Theta(n^{2.71})$ time.

## When to use it

Never use it to sort. Use it to teach the expectation of a geometric random variable, the difference between a Las Vegas algorithm and an algorithm with a worst-case bound, and the cost of throwing away information. For a real sort of small arrays, [insertion sort](/insertion-sort/) is simple and fast.

## Pitfalls

- **A biased shuffle.** Exchanging $A[i]$ with a random item of the whole array, for each $i$, does not give a uniform order. The algorithm still stops with probability 1, but the analysis above is wrong for it.
- **A generator with too few states.** A pseudorandom generator with $s$ bits of state gives at most $2^s$ different sequences of shuffles. From a fixed state, the run is deterministic, and the cycle of states may never produce the sorted order. With a 32-bit state and $n = 13$, there are $13! \approx 6.2 \times 10^9$ orders and only about $4.3 \times 10^9$ states, so some orders can never appear.
- **Checking with ≥.** The test $A[i-1] \ge A[i]$ in line L4 makes an array with two equal neighbours count as unsorted, so on an input with equal keys the loop never stops.

## Implementations

## History

The name is hacker slang, and the method is a joke that appears in many programming texts. Gruber, Holzer and Ruepp (2007) gave the exact expected numbers of comparisons and exchanges of bogosort and of its variants.

## References
