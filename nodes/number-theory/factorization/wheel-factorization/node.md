---
tag: SXCYK3
kind: algorithm
slug: wheel-factorization
name: Wheel factorization
aliases:
- wheel sieve
- wheel sieve trial division
area: number-theory/factorization
level: core
summary: Trial division that, after the first k primes, divides only by numbers coprime to W = 2 * 3 * ... * p_k, stepping through them with a fixed cycle of gaps. The wheel mod 30 tries 8 of every 30 numbers.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, W: the product of the wheel primes, k: the number of wheel primes}
  time: {worst: O(N^(1/2) φ(W) / W + k)}
  space: {extra: O(φ(W))}
  wheel_setup: {worst: O(W log W)}
  bit_operations: {worst: O(N^(1/2) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [trial-division, euler-totient, congruence]
see_also: [sieve-of-eratosthenes, smallest-prime-factor-table, primes-up-to-n, segmented-sieve, multiplicative-group-modulo-n, integer-factorization]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.1.2, Trial division, pages 118 to 119 (the 2, 4 wheel modulo 6, the wheel 4, 2, 4, 2, 4, 6, 2, 6 modulo 30, and the wheel of the primes below 30 with 1021870080 entries); Section 3.1.4, page 120 (the constant 1/2 replaced by a smaller one)
  - paper: "Paul Pritchard, Explaining the wheel sieve, Acta Informatica 17(4), 1982"
    locator: pages 477 to 485 (wheels as cyclic lists of the residues coprime to a primorial, and the wheel sieve for primes)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.4, Factoring into primes (Algorithm A and the trial divisor sequence 2, 3, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, ... that adds 2 and 4 in turn)
---

Wheel factorization is [trial division](/trial-division/) that skips most composite trial divisors. It first divides by the first $k$ [primes](/prime-number/) $p_1, \dots, p_k$, and then only by the numbers coprime to $W = p_1 p_2 \cdots p_k$, which repeat with period $W$ and so can be listed by a fixed cycle of additions, the wheel. With $W = 30$ the wheel is $4, 2, 4, 2, 4, 6, 2, 6$, and the method tries $8$ of every $30$ numbers instead of the $15$ odd ones. The gain shrinks fast as $k$ grows, because the fraction $\varphi(W)/W$ falls only like $1/\ln p_k$ while the wheel has $\varphi(W)$ entries.

## In plain words

Plain trial division wastes time on divisors such as $9$, $15$ or $25$, which can never divide what is left, because their prime factors are already removed.

A wheel removes many of them for free. After you divide out $2$, $3$ and $5$, every useful divisor leaves a remainder of $1$, $7$, $11$, $13$, $17$, $19$, $23$ or $29$ when divided by $30$. So the candidates go $7, 11, 13, 17, 19, 23, 29, 31$, then $37, 41, 43, \dots$: the same eight steps, $4, 2, 4, 2, 4, 6, 2, 6$, again and again, like a wheel rolling along the number line.

Some candidates are still composite, such as $49$, but they are rare, and they do no harm: they simply never divide.

## The problem

**Input.** An integer $N \ge 1$, and the wheel primes $p_1 < \cdots < p_k$, which are the first $k$ primes ($k \ge 0$).

**Output.** The prime factors of $N$ in non-decreasing order, with multiplicity. This is [integer factorization](/integer-factorization/).

**Cost model.** On the [word RAM](/word-ram/), with $N < 2^w$, one division and one addition cost $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, a division by a trial divisor below $N^{1/2}$ costs $O(n^2)$ bit operations with schoolbook division. The wheel itself is a table of $\varphi(W)$ small integers, built once.

## The algorithm

Let $W = p_1 \cdots p_k$, and let $s$ be the least integer above $1$ that is coprime to $W$ (so $s = p_{k+1}$). Let $r_0 = s < r_1 < \cdots < r_{\varphi(W) - 1}$ be the integers in $[s, s + W)$ that are coprime to $W$, where $\varphi$ is [Euler's totient](/euler-totient/). The gaps are $g_j = r_{j+1} - r_j$, and $g_{\varphi(W) - 1} = r_0 + W - r_{\varphi(W) - 1}$ wraps around.

```pseudo id=main
WHEEL-FACTOR(N, p_1, …, p_k)              ▷ N ≥ 1; the gaps g_0, …, g_{φ(W)−1} are precomputed
L1  F ← empty list, m ← N
L2  for each wheel prime p = p_1, …, p_k do
L3      while p divides m do append p to F, m ← m / p
L4  d ← s, i ← 0
L5  while d · d ≤ m do
L6      while d divides m do append d to F, m ← m / d
L7      d ← d + g_i, i ← (i + 1) mod φ(W)
L8  if m > 1 then append m to F
L9  return F
```

Lines L2 and L3 remove the wheel primes. The loop of lines L5 to L7 is the loop of [trial division](/trial-division/), with the step $d \leftarrow d + 2$ replaced by the next gap of the wheel. The wheel lists exactly the integers $d \ge s$ with $\gcd(d, W) = 1$, in increasing order, because $\gcd(d, W)$ depends only on $d \bmod W$. With $k = 0$ the wheel is the single gap $1$ from $s = 2$, and with $k = 1$ it is the gap $2$ from $s = 3$, which is the usual trial division by $2$ and the odd numbers.

**Some wheels.**

| wheel primes | $W$ | $s$ | gaps | $\varphi(W)/W$ |
|---|---|---|---|---|
| 2 | 2 | 3 | 2 | 0.500 |
| 2, 3 | 6 | 5 | 2, 4 | 0.333 |
| 2, 3, 5 | 30 | 7 | 4, 2, 4, 2, 4, 6, 2, 6 | 0.267 |
| 2, 3, 5, 7 | 210 | 11 | 48 gaps | 0.229 |
| 2, 3, 5, 7, 11 | 2310 | 13 | 480 gaps | 0.208 |

## Example

Factor $N = 8633$ with the wheel modulo $30$. Lines L2 and L3 try $2$, $3$ and $5$; none divides. Line L4 sets $d = 7$, and the loop tries the candidates of three turns of the wheel.

| turn | candidates $d$ | divides $8633$? |
|---|---|---|
| 1 | 7, 11, 13, 17, 19, 23, 29, 31 | no |
| 2 | 37, 41, 43, 47, 49, 53, 59, 61 | no |
| 3 | 67, 71, 73, 77, 79, 83, 89 | yes at $d = 89$: $m \leftarrow 97$ |

After the division, line L6 tests $89$ again ($89 \nmid 97$), line L7 moves to $d = 97$, and $97^2 > 97$ ends the loop. Line L8 appends $97$, so $8633 = 89 \cdot 97$. The method made $3 + 23 = 26$ trial divisions. Trial division by $2$ and the odd numbers needs $1 + 44 = 45$ divisions to reach $89$. The candidates $49$ and $77$ are composite; they cost a division each and do not divide.

## Correctness

The proof uses the invariant of line L5: $N = (\prod F) \cdot m$, the entries of $F$ are primes in non-decreasing order, all less than $d$, and $m$ has no prime factor less than $d$. After lines L2 and L3, $m$ has no wheel prime as a factor. A prime $q < d$ that is not a wheel prime is coprime to $W$ and at least $s$, so the wheel listed it and line L6 removed it. When $d$ divides $m$, each prime factor of $d$ divides $m$ and so is at least $d$; hence $d$ is prime. When the loop stops, $d^2 > m$, so $m$ is $1$ or a prime. The full proof is below.

## Complexity

- **Divisions.** On a prime $N$ the loop runs over the integers up to $\sqrt N$ that are coprime to $W$, about $\sqrt N \cdot \varphi(W)/W$ of them, plus $k$ divisions by the wheel primes. As in trial division, the loop on a composite $N$ stops near $\max(P, \sqrt Q)$, where $Q$ and $P$ are the largest and second largest prime factors.
- **Time.** $O(N^{1/2} \varphi(W)/W + k)$ on the word RAM, after the set-up. Since $\varphi(W)/W = \prod_{i \le k}(1 - 1/p_i)$ is a constant for a fixed wheel, the bound is still $O(N^{1/2})$; the wheel changes only the constant, from $\frac12$ to $\frac{4}{15} \approx 0.267$ for $W = 30$.
- **Bit operations.** $O(N^{1/2} n^2)$ for an arbitrary-precision $N$, as for trial division.
- **Set-up and space.** The table of gaps has $\varphi(W)$ entries and can be built in $O(W \log W)$ time with one gcd per residue, or in $O(W)$ with a sieve. The space is $O(\varphi(W))$ small integers.

**Diminishing returns.** By Mertens' third theorem, $\prod_{p \le x}(1 - 1/p) \sim e^{-\gamma}/\ln x$, so the fraction of candidates falls only like $1/\ln p_k$, while the table size $\varphi(W)$ grows faster than exponentially in $k$. The wheel of the primes below $30$ has $1{,}021{,}870{,}080$ entries and still saves only about $52.6\%$ of the divisions of the $2, 4$ wheel (Crandall and Pomerance). In practice the wheels modulo $30$, $210$ or $2310$ are used.

## Properties

- **Deterministic and exact.** The output is the full factorization, and each factor is proved prime by the invariant.
- **The same results as trial division.** Only the number of useless divisions changes.
- **Branch-free stepping.** The gap table makes the next divisor one addition away, with no test for divisibility by the small primes.
- **Periodic structure.** The residues coprime to $W$ form the [multiplicative group modulo $W$](/multiplicative-group-modulo-n/), of order $\varphi(W)$, and they are symmetric: $r$ is coprime to $W$ exactly when $W - r$ is. So the gaps between the residues in $(0, W)$ read the same backward; for $W = 30$ the residues $1, 7, 11, 13, 17, 19, 23, 29$ have the gaps $6, 4, 2, 4, 2, 4, 6$.

## Variants and improvements

- **Primes only.** With a precomputed list of the primes up to $\sqrt N$, from a [sieve of Eratosthenes](/sieve-of-eratosthenes/), trial division needs about $2\sqrt N/\ln N$ divisions, fewer than any wheel. It costs memory and a sieve, and is better when many numbers of the same size are factored.
- **Wheel sieves.** The same wheel speeds up the sieve of Eratosthenes: the sieve array stores only the residues coprime to $W$, which saves memory by the factor $\varphi(W)/W$. Pritchard's wheel sieve rolls a growing wheel to list the primes up to $X$ with $O(X/\log \log X)$ additions.
- **A smallest prime factor table.** For many queries $N \le X$, a [smallest prime factor table](/smallest-prime-factor-table/), which can also be stored on a wheel, answers each query in $O(\log N)$ steps.
- **Wheels in other loops.** The same gaps step through candidate primes in [segmented sieves](/segmented-sieve/) and in the search for the next prime.

## When to use it

Use a wheel modulo $30$ or $210$ whenever you write trial division by hand: it costs a table of $8$ or $48$ small numbers and saves about $47\%$ or $54\%$ of the divisions of the odd-number loop. For more savings, a table of primes is better than a larger wheel. For large $N$, the size of the largest factor matters more than the constant: switch to [Pollard's rho](/pollard-rho/) or the [elliptic curve method](/elliptic-curve-factorization/).

## Pitfalls

- **Forgetting the wheel primes.** The wheel never lists $2$, $3$ or $5$. Without lines L2 and L3, the factors $2$, $3$ and $5$ of $N$ are lost, and the output for $N = 12$ would be $[12]$.
- **The wrong start.** The wheel must start at $s = p_{k+1}$, the first residue coprime to $W$ above $1$. Starting at $1$ makes line L6 loop forever, because $1$ divides every $m$.
- **A basis that is not the first $k$ primes.** With the basis $(2, 5)$, the wheel starts at $s = 3$, below the wheel prime $5$, so for $N = 15$ the output is $[5, 3]$, out of order. The product is still right, but code that expects sorted factors breaks. Use the first $k$ primes.
- **Too large a wheel.** A wheel of the primes up to $23$ has $36{,}495{,}360$ entries and does not fit in a cache. The time to build and read it outweighs the saved divisions.
- **A wrong last gap.** The last gap wraps around the period: for $W = 30$ it is $37 - 31 = 6$, from the last residue back to the first of the next turn. An off-by-one here skips a prime in every turn.

## Implementations

## History

Stepping by $2$ and $4$ to skip the multiples of $2$ and $3$ is old practice in hand computation, and Knuth's Algorithm A uses that sequence of trial divisors. Paul Pritchard studied wheels systematically around 1980 and used growing wheels for sublinear sieves that list the primes; his 1982 paper "Explaining the wheel sieve" gave the name. Crandall and Pomerance describe the wheel modulo $30$ and show by the wheel of the primes below $30$ how fast the returns fall.

## References
