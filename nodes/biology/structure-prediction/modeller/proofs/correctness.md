---
title: What the restraint objective of MODELLER guarantees
proves: [correctness]
status: full
---

We use the core model of the page: coordinates $x = (x_1, \ldots, x_n)$ in $\mathbb{R}^3$, and a set $R$ of Gaussian distance restraints $\rho = (i, j, d_0, \sigma)$ with $i < j$ and $\sigma > 0$. Write $d_{ij}(x) = |x_i - x_j|$ and

$$F(x) = \sum_{\rho \in R} \frac{1}{2} \left( \frac{d_{ij}(x) - d_0}{\sigma} \right)^2.$$

MODELLER is a local optimizer of a nonconvex function, so the claims are about the objective and about the descent, not about a global optimum.

**Proposition 1 (the objective is a negative log density).** Let $p_\rho(d) = \frac{1}{\sigma\sqrt{2\pi}} \exp\big(-\frac{1}{2}((d - d_0)/\sigma)^2\big)$. Then

$$-\sum_{\rho \in R} \ln p_\rho\big(d_{ij}(x)\big) = F(x) + \sum_{\rho \in R} \ln\big(\sigma\sqrt{2\pi}\big).$$

So $x$ minimizes $F$ if and only if it maximizes the product $\prod_\rho p_\rho(d_{ij}(x))$, the molecular density under the independence assumption.

*Proof.* $-\ln p_\rho(d) = \ln(\sigma\sqrt{2\pi}) + \frac{1}{2}((d - d_0)/\sigma)^2$. Sum over $\rho$. The second sum does not depend on $x$, and $-\ln$ is strictly decreasing, so the minimizers of $F$ are the maximizers of the product. $\square$

**Proposition 2 (invariance).** For each rotation or reflection $Q$ (an orthogonal $3 \times 3$ matrix) and each vector $b$, $F(Qx + b) = F(x)$, where $Qx + b$ moves each atom.

*Proof.* $|(Qx_i + b) - (Qx_j + b)| = |Q(x_i - x_j)| = |x_i - x_j|$, since an orthogonal matrix keeps lengths. Each term of $F$ depends on $x$ only through such a distance. $\square$

In particular a reflection, $\det Q = -1$, does not change $F$. Distance restraints cannot tell a model from its mirror image.

**Proposition 3 (the template is a global minimum).** Let every target residue $i$ be aligned to a template residue $k(i)$, with $k$ increasing, and let each restraint have $d_0 = |T_{k(i)} - T_{k(j)}|$, including the chain restraints when consecutive template atoms are $3.8$ Å apart. Then $F \ge 0$, $F(y) = 0$ for $y_i = T_{k(i)}$, and every $x$ with $F(x) = 0$ has $d_{ij}(x) = d_{ij}(y)$ for every restrained pair $(i, j)$.

*Proof.* Each term is a square divided by a positive number, so $F \ge 0$. At $y$, each term has $d_{ij}(y) = d_0$ and so is zero. If $F(x) = 0$, each nonnegative term is zero, so $d_{ij}(x) = d_0 = d_{ij}(y)$ for each restraint. $\square$

The converse direction, that $F(x) = 0$ forces $x$ to be a rigid motion of $y$, holds only when the restrained distances fix the shape. The page example has a circle of solutions with $F = 0$, because one residue has only two restraints.

**Lemma 4 (the gradient).** Where $d_{ij}(x) > 0$, the gradient of the term of $\rho$ with respect to $x_i$ is

$$\frac{d_{ij}(x) - d_0}{\sigma^2} \cdot \frac{x_i - x_j}{d_{ij}(x)},$$

the gradient with respect to $x_j$ is the negative of this vector, and the gradient with respect to the other atoms is zero.

*Proof.* $\nabla_{x_i} |x_i - x_j| = (x_i - x_j)/|x_i - x_j|$ where the distance is not zero, and $\nabla_{x_j} |x_i - x_j|$ is its negative. The chain rule applied to $\frac{1}{2}((d - d_0)/\sigma)^2$, whose derivative in $d$ is $(d - d_0)/\sigma^2$, gives the claim. $\square$

**Proposition 5 (descent).** Let the minimizer accept a step $x' = x + t p$ only if $F(x') \le F(x) + c\, t\, \nabla F(x) \cdot p$ with a fixed $c \in (0, 1)$, where $p$ is a descent direction, $\nabla F(x) \cdot p < 0$. Then the values $F(x^{(0)}), F(x^{(1)}), \ldots$ of the accepted iterates are nonincreasing and converge.

*Proof.* With $t > 0$ and $\nabla F(x) \cdot p < 0$, the right side is less than $F(x)$, so every accepted step lowers $F$ or keeps it when the search stops. A nonincreasing sequence of real numbers that is bounded below, here by $0$ (Proposition 3, first part, which holds for any restraints), converges. The implementation restarts with $p = -\nabla F(x)$ when the conjugate direction is not a descent direction, so the condition on $p$ always holds. $\square$

**What is not guaranteed.** $F$ is not convex in $x$. For example, with two restraints that pull one atom to distance $3.8$ from two atoms $3.8$ apart, the set of minima is a circle, which is not convex, and the midpoint between two points of the circle is not a minimum. So a descent method can stop at a local minimum or a saddle, and the simulated annealing stage, which can raise $F$, gives no certificate. The method guarantees the objective (Propositions 1 to 3) and the descent of its minimizer (Proposition 5), not the global optimum.
