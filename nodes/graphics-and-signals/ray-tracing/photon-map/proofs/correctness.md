---
title: The photon map build gives a complete kd-tree, and the k-nearest query returns the k nearest photons
proves: [correctness]
status: full
---

Let $P$ be a list of $n \ge 1$ photons with positions in $\mathbb{R}^3$. Write $T(i)$ for the set of indices in the subtree of $i$ in the complete binary tree on $\{1, \ldots, n\}$, that is, the indices $j \le n$ of the form $2^d i + c$ with $0 \le c < 2^d$.

**Lemma 1 (subtree sizes).** For $N \ge 2$ nodes the left subtree of the root of a complete binary tree has LEFT-SIZE$(N)$ nodes, and the right subtree has $N - 1 - \text{LEFT-SIZE}(N)$ nodes. Each subtree of a complete tree is complete.

*Proof.* Let $2^h \le N < 2^{h+1}$. The levels $0, \ldots, h-1$ are full and hold $2^h - 1$ nodes. The last level holds $N - 2^h + 1$ nodes, filled from the left. The left subtree holds $2^{h-1} - 1$ nodes of the full levels below the root, and the first $2^{h-1}$ positions of the last level, so it gets $\min(N - 2^h + 1, 2^{h-1})$ nodes of that level. The sum is LEFT-SIZE$(N)$. The right subtree has the rest. A subtree of a complete tree has full levels and a last level filled from the left, so it is complete. $\square$

**Lemma 2 (selection).** After line L5 on a part $Q$ with $|Q| \ge 1$, the photon $q$ has exactly $m$ photons of $Q$ before it, each with coordinate at most $q[a]$, and $|Q| - 1 - m$ photons after it, each with coordinate at least $q[a]$.

*Proof.* This is the postcondition of quickselect with the Hoare partition. Each round partitions the active range into a left block of values at most the pivot, a middle block equal to it and a right block of values at least the pivot, and keeps the block that holds position $m$. The positions outside the active range never move again, and each is on the correct side of all positions of the active range. When the active range has one element, or position $m$ is in the middle block, the claim holds. The active range shrinks in each round, so the loop ends. $\square$

**Theorem 1 (build).** BUILD fills each index $1, \ldots, n$ with exactly one photon, and for each $i$ and each $j \in T(2i)$, $heap[j][a_i] \le heap[i][a_i]$, and for each $j \in T(2i+1)$, $heap[j][a_i] \ge heap[i][a_i]$, where $a_i = axis[i]$.

*Proof.* We show that each popped pair $(i, Q)$ has $|Q| = |T(i)|$, and that the photons of $Q$ are the photons that end in $T(i)$. At the start, $(1, P)$ has $|P| = n = |T(1)|$. When $(i, Q)$ is popped, line L6 puts $q$ at $i$, and line L7 pushes $(2i, Q_<)$ and $(2i+1, Q_>)$. By Lemma 1, applied to the complete subtree at $i$, and by Lemma 2, $|Q_<| = |T(2i)|$ and $|Q_>| = |T(2i+1)|$. An empty part is not pushed, and then the subtree is empty too. So by induction each index of $T(1) = \{1, \ldots, n\}$ is filled once, with a photon of the part pushed for it. The photons in $T(2i)$ are the photons of $Q_<$, and by Lemma 2 each has coordinate at most $q[a_i]$. The same holds for $T(2i+1)$ and $Q_>$. $\square$

For the query, write $R(i)$ for the set of points $y$ that satisfy, for each proper ancestor $u$ of $i$, $y[a_u] \le heap[u][a_u]$ if $i$ is in $T(2u)$, and $y[a_u] \ge heap[u][a_u]$ if $i$ is in $T(2u+1)$. By Theorem 1 every photon in $T(i)$ lies in $R(i)$.

**Lemma 3 (the bound).** Each pair $(j, b)$ pushed by the query has $b \le \|x - y\|^2$ for every $y \in R(j)$.

*Proof.* By induction on the pushes. The pair $(1, 0)$ is correct since distances are nonnegative. When $(i, b)$ is popped and $\delta = x[a_i] - heap[i][a_i]$, the near child gets the bound $b$, and $R(\text{near}) \subseteq R(i)$. The far child is on the other side of the plane $y[a_i] = heap[i][a_i]$ from $x$, or on it, so each of its points $y$ has $|x[a_i] - y[a_i]| \ge |\delta|$, so $\|x - y\|^2 \ge \delta^2$. Also $R(\text{far}) \subseteq R(i)$, so $\|x - y\|^2 \ge b$. So $\max(b, \delta^2)$ is a lower bound. $\square$

**Theorem 2 (k-nearest).** K-NEAREST$(x, k, r_{\max})$ returns $\min(k, m)$ photons, where $m$ is the number of photons with $\|x - x_p\| < r_{\max}$, and no photon left out is strictly nearer to $x$ than a photon returned.

*Proof.* Invariant: after each pop, $H$ holds the $\min(k, |V|)$ nearest photons of the set $V$ of visited photons with $d^2 < r_{\max}^2$, and $d2max$ is $r_{\max}^2$ if $|H| < k$ and the largest key of $H$ otherwise. Lines L13 and L14 keep this invariant, since they insert the new photon if it is nearer than $d2max$ and drop the largest when $H$ has $k + 1$ entries. Now let $p$ be a photon that is not visited. Then some ancestor-or-self $j$ of $p$ was popped with $b \ge d2max$ at that time. By Lemma 3, $\|x - x_p\|^2 \ge b \ge d2max$. Since $d2max$ never grows, at the end $\|x - x_p\|^2 \ge d2max$. If $|H| < k$ at the end, then $d2max = r_{\max}^2$, and $p$ is not within the radius, so $H$ holds all $m$ photons in the radius. If $|H| = k$, then $p$ is not strictly nearer than the largest element of $H$. A visited photon not in $H$ is also not strictly nearer, by the invariant. $\square$

**Corollary (in radius).** The same argument with a fixed $d2max = r^2$ shows that IN-RADIUS returns exactly the photons with $\|x - x_p\| < r$.
