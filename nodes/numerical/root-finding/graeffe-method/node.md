---
tag: 4YAGDA
kind: algorithm
slug: graeffe-method
name: Graeffe's method
aliases:
- root squaring
- Dandelin-Lobachevsky-Graeffe method
- Dandelin-Graeffe method
- Graeffe root squaring
area: numerical/root-finding
level: advanced
summary: Repeatedly squares the roots so that they separate in magnitude and can be read off the coefficients. The moduli converge quadratically once the squared roots separate.
solves: [polynomial-root-finding]
model: real-ram
complexity:
  vars: {n: "the degree", K: "the cap on the squaring steps", λ: "the largest ratio |r_(j+1)|/|r_j| of consecutive distinct root moduli", δ: "the tolerance"}
  time: {worst: "O(n^2 K)", average: "O(n^2 log(log(1/δ) / log(1/λ)))"}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true, simultaneous: true, global: true}
prereqs: [polynomial-root-finding, order-of-convergence]
see_also: [bernoulli-method, companion-matrix-method, cauchy-root-bound, multiplicity-of-roots, wilkinson-polynomial, durand-kerner-method, newton-raphson-method, quadratic-convergence]
sources:
  - book: "Alston S. Householder, The Numerical Treatment of a Single Nonlinear Equation, McGraw-Hill, 1970"
    locator: the chapter on methods of Graeffe type (the squaring step, regular and irregular coefficients, and the moduli of the roots)
  - paper: "Alston S. Householder, Dandelin, Lobacevskii, or Graeffe?, American Mathematical Monthly 66, 464-466, 1959"
    locator: the history of the method and its three independent discoverers
  - paper: "Alexander Ostrowski, Recherches sur la méthode de Graeffe et les zéros des polynomes et des séries de Laurent, Acta Mathematica 72, 99-257, 1940"
    locator: the convergence analysis of root squaring and the estimation of root moduli
  - paper: "Victor Y. Pan, Solving a polynomial equation: some history and recent progress, SIAM Review 39(2), 187-220, 1997"
    locator: the role of Graeffe steps in root radii computation and in fast polynomial root finders
  - paper: "Gregorio Malajovich and Jorge P. Zubelli, Tangent Graeffe iteration, Numerische Mathematik 89, 749-782, 2001"
    locator: the recovery of the roots themselves, not only their moduli, from a perturbed Graeffe sequence
---

Graeffe's method, or root squaring, finds the moduli of all the roots of a polynomial at once. One step replaces $p$ by the polynomial $q$ of the same degree with $q(x^2) = (-1)^n p(x) p(-x)$, whose roots are the squares of the roots of $p$. After $k$ steps the roots are raised to the power $N = 2^k$, roots of different moduli become wildly different in size, and by Vieta's formulas each modulus can be read off from the ratio of two consecutive coefficients. Once the squared roots separate, the error in the moduli squares at every step, so the method converges quadratically in the number of steps, with $O(n^2)$ work for each step. The method was found independently by Dandelin (1826), Lobachevsky (1834) and Graeffe (1837). It was the main way to solve polynomial equations by hand until the 1950s, and Graeffe steps are still used today to estimate root radii.

## In plain words

If one root is ten times larger than another, then after squaring the roots ten times it is $10^{1024}$ times larger. A polynomial whose roots differ that much in size is easy to read. Its coefficients are, up to sign, $r_1^N$, $r_1^Nr_2^N$, $r_1^Nr_2^Nr_3^N$ and so on, because every other term in the elementary symmetric functions is negligible. Dividing consecutive coefficients and taking the $N$-th root gives back $|r_1|, |r_2|, \dots$. The price is that the coefficients become astronomically large, so they must be stored with an unbounded exponent.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = p(x) = a_0x^n + \cdots + a_n$ with real coefficients, $a_0 \ne 0$, and roots $r_1, \dots, r_n$ ordered so that $|r_1| \ge \cdots \ge |r_n|$. The output is the list of distinct moduli with the number of roots of each, and, for a modulus carried by a single root, that real root with its sign. The method does not evaluate $p$ while it iterates, so the cost is counted in squaring steps of $O(n^2)$ arithmetic operations each. The stopping rule uses the deviation $d_j = |(-1)^j c_j/b_j^2 - 1|$ of each new coefficient $c_j$ from the square of the old one $b_j$: stop when every $d_j \le$ tol, or after $K$ steps.

## The algorithm

```pseudo id=main
GRAEFFE(a, tol, K):
L1   strip leading zero coefficients;  strip trailing zero coefficients and record a root 0 for each
L2   b <- a, stored with an unbounded exponent;  k <- 0
L3   while k < K:
L4       c_j <- (-1)^j (b_j^2 + 2 sum_(i>=1) (-1)^i b_(j-i) b_(j+i))   for j = 0..n
L5       k <- k + 1
L6       d_j <- |(-1)^j c_j / b_j^2 - 1|   (infinite when b_j or c_j is 0)
L7       b <- c
L8       if max_j d_j <= tol then status <- "separated";  break
L9   R <- {j : d_j <= tol} together with 0 and n
L10  for consecutive i < l in R:  l - i roots of modulus |b_l / b_i|^(1/(2^k (l - i)))
L11  for each modulus rho carried by one root:  the root is +rho or -rho, whichever gives the smaller |p|
L12  return the moduli with their counts, the real roots and the status
```

Line L4 is the squaring step. Its formula is the coefficient of $y^{n-j}$ in $(-1)^n p(x)p(-x)$ with $y = x^2$: the products $a_{j-i}a_{j+i}$ come in pairs, and the alternating signs come from $p(-x)$. Lines L6 and L8 implement the stopping rule. A coefficient index $j$ is regular when the step squares it, up to the sign $(-1)^j$. That happens exactly when $|r_j| > |r_{j+1}|$, so that one product of $j$ roots dominates all the others. Lines L9 and L10 handle the irregular indices: between two regular indices $i < l$ lie $l - i$ roots of one common modulus, such as a complex conjugate pair, a pair $\pm r$ or a multiple root, and only their common modulus is returned. Line L11 uses the fact that a modulus carried by a single root of a real polynomial must belong to a real root.

## Example

For $p(x) = x^3 - 6x^2 + 11x - 6 = (x - 1)(x - 2)(x - 3)$, the first step gives $c_1 = -(36 - 22) = -14$, $c_2 = 121 - 72 = 49$ and $c_3 = -36$. The result is $y^3 - 14y^2 + 49y - 36$, whose roots are $1, 4, 9$. The next steps give

| $k$ | coefficients $b_0, b_1, b_2, b_3$ | $\lvert b_1/b_0\rvert^{1/N}$ | $\lvert b_2/b_1\rvert^{1/N}$ | $\lvert b_3/b_2\rvert^{1/N}$ |
|---|---|---|---|---|
| 1 | $1, -14, 49, -36$ | 3.742 | 1.871 | 0.857 |
| 2 | $1, -98, 1393, -1296$ | 3.146 | 1.942 | 0.982 |
| 3 | $1, -6818, 1686433, -1679616$ | 3.014 | 1.991 | 0.9995 |

The deviation $d_2$ goes $0.008, 3.1 \times 10^{-5}, 4.7 \times 10^{-10}$ over steps 4 to 6, roughly squaring and halving each time. The run stops after 8 steps with the moduli $3, 2, 1$ correct to rounding. The signs, all positive, come from comparing $|p(\pm\rho)|$. For $x^4 + 3x^2 + 6x + 10$, whose roots are $-1 \pm i$ and $1 \pm 2i$, the indices 1 and 3 never become regular. The run ends at the cap and reports two moduli, $\sqrt5$ and $\sqrt2$, each carried by 2 roots, correct to 16 digits.

## Correctness

After $k$ steps the coefficients satisfy $b_j/b_0 = (-1)^j e_j(r_1^N, \dots, r_n^N)$ with $N = 2^k$, where $e_j$ is the $j$-th elementary symmetric function. If $|r_j| > |r_{j+1}|$, the product $r_1^N \cdots r_j^N$ dominates $e_j$, with a relative remainder of at most $\binom{n}{j}\lambda_j^N$ where $\lambda_j = |r_{j+1}/r_j|$. So between consecutive regular indices the formula of L10 converges to the common modulus of the roots there, with a relative error of order $\lambda^N/N$. The deviation $d_j$ tends to 0 at the same rate exactly at the regular indices. At an index inside a group of equal moduli the deviation does not tend to 0; for a complex pair it stays at least $1/2$. The loop ends after at most $K$ steps. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs about $n^2/2$ multiplications. Once the moduli separate, the relative error of a modulus behaves like $\lambda^N/N$. So reaching the tolerance $\delta$ takes about $\log_2(\ln(1/\delta)/\ln(1/\lambda))$ steps: the number of steps grows only like the logarithm of the logarithm of the accuracy, and like $\log_2$ of $1/(1 - \lambda)$ as the moduli get closer. On the test problems: 8 steps for $(x-1)(x-2)(x-3)$, 13 steps for roots $1$ and $1.01$, and 11 steps for the [Wilkinson polynomial](/wilkinson-polynomial/) of degree 20, whose two largest moduli differ by 5%. Over 500 random polynomials of degree 1 to 10, with real roots whose moduli differ by at least 5%, the average was 8.5 steps. With equal moduli, the method runs to the cap $K$. The coefficients need $O(N\log\max|r_j|)$ bits of exponent but only a fixed number of digits of mantissa, which the reference code keeps at 40.

## Properties

- Global: no starting point. It finds all the moduli at once, for any real polynomial.
- The deviations $d_j$ converge quadratically, $d_{k+1} \approx d_k^2/(2c)$, where $c$ is the number of products of $j$ roots that tie for second place in $e_j$. The moduli inherit an error of order $d_k/2^k$. This is an asymptotic statement, proved in the correctness page.
- Multiple roots and equal moduli do not slow the convergence of the other moduli. They show up as irregular indices and are reported as groups.
- Gives moduli, not arguments. A modulus carried by one root gives a real root, but complex pairs and $\pm r$ pairs need extra work.
- The squaring step is insensitive to rounding at regular indices, because the dominant term is a square. With a fixed relative precision for the mantissas, the moduli of the floating point polynomial come out to full accuracy. On the Wilkinson polynomial of degree 20, the computed moduli match the roots of the rounded coefficients to $2 \times 10^{-16}$. Those roots differ from $1, \dots, 20$ by up to $5 \times 10^{-4}$.

## Variants and improvements

- **Root radii.** A few Graeffe steps combined with [Cauchy-type bounds](/cauchy-root-bound/) give every root modulus to within a fixed relative factor. This is a building block of Schönhage's splitting circle method and of fast theoretical root finders (Pan's survey).
- **Arguments of complex roots.** The classical extensions recover the arguments of a complex pair from the sum and product of the roots, or from the Graeffe sequence of a shifted polynomial $p(x + h)$. Tangent Graeffe iteration (Malajovich and Zubelli) runs the iteration on $p(x) + \epsilon p'(x)$ to first order in $\epsilon$ and reads off the roots themselves.
- **Polishing.** The moduli and real roots make good starting points for [Newton's method](/newton-raphson-method/) or for simultaneous methods such as [Durand-Kerner](/durand-kerner-method/).
- **Logarithmic arithmetic.** Hand computers stored the coefficients as logarithms, which is the historical form of the unbounded exponent of L2.

## When to use it

Use it when you need the sizes of all the roots of a real polynomial, or a cheap global picture of where the roots lie before a local method. It is also useful as a robust way to count the roots in annuli. For the roots themselves, with arguments, prefer the [companion matrix method](/companion-matrix-method/) or Aberth's method. Do not run it in plain double precision: the coefficients overflow after about ten steps.

## Pitfalls

- L2: in ordinary floating point the coefficients grow like $|r|^{2^k}$ and overflow within about 10 steps. Use an extended exponent (the reference code uses Decimal with an unbounded exponent range), logarithms, or rescaling of $x$.
- L6: a zero coefficient, such as the middle one of $x^2 - 4$, or one that cancels to zero must count as irregular, not cause a division by zero.
- L8: if two moduli are very close, say with ratio $1 - \epsilon$, they look like one double modulus until $2^k \gg 1/\epsilon$. With a small cap they are reported as one group, and the reported modulus is their geometric mean.
- L11: choosing the sign by $|p(\pm\rho)|$ is reliable for a well conditioned real root. For an ill conditioned one, both values may be rounding noise. In that case a short Newton correction from both signs is safer.
- L10: a group of size 2 may be a complex pair, a pair $\pm r$ or a double real root. The moduli alone cannot tell which.

## Implementations

## History

Germinal Pierre Dandelin described root squaring in 1826, Nikolai Lobachevsky in his Algebra of 1834, and Karl Heinrich Gräffe in a prize essay of 1837. Encke and others extended it to complex roots later in the nineteenth century. Householder's note of 1959 untangled the priority. With logarithm tables, the method was the standard way to solve polynomial equations by hand until the 1950s. Ostrowski's long memoir of 1940 gave it a rigorous convergence theory. Computers favoured methods that work in fixed floating point. But Graeffe steps came back in complexity theory, for root radii in Schönhage's splitting circle method, and in the tangent Graeffe algorithms for polynomials over finite fields.

## References
