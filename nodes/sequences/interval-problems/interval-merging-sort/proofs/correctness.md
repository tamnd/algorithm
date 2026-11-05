---
title: Interval merging by sorting returns the components of the union
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Let $I_1 = [l_1, r_1], \ldots, I_n = [l_n, r_n]$ be the intervals in the order that line L1 makes, so $l_1 \le l_2 \le \cdots \le l_n$. Let $U_i = I_1 \cup \cdots \cup I_i$, with $U_0 = \emptyset$, and let $R_i = \max(r_1, \ldots, r_i)$.

**Claim.** For closed intervals, MERGE-INTERVALS returns the list of the connected components of $U_n$, sorted from left to right. With the test $l \ge out.last.r$ in line L4, it does the same for open intervals $(l_j, r_j)$ with $l_j < r_j$; with the test of the page, it does the same for half-open intervals $[l_j, r_j)$ with $l_j < r_j$.

*Proof for closed intervals.* We prove this invariant of the loop of line L3.

> **(I)** After $i$ steps, with $0 \le i \le n$: $out = (C_1, \ldots, C_k)$ is the list of the components of $U_i$, sorted, and if $i \ge 1$ then the last component is $C_k = [a_k, R_i]$ with $a_k \le l_i$.

Each component of a finite union of closed intervals is a closed interval, because it is the union of the finitely many input intervals that lie in it, and a finite union of closed intervals that is connected is a closed interval.

*Initialization.* With $i = 0$, line L2 makes $out$ empty, and $U_0$ has no components.

*Maintenance.* Assume (I) after $i$ steps, $i < n$, and let $[l, r] = I_{i+1}$.

1. If $out$ is empty, then $i = 0$, line L5 makes $out = ([l, r])$, and $[l, r]$ is the only component of $U_1$. Also $R_1 = r$ and $a_1 = l = l_1$.
2. If $l > R_i$, line L5 appends $[l, r]$. Each point of $U_i$ is at most $R_i < l$, so the open gap $(R_i, l)$ is not in $U_{i+1}$, and $U_{i+1}$ is the disjoint union of $U_i$ and $[l, r]$ with this gap between them. So the components of $U_{i+1}$ are $C_1, \ldots, C_k$ and $[l, r]$, in this order. Also $R_{i+1} = \max(R_i, r) = r$, since $r \ge l > R_i$, and the new last component starts at $l = l_{i+1}$.
3. If $l \le R_i$, line L6 sets the right end of $C_k$ to $\max(R_i, r) = R_{i+1}$. By (I) and the sort, $a_k \le l_i \le l \le R_i$, so $l \in C_k$ and $[l, r]$ meets $C_k$. Hence $C_k \cup [l, r] = [a_k, \max(R_i, r)]$ is an interval. For $j < k$, the component $C_j$ ends before $a_k$ with a gap, because $C_j$ and $C_k$ are different components of $U_i$ and $C_j$ is to the left. Since $[l, r]$ starts at $l \ge a_k$, it does not reach $C_j$ or the gap after it. So the components of $U_{i+1}$ are $C_1, \ldots, C_{k-1}$ and $[a_k, R_{i+1}]$, and $a_k \le l = l_{i+1}$.

In each case (I) holds after $i + 1$ steps.

*Termination.* The loop of line L3 runs exactly $n$ times, once for each interval, because each step consumes one element of the finite sorted list. After the last step, (I) with $i = n$ says that $out$ is the sorted list of the components of $U_n$, and line L7 returns it. $\square$

*Half-open intervals.* For $[l_j, r_j)$ with $l_j < r_j$, replace closed by half-open in (I) and let $C_k = [a_k, R_i)$. In case 2, $l > R_i$ leaves the nonempty gap $[R_i, l)$ uncovered. In case 3, $l \le R_i$ gives $[a_k, R_i) \cup [l, r) = [a_k, \max(R_i, r))$, an interval, also when $l = R_i$: the point $R_i$ is in $[l, r)$ because $l = R_i < r$. The rest of the proof is the same.

*Open intervals.* For $(l_j, r_j)$ with $l_j < r_j$ and line L4 changed to $l \ge out.last.r$, let $C_k = (a_k, R_i)$. In case 2, now $l \ge R_i$, and the point $R_i$ is in no interval $I_1, \ldots, I_i$ (each ends at most at $R_i$ and excludes its end) and not in $(l, r)$, since $l \ge R_i$. So the components are separated, and the new one is $(l, r)$. In case 3, now $l < R_i$, and $(a_k, R_i) \cup (l, r) = (a_k, \max(R_i, r))$ is an interval because $a_k \le l < R_i$ and the two open intervals share the points just above $l$. The rest is the same. $\blacksquare$

**Cost.** Line L1 sorts $n$ items. Each of the $n$ steps of the loop does one comparison in line L4, at most one maximum in line L6, and $O(1)$ other work, so the scan costs $\Theta(n)$ time.
