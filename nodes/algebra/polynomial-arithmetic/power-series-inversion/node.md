---
tag: KY02VK
kind: problem
slug: power-series-inversion
name: Power series inversion
aliases:
- inverse modulo x^n
- power series reciprocal
- reciprocal of a power series
area: algebra/polynomial-arithmetic
level: advanced
summary: Given f with f(0) a unit, compute g with fg = 1 modulo x^n.
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of coefficients of the inverse, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(n))}
prereqs: [polynomial-ring, polynomial-multiplication]
see_also: [newton-power-series-inversion, fast-polynomial-division, polynomial-division, newton-iteration, newton-raphson-division, linear-recurrence-nth-term, bostan-mori-algorithm, modular-inverse]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 9.1, Division with remainder using Newton iteration (inversion modulo x^l by Newton iteration and its use for division)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.7, Manipulation of power series (division of power series and Newton's method for reversion)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 4.2.4, Newton's method for formal power series
  - paper: doi:10.1007/BF02242389
    title: Malte Sieveking, An algorithm for division of power series, Computing 10, 1972
    locator: pp. 153 to 156
  - paper: doi:10.1007/BF01436917
    title: H. T. Kung, On computing reciprocals of power series, Numerische Mathematik 22(5), 1974
    locator: pp. 341 to 348
  - paper: doi:10.1006/jsco.2002.0562
    title: Joris van der Hoeven, Relax, but don't be too lazy, Journal of Symbolic Computation 34(6), 2002
    locator: pp. 479 to 542 (relaxed, that is online, multiplication and the operations built on it)
---

Power series inversion asks for the first $n$ coefficients of $1/f$, for a power series $f$ over a commutative ring $R$ whose constant term is a unit. The answer is the unique polynomial $g$ of degree less than $n$ with $f g \equiv 1 \pmod{x^n}$. The term-by-term recurrence solves it with $O(n^2)$ ring operations, and [Newton iteration](/newton-power-series-inversion/) solves it with $O(M(n))$, so inversion is as cheap as multiplication up to a constant factor. It is the core of fast [polynomial division](/polynomial-division/) and of many fast algorithms on power series.

## In plain words

A power series is like a polynomial that goes on forever. Some of them have an inverse: another series that gives exactly 1 when you multiply the two. For example, one minus x times one plus x plus x squared plus x cubed and so on gives 1.

We cannot write all of an infinite series, so we ask only for its first n numbers. These are fixed one after the other: the first number makes the constant term 1, the second makes the next term 0, and so on. This works when the first number of the series can be divided by, as any nonzero number can in the rationals.

The fast method guesses a short answer and then makes it twice as long at each step, with a few multiplications.

## Definition

Let $R$ be a commutative ring with $1$. A formal power series over $R$ is a sum $f = \sum_{i \ge 0} f_i x^i$ with $f_i \in R$; the series form the ring $R[[x]]$, with the product $(f g)_k = \sum_{i + j = k} f_i g_j$. For $n \ge 1$, $f \equiv g \pmod{x^n}$ means $f_i = g_i$ for all $i < n$.

**Problem.** Given $n \ge 1$ and the coefficients $f_0, \ldots, f_{n-1}$ of $f$, with $f_0$ a unit of $R$, compute the polynomial $g = \sum_{i < n} g_i x^i$ with

$$f g \equiv 1 \pmod{x^n}.$$

Only $f_0, \ldots, f_{n-1}$ affect the answer, because the coefficients of $f g$ below $x^n$ use only these.

**Existence and uniqueness.** Such a $g$ exists and is unique exactly when $f_0$ is a unit. If $f g \equiv 1$, the constant terms give $f_0 g_0 = 1$, so $f_0$ is a unit. Conversely, the coefficient of $x^k$ in $f g$ is $f_0 g_k + \sum_{j=1}^{k} f_j g_{k-j}$, so the conditions are

$$g_0 = f_0^{-1}, \qquad g_k = -f_0^{-1} \sum_{j=1}^{k} f_j\, g_{k-j} \quad (1 \le k < n),$$

and each $g_k$ is fixed by $g_0, \ldots, g_{k-1}$. Letting $n$ grow gives the result for $R[[x]]$: $f$ is a unit of $R[[x]]$ exactly when $f_0$ is a unit of $R$.

**Cost model.** Costs count operations in $R$ at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/), with one inversion in $R$ for $f_0^{-1}$. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$, and we assume, as von zur Gathen and Gerhard do in Section 8.3, that $M(n)/n$ is nondecreasing.

## Variants

- **Power series division.** Compute $h / f \bmod x^n$ for a second series $h$. It is $h \cdot (1/f) \bmod x^n$, one inversion and one product.
- **Inversion modulo $x^n$ of a polynomial.** The same problem, with $f$ a polynomial. It is a special case of inversion modulo a general polynomial $m$, which the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) solves when $\gcd(f, m) = 1$; for $m = x^n$ Newton iteration is faster.
- **Online inversion.** Output $g_k$ after reading only $f_0, \ldots, f_k$. The recurrence does this naturally. Van der Hoeven's relaxed multiplication gives online inversion within a factor $O(\log n)$ of $M(n)$.
- **Other coefficient domains.** Over $\mathbb{Z}$ the constant term must be $\pm 1$; otherwise the inverse lives in $\mathbb{Q}[[x]]$. The $p$-adic analogue inverts an integer modulo $p^n$, and the real analogue is [Newton-Raphson division](/newton-raphson-division/) of numbers.
- **Noncommutative coefficients.** The same recurrence and Newton step work in $R[[x]]$ for a noncommutative $R$, such as square matrices, when $f_0$ is invertible, with care for the order of the factors.
- **Related series operations.** Square roots, logarithms, exponentials and the reversion of series are computed by Newton iteration too, and their cost is a constant times $M(n)$; Knuth, Section 4.7, and Brent and Zimmermann, Section 4.2.4, treat them.

## Examples

All values below were checked by a script.

- **The geometric series.** $1/(1 - x) = 1 + x + x^2 + \cdots$: for every $n$, $(1 - x)(1 + x + \cdots + x^{n-1}) = 1 - x^n \equiv 1$.
- **Fibonacci numbers.** $1/(1 - x - x^2) \equiv 1 + x + 2x^2 + 3x^3 + 5x^4 + 8x^5 + 13x^6 + 21x^7 + 34x^8 + 55x^9 \pmod{x^{10}}$. The recurrence is $g_k = g_{k-1} + g_{k-2}$, so the coefficients are the [Fibonacci numbers](/fibonacci-numbers/). Every series $p/q$ with polynomials $p, q$ and $q_0$ a unit satisfies a [linear recurrence](/linear-recurrence-nth-term/) in this way.
- **A constant term that is not $\pm 1$.** $f = 2 + x$ has no inverse in $\mathbb{Z}[[x]]$. In $\mathbb{Q}[[x]]$, $1/(2 + x) \equiv \tfrac12 - \tfrac14 x + \tfrac18 x^2 - \tfrac1{16} x^3 + \tfrac1{32} x^4 \pmod{x^5}$.
- **A ring with zero divisors.** Over $\mathbb{Z}/4\mathbb{Z}$, $(1 + 2x)^2 = 1 + 4x + 4x^2 = 1$, so $1 + 2x$ is its own inverse modulo every $x^n$. The recurrence gives $g = 1 + 2x$.
- **Partitions.** By [Euler's pentagonal number theorem](/euler-pentagonal-number-theorem/), $\prod_{k \ge 1} (1 - x^k) = 1 - x - x^2 + x^5 + x^7 - x^{12} - \cdots$. Inverting it modulo $x^{12}$ gives $1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56$, the numbers of partitions of $0, \ldots, 11$.
- **Bernoulli numbers.** Over $\mathbb{Q}$, inverting $(e^x - 1)/x = \sum_{k \ge 0} x^k / (k+1)!$ modulo $x^7$ gives $1 - \tfrac12 x + \tfrac1{12} x^2 - \tfrac1{720} x^4 + \tfrac1{30240} x^6$, the start of $x / (e^x - 1) = \sum_k B_k x^k / k!$.
- **Non-example.** $f = x$ has $f_0 = 0$, which is not a unit, and no $g$ gives $x g \equiv 1$: the constant term of $x g$ is $0$.

## Known algorithms

- **Term-by-term recurrence.** The formula for $g_k$ in the definition, with $k$ products for $g_k$: $n(n-1)/2$ multiplications, as many additions, and one inversion. It is the method of Knuth, Section 4.7, for dividing power series, and it is online.
- **[Newton iteration](/newton-power-series-inversion/).** Start with $g = f_0^{-1}$, which is correct modulo $x$, and repeat $g \leftarrow g (2 - f g) \bmod x^{2k}$, which turns an inverse modulo $x^k$ into one modulo $x^{2k}$. *Proof of the step.* If $f g = 1 - e$ with $e \equiv 0 \pmod{x^k}$, then $f \cdot g (2 - f g) = (1 - e)(1 + e) = 1 - e^2$, and $e^2 \equiv 0 \pmod{x^{2k}}$. With $\lceil \log_2 n \rceil$ steps and the assumption on $M$, the total is $O(M(n))$; von zur Gathen and Gerhard, Section 9.1, bound it by $3 M(n) + O(n)$. This is due to Sieveking (1972) and Kung (1974).
- **Divide and conquer for online use.** Van der Hoeven's relaxed algorithms compute the recurrence in blocks with fast products, so that $g_k$ is still output after $f_k$ is read, at a cost of $O(M(n) \log n)$ ring operations.
- **Via the [subproduct tree](/subproduct-tree/) or the [FFT](/fft-polynomial-multiplication/).** These are not separate methods; they make the products inside Newton iteration fast.

## Bounds

- **Upper bound.** $O(M(n))$, from Newton iteration. So inversion costs $O(n \log n)$ when $R$ supports the FFT, and $O(n \log n \log \log n)$ over any commutative ring with Cantor and Kaltofen's multiplication. These are proved bounds; the constant in front of $M(n)$ depends on the method and is studied in Section 9.1 of von zur Gathen and Gerhard and in Section 4.2.4 of Brent and Zimmermann.
- **Lower bound.** $\Omega(n)$, since $g_k$ depends on $f_k$ for each $k$: $g_k = -f_0^{-2} f_k + (\text{terms in } f_1, \ldots, f_{k-1})$.
- **Equivalence with multiplication.** When $2$ is a unit of $R$, multiplication costs at most a constant times inversion, so inversion and multiplication have the same cost up to constant factors. The reduction is given under Reductions.

## Reductions

- **Polynomial division reduces to inversion.** For $f$ of degree $m$ and $g$ of degree $d \le m$ with a unit leading coefficient, the reversed quotient is $\operatorname{rev}(f) \cdot \operatorname{rev}(g)^{-1} \bmod x^{m - d + 1}$, where $\operatorname{rev}$ reverses the coefficient list. This is [fast polynomial division](/fast-polynomial-division/), and the [polynomial division](/polynomial-division/) page proves the identity.
- **Squaring reduces to inversion.** Let $a$ have degree less than $k$ and let $K = 2k$. Then
  $$(1 - x^K a)^{-1} \equiv 1 + x^K a + x^{2K} a^2 \pmod{x^{3K}},$$
  because $(1 - x^K a)(1 + x^K a + x^{2K} a^2) = 1 - x^{3K} a^3$. The term $x^K a$ has degree less than $K + k < 2K$ and $a^2$ has degree at most $2k - 2 < K$, so the coefficients of $x^{2K}, \ldots, x^{3K - 1}$ of the inverse are exactly those of $a^2$. One inversion modulo $x^{6k}$ gives a square of size $k$. For example, $a = 1 + 2x$ with $K = 4$ gives the coefficients $1, 4, 4, 0$ at $x^8, \ldots, x^{11}$, and $(1 + 2x)^2 = 1 + 4x + 4x^2$.
- **Multiplication reduces to squaring** when $2$ is a unit: $a b = \tfrac12 ((a + b)^2 - a^2 - b^2)$. With the previous reduction, $M(k) \le 3 I(6k) + O(k)$, where $I(n)$ is the cost of inversion modulo $x^n$. In characteristic $2$ the squaring map is additive, $(a + b)^2 = a^2 + b^2$, and this reduction does not apply.
- **Linear recurrences.** The first $n$ terms of a sequence with a rational generating function $p/q$ are $p \cdot q^{-1} \bmod x^n$. The $n$th term alone is cheaper with the [Bostan-Mori algorithm](/bostan-mori-algorithm/).
- **Modular inverses.** Inversion modulo $x^n$ is the polynomial analogue of the [modular inverse](/modular-inverse/) of an integer modulo $p^n$, and Newton's step $g \leftarrow g (2 - f g)$ lifts both.

## Applications

- **Fast division with remainder** of polynomials, and through it fast [multipoint evaluation](/multipoint-evaluation/), fast interpolation, fast gcds and fast Chinese remaindering, which all divide many times.
- **Integer and floating-point division.** The same Newton step computes reciprocals of numbers, as in [Newton-Raphson division](/newton-raphson-division/).
- **Combinatorics.** Many counting sequences have generating functions that are reciprocals, such as the partition numbers and the Bernoulli numbers above, so their first $n$ terms come from one inversion.
- **Rational functions and recurrences.** Expanding $p/q$ gives the terms of a linear recurrence; this is used for sequences, digital filters and the Taylor expansion of rational functions.
- **Other series operations.** Logarithms, exponentials, square roots, power series composition and reversion all use inversion inside their Newton iterations.

## References
