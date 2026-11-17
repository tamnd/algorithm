---
title: Each block step keeps Q and F feasible and never lowers the likelihood, the accelerated round never lowers it, and fixed points satisfy the KKT conditions
proves: [correctness]
status: full
---

**Setting.** $g_{ij} \in \{0, 1, 2\}$, each row $q_i$ of $Q$ is on the simplex $\Delta_K$, and $f_{kj} \in [0, 1]$. Write $\phi_{ij} = \sum_k q_{ik} f_{kj}$ and $L(Q, F) = \sum_{i, j} [g_{ij} \ln \phi_{ij} + (2 - g_{ij}) \ln(1 - \phi_{ij})]$, where a term with a zero count is 0. Assume the current point has $L > -\infty$. On $\Delta_K$, $1 - \phi_{ij} = \sum_k q_{ik} (1 - f_{kj})$.

**Complete data.** Give each of the two allele copies of $(i, j)$ a hidden label $z \in \{1, \ldots, K\}$, its source population. In the complete model, $P(z = k) = q_{ik}$, and given $z = k$ the copy is allele 1 with probability $f_{kj}$, independently over copies. Summing over the labels gives the binomial law of $g_{ij}$ with parameter $\phi_{ij}$, so $L$ is the observed-data log-likelihood of this model.

**Lemma 1 (E-step).** Given $g_{ij}$ and the current $(Q, F)$, the expected number of the $g_{ij}$ copies of allele 1 with label $k$ is $a_{ijk} = g_{ij} q_{ik} f_{kj} / \phi_{ij}$, and of the $2 - g_{ij}$ copies of allele 0 it is $b_{ijk} = (2 - g_{ij}) q_{ik} (1 - f_{kj}) / (1 - \phi_{ij})$. Also $\sum_k (a_{ijk} + b_{ijk}) = 2$.

*Proof.* For a copy of allele 1, Bayes' rule gives $P(z = k \mid \text{allele } 1) = q_{ik} f_{kj} / \phi_{ij}$, and the copies are independent given the parameters, so the expectation is $g_{ij}$ times this. The same holds for allele 0 with $1 - \phi_{ij} = \sum_k q_{ik}(1 - f_{kj})$. The posteriors of one copy sum to 1 over $k$, and there are 2 copies. $\square$

**Lemma 2 (M-steps).** Let $N^1_{ijk}$ and $N^0_{ijk}$ be the numbers of copies of allele 1 and of allele 0 with label $k$. The complete-data log-likelihood is

$$\ell_c = \sum_{i, k} (N^1_{i \cdot k} + N^0_{i \cdot k}) \ln q_{ik} + \sum_{k, j} \big( N^1_{\cdot jk} \ln f_{kj} + N^0_{\cdot jk} \ln(1 - f_{kj}) \big),$$

where a dot means a sum over that index. With $N$ replaced by its conditional means $a$ and $b$ (Lemma 1), the function $Q_c$ so obtained has its maximum over $\Delta_K$ in each row $q_i$ at $q_{ik} = \frac{1}{2m} \sum_j (a_{ijk} + b_{ijk})$, and its maximum over $[0, 1]$ in each $f_{kj}$ at $f_{kj} = \sum_i a_{ijk} / \sum_i (a_{ijk} + b_{ijk})$ when the denominator is positive.

*Proof.* The $q_i$ part is $\sum_k c_k \ln q_{ik}$ with $c_k = \sum_j (a_{ijk} + b_{ijk}) \ge 0$ and $\sum_k c_k = 2m$ by Lemma 1. By Gibbs' inequality its maximum on the simplex is at $q_{ik} = c_k / 2m$. The $f_{kj}$ part is $A \ln f + B \ln(1 - f)$ with $A, B \ge 0$, which is concave with maximum at $A / (A + B)$. $\square$

**Theorem 1 (block steps).** Let $Q'$ be the result of the Q update with $F$ fixed. Then each row of $Q'$ is on $\Delta_K$, and $L(Q', F) \ge L(Q, F)$. Let $F'$ be the result of the F update with $Q$ fixed. Then $F' \in [0, 1]^{K \times m}$ and $L(Q, F') \ge L(Q, F)$.

*Proof.* Feasibility: the entries of $Q'$ are non-negative, and its row sums are $\frac{1}{2m} \sum_j 2 = 1$ by Lemma 1. The entries of $F'$ are ratios of a non-negative number to a larger or equal one; where the denominator is 0, the code keeps the old value. Ascent: consider the complete-data model in which only the block being updated is free. The Q update maximizes the expected complete-data log-likelihood over $Q$ with $F$ fixed, by Lemma 2, so it is one EM step of the model with parameter $Q$ alone. The standard EM inequality (the observed log-likelihood equals the expected complete-data log-likelihood minus the expected log of the conditional law of the labels, and the second term is largest at the current value by Gibbs' inequality) gives $L(Q', F) \ge L(Q, F)$. The same argument with $F$ as the free block gives the second claim. $\square$

**Corollary (one round).** The map BLOCK of line L3 gives $L(\mathrm{BLOCK}(x)) \ge L(x)$, so $L(x_2) \ge L(x_1) \ge L(x)$.

**Theorem 2 (accelerated round).** The point chosen by lines L6 to L9 is feasible, and its likelihood is at least $L(x)$.

*Proof.* If the extrapolated point is used, line L7 has made it feasible: each row of $Q$ is the Euclidean projection onto $\Delta_K$, then raised to at least $\delta_q > 0$ and renormalized, so it is on $\Delta_K$; each $f_{kj}$ is clipped to $[\delta, 1 - \delta]$. Then $\phi_{ij} \in [\delta, 1 - \delta]$, so $L$ is finite. Line L8 keeps the extrapolated point only if its likelihood is at least $L(x_2)$, and otherwise keeps $x_2$. In both cases the likelihood is at least $L(x_2) \ge L(x)$ by the corollary. If $u = 0$ or $u^{\mathsf T}(v - u) \ge 0$, the code keeps $x_2$. $\square$

So the values $L^{(t)}$ do not decrease. Each $\phi_{ij} \in [0, 1]$ makes every term at most 0, so $L \le 0$, and the values converge. This shows that the test of line L10 is met for every $\varepsilon > 0$.

**Lemma 3 (the projection).** For $y \in \mathbb R^K$, the function project_simplex returns the unique point of $\Delta_K$ nearest to $y$.

*Proof.* $\Delta_K$ is closed and convex, so the nearest point $p$ is unique. The KKT conditions of minimizing $\frac12 \lVert p - y \rVert^2$ under $\sum p_k = 1$ and $p \ge 0$ say that $p_k = \max(y_k - \tau, 0)$ for one number $\tau$ with $\sum_k \max(y_k - \tau, 0) = 1$. The left side is continuous and strictly decreasing in $\tau$ where it is positive, so $\tau$ is unique. With $y$ sorted as $u_1 \ge \cdots \ge u_K$, let $\rho$ be the largest index with $u_\rho - (\sum_{s \le \rho} u_s - 1)/\rho > 0$; then $\tau = (\sum_{s \le \rho} u_s - 1)/\rho$ makes exactly the first $\rho$ entries positive and gives sum 1, which is what the code computes. $\square$

**Theorem 3 (fixed points).** Suppose a BLOCK round leaves $(Q, F)$ unchanged. Then for each $i$ and each $k$ with $q_{ik} > 0$, $\partial L / \partial q_{ik} = 2m$, where the derivative is taken with $1 - \phi_{ij}$ written as $\sum_k q_{ik}(1 - f_{kj})$. For each $k, j$ with $0 < f_{kj} < 1$, $\partial L / \partial f_{kj} = 0$.

*Proof.* With that form of $1 - \phi$, $\partial L / \partial q_{ik} = \sum_j [g_{ij} f_{kj} / \phi_{ij} + (2 - g_{ij})(1 - f_{kj}) / (1 - \phi_{ij})]$, so $q_{ik}\, \partial L / \partial q_{ik} = \sum_j (a_{ijk} + b_{ijk}) = 2m\, q'_{ik}$. If $Q' = Q$ and $q_{ik} > 0$, dividing by $q_{ik}$ gives $2m$. For $F$, $\partial L / \partial f_{kj} = \sum_i q_{ik} [g_{ij} / \phi_{ij} - (2 - g_{ij}) / (1 - \phi_{ij})] = A / f_{kj} - B / (1 - f_{kj})$ with $A = \sum_i a_{ijk}$ and $B = \sum_i b_{ijk}$. If $F' = F$ then $f_{kj} = A / (A + B)$, and the derivative is $(A + B) - (A + B) = 0$. Since BLOCK first updates $Q$ and then updates $F$ with the new $Q$, a fixed point of BLOCK has $Q' = Q$ and then $F' = F$. $\square$

The derivative in a row of $Q$ is equal on the support of $q_i$, with Lagrange multiplier $2m$ for the constraint $\sum_k q_{ik} = 1$. This is the KKT condition on the support. For $L$ written with $1 - \phi = 1 - \sum_k q_{ik} f_{kj}$, the derivatives differ by the constant $\sum_j (2 - g_{ij}) / (1 - \phi_{ij})$ in all $k$, so the condition is the same. The theorem does not say that the point is a local maximum; the symmetric start of the tests is a fixed point with $L = 8 \ln \frac12$, while $q_1 = (1, 0)$, $q_2 = (0, 1)$ with matching frequencies gives $L = 0$.
