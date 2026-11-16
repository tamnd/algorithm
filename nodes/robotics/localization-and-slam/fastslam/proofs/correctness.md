---
title: The FastSLAM factorization, the weights and the cost of the landmark tree
proves: [correctness]
status: full
---

**Setting.** The robot path is $x_{1:t}$, the map is $m = (m_1, \dots, m_M)$ with $M$ landmarks (the page calls this count $m$), the controls are $u_{1:t}$, and the readings $z_{1:t}$ come with known correspondences $c_{1:t}$: reading $z_k$ is of landmark $m_{c_k}$. The model has three parts. The motion model is $p(x_k \mid x_{k-1}, u_k)$. The measurement model is $p(z_k \mid x_k, m_{c_k})$, which depends on one landmark only. The prior over the landmarks is $p(m) = \prod_j p(m_j)$.

**Claim.** (1) The posterior factors as $p(x_{1:t}, m \mid z_{1:t}, u_{1:t}, c_{1:t}) = p(x_{1:t} \mid z_{1:t}, u_{1:t}, c_{1:t}) \prod_j p(m_j \mid x_{1:t}, z_{1:t}, c_{1:t})$. (2) Lines L2 to L7 are the RBPF step for this factorization, with the path as the sampled part, the motion model as the proposal and one EKF per landmark; in the linear Gaussian case the per landmark filters and the weights are exact. (3) The tree gives each particle its own landmarks at a cost of $O(\log M)$ per update and $O(1)$ per copy.

## (1) The factorization

Fix the path $x_{1:t}$. The readings are conditionally independent given the path and the map, so by Bayes' rule

$$p(m \mid x_{1:t}, z_{1:t}, c_{1:t}) \propto p(m) \prod_{k=1}^{t} p(z_k \mid x_k, m_{c_k}) = \prod_j \Big[ p(m_j) \prod_{k : c_k = j} p(z_k \mid x_k, m_j) \Big].$$

The controls do not enter, because given the path they carry no information about the map. The right side is a product of functions of one landmark each, so after normalization the landmarks are independent given the path, and the factor of $m_j$ is $p(m_j \mid x_{1:t}, z_{1:t}, c_{1:t})$. The chain rule $p(x_{1:t}, m \mid \cdot) = p(x_{1:t} \mid \cdot) \, p(m \mid x_{1:t}, \cdot)$ gives the claim. This is the observation of Montemerlo, Thrun, Koller and Wegbreit (2002). It needs the whole path: given only the current pose $x_t$, the landmarks are correlated through the unknown past poses.

## (2) The filter step

The target of the sampling is $p(x_{1:t} \mid z_{1:t}, u_{1:t}, c_{1:t})$. By Bayes' rule and the Markov property,

$$p(x_{1:t} \mid z_{1:t}, u_{1:t}) \propto p(z_t \mid x_{1:t}, z_{1:t-1}) \, p(x_t \mid x_{t-1}, u_t) \, p(x_{1:t-1} \mid z_{1:t-1}, u_{1:t-1}).$$

Line L2 draws $x_t$ from the motion model, which is the proposal. The importance weight of the extended path is then the old weight times $p(z_t \mid x_{1:t}, z_{1:t-1})$. For one reading of landmark $j$,

$$p(z_t \mid x_{1:t}, z_{1:t-1}) = \int p(z_t \mid x_t, m_j) \, p(m_j \mid x_{1:t-1}, z_{1:t-1}) \, dm_j.$$

The second factor is the belief that the particle stores for $m_j$, $N(\mu_j, \Sigma_j)$. With the measurement model linearized at $\mu_j$, $z_t \approx h(x_t, \mu_j) + H (m_j - \mu_j) + v$ with $v \sim N(0, Q)$, so the integral is $N(z_t; \hat z, S)$ with $\hat z = h(x_t, \mu_j)$ and $S = H \Sigma_j H^\top + Q$. Line L7 multiplies the weight by this density. For a model that is linear in $m_j$ with Gaussian noise, the formula is exact.

Lines L5 and L6 are the EKF update of $m_j$ with the reading, the closed form part of the RBPF; they are exact for a model linear in $m_j$. Landmarks that are not read keep their belief, which is correct because by (1) a reading of $m_j$ carries no information about another landmark once the path is fixed. With several readings in one step, the same argument applies to each in turn, because the readings are independent given the path and the map, and they concern different landmarks or update the same one in sequence.

**A new landmark (line L4).** With a flat prior on $m_j$, the integral above is not a proper density. Line L4 sets the belief from the inverse of the linearized model, $\mu_j = h^{-1}(x_t, z_t)$ and $\Sigma_j = H^{-1} Q H^{-\top}$, which is the posterior of the linearized model under the flat prior. It multiplies the weight by a constant $p_0$. When all particles see the same new landmark, as with known correspondences, the constant cancels at normalization.

**A check.** If a particle reads a landmark a second time from the same pose with the same value, then $\Sigma_j = H^{-1} Q H^{-\top}$ gives $S = 2Q$ and $K = \Sigma_j H^\top S^{-1} = \tfrac12 H^{-1}$. So the mean does not move and $\Sigma_j$ halves, as two equal independent readings should give. The tests check this.

**Resampling (line L8).** Drawing $N$ particles with probabilities proportional to the weights keeps the represented distribution, as in every particle filter. Each copy needs its own path sample and its own landmark beliefs. FastSLAM keeps only the current pose of each path, since neither the weights nor the landmark updates use the older poses.

## (3) The persistent tree

The landmarks of a particle are the leaves of a complete binary tree of depth $d = \lceil \log_2 M \rceil$, indexed by the landmark id. A node is never changed after it is made.

- **get** follows the bits of the id from the root, $d$ steps.
- **set** makes a new leaf and a new copy of each of the $d$ nodes on the path from the root, each pointing to the new child on the path and to the old sibling. So it creates $d + 1$ nodes in $O(d)$ time. All other nodes are shared. Because no node is changed, every older root still describes the old map: the structure is persistent.
- **Copy** of a particle in line L8 copies the reference to its root, $O(1)$. Two particles that share nodes can never see each other's updates, because an update makes new nodes and does not change shared ones.

So a step with $k$ readings per particle costs $O(N k \log M)$ for the updates, plus $O(N)$ for the resampling. A plain array of $M$ landmarks per particle needs $O(N M)$ per step, because each resampled copy must copy the array. Montemerlo et al. (2002) give this $O(N \log M)$ bound per reading. Memory is $O(N M)$ in the worst case, and less when particles share subtrees.
