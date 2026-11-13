---
tag: WKCJ1X
kind: definition
slug: branching-factor
name: Branching factor
aliases:
- game tree branching factor
- out-degree of a search tree
area: games-and-search/game-tree-search
level: intro
summary: The number of legal moves at a node of a game tree; its average b over a game, with the game length d, gives the estimate b^d of the size of the tree.
prereqs: [game-tree]
see_also: [effective-branching-factor, search-tree, minimax, alpha-beta-pruning, knuth-moore-theorem, solved-game, monte-carlo-tree-search, move-ordering]
sources:
  - paper: doi:10.26481/dis.19940923la
    title: Louis Victor Allis, Searching for solutions in games and artificial intelligence, PhD thesis, University of Limburg, Maastricht (1994)
    locator: Section 6.2.4 (game-tree complexity as b^d with the average branching factor) and Sections 6.3.2, 6.3.9 and 6.3.12 (the estimates for Connect Four, chess and Go)
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (about 30 legal moves in a typical chess position, about 10^3 for a move of each side, and the estimate of 10^120 games)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Sections 5.2 and 5.3 (the cost O(b^m) of minimax, and the effect of move ordering on alpha-beta)
---

The *branching factor* of a node in a [game tree](/game-tree/) is its number of children, that is, the number of legal moves of the player to move. The branching factor of a game is a typical value of this number, written $b$, and with the length $d$ of a game in plies it gives the estimate $b^d$ for the number of leaves of the game tree. It is the main parameter of the cost of every game-tree search: [minimax](/minimax/) evaluates $b^d$ leaves, and [alpha-beta pruning](/alpha-beta-pruning/) with perfect move ordering about $b^{d/2}$. The same word in single-agent search, and the effective branching factor of a search run, are defined on [search tree](/search-tree/) and [effective branching factor](/effective-branching-factor/).

## Definition

Let $T$ be a game tree and let $n$ be a node. The **branching factor** $b(n)$ of $n$ is the number of children of $n$, which is 0 for a terminal node. For a whole tree, several numbers are in use, and a page or a paper must say which one it means.

- **Uniform.** In the model tree of the analysis, every inner node has the same branching factor $b$ and every leaf is at depth $d$, so the tree has $b^d$ leaves. Cost bounds such as $O(b^d)$ are for this model.
- **Largest.** The largest $b(n)$ over the nodes. This is the one that [search tree](/search-tree/) uses for worst-case bounds.
- **Average over the inner nodes of the tree.** The number of edges divided by the number of inner nodes.
- **Average over the positions.** The average number of legal moves over the positions that can arise, each position counted once. This is closer to what a player sees in a typical position.
- **Average over a game.** The $b$ for which $b^d$ equals the number of games of length $d$, a geometric mean of the branching factors along the games. Allis (1994) estimates game-tree complexity as $b^d$ with $b$ the average branching factor and $d$ the average game length.

The averages differ because the game tree counts a position once per history that reaches it, and positions near the end of the game, with few moves, are reached by many histories.

## Examples and non-examples

**Tic-tac-toe.** A move is any empty square, so the player to move at ply $i$ has $9 - i$ moves until the game ends. The averages are far apart.

| measure | value |
| --- | --- |
| largest | 9, at the root |
| average over the 294,778 inner nodes of the tree (549,945 edges) | 1.8656 |
| average over the 4,520 positions that are not over (16,167 moves) | 3.577 |
| average game length | 8.25 plies |

The tree average is low because most inner nodes are deep in the tree, at plies 7 and 8, where only one or two squares are empty. The tests of [solved game](/solved-game/) compute these counts by a full walk of the tree and of the positions.

**Chess.** The start position has 20 legal moves. Shannon (1950) wrote that a typical position has about 30 legal moves, so about $10^3$ choices for a move of each side, and from games of 40 move pairs he estimated about $10^{120}$ games. Allis (1994) used $b = 35$ and 80 plies, which gives $35^{80} \approx 10^{123}$. These are estimates of the average, not counts.

**Go.** On the $19 \times 19$ board the first move has 361 choices. Allis used $b = 250$ and 150 plies, for a game-tree complexity of about $10^{360}$. The large $b$ is one reason why full-width alpha-beta search was weak in Go and [Monte Carlo tree search](/monte-carlo-tree-search/) took its place.

**Connect Four.** Seven columns, but full columns are not moves. Allis used $b = 4$ and 36 plies, about $10^{21}$.

**Non-example: the effective branching factor.** For a search that generates $N$ nodes to depth $d$, the [effective branching factor](/effective-branching-factor/) $b^*$ is defined by $N + 1 = 1 + b^* + (b^*)^2 + \cdots + (b^*)^d$. It measures the search, not the game. For alpha-beta with perfect move ordering, $b^*$ is close to $b^{1/2}$, though the game has branching factor $b$.

**Non-example: the number of positions.** The state-space complexity of a game counts positions, not histories. Tic-tac-toe has 5,478 reachable positions, far fewer than the $b^d$ estimate of its tree.

## Related definitions

- [Game tree](/game-tree/): the tree whose nodes have these branching factors.
- [Search tree](/search-tree/): the same notion for single-agent search, with the largest branching factor as the default.
- [Effective branching factor](/effective-branching-factor/): the measure of the work of a search, as above.
- [Knuth-Moore theorem](/knuth-moore-theorem/): in a uniform tree, alpha-beta must evaluate $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, so the best case halves the exponent.
- [Solved game](/solved-game/): whether a game can be solved depends on $b^d$ and on the number of positions.

## References
