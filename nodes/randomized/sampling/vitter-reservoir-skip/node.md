---
tag: 2ZA0EM
kind: algorithm
slug: vitter-reservoir-skip
name: Vitter's skip-based reservoir sampling
aliases:
- Vitter Algorithm X
- Vitter Algorithm Z
- Algorithm Z
- reservoir sampling with skips
area: randomized/sampling
level: advanced
summary: Reservoir sampling that draws how many stream items to skip before the next change, by search (Algorithm X) or by rejection (Algorithm Z), in O(k(1 + log(n/k))) expected time.
solves: [stream-sampling]
model: word-ram
complexity:
  vars: {n: the number of items in the stream, k: the sample size}
  time: {expected: "O(k(1 + log(n/k)))", worst: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1985
  people: [Jeffrey Scott Vitter]
  note: Vitter gave Algorithms X, Y and Z and the lower bound on the number of reservoir changes in ACM Transactions on Mathematical Software in 1985.
prereqs: [reservoir-sampling, rejection-sampling, inverse-transform-sampling]
see_also: [algorithm-l, reservoir-sampling, stream-sampling, selection-sampling, weighted-reservoir-sampling, rejection-sampling]
sources:
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 37 to 57, 1985
    locator: the sections on the skip random variable, Algorithm X, Algorithm Z with its rejection bounds, and the lower bound on the number of reservoir changes
  - paper: doi:10.1145/198429.198435
    title: Kim-Hung Li, Reservoir-sampling algorithms of time complexity O(n(1 + log(N/n))), ACM Transactions on Mathematical Software 20(4), 481 to 493, 1994
    locator: the comparison of Algorithms K, L and M with Algorithm Z
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2 (Algorithm R, the method whose skips Algorithms X and Z draw)
---

Vitter's skip-based reservoir sampling is a family of [reservoir sampling](/reservoir-sampling/) methods from Jeffrey Vitter's 1985 paper. [Algorithm R](/reservoir-sampling/) draws one random number for each item of the stream. Vitter's methods draw instead the *skip*, the number of items that Algorithm R would reject before the next item it accepts, and jump over those items. Algorithm X draws the skip by a sequential search with one random number. Algorithm Z draws it by [rejection](/rejection-sampling/) from a continuous envelope, with $O(1)$ expected work per skip. The output has the same law as Algorithm R: a uniform $k$-subset of the $n$ items. Algorithm Z runs in $O(k(1 + \log(n/k)))$ expected time when a skip costs $O(1)$, which is optimal up to a constant factor. [Algorithm L](/algorithm-l/) later reached the same bound with a shorter method.

## In plain words

The simple reservoir method rolls a die for every item that goes by, and late in a long stream almost every roll says "ignore this item". That wastes time.

Vitter's idea is to ask a different question once: how many items in a row will be ignored before the next one is kept? The answer has a known law, so it can be drawn directly, and the algorithm jumps over that many items at once.

Algorithm X finds the answer by walking up the table of chances until a random number is passed. That walk is as long as the jump, so it saves random numbers but not time. Algorithm Z guesses the answer from a smooth curve that lies a little above the true law, and keeps the guess only if a second random number agrees. Most guesses are kept, so each jump costs a few steps.

## The problem

The input is a sample size $k \ge 1$ and a stream $x_1, x_2, \ldots, x_n$ read once, with $n$ unknown in advance. The output is a uniform $k$-subset of the positions, given by their items, or all items if $n < k$. This is the [stream sampling problem](/stream-sampling/).

**The skip.** After Algorithm R has processed $t \ge k$ items, let $S$ be the number of later items that it rejects before the next item that it accepts. Item $t + j$ is accepted with probability $k/(t+j)$, independently, so
$$\Pr[S \ge s] = \prod_{j=1}^{s} \frac{t + j - k}{t + j}, \qquad f(s) = \Pr[S = s] = \frac{k}{t+s+1} \prod_{i=0}^{k-1} \frac{t-i}{t+s-i}.$$

**Model.** The algorithm uses independent uniform reals in $[0, 1)$, uniform integers, and $\ln$ and $\exp$, at unit cost. As for [Algorithm L](/algorithm-l/), the time bound counts a skip over $s$ items as $O(1)$. This holds for an array, a file with random access, or a source that can drop items without handing them over.

## The algorithm

```pseudo id=main
VITTER-RESERVOIR(stream, k)               ▷ k ≥ 1; T is the switch constant, Vitter uses 22
L1  R ← the first k items; t ← k            ▷ return R if the stream has fewer
L2  W ← exp(−ln(random()) / k)             ▷ W = U^(−1/k), the state of SKIP-Z
L3  loop
L4      if t ≤ T·k then S ← SKIP-X(t, k) else S ← SKIP-Z(t, k)
L5      skip S items; if the stream ends, return R
L6      R[a uniform random slot] ← the next item
L7      t ← t + S + 1

SKIP-X(t, k)                              ▷ sequential search
L8  V ← random(); S ← 0; t ← t + 1; q ← (t − k)/t     ▷ q = Pr[S ≥ 1]
L9  while q > V
L10     S ← S + 1; t ← t + 1; q ← q · (t − k)/t       ▷ q = Pr[S ≥ S + 1]
L11 return S

SKIP-Z(t, k)                              ▷ rejection; uses and updates W
L12 term ← t − k + 1
L13 loop
L14     U ← random(); X ← t(W − 1); S ← ⌊X⌋        ▷ X has density g
L15     lhs ← (U · ((t + 1)/term)² · (term + S)/(t + X))^(1/k)
L16     rhs ← ((t + X)/(term + S)) · term/t
L17     if lhs ≤ rhs then W ← rhs/lhs; return S      ▷ quick accept: U ≤ h(S)/(c g(X))
L18     y ← (U (t + 1)/term) · (t + S + 1)/(t + X) · ∏_{i<k} (t + S − i)/(t − i)
L19     W ← exp(−ln(random()) / k)
L20     if y^(1/k) ≤ (t + X)/t then return S        ▷ exact test: U ≤ f(S)/(c g(X))
```

SKIP-X walks through the tail probabilities $\Pr[S \ge s]$ until one falls to $V$ or below. This is [inversion](/inverse-transform-sampling/) by sequential search, and it takes $O(1 + S)$ steps.

SKIP-Z uses three functions. The continuous variable $X = t(U^{-1/k} - 1)$ has density
$$g(x) = \frac{k}{t+x}\left(\frac{t}{t+x}\right)^{k}, \qquad x \ge 0,$$
and with $c = \frac{t+1}{t-k+1}$ the curve $c\,g$ lies above $f$ on each interval $[s, s+1)$. A simpler function
$$h(s) = \frac{k}{t+1}\left(\frac{t-k+1}{t-k+1+s}\right)^{k+1}$$
lies below $f$. Line L14 draws $X$ from $g$ and proposes $S = \lfloor X \rfloor$. Line L17 accepts at once when $U \le h(S)/(c\,g(X))$, which costs $O(1)$. Only when that fails does line L18 compute the product in $f(S)$, and line L20 makes the exact test $U \le f(S)/(c\,g(X))$. The roots and quotients in lines L15 to L20 are these tests after the common factors are moved and the $k$-th roots are taken. Line L17 reuses $U$ to make the next $W$, so a quick accept costs one random number.

## Example

**Algorithm X.** Take $k = 3$ and $t = 10$. The tail probabilities are:

| $s$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $\Pr[S \ge s]$ | 1 | 0.7273 | 0.5455 | 0.4196 | 0.3297 | 0.2637 | 0.2143 | 0.1765 |

With $V = 0.35$, the loop passes $0.7273$, $0.5455$ and $0.4196$, which are all above $V$, and stops at $0.3297 \le V$. So $S = 3$: items 11, 12 and 13 are skipped and item 14 goes into a uniform slot. Algorithm R would have used four random numbers for these four items. SKIP-X used one.

**Algorithm Z.** Take $k = 3$ and $t = 100$, so $\mathit{term} = 98$ and $c = 101/98 \approx 1.0306$. Say the state came from $U' = 0.6$, so $W = 0.6^{-1/3} \approx 1.18563$. Line L14 gives $X = 100 \cdot 0.18563 = 18.563$ and $S = 18$. With $U = 0.4$:

- line L15: $\mathit{lhs} = (0.4 \cdot (101/98)^2 \cdot 116/118.563)^{1/3} \approx 0.7463$,
- line L16: $\mathit{rhs} = (118.563/116) \cdot 98/100 \approx 1.00165$.

So $\mathit{lhs} \le \mathit{rhs}$ and line L17 returns $S = 18$ without the product. The new state is $W = 1.00165/0.7463 \approx 1.3421$. For comparison, $f(18) \approx 0.015272$, $h(18) \approx 0.015131$ and $c\,g(18.563) \approx 0.015647$: the two bounds are within 3% of $f$ here, so the quick test decides almost every round.

## Correctness

**Theorem (Vitter 1985).** In exact arithmetic, SKIP-X and SKIP-Z both return a value with the law $f$ of the skip, and SKIP-Z leaves the state $W$ with the law of $U^{-1/k}$, independent of the past. Hence, for every $n \ge k \ge 1$ and every switch constant $T$, VITTER-RESERVOIR returns each $k$-subset of the positions with probability $1/\binom{n}{k}$, the same output law as [Algorithm R](/reservoir-sampling/).

SKIP-X is inversion: it returns at least $s$ exactly when $\Pr[S \ge s] > V$. For SKIP-Z the proof has three parts. The lemma $h(s) \le f(s) \le c\,g(x)$ for $s \le x < s+1$ reduces, factor by factor, to the polynomial inequality $a^2(a + i + s + 1) \le (a + i)(a + 1)(a + s)$, whose two sides differ by $as + ias + ia + is \ge 0$. Then each round accepts value $s$ with probability $\int_s^{s+1} g(x) \frac{f(s)}{c\,g(x)}\,dx = f(s)/c$, so the accepted value has law $f$. Last, after a quick accept, $U$ is uniform below the threshold, so the reused $W$ is again distributed as $U^{-1/k}$. The full proof is below.

## Complexity

- **Number of skips.** Each skip but the last ends in a reservoir change. Item $t > k$ is accepted with probability $k/t$, independently, so the expected number of changes is $k(H_n - H_k) \le k \ln(n/k)$.
- **Algorithm X alone.** One random number per skip, but $O(1 + S)$ time, so $O(n)$ time in total. It saves random numbers, not time.
- **Algorithm Z.** The number of rounds per skip is geometric with mean $c = \frac{t+1}{t-k+1}$. For $t > Tk$ with $T = 22$, $c < 1 + 1/21$. The quick test costs $O(1)$. Vitter shows that the exact test is reached rarely enough that its product of up to $\min(k, S)$ factors costs $O(1)$ expected time per skip. So each skip costs $O(1)$ in expectation.
- **Total time.** Line L1 takes $\Theta(k)$. While $t \le Tk$, SKIP-X spends $O(1)$ per item, so $O(Tk)$ in total. After that, $O(1)$ per change. The expected time is $O(k + k(H_n - H_k)) = O(k(1 + \log(n/k)))$.
- **Worst case.** Each round of line L3 moves $t$ forward by at least 1, so there are at most $n - k + 1$ skips. A single SKIP-Z call has no worst-case bound on its rounds, but it stops with probability 1.
- **Space.** The reservoir and $O(1)$ numbers: $\Theta(k)$.
- **Lower bound.** Vitter proved that every reservoir algorithm makes at least $k(1 + H_n - H_k)$ insertions into the reservoir in expectation, because after item $t$ the reservoir must already be a uniform sample of the first $t$ items. So Algorithm Z is optimal up to a constant factor.

**Measured cost.** In a simulation of SKIP-Z at fixed $t$, the mean number of rounds per skip and of steps of the product loop per skip were:

| $k$ | $t$ | rounds per skip | product steps per skip |
|---|---|---|---|
| 2 | $22k$ | 1.047 | 0.135 |
| 10 | $22k$ | 1.051 | 0.64 |
| 50 | $22k$ | 1.050 | 2.14 |
| 250 | $22k$ | 1.047 | 2.56 |
| 250 | $200k$ | 1.005 | 1.36 |

For $n = 10^5$ and $k = 10$, a full run used 185.8 random numbers on average over 400 seeds, against $k(H_n - H_k) \approx 91.6$ changes and $n - k = 99990$ random numbers for Algorithm R.

## Properties

- **Online.** After each change the reservoir is a uniform sample of the items so far.
- **Same output law as Algorithm R.** Only the use of random numbers differs, so a test can compare the two outputs in distribution.
- **Exact only in exact arithmetic.** SKIP-X uses products of reals and SKIP-Z uses $\ln$, $\exp$ and roots. In double precision the skip law is rounded, so the output is very close to uniform but not exactly uniform.
- **Randomized and not recursive.** It uses a constant number of variables besides the reservoir.

## Variants and improvements

- **Algorithm Y.** Vitter's paper also gives a method that searches for the skip faster than the linear walk of Algorithm X. Algorithm Z is the one that reaches the optimal bound.
- **Algorithm L.** Li (1994) draws the skip from a geometric law whose parameter is the largest of $k$ hidden keys. It needs no rejection and has the same order of expected time. See [Algorithm L](/algorithm-l/).
- **Known length.** When $n$ is known in advance, [selection sampling](/selection-sampling/) (Algorithm S) is the sequential method, and the same skip idea applies to it.
- **Weighted items.** The A-ExpJ method jumps over items with an exponential threshold. See [weighted reservoir sampling](/weighted-reservoir-sampling/).

## When to use it

Use a skip method when the stream is long compared with $k$ and either random numbers are costly or a skip is cheap, as in sampling rows of a large table or records of a file with random access. Algorithm Z is the classic method with the optimal bound. [Algorithm L](/algorithm-l/) gives the same bound with much shorter code, and is the easier choice for new code. For short streams, or when every item must be read anyway and random numbers are cheap, [Algorithm R](/reservoir-sampling/) is simpler and has no floating point.

## Pitfalls

- **Losing the state W.** SKIP-Z must keep $W$ between calls, and a quick accept must set $W = \mathit{rhs}/\mathit{lhs}$. If the old $W$ is used again, the next skips are not independent of the last one, and the sample is biased.
- **The switch.** Algorithm Z needs $t$ well above $k$: its envelope constant $c$ is large when $t$ is close to $k$, and $\mathit{term} = t - k + 1$ is small. Start with Algorithm X up to $t = Tk$.
- **ln(0).** A generator with values in $[0, 1)$ can return 0. Use $1 - \text{random}()$ for the logarithm in lines L2 and L19, and guard the root in line L15 when $U = 0$.
- **The product of line L18.** It must run from $t + S$ down over $k$ factors, or over the $S$ factors that do not cancel when $S < k$. An index off by one shifts $f$ and biases the sample.
- **The + 1 in line L7.** The accepted item itself is one position, so $t$ grows by $S + 1$.

## Implementations

## History

Jeffrey Scott Vitter published "Random sampling with a reservoir" in ACM Transactions on Mathematical Software in 1985. The paper names Algorithm R, which Knuth had given, and adds Algorithms X, Y and Z, which draw the skip instead of one decision per item. It also proves the lower bound $k(1 + H_n - H_k)$ on the expected number of reservoir insertions, so that Algorithm Z is optimal up to a constant factor. In 1994 Kim-Hung Li gave Algorithms K, L and M, which reach the same bound with simpler skip laws.

## References
