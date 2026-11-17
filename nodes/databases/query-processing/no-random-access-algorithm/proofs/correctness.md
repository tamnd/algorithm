---
title: NRA returns a top-k set, its bounds are sound, and it never stops before the threshold algorithm
proves: [correctness, complexity, optimality]
status: full
---

Setting. There are $N$ objects and $m$ lists. List $L_i$ holds each object $R$ once with grade $x_i(R) \ge f$, where $f$ is a fixed floor (0 in the paper), in non-increasing order. The aggregation $t$ is monotone, and $t(R) = t(x_1(R), \ldots, x_m(R))$. Let $k \le N$. A *top $k$ set* is a set $Y$ of $k$ objects with $t(y) \ge t(z)$ for all $y \in Y$, $z \notin Y$.

After round $d$ (line L4), let $\underline{x}_i$ be the grade of the $d$-th entry of $L_i$. For a seen object $R$, let $S(R)$ be the set of lists in which $R$ has been read so far. Line L5 sets

$$W(R) = t(w_1, \ldots, w_m),\ w_i = \begin{cases} x_i(R) & i \in S(R) \\ f & i \notin S(R) \end{cases} \qquad B(R) = t(b_1, \ldots, b_m),\ b_i = \begin{cases} x_i(R) & i \in S(R) \\ \underline{x}_i & i \notin S(R). \end{cases}$$

Line L6 sets $T$ to $k$ seen objects of largest $W$ (ties by larger $B$) and $M = \min_{R \in T} W(R)$. Line L7 stops when $|T| = k$, $B(R) \le M$ for each seen $R \notin T$, and either all $N$ objects are seen or $t(\underline{x}_1, \ldots, \underline{x}_m) \le M$.

**Lemma 1 (sound bounds).** After each round, $W(R) \le t(R) \le B(R)$ for each seen $R$, and $t(R) \le t(\underline{x}_1, \ldots, \underline{x}_m)$ for each unseen $R$.

*Proof.* For $i \in S(R)$ the grade used is exact. For $i \notin S(R)$, $R$ has not been read in $L_i$, so it lies below position $d$, and since $L_i$ is sorted, $f \le x_i(R) \le \underline{x}_i$. Monotonicity of $t$ gives both inequalities. An unseen object lies below position $d$ in every list, so $x_i(R) \le \underline{x}_i$ for all $i$. $\square$

**Theorem 1 (correctness; Fagin, Lotem and Naor, Theorem 8.4).** NRA returns a top $k$ set, and each returned object $R$ comes with bounds $W(R) \le t(R) \le B(R)$.

*Proof.* The bounds hold by Lemma 1. Suppose the test at line L7 succeeds. For $y \in T$, $t(y) \ge W(y) \ge M$. For a seen $z \notin T$, $t(z) \le B(z) \le M$. For an unseen $z$, if there is one, the test gives $t(\underline{x}_1, \ldots, \underline{x}_m) \le M$, so $t(z) \le M$ by Lemma 1. Hence $t(y) \ge M \ge t(z)$ for all $y \in T$ and $z \notin T$.

If the test never succeeds before $d = N$, then after round $N$ every object has been read in every list, so $W(R) = B(R) = t(R)$ for all $R$, and $T$ is a set of $k$ objects of largest $t$; the test then succeeds at once, since each $z \notin T$ has $B(z) = t(z) \le M$ and all objects are seen. $\blacksquare$

**Theorem 2 (cost).** If NRA stops after round $d$, it makes exactly $m d$ sorted accesses and no random accesses. It stores the known grades of at most $\min(N, m d)$ seen objects.

*Proof.* Each round reads one entry of each list, and nothing else is read. $\blacksquare$

**Theorem 3 (no earlier than TA).** If $k < N$, the threshold algorithm, run on the same database, stops at a depth no larger than NRA's.

*Proof.* Let NRA stop after round $d$, and let $\tau = t(\underline{x}_1, \ldots, \underline{x}_m)$ be TA's threshold at depth $d$. First, $\tau \le M$. If some object is unseen, this is part of the test at line L7. Otherwise, since $k < N$, some seen $z \notin T$ exists. For $i \in S(z)$, $z$ was read at a position $\le d$ in the sorted list $L_i$, so $x_i(z) \ge \underline{x}_i$; for $i \notin S(z)$, $b_i = \underline{x}_i$. By monotonicity, $B(z) \ge \tau$, and the test gives $B(z) \le M$.

By depth $d$, TA has made the same sorted accesses as NRA, so it has seen every object of $T$ and knows its exact score, which is at least $W \ge M \ge \tau$. So TA has seen $k$ objects with score at least $\tau$. By the buffer rule of TA, its $k$ buffered objects score at least the $k$-th best seen score, which is at least $\tau$, so TA's stopping test succeeds at depth $d$, if not before. $\blacksquare$

The bound $k < N$ is needed. If $k = N$, NRA stops as soon as all objects are seen, while TA, as stated, waits until its threshold drops below the $N$-th score.

**Instance optimality (cited).** Let $\mathbf{A}$ be the class of algorithms that find a top $k$ set correctly on every database and make no random accesses. Fagin, Lotem and Naor (Theorem 8.5) show that NRA is instance optimal over $\mathbf{A}$ with optimality ratio $m$: there is a constant $c'$ with $\mathrm{cost}(\mathrm{NRA}, D) \le m \cdot \mathrm{cost}(A, D) + c'$ for every $A \in \mathbf{A}$ and every database $D$. The proof shows that if NRA stops at depth $d$ and had already seen $k$ objects by depth $d - 1$, then every $A \in \mathbf{A}$ reads to depth $d$ in at least one list on $D$; otherwise a database that agrees with $D$ down to depth $d - 1$ makes $A$ err. So $A$ makes at least $d$ sorted accesses and NRA makes $m d$. The tie-breaking rule of line L6 (larger $B$ first) is used in this proof. Corollary 8.6 shows that for a strict $t$ the ratio $m$ is exact and best possible. The paper's Example 8.3 shows that NRA, and every algorithm in $\mathbf{A}$, may have to stop without knowing the exact scores of the answer; this is why NRA returns bounds. These results are cited, not proved, here.
