---
title: Fusion node rank by sketches is exact
proves: [correctness, invariant, termination]
status: full
---

Fix a node with keys $x_0 < \cdots < x_{k-1}$, positions $D$ and sketches as in the page. For $w$-bit numbers $a \ne b$, write $\delta(a, b) = \mathrm{msb}(a \oplus b)$, the highest position where they differ. Above $\delta(a, b)$ they agree, and $a < b$ exactly when $a$ has 0 at $\delta(a, b)$.

**Lemma 1.** For keys $x_a < x_b$ of the node, $\delta(x_a, x_b) \in D$.

*Proof.* Let $t = \max_{a \le j < b} \delta(x_j, x_{j+1})$, which is in $D$. Each consecutive pair agrees above $t$, so $x_a$ and $x_b$ agree above $t$. At $t$, the sequence $x_a, \ldots, x_b$ is increasing and agrees above $t$, so its bits at $t$ are a run of 0 then a run of 1, and some consecutive pair differs at $t$; so $x_a$ has 0 and $x_b$ has 1 at $t$, and $\delta(x_a, x_b) = t$. $\square$

**Lemma 2.** If $z$ and a key $x$ differ and $\delta(z, x) \in D$, then $\mathrm{sketch}(z) < \mathrm{sketch}(x)$ exactly when $z < x$, and the sketches differ.

*Proof.* The sketch bits come from positions of $D$ in decreasing order. At the positions of $D$ above $\delta(z, x)$ both agree; at $\delta(z, x)$ they differ, in the same direction as $z$ and $x$. $\square$

By Lemmas 1 and 2, the sketches of the keys are strictly increasing.

**Lemma 3 (packed rank).** For $0 \le s \le 2^r$, PACKED-RANK$(v, s) = |\{j : \mathrm{sketch}(x_j) < s\}|$.

*Proof.* $Q = sM$ has $s$ in each field, since $s < 2^{r+1}$. Field $j$ of $K$ is $2^r + \mathrm{sketch}(x_j)$, and $0 \le 2^r + \mathrm{sketch}(x_j) - s < 2^{r+1}$, so $K - Q$ is the field-wise difference with no borrow between fields. Its bit $r$ is set exactly when $2^r + \mathrm{sketch}(x_j) - s \ge 2^r$. So $T$ has one bit for each $j$ with $\mathrm{sketch}(x_j) \ge s$, and line L11 returns the count of the other keys. $\square$

Now let $q$ be a query that is not a key of the node. Let $\ell = \min_j \delta(q, x_j)$, so the keys with $\delta(q, x_j) = \ell$ are those with the longest common prefix with $q$; call this set the block $\mathcal{B}$. Write $P$ for the bits of $q$ above $\ell$.

**Lemma 4.** $\mathcal{B}$ is a nonempty set of consecutive keys, and for each key $x \notin \mathcal{B}$, $\delta(q, x) \in D$ and $\delta(q, x) > \ell$. With $i$ the value of line L2, at least one of $x_{i-1}$, $x_i$ (those that exist) is in $\mathcal{B}$, so line L3 picks $y \in \mathcal{B}$, and $\delta(q, y) = \ell = p$.

*Proof.* $\mathcal{B}$ is the set of keys whose bits above $\ell$ are $P$ and whose bit at $\ell$ is not that of $q$; since no key agrees with $q$ at $\ell$ and above (by the choice of $\ell$), $\mathcal{B}$ is the set of keys with prefix $P$, an interval of the sorted order, and it is nonempty. Take $x \notin \mathcal{B}$ and $y \in \mathcal{B}$. Then $j = \delta(q, x) > \ell$, and $y$ agrees with $q$ at all positions $\ge j$, so $\delta(x, y) = j$, which is in $D$ by Lemma 1. Since $q$ and $y$ agree at $j$ and above, Lemma 2 for $z = q$ shows that $\mathrm{sketch}(x) < \mathrm{sketch}(q)$ exactly when $x < q$, which holds exactly when $x < y$, that is, when $x$ is before the block. So the keys with sketch $< \mathrm{sketch}(q)$ are all keys before the block and some keys of the block, which by the order of sketches are a prefix of the block. Hence $a \le i \le b + 1$ where $x_a, \ldots, x_b$ is the block. If $i = a$ then $x_i \in \mathcal{B}$; if $i = b + 1$ then $x_{i-1} \in \mathcal{B}$; otherwise both are. Line L3 compares $q \oplus x_{i-1}$ and $q \oplus x_i$ as numbers; the smaller one has the lower top bit, so it picks a key with $\delta = \ell$. $\square$

If $q$ is a key, then $q$ itself has the longest common prefix, and the same argument with $\mathcal{B} = \{q\}$ (and $\ell = -1$) shows that $q \in \{x_{i-1}, x_i\}$. Its sketch is not less than itself, so $q = x_i$, which is what line L4 returns.

**Lemma 5 (the corrected rank).** Line L6 or L7 returns $|\{j : x_j \le q\}| - 1$.

*Proof.* Let $p = \ell$ from Lemma 4.

*Case bit $p$ of $q$ is 1.* The keys of $\mathcal{B}$ have prefix $P$ and bit 0 at $p$, so they are all $< q$; each other key is $< q$ exactly when it is $< e$, where $e = P\,0\,1\cdots1$, because $e$ and $q$ agree above $p$ and the other keys differ from both above $p$. So the number of keys $\le q$ is the number of keys $\le e$. Now count by sketch. For $x \notin \mathcal{B}$, $\delta(e, x) = \delta(q, x) \in D$, so by Lemma 2 the sketch comparison with $e$ is strict and correct. For $x \in \mathcal{B}$, $x \le e$ (it has prefix $P\,0$, and $e$ is the largest number with that prefix), and $\mathrm{sketch}(x) \le \mathrm{sketch}(e)$: both agree at the positions of $D$ at $p$ and above, and below $p$, $e$ has only ones. So $|\{j : \mathrm{sketch}(x_j) \le \mathrm{sketch}(e)\}| = |\{j : x_j \le e\}|$, and by Lemma 3 with $s = \mathrm{sketch}(e) + 1 \le 2^r$ this is what line L6 computes.

*Case bit $p$ of $q$ is 0.* The keys of $\mathcal{B}$ have bit 1 at $p$, so they are all $> q$; with $e = P\,1\,0\cdots0$, each other key is $< q$ exactly when it is $< e$. So the number of keys $\le q$ (equal to the number $< q$, as $q$ is not a key) is the number of keys $< e$. For $x \notin \mathcal{B}$ the sketch comparison is strict and correct as before. For $x \in \mathcal{B}$, $x \ge e$ and $\mathrm{sketch}(x) \ge \mathrm{sketch}(e)$, since $e$ has only zeros below $p$. So $|\{j : \mathrm{sketch}(x_j) < \mathrm{sketch}(e)\}| = |\{j : x_j < e\}|$, which line L7 computes by Lemma 3. $\square$

So NODE-PRED returns the index of the largest node key $\le q$, or $-1$.

**Theorem.** PRED$(T, q)$ returns $\max\{x \in S : x \le q\}$, or NIL.

*Proof.* Invariant of the loop of line L13: the answer is the larger of $best$ and the largest key $\le q$ in the subtree of $v$ (with NIL below every key), and every key of that subtree is larger than $best$. At the root it holds with $best = $ NIL. In a node, by Lemma 5, $x_j \le q < x_{j+1}$ (with the obvious meaning at the ends). If $x_j = q$, the answer is $q$ (line L15). Otherwise, by (U1), the keys of the subtree of $v$ that are $\le q$ are $x_0, \ldots, x_j$, the subtrees $c_0, \ldots, c_j$, and the part of $c_{j+1}$ that is $\le q$, and all the keys before $c_{j+1}$ are $\le x_j$. So the best candidate outside $c_{j+1}$ is $x_j$ (line L16), every key of $c_{j+1}$ is larger than $x_j$, and moving to $c_{j+1}$ keeps the invariant. The loop ends because the depth grows, and at $v = $ NIL the answer is $best$. $\blacksquare$
