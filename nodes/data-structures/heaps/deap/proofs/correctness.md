---
title: The deap operations keep the two heaps and the partner condition
proves: [correctness, termination]
status: full
---

We use the notation of the page. The keys are in $A[2 \ldots n]$; the level of $i$ is $k(i) = \lfloor \lg i \rfloor$; $\mathrm{PL}(i) = i + 2^{k(i) - 1}$ is the *place* of a min node $i$; $\mathrm{MAX\text{-}PARTNER}(i)$ is $\mathrm{PL}(i)$ if $\mathrm{PL}(i) \le n$ and $\lfloor \mathrm{PL}(i)/2 \rfloor$ else; and $\mathrm{MIN\text{-}PARTNER}(j) = j - 2^{k(j) - 1}$ for a max node $j$. The invariants are (L), (R) and (C) of the page. For a max node $j$, let $S(j)$ be the set of min nodes whose partner is $j$.

## Facts about partners

**Fact 1.** $\mathrm{MAX\text{-}PARTNER}(i) \le n$ for each min node $i \le n$, when $n \ge 3$.

*Proof.* If $\mathrm{PL}(i) > n$, the partner is the parent of $\mathrm{PL}(i)$, which is at level $k(i) - 1$. The tree is complete and $i \le n$ is at level $k(i)$, so every cell of level $k(i) - 1$ is at most $n$. $\square$

**Fact 2.** Let $c' \ge 4$ be a min node with parent $c$. Then $\mathrm{MAX\text{-}PARTNER}(c)$ is $\mathrm{MAX\text{-}PARTNER}(c')$ or its parent. So, under (R), $A[\mathrm{MAX\text{-}PARTNER}(c)] \ge A[\mathrm{MAX\text{-}PARTNER}(c')]$.

*Proof.* $\mathrm{PL}(c) = c + 2^{k(c) - 1} = \lfloor \mathrm{PL}(c')/2 \rfloor$, since $2^{k(c')-1}$ is even. If $\mathrm{PL}(c') \le n$, then $\mathrm{PL}(c) < \mathrm{PL}(c') \le n$, so the partner of $c$ is the parent of the partner of $c'$. Else the partner of $c'$ is $\lfloor \mathrm{PL}(c')/2 \rfloor = \mathrm{PL}(c) \le n$, by Fact 1, and that is also the partner of $c$. $\square$

**Fact 3.** For a max node $j \ge 6$, $\mathrm{MIN\text{-}PARTNER}(\lfloor j/2 \rfloor) = \lfloor \mathrm{MIN\text{-}PARTNER}(j)/2 \rfloor$. And $S(j)$ is $\{\mathrm{MIN\text{-}PARTNER}(j)\}$, together with the children of $\mathrm{MIN\text{-}PARTNER}(j)$ when $j$ is a leaf.

*Proof.* The first part is arithmetic, as in Fact 2. For the second, let $m = \mathrm{MIN\text{-}PARTNER}(j)$; then $\mathrm{PL}(m) = j$, so $m \in S(j)$. Another min node $i$ has the partner $j$ only if $\mathrm{PL}(i) > n$ and $\lfloor \mathrm{PL}(i)/2 \rfloor = j$, so $\mathrm{PL}(i) \in \{2j, 2j + 1\}$, which means $i$ is a child of $m$ and $j$ has no child at $\mathrm{PL}(i)$. If $j$ has a child $2j \le n$, then $2m + 1 < 2j \le n$ and $\mathrm{PL}(2m + 1) = 2j + 1$; this is $\le n$ unless $2j = n$, so a non-leaf $j$ has the extra member $2m + 1$ only when $2j = n$. We record this case: it occurs only when $2j + 1 = n + 1$. For a leaf $j$, both children of $m$, when they exist, have places $2j$ and $2j + 1$ beyond $n$, so they are in $S(j)$. Grandchildren of $m$ do not exist, since they would be at level $k(j) + 2$, beyond the level of the children of $j$, which do not exist. $\square$

**Lemma 0.** If (L), (R) and (C) hold and $n \ge 3$, then $A[2]$ is a smallest key and $A[3]$ a largest key. If $n = 2$, the one key $A[2]$ is both.

*Proof.* A min key is at least $A[2]$ by (L), and at most the key of its partner, which is at most $A[3]$ by (R). A max key $A[j]$ is at most $A[3]$ by (R), and at least $A[\mathrm{MIN\text{-}PARTNER}(j)]$ by (C), which is at least $A[2]$. $\square$

## The sifts

Say that the invariants hold *with $A[t] = h$* if they hold for the array in which the cell $t$ holds the key $h$; the code may treat $t$ as a hole.

**Lemma 1.** Let $t$ be a min node, and let the invariants hold with $A[t] = h$. If $x \le h$, then MIN-SIFT-UP$(t, x)$ stops after at most $k(t) - 1$ iterations, and afterwards the invariants hold with the keys of $A$ changed as follows: $x$ is in some cell $f$ on the path from $t$ up to 2, and the keys on the path from $f$ to the parent of $t$ have moved one cell down, so that the multiset is the old one with $h$ replaced by $x$.

*Proof.* Before each test of line L6, for the current hole $c$, the invariants hold with $A[c] = h_c$ for some $h_c \ge x$; this holds at the start with $h_t = h$. A min node has one lower bound, its parent's key, and its upper bounds are the keys of its children and of its partner. If the test is true, $y = A[\lfloor c/2 \rfloor] > x$ moves into $c$. Then $y$ meets the lower bound of $c$ by (L) at $\lfloor c/2 \rfloor$, and $y \le h_c$ meets the upper bounds of $c$. The parent cell becomes the hole with $h = y > x$, and no constraint at it changed. If the test is false, then $c \le 3$ or $x \ge A[\lfloor c/2 \rfloor]$, and $x \le h_c$ meets the upper bounds of $c$. Each iteration moves up one level, and the loop stops at level 1. $\square$

**Lemma 1'.** The mirror statement holds for MAX-SIFT-UP$(t, x)$ at a max node $t$ with $x \ge h$. A max node has one upper bound, its parent's key, and its lower bounds are the keys of its children and of the nodes of $S(t)$; the proof is the same with the order reversed.

## INSERT

Let the invariants hold for $A[2 \ldots n - 1]$, and let $n$ be the new cell, with the key $x$. If $n = 2$, there is nothing to check.

*A max node $n$.* Let $i = \mathrm{MIN\text{-}PARTNER}(n)$. Before the insert, $\mathrm{PL}(i) = n$ was beyond the end, so the partner of $i$ was $\lfloor n/2 \rfloor$ (or nothing if $n = 3$), and (C) gave $A[i] \le A[\lfloor n/2 \rfloor]$. After the insert, $S(n) = \{i\}$, because $i$ has no children (they would be at level $k(n) + 1$, beyond $n$). So the invariants hold with $A[n] = A[i]$: it meets the upper bound $A[\lfloor n/2 \rfloor]$ and the lower bound $A[i]$.

If $x < A[i]$, line L3 sets $A[n] = A[i]$, and the invariants hold with the hole $i$ and $h = A[i] > x$. Lemma 1 applies. Else $x \ge A[i]$, and Lemma 1' applies to MAX-SIFT-UP$(n, x)$ with $h = A[i]$.

*A min node $n \ge 4$.* Its place is beyond the end, so its partner is $j = \lfloor \mathrm{PL}(n)/2 \rfloor = \mathrm{PL}(\lfloor n/2 \rfloor)$, which is also the partner of the parent of $n$, so (C) gives $A[\lfloor n/2 \rfloor] \le A[j]$. So the invariants hold with $A[n] = A[j]$: $n$ has no children, and $A[j]$ meets its lower bound and its partner bound.

If $A[j] < x$, line L5 moves $A[j]$ to $n$, and the invariants hold with the hole $j$ and $h = A[j] < x$, because the only new member of $S(j)$ is $n$, which holds $A[j]$. Lemma 1' applies. Else Lemma 1 applies to MIN-SIFT-UP$(n, x)$ with $h = A[j] \ge x$.

## Removing the last cell

**Lemma 2.** If the invariants hold for $A[2 \ldots n + 1]$, they hold for $A[2 \ldots n]$.

*Proof.* (L) and (R) lose one edge. If $n + 1$ is a min node, no partner changes. If $n + 1$ is a max node, the only min node whose partner changes is $b = \mathrm{MIN\text{-}PARTNER}(n + 1)$, whose new partner is $q = \lfloor (n + 1)/2 \rfloor$, and $A[b] \le A[n + 1] \le A[q]$ by (C) and (R). $\square$

## EXTRACT-MIN

Let $n \ge 3$ be the size after line L10, and $x$ the key of the removed cell $n + 1$. By Lemma 0, $r = A[2]$ is a smallest key. By Lemma 2, the invariants hold for $A[2 \ldots n]$ with the old key at 2.

*The descent of line L12.* Claim: before each test, with the hole at $c$, the invariants hold for all cells other than $c$, where (L) is read with $c$ skipped, and the key that $c$ held before the descent reached it is at least the key now at its parent. When the smaller child $c'$ moves up to $c$, it is at most its sibling, and at least the key now above $c$, which was above $c'$ before, by (L). For (C) at $c$, Fact 2 gives $A[\mathrm{MAX\text{-}PARTNER}(c)] \ge A[\mathrm{MAX\text{-}PARTNER}(c')] \ge A[c']$. The max side does not change. The loop stops at a leaf $i$ after at most $k(n) - 1$ iterations.

*The placement.* Let $j = \mathrm{MAX\text{-}PARTNER}(i)$. The key now at $\lfloor i/2 \rfloor$, if $i \ge 4$, is the old key of $i$, which was at most $A[j]$ by (C) for $A[2 \ldots n]$. So the invariants hold with $A[i] = A[j]$. If $A[j] < x$, line L14 moves $A[j]$ to $i$; the invariants hold with the hole $j$ and $h = A[j] < x$, since the cell $i \in S(j)$ holds $A[j]$, and Lemma 1' applies. Else Lemma 1 applies to MIN-SIFT-UP$(i, x)$ with $h = A[j] \ge x$. For $n = 2$, line L11 puts $x$ at 2.

## EXTRACT-MAX

Let $n \ge 3$ be the size after line L16, $x$ the key of the removed cell $n + 1$, and $r = A[3]$, a largest key by Lemma 0. If $n + 1$ was a max node, let $b = \mathrm{MIN\text{-}PARTNER}(n + 1)$ and $q = \lfloor (n + 1)/2 \rfloor$; then $A[b] \le x \le A[q]$ before the removal, and $b$ has no children (as in INSERT).

*The descent of line L18.* Let $3 = c_0, c_1, \ldots, c_s = j$ be the path of the hole, where $c_{t+1}$ is the larger child of $c_t$, and $j$ is a leaf. After the descent, $c_t$ holds the old key of $c_{t+1}$ for $t < s$. These keys decrease along the path, and each is at most the old key above it, so (R) holds on the max side with $j$ as a hole. For (C), consider a min node $i$ whose partner is some $c_t$ with $t < s$. If $i = \mathrm{MIN\text{-}PARTNER}(c_t)$, then by Fact 3, $\mathrm{MIN\text{-}PARTNER}(c_{t+1})$ is a child of $i$, so $A[i] \le A[\mathrm{MIN\text{-}PARTNER}(c_{t+1})] \le$ the old $A[c_{t+1}]$, which is the new $A[c_t]$. Else, by Fact 3, $c_t$ is not a leaf, $2c_t = n$, and $i$ is the child $2m + 1$ with place $2c_t + 1 = n + 1$; so $i = b$ and $c_t = q$. So after the descent, (C) can fail only for $b$, and $A[b] \le x$.

*The choice of line L19.* By Fact 3, $S(j)$ is $\mathrm{MIN\text{-}PARTNER}(j)$ and its children; by (L), its largest key is at the larger child if there is one. So $i'$, the node chosen in line L19, holds the largest key of $S(j)$. The key now at the parent of $j$ is the old key of $j$, which is at least every key of $S(j) \setminus \{b\}$, by (C) for $A[2 \ldots n + 1]$ (for a node of $S(j)$ other than $b$, the partner did not change with the removal).

*Case $x \ge A[i']$.* The invariants other than (C) at $b$ hold with $A[j] = A[i']$, because $A[i']$ is at least the keys of $S(j)$ and at most the key above $j$, unless $i' = b$, where $A[b] \le x$ also allows $h = A[i']$. Lemma 1' applies to MAX-SIFT-UP$(j, x)$ with $h = A[i']$. Afterwards, the cells of the path from $j$ up to the final cell $f$ of $x$ hold their old keys again, below $f$, then $x$ at $f$, then the keys above $f$ that are at least $x$, since the loop stopped. So the partner $q$ of $b$, which is on the path or off it, holds a key that is at least $x$ or its old key, and the old key was at least $x$; in both cases it is at least $A[b]$, so (C) holds at $b$ too.

*Case $x < A[i']$.* Then $i' \ne b$, since $A[b] \le x$. Line L20 moves $A[i']$ to $j$; it is at most the key above $j$, as shown, and it is at least the keys of $S(j)$. The node $b$, if it exists, has a partner whose key is now at least $A[i'] > x \ge A[b]$ if it is on the path, and its old key, which is at least $x$, if it is not. So the invariants hold with the hole $i'$ and $h = A[i']$, which is a min leaf whose partner $j$ holds $h$. Lemma 1 applies to MIN-SIFT-UP$(i', x)$.

For $n \le 2$, lines L15 and L17 are correct by Lemma 0 and Lemma 2.

## Theorem

Starting from the empty deap, each sequence of INSERT, EXTRACT-MIN and EXTRACT-MAX keeps (L), (R) and (C), stops after $O(\log n)$ steps per operation, and keeps in $A[2 \ldots n]$ exactly the current multiset; FIND-MIN and FIND-MAX return a smallest and a largest key.

*Proof.* The invariants and the multiset are the cases above, with Lemmas 1 and 1' for the sifts; each loop moves one level per iteration. The answers of the finds and extracts follow from Lemma 0. $\blacksquare$
