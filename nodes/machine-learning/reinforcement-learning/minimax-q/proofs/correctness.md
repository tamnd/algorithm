---
title: What is proved about minimax-Q
proves: [correctness]
status: full
---

Notation is that of the page. The game is finite and discounted with $0 \le \gamma < 1$, and rewards are bounded. For a matrix $M$ with rows indexed by $A$ and columns by $O$,

$$\operatorname{val} M = \max_{x \in \Delta(A)} \min_{y \in \Delta(O)} x^\top M y = \min_{y \in \Delta(O)} \max_{x \in \Delta(A)} x^\top M y,$$

where the two forms are equal by the [minimax theorem](/minimax-theorem/). The minimum over mixed $y$ of the linear function $x^\top M y$ is attained at a pure column, so $\operatorname{val} M = \max_x \min_o \sum_a x(a) M[a, o]$, which is the linear program of line L6. For $Q : S \times A \times O \to \mathbb{R}$, write $Q(s)$ for the matrix $Q(s, \cdot, \cdot)$.

## Claim 1 (val is 1-Lipschitz)

For matrices $M$ and $M'$ of the same size, $|\operatorname{val} M - \operatorname{val} M'| \le \|M - M'\|_\infty = \max_{a, o} |M[a, o] - M'[a, o]|$.

*Proof.* Let $c = \|M - M'\|_\infty$. For probability vectors $x$ and $y$, $|x^\top (M - M') y| \le \sum_{a, o} x(a) y(o) c = c$. So $x^\top M y \le x^\top M' y + c$ for all $x, y$. Taking $\min_y$ and then $\max_x$ keeps the inequality, so $\operatorname{val} M \le \operatorname{val} M' + c$. Swap $M$ and $M'$. $\square$

The function $\operatorname{val}$ is also monotone ($M \le M'$ entrywise gives $\operatorname{val} M \le \operatorname{val} M'$) and $\operatorname{val}(M + c\mathbf{1}) = \operatorname{val} M + c$, by the same argument.

## Claim 2 (the minimax Bellman operator)

Let $(HQ)(s, a, o) = R(s, a, o) + \gamma \sum_{s'} P(s' \mid s, a, o) \operatorname{val} Q(s')$. Then $H$ is a $\gamma$-contraction in the max norm, and its unique fixed point is $Q^*(s, a, o) = R(s, a, o) + \gamma \sum_{s'} P(s' \mid s, a, o) v^*(s')$, where $v^*$ is the value of the game.

*Proof.* For $Q$ and $Q'$,

$$|(HQ)(s, a, o) - (HQ')(s, a, o)| \le \gamma \sum_{s'} P(s' \mid s, a, o)\, |\operatorname{val} Q(s') - \operatorname{val} Q'(s')| \le \gamma \|Q - Q'\|_\infty$$

by Claim 1, since $\|Q(s') - Q'(s')\|_\infty \le \|Q - Q'\|_\infty$. By the Banach fixed point theorem $H$ has one fixed point. By Shapley's theorem (proved on the [Markov game](/markov-game/) page), $v^*$ is the unique fixed point of $v \mapsto \operatorname{val} M_s(v)$ with $M_s(v)[a, o] = R(s, a, o) + \gamma \sum_{s'} P(s' \mid s, a, o) v(s')$. Define $Q^*$ from $v^*$ as above; then $Q^*(s) = M_s(v^*)$, so $\operatorname{val} Q^*(s) = v^*(s)$, and $HQ^* = Q^*$. $\square$

## Claim 3 (convergence)

Assume: every triple $(s, a, o)$ is updated infinitely often with probability 1; the step size $\alpha_n(s, a, o)$ of the $n$-th update of that triple satisfies $\sum_n \alpha_n = \infty$ and $\sum_n \alpha_n^2 < \infty$; rewards have bounded variance. Then $Q_t \to Q^*$ with probability 1.

*Proof.* Line L5 is

$$Q_{t+1}(s, a, o) = (1 - \alpha_t) Q_t(s, a, o) + \alpha_t \big((HQ_t)(s, a, o) + w_t\big), \qquad w_t = r + \gamma \operatorname{val} Q_t(s') - (HQ_t)(s, a, o),$$

for the visited triple, and leaves the others unchanged. Given the past, $w_t$ has mean zero, because $r$ and $s'$ are drawn from $R(s, a, o)$ and $P(\cdot \mid s, a, o)$, and $\operatorname{val} Q_t(s')$ depends on $s'$ only through the current table. Its conditional variance is at most $K(1 + \|Q_t\|_\infty^2)$ for a constant $K$, because $|\operatorname{val} Q_t(s')| \le \|Q_t\|_\infty$ and $r$ has bounded variance. These are the conditions of the asynchronous stochastic approximation theorem for a max-norm contraction (Jaakkola, Jordan and Singh, 1994; Tsitsiklis, 1994), which is the theorem behind [Q-learning convergence](/tabular-q-learning-convergence/). With Claim 2 it gives $Q_t \to Q^*$ with probability 1. Littman and Szepesvári (1996) state this result for minimax-Q as a case of generalized Q-learning, where any non-expansive summary operator replaces the max. $\square$

The value $V(s)$ and the strategy $\pi(s)$ of line L6 are computed from $Q_t$, so $V \to v^*$ by Claim 1. The strategies need not converge when $Q^*(s)$ has several optimal strategies, but by Claim 4 every limit point is optimal.

## Claim 4 (safety of the learned policy)

If $\|Q - Q^*\|_\infty \le \delta$ and, in each state $s$, $x(s)$ is an optimal row strategy of $Q(s)$, then the stationary strategy $x$ gets at least $v^*(s) - 2\delta/(1-\gamma)$ from every state $s$, against every strategy of the opponent.

*Proof.* Fix $x$. The opponent then faces an MDP in which it minimizes, and its optimal value $w$, which is the row player's value of $x$ against a best response, is the unique fixed point of the monotone $\gamma$-contraction

$$(Fu)(s) = \min_{o} \sum_a x(a \mid s) \Big[R(s, a, o) + \gamma \sum_{s'} P(s' \mid s, a, o) u(s')\Big].$$

A history-dependent opponent cannot do better than this MDP optimum. Since $x(s)$ is optimal in $Q(s)$, $\min_o \sum_a x(a \mid s) Q(s, a, o) = \operatorname{val} Q(s) \ge \operatorname{val} Q^*(s) - \delta = v^*(s) - \delta$ by Claim 1. Replacing $Q$ by $Q^*$ costs at most another $\delta$, so

$$(Fv^*)(s) = \min_o \sum_a x(a \mid s) Q^*(s, a, o) \ge v^*(s) - 2\delta.$$

Let $c = 2\delta/(1-\gamma)$. Then $F(v^* - c\mathbf{1}) = Fv^* - \gamma c \mathbf{1} \ge v^* - (2\delta + \gamma c)\mathbf{1} = v^* - c\mathbf{1}$. Since $F$ is monotone, $F^k(v^* - c\mathbf{1}) \ge v^* - c\mathbf{1}$ for every $k$, and $F^k(v^* - c\mathbf{1}) \to w$. So $w \ge v^* - c\mathbf{1}$. $\square$

With $\delta = 0$, this is part 2 of Shapley's theorem: the strategy that is optimal in each stage game $Q^*(s)$ guarantees $v^*$.

## Line L6 in the implementation

The implementation computes $\operatorname{val} M$ by the simplex method. After a shift that makes every entry positive (the shift adds a constant to the value, see Claim 1), the column player's problem is $\max \sum_o w_o$ subject to $Mw \le \mathbf{1}$, $w \ge 0$, with optimum $1/\operatorname{val} M$; its dual is $\min \sum_a u_a$ subject to $M^\top u \ge \mathbf{1}$, $u \ge 0$. By [LP duality](/lp-duality/) the two optima are equal, and $x = u / \sum u$ and $y = w / \sum w$ are optimal strategies. The slack basis is feasible because the right side is $\mathbf{1} \ge 0$, and Bland's rule (the lowest index enters, ties in the ratio test go to the lowest basic index) prevents cycling, so the method stops at an optimum. The tests certify each answer directly: the row strategy gets at least the value against every column and the column strategy allows at most the value, which proves optimality without trusting the solver.

## What is not proved

The finite-sample rate of minimax-Q is not proved here; it is like that of Q-learning and degrades with $1/(1-\gamma)$ and with the number of triples. Claim 3 needs every triple to be tried infinitely often, which the learner cannot ensure alone, because the opponent chooses $o$. Nothing is claimed for general-sum games, where $\operatorname{val}$ is not defined and Nash-Q needs further assumptions.
