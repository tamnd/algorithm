---
title: CLOAK returns the smallest quadtree cell that holds the requester and at least k users
proves: [correctness]
status: full
---

Let $A = [0, 2^h)^2$, let $U$ be a finite multiset of integer points in $A$, let $p \in U$ and let $k \ge 1$. For $0 \le d \le h$ let $C_d$ be the cell of side $2^{h-d}$ that holds $p$, that is $[x, x + s) \times [y, y + s)$ with $s = 2^{h-d}$, $x = s \lfloor p_x / s \rfloor$ and $y = s \lfloor p_y / s \rfloor$. Let $N_d$ be the number of users of $U$ in $C_d$.

**Claim 1 (the chain).** $C_0 = A$, each $C_{d+1}$ is the quadrant of $C_d$ that holds $p$, and $N_0 \ge N_1 \ge \cdots \ge N_h \ge 1$.

*Proof.* The four quadrants of $C_d$ are the cells of side $2^{h-d-1}$ inside it, and they partition it, so exactly one holds $p$, and it is $C_{d+1}$. Since $C_{d+1} \subseteq C_d$, $N_{d+1} \le N_d$. Every $C_d$ holds $p$, which is in $U$, so $N_h \ge 1$. $\square$

The cells that hold $p$ are exactly $C_0, \ldots, C_h$, and they are nested. So the smallest cell that holds $p$ and at least $k$ users is $C_{d^*}$ for the largest $d^*$ with $N_{d^*} \ge k$, if $N_0 \ge k$.

**Claim 2 (invariant).** Each time line L5 runs, $q = C_d$, $V$ is the multiset of users of $U$ in $C_d$, and if $d \ge 1$ then $q_{prev} = C_{d-1}$ and $N_{d-1} \ge k$.

*Proof.* At the first test, lines L1 and L2 give $d = 0$, $q = A = C_0$ and $V = U$. Suppose the claim holds at a test that neither line L5 nor line L6 ends. Then $|V| = N_d \ge k$ and $d < h$. Line L7 sets $q_{prev} = C_d$, line L8 sets $q$ to the quadrant of $C_d$ that holds $p$, which is $C_{d+1}$ by Claim 1, line L9 keeps the users of $V$ in $C_{d+1}$, which are all the users of $U$ in $C_{d+1}$ since $C_{d+1} \subseteq C_d$, and line L10 adds 1 to $d$. So the claim holds at the next test, with $N_d \ge k$ for the old $d$. $\square$

**Claim 3 (the result).** CLOAK returns NONE if $|U| < k$, and otherwise $C_{d^*}$.

*Proof.* If $|U| < k$, line L3 returns NONE. Otherwise $N_0 \ge k$, so line L5 does not return at $d = 0$. The loop stops by $d = h$ at the latest, since $d$ grows by one per pass. By Claim 2 and Claim 1, the tests at line L5 see $N_0, N_1, \ldots$ in turn. If line L5 returns at some $d \ge 1$, then $N_d < k \le N_{d-1}$, and by Claim 1 every later $N$ is also below $k$, so $d^* = d - 1$ and the result $q_{prev} = C_{d-1}$ is correct. If instead line L6 returns at $d = h$, then $N_h \ge k$, so $d^* = h$ and the result is $q = C_h$. $\blacksquare$

**Reciprocity is not implied.** The result depends on $p$ through line L8. The four users $(0, 0)$, $(1, 0)$, $(0, 1)$ and $(3, 3)$ with $h = 2$ and $k = 3$ give $C_{d^*} = [0, 2)^2$ for the first three and $A$ for the last, so the region $A$ is returned for only one user. The test file checks this case and compares the reciprocity check with an oracle.

**Cost.** By Claim 3 the loop makes at most $h + 1$ passes, and each pass scans $V$, which has at most $n$ users, once. The time is $O(n h)$, and $V$ needs $O(n)$ extra space.
