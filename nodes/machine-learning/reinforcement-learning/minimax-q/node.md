---
tag: ZSSWVB
kind: algorithm
slug: minimax-q
name: Minimax-Q
aliases:
- minimax Q-learning
area: machine-learning/reinforcement-learning
level: research
summary: "Q-learning for two-player zero-sum Markov games: Q(s, a, o) holds both players' actions, and the max in the target is replaced by the value of the matrix game Q(s', ., .), solved by a linear program."
solves: [rl-control]
model: real-ram
complexity:
  vars: {N: the number of steps, S: the number of states, A: the number of actions of the learner, O: the number of actions of the opponent, L: the cost of solving one A by O matrix game}
  time: {worst: "O(N L)"}
  space: {extra: "O(S A O)"}
properties: {deterministic: false, online: true, exact: false, recursive: false}
history:
  year: 1994
  people: [Michael L. Littman]
  note: "Littman proposed Markov games as the framework for multi-agent reinforcement learning and minimax-Q as its first algorithm at ICML 1994."
prereqs: [markov-game, q-learning]
see_also: [multi-agent-reinforcement-learning, minimax-theorem, zero-sum-game, simplex-method, linear-programming-problem, nash-equilibrium, tabular-q-learning-convergence, stochastic-approximation]
sources:
  - paper: "Michael L. Littman, Markov games as a framework for multi-agent reinforcement learning, Proceedings of the 11th International Conference on Machine Learning (ICML), 1994, pages 157 to 163"
    locator: the Markov game model, the minimax-Q algorithm (its figure of pseudocode), and the two-player grid soccer experiment
  - paper: "Michael L. Littman and Csaba Szepesvari, A generalized reinforcement-learning model, convergence and applications, Proceedings of the 13th International Conference on Machine Learning (ICML), 1996, pages 310 to 318"
    locator: convergence of generalized Q-learning when the summary operator is a non-expansion, with minimax-Q as an example
  - paper: doi:10.1073/pnas.39.10.1095
    title: "Lloyd S. Shapley, Stochastic games, Proceedings of the National Academy of Sciences 39(10), 1953, pages 1095 to 1100"
    locator: the value of discounted zero-sum games, stationary optimal strategies, and the contraction of the value operator
  - paper: "Junling Hu and Michael P. Wellman, Nash Q-learning for general-sum stochastic games, Journal of Machine Learning Research 4, 2003, pages 1039 to 1069"
    locator: the extension of minimax-Q to general-sum games with Nash equilibria of the stage games
  - paper: "Michael L. Littman, Friend-or-foe Q-learning in general-sum games, Proceedings of the 18th International Conference on Machine Learning (ICML), 2001, pages 322 to 328"
    locator: friend-or-foe Q-learning, which uses the minimax backup against foes
---

Minimax-Q (Littman, 1994) is [Q-learning](/q-learning/) for two-player zero-sum [Markov games](/markov-game/). The agent keeps a value $Q(s, a, o)$ for each state, its own action $a$ and the opponent's action $o$. After each step it moves $Q(s, a, o)$ toward $r + \gamma V(s')$, as Q-learning does, but $V(s')$ is not a max over actions. It is the value of the matrix game $Q(s', \cdot, \cdot)$ in mixed strategies, computed by a [linear program](/linear-programming-problem/). The optimal mixed strategy of that game is the agent's policy in $s'$. If every triple $(s, a, o)$ is tried infinitely often and the step sizes decrease in the usual way, $Q$ converges to the game's optimal $Q^*$, and the policy guarantees the game value against every opponent.

## In plain words

In a game against an opponent, the best move depends on what the opponent does, and a clever opponent will learn your habits. So the learner keeps a score for each pair of moves, its own and the opponent's. In each situation it asks: "if the opponent knew my plan and answered in the worst way for me, which plan, perhaps a random mix of moves, would still give me the most?" That plan is its policy, and the score it guarantees is the value it uses to update the scores of earlier situations. A learner that plans for the worst case is never exploited, but it may miss easy wins against a weak opponent.

## The problem

A two-player zero-sum discounted Markov game $(S, A, O, P, R, \gamma)$: in state $s$ the learner picks $a \in A$, the opponent picks $o \in O$ at the same time, the learner gets $r$ with mean $R(s, a, o)$ (the opponent gets $-r$), and the next state is $s' \sim P(\cdot \mid s, a, o)$. $P$ and $R$ are unknown; the learner sees $s$, $a$, $o$, $r$ and $s'$. By Shapley's theorem the game has a value $v^*(s)$ and optimal stationary strategies, and

$$Q^*(s, a, o) = R(s, a, o) + \gamma \sum_{s'} P(s' \mid s, a, o)\, v^*(s'), \qquad v^*(s) = \operatorname{val} Q^*(s, \cdot, \cdot),$$

where for a matrix $M$, $\operatorname{val} M = \max_{x \in \Delta(A)} \min_{o \in O} \sum_a x(a) M[a, o]$ is the value of the [zero-sum game](/zero-sum-game/), which exists by the [minimax theorem](/minimax-theorem/). The task is to learn $Q^*$ and a strategy that guarantees $v^*(s)$ from every state.

## The algorithm

```pseudo id=main
MINIMAX-Q(γ, exploration rate e, step sizes)
L1  Q(s, a, o) ← 0;  V(s) ← 0;  π(s, ·) ← uniform on A, for all s, a, o
L2  for each step, in the current state s
L3      with probability e choose a uniformly at random, else draw a from π(s, ·)
L4      observe the opponent's action o, the reward r and the next state s′
L5      Q(s, a, o) ← (1 − α) Q(s, a, o) + α (r + γ V(s′))
L6      π(s, ·), V(s) ← the optimal strategy and the value of the matrix game Q(s, ·, ·), by the linear program
           max v  subject to  Σ_a π(a) Q(s, a, o) ≥ v for every o,  Σ_a π(a) = 1,  π ≥ 0
L7      decrease α (for example α = n(s, a, o)^(−0.6), where n counts the visits)
L8  return Q, V, π
```

Line L6 is the only change from Q-learning, where $V(s) = \max_a Q(s, a)$. If the opponent has one action, the matrix has one column, and L6 is the max. Littman used an exponentially decaying step size and exploration $e = 0.2$; the convergence theorem needs the step size conditions of [stochastic approximation](/stochastic-approximation/).

The implementation solves line L6 by the [simplex method](/simplex-method/) with Bland's rule. For a positive matrix $M$, the value is $1/\max\{\sum_o w_o : Mw \le 1, w \ge 0\}$, the column player's strategy is $w$ scaled to sum to 1, and the row player's strategy comes from the dual variables. With rational entries the result is exact.

## Example

Take the two-state game of the [Markov game](/markov-game/) page, with $\gamma = 9/10$. In $s_1$ the rewards are $\begin{pmatrix} 3 & -1 \\ -2 & 2 \end{pmatrix}$, and the game stays in $s_1$ if the two players' actions have the same index, else it moves to $s_2$. In $s_2$ the rewards are $\begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix}$, and the next state is $s_1$ or $s_2$ with probability $1/2$ each. The value is $v^* = (29/4, 31/4)$. In $s_1$ the learner mixes with $p = 1/2$ (and the opponent with $q = 51/142$); in $s_2$ the second row is a saddle point.

Minimax-Q with both players choosing uniformly at random ($e = 1$, so the data cover every triple), step size $n^{-0.6}$ and seed 0:

| steps | $V(s_1)$ | $V(s_2)$ | $\pi(s_1)$ | worst-case value of $\pi$ |
|---|---|---|---|---|
| 1,000 | 5.648 | 6.109 | (0.504, 0.496) | (7.193, 7.703) |
| 10,000 | 7.107 | 7.607 | (0.5, 0.5) | (7.243, 7.744) |
| 100,000 | 7.248 | 7.758 | (0.5, 0.5) | (7.250, 7.750) |

The last column is the learner's value when the opponent knows $\pi$ and answers it in the best way. It approaches $v^*$ sooner than $V$ does, because the strategy only needs the right *shape* of $Q$.

Compare a single-agent Q-learner that treats the opponent as part of a random environment. Against the uniform opponent it learns the deterministic policy "row 1 in $s_1$, row 2 in $s_2$", worth $(12.25, 12.75)$ against that opponent. But an opponent that learns this policy plays column 2 in $s_1$ and holds it to $(70/29, 110/29) \approx (2.41, 3.79)$, far below $v^*$. Minimax-Q's mixed policy cannot be pushed below $v^*$.

## Correctness

The [proof page](proofs/correctness.md) proves:

1. **The value of a matrix game is 1-Lipschitz** in the max norm: $|\operatorname{val} M - \operatorname{val} M'| \le \max_{a, o} |M[a, o] - M'[a, o]|$.
2. **The minimax Bellman operator** $(HQ)(s, a, o) = R(s, a, o) + \gamma \sum_{s'} P(s' \mid s, a, o)\, \operatorname{val} Q(s', \cdot, \cdot)$ is a $\gamma$-contraction in the max norm, and its fixed point is $Q^*$.
3. **Convergence.** Line L5 is an asynchronous stochastic approximation step for $H$. If every triple is updated infinitely often, the step sizes satisfy $\sum_n \alpha_n = \infty$ and $\sum_n \alpha_n^2 < \infty$ for each triple, and rewards are bounded, then $Q \to Q^*$ with probability 1 (Littman and Szepesvári, 1996), by the same theorem that proves [Q-learning converges](/tabular-q-learning-convergence/).
4. **Safety of the learned policy.** If $\|Q - Q^*\|_\infty \le \delta$, the policy of line L6 guarantees at least $v^*(s) - 2\delta/(1 - \gamma)$ from every state against every opponent.

The tests check line L6 exactly: on 200 random integer matrices, the simplex strategies certify the value (the row strategy gets at least the value against every column, and the column strategy allows at most the value), and on $2 \times 2$ matrices the value equals the closed form. They also check that $v^*$ is a fixed point in exact arithmetic, and that minimax-Q reaches $v^*$ to 0.1 on three seeds.

## Complexity

Each step updates one entry and solves one $|A| \times |O|$ linear program, so $N$ steps cost $O(NL)$, where $L$ is the cost of that LP: polynomial with an interior point method, and fast in practice with the simplex method for small games. A table of $|S| \cdot |A| \cdot |O|$ entries is stored, plus a strategy and a value per state. The number of steps needed is like that of Q-learning on $|S| \cdot |A| \cdot |O|$ pairs, but the learner does not choose $o$, so covering all triples depends on the opponent.

## Properties

- **Off-policy and opponent-independent.** The update uses the opponent's observed action and the worst case over its next actions, so it learns $Q^*$ whatever the opponent does, if all triples are tried.
- **Mixed policies.** Unlike Q-learning, the greedy policy is a probability distribution; in many games no deterministic policy is optimal.
- **Conservative.** The policy guarantees $v^*$ but does not exploit a weak opponent. Against the uniform opponent of the example, minimax-Q's policy is worth less than the best response.
- **Exact in the limit, not in finite time.** With $\alpha$ fixed, $Q$ keeps moving.

## Variants and improvements

- **Shapley's value iteration** is the planning version with a known model: $V(s) \leftarrow \operatorname{val}\big(R(s) + \gamma \sum_{s'} P(s' \mid s)\, V(s')\big)$; on the example it stops after 70 sweeps for $\varepsilon = 0.01$.
- **Nash-Q** (Hu and Wellman, 2003) replaces $\operatorname{val}$ by the payoff of a [Nash equilibrium](/nash-equilibrium/) of the general-sum stage game; its convergence needs strong conditions on the stage games.
- **Friend-or-foe Q** (Littman, 2001) uses $\max$ over joint actions for friends and the minimax value against foes.
- **Correlated-Q** (Greenwald and Hall, 2003) uses correlated equilibria, which are also computed by a linear program.
- **Minimax-DQN and neural fictitious self-play** use function approximation; deep self-play methods for zero-sum games, and [counterfactual regret minimization](/counterfactual-regret-minimization/) for games with hidden information, are the modern successors.
- **Turn-based games**, where one player moves in each state, have pure saddle points, so $\operatorname{val}$ is a max or a min and no LP is needed.

## When to use it

- Use it in small two-player zero-sum games with simultaneous moves, when you want a policy that is safe against any opponent, including one that adapts.
- Use Shapley's value iteration instead when the model is known.
- Do not use it in general-sum or cooperative games; the worst-case value is then too pessimistic; see [multi-agent reinforcement learning](/multi-agent-reinforcement-learning/).
- Do not use it when the opponent is known to be weak and fixed; a best response (plain Q-learning against it) wins more.

## Pitfalls

- **Missing triples.** If the opponent never plays some $o$ in some state, $Q(s, \cdot, o)$ stays at its initial value, and the LP plans against a column that may be too good or too bad for the opponent. Optimistic or pessimistic initialization changes the learned policy.
- **Using max instead of val.** Taking $\max_a \max_o Q$ (assuming the opponent helps) or $\max_a \min_o Q$ over pure actions both give wrong values in games that need mixing; matching pennies has value 0 but $\max_a \min_o = -1$.
- **Floating-point LP.** Degenerate stage games make the simplex method cycle without an anti-cycling rule such as Bland's rule, and small rounding can flip the chosen pure strategy.
- **Reading the policy too early.** The strategy of L6 is only as good as $Q$; use the bound of Claim 4, or evaluate it against a best response, as the example does.

## Implementations

## History

Shapley (1953) introduced stochastic games and showed that the value iteration $v \leftarrow \operatorname{val} M_s(v)$ converges. Littman (1994) proposed Markov games as the framework for multi-agent reinforcement learning and minimax-Q, tested on a small grid soccer game in which minimax-Q policies held up against challengers trained to beat them, while Q-learned deterministic policies did not. Littman and Szepesvári (1996) proved its convergence as a case of generalized Q-learning. Hu and Wellman (2003) extended the idea to general-sum games with Nash-Q, and Littman (2001) proposed friend-or-foe Q-learning.

## References
