---
tag: JKF3JE
kind: theorem
slug: cassini-identity
name: Cassini's identity
area: foundations/recurrences
level: core
summary: States that F(n-1) F(n+1) minus F(n) squared equals (-1) to the n for consecutive Fibonacci numbers.
prereqs: [fibonacci-numbers, induction, determinant]
see_also: [binet-formula, matrix-fibonacci, fibonacci-fast-doubling, linear-recurrences-with-constant-coefficients, greatest-common-divisor, lames-theorem, continued-fraction, euclidean-algorithm]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.8, Fibonacci Numbers
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 6.6, Fibonacci Numbers
  - url: "https://en.wikipedia.org/wiki/Cassini_and_Catalan_identities"
    locator: Wikipedia, Cassini and Catalan identities (history, with Cassini 1680 and Simson 1753)
---

Cassini's identity states that $F_{n-1}F_{n+1} - F_n^2 = (-1)^n$ for the [Fibonacci numbers](/fibonacci-numbers/) and every integer $n$. So the product of the two neighbours of a Fibonacci number differs from its square by exactly 1, with a sign that alternates. The identity is the determinant of the $n$-th power of the Fibonacci matrix, and it is the source of several facts used in algorithms: consecutive Fibonacci numbers are coprime, their ratios approach the golden ratio from alternate sides, and the integer arithmetic of [fast doubling](/fibonacci-fast-doubling/) can be checked with it.

## Statement

Let $F_0 = 0$, $F_1 = 1$ and $F_{n} = F_{n-1} + F_{n-2}$ for every integer $n$, so that the sequence extends to negative indices with $F_{-n} = (-1)^{n+1}F_n$.

**Theorem (Cassini).** For every integer $n$,

$$F_{n-1}F_{n+1} - F_n^2 = (-1)^n.$$

**Theorem (Catalan).** For all integers $n$ and $r$,

$$F_n^2 - F_{n-r}F_{n+r} = (-1)^{n-r}F_r^2.$$

Cassini's identity is the case $r = 1$, up to the sign: $F_n^2 - F_{n-1}F_{n+1} = (-1)^{n-1}$.

## In plain words

Take any Fibonacci number, multiply the one before it by the one after it, and compare with the square of the middle one. The two results always differ by exactly one. The product is bigger at one step and smaller at the next, and this pattern never stops.

For example, five times thirteen is sixty-five, while eight times eight is sixty-four. This one-unit difference is the reason behind a well-known puzzle in which a square cut into four pieces seems to make a rectangle of larger area.

The identity holds because each new pair of Fibonacci numbers comes from the last pair by one fixed swap-and-add step, and that step flips the sign of this difference without changing its size.

## Proof

Three proofs follow. Each one proves the identity for all integers $n$.

### By induction

Let $D_n = F_{n-1}F_{n+1} - F_n^2$. Using $F_{n+2} = F_{n+1} + F_n$ and $F_{n+1} = F_n + F_{n-1}$,

$$D_{n+1} = F_nF_{n+2} - F_{n+1}^2 = F_n(F_{n+1} + F_n) - F_{n+1}(F_n + F_{n-1}) = F_n^2 - F_{n+1}F_{n-1} = -D_n.$$

This holds for every integer $n$, since only the recurrence was used. With $D_1 = F_0F_2 - F_1^2 = -1$, [induction](/induction/) upward and downward gives $D_n = (-1)^n$ for every integer $n$. $\square$

### By determinants

Let $Q = \begin{pmatrix}1&1\\1&0\end{pmatrix}$. For every integer $n$,

$$Q^n = \begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}.$$

For $n = 0$ this is the identity matrix, since $F_1 = 1$, $F_0 = 0$ and $F_{-1} = 1$. If it holds for $n$, then $Q^{n+1} = Q^nQ$ has first row $(F_{n+1} + F_n, F_{n+1}) = (F_{n+2}, F_{n+1})$ and second row $(F_n + F_{n-1}, F_n) = (F_{n+1}, F_n)$, so it holds for $n + 1$. In the same way, $Q^{-1} = \begin{pmatrix}0&1\\1&-1\end{pmatrix}$ and $Q^{n-1} = Q^nQ^{-1}$ give the step down. Since the [determinant](/determinant/) is multiplicative and $\det Q = -1$,

$$F_{n+1}F_{n-1} - F_n^2 = \det Q^n = (\det Q)^n = (-1)^n. \qquad \square$$

### By Binet's formula

With $\varphi = \frac{1+\sqrt5}{2}$, $\psi = \frac{1-\sqrt5}{2}$, $\varphi\psi = -1$ and [Binet's formula](/binet-formula/) $F_k = (\varphi^k - \psi^k)/\sqrt5$, valid for every integer $k$,

$$5(F_{n-r}F_{n+r} - F_n^2) = (\varphi^{n-r} - \psi^{n-r})(\varphi^{n+r} - \psi^{n+r}) - (\varphi^n - \psi^n)^2.$$

The terms $\varphi^{2n}$ and $\psi^{2n}$ cancel, and what remains is

$$-\varphi^{n-r}\psi^{n+r} - \psi^{n-r}\varphi^{n+r} + 2\varphi^n\psi^n = -(\varphi\psi)^{n-r}\left(\varphi^{2r} - 2(\varphi\psi)^r + \psi^{2r}\right) = -(\varphi\psi)^{n-r}(\varphi^r - \psi^r)^2.$$

Since $(\varphi\psi)^{n-r} = (-1)^{n-r}$ and $(\varphi^r - \psi^r)^2 = 5F_r^2$, this is $-5(-1)^{n-r}F_r^2$. Dividing by $-5$ gives Catalan's identity, and $r = 1$ gives Cassini's. $\blacksquare$

## Consequences

### Consecutive Fibonacci numbers are coprime

Cassini's identity writes $\pm 1$ as an integer combination of $F_n$ and $F_{n+1}$: $F_{n+1} \cdot F_{n-1} - F_n \cdot F_n = (-1)^n$. So each common divisor of $F_n$ and $F_{n+1}$ divides 1, and $\gcd(F_n, F_{n+1}) = 1$; see [greatest common divisor](/greatest-common-divisor/). The identity also gives the Bezout coefficients $\pm F_{n-1}$ and $\mp F_n$ directly. Consecutive Fibonacci numbers are the worst inputs for the [Euclidean algorithm](/euclidean-algorithm/), as [Lamé's theorem](/lames-theorem/) shows.

### Ratios approach the golden ratio from alternate sides

Dividing Cassini's identity by $F_nF_{n-1}$ gives, for $n \ge 2$,

$$\frac{F_{n+1}}{F_n} - \frac{F_n}{F_{n-1}} = \frac{(-1)^n}{F_nF_{n-1}}.$$

So consecutive ratios $1, 2, 1.5, 1.667, 1.6, 1.625, 1.615, 1.619, \ldots$ go up and down in turn, and the gaps shrink like $\varphi^{-2n}$. The ratios $F_{n+1}/F_n$ are the convergents of the [continued fraction](/continued-fraction/) $\varphi = [1; 1, 1, 1, \ldots]$, and Cassini's identity is the special case of the rule that consecutive convergents $p_k/q_k$ and $p_{k-1}/q_{k-1}$ satisfy $p_kq_{k-1} - p_{k-1}q_k = \pm 1$.

### The 64 and 65 puzzle

Cut an $8 \times 8$ square into two right triangles with legs 3 and 8 and two trapezoids with parallel sides 3 and 5 and height 5. The pieces seem to fit into a $5 \times 13$ rectangle, of area 65. The extra unit comes from $F_5F_7 - F_6^2 = 5 \cdot 13 - 8^2 = 1$: the long diagonal of the rectangle is not a straight line, and a thin gap of area 1 lies along it. With $F_{n-1}$, $F_n$ and $F_{n+1}$ in place of 5, 8 and 13, the gap or overlap is always one unit, while the slopes come closer as $n$ grows.

### D'Ocagne's identity

The matrix proof also gives the identity for arbitrary indices. From $Q^mQ^{-n} = Q^{m-n}$ and the top right entries, or by Binet's formula as above,

$$F_mF_{n+1} - F_{m+1}F_n = (-1)^nF_{m-n}$$

for all integers $m$ and $n$. Cassini's identity is the case $m = n - 1$, with $F_{-1} = 1$.

### A check for fast algorithms

The pairs $(F_n, F_{n+1})$ computed by [matrix powers](/matrix-fibonacci/) or by [fast doubling](/fibonacci-fast-doubling/) must satisfy $F_{n+1}^2 - F_nF_{n+1} - F_n^2 = (-1)^n$, which is Cassini's identity with $F_{n-1} = F_{n+1} - F_n$. This is a cheap test of a big-integer implementation.

## Tightness

### Other initial values

If $G_n = G_{n-1} + G_{n-2}$ with arbitrary $G_0$ and $G_1$, the induction proof gives $G_{n-1}G_{n+1} - G_n^2 = -(G_{n-2}G_n - G_{n-1}^2)$, so

$$G_{n-1}G_{n+1} - G_n^2 = (-1)^{n-1}(G_0G_2 - G_1^2).$$

The right side is $\pm 1$ only when $G_0G_2 - G_1^2 = \pm 1$. For the Lucas numbers $2, 1, 3, 4, 7, \ldots$, $G_0G_2 - G_1^2 = 5$, and the identity becomes $L_{n-1}L_{n+1} - L_n^2 = 5(-1)^{n-1}$. So the value $(-1)^n$ depends on the initial values $0, 1$, not only on the recurrence.

### Other coefficients

For $U_0 = 0$, $U_1 = 1$ and $U_n = PU_{n-1} - QU_{n-2}$, the matrix $\begin{pmatrix}P&-Q\\1&0\end{pmatrix}$ has determinant $Q$, and the same proof gives

$$U_{n-1}U_{n+1} - U_n^2 = -Q^{n-1}.$$

For example, $P = 3$ and $Q = 2$ give $U_n = 2^n - 1$, and the difference is $-2^{n-1}$, which is unbounded. The value has absolute value 1 for each $n$ only when $Q = \pm 1$. Fibonacci is $P = 1$, $Q = -1$.

### Higher order

For a recurrence of order 3 there is no identity of this form. The tribonacci numbers $0, 0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149, \ldots$ give $T_{n-1}T_{n+1} - T_n^2 = -1, 1, 0, -2, 3, -1, -4, 8, -5, -7$ for $n = 2, \ldots, 11$, with no constant size and no fixed sign pattern. The determinant argument gives an identity for the $3 \times 3$ determinant of the matrix power instead.

### The sign cannot be dropped

The difference alternates: $F_0F_2 - F_1^2 = -1$, $F_1F_3 - F_2^2 = 1$. So $|F_{n-1}F_{n+1} - F_n^2| = 1$ is exact, but neither $F_{n-1}F_{n+1} \ge F_n^2$ nor $F_{n-1}F_{n+1} \le F_n^2$ holds for all $n$.

## History

The Wikipedia article on the Cassini and Catalan identities states that Giovanni Domenico Cassini found the identity in 1680, that Robert Simson found it independently and published a proof in 1753. The general form carries the name of Eugène Catalan. Knuth gives the identity in Section 1.2.8 of The Art of Computer Programming, Volume 1, and Concrete Mathematics treats it in Section 6.6.

## References
