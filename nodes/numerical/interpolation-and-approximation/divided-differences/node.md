---
tag: 77WZBK
kind: concept
slug: divided-differences
name: Divided differences
aliases:
- Newton divided differences
- divided difference table
- confluent divided differences
area: numerical/interpolation-and-approximation
level: intro
summary: Recursive difference quotients f[x_0, ..., x_k] of data values. They are the coefficients of the Newton form of the interpolating polynomial and equal f^(k)(ξ)/k! for a smooth f.
prereqs: [interpolation-problem, lagrange-interpolation]
see_also: [newton-interpolation, finite-differences, hermite-interpolation, neville-algorithm, polynomial-interpolation-error-theorem, catastrophic-cancellation, horner-rule, interpolating-polynomial-uniqueness]
sources:
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 5, Divided differences (the recurrence, the Newton form, the mean value property and repeated arguments)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter I, Polynomial interpolation (divided differences, the Newton form and osculatory interpolation)
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.2, Newton divided differences
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 5.3, The Newton form and polynomial interpolation (rounding errors in divided differences)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation
---

The divided differences of a function $f$ at nodes $x_0, \ldots, x_k$ are the numbers $f[x_0, \ldots, x_k]$ defined by $f[x_i] = f(x_i)$ and a recurrence of difference quotients. The number $f[x_0, \ldots, x_k]$ is the leading coefficient of the polynomial of degree at most $k$ that [interpolates](/interpolation-problem/) $f$ at those nodes, so the divided differences are the coefficients of the [Newton form](/newton-interpolation/) of the interpolant. For a smooth $f$, $f[x_0, \ldots, x_k] = f^{(k)}(\xi)/k!$ for some $\xi$ between the nodes, which makes them discrete derivatives and lets them handle repeated nodes, the data of [Hermite interpolation](/hermite-interpolation/).

## In plain words

The slope between two points of a curve is the difference of the heights divided by the difference of the positions. That is a first divided difference. Do the same with the slopes: take two neighboring slopes, subtract them, and divide by the width that they span. That is a second divided difference, and it measures how fast the slope changes. Keep going to get higher orders.

These numbers do two jobs. They are the coefficients of a simple way to write the polynomial through the points, one new term for each new point. And for a smooth curve, the difference of a given order is close to the derivative of that order divided by a factorial. When two points move together, the slope between them becomes the derivative, so the same table can take derivative values as input.

## The idea

**Definition.** For distinct nodes,
$$f[x_i] = f(x_i), \qquad f[x_i, \ldots, x_{i+k}] = \frac{f[x_{i+1}, \ldots, x_{i+k}] - f[x_i, \ldots, x_{i+k-1}]}{x_{i+k} - x_i}.$$
The *divided difference table* holds $f[x_i, \ldots, x_{i+k}]$ for $0 \le i \le i + k \le n$. Column $k$ has $n + 1 - k$ entries, each from one subtraction of the column before, one subtraction of nodes and one division. The whole table costs $n(n+1)/2$ divisions and $n(n+1)$ subtractions, that is $\tfrac{3}{2} n^2 + O(n)$ operations; the Newton coefficients are its top diagonal $f[x_0], f[x_0, x_1], \ldots, f[x_0, \ldots, x_n]$, and they can be computed in place in one array of length $n + 1$.

Notation on these pages: $f$ is a function on $[a, b]$, the nodes are $x_0, \ldots, x_n$ in $[a, b]$, $p_n$ is the interpolating polynomial of degree at most $n$, and $\omega(x) = \prod_i (x - x_i)$.

**1. Leading coefficient.** Let $p_{i,k}$ be the polynomial of degree at most $k$ that interpolates $f$ at $x_i, \ldots, x_{i+k}$. Then $f[x_i, \ldots, x_{i+k}]$ is the coefficient of $x^k$ in $p_{i,k}$.

*Proof.* By induction on $k$. For $k = 0$, $p_{i,0} = f(x_i)$. For $k \ge 1$, put
$$r(x) = \frac{(x - x_i)\, p_{i+1,k-1}(x) - (x - x_{i+k})\, p_{i,k-1}(x)}{x_{i+k} - x_i}.$$
It has degree at most $k$. At $x_i$ it equals $p_{i,k-1}(x_i) = f(x_i)$; at $x_{i+k}$ it equals $p_{i+1,k-1}(x_{i+k}) = f(x_{i+k})$; at an inner node $x_j$ both polynomials equal $f(x_j)$, and $r(x_j) = f(x_j)\,((x_j - x_i) - (x_j - x_{i+k}))/(x_{i+k} - x_i) = f(x_j)$. By [uniqueness](/interpolating-polynomial-uniqueness/), $r = p_{i,k}$. Its coefficient of $x^k$ is the difference of the leading coefficients of $p_{i+1,k-1}$ and $p_{i,k-1}$, divided by $x_{i+k} - x_i$, which by the induction hypothesis is the recurrence. $\square$ (The formula for $r$ is the step of [Neville's algorithm](/neville-algorithm/).)

**2. Symmetry and the explicit formula.** The leading coefficient of the [Lagrange form](/lagrange-interpolation/) $\sum_j f(x_j) \prod_{m \ne j} (x - x_m)/(x_j - x_m)$ gives
$$f[x_0, \ldots, x_k] = \sum_{j=0}^{k} \frac{f(x_j)}{\prod_{m \ne j} (x_j - x_m)}.$$
So a divided difference does not depend on the order of its nodes, and it is linear in $f$.

**3. The Newton form.** $p_n(x) = \sum_{k=0}^{n} f[x_0, \ldots, x_k] \prod_{j=0}^{k-1} (x - x_j)$. *Proof.* $p_k - p_{k-1}$ (on the first $k+1$ and $k$ nodes) has degree at most $k$ and vanishes at $x_0, \ldots, x_{k-1}$, so it is $c \prod_{j<k} (x - x_j)$; comparing the coefficients of $x^k$ with property 1 gives $c = f[x_0, \ldots, x_k]$. Sum over $k$. $\square$ It is evaluated in $3n$ operations by a nested scheme like [Horner's rule](/horner-rule/).

**4. Error form.** For any $x$ that is not a node, adding $x$ as node $n + 1$ in property 3 gives
$$f(x) - p_n(x) = f[x_0, \ldots, x_n, x]\, \omega(x).$$

**5. Mean value property.** If $f \in C^k[a, b]$ and the distinct nodes $x_0, \ldots, x_k$ lie in $[a, b]$, then $f[x_0, \ldots, x_k] = f^{(k)}(\xi)/k!$ for some $\xi$ in $[\min x_j, \max x_j]$. *Proof.* $e = f - p_{0,k}$ has $k + 1$ distinct zeros. By Rolle's theorem $e'$ has $k$ distinct zeros between them, and after $k$ steps $e^{(k)}$ has a zero $\xi$ in that interval. Since $p_{0,k}^{(k)} = k!\, f[x_0, \ldots, x_k]$ by property 1, the claim follows. $\square$ With property 4 this gives the error formula $f(x) - p_n(x) = f^{(n+1)}(\xi)\, \omega(x)/(n+1)!$ of the [error theorem](/polynomial-interpolation-error-theorem/).

**6. Repeated nodes.** For $f \in C^k$, the Hermite and Genocchi formula
$$f[x_0, \ldots, x_k] = \int_{S_k} f^{(k)}(t_0 x_0 + \cdots + t_k x_k)\, dt,$$
over the simplex $S_k = \{t \ge 0, \sum t_j = 1\}$ with its volume $1/k!$, shows that $f[x_0, \ldots, x_k]$ is a continuous function of the nodes, also when some coincide. When the nodes coalesce, $f[x, \ldots, x]$ with $k + 1$ copies is $f^{(k)}(x)/k!$. In the table, an entry whose two end nodes are equal is filled with that value instead of the quotient $0/0$. The Newton form with such *confluent* divided differences solves the Hermite problem (de Boor, Chapter I; Powell, Chapter 5).

**7. Polynomials.** If $f$ is a polynomial of degree $m$, then $f[x_0, \ldots, x_k]$ is its leading coefficient when $k = m$ and zero when $k > m$, for any nodes (property 1 and uniqueness). On equally spaced nodes this is the statement that $m$-th [finite differences](/finite-differences/) of a degree $m$ polynomial are constant.

**Rounding errors and cancellation.** Each column subtracts nearly equal numbers when the nodes are close, which is [catastrophic cancellation](/catastrophic-cancellation/). The explicit formula of property 2 shows the effect of errors in the data: if each $f(x_j)$ is known only up to $\varepsilon$, the error in $f[x_0, \ldots, x_k]$ can be as large as $\varepsilon \sum_j 1/\prod_{m \ne j} |x_j - x_m|$, attained with the signs of the error chosen against the denominators. For equally spaced nodes with step $h$, $\prod_{m \ne j} |x_j - x_m| = h^k\, j!\, (k - j)!$, so this worst case is $\varepsilon\, 2^k / (k!\, h^k)$, while the true value is near $f^{(k)}/k!$. The relative error can thus grow like $\varepsilon\, 2^k / (h^k |f^{(k)}|)$. Higham (Section 5.3) analyzes the rounding errors of the table itself and of the Newton evaluation. Ordering the nodes (for example in increasing order, or in a Leja order) changes the error of the Newton evaluation but not the bound above for the data errors.

## Examples

**A table.** For the nodes $0, 1, 2, 4$ and the values $1, 2, 4, 16$ (the values of $2^x$):

| $x_i$ | $f[x_i]$ | first | second | third |
|---|---|---|---|---|
| 0 | 1 | | | |
| | | $\frac{2 - 1}{1 - 0} = 1$ | | |
| 1 | 2 | | $\frac{2 - 1}{2 - 0} = \frac{1}{2}$ | |
| | | $\frac{4 - 2}{2 - 1} = 2$ | | $\frac{4/3 - 1/2}{4 - 0} = \frac{5}{24}$ |
| 2 | 4 | | $\frac{6 - 2}{4 - 1} = \frac{4}{3}$ | |
| | | $\frac{16 - 4}{4 - 2} = 6$ | | |
| 4 | 16 | | | |

The top diagonal gives the Newton form $p_3(x) = 1 + x + \tfrac{1}{2} x(x - 1) + \tfrac{5}{24} x(x - 1)(x - 2)$. At $x = 3$ it gives $1 + 3 + 3 + \tfrac{5}{4} = \tfrac{33}{4}$, the same value as the Lagrange form on the [Lagrange page](/lagrange-interpolation/). By property 5, $\tfrac{5}{24} = (\ln 2)^3\, 2^{\xi}/6$ for some $\xi$ in $[0, 4]$; indeed $2^{\xi} = 5/(4 (\ln 2)^3) \approx 3.75$, so $\xi \approx 1.91$.

**Repeated nodes.** Data $f(0) = 1$, $f'(0) = 1$, $f(1) = e$ (from $f = e^x$) use the nodes $0, 0, 1$. Then $f[0, 0] = f'(0) = 1$, $f[0, 1] = e - 1$, and $f[0, 0, 1] = (e - 1 - 1)/(1 - 0) = e - 2$. The Hermite interpolant is $1 + x + (e - 2) x^2$, which matches $f$, $f'$ at 0 and $f$ at 1.

**Cancellation, observed in double precision.** For $f = e^x$ at the nodes $1, 1 + h, \ldots, 1 + kh$, the exact divided difference is $e\,(e^h - 1)^k / (k!\, h^k)$. Computing the table from the rounded values of $e^x$ gives these relative errors:

| $k$ | $h = 0.1$ | $h = 0.01$ | $h = 0.001$ |
|---|---|---|---|
| 2 | $9.5 \times 10^{-15}$ | $4.1 \times 10^{-14}$ | $2.1 \times 10^{-11}$ |
| 4 | $2.4 \times 10^{-12}$ | $5.2 \times 10^{-9}$ | $1.2 \times 10^{-4}$ |
| 6 | $8.6 \times 10^{-10}$ | $1.0 \times 10^{-3}$ | $1.3 \times 10^{3}$ |

At $k = 6$ and $h = 0.001$ the computed value is $-4.8$ while the true value is $3.8 \times 10^{-3}$: not one digit is right, and even the sign is wrong. Each entry stays below the worst case $u\, e^{1+kh}\, 2^k / (k!\, h^k)$ relative to the true value, with $u = 2^{-53}$.

**Non-example.** The quotient $(f(x_2) - f(x_0))/(x_2 - x_0)$ is a first divided difference, but $(f[x_1, x_2] - f[x_0, x_1])/(x_2 - x_1)$ is not a second one: the denominator must be the span $x_2 - x_0$ of all the nodes. With the wrong span the table is not symmetric and the Newton form fails to interpolate.

## Where it is used

- [Newton interpolation](/newton-interpolation/): the coefficients of the Newton form, with $O(n)$ work to add a node.
- [Hermite interpolation](/hermite-interpolation/) and [cubic Hermite splines](/cubic-hermite-spline/): confluent divided differences.
- [Finite differences](/finite-differences/): on equispaced nodes, $f[x_0, \ldots, x_k] = \Delta^k f(x_0)/(k!\, h^k)$.
- Splines: B-splines are defined as divided differences of truncated powers (de Boor, Chapter IX), see [B-splines](/b-spline/).
- Root finding: the [secant method](/secant-method/), [Muller's method](/muller-method/) and the analysis of [Steffensen's method](/steffensen-method/) are written with divided differences.
- Error analysis: property 4 and property 5 give the [interpolation error theorem](/polynomial-interpolation-error-theorem/) and the error of [interpolatory quadrature](/interpolatory-quadrature/).

## References
