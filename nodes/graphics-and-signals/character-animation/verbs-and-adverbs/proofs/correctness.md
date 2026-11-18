---
title: The verb interpolant reproduces its examples, is exact on linear data, and is linear far from the examples
proves: [correctness]
status: full
---

We use the notation of the page.
The arithmetic is exact.
There are $n$ examples with adverb points $p_i \in \mathbb{R}^a$ and value vectors $y_i \in \mathbb{R}^q$, and the $p_i$ are distinct.
$X$ is the $n$ by $(a + 1)$ matrix with rows $(1, p_i^T)$.
The radial function of example $i$ is $R_i(p) = B(2|p - p_i| / \alpha_i)$, where $B$ is the cubic B-spline of the page and $\alpha_i$ is twice the distance from $p_i$ to the nearest other example.
$K$ is the $n$ by $n$ matrix $K_{ri} = R_i(p_r)$.

Two hypotheses are needed, and the code raises an error when either fails:
- (H1) $X^T X$ is nonsingular, that is, the points $p_i$ do not all lie on one hyperplane of $\mathbb{R}^a$ (so $n \ge a + 1$);
- (H2) $K$ is nonsingular.

H2 is not proved for this choice of radial functions.
The $\alpha_i$ differ, so $K$ is not symmetric, and the theory of positive definite radial kernels does not apply.

## The linear part

**Lemma 1.** Lines L1 to L3 give the least squares fit: the coefficient matrix $A = (X^T X)^{-1} X^T Y$ minimizes $\sum_i |y_i - (c_0 + C p_i)|^2$, and the residuals $e_i = y_i - (c_0 + C p_i)$ satisfy $\sum_i e_i = 0$ and $\sum_i p_{il}\, e_i = 0$ for every adverb $l$.

*Proof.*
The objective is a convex quadratic in $A$, and its gradient is $-2 X^T (Y - X A)$.
It is zero exactly at the solution of the normal equations $X^T X A = X^T Y$, which is unique under H1.
The two families of equations in the claim are the rows of $X^T (Y - X A) = 0$: the row of ones and the row of adverb $l$. $\square$

## The radial part

**Lemma 2.** $R_i(p_i) = B(0) = 2/3$, and $R_i(p) = 0$ when $|p - p_i| \ge \alpha_i$.

*Proof.*
$B$ is $2/3 - s^2 + s^3/2$ on $[0, 1)$, $(2 - s)^3/6$ on $[1, 2)$, and 0 for $s \ge 2$, and $2|p - p_i|/\alpha_i \ge 2$ exactly when $|p - p_i| \ge \alpha_i$. $\square$

$B$ is $C^2$: at $s = 1$ both pieces have the value $1/6$, the slope $-1/2$ and the second derivative $1$, and at $s = 2$ the second piece has value, slope and second derivative 0.

**Theorem 1.** Under H1 and H2, the interpolant $y(p) = c_0 + C p + \sum_i w_i R_i(p)$ of line L7 satisfies $y(p_r) = y_r$ for every example $r$.

*Proof.*
Line L6 solves $K W = E$, where row $r$ of $E$ is the residual $e_r$.
So $\sum_i w_i R_i(p_r) = \sum_i K_{ri} w_i = e_r$, and $y(p_r) = c_0 + C p_r + e_r = y_r$. $\blacksquare$

**Theorem 2.** Under H1 and H2, if the examples are linear, $y_i = c_0^* + C^* p_i$, then $W = 0$ and $y(p) = c_0^* + C^* p$ for every $p$.

*Proof.*
The true coefficients give zero residuals, so they minimize the least squares objective, and by uniqueness (H1) the fit returns them.
Then $E = 0$, and $K W = 0$ gives $W = 0$ under H2. $\blacksquare$

**Theorem 3.** If $|p - p_i| \ge \alpha_i$ for every $i$, then $y(p) = c_0 + C p$.

*Proof.*
Lemma 2 makes every radial term zero. $\blacksquare$

So, far from all examples, the interpolant falls back to the least squares hyperplane, and it does not oscillate there.

## What is not proved

The interpolation error at a new adverb point is not bounded on this page.
The test measures it on one smooth synthetic verb: the radial part lowers the mean squared error at 200 random points compared with the linear part alone.
That is a measurement of one case, not a property of the method.
