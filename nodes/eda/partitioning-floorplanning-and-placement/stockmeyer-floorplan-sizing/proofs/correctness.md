---
title: Stockmeyer's sizing returns a least-area realization of a slicing floorplan in O(n d) time
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page. A *shape* is a pair $(w, h)$ of positive integers. The shape $(w, h)$ *dominates* $(w', h')$ if $w \le w'$ and $h \le h'$ and the two are different. For a set $P$ of shapes, the *front* of $P$ is the set of shapes of $P$ that no shape of $P$ dominates. We write a front as a list by increasing width. Then the heights strictly decrease, because two shapes of a front with $w \le w'$ and $h \le h'$ would be equal or one would dominate the other.

For a node $v$ of the slicing tree, a *realization* of $v$ gives each block below $v$ one of its allowed shapes. Its width and height are computed as in EVALUATE on the page of the [normalized Polish expression](/normalized-polish-expression/). Let $P(v)$ be the set of $(W, H)$ pairs of all realizations of $v$, and let $F(v)$ be its front.

**Lemma 1 (monotonicity).** At a $V$ node with children $a$ and $b$, the pair of the node is $(W_a + W_b, \max(H_a, H_b))$, and at an $H$ node it is $(\max(W_a, W_b), H_a + H_b)$. Both maps do not decrease when any argument increases. So if a realization of $a$ is changed to one whose pair dominates the old pair, the pair of the node does not get larger in either coordinate.

*Proof.* Sums and maxima of nonnegative numbers are monotone in each argument. $\square$

**Lemma 2.** $F(v)$ is the front of the set of pairs obtained by combining one pair of $F(a)$ with one pair of $F(b)$.

*Proof.* Let $p$ be a pair of $F(v)$, from realizations of $a$ and $b$ with pairs $p_a$ and $p_b$. If $p_a \notin F(a)$, some $q_a \in F(a)$ dominates $p_a$ (the set is finite), and by Lemma 1 the combination of $q_a$ and $p_b$ is at most $p$ in both coordinates. It is in $P(v)$ and $p$ is in the front, so it is equal to $p$. Do the same for $b$. So every pair of $F(v)$ is a combination of front pairs. All combinations of front pairs are in $P(v)$, so the front of the combinations is $F(v)$. $\square$

**Lemma 3 (MERGE-V).** Let $A$ and $B$ be fronts, by increasing width. MERGE-V$(A, B)$ returns the front of $\{(w_A[i] + w_B[j], \max(h_A[i], h_B[j]))\}$, by increasing width, with $|R| \le |A| + |B| - 1$. Each entry has a back pointer $(i, j)$ to a pair that gives it.

*Proof.* Let $M = \max(h_A[i], h_B[j])$ for the current $(i, j)$. We claim this invariant at line L10: every $i' < i$ has $h_A[i'] > M$, and every $j' < j$ has $h_B[j'] > M$. At the start there are no such indices. If line L11 moves $i$ to $i + 1$, then $h_A[i] > h_B[j]$ and $M = h_A[i]$. The new maximum $M'$ is $\max(h_A[i+1], h_B[j]) < h_A[i]$, because the heights of $A$ decrease. Every $i' \le i$ has $h_A[i'] \ge h_A[i] > M'$, and every $j' < j$ had $h_B[j'] > M \ge M'$. Line L12 is the same with the roles of $A$ and $B$ exchanged. In line L13, $h_A[i] = h_B[j] = M$, both indices move, and $M' < M$ for the same reason.

So at line L10, $i$ is the least index with $h_A[i] \le M$ and $j$ is the least index with $h_B[j] \le M$, and the widths increase with the index. A combination with height at most $M$ needs $h_A[i'] \le M$ and $h_B[j'] \le M$, so $i' \ge i$ and $j' \ge j$, and its width is at least $w_A[i] + w_B[j]$. So the entry of line L10 is the narrowest combination of height at most $M$, and its height is exactly $M$. Hence no combination dominates it, and it is on the front.

The values of $M$ strictly decrease from step to step, as shown, and the widths strictly increase, because at least one index moves. So $R$ lists distinct front pairs by increasing width. Write the entries as $(W_1, M_1), \ldots, (W_t, M_t)$. It remains to show that every front pair $(W^*, M^*)$ is one of them. The first entry is the narrowest of all combinations, so $M^* \le M_1$, or the first entry would dominate $(W^*, M^*)$. When the loop stops after entry $t$, the index of a list that gives $M_t$ is at the end of that list, so every combination has height at least $M_t$, and $M^* \ge M_t$. Now take an entry $s < t$ and a combination $(i', j')$ of height $h < M_s$. Each index that moved after entry $s$ pointed to a part of height exactly $M_s$, and the part $i'$ or $j'$ of the same list has height less than $M_s$, so it lies after the moved index. So $i' \ge i_{s+1}$ and $j' \ge j_{s+1}$, and the width of the combination is at least $W_{s+1}$. If $M_{s+1} < h < M_s$, the entry $s + 1$ dominates the combination. So no front pair has a height strictly between two consecutive entries. A front pair of height $M_s$ is the narrowest combination of height at most $M_s$, so it is entry $s$. Hence every front pair is listed.

Each step before the last moves at least one index, and the indices can move at most $|A| - 1$ and $|B| - 1$ times. So there are at most $|A| + |B| - 1$ steps and entries. $\square$

**Lemma 4 (MERGE-H).** MERGE-H$(A, B)$ returns the front of $\{(\max(w_A[i], w_B[j]), h_A[i] + h_B[j])\}$ with at most $|A| + |B| - 1$ entries.

*Proof.* Exchange the two coordinates. A front by increasing width becomes a front by decreasing width, so reversing the lists gives inputs for MERGE-V, and the reverse of the output, with the coordinates exchanged back, is the front of the $H$ combinations by Lemma 3. $\square$

**Theorem 1 (correctness).** STOCKMEYER returns the least area $W \cdot H$ over all realizations of the floorplan, and shapes of the blocks that reach it.

*Proof.* For a leaf, line L2 pushes the front of the allowed shapes. By Lemmas 2, 3 and 4 and induction on the tree, line L3 pushes $F(v)$ for each node $v$. So $R = F(r)$ for the root $r$. The area $W \cdot H$ is monotone in both coordinates, so a realization of least area can be changed to one whose pair is on the front without making the area larger. Hence the least area over $F(r)$, taken in line L5, is the least area over all realizations. The back pointers of each entry point to entries of the children that combine to it, so line L6 reaches one shape for each leaf, and by induction the realization built from these shapes has exactly the pair of entry $k$. $\square$

**Theorem 2 (list lengths).** Let $k_i$ be the number of non-dominated allowed shapes of block $i$. For each node $v$ with $\ell(v)$ leaves, $|F(v)| \le \sum_{i \text{ below } v} k_i - (\ell(v) - 1)$. If every block has at most two shapes, a rectangle and its rotation, then $|F(v)| \le \ell(v) + 1$.

*Proof.* By induction with Lemmas 3 and 4: $|F(v)| \le |F(a)| + |F(b)| - 1$, and $\ell(v) = \ell(a) + \ell(b)$. With $k_i \le 2$ the bound is $2\ell(v) - \ell(v) + 1$. $\square$

**Theorem 3 (time).** Let $K = \sum_i k_i$ and let $d$ be the depth of the tree. STOCKMEYER takes $O(K d + \sum_i |S_i| \log |S_i|)$ time. For blocks with two orientations this is $O(n d)$, which is $O(n^2)$ in the worst case and $O(n \log n)$ for a balanced tree.

*Proof.* Line L2 sorts each list. A merge at node $v$ takes $O(|F(a)| + |F(b)|)$ time, which is $O(K(v))$ where $K(v)$ is the number of shapes of the blocks below $v$, by Theorem 2. The sum of $K(v)$ over the internal nodes counts each block $i$ with weight $k_i$ one time for each proper ancestor, so it is at most $K d$. Line L6 visits each node one time. With $k_i \le 2$, $K \le 2n$. The depth is at most $n - 1$, and it is $O(\log n)$ for a balanced tree. $\blacksquare$
