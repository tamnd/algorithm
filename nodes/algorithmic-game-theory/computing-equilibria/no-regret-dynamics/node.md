---
tag: JK0P2M
kind: technique
slug: no-regret-dynamics
name: No-regret dynamics
aliases:
- no-regret learning in games
area: algorithmic-game-theory/computing-equilibria
level: core
summary: Every player runs a no-regret online learning algorithm against the others. The time average of play is then an approximate equilibrium.
prereqs: [regret, multiplicative-weights-update, coarse-correlated-equilibrium]
see_also: [no-regret-coarse-correlated-theorem, no-regret-zero-sum-theorem, regret-matching, blum-mansour-reduction, optimistic-hedge, counterfactual-regret-minimization, smoothness-framework, best-response-dynamics]
sources:
  - book: isbn:9781316624791
    title: "Tim Roughgarden, Twenty Lectures on Algorithmic Game Theory, Cambridge University Press, 2016"
    locator: "Lecture 17 (no-regret dynamics, multiplicative weights and coarse correlated equilibria) and Lecture 18 (swap regret, correlated equilibria and the minimax theorem)"
  - book: isbn:9780521841085
    title: "Nicolo Cesa-Bianchi and Gabor Lugosi, Prediction, Learning, and Games, Cambridge University Press, 2006"
    locator: Chapter 7 (prediction and playing games)
  - paper: doi:10.1006/game.1999.0738
    title: "Yoav Freund and Robert E. Schapire, Adaptive game playing using multiplicative weights, Games and Economic Behavior 29(1-2) (1999), 79-103"
    locator: repeated play of a matrix game with multiplicative weights and the approximately optimal average strategies
  - paper: doi:10.1111/1468-0262.00153
    title: "Sergiu Hart and Andreu Mas-Colell, A simple adaptive procedure leading to correlated equilibrium, Econometrica 68(5) (2000), 1127-1150"
    locator: regret matching and the convergence of the empirical distribution of play to the set of correlated equilibria
---

No-regret dynamics turns an online learning algorithm into a method to compute equilibria, and into a model of how players reach them. Every player of a game runs its own algorithm with small [regret](/regret/), such as [multiplicative weights](/multiplicative-weights-update/), and treats the payoffs that the others' choices give it as the data of an online problem. Nobody solves the game. Still, the time average of the joint play is an approximate equilibrium, of a kind fixed by the kind of regret: small external regret gives a [coarse correlated equilibrium](/no-regret-coarse-correlated-theorem/), small swap regret gives a [correlated equilibrium](/correlated-equilibrium/), and in two-player zero-sum games small external regret gives [optimal strategies](/no-regret-zero-sum-theorem/). The error is the largest average regret, so it falls like $1/\sqrt{T}$ with standard algorithms and faster with [optimistic Hedge](/optimistic-hedge/). The method contrasts with [best-response dynamics](/best-response-dynamics/), which looks for a pure Nash equilibrium and need not stop.

## In plain words

Many players play the same game again and again. Each one has a simple rule of thumb: play more often the moves that would have done well in the past, so that, looking back, no fixed move would have been clearly better. No player needs to know the others' payoffs, and the players do not talk to each other. If one writes down what everybody did in every round and treats the record as a lottery over joint moves, this lottery is almost an equilibrium. So simple, selfish learning finds an equilibrium of a weaker kind, even where finding a Nash equilibrium is hard.

## When it applies

- The game is finite, or has convex strategy sets with concave utilities, and each player can get, after each round, its payoff for every one of its own strategies against the current play of the others (full information), or at least its own realized payoff (bandit feedback).
- A coarse correlated or correlated equilibrium is good enough, or the game is two-player zero-sum, where these equilibria give optimal strategies.
- The output may be the average of the joint play, a distribution on profiles, and not a product of mixed strategies.
- Approximate answers are acceptable. The error after $T$ rounds is the largest average regret, which is $O(\sqrt{\log k / T})$ for multiplicative weights against any opponents.

## The template

```pseudo id=main
NO-REGRET-DYNAMICS(game, T)
L1  for each player i: start a learner A_i on the strategy set S_i      ▷ hole: the learner
L2  for t = 1 to T:
L3      for each player i: σ_i^t ← the mixed strategy that A_i proposes
L4      play the profile σ^t = σ_1^t × ... × σ_n^t, or draw s^t from it  ▷ hole: expected or realized play
L5      for each player i: u_i^t(a) ← u_i(a, σ_-i^t) for every a in S_i  ▷ hole: the feedback
L6      for each player i: give u_i^t to A_i
L7  return the empirical distribution (1/T) Σ_t σ^t                    ▷ hole: what to output
```

The holes are:

- **The learner (line L1).** Any algorithm with regret $o(T)$ against every sequence of payoff vectors. The kind of regret decides the kind of equilibrium: external regret for coarse correlated equilibria and zero-sum games, swap or internal regret for correlated equilibria.
- **Expected or realized play (line L4).** With expected play, the regret is deterministic. With realized play, each player draws a pure strategy, the output is the empirical distribution of the drawn profiles, and the bounds hold with high probability.
- **The feedback (line L5).** Full information gives the whole vector $u_i^t$. With bandit feedback a player sees only $u_i(s^t)$ and needs a bandit learner.
- **The output (line L7).** The average of the joint play is the general answer. In two-player zero-sum games the averages of the marginals, $\bar x$ and $\bar y$, are enough, and some learners also make the last strategies converge.

Why the template works: for every player $i$ and strategy $a$, the gain of $a$ over the actual play, averaged over the rounds, is the regret of player $i$ against $a$ divided by $T$. For the empirical distribution of line L7, this average is exactly the gain of the deviation to $a$, which is the quantity in the definition of a coarse correlated equilibrium. The proofs are on the theorem pages linked above.

## Classic examples

- **Multiplicative weights in any finite game.** Every player runs [multiplicative weights](/multiplicative-weights-update/) with payoffs in $[0, 1]$ and step $\eta = \sqrt{8 \ln k / T}$, so its regret is at most $\sqrt{T \ln k / 2}$. By the [theorem on coarse correlated equilibria](/no-regret-coarse-correlated-theorem/), the output is an $\varepsilon$-coarse correlated equilibrium for $T \ge \ln k / (2 \varepsilon^2)$. With $k = 10$ strategies and $\varepsilon = 0.01$, this is $T = 11{,}513$ rounds, for any number of players.
- **Zero-sum games.** In the game $M = \begin{pmatrix} 0 & -1 & 2 \\ 1 & 0 & -1 \\ -1 & 1 & 0 \end{pmatrix}$, a variant of rock-paper-scissors, the value is $1/12$ with optimal strategies $x^* = (1/4, 5/12, 1/3)$ and $y^* = (1/3, 5/12, 1/4)$. Both players run multiplicative weights with $\eta = \sqrt{\ln 3 / T}$. The gap $\max_i (M \bar y)_i - \min_j (\bar x^\top M)_j$ of the average strategies was about $0.038$ for $T = 100$, $0.020$ for $T = 1000$ and $0.0034$ for $T = 10{,}000$, and for $T = 10{,}000$ the averages were $(0.251, 0.416, 0.333)$ and $(0.333, 0.416, 0.251)$. The [zero-sum theorem](/no-regret-zero-sum-theorem/) bounds this gap by the sum of the two average regrets.
- **Correlated equilibria.** With [regret matching](/regret-matching/) on the internal regrets, or any learner wrapped by the [Blum-Mansour reduction](/blum-mansour-reduction/), each player has small swap regret, and the empirical distribution of play converges to the set of correlated equilibria (Hart and Mas-Colell 2000).
- **Poker and other extensive-form games.** [Counterfactual regret minimization](/counterfactual-regret-minimization/) runs a regret minimizer at every information set of a two-player zero-sum game in extensive form. The average strategies then approach a Nash equilibrium, which is how large poker games were solved.
- **Price of anarchy of learning.** When the game is smooth, the bound of the [smoothness framework](/smoothness-framework/) holds for every coarse correlated equilibrium, so the average welfare of any no-regret dynamics is within that factor of the optimum, up to the average regret.

## Variations

- **Faster in self-play.** When all players use the same predictable learner, the regrets can be much smaller than against an adversary. [Optimistic Hedge](/optimistic-hedge/) has regret polylogarithmic in $T$ in self-play, so the error falls like $1/T$ up to logarithmic factors.
- **Bandit feedback.** With only the realized payoff, players use [EXP3](/exp3/) or another [bandit algorithm](/multi-armed-bandit/); the regret is $O(\sqrt{T k \log k})$, so more rounds are needed.
- **Continuous games.** With convex strategy sets and concave utilities, players run [online gradient descent](/online-gradient-descent/) or [mirror descent](/mirror-descent/), as in [online convex optimization](/online-convex-optimization/).
- **Best responses and fictitious play.** If a player best responds to the empirical mix of the others instead of running a no-regret learner, the dynamics is fictitious play. It still converges in zero-sum games by [Robinson's theorem](/robinson-fictitious-play-theorem/), but it is not no-regret and can cycle in other games.
- **Approachability.** [Blackwell's approachability theorem](/blackwell-approachability/) gives a general way to build learners for many kinds of regret at once.

## Pitfalls

- **Returning the last strategies in line L7.** The time average converges, but the strategies $\sigma^t$ need not. In matching pennies, multiplicative weights on both sides moves away from the equilibrium, toward the boundary of the simplex. Return the average, or use a learner with last-iterate guarantees.
- **Averaging the marginals in line L7 of a general-sum game.** The average of the products $\sigma^t$ is a correlated distribution, and the product of the averaged marginals can be far from it. In the game where both players get 2 at (A, A), 1 at (B, B) and 0 otherwise, alternating between (A, A) and (B, B) gives the average uniform on these two profiles, an equilibrium, but the product of the marginals is uniform on all four profiles, and there a player gains by switching to A (1 against $3/4$).
- **The wrong kind of regret in line L1.** External regret gives only a coarse correlated equilibrium. In rock-paper-scissors, play that cycles through the six profiles with different moves has bounded external regret, but its average is not a correlated equilibrium. For a correlated equilibrium, use a learner with small swap regret.
- **Badly scaled feedback in line L5.** The step size of the learner and its regret bound assume payoffs in a fixed range, usually $[0, 1]$ or $[-1, 1]$. Scale the utilities first, or the regret bound, and so the error, is off by the range.
- **Expecting a Nash equilibrium.** The output of line L7 is a coarse correlated or correlated equilibrium. Outside two-player zero-sum games, and a few other classes, no-regret dynamics does not find a Nash equilibrium in general, which matches the hardness of computing one.

## Exercises

1. All players of a game with $k = 10$ strategies each run multiplicative weights with regret at most $\sqrt{T \ln k / 2}$ for payoffs in $[0, 1]$. How many rounds make the empirical distribution an $\varepsilon$-coarse correlated equilibrium for $\varepsilon = 0.01$? *Answer:* The average regret is at most $\sqrt{\ln k / (2T)}$, which is at most $\varepsilon$ when $T \ge \ln 10 / (2 \cdot 10^{-4}) \approx 11{,}513$.
2. In a two-player zero-sum game, the column player plays a best response to $x^t$ in every round. Show that its regret is at most 0. *Answer:* $\sum_t x^{t\top} M y^t = \sum_t \min_j (x^{t\top} M)_j \le \min_j \sum_t (x^{t\top} M)_j$, because a sum of minima is at most the minimum of the sums.
3. In the coordination game of the pitfalls, check that the uniform distribution on (A, A) and (B, B) is a coarse correlated equilibrium, and that the product of its marginals is not. *Answer:* Under the first, each player gets $3/2$, while always A gives $1$ and always B gives $1/2$. Under the product, each player gets $(2 + 1)/4 = 3/4$, and always A gives $2 \cdot 1/2 = 1 > 3/4$.

## References
