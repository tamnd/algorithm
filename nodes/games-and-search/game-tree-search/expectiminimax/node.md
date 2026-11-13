---
tag: 8K5D18
kind: algorithm
slug: expectiminimax
name: Expectiminimax
aliases:
- expectimax
area: games-and-search/game-tree-search
level: core
summary: Values a game tree with chance nodes by taking the maximum at MAX nodes, the minimum at MIN nodes and the probability-weighted average at chance nodes.
model: real-ram
complexity:
  vars: {b: the number of moves at a decision node, n: the number of outcomes at a chance node, d: the number of rounds of a decision and a chance event}
  time: {worst: O((b n)^d), best: O((b n)^d)}
  space: {extra: O(d)}
properties: {deterministic: true, recursive: true, exact: true}
prereqs: [minimax, stochastic-game, expected-value]
see_also: [alpha-beta-pruning, evaluation-function, monte-carlo-tree-search, imperfect-information-game, markov-decision-process, value-iteration, game-tree, rollout-algorithm]
sources:
  - book: "L. Fox (ed.), Advances in Programming and Non-Numerical Computation, Pergamon Press, 1966"
    title: "Donald Michie, Game-playing and game-learning automata, Chapter 8"
    locator: pp. 183 to 200 (expectiminimax, the backing up of expected values through chance moves)
  - paper: doi:10.1016/S0004-3702(83)80015-0
    title: "Bruce W. Ballard, The *-minimax search procedure for trees containing chance nodes, Artificial Intelligence 21(3) (1983), 327-350"
    locator: the *-minimax procedure, and the Star1 and Star2 cutoffs at chance nodes with bounded leaf values
  - paper: doi:10.1007/11674399_3
    title: "Thomas Hauk, Michael Buro and Jonathan Schaeffer, Rediscovering *-minimax search, Computers and Games (CG 2004), LNCS 3846, Springer, 2006, 35-50"
    locator: Star1 and Star2 with probing and modern search enhancements, and the measured savings in backgammon
  - paper: doi:10.1145/203330.203343
    title: "Gerald Tesauro, Temporal difference learning and TD-Gammon, Communications of the ACM 38(3) (1995), 58-68"
    locator: the learned evaluation function of TD-Gammon and its use with shallow search over the dice rolls
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 5 (the section on stochastic games, the EXPECTIMINIMAX value and why the evaluation must be a positive linear transform of the expected utility)
---

Expectiminimax computes the value of a finite game tree that has chance nodes as well as the moves of two players, as in backgammon, where dice decide what moves are possible. It is [minimax](/minimax/) with one more rule: at a chance node, take the average of the children weighted by their probabilities. The result is the expected payoff under optimal play by both players, and the move it picks at the root is an optimal move.

## In plain words

Think of a board game where each turn starts with a dice roll. To judge a move, you look at every way the dice can fall next. For each roll you ask what your opponent would then do to hurt you most, and what you would do after that. You cannot pick the roll, so you do not take the best roll or the worst: you take the average over the rolls, with likely rolls counted more. You take the best for yourself at your turns and the worst at the opponent's turns. Working back from the end of the game this way gives each position a fair score and tells you the best move.

## The problem

A *stochastic game tree* ([stochastic game](/stochastic-game/)) is a finite rooted tree whose internal nodes are of three kinds. At a MAX node the maximizing player picks a child, at a MIN node the minimizing player picks a child, and at a chance node a child is drawn at random with given probabilities $p_1, \ldots, p_k \ge 0$ that sum to 1. Each leaf has a payoff to MAX, a real number. Both players see the whole history, so this is a game of perfect information with chance moves.

The input is such a tree, given by a successor function, or a position with a depth limit and an [evaluation function](/evaluation-function/) for the cut leaves. The output is the value of the root and a best move. The *value* of a node is the expected payoff that MAX can guarantee from it against every MIN strategy, which by the proof below equals the expected payoff that MIN can hold MAX to.

## The algorithm

```pseudo id=main
EXPECTIMINIMAX(n)
L1  if n is a leaf then return UTILITY(n)
L2  if n is a MAX node then return max over children c of n of EXPECTIMINIMAX(c)
L3  if n is a MIN node then return min over children c of n of EXPECTIMINIMAX(c)
L4  return the sum over outcomes (p, c) of n of p · EXPECTIMINIMAX(c)
```

Line L4 handles the chance nodes. The best move at a MAX root is a child with the largest value, and at a MIN root a child with the smallest. In a game program, line L1 also stops at a depth limit and returns the evaluation of the position. The implementation keeps an explicit stack of frames, one per node on the current path, so a deep tree does not overflow the call stack.

## Example

MAX chooses between moves $a$ and $b$. Then a die decides one of two outcomes, and then MIN chooses between two leaves.

| move | outcome | probability | MIN's options | MIN's choice |
| --- | --- | --- | --- | --- |
| a | 1 | 1/3 | 3, 5 | 3 |
| a | 2 | 2/3 | 4, 8 | 4 |
| b | 1 | 1/2 | 6, 1 | 1 |
| b | 2 | 1/2 | 9, 7 | 7 |

Line L3 gives the MIN values in the last column. Line L4 gives the chance node under $a$ the value $\tfrac13 \cdot 3 + \tfrac23 \cdot 4 = 11/3$, and the chance node under $b$ the value $\tfrac12 \cdot 1 + \tfrac12 \cdot 7 = 4$. Line L2 gives the root $\max(11/3, 4) = 4$, so MAX plays $b$. The search evaluates all 8 leaves.

Plain minimax with the chance node replaced by MIN would give $a$ the value 3 and $b$ the value 1 and pick $a$; with the chance node replaced by MAX it would give 4 and 7 and pick $b$, but for the wrong reason. A third mistake is to average over the dice *before* the decision: if MAX could see both rolls in advance, the expected value would be $\tfrac16 \cdot 3 + \tfrac16 \cdot 7 + \tfrac26 \cdot 4 + \tfrac26 \cdot 7 = 16/3$, more than the true value 4. The order of max and expectation matters.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows, by induction on the height of the tree, that EXPECTIMINIMAX$(n)$ equals both $\max_\sigma \min_\tau$ and $\min_\tau \max_\sigma$ of the expected payoff from $n$, over pure strategies $\sigma$ of MAX and $\tau$ of MIN. So the value is well defined, pure strategies suffice (no mixing is needed in a game of perfect information, even with chance), and the strategy that picks a child of largest value at each MAX node is optimal. The key step is at a chance node: the strategies in different subtrees are independent, so the expectation of a sum of separate optimizations is the sum of the optimized expectations.

## Complexity

**Time.** Each node is visited once, and each visit costs $O(1)$ plus the work on its children, with exact arithmetic counted as $O(1)$ per operation ([real RAM](/real-ram/)). For $d$ rounds, each a decision with $b$ moves followed by a chance event with $n$ outcomes, the tree has $(bn)^d$ leaves, so the time is $\Theta((bn)^d)$ in all cases. Backgammon has $n = 21$ distinct rolls of two dice, and about 20 legal moves per roll, so each round multiplies the tree by about 400, and searches of more than two or three rounds are not practical.

**Space.** A depth-first search keeps one frame per level, $O(d)$ frames of $O(1)$ each when children are generated one at a time.

**Lower bound.** Without bounds on the leaf values, an unread outcome of positive probability can move the value of a chance node by any amount, so until all its outcomes are read the outcomes read so far give no bound on its value, and no cutoff can be made at it. Cutoffs at MAX and MIN nodes below a chance node are still possible (in the example, if the first leaf under $b$, outcome 2, were 6 instead of 9, then after it the value of $b$ is at most $\tfrac12 \cdot 1 + \tfrac12 \cdot 6 = 7/2 < 11/3$, and the leaf 7 need not be read). Cutoffs at chance nodes need known bounds $L \le \text{leaf} \le U$ (Ballard's Star1 and Star2), and they save less than alpha-beta pruning saves in trees without chance.

## Properties

- **Exact.** With rational probabilities and payoffs, the value is rational and the implementation computes it with no rounding.
- **Deterministic.** The chance nodes are averaged, not sampled.
- **Optimal in expectation.** The chosen move maximizes the expected payoff against an opponent who minimizes it. It does not maximize the probability of winning unless the payoffs are 1 for a win and 0 for a loss.
- **Sensitive to the scale of the evaluation.** The decision is invariant under positive affine changes $v \mapsto \alpha v + \beta$ with $\alpha > 0$, but not under other increasing changes (see Pitfalls). Plain minimax is invariant under every increasing change.
- **Perfect information only.** All players see all past chance outcomes. For hidden information, see [imperfect-information games](/imperfect-information-game/).

## Variants and improvements

- **Expectimax.** With no MIN nodes, the same recursion computes the optimal value of a finite-horizon [Markov decision process](/markov-decision-process/) unrolled into a tree. [Value iteration](/value-iteration/) does the same work on the state graph instead of the tree, so repeated states are computed once.
- **Star1 (Ballard 1983).** If all leaf values lie in $[L, U]$ and the search window is $(\alpha, \beta)$, then after the first $i$ outcomes of a chance node with values $v_1, \ldots, v_i$ the node's value lies between $\sum_{j \le i} p_j v_j + (1 - \sum_{j \le i} p_j)\,L$ and $\sum_{j \le i} p_j v_j + (1 - \sum_{j \le i} p_j)\,U$. If the upper bound is at most $\alpha$ or the lower bound at least $\beta$, the other outcomes are skipped.
- **Star2 (Ballard 1983).** When the children of a chance node are MAX (or MIN) nodes, first probe one child of each to get bounds, which makes Star1 cutoffs come sooner. Hauk, Buro and Schaeffer (2006) combined Star2 with probing, iterative deepening and a transposition table, and reported large savings over plain expectiminimax in backgammon.
- **Sampling.** Replace the average over all outcomes by an average over a few sampled outcomes, as in sparse sampling and in [Monte Carlo tree search](/monte-carlo-tree-search/) with chance nodes. The result is then an estimate.
- **Rollouts.** Estimate the value of each candidate move by many simulated games with a fixed policy and random dice ([rollout algorithms](/rollout-algorithm/)), which Tesauro and Galperin used for backgammon.
- **Negamax form.** With payoffs from the side to move, MAX and MIN merge into one rule $v(n) = \max_c (-v(c))$, and chance nodes average with no sign change if the side to move does not change at them.

## When to use it

Use expectiminimax for two-player zero-sum games with dice, shuffled cards dealt face up or other random events that both players see, when the tree up to the search depth is small enough to expand: backgammon programs search two or three plies with it, and it is the standard algorithm for games such as 2048 played against random tile placement (as expectimax). For one player against chance, it is dynamic programming over a finite horizon. When the tree is too large, use Star2 with good bounds, sampling, or Monte Carlo tree search. When the players do not see the chance outcomes, expectiminimax is wrong, and the game needs the methods of [imperfect-information games](/imperfect-information-game/).

## Pitfalls

- **A nonlinear evaluation changes the decision.** Let move $a$ lead to a fair coin flip between leaves 2 and 10, and move $b$ to the leaf 7. Expectiminimax picks $b$, since $7 > 6$. Square all leaf values, an increasing change on these leaves: now $a$ is worth $(4 + 100)/2 = 52$ and $b$ is worth 49, so it picks $a$. An evaluation function for expectiminimax must be proportional to the expected payoff (for example, the probability of winning), not only rank positions in the right order.
- **Swapping max and expectation.** Averaging over the outcomes first and then taking the best move for each outcome assumes that MAX knows the dice in advance. In the example this gives $16/3$ instead of 4.
- **Probabilities that do not sum to 1.** A move generator that lists duplicate rolls, or forgets that a double in backgammon has probability $1/36$ and a non-double $1/18$, gives a wrong average with no error message.
- **Floating-point ties.** With float probabilities, two moves of equal exact value can compare as unequal. Use exact fractions in tests.
- **Alpha-beta cutoffs at chance nodes without bounds.** Cutting off a chance node as if it were a MIN node is unsound. Use Star1 with true bounds $L$ and $U$, and remember that a depth limit with an evaluation needs bounds on the evaluation too.
- **Hidden chance outcomes.** If a card is dealt face down, the player to move does not know which subtree they are in, and expectiminimax gives a value that the player cannot reach.

## Implementations

## History

Michie (1966) described how to back up values through chance moves by expectation and named the procedure expectiminimax, in a chapter on game-playing and game-learning machines. Ballard (1983) gave the first pruning methods for chance nodes, Star1 and Star2, in the *-minimax procedure. Backgammon became the main test: Berliner's BKG program won against the world champion in an exhibition match in 1979, and Tesauro's TD-Gammon (1992 to 1995) combined a learned evaluation with a shallow expectiminimax search and with rollouts. Hauk, Buro and Schaeffer (2004, published 2006) revisited *-minimax with modern search enhancements.

## References
