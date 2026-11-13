---
tag: Q2C8WC
kind: technique
slug: null-move-pruning
name: Null-move pruning
aliases:
- null move heuristic
area: games-and-search/game-tree-search
level: advanced
summary: Prunes a node when even passing the move to the opponent still leaves a position good enough to cause a cutoff.
prereqs: [alpha-beta-pruning, evaluation-function, pruning]
see_also: [futility-pruning, late-move-reductions, search-extensions, quiescence-search, transposition-table, zobrist-hashing, principal-variation-search, horizon-effect]
sources:
  - paper: "Don F. Beal, Experiments with the null move, in D. F. Beal (editor), Advances in Computer Chess 5 (1989)"
    locator: pp. 65 to 79 (the null move as a way to bound the value of a position)
  - paper: doi:10.1007/978-1-4613-9080-0_9
    title: Gordon Goetsch and Murray S. Campbell, Experiments with the null-move heuristic, in T. Anthony Marsland and Jonathan Schaeffer (editors), Computers, Chess, and Cognition, Springer (1990)
    locator: pp. 159 to 168 (experiments with null-move pruning at a reduced depth in a chess program)
  - paper: "Chrilly Donninger, Null move and deep search, Selective-search heuristics for obtuse chess programs, ICCA Journal 16(3) (1993)"
    locator: pp. 137 to 143 (null moves searched recursively with a depth reduction R, and the choice R = 2)
  - paper: doi:10.3233/ICG-1999-22302
    title: Ernst A. Heinz, Adaptive null-move pruning, ICCA Journal 22(3) (1999)
    locator: pp. 123 to 132 (a reduction R = 3 at large remaining depths and R = 2 at small ones, tested in the program DarkThought)
  - paper: doi:10.3233/ICG-2002-25305
    title: Omid David-Tabibi and Nathan S. Netanyahu, Verified null-move pruning, ICGA Journal 25(3) (2002)
    locator: pp. 153 to 161 (on a fail high, go on with the depth reduced by one ply and search again at full depth if no cutoff follows; R = 3)
---

Null-move pruning is a forward pruning heuristic for [alpha-beta](/alpha-beta-pruning/) search in games such as chess. Before the moves of a node are searched, the side to move *passes*: it makes a "null move", which is not legal in the game, and the opponent then moves twice in a row. This null-move position is searched to a depth reduced by $R$ plies, usually 2 or 3, with a null window just below $\beta$. If even after a free move for the opponent the result is at least $\beta$, the node is cut off without a search of its real moves. The idea rests on the *null-move observation*: in most positions the right to move is worth something, so a real move scores at least as well as a pass. The observation is false in *zugzwang*, where every legal move makes the position worse, and there null-move pruning returns wrong values. It is a heuristic with this known failure case, not a sound pruning rule.

## In plain words

Suppose it is your turn and your position is already so good that the opponent will avoid it. A program wants to know this quickly, so that it can stop thinking about the position.

The trick is to let the opponent move twice. You skip your turn, and the opponent gets a free move. If your position is still good enough after the free move, then a real move from you will almost surely be even better, so the program stops here.

The free-move search is also done with less depth, so it is cheap. Most of the time this saves a lot of work.

It goes wrong in positions where any move you make hurts you, and you would rather skip your turn. Then the free-move test lies.

## When it applies

- The game is one where having the move is usually an advantage, as in chess and shogi. It is a bad fit for games and endgames in which zugzwang is common.
- The search uses [alpha-beta](/alpha-beta-pruning/) with windows, so that a node can fail high at $\beta$.
- The position can be "passed" cheaply: switch the side to move, clear the en passant square, and update the [Zobrist hash](/zobrist-hashing/) key for the side to move.
- The remaining depth is at least $R + 1$, so that the reduced search has depth 0 or more.

## The template

The search is fail-soft negamax alpha-beta, with values for the side to move. NULL($n$) is the position after a pass.

```pseudo
SEARCH(n, d, α, β, null_ok)
    if n is terminal or d = 0 then return QUIESCE(n, α, β) or EVALUATE(n)
    if null_ok and d ≥ R + 1 and not in check and EVALUATE(n) ≥ β then
        t ← −SEARCH(NULL(n), d − 1 − R, −β, −β + 1, false)    ▷ null window, no second pass
        if t ≥ β then return t                                ▷ cut off on the null move
    m ← −∞
    for each move to a child c of n do
        t ← −SEARCH(c, d − 1, −β, −max(m, α), true)
        m ← max(m, t)
        if m ≥ β then return m
    return m
```

The test EVALUATE($n$) $\ge \beta$ is common practice: if the static score is below $\beta$, the pass is unlikely to reach $\beta$, and the null search is wasted. The ban on two null moves in a row keeps the search from passing twice, which would just give back the same position with less depth.

**Verified null-move pruning** (David-Tabibi and Netanyahu 2002) changes the cutoff. In a subtree marked "verify", a fail high on the null move does not return. The node is instead searched with depth $d - 1$, and the verify mark is turned off below it. If that search does not fail high, a zugzwang is suspected, and the node is searched again at depth $d$.

## Classic examples

**A zugzwang that is cut off.** White moves at R. The move "quiet" is searched first and is worth $+1$. The move "zug" leaves Black in zugzwang: each of the two Black moves loses 5 points, but if Black could pass, the score would stay 0. With depth 4 and $R = 2$, the search of "zug" has the window $(-\infty, -1)$ for Black, the static score 0 is at least $\beta = -1$, and the null-move search returns 0 for Black, at least $\beta$. So "zug" is cut off and the root returns $+1$. The true value, which plain alpha-beta returns, is $+5$. Verified null-move pruning searches "zug" again after the reduced search fails low, and returns $+5$.

**Measured on random trees.** The tests use 200 lazy random game trees from the seeds 10000 to 10199 (Python's `random.Random`, seeded per node), with branching factor 4 and height 7, moves ordered by their static score, and scores that change by $-4$ to $+4$ at each move. Each tree is searched to depth 7.

| search | nodes visited, all 200 trees | root value equal to plain alpha-beta |
| --- | --- | --- |
| plain alpha-beta | 163,755 | 200 of 200 |
| null move, $R = 2$ | 70,499 | 173 of 200 |
| verified null move, $R = 3$ | 101,630 | 136 of 200 |

These random trees have no rule that the move is worth something, so the null-move observation is often false in them, and the values change in many trees. In chess programs the change is much rarer, but we do not have a measured rate from a source we have checked. The verified search here also differs in many trees, because its reduced-depth search after a null fail high is a different search, and this table measures agreement with plain alpha-beta, not with the true value of the game.

**Chess programs.** Beal (1989) studied the null move as a bound on the value of a position. Goetsch and Campbell (1990) tested null-move pruning with a reduced depth in a chess program. Donninger (1993) searched null moves recursively, with $R = 2$. Heinz (1999) made $R$ depend on the remaining depth.

## Variations

- **Adaptive $R$.** Heinz (1999) uses $R = 3$ when much depth is left and $R = 2$ near the leaves. He reports that the search tree in his program DarkThought was 10 to 30% smaller than with the standard null move.
- **Verified null move.** David-Tabibi and Netanyahu (2002) give the verification above, with $R = 3$. It costs more nodes than the plain null move and catches many zugzwang positions.
- **Zugzwang guards.** Programs often turn the null move off when the side to move has only a king and pawns, because zugzwang is common in such endgames.
- **Mate threat detection.** If the null-move search returns a mate score against the side to move, the position has a strong threat, and a program may [extend](/search-extensions/) the search instead of pruning.
- **Null-move quiescence.** Beal (1990) uses null moves inside the [quiescence search](/quiescence-search/), so that the stand-pat score is checked against threats.

## Pitfalls

- **Zugzwang.** The method returns a wrong value when a pass would be the best move. The example above shows this. In chess this happens mainly in endgames, but it can happen in the middle game too.
- **Positions in check.** A pass from check would leave the king in check, which is not a legal position. Never try the null move in check.
- **Two passes in a row.** Without the ban, the search passes twice and searches the same position with less depth, which wastes nodes and can hide threats.
- **Hash keys.** The null move changes the side to move, so the hash key must change. A [transposition table](/transposition-table/) entry stored from a null-move search must not be used as a real move.
- **Repetition.** A null move is not a move of the game. A draw by repetition test that counts positions across a null move can find false repetitions.
- **Claims of strength.** The gain of null-move pruning depends on the program, the game and the other methods used. Do not take a node count or rating gain from one program as true for another.

## Exercises

1. In the zugzwang example, find the smallest search depth with $R = 2$ at which the null move is tried at the node "zug". *Hint.* The node needs $d \ge R + 1$.
2. Show that if the null-move observation holds at every node, that is, the value of $n$ is at least the value of NULL($n$) at the same depth, and if the reduced search returned the full-depth value, then null-move pruning never changes the root value. Explain why the reduced depth breaks the proof.
3. Write the zugzwang guard that turns the null move off when the side to move has no pieces other than king and pawns, and build a king and pawn position where it matters.
4. Modify the template so that it returns $\beta$ instead of $t$ on a null-move cutoff. Which bound is lost?
5. Count the nodes of a null-move search on a uniform tree of branching factor $b$ in which every null move fails high, as a function of $d$, $b$ and $R$.

## References
