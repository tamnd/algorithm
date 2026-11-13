---
title: Principal variation search returns the bounds of fail-soft alpha-beta, and makes no re-search when the first move is best
proves: [correctness, termination]
status: full
---

We use the pseudocode PVS of the page, lines L1 to L11, with a grain $g > 0$. Let $N(n)$ be the [negamax](/negamax/) value of node $n$ to the given depth; a node at the depth limit counts as terminal. For a child $c$ of $n$ write $u_c = -N(c)$, the score of the move to $c$ for the side to move at $n$. The tree is finite and every call is on a child, so the recursion stops.

**Theorem.** For $\alpha < \beta$, the result $r$ of PVS$(n, \alpha, \beta)$ satisfies
- (F1) if $r \le \alpha$ then $N(n) \le r$,
- (F2) if $\alpha < r < \beta$ then $N(n) = r$,
- (F3) if $r \ge \beta$ then $N(n) \ge r$.

These are the conditions of fail-soft [alpha-beta](/alpha-beta-pruning/). With $\alpha = -\infty$ and $\beta = +\infty$, (F2) gives $r = N(n)$.

*Proof.* By induction on the height of $n$. A terminal node returns $N(n)$ at line L1, which satisfies all three.

Let $n$ be an inner node, and let the theorem hold for its children. We first show what lines L6 to L8 give for one later child.

**Claim.** Let $a$ be the value of line L5 for a later child $c$, with $a < \beta$, and let $t$ be its value after line L8. Then: if $t \le a$ then $u_c \le t$; if $a < t < \beta$ then $u_c = t$; if $t \ge \beta$ then $u_c \ge t$.

*Proof of the claim.* Line L6 calls PVS on $c$ with the window $(-a - g, -a)$ and gets $r_0$, so $t_0 = -r_0$. Negate the three cases of the theorem for $c$:
- if $r_0 \ge -a$, that is $t_0 \le a$, then $N(c) \ge r_0$, so $u_c \le t_0$;
- if $-a - g < r_0 < -a$, that is $a < t_0 < a + g$, then $u_c = t_0$;
- if $r_0 \le -a - g$, that is $t_0 \ge a + g$, then $N(c) \le r_0$, so $u_c \ge t_0$.

So in every case: $t_0 \le a$ gives $u_c \le t_0$, and $t_0 > a$ gives $u_c \ge t_0$, with equality when $t_0 < a + g$.

If $t_0 \le a$ or $t_0 \ge \beta$, line L7 makes no re-search, $t = t_0$, and the claim holds. If $a < t_0 < \beta$ and $c$ is terminal, the result of a terminal node is exact, so $u_c = t_0$. Else line L8 searches $c$ again with the window $(-\beta, -t_0)$, which is not empty, and gets $r_1$, so $t = -r_1$. We know $u_c \ge t_0$. By the theorem for $c$:
- if $t \le t_0$, then $u_c \le t$, so $t_0 \le u_c \le t \le t_0$, and $u_c = t = t_0$, which is strictly between $a$ and $\beta$;
- if $t_0 < t < \beta$, then $u_c = t$;
- if $t \ge \beta$, then $u_c \ge t$.

This proves the claim. $\square$

Now the node. Let $W$ be the best score $u_c$ among the children searched so far. We show the invariant: before a cutoff, $\max(m, \alpha) = \max(\alpha, W)$, and if $m \le \alpha$ then $u_c \le m$ for every child searched so far.

*First child.* Line L2 searches $c_1$ with the window $(\alpha, \beta)$ and gets $m$; negating the theorem for $c_1$ gives the three cases. If $m \ge \beta$, line L3 returns $m$, and $N(n) \ge u_{c_1} \ge m$, so (F3) holds. If $\alpha < m < \beta$, then $m = u_{c_1} = W$. If $m \le \alpha$, then $u_{c_1} \le m \le \alpha$, so $\max(m, \alpha) = \alpha = \max(\alpha, W)$. The invariant holds.

*Later child.* Line L5 sets $a = \max(\alpha, m) = \max(\alpha, W)$, and $a < \beta$ because there was no cutoff. Apply the claim.
- If $t \le a$: $u_c \le t \le a$. Line L9 sets $m' = \max(m, t)$, and $\max(m', \alpha) = a = \max(\alpha, W, u_c)$. If $m' \le \alpha$ then $u_c \le t \le m'$.
- If $a < t < \beta$: $u_c = t > a$, so the new best is $W' = t$, and $m' = t = \max(\alpha, W')$.
- If $t \ge \beta$: line L10 returns $m' = t$, since $m < \beta \le t$. Then $N(n) \ge u_c \ge t$, so (F3) holds.

*End.* If the loop ends without a cutoff, every child is searched, $W = N(n)$, and $r = m$ with $\max(r, \alpha) = \max(\alpha, N(n))$. If $r > \alpha$, this gives $r = N(n)$, which is (F2) since $r < \beta$. If $r \le \alpha$, the invariant gives $u_c \le r$ for every child, so $N(n) \le r$, which is (F1). $\blacksquare$

The grain $g$ plays no part in the proof, so PVS is correct for every $g > 0$. The grain matters for the work: if every value is a multiple of $g$, then no value lies strictly inside a window $(a, a + g)$ with $a$ a multiple of $g$, and the null-window search prunes as much as a window of width zero.

**Lemma (no re-search with the best move first).** If, at every node, the first child is a best move, then line L8 is never run.

*Proof.* At a node $n$ take a later child $c$. Since $c_1$ is best, $u_c \le u_{c_1}$. If the first child returned $m$ with $\alpha < m < \beta$, then $m = u_{c_1}$, and if it returned $m \le \alpha$, then $u_{c_1} \le \alpha$. In both cases $u_c \le \max(\alpha, m) = a$, so $N(c) \ge -a$, which is the upper end of the window $(-a - g, -a)$ of the null-window search. If its result were $r_0 < -a$, the theorem for $c$ would give $N(c) = r_0$ or $N(c) \le r_0$, so $N(c) < -a$, which is false. So $r_0 \ge -a$, $t_0 \le a$, and line L7 makes no re-search. $\square$
