---
title: Fixed points of the one-step-late algorithm, and why it is not monotone
proves: [correctness]
status: full
---

We use the notation of the page. $A$ is an $m \times N$ matrix with $a_{ij} \ge 0$ and column sums $s_j > 0$, $b \ge 0$, $y \ge 0$, $\beta \ge 0$, and
$$\Phi(x) = L(x) - \beta R(x), \qquad L(x) = \sum_i \big[y_i \log \bar y_i - \bar y_i\big], \qquad R(x) = \tfrac12 \sum_{\{j,k\} \in E} w_{jk} (x_j - x_k)^2,$$
with $\bar y = A x + b$ and weights $w_{jk} \ge 0$ on the edges $E$. Write $u_j(x) = \partial R / \partial x_j = \sum_{k \sim j} w_{jk} (x_j - x_k)$ and $g_j(x) = \sum_i a_{ij} y_i / \bar y_i$. One iteration (lines L4 to L9) maps $x$ to
$$x'_j = \frac{x_j\, g_j(x)}{s_j + \beta u_j(x)}, \tag{1}$$
and it is defined only if every denominator $d_j(x) = s_j + \beta u_j(x)$ is positive. We work in exact arithmetic.

**Where the update comes from.** For a fixed admissible $x$, the MLEM proof gives the surrogate $L(x') \ge C + \sum_j [x_j g_j(x) \log x'_j - s_j x'_j]$. Maximizing this surrogate minus $\beta R(x')$ would need the solution of the coupled equations
$$\frac{x_j g_j(x)}{x'_j} - s_j - \beta u_j(x') = 0 \quad \text{for all } j,$$
which couple the pixels through $u_j(x')$. Green's idea is to evaluate $u_j$ one step late, at the old image $x$. Then each equation has one unknown and the solution is (1). So (1) is not the maximizer of a surrogate of $\Phi$, and the monotone argument of MLEM does not apply.

**Theorem 1 (fixed points).** Let $x > 0$ with $\bar y_i > 0$ wherever $y_i > 0$, and $d_j(x) > 0$ for all $j$. Then $x$ is a fixed point of (1) if and only if $\nabla \Phi(x) = 0$.

*Proof.* $\partial \Phi / \partial x_j = g_j(x) - s_j - \beta u_j(x)$. Since $x_j > 0$ and $d_j(x) > 0$, (1) gives $x'_j = x_j$ if and only if $g_j(x) = s_j + \beta u_j(x)$, that is $\partial \Phi / \partial x_j = 0$. $\square$

$\Phi$ is concave, because $L$ is concave and $R$ is a convex quadratic. So a positive fixed point is a maximizer of $\Phi$ over $x \ge 0$. If $\Phi$ is strictly concave (for example if $A$ has full column rank on the rows with $y_i > 0$), it is the unique maximizer.

**Theorem 2 (a sufficient condition for a positive denominator).** If $x \ge 0$ and $\beta \sum_{k \sim j} w_{jk} x_k < s_j$, then $d_j(x) > 0$.

*Proof.* $u_j(x) = x_j \sum_{k \sim j} w_{jk} - \sum_{k \sim j} w_{jk} x_k \ge -\sum_{k \sim j} w_{jk} x_k$, because $x_j \ge 0$. So $d_j(x) \ge s_j - \beta \sum_{k \sim j} w_{jk} x_k > 0$. $\square$

The condition depends on the current image, so it cannot be checked once in advance. For a fixed image it holds for $\beta$ small enough, and it can fail for a large $\beta$, as the next theorem shows.

**Theorem 3 (failure for a large beta).** There are data and a $\beta > 0$ for which the second iterate has a nonpositive denominator, and data and a $\beta > 0$ for which $\Phi$ decreases from one iterate to the next.

*Proof.* Take two pixels, $A = I$, $b = 0$, $y = (1, 3)$, one edge with $w_{12} = 1$, and the start $x^0 = (2, 2)$. Then $g_j(x) = y_j / x_j$, so $x_j g_j(x) = y_j$ and (1) reads $x'_1 = 1 / (1 + \beta (x_1 - x_2))$ and $x'_2 = 3 / (1 + \beta (x_2 - x_1))$. At $x^0$ the penalty gradient is 0, so $x^1 = (1, 3)$ for every $\beta$. At $x^1$, $d_1 = 1 - 2\beta$, which is 0 for $\beta = 1/2$ and $-1$ for $\beta = 1$. For $\beta = 1$ the formula (1) would give $x^2_1 = 1/(-1) = -1 < 0$.

For $\beta = 3/10$, $d_1(x^1) = 2/5$ and $d_2(x^1) = 8/5$, so $x^2 = (5/2, 15/8)$. Then
$$\Phi(x^1) = \log 1 - 1 + 3 \log 3 - 3 - \tfrac{3}{20} \cdot 4 = -1.3042, \qquad \Phi(x^2) = \log \tfrac52 - \tfrac52 + 3 \log \tfrac{15}{8} - \tfrac{15}{8} - \tfrac{3}{20} \cdot \tfrac{25}{64} = -1.6315,$$
so $\Phi(x^2) < \Phi(x^1)$. $\square$

In the same example with $\beta = 3/10$ the iterates oscillate with a growing amplitude: $x^3 = (16/19, 48/13)$, $x^4 = (1235/179, 3705/2291)$, and $d_2(x^4) < 0$. The maximizer of $\Phi$ for $\beta = 3/10$ is about $(1.395, 2.338)$, a positive point. So the failure is a property of the iteration, not of the problem.

**Convergence (cited, not proved here).** Green (1990) gave no general convergence proof. Lange (1990) showed that a modified OSL with a line search along the OSL direction increases $\Phi$ at each step and converges under conditions on the penalty. For a small $\beta$ the plain update usually converges in practice; this is an observation, as in the $\beta = 1/10$ example of the page.
