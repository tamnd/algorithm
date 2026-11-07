---
tag: 22K1SK
kind: problem
slug: fibonacci-numbers
name: Fibonacci numbers
aliases:
- Polynomial-time Fibonacci algorithm
area: algebra/integer-arithmetic
level: intro
summary: Computing the sequence in which each number is the sum of the two before it, with methods ranging from recursion to matrix powers.
model: multitape-turing-machine
complexity:
  vars: {n: the index of the Fibonacci number, M: the cost of multiplying two numbers of the given length in binary digits}
  time: {worst: O(M(n))}
prereqs: [recurrence-relation, integer-multiplication]
see_also: [fibonacci-fast-doubling, matrix-fibonacci, binet-formula, memoization, integer-exponentiation, linear-recurrence-nth-term, pisano-period, cassini-identity]
sources:
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2008
    locator: Chapter 0, Prologue, Section 0.2, Enter Fibonacci (the exponential recursion, the polynomial algorithm, the cost of the additions of long numbers, and the matrix form in the exercises)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.8, Fibonacci numbers (the matrix identity, Binet's formula, and the identities for F(m+n))
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.6, Fibonacci numbers (Cassini's identity, the addition law, gcd(F(m), F(n)) = F(gcd(m, n)))
  - paper: doi:10.1016/S0020-0190(00)00112-5
    title: Daisuke Takahashi, A fast algorithm for computing large Fibonacci numbers, Information Processing Letters 75(6), 2000
    locator: pp. 243 to 246 (the method by Lucas numbers with two squarings per bit, and the comparison with the matrix and doubling methods)
  - url: https://www.cs.utexas.edu/~EWD/ewd06xx/EWD654.PDF
    title: Edsger W. Dijkstra, In honour of Fibonacci, EWD654, 1978
    locator: the whole note (the doubling formulas for F(2n) and F(2n+1))
---

The Fibonacci numbers are defined by $F_0 = 0$, $F_1 = 1$ and $F_n = F_{n-1} + F_{n-2}$, and the computational problem is to compute $F_n$ for a given $n$. The problem is a standard first example of how much the choice of algorithm matters: the direct recursion takes time exponential in $n$, the loop over the sequence takes $\Theta(n^2)$ bit operations, and methods based on squaring ([matrix powers](/matrix-fibonacci/) or [fast doubling](/fibonacci-fast-doubling/)) take $O(M(n))$, the cost of one [multiplication](/integer-multiplication/) of $n$-digit numbers. Since $F_n$ has about $0.694 n$ binary digits, the last bound is within a constant factor of the cost of multiplying numbers of the size of the answer.

## In plain words

Start with 0 and 1, and get each new number by adding the two before it: 0, 1, 1, 2, 3, 5, 8, 13, and so on. The task is to find the number at a given position in this list.

The obvious recursive program asks for the two numbers before, and each of those asks for two more, so the same numbers are computed again and again, and the work grows as fast as the numbers themselves. A simple loop that walks along the list does much better.

The numbers grow fast, though: the millionth one has over two hundred thousand decimal digits. The fastest methods jump ahead by doubling the position at each step, using a few multiplications of large numbers, so they reach the millionth number in about twenty steps.

## Definition

**Input.** An integer $n \ge 0$.

**Output.** The integer $F_n$, defined by $F_0 = 0$, $F_1 = 1$ and $F_n = F_{n-1} + F_{n-2}$ for $n \ge 2$.

**Size of the output.** By [Binet's formula](/binet-formula/), $F_n = \frac{\varphi^n - \psi^n}{\sqrt 5}$ with $\varphi = \frac{1 + \sqrt 5}{2}$ and $\psi = \frac{1 - \sqrt 5}{2}$. Since $|\psi^n / \sqrt 5| < \frac12$, $F_n$ is the integer nearest to $\varphi^n / \sqrt 5$, and it has $n \log_2 \varphi + O(1) \approx 0.6942\, n$ binary digits. The input has only $\log_2 n$ digits, so time polynomial in the input length is impossible; the measure is the cost in terms of $n$, which is linear in the output length.

**Cost model.** Bit operations on a multitape Turing machine, or limb operations on a word RAM with words of $w$ bits, where an addition of $n$-digit numbers costs $\Theta(n)$ bit operations ($\Theta(n/w)$ limb operations) and a product costs $M(n)$.

## Variants

- **Modulo $m$.** Compute $F_n \bmod m$. The numbers stay below $m$, and the doubling methods use $O(\log n)$ products modulo $m$. The sequence modulo $m$ is periodic, with the [Pisano period](/pisano-period/), 60 for $m = 10$.
- **All of $F_0, \ldots, F_n$.** The loop is optimal up to a constant: the output has $\Theta(n^2)$ digits in total.
- **Negative indices.** The recurrence extends backward with $F_{-n} = (-1)^{n+1} F_n$.
- **Lucas numbers** $L_0 = 2$, $L_1 = 1$ satisfy the same recurrence and $L_n = \varphi^n + \psi^n$; Takahashi's method computes $F_n$ from them.
- **General linear recurrences** of order $k$ with constant coefficients: the $n$th term by powers of a $k \times k$ companion matrix, or by polynomial arithmetic modulo the characteristic polynomial ([linear recurrence nth term](/linear-recurrence-nth-term/), [Bostan-Mori](/bostan-mori-algorithm/)).

## Examples

**The first values.**

| $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $F_n$ | 0 | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 | 34 | 55 | 89 | 144 | 233 | 377 | 610 |

**Larger values.** $F_{100} = 354224848179261915075$. $F_{1000}$ has 209 decimal digits and 694 binary digits. $F_{10^6}$ has 208988 decimal digits and 694241 binary digits.

**The naive recursion.** The program `fib(n) = fib(n-1) + fib(n-2)` with base cases 0 and 1 makes $C(n) = 1 + C(n-1) + C(n-2)$ calls, with $C(0) = C(1) = 1$, which solves to $C(n) = 2F_{n+1} - 1$. For $n = 30$ that is $2 \cdot 1346269 - 1 = 2692537$ calls, to compute $F_{30} = 832040$.

**Doubling.** The identities $F_{2k} = F_k (2F_{k+1} - F_k)$ and $F_{2k+1} = F_k^2 + F_{k+1}^2$ give $(F_{10}, F_{11}) = (55, 89)$ from $(F_5, F_6) = (5, 8)$: $5 \cdot (16 - 5) = 55$ and $25 + 64 = 89$.

**Floating point.** Rounding $\varphi^n / \sqrt 5$ in IEEE double precision gives the correct $F_n$ for $n \le 70$ and fails first at $n = 71$. Here $F_{71} = 308061521170129$ still fits in the 53-bit significand, but the rounding error of the computed $\varphi^{71}/\sqrt 5$ is larger than $\frac12$. Binet's formula is exact only with $\Theta(n)$ digits of precision, which costs as much as the integer methods.

**Identities used as checks.** Cassini's identity $F_{n+1} F_{n-1} - F_n^2 = (-1)^n$: for $n = 10$, $89 \cdot 34 - 55^2 = 1$. The gcd law $\gcd(F_m, F_n) = F_{\gcd(m, n)}$: $\gcd(F_{30}, F_{20}) = F_{10} = 55$.

## Known algorithms

| algorithm | arithmetic operations | bit cost |
|---|---|---|
| naive recursion | $F_{n+1} - 1$ additions, $\Theta(\varphi^n)$ | $\Theta(\varphi^n)$ times the size of the numbers |
| loop, or recursion with [memoization](/memoization/) | $n - 1$ additions | $\Theta(n^2)$, from additions of $O(n)$ digits |
| [matrix powers](/matrix-fibonacci/) of $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ | $O(\log n)$ products of $2 \times 2$ matrices | $O(M(n))$ |
| [fast doubling](/fibonacci-fast-doubling/) | 2 or 3 multiplications per bit of $n$ | $O(M(n))$, with a smaller constant |
| Takahashi's method by Lucas numbers | about 2 squarings per bit of $n$ | $O(M(n))$, squarings are cheaper than products |
| Binet's formula with exact real arithmetic | $O(\log n)$ operations on $\Theta(n)$-digit reals | $O(M(n))$, with larger constants |

The squaring methods are $O(M(n))$ for the same reason as [integer exponentiation](/integer-exponentiation/): the products at the step $j$ from the end have about $0.694 n / 2^j$ digits, and the sizes form a geometric series, so the last step dominates. With schoolbook multiplication, $M(n) = \Theta(n^2)$ and the doubling methods are only a constant factor faster than the loop. Which method is fastest for a given $n$ is a measured fact of the machine and the library, not a theorem; the loop wins for small $n$ because additions are cheap.

## Bounds

**Lower bound.** Any algorithm writes the $\Theta(n)$ digits of $F_n$, so $\Omega(n)$ bit operations are needed.

**Upper bound.** $O(M(n))$ by the doubling methods, which is $O(n \log n)$ with the bound of [integer multiplication](/integer-multiplication/) on the multitape Turing machine.

**Relation to multiplication.** It is not known that computing $F_n$ is as hard as multiplying $n$-digit numbers. All known algorithms faster than $\Theta(n^2)$ use fast multiplication, and the gap between $\Omega(n)$ and $O(n \log n)$ is open, as for multiplication itself.

## Reductions

- **To matrix powering.** $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$, by induction on $n$. So $F_n$ is one entry of a power, and the methods of [integer exponentiation](/integer-exponentiation/) apply in the ring of $2 \times 2$ integer matrices.
- **To powering in $\mathbb{Z}[\varphi]$.** $\varphi^n = F_n \varphi + F_{n-1}$, since $\varphi^2 = \varphi + 1$. Powering $a + b\varphi$ modulo $\varphi^2 - \varphi - 1$ is the doubling method in another form.
- **To linear recurrences.** Fibonacci is the order-2 case of computing the $n$th term of a linear recurrence with constant coefficients.

## Applications

- The analysis of the [Euclidean algorithm](/euclidean-algorithm/): consecutive Fibonacci numbers are its worst case (Lamé's theorem). For $(144, 89) = (F_{12}, F_{11})$ it takes 10 division steps.
- The analysis of [Fibonacci heaps](/fibonacci-heap/), whose node degrees are bounded through $F_{k+2} \ge \varphi^k$.
- [Fibonacci search](/fibonacci-search/) and [Zeckendorf representations](/zeckendorf-theorem/) of integers as sums of nonconsecutive Fibonacci numbers.
- Benchmarks and teaching examples for recursion, memoization and big-integer arithmetic.

## References
