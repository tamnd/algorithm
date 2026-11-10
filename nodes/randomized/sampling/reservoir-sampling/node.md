---
tag: 70ENBG
kind: algorithm
slug: reservoir-sampling
name: Reservoir sampling
aliases:
- Algorithm R
- Vitter's algorithm R
- reservoir algorithm
- Waterman's reservoir algorithm
area: randomized/sampling
level: core
summary: Keep a uniform sample of k items from a stream of unknown length in one pass. Item t replaces a random slot with probability k/t, so each k-subset has probability exactly 1/C(n, k).
solves: [stream-sampling, uniform-random-subset]
model: word-ram
complexity:
  vars: {n: the number of items in the stream, k: the sample size}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1981
  people: [Alan G. Waterman, Donald E. Knuth]
  note: Knuth gives Algorithm R in the second edition of The Art of Computer Programming, Volume 2 (1981), and credits it to Alan G. Waterman. Vitter analyzed it and made it faster in 1985.
prereqs: [uniform-random-subset, binomial-coefficient, linearity-of-expectation, loop-invariant]
see_also: [stream-sampling, vitter-reservoir-skip, algorithm-l, weighted-reservoir-sampling, selection-sampling, floyd-sampling, fisher-yates-shuffle, priority-sampling]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Random sampling and shuffling, Algorithm R (Reservoir sampling), credited there to Alan G. Waterman
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 37 to 57, 1985
    locator: Section 2 (Algorithm R and the lower bound for reservoir algorithms)
  - paper: doi:10.1145/198429.198435
    title: Kim-Hung Li, Reservoir-sampling algorithms of time complexity O(n(1 + log(N/n))), ACM Transactions on Mathematical Software 20(4), 481 to 493, 1994
    locator: Section 1 (Algorithm R as the base method)
---

Reservoir sampling, or Algorithm R, picks a uniform random sample of $k$ items from a stream that it reads once, without knowing the length $n$ of the stream in advance. It keeps the first $k$ items in an array, the *reservoir*. Then item number $t$ replaces a uniformly chosen slot with probability $k/t$. At the end, each of the $\binom{n}{k}$ sets of $k$ positions is the sample with probability exactly $1/\binom{n}{k}$. It takes $\Theta(n)$ time, one random integer per item after the first $k$, and $\Theta(k)$ extra space. It is the base solution of the [stream sampling problem](/stream-sampling/), and the slower but simpler parent of the skip-based methods [Algorithm L](/algorithm-l/) and [Vitter's Algorithms X and Z](/vitter-reservoir-skip/).

## In plain words

You want to pick a few cards, fairly, from a long line of cards that pass in front of you one at a time. You do not know how many cards will come, and you cannot go back.

Keep the first few cards in your hand. When a new card comes, decide at random whether it goes into your hand. The later the card, the smaller its chance: it gets the same chance that it would have in a fair draw from all the cards seen so far. If it goes in, it replaces a card of your hand chosen at random.

At each moment, your hand is a fair sample of all the cards seen up to that moment. So whenever the line stops, the hand is a fair sample of the whole line.

## The problem

The input is a sample size $k \ge 0$ and a stream $x_1, x_2, \ldots, x_n$ that is read once, in order. The number $n$ is not known until the stream ends. The output is a set of $\min(n, k)$ positions, given by their items, such that for $n \ge k$ each $k$-subset of $\{1, \ldots, n\}$ is output with probability $1/\binom{n}{k}$. This is the [stream sampling problem](/stream-sampling/), and also a one-pass solution of the [uniform random subset problem](/uniform-random-subset/).

**Model of randomness.** The algorithm draws uniform random integers in $\{1, \ldots, t\}$. From uniform random bits, such an integer needs rejection when $t$ is not a power of 2: draw $\lceil \lg t \rceil$ bits and retry when the value is too large, which takes fewer than 2 rounds on average. All probabilities below assume exact uniform integers.

## The algorithm

```pseudo id=main
RESERVOIR-SAMPLE(stream, k)             ▷ R is an array with slots 1 .. k
L1  R ← an empty array; t ← 0
L2  for each item x of the stream do
L3      t ← t + 1                        ▷ x is item number t
L4      if t ≤ k then R[t] ← x
L5      else j ← a uniform random integer in {1, ..., t}
L6          if j ≤ k then R[j] ← x        ▷ happens with probability k/t
L7  return R[1 .. min(t, k)]
```

The first $k$ items fill the reservoir (line L4). For item $t > k$, line L5 draws $j$ uniformly from $\{1, \ldots, t\}$. The test of line L6 is true with probability $k/t$, and when it is true, $j$ is uniform over the $k$ slots. So one random integer decides both whether item $t$ enters and which slot it takes. The loop never needs $n$, so the algorithm can stop at any time and return the current reservoir.

## Example

Take $k = 3$ and the stream $a, b, c, d, e, f, g, h$ ($n = 8$). The table uses the random values $j = 2, 5, 1, 6, 3$ for $t = 4, \ldots, 8$.

| $t$ | item | chance $k/t$ | $j$ | action | reservoir after |
|---|---|---|---|---|---|
| 1 to 3 | $a, b, c$ | 1 | none | fill | $[a, b, c]$ |
| 4 | $d$ | 3/4 | 2 | $R[2] \leftarrow d$ | $[a, d, c]$ |
| 5 | $e$ | 3/5 | 5 | $j > 3$, skip | $[a, d, c]$ |
| 6 | $f$ | 1/2 | 1 | $R[1] \leftarrow f$ | $[f, d, c]$ |
| 7 | $g$ | 3/7 | 6 | $j > 3$, skip | $[f, d, c]$ |
| 8 | $h$ | 3/8 | 3 | $R[3] \leftarrow h$ | $[f, d, h]$ |

The sample is $\{d, f, h\}$. The run used $n - k = 5$ random integers. Over all $4 \cdot 5 \cdot 6 \cdot 7 \cdot 8 = 6720$ equally likely sequences of $j$, each of the $\binom{8}{3} = 56$ subsets comes out exactly $6720/56 = 120$ times.

## Correctness

**Theorem.** If $n \ge k$, RESERVOIR-SAMPLE returns each $k$-subset of the positions $\{1, \ldots, n\}$ with probability exactly $1/\binom{n}{k}$. If $n < k$, it returns all $n$ items.

The proof is by induction on $t$, with this [loop invariant](/loop-invariant/): after item $t \ge k$, the set of positions in the reservoir is a uniform $k$-subset of $\{1, \ldots, t\}$. For the step, fix a $k$-subset $S$ of $\{1, \ldots, t+1\}$. If $t + 1 \notin S$, the reservoir is $S$ after item $t+1$ exactly when it was $S$ before and item $t+1$ was rejected:

$$\frac{1}{\binom{t}{k}} \cdot \frac{t+1-k}{t+1} = \frac{1}{\binom{t+1}{k}}.$$

If $t + 1 \in S$, write $S = S' \cup \{t+1\}$. The reservoir before must be $S' \cup \{y\}$ for one of the $t - k + 1$ positions $y \notin S'$, item $t+1$ must enter (probability $k/(t+1)$), and it must take the slot of $y$ (probability $1/k$). This gives $(t-k+1) \cdot \frac{1}{\binom{t}{k}} \cdot \frac{k}{t+1} \cdot \frac{1}{k} = \frac{1}{\binom{t+1}{k}}$ again. The full proof, with the identity behind both lines, is below.

A useful consequence: each item is in the final sample with probability $k/n$, because it lies in $\binom{n-1}{k-1}$ of the $\binom{n}{k}$ equally likely subsets.

## Complexity

- **Time.** Each item costs $O(1)$ work: lines L3 to L6 do one comparison, at most one random integer and at most one write. So the time is $\Theta(n)$ for every run, best and worst, in the [word RAM](/word-ram/) model with a unit-cost random integer.
- **Random integers.** Exactly $n - k$ for $n \ge k$, one for each item after the first $k$. With random bits and rejection, the expected number of bits is less than $2 \sum_{t=k+1}^{n} \lceil \lg t \rceil$.
- **Writes to the reservoir.** Item $t > k$ enters with probability $k/t$, so by [linearity of expectation](/linearity-of-expectation/) the expected number of replacements is
$$\sum_{t=k+1}^{n} \frac{k}{t} = k\,(H_n - H_k) \approx k \ln \frac{n}{k}.$$
For $n = 10^6$ and $k = 100$ this is about 920.5. So most of the random integers of Algorithm R are spent on items that are thrown away. The skip methods use this: they draw the gap to the next replacement directly, and need only $O(k(1 + \log(n/k)))$ random numbers in expectation.
- **Space.** The reservoir holds $k$ items, so the extra space is $\Theta(k)$.

## Properties

- **Online.** After any prefix of $t \ge k$ items, the reservoir is a uniform sample of that prefix. The caller can stop the stream at any time.
- **One pass.** Each item is read once and is not stored unless it enters the reservoir.
- **Randomized.** The output is random. The time and the number of random integers do not depend on the random choices.
- **The order is not random.** The set of positions is uniform, but the order in the array is not: for $n = k$ the array is the stream in order. Shuffle the reservoir with [Fisher-Yates](/fisher-yates-shuffle/) if a random order is needed.

## Variants and improvements

- **Skip-based methods.** Instead of one random integer per item, draw the number of items to skip before the next replacement. [Vitter's Algorithm X](/vitter-reservoir-skip/) finds the skip by a sequential search, and Algorithm Z by rejection, in $O(k(1 + \log(n/k)))$ expected time. [Algorithm L](/algorithm-l/) of Li draws the skip from a geometric distribution with a random parameter, with the same expected time and a much shorter program.
- **Weighted sampling.** When item $i$ has a weight $w_i$, the key method of Efraimidis and Spirakis keeps the $k$ items with the largest keys $u_i^{1/w_i}$. See [weighted reservoir sampling](/weighted-reservoir-sampling/), and [priority sampling](/priority-sampling/) for unbiased estimates of subset sums.
- **Known length.** If $n$ is known in advance, [selection sampling](/selection-sampling/) (Knuth's Algorithm S) gives a sample in stream order, and [Floyd's algorithm](/floyd-sampling/) draws $k$ positions with exactly $k$ random integers.
- **Sampling with replacement.** Run $k$ independent reservoirs of size 1. Each keeps item $t$ with probability $1/t$.
- **Distributed streams.** Give each item a uniform random key and keep the $k$ smallest keys. The samples of several streams then merge by taking the $k$ smallest keys of their union. This is the uniform case of the key method of [weighted reservoir sampling](/weighted-reservoir-sampling/).

## When to use it

Use Algorithm R when the length of the input is unknown or too large to store, and the per-item cost of one random integer is acceptable: logs, database scans, and the result rows of a query. When $n \gg k$ and random numbers are expensive, use [Algorithm L](/algorithm-l/), which draws only about $3k \ln(n/k)$ random numbers. When the items are in an array of known length $n$, [Floyd's algorithm](/floyd-sampling/) or a partial [Fisher-Yates shuffle](/fisher-yates-shuffle/) needs only $k$ random integers. The page on the [stream sampling problem](/stream-sampling/) compares all of these.

## Pitfalls

- **The wrong range in line L5.** Drawing $j$ from $\{1, \ldots, t-1\}$, a common off-by-one with 0-based code such as `randrange(t - 1)`, gives item $t$ the chance $k/(t-1)$ and makes the sample biased toward late items. The right call is `randrange(t)` with 0-based slots and the test `j < k`. For $n = 5$ and $k = 2$ the wrong version is far from uniform.
- **Two random numbers where one suffices.** First testing "accept with probability $k/t$" with a random real, then drawing a slot, is correct but costs twice the random numbers. Drawing one $j$ in $\{1, \ldots, t\}$ does both.
- **A random real for the test.** `random() < k / t` in floating point has a bias of order $2^{-53}$, which is invisible in tests. `floor(t * random())` also has a small bias for large $t$. Use an exact uniform integer, as in Python's `randrange`.
- **Returning the reservoir in its stored order.** Code that takes "the first item of the sample" as a random item is wrong when $n$ is small, since the first slot holds item 1 unless it was replaced.
- **Assuming the sample is a random sample with replacement.** The $k$ items are distinct positions. Statistics that assume independent draws need a correction factor of $(n-k)/(n-1)$ for the variance.

## Implementations

## History

Knuth gives Algorithm R in Section 3.4.2 of The Art of Computer Programming, Volume 2, and credits it to Alan G. Waterman. Vitter (1985) proved that every reservoir algorithm must, in expectation, put at least $k(1 + H_n - H_k)$ items in the reservoir, and he gave Algorithms X, Y and Z, which reach this bound in the number of random draws and, for Z, in the running time. Li (1994) gave the simpler Algorithm L with the same expected time. The name "Vitter's Algorithm R" is common, because Vitter's paper made the method widely known, but the method is older than that paper.

## References
