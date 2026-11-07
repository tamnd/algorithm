---
tag: 947TVN
kind: algorithm
slug: horner-rule
name: Horner's rule
aliases:
- Horner's method
- Horner's scheme
- synthetic division
- nested multiplication
area: algebra/polynomial-arithmetic
level: intro
summary: Evaluates a degree-n polynomial with n multiplications and n additions by nested evaluation.
solves: [polynomial-evaluation]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the polynomial}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
  ring_operations: {worst: 2n, best: 2n}
properties: {deterministic: true, in_place: true, recursive: false, online: true}
history:
  year: 1819
  people: [William George Horner, Paolo Ruffini, Qin Jiushao]
  note: Horner published the method in 1819 as part of a method for solving numerical equations; Ruffini had described it in 1804 and 1809, and Qin Jiushao used it in 1247.
prereqs: [polynomial, dense-polynomial-representation, loop-invariant]
see_also: [horners-rule-optimality, factor-theorem, estrin-scheme, paterson-stockmeyer-algorithm, multipoint-evaluation, fused-multiply-add, polynomial-remainder-theorem, polynomial-root-finding]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials (Horner's rule, its history, evaluation of derivatives, adaptation of coefficients, and the optimality results)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.2, Evaluation and interpolation (Horner's rule); Section 9.3, Formal derivatives and Taylor expansion
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 30.1, Representing polynomials (evaluation by Horner's rule in Theta(n) time)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 5, Polynomials (Section 5.1, Horner's method, and its rounding error analysis)
  - paper: doi:10.1098/rstl.1819.0023
    title: W. G. Horner, A new method of solving numerical equations of all orders, by continuous approximation, Philosophical Transactions of the Royal Society of London 109 (1819), 308 to 335
    locator: the whole paper (the nested scheme appears as the step that transforms the equation)
---

Horner's rule evaluates a [polynomial](/polynomial/) $a_0 + a_1 x + \cdots + a_n x^n$ at a point $u$ by rewriting it as $a_0 + u(a_1 + u(a_2 + \cdots + u\, a_n))$ and working from the inside out. It uses $n$ multiplications and $n$ additions and keeps one value in memory, and Pan proved in 1966 that no algorithm for a general polynomial uses fewer ([Horner's rule optimality](/horners-rule-optimality/)). The values it computes on the way are the coefficients of the quotient by $x - u$, so the same loop is synthetic division, and repeating it gives the Taylor expansion at $u$.

## In plain words

To find the value of a polynomial at a number, the obvious way computes each power of the number, multiplies it by its coefficient, and adds the results. Horner's rule does less work. Start with the top coefficient. Then, again and again, multiply the running value by the number and add the next coefficient, going down to the constant. At the end the running value is the answer.

For a polynomial of degree n this is n multiplications and n additions, and it needs no list of powers. The running values on the way have a use too: they are the coefficients of the polynomial that remains after dividing by "x minus the number".

## The problem

This is the [polynomial evaluation](/polynomial-evaluation/) problem. Let $R$ be a commutative ring with $1$. The input is a polynomial $f = \sum_{i=0}^{n} a_i x^i \in R[x]$ in the [dense representation](/dense-polynomial-representation/) $[a_0, \ldots, a_n]$ with $a_n \ne 0$, and a point $u$. The output is $f(u) = \sum_{i=0}^{n} a_i u^i$. The point can be an element of $R$ or of any ring that contains $R$ in its center, for example a square matrix over $R$ or a polynomial; the rule uses only ring operations.

We use the algebraic complexity model: the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$, in which each addition, subtraction and multiplication of ring elements costs 1. The degree is $n$, and the zero polynomial, of degree $-\infty$, is the empty list.

## The algorithm

Write $f(u)$ in nested form:

$$f(u) = a_0 + u\bigl(a_1 + u\bigl(a_2 + \cdots + u(a_{n-1} + u\, a_n)\cdots\bigr)\bigr).$$

Evaluate the innermost bracket first. Each level is one multiplication by $u$ and one addition of a coefficient.

```pseudo id=main
HORNER(a, u)                         ▷ a = [a_0, ..., a_n] normalized; returns f(u)
L1  if a is empty then return 0
L2  s ← a[n]
L3  for i ← n − 1 down to 0 do
L4      s ← s · u + a[i]
L5  return s
```

The values of $s$ after each step of line L4 are useful. Call them $b_{n-1} = a_n$, $b_{i-1} = b_i u + a_i$. Then $f = (x - u)(b_{n-1} x^{n-1} + \cdots + b_0) + f(u)$: the loop divides $f$ by $x - u$, which is the [factor theorem](/factor-theorem/) in algorithmic form. This version is called synthetic division, and it is the deflation step of root finders.

```pseudo id=synthetic
SYNTHETIC-DIVISION(a, u)             ▷ n ≥ 1; returns q, r with f = (x − u) q + r
S1  b[n − 1] ← a[n]
S2  for i ← n − 1 down to 1 do
S3      b[i − 1] ← b[i] · u + a[i]
S4  r ← b[0] · u + a[0]
S5  return (b, r)                    ▷ r = f(u); b holds the quotient, lowest degree first
```

Running synthetic division again on the quotient gives $f'(u)$ as the new remainder, and $n$ rounds give all Taylor coefficients $c_k = f^{(k)}(u)/k!$, with $f(x) = \sum_k c_k (x - u)^k$. In place, this is the Taylor shift, which computes the coefficients of $f(x + u)$:

```pseudo id=taylor
TAYLOR-SHIFT(a, u)                   ▷ returns c with f(x + u) = Σ c_k x^k
T1  c ← a copy of a
T2  for k ← 0 to n − 1 do
T3      for i ← n − 1 down to k do
T4          c[i] ← c[i] + u · c[i + 1]
T5  return c
```

## Example

Evaluate $f = 2x^3 - 6x^2 + 2x - 1$, stored as $[-1, 2, -6, 2]$, at $u = 3$.

| step | line | $i$ | $s$ before | $s \cdot 3 + a_i$ | $s$ after |
|---|---|---|---|---|---|
| start | L2 | | | | $2$ |
| 1 | L4 | 2 | $2$ | $6 - 6$ | $0$ |
| 2 | L4 | 1 | $0$ | $0 + 2$ | $2$ |
| 3 | L4 | 0 | $2$ | $6 - 1$ | $5$ |

So $f(3) = 5$, with 3 multiplications and 3 additions. The direct method computes $3^2 = 9$ and $3^3 = 27$ and then $2 \cdot 27$, $-6 \cdot 9$ and $2 \cdot 3$: 5 multiplications.

The intermediate values $2, 0, 2$ are the quotient: $f = (x - 3)(2x^2 + 0x + 2) + 5$. For the Taylor shift, TAYLOR-SHIFT$(f, 3)$ turns $[-1, 2, -6, 2]$ into $[5, 2, 0, 2]$ after round $k = 0$ (this is synthetic division), into $[5, 20, 6, 2]$ after round 1, and into $[5, 20, 12, 2]$ after round 2. So

$$f(x) = 5 + 20(x - 3) + 12(x - 3)^2 + 2(x - 3)^3,$$

and indeed $f'(3) = 6 \cdot 9 - 12 \cdot 3 + 2 = 20$ and $f''(3)/2 = (12 \cdot 3 - 12)/2 = 12$.

## Correctness

**Invariant.** Before the step of line L4 for the index $i$, $s = \sum_{j=i+1}^{n} a_j u^{j-i-1}$.

*Initialization.* Before the step for $i = n - 1$, line L2 has set $s = a_n$, and the sum has the single term $a_n u^0$.

*Maintenance.* Line L4 sets $s \cdot u + a_i = \sum_{j=i+1}^{n} a_j u^{j-i} + a_i = \sum_{j=i}^{n} a_j u^{j-i}$, which is the invariant for $i - 1$.

*Termination.* After the step for $i = 0$, $s = \sum_{j=0}^{n} a_j u^j = f(u)$. For the empty list, line L1 returns $0 = f(u)$.

The step $(\sum c_j u^j) u = \sum c_j u^{j+1}$ uses only associativity and distributivity, so the rule is correct when $u$ is a matrix or any element of an associative ring that commutes with the coefficients. The proofs for synthetic division and the Taylor shift are in the proof file.

## Complexity

The cost is counted in ring operations in the algebraic complexity model. For a polynomial of degree $n \ge 0$, line L4 runs $n$ times, so HORNER uses exactly $n$ multiplications and $n$ additions, and $\Theta(1)$ extra space: one ring element and a loop index. This bound is proved and exact.

**Optimality (proved).** In the model where the coefficients $a_0, \ldots, a_n$ are indeterminates and $u$ is the input point, every straight-line program that computes $f(u)$ needs at least $n$ multiplications and divisions (Pan, 1966) and at least $n$ additions and subtractions. So Horner's rule is optimal for a general polynomial. Borodin showed in 1971 that it is the only optimal algorithm in a precise sense. See [Horner's rule optimality](/horners-rule-optimality/) for the statements and the sources.

**When the polynomial is fixed (proved).** If the same $f$ is evaluated at many points, its coefficients can be transformed once in advance. Knuth's Section 4.6.4 describes such "adaptation of coefficients" schemes that use about $\lfloor n/2 \rfloor + 2$ multiplications and $n$ additions per point, Motzkin showed that about $n/2$ multiplications are still needed with such a preparation, and Belaga that $n$ additions are needed. The transformation needs roots of auxiliary polynomials, so it is practical over $\mathbb{R}$ or $\mathbb{C}$ for small fixed $n$ and not over exact rings in general.

**Many points.** Evaluating at $m$ points by Horner costs $mn$ multiplications. For $m \approx n$, [fast multipoint evaluation](/fast-multipoint-evaluation/) costs $O(M(n) \log n)$, where $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. The crossover where the fast method wins depends on the ring and the machine; in practice it is observed at degrees in the hundreds or thousands.

**Synthetic division and Taylor shift.** SYNTHETIC-DIVISION has the cost of HORNER. TAYLOR-SHIFT runs line T4 $n + (n-1) + \cdots + 1 = n(n+1)/2$ times, so $\Theta(n^2)$ ring operations. Over a ring where $n!$ is invertible, the Taylor shift costs $O(M(n))$ by a single product (von zur Gathen and Gerhard, Section 9.3).

**Time on a real machine (observed).** Each step depends on the result of the previous one, so the loop is a chain of $n$ dependent multiply-add steps. Its time is bounded by the latency of one multiply-add times $n$, not by the throughput of the processor. For floating point evaluation of large degree, [Estrin's scheme](/estrin-scheme/), which has more independent work, is often faster on hardware with several pipelined multipliers, and slower on simple hardware.

## Properties

- **Exact count.** $n$ multiplications and $n$ additions for degree $n$, independent of the values.
- **Constant extra space.** One running value. The coefficients are read once, from the top down, so they can come from a stream: the algorithm is online in the coefficients, highest first.
- **Inherently sequential.** The dependency chain has length $2n$ ring operations (or $n$ fused multiply-adds). The [critical path](/critical-path/) is $\Theta(n)$, while Estrin's scheme has critical path $O(\log n)$.
- **Works over any associative ring.** The point may be a matrix, a polynomial (this is composition $f(g)$), or an element of $\mathbb{Z}/m\mathbb{Z}$ for any $m$.
- **Backward stable in floating point.** In IEEE arithmetic with unit roundoff $\mathbf{u}$, the computed value is the exact value of a polynomial whose coefficients have relative changes at most $\gamma_{2n} = 2n\mathbf{u}/(1 - 2n\mathbf{u})$. So the error is at most $\gamma_{2n} \sum |a_i| |u|^i$ (Higham, Section 5.1). The relative error can still be large near a root, where $|f(u)|$ is much smaller than $\sum |a_i||u|^i$.

## Variants and improvements

- **Synthetic division and deflation.** The intermediate values give the quotient by $x - u$ (pseudocode `synthetic`). Root finders divide out each root they find and continue with the quotient.
- **Value and derivative together.** Run a second accumulator $d \leftarrow d \cdot u + s$ before each update of $s$. This gives $f(u)$ and $f'(u)$ with $2n - 1$ multiplications, the inner loop of Newton's method for roots.
- **Taylor shift.** $n$ rounds of synthetic division give $f(x + u)$ in $\Theta(n^2)$ (pseudocode `taylor`). This is used in [real root isolation](/real-root-isolation/) by the [Vincent](/vincent-theorem/) method.
- **Division by a quadratic.** Bairstow's method divides by $x^2 - px - q$ with a two-term recurrence. This evaluates a real polynomial at a complex point $z$ in real arithmetic, with $p = 2\operatorname{Re} z$ and $q = -|z|^2$.
- **Second-order Horner.** Split $f(x) = g(x^2) + x\, h(x^2)$ and evaluate $g$ and $h$ at $x^2$ by Horner's rule, in two independent chains. This halves the critical path at the cost of one extra multiplication. Splitting into $k$ chains gives $k$-th order Horner.
- **Estrin's scheme.** Pair the coefficients, then pair the pairs, with $u^2, u^4, \ldots$ as multipliers. It has depth $O(\log n)$ and about the same number of operations. See [Estrin's scheme](/estrin-scheme/).
- **Expensive point.** When multiplication by $u$ is much more costly than multiplication by a coefficient, as for matrices or power series, the [Paterson-Stockmeyer algorithm](/paterson-stockmeyer-algorithm/) uses $O(\sqrt n)$ nonscalar multiplications instead of $n$.
- **Radix conversion.** Reading the digits of a number from the top with $s \leftarrow s \cdot 10 + d$ is Horner's rule at $u = 10$. Converting a decimal string to an integer uses it.
- **Compensated Horner.** In floating point, an error-free transformation of each product and sum recovers the rounding error and adds it back at the end. The result is about as accurate as Horner's rule in twice the working precision.

## When to use it

Use Horner's rule to evaluate a polynomial at one point, or at a few points, whatever the ring. It is the default in numerical libraries for polynomial approximations of elementary functions, often combined with Estrin's scheme for the high-order part. Use synthetic division when the quotient by $x - u$ is needed, as in root finding. For many points at once, use [fast multipoint evaluation](/fast-multipoint-evaluation/) when the number of points and the degree are large; for points that are roots of unity, use the [FFT](/fast-fourier-transform/). For a point that is a matrix or another expensive object, use [Paterson-Stockmeyer](/paterson-stockmeyer-algorithm/).

## Pitfalls

- **Coefficient order.** HORNER starts at the highest coefficient. With a list stored lowest degree first, the loop must run from the end of the list; running it from the start evaluates the reversed polynomial $x^n f(1/x)$. The worked example gives $f(3) = 5$, while the wrong order gives $-1 \cdot 27 + 2 \cdot 9 - 6 \cdot 3 + 2 = -25$.
- **Leading zeros.** If the list has top zero entries, the result is still right, but the cost and the degree of the synthetic quotient are wrong. Normalize the list first.
- **Overflow in fixed width.** Over $\mathbb{Z}/m\mathbb{Z}$ with machine integers, $s \cdot u + a_i$ can overflow before the reduction. Reduce after each product, or use a double-width type.
- **Cancellation in floating point.** Near a multiple root, many terms cancel, and the computed value is mostly rounding error. The error bound $\gamma_{2n}\sum |a_i||u|^i$ shows how large the noise can be; use it to decide whether a computed value is zero.
- **The empty polynomial.** Line L1 returns $0$. Code that starts with `s = a[n]` without this check fails on the zero polynomial.
- **Expecting parallel speed.** Each step needs the previous one. Splitting the loop across threads does not help; use Estrin's scheme or second-order Horner.

## Implementations

## History

Horner published the method in 1819 in the Philosophical Transactions of the Royal Society, as the step of a method for the numerical solution of equations by successive transformations. Ruffini had described the same procedure in 1804 and 1809, and the method is known as Ruffini's rule in some countries. Qin Jiushao used it in his Mathematical Treatise in Nine Sections (1247), and Knuth's Section 4.6.4 traces the idea further, including its use by Newton. Ostrowski asked in 1954 whether the rule is optimal, Pan proved the bound on multiplications in 1966, and Borodin proved in 1971 that it is the unique optimal algorithm.

## References
