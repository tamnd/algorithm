---
tag: XFPEGD
kind: algorithm
slug: counterfactual-regret-minimization
name: Counterfactual regret minimization
aliases:
- CFR
- CFR+
area: games-and-search/game-tree-search
level: research
summary: Iterative self-play method whose average strategy converges to a Nash equilibrium in two-player zero-sum games.
model: real-ram
complexity:
  vars: {n: the number of histories of the game tree, k: the number of information sets, a: the largest number of actions at an information set, t: the number of iterations, d: the depth of the tree}
  time: {worst: O(t n), best: O(t n)}
  space: {extra: O(k a + d)}
properties: {deterministic: true, iterative: true, anytime: true, approximate: true}
prereqs: [imperfect-information-game, regret, nash-equilibrium]
see_also: [nash-equilibrium-computation, minimax-theorem, multiplicative-weights-update, expert-problem, exp3, monte-carlo-tree-search, zero-sum-game, linear-programming-problem]
sources:
  - book: "J. C. Platt, D. Koller, Y. Singer and S. Roweis (eds.), Advances in Neural Information Processing Systems 20 (NIPS 2007), Curran Associates, 2008"
    title: "Martin Zinkevich, Michael Johanson, Michael Bowling and Carmelo Piccione, Regret minimization in games with incomplete information"
    locator: pp. 1729 to 1736 (immediate counterfactual regret, Eq. 4 for the average strategy, Eq. 7 and 8 for regret matching, Theorem 2 on average regret and equilibria, Theorem 3 on the decomposition of regret, Theorem 4 on the convergence bound)
  - paper: doi:10.1111/1468-0262.00153
    title: "Sergiu Hart and Andreu Mas-Colell, A simple adaptive procedure leading to correlated equilibrium, Econometrica 68(5) (2000), 1127-1150"
    locator: regret matching, the rule that plays actions in proportion to their positive regrets
  - paper: arXiv:1407.5042
    title: "Oskari Tammelin, Solving large imperfect information games using CFR+, 2014"
    locator: the CFR+ variant (regret matching+, alternating updates and a weighted average)
  - paper: doi:10.1126/science.1259433
    title: "Michael Bowling, Neil Burch, Michael Johanson and Oskari Tammelin, Heads-up limit hold'em poker is solved, Science 347(6218) (2015), 145-149"
    locator: CFR+ on heads-up limit Texas hold'em, and the exploitability that makes the game essentially solved
  - book: "Y. Bengio, D. Schuurmans, J. Lafferty, C. Williams and A. Culotta (eds.), Advances in Neural Information Processing Systems 22 (NIPS 2009), Curran Associates, 2009"
    title: "Marc Lanctot, Kevin Waugh, Martin Zinkevich and Michael Bowling, Monte Carlo sampling for regret minimization in extensive games"
    locator: pp. 1078 to 1086 (Monte Carlo CFR, with outcome sampling and external sampling)
  - book: "H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games, Volume I, Annals of Mathematics Studies 24, Princeton University Press, 1950"
    title: "Harold W. Kuhn, A simplified two-person poker"
    locator: pp. 97 to 103 (the three-card game, its equilibria and the value -1/18 to the first player)
---

Counterfactual regret minimization (CFR) computes an approximate Nash equilibrium of a two-player zero-sum game with hidden information, such as poker. It plays the game against itself many times. At every information set it keeps a regret for each action, which measures how much better that action would have done in the past, weighted by the probability that the other player and chance lead to that information set. The next strategy at the set plays the actions in proportion to their positive regrets. The average of the strategies over all iterations converges to an equilibrium, and its exploitability after $T$ iterations is at most a constant times $1/\sqrt{T}$.

## In plain words

Imagine you play many rounds of a card game against a copy of yourself. After each round you look at every decision you could have faced and ask: if I always took this action here, how much more would I have won? This is the regret of the action. You count it only as much as the cards and your opponent made that decision point likely. Next round, you choose each action with a chance that grows with its regret, and you never choose actions whose regret is zero or less. Your strategy in any single round may jump around. But the average over all rounds settles down to a strategy that nobody can beat.

## The problem

The input is a finite two-player zero-sum extensive game with perfect recall ([imperfect-information game](/imperfect-information-game/)). It has a game tree with chance nodes and decision nodes. The decision nodes of each player are grouped into information sets, the nodes that the player cannot tell apart. Payoffs to player 1 are given at the leaves, and player 2 gets the negative. A behavior strategy $\sigma_i$ gives a probability distribution $\sigma_i(I, \cdot)$ on the actions at each information set $I$ of player $i$.

The output is a strategy profile $\bar\sigma = (\bar\sigma_1, \bar\sigma_2)$ with small **exploitability**

$$\mathrm{expl}(\bar\sigma) = \max_{\tau} u(\tau, \bar\sigma_2) - \min_{\tau} u(\bar\sigma_1, \tau),$$

where $u$ is the expected payoff to player 1. The exploitability is at least 0, and it is 0 exactly when $\bar\sigma$ is a [Nash equilibrium](/nash-equilibrium/). The value $v$ of the game is between the two terms, so each player of $\bar\sigma$ is guaranteed a payoff within $\mathrm{expl}(\bar\sigma)$ of $v$.

## The algorithm

```pseudo id=main
CFR(G, T)
L1  set R[I][a] ← 0 and S[I][a] ← 0 for every information set I and action a
L2  repeat T times
L3    for every I: σ(I, a) ← R⁺[I][a] / Σ_b R⁺[I][b], or 1/|A(I)| if no regret is positive
L4    WALK(root, 1, 1, 1)
L5  return the average strategy S[I][a] / Σ_b S[I][b] for every I

WALK(h, π₁, π₂, π_c)
L6  if h is a leaf then return u(h)
L7  if h is a chance node then return Σ_a p(a) · WALK(ha, π₁, π₂, π_c · p(a))
L8  let I be the information set of h and i the player to act; −i is the other player
L9  for each action a: v[a] ← WALK(ha) with π_i multiplied by σ(I, a)
L10 v_h ← Σ_a σ(I, a) · v[a]
L11 for each a: R[I][a] ← R[I][a] + s_i · π_{−i} · π_c · (v[a] − v_h)
L12 for each a: S[I][a] ← S[I][a] + π_i · σ(I, a)
L13 return v_h
```

Here $R^+ = \max(R, 0)$, and $s_1 = 1$, $s_2 = -1$ turn the payoff to player 1 into the payoff of the player who acts. Line L3 is **regret matching** (Hart and Mas-Colell 2000), and it fixes the strategy $\sigma^t$ of iteration $t$ before the walk starts, so every node of the same information set uses the same probabilities. Line L11 adds the **counterfactual regret** of each action: the gain of always playing $a$ at $h$, weighted by the probability $\pi_{-i}\pi_c$ that the other player and chance reach $h$. Line L12 weights the average strategy by the player's own reach, which is Eq. 4 of Zinkevich et al. Both players are updated in the same walk. The implementation follows this pseudocode, and it also computes an exact best response and the exploitability, which the tests use to measure convergence.

## Example

**One information set per player.** Take the matrix game with payoffs to the row player $\begin{pmatrix} 3 & -1 \\ -2 & 1 \end{pmatrix}$, whose value is $1/7$ with optimal strategies $(3/7, 4/7)$ for the rows and $(2/7, 5/7)$ for the columns ([minimax theorem](/minimax-theorem/)). Write it as a game tree in which the column player moves without seeing the row. Then CFR is regret matching in self-play:

| iteration | row strategy | column strategy | row regrets after | column regrets after |
|---|---|---|---|---|
| 1 | (1/2, 1/2) | (1/2, 1/2) | (3/4, −3/4) | (−1/4, 1/4) |
| 2 | (1, 0) | (0, 1) | (3/4, 5/4) | (−17/4, 1/4) |
| 3 | (3/8, 5/8) | (0, 1) | (−1/2, 2) | (−31/8, 1/4) |

In iteration 1 the rows are worth $1$ and $-1/2$ against the uniform column, and the mix is worth $1/4$, so the regrets are $3/4$ and $-3/4$. The strategies of single iterations jump between extremes. The average strategies after 3 iterations are $(5/8, 3/8)$ and $(1/6, 5/6)$, and after 2000 iterations they are within 0.02 of $(3/7, 4/7)$ and $(2/7, 5/7)$.

**Kuhn poker.** Three cards J < Q < K are dealt, one to each player, and each player puts 1 chip in the pot. Player 1 checks or bets 1. After a check, player 2 checks (the higher card wins 1) or bets 1, and then player 1 folds (and loses 1) or calls (the higher card wins 2). After a bet, player 2 folds (and loses 1) or calls (the higher card wins 2). The tree has 55 histories and 30 leaves, and each player has 6 information sets: a card together with the actions so far. Kuhn (1950) found all equilibria. Player 1 bets J with some $\alpha \in [0, 1/3]$, never bets Q, bets K with $3\alpha$, and after a check and a bet calls with Q with $\alpha + 1/3$. Player 2 has one equilibrium strategy: after a bet, call with K and with Q with $1/3$; after a check, bet with K and with J with $1/3$. The value is $-1/18$ to player 1. The implementation measures, from the uniform profile (exploitability $11/12$):

| iterations $T$ | 10 | 100 | 1000 | 10000 |
|---|---|---|---|---|
| exploitability of $\bar\sigma^T$ | 0.192 | 0.0513 | 0.0145 | 0.00464 |

Each tenfold increase of $T$ divides the exploitability by about 3, close to $\sqrt{10}$. After 10000 iterations the average strategy of player 1 bets J with 0.208 and K with 0.613, about $3 \cdot 0.208$, so CFR picks one member of Kuhn's family.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has five steps. First, the average strategy of line L12 has realization weights equal to the averages of the realization weights of the iterations, so the payoff against it is the average payoff. Second, the exploitability of the average profile equals $(R_1^T + R_2^T)/T$, the sum of the two players' average overall regrets. Third, line L11 accumulates the immediate counterfactual regret $R^T_{\mathrm{imm}}(I, a)$. Fourth, regret matching keeps $\max_a R^T_{\mathrm{imm}}(I, a) \le \Delta\sqrt{A}\sqrt{T}$, where $\Delta$ is the range of the payoffs and $A$ the number of actions. Fifth, perfect recall lets the overall regret of a player split along the tree, so it is at most the sum of the positive immediate regrets over the player's information sets (Theorem 3 of Zinkevich et al.). Together,

$$\mathrm{expl}(\bar\sigma^T) \le \frac{2\,\Delta\,|\mathcal I|\,\sqrt{A}}{\sqrt{T}},$$

with $|\mathcal I|$ the larger number of information sets of a player. This is Theorems 2 and 4 of the paper.

## Complexity

**Time.** Each iteration walks the whole game tree once, with $O(1)$ work per history and action, so an iteration costs $O(n)$ for $n$ histories and $T$ iterations cost $O(Tn)$. To reach exploitability $\varepsilon$, the bound needs $T = O(\Delta^2 |\mathcal I|^2 A / \varepsilon^2)$ iterations. In practice CFR converges much faster than the bound: for Kuhn poker the bound after 1000 iterations is $2 \cdot 4 \cdot 6 \cdot \sqrt{2}/\sqrt{1000} \approx 2.15$, while the measured exploitability is $0.0145$.

**Space.** Two tables of $O(ka)$ numbers for $k$ information sets with at most $a$ actions, and a recursion stack of depth $d$. The tree itself is not stored if the game can generate its moves. The table size, not the tree size, limits CFR: an information set is usually much smaller than the set of strategies, which grows exponentially in $k$.

**A best response** for the measurement costs one more walk of the tree for each player.

## Properties

- **Average, not last, iterate.** The guarantee is for $\bar\sigma^T$. The current strategy $\sigma^t$ of vanilla CFR need not converge, as the table above shows.
- **No step size.** Regret matching has no learning rate, unlike [multiplicative weights](/multiplicative-weights-update/), which can be used in its place at each information set.
- **Two players, zero sum.** Step 2 of the proof needs it. In general-sum or multiplayer games each player still has small regret, but the average profile need not be close to a Nash equilibrium.
- **Perfect recall needed.** Step 5 of the proof uses it, and with imperfect recall the regret need not decompose.
- **Anytime.** The average profile can be used after any number of iterations, and its exploitability can be measured exactly in small games.

## Variants and improvements

- **CFR+** (Tammelin 2014), listed as an alias of this page, changes three things: regrets are set to $\max(R, 0)$ after every update (regret matching+), the players are updated in turn rather than in the same walk, and the average gives iteration $t$ weight proportional to $t$. CFR+ converges much faster in practice, and its current iterate is often close to an equilibrium too. Bowling, Burch, Johanson and Tammelin (2015) used it to solve heads-up limit Texas hold'em.
- **Monte Carlo CFR** (Lanctot et al. 2009) samples part of the tree in each iteration: outcome sampling follows one path, and external sampling samples the actions of chance and of the other player but tries all actions of the updated player. Each iteration is much cheaper, and the regret bound holds in expectation.
- **Discounted and linear CFR** weight early iterations less, which helps when early regrets are large and wrong.
- **Abstraction and function approximation.** For games too large to store the tables, similar information sets are merged, or the regrets are predicted by a neural network (Deep CFR). Poker programs then combine CFR with search during play.

## When to use it

Use CFR to compute strategies for two-player zero-sum games with hidden information whose tree is too large for the linear program of the sequence form ([equilibrium computation](/nash-equilibrium-computation/)) but whose information sets fit in memory: poker variants, and card and board games with hidden state. For a game of perfect information, [minimax](/minimax/) and [alpha-beta pruning](/alpha-beta-pruning/) are exact and faster. For a single matrix game a linear program is exact. If the tree cannot be walked at all in one iteration, use a Monte Carlo variant.

## Pitfalls

- **Using the current strategy.** Return the average strategy of line L5, not the regret-matching strategy of the last iteration.
- **Updating the strategy during the walk.** Compute $\sigma^t$ once before the walk (line L3). If the regrets of an information set change while other nodes of the same set are still to be visited, those nodes use a different strategy and the proof no longer applies.
- **Wrong weights.** The regret uses the reach of the other player and of chance, $\pi_{-i}\pi_c$; the average strategy uses the player's own reach $\pi_i$. If you swap them, the tables hold other quantities and the proof no longer applies.
- **Sign of player 2.** With payoffs to player 1 in the tree, the regret of player 2 must be negated (the factor $s_i$).
- **Trusting the bound to judge progress.** The theoretical bound is very loose. Measure the exploitability with a best response when the game is small enough.

## Implementations

## History

Hart and Mas-Colell (2000) introduced regret matching for repeated matrix games and showed that its empirical play converges to the set of correlated equilibria. Zinkevich, Johanson, Bowling and Piccione (2007) at the University of Alberta defined counterfactual regret, proved that minimizing it at each information set minimizes the overall regret, and used CFR to compute strategies for abstractions of limit Texas hold'em with about $10^{12}$ states. Lanctot, Waugh, Zinkevich and Bowling (2009) gave the Monte Carlo variants. Tammelin (2014) proposed CFR+, and Bowling, Burch, Johanson and Tammelin (2015) used it to solve heads-up limit hold'em to an exploitability too small to detect in a lifetime of play. Later poker programs that beat professional players in no-limit hold'em built on CFR with abstraction and real-time search. Kuhn's three-card poker (1950), solved by hand, is the standard first test.

## References
