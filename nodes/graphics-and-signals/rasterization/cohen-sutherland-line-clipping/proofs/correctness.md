---
title: Cohen-Sutherland clipping returns the exact inside part after at most four cuts
proves: [correctness]
status: full
---

We use the pseudocode of the page. The window is $W = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$, and the arithmetic is exact. For a side $s$ of $W$, let $H_s$ be its closed half-plane: $H_{\text{LEFT}} = \{x \ge x_{\min}\}$, $H_{\text{RIGHT}} = \{x \le x_{\max}\}$, $H_{\text{BOTTOM}} = \{y \ge y_{\min}\}$ and $H_{\text{TOP}} = \{y \le y_{\max}\}$. Then $W$ is the intersection of the four half-planes, and the bit $s$ of OUTCODE$(p)$ is set if and only if $p \notin H_s$. So OUTCODE$(p) = 0$ if and only if $p \in W$.

Let $S_0$ be the input segment from $P_0$ to $Q_0$, and let $A = S_0 \cap W$ be the answer.

**Lemma 1 (one cut).** Let $P$ and $Q$ be the current end points, with codes $c_P$ and $c_Q$, and assume that $c_P \ne 0$ or $c_Q \ne 0$ and that $c_P \wedge c_Q = 0$. Let $E$ be the end point that line L5 picks, let $O$ be the other end point, and let $s$ be the side that lines L6 to L9 pick. Then the division in that line has a nonzero divisor, the point $X$ it computes lies on the segment $EO$ and on the line of side $s$, and $\overline{EO} \cap W = \overline{XO} \cap W$.

*Proof.* The bit $s$ is set in the code of $E$, so $E \notin H_s$. The bit is not set in the code of $O$, because $c_P \wedge c_Q = 0$, so $O \in H_s$. Take $s = \text{TOP}$; the other sides are the same with other signs. Then $y_E > y_{\max} \ge y_O$, so $y_Q - y_P \ne 0$. The segment meets the line $y = y_{\max}$ at exactly one point, and line L6 computes this point $X$ from the equation of the line through $P$ and $Q$. Because $y_E > y_{\max} \ge y_O$, the point $X$ lies between $E$ and $O$. Each point strictly between $E$ and $X$ has $y > y_{\max}$, so it is not in $H_s$ and not in $W$. So the part of $\overline{EO}$ in $W$ is the part of $\overline{XO}$ in $W$. $\square$

**Lemma 2 (codes shrink).** In Lemma 1, let $c_X$ be the code of $X$, and let $c_E$, $c_O$ be the codes of $E$ and $O$. Then $c_X \subseteq (c_E \cup c_O) \setminus \{s\}$, when we read codes as sets of bits.

*Proof.* $X$ is on the line of side $s$, so it is in $H_s$, and the bit $s$ is not in $c_X$. For any side $r$, the half-plane $H_r$ is convex. If $E$ and $O$ are both in $H_r$, then $X$, which lies on the segment between them, is in $H_r$ too. So if the bit $r$ is in $c_X$, it is in $c_E$ or in $c_O$. $\square$

**Theorem.** COHEN-SUTHERLAND$(P_0, Q_0, W)$ stops after at most four runs of lines L6 to L10. It returns the empty set if $A$ is empty, and otherwise the segment $A$, with its end points in the direction from $P_0$ to $Q_0$.

*Proof.* We use this invariant at the start of each pass of the loop of line L2:

> **(C)** $P$ and $Q$ lie on $S_0$ in the same order as $P_0$ and $Q_0$, the segment $\overline{PQ} \cap W$ equals $A$, and $c_P$ and $c_Q$ are the codes of $P$ and $Q$.

Line L1 makes (C) true. If line L3 returns, both end points are in $W$. The window is convex, so the whole segment $\overline{PQ}$ is in $W$, and by (C) it equals $A$. If line L4 returns, a bit $r$ is set in both codes, so $P$ and $Q$ are both outside the closed half-plane $H_r$. The complement of $H_r$ is convex, so the whole segment $\overline{PQ}$ is outside $H_r$ and outside $W$, and by (C) the set $A$ is empty. Otherwise Lemma 1 applies, and line L10 replaces $E$ by a point $X$ on the segment $EO$ with $\overline{XO} \cap W = \overline{EO} \cap W$. The new end point stays in the same place in the order, and line L10 recomputes its code, so (C) stays true.

For the bound, let $\sigma = |c_P| + |c_Q|$ be the total number of set bits. A code has at most one bit for each axis, so $\sigma \le 4$ at the start. Consider one cut, with the names of Lemma 1. If $c_X \cap c_O \ne \emptyset$, the next pass returns at line L4, so this cut is the last one. Otherwise Lemma 2 gives $c_X \subseteq c_E \setminus \{s\}$, so $|c_X| \le |c_E| - 1$, and $\sigma$ falls by at least one. A cut needs $\sigma \ge 1$ before it, because $E$ has the bit $s$. So all cuts except a possible last one lower $\sigma$ by at least one. If the last cut does not lower $\sigma$, there was $\sigma \ge 1$ before it, so at most three cuts came before it. In both cases there are at most four cuts. After the last cut, the next pass returns at line L3 or line L4, and the first part of the proof applies. $\blacksquare$

The bound is tight. For $W = [0, 10]^2$ and the segment from $(-3, -1)$ to $(13, 11)$, each end point lies in a corner region and needs two cuts: the first cut of each end point lands outside the window on another side.
