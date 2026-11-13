---
tag: K9327M
kind: algorithm
slug: aspiration-search
name: Aspiration search
aliases:
- aspiration windows
area: games-and-search/game-tree-search
level: advanced
summary: Alpha-beta at the root with a narrow window around a guess of the value, usually the score of the last iteration. If the result falls outside, the window moves and widens for a new search.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies, k: the number of searches of the root}
  time: {worst: O(k b^d), best: O(b^(d/2))}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [alpha-beta-pruning, iterative-deepening-search]
see_also: [principal-variation-search, mtdf, scout-search, transposition-table, principal-variation, knuth-moore-theorem, parallel-alpha-beta, best-move-selection]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: Section 4 (F2(p, a, b) in place of F2(p, -inf, +inf) when the value is expected between a and b, the re-search F2(p, -inf, v) after a fail low, and its use in Greenblatt's program)
  - paper: doi:10.1016/0004-3702(83)90001-2
    title: Murray S. Campbell and T. Anthony Marsland, A comparison of minimax tree search algorithms, Artificial Intelligence 20(4) (1983)
    locator: pp. 347 to 367 (the comparison of alpha-beta and its narrow-window forms on strongly ordered trees)
  - paper: doi:10.1016/0004-3702(95)00126-3
    title: Aske Plaat, Jonathan Schaeffer, Wim Pijls and Arie de Bruin, Best-first fixed-depth minimax algorithms, Artificial Intelligence 87(1-2) (1996)
    locator: pp. 255 to 293 (the experiments that compare MTD(f) with NegaScout using aspiration windows)
  - paper: "Gérard M. Baudet, The design and analysis of algorithms for asynchronous multiprocessors, PhD thesis, Carnegie Mellon University (1978)"
    title: Baudet 1978
    locator: the chapters on parallel alpha-beta (parallel aspiration search, where each processor searches the root with one part of the window)
---

Aspiration search runs [alpha-beta](/alpha-beta-pruning/) at the root with a narrow window $(g - \delta, g + \delta)$ around a guess $g$ of the value, in place of the full window $(-\infty, +\infty)$. A narrow window gives more cutoffs, so when the value is inside it the search is cheaper and still exact. When the value is outside, the result is only a bound: a *fail low* says that the value is at most the result, a *fail high* says that it is at least the result. The root is then searched again with a window on the side of the failure. Programs use it inside [iterative deepening](/iterative-deepening-search/), with the value of the search to depth $d - 1$ as the guess for depth $d$, because the two values are usually close. The result is always the [negamax](/negamax/) value of the root. Only the work changes with the guess.

## In plain words

Before a search, you often have a good idea of the answer, because the search one move less deep gave almost the same score. So you tell the search: "I only care about scores close to this one." The search can then drop more branches, because more of them are clearly outside the range.

If the true score is in the range, you get it, and you saved work. If it is outside, the search says so and on which side. Then you search again with a range on that side, and you make the range wider each time, so that a bad guess costs only a few extra searches.

The answer is always the same as the answer of a full search.

## The problem

The input is as on the [alpha-beta](/alpha-beta-pruning/) page: a [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/), a depth limit $d$ and an evaluation for the side to move. In addition there is a guess $g$ and a half-width $\delta > 0$. The output is the negamax value $V$ of the root to depth $d$. This is the [game tree evaluation](/game-tree-evaluation/) problem. The guess may be wrong by any amount. A good guess makes the search faster and a bad guess makes it slower, but it never changes the result.

The procedure uses a fail-soft ALPHABETA$(n, \alpha, \beta)$, whose result $v$ satisfies: $v \le \alpha$ implies $V \le v$, $\alpha < v < \beta$ implies $V = v$, and $v \ge \beta$ implies $V \ge v$.

## The algorithm

```pseudo id=main
ASPIRATION(root, g, δ)
L1  lo ← −∞; hi ← +∞               ▷ the value is always in [lo, hi]
L2  α ← g − δ; β ← g + δ
L3  loop
L4      v ← ALPHABETA(root, α, β)
L5      if α < v < β then return v   ▷ inside the window: exact
L6      if v ≤ α then hi ← v else lo ← v
L7      if lo = hi then return lo
L8      δ ← 2δ
L9      if v ≤ α then (α, β) ← (max(lo, v − δ), v)    ▷ fail low: search below v
L10     else (α, β) ← (v, min(hi, v + δ))              ▷ fail high: search above v
```

Lines L1 and L6 keep the interval $[\text{lo}, \text{hi}]$ that is known to hold the value. A fail low lowers hi to its result, and a fail high raises lo to its result. Line L7 stops when the two meet: the value is then known, though no search returned it inside its window. This happens when the value is exactly on the edge of a window. Lines L9 and L10 put the next window next to the result of the failed search, on the side where the value must be, and line L8 doubles its width. The next window always lies inside $[\text{lo}, \text{hi}]$, so no part of a window is spent on values that are already ruled out.

Other schemes for the next window are also correct, as long as the window is not empty and the loop keeps lo and hi. Many programs open the side of the failure to $\pm\infty$ at once. Others widen by a fixed step, or by a step that grows more slowly than doubling.

## Example

**Knuth and Moore's remark.** Section 4 of their paper suggests $F2(p, 0, 4)$ in place of $F2(p, -10, +10)$ for their Fig. 3, where the value is expected between 0 and 4, and shows that two of the leaves then need no search.

**A guess on the edge.** Take the tree whose root has two children, with the leaves 3 and 17 under the first child and 2 and 12 under the second. In the minimax view MAX is at the root and MIN below, so the children are worth 3 and 2, and the root is worth 3. Start with the guess $g = 5$ and $\delta = 2$.

| search | window $(\alpha, \beta)$ | leaves visited | result | outcome | $[\text{lo}, \text{hi}]$ after it |
| --- | --- | --- | --- | --- | --- |
| 1 | $(3, 7)$ | 3, 2 | 3 | fail low, $3 \le \alpha$ | $[-\infty, 3]$ |
| 2 | $(-1, 3)$ | 3, 17 | 3 | fail high, $3 \ge \beta$ | $[3, 3]$ |

In search 1 the leaf 3 already shows that the first child is worth at most 3 to MAX, which is not above $\alpha = 3$, so the leaf 17 is skipped, and the same holds for the leaf 2 under the second child. The search proves only that the value is at most 3. In search 2 the first child is worth exactly 3, which is $\beta$, so the second child is skipped. Now $\text{lo} = \text{hi} = 3$, and line L7 returns 3. The two searches visit 4 leaves, one more than alpha-beta with the full window. A guess that is too high costs a little here. The tests check this run, window by window.

**Inside iterative deepening.** On 20 random games with 4 moves per position and depth 7, in which each move adds a random gain to the score, alpha-beta with the full window visits 78333 nodes in total. Aspiration search with $\delta = 2$ around the value of depth 6 visits 64950 nodes, about 17% fewer, though the depth 6 value is often off by 2 or more. With a guess 40 points too high it visits 96281 nodes, because it needs several searches. All three give the same values.

## Correctness

The [proof](proofs/correctness/) shows the invariant that $\text{lo} \le V \le \text{hi}$ and that the window lies inside $[\text{lo}, \text{hi}]$ at each search. A return at line L5 is exact by the property of fail-soft alpha-beta, and a return at line L7 is exact because $\text{lo} = V = \text{hi}$. For termination, the proof shows that after a fail low, a fail high ends the loop at once, and the other way round. So all searches but the last fail on the same side, and with doubling widths they reach the value after at most $\lceil \log_2(D/\delta) \rceil + 3$ searches, where $D$ is the distance from the guess to the value.

The tests compare the result with negamax on random uniform and irregular trees with integer and fraction leaves, for guesses at the value, near it, far from it and on its edge, and for widths from $1/100$ to 100. They check the bound on the number of searches, the run of the example above, the bounds of the fail-soft search for random windows, and iterative deepening with aspiration on random games with incremental scores.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of the move generator and of EVALUATE counted as $O(1)$, on a uniform tree of branching factor $b$ and depth $d$.

**One search.** A single alpha-beta search with any window visits at most the $b^d$ leaves of the tree. When the window holds the value and the first child at each node is best, it visits $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, the minimum of the [Knuth-Moore theorem](/knuth-moore-theorem/), which holds for any search that proves the exact value. So a narrow window cannot beat that bound. It helps when the order is not perfect: a narrow window cuts off moves that a wider window would search.

**The number of searches.** If the guess is at distance $D$ from the value, the loop makes $k \le \lceil \log_2(D/\delta) \rceil + 3$ searches, and $k \le 3$ when $D \le \delta$. So the time is $O(k\, b^d)$ in the worst case, and $O(b^{d/2})$ in the best case, with one search. The failed searches are cheaper than full searches, since a narrow window prunes more, but in practice the second and later searches are a real cost, and the choice of $\delta$ is a trade-off between more cutoffs and fewer re-searches.

**Space.** The same as alpha-beta, $O(bd)$, plus two numbers for lo and hi.

## Properties

- **Exact.** For any guess and any $\delta > 0$ the result is the value of the root.
- **A wrapper.** It changes only the call at the root. The search below is plain alpha-beta, so it works with every enhancement of alpha-beta.
- **Needs fail-soft for tight bounds.** With a fail-hard search, a fail low gives only $V \le \alpha$, and the next window must start from $\alpha$, not from the result.
- **Directional.** Each search is directional. With a [transposition table](/transposition-table/), the later searches reuse the work of the earlier ones.
- **Depends on the guess.** Work, but not the result, depends on $g$ and $\delta$.

## Variants and improvements

- **Open the failed side.** After a fail low, search $(-\infty, v)$, as Knuth and Moore suggest; after a fail high, $(v, +\infty)$. This makes at most 3 searches, but the second one has no pruning on its open side.
- **Gradual widening.** Widen by a fixed step or a growing step, as in the procedure above. Many chess programs widen by a step that grows each time and keep the window centered near the last result.
- **[Principal variation search](/principal-variation-search/).** It uses the same idea at every node, with the narrowest window, and searches again only when a test fails. Aspiration at the root and PVS below are often combined.
- **[MTD(f)](/mtdf/).** The limit case: every search has a window of width zero, and the guess moves after each one. It needs a [transposition table](/transposition-table/) to be fast.
- **Parallel aspiration.** Baudet split the full range into disjoint windows and gave one to each processor. The search whose window holds the value finds it, and the bounds from the others confirm it. The speedup is limited, because even a window that holds the value needs the minimal tree.
- **The odd-even effect.** In many games the values at odd and even depths differ. Some programs use the value of depth $d - 2$ as the guess for depth $d$.

## When to use it

Use it at the root of every [iterative deepening](/iterative-deepening-search/) alpha-beta or PVS search in a game program. It is cheap to add and often saves some percent of the nodes. Keep $\delta$ about the size of the usual change of the score from one depth to the next. Do not use it when no good guess is available, or when the score can jump a lot between depths, for example near a mate. Then a full window or [MTD(f)](/mtdf/) with a [transposition table](/transposition-table/) is better.

## Pitfalls

- **Fail-hard re-search.** With a fail-hard search, the re-search $F2(p, -\infty, v)$ after a fail low at $v$ returns $\beta = v$ when the value is exactly $v$. This looks like a fail high. Only the bound from the first search shows that the value is $v$. Keep lo and hi, as lines L1, L6 and L7 do, or use the fail-soft form.
- **Search instability.** With a [transposition table](/transposition-table/), or with pruning that depends on the window, a re-search can return a result that contradicts the first one, for example a fail high above the result of an earlier fail low. Then $\text{lo} > \text{hi}$, and the next window of the procedure above is empty. Real programs check for this case and search again with the full window.
- **No move after a fail low.** A search that fails low at the root has no reliable best move: every move was only proved worse than $\alpha$. Do not play its best move. Re-search, or keep the move of the last full search, as on [best move selection](/best-move-selection/).
- **A fail high is not the end.** After a fail high the best move is often right, and programs under time pressure play it. But the value is only a lower bound, so a program that reports it as exact prints a wrong score.
- **Mate scores.** A mate score is far from all normal values, so a narrow window around a normal score needs many doublings to reach it. Open the window to $\pm\infty$ once the result is near the mate range.
- **The empty window.** In line L9, $\max(\text{lo}, v - \delta)$ must stay below $v$. This holds because the loop has already stopped if $\text{lo} = v$.

## Implementations

## History

Knuth and Moore (1975) describe the idea in Section 4 of their analysis of alpha-beta: search with a window $(a, b)$ where the value is expected, and after a fail low at $v$ search again with $(-\infty, v)$. They report that some versions of Greenblatt's chess program used it. Baudet (1978), in his thesis on algorithms for asynchronous multiprocessors, studied the parallel form, where each processor searches the root with one part of the range. Campbell and Marsland (1983) compared alpha-beta with its narrow-window forms on strongly ordered trees. Later chess programs used aspiration windows at the root of iterative deepening as a matter of course, usually with principal variation search below. Plaat, Schaeffer, Pijls and de Bruin (1996) took the idea to its limit with [MTD(f)](/mtdf/), which uses only windows of width zero, and compared it with NegaScout using aspiration windows.

## References
