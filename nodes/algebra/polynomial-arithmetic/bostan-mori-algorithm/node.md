---
tag: 8WEKFW
kind: algorithm
slug: bostan-mori-algorithm
name: Bostan-Mori algorithm
aliases:
- Bostan-Mori method
- Graeffe-type coefficient extraction
area: algebra/polynomial-arithmetic
level: advanced
summary: Computes the n-th coefficient of a rational function by halving n and multiplying by the conjugate denominator.
solves: [linear-recurrence-nth-term]
model: blum-shub-smale-machine
complexity:
  vars: {d: the degree of the denominator Q, N: the index of the wanted coefficient, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(d) log N), best: O(M(d) log N)}
  space: {extra: O(d)}
  ring_operations: {worst: 2M(d + 1)(log2 N + 1) + O(d log N)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 2021
  people: [Alin Bostan, Ryuhei Mori]
  note: Bostan and Mori published the method in 2021 as a simpler and faster way to get the N-th term of a linear recurrence than the method of Fiduccia from 1985.
prereqs: [polynomial, linear-recurrence-nth-term, dense-polynomial-representation]
see_also: [linear-recurrence-nth-term, fft-polynomial-multiplication, newton-power-series-inversion, matrix-exponentiation, fibonacci-fast-doubling, kronecker-substitution, berlekamp-massey]
sources:
  - paper: doi:10.1137/1.9781611976496.14
    title: Alin Bostan and Ryuhei Mori, A simple and fast algorithm for computing the N-th term of a linearly recurrent sequence, Symposium on Simplicity in Algorithms (SOSA 2021), 118-132
    locator: the algorithm on rational power series and its comparison with Fiduccia's algorithm
  - paper: doi:10.1137/0214007
    title: Charles M. Fiduccia, An efficient formula for linear recurrences, SIAM Journal on Computing 14(1), 106-112, 1985
    locator: the earlier method by powers of x modulo the characteristic polynomial
---

The Bostan-Mori algorithm computes the coefficient of $x^N$ in the power series $P(x)/Q(x)$, where $P$ and $Q$ are polynomials and $Q(0)$ is a unit. Each step multiplies the numerator and the denominator by $Q(-x)$. Then the denominator has only even powers, the index $N$ can be halved, and the numerator keeps only its even or only its odd coefficients. After about $\log_2 N$ steps, with two polynomial products in each, the answer is the constant term. Since every linear recurrence with constant coefficients has a rational generating function, this gives the [$N$-th term of a linear recurrence](/linear-recurrence-nth-term/) in $O(M(d) \log N)$ operations.

Notation: $R$ is a commutative ring, polynomials in $R[x]$ are lists of coefficients with the constant term first, $Q \in R[x]$ has degree $d$ and $Q(0)$ a unit, and $[x^N] F$ is the coefficient of $x^N$ in a power series $F$. $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Costs count ring operations in the algebraic complexity model.

## In plain words

Suppose you want one far coefficient of a fraction of two polynomials, for example the ten millionth Fibonacci number modulo a prime. Multiply the top and the bottom of the fraction by the bottom with the sign of every odd power flipped. The fraction does not change, but the new bottom has only even powers. So the far coefficient comes from only half of the top: the even half if the index is even, the odd half if it is odd. Keep that half, rename the square of the variable as the variable, and halve the index. Each round halves the index, so a few dozen rounds reach index zero, where the answer is the constant term of the top divided by that of the bottom.

## The problem

**Input:** polynomials $P, Q \in R[x]$ with $Q(0)$ a unit, and an integer $N \ge 0$.

**Output:** $[x^N]\, P(x)/Q(x)$.

The series $P/Q$ is defined because $Q(0)$ is a unit, so $Q$ is invertible in $R[[x]]$. In the main use, $Q = 1 - c_1 x - \cdots - c_d x^d$ comes from the recurrence $a_i = c_1 a_{i-1} + \cdots + c_d a_{i-d}$, and $P$ has degree less than $d$.

## The algorithm

For a polynomial $U = \sum_i u_i x^i$, write $U_{\mathrm{even}}(y) = \sum_i u_{2i} y^i$ and $U_{\mathrm{odd}}(y) = \sum_i u_{2i+1} y^i$, so that $U(x) = U_{\mathrm{even}}(x^2) + x\, U_{\mathrm{odd}}(x^2)$. The product $Q(x)Q(-x)$ is unchanged when $x$ is replaced by $-x$, so it has only even powers. The identity behind the algorithm is

$$\frac{P(x)}{Q(x)} = \frac{P(x)\, Q(-x)}{Q(x)\, Q(-x)} = \frac{U_{\mathrm{even}}(x^2) + x\, U_{\mathrm{odd}}(x^2)}{V(x^2)}, \qquad U = P(x) Q(-x),\ V(x^2) = Q(x) Q(-x).$$

The first part has only even powers of $x$ and the second only odd powers, so $[x^{2M}]\, P/Q = [y^M]\, U_{\mathrm{even}}/V$ and $[x^{2M+1}]\, P/Q = [y^M]\, U_{\mathrm{odd}}/V$.

```pseudo id=main
BOSTAN-MORI(P, Q, N)
L1  while N ≥ 1 do
L2      Q⁻ ← Q(-x)                         ▷ flip the sign of the odd coefficients
L3      U ← P · Q⁻
L4      V ← Q · Q⁻                          ▷ only even powers
L5      P ← U_even if N is even, else U_odd
L6      Q ← V_even
L7      N ← ⌊N/2⌋
L8  return P(0) / Q(0)
```

The implementation also stops early when $P$ becomes zero. For a recurrence with initial values $a_0, \ldots, a_{d-1}$, take $Q = 1 - \sum_{i=1}^d c_i x^i$ and $P = (a_0 + a_1 x + \cdots + a_{d-1} x^{d-1}) \cdot Q \bmod x^d$.

## Example

The Fibonacci numbers have $\sum_n F_n x^n = x/(1 - x - x^2)$. Compute $F_{10}$ over $\mathbb{Z}$.

| step | $N$ before | $U = P \cdot Q(-x)$ | new $P$ | new $Q$ | $N$ after |
|---|---|---|---|---|---|
| 1 | 10 | $x + x^2 - x^3$ | $y$ (even part) | $1 - 3y + y^2$ | 5 |
| 2 | 5 | $x + 3x^2 + x^3$ | $1 + y$ (odd part) | $1 - 7y + y^2$ | 2 |
| 3 | 2 | $1 + 8x + 8x^2 + x^3$ | $1 + 8y$ (even part) | $1 - 47y + y^2$ | 1 |
| 4 | 1 | $1 + 55x + 377x^2 + 8x^3$ | $55 + 8y$ (odd part) | $1 - 2207y + y^2$ | 0 |

Line L8 returns $55/1 = 55 = F_{10}$. The middle coefficients $3, 7, 47, 2207$ of the denominators are the Lucas numbers $L_2, L_4, L_8, L_{16}$: each step squares the roots of $Q$. A script checked every row.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The invariant is that $[x^N]\, P/Q$, for the current $P$, $Q$ and $N$, equals the wanted coefficient, and that $Q(0)$ is a unit. One step keeps it by the identity above: $Q(-x)$ has the same constant term as $Q$, so $V(0) = Q(0)^2$ is a unit, and the even-odd split of $U$ picks the part that holds $x^N$. When $N = 0$, the coefficient of $x^0$ in $P/Q$ is $P(0)\, Q(0)^{-1}$.

## Complexity

The bounds are proved and count ring operations.

- **Steps.** $N$ is halved in each step, so there are $\lfloor \log_2 N \rfloor + 1$ steps for $N \ge 1$.
- **Degrees.** If $\deg P < d = \deg Q$, then $\deg U \le 2d - 1$ and $\deg V = 2d$ at most, so the new $P$ has degree less than $d$ and the new $Q$ has degree at most $d$. The degrees never grow.
- **One step.** Two products of polynomials with at most $d + 1$ coefficients, so $2M(d + 1)$, and $O(d)$ for the signs and the splits. In total, $2M(d + 1)(\log_2 N + 1) + O(d \log N)$, which is $O(M(d) \log N)$.
- **Space.** $O(d)$ ring elements.
- **Comparison.** Fiduccia's method computes $x^N \bmod \chi$ for the characteristic polynomial $\chi$ by binary powering. Each squaring modulo $\chi$ is one product and one division, about $3M(d)$ with a stored inverse. With fast Fourier multiplication, Bostan-Mori can also reuse transforms: the values of $Q(-x)$ at the $2K$-th roots of unity are those of $Q(x)$ at the negated points, so $Q(-x)$ needs no transform of its own.

**In practice (observed).** The algorithm is short, has no division except at the end, and is widely used in competitive programming for indices up to about $10^{18}$, modulo primes suited to the number theoretic transform. Bostan and Mori report that it is faster than Fiduccia's method. The gain depends on the multiplication and on the machine.

## Properties

- **No inverses except one.** Only $Q(0)$ must be invertible, and only at the end. Over $\mathbb{Z}$ with $Q(0) = \pm 1$, all steps stay in $\mathbb{Z}$.
- **Graeffe's root squaring.** $V(x^2) = Q(x) Q(-x)$ is the step of Graeffe's method: if $Q = \prod (1 - \alpha_i x)$, then $V = \prod (1 - \alpha_i^2 y)$.
- **Any numerator.** $\deg P \ge \deg Q$ is allowed; the degree of $P$ then shrinks by about half in each step until it is less than $d$.
- **Deterministic and iterative.** No recursion and no randomness.

## Variants and improvements

- **Powers modulo a polynomial.** Bostan and Mori derive from the same idea a way to compute $x^N \bmod Q$ and powers of matrices, by the transposition principle.
- **Fewer transforms.** With FFT multiplication, Bostan and Mori also show how to save discrete Fourier transforms between the steps, which lowers the constant further.
- **Other series.** For algebraic power series over finite prime fields, other methods compute the $N$-th coefficient quickly; they do not use this halving step.

## When to use it

Use the Bostan-Mori algorithm for one far term of a linear recurrence with constant coefficients, or one far coefficient of a rational power series, when $d$ is moderate or large and $N$ is large. For $d = 2$ or $3$, [matrix exponentiation](/matrix-exponentiation/) or [fast doubling for Fibonacci numbers](/fibonacci-fast-doubling/) is just as good. If the recurrence is not known, find it first with [Berlekamp-Massey](/berlekamp-massey/) from $2d$ terms.

## Pitfalls

- **Wrong numerator.** $P$ is $(a_0 + \cdots + a_{d-1} x^{d-1}) Q \bmod x^d$, not the list of initial values. Forgetting the truncation or the product gives a different sequence.
- **Using the wrong half.** For odd $N$ keep the odd coefficients $u_1, u_3, \ldots$; for even $N$ the even ones $u_0, u_2, \ldots$.
- **Not halving $Q$.** The new denominator is $V_{\mathrm{even}}$, the coefficients $v_0, v_2, v_4, \ldots$, not $V$ itself.
- **Dividing by $Q(0)$ when it is not $1$.** $Q(0)$ is squared in each step. Divide by the final $Q(0)$, not by the original one.
- **Coefficient growth over $\mathbb{Z}$.** The coefficients roughly double in length per step; for exact integers this makes the bit cost much larger than the operation count. Work modulo a prime when possible.

## Implementations

## History

Charles Fiduccia showed in 1985 that the $N$-th term of a linear recurrence of order $d$ can be computed with $O(M(d) \log N)$ operations by working with $x^N$ modulo the characteristic polynomial, which improved on powering the $d \times d$ companion matrix. Alin Bostan and Ryuhei Mori published their method in 2021 at the Symposium on Simplicity in Algorithms. It works directly on the rational generating function, has the same complexity up to a constant factor, and is simpler and faster in practice. The step $Q(x) Q(-x)$ is the root-squaring step of the method of Dandelin, Lobachevsky and Graeffe for polynomial roots.

## References
