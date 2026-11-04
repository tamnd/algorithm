---
tag: 8H7Y8B
kind: technique
slug: binet-formula
name: Binet's formula for Fibonacci numbers
aliases:
- Fibonacci numbers by closed-form formula (Binet)
area: foundations/recurrences
level: core
summary: A closed form for the n-th Fibonacci number using powers of the golden ratio and its conjugate.
prereqs: [fibonacci-numbers, linear-recurrences-with-constant-coefficients, induction]
see_also: [cassini-identity, closed-form-solution, matrix-fibonacci, fibonacci-fast-doubling, lames-theorem, avl-tree, fibonacci-heap, zeckendorf-theorem]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.8, Fibonacci Numbers
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 6.6, Fibonacci Numbers; Section 7.3, Solving Recurrences
  - url: "https://en.wikipedia.org/wiki/Fibonacci_sequence"
    locator: Wikipedia, Fibonacci sequence, section Closed-form expression (history of the formula, with de Moivre, Daniel Bernoulli and Binet)
---

Binet's formula is the [closed form](/closed-form-solution/) $F_n = \frac{\varphi^n - \psi^n}{\sqrt5}$ of the [Fibonacci numbers](/fibonacci-numbers/) $F_0 = 0$, $F_1 = 1$, $F_{n} = F_{n-1} + F_{n-2}$, where $\varphi = \frac{1 + \sqrt5}{2} \approx 1.618$ is the golden ratio and $\psi = \frac{1 - \sqrt5}{2} = -1/\varphi \approx -0.618$. Because $|\psi| < 1$, the second term is small, so $F_n$ is the integer nearest to $\varphi^n/\sqrt5$ and $F_n \sim \varphi^n/\sqrt5$. The formula is the simplest case of the [characteristic-polynomial method](/linear-recurrences-with-constant-coefficients/), and it is the usual tool for growth bounds in which Fibonacci numbers appear, from Euclid's algorithm to AVL trees.

## In plain words

Each Fibonacci number is the sum of the two before it. The formula gives the value at any position directly, without computing all the earlier ones.

It writes each Fibonacci number as the difference of two simple sequences, each of which is multiplied by a fixed factor at every step. One factor is the golden ratio, a bit more than one and a half, so its sequence grows quickly. The other factor is negative and smaller than one in size, so its sequence flips sign and fades away.

So after the first few steps, the Fibonacci numbers are almost exactly a growing geometric sequence, and rounding that sequence to the nearest whole number gives each of them exactly. This is why each new Fibonacci number is about the golden ratio times the previous one.

## When it applies

- To compute the order of growth of anything bounded by Fibonacci numbers: $F_n = \Theta(\varphi^n)$, so a quantity that satisfies $N(h) \ge F_{h+c}$ gives $h \le \log_\varphi N + O(1)$.
- To prove identities about Fibonacci and Lucas numbers by algebra in $\varphi$ and $\psi$.
- To find the index of a Fibonacci number from its value: $n = \operatorname{round}(\log_\varphi(F_n\sqrt5))$ for $n \ge 2$.
- Not, in floating point, to compute large Fibonacci numbers exactly: use [matrix powers](/matrix-fibonacci/) or [fast doubling](/fibonacci-fast-doubling/).

## The template

### The formula and its exact hypotheses

$\varphi$ and $\psi$ are the two roots of $x^2 = x + 1$. They satisfy $\varphi + \psi = 1$, $\varphi\psi = -1$ and $\varphi - \psi = \sqrt5$. The formula

$$F_n = \frac{\varphi^n - \psi^n}{\sqrt5}$$

holds for every integer $n$, negative ones included, when the recurrence $F_{n} = F_{n-1} + F_{n-2}$ is extended to all integers (so $F_{-1} = 1$, $F_{-2} = -1$, and in general $F_{-n} = (-1)^{n+1}F_n$).

### Proof by induction

The right side $B_n = (\varphi^n - \psi^n)/\sqrt5$ satisfies $B_0 = 0$ and $B_1 = (\varphi - \psi)/\sqrt5 = 1$. Since $\varphi^2 = \varphi + 1$, multiplying by $\varphi^{n-2}$ gives $\varphi^n = \varphi^{n-1} + \varphi^{n-2}$, and the same for $\psi$. So $B_n = B_{n-1} + B_{n-2}$ for every integer $n$. Two sequences that satisfy the same second-order recurrence and agree at $n = 0, 1$ agree for all $n \ge 0$, by [induction](/induction/), and for $n < 0$ by running the recurrence backwards as $F_{n-2} = F_n - F_{n-1}$.

### Proof by the characteristic polynomial

The [method](/linear-recurrences-with-constant-coefficients/) gives $F_n = \alpha\varphi^n + \beta\psi^n$, with $\alpha + \beta = F_0 = 0$ and $\alpha\varphi + \beta\psi = F_1 = 1$. So $\beta = -\alpha$ and $\alpha(\varphi - \psi) = 1$, that is $\alpha = 1/\sqrt5$.

### Proof by the matrix

$\begin{pmatrix}1&1\\1&0\end{pmatrix}^n = \begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}$ for $n \ge 1$, by induction. The matrix has eigenvalues $\varphi$ and $\psi$ with eigenvectors $(\varphi, 1)$ and $(\psi, 1)$; diagonalizing it and reading off the top right entry gives Binet's formula.

### Rounding

For $n \ge 0$, $|\psi^n/\sqrt5| \le 1/\sqrt5 \approx 0.447 < \frac12$. So

$$F_n = \operatorname{round}\left(\frac{\varphi^n}{\sqrt5}\right) = \left\lfloor \frac{\varphi^n}{\sqrt5} + \frac12 \right\rfloor \quad (n \ge 0).$$

The error $|\psi^n|/\sqrt5$ is $0.276$ at $n = 1$, $0.065$ at $n = 4$ and $0.0095$ at $n = 8$, and it shrinks by the factor $0.618$ at each step. For $n < 0$ the rounding form fails: $|\psi^n|$ grows.

## Classic examples

### Growth and digits

$F_n \sim \varphi^n/\sqrt5$, and $F_{n+1}/F_n \to \varphi$, since $F_{n+1}/F_n = \varphi \cdot \frac{1 - (\psi/\varphi)^{n+1}}{1 - (\psi/\varphi)^n}$ and $|\psi/\varphi| < 1$. The number of decimal digits of $F_n$ is about $n\log_{10}\varphi \approx 0.20899n$. For example $F_{100} = 354224848179261915075$, with 21 digits.

### Lamé's theorem

If Euclid's algorithm on $a > b > 0$ takes $k$ division steps, then $b \ge F_{k+1}$. By the rounding bound, $F_{k+1} \ge \varphi^{k-1}$, so $k \le \log_\varphi b + 1 \approx 4.785\log_{10} b + 1$. See [Lamé's theorem](/lames-theorem/).

### AVL trees

The fewest nodes in an [AVL tree](/avl-tree/) of height $h$ satisfies $N_h = N_{h-1} + N_{h-2} + 1$ with $N_0 = 1$, $N_1 = 2$, so $N_h + 1$ satisfies the Fibonacci recurrence and $N_h = F_{h+3} - 1$. With Binet's formula, $n \ge N_h$ gives $h < \log_\varphi n + O(1) \approx 1.4404\lg n + O(1)$.

### Fibonacci heaps

In a [Fibonacci heap](/fibonacci-heap/), a node of degree $k$ has at least $F_{k+2} \ge \varphi^k$ descendants, itself included. So the maximum degree in a heap of $n$ nodes is at most $\log_\varphi n$.

### Lucas numbers and an identity

The Lucas numbers $L_0 = 2$, $L_1 = 1$, $L_n = L_{n-1} + L_{n-2}$ have the closed form $L_n = \varphi^n + \psi^n$, by the same fitting. Then

$$L_n^2 - 5F_n^2 = (\varphi^n + \psi^n)^2 - (\varphi^n - \psi^n)^2 = 4(\varphi\psi)^n = 4(-1)^n.$$

### Fast doubling

From Binet's formula, or from the square of the matrix above,

$$F_{2n} = F_n(2F_{n+1} - F_n), \qquad F_{2n+1} = F_n^2 + F_{n+1}^2.$$

These give $F_n$ in $O(\log n)$ arithmetic operations on exact integers; see [fast doubling](/fibonacci-fast-doubling/).

## Variations

- **Other initial values.** Each solution of $G_n = G_{n-1} + G_{n-2}$ is $G_n = A\varphi^n + B\psi^n$ with $A = \frac{G_1 - G_0\psi}{\sqrt5}$ and $B = \frac{G_0\varphi - G_1}{\sqrt5}$. Equivalently, $G_n = G_0 F_{n-1} + G_1 F_n$.
- **Lucas sequences.** For $x^2 = Px - Q$ with distinct roots $\alpha$ and $\beta$, the sequence $U_0 = 0$, $U_1 = 1$, $U_n = PU_{n-1} - QU_{n-2}$ is $U_n = \frac{\alpha^n - \beta^n}{\alpha - \beta}$. Fibonacci is $P = 1$, $Q = -1$.
- **A repeated root.** For $P^2 = 4Q$ the formula degenerates, and the limit $\beta \to \alpha$ gives $U_n = n\alpha^{n-1}$, the case of a double root.
- **Exact arithmetic in $\mathbb{Z}[\varphi]$.** Writing $\varphi^n = F_n\varphi + F_{n-1}$ (induction from $\varphi^2 = \varphi + 1$) gives an exact form of the formula with integers only.

## Pitfalls

- **Floating point.** In IEEE double precision, $\operatorname{round}(\varphi^n/\sqrt5)$ is correct up to $n = 70$ and wrong from $n = 71$ on: $F_{71} = 308061521170129$, while the computation gives $308061521170130$. The double has 53 bits, and $F_{71}$ needs 49 bits, so the relative error of $\varphi^{71}$ already exceeds the gap.
- **Cost.** Computing $\varphi^n$ to enough precision for the exact $F_n$ needs about $0.694n$ bits, so the formula does not give $F_n$ in $O(1)$ time in any honest model.
- **The index convention.** Some texts start with $F_1 = F_2 = 1$ and others with $F_0 = 0$, $F_1 = 1$. The formula as written uses $F_0 = 0$; with another start, shift the index.
- **The sign of $\psi$.** $\psi$ is negative, so $\psi^n$ alternates. So $F_n > \varphi^n/\sqrt5$ for odd $n$ and $F_n < \varphi^n/\sqrt5$ for even $n \ge 2$: $F_1 = 1 > \varphi/\sqrt5 \approx 0.724$, but $F_2 = 1 < \varphi^2/\sqrt5 \approx 1.171$. A one-sided bound such as $F_n \ge \varphi^n/\sqrt5$ is false for each even $n \ge 2$. Use $\varphi^{n-2} \le F_n \le \varphi^{n-1}$ for $n \ge 1$, which follows by induction.

## Exercises

1. Prove $\varphi^{n-2} \le F_n \le \varphi^{n-1}$ for $n \ge 1$.
2. Prove $F_{-n} = (-1)^{n+1}F_n$ from Binet's formula, using $\psi = -1/\varphi$.
3. Use Binet's formula to prove $F_{m+n} = F_mF_{n+1} + F_{m-1}F_n$.
4. Show that $\sum_{k=0}^{n} F_k = F_{n+2} - 1$ by summing the two [geometric series](/geometric-series/).
5. Prove [Cassini's identity](/cassini-identity/) $F_{n-1}F_{n+1} - F_n^2 = (-1)^n$ from Binet's formula.

## References
