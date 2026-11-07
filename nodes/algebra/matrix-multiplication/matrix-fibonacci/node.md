---
tag: PJGV8M
kind: technique
slug: matrix-fibonacci
name: Matrix exponentiation for Fibonacci numbers
aliases:
- Matrix Fibonacci computation
- Fibonacci Q-matrix method
- Fibonacci by matrix powers
area: algebra/matrix-multiplication
level: core
summary: Computes the nth Fibonacci number, or the nth term of any linear recurrence with constant coefficients, by raising a small matrix to a power with repeated squaring, in O(log n) matrix products.
prereqs: [fibonacci-numbers, matrix-exponentiation]
see_also: [fibonacci-fast-doubling, linear-recurrence-nth-term, matrix-power, cassini-identity, binet-formula, pisano-period, transfer-matrix-method, bostan-mori-algorithm]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.8, Fibonacci numbers (the matrix identity for the powers of the matrix with rows 1 1 and 1 0, and Cassini's identity)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.6, Fibonacci numbers (the matrix form, the addition rule F(m+n) = F(m)F(n+1) + F(m-1)F(n), and Cassini's identity)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the binary method used for the matrix power)
  - paper: "Charles M. Fiduccia, An efficient formula for linear recurrences, SIAM Journal on Computing 14(1), 1985"
    locator: the main result (the n-th term of a recurrence of order d from x^n modulo the characteristic polynomial)
---

The matrix Fibonacci method computes the Fibonacci number $F_n$ from the identity $Q^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$ for $Q = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$. With [matrix exponentiation](/matrix-exponentiation/) by repeated squaring, this takes at most $2 \lfloor \lg n \rfloor$ products of $2 \times 2$ matrices, so $O(\log n)$ ring operations, instead of the $n - 1$ additions of the direct loop. The same technique gives the $n$-th term of any linear recurrence of order $d$ with constant coefficients from a $d \times d$ companion matrix, in $O(d^3 \log n)$ ring operations with the triple loop.

## In plain words

Each Fibonacci number is the sum of the two before it. Keep the last two numbers as a pair. One step turns the pair into the next pair, and this step is the same each time. So you can write it once as a small square table, and many steps in a row are the table multiplied by itself many times.

Multiplying a table by itself many times is fast with repeated squaring: square it to jump two steps, square again to jump four, then eight, and so on. To jump a million steps, you need about forty table products, not a million additions.

Any rule that builds the next number from a fixed mix of the last few numbers works the same way, with a larger table.

## When it applies

The technique applies to a sequence that obeys a linear recurrence of fixed order $d$ with constant coefficients over a ring $R$:

$$a_m = c_1 a_{m-1} + c_2 a_{m-2} + \cdots + c_d a_{m-d} \qquad (m \ge d),$$

with given start values $a_0, \ldots, a_{d-1}$. The ring need not be commutative for the matrix form, but the usual cases are $\mathbb{Z}$ and $\mathbb{Z}/q\mathbb{Z}$. Put the last $d$ terms into the state vector $s_m = (a_m, a_{m-1}, \ldots, a_{m-d+1})^{\mathsf T}$. Then $s_{m+1} = M s_m$ for the companion matrix

$$M = \begin{pmatrix} c_1 & c_2 & \cdots & c_{d-1} & c_d \\ 1 & 0 & \cdots & 0 & 0 \\ 0 & 1 & \cdots & 0 & 0 \\ \vdots & & \ddots & & \vdots \\ 0 & 0 & \cdots & 1 & 0 \end{pmatrix},$$

so $s_n = M^{n-d+1} s_{d-1}$ for $n \ge d - 1$. The technique is worth it when $n$ is much larger than $d$: one term with large $n$, usually modulo $q$. It does not apply when the coefficients depend on $m$, or when the step is not linear.

For the Fibonacci numbers, $d = 2$, $c_1 = c_2 = 1$, $a_0 = 0$, $a_1 = 1$, and $M = Q$. The identity holds for $n = 1$, since $Q = \begin{pmatrix} F_2 & F_1 \\ F_1 & F_0 \end{pmatrix}$, and $Q^{n+1} = Q^n Q$ gives $\begin{pmatrix} F_{n+1} + F_n & F_{n+1} \\ F_n + F_{n-1} & F_n \end{pmatrix}$, induction on $n$ proves $Q^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$ for every $n \ge 1$, and also for $n = 0$ with $F_{-1} = 1$.

## The template

```pseudo id=main
LINEAR-RECURRENCE-TERM(c_1 … c_d, a_0 … a_(d−1), n)
L1  if n < d then return a_n
L2  M ← the d × d matrix with row 0 equal to (c_1, …, c_d), M[i][i−1] = 1 for 1 ≤ i < d, and 0 elsewhere
L3  P ← M^(n−d+1)                ▷ by repeated squaring
L4  v ← (a_(d−1), a_(d−2), …, a_0)
L5  return (P v)[0]
```

Line L3 is the only costly line: it makes at most $2 \lfloor \lg (n - d + 1) \rfloor$ products of $d \times d$ matrices, each with $2d^3 - d^2$ ring operations by the [triple loop](/naive-matrix-multiplication/). Line L5 is one [matrix-vector product](/matrix-vector-multiplication/). For Fibonacci, the template returns $(Q^{n-1})[0][0] = F_n$; in practice one reads $F_n$ from the top right entry of $Q^n$ directly.

## Classic examples

- **$F_{10}$.** $n = 10 = (1010)_2$. Start with $R = Q$. Square: $Q^2 = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$. Digit $0$, square: $Q^4 = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}$. Digit $1$, square and multiply by $Q$: $Q^5 = \begin{pmatrix} 8 & 5 \\ 5 & 3 \end{pmatrix}$. Digit $0$, square: $Q^{10} = \begin{pmatrix} 89 & 55 \\ 55 & 34 \end{pmatrix}$. So $F_{10} = 55$, after $4 = 3 + 2 - 1$ products.
- **$F_n \bmod q$ for huge $n$.** With $q = 10^9 + 7$ and $n = 10^{18}$, about $60$ squarings and at most $60$ further products of $2 \times 2$ matrices modulo $q$ give $F_{10^{18}} \equiv 209783453 \pmod q$. The direct loop would need $10^{18}$ steps. The sequence $F_n \bmod q$ is periodic, see the [Pisano period](/pisano-period/), but the period is near $q$ or $2q$ in general, so the matrix method is still faster.
- **Tribonacci numbers.** $T_m = T_{m-1} + T_{m-2} + T_{m-3}$ with $T_0 = T_1 = 0$, $T_2 = 1$. Here $M = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$ and $T_{10}$ is the first entry of $M^8 (1, 0, 0)^{\mathsf T}$, which is $81$.
- **A constant term.** $a_m = a_{m-1} + a_{m-2} + 1$ is not homogeneous. Add a constant $1$ to the state: $(a_m, a_{m-1}, 1)^{\mathsf T} = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} (a_{m-1}, a_{m-2}, 1)^{\mathsf T}$. With $a_0 = a_1 = 0$, this gives $a_{10} = 88 = F_{11} - 1$.
- **Counting tilings and walks.** The number of tilings of a $2 \times n$ strip by dominoes is $F_{n+1}$, and the number of binary strings of length $n$ with no two adjacent ones is $F_{n+2}$. Both are entries of powers of a [transfer matrix](/transfer-matrix-method/).
- **Identities.** Taking determinants in $Q^n$ gives [Cassini's identity](/cassini-identity/) $F_{n+1} F_{n-1} - F_n^2 = (-1)^n$. Comparing entries of $Q^{m+n} = Q^m Q^n$ gives $F_{m+n} = F_{m+1} F_n + F_m F_{n-1}$.

## Variations

- **Fast doubling.** Read $Q^{2n} = (Q^n)^2$ entry by entry: $F_{2n} = F_n (2 F_{n+1} - F_n)$ and $F_{2n+1} = F_{n+1}^2 + F_n^2$. These formulas carry only the pair $(F_n, F_{n+1})$ and use $3$ multiplications per binary digit instead of the $8$ of a full $2 \times 2$ product. This is the [fast doubling](/fibonacci-fast-doubling/) method.
- **Exploiting symmetry.** Every power of $Q$ is symmetric and has the form $F_n Q + F_{n-1} I$, because $Q^2 = Q + I$. So a product of two powers needs only the pairs: $(aQ + bI)(cQ + dI) = (ac + ad + bc) Q + (ac + bd) I$, with $4$ multiplications. This is the same as computing $x^n \bmod (x^2 - x - 1)$.
- **Polynomial method for order $d$.** By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), $M^n = r(M)$ with $r(x) = x^n \bmod \chi(x)$ and $\chi(x) = x^d - c_1 x^{d-1} - \cdots - c_d$. Repeated squaring of $x$ modulo $\chi$ costs $O(d^2 \log n)$ ring operations with the classical product of polynomials, and $O(M(d) \log n)$ with fast polynomial products (Fiduccia, 1985). The [Bostan and Mori algorithm](/bostan-mori-algorithm/) is a fast version. See [linear recurrence nth term](/linear-recurrence-nth-term/).
- **Closed form.** Over the reals, [Binet's formula](/binet-formula/) $F_n = (\varphi^n - \psi^n)/\sqrt{5}$ comes from the eigenvalues $\varphi, \psi = (1 \pm \sqrt{5})/2$ of $Q$. With floating-point numbers it is exact only for small $n$ (in IEEE double precision, up to about $n = 70$).
- **Negative indices.** $Q^{-1} = \begin{pmatrix} 0 & 1 \\ 1 & -1 \end{pmatrix}$ has integer entries, and $F_{-n} = (-1)^{n+1} F_n$.

## Pitfalls

- **Index shift.** With $F_0 = 0$ and $F_1 = 1$, $F_n$ is the top right entry of $Q^n$, not of $Q^{n-1}$. Check $n = 0$ (the identity gives $F_0 = 0$) and $n = 1$.
- **Overflow.** $F_n$ has about $0.694 n$ binary digits, so $F_{94}$ already exceeds $2^{64}$. Reduce each entry modulo $q$ after each product, or use big integers.
- **Cost with big integers.** Over $\mathbb{Z}$ the count of products is $O(\log n)$, but the numbers double in length at each squaring. The last squaring dominates, so the total cost is a constant times one multiplication of numbers with about $0.694 n$ binary digits, not $O(\log n)$ word operations.
- **Too much work per digit.** A full $2 \times 2$ product costs $8$ multiplications. Fast doubling or the symmetric form needs $3$ or $4$, which matters with big integers.
- **Wrong matrix layout.** If the state vector is ordered $(a_{m-d+1}, \ldots, a_m)$ instead, the coefficients go into the last row. Mixing the two layouts gives wrong terms.

## Exercises

1. Prove $Q^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$ by induction on $n$, and derive Cassini's identity from it.
2. Derive the fast doubling formulas from $Q^{2n} = (Q^n)^2$.
3. Count the multiplications of the binary method on $Q$ for $n = 2^t$ and $n = 2^{t+1} - 1$, with a full $2 \times 2$ product of $8$ multiplications.
4. Write the companion matrix for $a_m = 2a_{m-1} - a_{m-2} + 3$ and compute $a_{20}$ with $a_0 = 0$ and $a_1 = 1$.
5. Show that the number of tilings of a $2 \times n$ strip by dominoes is $F_{n+1}$.
6. Show that the method computes $F_n \bmod q$ in $O(\log n)$ operations on numbers smaller than $q^2$.

## References
