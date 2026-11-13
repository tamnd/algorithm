---
title: Alpha-beta with a transposition table keeps every entry true and returns the alpha-beta result
proves: [correctness]
status: full
---

We use the pseudocode of the page: TT-PROBE in lines L1 to L3, TT-STORE in lines L4 to L6, and SEARCH in lines L7 to L20. The game is a finite game graph, and EVALUATE gives each position its value for the side to move. For a position $p$ and a depth $d \ge 0$, the *depth-$d$ value* is $V_0(p) = \text{EVALUATE}(p)$, $V_d(p) = \text{EVALUATE}(p)$ when $p$ is terminal, and $V_d(p) = \max_c (-V_{d-1}(c))$ over the children $c$ of $p$ otherwise. This is the [negamax](/negamax/) value of the tree of depth $d$ below $p$. $Z(p)$ is the key of $p$.

**Assumptions.**
- (A1) $Z$ is one-to-one on the positions that the search meets.
- (A2) The children and the value of a position do not depend on the path to it.
- (A3) If the search meets a position $p$ at two remaining depths $d$ and $e$, then $V_d(p) = V_e(p)$.

Assumption (A3) holds when every path from the root to $p$ has the same length, as in a layered game graph, and when the depth of the root is at least the height of the graph, since then $V_d(p)$ is the full negamax value for every depth that occurs. Without (A3), line L8 can give a node a deeper value than $V_d(p)$. The result is then a mix of depths, and the claims below do not hold for $V_d$.

**Definition.** A value $r$ is a *fail-soft result* for the window $(\alpha, \beta)$ and the true value $V$ if
- $r \le \alpha$ implies $V \le r$,
- $\alpha < r < \beta$ implies $V = r$,
- $r \ge \beta$ implies $V \ge r$.

With $\alpha = -\infty$ and $\beta = +\infty$ only the middle case can apply, so $r = V$.

**Invariant (T).** Each entry $(z, e, f, v, x)$ in the table describes a position $p$ with $Z(p) = z$, and
- if $f = \text{EXACT}$ then $V_e(p) = v$,
- if $f = \text{LOWER}$ then $V_e(p) \ge v$,
- if $f = \text{UPPER}$ then $V_e(p) \le v$.

The move $x$ plays no part in the proof.

**Theorem.** Under (A1) to (A3), if (T) holds when a call SEARCH$(p, d, \alpha, \beta)$ with $\alpha < \beta$ starts, then (T) holds when it returns, and its result $r$ is a fail-soft result for $(\alpha, \beta)$ and $V_d(p)$. In particular, SEARCH$(p, d, -\infty, +\infty)$ returns $V_d(p)$.

*Proof.* By induction on $d$, and within the same $d$ on the number of steps of the call. TT-STORE only writes entries, and it removes old entries without changing the others. A removed entry cannot make (T) false, so (T) is kept by every call of TT-STORE whose new entry is true.

*Lines L7 to L9.* By (A1), an entry that TT-PROBE returns is about $p$ itself, because line L2 compares the full key. Line L8 needs $e \ge d$ for the depth of the entry, and (A3) gives $V_e(p) = V_d(p)$; write $V$ for this value. If the flag is EXACT, the result $r = V$ is a fail-soft result for every window. If the flag is LOWER and $v \ge \beta$, then $V \ge v = r \ge \beta$, so the third case holds, and the first two cases cannot apply because $r \ge \beta > \alpha$. If the flag is UPPER and $v \le \alpha$, then $V \le v = r \le \alpha$, and the first case holds. The table does not change.

*Lines L10 and L11.* If $d = 0$ or $p$ is terminal, then $V_d(p) = \text{EVALUATE}(p) = r$. The new entry is EXACT and true.

*Lines L12 to L17.* The order of the children does not matter in what follows, so line L12 is harmless. Let $c_1, \ldots, c_k$ be the children in the order of the loop, $w_i = -V_{d-1}(c_i)$, so that $V = V_d(p) = \max_i w_i$. Let $m_0 = -\infty$, let $m_i$ be the value of $m$ after the pass for $c_i$, and let $a_i = \max(m_{i-1}, \alpha)$. The child gets the window $(-\beta, -a_i)$, and $-\beta < -a_i$ because the loop runs only while $m_{i-1} < \beta$. By induction the child returns a fail-soft result $t_i$ for $(-\beta, -a_i)$ and $V_{d-1}(c_i)$, and (T) still holds. Let $u_i = -t_i$. Negating the three cases gives:
- $u_i \ge \beta$ implies $w_i \ge u_i$,
- $a_i < u_i < \beta$ implies $w_i = u_i$,
- $u_i \le a_i$ implies $w_i \le u_i$.

Line L16 keeps $m_i = \max(m_{i-1}, u_i)$.

Case 1: the loop stops at line L17 after child $c_i$. Then $m_{i-1} < \beta \le m_i$, so $m_i = u_i \ge \beta$, and the first case gives $V \ge w_i \ge u_i = r$. So $r$ is a fail-soft result: the third case holds, and the other two do not apply.

Case 2: the loop ends without a cutoff, and $r = m_k = \max_i u_i < \beta$. For each $i$, either $u_i \le a_i$ and $w_i \le u_i \le r$, or $a_i < u_i < \beta$ and $w_i = u_i \le r$. So $V = \max_i w_i \le r$. If $r \le \alpha$, this is the first case. If $\alpha < r < \beta$, let $j$ be the first index with $u_j = r$. Then $m_{j-1} < r$ and $\alpha < r$, so $a_j < u_j < \beta$, and $w_j = u_j = r$. Hence $V \ge r$, and $V = r$.

*Lines L18 and L19.* If $r \le \alpha$, then $V \le r$ and the UPPER entry is true. If $r \ge \beta$, then $V \ge r$ and the LOWER entry is true. Else $V = r$ and the EXACT entry is true. So (T) holds when the call returns. $\blacksquare$

**The entries made without flags.** If line L18 always sets EXACT, the entry claims $V_d(p) = r$ also after a cutoff, where the proof gives only $V_d(p) \ge r$. A later probe in a wider window returns $r$ as if it were the value, and the root value can change. The page gives an example of 9 positions where the result becomes 4 instead of 3.

**Hash collisions.** Without (A1), line L2 can accept the entry of another position with the same key. For keys of $w$ random bits and $n$ positions, the chance that two of them share a key is at most $n(n-1)/2^{w+1}$, by the bound of the [birthday paradox](/birthday-paradox/).

**Replacement.** The proof uses no fact about which entries are in the table. So the table may drop entries at any time, as line L5 and the replacement policies do, and the result is the same. Only the work changes.
