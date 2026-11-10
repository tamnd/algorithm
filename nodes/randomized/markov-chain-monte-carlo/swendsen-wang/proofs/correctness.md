---
title: Swendsen-Wang is a two-block Gibbs sampler on the Edwards-Sokal measure, so it is reversible with respect to the Potts law
proves: [correctness]
status: full
---

**Setting.** $G = (V, E)$ is a finite graph with $|E| = m$, $q \ge 2$ is an integer, $J > 0$ and $p = 1 - e^{-J} \in (0, 1)$. For a colouring $\sigma \in \Omega = \{1, \dots, q\}^V$ let $a(\sigma)$ be the number of edges whose two ends have the same colour, so that the Potts law is $\pi(\sigma) = e^{Ja(\sigma)}/Z$. For $A \subseteq E$ let $c(A)$ be the number of connected components of $(V, A)$, and say that $\sigma$ is compatible with $A$, written $\sigma \sim A$, if $\sigma$ is constant on every edge of $A$. The Edwards-Sokal weight is

$$w(\sigma, A) = p^{|A|}(1 - p)^{m - |A|}\,\mathbf 1[\sigma \sim A],$$

and $\mu = w/W$ with $W = \sum_{\sigma, A}w(\sigma, A)$.

**Step 1: the spin marginal is the Potts law.** Fix $\sigma$, and let $E_=(\sigma)$ be the set of edges with equal ends. The condition $\sigma \sim A$ means $A \subseteq E_=(\sigma)$. So

$$\sum_Aw(\sigma, A) = \prod_{e \in E_=(\sigma)}\big(p + (1 - p)\big)\prod_{e \notin E_=(\sigma)}(1 - p) = (1 - p)^{m - a(\sigma)} = e^{-Jm}e^{Ja(\sigma)},$$

since $1 - p = e^{-J}$. The factor $e^{-Jm}$ does not depend on $\sigma$, so $\sum_A\mu(\sigma, A) = \pi(\sigma)$.

**Step 2: the bond marginal is the random-cluster law.** Fix $A$. A colouring is compatible with $A$ if and only if it is constant on each component of $(V, A)$, and there are $q^{c(A)}$ such colourings. So $\sum_\sigma w(\sigma, A) = p^{|A|}(1 - p)^{m - |A|}q^{c(A)}$.

**Step 3: the bonds given the spins (line L3).** By Step 1, for fixed $\sigma$,

$$\mu(A \mid \sigma) = \frac{w(\sigma, A)}{\sum_{A'}w(\sigma, A')} = \mathbf 1[A \subseteq E_=(\sigma)]\prod_{e \in A}p\prod_{e \in E_=(\sigma) \setminus A}(1 - p).$$

This is the law of a set that contains each edge of $E_=(\sigma)$ independently with probability $p$ and no other edge, which is what line L3 draws.

**Step 4: the spins given the bonds (lines L4 to L6).** By Step 2, for fixed $A$, $\mu(\sigma \mid A) = \mathbf 1[\sigma \sim A]/q^{c(A)}$, the uniform law on the colourings that are constant on each component. Lines L4 to L6 give each component an independent uniform colour, which is a uniform draw from exactly this set.

**Step 5: reversibility.** By Steps 3 and 4, one update maps $\sigma$ to $\sigma'$ with probability

$$P(\sigma, \sigma') = \sum_A\mu(A \mid \sigma)\,\mu(\sigma' \mid A).$$

Multiply by $\pi(\sigma) = \mu(\sigma)$ and use $\mu(\sigma)\mu(A \mid \sigma) = \mu(\sigma, A) = \mu(A)\mu(\sigma \mid A)$:

$$\pi(\sigma)P(\sigma, \sigma') = \sum_A\mu(A)\,\mu(\sigma \mid A)\,\mu(\sigma' \mid A),$$

which is symmetric in $\sigma$ and $\sigma'$. So $P$ satisfies detailed balance with respect to $\pi$, and summing over $\sigma$ shows that $\pi$ is stationary.

**Step 6: convergence.** For every $\sigma$, the empty bond set has probability $(1 - p)^{a(\sigma)} > 0$ in line L3, and then each of the $q^n$ colourings has probability $q^{-n}$ in lines L4 to L6. So $P(\sigma, \sigma') \ge (1 - p)^mq^{-n} > 0$ for all $\sigma, \sigma'$. A finite chain with all entries positive is irreducible and aperiodic, so its law converges to $\pi$ from every start. The same bound gives a Doeblin condition: the total variation distance to $\pi$ after $t$ updates is at most $(1 - q^{-n}(1 - p)^m)^t$, which is a valid but very weak bound. $\blacksquare$

**Remark.** If $J < 0$, then $p < 0$ and $w$ is not a weight, so the argument does not apply to antiferromagnets. If $p = 0$, then every vertex is its own cluster, the update draws a uniform colouring, and $\pi$ is the uniform law, so the theorem still holds.
