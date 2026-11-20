---
title: Direct summation gives the exact accelerations, the potential energy and zero total force
proves: [correctness]
status: full
---

We use exact real arithmetic, as in the real RAM model. Let $N \ge 1$, masses $m_i > 0$, positions $\mathbf{x}_i$, $G > 0$ and $\epsilon \ge 0$. If $\epsilon = 0$, we assume that no two positions are equal. For a pair $i \ne j$ write $\mathbf{d}_{ij} = \mathbf{x}_j - \mathbf{x}_i$, $s_{ij} = |\mathbf{d}_{ij}|^2 + \epsilon^2 > 0$ and $w_{ij} = G s_{ij}^{-3/2}$. Then $\mathbf{d}_{ji} = -\mathbf{d}_{ij}$, $s_{ji} = s_{ij}$ and $w_{ji} = w_{ij}$.

**Claim 1 (the loop computes the sums).** After line L10, $\mathbf{a}_i = \sum_{j \ne i} m_j w_{ij} \mathbf{d}_{ij}$ for each $i$, and $U = -G \sum_{i < j} m_i m_j s_{ij}^{-1/2}$.

*Proof.* Lines L2 and L3 run over the pairs $(i, j)$ with $i < j$, and each such pair occurs exactly once. Consider a fixed body $k$. The pairs that change $\mathbf{a}_k$ are the pairs $(k, j)$ with $j > k$, at line L7, and the pairs $(i, k)$ with $i < k$, at line L8. Line L7 for the pair $(k, j)$ adds $m_j w_{kj} \mathbf{d}_{kj}$. Line L8 for the pair $(i, k)$ adds $-m_i w_{ik} \mathbf{d}_{ik} = m_i w_{ki} \mathbf{d}_{ki}$. So each $j \ne k$ adds its term exactly once, and $\mathbf{a}_k$ starts at $0$ by line L1. Line L9 adds the term of each pair $i < j$ to $U$ exactly once, and $U$ starts at $0$. $\square$

**Claim 2 (force is minus the gradient).** For each $i$, $m_i \mathbf{a}_i = -\nabla_{\mathbf{x}_i} U$.

*Proof.* Only the pairs that contain $i$ depend on $\mathbf{x}_i$. For the pair of $i$ and $j$, the term of $U$ is $-G m_i m_j s_{ij}^{-1/2}$, and $\nabla_{\mathbf{x}_i} s_{ij} = -2 \mathbf{d}_{ij}$. So
$$\nabla_{\mathbf{x}_i}\left(-G m_i m_j s_{ij}^{-1/2}\right) = -G m_i m_j \left(-\tfrac{1}{2}\right) s_{ij}^{-3/2} \left(-2 \mathbf{d}_{ij}\right) = -m_i m_j w_{ij} \mathbf{d}_{ij}.$$
So minus the gradient of this term is $m_i m_j w_{ij} \mathbf{d}_{ij}$.
The sum over $j \ne i$ is $m_i \mathbf{a}_i$ by Claim 1. $\square$

**Claim 3 (zero total force).** $\sum_i m_i \mathbf{a}_i = 0$.

*Proof.* By Claim 1, $\sum_i m_i \mathbf{a}_i = \sum_i \sum_{j \ne i} m_i m_j w_{ij} \mathbf{d}_{ij}$. Group the terms in pairs $\{i, j\}$. The two terms of a pair are $m_i m_j w_{ij} \mathbf{d}_{ij}$ and $m_j m_i w_{ji} \mathbf{d}_{ji} = -m_i m_j w_{ij} \mathbf{d}_{ij}$, so they cancel. $\square$

**Consequences.** Claim 1 is the definition of the softened (or, for $\epsilon = 0$, the Newtonian) accelerations, so the algorithm has no truncation error. By Claim 3, an integrator that updates all velocities with forces computed at one common time changes the total momentum $\sum_i m_i \mathbf{v}_i$ by $h \sum_i m_i \mathbf{a}_i = 0$ per kick. In floating-point arithmetic the two terms of a pair are computed from the same rounded $w_{ij}$ and $\mathbf{d}_{ij}$, but the sums are rounded in different orders, so Claim 3 holds only up to rounding.

**Cost.** The inner body of lines L4 to L9 runs $\sum_{i=1}^{N-1} (N - i) = N(N-1)/2$ times, and each run costs a constant number of operations for a fixed dimension. Line L1 costs $\Theta(N)$. So the time is $\Theta(N^2)$ for all inputs, and the extra space is the $N$ accelerations. $\square$
