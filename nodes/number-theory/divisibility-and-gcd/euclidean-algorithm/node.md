---
tag: 4XB0RJ
kind: algorithm
slug: euclidean-algorithm
name: Euclidean algorithm
aliases:
- Euclid's algorithm
- subtractive Euclidean algorithm
- division-based gcd
area: number-theory/divisibility-and-gcd
level: intro
summary: Repeatedly replace (a, b) by (b, a mod b) until the remainder is zero; runs in O(log min(a, b)) steps.
solves: [gcd-of-two-integers]
model: word-ram
complexity:
  vars: {m: the smaller of the absolute values of the inputs, n: the bit length of the larger input}
  time: {worst: Θ(log m), best: Θ(1)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: -300
  people: [Euclid]
  note: Euclid's Elements, Book VII, Propositions 1 and 2, give the method by repeated subtraction.
prereqs: [greatest-common-divisor, divisibility, gcd-recursion-theorem, loop-invariant]
see_also: [extended-euclidean-algorithm, binary-gcd, lames-theorem, lehmers-gcd, half-gcd, continued-fraction, gcd-of-array, polynomial-gcd]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The greatest common divisor (Algorithm E, Algorithm A, the history of Euclid's algorithm), and Section 4.5.3, Analysis of Euclid's algorithm (Lamé's bound and the average number of steps)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (the procedure EUCLID, the GCD recursion theorem, the Fibonacci lemma and Lamé's theorem)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 2.1.1, Greatest common divisor and inverse; Section 9.4, Enhancements for gcd and inverse
  - paper: "Jeffrey Shallit, Origins of the analysis of the Euclidean algorithm, Historia Mathematica 21(4), 1994"
    locator: pages 401 to 419 (Reynaud, Finck and Lamé)
---

The Euclidean algorithm computes the [greatest common divisor](/greatest-common-divisor/) of two integers by replacing the pair $(a, b)$ with $(b, a \bmod b)$ until the second number is zero; the first number is then the gcd. It solves the [GCD of two integers](/gcd-of-two-integers/) problem with at most $2 + \log_\varphi \min(|a|, |b|)$ division steps, where $\varphi \approx 1.618$ is the golden ratio, and consecutive Fibonacci numbers reach this bound. On numbers of $n$ binary digits it uses $O(n^2)$ bit operations with schoolbook division. It is one of the oldest algorithms in use, and the base of [modular inverses](/modular-inverse/), [continued fractions](/continued-fraction/) and fraction arithmetic.

## In plain words

You want the largest number that divides two given numbers. Any number that divides both of them also divides their difference, and so it also divides the remainder when the larger one is divided by the smaller one. So you can throw away the larger number and keep the smaller one and that remainder: the answer does not change.

Repeat this. The numbers get smaller each time, so the process ends. It ends when one of the two numbers is zero. Every number divides zero, so the answer is the other number. The remainders shrink fast: two rounds at least halve the larger number, so even a number with three hundred digits needs fewer than fifteen hundred rounds.

## The problem

The input is two integers $a$ and $b$, of any sign, possibly zero. The output is $\gcd(a, b)$: the largest integer that divides both, which is non-negative. The conventions are $\gcd(a, 0) = |a|$ and $\gcd(0, 0) = 0$. This is the [GCD of two integers](/gcd-of-two-integers/) problem.

**Cost model.** The page states the bounds in two models. On the [word RAM](/word-ram/), the inputs fit in a machine word and a division with remainder costs one step; the bound is then a number of division steps. For [arbitrary-precision](/arbitrary-precision-arithmetic/) inputs of $n$ binary digits, the cost is counted in bit operations, and a division costs time that depends on the lengths of its operands.

## The algorithm

```pseudo id=main
EUCLID(a, b)
L1  a ← |a|, b ← |b|                ▷ the gcd does not depend on signs
L2  while b ≠ 0 do
L3      r ← a mod b                  ▷ 0 ≤ r < b
L4      a ← b
L5      b ← r
L6  return a
```

Line L1 removes the signs, so each later remainder is non-negative and the result is non-negative in each language. Each pass of the loop does one division with remainder (line L3) and shifts the pair. If $a < b$ at the start, the first pass computes $a \bmod b = a$ and only swaps the two numbers. When $b$ reaches $0$, the gcd of the pair is $a$, and line L6 returns it. For $(0, 0)$ the loop does not run and the result is $0$, the convention.

The same loop can be written as a recursion, $\gcd(a, b) = \gcd(b, a \bmod b)$ with $\gcd(a, 0) = a$. The recursion depth is the number of division steps, $O(\log m)$, so recursion is safe here, but the loop needs no stack.

## Example

Compute $\gcd(1071, 462)$.

| pass | $a$ | $b$ | $q = \lfloor a/b \rfloor$ | $r = a \bmod b$ |
|---|---|---|---|---|
| 1 | 1071 | 462 | 2 | 147 |
| 2 | 462 | 147 | 3 | 21 |
| 3 | 147 | 21 | 7 | 0 |
| end | 21 | 0 | | |

The result is $21$, after 3 division steps: $1071 = 3^2 \cdot 7 \cdot 17$ and $462 = 2 \cdot 3 \cdot 7 \cdot 11$, so the gcd is $3 \cdot 7 = 21$. With the arguments swapped, $\gcd(462, 1071)$ takes one more step, the swap $462 \bmod 1071 = 462$.

**The worst case.** Consecutive Fibonacci numbers make each quotient $1$, the smallest possible, so the numbers shrink as slowly as possible. On $(144, 89) = (F_{12}, F_{11})$ the remainders are $55, 34, 21, 13, 8, 5, 3, 2, 1, 0$: ten steps, and the gcd is $1$.

## Correctness

The algorithm keeps the [loop invariant](/loop-invariant/) $\gcd(a, b) = \gcd(a_0, b_0)$ with $a, b \ge 0$, where $a_0, b_0$ are the inputs. Line L1 makes it true, because the gcd does not depend on signs. A pass keeps it by the [GCD recursion theorem](/gcd-recursion-theorem/): for $b > 0$, $\gcd(a, b) = \gcd(b, a \bmod b)$, because $a$ and $b$ have the same common divisors as $b$ and $a - \lfloor a/b \rfloor b$. The value $b$ is a non-negative integer that drops by at least $1$ at each pass, so the loop stops. At exit $b = 0$, and $\gcd(a, 0) = a$. The full proof, with the step bound below, is in the proofs.

## Complexity

**Division steps, worst case.** Let $m = \min(|a|, |b|)$. If $|a| \ge |b| \ge 1$, the loop runs at most $1 + \log_\varphi m$ times, where $\varphi = (1 + \sqrt 5)/2$ and $\log_\varphi m \approx 1.44 \lg m$. If $|a| < |b|$, add one pass for the swap. The proof is Lamé's argument ([Lamé's theorem](/lames-theorem/)): if the loop runs $k$ times on $a > b \ge 1$, then $b \ge F_{k+1}$ and $a \ge F_{k+2}$, by induction on $k$, because each quotient is at least $1$ and so $a \ge b + (a \bmod b)$. Since $F_{k+1} \ge \varphi^{k-1}$, this gives $k \le 1 + \log_\varphi b$. In decimal terms: the number of steps is at most five times the number of decimal digits of the smaller number.

**The bound is tight.** On $(F_{k+2}, F_{k+1})$ the loop runs exactly $k$ times, because $F_{j+1} \bmod F_j = F_{j-1}$. So the worst case is $\Theta(\log m)$ steps. With $10^6$ as the largest input, the worst pair is $(832040, 514229) = (F_{30}, F_{29})$, with 28 steps.

**Best case.** If $|b|$ divides $|a|$, one pass ends the loop, and if $b = 0$, none. So the best case is $\Theta(1)$.

**Average case.** Over pairs of random integers, the number of steps grows as $\frac{12 \ln 2}{\pi^2} \ln N \approx 0.843 \ln N$ for inputs up to $N$ (Heilbronn, Dixon; see Knuth, Section 4.5.3). For random $a, b \le 10^6$ the mean is about $11.7$ steps, against the worst case of 28.

**Time on the word RAM.** Each pass costs $O(1)$ word operations, so the time is $\Theta(\log m)$ in the worst case and $\Theta(1)$ in the best case. The extra space is $\Theta(1)$ words.

**Bit operations.** For inputs of $n$ binary digits, a schoolbook division of $r_{i-1}$ by $r_i$ with quotient $q_i$ costs $O((1 + \lg q_i) \cdot n)$ bit operations. The quotients satisfy $q_1 q_2 \cdots q_k \le a$, because $r_{i-1} \ge q_i r_i$ for each $i$. So $\sum \lg q_i \le n$, and with $k = O(n)$ passes the total is $O(n \cdot (k + \sum \lg q_i)) = O(n^2)$. The extra space is $O(n)$ bits. The proof is in `proofs/complexity.md`.

| measure | bound |
|---|---|
| division steps, worst | $\le 1 + \log_\varphi m$ (plus one if $|a| < |b|$), tight for Fibonacci pairs |
| time on the word RAM | worst $\Theta(\log m)$, best $\Theta(1)$ |
| extra space | $\Theta(1)$ words |
| bit operations, schoolbook division | $O(n^2)$ |
| bit operations, [half-GCD](/half-gcd/) | $O(M(n) \log n)$ |

## Properties

- **Deterministic and iterative.** No random choices, no recursion, and a constant number of variables.
- **Division based.** Each step needs a division with remainder. On hardware where division is slow, [binary GCD](/binary-gcd/) replaces it with shifts and subtractions.
- **The quotients carry information.** The sequence $q_1, q_2, \ldots$ is the [continued fraction](/continued-fraction/) of $a/b$. The [extended Euclidean algorithm](/extended-euclidean-algorithm/) uses the same quotients to build Bézout coefficients.
- **Works in other rings.** The same loop computes gcds in each [Euclidean domain](/euclidean-domain/), for example of polynomials over a field ([polynomial GCD](/polynomial-gcd/)).

## Variants and improvements

- **Subtractive version.** Euclid's form replaces the larger number by the difference, $(a, b) \to (a - b, b)$ for $a \ge b$. It needs no division, but it takes $a$ steps on $(a, 1)$, so it is exponential in the input length. The division is a batch of subtractions.
- **Least absolute remainder.** Choose $r$ with $|r| \le b/2$, that is $r = a \bmod b$ or $r - b$, and continue with $|r|$. Then $b$ at least halves at each step, so at most $\lfloor \lg m \rfloor + 1$ steps are needed.
- **[Extended Euclidean algorithm](/extended-euclidean-algorithm/).** Also returns $x, y$ with $ax + by = \gcd(a, b)$, at the same asymptotic cost.
- **[Binary GCD](/binary-gcd/) (Stein's algorithm).** Uses parity tests, shifts and subtractions. Also $O(n^2)$ bit operations.
- **[Lehmer's GCD](/lehmers-gcd/).** Runs the algorithm on the leading words of big numbers and applies many steps at once with a $2 \times 2$ matrix. Faster by a constant factor for numbers of many words.
- **[Half-GCD](/half-gcd/).** A divide-and-conquer form that reaches $O(M(n) \log n)$ bit operations, where $M(n)$ is the cost of [multiplying](/integer-multiplication/) two $n$-digit numbers.
- **[GCD of an array](/gcd-of-array/).** Fold the algorithm over the elements, since $\gcd(a, b, c) = \gcd(\gcd(a, b), c)$.

## When to use it

Use it as the default gcd for machine integers: the loop is short, it has no branch on the data except the loop test, and $\Theta(\log m)$ divisions are few. Use [binary GCD](/binary-gcd/) when division is much slower than shifts, for example on small processors or for numbers of a few words. For numbers of thousands of digits, use [Lehmer's GCD](/lehmers-gcd/) or the [half-GCD](/half-gcd/), as the libraries for big numbers do. When the coefficients of Bézout's identity are needed, for example for a [modular inverse](/modular-inverse/), use the [extended Euclidean algorithm](/extended-euclidean-algorithm/).

## Pitfalls

- **Negative results.** In C, Java and Go, `%` rounds the quotient toward zero, so the remainder takes the sign of $a$, and a loop without line L1 can return $-\gcd$: on $(-12, 18)$ it returns $-6$. Take absolute values first (line L1), or return $|a|$ at line L6.
- **The absolute value of the most negative integer.** In 64-bit two's complement, $|-2^{63}|$ does not fit, so line L1 overflows on $(-2^{63}, b)$. Use unsigned arithmetic for the absolute values.
- **The wrong loop test.** A loop that tests $a \ne 0$ and divides by $b$, or that swaps the lines L4 and L5, divides by zero on inputs such as $(5, 0)$. The test must be on the divisor, as in line L2.
- **The subtractive form on unequal inputs.** Replacing line L3 by a subtraction makes $\gcd(10^{18}, 1)$ take $10^{18}$ steps.
- **Overflow in the least common multiple.** $\operatorname{lcm}(a, b) = |ab| / \gcd(a, b)$ overflows in the product even when the result fits. Compute $|a| / \gcd(a, b) \cdot |b|$ instead; see [least common multiple](/least-common-multiple/).

## Implementations

## History

The algorithm is in Euclid's *Elements*, Book VII, Propositions 1 and 2, written about 300 BC, as a process of repeated subtraction of the smaller magnitude from the larger. Knuth (Section 4.5.2) discusses this history and calls it the oldest nontrivial algorithm that has survived to the present day. The first bounds on its number of steps came in the nineteenth century: Shallit traces bounds by Reynaud and by Finck, and Lamé's 1844 proof that the number of steps is at most five times the number of decimal digits of the smaller number, by the comparison with Fibonacci numbers given above. Lamé's result is often cited as an early analysis of the running time of an algorithm. The average number of steps was found later, by Heilbronn and by Dixon, as Knuth reports in Section 4.5.3.

## References
