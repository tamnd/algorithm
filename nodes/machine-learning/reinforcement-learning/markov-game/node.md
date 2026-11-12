---
tag: VR68TW
kind: model
slug: markov-game
name: Markov game
aliases:
- competitive Markov decision process
area: machine-learning/reinforcement-learning
level: advanced
summary: "An MDP with several players who act at once and get their own rewards. Zero-sum discounted games have a value and optimal stationary strategies (Shapley 1953)."
prereqs: [markov-decision-process, zero-sum-game, bellman-contraction]
see_also: [minimax-q, multi-agent-reinforcement-learning, nash-equilibrium, minimax-theorem, zero-sum-game, stochastic-game, linear-programming-problem, pomdp]
sources:
  - paper: doi:10.1073/pnas.39.10.1095
    title: Lloyd S. Shapley, Stochastic Games, Proceedings of the National Academy of Sciences 39(10), 1095-1100, 1953
    locator: "the existence of the value and of optimal stationary strategies, and the successive approximation scheme"
  - paper: "Michael L. Littman, Markov Games as a Framework for Multi-Agent Reinforcement Learning, Proceedings of the 11th International Conference on Machine Learning (ICML), 157-163, 1994"
    title: Markov Games as a Framework for Multi-Agent Reinforcement Learning
    locator: "the Markov game model and the minimax-Q algorithm"
  - book: isbn:9780387948058
    title: Jerzy Filar and Koos Vrieze, Competitive Markov Decision Processes, Springer, 1997
    locator: "the discounted zero-sum stochastic game and its mathematical programming formulations"
  - paper: "A. M. Fink, Equilibrium in a Stochastic n-Person Game, Journal of Science of the Hiroshima University, Series A-I, 28, 89-93, 1964"
    title: Equilibrium in a Stochastic n-Person Game
    locator: "the existence of stationary equilibrium points in discounted games"
  - paper: "Anne Condon, The Complexity of Stochastic Games, Information and Computation 96(2), 203-224, 1992"
    title: The Complexity of Stochastic Games
    locator: "simple stochastic games and the NP and coNP bound"
---

A Markov game is a [Markov decision process](/markov-decision-process/) with two or more players. In each state every player picks an action at the same time, the joint action sets the rewards of all players and the law of the next state, and the play goes on. Shapley (1953) introduced the model for two-player zero-sum games and proved that such a game has a value and optimal strategies that depend only on the current state. Littman (1994) made it the base model for multi-agent reinforcement learning. The [stochastic game](/stochastic-game/) page of the game tree area is a different object: a game tree with chance nodes, such as backgammon, with alternating moves and no repeated states or discount.

## The machine

A finite discounted Markov game with $N$ players is a tuple $(S, A^1, \dots, A^N, P, R^1, \dots, R^N, \gamma)$:

- $S$ is a finite set of states and $A^k$ a finite set of actions of player $k$.
- $P(s' \mid s, a^1, \dots, a^N)$ is the transition law of the joint action.
- $R^k(s, a^1, \dots, a^N)$ is the expected reward of player $k$.
- $0 \le \gamma < 1$ is the discount.

Each player maximizes its own expected discounted return. All players see the state and the past actions. A strategy maps histories to distributions over actions. A stationary strategy $x^k(\cdot \mid s)$ depends only on the current state. With one player the model is an MDP.

**Zero-sum games.** For two players with $R^2 = -R^1$, write $R = R^1$. The row player maximizes and the column player minimizes. In state $s$, for a value vector $v$, the stage game is the matrix game

$$M_s(v)[i, j] = R(s, i, j) + \gamma \sum_{s'} P(s' \mid s, i, j)\, v(s').$$

The Shapley operator is $(Tv)(s) = \operatorname{val} M_s(v)$, where $\operatorname{val}$ is the value of a finite [zero-sum game](/zero-sum-game/) in mixed strategies, which exists by the [minimax theorem](/minimax-theorem/).

**Computing $\operatorname{val}$.** For an $m \times n$ matrix $M$, $\operatorname{val} M$ is the optimum of the [linear program](/linear-programming-problem/) $\max u$ subject to $\sum_i x_i M[i, j] \ge u$ for all $j$, $\sum_i x_i = 1$ and $x \ge 0$. So one sweep of Shapley's iteration solves $|S|$ linear programs. For a $2 \times 2$ matrix $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ there is a closed form. If $\max_i \min_j M = \min_j \max_i M$, there is a saddle point and pure strategies are optimal. Otherwise both players mix, $a + d - b - c \ne 0$, and

$$\operatorname{val} M = \frac{ad - bc}{a + d - b - c}, \qquad p = \frac{d - c}{a + d - b - c}, \qquad q = \frac{d - b}{a + d - b - c},$$

where $p$ is the probability of the first row and $q$ the probability of the first column.

## What it counts

For the zero-sum case the measures are the number of sweeps of Shapley's iteration to reach an error $\varepsilon$ in the max norm, and the cost of a sweep, $|S|$ matrix games of size $|A^1| \times |A^2|$ with $O(|S|)$ terms per entry. For learning, the measure is the number of samples, as for [Q-learning](/q-learning/).

**Shapley's theorem.** Let the game be zero-sum and discounted. Then:

1. $T$ is a $\gamma$-contraction in the max norm, so it has one fixed point $v^*$, and $v_{k+1} = T v_k$ converges to it with $\|v_k - v^*\|_\infty \le \gamma^k \|v_0 - v^*\|_\infty$.
2. Let $x^*(s)$ and $y^*(s)$ be optimal strategies of the stage game $M_s(v^*)$. The stationary strategy $x^*$ guarantees the row player at least $v^*(s)$ from each state $s$ against every strategy of the column player, history-dependent ones included. In the same way $y^*$ holds the row player to at most $v^*(s)$. So $v^*$ is the value of the game, and $(x^*, y^*)$ is an equilibrium in stationary strategies.

*Lemma.* For matrices $M, M'$ of the same size, $|\operatorname{val} M - \operatorname{val} M'| \le \max_{i,j} |M[i,j] - M'[i,j]|$.

*Proof.* Let $c = \max_{i,j}|M[i,j] - M'[i,j]|$. For all mixed strategies $x, y$, $x^\top M y \le x^\top M' y + c$, since $x$ and $y$ are probability vectors. Take $\min_y$ and then $\max_x$ on both sides: $\operatorname{val} M \le \operatorname{val} M' + c$. Swap $M$ and $M'$. $\blacksquare$

*Proof of 1.* $|M_s(u)[i,j] - M_s(w)[i,j]| = \gamma \left|\sum_{s'} P(s' \mid s, i, j)(u(s') - w(s'))\right| \le \gamma\|u - w\|_\infty$. By the lemma, $|(Tu)(s) - (Tw)(s)| \le \gamma \|u - w\|_\infty$. The Banach fixed point theorem gives the rest, as for the [Bellman contraction](/bellman-contraction/). $\blacksquare$

*Proof of 2.* Fix $x^*$. Then the column player faces an MDP in which it minimizes. Its optimal value $w$ solves $w(s) = \min_j \sum_i x^*(i \mid s) M_s(w)[i, j]$, and one of its optimal policies is stationary and deterministic. Since $x^*(s)$ is optimal in $M_s(v^*)$, $\min_j \sum_i x^*(i \mid s) M_s(v^*)[i, j] = v^*(s)$, so $v^*$ is a fixed point of this minimizing Bellman operator, which is a $\gamma$-contraction. So $w = v^*$, and no strategy of the column player, stationary or not, pushes the row player below $v^*$. The case of $y^*$ is symmetric. $\blacksquare$

Shapley stated the model with a positive stopping probability at each stage in place of a discount. A stopping probability of at least $\delta > 0$ in every state and joint action plays the role of $1 - \gamma$, and the same proof gives a contraction with the factor $1 - \delta$.

## Relation to other models

- **MDP.** With one player, or when the other players have one action each, $\operatorname{val}$ becomes a max and $T$ becomes the Bellman optimality operator $T^*$.
- **Matrix games.** With one state and $\gamma = 0$, a zero-sum Markov game is a matrix game, and $v^* = \operatorname{val} M$.
- **Game trees.** A [stochastic game](/stochastic-game/) in the game tree sense, a tree with chance nodes, is a finite-horizon turn-based game. Each node is its own state, and play never comes back to a state. A Markov game has simultaneous moves and states that recur.
- **General-sum games.** With $R^1 + R^2 \ne 0$, the solution concept is a [Nash equilibrium](/nash-equilibrium/). A discounted finite Markov game has an equilibrium in stationary strategies (Fink 1964), but different equilibria can give different payoffs, and there is no single value.
- **Turn-based games.** If in each state only one player has more than one action, the stage games have pure saddle points, and both players have optimal stationary deterministic strategies. Condon's simple stochastic games are the case with reachability payoffs.
- **POMDP.** A [POMDP](/pomdp/) hides the state from one player. Markov games keep the state visible. Games with hidden states are partially observable stochastic games.
- **Learning.** [Minimax-Q](/minimax-q/) (Littman 1994) replaces the max of [Q-learning](/q-learning/) by $\operatorname{val}$ of the estimated stage game. [Multi-agent reinforcement learning](/multi-agent-reinforcement-learning/) studies the general-sum and many-player cases.

## Known results in the model

Take two states and two actions per player, with $\gamma = 9/10$. In $s_1$ the rewards to the row player are $\begin{pmatrix} 3 & -1 \\ -2 & 2 \end{pmatrix}$. If the two actions have the same index, the game stays in $s_1$, and otherwise it moves to $s_2$. In $s_2$ the rewards are $\begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix}$, and the next state is $s_1$ or $s_2$ with probability 1/2 each.

- **The value.** $v^* = (29/4, 31/4) = (7.25, 7.75)$.
- **The stage games at $v^*$.** In $s_2$, $M_{s_2}(v^*) = \begin{pmatrix} 31/4 & 27/4 \\ 35/4 & 31/4 \end{pmatrix}$ has a saddle point at the second row and the second column, with the value $31/4$. In $s_1$, $M_{s_1}(v^*) = \frac{1}{40}\begin{pmatrix} 381 & 239 \\ 199 & 341 \end{pmatrix}$ has no saddle point. The closed form gives the value $\frac{381 \cdot 341 - 239 \cdot 199}{40 \cdot 284} = \frac{29}{4}$, with $p = 1/2$ and $q = 51/142$. So $v^*$ is a fixed point of $T$.
- **Shapley's iteration.** From $v_0 = 0$ with the stopping rule $\|v_{k+1} - v_k\|_\infty < \varepsilon(1-\gamma)/(2\gamma)$ and $\varepsilon = 0.01$, the iteration stops after 70 sweeps in floating point, at about $(7.2453, 7.7453)$. The error is about 0.0047, below $\varepsilon/2$.

General results:

- **Value and stationary strategies** (Shapley 1953). Every finite discounted zero-sum Markov game has a value, and both players have optimal stationary strategies.
- **No pure strategies in general.** Unlike an MDP, optimal strategies may need to mix, as in $s_1$ above. Also unlike an MDP, the value can be irrational when all data are rational, so an exact algorithm cannot, in general, output it as a fraction.
- **General-sum** (Fink 1964). Stationary Nash equilibria exist in every finite discounted Markov game.
- **Complexity of turn-based games** (Condon 1992). For simple stochastic games, deciding whether the value from the start state exceeds 1/2 is in NP $\cap$ coNP. No polynomial algorithm is known.
- **Learning** (Littman 1994; Littman and Szepesvári 1996). Minimax-Q, proposed by Littman in 1994, learns the value of a zero-sum game from play, with the same kind of step size and exploration conditions as Q-learning; the convergence proof is from Littman and Szepesvári (1996).

## References
