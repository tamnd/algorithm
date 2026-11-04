---
title: The rectangle intersection sweep returns a pair if and only if two rectangles intersect
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The rectangles are $R_i = [a_i, b_i] \times [c_i, d_i]$ with $a_i \le b_i$ and $c_i \le d_i$, for $i = 1, \ldots, n$. We write $I_i = [c_i, d_i]$ for the $y$-interval of $R_i$. Two closed intervals $[u, v]$ and $[u', v']$ meet if and only if $u \le v'$ and $u' \le v$, so two rectangles intersect if and only if their $x$-intervals meet and their $y$-intervals meet.

After line L2, $E$ is the sorted list of the $2n$ events. Event $(a_i, 0, i)$ is the *insert* of $i$, and event $(b_i, 1, i)$ is the *delete* of $i$. Since $a_i \le b_i$ and $0 < 1$, the insert of $i$ comes before the delete of $i$ in $E$. A rectangle is *active* at an event $e$ if its insert comes before $e$ in $E$ and its delete does not. By lines L6 and L10, just before the loop processes $e$, the set $S$ holds exactly the rectangles that are active at $e$.

**Termination.** The loop of line L4 runs at most once for each of the $2n$ events, and each iteration does a constant number of operations on $S$. So the algorithm stops.

**Lemma 1 (activity).** Let $j \ne i$. Then $j$ is active at the insert of $i$ if and only if the insert of $j$ comes before the insert of $i$ and $b_j \ge a_i$. In particular, if $j$ is in $S$ when $i$ is inserted, then the $x$-intervals $[a_j, b_j]$ and $[a_i, b_i]$ meet.

*Proof.* The delete of $j$ is $(b_j, 1, j)$ and the insert of $i$ is $(a_i, 0, i)$. In lexicographic order, the delete of $j$ comes after the insert of $i$ if and only if $b_j > a_i$, or $b_j = a_i$ (then $1 > 0$ decides). So it comes after if and only if $b_j \ge a_i$. This proves the equivalence. If $j$ is active at the insert of $i$, then $a_j \le a_i$ (the insert of $j$ comes first) and $b_j \ge a_i$. So $a_j \le a_i \le b_i$ and $a_i \le b_j$, and the $x$-intervals meet. $\square$

**Lemma 2 (soundness).** If the algorithm returns a pair, the two rectangles intersect.

*Proof.* A pair is returned only in line L8 or line L9, during the insert of some $i$. The other member, $p$ or $s$, is in $S$ and is not $i$, so by Lemma 1 its $x$-interval meets that of $R_i$. In line L8, $p$ precedes $i$ in the key order, so $c_p \le c_i$, and the test gives $d_p \ge c_i$. Together with $c_i \le d_i$, this gives $c_p \le d_i$ and $c_i \le d_p$, so $I_p$ and $I_i$ meet. In line L9, $s$ follows $i$, so $c_i \le c_s$, and the test gives $c_s \le d_i$; with $c_s \le d_s$ this gives $c_i \le d_s$, so $I_i$ and $I_s$ meet. In both cases both intervals meet, and the rectangles intersect. $\square$

**Lemma 3 (neighbors).** Let $T$ be a finite set of closed intervals that are pairwise disjoint, ordered by the key $(c, \text{index})$. Let $J = [c, d]$ be a new interval with a key not in $T$, and let $p$ and $s$ be the predecessor and the successor of $J$ in $T \cup \{J\}$. If $J$ meets some interval of $T$, then $J$ meets $p$ or $J$ meets $s$.

*Proof.* Since the intervals of $T$ are pairwise disjoint and closed, for two of them $[c', d']$ before $[c'', d'']$ in key order we have $c' \le c''$, and they do not meet, so $d' < c''$. Let $A = [c_A, d_A] \in T$ meet $J$.

*Case 1: $A$ precedes $J$.* Then $p$ exists. If $p = A$, we are done. Otherwise $A$ precedes $p$, and $p$ precedes $J$. By the remark above, $c_p > d_A$. Since $A$ meets $J$, $d_A \ge c$. So $c_p > c$. But $p$ precedes $J$, so $c_p \le c$. This is a contradiction, so $p = A$.

*Case 2: $A$ follows $J$.* Then $s$ exists, and $s = A$ or $s$ precedes $A$. In both cases $c_s \le c_A$. Since $A$ meets $J$, $c_A \le d$. So $c_s \le d$. Since $s$ follows $J$, $c \le c_s \le d_s$. So $J$ and $s$ meet. $\square$

**Lemma 4 (completeness).** If two rectangles intersect, the algorithm returns a pair.

*Proof.* For an intersecting pair $\{j, i\}$, call the one whose insert comes later in $E$ its *late* member, and call the insert of the late member the *time* of the pair. Assume that intersecting pairs exist, and let $e^\ast$, the insert of $i^\ast$, be the earliest time over all intersecting pairs. If the algorithm returns at an event before $e^\ast$, it returns a pair and we are done. So assume that it reaches $e^\ast$.

*The active intervals are disjoint at $e^\ast$.* Let $j$ and $k$ be two rectangles in $S$ just before $e^\ast$, with the insert of $k$ after the insert of $j$. Both are active at $e^\ast$, so $j$ is active at the insert of $k$ (its delete comes after $e^\ast$, which is after the insert of $k$). By Lemma 1 their $x$-intervals meet. If $I_j$ and $I_k$ met, $\{j, k\}$ would be an intersecting pair of time before $e^\ast$, against the choice of $e^\ast$. So the intervals of the active rectangles are pairwise disjoint.

*Some active interval meets $I_{i^\ast}$.* Let $\{j, i^\ast\}$ be an intersecting pair with time $e^\ast$, so the insert of $j$ comes before $e^\ast$. The $x$-intervals meet, so $b_j \ge a_{i^\ast}$. By Lemma 1, $j$ is active at $e^\ast$, so $j \in S$. And $I_j$ meets $I_{i^\ast}$.

Now line L6 inserts $i^\ast$ with key $(c_{i^\ast}, i^\ast)$, which differs from each key in $S$ by its index. By Lemma 3, $I_{i^\ast}$ meets $I_p$ or $I_s$. If it meets $I_p$, then $c_p \le c_{i^\ast}$ and $c_{i^\ast} \le d_p$, so the test of line L8 is true. If it does not meet $I_p$ but meets $I_s$, then line L8 is false or $p$ does not exist, and $c_s \le d_{i^\ast}$, so the test of line L9 is true. In both cases the algorithm returns a pair at $e^\ast$. $\square$

**Theorem.** RECT-INTERSECT stops. It returns a pair $(i, j)$ with $i \ne j$ and $R_i \cap R_j \ne \emptyset$ if such a pair exists, and it returns NONE otherwise.

*Proof.* Termination was shown above. If an intersecting pair exists, Lemma 4 shows that the algorithm returns a pair, and Lemma 2 shows that the pair intersects. If no intersecting pair exists, Lemma 2 shows that no pair can be returned, so the loop ends and line L11 returns NONE. $\blacksquare$
