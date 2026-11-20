---
title: Fixed points of HIO give solutions, and HIO with beta = 1 is Douglas-Rachford
proves: [correctness]
status: full
---

The setting is that of the algorithm. Images have $N$ pixels. $M$ is the set of images whose DFT has magnitude $A$, and $P_M$ is the map of lines L3 to L5: a nearest point of $M$ (Lemma 2 of the error reduction proof, which uses only Parseval's identity and the triangle inequality). $C$ is the object constraint set: zero off the support $S$ and, with nonnegativity, real and nonnegative on $S$. A *solution* is an image in $C \cap M$. The feedback $\beta$ is a fixed number with $\beta > 0$. Arithmetic is exact.

For an image $g$ let $g' = P_M g$ (in the nonnegative case, $g$ is real and $g'$ stands for the real part of $P_M g$, as in the implementation). Let $\gamma(g)$ be the set of pixels $r$ with $r \in S$ and, in the nonnegative case, $g'(r) \ge 0$. The HIO map is

$$H(g)(r) = g'(r) \text{ for } r \in \gamma(g), \qquad H(g)(r) = g(r) - \beta g'(r) \text{ otherwise},$$

as in lines L6 to L8.

There is no theorem that HIO converges, and its error is not monotone. What can be proved is what its fixed points mean, and its link to the Douglas-Rachford method.

**Theorem 1 (solutions are fixed points).** If $f \in C \cap M$, then $H(f) = f$.

*Proof.* $f \in M$, so $P_M f = f$ by Lemma 2 of the error reduction proof (a point of $M$ is its own nearest point: the map of line L4 sends $G_u$ to $A_u G_u / |G_u| = G_u$ when $|G_u| = A_u > 0$, and sends $0$ to $A_u = 0$). So $f' = f$. Off $S$, $f = 0$, so $H(f)(r) = 0 - \beta \cdot 0 = 0 = f(r)$. On $S$ in the nonnegative case, $f'(r) = f(r) \ge 0$, so $r \in \gamma(f)$ and $H(f)(r) = f'(r) = f(r)$. Without nonnegativity every $r \in S$ is in $\gamma(f)$, with the same result. $\square$

**Theorem 2 (fixed points give solutions).** If $H(g) = g$, then $g' = P_M g$ is a solution: $g' \in C \cap M$. The algorithm returns $P_S(g') = g'$ at such a point.

*Proof.* $g' \in M$ by construction. Take a pixel $r \notin \gamma(g)$. Then $g(r) = H(g)(r) = g(r) - \beta g'(r)$, so $\beta g'(r) = 0$, and $g'(r) = 0$ since $\beta > 0$. So $g'$ is zero at every pixel outside $\gamma(g)$. Every pixel off $S$ is outside $\gamma(g)$, so $g'$ is zero off $S$. In the nonnegative case, a pixel of $S$ with $g'(r) < 0$ is outside $\gamma(g)$, so $g'(r) = 0$, which is a contradiction; so $g'(r) \ge 0$ on $S$, and $g'$ is real by the convention above. So $g' \in C$. Since $g' \in C$, the object projection of line L9 does not change it. $\square$

Theorem 2 is the main difference from [error reduction](/error-reduction-algorithm/). An error reduction fixed point can be a stagnation point with a positive error. A fixed point of HIO always gives a solution. The iterate $g$ itself need not be a solution: off the support it holds the accumulated feedback, and $P_M g$ is the answer.

**Theorem 3 (Douglas-Rachford, Bauschke, Combettes and Luke 2002).** Take the case with a support and no nonnegativity, so that $P_S$ (zero off $S$, unchanged on $S$) is a linear projection, and take $\beta = 1$. Then for every image $x$,

$$H(x) = x + P_S(2 P_M x - x) - P_M x .$$

The right side is the Douglas-Rachford iteration for the two sets $C$ and $M$.

*Proof.* Without nonnegativity, $\gamma(x) = S$. Let $p = P_M x$. On $S$: $P_S(2p - x)(r) = 2p(r) - x(r)$, so the right side is $x(r) + 2p(r) - x(r) - p(r) = p(r) = H(x)(r)$. Off $S$: $P_S(2p - x)(r) = 0$, so the right side is $x(r) - p(r) = H(x)(r)$ with $\beta = 1$. $\square$

**What is not claimed.** The convergence theorems for Douglas-Rachford need convex sets, and $M$ is not convex, so Theorem 3 gives no convergence. The value $\beta = 0.9$ that Fienup and later users found good is a tuned choice. The test file checks Theorems 1 and 3 and the update rule. It does not check a monotone error, because there is none.
