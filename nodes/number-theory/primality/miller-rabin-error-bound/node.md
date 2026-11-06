---
tag: XV8E5A
kind: theorem
slug: miller-rabin-error-bound
name: Miller-Rabin error bound
aliases:
- Rabin's theorem on strong liars
- Monier-Rabin theorem
area: number-theory/primality
level: core
summary: For odd composite n > 9, at most φ(n)/4 of the bases are strong liars, so each round of Miller-Rabin accepts a composite with probability below 1/4.
prereqs: [strong-pseudoprime, chinese-remainder-theorem, primitive-roots-existence, cyclic-group]
see_also: [miller-rabin, strong-liar, strong-pseudoprime, compositeness-witness, nontrivial-square-root-of-one, error-amplification, deterministic-miller-rabin-bases, carmichael-number]
sources:
  - paper: doi:10.1016/0022-314X(80)90084-0
    title: Michael O. Rabin, Probabilistic algorithm for testing primality, Journal of Number Theory 12 (1980)
    locator: pages 128 to 138 (the bound of one quarter on the share of strong liars)
  - paper: doi:10.1016/0304-3975(80)90007-9
    title: Louis Monier, Evaluation and comparison of two efficient probabilistic primality testing algorithms, Theoretical Computer Science 12 (1980)
    locator: pages 97 to 108 (the exact count of strong liars and the bound φ(n)/4)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 3.5, Probable primes and witnesses (Theorem 3.5.4, the Monier-Rabin theorem)
  - paper: doi:10.1090/S0025-5718-1993-1189518-9
    title: Ivan Damgård, Peter Landrock and Carl Pomerance, Average case error estimates for the strong probable prime test, Mathematics of Computation 61 (1993)
    locator: pages 177 to 194
---

The Miller-Rabin error bound says that an odd composite $n > 9$ has at most $\varphi(n)/4$ [strong liars](/strong-liar/), the bases $a$ for which $n$ passes the strong probable prime test. So one round of the [Miller-Rabin test](/miller-rabin/) with a random base accepts a composite with probability less than $1/4$, and $k$ independent rounds with probability less than $4^{-k}$. Rabin and Monier proved it independently in 1980, and Monier gave the exact number of strong liars. The bound is attained, for example by $n = 15$ and $n = 91$.

## Statement

Let $n$ be odd, and write $n - 1 = 2^s d$ with $d$ odd. A base $a$ with $1 \le a \le n - 1$ is a **strong liar** for $n$ if

$$a^d \equiv 1 \pmod n \qquad \text{or} \qquad a^{2^j d} \equiv -1 \pmod n \ \text{ for some } 0 \le j < s.$$

Let $S(n)$ be the set of strong liars, and $\varphi$ [Euler's totient function](/euler-totient/).

**Theorem (Monier-Rabin).** If $n > 9$ is odd and composite, then $|S(n)| \le \varphi(n)/4$.

**Theorem (Monier's count).** Let $n = \prod_{i=1}^{r} p_i^{e_i}$ be odd and composite with distinct primes $p_i$, and let $\nu = \min_i v_2(p_i - 1)$, where $v_2(m)$ is the exponent of 2 in $m$. Then

$$|S(n)| = \left(1 + \sum_{j=0}^{\nu - 1} 2^{jr}\right) \prod_{i=1}^{r} \gcd(d, p_i - 1).$$

**Corollary (error per round).** If $a$ is uniform in $[2, n-2]$ and $n > 9$ is odd and composite, then $n$ passes the strong test with the base $a$ with probability $(|S(n)| - 2)/(n - 3) < 1/4$. With $k$ independent bases the probability is less than $4^{-k}$.

## In plain words

The Miller-Rabin test checks a number with a random helper. A prime always passes. A composite number sometimes passes too, when the helper happens to be a liar. This theorem says that at most one helper in four is a liar, whatever the composite number is. So a composite number survives one round with a chance below one in four, two rounds with a chance below one in sixteen, and so on.

The proof splits the composite number into its prime parts and counts, for each part, how many helpers behave like they would for a prime. The counts multiply. With three or more different prime parts the product is already small. With two parts, or one repeated part, a little more care shows the same bound.

## Proof

Let $n = \prod_{i=1}^{r} p_i^{e_i}$ be odd and composite, $n - 1 = 2^s d$ with $d$ odd, and $v_i = v_2(p_i - 1)$, $\nu = \min_i v_i$. Each strong liar is a unit modulo $n$, since $a^{n-1} \equiv 1$.

**Step 1: a count in a cyclic group.** Let $G$ be a cyclic group of order $N$ with generator $g$, and let $m \ge 1$. The equation $x^m = 1$ has exactly $\gcd(m, N)$ solutions. If $N$ is even, let $-1 = g^{N/2}$ be its unique element of order 2. Then $x^m = -1$ has a solution if and only if $v_2(m) < v_2(N)$, and then it has exactly $\gcd(m, N)$ solutions.

*Proof.* Write $x = g^t$ with $0 \le t < N$. Then $x^m = g^{tm}$, and $g^{tm} = 1$ if and only if $N \mid tm$, which has $\gcd(m, N)$ solutions $t$. Next $g^{tm} = g^{N/2}$ if and only if $tm \equiv N/2 \pmod N$. With $c = \gcd(m, N)$, this linear congruence is solvable if and only if $c \mid N/2$, and then it has $c$ solutions. Finally $c \mid N/2$ holds exactly when $v_2(c) \le v_2(N) - 1$, and $v_2(c) = \min(v_2(m), v_2(N))$, so the condition is $v_2(m) < v_2(N)$. $\square$

**Step 2: Monier's count.** For each $i$, the group $(\mathbb{Z}/p_i^{e_i}\mathbb{Z})^*$ is cyclic of order $N_i = p_i^{e_i - 1}(p_i - 1)$ ([existence of primitive roots](/primitive-roots-existence/)), and $v_2(N_i) = v_i$. For $m \mid n - 1$, $p_i \nmid m$, so $\gcd(m, N_i) = \gcd(m, p_i - 1)$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), a congruence $a^m \equiv \pm 1 \pmod n$ holds if and only if it holds modulo each $p_i^{e_i}$, so the counts multiply.

- The number of $a$ with $a^d \equiv 1 \pmod n$ is $\prod_i \gcd(d, p_i - 1)$.
- Let $0 \le j < s$ and $m = 2^j d$, so $v_2(m) = j$. If $j < \nu$, then $j < v_i$ for each $i$, so by Step 1 the number of $a$ with $a^{m} \equiv -1 \pmod n$ is $\prod_i \gcd(2^j d, p_i - 1) = \prod_i 2^j \gcd(d, p_i - 1) = 2^{jr} \prod_i \gcd(d, p_i - 1)$. If $j \ge \nu$, then $j \ge v_i$ for some $i$, and there is no solution modulo $p_i^{e_i}$, so none modulo $n$.

Each $p_i \equiv 1 \pmod{2^\nu}$, so $n \equiv 1 \pmod{2^\nu}$ and $\nu \le s$. The cases in the definition of a strong liar are disjoint. If $a^{2^j d} \equiv -1$, then $a^{2^{j'} d} \equiv 1 \not\equiv -1$ for every $j' > j$. If $a^d \equiv 1$, then $a^{2^j d} \equiv 1 \not\equiv -1$ for every $j$. Summing the counts over the disjoint cases gives the formula.

**Step 3: the general estimate.** Let $T = \prod_i \gcd(d, p_i - 1)$. Since $d$ is odd, $\gcd(d, p_i - 1)$ divides the odd part $(p_i - 1)/2^{v_i}$ of $p_i - 1$. Hence

$$\frac{|S(n)|}{\varphi(n)} = \frac{T}{\prod_i (p_i - 1)} \cdot \frac{1 + \sum_{j<\nu} 2^{jr}}{\prod_i p_i^{e_i - 1}} \le \frac{1 + \sum_{j<\nu} 2^{jr}}{2^{v_1 + \cdots + v_r}} \cdot \frac{1}{\prod_i p_i^{e_i - 1}}. \tag{1}$$

With $\sum_i v_i \ge r\nu$ and $\sum_{j<\nu} 2^{jr} = (2^{r\nu} - 1)/(2^r - 1)$,

$$\frac{1 + \sum_{j<\nu} 2^{jr}}{2^{r\nu}} = \frac{1}{2^r - 1} + 2^{-r\nu} \cdot \frac{2^r - 2}{2^r - 1} \le \frac{1}{2^r - 1} + 2^{-r} \cdot \frac{2^r - 2}{2^r - 1} = 2^{1 - r}, \tag{2}$$

since $\nu \ge 1$ and $2^r - 2 \ge 0$.

**Step 4: three or more prime factors.** If $r \ge 3$, then (1) and (2) give $|S(n)|/\varphi(n) \le 2^{1-r} \le 1/4$.

**Step 5: two prime factors.** Let $r = 2$. If $n$ is not squarefree, the last factor of (1) is at most $1/3$, and $|S(n)|/\varphi(n) \le \frac{1}{2} \cdot \frac{1}{3} < \frac14$. So let $n = pq$ with primes $p < q$. Two cases give an extra factor $\frac12$ in (1):

- If $v_1 + v_2 > 2\nu$, then $2^{v_1 + v_2} \ge 2 \cdot 2^{2\nu}$.
- If $v_1 = v_2 = \nu$, then $\gcd(d, q - 1)$ is a proper divisor of the odd part $q' = (q - 1)/2^\nu$. Otherwise $q' \mid d$ and $2^\nu \mid 2^s$ give $q - 1 \mid n - 1$. But $n - 1 = p(q - 1) + (p - 1)$, so $q - 1 \mid p - 1$, which is false as $0 < p - 1 < q - 1$. A proper divisor of an odd number is at most a third of it, so $T \le \frac13 \prod_i (p_i - 1)/2^{\nu}$.

In both cases $|S(n)|/\varphi(n) \le \frac12 \cdot 2^{1-2} = \frac14$.

**Step 6: prime powers.** Let $r = 1$, $n = p^e$ with $e \ge 2$. The formula gives $|S(n)| = 2^{\nu} \gcd(d, p - 1) \le p - 1$, and $\varphi(n) = p^{e-1}(p - 1)$. So $|S(n)|/\varphi(n) \le p^{1-e}$. This is at most $1/5$ for $p \ge 5$, and $1/9$ for $p = 3$, $e \ge 3$. The only case left is $n = 9$.

So $|S(n)| \le \varphi(n)/4$ for each odd composite $n \ne 9$.

**Corollary.** The liars $1$ and $n - 1$ are always in $S(n)$, so $[2, n - 2]$ holds $|S(n)| - 2$ of them, and $n - 3$ bases. As $\varphi(n) \le n - 1$,

$$\frac{|S(n)| - 2}{n - 3} \le \frac{(n - 1)/4 - 2}{n - 3} = \frac{n - 9}{4(n - 3)} < \frac14.$$

Independent bases multiply the probabilities. $\blacksquare$

## Consequences

- **The error of Miller-Rabin.** A prime is always accepted, and a composite is accepted by $k$ rounds with probability less than $4^{-k}$. The bound depends only on $k$, not on $n$ or on any assumption about the input; the randomness is in the bases. This makes [Miller-Rabin](/miller-rabin/) a [Monte Carlo](/monte-carlo-algorithm/) algorithm with [one-sided error](/one-sided-error/), and shows that compositeness is in [RP](/rp/).
- **Better than Fermat and Solovay-Strassen.** The [Fermat test](/fermat-primality-test/) has no bound below 1 for [Carmichael numbers](/carmichael-number/), and [Solovay-Strassen](/solovay-strassen/) has the bound $1/2$. Each strong liar is an Euler liar, so Miller-Rabin is never weaker for the same base.
- **Random inputs.** For a random odd $k$-bit number, the probability of being composite and passing one round is far below $1/4$, because most composites have very few strong liars. Damgård, Landrock and Pomerance (1993) showed that it is at most $k^2 4^{2 - \sqrt k}$ for $k \ge 2$; for candidates of several hundred bits, a few rounds give an error far below $4^{-k}$. This is the bound behind the round counts of [random prime generation](/random-prime-generation/) in standards.
- **Deterministic bases.** The count formula and the bound guide the search for [deterministic Miller-Rabin bases](/deterministic-miller-rabin-bases/), which remove the randomness below fixed limits.

## Tightness

The constant $1/4$ is attained. For $n = 15$, $|S(n)| = 2 = \varphi(15)/4$. The same holds for $n = pq$ with $p \equiv 3 \pmod 4$ prime and $q = 2p - 1$ prime: here $n - 1 = (2p + 1)(p - 1)$, $\nu = v_2(p - 1) = 1$, and $(p - 1)/2$ is the odd part of both $p - 1$ and $q - 1 = 2(p - 1)$ and divides $d$. The formula gives $|S(n)| = 2 \cdot \left(\frac{p-1}{2}\right)^2$, while $\varphi(n) = 2(p - 1)^2$, so $|S(n)| = \varphi(n)/4$. Examples are $15, 91, 703, 1891$. The Carmichael number $8911 = 7 \cdot 19 \cdot 67$, with all $p_i \equiv 3 \pmod 4$, attains it too: $|S(8911)| = 1782 = 7128/4$. Below $10^6$, 20 odd composites attain the bound. The exception $n = 9$ is real: $S(9) = \{1, 8\}$ and $\varphi(9)/4 = 3/2$.

The per-round probability over $[2, n - 2]$ is below $1/4$ but tends to it: for $n = 954271$ it is about $0.2495$.

## History

Gary Miller (1976) gave a deterministic test that tries all bases up to $O((\log n)^2)$ and is correct under the extended Riemann hypothesis. Michael Rabin (1976 talk, 1980 paper) turned it into a randomized test without any hypothesis, by proving that at most a quarter of the bases are strong liars. Louis Monier (1980) proved the same bound independently and gave the exact count of strong liars. Both papers appeared in 1980, which is why the theorem carries both names.

## References
