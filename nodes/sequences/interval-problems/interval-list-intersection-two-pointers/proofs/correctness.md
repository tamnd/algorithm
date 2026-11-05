---
title: The two-pointer scan returns every nonempty intersection in order
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The lists are $A[1 \ldots m]$ and $B[1 \ldots n]$. Write $A[p] = \langle a_p, a'_p \rangle$ and $B[q] = \langle b_q, b'_q \rangle$. For closed intervals the lists are sorted and disjoint when $a'_p < a_{p+1}$ and $b'_q < b_{q+1}$ for all $p$ and $q$. For half-open intervals $[a_p, a'_p)$ the condition is $a'_p \le a_{p+1}$ and $b'_q \le b_{q+1}$. Line L5 tests $lo \le hi$ for closed intervals and $lo < hi$ for half-open ones.

**Claim.** INTERSECT-LISTS stops, and it returns the list of all nonempty sets $A[p] \cap B[q]$, each once, sorted from left to right.

**Lemma 1 (line L5).** In the step for the pair $(i, j)$, line L5 appends a piece if and only if $A[i] \cap B[j] \ne \emptyset$, and the piece it appends is $A[i] \cap B[j]$.

*Proof.* For closed intervals, $x \in [a_i, a'_i] \cap [b_j, b'_j]$ if and only if $\max(a_i, b_j) \le x \le \min(a'_i, b'_j)$, that is $lo \le x \le hi$. So the intersection is $[lo, hi]$, and it is nonempty if and only if $lo \le hi$. For half-open intervals the same argument gives $[lo, hi)$, which is nonempty if and only if $lo < hi$. $\square$

**Lemma 2 (the discard).** If $a'_i \le b'_j$, then $A[i] \cap B[q] = \emptyset$ for every $q > j$. If $b'_j \le a'_i$, then $A[p] \cap B[j] = \emptyset$ for every $p > i$.

*Proof.* Take $q > j$. Since $B$ is sorted and disjoint, $b_q \ge b_{j+1}$. For closed intervals $b_{j+1} > b'_j \ge a'_i$, so every point of $B[q]$ is greater than $a'_i$, and every point of $A[i]$ is at most $a'_i$. For half-open intervals $b_{j+1} \ge b'_j \ge a'_i$, so every point of $B[q]$ is at least $a'_i$, and every point of $A[i]$ is less than $a'_i$. In both cases the two sets are disjoint. The second statement is the same with the roles of $A$ and $B$ exchanged. $\square$

**Lemma 3 (order).** If $p < p'$, then every point of $A[p]$ is less than every point of $A[p']$, and the same holds for $B$.

*Proof.* By the sorted and disjoint condition, $a'_p$ is at most $a_{p+1} \le a_{p'}$, and for closed intervals $a'_p < a_{p+1}$. A point of $A[p]$ is at most $a'_p$ (less than $a'_p$ for half-open intervals), and a point of $A[p']$ is at least $a_{p'}$. In each case the first is less than the second. $\square$

**Invariant.** Let $D(i, j)$ be the set of pairs $(p, q)$ with $1 \le p \le m$, $1 \le q \le n$, and $p < i$ or $q < j$. Before each test of line L2:

> **(I)** $out$ is the list of the nonempty sets $A[p] \cap B[q]$ with $(p, q) \in D(i, j)$, each once, sorted from left to right.

*Initialization.* Line L1 sets $i = j = 1$, so $D(1, 1)$ is empty, and $out$ is empty.

*Maintenance.* Assume (I), with $i \le m$ and $j \le n$, so the loop body runs. By Lemma 1, line L5 appends $P = A[i] \cap B[j]$ if it is nonempty, and nothing else. The pair $(i, j)$ is not in $D(i, j)$, so $P$ is not already in $out$.

First, $P$ comes after every piece already in $out$. Take a piece $A[p] \cap B[q]$ in $out$. If $p < i$, the piece lies in $A[p]$ and $P$ lies in $A[i]$, so every point of the piece is less than every point of $P$ by Lemma 3. If $q < j$, the same holds with $B$. So $out$ stays sorted.

Next, consider line L6. If $a'_i < b'_j$, it sets $i \leftarrow i + 1$. Then $D(i + 1, j) = D(i, j) \cup \{(i, q) : q \ge j\}$. The pair $(i, j)$ is handled by line L5, and for $q > j$ the set $A[i] \cap B[q]$ is empty by Lemma 2, since $a'_i \le b'_j$. So $out$ is the list for $D(i + 1, j)$, and (I) holds.

Otherwise $a'_i \ge b'_j$, and line L7 sets $j \leftarrow j + 1$. Then $D(i, j + 1) = D(i, j) \cup \{(p, j) : p \ge i\}$. The pair $(i, j)$ is handled by line L5, and for $p > i$ the set $A[p] \cap B[j]$ is empty by the second part of Lemma 2, since $b'_j \le a'_i$. This case includes the tie $a'_i = b'_j$. So (I) holds.

*Termination.* Each step increases $i + j$ by exactly 1, and the loop runs only while $i + j \le m + n$. So it stops after at most $m + n - 1$ steps when $m, n \ge 1$, and at once when $m = 0$ or $n = 0$.

*Conclusion.* When the loop stops, $i = m + 1$ or $j = n + 1$. In the first case every $p \le m$ satisfies $p < i$; in the second every $q \le n$ satisfies $q < j$. Either way $D(i, j)$ contains all $mn$ pairs, and by (I) line L8 returns all nonempty sets $A[p] \cap B[q]$, each once, sorted from left to right. These pieces are pairwise disjoint, because two different pairs differ in $p$ or in $q$, and the intervals of each list are disjoint. $\blacksquare$
