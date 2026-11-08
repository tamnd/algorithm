---
tag: Q79FRC
kind: algorithm
slug: pade-approximation
name: Padé approximation
aliases:
- Padé approximant
- Padé table
area: numerical/interpolation-and-approximation
level: advanced
summary: The rational function p/q of type (m, n) whose Taylor series agrees with that of f to order m + n. Its coefficients come from a Toeplitz linear system built from c_0..c_(m+n).
solves: [rational-approximation]
model: real-ram
complexity:
  vars: {m: the numerator degree, n: the denominator degree}
  time: {build_dense: Θ(n^3 + m n), build_toeplitz_solver: Θ(n^2 + m n), evaluate: Θ(m + n)}
  space: {extra: Θ(n^2)}
  flops: {build_dense: "(2/3) n^3 + 2 m n"}
properties: {deterministic: true, recursive: false, exact_on_rational_functions: true, linear_in_data: false, uses_only_taylor_coefficients: true}
history:
  year: 1892
  people: [Henri Padé]
  note: Padé's thesis (1892) organized the approximants into a table and studied its structure; Frobenius (1881) and Jacobi had considered the same rational functions earlier.
prereqs: [rational-approximation, polynomial, gaussian-elimination]
see_also: [continued-fraction, sequence-extrapolation, aitken-delta-squared, orthogonal-polynomials, thiele-continued-fraction-interpolation, minimax-approximation, gauss-legendre-runge-kutta, toeplitz-system-solving]
sources:
  - paper: "Henri Padé, Sur la représentation approchée d'une fonction par des fractions rationnelles, Annales scientifiques de l'École Normale Supérieure, 3e série, 9 (1892), supplément, 3-93"
    locator: the table of approximants and its block structure
  - book: isbn:9780521450072
    title: George A. Baker Jr. and Peter Graves-Morris, Padé Approximants, second edition, Cambridge University Press, 1996
    locator: Part I, Chapter 1, Introduction and definitions (existence, uniqueness, the block structure), and the chapters on convergence theory (de Montessus de Ballore's theorem, convergence in measure and capacity)
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 27, Padé approximation, and Chapter 28, Analytic continuation and convergence acceleration
  - paper: "Pedro Gonnet, Stefan Güttel and Lloyd N. Trefethen, Robust Padé approximation via SVD, SIAM Review 55(1) (2013) 101-117"
    locator: spurious pole-zero pairs (Froissart doublets) and the SVD-based algorithm that removes them
  - paper: "Robert de Montessus de Ballore, Sur les fractions continues algébriques, Bulletin de la Société Mathématique de France 30 (1902) 28-36"
    locator: convergence of the rows of the Padé table for meromorphic functions with n poles in a disk
  - book: isbn:9780444888143
    title: Claude Brezinski and Michela Redivo Zaglia, Extrapolation Methods, Theory and Practice, North-Holland, 1991
    locator: Chapter 2, the epsilon-algorithm and its connection with the Shanks transformation and Padé approximants
---

A Padé approximant is the rational analogue of a Taylor polynomial. Given the Taylor coefficients $c_0, c_1, \ldots$ of a function $f$ at 0, the $[m/n]$ Padé approximant is the rational function $r = p/q$ with $\deg p \le m$ and $\deg q \le n$ whose own Taylor series agrees with that of $f$ through the term $x^{m+n}$. The coefficients of $q$ solve a small Toeplitz linear system; those of $p$ then follow by a convolution. Because a rational function can have poles, Padé approximants often converge far beyond the radius of convergence of the Taylor series, which makes them a standard tool for analytic continuation and for summing divergent or slowly convergent series.

## In plain words

A Taylor polynomial copies the first few derivatives of a function at one point, but it is useless beyond the nearest place where the function blows up. A Padé approximant also copies the first few derivatives, but it is a fraction of two polynomials, so it can blow up too. When the function has a pole, the fraction can put a pole in the same place and keep approximating on the other side.

The recipe is short: the coefficients of the bottom polynomial solve a small system of equations made from the known derivatives, and the coefficients of the top polynomial follow by multiplication. The method is fast and often very accurate, but noisy coefficients can create fake poles, each paired with a nearby zero, which must be watched for.

## The problem

Notation on the interpolation pages: $f(x) = \sum_{k \ge 0} c_k x^k$ is a power series with known coefficients $c_0, \ldots, c_{m+n}$ (put $c_k = 0$ for $k < 0$); a rational function $r = p/q$ has type $(m, n)$ if $\deg p \le m$ and $\deg q \le n$.

**Definition.** The $[m/n]$ Padé approximant of $f$ is $r = p/q$ of type $(m, n)$ with $q(0) = 1$ and
$$f(x)\, q(x) - p(x) = O(x^{m+n+1}).$$
Comparing coefficients of $x^k$ gives, with $q_0 = 1$,
$$\sum_{j=0}^{n} q_j\, c_{k-j} = 0 \quad (k = m + 1, \ldots, m + n), \qquad p_k = \sum_{j=0}^{\min(k, n)} q_j\, c_{k-j} \quad (k = 0, \ldots, m).$$
The first set is $n$ linear equations in $q_1, \ldots, q_n$ with the Toeplitz matrix $C = (c_{m+i-j})_{i,j=1}^{n}$.

**Existence and uniqueness.** The homogeneous problem, find $(p, q) \ne 0$ of type $(m, n)$ with $fq - p = O(x^{m+n+1})$, always has a solution, since it has $n + 1$ unknowns in $q$ and $n$ equations. All solutions give the same rational function $p/q$ (Frobenius): if $(p, q)$ and $(\tilde p, \tilde q)$ are two, then $p\tilde q - \tilde p q = (fq - p)\tilde q - (f\tilde q - \tilde p) q = O(x^{m+n+1})$ has degree at most $m + n$, so it is 0. The $[m/n]$ approximant in the sense above exists exactly when some solution has $q(0) \ne 0$. When $C$ is nonsingular, $q$ is unique with $q_0 = 1$ and the approximant is **normal**. Singular cases come in square **blocks** of the Padé table, where several entries coincide (Padé 1892).

## The algorithm

```pseudo id=main
PADE(c, m, n)                    ▷ c[0..m+n], c[k] = 0 for k < 0
L1  A[i][j] ← c[m + i − j] for i, j = 1..n
L2  b[i] ← −c[m + i] for i = 1..n
L3  solve A · (q[1], …, q[n]) = b    ▷ if A is singular, report a block
L4  q[0] ← 1
L5  p[k] ← Σ_{j=0}^{min(k, n)} q[j] · c[k − j] for k = 0..m
L6  return p, q
```

Line L3 is the only expensive step. The implementation uses Gaussian elimination with partial pivoting, in exact rational arithmetic when the coefficients are fractions. Toeplitz solvers (Levinson-Trench type) do it in $\Theta(n^2)$ operations when all leading minors are nonzero, and superfast solvers in $O(n \log^2 n)$; see [Toeplitz system solving](/toeplitz-system-solving/). Line L5 is the truncated product of the series $f$ and the polynomial $q$.

## Example

**$e^x$, $[2/2]$.** With $c = (1, 1, \tfrac12, \tfrac16, \tfrac1{24})$, lines L1 to L3 solve
$$\begin{pmatrix} c_2 & c_1 \\ c_3 & c_2 \end{pmatrix} \begin{pmatrix} q_1 \\ q_2 \end{pmatrix} = -\begin{pmatrix} c_3 \\ c_4 \end{pmatrix}, \quad \text{that is} \quad \begin{pmatrix} \tfrac12 & 1 \\ \tfrac16 & \tfrac12 \end{pmatrix} \begin{pmatrix} q_1 \\ q_2 \end{pmatrix} = \begin{pmatrix} -\tfrac16 \\ -\tfrac1{24} \end{pmatrix},$$
with solution $q_1 = -\tfrac12$, $q_2 = \tfrac1{12}$. Line L5 gives $p_0 = 1$, $p_1 = 1 - \tfrac12 = \tfrac12$, $p_2 = \tfrac12 - \tfrac12 + \tfrac1{12} = \tfrac1{12}$. So
$$[2/2]_{\exp}(x) = \frac{1 + x/2 + x^2/12}{1 - x/2 + x^2/12}.$$
At $x = 1$ it gives $19/7 \approx 2.714286$, an error of $4.0 \times 10^{-3}$; the Taylor polynomial of the same degree 4 gives $2.708333$, an error of $9.9 \times 10^{-3}$. The error series starts with $x^5/720$, in agreement with the general formula $e^x - [m/n](x) = (-1)^n \frac{m!\, n!}{(m+n)!\,(m+n+1)!} x^{m+n+1} + O(x^{m+n+2})$.

**$\log(1 + x)$, beyond the radius of convergence.** The Taylor series converges only for $|x| \le 1$ (slowly at $x = 1$: the partial sum through $x^{32}$ is off by $0.015$). The diagonal approximants $[n/n]$, computed in exact arithmetic, give errors

| $n$ | $x = 1$ | $x = 3$ | $x = 10$ |
|---|---|---|---|
| 2 | $8.4 \times 10^{-4}$ | $2.3 \times 10^{-2}$ | 0.23 |
| 4 | $7.6 \times 10^{-7}$ | $3.0 \times 10^{-4}$ | $2.1 \times 10^{-2}$ |
| 8 | $5.9 \times 10^{-13}$ | $4.7 \times 10^{-8}$ | $1.5 \times 10^{-4}$ |
| 16 | below $10^{-16}$ | $1.1 \times 10^{-15}$ | $7.4 \times 10^{-9}$ |

The poles of the approximants lie on the branch cut $(-\infty, -1]$, and the approximants converge on the rest of the plane, as the theory of Stieltjes functions predicts.

**Spurious poles from noise.** Take $f(x) = 1/(1 - x/2)$, whose only pole is at 2, and perturb its coefficients $2^{-k}$ by relative errors of size $10^{-10}$. The $[4/4]$ approximant then has its true pole at $2.0000$, and three more poles at $-0.065$, $-1.089$ and $1.381$, each with a zero of $p$ within $2 \times 10^{-11}$ of it. These are **Froissart doublets**: they barely affect the function away from the doublet, but they are not poles of $f$. With exact coefficients, $[4/4]$ lies in a block of the table, since $f$ already has type $(0, 1)$, and the implementation reports a singular system.

## Correctness

The equations of lines L1 and L2 are the coefficients of $x^{m+1}, \ldots, x^{m+n}$ in $fq - p$, in which $p$ does not appear; line L5 sets the coefficients of $x^0, \ldots, x^m$ to zero. So if line L3 succeeds, $fq - p = O(x^{m+n+1})$ with $q_0 = 1$, which is the definition. If $A$ is nonsingular, $q$ is the unique solution with $q_0 = 1$, and by Frobenius' argument every solution of the homogeneous problem gives the same $r$. If $f$ is itself a rational function of type $(m, n)$ in lowest terms with nonzero denominator at 0, then $r = f$. The full argument is in the correctness proof below.

## Complexity

- **Dense solve.** Line L1 builds an $n \times n$ matrix; Gaussian elimination costs about $\tfrac23 n^3$ flops; line L5 costs about $2mn$ flops (fewer, since $j \le k$). Total $\Theta(n^3 + mn)$.
- **Toeplitz solve.** $\Theta(n^2)$ by Levinson-type recursions, or $O(n \log^2 n)$ by superfast methods, when the needed minors are nonzero. The whole Padé table along a staircase can be computed in $\Theta(n^2)$ by recursive algorithms related to the Euclidean algorithm.
- **Evaluation.** $\Theta(m + n)$ by Horner's rule on $p$ and $q$.
- **Exact arithmetic.** With rational coefficients, entries grow, and the bit cost of exact elimination grows faster than the operation count.

## Properties

- **Exact on rational functions** of type $(m, n)$, in exact arithmetic.
- **Uses only local data.** Only $c_0, \ldots, c_{m+n}$ at one point are used; the approximant is good near 0 and, often, far away.
- **Nonlinear in $f$.** $[m/n]_{f+g} \ne [m/n]_f + [m/n]_g$ in general, unlike Taylor polynomials.
- **Invariances.** Padé approximants commute with Möbius transformations of the variable $x \mapsto ax/(1 + bx)$ (diagonal case) and of the value $f \mapsto (a + bf)/(c + df)$, under conditions on the degrees; $[n/n]$ of $1/f$ is $1/[n/n]_f$.
- **Convergence: proved cases.** Rows ($n$ fixed, $m \to \infty$): if $f$ is meromorphic in $|x| < R$ with exactly $n$ poles there, $[m/n] \to f$ uniformly on compact subsets of the disk minus the poles (de Montessus de Ballore 1902). Diagonals of Stieltjes functions $f(x) = \int d\mu(t)/(1 - xt)$ converge on compact subsets of the cut plane (Markov), and their denominators are [orthogonal polynomials](/orthogonal-polynomials/). For general meromorphic $f$, diagonals converge in measure (Nuttall 1970) and in capacity (Pommerenke 1973); Stahl extended convergence in capacity to functions with branch points.
- **Convergence: what fails.** Uniform convergence of diagonal sequences fails in general because of spurious poles; the Baker-Gammel-Wills conjecture, that a subsequence always converges uniformly, is false (Lubinsky 2003). Spurious poles are observed in floating point whenever the order exceeds what the data support.
- **Exponential function.** The approximants of $e^x$ have the closed form $P_{mn}(x)/P_{nm}(-x)$ with $P_{mn}(x) = \sum_{j=0}^{m} \frac{(m+n-j)!\, m!}{(m+n)!\, j!\, (m-j)!} x^j$. The diagonal ones are the stability functions of the Gauss-Legendre implicit Runge-Kutta methods and are A-stable.

## Variants and improvements

- **Robust Padé via SVD.** Gonnet, Güttel and Trefethen (2013) compute the null space of the $(n) \times (n + 1)$ Toeplitz matrix by the SVD, lower $n$ until the matrix has full rank to a tolerance, and so remove Froissart doublets automatically.
- **Continued fractions and the epsilon algorithm.** The staircase of the table is generated by the convergents of a continued fraction (the qd algorithm), and Wynn's epsilon algorithm computes the values $[n + k/k](x)$ from the partial sums without solving any system; it equals the Shanks transformation ([sequence extrapolation](/sequence-extrapolation/)).
- **Multipoint Padé.** Match values and derivatives at several points: this is rational interpolation, computed by [Thiele continued fractions](/thiele-continued-fraction-interpolation/) or barycentric rational forms.
- **Padé-Chebyshev and Padé-type approximants.** Replace powers of $x$ by Chebyshev polynomials, or fix the denominator in advance.
- **Hermite-Padé.** Simultaneous approximants of several functions, used in number theory and for algebraic approximants.
- **Matrix exponential.** Scaling and squaring with a diagonal Padé approximant is the standard algorithm for $e^A$.

## When to use it

Use Padé approximation when a function is known through its Taylor coefficients and must be evaluated beyond their radius of convergence, or near poles; for summing slowly convergent or divergent series (perturbation series in physics); for the matrix exponential; and as the starting point of rational minimax approximation. For approximation on a whole interval from function values, prefer [rational approximation](/rational-approximation/) methods based on samples, such as AAA, or [Chebyshev interpolation](/chebyshev-interpolation/) when $f$ is smooth.

## Pitfalls

- **Froissart doublets.** Noise or rounding in the coefficients produces pole-zero pairs that are not features of $f$. Check for poles with a nearby zero, or use the SVD-based robust algorithm.
- **Blocks.** For even or odd $f$, or for a rational $f$ of lower type, the Toeplitz matrix is singular and the requested entry does not exist with $q(0) = 1$; the cosine $[1/1]$ is an example. Use a neighbouring entry or the reduced form.
- **Ill-conditioning in floating point.** For high orders the Toeplitz matrix can be badly conditioned, and the coefficients of $p$ and $q$ are then inaccurate even when $p/q$ is accurate. Judge accuracy by values of $r$, not by coefficients.
- **Poles in the region of interest.** A real pole of $r$ inside the interval where it is used gives a wrong, even infinite, value. Inspect the zeros of $q$.
- **Defects of the definition.** The Baker definition ($q(0) = 1$) and the Frobenius definition (any $q \ne 0$) differ in blocks; libraries differ too.

## Implementations

## History

Rational approximants matching a power series were studied by Jacobi and by Frobenius (1881), who showed the uniqueness of the rational function. Padé's thesis (1892) arranged them into the table that bears his name and described its blocks. De Montessus de Ballore (1902) proved convergence along rows for meromorphic functions. Physicists revived the method in the 1960s for summing perturbation series, Baker's books made it standard, and Wynn's epsilon algorithm (1956) linked it to sequence acceleration. Gonnet, Güttel and Trefethen (2013) gave the SVD-based robust version.

## References
