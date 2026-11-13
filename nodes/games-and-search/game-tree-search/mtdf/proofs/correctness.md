---
title: MTD(f) returns the value of the root, for every guess and every grain
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page: MTDF in lines L1 to L7 and ABWM, alpha-beta with memory, in lines L8 to L15. Let $N(n)$ be the [negamax](/negamax/) value of node $n$ to its remaining depth; a node at the depth limit counts as terminal. The table maps a node, with its remaining depth, to a pair $(\text{lo}, \text{hi})$. The proof has three parts: the table only holds true bounds, ABWM returns the bounds of fail-soft [alpha-beta](/alpha-beta-pruning/), and the driver keeps an interval that holds the value and shrinks it to one point.

## ABWM

**Theorem 1.** Suppose that, when ABWM$(n, \alpha, \beta)$ is called with $\alpha < \beta$, every entry of the table satisfies $\text{lo} \le N \le \text{hi}$ for its node. Then the result $r$ satisfies
- (F1) if $r \le \alpha$ then $N(n) \le r$,
- (F2) if $\alpha < r < \beta$ then $N(n) = r$,
- (F3) if $r \ge \beta$ then $N(n) \ge r$,

and when the call returns, every entry of the table still satisfies $\text{lo} \le N \le \text{hi}$.

*Proof.* By induction on the height of $n$.

*Returns from the table, lines L8 and L9.* If $\text{lo} \ge \beta$, the result is $r = \text{lo} \ge \beta$, and $N(n) \ge \text{lo} = r$, so (F3) holds. If $\text{lo} = \text{hi}$, then $r = N(n)$, which satisfies all three conditions. If $\text{hi} \le \alpha$, the result is $r = \text{hi} \le \alpha$ and $N(n) \le r$, so (F1) holds. The table does not change.

*The narrowed window, line L10.* Otherwise $\text{lo} < \beta$, $\text{hi} > \alpha$ and $\text{lo} < \text{hi}$, so $\alpha' = \max(\alpha, \text{lo})$ and $\beta' = \min(\beta, \text{hi})$ satisfy $\alpha' < \beta'$: each of $\alpha, \text{lo}$ is less than each of $\beta, \text{hi}$. Without an entry, $\alpha' = \alpha$ and $\beta' = \beta$.

*The search, lines L11 to L13.* A terminal node returns $r = N(n)$, which satisfies all three conditions, and stores the exact pair $(r, r)$. At an inner node, lines L12 and L13 are the fail-soft alpha-beta loop with the window $(\alpha', \beta')$: the best score $g$ starts at $-\infty$, each child gets the window $(-\beta', -a)$ with $a = \max(\alpha', g)$, and the loop stops when $g \ge \beta'$. Each child call starts with a table of true bounds, by the induction hypothesis on the earlier calls, so it returns the fail-soft bounds and leaves a table of true bounds. The proof on the alpha-beta page uses only these bounds of the children, so the result $r$ satisfies (F1) to (F3) for the window $(\alpha', \beta')$.

*Back to the window $(\alpha, \beta)$.* If $r \le \alpha'$, then $N(n) \le r$. If also $r \le \alpha$, this is (F1). Else $\alpha < r \le \alpha' = \text{lo} \le N(n)$, so $N(n) = r$, and $r \le \text{lo} < \beta$, so (F2) holds. If $\alpha' < r < \beta'$, then $N(n) = r$ and $\alpha < r < \beta$, which is (F2). If $r \ge \beta'$, then $N(n) \ge r$. If also $r \ge \beta$, this is (F3). Else $r < \beta$, so $\beta' = \text{hi}$ and $N(n) \le \text{hi} \le r$, so $N(n) = r$, which is (F2).

*The store, line L14.* The search stores $\text{hi} = r$ if $r \le \alpha'$, the pair $(r, r)$ if $\alpha' < r < \beta'$, and $\text{lo} = r$ if $r \ge \beta'$, keeping the other bound of an older entry. By the three cases for the window $(\alpha', \beta')$, each new bound is a true bound on $N(n)$. The older bound was true before, so the entry is still true. $\square$

The table starts empty, which satisfies the hypothesis, so by induction on the calls every call of ABWM returns fail-soft bounds. Note that the entries are keyed by the remaining depth as well, so a node that is reached at two depths has two entries, one for each value.

## The driver

**Theorem 2.** For every guess $f$ and every grain $\gamma > 0$, MTDF returns $V = N(\text{root})$.

*Proof.* We show the invariant $\text{lower} \le V \le \text{upper}$. It holds at line L1. In a pass, line L3 sets $\beta$ and line L4 searches the window $(\beta - \gamma, \beta)$ with the result $g$. By Theorem 1:
- if $g \le \beta - \gamma$, then $V \le g$; line L5 sets $\text{upper} = g$, and line L6 does nothing;
- if $\beta - \gamma < g < \beta$, then $V = g$; lines L5 and L6 set both bounds to $g$;
- if $g \ge \beta$, then $V \ge g$; line L6 sets $\text{lower} = g$, and line L5 does nothing.

In each case the invariant holds after the pass. When the loop ends, $\text{lower} \ge \text{upper}$, so $\text{lower} = V = \text{upper}$. The last pass set one of the bounds to its result $g$, so line L7 returns $V$.

*Termination.* The result of every search is a finite leaf value: an inner node scores at least one child, and the table only holds results of earlier searches. Let $L$ be the finite set of leaf values. After its first change, each bound is in $L$. We show that each pass either ends the loop or moves a bound strictly, lower up or upper down.
- A fail high gives $\text{lower} = g \ge \beta \ge \text{lower}_{\text{old}} + \gamma$, a strict move up.
- An exact result ends the loop.
- A fail low gives $\text{upper} = g \le \beta - \gamma$. Before the pass, the variable $g$ held the result of the last pass, so $g_{\text{old}}$ is the current lower or the current upper, or the guess $f$ in the first pass, when $\text{upper} = +\infty$ and any finite result is a strict move. If $\beta = g_{\text{old}} = \text{upper}_{\text{old}}$, then $g \le \text{upper}_{\text{old}} - \gamma$, a strict move down. Else $\beta = \text{lower} + \gamma$, so $g \le \text{lower}$, and $V \le g \le \text{lower} \le V$ makes the two bounds equal, which ends the loop.

Lower only goes up and upper only goes down, each through values of $L$, so the loop makes at most $2|L| + 1$ passes. $\blacksquare$

**Two passes with a perfect guess.** Let all values be multiples of $\gamma$, and let $f = V$. The first pass has $\beta = \max(V, -\infty) = V$ and fails high with $g \ge V$, so $g = V$ by the invariant, and lower becomes $V$. The second pass has $\beta = \max(V, V + \gamma) = V + \gamma$, so its window $(V, V + \gamma)$ holds no value, and it fails low with $g \le V$, so $g = V$ and upper becomes $V$. The loop ends after two passes, one that proves $V \ge f$ and one that proves $V \le f$.

**A grain that is too coarse.** If some values are not multiples of $\gamma$, a window $(\beta - \gamma, \beta)$ can hold a value strictly inside, and then the search returns it exactly. Line L6 sets lower as well as upper in this case. Without it, upper would stay at that value, the next window would be the same, and the loop would not end. With integer values and $\gamma = 1$, the case never happens, and line L6 is the usual "else lower = g".
