---
tag: AEGV52
kind: algorithm
slug: newton-interpolation
name: Newton interpolation
aliases:
- Newton divided-difference interpolation
- Newton form of the interpolating polynomial
- Newton's divided-difference formula
area: numerical/interpolation-and-approximation
level: intro
summary: Build the interpolating polynomial in the Newton basis from a table of divided differences in Θ(n^2) operations, evaluate it by nested multiplication in Θ(n), and add a node in Θ(n).
solves: [polynomial-interpolation]
model: real-ram
complexity:
  vars: {n: "the degree bound, with n + 1 nodes"}
  time: {build: Θ(n^2), evaluate: Θ(n), append: Θ(n)}
  space: {extra: Θ(n)}
  flops: {build: "3n(n+1)/2", evaluate: "3n"}
properties: {deterministic: true, recursive: false, exact_on_polynomials: true, incremental: true, hermite_data: true}
history:
  year: 1711
  people: [Isaac Newton]
  note: Newton gave the divided-difference interpolation formula in the Principia (1687, Book III, Lemma V) and in the Methodus differentialis (1711).
prereqs: [polynomial-interpolation, divided-differences, horner-rule]
see_also: [lagrange-interpolation, barycentric-interpolation, neville-algorithm, hermite-interpolation, polynomial-interpolation-error-theorem, finite-differences]
sources:
  - book: isbn:9780471500230
    title: Kendall E. Atkinson, An Introduction to Numerical Analysis, second edition, Wiley, 1989
    locator: Section 3.2, Newton divided differences (the Newton form, the recursive formula and the error term)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 6, Polynomial interpolation (divided differences and the Newton form)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 5, Divided differences (the recurrence, repeated arguments and Hermite data)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter I, Polynomial interpolation (divided differences, osculatory interpolation and the Newton form)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5, Polynomials (Section 5.3, the Newton form and polynomial interpolation, with the effect of the ordering of the nodes)
  - paper: "Lothar Reichel, Newton interpolation at Leja points, BIT Numerical Mathematics 30 (1990) 332-346"
    locator: the stability of the Newton form when the nodes are taken in Leja order
  - paper: "Erik Meijering, A chronology of interpolation: from ancient astronomy to modern signal and image processing, Proceedings of the IEEE 90(3) (2002) 319-342"
    locator: the section on the seventeenth and eighteenth centuries (Newton's formulas)
---

Newton interpolation writes the interpolating polynomial $p_n$ of the data $(x_0, y_0), \ldots, (x_n, y_n)$ in the Newton basis $1, (x - x_0), (x - x_0)(x - x_1), \ldots$, with the [divided differences](/divided-differences/) $f[x_0, \ldots, x_k]$ as coefficients. The table of divided differences costs $\Theta(n^2)$ operations, the value at a point costs $\Theta(n)$ by a nested multiplication like [Horner's rule](/horner-rule/), and a new node costs only $\Theta(n)$. The same table with repeated nodes solves the [Hermite interpolation](/hermite-interpolation/) problem.

## In plain words

Start with a constant that matches the first data point. Add a straight-line term that is zero at the first point and fixes the second. Add a term that is zero at the first two points and fixes the third, and so on. Each new term keeps all the points already matched, because it is zero there, and it repairs only the newest point.

The weights of these terms come from a triangular table of differences of the data, each divided by the distance between the points involved. Once you have the weights, you get the value at any place by a short loop of multiply-and-add steps. When a new measurement arrives, you add one new diagonal to the table and one new term. Nothing that you computed before changes.

## The problem

Notation on the interpolation pages: $f$ is a function on $[a, b]$, the data are $y_i = f(x_i)$, $\mathcal{P}_n$ is the space of polynomials of degree at most $n$, and $\omega_k(x) = \prod_{i=0}^{k-1} (x - x_i)$. The input is a list of nodes $z_0, \ldots, z_n$ and data. If all nodes are distinct, the data are $y_i = f(z_i)$, and the output is $p_n \in \mathcal{P}_n$ with $p_n(z_i) = y_i$ ([polynomial interpolation](/polynomial-interpolation/)). If a node repeats $m$ times, the copies must be adjacent and the data at it are $f(z), f'(z), \ldots, f^{(m-1)}(z)$; then $p_n$ must match all of them (Hermite data).

The output is the Newton form
$$p_n(x) = \sum_{k=0}^{n} c_k\, \omega_k(x), \qquad c_k = f[z_0, \ldots, z_k],$$
where the divided differences are defined by $f[z_i] = f(z_i)$ and
$$f[z_i, \ldots, z_{i+k}] = \begin{cases} \dfrac{f[z_{i+1}, \ldots, z_{i+k}] - f[z_i, \ldots, z_{i+k-1}]}{z_{i+k} - z_i} & z_{i+k} \ne z_i, \\[2ex] \dfrac{f^{(k)}(z_i)}{k!} & z_i = z_{i+1} = \cdots = z_{i+k}. \end{cases}$$

## The algorithm

```pseudo id=main
NEWTON-COEFFICIENTS(z, y, D)        ▷ z[0 .. n], equal nodes adjacent; D(z, k) = f⁽ᵏ⁾(z)
L1  for i ← 0 to n do c[i] ← y[i]
L2  for k ← 1 to n do
L3      for i ← n downto k do       ▷ c[i] = f[z_(i−k+1) .. z_i] before the update
L4          if z[i] = z[i − k] then c[i] ← D(z[i], k) / k!
L5          else c[i] ← (c[i] − c[i − 1]) / (z[i] − z[i − k])
L6  return c                        ▷ c[k] = f[z_0 .. z_k]

NEWTON-EVALUATE(z, c, t)
L7  p ← c[n]
L8  for k ← n − 1 downto 0 do
L9      p ← p · (t − z[k]) + c[k]
L10 return p
```

The array $c$ holds one column of the divided-difference table at a time. Pass $k$ of lines L3 to L5 turns the differences of order $k - 1$ into those of order $k$. It runs from the bottom up, so when it updates $c[i]$ the entry $c[i - 1]$ still holds the old value of order $k - 1$. At the end $c[k]$ is the top entry of column $k$, the Newton coefficient $f[z_0, \ldots, z_k]$. Line L4 applies only to a block of equal nodes: because equal nodes are adjacent, $z[i] = z[i - k]$ means that all of $z[i - k], \ldots, z[i]$ are equal. For distinct nodes $D$ is never called.

NEWTON-EVALUATE computes $c_0 + (t - z_0)(c_1 + (t - z_1)(c_2 + \cdots))$ from the inside out, as Horner's rule does for the monomial basis. If $t$ is a node $z_j$, all terms with $k > j$ contain the factor $t - z_j = 0$ and contribute exactly 0.

## Example

Take the nodes $0, 1, 2, 4, 5$ and the data $y_i = 2^{x_i}$: $1, 2, 4, 16, 32$. The array $c$ after each pass of line L2 is:

| after pass | $c[0]$ | $c[1]$ | $c[2]$ | $c[3]$ | $c[4]$ |
|---|---|---|---|---|---|
| L1 | 1 | 2 | 4 | 16 | 32 |
| $k = 1$ | 1 | 1 | 2 | 6 | 16 |
| $k = 2$ | 1 | 1 | $\tfrac{1}{2}$ | $\tfrac{4}{3}$ | $\tfrac{10}{3}$ |
| $k = 3$ | 1 | 1 | $\tfrac{1}{2}$ | $\tfrac{5}{24}$ | $\tfrac{1}{2}$ |
| $k = 4$ | 1 | 1 | $\tfrac{1}{2}$ | $\tfrac{5}{24}$ | $\tfrac{7}{120}$ |

For instance, in pass $k = 2$ the entry $c[3]$ becomes $(6 - 2)/(4 - 1) = \tfrac{4}{3}$. So
$$p_4(x) = 1 + x + \tfrac{1}{2}x(x - 1) + \tfrac{5}{24}x(x - 1)(x - 2) + \tfrac{7}{120}x(x - 1)(x - 2)(x - 4).$$
NEWTON-EVALUATE at $t = 3$ gives $p = \tfrac{7}{120}$, then $\tfrac{7}{120}(3 - 4) + \tfrac{5}{24} = \tfrac{3}{20}$, then $\tfrac{3}{20} \cdot 1 + \tfrac{1}{2} = \tfrac{13}{20}$, then $\tfrac{13}{20} \cdot 2 + 1 = \tfrac{23}{10}$, then $\tfrac{23}{10} \cdot 3 + 1 = \tfrac{79}{10}$. So $p_4(3) = 7.9$ against $2^3 = 8$.

The error agrees with the [error theorem](/polynomial-interpolation-error-theorem/): $f(3) - p_4(3) = \tfrac{f^{(5)}(\xi)}{5!}\, \omega(3)$ with $\omega(3) = 3 \cdot 2 \cdot 1 \cdot (-1) \cdot (-2) = 12$ and $f^{(5)}(\xi) = (\ln 2)^5 2^{\xi}$. The equation $0.1 = 0.1\, (\ln 2)^5\, 2^{\xi}$ gives $\xi = -5 \log_2 \ln 2 \approx 2.64$, inside $(0, 5)$.

**Hermite data.** For $f(x) = x^4$ with $f$ and $f'$ given at 0 and at 1, the nodes are $0, 0, 1, 1$ and the data are $f(0) = 0$, $f'(0) = 0$, $f(1) = 1$, $f'(1) = 4$. Line L4 sets $c[1] = f'(0) = 0$ in pass 1, and the passes give $c = (0, 0, 1, 2)$. So $p_3(x) = x^2 + 2x^2(x - 1) = 2x^3 - x^2$, which has $p_3(1) = 1$ and $p_3'(1) = 4$.

## Correctness

After NEWTON-COEFFICIENTS, $c[k] = f[z_0, \ldots, z_k]$ for each $k$. The key invariant is: before pass $k$ of line L2, $c[i] = f[z_{i-k+1}, \ldots, z_i]$ for $i \ge k - 1$, and $c[i] = f[z_0, \ldots, z_i]$ for $i < k - 1$. The Newton form with these coefficients interpolates the data, because $p_k = p_{k-1} + f[z_0, \ldots, z_k]\, \omega_k$ and $\omega_k$ vanishes, with its derivatives of the needed order, at $z_0, \ldots, z_{k-1}$. NEWTON-EVALUATE returns $\sum_k c_k \omega_k(t)$ by induction on the loop. The full proofs are in the correctness proof below.

## Complexity

**Coefficients.** For each $k$ from 1 to $n$, line L5 runs $n - k + 1$ times, with two subtractions and one division. That is $\sum_{k=1}^{n} (n - k + 1) = n(n+1)/2$ updates and $3n(n+1)/2$ operations, $\Theta(n^2)$ in every case. Line L4 costs one division for each update that it makes, with $k!$ computed once per pass. The array $c$ is the only extra storage: $\Theta(n)$.

**Evaluation.** Lines L8 and L9 run $n$ times, with one subtraction, one multiplication and one addition: $3n$ operations, $\Theta(n)$. Evaluating at $m$ points costs $\Theta(n^2 + mn)$ in total.

**Adding a node.** Keep also the bottom diagonal $b_k = f[z_{n-k}, \ldots, z_n]$, $k = 0, \ldots, n$. For a new distinct node $z_{n+1}$, set $b'_0 = y_{n+1}$ and $b'_k = (b'_{k-1} - b_{k-1})/(z_{n+1} - z_{n-k+1})$ for $k = 1, \ldots, n + 1$. Then $c_{n+1} = b'_{n+1}$, and the old coefficients do not change: $3(n+1)$ operations, $\Theta(n)$.

**Rounding errors.** The accuracy of the computed divided differences depends on the order of the nodes (Higham, Section 5.3). For $f(x) = e^x$ at the $n + 1$ Chebyshev points of the second kind on $[-1, 1]$, in double precision, the maximum error of the computed $p_n$ on a grid is:

| $n$ | nodes in increasing order | nodes in Leja order |
|---|---|---|
| 20 | $8.9 \times 10^{-16}$ | $8.9 \times 10^{-16}$ |
| 40 | $1.6 \times 10^{-14}$ | $1.2 \times 10^{-15}$ |
| 60 | $1.8 \times 10^{-4}$ | $1.9 \times 10^{-15}$ |
| 100 | $1.5 \times 10^{15}$ | $1.3 \times 10^{-15}$ |

In Leja order each new node maximizes the product of its distances to the nodes already chosen; Reichel (1990) analyzed this ordering. These figures are observed in practice; no simple bound covers all orders.

## Properties

- **Incremental.** Adding a node appends one coefficient and keeps the old ones. The partial sums $p_0, p_1, \ldots, p_n$ are the interpolants of the leading subsets of the nodes, so $|c_{k+1} \omega_{k+1}(t)|$ is a cheap estimate of the error of $p_k(t)$.
- **Exact on polynomials.** If $f \in \mathcal{P}_m$ with $m < n$, then $c_k = 0$ for $k > m$ in exact arithmetic.
- **Hermite data.** Repeated nodes need no new code beyond line L4.
- **Order dependent in floating point.** The polynomial does not depend on the order of the nodes, but the coefficients and the rounding errors do.
- **Symmetric divided differences.** $f[z_0, \ldots, z_k]$ does not depend on the order of its arguments, and for $f \in C^k$ it equals $f^{(k)}(\xi)/k!$ for some $\xi$ between the smallest and largest argument.

## Variants and improvements

- **Equispaced nodes.** With $x_i = x_0 + ih$, $f[x_0, \ldots, x_k] = \Delta^k y_0 / (k!\, h^k)$, and the Newton form becomes the Newton forward difference formula in the variable $s = (x - x_0)/h$; see [finite differences](/finite-differences/).
- **Leja ordering.** Reorder the nodes greedily so that each new node is as far as possible, in the product sense, from those before it. This keeps the Newton form stable for many hundreds of Chebyshev points.
- **Exact arithmetic.** Over $\mathbb{Q}$ or a finite field the same table gives the exact coefficients, and the Newton form is the usual route in [sparse polynomial interpolation](/sparse-polynomial-interpolation/) and in Chinese remaindering for polynomials.
- **Several points.** To evaluate at many points, convert the Newton form to the monomial form in $O(n^2)$ by repeated synthetic multiplication, or better, use the [barycentric form](/barycentric-interpolation/).

## When to use it

Use the Newton form when the nodes arrive one at a time, when you want the degree to grow until an error estimate is small, or when the data include derivatives. For a fixed node set and many evaluation points, the second barycentric form costs the same $O(n)$ per point and is stable for good nodes in every order. For a single value with an error estimate and no coefficients, [Neville's algorithm](/neville-algorithm/) is an alternative at $\Theta(n^2)$ per point.

## Pitfalls

- **Overwriting the table in the wrong direction.** If line L3 runs $i$ upward from $k$ to $n$, the update of $c[i]$ uses the new $c[i - 1]$, which already has order $k$. The loop must run downward.
- **Wrong denominator.** The denominator in line L5 is $z[i] - z[i - k]$, the distance between the outermost nodes of the difference, not $z[i] - z[i - 1]$.
- **Repeated nodes that are not adjacent.** Line L4 tests only $z[i] = z[i - k]$. If equal nodes are separated, line L5 divides by zero or uses a wrong formula. Sort the nodes, or at least group equal ones.
- **Bad node order for large n.** The increasing order loses all accuracy for about 100 Chebyshev points (table above). Use Leja order, or the barycentric form.
- **Forgetting the factorial.** Line L4 divides the derivative by $k!$; omitting it gives a polynomial that matches the values but not the derivatives.

## Implementations

## History

Newton stated the divided-difference interpolation formula in the Principia (1687, Book III, Lemma V) and developed it in the Methodus differentialis, published in 1711; Meijering's chronology traces these steps. The treatment of repeated arguments by derivatives is the standard modern one in de Boor and Powell. Higham analyzed the rounding errors of the Newton form, and Reichel (1990) showed the value of the Leja ordering.

## References
