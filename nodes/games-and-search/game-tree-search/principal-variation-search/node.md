---
tag: HEBCKY
kind: algorithm
slug: principal-variation-search
name: Principal variation search
aliases:
- NegaScout
area: games-and-search/game-tree-search
level: advanced
summary: Alpha-beta that searches the first move with the full window and each later move with a null window, to test that it is not better. Only a move that fails the test is searched again.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies}
  time: {worst: O(d b^d), best: O(b^(d/2))}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [scout-search, principal-variation]
see_also: [aspiration-search, mtdf, transposition-table, move-ordering, iterative-deepening-search, knuth-moore-theorem, late-move-reductions, sss-star]
sources:
  - paper: doi:10.1145/356893.356895
    title: T. A. Marsland and M. Campbell, Parallel search of strongly ordered game trees, ACM Computing Surveys 14(4) (1982)
    locator: pp. 533 to 551; the sections on the minimal tree and on principal variation search with null windows
  - paper: doi:10.3233/icg-1983-6402
    title: Alexander Reinefeld, An improvement to the Scout tree search algorithm, ICCA Journal 6(4) (1983)
    locator: pp. 4 to 14 (NegaScout in negamax form, with the re-search after a failed null-window test)
  - paper: doi:10.1016/0004-3702(83)90001-2
    title: Murray S. Campbell and T. Anthony Marsland, A comparison of minimax tree search algorithms, Artificial Intelligence 20(4) (1983)
    locator: pp. 347 to 367 (PVS compared with alpha-beta, SCOUT and SSS* on strongly ordered trees)
  - paper: "Judea Pearl, SCOUT: a simple game-searching algorithm with proven optimal properties, Proceedings of the First Annual National Conference on Artificial Intelligence (AAAI-80), Stanford (1980)"
    title: Pearl 1980, AAAI
    locator: pp. 143 to 145 (TEST and EVAL, the procedures that PVS merges into one)
  - paper: doi:10.1016/0004-3702(95)00126-3
    title: Aske Plaat, Jonathan Schaeffer, Wim Pijls and Arie de Bruin, Best-first fixed-depth minimax algorithms, Artificial Intelligence 87(1-2) (1996)
    locator: pp. 255 to 293 (NegaScout with a transposition table as the reference in the experiments with MTD(f))
---

Principal variation search, or PVS, is a form of [alpha-beta](/alpha-beta-pruning/) that bets on its [move ordering](/move-ordering/). At each node it searches the first move with the full window $(\alpha, \beta)$. It searches every later move with a *null window* $(a, a + g)$ just above the best score $a$ so far, where $g$ is the smallest step between two values. A null-window search cannot find a value. It answers only "is this move better than $a$?", and it prunes much more than a full search. If the answer is no, as it usually is when the first move is best, the move is done. If the answer is yes, the move is searched again with the window $(t, \beta)$ to find its value. The result is the same as alpha-beta, with the same bounds when a window is given. With good ordering, PVS visits fewer nodes, and it is the main search of most alpha-beta chess programs. It is the negamax form of [SCOUT](/scout-search/) with the test and the search merged into one procedure, and Reinefeld called it NegaScout. The name comes from the nodes on the expected [principal variation](/principal-variation/): they are the only ones that get a full window.

## In plain words

You trust your move ordering. The first move at each position is probably the best one, so you search it properly.

For each other move, you ask a cheap question: "is this one better than what I have?". You ask it with the narrowest possible range, just above your best score. In such a narrow range, almost every branch is cut off at once, so the answer comes fast.

If the answer is no, which is the usual case, you go on. If the answer is yes, you were wrong about the order. You search that move properly, and it becomes the move to beat.

The answer is the same as plain alpha-beta. You win when your ordering is good and lose a little when it is bad.

## The problem

The input is as on the [alpha-beta](/alpha-beta-pruning/) page: a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/), an EVALUATE function for the side to move, and a window $(\alpha, \beta)$ with $\alpha < \beta$. In addition there is a grain $g > 0$, the width of a null window. For integer scores $g = 1$. The output $r$ satisfies the conditions of fail-soft alpha-beta for the [negamax](/negamax/) value $N(n)$:
- if $r \le \alpha$ then $N(n) \le r$,
- if $\alpha < r < \beta$ then $r = N(n)$,
- if $r \ge \beta$ then $N(n) \ge r$.

With the full window the result is the value of the root, the [game tree evaluation](/game-tree-evaluation/) problem.

## The algorithm

```pseudo id=main
PVS(n, α, β)
L1  if n is terminal then return EVALUATE(n)
L2  m ← −PVS(c₁, −β, −α)               ▷ the first child: full window
L3  if m ≥ β then return m
L4  for each later child c of n, in order, do
L5      a ← max(α, m)
L6      t ← −PVS(c, −a − g, −a)          ▷ null window (a, a + g): is c better than a?
L7      if a < t < β and c is not terminal then
L8          t ← −PVS(c, −β, −t)          ▷ yes: search again for the value
L9      if t > m then m ← t
L10     if m ≥ β then return m
L11 return m
```

A null-window search at line L6 has three outcomes. If $t \le a$, the move is not better than $a$, and $t$ is an upper bound on its score. If $t \ge a + g$, the move is better, and $t$ is a lower bound on its score. If $t$ is strictly between $a$ and $a + g$, it is the exact score; this happens only when the grain is too coarse for the values.

The re-search at line L8 is needed only when the test says "better" and the bound $t$ is still below $\beta$. If $t \ge \beta$, the move already causes a cutoff, and line L10 returns. The re-search starts from $t$ and not from $a$, since the score of the move is known to be at least $t$. A terminal child returns an exact value at once, so it needs no re-search.

The grain must not be larger than the step between two values, or the null window holds values strictly inside it and prunes less. It is still correct for every $g > 0$. With integer scores $g = 1$, and the window $(a, a + 1)$ is the usual "null window" $(\alpha, \alpha + 1)$ of chess programs.

## Example

Take the tree of the [alpha-beta](/alpha-beta-pruning/) page. MAX is at the root A, MIN at B and C, and MAX at D, E, F and G. The leaves, as values for MAX, are 3 and 17 under D, 19 and 12 under E, 2 and 5 under G, and 15 and 25 under F. The children are in the order B, C at A, D, E at B and G, F at C.

| node | window | what happens | leaves |
| --- | --- | --- | --- |
| D | full | first child of B, first child of A: full search, value 17 | 3, 17 |
| E | null window at 17 for MIN | is E below 17? the leaf 19 says no | 19 |
| B | full | value 17 | |
| C | null window at 17 for MAX | is C above 17? G is at most 5, so no | 2, 5 |
| A | full | value 17 | |

PVS evaluates 5 leaves, the same leaves as alpha-beta, because the first move at each node is best. Now swap D and E, so that B tries E first. E gets the full window and is worth 19. The test of D with the null window at 19 says that D is below 19, so for MIN at B it is better, and D is searched again for its value, 17. The leaves 3 and 17 are evaluated twice, and the search makes 8 leaf evaluations in all. The tests check both runs.

In tic-tac-toe from the empty board, with the squares tried in reading order, PVS evaluates 6825 terminal positions, with 3 re-searches, and alpha-beta evaluates 7330. On 200 uniform trees with 4 children and depth 6 with random integer leaves, PVS made 181773 leaf evaluations and alpha-beta 165316: with random order the re-searches cost more than the null windows save. With the best move first on the same kind of trees, both made exactly 127 per tree, which is $4^3 + 4^3 - 1$, with no re-search.

## Correctness

The [proof](proofs/correctness/) shows that PVS satisfies the three conditions of fail-soft alpha-beta, by induction on the height. The core is a claim about one later child: after lines L6 to L8, the value $t$ is an upper bound on the score of the move if $t \le a$, its exact score if $a < t < \beta$, and a lower bound if $t \ge \beta$. This is what alpha-beta gets from one search with the window $(a, \beta)$, so the rest of the alpha-beta proof goes through. The grain plays no part in the proof. The proof also shows that when the first move at every node is best, no re-search happens.

The tests compare PVS with negamax on random uniform and irregular trees with integer and fraction leaves, with and without a depth limit, with the grain $1/60$ for leaves $p/q$ with $q \le 6$, and with grains that are too coarse or too fine. They check the three bounds for random windows, tic-tac-toe positions, the two runs of the example, and that with the best move first PVS evaluates the same leaves as alpha-beta, in the same order, with no re-search.

## Complexity

Costs are in the [word RAM](/word-ram/), with each move generation and EVALUATE counted as $O(1)$, on a uniform tree of branching factor $b$ and depth $d$, with all values multiples of the grain.

**Best case.** If the first move at every node is best, no re-search happens, and PVS evaluates the minimal tree of the [Knuth-Moore theorem](/knuth-moore-theorem/), $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, the same as alpha-beta. So the time is $O(b^{d/2})$.

**Worst case.** A null-window search with $a$ a multiple of the grain never re-searches inside, so it is an alpha-beta search and visits at most the $b^h$ leaves below its node. If every later move passes its test, a node of height $h$ costs $T(h) \le b\,T(h-1) + (b-1)\,b^{h-1}$, so $T(d) \le b^d(1 + d(b-1)/b)$, which is $O(d\, b^d)$. This is worse than alpha-beta, which never evaluates a leaf twice.

**In practice.** With the good [move ordering](/move-ordering/) of a real program, the first move is best at most nodes, so re-searches are rare and the null windows prune much more than alpha-beta. Campbell and Marsland compared PVS with alpha-beta on strongly ordered trees, the kind that real programs make. With poor order the re-searches cost more than the null windows save, as in the random trees of the example.

**Space.** The current path only: $O(bd)$ with a list of children per call.

## Properties

- **The same result as alpha-beta.** With any window it returns the value or a bound of the same kind as fail-soft alpha-beta. With the full window it returns the value.
- **Depends on the order.** More than alpha-beta: with good order it visits fewer nodes, and with bad order more.
- **Fail-soft.** The fail-soft form gives a tight bound $t$ from the test, so the re-search at line L8 starts higher. With a fail-hard search, $t$ is only $a + g$, and the test gives the re-search nothing more.
- **A principal variation for free.** The nodes that get a full window are the nodes of the expected [principal variation](/principal-variation/). If a test fails, the new line becomes the principal variation.
- **Small memory.** Only the current path, like alpha-beta.

## Variants and improvements

- **[Transposition table](/transposition-table/).** A re-search visits the same subtree again. With a table, it reuses the bounds and the best moves of the null-window search, so the second search is much cheaper. All real programs use one.
- **No re-search near the leaves.** If the child $c$ has only terminal children, its fail-soft null-window result is exact whenever the test says "better": a fail high for $n$ is a fail low at $c$, so $c$ searched all its children and found its value. Then line L8 can be skipped for such children too.
- **[Aspiration search](/aspiration-search/) at the root.** The full window at the root is often replaced by a narrow window around the value of the last iteration.
- **[Late move reductions](/late-move-reductions/).** Later moves get a null-window search to a smaller depth first, and a full-depth search only if it says "better". This builds on the null window of PVS and can change the result.
- **[MTD(f)](/mtdf/).** Only null-window searches, at the root too, with a [transposition table](/transposition-table/) to keep the results.
- **NegaScout and PVS.** Reinefeld's NegaScout and the PVS of Marsland and Campbell differ in small details, such as the window of the re-search and when it can be skipped. The names are now used for the same idea.

## When to use it

Use PVS as the main search of a game program with good move ordering: a move from the [transposition table](/transposition-table/), then captures, [killer moves](/killer-heuristic/) and the [history heuristic](/history-heuristic/). Use it with [iterative deepening](/iterative-deepening-search/), whose last principal variation gives the first moves. With poor ordering, or no way to order the moves at all, plain alpha-beta is often as good or better.

## Pitfalls

- **The grain.** With integer scores the null window is $(a, a + 1)$. With fractional scores, a null window of width 1 lets values inside it and wastes pruning; use the true step of the scores.
- **The re-search condition.** Re-search only if $a < t < \beta$. If $t \ge \beta$, the move already gives a cutoff and needs no re-search. If $t \le a$, the move is not better.
- **The re-search window.** Start the re-search from $t$ or from $a$, never from above $t$. The score is only known to be at least $t$, so a window that starts higher can miss it.
- **Search instability.** With a transposition table or with pruning that depends on the window, a null-window search can say "better" and the re-search can then fail low. A program must then keep the old best move, or the bound from the test, and not trust the new low value.
- **The root.** At the root, a move that passes its test becomes the new best move only after the re-search. Programs short of time sometimes play it at once.
- **Terminal children.** A terminal child returns its exact value, so a re-search of a terminal child is wasted work.

## Implementations

## History

Pearl (1980) introduced [SCOUT](/scout-search/), which finds the value of the first move and tests each later move with a separate yes-or-no procedure. Marsland and Campbell (1982), in their survey of parallel search of strongly ordered game trees, described principal variation search, which gives a full window only to the nodes of the expected principal variation and searches the other nodes with minimal windows. Reinefeld (1983) published NegaScout, an improvement of SCOUT in negamax form that uses an alpha-beta window for the test, so that a test that fails returns a bound for the re-search. Campbell and Marsland (1983) compared the algorithms on strongly ordered trees. With [transposition tables](/transposition-table/) and good [move ordering](/move-ordering/), PVS became the standard search of chess programs. Plaat, Schaeffer, Pijls and de Bruin (1996) used NegaScout with a transposition table as the reference when they tested [MTD(f)](/mtdf/).

## References
