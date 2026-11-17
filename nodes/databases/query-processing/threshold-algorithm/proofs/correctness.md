---
title: The threshold algorithm is correct, stops no later than Fagin's algorithm, and is instance optimal
proves: [correctness, complexity, optimality]
status: full
---

Setting. There are $N$ objects and $m$ lists. List $L_i$ holds each object $R$ once with grade $x_i(R) \in [0, 1]$, in non-increasing order. The aggregation $t$ is monotone, and $t(R) = t(x_1(R), \ldots, x_m(R))$. A *top $k$ set* is a set $Y$ of $\min(k, N)$ objects with $t(y) \ge t(z)$ for $y \in Y$, $z \notin Y$. At depth $d$, let $\underline{x}_i$ be the grade of the $d$-th entry of $L_i$, and $\tau = t(\underline{x}_1, \ldots, \underline{x}_m)$ the threshold of line L7. The middleware cost of a run with $s$ sorted and $r$ random accesses is $s c_S + r c_R$.

**Lemma 1 (buffer).** At each point, the buffer $Y$ of line L6 holds the $\min(k, \text{number seen})$ seen objects of highest score, up to ties: each seen object $z \notin Y$ has $t(z) \le \min_{y \in Y} t(y)$.

*Proof.* When $z$ is processed at line L5, either it enters $Y$, or $Y$ is full and $t(z)$ is at most the smallest score in $Y$. When an object leaves $Y$, it is the one with the smallest score, and the newcomer scores more. The smallest score in a full $Y$ never decreases. So an object that is outside $Y$ scores at most the current smallest score in $Y$. An object of $Y$ that is seen again is skipped, so $Y$ never holds an object twice. $\square$

**Theorem 1 (correctness).** For a monotone $t$, TA returns a top $k$ set with exact scores.

*Proof.* Each object in $Y$ got all its grades by sorted and random access, so its score is exact. If the loop ended at line L9, then $|Y| = \min(k, N)$ and each $y \in Y$ has $t(y) \ge \tau$. A seen object $z \notin Y$ has $t(z) \le t(y)$ by Lemma 1. An unseen object $z$ lies below depth $d$ in each list, so $x_i(z) \le \underline{x}_i$, and by monotonicity $t(z) \le \tau \le t(y)$. If the loop ended because $d = N$, every object was seen, and Lemma 1 gives the claim. $\blacksquare$

**Theorem 2 (no later than FA).** On every database, TA stops at a depth no larger than the depth at which Fagin's algorithm stops.

*Proof.* Suppose FA stops at depth $d$: at least $k$ objects $h$ have been seen in all $m$ lists by depth $d$. For such $h$, $x_i(h) \ge \underline{x}_i$ for each $i$, so $t(h) \ge \tau$. TA has seen each such $h$ by depth $d$ and computed its exact score. By Lemma 1, the $k$ objects of $Y$ score at least the $k$-th highest score among seen objects, which is at least $\min_h t(h) \ge \tau$. So the test at line L9 succeeds at depth $d$, if not before. $\blacksquare$

**Theorem 3 (cost per depth).** If TA stops at depth $d$, it makes $m d$ sorted accesses and at most $m (m - 1) d$ random accesses, and it keeps at most $k$ objects with their scores, plus the $m$ last grades.

*Proof.* Each round makes $m$ sorted accesses and, for each of them, at most $m - 1$ random accesses. $\blacksquare$

**Theorem 4 (instance optimality; Fagin, Lotem and Naor, Theorem 6.1).** Let $\mathbf{A}$ be the class of algorithms that find a top $k$ set correctly on every database and make no *wild guesses* (no random access to an object before it is seen under sorted access). For every $A \in \mathbf{A}$ and every database $D$,

$$\mathrm{cost}(TA, D) \le \Bigl(m + m(m - 1)\frac{c_R}{c_S}\Bigr) \mathrm{cost}(A, D) + c',$$

where $c' = k m c_S + k m (m - 1) c_R$ does not depend on $D$.

*Proof.* Let $A$ see $a$ distinct objects on $D$. Since $A$ makes no wild guesses, it makes at least $a$ sorted accesses, so $\mathrm{cost}(A, D) \ge a c_S$. By Theorem 3, it suffices to show that TA stops by depth $a + k$. By depth $d'$, TA has made $m d'$ sorted accesses and seen each object at most $m$ times, so it has seen at least $d'$ distinct objects (or all of them).

If at most $k$ objects are unseen by $A$, then TA has seen all objects by depth $a + k$ and stops. Otherwise, let $Y_A$ be $A$'s output, and pick an object $V$ that $A$ does not see and that is not in $Y_A$. Let $\tau_A = t(x_1, \ldots, x_m)$, where $x_i$ is the last grade $A$ read under sorted access in list $i$ ($x_i = 1$ if it read none). Call an object *big* if its score is at least $\tau_A$.

*Each member of $Y_A$ is big.* Let $D'$ be $D$ with the grades of $V$ changed to $x_1, \ldots, x_m$, placed in each list below the other objects with the same grade. Then $V$ is still below every position $A$ read in each list, so $A$ sees the same answers and outputs $Y_A$ on $D'$. On $D'$, $t(V) = \tau_A$ and $V \notin Y_A$, so by correctness every member of $Y_A$ scores at least $\tau_A$ on $D'$, and these scores are the same on $D$.

*Two facts about depth.* Each list holds each object once, so the entries that $A$ reads in one list are distinct objects, and $A$ reads at most $a$ entries of each list. Since $A$ makes no wild guesses, each object that $A$ sees is at depth at most $a$ in some list, so TA has seen it by depth $a$. Also, for $d' \ge a$, the grade of TA's $d'$-th entry of $L_i$ is at most the last grade $x_i$ that $A$ read in $L_i$ (or at most 1 if $A$ read none), so TA's threshold at depth $d'$ is at most $\tau_A$ by monotonicity.

*Case 1: $A$ sees every member of $Y_A$.* By depth $a$, TA has seen the $k$ members of $Y_A$, which are big, so they score at least $\tau_A$, which is at least TA's threshold. By Lemma 1, the test at line L9 succeeds by depth $a$.

*Case 2: $A$ does not see some $R \in Y_A$.* Then every object $R'$ that $A$ does not see is big: on the database $D'$ above, $A$ cannot tell $R$ from $R'$, so the output with $R'$ in place of $R$ must also be correct, and it leaves out $V$ with score $\tau_A$; hence $t(R') \ge \tau_A$. By depth $a + k$, TA has seen at least $a + k$ objects, so at least $k$ objects that $A$ did not see, all big. By the depth facts, TA's threshold at depth $a + k$ is at most $\tau_A$. So at least $k$ seen objects score at least TA's threshold, and by Lemma 1 the test at line L9 succeeds by depth $a + k$. $\blacksquare$

Fagin, Lotem and Naor also show (Corollary 6.2) that for a strict $t$ the ratio $m + m(m - 1) c_R / c_S$ is exactly the optimality ratio of TA and that no deterministic algorithm in $\mathbf{A}$ has a lower one, and (Example 6.3 and Theorem 6.4) that if wild guesses are allowed, no algorithm is instance optimal. These are cited, not proved, here.
