---
tag: FACB98
kind: definition
slug: modulo-bias
name: Modulo bias
aliases:
- modulo reduction bias
area: numerical/random-number-generation
level: intro
summary: The non-uniform distribution of W mod n when W is uniform on M values and n does not divide M.
prereqs: [congruence, uniform-distribution]
see_also: [uniform-random-integer-generation, lemire-bounded-integers, rejection-sampling, fisher-yates-shuffle, unbiased-bits-from-biased-coin, linear-congruential-generator]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.1, part A (random integers in a range, and why multiplication is preferred to the remainder for a linear congruential generator)
  - paper: doi:10.1145/3230636
    title: Daniel Lemire, Fast random integer generation in an interval, ACM Transactions on Modeling and Computer Simulation 29(1), 2019, Article 3
    locator: Section 2 (the bias of the modulo reduction and of the multiply-shift reduction, and the rejection fix)
  - url: https://www.pcg-random.org/posts/bounded-rands.html
    title: Melissa E. O'Neill, Efficiently generating a number in a range, 2018
    locator: the sections on the biased modulo method and the debiased methods
---

Modulo bias is the error made when a program reduces a uniform random word modulo a range size that does not divide the number of possible words. Some remainders then have one more preimage than others, so they come out more often. The bias is small when the range is much smaller than the word range, but it is never zero, and it is large when the range is a sizable fraction of the word range. Exact methods remove it by [rejection sampling](/rejection-sampling/).

## Definition

Let $W$ be [uniform](/uniform-distribution/) on $\{0, 1, \ldots, M - 1\}$, for example $M = 2^w$ for a random $w$-bit word, and let $n$ be an integer with $1 \le n \le M$. Write $M = qn + r$ with $q = \lfloor M / n \rfloor \ge 1$ and $0 \le r < n$. The reduction $X = W \bmod n$ has the distribution

$$\Pr[X = k] = \begin{cases} (q + 1)/M & \text{if } 0 \le k < r, \\ q/M & \text{if } r \le k < n. \end{cases}$$

This holds because the values $w < M$ with $w \equiv k \pmod n$ are $k, k + n, \ldots$, and there are $q + 1$ of them when $k < r$ and $q$ of them when $k \ge r$. *Modulo bias* is the difference between this distribution and the uniform distribution on $\{0, \ldots, n - 1\}$. It is zero exactly when $r = 0$, that is, when $n \mid M$.

**Size of the bias.** The ratio of the largest to the smallest probability is $(q+1)/q$ when $r > 0$. The total variation distance to uniform is

$$\delta(M, n) = \frac{1}{2} \sum_{k=0}^{n-1} \left| \Pr[X = k] - \frac{1}{n} \right| = \frac{r (n - r)}{n M} \le \frac{n}{4M}.$$

Proof: for $k < r$, $(q+1)/M - 1/n = (n - r)/(nM)$, and for $k \ge r$, $1/n - q/M = r/(nM)$. There are $r$ terms of the first kind and $n - r$ of the second, so the sum is $2 r (n - r) / (nM)$. The bound follows from $r(n - r) \le n^2/4$.

**No fixed-cost map is exact.** The remainder is not the only culprit. Let $h$ be any function from $\{0, \ldots, M - 1\}$ to $\{0, \ldots, n - 1\}$. Then $\Pr[h(W) = k] = |h^{-1}(k)| / M$, and this equals $1/n$ for each $k$ only if $M / n$ is an integer. So when $n \nmid M$, every method that uses one word and a fixed map is biased, including $\lfloor n W / M \rfloor$ (multiply and shift) and $\lfloor n U \rfloor$ for a floating-point $U$ with $2^{53}$ possible values. Further, if an exact method uses at most $t$ words in every run, then each output probability is a multiple of $M^{-t}$; with $M = 2^w$ this forces $n \mid 2^{wt}$, so $n$ is a power of two. Hence for any other $n$, an exact method has no bound on the number of words in its worst case. Rejection gives such a method with a small expected cost.

**The rejection fix.** Draw $W$. If $W \ge qn$, draw again. Otherwise return $W \bmod n$. Each accepted value $k$ has exactly $q$ preimages in $\{0, \ldots, qn - 1\}$, so the output is exactly uniform. The acceptance rate is $qn / M > 1/2$, because $qn > M - n \ge M - qn$. So the expected number of words is $M / (qn) < 2$, and it is close to 1 when $n \ll M$.

## Examples and non-examples

**A 3-bit word and a die with three faces.** $M = 8$ and $n = 3$ give $q = 2$ and $r = 2$. The values 0 and 1 have probability $3/8$ each, and 2 has $1/4$. The total variation distance is $\delta = 2 \cdot 1 / (3 \cdot 8) = 1/12$. Multiply and shift, $\lfloor 3W/8 \rfloor$, gives the counts $3, 3, 2$ for the values 0, 1, 2: the same bias in a different place.

**A byte and a six-sided die.** $M = 256$ and $n = 6$ give $256 = 42 \cdot 6 + 4$. The faces 0 to 3 have probability $43/256$ and the faces 4 and 5 have $42/256$, and $\delta = 4 \cdot 2 / (6 \cdot 256) = 1/192$. The rejection fix rejects the bytes 252 to 255.

**A byte and a percentage.** $M = 256$ and $n = 100$ give $256 = 2 \cdot 100 + 56$. The values 0 to 55 have probability $3/256$ and the values 56 to 99 have $2/256$, so a small value is 1.5 times as likely as a large one.

**A large range.** $M = 2^{32}$ and $n = 3 \cdot 2^{30}$ give $q = 1$ and $r = 2^{30}$. The values below $2^{30}$ come out with probability $2^{-31}$, twice the probability $2^{-32}$ of the others, and $\delta = 1/6$. The rejection fix accepts with probability $3/4$, so it uses $4/3$ words on average.

**Non-example: a power of two.** With $M = 2^{32}$ and $n = 2^{10}$, $n$ divides $M$ and $W \bmod n$ is exactly uniform. (If the words come from a [linear congruential generator](/linear-congruential-generator/) modulo $2^w$, the low bits have short periods, so the remainder has no bias but takes the worst bits of the word. That is a separate defect.)

**Non-example: a range of size 1.** For $n = 1$, every method returns 0, and there is no bias.

**Non-example: the correct library calls.** Python's `random.randrange(n)` draws an integer with `getrandbits(k)`, where $k$ is the bit length of $n$, and rejects values of $n$ or more. Java's `Random.nextInt(bound)` rejects a draw when it falls in the last incomplete block. Both are exact if the underlying bits are uniform.

## Related definitions

- **The problem.** [Uniform random integer generation](/uniform-random-integer-generation/) asks for an exact uniform integer in a range from uniform words, with few words and few divisions.
- **Lemire's method.** [Lemire's nearly divisionless method](/lemire-bounded-integers/) uses the multiply-high reduction $\lfloor nW/2^w \rfloor$ and rejects in a way that avoids a division in most calls.
- **Biased shuffles.** A [Fisher-Yates shuffle](/fisher-yates-shuffle/) that picks its swap index with a biased reduction gives a non-uniform permutation, even when the shuffle loop is correct.
- **Biased bits.** The reverse problem, making exact uniform bits from a biased source, is [unbiased bits from a biased coin](/unbiased-bits-from-biased-coin/).

## References
