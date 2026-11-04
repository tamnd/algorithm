---
title: The stable fraction of zero cells
proves: [complexity]
status: full
---

**Model.** At each step $t$, the set $H(x_t)$ is a uniform random $K$-subset of the $m$ cells and $V_t$ is a uniform random $P$-subset, and all these sets are independent. This holds under ideal hashing for a stream of distinct elements. Assume $1 \le K < m$ and $P \ge 1$.

**Theorem 1.** For each cell $j$,
$$ \lim_{t \to \infty} \Pr[C_t[j] = 0] = q^{\mathrm{Max}}, \qquad q = \frac{1}{1 + \frac{1}{P(1/K - 1/m)}}. $$

*Proof.* Fix $j$. At each step $s$, let $A_s$ be the event $j \in H(x_s)$, a *set*, and $B_s$ the event $j \in V_s$ and $j \notin H(x_s)$, a *pure decrement*. Then $\Pr[A_s] = a = K/m$ and, by the independence of $H(x_s)$ and $V_s$, $\Pr[B_s] = b = (P/m)(1 - K/m)$. Steps are independent.

By the invariant (D) of the correctness proof, $C_t[j] = 0$ exactly when either no step $s \le t$ is a set, or the last set $\tau$ is followed by at least Max pure decrements in the steps $\tau + 1, \ldots, t$ (a step that is both a set and a decrement counts as a set, since line L4 runs after line L3).

Look at the steps $t, t - 1, \ldots, 1$ in this order, and keep only the *relevant* steps, those that are a set or a pure decrement. Since the steps are independent and identically distributed, each relevant step is, independently of the others, a pure decrement with probability
$$ \frac{b}{a + b} = \frac{P(1 - K/m)}{K + P(1 - K/m)} = \frac{1}{1 + \frac{K}{P(1 - K/m)}} = \frac{1}{1 + \frac{1}{P(1/K - 1/m)}} = q, $$
and a set otherwise. The cell is 0 at time $t$ if and only if the first Max relevant steps in this backward order are all pure decrements, or there are fewer than Max relevant steps and none is a set.

Let $R_t$ be the number of relevant steps among $1, \ldots, t$. Given $R_t = \rho \ge \mathrm{Max}$, the first event has probability exactly $q^{\mathrm{Max}}$ and the second is impossible. So
$$ \big|\Pr[C_t[j] = 0] - q^{\mathrm{Max}}\big| \le \Pr[R_t < \mathrm{Max}]. $$
Each step is relevant with probability $a + b \ge K/m > 0$, independently, so $\Pr[R_t < \mathrm{Max}] \to 0$ as $t \to \infty$. $\square$

**Theorem 2 (time and space).** PROCESS takes $\Theta(K + P)$ time, given $\Theta(1)$ time for each random cell and each hash value, and the array has $m d$ bits.

*Proof.* Line L2 reads $K$ cells, line L3 chooses and updates $P$ cells, and line L4 writes $K$ cells. $\blacksquare$
