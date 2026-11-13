---
title: Warnsdorff's rule always stops with a valid knight path, and it is not complete
proves: [correctness]
status: full
---

We use the pseudocode of the page on an $m \times n$ board with start square $s$. Write $V$ for the set of visited squares and $v$ for the current square.

**Claim 1 (soundness and termination).** WARNSDORFF stops after at most $mn - 1$ passes of the loop of line L2. The returned path $p_1, \ldots, p_k$ has $p_1 = s$, its squares are distinct, and $p_{i+1}$ is a knight move from $p_i$ for $1 \le i < k$. So it is an open knight's tour exactly when $k = mn$.

*Proof.* We use this invariant of the loop of line L2.

> **(I)** Before each pass: the path is $p_1, \ldots, p_k$ with $p_1 = s$ and $p_k = v$; its squares are distinct; consecutive squares are a knight move apart; and $V = \{p_1, \ldots, p_k\}$.

*Initialization.* Line L1 sets $v = s$, $V = \{s\}$ and the path to $[s]$, so (I) holds with $k = 1$.

*Maintenance.* Assume (I) before a pass. Line L3 builds $C$ from squares one knight move from $v$ that are not in $V$. If $C$ is empty, line L4 returns the path, which satisfies the claim by (I). Otherwise line L6 picks some $u \in C$, which is not in $V$, so it differs from every $p_i$, and is a knight move from $p_k = v$. Line L7 adds $u$ to $V$ and appends it as $p_{k+1}$, and $v$ becomes $u$. So (I) holds again with $k + 1$.

*Termination.* Each pass that does not return increases $k$ by exactly 1, and the loop of line L2 makes at most $mn - 1$ passes, so the algorithm stops. If it stops at line L8, all $mn - 1$ passes added a square, so $k = mn$; since the squares are distinct, the path holds every square of the board once, and it is an open tour. If it stops at line L4, then $k < mn$, and the path is not a tour. $\square$

**Claim 2 (the parity limit).** If $m$ and $n$ are both odd, an open tour starts and ends on a square of the majority color, the color of $(0, 0)$. So from a square of the other color every method fails, Warnsdorff's rule included.

*Proof.* Color $(r, c)$ black when $r + c$ is even. A knight move changes $r + c$ by $\pm 1$ or $\pm 3$, so it changes the color. Along a tour $p_1, \ldots, p_{mn}$ the squares $p_i$ with odd $i$ all have the color of $p_1$, and there are $(mn + 1)/2$ of them. The board has $(mn + 1)/2$ black squares and $(mn - 1)/2$ white squares, so $p_1$ is black, and so is $p_{mn}$, since $mn$ is odd. $\square$

**Claim 3 (not complete).** There is a board and a black start square from which an open tour exists but Warnsdorff's rule, with the move order of the page, does not find one.

*Proof.* On the $5 \times 5$ board with start $(2, 0)$, which is black, the page shows the run of the rule: it reaches 17 squares and then line L3 finds no unvisited knight move, so line L4 returns a path of 17 squares. The page also shows a sequence of all 25 squares starting at $(2, 0)$; each consecutive pair in it is a knight move, which is a finite check of 24 pairs, so it is an open tour from $(2, 0)$. $\square$

So a full-length result is always a tour (Claim 1), but a short result does not prove that no tour exists (Claim 3), except in the parity case of Claim 2.
