---
title: Gaussian BP is exact on trees, and at any fixed point its means solve J x = h
proves: [correctness]
status: full
---

We use the model $p(x) \propto \exp(-\tfrac12 x^\top J x + h^\top x)$ with $J$ symmetric positive definite, and the messages, cavity values $J_{i \setminus j}, h_{i \setminus j}$ and marginal values $\hat J_i, \hat h_i$ of the page. A message $(P_{ij}, v_{ij})$ stands for the function $\exp(-\tfrac12 P_{ij} x_j^2 + v_{ij} x_j)$.

**Lemma 1 (the update is the sum-product update).** If $J_{i \setminus j} > 0$, then

$$\int \exp\big(-\tfrac12 J_{i \setminus j} x_i^2 + h_{i \setminus j} x_i - J_{ij} x_i x_j\big)\, dx_i \propto \exp\big(-\tfrac12 P_{ij} x_j^2 + v_{ij} x_j\big)$$

with $P_{ij} = -J_{ij}^2 / J_{i \setminus j}$ and $v_{ij} = -J_{ij} h_{i \setminus j} / J_{i \setminus j}$.

*Proof.* With $a = J_{i \setminus j} > 0$ and $b = h_{i \setminus j} - J_{ij} x_j$, the integral $\int \exp(-\tfrac12 a x_i^2 + b x_i)\, dx_i$ is $\sqrt{2\pi / a}\, \exp(b^2 / (2a))$. Expand $b^2/(2a) = \tfrac{1}{2a}(h_{i \setminus j}^2 - 2 J_{ij} h_{i \setminus j} x_j + J_{ij}^2 x_j^2)$. The first term does not depend on $x_j$; the other two are $v_{ij} x_j$ and $-\tfrac12 P_{ij} x_j^2$. $\square$

The left side is the sum-product message from $i$ to $j$: the local factor $\exp(-\tfrac12 J_{ii} x_i^2 + h_i x_i)$, the pair factor $\exp(-J_{ij} x_i x_j)$, and the product of the incoming messages from $N(i) \setminus j$, whose exponents add to give $J_{i \setminus j}$ and $h_{i \setminus j}$.

**Theorem 1 (trees).** If the graph of $J$ is a tree, the synchronous iteration reaches a fixed point after at most $D + 1$ iterations, where $D$ is the diameter, and at the fixed point $\hat h_i / \hat J_i$ and $1 / \hat J_i$ are the exact mean and variance of $x_i$.

*Proof.* Remove the edge $(i, j)$; let $V_{i \to j}$ be the part that holds $i$. By induction on the height $k$ of $V_{i \to j}$ seen from $i$, the message on $(i, j)$ is constant from iteration $k + 1$ on and is proportional to the integral of $\exp(-\tfrac12 x^\top J x + h^\top x)$ restricted to the terms inside $V_{i \to j}$ and the edge $(i, j)$, over all the variables of $V_{i \to j}$. For $k = 0$, $i$ is a leaf of the cut tree, $J_{i \setminus j} = J_{ii} > 0$, and Lemma 1 gives the claim from the first iteration. For $k > 0$, the incoming messages are fixed from iteration $k$ on, by the induction hypothesis, and the subtrees behind them are disjoint, so the integral over $V_{i \to j}$ factors into the integrals over these subtrees times the integral over $x_i$, which is Lemma 1. The cavity precision $J_{i \setminus j}$ is the precision of $x_i$ in the Gaussian over $V_{i \to j}$ without the edge $(i, j)$, a Schur complement of a principal submatrix of $J$, and so positive. All heights are at most $D$. Then the product of the local factor of $j$ and all its incoming messages is proportional to the marginal density of $x_j$, a Gaussian with precision $\hat J_j$ and potential $\hat h_j$, whose mean is $\hat h_j / \hat J_j$ and whose variance is $1 / \hat J_j$. $\square$

**Theorem 2 (means at a fixed point; Weiss and Freeman 2001).** Let the messages be a fixed point of the updates with all $J_{i \setminus j} > 0$ and all $\hat J_i \ne 0$, and let $\mu_i = \hat h_i / \hat J_i$. Then $J \mu = h$, so $\mu$ is the exact mean, on any graph.

*Proof.* Fix an edge $(i, j)$ and write $a = J_{i \setminus j}$, $b = J_{j \setminus i}$, $c = J_{ij}$, $p = h_{i \setminus j}$, $q = h_{j \setminus i}$. At the fixed point, $P_{ji} = -c^2 / b$ and $v_{ji} = -c q / b$, and $\hat J_i = a + P_{ji}$, $\hat h_i = p + v_{ji}$, because $\hat J_i$ is $J_{i \setminus j}$ plus the message from $j$. So $\hat J_i = (ab - c^2)/b$ and $\hat h_i = (pb - cq)/b$, and $ab - c^2 = b \hat J_i \ne 0$. Then

$$\mu_i = \frac{pb - cq}{ab - c^2}, \qquad \mu_j = \frac{qa - cp}{ab - c^2}$$

(the second by the same argument with $i$ and $j$ swapped), which is the solution of the $2 \times 2$ system $a \mu_i + c \mu_j = p$, $c \mu_i + b \mu_j = q$, by Cramer's rule. The first equation reads $J_{i \setminus j} \mu_i + J_{ij} \mu_j = h_{i \setminus j}$. Substitute $J_{i \setminus j} = \hat J_i - P_{ji}$ and $h_{i \setminus j} = \hat h_i - v_{ji}$, and use $\hat h_i = \hat J_i \mu_i$:

$$v_{ji} - P_{ji} \mu_i = -J_{ij} \mu_j.$$

Add this over all $j \in N(i)$. The left side becomes $(\hat h_i - h_i) - \mu_i (\hat J_i - J_{ii}) = J_{ii} \mu_i - h_i$. So $J_{ii} \mu_i + \sum_{j \in N(i)} J_{ij} \mu_j = h_i$, and as $J_{ij} = 0$ for $j \notin N(i) \cup \{i\}$, this is row $i$ of $J \mu = h$. As $J$ is invertible, $\mu = J^{-1} h$. $\blacksquare$

**Remark.** Theorem 2 says nothing about the variances, and they are wrong in general on graphs with cycles. It also says nothing about convergence. Malioutov, Johnson and Willsky (2006) proved that if $J$ is walk-summable, that is, if the spectral radius of $|R|$ with $R = I - D^{-1/2} J D^{-1/2}$ is below 1, the variances and the means converge; that proof is not repeated here.
