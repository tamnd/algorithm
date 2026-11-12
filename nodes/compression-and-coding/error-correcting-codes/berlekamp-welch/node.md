---
tag: 7100GD
kind: algorithm
slug: berlekamp-welch
name: Berlekamp-Welch algorithm
aliases:
- Berlekamp-Welch decoder
- Welch-Berlekamp algorithm
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Decode a Reed-Solomon code in the evaluation view by one linear system for an error locator E and a product Q = E f, then divide Q by E.
solves: [reed-solomon-decoding]
model: word-ram
complexity:
  vars: {n: the code length, k: the dimension}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1986
  people: [Elwyn R. Berlekamp, Lloyd R. Welch]
  note: The method appeared in a US patent filed in 1983 and granted in 1986; Gemmell and Sudan gave a short published account in 1992.
prereqs: [reed-solomon-code, gaussian-elimination]
see_also: [guruswami-sudan, peterson-gorenstein-zierler, berlekamp-massey, list-decoding, polynomial-interpolation, lagrange-interpolation, polynomial-extended-euclidean-algorithm]
sources:
  - paper: "E. R. Berlekamp and L. R. Welch, Error correction for algebraic block codes, US Patent 4,633,470, 1986"
    title: E. R. Berlekamp and L. R. Welch, Error correction for algebraic block codes, US Patent 4,633,470, granted 30 December 1986
    locator: The description and claims (decoding from the received values with an error locator polynomial, without syndromes in the power sum form)
  - paper: "P. Gemmell and M. Sudan, Highly resilient correctors for polynomials, Information Processing Letters 43(4), 1992"
    title: P. Gemmell and M. Sudan, Highly resilient correctors for polynomials, Information Processing Letters 43(4), 1992
    locator: The presentation of the Berlekamp-Welch decoder as a linear system in E and Q
  - url: https://cse.buffalo.edu/faculty/atri/courses/coding-theory/book/
    title: V. Guruswami, A. Rudra and M. Sudan, Essential Coding Theory (book draft)
    locator: The chapter on efficient decoding of Reed-Solomon codes (the Welch-Berlekamp algorithm and its proof)
  - paper: "S. Gao, A new algorithm for decoding Reed-Solomon codes, in Communications, Information and Network Security, Kluwer, 2003"
    title: S. Gao, A new algorithm for decoding Reed-Solomon codes, 2003
    locator: The decoder by interpolation and a partial extended Euclidean algorithm
---

The Berlekamp-Welch algorithm decodes a [Reed-Solomon code](/reed-solomon-code/) directly from the received values, with no syndromes. The codeword is $(f(a_1), \ldots, f(a_n))$ for a message polynomial $f$ of degree less than $k$. The received word $y$ differs from it in at most $e = \lfloor (n-k)/2 \rfloor$ places. The decoder looks for a monic error locator $E$ of degree $e$ that is zero at the bad places, and the product $Q = E f$. The conditions $Q(a_i) = y_i E(a_i)$ for all $i$ are linear in the coefficients of $E$ and $Q$, so one run of [Gaussian elimination](/gaussian-elimination/) finds them, and $f = Q / E$. The cost is $O(n^3)$ field operations. The method is easy to state and to prove, and it is the base of [Sudan's list decoder](/guruswami-sudan/).

## In plain words

The sender evaluates a short polynomial at many points and sends the values. Some values are changed on the way. The receiver does not know which. It looks for a second polynomial that is zero at the bad points. If it multiplies the received values by this polynomial, the bad values no longer matter, because they are multiplied by zero. That product is a polynomial too, and the unknowns appear in a simple linear way. So the receiver solves one system of linear equations, then divides one polynomial by the other to get the message.

## The algorithm

The input is $n$ distinct points $a_1, \ldots, a_n$ of a field $F$, a received word $y_1, \ldots, y_n$, and the dimension $k$, with $1 \le k \le n$. The unknowns are $E(x) = E_0 + E_1 x + \cdots + E_{e-1} x^{e-1} + x^e$ and $Q(x) = Q_0 + \cdots + Q_{e+k-1} x^{e+k-1}$, so there are $2e + k \le n$ unknowns.

```pseudo id=main
BERLEKAMP-WELCH(a_1 .. a_n, y_1 .. y_n, k)    ▷ f with deg f < k and at most e errors, or FAIL
L1  e ← ⌊(n − k)/2⌋
L2  for i ← 1 to n: write the equation Q(a_i) − y_i E(a_i) = 0, with E monic of degree e and deg Q < e + k
L3  find any solution (Q, E) by Gaussian elimination; if there is none, return FAIL
L4  (f, R) ← (Q div E, Q mod E)
L5  if R ≠ 0 then return FAIL
L6  return f
```

Line L2 gives $n$ linear equations. The term $y_i a_i^e$ of the leading coefficient $E_e = 1$ is known, so it moves to the right side:

$$\sum_{j=0}^{e+k-1} Q_j a_i^{\,j} - y_i \sum_{j=0}^{e-1} E_j a_i^{\,j} = y_i a_i^{\,e}.$$

The system can have many solutions when there are fewer than $e$ errors. Line L3 can take any of them, because every solution gives the same quotient. Since $\deg Q < e + k$ and $\deg E = e$, the quotient of line L4 has degree less than $k$.

## Example

Take $F = \mathrm{GF}(7)$, $n = 6$, $k = 2$, the points $0, 1, \ldots, 5$, and $f(x) = 1 + 2x$. The codeword is $(1, 3, 5, 0, 2, 4)$. Two errors change position 1 (the point $a = 1$) from 3 to 6 and position 4 (the point $a = 4$) from 2 to 0, so

$$y = (1, 6, 5, 0, 0, 4), \qquad e = \lfloor (6 - 2)/2 \rfloor = 2 .$$

The unknowns are $Q_0, Q_1, Q_2, Q_3, E_0, E_1$, six unknowns for six equations. The equation for the point $a$ is $Q_0 + Q_1 a + Q_2 a^2 + Q_3 a^3 - y E_0 - y a E_1 = y a^2$. The system has the unique solution

$$E(x) = 4 + 2x + x^2 = (x - 1)(x - 4), \qquad Q(x) = 4 + 3x + 5x^2 + 2x^3 .$$

Check two equations. At $a = 2$, $Q(2) = 4 + 6 + 20 + 16 = 46 \equiv 4$ and $y E(2) = 5 \cdot 12 = 60 \equiv 4$. At the error point $a = 4$, $Q(4) = 224 \equiv 0$ and $E(4) = 28 \equiv 0$, so the equation holds for any received value.

Line L4 divides: $2x^3 + 5x^2 + 3x + 4 = (2x + 1)(x^2 + 2x + 4)$ in $\mathrm{GF}(7)[x]$, with remainder 0. So $f(x) = 1 + 2x$, and the roots of $E$ are the error points 1 and 4.

## Correctness

**Existence.** If $f$ has $\deg f < k$ and differs from $y$ at a set $B$ of at most $e$ points, put $E^*(x) = \prod_{b \in B}(x - b) \cdot x^{e - |B|}$ and $Q^* = E^* f$. At a point of $B$, both sides of line L2 are 0. At any other point, $y_i = f(a_i)$, so $Q^*(a_i) = y_i E^*(a_i)$. So line L3 finds a solution.

**Uniqueness of the quotient.** Let $(Q, E)$ be any solution. For every $i$, $Q(a_i) E^*(a_i) = y_i E(a_i) E^*(a_i) = Q^*(a_i) E(a_i)$. So $Q E^* - Q^* E$ is zero at $n$ distinct points, and its degree is less than $2e + k \le n$. It is the zero polynomial, so $Q E^* = E^* f E$, and since $E^* \ne 0$, $Q = E f$. Line L4 returns $f$ with remainder 0.

**No wrong answer.** If line L5 passes, then $Q = E f$ with $\deg f < k$. At each $a_i$ with $E(a_i) \ne 0$, $f(a_i) = Q(a_i)/E(a_i) = y_i$. A monic $E$ of degree $e$ has at most $e$ roots, so $f$ is within distance $e$ of $y$, and by uniqueness of the nearest codeword it is the only one. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The system has $n$ equations and $2e + k \le n$ unknowns. Building it costs $O(n^2)$, Gaussian elimination $O(n^3)$, and the division $O(e k)$. So the total is $\Theta(n^3)$ field operations and $\Theta(n^2)$ space for the matrix. The syndrome decoders ([Berlekamp-Massey](/berlekamp-massey/) with the [Chien search](/chien-search/) and [Forney](/forney-algorithm/)) take $O(n(n-k))$. The fast forms of Berlekamp-Welch below reach $O(n^2)$, and $O(n \log^2 n)$ or less with fast polynomial arithmetic.

## Properties

- **Decoding radius.** It corrects every pattern of at most $\lfloor (n-k)/2 \rfloor$ errors, the full unique decoding radius.
- **Any points.** The points $a_i$ need only be distinct. They can include 0, and they need not be powers of a primitive element, so the method also decodes generalized Reed-Solomon codes after division by the column multipliers.
- **Any field.** The method works over any field, for example a prime field $\mathrm{GF}(p)$ or $\mathrm{GF}(2^m)$.
- **Detection.** When line L3 or L5 fails, there is no codeword within distance $e$. A result is never a codeword at distance more than $e$.
- **Message out.** The output is the message polynomial $f$, not the corrected codeword. In the evaluation view, this is the data.

## Variants and improvements

- **Errors and erasures.** Drop the erased positions and decode the shorter code: $n - \rho$ points, the same $k$, and $e = \lfloor (n - \rho - k)/2 \rfloor$. This corrects $\nu$ errors with $2\nu + \rho \le n - k$.
- **Gao's algorithm.** Interpolate $y$ by a polynomial $g_1$ of degree less than $n$, and run the extended Euclidean algorithm on $g_0 = \prod (x - a_i)$ and $g_1$ until the remainder has degree less than $(n + k)/2$. The remainder and its cofactor give $Q$ and $E$ up to a constant. This costs $O(n^2)$, or less with fast arithmetic.
- **Iterative forms.** The system can also be solved by updating the two polynomials one point at a time, in $O(n^2)$ operations, without a general matrix elimination.
- **Sudan and Guruswami-Sudan.** Write the condition as $Q(x) - y E(x) = 0$ at each point $(a_i, y_i)$. This is a bivariate polynomial $Q_0(x) + Q_1(x) y$ of degree 1 in $y$. Allowing a higher degree in $y$, and multiplicities, gives the [Guruswami-Sudan](/guruswami-sudan/) list decoder, which corrects more than $e$ errors.

## When to use it

Use Berlekamp-Welch when the code is given in the evaluation view, when the points are arbitrary, or when a short and clear decoder is more important than speed: in teaching, in proofs of complexity theory such as polynomial reconstruction and probabilistically checkable proofs, and in secret sharing, where the shares are values of a polynomial. For long codes in high speed systems, use a syndrome decoder or Gao's algorithm.

## Pitfalls

- **Dropping the monic condition.** Without $E_e = 1$, the system has the trivial solution $Q = E = 0$. Fix the leading coefficient of $E$, or require $E \ne 0$ in another way.
- **Wrong degree bounds.** $Q$ must have degree less than $e + k$, not $e + k$ or more. With one more unknown, the system has solutions that do not come from a codeword, and the uniqueness argument fails because $2e + k$ can exceed $n$.
- **Treating any solution as the true locator.** With fewer than $e$ errors, $E$ is not unique and can have roots at correct points. Only the quotient $f$ is unique. To find the error positions, compare $f(a_i)$ with $y_i$.
- **Skipping the remainder check.** Beyond $e$ errors, the system can still have a solution with $E \nmid Q$. The quotient is then not a valid decoding.

## Implementations

## History

Elwyn Berlekamp and Lloyd Welch described the method in a US patent, filed in 1983 and granted in 1986 as patent 4,633,470, "Error correction for algebraic block codes". The patent was the main record for some years. Peter Gemmell and Madhu Sudan gave a short account of the decoder as a linear system in 1992, in a paper on correcting polynomials, and it became the standard first decoder in courses on coding theory and in theoretical computer science. In 1997, Sudan generalized the idea to a bivariate polynomial of higher degree in $y$, which gave the first polynomial time list decoder for Reed-Solomon codes. Gao described a fast form based on the Euclidean algorithm in 2003.

## References
