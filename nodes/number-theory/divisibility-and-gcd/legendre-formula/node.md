---
tag: 3NM3HM
kind: theorem
slug: legendre-formula
name: Legendre's formula
area: number-theory/divisibility-and-gcd
level: intro
summary: Gives the exponent of a prime p in n factorial as the sum of floor(n divided by p to the k) over k.
prereqs: [prime-number, fundamental-theorem-of-arithmetic, factorial]
see_also: [lucas-theorem, factorial-modulo-prime, divisibility, binomial-coefficient, prime-number, divisor-function]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.4, Factorial Factors (the exponent of p in n!, the sum of floors and the form with the digit sum in base p)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.5, Permutations and Factorials (the highest power of a prime that divides n!)
  - url: "https://en.wikipedia.org/wiki/Legendre%27s_formula"
    locator: lead and section Alternate form (the digit-sum form, and the references to Legendre's Théorie des Nombres and to Dickson's History of the Theory of Numbers, Volume 1, page 263)
---

Legendre's formula gives the exponent of a [prime](/prime-number/) $p$ in the [factorial](/factorial/) $n!$ as $\sum_{i \ge 1} \lfloor n / p^i \rfloor$, a sum with only $\lfloor \log_p n \rfloor$ nonzero terms. An equal form is $(n - s_p(n))/(p - 1)$, where $s_p(n)$ is the sum of the digits of $n$ in base $p$. It finds the number of trailing zeros of $n!$, the exact power of a prime in a [binomial coefficient](/binomial-coefficient/), and the factorization of $n!$, all without computing $n!$, which has about $n \lg n$ bits.

## Statement

For a prime $p$ and an integer $m \ne 0$, let $v_p(m)$ be the exponent of $p$ in $|m|$: the largest $e \ge 0$ with $p^e \mid m$. Let $s_p(n)$ be the sum of the base-$p$ digits of $n$.

**Theorem.** For each prime $p$ and each integer $n \ge 0$,

$$v_p(n!) = \sum_{i=1}^{\infty} \left\lfloor \frac{n}{p^i} \right\rfloor = \frac{n - s_p(n)}{p - 1}.$$

The sum is finite: its terms are 0 for $p^i > n$. For $n = 0$ both sides are 0, since $0! = 1$.

**Corollary (bounds).** For $n \ge 1$,

$$\frac{n}{p - 1} - \left(\lfloor \log_p n \rfloor + 1\right) \le v_p(n!) \le \frac{n - 1}{p - 1},$$

and the upper bound is an equality if and only if $n$ is a power of $p$.

## In plain words

To count how many times a prime such as five divides the product of all numbers from one up to some limit, you do not multiply the numbers. Every multiple of five gives one factor of five. Every multiple of twenty-five gives one more. Every multiple of one hundred twenty-five gives one more again, and so on. So you count the multiples of five, then the multiples of twenty-five, then of one hundred twenty-five, and add the counts.

A factorial ends in as many zeros as it has factors of ten, and it always has more factors of two than of five. So this count for five tells you how many zeros the factorial ends with.

## Proof

**The sum of floors.** By the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/), $v_p(ab) = v_p(a) + v_p(b)$ for nonzero $a$ and $b$, so

$$v_p(n!) = \sum_{j=1}^{n} v_p(j).$$

For $j \ge 1$, $v_p(j)$ is the number of $i \ge 1$ with $p^i \mid j$, because $p^i \mid j$ holds exactly for $i = 1, \ldots, v_p(j)$. So

$$\sum_{j=1}^{n} v_p(j) = \sum_{j=1}^{n} \sum_{i \ge 1} [p^i \mid j] = \sum_{i \ge 1} \#\{ j : 1 \le j \le n,\ p^i \mid j \},$$

where the exchange of the sums is valid because only finitely many terms are nonzero. The multiples of $m \ge 1$ in $\{1, \ldots, n\}$ are $m, 2m, \ldots, \lfloor n/m \rfloor m$, so there are $\lfloor n/m \rfloor$ of them. With $m = p^i$ this gives the first formula.

**The digit sum.** Write $n = \sum_{j=0}^{k} d_j p^j$ with digits $0 \le d_j \le p - 1$. For $i \ge 1$,

$$\left\lfloor \frac{n}{p^i} \right\rfloor = \sum_{j \ge i} d_j p^{j - i},$$

because the remaining part $\sum_{j < i} d_j p^j$ is at most $(p - 1)(1 + p + \cdots + p^{i-1}) = p^i - 1 < p^i$. Summing over $i \ge 1$, the digit $d_j$ is multiplied by $p^{j-1} + p^{j-2} + \cdots + 1 = (p^j - 1)/(p - 1)$. Hence

$$\sum_{i \ge 1} \left\lfloor \frac{n}{p^i} \right\rfloor = \sum_{j=0}^{k} d_j \frac{p^j - 1}{p - 1} = \frac{n - s_p(n)}{p - 1}.$$

**The bounds.** For $n \ge 1$, $s_p(n) \ge 1$, so $v_p(n!) \le (n - 1)/(p - 1)$, with equality exactly when $s_p(n) = 1$, that is, when $n$ is a power of $p$. Also $n$ has $\lfloor \log_p n \rfloor + 1$ digits, each at most $p - 1$, which gives the lower bound. $\blacksquare$

## Consequences

**Examples.**

| $n$ | $p$ | nonzero terms $\lfloor n/p^i \rfloor$ | $v_p(n!)$ |
| --- | --- | --- | --- |
| 10 | 2 | 5, 2, 1 | 8 |
| 6 | 2 | 3, 1 | 4 |
| 25 | 5 | 5, 1 | 6 |
| 100 | 5 | 20, 4 | 24 |
| 100 | 3 | 33, 11, 3, 1 | 48 |
| 100 | 2 | 50, 25, 12, 6, 3, 1 | 97 |
| 1000 | 7 | 142, 20, 2 | 164 |

For $n = 100$ and $p = 2$, $100 = 1100100_2$ has digit sum 3, and $(100 - 3)/1 = 97$. Indeed $10! = 3628800 = 2^8 \cdot 3^4 \cdot 5^2 \cdot 7$.

- **Trailing zeros.** The number of trailing zeros of $n!$ in base 10 is $\min(v_2(n!), v_5(n!)) = v_5(n!)$, since $v_2(n!) \ge v_5(n!)$ term by term. So $100!$ ends in 24 zeros and $1000!$ in 249 zeros. In base $b$, the count is $\min_{p \mid b} \lfloor v_p(n!) / v_p(b) \rfloor$.
- **Computation.** The loop "$e \leftarrow 0$; while $n > 0$: $n \leftarrow \lfloor n/p \rfloor$, $e \leftarrow e + n$" computes $v_p(n!)$ with $\lfloor \log_p n \rfloor + 1$ divisions. On the [word RAM](/word-ram/) it takes $O(\log_p n)$ time, with no overflow, because $e < n$. For $n = 10^{18}$ and $p = 5$ it gives 249999999999999995.
- **Binomial coefficients and Kummer's theorem.** Applying the digit form to $\binom{n}{k} = n! / (k!\,(n - k)!)$ gives
$$v_p\!\left(\binom{n}{k}\right) = \frac{s_p(k) + s_p(n - k) - s_p(n)}{p - 1},$$
which is the number of carries when $k$ and $n - k$ are added in base $p$ (Kummer's theorem). For example, $v_2\big(\binom{100}{50}\big) = 3$. This complements [Lucas's theorem](/lucas-theorem/), which gives $\binom{n}{k} \bmod p$.
- **Factorizing $n!$.** With the primes up to $n$ from the [sieve of Eratosthenes](/sieve-of-eratosthenes/), the formula gives the full factorization of $n!$, and of $\binom{n}{k}$, in $O(n)$ word operations after the sieve. This is how big binomial coefficients and $n! \bmod m$ for composite $m$ are often computed; see also [factorial modulo a prime](/factorial-modulo-prime/).

## Tightness

The upper bound $v_p(n!) \le (n - 1)/(p - 1)$ is reached exactly at $n = p^k$: for example $v_2(1024!) = 1023$. The lower bound loses at most the number of digits times $p - 1$, which is reached when every digit is $p - 1$, for example $n = 2^k - 1$, where $v_2(n!) = n - k$.

The formula needs $p$ prime. For a composite base it is false: with $m = 4$, $\sum_i \lfloor 10/4^i \rfloor = 2$, but the largest power of 4 that divides $10! = 2^8 \cdot 3^4 \cdot 5^2 \cdot 7$ is $4^4$. For a composite $m$, factor $m = \prod p^{e_p}$ and use $\min_p \lfloor v_p(n!) / e_p \rfloor$.

## History

The formula is named after Adrien-Marie Legendre, who gave it in his work on the theory of numbers; Dickson's History of the Theory of Numbers records it in Volume 1, page 263 (as cited by the Wikipedia article). Kummer's theorem on the carries is a later result that follows from the digit form. Concrete Mathematics derives both forms in Section 4.4.

## References
