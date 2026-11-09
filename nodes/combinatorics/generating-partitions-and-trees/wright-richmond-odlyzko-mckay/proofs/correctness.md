---
title: The Wright-Richmond-Odlyzko-McKay successor lists every free tree once
proves: [correctness]
status: full
---

We use the notation and the results of the [Beyer-Hedetniemi proof](/beyer-hedetniemi/): level sequences, blocks, the set $\mathcal{C}_n$ of canonical level sequences (the sorted ones), the fact that prefixes of canonical sequences are canonical, and the successor lemma, which says that $\mathrm{succ}(\ell)$, computed from $p = \max\{i : \ell_i \ge 2\}$, is the next smaller element of $\mathcal{C}_n$. The call NEXT with the copy branch, started at a position $p_0$ with $\ell_{p_0} \ge 2$, computes $\mathrm{succ}$ of the sequence $\ell_1, \ldots, \ell_{p_0}, 1, \ldots, 1$, because it reads only positions up to $p_0$ and the parent array there, and it rewrites every position from $p_0$ on. Fix $n \ge 3$.

For $\ell \in \mathcal{C}_n$ whose root has the child blocks $T_1 \ge T_2 \ge \cdots \ge T_m$, write $k = |T_1|$, so $T_1$ occupies the positions $2, \ldots, k + 1$, write $h(T)$ for the height of a block, measured in edges from its first node, and let $Q(\ell) = (0, \ell_{k+2}, \ldots, \ell_n)$, the level sequence of the root with $T_2, \ldots, T_m$. The height of $\ell$ is $H = h(T_1) + 1$.

**Fact 1.** In a canonical sequence, a block of larger height is larger. So $h(T_1) \ge h(T_2) \ge \cdots$, a canonical sequence of height $H$ starts with $0, 1, \ldots, H$, and if two canonical sequences of the same length satisfy $u \le v$, then the height of $u$ is at most the height of $v$.

*Proof.* A sorted block of height $g$ at level $c$ starts with $c, c + 1, \ldots, c + g$, because at every node the child of greatest height comes first, by induction. If two blocks at level $c$ have heights $g < g'$, they agree up to the entry $c + g$, and then the second block has $c + g + 1$, while the first one has a smaller entry or ends. $\square$

**Lemma 1 (Theorem 4.3 in Ruskey's book).** Root each free tree $T$ at its center, or, if $T$ has two adjacent centers $u$ and $v$, cut the edge $uv$ into the rooted parts $T_u$ and $T_v$ and root $T$ at $u$ if $T_v \prec T_u$ and at $v$ otherwise, where $S \prec S'$ means $|S| < |S'|$, or $|S| = |S'|$ and the canonical sequence of $S$ is smaller. Let $\mathcal{V}_n$ be the set of canonical sequences of these rooted versions. Then $\ell \in \mathcal{C}_n$ is in $\mathcal{V}_n$ if and only if

- (A) $m \ge 2$, and
- (B1) $h(T_2) = h(T_1)$, or
- (B2) $h(T_2) = h(T_1) - 1$, and (C) $k \le n - k$, and (D) if $k = n - k$, then $T_1 - 1 \le Q(\ell)$, where $T_1 - 1$ subtracts $1$ from each entry.

Each free tree has exactly one rooted version, so $\mathcal{V}_n$ is in bijection with the free trees with $n$ nodes.

*Proof.* The centers of a tree are the middle node or the two middle nodes of any longest path. Every path either stays inside one $T_j$ plus the root or passes through the root between two different subtrees. If $m \ge 2$ and $h(T_2) = h(T_1)$, a longest path has length $2H$ and passes through the root at its middle, so the root is the only center. If $m \ge 2$ and $h(T_2) = h(T_1) - 1$, every path has length at most $2H - 1$, a path from a deepest node of $T_1$ through the root into $T_2$ has this length, and its middle edge joins the root to the first node of $T_1$; these are the two centers. If $m = 1$, the root is a leaf, and for $n \ge 3$ a leaf is not a center. If $h(T_2) \le h(T_1) - 2$, the first node of $T_1$ has a smaller largest distance than the root, so the root is not a center. So the root is a center exactly when (A) and (B1) or (B2) hold. In case (B2), $T_v = T_1 - 1$ and $T_u$ has the sequence $Q(\ell)$, which is canonical because $T_2, \ldots, T_m$ are sorted, so the rule chooses the root $u$ exactly when (C) and (D) hold. If $T_u$ and $T_v$ are isomorphic, the two choices give the same rooted tree. $\square$

**Lemma 2 (the start).** The sequence $\pi = 0, 1, \ldots, \lfloor n/2 \rfloor, 1, 2, \ldots, \lceil n/2 \rceil - 1$ is the largest element of $\mathcal{V}_n$.

*Proof.* It is the path rooted at a center, and it satisfies the conditions: for odd $n$ both subtrees are paths of height $(n - 3)/2$, and (B1) holds; for even $n$, $T_1$ is a path with $n/2$ nodes, $Q(\pi)$ is the same path, and (B2), (C) and (D) hold with equality. Let $w \in \mathcal{V}_n$ have height $H$. Then $T_1$ has at least $H$ nodes and $T_2$ has at least $H - 1$, so $n \ge 2H$ and $H \le \lfloor n/2 \rfloor$. If $H < \lfloor n/2 \rfloor$, then $w < \pi$ at position $H + 2$ by Fact 1. Let $H = \lfloor n/2 \rfloor$, so $w$ and $\pi$ agree on the first $H + 1$ entries. If $w_{H+2} \ge 2$, then $|T_1| \ge H + 1$, and the rest has at most $n - H - 2 \le H - 1$ nodes; its height is at most $H - 2$, which is one less than $h(T_1) = H - 1$, so (B1) fails, and (C) fails because $H + 1 > n - H - 1$. So $w_{H+2} = 1$, and a level sequence that continues from $1$ is at most $1, 2, 3, \ldots$ entry by entry. So $w \le \pi$. $\square$

From now on let $x \in \mathcal{V}_n$, not the star, and let $s = \mathrm{succ}(x)$, the next smaller element of $\mathcal{C}_n$. If $s \in \mathcal{V}_n$, it is the next smaller element of $\mathcal{V}_n$, because $\mathcal{V}_n \subseteq \mathcal{C}_n$. So assume that $s \notin \mathcal{V}_n$. Let $p$ be the position used by $\mathrm{succ}$, and let $k$ and $T_1$ be those of $s$.

**Lemma 3 (where the step happens).** $s$ satisfies (A), the step did not change $T_1$, so $T_1(s) = T_1(x)$, and $x$ satisfies $n - k \ge h(T_1) + 1$ and $k \le n - k$.

*Proof.* Suppose $p$ lies in $T_1(x)$. Then all later entries of $x$ are $1$, so $h(T_2(x)) = 0$, and (B1) or (B2) for $x$ gives $h(T_1(x)) = 1$: $x = 0, 1, 2, \ldots, 2, 1, \ldots, 1$ with $|T_1(x)| \le n - |T_1(x)|$ by (C). Then $\mathrm{succ}$ copies $A = 1, 2, \ldots, 2$, with one $2$ less than $T_1(x)$, from position $p$ on. The second copy fits, because $n - 1 - |A| = n - |T_1(x)| \ge |A| + 1$, so $T_1(s) = T_2(s) = A$, and $s$ satisfies (A) and (B1), against the assumption. So $p$ lies after $T_1(x)$. Since $x$ satisfies (A), $x_{k'+2} = 1$ for $k' = |T_1(x)|$, while $x_p \ge 2$, so $p \ge k' + 3$. The step keeps the positions before $p$, so $s$ agrees with $x$ on $1, \ldots, k' + 2$. Hence $T_1(s) = T_1(x)$, $k = k'$, and $s_{k+2} = 1$, which is (A) for $s$. Finally, $x$ satisfies $h(T_2(x)) \ge h(T_1) - 1$, so the rest of $x$ has at least $h(T_1)$ nodes, $n - 1 - k \ge h(T_1)$, and $x$ satisfies (C). $\square$

**Lemma 4 (failure is inherited).** No $w \in \mathcal{V}_n$ with $w \le s$ agrees with $s$ on the positions $1, \ldots, k + 1$.

*Proof.* Let $w \in \mathcal{C}_n$, $w \le s$, with the same first $k + 1$ entries. Since $s_{k+2} = 1$ by (A), also $w_{k+2} = 1$, so $T_1(w) = T_1(s)$ and $Q(w) \le Q(s)$. By Fact 1, $h(T_2(w)) \le h(T_2(s))$. Now $s$ fails, so one of three things holds. If $h(T_2(s)) \le h(T_1) - 2$, then the same holds for $w$, and (B1) and (B2) fail. If $h(T_2(s)) = h(T_1) - 1$ and (C) fails, then (B1) fails for $w$ and (C) fails for $w$, because $k$ is the same. If $h(T_2(s)) = h(T_1) - 1$, $k = n - k$ and (D) fails, then $T_1 - 1 > Q(s) \ge Q(w)$, so (D) fails for $w$, and (B1) fails. $\square$

So the next element of $\mathcal{V}_n$ below $x$ is the largest $w \in \mathcal{V}_n$ with $(w_1, \ldots, w_{k+1}) < (s_1, \ldots, s_{k+1})$.

**Lemma 5 (the jump).** Let $y^*$ be the largest $y \in \mathcal{C}_n$ with $(y_1, \ldots, y_{k+1}) < (s_1, \ldots, s_{k+1})$. Line L4, the call of NEXT at $p_0 = k + 1$ with the copy branch, computes $y^*$, or returns LAST when there is no such $y$.

*Proof.* Let $s^* = s_1, \ldots, s_{k+1}, 1, \ldots, 1$. It is canonical: the prefix is canonical, and blocks $(1)$ after it are the smallest blocks at level $1$. A canonical $y$ satisfies $y < s^*$ exactly when its first $k + 1$ entries are smaller, since $s^*$ has the smallest possible entries after position $k + 1$. So $y^* = \mathrm{succ}(s^*)$, which is what the call computes. If $k \ge 2$, then $s_{k+1} \ge 2$ and the call starts with $p = k + 1$; if $k = 1$, $s^*$ is the star and the call returns LAST. $\square$

**Lemma 6 (the repair).** Let $y^*$ exist, and let $q$ be the parent of $k + 1$ in $s$.

1. If $y^*_{k+1} = 1$, then $y^* \in \mathcal{V}_n$.
2. If $y^*_{k+1} \ge 2$, let $h$ be the largest entry of $y^*$. Then $n \ge 2h + 1$, and the sequence $z$ that keeps $y^*_1, \ldots, y^*_{n-h}$ and ends with $1, 2, \ldots, h$ is the largest element of $\mathcal{V}_n$ that is at most $y^*$.

*Proof.* Write $c = s_q$. The call copies the block $A = s_q, \ldots, s_k$ from position $k + 1$ to the end, so $y^*_{k+1} = c$.

(1) Here $c = 1$, so $q = 2$, $A$ is $T_1$ without its last node, and $y^* = 0, A, A, \ldots, A'$, with $A'$ a prefix of $A$ of length $n - k$, or more full copies. So $T_1(y^*) = A$ and (A) holds. The block $A$ starts with $1, 2, \ldots, 1 + h(A)$, and $h(A) \le h(T_1)$; by Lemma 3, $n - k \ge h(T_1) + 1 \ge h(A) + 1$, so the second block of $y^*$ contains the entries $1, \ldots, 1 + h(A)$ and has height $h(A)$. So (B1) holds.

(2) Here $c \ge 2$, so all entries of $y^*$ after position $2$ are at least $2$, and the root has one child. The entries of $y^*$ are entries of $s_1, \ldots, s_k$, so $h \le h(T_1) + 1$. If $T_1$ is a path, $k = h(T_1) + 1$, the deepest node of $T_1$ is position $k + 1$ itself, and $h \le h(T_1)$; then $n \ge k + h(T_1) + 1 = 2h(T_1) + 2 \ge 2h + 2$ by Lemma 3. Otherwise $k \ge h(T_1) + 2$, and $n \ge k + h(T_1) + 1 \ge 2h(T_1) + 3 \ge 2h + 1$. So $n - h \ge h + 1$.

By Fact 1, $y^*$ starts with $0, 1, \ldots, h$, so the prefix $y^*_1, \ldots, y^*_{n-h}$ contains a node of depth $h$, and it is canonical. Its root has one child block $B$ of height $h - 1$, and the appended path $P = 1, 2, \ldots, h$ is a block of height $h - 1$ that is a prefix of $B$, so $B \ge P$, $z$ is canonical, and $z$ satisfies (A) and (B1). Also $z < y^*$, because $z_{n-h+1} = 1$ while $y^*_{n-h+1} \ge 2$, as $n - h + 1 \ge 3$.

Let $w \in \mathcal{V}_n$ with $z < w \le y^*$. Then $w$ agrees with $y^*$ on the positions $1, \ldots, n - h$, since a first difference there would put $w$ above $y^*$. Let $t = w_{n-h+1}, \ldots, w_n$, so $t > (1, 2, \ldots, h)$. If $t_1 = 1$, then $t$ is a level sequence continuation from $1$, so $t \le (1, 2, \ldots, h)$ entry by entry, a contradiction. If $t_1 \ge 2$, then $T_1(w)$ contains the positions $2, \ldots, n - h + 1$, so $|T_1(w)| \ge n - h$ and the rest has at most $h - 1$ nodes. The height of $w$ is $h$, by Fact 1 and $w \le y^*$, so $h(T_1(w)) = h - 1$, while the rest has height at most $h - 2$; so (B1) fails, and (C) fails because $n - h > h$. So no such $w$ exists. $\square$

**Lemma 7 (the bookkeeping).** Before each test of line L2, $s_2$ and $s_3$ are the starts of $T_2$ and $T_3$, or $n + 1$, and $\mathit{mx}[i]$ is the largest entry from the start of the root's child block that contains $i$ up to $i$. So line L2 decides (A) to (D) of Lemma 1 correctly.

*Proof.* These values at position $i$ depend only on $L_1, \ldots, L_i$. Each call recomputes them at every position that it writes, in increasing order, from the value at the previous position; a start before the first written position stays valid, and the first two entries equal to $1$ from that position on are the new starts. The repair rebuilds them for the rewritten suffix. With them, $k = s_2 - 2$, $h(T_1) + 1 = \mathit{mx}[s_2 - 1]$ and $h(T_2) + 1 = \mathit{mx}[s_3 - 1]$, and (D) is a direct comparison. $\square$

**Theorem.** For $n \ge 3$, the generator visits every free tree with $n$ nodes exactly once, as the canonical sequence of its rooted version, in decreasing lexicographic order, from the path to the star. For $n = 1, 2$ it visits the one tree.

*Proof.* The first visited sequence is the largest element of $\mathcal{V}_n$, by Lemma 2. Let $x \in \mathcal{V}_n$ be visited, and assume that the arrays satisfy the invariants of the Beyer-Hedetniemi proof and Lemma 7. If $x$ is the star, line L1 returns LAST, and the star is the smallest element of $\mathcal{C}_n$. Otherwise line L1 computes $s = \mathrm{succ}(x)$. If line L2 accepts $s$, it is the next element of $\mathcal{V}_n$. If not, Lemmas 3 and 4 show that the next element is the largest $w \in \mathcal{V}_n$ whose first $k + 1$ entries are smaller than those of $s$; line L3 reads $k$; line L4 computes $y^*$ by Lemma 5, or stops when no such $w$ can exist. By Lemma 6, $y^*$ is the next element if its root has two or more children, which line L5 detects by $L[k + 1] = 1$, and otherwise lines L6 and L7 turn it into the next element $z$. The new sequence is again canonical with correct arrays, and $p = n$ satisfies the Beyer-Hedetniemi invariant. By induction, the visited sequences are the elements of $\mathcal{V}_n$ in decreasing order, which by Lemma 1 are the free trees, each once. $\blacksquare$
