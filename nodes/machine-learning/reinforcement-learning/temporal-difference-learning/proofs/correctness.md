---
title: Tabular TD(0) converges to V^pi, and batch TD(0) converges to the certainty-equivalence estimate
proves: [correctness, termination]
status: full
---

We use the notation of the page: a finite MDP, a fixed policy $\pi$, $0 \le \gamma < 1$, bounded rewards $|R_{t+1}| \le R_{\max}$, and the max norm $\lVert U \rVert = \max_s |U(s)|$. Write $(T^\pi U)(s) = \mathbb{E}_\pi[R_{t+1} + \gamma U(S_{t+1}) \mid S_t = s]$ and $r^\pi(s) = \mathbb{E}_\pi[R_{t+1} \mid S_t = s]$.

**Termination.** Lines L2 to L6 run $T$ times for an episode of $T$ steps, and line L1 runs once per episode. So TD0 stops on any finite list of episodes. $\square$

**Lemma 1 (the expected TD error is the Bellman residual).** For any fixed table $V$ and any state $s$, $\mathbb{E}_\pi[\delta_t \mid S_t = s, \text{past}] = (T^\pi V)(s) - V(s)$, where $\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(s)$.

*Proof.* By the Markov property, given $S_t = s$ the pair $(R_{t+1}, S_{t+1})$ has the law of one step of $\pi$ from $s$, whatever the past. Take the expectation of $\delta_t$ and use the definition of $T^\pi$. $\square$

**Lemma 2 (the unique zero).** The expected update vanishes in every state, $T^\pi V = V$, exactly when $V = V^\pi$.

*Proof.* $T^\pi$ is a $\gamma$-contraction in the max norm, since for each $s$, $|(T^\pi U)(s) - (T^\pi W)(s)| = \gamma |\mathbb{E}[U(S_{t+1}) - W(S_{t+1}) \mid S_t = s]| \le \gamma \lVert U - W \rVert$. By the Banach fixed point theorem it has exactly one fixed point, and $V^\pi$ is a fixed point by the [Bellman expectation equation](/bellman-expectation-equation/). $\square$

**The stochastic approximation lemma.** We use the following theorem without proof. It is the main lemma of Jaakkola, Jordan and Singh (1994) and a case of the results in Bertsekas and Tsitsiklis (1996, Chapter 4); the [stochastic approximation](/stochastic-approximation/) page discusses it. Let $X$ be a finite set and let

$$\Delta_{t+1}(x) = (1 - \alpha_t(x))\, \Delta_t(x) + \alpha_t(x)\, F_t(x), \qquad x \in X,$$

where $\alpha_t$, $\Delta_t$ and the past are known at time $t$ (they generate the history $\mathcal{F}_t$). Suppose that, with probability 1: (a) $0 \le \alpha_t(x) \le 1$, $\sum_t \alpha_t(x) = \infty$ and $\sum_t \alpha_t(x)^2 < \infty$ for each $x$; (b) $|\mathbb{E}[F_t(x) \mid \mathcal{F}_t]| \le \kappa \lVert \Delta_t \rVert$ for a constant $\kappa < 1$, whenever $\alpha_t(x) > 0$; (c) $\mathrm{Var}[F_t(x) \mid \mathcal{F}_t] \le C(1 + \lVert \Delta_t \rVert)^2$ for a constant $C$. Then $\Delta_t \to 0$ with probability 1.

**Theorem 1 (convergence with probability 1).** Run TD(0) on the stream of transitions of $\pi$. Let the step of the update at time $t$ be $\alpha_t(S_t)$, and set $\alpha_t(x) = 0$ for $x \ne S_t$. If each state is updated infinitely often and the steps of each state meet $\sum_t \alpha_t(x) = \infty$ and $\sum_t \alpha_t(x)^2 < \infty$, with $\alpha_t(x) \le 1$, then $V_t \to V^\pi$ with probability 1.

*Proof.* Let $\Delta_t = V_t - V^\pi$. Line L6 changes only the entry $x = S_t$, and

$$\Delta_{t+1}(x) = V_t(x) + \alpha_t(x)\big(R_{t+1} + \gamma V_t(S_{t+1}) - V_t(x)\big) - V^\pi(x) = (1 - \alpha_t(x))\Delta_t(x) + \alpha_t(x) F_t(x)$$

with $F_t(x) = R_{t+1} + \gamma V_t(S_{t+1}) - V^\pi(x)$. For $x \ne S_t$, $\alpha_t(x) = 0$ and the same identity holds with any $F_t(x)$; put $F_t(x) = 0$ there. Condition (a) is the hypothesis. For (b), by Lemma 1 with the table $V_t$, which is known at time $t$,

$$\mathbb{E}[F_t(x) \mid \mathcal{F}_t] = (T^\pi V_t)(x) - V^\pi(x) = (T^\pi V_t)(x) - (T^\pi V^\pi)(x),$$

whose absolute value is at most $\gamma \lVert V_t - V^\pi \rVert = \gamma \lVert \Delta_t \rVert$ by Lemma 2. So (b) holds with $\kappa = \gamma < 1$. For (c), $|F_t(x)| \le R_{\max} + \gamma(\lVert V^\pi \rVert + \lVert \Delta_t \rVert) + \lVert V^\pi \rVert$, so the conditional variance is at most the square of this bound, which is at most $C(1 + \lVert \Delta_t \rVert)^2$ with $C = (R_{\max} + 2\lVert V^\pi \rVert + 1)^2$. The lemma gives $\Delta_t \to 0$ with probability 1. $\square$

For episodic tasks with $\gamma = 1$ the same argument works in a weighted max norm in which $T^\pi$ is a contraction, which exists when every episode ends with probability 1 (Bertsekas and Tsitsiklis 1996, Chapter 2, stochastic shortest paths). Treat the episodes as one stream in which the terminal step restarts the episode.

**Theorem 2 (the batch fixed point).** Fix a batch of episodes. For each state $s$ that occurs in it, let $n_s$ be the number of steps taken from $s$, $\hat r(s)$ the mean reward of these steps, and $\hat P(s' \mid s)$ the fraction of them that go to $s'$ (steps into the terminal state go to no $s'$). Then the summed batch increment is zero for every state exactly when $V = \hat r + \gamma \hat P V$, the Bellman equation of the maximum likelihood model. If $\gamma < 1$ and $0 < \alpha \le 1/\max_s n_s$, batch TD(0) converges to its unique solution.

*Proof.* The summed increment of state $s$ is

$$\alpha \sum_{\text{steps } (s, r, s')} \big(r + \gamma V(s') - V(s)\big) = \alpha\, n_s \Big(\hat r(s) + \gamma \sum_{s'} \hat P(s' \mid s) V(s') - V(s)\Big),$$

with $V(s') = 0$ for the terminal state. Since $n_s > 0$, all increments vanish exactly when $V = \hat r + \gamma \hat P V$. One sweep maps $V$ to $MV + \alpha N \hat r$ with $N = \mathrm{diag}(n_s)$ and $M = (I - \alpha N) + \alpha \gamma N \hat P$. When $\alpha n_s \le 1$, the entries of $M$ are nonnegative, and row $s$ sums to $1 - \alpha n_s + \alpha \gamma n_s \sum_{s'} \hat P(s' \mid s) \le 1 - \alpha n_s (1 - \gamma) \le 1 - \alpha (1-\gamma) \min_s n_s < 1$. A nonnegative matrix with row sums at most $\beta < 1$ is a $\beta$-contraction in the max norm. So the sweeps converge geometrically to the unique fixed point, which is the solution above. $\blacksquare$
