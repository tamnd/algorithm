---
title: Aspiration search returns the value of the root and stops after a logarithmic number of searches
proves: [correctness, termination]
status: full
---

We use the pseudocode ASPIRATION of the page, lines L1 to L10, with a fail-soft ALPHABETA. Let $V$ be the [negamax](/negamax/) value of the root to the given depth. The proof on the [alpha-beta](/alpha-beta-pruning/) page shows that for $\alpha < \beta$ the result $v$ of ALPHABETA$(n, \alpha, \beta)$ satisfies:
- (F1) if $v \le \alpha$ then $V \le v$,
- (F2) if $\alpha < v < \beta$ then $V = v$,
- (F3) if $v \ge \beta$ then $V \ge v$.

**Invariant.** At line L4: $\text{lo} \le V \le \text{hi}$, $\text{lo} < \text{hi}$, $\alpha < \beta$, and $\text{lo} \le \alpha$, $\beta \le \text{hi}$ whenever lo or hi is finite on the side in question. That is, the window lies inside $[\text{lo}, \text{hi}]$.

*Base.* Line L1 sets $\text{lo} = -\infty$ and $\text{hi} = +\infty$, so $\text{lo} \le V \le \text{hi}$ and $\text{lo} < \text{hi}$. Line L2 gives $\alpha = g - \delta < g + \delta = \beta$ since $\delta > 0$.

*Step.* Suppose the invariant holds at line L4, and the search returns $v$. If $\alpha < v < \beta$, line L5 returns $v$, which is $V$ by (F2). Else consider the two cases of line L6.

Fail low, $v \le \alpha$. By (F1), $V \le v$, so the new $\text{hi} = v$ keeps $V \le \text{hi}$. Also $v \le \alpha < \beta \le \text{hi}_{\text{old}}$, so hi only goes down. If now $\text{lo} = \text{hi}$, then $\text{lo} \le V \le \text{hi}$ gives $V = \text{lo}$, and line L7 returns the right value. Else $\text{lo} < \text{hi} = v$. Line L9 sets $\beta = v$ and $\alpha = \max(\text{lo}, v - \delta)$ with the doubled $\delta > 0$. Both terms of the max are less than $v$, so $\alpha < \beta$, and the window lies in $[\text{lo}, \text{hi}]$.

Fail high, $v \ge \beta$. By (F3), $V \ge v$, so the new $\text{lo} = v$ keeps $\text{lo} \le V$, and lo only goes up. Line L7 returns $V$ if $\text{lo} = \text{hi}$. Else line L10 sets $\alpha = v$ and $\beta = \min(\text{hi}, v + \delta) > v$. The invariant holds again.

So every return, at line L5 or line L7, returns $V$.

**Termination.** Let $\delta_0$ be the first width, so the window of search $k \ge 2$ is built with the width $\delta_0 2^{k-1}$.

First, a fail low is never followed by a fail high that does not end the loop. After a fail low with result $v$, the next window is $(\alpha, v)$ and $\text{hi} = v$. If the next search fails high, its result $v'$ satisfies $v' \ge \beta = v$ and $v' \le V \le \text{hi} = v$ by (F3), so $v' = v$, the new lo is $v$, and line L7 stops. The same holds with the sides exchanged. So, apart from a last search, all searches fail on the same side.

Suppose they all fail low; the other case is symmetric. The first window has $\beta - \alpha = 2\delta_0$ and contains the guess $g$. After search $k$ fails low with result $v_k$, the window of search $k + 1$ is $(v_k - \delta_0 2^k, v_k)$ unless lo cuts it. If search $k + 1$ also fails low, then $V \le v_{k+1} \le v_k - \delta_0 2^k$. Summing, after $j$ fail lows in a row past the first, $V \le g - \delta_0 (1 + 2 + \cdots + 2^{j})$, which is less than $g - \delta_0 2^{j}$. So if $D = g - V$, the number $j$ of such extra fail lows satisfies $2^{j} < D/\delta_0$, that is $j < \log_2(D/\delta_0)$. Counting the first search and up to two more at the end (the search that is inside the window, or the one that sets $\text{lo} = \text{hi}$), the loop makes at most $\lceil \log_2(D/\delta_0) \rceil + 3$ searches when $D > \delta_0$, and at most 3 when $D \le \delta_0$. In particular it stops. $\blacksquare$

**Remark on fail-hard searches.** With a fail-hard ALPHABETA, (F1) and (F3) hold only in the weak form "$v \le \alpha$ implies $V \le \alpha$", so a fail low gives $\text{hi} = \alpha$, not a tighter bound. The proof still works with $v = \alpha$ after a fail low and $v = \beta$ after a fail high. Knuth and Moore, in Section 4 of their paper, suggest the re-search $F2(p, -\infty, v)$ after a fail low with result $v$. With the fail-hard form this search returns its $\beta = v$ when $V = v$, which is a fail high. Only together with the bound $V \le v$ from the first search does it give $V = v$. A program that does not keep lo and hi, as the procedure above does, may search again, or report the wrong side.
