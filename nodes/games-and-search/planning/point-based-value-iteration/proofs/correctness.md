---
title: The point backup is the Bellman backup at the point, PBVI values are lower bounds, and PBVI is exact at b0 with all reachable beliefs
proves: [correctness]
status: full
---

We use the pseudocode of the page. For a vector $\alpha \in \mathbb{R}^S$, an action $a$ and an observation $o$, let

$$g^\alpha_{a,o}(s) = \sum_{s'} P(s' \mid s, a) \, O(o \mid a, s') \, \alpha(s').$$

For a finite set $\Gamma$ of vectors, write $V_\Gamma(b) = \max_{\alpha \in \Gamma} \alpha \cdot b$, and let $H$ be the Bellman backup of the belief MDP,

$$(H V)(b) = \max_a \Big[ R_a \cdot b + \gamma \sum_o \Pr(o \mid b, a) \, V(b^{a,o}) \Big],$$

where $R_a(s) = R(s, a)$.

**Lemma 1 (the point backup is exact at its point).** Let $\beta = \text{BACKUP}(\Gamma, b)$. Then $\beta \cdot b = (H V_\Gamma)(b)$.

*Proof.* From the belief update, $\Pr(o \mid b, a) \, b^{a,o}(s') = O(o \mid a, s') \sum_s P(s' \mid s, a) b(s)$. So for each $\alpha$,

$$\Pr(o \mid b, a) \, \alpha \cdot b^{a,o} = \sum_s b(s) \sum_{s'} P(s' \mid s, a) O(o \mid a, s') \alpha(s') = g^\alpha_{a,o} \cdot b.$$

This also holds when $\Pr(o \mid b, a) = 0$, since then both sides are 0. Taking the maximum over $\alpha \in \Gamma$ gives $\Pr(o \mid b, a) V_\Gamma(b^{a,o}) = \max_{\alpha} g^\alpha_{a,o} \cdot b$, and line L6 picks a vector $g_{a,o}$ that attains this maximum. The vector $\alpha_a$ of line L7 has $\alpha_a \cdot b = R_a \cdot b + \gamma \sum_o \max_\alpha g^\alpha_{a,o} \cdot b$, which is the bracket of $H V_\Gamma$ for the action $a$. Line L8 takes the maximum over $a$. $\square$

So a point backup costs the same work at $b$ as an exact backup at $b$, but it returns one vector, not a whole set.

**Lemma 2 (each vector is the value of a plan).** Suppose that each vector of $\Gamma$ is the value vector of some policy $p_\alpha$ that acts on the actions and observations only: $\alpha(s)$ is the expected total reward of $p_\alpha$ when the state is $s$ at the start. Then each vector that BACKUP returns is the value vector of a policy: do $a$, then after the observation $o$ follow $p_{\alpha_o}$, where $\alpha_o$ is the vector with $g_{a,o} = g^{\alpha_o}_{a,o}$.

*Proof.* Start in the state $s$. The first reward is $R(s, a)$. The next state is $s'$ with probability $P(s' \mid s, a)$, and then $o$ comes with probability $O(o \mid a, s')$. After that the policy $p_{\alpha_o}$ runs from the state $s'$, with expected reward $\alpha_o(s')$. The expected total is $R(s, a) + \gamma \sum_o \sum_{s'} P(s' \mid s, a) O(o \mid a, s') \alpha_o(s') = R(s, a) + \gamma \sum_o g^{\alpha_o}_{a,o}(s)$, the vector of line L7. $\square$

**Theorem 1 (lower bound).** For a finite horizon, start PBVI from $\Gamma_0 = \{0\}$. After $k$ sweeps, every vector of $\Gamma_k$ is the value vector of a policy tree of depth $k$, and $V_{\Gamma_k} \le V_k$ on the whole simplex. For a discounted problem, start from $\Gamma_0 = \{\alpha_{\min}\}$ with $\alpha_{\min}(s) = R_{\min} / (1 - \gamma)$. Then $V_{\Gamma_k} \le V^*$ for every $k$.

*Proof.* The zero vector is the value of the empty tree, so the first claim follows from Lemma 2 by induction on $k$. The value of a policy tree $p$ at $b$ is $\alpha_p \cdot b$, and $V_k(b)$ is the maximum of this over all trees of depth $k$. So $V_{\Gamma_k} \le V_k$.

For the discounted case, $\alpha_{\min}(s)$ is at most the value of any policy from $s$, since each reward is at least $R_{\min}$. Lemma 2 with "at most" in place of "equal" goes through, because the weights $P$ and $O$ are nonnegative: if $\alpha \le$ the value of $p_\alpha$ for each $\alpha \in \Gamma$, then each new vector is at most the value of the composed policy. Each such value is at most $V^*$. $\square$

**Theorem 2 (exact at the start belief).** Take a finite horizon $H$ and $\Gamma_0 = \{0\}$. Let $B$ contain every belief that $b_0$ reaches with positive probability in fewer than $H$ steps. After $H$ sweeps over $B$, $V_{\Gamma_H}(b_0) = V_H(b_0)$.

*Proof.* We show by induction on $k$ that $V_{\Gamma_k}(b) = V_k(b)$ for every $b$ that $b_0$ reaches in exactly $H - k$ steps. For $k = 0$ both sides are 0. Let $k \ge 1$ and let $b$ be reached in $H - k$ steps. Then $b \in B$, and the sweep $k$ adds $\beta = \text{BACKUP}(\Gamma_{k-1}, b)$ to $\Gamma_k$. By Lemma 1, $\beta \cdot b = (H V_{\Gamma_{k-1}})(b)$. In this backup, $V_{\Gamma_{k-1}}$ is used only at the beliefs $b^{a,o}$ with $\Pr(o \mid b, a) > 0$, which are reached in $H - k + 1$ steps, so $V_{\Gamma_{k-1}} = V_{k-1}$ there by induction. Hence $\beta \cdot b = (H V_{k-1})(b) = V_k(b)$, and $V_{\Gamma_k}(b) \ge V_k(b)$. Theorem 1 gives $V_{\Gamma_k}(b) \le V_k(b)$. With $k = H$ and $b = b_0$ the claim follows. $\square$

**The error bound.** Pineau, Gordon and Thrun (2006, Section 3) prove a bound for the discounted case with a fixed set $B$. Let $\delta_B$ be the largest L1 distance from a reachable belief to the nearest point of $B$. Then the error of the PBVI value after convergence, on the reachable beliefs, is at most $(R_{\max} - R_{\min}) \, \delta_B / (1 - \gamma)^2$. The idea is that an alpha vector has entries in $[R_{\min}/(1-\gamma), R_{\max}/(1-\gamma)]$, so the vector chosen at the nearest point of $B$ loses at most a multiple of $\delta_B / (1 - \gamma)$ at each backup, and these losses add up with the factor $1/(1 - \gamma)$.
