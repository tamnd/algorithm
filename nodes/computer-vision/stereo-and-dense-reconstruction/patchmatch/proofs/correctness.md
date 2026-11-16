---
title: PatchMatch keeps valid distances that never increase, and propagation fills a coherent rectangle in two passes
proves: [correctness]
status: full
---

We use the pseudocode of the page. A center of $A$ is a pixel whose patch of radius $r$ lies inside $A$, and the same for $B$. We write $\operatorname{dist}(a, b)$ for the SSD of the patch of $A$ at $a$ and the patch of $B$ at $b$, so $\operatorname{dist}(a, b) \ge 0$.

**Lemma 1 (invariant).** At every point of the run, for every center $a$ of $A$: (a) $a + f[a]$ is a center of $B$; (b) $D[a] = \operatorname{dist}(a, a + f[a])$; (c) the value of $D[a]$ is never larger than any earlier value of $D[a]$.

*Proof.* After line L1, $f[a] = b_0 - a$ for a center $b_0$ of $B$, and $D[a] = \operatorname{dist}(a, b_0)$, so (a) and (b) hold. Only lines L6 and L11 change $f[a]$ or $D[a]$. Line L6 sets $f[a] \leftarrow f[n]$ only after it checks that $b = a + f[n]$ is a center of $B$, and sets $D[a] \leftarrow \operatorname{dist}(a, b)$ at the same time. Line L10 picks $b$ among the centers of $B$ (the square around $v$ always contains $v$, which is a center of $B$ by (a), so the set is not empty), and line L11 sets $f[a] \leftarrow b - a$ and $D[a] \leftarrow \operatorname{dist}(a, b)$ together. So (a) and (b) stay true. Both lines change $D[a]$ only when the new distance is strictly smaller, which gives (c). $\square$

**Corollary.** At the end, $D[a] \ge \min_b \operatorname{dist}(a, b)$ for every $a$, where $b$ ranges over the centers of $B$, and the value of $D[a]$ after $T$ iterations is at most its value after $T' < T$ iterations with the same random numbers in the first $T'$ iterations.

*Proof.* The first claim follows from (a) and (b). The second follows from (c), because the run of $T$ iterations starts with the run of $T'$ iterations. $\square$

**Lemma 2 (propagation).** Let $R = \{(x, y) : x_0 \le x \le x_1,\ y_0 \le y \le y_1\}$ be a rectangle of centers of $A$, and $v$ an offset with these properties: for each $a \in R$, $a + v$ is a center of $B$ and $\operatorname{dist}(a, a + v) = 0$, and $\operatorname{dist}(a, a + u) > 0$ for every other offset $u$ for which $a + u$ is a center of $B$. Suppose that at the start of a forward pass (an odd $k$) some center $q = (x_q, y_q) \in R$ has $f[q] = v$. Then at the end of that pass, $f[a] = v$ for every $a = (x, y) \in R$ with $x \ge x_q$ and $y \ge y_q$. At the end of the next backward pass, $f[a] = v$ for every $a \in R$. This holds with or without the random search.

*Proof.* First a remark. If $f[a] = v$ at some time, then $D[a] = 0$ by Lemma 1, and no later step changes $f[a]$, because a change needs a strictly smaller distance and distances are not negative. Conversely, if $D[a] = 0$ for $a \in R$, then $f[a] = v$ by the uniqueness of the zero offset.

*Forward pass.* The pass visits the centers in row order, and at $a = (x, y)$ line L5 looks at $(x - 1, y)$ and $(x, y - 1)$. We show by induction over the visiting order that, for every $a \in R$ with $x \ge x_q$ and $y \ge y_q$, $f[a] = v$ right after the visit of $a$. For $a = q$ this holds by the remark. For another such $a$, either $x > x_q$, and then $(x - 1, y)$ is in $R$, satisfies the same two bounds, and is visited earlier in the same row; or $x = x_q$ and $y > y_q$, and then $(x, y - 1)$ is in $R$, satisfies the bounds, and is visited in an earlier row. By the induction hypothesis that neighbor $n$ has $f[n] = v$ at the visit of $a$. Line L6 then considers $b = a + v$, which is a center of $B$, with $\operatorname{dist}(a, b) = 0$. Either $D[a] = 0$ already, and then $f[a] = v$ by the remark, or $D[a] > 0$, and then line L6 sets $f[a] = v$. Line L11 cannot change it afterwards, by the remark.

*Backward pass.* The pass visits the centers in reverse row order, and at $(x, y)$ looks at $(x + 1, y)$ and $(x, y + 1)$. By the forward pass and the remark, at the start of this pass $f = v$ on the part $R' = \{(x, y) \in R : x \ge x_q, y \ge y_q\}$, and it stays so. We show by induction over the visiting order that every $a \in R$ has $f[a] = v$ right after its visit. Take $a = (x, y) \in R$. If $a \in R'$ this is already true. Else $x < x_q$ or $y < y_q$.

- If $y \ge y_q$ (so $x < x_q$), the neighbor $(x + 1, y)$ is in $R$ (since $x + 1 \le x_q \le x_1$), and it comes earlier in the reverse order, in the same row. It is in $R'$ or it was visited before, so $f = v$ there.
- If $y < y_q$, the neighbor $(x, y + 1)$ is in $R$ (since $y + 1 \le y_q \le y_1$), and it lies in a later row, so the reverse order visits it earlier. Again $f = v$ there.

In both cases line L6 gives $f[a] = v$ as in the forward pass. $\square$

**Theorem.** PATCHMATCH returns a field $f$ such that every $a + f[a]$ is a center of $B$ and $D[a] = \operatorname{dist}(a, a + f[a]) \ge \min_b \operatorname{dist}(a, b)$, and the distances never increase from one iteration to the next. If the conditions of Lemma 2 hold on a rectangle $R$ and some center of $R$ has the offset $v$ at the start of an odd iteration $k$ with $k + 1 \le T$, the result is exact on all of $R$.

*Proof.* The first part is Lemma 1 and its corollary. The second part is Lemma 2, applied to iterations $k$ and $k + 1$. By the remark in its proof the offsets on $R$ do not change in the later iterations. $\blacksquare$

**What is not proved.** The theorem says nothing about when a first correct offset appears in $R$. That depends on the random initialization and the random search. The estimate of Barnes et al. (Section 3.3, Eqs. 2 and 3) is a probabilistic model under stated assumptions, not a bound for all images.
