---
tag: N47W7S
kind: algorithm
slug: lemire-bounded-integers
name: Lemire's nearly divisionless bounded integers
aliases:
- Lemire's method
- multiply-shift range reduction with rejection
area: numerical/random-number-generation
level: advanced
summary: Maps a random w-bit word to an exactly uniform integer in [0, s) with one multiplication, taking the high half of x s and rejecting rare words, with a division only when the low half is below s.
model: word-ram
complexity:
  vars: {n: the number of outputs, s: the range size, w: the word size}
  time: {expected: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 2019
  people: [Daniel Lemire]
  note: Lemire published the method in ACM Transactions on Modeling and Computer Simulation, with benchmarks against the division-based methods then used in standard libraries.
prereqs: [modulo-bias, rejection-sampling, word-ram]
see_also: [uniform-random-integer-generation, fisher-yates-shuffle, multiply-shift-hashing, integer-division, pcg-random, xoshiro-xoroshiro, granlund-montgomery-division]
sources:
  - paper: doi:10.1145/3230636
    title: Daniel Lemire, Fast random integer generation in an interval, ACM Transactions on Modeling and Computer Simulation 29(1), 2019
    locator: Algorithm 5 (the nearly divisionless method), Lemma 4.1 and its proof of exact uniformity, and the benchmarks against the OpenBSD and Java methods
  - url: https://www.pcg-random.org/posts/bounded-rands.html
    title: Melissa E. O'Neill, Efficiently generating a number in a range, 2018
    locator: the comparison of range reduction methods, including the debiased integer multiplication method
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.1, Numerical distributions, part A (random integers in a range and the bias of taking remainders)
---

Lemire's method turns a uniformly random $w$-bit word into an exactly uniform integer in $[0, s)$ for any $1 \le s \le 2^w$. It multiplies the word by $s$ and keeps the high $w$ bits of the $2w$-bit product, which is a fast and almost uniform map; to make it exactly uniform it rejects the few words whose low half falls below $2^w \bmod s$. The remainder $2^w \bmod s$, which costs a division, is computed only when the low half is below $s$, which happens with probability at most $s / 2^w$, so for small ranges the method almost never divides. It is the standard way to draw [uniform random integers](/uniform-random-integer-generation/) in libraries that care about speed.

## In plain words

You have a random whole number from a huge range and you want one from a small range, say a die roll. Taking the remainder after division is slow, because division is slow on computers, and slightly unfair, because the huge range does not split into equal parts ([modulo bias](/modulo-bias/)).

This method instead multiplies the random number by the size of the small range and keeps the top half of the result, which is like scaling a fraction. That is fast and nearly fair. To make it exactly fair, it throws away a handful of starting numbers that would give some answers one extra chance. Deciding which ones to throw away needs a division, but a quick check shows that for almost every draw no starting number is in danger, so the division is skipped.

## The problem

Given a source of independent uniform $w$-bit words $x \in \{0, \ldots, 2^w - 1\}$ (the output $g(s_i)$ of a generator, $s_{i+1} = f(s_i)$) and a range size $s$ with $1 \le s \le 2^w$, produce $r$ with $\Pr[r = v] = 1/s$ for each $v \in \{0, \ldots, s - 1\}$, independently across calls. The cost model counts word operations on a [word RAM](/word-ram/), with the full product of two words ($2w$ bits) as one operation and integer division as a far more expensive operation, often 20 to 90 cycles against 3 or 4 for a multiplication on current 64-bit processors.

The obvious $x \bmod s$ costs a division and is biased unless $s$ divides $2^w$. The scaled value $\lfloor x s / 2^w \rfloor$ costs a multiplication but has the same bias: each output arises from $\lfloor 2^w / s \rfloor$ or $\lceil 2^w / s \rceil$ words.

## The algorithm

```pseudo id=main
BOUNDED(s)                         ▷ 1 ≤ s ≤ 2^w; RANDOM() returns a uniform w-bit word
L1  x ← RANDOM()
L2  m ← x · s                       ▷ the full 2w-bit product
L3  l ← m mod 2^w                   ▷ the low half
L4  if l < s then                   ▷ only now can x be one of the rejected words
L5      t ← (2^w − s) mod s         ▷ equals 2^w mod s, computed in w-bit arithmetic
L6      while l < t
L7          x ← RANDOM(); m ← x · s; l ← m mod 2^w
L8  return ⌊m / 2^w⌋                ▷ the high half
```

The rejected words are exactly those with $x s \bmod 2^w < t$, where $t = 2^w \bmod s$; there are $t$ of them. Since $t < s$, a word with $l \ge s$ is certainly accepted, which is why the test at L4 skips the division. In C, $(2^w - s) \bmod s$ is written `(-s) % s` on unsigned $w$-bit integers, and the high and low halves come from one widening multiplication (`__uint128_t` for $w = 64$, or a `mulhi` instruction).

## Example

Take $w = 8$ and $s = 6$, so $t = 256 \bmod 6 = 4$ and $\lfloor 256 / 6 \rfloor = 42$.

| $x$ | $m = 6x$ | $l = m \bmod 256$ | action | output $\lfloor m / 256 \rfloor$ |
|---|---|---|---|---|
| 200 | 1200 | 176 | $l \ge s$: accept, no division | 4 |
| 42 | 252 | 252 | $l \ge s$: accept | 0 |
| 43 | 258 | 2 | $l < s$: compute $t = 4$; $2 < 4$: reject | |
| 0 | 0 | 0 | $0 < 4$: reject | |
| 85 | 510 | 254 | $254 \ge 4$: accept | 1 |

Over all 256 words, exactly four are rejected, $x \in \{0, 43, 128, 171\}$ (the first word of each of four groups that would otherwise be one too large), and each output $0, \ldots, 5$ comes from exactly 42 accepted words, so the result is exactly uniform. Only 6 of the 256 words have $l < 6$ and so need the division; the other 250 cost one multiplication.

At $w = 32$, the range $s = 3 \cdot 2^{30}$ is a bad case: $t = 2^{32} \bmod s = 2^{30}$, a quarter of all words are rejected, and the expected number of words per output is $4/3$. A simulation with 20000 outputs averages within 0.03 of that.

## Correctness

**Uniformity.** Fix $v \in \{0, \ldots, s - 1\}$. A word $x$ is accepted with output $v$ if and only if $v 2^w + t \le x s < (v + 1) 2^w$: the high half is $v$ and the low half $x s - v 2^w$ is at least $t$. The interval $[v 2^w + t, (v+1) 2^w)$ has length $2^w - t = s \lfloor 2^w / s \rfloor$, a multiple of $s$, so it contains exactly $\lfloor 2^w / s \rfloor$ multiples of $s$, that is, exactly that many words $x$. The count does not depend on $v$, so conditioned on acceptance the output is uniform; the loop repeats with fresh independent words until acceptance, so the returned value is uniform. The total number of rejected words is $2^w - s \lfloor 2^w / s \rfloor = t$.

**Skipping the division.** A word with $l \ge s$ has $l \ge s > t$, so it is accepted whatever $t$ is. The first word is the only one examined without knowing $t$, and the loop at L6 compares every later word with the true $t$. The proof page gives the details.

## Complexity

Each attempt accepts with probability $1 - t / 2^w \ge 1 - (s-1)/2^w$, which is more than $1/2$ for every $s \le 2^w$, so the number of words drawn is geometric with mean $2^w / (2^w - t) < 2$, and $n$ outputs cost $\Theta(n)$ expected word operations. The probability that a call computes the division is exactly $\Pr[l < s] = s / 2^w$: with $g = \gcd(s, 2^w)$, the map $x \mapsto x s \bmod 2^w$ hits each multiple of $g$ exactly $g$ times, and $s/g$ multiples of $g$ lie below $s$. For 64-bit words and $s$ below $2^{32}$ that is below $2^{-32}$. Space is constant.

## Properties

- Exactly uniform for every $s$ in $[1, 2^w]$, assuming uniform independent input words. This is a proved property, verified by enumeration for all $s$ and all $w \le 8$.
- One multiplication per output in the common case, no division, at most one division per output.
- Uses the high bits of the input word, which are the best bits of LCGs and of many other generators; $x \bmod s$ uses the low bits, which are the worst bits of LCGs with power-of-two modulus.
- Monotone in $x$ among accepted words: larger words give larger or equal outputs, which helps when inverting or testing.
- For $s$ a power of two, $t = 0$, nothing is rejected, and the output is the top $\log_2 s$ bits of $x$.

## Variants and improvements

- **Division method (OpenBSD arc4random_uniform).** Reject $x < (2^w - s) \bmod s$ and return $x \bmod s$; also exact, but always one division and one remainder.
- **Java's method.** Compute $r = x \bmod s$ and reject when $x - r + (s - 1)$ overflows; one remainder per attempt, no precomputed threshold.
- **Bitmask with rejection.** Mask $x$ to the smallest $2^b \ge s$ and reject values $\ge s$; no multiplication or division, but up to half the words are rejected. O'Neill (2018) compares these methods.
- **Precomputed threshold.** When many values with the same $s$ are needed, as in sampling with a fixed range, compute $t$ once and drop the test at L4.
- **Batched and shuffling variants.** Fisher-Yates shuffles use a different $s$ at each step; later work by Brackett-Rozinsky and Lemire draws several bounded integers from one word to save random bits and multiplications.
- **Without rejection.** The bare multiply-high step $\lfloor x s / 2^w \rfloor$ maps a hash value to a table index of size $s$ in hash tables ([multiply-shift hashing](/multiply-shift-hashing/)), where exact uniformity is not needed.

## When to use it

Use it whenever a uniform integer in a range is needed from a fast generator: dice, random indices, [Fisher-Yates shuffles](/fisher-yates-shuffle/), random sampling, randomized algorithms. It is the method of choice when the range changes from call to call, since there is no setup. For cryptographic uses the same method works on the output of a [CSPRNG](/cryptographically-secure-prng/); its running time depends on the random word only through the rejection, which leaks nothing about the accepted output.

## Pitfalls

- **Dropping the rejection.** $\lfloor x s / 2^w \rfloor$ alone is biased by up to $1/\lfloor 2^w / s \rfloor$ in relative terms; this is harmless for $s \ll 2^w$ in simulations, but not for cryptography or exact tests.
- **Wrong threshold.** The threshold is $2^w \bmod s$, not $s$ and not $2^w - s$; `(-s) % s` in unsigned arithmetic computes it, `-s % s` on signed integers does not.
- **Truncating the product.** The method needs the full $2w$-bit product. Languages without a widening multiply must split the words or use a smaller $w$; on 32-bit words with 64-bit products it is straightforward.
- **Range zero.** $s = 0$ has no valid output; check it before the call. $s = 2^w$ does not fit in a $w$-bit variable and needs a special case (return $x$).
- **Low-quality input words.** Exactness assumes uniform input. A generator with weak high bits, which is rare, would pass its weakness on.

## Implementations

## History

Taking the high half of $x \cdot s$ as a cheap substitute for $x \bmod s$ is old and appears in hashing and in scaling floating-point values. Lemire (2019) added the rejection step with the observation that the threshold $2^w \bmod s$ is needed only when the low half is below $s$, proved that the result is exactly uniform, and showed speedups over the division-based methods of OpenBSD and Java. The method was adopted in several language runtimes and libraries shortly after.

## References
