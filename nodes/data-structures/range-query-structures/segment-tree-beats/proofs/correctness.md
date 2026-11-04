---
title: Segment tree beats keeps the capped node fields and returns correct sums and maximums
proves: [correctness, termination]
status: full
---

We use the notation of the page. For a node $v$ with range $I(v)$ and an item $i \in I(v)$, the *seen value* is $s_v(i) = \mathit{mx1}[v]$ if $v$ is a leaf, and $s_v(i) = \min(s_c(i), \mathit{mx1}[v])$ otherwise, where $c$ is the child of $v$ whose range holds $i$. For a finite multiset $X$ of numbers, let $\mathrm{fields}(X)$ be the tuple $(\max X, \max\{y \in X : y < \max X\}, |\{y \in X : y = \max X\}|, \sum X)$, with $\max \emptyset = -\infty$. Write $X_v = \{ s_v(i) : i \in I(v) \}$ as a multiset. The invariant is

$$\text{(B)} \qquad (\mathit{mx1}, \mathit{mx2}, \mathit{cnt}, \mathit{sum})[v] = \mathrm{fields}(X_v) \text{ for every node } v, \quad \text{and } A[i] = s_1(i) \text{ for every } i.$$

Besides (B) we keep a second invariant, which says that a pending cap only ever cuts the copies of the maximum of a child:

$$\text{(C)} \qquad \text{for every inner node } v \text{ and child } c \text{ of } v: \text{ if } \mathit{mx1}[c] > \mathit{mx1}[v] \text{, then } \mathit{mx2}[c] < \mathit{mx1}[v].$$

**Lemma 1 (pull).** If $v$ has children $a$ and $b$ whose fields are $\mathrm{fields}(Y_a)$ and $\mathrm{fields}(Y_b)$ for multisets $Y_a$, $Y_b$, then after PULL$(v)$ the fields of $v$ are $\mathrm{fields}(Y_a \uplus Y_b)$, and (C) holds for $v$ and its two children.

*Proof.* The sum of a disjoint union is the sum of the sums (line L5). Let $M_a = \max Y_a$ and $M_b = \max Y_b$. The maximum of the union is $\max(M_a, M_b)$. If $M_a = M_b$, the copies of the maximum are those of both sides, and a value below the maximum is a value of one side below its maximum, so the strict second maximum is the larger of the two second maximums (line L6). If $M_a > M_b$, the copies are those of $a$ only, and the values below the maximum are those of $a$ below $M_a$ together with all of $Y_b$, whose largest is $M_b$, so the strict second maximum is $\max(\mathit{mx2}[a], M_b)$ (line L7). Line L8 is the mirror case. Now $\mathit{mx1}[v] \ge \mathit{mx1}[a], \mathit{mx1}[b]$, so the premise of (C) is false for both children. $\square$

**Lemma 2 (apply).** Let (B) and (C) hold, let $v$ be a node whose parent $p$, if any, has $\mathit{mx1}[p] \ge \mathit{mx1}[v]$, and let $\mathit{mx2}[v] < x$. After APPLY$(v, x)$, the fields of $v$ are $\mathrm{fields}(\{ \min(y, x) : y \in X_v \})$, and (C) still holds.

*Proof.* If $x \ge \mathit{mx1}[v] = \max X_v$, nothing changes. Otherwise $\mathit{mx2}[v] < x < \mathit{mx1}[v]$. The items of $X_v$ above $x$ are exactly the $\mathit{cnt}[v]$ copies of $\max X_v$, since every other item is at most $\mathit{mx2}[v] < x$. Capping lowers each copy by $\mathit{mx1}[v] - x$, which line L9 subtracts from the sum. The new maximum is $x$ with the same count, and the values below it are unchanged, with the largest still $\mathit{mx2}[v] < x$.

For (C) between $p$ and $v$: $\mathit{mx1}[v]$ only goes down, so it stays at most $\mathit{mx1}[p]$. For (C) between $v$ and a child $c$, assume $\mathit{mx1}[c] > x$; we show $\mathit{mx2}[c] < x$. If $\mathit{mx2}[c] = -\infty$ this holds. Otherwise let $y = \mathit{mx2}[c]$, a value of $X_c$. If $\mathit{mx1}[c] \le$ the old $\mathit{mx1}[v]$, the cap of $v$ did not cut $X_c$, so $y$ is a value of $X_v$ below $\max X_c \le \max X_v$, hence $y \le \mathit{mx2}[v] < x$. If $\mathit{mx1}[c] >$ the old $\mathit{mx1}[v]$, then by (C) $y <$ the old $\mathit{mx1}[v]$, so $y$ is not cut, it is a value of $X_v$ below $\max X_v$, and again $y \le \mathit{mx2}[v] < x$. $\square$

**Lemma 3 (push).** Let (B) and (C) hold, and let $v$ be an inner node with $s_1(i) = s_v(i)$ for $i \in I(v)$. After PUSH$(v)$, (B) and (C) hold, no value $s_u(i)$ at $v$ or above has changed, and each child $c$ has $\mathit{mx1}[c] \le \mathit{mx1}[v]$, so that $s_1(i) = s_c(i)$ for $i \in I(c)$.

*Proof.* Let $c$ be a child and $x = \mathit{mx1}[v]$. If $\mathit{mx1}[c] \le x$, line L9 does nothing. Otherwise (C) gives $\mathit{mx2}[c] < x$, and $\mathit{mx1}[c] > x$ is not at most $\mathit{mx1}[v]$, so we cannot use Lemma 2 for $c$ as stated; but its proof of the fields and of (C) toward the children of $c$ uses only $\mathit{mx2}[c] < x$, so the fields of $c$ become those of $\{ \min(y, x) : y \in X_c \}$, which is $X_v$ on $I(c)$, and (C) holds below $c$. Now $\mathit{mx1}[c] \le x = \mathit{mx1}[v]$, so (C) holds between $v$ and $c$. The new $s_c(i)$ equals the old $s_v(i)$, and $s_v(i) = \min(s_c(i), x)$ is unchanged, so no value at $v$ or above changes and (B) holds. Since $\mathit{mx1}[c] \le \mathit{mx1}[v]$, the cap of $v$ does not cut $s_c$, and $s_1(i) = s_v(i) = s_c(i)$ on $I(c)$. $\square$

**Lemma 4 (chmin).** Let (B) and (C) hold, and call CHMIN$(v, lo, hi, l, r, x)$ on a node $v$ with $I(v) = [lo, hi]$ such that $\max X_v$ is not above the cap of any ancestor, that is, $s_1(i) = s_v(i)$ for $i \in I(v)$. After the call, (B) and (C) hold, (B) for the array $A'$ with $A'[i] = \min(A[i], x)$ for $i \in [l, r] \cap I(v)$ and $A'[i] = A[i]$ otherwise, and the fields of $v$ are $\mathrm{fields}$ of the new values of $I(v)$.

*Proof.* By induction on $hi - lo$. If line L11 returns because $I(v)$ misses $[l, r]$, nothing changes, which is right. If it returns because $\mathit{mx1}[v] \le x$, every value of $I(v)$ is at most $x$ and the chmin does nothing on it. If line L12 applies, $I(v) \subseteq [l, r]$, the parent of $v$ was pushed before the call so that $\mathit{mx1}$ of the parent is at least $\mathit{mx1}[v]$, and Lemma 2 gives the fields of $\{ \min(y, x) : y \in X_v \}$ and keeps (C); the seen values $s_v(i)$ become $\min(s_v(i), x)$, which by the assumption on the ancestors are the new $A'[i]$; the caps of the ancestors are at least the old $\max X_v > x$, so they still do not cut. Otherwise $v$ is not a leaf, because a leaf has $\mathit{mx2} = -\infty < x$ and a leaf that meets $[l, r]$ lies inside it. Line L13 pushes, which by Lemma 3 keeps (B) and (C) and makes each child satisfy the assumption of the lemma. By the hypothesis, the two calls of line L14 update the children correctly, and they do not touch each other's subtrees. Then $X_v$ is again $\{ \min(s_c(i), \mathit{mx1}[v]) \}$, but the children may now have smaller maximums, so line L15 recomputes the fields of $v$ from the children by Lemma 1, which also restores (C) for $v$. After this, $\mathit{mx1}[v]$ is the maximum of the children, so it caps nothing, and the fields of $v$ are those of the new values of $I(v)$. $\square$

**Lemma 5 (query).** Under the same assumption on $v$ as in Lemma 4, QUERY-SUM$(v, lo, hi, l, r)$ returns $\sum_{i \in [l, r] \cap I(v)} A[i]$, and leaves (B) and (C) true. The same holds for QUERY-MAX with $\max$ and $-\infty$.

*Proof.* By induction on $hi - lo$. Lines L16 and L17 return the empty sum or, by (B) and the assumption, the sum of the true values of $I(v)$. Otherwise line L18 pushes, which keeps (B) and (C) and gives each child the assumption, by Lemma 3, and the two recursive results add up to the answer. $\square$

**Termination.** Each recursive call of BUILD, CHMIN and QUERY is on a child, whose range is strictly shorter, and no call recurses on a leaf: in CHMIN, a leaf either meets line L11 or satisfies line L12, as shown in Lemma 4. PULL, APPLY and PUSH do $O(1)$ work.

**Theorem.** After BUILD on $A$ and any sequence of operations, CHMIN$(1, 0, n - 1, l, r, x)$ performs the chmin on $[l, r]$, and QUERY-SUM and QUERY-MAX at the root return the sum and the maximum of $A[l \ldots r]$ for the current array.

*Proof.* BUILD establishes (B) and (C) by Lemma 1, with no caps cutting. The root has no ancestors, so Lemmas 4 and 5 apply to the root, and they keep (B) and (C). Induction over the sequence of operations gives the claim, and each call ends by the termination argument. $\blacksquare$
