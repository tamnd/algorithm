---
title: Incremental sweep and prune reports exactly the overlapping pairs, and one update makes r swaps
proves: [correctness, termination]
status: full
---

Let the boxes be $B_i = [x^{lo}_i, x^{hi}_i] \times [y^{lo}_i, y^{hi}_i]$ for $i = 0, \ldots, n - 1$, closed, with $x^{lo}_i \le x^{hi}_i$ and $y^{lo}_i \le y^{hi}_i$. On axis $a$, box $i$ has two endpoints, $\ell^a_i = (lo^a_i, 0, i)$ and $h^a_i = (hi^a_i, 1, i)$. Endpoints are compared as triples in lexicographic order, so at equal values a lower endpoint comes before an upper endpoint. This is the key of line L6. Write $u \prec v$ for this order. It is a strict total order on the $2n$ endpoints of one axis, because the triples are distinct.

The state holds, for each axis $a$, a list $E[a]$ of the endpoints of the axis, a counter $c(i, j)$ for each pair $i < j$, and a set $P$ of pairs. The invariant is:

- **(S)** each list $E[a]$ is sorted by $\prec$;
- **(C)** $c(i, j)$ is the number of axes $a$ with $\ell^a_i \prec h^a_j$ and $\ell^a_j \prec h^a_i$;
- **(P)** $P = \{(i, j) : c(i, j) = 2\}$.

**Lemma 1 (order and overlap).** On axis $a$, the intervals of boxes $i \ne j$ intersect if and only if $\ell^a_i \prec h^a_j$ and $\ell^a_j \prec h^a_i$.

*Proof.* $\ell^a_i \prec h^a_j$ holds if $lo^a_i < hi^a_j$, or if the values are equal and the second fields compare $0 < 1$. So it holds exactly when $lo^a_i \le hi^a_j$. In the same way $\ell^a_j \prec h^a_i$ holds exactly when $lo^a_j \le hi^a_i$. Two closed intervals intersect exactly when both inequalities hold. $\square$

So under (C) and (P), the set $P$ is the set of pairs of boxes that intersect on both axes, which is the set of pairs of intersecting boxes.

**Lemma 2 (one swap).** Let $y, x$ be adjacent in $E[a]$ with $y$ before $x$ and $x \prec y$, and let $E'$ be $E[a]$ after the swap of line L10. Let $p$ be the pair of the owners of $x$ and $y$. Then the relation of Lemma 1 on axis $a$ changes only for $p$. It changes from false to true if $x$ is a lower endpoint and $y$ is an upper endpoint, from true to false if $x$ is an upper endpoint and $y$ is a lower endpoint, and it does not change otherwise.

*Proof.* The relation of Lemma 1 for a pair $(i, j)$ depends only on the relative positions of the four endpoints of $i$ and $j$ in the list. Here the "position" order of the list and the key order $\prec$ are different things while the list is not sorted, so we define the relation by list positions: $R_a(i, j)$ holds if $\ell^a_i$ is before $h^a_j$ and $\ell^a_j$ is before $h^a_i$ in the list. A swap of two adjacent elements changes the relative position of these two elements only. So $R_a$ can change only for the pair $p$ of the owners of $x$ and $y$.

The two endpoints of one box are never swapped. Line L3 sets the values from boxes with $lo \le hi$, so $\ell^a_i \prec h^a_i$, and line L6 swaps only a pair that is out of order.

Now let $x$ belong to box $i$ and $y$ to box $j \ne i$. Suppose $x = \ell^a_i$ and $y = h^a_j$. Before the swap, $h^a_j$ is before $\ell^a_i$, so $R_a(i, j)$ is false. After the swap, $\ell^a_i$ is before $h^a_j$. Also $\ell^a_j$ is before $h^a_j$, which is now directly after $\ell^a_i$, so $\ell^a_j$ is before $\ell^a_i$, which is before $h^a_i$. So $R_a(i, j)$ is true. Suppose $x = h^a_i$ and $y = \ell^a_j$. After the swap, $h^a_i$ is before $\ell^a_j$, so $R_a(i, j)$ is false. Before the swap, $\ell^a_j$ was directly before $h^a_i$, and $\ell^a_i$ is before $h^a_i$, so $\ell^a_i$ was before $\ell^a_j$ and thus before $h^a_j$, and $R_a(i, j)$ was true. If $x$ and $y$ are both lower endpoints or both upper endpoints, the two conditions of $R_a(i, j)$ compare a lower endpoint with an upper endpoint, and neither of them compares $x$ with $y$, so neither changes. $\square$

We now use the invariant with $R_a$ in place of the relation of Lemma 1 in (C): $c(i, j)$ is the number of axes with $R_a(i, j)$. When a list is sorted, $R_a$ and the relation of Lemma 1 agree, so after each completed update this is the same as (C).

**Theorem.** If the invariant holds before UPDATE, then UPDATE terminates, the invariant holds after it for the new boxes, and the returned number $r$ is the total number of inversions of the lists after line L3, that is, the number of pairs of endpoints that are in the wrong order.

*Proof.* Line L3 changes the values of the endpoints but not the list positions, so (C) and (P) hold for $R_a$ after line L3. (S) may fail.

Lines L4 to L10 are insertion sort on $E[a]$ with the order $\prec$. Each swap of line L10 exchanges an adjacent pair that is out of order, so it removes exactly one inversion and creates none. The number of inversions is finite and is at least 0, so the loop terminates, and the number of swaps is the number of inversions after line L3. When the loop of line L4 ends, the list is sorted, which is the standard invariant of insertion sort: before step $i$ the prefix $E[0..i-1]$ is sorted, and the inner loop moves $E[i]$ left until its left neighbor is smaller.

At each swap, Lemma 2 says how $R_a$ changes. Line L8 adds 1 to $c(p)$ when $R_a(p)$ changes from false to true, and line L9 subtracts 1 when it changes from true to false. No other counter changes, and by Lemma 2 no other $R_a$ changes. So (C) for $R_a$ holds after each swap. Line L8 adds $p$ to $P$ when the new counter is 2, and line L9 removes $p$ when the old counter is 2. Since a counter changes by one at a time, this keeps (P). After both axes are sorted, (S) holds, and $R_a$ equals the relation of Lemma 1, so (C) holds as stated. $\blacksquare$

**Initialization.** The constructor sorts each list, so (S) holds, and then sweeps each sorted list: at each lower endpoint of box $i$ it adds 1 to $c(i, j)$ for each box $j$ whose interval is open at that moment, that is, whose lower endpoint was passed and whose upper endpoint was not. For a pair $i, j$ with $\ell^a_j \prec \ell^a_i$, box $j$ is open at $\ell^a_i$ exactly when $\ell^a_i \prec h^a_j$, and $\ell^a_j \prec h^a_i$ holds already because $\ell^a_j \prec \ell^a_i \prec h^a_i$. So the counter gets 1 on axis $a$ exactly when the relation of Lemma 1 holds, and it is counted once, at the later of the two lower endpoints. So (C) and (P) hold.

**The one-shot sweep.** SORT-AND-SWEEP sorts the boxes by $lo$ on the sweep axis and keeps the boxes whose interval contains the current $lo$. For $i$ processed after $j$, the interval of $j$ is kept exactly when $hi_j \ge lo_i$, and $lo_j \le lo_i \le hi_i$ holds by the order, so $j$ is tested against $i$ exactly when the intervals on the sweep axis intersect. Each such pair is then tested on the other axis. Each pair is considered once, when the later box is processed. So the output is the set of intersecting pairs. $\blacksquare$
