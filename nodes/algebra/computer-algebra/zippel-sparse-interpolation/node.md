---
tag: GB4A8V
kind: algorithm
slug: zippel-sparse-interpolation
name: Zippel's sparse interpolation
aliases: [Zippel algorithm, Zippel's probabilistic interpolation, variable-by-variable sparse interpolation, Zippel's sparse interpolation algorithm]
area: algebra/computer-algebra
level: research
summary: Recovers a multivariate polynomial variable by variable from evaluations.
solves: [sparse-polynomial-interpolation]
model: blum-shub-smale-machine
complexity:
  vars: {n: "the number of variables", d: "the degree bound in each variable", t: "the number of terms of f"}
  time: {worst: O(n d t (t + d))}
  space: {extra: O(t (n + d))}
properties: {deterministic: false, recursive: false, in_place: false}
prereqs: [sparse-polynomial-interpolation, schwartz-zippel-lemma, newton-interpolation, vandermonde-matrix]
see_also: [ben-or-tiwari-algorithm, sparse-polynomial, brown-modular-gcd, polynomial-gcd, polynomial-identity-testing, evaluation-interpolation-paradigm, kronecker-substitution, straight-line-program]
sources:
  - paper: doi:10.1007/3-540-09519-5_73
    title: Richard Zippel, Probabilistic algorithms for sparse polynomials, EUROSAM 1979, Lecture Notes in Computer Science 72
    locator: pp. 216 to 226 (the variable by variable interpolation, the probabilistic assumption and the sparse modular GCD)
  - paper: doi:10.1016/S0747-7171(08)80018-1
    title: Richard Zippel, Interpolating polynomials from their values, Journal of Symbolic Computation 9(3), 1990
    locator: pp. 375 to 403 (nodes chosen as powers, and the transposed Vandermonde solve in quadratic time and linear space)
  - book: isbn:9780792393757
    title: Richard Zippel, Effective Polynomial Computation, Kluwer, 1993
    locator: Chapter 14, Multivariate Interpolation, pp. 231 to 246, and Chapter 15 for GCDs by interpolation
  - paper: doi:10.1145/62212.62241
    title: Michael Ben-Or and Prasoon Tiwari, A deterministic algorithm for sparse multivariate polynomial interpolation, STOC 1988
    locator: pp. 301 to 309
  - paper: doi:10.1007/3-540-51084-2_44
    title: Erich Kaltofen and Lakshman Yagati, Improved sparse multivariate polynomial interpolation algorithms, ISSAC 1988, Lecture Notes in Computer Science 358
    locator: pp. 467 to 474 (transposed Vandermonde systems in O(M(t) log t) operations)
  - paper: doi:10.1145/345542.345629
    title: Erich Kaltofen, Wen-shin Lee and Austin A. Lobo, Early termination in Ben-Or/Tiwari sparse interpolation and a hybrid of Zippel's algorithm, ISSAC 2000
    locator: pp. 192 to 201
  - paper: doi:10.1016/S0747-7171(03)00088-9
    title: Erich Kaltofen and Wen-shin Lee, Early termination in sparse interpolation algorithms, Journal of Symbolic Computation 36(3-4), 2003
    locator: pp. 365 to 400 (early termination of the univariate stages of Zippel's method)
  - paper: doi:10.1145/1073884.1073903
    title: Jennifer de Kleine, Michael Monagan and Allan Wittkopf, Algorithms for the non-monic case of the sparse modular GCD algorithm, ISSAC 2005
    locator: pp. 124 to 131
  - paper: doi:10.1145/1837210.1837233
    title: Seyed Mohammad Mahdi Javadi and Michael Monagan, Parallel sparse polynomial interpolation over finite fields, PASCO 2010
    locator: pp. 160 to 168
  - paper: doi:10.1016/j.jsc.2020.06.001
    title: Jiaxiong Hu and Michael Monagan, A fast parallel sparse polynomial GCD algorithm, Journal of Symbolic Computation 105, 2021
    locator: pp. 28 to 63
---

Zippel's sparse interpolation finds the terms of a multivariate polynomial that is given only as a black box for its values. It adds one variable at a time and assumes that the terms found so far keep their shape when the next variable is added. With $t$ terms, $n$ variables and degree at most $d$ in each variable, it makes at most $(d + 1)(1 + (n - 1) t)$ evaluations. A dense method needs $(d + 1)^n$. The assumption fails only with small probability over a random choice of point. Richard Zippel introduced the method in 1979 for sparse polynomial GCDs, and it is still the base of the sparse modular GCD algorithms in computer algebra systems.

## In plain words

Suppose a procedure can compute the value of a hidden polynomial at any point, and the polynomial has many variables but few terms. First fix every variable except the first one to random values, and find the hidden polynomial in the first variable alone, as in school interpolation. This gives a list of terms. Then let the second variable vary too. The method guesses that every term found so far still appears, now with coefficients that depend on the second variable. This guess turns each step into a small system of equations with one unknown per term. Solve such systems at a few values of the second variable, and then interpolate each coefficient. Repeat for the third variable, and so on. The work grows with the number of terms, not with the number of all possible terms. A rare unlucky random choice can make the method miss a term.

## The problem

Notation follows the rest of this sub-area. $K$ is a field, here $K = \mathbb{Z}/p\mathbb{Z}$ with $p$ prime. The polynomial $f \in K[x_1, \ldots, x_n]$ has degree at most $d$ in each variable and $t$ terms. The monomial order plays no role here. $M(d)$ is the cost of multiplying two polynomials of degree $d$ in one variable.

**Input.** A black box that returns $f(\xi)$ for any $\xi \in K^n$, the number $n$, the degree bound $d$ with $d + 1 < p$, and a source of random elements of $K$. The number $t$ is not needed.

**Output.** The terms of $f$, as a map from exponent vectors to nonzero coefficients.

**Cost model.** Operations in $K$, and calls of the black box (probes), counted apart. Over $\mathbb{Z}$ or $\mathbb{Q}$ one runs the method modulo one or more primes and lifts by the [Chinese remainder theorem](/chinese-remainder-theorem/) or by rational reconstruction. The skeleton found modulo the first prime can then be reused for the other primes.

## The algorithm

For $1 \le i \le n$, write $f = \sum_m c_{i,m}(x_{i+1}, \ldots, x_n)\, m$, where $m$ runs over the set $M_i$ of monomials in $x_1, \ldots, x_i$ with $c_{i,m} \ne 0$. The algorithm fixes a random anchor $(a_2, \ldots, a_n)$ and, after stage $i$, holds the *skeleton*: the monomials $m$ of $f(x_1, \ldots, x_i, a_{i+1}, \ldots, a_n)$ with their coefficients. The *Zippel assumption* is that no $c_{i,m}$ vanishes at the anchor. Then the skeleton after stage $i$ is exactly $M_i$.

To add $x_{i+1}$, fix $x_{i+1} = b$. The polynomial $f(x_1, \ldots, x_i, b, a_{i+2}, \ldots)$ has support inside $M_i$, so only its $T = |M_i|$ coefficients are unknown. Evaluate it at the powers $(r_1^k, \ldots, r_i^k)$ for $k = 0, \ldots, T - 1$ of a random point $r$. A term $c\, m$ then contributes $c\, v_m^k$ with $v_m = m(r_1, \ldots, r_i)$, so the $T$ probes form a transposed Vandermonde system in the unknown coefficients with nodes $v_m$.

```pseudo id=main
ZIPPEL(f, n, d, p)                                  ▷ f a black box over Z/pZ
L1  choose a random anchor a_2, ..., a_n in (Z/pZ)^*
L2  interpolate f(x_1, a_2, ..., a_n) from d + 1 probes; skeleton S ← its terms
L3  for i ← 1 to n − 1: if S is empty: return 0
L4    choose random r_1, ..., r_i until the nodes v_m = m(r) for m in S are distinct
L5    for each of d + 1 distinct values b: probe w_k ← f(r_1^k, ..., r_i^k, b, a_(i+2), ..., a_n) for k = 0..|S| − 1
L6      solve Σ_m c_m v_m^k = w_k for k < |S| (transposed Vandermonde); store c_m(b)
L7    for each m in S: interpolate c_m(x_(i+1)) from its d + 1 values; S ← the terms m · x_(i+1)^e with nonzero coefficient
L8  return S
```

Line L2 uses [Newton interpolation](/newton-interpolation/) in one variable. Line L6 solves the system in $O(T^2)$ operations: with $\Lambda(z) = \prod_m (z - v_m)$ and $\Lambda_m = \Lambda / (z - v_m)$, the coefficient is $c_m = \sum_k \lambda_{m,k} w_k / \Lambda_m(v_m)$, where $\lambda_{m,k}$ are the coefficients of $\Lambda_m$ (Zippel 1990). Line L7 is again dense interpolation in one variable, now applied to each of the $|S|$ coefficients. The new skeleton has at most $t$ terms, because every term of it is a term of $f(x_1, \ldots, x_{i+1}, a_{i+2}, \ldots)$, whose monomials lie in $M_{i+1}$.

## Example

Take $p = 101$, $n = 2$, $d = 3$ and $f = 3x^2 y + 5 x y^3 - 2$. The anchor is $y = 5$.

Stage 1 (L2). The probes $f(x, 5)$ at $x = 1, 2, 3, 4$ give $32, 96, 89, 11$. Interpolation gives $15 x^2 + 19 x + 99$, that is, $15x^2 + 19x - 2$ modulo $101$. The skeleton is $\{x^2, x, 1\}$, so $T = 3$.

Stage 2 (L4 to L7). Take $r = 2$. The nodes are $v_{x^2} = 4$, $v_x = 2$ and $v_1 = 1$, which are distinct. For each $b = 1, 2, 3, 4$, probe $f(2^k, b)$ for $k = 0, 1, 2$ and solve the $3 \times 3$ system:

| $y = b$ | probes $f(1, b), f(2, b), f(4, b)$ | coefficients of $x^2, x, 1$ |
|---|---|---|
| 1 | 6, 20, 66 | 3, 5, 99 |
| 2 | 44, 1, 52 | 6, 40, 99 |
| 3 | 41, 1, 76 | 9, 34, 99 |
| 4 | 27, 80, 56 | 12, 17, 99 |

Interpolating each column in $y$ gives $3y$ for $x^2$, $5y^3$ for $x$ (since $5 \cdot 27 = 135 \equiv 34$ and $5 \cdot 64 = 320 \equiv 17$), and $99 = -2$ for $1$. The output is $3 x^2 y + 5 x y^3 - 2$. The method used $4 + 12 = 16$ probes, which equals the bound $(d + 1)(1 + (n - 1) t) = 4 \cdot 4$. Dense interpolation would also use $16$ here, but for $n = 10$, $d = 10$ and $t = 20$ the counts are about $2 \cdot 10^3$ and $2.6 \cdot 10^{10}$.

## Correctness

The full proof is in the proof file. Fix one stage and one value $b$. Whatever the random choices, the support of $f(x_1, \ldots, x_i, b, a_{i+2}, \ldots)$ lies in $M_i$. If the skeleton is $M_i$ and the nodes are distinct, the Vandermonde matrix is invertible, so L6 returns the exact coefficients $c_{i,m}(b, a_{i+2}, \ldots)$. Each of these is a polynomial of degree at most $d$ in $b$, so L7 recovers it from $d + 1$ values. By induction, under the Zippel assumption the skeleton after the last stage is the support of $f$ with the right coefficients.

The assumption can fail. Each $c_{i,m}$ is a nonzero polynomial of total degree at most $(n - i) d$, so by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) it vanishes at a uniform anchor in $(K^*)^{n-i}$ with probability at most $(n - i) d / (p - 1)$. A union bound over at most $t$ monomials in each stage gives a failure probability of at most $n (n - 1) d t / (2 (p - 1))$. Colliding nodes in L4 are seen and only cost a new choice of $r$. When the assumption fails, the output misses terms and nothing signals it. One extra probe at a random point detects a wrong answer with probability at least $1 - n d / (p - 1)$.

## Complexity

All bounds are in operations in $K = \mathbb{Z}/p\mathbb{Z}$ and are proved. Observed costs follow them closely, since the method does the same work for every input of the given shape.

- **Probes.** $d + 1$ in stage 1 and $(d + 1) |S| \le (d + 1) t$ in each later stage, so at most $(d + 1)(1 + (n - 1) t) = O(n d t)$.
- **Vandermonde solves.** $d + 1$ solves of size at most $t$ in each stage, $O(t^2)$ each, so $O(n d t^2)$ in total. With fast methods (Kaltofen and Lakshman 1988) one solve costs $O(M(t) \log t)$.
- **Univariate interpolation.** At most $t$ dense interpolations of degree $d$ in each stage, $O(d^2)$ each, so $O(n t d^2)$. Fast interpolation lowers this to $O(n t M(d) \log d)$.
- **Nodes.** Computing the $v_m$ and the probe points costs $O(n t \log d)$ in each stage, which is dominated.

The total is $O(n d t (t + d))$ operations plus the cost of the probes. The extra space is $O(t (n + d))$: the skeleton, the nodes and a $(d + 1) \times t$ table of coefficient values. Ben-Or and Tiwari use only $O(t)$ probes, but need a bound on $t$, a field with large multiplicative order and discrete logarithms or a large characteristic. Zippel's method needs only a degree bound. Over $\mathbb{Z}$ with coefficients of $h$ binary digits, the cost is multiplied by the number of primes, about $h / \log_2 p$, plus the cost of Chinese remaindering.

## Properties

- **Randomized, of Monte Carlo type.** The answer can be wrong with probability at most $n (n - 1) d t / (2 (p - 1))$. It is never reported as failed. One checking probe makes a wrong answer very unlikely to go unnoticed.
- **Needs only a degree bound.** The number of terms $t$ is found by the method. A larger bound $d$ is allowed and only costs more probes.
- **Order of variables.** The bound is the same for every order, but the size of the intermediate skeletons depends on it.
- **Parallel.** The $d + 1$ values $b$ in a stage, and the probes for one $b$, are independent of each other.
- **Not recursive.** The stages are a loop. The Python code uses no recursion.

## Variants and improvements

- **Zippel 1990.** Choosing the probe points as powers of one point makes every system a transposed Vandermonde system, solvable in $O(T^2)$ time and $O(T)$ space. The 1979 version solved general linear systems.
- **Fast Vandermonde solving.** Kaltofen and Lakshman (1988) solve transposed Vandermonde systems in $O(M(t) \log t)$ operations.
- **Early termination.** Kaltofen and Lee (2003) stop each univariate interpolation once the values agree with the current interpolant at a few more random points, so a good $d$ need not be known. Kaltofen, Lee and Lobo (2000) combine this with the [Ben-Or and Tiwari algorithm](/ben-or-tiwari-algorithm/) in a hybrid.
- **Sparse GCDs.** Zippel's main application is the sparse modular GCD: the skeleton of a GCD computed at one point is reused at other points, and the dense recursion of the [modular GCD of Brown](/brown-modular-gcd/) is avoided. de Kleine, Monagan and Wittkopf (2005) handle the case where the leading coefficient of the GCD is not known. Hu and Monagan (2021) give a fast parallel version.
- **Parallel interpolation.** Javadi and Monagan (2010) combine the skeleton idea with Ben-Or and Tiwari for parallel interpolation over finite fields.
- **Kronecker substitution.** An alternative maps the $n$ variables to one with [Kronecker substitution](/kronecker-substitution/) and runs a univariate sparse method. The degree then becomes about $(d + 1)^n$, which needs a large field.

## When to use it

Use it when $f$ is given by an evaluation procedure, for example a determinant with polynomial entries, a resultant, or a GCD computed at points, and $f$ is expected to be sparse. It is the standard choice inside sparse GCD and factorization codes because it needs only a degree bound and a modest prime. When $t$ is known and the field allows discrete logarithms, the Ben-Or and Tiwari method uses fewer probes. When $f$ is dense, plain dense interpolation on a grid costs about the same and has no failure probability.

## Pitfalls

- **Small primes.** The failure bound $n (n - 1) d t / (2 (p - 1))$ must be small. For $p$ near $10^4$ and large $n d t$ it is not. Use a word-size prime of about $2^{31}$ or more, or repeat with fresh random choices.
- **Zero anchors.** An anchor coordinate equal to $0$ kills every coefficient that contains that variable. Choose anchors in $K^*$.
- **Node collisions.** If $r_l$ has small multiplicative order, distinct monomials can give the same node. The code checks distinctness before it probes and draws again.
- **Silent errors.** A missing term is not detected by the method. Check the result at one or two random points.
- **Degree bound.** The bound must hold in each variable, and $p$ must exceed $d + 1$ so that $d + 1$ distinct values exist.
- **Large skeletons.** An intermediate skeleton can be larger than you expect if the variable order is bad, though never larger than $t$.

## Implementations

## History

Richard Zippel introduced the method in his 1979 MIT thesis and in the EUROSAM 1979 paper "Probabilistic algorithms for sparse polynomials". The same paper gave the probabilistic zero test now called the Schwartz-Zippel lemma, and used interpolation for sparse polynomial GCDs. Zippel (1990) changed the probe points to powers of one point, which reduced each linear system to a transposed Vandermonde system. Ben-Or and Tiwari (1988) gave a deterministic method with fewer probes but a stronger assumption on the field. Kaltofen and Lee (2003) added early termination. Monagan and his students later extended the sparse GCD to the non-monic case and to parallel machines. Zippel's book Effective Polynomial Computation (1993) gives a textbook account in Chapter 14.

## References
