---
tag: 73PV1J
kind: algorithm
slug: monte-carlo-tree-search
name: Monte Carlo tree search
aliases:
- MCTS
area: games-and-search/game-tree-search
level: advanced
summary: Builds a search tree with random playouts, selecting nodes by a bandit-style rule and backing up results.
model: real-ram
complexity:
  vars: {n: the number of playouts, b: the largest number of moves in a position, d: the depth of the stored tree, l: the length of a random playout}
  time: {worst: O(n (b d + l)), best: O(n (b d + l))}
  space: {extra: O(n b)}
properties: {randomized: true, anytime: true, iterative: true, approximate: true}
prereqs: [game-tree, minimax, multi-armed-bandit, monte-carlo-algorithm]
see_also: [uct, ucb1, rapid-action-value-estimation, rollout-algorithm, alpha-beta-pruning, evaluation-function, muzero, expectiminimax]
sources:
  - paper: doi:10.1007/978-3-540-75538-8_7
    title: "Rémi Coulom, Efficient selectivity and backup operators in Monte-Carlo tree search, Computers and Games (CG 2006), LNCS 4630, Springer, 2007, 72-83"
    locator: the name Monte Carlo tree search, the growth of the tree by one node per simulation, and the backup operators of Crazy Stone
  - paper: doi:10.1007/11871842_29
    title: "Levente Kocsis and Csaba Szepesvári, Bandit based Monte-Carlo planning, Machine Learning (ECML 2006), LNCS 4212, Springer, 2006, 282-293"
    locator: Section 2.3 (UCT, the UCB1 rule at each node of the tree) and Theorem 6 (convergence)
  - paper: doi:10.1109/TCIAIG.2012.2186810
    title: "Cameron B. Browne et al., A survey of Monte Carlo tree search methods, IEEE Transactions on Computational Intelligence and AI in Games 4(1) (2012), 1-43"
    locator: the four phases of selection, expansion, simulation and backpropagation, the tree and default policies, and the enhancements
  - paper: doi:10.1609/icaps.v20i1.13437
    title: "Raghuram Ramanujan, Ashish Sabharwal and Bart Selman, On adversarial search spaces and sampling-based planning, ICAPS 2010, 242-245"
    locator: shallow traps, positions where sampling methods do worse than minimax search
  - paper: arXiv:cs/0703062
    title: "Pierre-Arnaud Coquelin and Rémi Munos, Bandit algorithms for tree search, UAI 2007, 67-74"
    locator: the abstract and the analysis of UCT, whose regret can be of order exp(exp(D)) on trees of depth D
  - paper: doi:10.1038/nature16961
    title: "David Silver et al., Mastering the game of Go with deep neural networks and tree search, Nature 529 (2016), 484-489"
    locator: MCTS guided by a policy network and a value network (AlphaGo)
  - paper: doi:10.1126/science.aar6404
    title: "David Silver et al., A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play, Science 362(6419) (2018), 1140-1144"
    locator: MCTS with learned priors and values and no random playouts (AlphaZero)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 5 (the section on Monte Carlo tree search, its four steps and the UCT selection rule)
---

Monte Carlo tree search (MCTS) chooses a move in a game by playing many random games, called playouts, from the current position. It stores a tree of the positions it has visited, with the number of visits and the total result of each. Every playout first walks down the stored tree, where a bandit rule chooses moves that have done well or have been tried little. It then adds one new position to the tree, plays random moves to the end of the game, and adds the result to every position on the path. Good moves get more playouts, so the tree grows deep along the important lines. MCTS needs no evaluation function, only the rules of the game, and it can be stopped at any time.

## In plain words

Suppose you must pick a move in a game you cannot judge by looking at the board. You can still play the rest of the game randomly many times and count how often each move leads to a win. MCTS does this in a smarter way. It remembers the positions it has already played through. When it starts a new random game, it first follows the moves that won most often so far, but it also tries now and then the moves it has not tested much. Each new random game adds one more position to its memory. After many games, the move it played most often from the start is its choice.

## The problem

The input is a position $s_0$ of a two-player game with alternating moves and a finite game tree, given by its rules: the legal moves, the result of a move, and the payoff at the end, a number in $[0, 1]$ for player 0 (player 1 gets 1 minus it). The input also includes a budget of $n$ playouts. The output is a move at $s_0$. The goal is the [minimax](/minimax/) move, the move with the best value under optimal play by both players, but the tree is too large to search fully.

## The algorithm

```pseudo id=main
MCTS(s₀, n)
L1  create a root node for s₀ with all its moves untried
L2  repeat n times
L3    v ← root; s ← s₀
L4    while v has no untried move and has children: v ← the child c of v with the largest Q(c) + C·√(ln N(v) / N(c)); s ← the position of c
L5    if v has an untried move m: s ← play(s, m); add a child for m under v; v ← that child
L6    while s is not a final position: s ← play(s, a random legal move)
L7    r ← the payoff of s to player 0
L8    for v and every ancestor of v: N ← N + 1; W ← W + (r, or 1 − r if player 1 made the move into the node)
L9  return the move of the child of the root with the most visits
```

A node stores the visit count $N$ and the total reward $W$ of the player who made the move into it, and $Q = W/N$. Each iteration has the four phases of Browne et al.: **selection** (line L4), **expansion** (line L5), **simulation** (line L6, the *default policy*) and **backpropagation** (lines L7 and L8). The selection rule in line L4 is UCB1 applied at each node, which makes this version [UCT](/uct/), the most common one. The constant $C = \sqrt2$ fits rewards in $[0, 1]$. The tree grows by one node per playout, as in Coulom (2006). The implementation follows this pseudocode, with uniform random playouts.

## Example

**A trap for plain sampling.** In the tree below MAX moves first and MIN replies. Move A leads to the leaves $1, 1, 1, 0$, and move B to $1/2, 1/2$.

| root move | leaves after the reply of MIN | average of the leaves | minimax value |
|---|---|---|---|
| A | 1, 1, 1, 0 | 3/4 | 0 |
| B | 1/2, 1/2 | 1/2 | 1/2 |

Flat Monte Carlo, which only plays random games after each root move, prefers A (3/4 against 1/2) however many playouts it uses. MCTS stores the replies of MIN and learns that MIN answers A with 0. The implementation, with seed 0, gives:

| playouts | visits to A | mean of A | visits to B | mean of B | choice |
|---|---|---|---|---|---|
| 10 | 6 | 0.667 | 4 | 0.5 | A |
| 50 | 19 | 0.368 | 31 | 0.5 | B |
| 400 | 57 | 0.228 | 343 | 0.5 | B |

After 400 playouts, 44 of the 56 visits below A went to the reply 0, and the mean of A keeps falling toward its minimax value 0. With 50 playouts, MCTS chose B for all of the seeds 0 to 49, and flat Monte Carlo with 400 playouts chose A for all seeds tested.

**Nim.** In Nim with heaps $(2, 3, 4)$ the only winning move takes 3 from the heap of 4, since $2 \oplus 3 \oplus 1 = 0$ ([Nim](/nim/)). With 1000 playouts MCTS found it with 4 of 10 seeds, and with 3000 playouts with all 10. With heaps $(1, 2, 4)$, 1000 playouts were enough for all 10 seeds.

## Correctness

MCTS is a heuristic for a fixed budget, and with a small budget it can pick a bad move, as the table shows. The proof in [proofs/correctness.md](proofs/correctness.md) shows that it is consistent on a finite game tree with payoffs at the leaves: each iteration stops, the whole tree is stored after finitely many iterations, and from then on the search is deterministic. By induction on the height, every node is visited infinitely often, each child that is worse than the best for the player to move gets only $O(\log N)$ of the $N$ visits of its parent, and the mean $Q$ of every node converges to its minimax value. So the most visited child of the root is a minimax move once $n$ is large enough. Kocsis and Szepesvári (2006) give rates for UCT, including random payoffs (see [UCT](/uct/)).

## Complexity

**Time.** An iteration walks down at most $d$ stored levels, and at each it compares up to $b$ children, so selection costs $O(bd)$. Expansion costs $O(1)$ plus the move generation, the playout $O(l)$ moves, and the backup $O(d)$. In total $O(n(bd + l))$ for $n$ playouts. In practice the playouts dominate, and fast playouts matter more than fast tree code.

**Space.** One node per iteration, each with a list of up to $b$ untried moves or children: $O(nb)$. Programs that run long searches free the subtrees that can no longer be reached.

**Budget.** The number of playouts needed to find the minimax move depends on the game, not only on its size. The proof gives no bound, and Coquelin and Munos (2007) showed that UCT can be too optimistic, with a regret of order $\exp(\exp(D))$ on some trees of depth $D$, so the number of playouts needed can be enormous even for small trees.

## Properties

- **Anytime.** The search can stop after any number of playouts and return the current best move.
- **Asymmetric.** Promising lines are searched deeper than the others, unlike a fixed-depth [alpha-beta](/alpha-beta-pruning/) search.
- **No evaluation function needed.** Playouts to the end of the game give the payoffs. Learned value functions can replace them.
- **Randomized.** With a fixed seed the result is reproducible. Different seeds can give different moves when the budget is small.
- **Robust final move.** The most visited child is less noisy than the child with the best mean, which may have few visits.

## Variants and improvements

- **Tree policy.** UCB1 ([UCT](/uct/)) is the standard. PUCT adds a prior from a policy network to the bonus, as in AlphaGo and AlphaZero. Progressive widening adds children slowly when a node has many moves.
- **Shared statistics.** [Rapid action value estimation](/rapid-action-value-estimation/) shares the results of a move across positions, which helps when the tree is young, as in Go.
- **Better playouts.** Hand-made or learned playout policies, or no playouts at all: AlphaZero stops at the new node and uses a value network instead.
- **Solvers.** MCTS-Solver backs up proven wins and losses exactly, so that the search can prove results near the end of a game.
- **Chance and hidden information.** Chance nodes can be sampled as in [expectiminimax](/expectiminimax/) trees. For hidden information, information-set MCTS searches over information sets, but determinization has the errors described in [imperfect-information games](/imperfect-information-game/).
- **Parallel search.** Root, leaf and tree parallelism, with virtual loss to spread the threads over the tree.

## When to use it

Use MCTS when the game tree is large and no good evaluation function is known, as in Go before deep learning, in general game playing, and in many board and card games. It also works for planning in large Markov decision processes with a simulator. With learned policies and values it is the search of AlphaGo, AlphaZero and [MuZero](/muzero/). For games with strong tactical traps and a good evaluation function, such as chess with hand-made evaluation, [alpha-beta pruning](/alpha-beta-pruning/) has long been better.

## Pitfalls

- **Shallow traps.** A move that loses by force in a few moves can look good in random playouts (the example above). With a small budget MCTS can fall into such traps, which Ramanujan, Sabharwal and Selman (2010) studied in chess.
- **Rewards from the wrong side.** Each node must store the reward of the player who moved into it, or the selection must flip the sign at MIN nodes. Storing the reward of player 0 everywhere makes MIN choose its worst moves.
- **Choosing by the best mean.** A child with one lucky playout can have the best mean. Use the visit count, or require many visits.
- **Exploration constant.** $C$ must match the scale of the rewards. With payoffs in $\{-1, 0, 1\}$ instead of $[0, 1]$, the same $C$ explores half as much.
- **Biased playouts.** A playout policy that is strong but systematically wrong in some positions can lead the search away from the right move, and more playouts do not fix this.

## Implementations

## History

Abramson (1990) proposed judging positions by the expected outcome of random games, and Brügmann (1993) applied random games with simulated annealing to Go. Coulom (2006) combined random playouts with a growing tree and named the method Monte Carlo tree search; his program Crazy Stone won the 9x9 Go tournament at the 2006 Computer Olympiad. In the same year Kocsis and Szepesvári proposed UCT, which uses UCB1 in the tree and has a convergence proof, and Gelly and coworkers used it in MoGo. MCTS made programs much stronger at Go and was used for general game playing, Hex and many other games. The survey of Browne et al. (2012) fixed the description in four phases. AlphaGo (2016) combined MCTS with deep neural networks and beat a top professional player, and AlphaZero (2018) used the same search with no random playouts for chess, shogi and Go.

## References
