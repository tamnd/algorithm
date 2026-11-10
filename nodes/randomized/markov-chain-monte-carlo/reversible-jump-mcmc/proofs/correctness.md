---
title: With the Jacobian in the acceptance ratio, every reversible jump satisfies detailed balance with respect to π
proves: [correctness]
status: full
---

**Setting.** $\mathcal{X} = \bigcup_{k=0}^K\{k\} \times \mathbb{R}^{d_k}$ with the measure $\lambda$ that is Lebesgue measure on each piece. $\pi$ is a probability density on $\mathcal{X}$ with respect to $\lambda$, and $\tilde\pi = Z\pi$. For $k < K$, $g = g_k$ is a positive density on $\mathbb{R}^r$ with $d_k + r = d_{k+1}$, and $h = h_k$ is a $C^1$ bijection from an open set $U \subseteq \mathbb{R}^{d_k} \times \mathbb{R}^r$ onto an open set $V \subseteq \mathbb{R}^{d_{k+1}}$ that contains $\{\theta' : \pi(k + 1, \theta') > 0\}$, with a $C^1$ inverse. Let $J(\theta, u) = |\det\nabla h(\theta, u)|$, which is positive on $U$. Proposals $(\theta, u) \notin U$ have ratio 0 and are rejected.

**Step 1: the acceptance probabilities.** Line L5 gives, for $(\theta, u) \in U$ and $\theta' = h(\theta, u)$, the up acceptance probability

$$a(\theta, u) = \min\Big(1, \frac{\pi(k + 1, \theta')J(\theta, u)}{\pi(k, \theta)g(u)}\Big).$$

Line L7 gives, for $\theta' \in V$ and $(\theta, u) = h^{-1}(\theta')$, the down acceptance probability $b(\theta') = \min\big(1, \pi(k, \theta)g(u)/(\pi(k + 1, \theta')J(\theta, u))\big)$. The constant $Z$ cancels in both. Whenever both sides are defined,

$$\pi(k, \theta)g(u)\,a(\theta, u) = \min\big(\pi(k, \theta)g(u),\ \pi(k + 1, \theta')J(\theta, u)\big) = \pi(k + 1, \theta')J(\theta, u)\,b(\theta'). \tag{1}$$

**Step 2: the flows between two models.** Let $A \subseteq \mathbb{R}^{d_k}$ and $B \subseteq \mathbb{R}^{d_{k+1}}$ be Borel sets. A jump from $\{k\} \times A$ into $\{k + 1\} \times B$ happens when the move type is up (probability $\frac14$), $u$ is drawn from $g$, and the proposal $h(\theta, u) \in B$ is accepted. In stationarity its probability is

$$F_\uparrow = \frac14\int_U\mathbf 1[\theta \in A]\,\mathbf 1[h(\theta, u) \in B]\,\pi(k, \theta)g(u)a(\theta, u)\,d\theta\,du.$$

By (1), the integrand equals $\mathbf 1[\theta \in A]\mathbf 1[h(\theta, u) \in B]\,\pi(k + 1, h(\theta, u))\,b(h(\theta, u))\,J(\theta, u)$. The change of variables theorem for the $C^1$ bijection $h : U \to V$ says that $\int_UF(h(\theta, u))J(\theta, u)\,d\theta\,du = \int_VF(\theta')\,d\theta'$ for every measurable $F \ge 0$. Apply it with $F(\theta') = \mathbf 1[\theta' \in B]\mathbf 1[\mathrm{pr}(h^{-1}(\theta')) \in A]\pi(k + 1, \theta')b(\theta')$, where $\mathrm{pr}$ keeps the $\theta$ part:

$$F_\uparrow = \frac14\int_V\mathbf 1[\theta' \in B]\,\mathbf 1[\mathrm{pr}(h^{-1}(\theta')) \in A]\,\pi(k + 1, \theta')b(\theta')\,d\theta'.$$

This is the probability, in stationarity, that the chain is in $\{k + 1\} \times B$, chooses the down move (probability $\frac14$), and accepts a down proposal that lands in $\{k\} \times A$. So $F_\uparrow = F_\downarrow$. Without the factor $J$ in line L5, (1) would hold with $J$ missing on the right, and the change of variables would leave a factor $1/J$ in the last integral, so the two flows would differ unless $J = 1$.

**Step 3: all moves.** The kernel of one step is a mixture with weights $\frac12, \frac14, \frac14$ of three kernels: the move inside the model, the up move and the down move, where a move out of the model range and a rejected proposal both keep the state. The move inside the model keeps $\pi(k, \cdot)$ for each $k$, so it keeps $\pi$. If $P_k$ is also reversible, it satisfies detailed balance. Step 2 shows that the jumps, taken together as the kernel $\frac12(\text{up}) + \frac12(\text{down})$, satisfy detailed balance between every pair of sets in neighbour models. Jumps between models that are not neighbours have probability 0 in both directions. The part of the jump kernel that keeps the state is symmetric by itself. So the jump kernel is reversible with respect to $\pi$, and in particular it keeps $\pi$. A mixture of kernels that keep $\pi$ keeps $\pi$, so $\pi$ is stationary. $\blacksquare$

**Remark.** The argument does not use the specific move probabilities. With general $j(k \to k')$, the factor $j(k' \to k)/j(k \to k')$ enters (1) and cancels in the same way. With a density $g'$ of extra variables $u'$ for the reverse move as well, dimension matching becomes $d_k + r = d_{k'} + r'$, $h$ maps $(\theta, u)$ to $(\theta', u')$, and the same change of variables applies with $g(u)$ and $g'(u')$ on the two sides.
