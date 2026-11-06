---
tag: Y2XXPK
kind: concept
slug: prime-gaps
name: Prime gaps
aliases:
- maximal prime gap
area: number-theory/primality
level: advanced
summary: The gap after the prime p_n is p_(n+1) - p_n. Gaps near x are about ln x on average, can be arbitrarily large, are at most x^0.525 for large x, and are at most 246 infinitely often.
prereqs: [prime-number, prime-number-theorem]
see_also: [bertrands-postulate, prime-number-theorem, random-prime-generation, segmented-sieve, sieve-of-eratosthenes, aks-primality-test, primality-testing, prime-counting-function]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 1.4.1 (the discussion of p_(n+1) - p_n after relation (1.25), with the Cramer and Granville conjectures and the values for 113, 1327 and 1693182318746371), Section 1.2.1 (twin primes) and Section 1.1.5
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Exercise 1.28 (arbitrarily large gaps), Section 5.2 (Theorem 5.8, Bertrand's postulate) and Exercise 5.22
  - paper: doi:10.1112/plms/83.3.532
    title: R. C. Baker, G. Harman and J. Pintz, The difference between consecutive primes, II, Proceedings of the London Mathematical Society 83 (2001)
    locator: pages 532 to 562
  - paper: doi:10.4007/annals.2014.179.3.7
    title: Yitang Zhang, Bounded gaps between primes, Annals of Mathematics 179 (2014)
    locator: pages 1121 to 1174
  - paper: doi:10.4007/annals.2015.181.1.7
    title: James Maynard, Small gaps between primes, Annals of Mathematics 181 (2015)
    locator: pages 383 to 413
  - paper: doi:10.1186/s40687-014-0012-7
    title: D. H. J. Polymath, Variants of the Selberg sieve, and bounded intervals containing many primes, Research in the Mathematical Sciences 1 (2014)
    locator: article 12
  - paper: doi:10.1090/jams/876
    title: Kevin Ford, Ben Green, Sergei Konyagin, James Maynard and Terence Tao, Long gaps between primes, Journal of the American Mathematical Society 31 (2018)
    locator: pages 65 to 105
  - paper: doi:10.4064/aa-2-1-23-46
    title: Harald Cramer, On the order of magnitude of the difference between consecutive prime numbers, Acta Arithmetica 2 (1936)
    locator: pages 23 to 46
  - paper: doi:10.1090/S0025-5718-2013-02787-1
    title: Tomas Oliveira e Silva, Siegfried Herzog and Silvio Pardi, Empirical verification of the even Goldbach conjecture and computation of prime gaps up to 4 x 10^18, Mathematics of Computation 83 (2014)
    locator: pages 2033 to 2060
---

A prime gap is the difference $g_n = p_{n+1} - p_n$ between the $n$th [prime](/prime-number/) $p_n$ and the next one. By the [prime number theorem](/prime-number-theorem/) the gaps near $x$ are $\ln x$ on average, but single gaps vary a lot: there are gaps of every even length that has been searched, gaps as large as one wants, and, as proved in 2013, gaps of bounded size infinitely often. A *maximal gap* is a gap larger than every earlier gap. For algorithms, gaps bound the cost of searching upward from a number to the next prime.

## In plain words

List the primes in order and look at the distance from each one to the next: 1, 2, 2, 4, 2, 4, 2, 4, 6, and so on. These distances are the prime gaps. On average they grow slowly, like the number of digits of the primes, so near a billion a typical gap is about 20. But they are irregular. Two primes can be only 2 apart even among very large numbers, and long runs with no prime at all also exist, as long as one likes. Mathematicians know good bounds on how long these runs can be, but not the best ones. When a program looks for a prime by testing one number after another, the gaps decide how long it searches.

## The idea

**Definitions.** Let $p_1 = 2 < p_2 = 3 < \cdots$ be the primes and $g_n = p_{n+1} - p_n$. Apart from $g_1 = 1$, every gap is even. Define $G(x) = \max\{g_n : p_{n+1} \le x\}$, the largest gap up to $x$. A gap $g_n$ is *maximal* (a record) if $g_n > g_m$ for all $m < n$. The *merit* of a gap is $g_n / \ln p_n$, its size in units of the average gap.

**Average size.** Summing gaps telescopes: $\sum_{p_n \le x} g_n = p_{\pi(x) + 1} - 2$, so the mean gap below $x$ is about $x/\pi(x) \sim \ln x$ by the prime number theorem (Crandall and Pomerance, Section 1.4.1). Averaged over windows, the same holds locally: for each fixed $\epsilon > 0$ the interval $(x, (1 + \epsilon)x]$ has $\sim \epsilon x/\ln x$ primes (Shoup, Exercise 5.22).

**Large gaps exist.** For $k \ge 1$, the $k$ numbers $(k + 1)! + j$, $2 \le j \le k + 1$, are all composite, because $j$ divides $(k + 1)! + j$ (Shoup, Exercise 1.28). So some gap is at least $k + 1$, for every $k$. The construction is far from the truth: the first run of 6 composites starts at 90, not at $7! + 2 = 5042$.

**Upper bounds on gaps.** Each statement holds for all large $n$.

- Bertrand's postulate: $g_n < p_n$, since there is a prime between $p_n$ and $2 p_n$ (Shoup, Theorem 5.8; see [Bertrand's postulate](/bertrands-postulate/)).
- From the prime number theorem: $g_n = o(p_n)$.
- Baker, Harman and Pintz (2001): $g_n = O(p_n^{0.525})$, the best unconditional bound (Crandall and Pomerance, Section 1.4.1).
- Under the Riemann hypothesis: $g_n = O(p_n^{1/2 + \epsilon})$ for every fixed $\epsilon > 0$ (Crandall and Pomerance, Section 1.4.1), and Cramer sharpened this to $O(p_n^{1/2} \ln p_n)$. This is a conditional result.

**Conjectures on the largest gaps.** Cramer (1936) modelled the primes as random, with each $m$ prime with probability $1/\ln m$, and conjectured $\limsup g_n / \ln^2 p_n = 1$. Granville argued that the true value is at least $2 e^{-\gamma} \approx 1.1229$, where $\gamma$ is Euler's constant (Crandall and Pomerance, Section 1.4.1). Either way the largest gaps up to $x$ would be of order $\ln^2 x$, far below the proven $x^{0.525}$.

**Lower bounds on the largest gaps.** Erdos and Rankin proved that $g_n \ge c \ln p_n \ln \ln p_n \ln \ln \ln \ln p_n / (\ln \ln \ln p_n)^2$ infinitely often (Crandall and Pomerance, Section 1.4.1). Ford, Green, Konyagin, Maynard and Tao (2018) removed one factor $\ln \ln \ln p_n$ from the denominator and showed $G(x) \gg \ln x \ln \ln x \ln \ln \ln \ln x / \ln \ln \ln x$ for large $x$. The gap between this and the conjectured $\ln^2 x$ is wide.

**Small gaps.** The twin prime conjecture says $g_n = 2$ infinitely often; it is open. Goldston, Pintz and Yildirim proved $\liminf g_n / \ln p_n = 0$ (Crandall and Pomerance, Section 1.4.1). Zhang (2014) proved the first bounded gap result, $\liminf g_n < 7 \cdot 10^7$. Maynard (2015) gave a simpler method with $\liminf g_n \le 600$, and also bounded gaps between $m$ primes for every $m$. The Polymath project (2014) brought the bound down to $\liminf g_n \le 246$, and to $6$ under the generalized Elliott-Halberstam conjecture, a conditional result.

**Computing maximal gaps.** All gaps up to $x$ come from one pass of a [segmented sieve](/segmented-sieve/) that keeps the last prime seen and the largest difference. This takes $O(x \log \log x)$ operations and $O(\sqrt x)$ memory. The largest such search, by Oliveira e Silva, Herzog and Pardi, went to $4 \cdot 10^{18}$. To confirm one known gap, it is enough to test the two end points and every number between them for primality.

## Examples

**The first gaps.** The primes $2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31$ give the gaps $1, 2, 2, 4, 2, 4, 2, 4, 6, 2$.

**Maximal gaps below $10^8$.** A sieve up to $10^8$ gives the records below; for each, $p$ is the prime before the gap and $n$ its index. The last two columns are the merit and the ratio $g/\ln^2 p$ of Cramer's conjecture.

| $g$ | $p$ | $n$ | $g / \ln p$ | $g / \ln^2 p$ |
|---|---|---|---|---|
| 1 | 2 | 1 | 1.443 | 2.081 |
| 2 | 3 | 2 | 1.820 | 1.657 |
| 4 | 7 | 4 | 2.056 | 1.056 |
| 6 | 23 | 9 | 1.914 | 0.610 |
| 8 | 89 | 24 | 1.782 | 0.397 |
| 14 | 113 | 30 | 2.961 | 0.626 |
| 18 | 523 | 99 | 2.876 | 0.459 |
| 20 | 887 | 154 | 2.946 | 0.434 |
| 22 | 1129 | 189 | 3.130 | 0.445 |
| 34 | 1327 | 217 | 4.728 | 0.658 |
| 36 | 9551 | 1183 | 3.928 | 0.429 |
| 44 | 15683 | 1831 | 4.555 | 0.472 |
| 52 | 19609 | 2225 | 5.261 | 0.532 |
| 72 | 31397 | 3385 | 6.954 | 0.672 |
| 86 | 155921 | 14357 | 7.192 | 0.602 |
| 96 | 360653 | 30802 | 7.503 | 0.586 |
| 112 | 370261 | 31545 | 8.735 | 0.681 |
| 114 | 492113 | 40933 | 8.698 | 0.664 |
| 118 | 1349533 | 103520 | 8.360 | 0.592 |
| 132 | 1357201 | 104071 | 9.348 | 0.662 |
| 148 | 2010733 | 149689 | 10.197 | 0.703 |
| 154 | 4652353 | 325852 | 10.031 | 0.653 |
| 180 | 17051707 | 1094421 | 10.810 | 0.649 |
| 210 | 20831323 | 1319945 | 12.461 | 0.740 |
| 220 | 47326693 | 2850174 | 12.449 | 0.704 |

Crandall and Pomerance quote the ratio with $\ln^2 n$, the index, in place of $\ln^2 p_n$; this gives the same limit superior but other values: $14/\ln^2 30 \approx 1.210$ at $p = 113$ and $34/\ln^2 217 \approx 1.175$ at $p = 1327$, which match their figures.

**Large known gaps.** Nyman found the gap of $1132$ after $p = 1693182318746371$ (Crandall and Pomerance, Section 1.4.1); its merit is $32.28$ and $g/\ln^2 p = 0.921$. The gap of $1476$ after $p = 1425172824437699411$ is the largest gap below $4 \cdot 10^{18}$ (Oliveira e Silva, Herzog and Pardi); its merit is $35.31$ and $g/\ln^2 p = 0.845$. For both, a script with the Miller-Rabin test on the 12 prime bases up to 37, which is deterministic below $2^{64}$, confirmed that the two ends are prime and that every number between them is composite. That they are records rests on the published searches.

**Average gaps.** The mean gap between the primes in $[99 \cdot 10^6, 10^8)$ is $18.41$, against $\ln(9.95 \cdot 10^7) = 18.42$. There are $8169$ twin prime pairs below $10^6$, and among the gaps between primes up to $10^6$ the length 6 is more common ($13549$ times) than 2 ($8169$) or 4 ($8143$). For a prime $p > 3$, $p + 6 \equiv p \pmod 3$, so 3 never rules out $p + 6$, while it rules out $p + 2$ when $p \equiv 1$ and $p + 4$ when $p \equiv 2 \pmod 3$.

**Bias of an upward search.** Choose a random odd start and return the first prime at or above it. Below $10^4$, the prime $1361$ follows the gap of 34 after $1327$, so 17 odd starts ($1329$ to $1361$) return it. The next prime $1367$ has only 3 odd starts ($1363$ to $1367$). So this search does not give a uniform prime: each prime is returned with probability proportional to the gap before it.

## Where it is used

- **Searching for the next prime.** Testing $x, x + 1, x + 2, \ldots$ with a [primality test](/primality-testing/) stops after $g$ steps, where $g$ is the distance to the next prime. From a random start the search tests a little under $\ln x$ integers on average: a script measured $15.6$ near $4 \cdot 10^7$, where $\ln x = 17.5$, and skipping even numbers halves this. So this is the usual way to produce a prime of a given size; see [random prime generation](/random-prime-generation/).
- **Deterministic construction of primes.** To find some prime with $\ell$ binary digits with no randomness, one can test $2^{\ell - 1}, 2^{\ell - 1} + 1, \ldots$ with the [AKS test](/aks-primality-test/). Bertrand's postulate guarantees a prime before $2^\ell$, and the bound of Baker, Harman and Pintz limits the search to $O(2^{0.525 \ell})$ candidates for large $\ell$; under the Riemann hypothesis $O(2^{\ell/2} \ell)$. If Cramer's conjecture holds, the search takes $O(\ell^2)$ candidates and is deterministic polynomial time; no unconditional polynomial bound is known.
- **Bias in key generation.** As in the example above, incremental search favours primes after long gaps. The bias is small for cryptographic sizes but makes the output distribution not uniform; a fresh random candidate at each step avoids it.
- **Choosing table sizes.** Hash tables and some data structures use a prime size near a target $m$; Bertrand's postulate and the average gap $\ln m$ say that one is always close.
- **Testing conjectures and sieves.** Tables of maximal gaps and of gap counts by a [sieve](/sieve-of-eratosthenes/) are a standard check of the random model of the primes and of the Hardy and Littlewood prime tuple conjectures.

## References
