---
tag: ZE9C9M
kind: algorithm
slug: algorithm-l
name: Algorithm L
aliases:
- Li's skip reservoir sampling
- Li's Algorithm L
- geometric-jump reservoir sampling
area: randomized/sampling
level: core
summary: Reservoir sampling that skips ahead by geometric jumps whose parameter is the largest of k hidden uniform keys. It uses about 3k ln(n/k) random numbers instead of n.
solves: [stream-sampling]
model: word-ram
complexity:
  vars: {n: the number of items in the stream, k: the sample size}
  time: {expected: "O(k(1 + log(n/k)))", worst: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1994
  people: [Kim-Hung Li]
  note: Li published Algorithm L, with Algorithms K and M, in ACM Transactions on Mathematical Software in 1994.
prereqs: [reservoir-sampling, geometric-distribution, uniform-distribution]
see_also: [vitter-reservoir-skip, reservoir-sampling, stream-sampling, weighted-reservoir-sampling, inverse-transform-sampling, selection-sampling]
sources:
  - paper: doi:10.1145/198429.198435
    title: Kim-Hung Li, Reservoir-sampling algorithms of time complexity O(n(1 + log(N/n))), ACM Transactions on Mathematical Software 20(4), 481 to 493, 1994
    locator: the section on Algorithm L (the geometric skip with a random parameter) and its expected cost
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 37 to 57, 1985
    locator: Section 3 (the skip random variable) and the lower bound of Section 2
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2 (Algorithm R, the method that Algorithm L speeds up)
---

Algorithm L, by Kim-Hung Li (1994), is a [reservoir sampling](/reservoir-sampling/) method that skips over the items that will not enter the sample. It gives each item a hidden uniform key and keeps the $k$ items with the smallest keys, but it never draws the keys of the skipped items. It only keeps $W$, the largest key in the reservoir, and draws the number of items to skip from a [geometric distribution](/geometric-distribution/) with parameter $W$. It returns a uniform $k$-subset of a stream of $n$ items with $O(k(1 + \log(n/k)))$ random numbers and time in expectation, if a skip costs $O(1)$. It reaches the same bound as [Vitter's Algorithm Z](/vitter-reservoir-skip/), with a loop of four lines.

## In plain words

Think of each item of the stream as getting a secret lottery ticket, a random number between 0 and 1. The sample is the set of items with the smallest tickets. The hand of kept items has a worst ticket, the largest one among them. A new item gets into the hand only if its ticket beats that worst ticket.

The trick is not to draw tickets for the items that lose. The chance that a new item wins is just the value of the worst ticket. So the algorithm draws, in one step, how many items lose in a row before the next winner, and jumps over them. When a winner arrives, it throws out a random kept item, and it draws the new worst ticket directly. Late in the stream, winners are rare, so the jumps are long and few random numbers are needed.

## The problem

The input is a sample size $k \ge 1$ and a stream $x_1, x_2, \ldots, x_n$ read once, with $n$ unknown in advance. The output is a uniform $k$-subset of the positions, given by their items, or all items if $n < k$. This is the [stream sampling problem](/stream-sampling/).

**Model.** The algorithm uses independent uniform reals in $(0, 1]$, uniform integers in $\{1, \ldots, k\}$, and the functions $\ln$ and $\exp$, at unit cost. The cost bound counts a skip of $g$ items as $O(1)$: this holds for an array, a file with random access, or a source that can drop items without handing them over. If each item must be read, the reading takes $\Theta(n)$ time, but the work of the algorithm is still $O(k(1 + \log(n/k)))$.

## The algorithm

```pseudo id=main
ALGORITHM-L(stream, k)                  ▷ k ≥ 1; R has slots 1 .. k
L1  R ← the first k items; i ← k          ▷ return R if the stream has fewer
L2  W ← exp(ln(random()) / k)            ▷ W = U^(1/k), the largest of k uniform keys
L3  loop
L4      G ← ⌊ln(random()) / ln(1 − W)⌋     ▷ number of items that do not enter
L5      i ← i + G + 1
L6      if the stream has fewer than i items then return R
L7      R[a uniform random integer in {1, ..., k}] ← item i
L8      W ← W · exp(ln(random()) / k)    ▷ the largest of k uniform keys in (0, W)
```

Here random() is a uniform real in $(0, 1]$. The key of each item in the reservoir is uniform below $W$, and $W$ is the largest of them. A new item enters when its key is less than $W$, so the number $G$ of items that do not enter before the next one that does has $\Pr[G \ge g] = (1 - W)^g$. Line L4 draws $G$ by [inversion](/inverse-transform-sampling/). The entering item has a key uniform below $W$, so after it replaces the item with the largest key, the $k$ keys are again independent and uniform below $W$, and their new maximum is $W \cdot V^{1/k}$. Line L8 draws it. Which item had the largest key is uniform over the slots, by symmetry, so line L7 picks a uniform slot.

## Example

Take $k = 3$ and a stream $x_1, \ldots, x_{20}$. Line L1 keeps $[x_1, x_2, x_3]$. The table shows the random reals $u$ of line L4, the slots of line L7, and the reals $v$ of line L8. The first real is $0.729$, so $W = 0.729^{1/3} = 0.9$.

| round | $W$ before | $u$ | $\ln u / \ln(1 - W)$ | $G$ | $i$ | slot | $v$ | reservoir after | $W$ after |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.9 | 0.5 | 0.301 | 0 | 4 | 2 | 0.512 | $[x_1, x_4, x_3]$ | 0.72 |
| 2 | 0.72 | 0.3 | 0.946 | 0 | 5 | 1 | 0.343 | $[x_5, x_4, x_3]$ | 0.504 |
| 3 | 0.504 | 0.2 | 2.295 | 2 | 8 | 3 | 0.729 | $[x_5, x_4, x_8]$ | 0.4536 |
| 4 | 0.4536 | 0.1 | 3.810 | 3 | 12 | 2 | 0.125 | $[x_5, x_{12}, x_8]$ | 0.2268 |
| 5 | 0.2268 | 0.05 | 11.647 | 11 | 24 | stop | | $[x_5, x_{12}, x_8]$ | |

The sample is $\{x_5, x_8, x_{12}\}$. The run used 14 random numbers for a stream of 20 items. Algorithm R would use 17. The gap grows as $W$ falls: the expected number of entries for $n = 20$ and $k = 3$ is $3(H_{20} - H_3) \approx 5.29$, and on a stream of $10^6$ items with $k = 100$ it is only about 920.5.

## Correctness

**Theorem (Li 1994).** In exact arithmetic, for $n \ge k \ge 1$, ALGORITHM-L returns each $k$-subset of the positions with probability $1/\binom{n}{k}$, the same output law as [Algorithm R](/reservoir-sampling/).

The proof couples the algorithm with the *key process*: independent uniform keys $u_1, \ldots, u_n$, and $A_t$ the positions of the $k$ smallest keys among the first $t$. By symmetry $A_n$ is a uniform $k$-subset. Then one shows that $(A_t, M_t)$, where $M_t$ is the $k$-th smallest key, is a Markov chain that moves exactly as lines L4 to L8 do: the next entry comes after a geometric number of items with parameter $M_t$, a uniform member of $A_t$ leaves, and $M$ is multiplied by $V^{1/k}$. The key step is the invariant that, given the past, the $k - 1$ keys of $A_t$ other than the largest are independent and uniform on $(0, M_t)$. The full proof is below.

## Complexity

- **Number of rounds.** Each round of the loop puts one item into the reservoir, except the last one. Item $t > k$ enters with probability $k/t$, and these events are independent, so the expected number of entries is
$$E[\text{entries}] = \sum_{t=k+1}^{n} \frac{k}{t} = k(H_n - H_k) \le k \ln \frac{n}{k}.$$
- **Random numbers.** One for line L2, then three in each round that enters (lines L4, L7 and L8) and one in the last round. The expected total is $2 + 3k(H_n - H_k)$. For $n = 10^5$ and $k = 10$ this is about 276.8, against $n - k = 99990$ for Algorithm R.
- **Time.** Line L1 takes $\Theta(k)$. Each round takes $O(1)$ when a skip costs $O(1)$. So the expected time is $O(k + k(H_n - H_k)) = O(k(1 + \log(n/k)))$.
- **Worst case.** Each round moves $i$ forward by at least 1, so there are at most $n - k + 1$ rounds and the time is $O(n)$ for every sequence of random numbers.
- **Space.** The reservoir and $O(1)$ numbers: $\Theta(k)$.
- **Lower bound.** Vitter (1985) showed that every reservoir algorithm puts at least $k(1 + H_n - H_k)$ items in the reservoir in expectation, because after item $t$ the reservoir must already be a uniform sample of the first $t$ items. So Algorithm L is optimal up to a constant factor.

## Properties

- **Online.** After each round the reservoir is a uniform sample of the items so far, so the stream can stop at any time.
- **Same output law as Algorithm R.** Only the use of random numbers differs. A test can compare the two outputs in distribution.
- **Exact only in exact arithmetic.** Lines L2, L4 and L8 use $\ln$, $\exp$ and a floor of a real. In double precision the skip law is rounded, with relative errors near $10^{-16}$ per round. The output is then very close to uniform, but not exactly uniform.
- **Randomized, not recursive.** The work is random. It uses a constant number of variables besides the reservoir.

## Variants and improvements

- **Vitter's Algorithm Z.** It draws the same skip by rejection from a continuous envelope, in $O(1)$ expected time per skip, and Algorithm X draws it by a sequential search. See [Vitter's skip-based reservoir sampling](/vitter-reservoir-skip/). Algorithm L draws the skip by inversion from a geometric law with a random parameter, which needs no rejection.
- **Weighted version.** The A-ExpJ method of Efraimidis and Spirakis uses the same idea, an exponential jump over the items that cannot enter, for weighted keys. See [weighted reservoir sampling](/weighted-reservoir-sampling/).
- **Li's Algorithms K and M.** Li's paper gives two more skip methods, K and M, with the same order of expected time.
- **Known length.** If $n$ is known, [selection sampling](/selection-sampling/) gives a sample in stream order, and it also has skip forms.

## When to use it

Use Algorithm L when the stream is long compared with $k$ and either random numbers are costly or skipping is cheap: sampling rows from a large table, lines from a file read in blocks, or events from a fast feed. It has the time bound of Algorithm Z with much shorter code. For short streams, or when every item must be touched anyway, [Algorithm R](/reservoir-sampling/) is simpler and has no floating point. For weighted items, use [weighted reservoir sampling](/weighted-reservoir-sampling/).

## Pitfalls

- **ln(0).** Many generators return reals in $[0, 1)$, and $\ln 0$ fails. Use $1 - \text{random}()$, which is in $(0, 1]$.
- **ln(1 − W) for a tiny W.** When $W < 10^{-16}$, $1 - W$ rounds to 1 and line L4 divides by 0. Compute $\ln(1 - W)$ as `log1p(-W)`.
- **The missing + 1 in line L5.** With $i \leftarrow i + G$, a skip of 0 puts the current item in the reservoir a second time. The sample then has repeats.
- **W not updated.** If line L8 is left out, late items enter far too often. With $n = 12$ and $k = 3$ the chi-squared statistic over the 220 subsets is above $2 \cdot 10^5$, against about 220 for the right method.
- **A new key instead of $W \cdot V^{1/k}$.** Setting $W$ to a fresh $U^{1/k}$ forgets that all keys are below the old $W$, and biases the sample toward late items.

## Implementations

## History

Kim-Hung Li published Algorithms K, L and M in ACM Transactions on Mathematical Software in 1994, with the title giving their common bound $O(n(1 + \log(N/n)))$ in the notation where $n$ is the sample size and $N$ the stream length. The bound and the lower bound behind it are from Vitter (1985), whose Algorithm Z first reached it, with a longer method based on rejection.

## References
