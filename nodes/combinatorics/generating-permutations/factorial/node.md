---
tag: GZFT4W
kind: definition
slug: factorial
name: Factorial
aliases:
- n factorial
- factorial function
area: combinatorics/generating-permutations
level: intro
summary: N! is the number of permutations of n distinct items; it grows superexponentially.
prereqs: [rule-of-product]
see_also: [permutation, stirling-approximation, legendre-formula, binomial-coefficient, factorial-number-system, factorial-modulo-prime, wilsons-theorem, big-integer]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.5, Permutations and factorials (the definition, Stirling's approximation, the power of a prime that divides n!, and the gamma function)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.4, Factorial factors (the largest power of a prime that divides n!), and Chapter 9 (Stirling's approximation)
  - paper: doi:10.2307/2308012
    title: Herbert Robbins, A remark on Stirling's formula, The American Mathematical Monthly 62(1) (1955) 26-29
    locator: the whole note (the bounds e^(1/(12n+1)) and e^(1/(12n)) on the ratio of n! to Stirling's approximation)
---

The factorial of a nonnegative integer $n$ is $n! = 1 \cdot 2 \cdots n$, with $0! = 1$. It is the number of [permutations](/permutation/) of $n$ distinct items, and so the length of every list of [all permutations](/generating-all-permutations/). It grows faster than every exponential $c^n$: by [Stirling's approximation](/stirling-approximation/), $n! \approx \sqrt{2\pi n}\,(n/e)^n$, and $\lg n! = n \lg n - n \lg e + O(\log n)$. Exact values need a [big integer](/big-integer/) for $n > 20$, and many problems use $n!$ modulo a prime instead.

## Definition

**Factorial.** For an integer $n \ge 0$,

$$0! = 1, \qquad n! = n \cdot (n-1)! \quad (n \ge 1),$$

so $n! = \prod_{k=1}^{n} k$. The empty product gives $0! = 1$.

**Counting meaning.** $n!$ is the number of ways to arrange $n$ distinct items in a row. The first place has $n$ choices, the second $n - 1$, and so on, and the [rule of product](/rule-of-product/) multiplies them. It is also the number of bijections from an $n$-set to itself, the size of the [symmetric group](/symmetric-group/) $S_n$, and, for $n = 0$, the one empty arrangement.

**Size.** Stirling's approximation, with the bounds of Robbins, holds for all $n \ge 1$:

$$\sqrt{2\pi n}\,\Big(\frac{n}{e}\Big)^n e^{1/(12n+1)} < n! < \sqrt{2\pi n}\,\Big(\frac{n}{e}\Big)^n e^{1/(12n)}.$$

So the ratio of $n!$ to $\sqrt{2\pi n}\,(n/e)^n$ tends to 1: it is $1.0844$ for $n = 1$, $1.0168$ for $n = 5$, $1.0084$ for $n = 10$ and $1.0042$ for $n = 20$. In base 2, $n!$ has $n \lg n - n \lg e + \tfrac{1}{2}\lg n + O(1)$ bits, which is $\Theta(n \log n)$. This is the reason a [comparison sort](/comparison-sort-lower-bound/) needs $\lg n! = \Theta(n \log n)$ comparisons.

**Prime factors.** For a prime $p$, the exponent of $p$ in $n!$ is given by [Legendre's formula](/legendre-formula/):

$$v_p(n!) = \sum_{i \ge 1} \Big\lfloor \frac{n}{p^i} \Big\rfloor = \frac{n - s_p(n)}{p - 1},$$

where $s_p(n)$ is the sum of the digits of $n$ in base $p$. The number of trailing zeros of $n!$ in base 10 is $v_5(n!)$, since there are always more factors 2 than 5.

**Computation.** In exact arithmetic, the product $1 \cdot 2 \cdots n$ has $\Theta(n \log n)$ bits. Multiplying in order from 1 to $n$, each step multiplies a number of $O(n \log n)$ bits by a number that fits in a word, so the total is $O(n^2 \log n / w)$ word operations with $w$-bit words. Multiplying in a balanced tree of products and using fast multiplication, such as [Karatsuba multiplication](/karatsuba-multiplication/) or methods based on the [fast Fourier transform](/fast-fourier-transform/), is much faster for large $n$. Modulo a prime $p$, the product takes $O(n)$ operations; [Wilson's theorem](/wilsons-theorem/) gives $(p - 1)! \equiv -1 \pmod p$, and [factorial modulo a prime](/factorial-modulo-prime/) treats $n!$ with $n \ge p$.

## Examples and non-examples

**Values.**

| $n$ | $n!$ | $n$ | $n!$ |
|---|---|---|---|
| 0 | 1 | 7 | 5040 |
| 1 | 1 | 8 | 40320 |
| 2 | 2 | 9 | 362880 |
| 3 | 6 | 10 | 3628800 |
| 4 | 24 | 11 | 39916800 |
| 5 | 120 | 12 | 479001600 |
| 6 | 720 | 20 | 2432902008176640000 |

**Limits of machine numbers.** $12!$ is the largest factorial below $2^{31}$, so it fits in a signed 32-bit integer, and $13! = 6\,227\,020\,800$ does not fit even in an unsigned one. $20! < 2^{63}$ fits in a signed 64-bit integer, and $21!$ is larger than $2^{64}$. In double-precision floating point, $170! \approx 7.257 \times 10^{306}$ is the largest factorial below the overflow limit, and $171!$ overflows.

**A large value.** $100!$ has 158 decimal digits and 525 bits. It ends in $v_5(100!) = 20 + 4 = 24$ zeros, and $v_2(100!) = 50 + 25 + 12 + 6 + 3 + 1 = 97$.

**A factorization.** $10! = 2^8 \cdot 3^4 \cdot 5^2 \cdot 7$. Legendre's formula gives $v_2 = 5 + 2 + 1 = 8$, $v_3 = 3 + 1 = 4$, $v_5 = 2$ and $v_7 = 1$.

**Wilson's theorem.** $6! = 720 = 102 \cdot 7 + 6$, so $6! \equiv -1 \pmod 7$. In the same way $12! \equiv 12 \equiv -1 \pmod{13}$.

**Non-examples.**

- $(-1)!$ is not defined. The recurrence would need $0! = 0 \cdot (-1)!$, which is impossible, and the gamma function, which extends $n!$ by $\Gamma(n + 1) = n!$, has poles at the non-positive integers.
- The double factorial $n!! = n (n-2)(n-4) \cdots$ is not $(n!)!$. For example $5!! = 15$, while $(5!)! = 120!$.
- $(2n)!$ is not $2 \cdot n!$, nor $(n!)^2$. The ratio $(2n)!/(n!)^2$ is the central [binomial coefficient](/binomial-coefficient/) $\binom{2n}{n}$, which is about $4^n / \sqrt{\pi n}$.
- The notation $!n$, the subfactorial, means the number of [derangements](/derangement/) of $n$ items, not $n!$.

## Related definitions

- **Falling factorial.** $n^{\underline{k}} = n (n-1) \cdots (n - k + 1) = n!/(n-k)!$, the number of sequences of $k$ distinct items from $n$.
- **[Binomial coefficient](/binomial-coefficient/).** $\binom{n}{k} = n!/(k!\,(n-k)!)$, the number of $k$-subsets of an $n$-set.
- **[Multinomial coefficient](/multinomial-coefficient/).** $n!/(m_1! \cdots m_k!)$, the number of arrangements of a multiset, as in [multiset permutations](/multiset-permutations/).
- **[Factorial number system](/factorial-number-system/).** A mixed-radix system with place values $0!, 1!, 2!, \ldots$, in which every integer in $[0, n!)$ has a unique numeral. It is the basis of [permutation ranking](/permutation-ranking/).
- **[Stirling numbers of the first kind](/stirling-numbers-first-kind/).** They split $n!$ by the number of cycles: $\sum_c {n \brack c} = n!$.
- **[Derangement](/derangement/) number.** The number of permutations without fixed points, which is the nearest integer to $n!/e$ for $n \ge 1$.

## References
