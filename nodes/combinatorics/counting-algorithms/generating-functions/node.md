---
tag: DWV9NX
kind: technique
slug: generating-functions
name: Generating functions
aliases:
- ordinary generating functions
- formal power series counting
- OGF
area: combinatorics/counting-algorithms
level: core
summary: Encodes a sequence as a power series to solve counting recurrences.
prereqs: [recurrence-relation, polynomial]
see_also: [exponential-generating-functions, symbolic-method, transfer-matrix-method, catalan-numbers, coin-change-counting, integer-partition-counting, power-series-inversion, linear-recurrence-nth-term]
sources:
  - book: isbn:9781568812793
    title: Herbert S. Wilf, generatingfunctionology, third edition, A K Peters, 2006
    locator: Chapter 1, Introductory ideas and examples, and Chapter 2, Series
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Chapter 7, Generating Functions (Sections 7.1 to 7.5)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.9, Generating Functions
  - book: isbn:9780521898065
    title: Philippe Flajolet and Robert Sedgewick, Analytic Combinatorics, Cambridge University Press, 2009
    locator: Chapter I, Combinatorial structures and ordinary generating functions, and Appendix A.5, Formal power series
---

A generating function encodes a sequence $a_0, a_1, a_2, \ldots$ as one formal power series $A(z) = \sum_{n \ge 0} a_n z^n$. A [recurrence](/recurrence-relation/) for the sequence becomes an equation for $A(z)$, and the rules of algebra on series solve it. The coefficient of $z^n$ in the solution is the answer for size $n$, either in closed form or by a fast series computation. The method counts [Catalan](/catalan-numbers/) structures, [ways to make change](/coin-change-counting/), [partitions](/integer-partition-counting/) and the solutions of every linear recurrence with constant coefficients.

## In plain words

Suppose you want the number of objects of each size: the number of strings of length 0, of length 1, of length 2, and so on. Instead of a table, write one long sum: the first count, plus the second count times a marker, plus the third count times the marker squared, and so on. The power of the marker says which size a count belongs to.

The point is that this long sum behaves like a polynomial. You can add two of them, multiply them, and divide by them. A rule that builds big objects from small ones turns into an equation between such sums. You solve the equation with ordinary algebra, and then you read off the count of each size from the answer. The marker never gets a numeric value. It only keeps the counts apart.

## When it applies

- The objects have a size $n$, and the number $a_n$ of objects of size $n$ is finite for each $n$.
- An object of size $n$ splits into smaller objects whose sizes add up to $n$, or it extends a smaller object by a piece of fixed size. Splits of the first kind give a product of series, splits of the second kind give a shift.
- The question asks for $a_n$ for one large $n$, for all $n \le N$, for a closed form, or for the growth rate of $a_n$.
- The objects are unlabeled, or the order of the atoms does not matter. For labeled objects, such as permutations and set partitions, use [exponential generating functions](/exponential-generating-functions/).

## The template

**Notation.** $n$ is the size, $a_n$ the number of objects of size $n$, and $N$ the largest size that a program needs. $[z^n] A(z)$ is the coefficient of $z^n$ in $A(z)$.

**Formal power series.** A formal power series is a sequence $(a_n)_{n \ge 0}$ written as $A(z) = \sum_n a_n z^n$. No value of $z$ is ever put in, so no question of convergence comes up. The operations are:

- sum: $[z^n](A + B) = a_n + b_n$;
- product (the Cauchy product, or convolution): $[z^n] A B = \sum_{k=0}^{n} a_k b_{n-k}$, a finite sum for each $n$;
- shift: $[z^n]\, z^m A(z) = a_{n-m}$ for $n \ge m$, and $0$ for $n < m$;
- derivative: $[z^n] A'(z) = (n+1) a_{n+1}$.

With these operations the series with coefficients in a field form a commutative ring with unit $1$.

**Inverse.** $A(z)$ has a series $B(z)$ with $A B = 1$ if and only if $a_0 \ne 0$. *Proof.* If $AB = 1$, the constant terms give $a_0 b_0 = 1$, so $a_0 \ne 0$. If $a_0 \ne 0$, put $b_0 = 1/a_0$ and, for $n \ge 1$, $b_n = -\frac{1}{a_0} \sum_{k=1}^{n} a_k b_{n-k}$. Then $[z^0] AB = 1$, and for $n \ge 1$, $[z^n] AB = a_0 b_n + \sum_{k=1}^{n} a_k b_{n-k} = 0$. The equation for $b_n$ has the single solution given, so $B$ is unique. $\square$ The most used case is the geometric series $\frac{1}{1 - cz} = \sum_n c^n z^n$, where $a_0 = 1$, $a_1 = -c$, and the rule gives $b_n = c\, b_{n-1} = c^n$.

The method has these steps.

```pseudo id=main
GF-SOLVE(rule for a_n, N)
L1  write the rule as one equation that holds for every n ≥ 0, with a_n = 0 for n < 0
L2      ▷ add a correction term such as [n = 0] for each initial value the rule misses
L3  multiply both sides by z^n and sum over all n ≥ 0
L4  rewrite each sum with A(z): a_(n−m) gives z^m A(z), a convolution gives a product
L5  solve the equation for A(z)                          ▷ hole: algebra on series
L6  if a closed form is wanted then
L7      expand A(z): partial fractions, the binomial series, or a known series
L8  else compute [z^0], ..., [z^N] of A(z) by series arithmetic truncated at degree N
L9  return a_n = [z^n] A(z)
```

Line L1 is the step that most often goes wrong. A recurrence like $a_n = a_{n-1} + a_{n-2}$ is usually stated only for $n \ge 2$. For $n = 0$ and $n = 1$ it is false as written, so it needs correction terms before the sums of line L3 are correct.

**Cost of line L8.** All arithmetic is exact. The product of two series truncated at degree $N$ takes $O(N^2)$ coefficient operations by the definition, and $O(N \log N)$ operations with [FFT multiplication](/fft-polynomial-multiplication/) when the coefficients are residues modulo a prime $p$ with a suitable root of unity, see the [number-theoretic transform](/number-theoretic-transform/). The inverse costs $O(N^2)$ operations by the rule of the proof above, and the cost of one product by [Newton iteration](/newton-power-series-inversion/). For a rational series $P(z)/Q(z)$ with $Q(0) = 1$ and $\deg Q = d$, the rule $a_n = p_n - \sum_{k=1}^{d} q_k a_{n-k}$ gives $a_0, \ldots, a_N$ in $O(dN)$ operations. With exact big integers, the coefficients usually have $\Theta(n)$ bits, so these counts must be multiplied by the bit length, for example $O(dN^2)$ bit operations for a rational series whose coefficients grow exponentially.

## Classic examples

**1. Fibonacci numbers (Concrete Mathematics, Section 7.3).** The rule $F_n = F_{n-1} + F_{n-2}$ for $n \ge 2$, with $F_0 = 0$ and $F_1 = 1$, holds for all $n \ge 0$ in the form $F_n = F_{n-1} + F_{n-2} + [n = 1]$, with $F_n = 0$ for $n < 0$. Line L4 gives $F(z) = z F(z) + z^2 F(z) + z$, so

$$F(z) = \frac{z}{1 - z - z^2}.$$

With $\varphi = (1 + \sqrt 5)/2$ and $\psi = (1 - \sqrt 5)/2$, the denominator is $(1 - \varphi z)(1 - \psi z)$, and partial fractions give $F(z) = \frac{1}{\sqrt 5}\bigl(\frac{1}{1 - \varphi z} - \frac{1}{1 - \psi z}\bigr)$. The geometric series then give $F_n = (\varphi^n - \psi^n)/\sqrt 5$. The rule of line L8 gives the values $0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89$ (OEIS A000045). See [Fibonacci numbers](/fibonacci-numbers/).

**2. Binary strings with no two adjacent 1s.** Let $b_n$ count them. A string ends in 0 after any good string of length $n-1$, or in 01 after any good string of length $n-2$. The single strings "" and "1" need the corrections $[n = 0]$ and $[n = 1]$. So $B(z) = 1 + z + z B(z) + z^2 B(z)$, and $B(z) = (1 + z)/(1 - z - z^2)$. The coefficients are $1, 2, 3, 5, 8, 13, 21, 34$, so $b_n = F_{n+2}$.

**3. Making change.** The number of ways to pay $n$ cents with coins of values $c_1, \ldots, c_m$, each value used any number of times, is

$$[z^n] \prod_{i=1}^{m} \frac{1}{1 - z^{c_i}},$$

because the factor $1/(1 - z^{c}) = 1 + z^c + z^{2c} + \cdots$ chooses how many coins of value $c$ to use. For the values 1, 2 and 5 the coefficients for $n = 0$ to $10$ are $1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 10$ (OEIS A000115). For the US coins 1, 5, 10, 25 and 50, the coefficient of $z^{100}$ is 292. See [coin change counting](/coin-change-counting/).

**4. Integer partitions.** Take every positive integer as a coin value: $\sum_n p(n) z^n = \prod_{k \ge 1} 1/(1 - z^k)$. Each coefficient of $z^n$ needs only the factors with $k \le n$, so the infinite product is a well defined formal series. The inverse of this product is the subject of [Euler's pentagonal number theorem](/euler-pentagonal-number-theorem/), and it gives the [pentagonal recurrence](/euler-pentagonal-recurrence/) for $p(n)$.

**5. Catalan numbers.** A binary tree is empty, or it is a root with a left and a right subtree. With $C_n$ the number of binary trees with $n$ nodes, the rule is $C_n = [n = 0] + \sum_{k=0}^{n-1} C_k C_{n-1-k}$, and line L4 turns the convolution into a product: $C(z) = 1 + z\, C(z)^2$. The quadratic formula gives two roots. The root $(1 + \sqrt{1 - 4z})/(2z)$ has a term $1/z$, so it is not a power series. The other root is

$$C(z) = \frac{1 - \sqrt{1 - 4z}}{2z},$$

and the binomial series of $\sqrt{1 - 4z}$ gives $C_n = \frac{1}{n+1}\binom{2n}{n}$: $1, 1, 2, 5, 14, 42, 132, 429, 1430$ (OEIS A000108). See [Catalan numbers](/catalan-numbers/).

**6. Compositions.** An ordered sequence of $k$ parts, each part a positive integer, has the series $\bigl(z/(1 - z)\bigr)^k$. Summing over $k \ge 0$ gives $\frac{1 - z}{1 - 2z}$, so there are $2^{n-1}$ compositions of $n \ge 1$. See [counting integer compositions](/counting-integer-compositions/).

## Variations

- **Exponential generating functions.** $\sum_n a_n z^n / n!$ fits labeled objects, because the product of two such series counts the ways to split a set of labels. See [exponential generating functions](/exponential-generating-functions/).
- **The symbolic method.** A grammar of the objects (sum, product, sequence, set) gives the equation of line L5 directly, with no recurrence at all. See [symbolic method](/symbolic-method/).
- **The transfer-matrix method.** Objects that a finite automaton or a walk in a finite graph describes have a rational series $\det(I - zM)$ in the denominator. See [transfer-matrix method](/transfer-matrix-method/).
- **Bivariate series.** A second variable $u$ marks a parameter, such as the number of parts: $\sum_{n,k} a_{n,k} u^k z^n$. The [Stirling numbers](/stirling-numbers-second-kind/) and the [Eulerian numbers](/eulerian-numbers/) have such series.
- **Linear recurrences.** A rational series is the same thing as a sequence that satisfies a linear recurrence with constant coefficients. Its $N$th term costs $O(d^2 \log N)$ or less operations, see [the Nth term of a linear recurrence](/linear-recurrence-nth-term/).
- **Asymptotics.** The smallest singularity of $A(z)$, as a function of a complex $z$, fixes the exponential growth of $a_n$. For $F(z)$ it is $1/\varphi$, so $F_n$ grows like $\varphi^n$. Analytic combinatorics makes this precise.

## Pitfalls

- **A recurrence that does not hold for small n.** For Fibonacci, the sum of $F_n z^n$ over all $n$ is not $z F + z^2 F$, because the equation fails at $n = 1$. Without the term $[n = 1]$ the solution is $F(z) = 0$. Test: compare the first few coefficients of the solution with the first few terms of the sequence.
- **The wrong root.** A quadratic or higher equation has several solutions. Only the one that is a power series, with the right constant term, is the answer. For Catalan, the $+$ sign gives a series that starts with $1/z$.
- **Division by a series with zero constant term.** $1/A(z)$ exists only when $a_0 \ne 0$. For example, $1/z$ is not a power series. Factor out the power of $z$ first.
- **Floating point.** Coefficients grow fast: $C_{30} = 3814986502092304$ already has 52 bits, and $p(1000)$ has 32 decimal digits. Use exact integers or residues modulo a prime.
- **An off-by-one in the shift.** $\sum_{n \ge 0} a_{n+1} z^n = (A(z) - a_0)/z$, not $A(z)/z$.

## Exercises

1. Show that $\sum_{n \ge 0} n z^n = z/(1 - z)^2$ by taking the derivative of $1/(1 - z)$, and use it to get the sum $1 + 2 + \cdots + n$.
2. Let $t_n$ be the number of tilings of a $2 \times n$ board with $1 \times 2$ dominoes. Show that $\sum t_n z^n = 1/(1 - z - z^2)$, so $t_n = F_{n+1}$.
3. Show that the number of partitions of $n$ into distinct parts equals the number into odd parts, by the identity $\prod_k (1 + z^k) = \prod_k \frac{1 - z^{2k}}{1 - z^k}$.
4. Compute $[z^{10}] \frac{1}{(1 - z)(1 - z^2)(1 - z^5)}$ by hand with the rule of example 3. The answer is 10.
5. Write a program that inverts a series modulo a prime $p$ with the rule of the proof of the inverse, and check it on $1 - z - z^2$, whose inverse has the coefficients $F_{n+1}$.

## References
