---
tag: 42DKME
kind: technique
slug: search-extensions
name: Search extensions
aliases:
- check extensions
area: games-and-search/game-tree-search
level: advanced
summary: Searches certain forcing lines, such as checks, one ply deeper than the nominal depth.
prereqs: [alpha-beta-pruning, horizon-effect]
see_also: [quiescence-search, late-move-reductions, null-move-pruning, iterative-deepening-search, principal-variation-search, transposition-table, move-ordering]
sources:
  - paper: doi:10.1016/0004-3702(90)90073-9
    title: Thomas Anantharaman, Murray S. Campbell and Feng-hsiung Hsu, Singular extensions, Adding selectivity to brute-force searching, Artificial Intelligence 43(1) (1990)
    locator: pp. 99 to 109 (the definition of a singular move, the test with a margin and a reduced window, and the experiments with the program ChipTest)
  - paper: doi:10.3233/ICG-1988-11402
    title: Thomas Anantharaman, Murray S. Campbell and Feng-hsiung Hsu, Singular extensions, Adding selectivity to brute-force searching, ICCA Journal 11(4) (1988)
    locator: pp. 135 to 143 (the earlier version of the same paper)
  - url: https://apps.dtic.mil/sti/tr/pdf/AD0784881.pdf
    title: Hans J. Berliner, Chess as Problem Solving, The Development of a Tactics Analyzer, PhD thesis, Carnegie-Mellon University (1974)
    locator: the chapter on the horizon effect (why a fixed depth fails on forcing lines)
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the type B strategy, which follows forceful variations such as checks and captures further than the other moves)
---

A search extension is a rule that lets a depth-limited game search go deeper on some lines than on others. When a move is *forcing*, for example a check, a recapture, or the only legal reply, the search gives the move to the next ply without using up one ply of the depth budget. The forcing line then costs almost nothing, because each extended node has few moves, but the search sees its end. Extensions are the counterpart of [late move reductions](/late-move-reductions/) and of the other forward pruning methods, which make the depth smaller on lines that look bad. Both turn a uniform depth into a depth that depends on the line. A total budget of extensions on each path keeps the search finite.

## In plain words

A chess program looks a fixed number of moves ahead. Some lines are like a narrow corridor: after a check, the other side often has only one or two moves. Such a line costs almost no work to follow, and its end is often a mate or the loss of a piece.

An extension says: this move was forced, so do not count it. The program follows the corridor further and sees what is at its end, while the wide parts of the tree keep the normal depth.

The rule needs a limit. A series of checks can go on for ever, so each line may only be extended a few times.

## When it applies

- The game has moves that cut the choices of the opponent to one or a few, such as check in chess or shogi, or a capture that must be taken back.
- The search is depth-limited, so it suffers from the [horizon effect](/horizon-effect/) on these forcing lines.
- The program can test the forcing condition cheaply when it makes the move, for example "is the opponent in check" or "does this capture take back on the square of the last capture".
- A total extension budget, or a rule that the extensions on a path add up to less than the depth, can be enforced.

## The template

The extension is a function EXTENSION($n$, $c$) that returns how many extra plies the move from $n$ to $c$ gets, usually 0 or 1. The search keeps the extension used on the current path, so that the total stays at most $E$.

```pseudo
SEARCH(n, d, α, β, e)                       ▷ e = extension budget left on this path
    if n is terminal or d = 0 then return QUIESCE(n, α, β) or EVALUATE(n)
    m ← −∞
    for each move to a child c of n do
        x ← min(EXTENSION(n, c), e)          ▷ 1 for a check, a one-reply move, ...
        t ← −SEARCH(c, d − 1 + x, −β, −max(m, α), e − x)
        m ← max(m, t)
        if m ≥ β then return m
    return m
```

The test code uses the *one-reply* extension: EXTENSION($n$, $c$) $= 1$ if the side to move at $c$ has exactly one legal move. A check that leaves one reply is the typical case.

**What the template computes.** With the one-reply extension, the search returns the value of a fixed-depth search in which a move into a one-reply position costs no depth, until the budget is spent. The tests check this against a plain recursive solver with the same rule, on 500 random trees in which 30% of the nodes have one move, with depths 1 to 3 and budgets 0 to 3, with the full window and with a random window.

**Forced lines past the horizon.** The tests build trees of depth 2 with branching factor 3, in which each node at depth 2 starts a forced line of $k$ moves, with $k$ from 1 to 4, and in which the static score changes by up to 9 points at each move. On 600 such trees from the seed 31:

- the depth-2 search with budget $k$ returns the exact value of the whole tree, which is also the value of a full search to depth $2 + k$;
- with a budget $E < k$ it returns the value of a full search to depth $2 + E$, so the budget decides how far past the horizon it sees;
- without extensions the depth-2 value was wrong in 556 of the 600 trees.

A single forced line of 50 moves shows the budget at work: a depth-1 search with budget 5 visits 7 nodes and stops.

## Classic examples

- **Check extension.** Extend a move that gives check. In chess the side in check has few legal moves, so the extended node is cheap, and many mates and wins of material start with a series of checks. It is the most common extension in chess programs.
- **One-reply extension.** Extend when the side to move has a single legal move. The node then costs one move, so the extension costs almost nothing.
- **Recapture extension.** Extend a capture that takes back on the square where the opponent just captured, so that an exchange is seen to its end at the frontier.
- **Passed pawn extension.** Extend a pawn move to the seventh rank, because a promotion just past the horizon changes the value by a queen.
- **Singular extension.** Anantharaman, Campbell and Hsu (1988, 1990) extend a move that is much better than all its siblings. The test searches the other moves with a reduced depth and a window just below the value of the best move minus a margin. If all of them fail low, the best move is *singular* and is searched one ply deeper. The idea does not depend on knowledge of chess. The paper tests it in the program ChipTest.
- **Mate threat extension.** Extend when a [null move](/null-move-pruning/) search shows that the side to move would be mated if it passed, so the position has a strong threat.

## Variations

- **Fractional plies.** Count the depth in fractions of a ply, and give each kind of extension a weight, such as 3/4 of a ply for a check. Two weak signals then add up to one ply. This is engine practice; we have not seen a primary source that states the weights.
- **Budget rules.** Some programs limit the total extension on a path to a fixed number of plies. Others allow an extension only while the path is shorter than twice the nominal depth.
- **Extensions and reductions together.** The same move loop that extends forcing moves can reduce late quiet moves, as in [late move reductions](/late-move-reductions/). The two work against each other on a few moves, and a move that is extended is normally not reduced.
- **Extensions in quiescence.** [Quiescence search](/quiescence-search/) is the limit case: below the frontier only captures are searched, without a depth count.

## Pitfalls

- **No budget.** A series of checks can be long, and in games with repetition it can be infinite, as in a perpetual check. Without a budget the search may not finish. With the depth counted per path, the bound is that a path has at most $d + E$ moves.
- **Too many extensions.** Each extension multiplies the size of the subtree by the branching factor below it. Extensions on moves that are not really forcing, such as all captures, make the search slower than one more ply of plain search.
- **Search instability.** With a [transposition table](/transposition-table/), the same position can be reached with and without an extension, so its stored depth is not the depth that the line had. The stored value can then be from a shallower or deeper search than the caller expects.
- **Singular test cost.** The singular test is a search of all siblings. It pays only at nodes that are expected to be important, such as nodes on the [principal variation](/principal-variation/) or nodes with a good table entry.
- **Measured gains.** The value of each extension depends on the program and on the other methods in it. Do not carry a gain measured in one program over to another.

## Exercises

1. Show that with the one-reply extension and a budget $E$ per path, the search makes at most $d + E$ moves on any path. *Hint.* Each move changes $d$ to $d - 1 + x$ and $e$ to $e - x$, so it lowers $d + e$ by exactly 1, and the search stops before $d$ becomes negative.
2. Take a tree of depth $d$ in which each node at depth $d$ starts a forced line of $k$ moves. Show that the extended search with budget $E \le k$ equals a plain search to depth $d + E$. *Hint.* Only the moves below depth $d$ are extended.
3. A program extends every capture by one ply, and in its test positions a node has 4 captures on average. Estimate how the size of the tree grows with the depth, compared with a program that does not extend captures.
4. Write the singular extension test as a call to SEARCH with a null window, and explain why the test can use a reduced depth.
5. Build a small game with a cycle, such as a king that can give check for ever, and show that the search without a budget does not stop.

## References
