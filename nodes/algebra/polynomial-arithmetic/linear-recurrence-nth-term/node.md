---
tag: 8X8ES6
kind: problem
slug: linear-recurrence-nth-term
name: n-th term of a linear recurrence
aliases:
- coefficient of a rational generating function
- N-th term of a C-finite sequence
- jumping ahead in a linear recurrence
area: algebra/polynomial-arithmetic
level: advanced
summary: Compute the n-th term of a linear recurrence with constant coefficients in O(M(d) log n) time.
model: blum-shub-smale-machine
complexity:
  vars: {d: the order of the recurrence, N: the index of the wanted term, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(d) log N)}
prereqs: [polynomial, linear-recurrences-with-constant-coefficients, generating-functions, matrix-exponentiation]
see_also: [bostan-mori-algorithm, matrix-exponentiation, fibonacci-fast-doubling, fibonacci-numbers, berlekamp-massey, cayley-hamilton-theorem, fast-polynomial-division, binary-exponentiation]
sources:
  - paper: doi:10.1137/0214007
    title: Charles M. Fiduccia, An efficient formula for linear recurrences, SIAM Journal on Computing 14(1), 106-112, 1985
    locator: the N-th term from x^N modulo the characteristic polynomial
  - paper: doi:10.1137/1.9781611976496.14
    title: Alin Bostan and Ryuhei Mori, A simple and fast algorithm for computing the N-th term of a linearly recurrent sequence, Symposium on Simplicity in Algorithms (SOSA 2021), 118-132
    locator: the problem statement, the survey of earlier methods, and the new algorithm
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 4.7, Recurrence relations
---

The problem asks for the term $a_N$ of a sequence that satisfies a linear recurrence $a_i = c_1 a_{i-1} + \cdots + c_d a_{i-d}$ with constant coefficients, given the coefficients and the first $d$ terms, when $N$ is much larger than $d$. Running the recurrence forward costs $\Theta(N d)$ operations. Powering the companion matrix costs $O(d^\omega \log N)$. Working with polynomials, either with $x^N$ modulo the characteristic polynomial (Fiduccia, 1985) or with the rational generating function (Bostan and Mori, 2021), costs $O(M(d) \log N)$.

Notation: $R$ is a commutative ring, $c_1, \ldots, c_d \in R$ and $a_0, \ldots, a_{d-1} \in R$, the characteristic polynomial is $\chi(x) = x^d - c_1 x^{d-1} - \cdots - c_d$, and its reversal is $Q(x) = 1 - c_1 x - \cdots - c_d x^d$. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$, and $\omega$ is an exponent of matrix multiplication. Costs count ring operations in the algebraic complexity model.

## In plain words

Many counting questions give a sequence in which each term is a fixed mix of the few terms before it. The Fibonacci numbers are the best known case: each term is the sum of the two before it. To get the term at a huge position, such as the trillionth, you cannot step through all earlier terms. The fast methods jump: from the rule for one position they get the rule for twice that position in a few steps of polynomial arithmetic. So the work grows with the number of digits of the position, not with the position itself.

## Definition

**Input:** an order $d \ge 1$, coefficients $c_1, \ldots, c_d \in R$, initial values $a_0, \ldots, a_{d-1} \in R$, and an index $N \ge 0$.

**Output:** $a_N$, where $a_i = \sum_{j=1}^{d} c_j a_{i-j}$ for all $i \ge d$.

Equivalent forms:

- **Rational generating function.** $\sum_{i \ge 0} a_i x^i = P(x)/Q(x)$ with $P = (a_0 + \cdots + a_{d-1} x^{d-1})\, Q \bmod x^d$, so $\deg P < d$. So the problem is to find $[x^N]\, P/Q$, the coefficient of $x^N$ in a rational power series with $Q(0) = 1$.
- **Companion matrix.** With the state $s_i = (a_i, \ldots, a_{i+d-1})^T$ and the $d \times d$ companion matrix $C$, $s_{i+1} = C s_i$, so $a_N$ is the first entry of $C^N s_0$.
- **Powers modulo $\chi$.** If $x^N \bmod \chi = \sum_{i<d} r_i x^i$, then $a_N = \sum_{i<d} r_i a_i$. The reason is that $x \mapsto$ shift is a linear map on sequences, and $\chi$ maps every solution to zero (Cayley-Hamilton for $C$).

## Variants

- **Inhomogeneous recurrences.** $a_i = \sum_j c_j a_{i-j} + b(i)$ with $b$ a polynomial or an exponential in $i$ becomes a homogeneous recurrence of higher order.
- **Many terms.** All of $a_0, \ldots, a_N$ cost $O(M(N))$ by [power series inversion](/newton-power-series-inversion/) of $Q$ and one product, or $\Theta(N d)$ by direct iteration.
- **Modular terms.** $a_N \bmod p$, the most common form in practice, is the problem over $R = \mathbb{Z}/p\mathbb{Z}$.
- **Unknown recurrence.** Given $2d$ terms only, [Berlekamp-Massey](/berlekamp-massey/) finds the shortest recurrence first.
- **Holonomic sequences.** Recurrences with polynomial coefficients, such as $n!$, are a different problem with different methods, near $\sqrt{N}$ operations instead of $\log N$; see [factorials modulo a prime](/factorial-modulo-prime/).

## Examples

- **Fibonacci numbers.** $d = 2$, $c = (1, 1)$, $a_0 = 0$, $a_1 = 1$, and $\chi = x^2 - x - 1$. Binary powering modulo $\chi$ for $N = 10 = 1010_2$ gives $x$, $x^2 \equiv x + 1$, $x^5 \equiv 5x + 3$, $x^{10} \equiv (5x + 3)^2 \equiv 55x + 34$. So $a_{10} = 34 a_0 + 55 a_1 = 55$. In general $x^N \equiv F_N x + F_{N-1}$. The generating function is $x/(1 - x - x^2)$, and the [Bostan-Mori algorithm](/bostan-mori-algorithm/) page traces the same value with four halvings.
- **Tribonacci numbers.** $c = (1, 1, 1)$ with $a = (0, 0, 1)$ gives $0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, \ldots$, with generating function $x^2/(1 - x - x^2 - x^3)$.
- **Tilings.** The number of ways to tile a $2 \times n$ board with dominoes is $F_{n+1}$. Tiling counts for boards of fixed width and walks in a fixed graph are linear recurrences, with order up to the number of states.
- **Pseudorandom generators.** A linear feedback shift register over $\mathbb{Z}/2\mathbb{Z}$ is a linear recurrence; jumping ahead $N$ steps is this problem.

A script checked the Fibonacci powers and the Tribonacci terms.

## Known algorithms

| method | cost | notes |
|---|---|---|
| direct iteration | $\Theta(N d)$ | best for small $N$ |
| [matrix exponentiation](/matrix-exponentiation/) of the companion matrix | $O(d^\omega \log N)$ | simple; $O(d^3 \log N)$ with schoolbook products |
| Fiduccia: $x^N \bmod \chi$ by [binary exponentiation](/binary-exponentiation/) | $O(M(d) \log N)$ | one product and one [fast division](/fast-polynomial-division/) per step, about $3M(d)$ |
| [Bostan-Mori](/bostan-mori-algorithm/) | $O(M(d) \log N)$ | two products per step, no division |
| [fast doubling](/fibonacci-fast-doubling/) for $d = 2$ | $O(\log N)$ | special formulas for Fibonacci and Lucas numbers |

For $d = 1$ the problem is one power, $a_N = c_1^N a_0$, by binary exponentiation.

## Bounds

- **Upper bound.** $O(M(d) \log N)$ ring operations, which is $O(d \log d \log N)$ when the ring supports fast Fourier multiplication. This is proved for both polynomial methods.
- **Lower bound.** Any method must read the $2d$ inputs, so $\Omega(d)$ operations. For $d = 1$ the problem is computing $c^N$, which needs at least $\log_2 N$ multiplications in a straight-line program in the indeterminate $c$, since each product at most doubles the degree. No better general lower bound is known to us.
- **Bit cost over $\mathbb{Z}$.** The term $a_N$ can have $\Theta(N)$ digits, so exact integer answers cost at least linear time in $N$; the bounds above are useful mainly modulo $m$ or over finite fields.

## Reductions

- **Recurrence to rational series.** The term $a_N$ is $[x^N]\, P/Q$, as in the definition; conversely, the coefficients of a rational series $P/Q$ with $Q = 1 - \sum_j c_j x^j$ satisfy $a_i = \sum_j c_j a_{i-j}$ for all $i \ge \max(d, \deg P + 1)$, because $Q \cdot \sum_i a_i x^i = P$ has no terms of degree above $\deg P$.
- **Recurrence to polynomial powering.** $a_N$ is a linear form in the coefficients of $x^N \bmod \chi$, so the problem reduces to modular exponentiation in $R[x]/(\chi)$.
- **Matrix powers.** For any $d \times d$ matrix $A$, an entry of $A^N v$ satisfies a linear recurrence of order at most $d$, given by the characteristic polynomial of $A$ (Cayley-Hamilton). So one far entry of $A^N v$ reduces to this problem after computing that polynomial.

## Applications

- **Combinatorics.** Counting words of a regular language, tilings, and walks in graphs of fixed size, all modulo a prime.
- **Competitive programming.** Dynamic programs with constant transitions and very large step counts are solved through the recurrence of the sequence they produce.
- **Pseudorandom number generators.** Jumping ahead in linear feedback shift registers and in linear congruential generators, for example to give parallel streams.
- **Cryptanalysis and coding.** Linear complexity of sequences, together with [Berlekamp-Massey](/berlekamp-massey/).
- **Computer algebra.** Coefficients of rational functions, and the high order lifting and polynomial powering methods that Bostan and Mori derive from the same idea.

## References
