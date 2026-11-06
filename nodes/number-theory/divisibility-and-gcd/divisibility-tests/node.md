---
tag: 5KB4Z2
kind: concept
slug: divisibility-tests
name: Divisibility tests
aliases:
- casting out nines
- divisibility rules
area: number-theory/divisibility-and-gcd
level: intro
summary: Digit-based rules for testing divisibility by small integers such as 3, 9 and 11.
prereqs: [divisibility, congruence, radix]
see_also: [casting-out-nines, check-digit-computation, horner-rule, integer-division, coprime-integers, deterministic-finite-automaton]
sources:
  - book: isbn:9780321500311
    title: Kenneth H. Rosen, Elementary Number Theory and Its Applications, sixth edition
    locator: Chapter 5, Section 5.1, Divisibility tests
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 5 (congruences and residues), the rules of congruence arithmetic used by each test
  - url: "https://en.wikipedia.org/wiki/Divisibility_rule"
    locator: Wikipedia, Divisibility rule (the tables of rules for divisors up to 30 and the proofs by congruences)
---

Divisibility tests are rules that decide whether a number written in base 10 is a multiple of a small integer $m$, by looking at its digits instead of dividing. Each rule comes from one fact of [congruence](/congruence/) arithmetic: a power of the [radix](/radix/) $10^i$ leaves a simple remainder modulo $m$, such as $0$, $1$ or $-1$. The best known are the last-digit rules for $2$, $5$ and $10$, the digit sum for $3$ and $9$ (the root of *casting out nines*), and the alternating digit sum for $11$. In software, the general form of the same idea is a left-to-right scan that keeps the remainder, which works for each $m$.

## In plain words

Dividing a long number by hand is slow, but some divisors can be checked by a glance at the digits. A number is even when its last digit is even, because all the other digits stand for multiples of ten, and ten is even. A number is a multiple of nine when the sum of its digits is a multiple of nine, because ten, a hundred and a thousand are each one more than a multiple of nine. For eleven, ten is one less than eleven, so the digits are added and subtracted in turn.

Each rule is the same trick: replace each place value by its small remainder, and the remainder of the whole number does not change. For divisors with no simple rule, read the digits from left to right and keep only the remainder so far.

## The idea

Write a non-negative integer in base 10 as $n = \sum_{i=0}^{k} d_i 10^i$, with digits $0 \le d_i \le 9$ and $d_0$ the last digit. Let $m \ge 2$, and let $w_i$ be any integers with $10^i \equiv w_i \pmod m$. Then

$$n \equiv \sum_{i=0}^{k} d_i w_i \pmod m,$$

because congruences modulo $m$ can be multiplied and added term by term. So $m \mid n$ if and only if $m \mid \sum d_i w_i$. A rule is useful when the weights $w_i$ are small or mostly zero. Negative inputs reduce to $|n|$, because $m \mid n$ if and only if $m \mid -n$, and $0$ passes every test.

### Rules from a zero weight

If $m \mid 10^j$, then $w_i = 0$ for $i \ge j$, and only the last $j$ digits matter.

- $2$, $5$, $10$: $m \mid 10$, so test the last digit.
- $4$, $25$, $100$: $m \mid 100$, so test the number formed by the last two digits.
- $2^j$ and $5^j$: test the last $j$ digits.

### Rules from the weight 1

Since $10 \equiv 1 \pmod 9$, each $10^i \equiv 1$, and $n \equiv d_0 + d_1 + \cdots + d_k \pmod 9$. The same holds modulo $3$, a divisor of $9$. So the digit sum has the same remainder as $n$ modulo $9$ and modulo $3$, not only the same divisibility. Repeating the digit sum until one digit remains gives the *digital root*, which is $n \bmod 9$ with $9$ in place of $0$ for $n > 0$.

The same argument with blocks of digits gives more rules. Since $100 \equiv 1 \pmod{99}$, the sum of the 2-digit blocks of $n$ is congruent to $n$ modulo $99$, so modulo $11$ and $9$ as well. Since $1000 \equiv 1 \pmod{999}$ and $999 = 27 \cdot 37$, the sum of the 3-digit blocks tests $27$, $37$ and $999$.

### Rules from the weight $-1$

Since $10 \equiv -1 \pmod{11}$, $10^i \equiv (-1)^i$, and $n \equiv d_0 - d_1 + d_2 - \cdots \pmod{11}$. The alternating sum starts with $+$ at the last digit.

Since $1000 \equiv -1 \pmod{1001}$ and $1001 = 7 \cdot 11 \cdot 13$, the alternating sum of the 3-digit blocks, starting at the right, is congruent to $n$ modulo $7$, $11$ and $13$. This gives one test for all three primes.

### Truncation rules for divisors coprime to 10

Let $\gcd(m, 10) = 1$, and let $c$ be an integer with $10c \equiv 1 \pmod m$. Write $n = 10a + b$, where $b$ is the last digit. Then

$$m \mid 10a + b \iff m \mid a + cb.$$

*Proof.* Multiply by $c$: $c(10a + b) \equiv a + cb \pmod m$. If $m \mid 10a + b$, then $m \mid c(10a + b)$, so $m \mid a + cb$. Conversely, $10(a + cb) \equiv 10a + b \pmod m$ because $10c \equiv 1$, so $m \mid a + cb$ gives $m \mid 10a + b$. $\square$

The rule removes one digit at each step. The values of $c$ are $-2$ for $7$ (as $-20 \equiv 1 \pmod 7$), $4$ for $13$, $-5$ for $17$ and $2$ for $19$. Unlike the digit sum, this rule keeps divisibility but not the remainder: $a + cb \equiv c \, n$, not $n$.

### Products of divisors

If $m = m_1 m_2$ with $\gcd(m_1, m_2) = 1$, then $m \mid n$ if and only if $m_1 \mid n$ and $m_2 \mid n$ (see [coprime integers](/coprime-integers/), property 3). So $6$ is tested by $2$ and $3$, $12$ by $4$ and $3$, and $15$ by $3$ and $5$. The factors must be coprime: $12$ is divisible by $4$ and by $6$, but not by $24$.

### Other bases, and the general method

In base $b$, the digit sum tests $b - 1$ and its divisors, and the alternating sum tests $b + 1$. In base 2, $2 \equiv -1 \pmod 3$, so the alternating sum of the bits gives $n \bmod 3$. Since $2^j \equiv 1 \pmod{2^j - 1}$, the sum of the $j$-bit blocks of $n$ is congruent to $n$ modulo $2^j - 1$. This is the fast reduction modulo a Mersenne number.

For an arbitrary $m$, read the digits from the most significant one and keep $r \leftarrow (10r + d) \bmod m$, starting from $r = 0$. This is [Horner's rule](/horner-rule/) modulo $m$, and it is a [deterministic finite automaton](/deterministic-finite-automaton/) with $m$ states. It takes one small multiplication and reduction for each digit, so $O(k)$ word operations for a number of $k$ digits, and it returns $n \bmod m$, not only the yes or no answer.

## Examples

**Digit sum.** $n = 9{,}876{,}543{,}210$ has digit sum $45$, a multiple of $9$, so $9 \mid n$ and $3 \mid n$. Its alternating sum from the right is $0 - 1 + 2 - 3 + 4 - 5 + 6 - 7 + 8 - 9 = -5$, so $n \equiv -5 \equiv 6 \pmod{11}$, and $11 \nmid n$.

**The test for 7, 11 and 13 together.** $n = 918{,}082$. The blocks from the right are $082$ and $918$, and the alternating sum is $82 - 918 = -836$. Since $836 = 11 \cdot 76$, $11 \mid n$. Since $836 = 7 \cdot 119 + 3$ and $836 = 13 \cdot 64 + 4$, $n$ is not divisible by $7$ or $13$. Indeed $n \bmod 7 = 4 \equiv -3$ and $n \bmod 13 = 9 \equiv -4$, matching the sign of $-836$.

**Truncation for 7.** $n = 3976$: $397 - 2 \cdot 6 = 385$, then $38 - 2 \cdot 5 = 28 = 4 \cdot 7$. So $7 \mid 3976$, and indeed $3976 = 7 \cdot 568$.

**Bits for 3.** $1{,}234{,}567$ is $100101101011010000111$ in binary. The alternating sum of its bits from the right is $1$, and indeed $1{,}234{,}567 \bmod 3 = 1$.

**Casting out nines.** To check $12345 \cdot 6789 = 83{,}810{,}205$, reduce each number modulo $9$ by digit sums: $12345 \to 15 \to 6$, $6789 \to 30 \to 3$, and $6 \cdot 3 = 18 \to 0$. The claimed product has digit sum $27 \to 0$, so the check passes. The check cannot see an error that keeps the remainder modulo $9$: the wrong result $83{,}810{,}250$, with two digits swapped, also passes. The page [casting out nines](/casting-out-nines/) covers this check.

| divisor | rule | why |
|---|---|---|
| 2, 5, 10 | last digit | $10 \equiv 0$ |
| 4, 25 | last two digits | $100 \equiv 0$ |
| 8, 125 | last three digits | $1000 \equiv 0$ |
| 3, 9 | digit sum | $10 \equiv 1$ |
| 11 | alternating digit sum | $10 \equiv -1$ |
| 7, 11, 13 | alternating sum of 3-digit blocks | $1000 \equiv -1 \pmod{1001}$ |
| 27, 37 | sum of 3-digit blocks | $1000 \equiv 1 \pmod{999}$ |
| 7 | $a - 2b$ | $10 \cdot (-2) \equiv 1 \pmod 7$ |
| 6, 12, 15 | test coprime factors | $\gcd$ of the factors is 1 |
| any $m$ | $r \leftarrow (10r + d) \bmod m$ | Horner's rule |

## Where it is used

- **Checks of hand arithmetic.** Casting out nines and casting out elevens check sums and products, as in [casting out nines](/casting-out-nines/).
- **Check digits.** ISBN-10 uses a weighted sum modulo $11$, and other codes use similar weighted digit sums, to catch typing errors. See [check digit computation](/check-digit-computation/).
- **Big numbers given as text.** A number of thousands of digits, read as a string, is reduced modulo $m$ by the Horner scan without any [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/).
- **Special moduli in hardware and libraries.** Reduction modulo $2^j - 1$ by adding $j$-bit blocks, and modulo $3$ by alternating bit sums, avoid a division.
- **Number theory exercises.** The rules are first applications of [congruences](/congruence/) and of the [division theorem](/divisibility/).

## References
