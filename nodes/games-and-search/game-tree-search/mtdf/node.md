---
tag: C2MWH2
kind: algorithm
slug: mtdf
name: "MTD(f)"
aliases:
- MTD-f
- memory-enhanced test driver
area: games-and-search/game-tree-search
level: advanced
summary: Finds the minimax value with a sequence of null-window alpha-beta searches. Each pass moves an upper or a lower bound, and a transposition table keeps the work of the earlier passes.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies, k: the number of passes}
  time: {worst: O(k b^d), best: O(b^(d/2))}
  space: {extra: O(b^d)}
properties: {deterministic: true, recursive: true}
prereqs: [alpha-beta-pruning, transposition-table]
see_also: [aspiration-search, principal-variation-search, sss-star, scout-search, iterative-deepening-search, knuth-moore-theorem, move-ordering, best-move-selection]
sources:
  - paper: doi:10.1016/0004-3702(95)00126-3
    title: Aske Plaat, Jonathan Schaeffer, Wim Pijls and Arie de Bruin, Best-first fixed-depth minimax algorithms, Artificial Intelligence 87(1-2) (1996)
    locator: pp. 255 to 293 (AlphaBetaWithMemory, the MTD framework with MTD(f), MTD(+inf) as SSS* and MTD(-inf) as DUAL*, and the experiments in chess, checkers and Othello programs)
  - paper: doi:10.1145/228329.228344
    title: Jonathan Schaeffer and Aske Plaat, New advances in alpha-beta searching, Proceedings of the 1996 ACM 24th Annual Computer Science Conference (CSC '96)
    locator: pp. 124 to 130 (MTD(f) for practitioners, compared with NegaScout)
  - paper: doi:10.3233/icg-1994-17404
    title: Arie de Bruin, Wim Pijls and Aske Plaat, Solution trees as a basis for game-tree search, ICCA Journal 17(4) (1994)
    locator: pp. 207 to 219 (bounds from solution trees, the basis of the null-window search driver)
  - paper: "Judea Pearl, SCOUT: a simple game-searching algorithm with proven optimal properties, Proceedings of the First Annual National Conference on Artificial Intelligence (AAAI-80), Stanford (1980)"
    title: Pearl 1980, AAAI
    locator: pp. 143 to 145 (TEST, a yes-or-no search against a bound, the idea that MTD(f) repeats at the root)
---

MTD(f) finds the [minimax](/minimax/) value of a game tree with a sequence of null-window searches at the root. Each search is [alpha-beta](/alpha-beta-pruning/) with the window $(\beta - 1, \beta)$, for integer scores, so it only answers "is the value at least $\beta$?". A yes gives a lower bound on the value, a no gives an upper bound, and the next search is placed at the new bound. The searches start at a guess $f$, usually the value of the last iteration of [iterative deepening](/iterative-deepening-search/), and stop when the two bounds meet. On its own, this would search the same tree many times. MTD(f) makes it cheap with a [transposition table](/transposition-table/) that keeps a lower and an upper bound for every node it has searched, so each pass reuses the work of the earlier ones. The name means "memory-enhanced test driver" with the first guess $f$. Plaat, Schaeffer, Pijls and de Bruin introduced it in 1994 to 1996, as one member of a family that also contains [SSS*](/sss-star/).

## In plain words

You want to know a number, the value of the position, and you can only ask yes-or-no questions: "is it at least 10?". Each question is a search, but a search for a yes or a no is much faster than a search for the exact number.

Start with your best guess. Ask whether the value is at least the guess. If yes, ask a little higher. If no, ask lower, at the bound that the last answer gave you. Stop when the answers meet.

Each question searches the same tree again, so you keep notes: for each position you have seen, what you already know about it. The next question reads the notes and does not repeat old work. With a good first guess, two questions are enough.

## The problem

The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/), an EVALUATE function for the side to move, a depth $d$, a key for each position, a first guess $f$, and a grain $\gamma > 0$, the smallest step between two values; $\gamma = 1$ for integer scores. The output is the [negamax](/negamax/) value $V$ of the root to depth $d$, the [game tree evaluation](/game-tree-evaluation/) problem. The table maps a position and its remaining depth to a pair $(\text{lo}, \text{hi})$ with $\text{lo} \le N \le \text{hi}$.

## The algorithm

```pseudo id=main
MTDF(root, f)
L1  g ← f; lower ← −∞; upper ← +∞
L2  while lower < upper do
L3      β ← max(g, lower + γ)
L4      g ← ABWM(root, β − γ, β)           ▷ is the value at least β?
L5      if g < β then upper ← g             ▷ no: the value is at most g
L6      if g > β − γ then lower ← g         ▷ yes, or exact: the value is at least g
L7  return g

ABWM(n, α, β)                              ▷ fail-soft alpha-beta with memory
L8  if the table has (lo, hi) for n then
L9      if lo ≥ β or lo = hi then return lo;  if hi ≤ α then return hi
L10     α ← max(α, lo); β ← min(β, hi)
L11 if n is terminal then store (g, g) with g ← EVALUATE(n); return g
L12 g ← −∞; a ← α
L13 for each child c while g < β do  g ← max(g, −ABWM(c, −β, −a)); a ← max(a, g)
L14 if g ≤ α then hi ← g  else if g < β then lo ← hi ← g  else lo ← g;  store (lo, hi)
L15 return g
```

**The driver.** Lines L1 to L7 keep an interval $[\text{lower}, \text{upper}]$ that holds the value. Line L3 puts the next test at the last result $g$, or one grain above lower when $g$ is lower itself, so that each test asks a new question. A fail low moves upper down to $g$, and a fail high moves lower up to $g$. With integer scores and $\gamma = 1$, line L6 is the usual "else lower ← g". It also catches a result strictly inside the window, which can happen only when the grain is too coarse; the value is then exact.

**The memory.** ABWM (alpha-beta with memory) is fail-soft alpha-beta that reads and writes a lower and an upper bound for each node. A stored bound can answer the question at once (line L9), or narrow the window (line L10). After the search, line L14 stores what the result proves, against the narrowed window: an upper bound after a fail low, the exact value inside the window, a lower bound after a fail high. The entry must include the remaining depth, since a node has a different value at a different depth.

## Example

Take the tree of the [alpha-beta](/alpha-beta-pruning/) page. MAX is at the root A, MIN at B and C, and MAX at D, E, F and G. The leaves, as values for MAX, are 3 and 17 under D, 19 and 12 under E, 2 and 5 under G, and 15 and 25 under F. The value is 17. Start with the guess $f = 0$.

| pass | $\beta$ | question | what the search finds | result | bounds after it | new leaves |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | is A at least 0? | D is at least 3, E at least 19, so B is at least 3 | 3, fail high | $[3, +\infty]$ | 3, 19 |
| 2 | 4 | is A at least 4? | D: the leaf 3 is in the table, then 17; so B is at least 17 | 17, fail high | $[17, +\infty]$ | 17 |
| 3 | 18 | is A at least 18? | D is 17 from the table, so B is at most 17; G is 5, so C is at most 5 | 17, fail low | $[17, 17]$ | 2, 5 |

The three passes evaluate 5 leaves, each once, the same as alpha-beta in this order. Without the table, passes 2 and 3 would evaluate the leaves 3 and 17 again. With the perfect guess $f = 17$, MTD(f) needs only two passes: the window $(16, 17)$ proves that the value is at least 17, and the window $(17, 18)$ proves that it is at most 17. The tests check both runs.

In tic-tac-toe from the empty board, with a win scored as 10 plus the number of empty squares, plain alpha-beta visits 20866 nodes, and alpha-beta with the full window and the same table visits 5433. MTD(f) with the guess 0 visits 4377 nodes in 2 passes. On 10 random games with 4 moves per position, with iterative deepening from depth 1 to 6 and the last value as the guess, alpha-beta visits 19989 nodes and MTD(f) 14201, in 227 passes, about 3.8 per depth.

## Correctness

The [proof](proofs/correctness/) has three parts. First, every entry of the table is a true bound: the terminal values are exact, and each stored bound follows from the fail-soft bounds of the search against the narrowed window. Second, ABWM returns the bounds of fail-soft alpha-beta for the window it was given, even after the table has narrowed it. Third, the driver keeps $\text{lower} \le V \le \text{upper}$, and each pass either ends the loop or moves a bound strictly, through leaf values. So it stops, with $\text{lower} = V = \text{upper}$. The proof also shows that a perfect guess takes exactly two passes, and that the loop ends for every grain.

The tests compare MTD(f) with negamax on random uniform and irregular trees with integer and fraction leaves, for guesses at the value, near it and far from it, with and without a depth limit. They check two passes for a perfect guess, grains that are too coarse or too fine, the fail-soft bounds of ABWM for random windows with one table shared by many searches, that every stored bound is true, tic-tac-toe with the board as the key so that the table merges transpositions, and iterative deepening with one table for all depths.

## Complexity

Costs are in the [word RAM](/word-ram/), with each move generation, EVALUATE and table access counted as $O(1)$, on a uniform tree of branching factor $b$ and depth $d$.

**Passes.** With all values multiples of $\gamma$, each pass moves a bound by at least $\gamma$, so with a guess at distance $D$ from the value the number of passes $k$ is at most about $D/\gamma + 2$. With a perfect guess $k = 2$. Without such a guess, it is bounded by twice the number of distinct leaf values, plus one.

**Time.** One pass visits at most all $b^d$ leaves, so the worst case is $O(k\, b^d)$. In practice the table makes the later passes much cheaper. In the best case, with the best move first and a perfect guess, the first pass visits the minimal tree that proves a lower bound, and the second the minimal tree that proves an upper bound. Their union is the minimal tree of the [Knuth-Moore theorem](/knuth-moore-theorem/), $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, so the time is $O(b^{d/2})$.

**Space.** The table holds one entry per node searched, so up to $O(b^d)$ with no limit on its size. Real programs use a table of fixed size, which keeps the most useful entries and loses the rest; the result is still correct, but some work is done again.

## Properties

- **Exact.** For every guess and every grain it returns the value.
- **Only null windows.** Every search at the root has a window of width one grain. Null-window searches prune the most.
- **Needs memory.** Without the table, each pass searches from scratch, and MTD(f) is slower than one full alpha-beta search.
- **Best-first in effect.** With enough memory, the sequence of passes expands the tree in a best-first order. MTD with the first guess $+\infty$ visits the same leaves as [SSS*](/sss-star/), and with $-\infty$ the same as DUAL*.
- **Depends on the guess and on the grain of the evaluation.** A guess far from the value, or an evaluation with a very fine grain, needs many passes.

## Variants and improvements

- **The MTD family.** MTD$(+\infty)$ starts at the top and makes only fail lows: it is a form of [SSS*](/sss-star/). MTD$(-\infty)$ starts at the bottom: it is a form of DUAL*. MTD(bi) puts each test halfway between the bounds. MTD(step) moves by more than one grain at a time.
- **[Iterative deepening](/iterative-deepening-search/).** The value of the last depth is the guess. Since the values at odd and even depths often differ, some programs use the value of depth $d - 2$, or the average of the last two.
- **Best move.** The best move at the root comes from the table, or from the last pass that failed high, since a fail low has no reliable best move.
- **Coarser evaluation.** Fewer distinct values mean fewer passes. Some programs round the evaluation for MTD(f).
- **Enhanced transposition cutoffs.** Before searching the children, check whether one of them already has a bound in the table that gives a cutoff.

## When to use it

Use MTD(f) in a program that already has a good [transposition table](/transposition-table/) and [iterative deepening](/iterative-deepening-search/), and an evaluation with a coarse grain. Plaat and his coauthors found it faster than NegaScout, which is [principal variation search](/principal-variation-search/), in their chess, checkers and Othello programs. Use [principal variation search](/principal-variation-search/) with [aspiration windows](/aspiration-search/) when the table is small, when the evaluation has many distinct values, or when the program needs the principal variation and stable scores from each search.

## Pitfalls

- **No table, no speed.** The passes repeat the same work without memory. The table must hold both a lower and an upper bound per node, and both must be kept when one is updated.
- **The depth in the key.** An entry from a search to a smaller depth is not a bound for a deeper search. Key the entries by position and depth, or keep only entries of at least the depth needed.
- **Store against the narrowed window.** After line L10 has narrowed the window, the result is a bound against the narrowed window, and it must be stored so.
- **Fail-soft is needed.** With a fail-hard search, every pass moves a bound by only one grain, and the number of passes grows with the distance from the guess.
- **Search instability.** With a table of fixed size, a replaced entry, or pruning that depends on the window, two passes can disagree, for example lower above upper. Programs check for this and fall back to a wider window.
- **The best move and the principal variation.** The passes give a value and bounds, not a line. Take the best move from the table or the last fail high, and read the [principal variation](/principal-variation/) from the table.
- **An infinite guess.** In floating point, $+\infty - 1 = +\infty$, so the window $(+\infty - \gamma, +\infty)$ is empty. The children then return at once with false bounds, and the loop does not end. For MTD$(+\infty)$, use a finite guess above every value.
- **A fine evaluation.** With scores in thousandths of a pawn, a guess that is off by half a pawn needs hundreds of passes.

## Implementations

## History

Pearl's [SCOUT](/scout-search/) (1980) showed that a yes-or-no search against a bound is cheaper than a search for the value. Stockman's [SSS*](/sss-star/) (1979) visited fewer leaves than alpha-beta but needed a large list of open nodes, and for many years it was seen as a different kind of algorithm. De Bruin, Pijls and Plaat (1994) studied game-tree search in terms of solution trees, and with Schaeffer they showed that SSS* is a sequence of null-window alpha-beta searches with memory, starting at $+\infty$. Plaat, Schaeffer, Pijls and de Bruin (1996) built the MTD framework on this view, with MTD(f) as its most useful member, and tested it in chess, checkers and Othello programs. Schaeffer and Plaat (1996) presented it to practitioners as a replacement for NegaScout.

## References
