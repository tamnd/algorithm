---
tag: Z8KNKX
kind: technique
slug: rapid-action-value-estimation
name: Rapid action value estimation
aliases:
- RAVE
- all-moves-as-first
area: games-and-search/game-tree-search
level: research
summary: MCTS enhancement sharing action value statistics across subtrees to speed early learning.
prereqs: [monte-carlo-tree-search, uct]
see_also: [history-heuristic, hex-game, bias-variance-tradeoff, mean-squared-error, ucb1, rollout-algorithm, killer-heuristic, monte-carlo-policy-evaluation]
sources:
  - paper: doi:10.1016/j.artint.2011.03.007
    title: "Sylvain Gelly and David Silver, Monte-Carlo tree search and rapid action value estimation in computer Go, Artificial Intelligence 175(11) (2011), 1856-1875"
    locator: Section 3.5 (all-moves-as-first in Gobble), Section 4.1 (the AMAF value, Eq. 9 to 11), Section 4.2 (RAVE and the history heuristic), Section 4.3 (MC-RAVE, Eq. 12 to 17), Section 4.4 (UCT-RAVE, Eq. 18), Section 4.5 (the hand-selected schedule, Eq. 19), Section 4.6 (the minimum MSE schedule, Eq. 46 and 47, Table 1), Section 5 (heuristic prior knowledge, Algorithm 2)
  - paper: doi:10.1145/1273496.1273531
    title: "Sylvain Gelly and David Silver, Combining online and offline knowledge in UCT, Proceedings of the 24th International Conference on Machine Learning (ICML 2007), 273-280"
    locator: the section on rapid action value estimation (the UCT-RAVE algorithm in MoGo and its equivalence parameter k)
  - paper: doi:10.1109/TCIAIG.2012.2186810
    title: "Cameron B. Browne et al., A survey of Monte Carlo tree search methods, IEEE Transactions on Computational Intelligence and AI in Games 4(1) (2012), 1-43"
    locator: the sections on all moves as first and RAVE among the enhancements of the tree policy
---

Rapid action value estimation (RAVE) is a technique for [Monte Carlo tree search](/monte-carlo-tree-search/) that gives each action at a node a second, fast estimate of its value: the mean outcome of all playouts through the node in which the action was played at any later turn, not only as the next move. This is the all-moves-as-first (AMAF) heuristic, which is older than RAVE; RAVE is its use at every node of the search tree. The AMAF estimate is biased but is backed by many more playouts, so the search blends it with the usual Monte Carlo estimate and moves the weight to the Monte Carlo estimate as the counts grow. Gelly and Silver introduced it in the Go program MoGo (2007) and described it in full in 2011.

## In plain words

Normal tree search only learns about a move when it tries that exact move at that exact position. In Go, a move that is good now is often also good a few turns later, because a stone on one side of the board rarely depends on a stone far away. So every time a random game is played, you can credit its result to every move your side made in it, at every position on the path where that move was possible. After a few games, each move already has many results.

These shared results are rough, because the move was played in a slightly different situation. So you use them a lot at first, when the exact results are few, and less and less as the exact results build up.

## When it applies

- The search is MCTS with playouts that run to the end of the game, so each playout produces a list of moves and one outcome.
- A move has an identity that keeps its meaning across nearby positions, such as a point on a Go, Hex or Havannah board. The AMAF value assumes that the value of a move is mostly the same in the whole subtree below a node.
- The branching factor is large, so the plain Monte Carlo estimate of each child would need many playouts before it is reliable.
- It does not apply well when the value of a move depends strongly on the moves before it, as in chess, where the same piece move can win or lose according to the rest of the board.

## The template

```pseudo id=main
SELECT(s)
L1  for each legal action a of s
L2    β ← SCHEDULE(N(s), N(s, a), Ñ(s, a)), a weight in [0, 1] that goes to 0 as N(s, a) grows
L3    Q*(s, a) ← (1 − β) Q(s, a) + β Q̃(s, a)
L4  return the action with the largest Q*(s, a), optionally plus a UCT bonus on N(s, a)

BACKUP(tree path s_0 a_0 … s_T a_T, playout moves a_{T+1} … a_D, outcome z)
L5  for t ← 0 to T
L6    N(s_t) ← N(s_t) + 1; N(s_t, a_t) ← N(s_t, a_t) + 1; move Q(s_t, a_t) toward z by 1/N(s_t, a_t)
L7    for each u ≥ t with u − t even, such that a_u is the first move at its point since t and is legal at s_t
L8      Ñ(s_t, a_u) ← Ñ(s_t, a_u) + 1; move Q̃(s_t, a_u) toward z by 1/Ñ(s_t, a_u)
```

Here $z$ is the outcome for the player to move at $s_t$, $Q$ and $N$ are the Monte Carlo statistics of MCTS, and $\tilde Q$ and $\tilde N$ are the AMAF statistics. Line L7 keeps only moves of the same player (the same parity as $t$), the first move at each point, and moves that are legal at $s_t$, as in Gelly and Silver (2011, Section 4.3). Line L7 includes $u = t$, so every Monte Carlo update is also an AMAF update.

Two schedules for line L2 are standard. The hand-selected schedule uses an equivalence parameter $k$,

$$\beta(s, a) = \sqrt{\frac{k}{3N(s) + k}},$$

which is $1/2$ when $N(s) = k$, the number of playouts at which both estimates get equal weight. The minimum MSE schedule picks $\beta$ to minimize the mean squared error of $Q^*$ under a model in which the outcomes are independent Bernoulli variables and the AMAF estimate has a constant bias $\tilde b$. In roughly even positions it is

$$\beta(s, a) = \frac{\tilde N}{N + \tilde N + 4 N \tilde N \tilde b^2}, \qquad N = N(s, a),\ \tilde N = \tilde N(s, a).$$

Both go to 0 as the counts grow. So in the limit $Q^*$ is the Monte Carlo value, and with a UCT bonus the asymptotic behavior is that of [UCT](/uct/).

## Classic examples

- **Go.** In MoGo the hand-selected schedule worked best with $k$ of 1000 or more, which means that the AMAF estimate was more reliable than the Monte Carlo estimate until several thousand playouts had gone through a node. With 3000 playouts per move against GnuGo, UCT-RAVE won between 50 and 60 percent of its games, according to $k$, against 24 percent for UCT without it (Gelly and Silver 2007). The minimum MSE schedule added about 80 Elo on the 9x9 board and more than 100 Elo on 19x19 (Gelly and Silver 2011, Table 1). With RAVE and heuristic prior knowledge, MoGo became the first program to reach dan level at 9x9 Go.
- **Hex and Havannah.** Gelly and Silver report that variants of heuristic MC-RAVE outperformed earlier search methods in [Hex](/hex-game/) and Havannah, games in which a move is a cell of the board and its value carries over well between nearby positions.
- **The history heuristic.** In alpha-beta search, the [history heuristic](/history-heuristic/) gives a move credit when it caused a cutoff anywhere in the tree and tries such moves first. RAVE is the best-first analogue: it shares the success of a move within a subtree, and it also counts the moves of the playouts outside the tree.
- **A key move hidden by bad luck.** The worked example below shows how AMAF finds a move whose own first tries lost, and how the two schedules differ.

### A worked example

At a node $s$ with Black to move, 10 playouts have gone through $s$. Black played $a$ first in 2 of them and lost both. Black played $b$ first in the other 8 and won 5, and in exactly those 5 wins Black also played $a$ later. Black played $b$ later in both games that started with $a$. The statistics are:

| action | N(s, a) | Q(s, a) | Ñ(s, a) | Q̃(s, a) |
|---|---|---|---|---|
| a | 2 | 0 | 7 | 5/7 = 0.714 |
| b | 8 | 0.625 | 10 | 0.5 |

Plain MCTS prefers $b$. With the hand-selected schedule and $k = 1000$, $\beta = \sqrt{1000/1030} = 0.985$, so $Q^*(a) = 0.704$ and $Q^*(b) = 0.502$, and the search tries $a$, the move that the wins have in common. With the minimum MSE schedule and $\tilde b = 0.1$, $\beta = 0.732$ for $a$ and $0.472$ for $b$, so $Q^*(a) = 0.523$ and $Q^*(b) = 0.566$: this schedule trusts the 8 direct results for $b$ more and keeps $b$ first for now. With the hand-selected schedule and $k = 1000$, the weight on AMAF is $0.5$ at $N(s) = 1000$, $0.32$ at $3000$ and $0.18$ at $10000$.

## Variations

- **AMAF without a tree.** Brügmann's program Gobble (1993) and later the programs of Bouzy and Helmstetter estimated each move of the root by the mean outcome of the random games in which it was played at any time. RAVE applies the same idea at every node of the tree.
- **Pure RAVE.** Selecting by $\tilde Q$ alone learns very fast but is often wrong in tactical positions, so it does not converge; MC-RAVE fixes this with the weight $\beta$.
- **UCT-RAVE.** An exploration bonus $c\sqrt{\log N(s)/N(s, a)}$ is added to $Q^*$. The first version of UCT-RAVE also put the AMAF count into the bonus, which Gelly and Silver later considered hard to justify, because AMAF already updates many actions whatever action is selected.
- **Ancestor statistics.** The AMAF values of ancestor nodes could also be used. Gelly and Silver tried this and saw no gain.
- **Heuristic priors.** A new node can start with $Q = \tilde Q = H(s, a)$ and with counts set to a confidence, the number of playouts that the heuristic is worth. This combines with RAVE in heuristic MC-RAVE (Gelly and Silver 2011, Algorithm 2).
- **Other AMAF variants.** The survey of Browne et al. lists variants that weight or cut off the later moves of a playout differently.

## Pitfalls

- **Bias in tactics.** The main assumption fails when a nearby move changes everything. Gelly and Silver give the example of a ladder breaker in one corner of a Go board, which changes the value of a ladder in the opposite corner. A schedule that keeps $\beta$ large for too long locks the search onto such moves.
- **Moves of the wrong player.** Only moves of the player to move at $s_t$ count for $s_t$. Mixing in the opponent's moves at the same point gives a meaningless value.
- **Repeated moves at a point.** In Go a point can be played again after a capture. Only the first move at a point after $s_t$ should be counted.
- **A schedule that does not go to 0.** A constant $\beta$ keeps the bias forever and loses the convergence of UCT.
- **Wrong scale of $k$ or $\tilde b$.** The best values depend on the game, the playout policy and the number of playouts per move. Tune them with matches, not with one position.
- **Memory.** Each node keeps $\tilde N$ and $\tilde Q$ for all legal actions, not only for its expanded children, which roughly doubles the size of a node.

## References
