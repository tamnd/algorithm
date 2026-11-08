---
tag: JHNPEY
kind: concept
slug: finite-differences
name: Finite differences
aliases:
- Difference table
- Forward and backward differences
- delta operator
- difference operator
- discrete derivative
- forward difference
- central difference
area: numerical/interpolation-and-approximation
level: intro
summary: Differences of values on an equally spaced grid, such as Δf(x) = f(x + h) - f(x). A polynomial of degree m has constant m-th differences, and Δ^k f / h^k approximates the k-th derivative.
prereqs: [divided-differences, polynomial]
see_also: [divided-differences, newton-interpolation, catastrophic-cancellation, richardson-extrapolation, interpolation-problem, euler-maclaurin-formula]
sources:
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.3, Finite differences and table-oriented interpolation formulas; Section 3.4, Errors in data and forward differences; Section 5.7, Numerical differentiation (the effect of rounding errors on the step size)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 2.6, Finite and infinite calculus (the difference operator, falling powers and summation by parts) and Section 5.3 (Newton series)
  - book: isbn:9780486624952
    title: Philip J. Davis, Interpolation and Approximation, Dover, 1975 (first published 1963)
    locator: Chapter II, Interpolation (the Newton forward difference formula)
---

Finite differences are the differences of the values of a function on an equally spaced grid $x_j = x_0 + jh$. The forward difference is $\Delta f(x) = f(x + h) - f(x)$, and higher orders are $\Delta^{k} f = \Delta(\Delta^{k-1} f)$. On such a grid they are [divided differences](/divided-differences/) up to a fixed factor, $\Delta^k f(x_0) = k!\, h^k f[x_0, \ldots, x_k]$, so they give the Newton form of the interpolant on equally spaced data, approximate derivatives, and turn sums into a discrete calculus.

## In plain words

Write the values of a function at evenly spaced points in a column. In the next column, write the difference of each pair of neighbors. Repeat on the new column. This is a difference table, and people used it for centuries to build and check tables of logarithms and sines.

For a polynomial, the columns become constant after a few steps: a cubic gives a constant third column and zeros after it. A smooth function gives columns that shrink fast. A mistake in one entry of the original table shows up as a growing zigzag pattern in the later columns, so the table finds typing errors. Divide a difference by the step size and you get an estimate of the slope, which is how a computer often estimates a derivative.

## The idea

**Operators.** With step $h > 0$ define the shift $E f(x) = f(x + h)$ and
$$\Delta f(x) = f(x + h) - f(x), \qquad \nabla f(x) = f(x) - f(x - h), \qquad \delta f(x) = f(x + \tfrac{h}{2}) - f(x - \tfrac{h}{2}),$$
the forward, backward and central differences. So $\Delta = E - I$, and since $E$ and $I$ commute, the binomial theorem gives
$$\Delta^k f(x) = \sum_{j=0}^{k} (-1)^{k-j} \binom{k}{j} f(x + jh).$$
Write $f_j = f(x_0 + jh)$. The difference table holds $\Delta^k f_j$ in column $k$; building columns $1$ to $n$ from $n + 1$ values costs $n(n+1)/2$ subtractions and no division.

**Relation to divided differences.** For $x_j = x_0 + jh$,
$$f[x_0, \ldots, x_k] = \frac{\Delta^k f_0}{k!\, h^k}.$$
*Proof.* By induction on $k$; $k = 0$ is trivial. The divided difference recurrence gives $f[x_0, \ldots, x_k] = (f[x_1, \ldots, x_k] - f[x_0, \ldots, x_{k-1}])/(kh)$, and by the hypothesis the numerator is $(\Delta^{k-1} f_1 - \Delta^{k-1} f_0)/((k-1)!\, h^{k-1}) = \Delta^k f_0 / ((k-1)!\, h^{k-1})$. $\square$

**Polynomials.** If $f$ is a polynomial of degree $m$ with leading coefficient $a_m$, then $\Delta^m f = m!\, a_m h^m$ is constant and $\Delta^{m+1} f = 0$. This follows from the relation above and the leading coefficient property of divided differences. Conversely, for a function sampled on a grid, constant $m$-th differences on $m + 2$ or more consecutive values mean that these values lie on a polynomial of degree $m$.

**Derivatives.** For $f \in C^{k}$, the mean value property of divided differences gives $\Delta^k f(x)/h^k = f^{(k)}(\xi)$ for some $\xi \in [x, x + kh]$. With more smoothness, Taylor's theorem gives the leading error terms
$$\frac{\Delta f(x)}{h} = f'(x) + \frac{h}{2} f''(\xi_1), \qquad \frac{f(x + h) - f(x - h)}{2h} = f'(x) + \frac{h^2}{6} f'''(\xi_2)$$
for $f \in C^2$ and $f \in C^3$ respectively, with $\xi_1 \in (x, x+h)$ and $\xi_2 \in (x - h, x + h)$. These errors cancel in [Richardson extrapolation](/richardson-extrapolation/), which removes the leading power of $h$.

**Newton's forward difference formula.** With $x = x_0 + sh$,
$$p_n(x_0 + sh) = \sum_{k=0}^{n} \binom{s}{k} \Delta^k f_0, \qquad \binom{s}{k} = \frac{s(s-1)\cdots(s-k+1)}{k!},$$
which is the Newton form of the interpolant at $x_0, \ldots, x_n$ rewritten with the relation above. The backward form uses $\nabla^k f_n$ and the nodes nearest the right end. Gauss, Stirling and Bessel formulas use central differences around a middle node.

**Discrete calculus.** With $h = 1$ and the falling power $x^{\underline{m}} = x(x-1)\cdots(x-m+1)$, $\Delta x^{\underline{m}} = m\, x^{\underline{m-1}}$, the analogue of $\frac{d}{dx} x^m = m x^{m-1}$. Sums become differences: if $\Delta F = f$, then $\sum_{j=a}^{b-1} f(j) = F(b) - F(a)$ (Graham, Knuth and Patashnik, Section 2.6).

**Errors in a table.** An error $\varepsilon$ in the single entry $f_j$ adds $(-1)^{k-i}\binom{k}{i}\varepsilon$ to $\Delta^k f_{j-i}$, by the binomial formula. So it grows to a zigzag with the binomial coefficients in column $k$, with largest size $\binom{k}{\lfloor k/2 \rfloor}\varepsilon$. Independent errors of size at most $\varepsilon$ in all entries give errors of size up to $2^k \varepsilon$ in column $k$ (Atkinson, Section 3.4). Meanwhile the true differences of a smooth function shrink like $h^k f^{(k)}$, so beyond some order the table shows only noise.

**Rounding in a derivative.** In floating point with unit roundoff $u$, the forward quotient $(\hat f(x+h) - \hat f(x))/h$ has a truncation error near $\tfrac{h}{2}|f''|$ and a rounding error up to about $2u|f|/h$, from the [cancellation](/catastrophic-cancellation/) in the numerator. The sum is smallest near $h = 2\sqrt{u |f|/|f''|}$, which is of order $\sqrt{u}$ for a well-scaled $f$; the error is then also of order $\sqrt{u}$. For the central quotient the best $h$ is of order $u^{1/3}$ and the error of order $u^{2/3}$ (Atkinson, Section 5.7).

## Examples

**The table of $x^3$.** For $f(x) = x^3$ at $x = 0, 1, \ldots, 6$ with $h = 1$:

| $f_j$ | 0 | 1 | 8 | 27 | 64 | 125 | 216 |
|---|---|---|---|---|---|---|---|
| $\Delta f_j$ | 1 | 7 | 19 | 37 | 61 | 91 | |
| $\Delta^2 f_j$ | 6 | 12 | 18 | 24 | 30 | | |
| $\Delta^3 f_j$ | 6 | 6 | 6 | 6 | | | |
| $\Delta^4 f_j$ | 0 | 0 | 0 | | | | |

The third differences are $3! \cdot 1 \cdot 1^3 = 6$. Newton's formula with $s = x$ and the top row $0, 1, 6, 6$ gives $x^3 = x + 6\binom{x}{2} + 6\binom{x}{3}$, which is the expansion of $x^3$ in falling powers, $x^{\underline{1}} + 3x^{\underline{2}} + x^{\underline{3}}$.

**Finding an error.** Change the entry $f_4 = 64$ of the table of $x^3$ on $x = 0, \ldots, 8$ to $65$. The fourth differences, zero before, become $1, -4, 6, -4, 1$: the binomial pattern of the error, centered on the bad entry.

**A derivative in double precision.** For $f = e^x$ at $x = 1$, the errors of the forward quotient $\Delta f(1)/h$ and the central quotient are:

| $h$ | $10^{-1}$ | $10^{-2}$ | $10^{-4}$ | $10^{-6}$ | $10^{-8}$ | $10^{-10}$ | $10^{-12}$ |
|---|---|---|---|---|---|---|---|
| forward | $1.4 \times 10^{-1}$ | $1.4 \times 10^{-2}$ | $1.4 \times 10^{-4}$ | $1.4 \times 10^{-6}$ | $6.6 \times 10^{-9}$ | $1.5 \times 10^{-6}$ | $4.3 \times 10^{-4}$ |
| central | $4.5 \times 10^{-3}$ | $4.5 \times 10^{-5}$ | $4.5 \times 10^{-9}$ | $1.6 \times 10^{-10}$ | $6.6 \times 10^{-9}$ | $6.7 \times 10^{-7}$ | $2.1 \times 10^{-4}$ |

The forward error falls like $h e/2$ until $h$ is near $\sqrt{u} \approx 10^{-8}$ and then rises like $u/h$. The central error falls like $h^2 e/6$ and is smallest near $h = 10^{-6}$, of order $u^{1/3} \approx 5 \times 10^{-6}$.

**Non-example.** On the unequal nodes $0, 1, 3$ the differences of $f = x^2$ are $1, 8$ and then $7$, which is not $2!\, h^2$ for any single $h$. Plain differences need equal spacing; on unequal nodes use [divided differences](/divided-differences/).

## Where it is used

- [Newton interpolation](/newton-interpolation/) on equally spaced tables, and the classical formulas of Gauss, Stirling and Bessel.
- Numerical differentiation and the finite difference methods for differential equations, with [Richardson extrapolation](/richardson-extrapolation/) to raise the order.
- The [Euler-Maclaurin formula](/euler-maclaurin-formula/) and summation of series, through the discrete calculus of $\Delta$.
- Sequence acceleration: [Aitken's delta-squared process](/aitken-delta-squared/) is built from $\Delta s_k$ and $\Delta^2 s_k$.
- Checking and building tables: constant high differences and the binomial pattern of an error; the difference engines of the nineteenth century tabulated polynomials by additions only.

## References
