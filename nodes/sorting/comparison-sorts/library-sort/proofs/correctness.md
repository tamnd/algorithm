---
title: Library sort returns the stable sorted order
proves: [correctness, termination]
status: full
---

Each inserted item is a pair $(x, p)$ of an item and its input position. Write $(y, i) \prec (x, p)$ when $y < x$, or neither $y < x$ nor $x < y$ and $i < p$. The positions are distinct, so $\prec$ is a strict total order on the pairs, and listing the pairs in $\prec$ order lists the items in the stable sorted order.

Call a slot array *ordered* if its filled slots, read from left to right, are increasing in $\prec$.

**Lemma 1 (spreading).** In line L5, with $k$ items and $L > k$ slots, the slots $\lfloor (2j+1) L / (2k) \rfloor$ for $j = 0, \ldots, k-1$ are distinct and lie in $[0, L)$, so spreading an ordered list gives an ordered array.

*Proof.* The values $(2j+1) L / (2k)$ grow by $L/k > 1$ from one $j$ to the next, and two reals that differ by more than 1 have different floors, so the floors are strictly increasing. The largest is $\lfloor (2k-1) L / (2k) \rfloor < L$. $\square$

**Lemma 2 (the search).** On an ordered array, line L9 ends with a slot $b$ such that every filled slot before $b$ holds a pair $\prec (x, p)$ and every filled slot from $b$ on holds a pair $\succ (x, p)$.

*Proof.* The pair $(x, p)$ is not yet in the array, so every placed pair is either $\prec$ or $\succ$ it. The search keeps $lo \le hi$ and the invariant: filled slots before $lo$ hold pairs $\prec (x, p)$, and filled slots from $hi$ on hold pairs $\succ (x, p)$. It holds for $lo = 0$, $hi = L$. Take $mid = \lfloor (lo + hi)/2 \rfloor$, so $lo \le mid < hi$, and let $j$ be the first filled slot in $[mid, hi)$. If there is none, the slots $[mid, hi)$ are empty, and $hi \leftarrow mid$ keeps the invariant. If $(x, p) \prec S[j]$, then the filled slots from $mid$ on are $S[j]$, which is $\succ (x,p)$, and slots after $j$; since the array is ordered, those are $\succ S[j]$ and so $\succ (x, p)$; $hi \leftarrow mid$ keeps the invariant. Otherwise $S[j] \prec (x, p)$, and so are all filled slots before $j$, so $lo \leftarrow j + 1$ keeps it. In the first two cases $hi$ drops, and in the third $lo$ rises past $mid \ge lo$, so $hi - lo$ falls each step and the loop ends with $lo = hi = b$. $\square$

**Lemma 3 (insertion).** If the array is ordered and has an empty slot, INSERT$(S, x, p)$ ends and leaves an ordered array whose pairs are the old ones plus $(x, p)$.

*Proof.* By Lemma 2 and line L10, $q$ and $r$ are consecutive filled slots with $S[q] \prec (x, p) \prec S[r]$, where $q = -1$ or $r = L$ stands for no slot. All slots strictly between $q$ and $r$ are empty.

If $r - q > 1$, line L11 writes into the empty slot $\lfloor (q + r)/2 \rfloor$, which lies strictly between them, and the array stays ordered.

Otherwise $r = q + 1$. In line L12, $e$ is the first empty slot after $r$, so $S[r \ldots e-1]$ are filled. Shifting them one slot right fills slot $e$ and empties slot $r$, keeping their order. Then $(x, p)$ goes into slot $r$, between $S[q]$ and the old $S[r]$, now in slot $r + 1$. In line L13 there is no empty slot after $r$ and none between $q$ and $r$, so the empty slot that exists is before $q$, and $e$ is the last one. The slots $e+1, \ldots, q$ are filled; shifting them one slot left empties slot $q$ and keeps their order, and $(x, p)$ goes into slot $q$, after the old $S[q]$, now in slot $q - 1$, and before $S[r]$. Each case writes $(x, p)$ once and loses no pair. The scans for $q$, $r$ and $e$ run over finite ranges, so INSERT ends. $\square$

**Theorem.** LIBRARY-SORT ends and leaves $A$ in stable sorted order.

*Proof.* We show by induction on the rounds that at line L3 the placed items are the pairs $(A[\pi(t)], \pi(t))$ for $t < k$, listed in $\prec$ order. This holds at line L2 with $k = 1$. In a round, $k < m$ and $L = \lfloor (1 + \varepsilon) m \rfloor + 1 > m > k$, so by Lemma 1 spreading gives an ordered array. Each insertion of the round starts with fewer than $m < L$ items, so an empty slot exists, and Lemma 3 applies. After the round the array is ordered and holds the pairs for $t < m$, and line L7 lists them in order. The rounds double $k$ until $k = n$, so there are $\lceil \lg n \rceil$ rounds and the loop ends. Then the placed items are all $n$ pairs in $\prec$ order, and line L8 writes their items to $A$ in stable sorted order. $\blacksquare$
