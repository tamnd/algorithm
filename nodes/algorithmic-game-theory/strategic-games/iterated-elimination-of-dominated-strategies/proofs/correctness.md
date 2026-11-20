---
title: Iterated strict dominance stops, keeps every Nash equilibrium, adds none, and does not depend on the order
proves: [correctness]
status: full
---

Let $G$ be a finite game with players $1, \ldots, n$, pure strategy sets $S_i$ and utilities $u_i$, which the players maximize. For a product $Y = Y_1 \times \cdots \times Y_n$ of subsets $Y_i \subseteq S_i$, a strategy $a \in Y_i$ is *strictly dominated relative to $Y$* if some mixed strategy $\tau$ on $Y_i$ has $u_i(\tau, t) > u_i(a, t)$ for every $t \in Y_{-i}$, where $u_i(\tau, t) = \sum_b \tau(b)\, u_i(b, t)$. The pure test of line L4 is the case where $\tau$ puts weight 1 on one strategy. Every claim below holds for both tests; where the two proofs differ, both are given.

**A removed strategy has a dominator that puts no weight on it.** If $\tau$ dominates $a$ and $\tau(a) = p > 0$, then $p < 1$, since $\tau = a$ would give $u_i(a, t) > u_i(a, t)$. Let $\rho = (\tau - p\,a)/(1 - p)$, a mixed strategy on $Y_i$ minus $\{a\}$. For every $t \in Y_{-i}$, $p\,u_i(a, t) + (1 - p)\,u_i(\rho, t) = u_i(\tau, t) > u_i(a, t)$, so $u_i(\rho, t) > u_i(a, t)$. So from now on each dominator of $a$ puts weight 0 on $a$; the code builds its witness this way.

## Termination and the exit condition

Let $\Phi = \sum_i |A_i|$. Line L1 sets $\Phi = \sum_i |S_i|$. Each pass through line L5 lowers $\Phi$ by exactly 1. A strategy $a$ that is alone in $A_i$ is never dominated, because its only possible dominator is $a$ itself, which was excluded above. So every $A_i$ stays nonempty, $\Phi \ge n$ at all times, and line L5 runs at most $\sum_i |S_i| - n$ times. Between two passes through line L5, the scan of line L3 makes at most $\sum_i |A_i|$ calls. So the procedure stops. It stops only at line L7, after a full scan in which no call of line L4 returned a witness, so no strategy of the result $A$ is strictly dominated relative to $A$.

## No removed strategy is used by a Nash equilibrium

Let $\sigma^*$ be a mixed Nash equilibrium of $G$. We show by induction on the number of removals that the support of every $\sigma^*_j$ stays inside $A_j$. At line L1, $A_j = S_j$. Suppose the claim holds before line L5 removes $a$ from $A_i$, with dominator $\tau$ relative to $A$. By the induction hypothesis, $\sigma^*_{-i}$ puts all its weight on profiles $t \in A_{-i}$, and so

$$u_i(\tau, \sigma^*_{-i}) = \sum_{t \in A_{-i}} \sigma^*_{-i}(t)\, u_i(\tau, t) > \sum_{t \in A_{-i}} \sigma^*_{-i}(t)\, u_i(a, t) = u_i(a, \sigma^*_{-i}),$$

where the inequality is strict because the weights $\sigma^*_{-i}(t)$ are nonnegative and sum to 1, and each term on the left is larger. Since $u_i(\tau, \sigma^*_{-i})$ is an average of the values $u_i(b, \sigma^*_{-i})$ with $b \in A_i$, some pure $b$ has $u_i(b, \sigma^*_{-i}) > u_i(a, \sigma^*_{-i})$. So $a$ is not a pure best response to $\sigma^*_{-i}$. In an equilibrium every strategy in the support of $\sigma^*_i$ is a pure best response to $\sigma^*_{-i}$ (if a strategy $a$ with $\sigma^*_i(a) > 0$ were not, moving its weight to a best response would raise $u_i$). So $\sigma^*_i(a) = 0$, and the claim holds after the removal.

## A lemma: pushing a dominator into the surviving sets

Fix one run of the procedure. Number its removals $1, 2, \ldots, r$ in order, and let $A$ be its result. For a removed strategy $b$ of player $i$, let $\mathrm{time}(b)$ be its number, and let $\tau_b$ be its witness; $\tau_b$ is a mixed strategy on the set $Z_i$ alive at that time, with weight 0 on $b$, and it dominates $b$ relative to $Z \supseteq A$.

**Lemma.** Let $X \subseteq A_{-i}$ be a set of profiles of the others, and let $\sigma$ be a mixed strategy of player $i$ on $S_i$. Then there is a mixed strategy $\sigma'$ on $A_i$ with $u_i(\sigma', t) \ge u_i(\sigma, t)$ for every $t \in X$, and with strict inequality for every $t \in X$ if $\sigma$ puts positive weight outside $A_i$.

*Proof.* If the support of $\sigma$ is inside $A_i$, take $\sigma' = \sigma$. Otherwise let $b$ be the strategy outside $A_i$ in the support of $\sigma$ with the smallest $\mathrm{time}(b)$, and let $\hat\sigma = \sigma - \sigma(b)\, b + \sigma(b)\, \tau_b$. This is a mixed strategy. For each $t \in X$, $t \in A_{-i} \subseteq Z_{-i}$, so $u_i(\tau_b, t) > u_i(b, t)$ and $u_i(\hat\sigma, t) = u_i(\sigma, t) + \sigma(b)\,(u_i(\tau_b, t) - u_i(b, t)) > u_i(\sigma, t)$. The support of $\tau_b$ is inside $Z_i$, the set alive at time $\mathrm{time}(b)$, and does not contain $b$. So every strategy outside $A_i$ in the support of $\hat\sigma$ was removed strictly after $b$: those from $\tau_b$ because they were still alive when $b$ was removed, and the others from $\sigma$ by the choice of $b$. The smallest removal time outside $A_i$ in the support therefore grows by at least 1 at each step, and it is at most $r$, so after at most $r$ steps the support is inside $A_i$. Each step raised the payoff strictly against every $t \in X$, which gives the lemma. For the pure test, each $\tau_b$ is pure, $\sigma$ stays pure at every step, and $\sigma'$ is pure. $\square$

## Every equilibrium of the reduced game is an equilibrium of G

Let $\sigma$ be a mixed Nash equilibrium of the game restricted to $A$, so each $\sigma_j$ lives on $A_j$ and no deviation inside $A_i$ gains. Suppose some $b \in S_i$ minus $A_i$ had $u_i(b, \sigma_{-i}) > u_i(\sigma)$. Apply the lemma to the pure strategy $b$ with $X = A_{-i}$: it gives $\sigma'$ on $A_i$ with $u_i(\sigma', t) > u_i(b, t)$ for every $t \in A_{-i}$, so $u_i(\sigma', \sigma_{-i}) > u_i(b, \sigma_{-i}) > u_i(\sigma)$. That is a gain inside $A_i$, which contradicts the choice of $\sigma$. So no pure deviation of $G$ gains, and $\sigma$ is a Nash equilibrium of $G$.

Together with the previous section: the Nash equilibria of $G$ are exactly the Nash equilibria of the game restricted to $A$.

## The result does not depend on the order

Take two runs, with results $A$ and $B$. Let the second run remove $c_1, c_2, \ldots$ in this order, where $c_j$ belongs to player $i_j$ and is strictly dominated relative to the set $Y^j$ alive before its removal. We show by induction on $j$ that no $c_j$ lies in $A$.

Suppose $c_1, \ldots, c_{j-1}$ are not in $A$. Then $A \subseteq Y^j$, since $Y^j$ is $S$ minus these strategies. Suppose $c = c_j$ were in $A_i$, with $i = i_j$. Its dominator $\sigma$ in the second run satisfies $u_i(\sigma, t) > u_i(c, t)$ for every $t \in Y^j_{-i}$, and so for every $t \in A_{-i}$. The lemma for the first run with $X = A_{-i}$ gives $\sigma'$ on $A_i$ with $u_i(\sigma', t) \ge u_i(\sigma, t) > u_i(c, t)$ for every $t \in A_{-i}$. Then $c$ is strictly dominated relative to $A$ (by a pure strategy for the pure test, by the last sentence of the lemma), which contradicts the exit condition of the first run. So $c_j \notin A$.

Hence every strategy that the second run removes is outside $A$, which means $A \subseteq B$. Swapping the two runs gives $B \subseteq A$. So $A = B$. $\blacksquare$

## Weak dominance

For weak dominance by a pure strategy, termination and the exit condition hold with the same proof. The section on equilibria of $G$ fails: in the first order of the example of the page, the equilibrium (T, L) is removed. The section on the reduced game still holds with weak inequalities: the lemma, with $\ge$ in place of $>$, gives $u_i(\sigma', \sigma_{-i}) \ge u_i(b, \sigma_{-i}) > u_i(\sigma)$ for a gaining $b$, the same contradiction. So every equilibrium of the reduced game is an equilibrium of $G$, and since the reduced game is finite, [Nash's theorem](/nash-existence-theorem/) gives it an equilibrium: at least one equilibrium of $G$ survives every order. The order section fails, because the step "$u_i(\sigma', t) \ge u_i(\sigma, t) \ge u_i(c, t)$ with one strict" does not transfer from $Y^j_{-i}$ to the smaller set $A_{-i}$: the profile with the strict inequality may be gone.
