---
title: Why the Gaussian mixture PHD recursion is exact under linear Gaussian models, constant detection and survival probabilities and Gaussian mixture birth, and what pruning and merging keep
proves: [correctness]
status: full
---

Notation as on the page. $\mathcal N(x; m, P)$ is the Gaussian density with mean $m$ and a symmetric positive definite covariance $P$. The matrices $Q$ and $R$ are positive definite, and $\kappa(z) > 0$ for every $z$. The PHD recursion is Mahler's prediction and update, as written on the page. This file proves that lines L1 to L5 compute it exactly when the PHD of the previous frame is a Gaussian mixture, and states what lines L6 and L7 keep.

## Two facts about Gaussians

**Lemma A.** $\int \mathcal N(x; F x', Q) \, \mathcal N(x'; m, P) \, dx' = \mathcal N(x; F m, F P F^\mathsf{T} + Q)$.

*Proof.* Let $x'$ have the density $\mathcal N(x'; m, P)$ and let $x = F x' + v$, with $v$ independent of $x'$ and with density $\mathcal N(v; 0, Q)$. Given $x'$, the density of $x$ is $\mathcal N(x; F x', Q)$, so by the law of total probability the left side is the density of $x$. A linear function of the independent Gaussian vectors $x'$ and $v$ is Gaussian, with mean $F m$ and covariance $F P F^\mathsf{T} + Q$. This covariance is positive definite because $Q$ is. $\square$

**Lemma B.** Let $\eta = H m$, $S = H P H^\mathsf{T} + R$, $K = P H^\mathsf{T} S^{-1}$ and $P^+ = (I - K H) P$. Then

$$\mathcal N(z; H x, R) \, \mathcal N(x; m, P) = \mathcal N(z; \eta, S) \, \mathcal N(x; m + K (z - \eta), P^+).$$

*Proof.* Let $x$ have the density $\mathcal N(x; m, P)$ and let $z = H x + w$, with $w$ independent of $x$ and with density $\mathcal N(w; 0, R)$. The left side is the joint density of $(x, z)$. The pair is jointly Gaussian with mean $(m, \eta)$ and covariance with the blocks $P$, $P H^\mathsf{T}$, $H P$ and $S$. The matrix $S$ is positive definite because $R$ is. A joint density is the marginal density of $z$, which is $\mathcal N(z; \eta, S)$, times the conditional density of $x$ given $z$. For a jointly Gaussian pair this conditional density is Gaussian with mean $m + P H^\mathsf{T} S^{-1} (z - \eta) = m + K (z - \eta)$ and covariance $P - P H^\mathsf{T} S^{-1} H P = (I - K H) P$, by the standard formula for Gaussian conditioning (the Schur complement). $\square$

Lemma B is the measurement update of the [Kalman filter](/kalman-filter/), with the normalizing constant $\mathcal N(z; \eta, S)$ kept.

## Claim 1: the mixture is closed, and lines L1 to L5 are exact

Let $D_{k-1}(x) = \sum_j w_j \, \mathcal N(x; m_j, P_j)$. Then the predicted PHD is the mixture of lines L1 and L2, and the updated PHD is the mixture of lines L4 and L5.

*Proof.* The prediction is linear in $D_{k-1}$, and $p_S$ is a constant, so it can be taken out of the integral:

$$D_{k|k-1}(x) = \sum_j p_S w_j \int \mathcal N(x; F x', Q) \, \mathcal N(x'; m_j, P_j) \, dx' + \gamma(x) = \sum_j p_S w_j \, \mathcal N(x; F m_j, F P_j F^\mathsf{T} + Q) + \sum_b w_b \, \mathcal N(x; m_b, P_b)$$

by Lemma A. This is line L1 for the surviving components and line L2 for the birth components, since the birth intensity is a Gaussian mixture.

Write the predicted PHD as $\sum_k w_k \, \mathcal N(x; m_k, P_k)$ and let $\eta_k$, $S_k$, $K_k$ and $P^+_k$ be as in line L3, with $q_k = \mathcal N(z; \eta_k, S_k)$. The missed term of the update is $(1 - p_D) D_{k|k-1}(x) = \sum_k (1 - p_D) w_k \, \mathcal N(x; m_k, P_k)$, which is line L4. For a measurement $z$, because $p_D$ is a constant, Lemma B gives

$$p_D \, \mathcal N(z; H x, R) \, D_{k|k-1}(x) = \sum_k p_D w_k q_k \, \mathcal N(x; m_k + K_k (z - \eta_k), P^+_k).$$

Each Gaussian on the right integrates to 1, so the integral in the denominator of the update is $\sum_l p_D w_l q_l$. Dividing by $\kappa(z) + \sum_l p_D w_l q_l$ gives the components of line L5, one for each $k$, with the weights $p_D w_k q_k / (\kappa(z) + \sum_l p_D w_l q_l)$. The update is the sum of the missed term and of these terms over all $z \in Z$, which is the mixture that lines L4 and L5 build. $\square$

Each hypothesis is used. If $p_D$ depended on $x$, the product $p_D(x) \, \mathcal N(x; m, P)$ would not be a Gaussian in general. If $p_S$ depended on $x$, the same would hold in the prediction. If the models were not linear Gaussian, Lemmas A and B would not apply. If the birth intensity were not a Gaussian mixture, line L2 would not add Gaussian components.

## Claim 2: the expected number of targets

The weights after line L5 sum to $(1 - p_D) \hat N_{k|k-1} + \sum_{z \in Z} \rho(z)$, where $\hat N_{k|k-1} = p_S \hat N_{k-1} + \sum_b w_b$ and $\rho(z) = A(z) / (\kappa(z) + A(z))$ with $A(z) = \sum_l p_D w_l q_l$. Each $\rho(z)$ lies in $[0, 1)$.

*Proof.* The integral of a mixture is the sum of its weights, since each Gaussian integrates to 1. By the property of the PHD on the page, this integral is the expected number of targets. The weights of line L1 sum to $p_S \hat N_{k-1}$, and line L2 adds $\sum_b w_b$. Line L4 gives $(1 - p_D) \hat N_{k|k-1}$. For one $z$, the weights of line L5 sum to $\sum_k p_D w_k q_k / (\kappa(z) + A(z)) = \rho(z)$. Since $A(z) \ge 0$ and $\kappa(z) > 0$, $0 \le \rho(z) < 1$. With $Z$ empty the sum is $(1 - p_D)(p_S \hat N_{k-1} + \sum_b w_b)$. $\square$

## Claim 3: what line L6 keeps

Let a merge join the components $i \in G$ into $(\tilde w, \tilde m, \tilde P)$ with $\tilde w = \sum_{i \in G} w_i$, $\tilde m = \sum_{i \in G} w_i m_i / \tilde w$ and $\tilde P = \sum_{i \in G} w_i (P_i + (\tilde m - m_i)(\tilde m - m_i)^\mathsf{T}) / \tilde w$. Then the merged component has the same integral, the same first moment and the same second moment as the part of the mixture it replaces, and $\tilde P$ is positive definite. Pruning a set of components of total weight $\delta$ changes the PHD by exactly $\delta$ in the $L^1$ norm. The merge loop stops after at most as many rounds as there are components.

*Proof.* The part $\sum_{i \in G} w_i \, \mathcal N(x; m_i, P_i)$ has integral $\sum w_i = \tilde w$, first moment $\int x \sum w_i \mathcal N_i = \sum w_i m_i = \tilde w \tilde m$, and second moment $\sum w_i (P_i + m_i m_i^\mathsf{T})$. The merged component has the integral $\tilde w$, the first moment $\tilde w \tilde m$ and the second moment $\tilde w (\tilde P + \tilde m \tilde m^\mathsf{T})$. Expanding,

$$\tilde w \tilde P = \sum w_i P_i + \tilde w \tilde m \tilde m^\mathsf{T} - \tilde m \Big(\sum w_i m_i\Big)^\mathsf{T} - \Big(\sum w_i m_i\Big) \tilde m^\mathsf{T} + \sum w_i m_i m_i^\mathsf{T} = \sum w_i (P_i + m_i m_i^\mathsf{T}) - \tilde w \tilde m \tilde m^\mathsf{T},$$

since $\sum w_i m_i = \tilde w \tilde m$. So the second moments agree. The matrix $\tilde P$ is a positive combination of positive definite matrices and positive semidefinite matrices, so it is positive definite.

Every component is a nonnegative function, so removing components of total weight $\delta$ removes a nonnegative function with integral $\delta$, and the $L^1$ distance is $\delta$. The same holds for the cap $J_{\max}$, which removes the lightest components. In each round of merging, the heaviest component $j$ is at distance 0 from itself, so it is in the group and is removed, and the number of remaining components falls by at least one. $\square$

Line L7 reads the expected number from the weights by Claim 2. The rule that reports a mean for each weight above 0.5 is a heuristic of Vo and Ma, not a consequence of the recursion. The PHD recursion is itself an approximation of the multi-target Bayes filter. So these claims prove that the mixture is the exact PHD before line L6, and they do not prove that the reported states are close to the true states.
