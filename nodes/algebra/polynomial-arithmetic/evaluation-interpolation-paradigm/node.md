---
tag: Q4JJ5P
kind: technique
slug: evaluation-interpolation-paradigm
name: Evaluation-interpolation paradigm
aliases:
- evaluate and interpolate
- evaluation and interpolation
- evaluation-interpolation method
area: algebra/polynomial-arithmetic
level: core
summary: Multiplies or manipulates polynomials by evaluating at enough points, operating pointwise, and interpolating back.
prereqs: [point-value-representation, polynomial, factor-theorem]
see_also: [fft-polynomial-multiplication, karatsuba-multiplication, toom-cook-multiplication, fast-multipoint-evaluation, fast-interpolation, modular-methods, brown-modular-gcd, chinese-remainder-theorem]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 5, Modular algorithms and interpolation (Section 5.1, Change of representation; Section 5.2, Evaluation and interpolation; Section 5.5, Modular determinant computation; Section 5.6, Hermite interpolation); Section 6.5, Modular gcd algorithm in F[x, y]; Section 8.1, Karatsuba's multiplication algorithm
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 30.1, Representing polynomials (the evaluate, multiply pointwise, interpolate scheme for fast multiplication)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3.2, Karatsuba's algorithm, and Section 1.3.3, Toom-Cook multiplication (multiplication as evaluation and interpolation at chosen points, including infinity)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.3, How fast can we multiply? (Toom-Cook as evaluation and interpolation); Section 4.6.4, Evaluation of polynomials (interpolation)
---

The evaluation-interpolation paradigm computes a polynomial result by working with values instead of coefficients. It evaluates the inputs at enough points, solves the problem separately at each point, where the polynomials have become ring elements, and then interpolates the values back into a polynomial. It works because evaluation at a point is a ring homomorphism, and because a polynomial of degree less than $N$ is fixed by its values at $N$ distinct points. FFT multiplication, Karatsuba and Toom-Cook multiplication, modular determinant and resultant algorithms, and Brown's gcd algorithm are all instances.

## In plain words

Some problems on polynomials are hard to solve with the polynomials themselves, but easy to solve with numbers. The idea is to replace each polynomial by its values at a set of chosen numbers. At each number, the problem is now about plain numbers, so it is easy. Then the answers at all the numbers are glued back into one polynomial.

This gives the right answer if two things are true. First, the steps of the problem must give the same result whether they are done before or after putting in a number; this is true for adding, subtracting and multiplying. Second, there must be enough numbers: one more than the degree of the answer.

## When it applies

The technique fits a problem when these conditions hold.

1. **The result is a polynomial expression in the inputs.** Let $h = \Phi(f_1, \ldots, f_k)$, where $\Phi$ is built from additions, subtractions and multiplications in $R[x]$, for example a product, a determinant of a matrix with polynomial entries, or a resultant. Evaluation at $u$ is a ring homomorphism $R[x] \to R$, so $h(u) = \Phi(f_1(u), \ldots, f_k(u))$: the problem can be solved at each point. Division is allowed only where it is exact and the divisor does not vanish at the point.
2. **There is a degree bound.** Some $D$ with $\deg h \le D$ is known in advance, for example $\deg f + \deg g$ for a product, or $n d$ for the determinant of an $n \times n$ matrix with entries of degree at most $d$.
3. **There are enough points.** The coefficient ring has $N = D + 1$ points $u_0, \ldots, u_{N-1}$ whose pairwise differences are units. Over a field $F$ this means $N$ distinct elements, so $F$ must have at least $D + 1$ elements.
4. **The detour is cheaper.** Evaluation, $N$ problems over $R$, and interpolation together cost less than the direct method. This holds when the problem over $R$ is much cheaper than the same problem over $R[x]$, as for determinants and gcds, or when the points are chosen so that evaluation and interpolation are fast, as for multiplication at roots of unity.

## The template

```pseudo id=template
EVAL-INTERP(f_1, ..., f_k, Φ, D)
E1  N ← D + 1                                  ▷ D bounds the degree of the result
E2  choose points u_0, ..., u_{N−1} with all u_i − u_j units
E3  for i ← 0 to N − 1 do
E4      v[j] ← f_j(u_i) for j ← 1 to k         ▷ evaluate
E5      y[i] ← Φ(v[1], ..., v[k])              ▷ solve the problem over R
E6  return INTERPOLATE((u_0, y[0]), ..., (u_{N−1}, y[N−1]))
```

**Why it is correct.** Let $h = \Phi(f_1, \ldots, f_k)$. Since evaluation at $u_i$ is a ring homomorphism, $h(u_i) = \Phi(f_1(u_i), \ldots, f_k(u_i)) = y_i$. The polynomial $h$ has degree at most $D < N$, and by the [factor theorem](/factor-theorem/) it is the only polynomial of degree less than $N$ with these $N$ values. So the interpolant of line E6 is $h$.

**Cost.** Let $E(N)$ be the cost of evaluating one input at $N$ points, $C$ the cost of one problem over $R$, and $I(N)$ the cost of interpolation from $N$ points, all in ring operations of $R$ in the algebraic complexity model. The template costs

$$k\, E(N) + N\, C + I(N).$$

With [Horner's rule](/horner-rule/) and Newton interpolation, $E(N)$ and $I(N)$ are $O(N^2)$. With [fast multipoint evaluation](/fast-multipoint-evaluation/) and [fast interpolation](/fast-interpolation/) they are $O(M(N) \log N)$, where $M(N)$ is the cost of multiplying two polynomials of degree less than $N$. At the $N$-th roots of unity they are $O(N \log N)$ by the [FFT](/fast-fourier-transform/). These bounds are proved; which method is fastest for a given $N$ is observed in practice and depends on the ring and the machine.

**Choices to make.** The degree bound $D$; the points, which decide the cost of evaluation and interpolation; and how to solve the pointwise problem.

## Classic examples

**Multiplication by the FFT.** For $h = fg$ with $\deg f, \deg g < n$, take $D = 2n - 2$, round $N$ up to a power of two, and take the $N$-th roots of unity as points. Evaluation and interpolation are the FFT and its inverse, and the pointwise step is $N$ multiplications. The cost is $O(n \log n)$. See [FFT polynomial multiplication](/fft-polynomial-multiplication/).

**Karatsuba multiplication.** For $f = f_0 + f_1 x$ and $g = g_0 + g_1 x$, the product has degree 2, so 3 points are needed. Take $0$, $1$ and the point at infinity, where the "value" is the leading coefficient. The values of the product are $v_0 = f_0 g_0$, $v_1 = (f_0 + f_1)(g_0 + g_1)$ and $v_\infty = f_1 g_1$, and interpolation gives $fg = v_0 + (v_1 - v_0 - v_\infty) x + v_\infty x^2$. For $(3 + 5x)(2 + 7x)$: $v_0 = 6$, $v_1 = 8 \cdot 9 = 72$, $v_\infty = 35$, and the middle coefficient is $72 - 6 - 35 = 31$. So the product is $6 + 31x + 35x^2$, with 3 multiplications instead of 4. Applied recursively to the halves of polynomials or of integers, this gives $O(n^{\log_2 3})$. See [Karatsuba multiplication](/karatsuba-multiplication/).

**Toom-Cook multiplication.** Split each operand into $k$ parts, and evaluate at $2k - 1$ points, such as $0, 1, -1, 2, \infty$ for $k = 3$. The $2k - 1$ products of size $n/k$ give $O(n^{\log_k (2k-1)})$, which is $O(n^{\log_3 5})$ for Toom-3. Interpolation needs divisions by small integers, such as 2 and 3, so Toom-3 does not work directly over $\mathbb{F}_2$ or $\mathbb{F}_3$. See [Toom-Cook multiplication](/toom-cook-multiplication/).

**Determinant of a polynomial matrix.** Let $A(x)$ be an $n \times n$ matrix over $F[x]$ with entries of degree at most $d$. Then $\deg \det A \le nd$. Evaluate $A$ at $nd + 1$ points, compute each scalar determinant by [Gaussian elimination](/gaussian-elimination/) in $O(n^3)$ field operations, and interpolate. The total is $O(n^4 d + n^3 d^2)$ field operations with Horner evaluation, and it never forms a fraction of polynomials. Example: for $A = \begin{pmatrix} x + 1 & 2 \\ x & x - 1 \end{pmatrix}$, $D = 2$, and the determinants at $0, 1, 2$ are $-1, -2, -1$. Interpolation gives $-1 - x + x(x - 1) = x^2 - 2x - 1$, which is $(x + 1)(x - 1) - 2x$. The [characteristic polynomial](/characteristic-polynomial/) $\det(xI - B)$ of a scalar matrix $B$ is the special case $d = 1$: for $B = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$, the values at $0, 1, 2$ are $5, 1, -1$, and they interpolate to $x^2 - 5x + 5$.

**Resultants and bivariate problems.** The [resultant](/resultant/) $\operatorname{res}_y(f, g) \in F[x]$ of two polynomials in $F[x, y]$ is a determinant of the [Sylvester matrix](/sylvester-matrix/), so it can be computed by evaluating $x$ at enough points, computing univariate resultants over $F$, and interpolating. Von zur Gathen and Gerhard use this in Section 6.8 to intersect plane curves.

**Gcd of bivariate polynomials.** Brown's algorithm computes $\gcd(f, g)$ in $F[x, y]$ by evaluating $y$ at points, computing univariate gcds in $F[x]$, and interpolating. The gcd does not commute with evaluation at every point, so the algorithm must detect and skip unlucky points, where the degree of the image gcd is too large. See [Brown's modular gcd](/brown-modular-gcd/).

**The integer analogue.** For a problem with an integer result, reduce modulo primes $p_1, \ldots, p_N$ instead of evaluating at points, solve modulo each prime, and rebuild the result by the [Chinese remainder theorem](/chinese-remainder-theorem/). The degree bound becomes a bound on the absolute value, such as the [Hadamard bound](/hadamard-bound/) for a determinant. These are the [modular methods](/modular-methods/), and von zur Gathen and Gerhard treat both forms together in Chapter 5, as Chinese remaindering in a Euclidean domain.

## Variations

- **Points at infinity.** The value at infinity is the leading coefficient. It costs no evaluation and makes interpolation simpler, which is why Karatsuba and Toom-Cook use it.
- **Roots of unity.** They make evaluation and interpolation one transform each, of cost $O(N \log N)$. Over finite fields $\mathbb{F}_p$ with $p - 1$ divisible by a large power of two, the [number-theoretic transform](/number-theoretic-transform/) gives exact arithmetic.
- **Chinese remaindering with general moduli.** Replace $x - u_i$ by coprime polynomials $m_i$ of higher degree; the "value" is $h \bmod m_i$. This handles fields with too few elements: over $\mathbb{F}_2$, work modulo distinct irreducible polynomials.
- **Hermite interpolation.** Use the value and some derivatives at each point, that is $h \bmod (x - u_i)^{e_i}$ (von zur Gathen and Gerhard, Section 5.6).
- **Rational results.** When the result is a rational function, interpolate to a polynomial of high enough degree and then recover the fraction by rational function reconstruction (Section 5.7) or Pade approximation.
- **Early termination.** When no good degree bound is known, add points one at a time and stop when the interpolant does not change for one or a few more points. This is a heuristic unless the points are random, in which case the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) bounds the error probability.
- **Sparse interpolation.** If the result has few terms but high degree, as for many multivariate results, algorithms of Zippel and of Ben-Or and Tiwari use far fewer points than the degree bound requires.
- **Lucky points.** For operations that are not ring homomorphisms, such as the gcd, the result commutes with evaluation only for most points. The algorithm must recognize the bad points, usually from the degree of the image.

## Pitfalls

- **A degree bound that is too small.** With $N \le \deg h$ points, the template returns $h \bmod \prod (x - u_i)$, with no error. For the matrix example above, two points would give a polynomial of degree 1. Derive $D$ from a proof, not from a guess.
- **Too few elements in the field.** $\mathbb{F}_p$ has only $p$ points. To compute a product of degree 10 over $\mathbb{F}_7$, use points in an extension field such as $\mathbb{F}_{49}$, or general moduli instead of points.
- **Small divisors in interpolation.** Interpolation divides by $u_i - u_j$. Over $\mathbb{Z}/m\mathbb{Z}$ the differences must be units, and over $\mathbb{Z}$ the intermediate values are fractions even when the result has integer coefficients.
- **Division in the pointwise step.** If $\Phi$ contains a division, a point where the divisor vanishes gives no value. Gaussian elimination over $F$ at a point is fine, but a formula that divides by a polynomial must avoid its roots.
- **Unlucky points for nonhomomorphic operations.** At $y = 0$, $\gcd(x + y, x)$ has the image $\gcd(x, x) = x$, but the true gcd is $1$. Without a check of the degrees, interpolation of such images gives a wrong result.
- **Floating point.** Over $\mathbb{R}$ with equally spaced points, interpolation is badly conditioned. Use roots of unity or Chebyshev points.
- **Overhead for small sizes.** For small degrees the conversion costs more than the direct method. Implementations switch to the direct method below a crossover point that is found by measurement.

## Exercises

1. How many points are needed to compute $f g h$ by evaluation and interpolation, if $\deg f = a$, $\deg g = b$ and $\deg h = c$? *Answer:* $a + b + c + 1$.
2. Show that the Karatsuba formula is the template with the points $0$, $1$ and $\infty$, and that the points $0$, $-1$ and $\infty$ give the variant with $v_{-1} = (f_0 - f_1)(g_0 - g_1)$ and middle coefficient $v_0 + v_\infty - v_{-1}$.
3. Over $\mathbb{F}_2$, two polynomials of degree 3 have a product of degree 6. Which is the smallest field $\mathbb{F}_{2^k}$ that has enough points? *Answer:* $\mathbb{F}_8$, with 8 elements, since 7 points are needed.
4. Compute the characteristic polynomial of an $n \times n$ matrix over $F$ by the template with $n + 1$ points. What does it cost in field operations, and how does this compare with the $O(n^3)$ of reduction to Hessenberg form? *Answer:* $O(n^4)$ for the $n + 1$ determinants, plus $O(n^2)$ for interpolation, so it is slower by a factor of $n$.
5. Let $A(x)$ be an $n \times n$ matrix with entries in $F[x]$ of degree at most $d$, and let $B(x)$ be another. How many points does the template need to compute the product matrix $A(x)B(x)$, and how many scalar matrix products? *Answer:* $2d + 1$ points and $2d + 1$ products of $n \times n$ matrices.

## References
