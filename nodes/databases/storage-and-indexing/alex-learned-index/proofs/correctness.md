---
title: Routing by monotone models and gapped arrays with gap values keep ALEX exact
proves: [correctness]
status: full
---

We use the notation of the page and of the code. An inner node $v$ with $F$ slots routes a key $k$ to the slot $slot_v(k) = \min(\max(\lfloor a_v k + b_v \rfloor, 0), F - 1)$. The *route* of $k$ is the path from the root that follows these slots, and $leaf(k)$ is the data node at its end. A data node has $C$ slots with values $vals[0..C-1]$ and bits $occ[0..C-1]$. Its keys are the values of the occupied slots.

**Invariant.**

- (R1) Every key of the index is stored in $leaf(k)$, exactly once.
- (R2) Every model of an inner node has a slope $a_v \ge 0$, and each child of $v$ fills one run of consecutive slots.
- (G1) In each data node, the values of the occupied slots are strictly increasing from left to right.
- (G2) Each gap holds the value of the next occupied slot to its right, or $\infty$ if there is none. With (G1), the whole array $vals$ is nondecreasing.
- (D) The number of keys of a data node is at most $C$, and after an insert at most $d_u C$.
- (L) The data nodes, read along the `next` links, are in the order of the leaves of the tree from left to right.

**Lemma 1 (slopes).** `fit_linear` on sorted keys returns a slope of at least 0.

*Proof.* The slope is $\sum (k_i - \bar k)(i - \bar\imath) / \sum (k_i - \bar k)^2$, times a positive scale. The keys and the ranks are both sorted in the same order, so by Chebyshev's sum inequality $\sum (k_i - \bar k)(i - \bar\imath) \ge 0$. $\square$

The model of a node made by a down split has the slope $2/(hi - lo + 1) > 0$, and doubling a node multiplies its slope by 2. So (R2) holds for slopes. The run property holds at the bulk load (one child per slot), is kept by doubling (slot $j$ becomes $2j$ and $2j + 1$), and by a sideways split, which cuts a run into two runs.

**Lemma 2 (monotone routing).** If $k < k'$, then $leaf(k)$ is equal to $leaf(k')$ or comes before it in the left-to-right order of the leaves.

*Proof.* With $a_v \ge 0$, the floor and the clamp are nondecreasing, so $slot_v(k) \le slot_v(k')$ at every inner node on the common part of the two routes. At the first node where the routes differ, $k$ takes a smaller slot, and by the run property a different child to the left. $\square$

**Lemma 3 (exponential search).** If (G1) and (G2) hold, `lower_bound(k, p)` returns the first index $i$ with $vals[i] \ge k$, or $C$ if there is none.

*Proof.* If $vals[p] \ge k$, the loop keeps $vals[hi] \ge k$ and moves $hi$ left by doubling steps. It stops with $lo = 0$, or with $vals[lo] < k$ for $lo = hi - step$. If $vals[p] < k$, the loop keeps $vals[lo] < k$ and stops with $hi = C$, or with $vals[hi] \ge k$. In both cases every index below $lo$ has a value $< k$ (the array is nondecreasing), the first index with a value $\ge k$ lies in $[lo, hi]$, and `bisect_left` on $[lo, hi)$ returns it, or $hi$. $\square$

**Lemma 4 (find).** In a data node, $k$ is a key if and only if the first occupied slot $j \ge i$ exists and $vals[j] = k$, where $i$ is the result of Lemma 3.

*Proof.* If $vals[j] = k$ with $occ[j]$, then $k$ is a key. Conversely, let $k$ be in the occupied slot $t$. Then $vals[t] = k$, so $i \le t$. Every slot in $[i, t)$ has a value $\ge k$; an occupied one would have a value $< k$ by (G1), since it is left of $t$; so these slots are all gaps, and $j = t$. $\square$

**Lemma 5 (data node insert).** If the node has a free slot and $k$ is not a key, `DataNode.insert` adds $k$ and keeps (G1) and (G2).

*Proof.* Let $i$ be from Lemma 3 and $q$ the first occupied slot $\ge i$. Slot $i - 1$ is occupied (or $i = 0$): a gap at $i - 1$ would hold the value of the next occupied slot, which is $q$, so its value would be $\ge k$, against the choice of $i$. So the occupied slots left of $i$ hold the keys $< k$, the slots $[i, q)$ are gaps, and the occupied slots from $q$ on hold the keys $> k$.

If $i < q$, the code puts $k$ in a slot of $[i, q)$, which keeps (G1). If $i = q$, there is no gap between the last key $< k$ and the first key $> k$. The code finds the nearest gap $g$ on the right of $q$ or on the left of $i$, which exists because a slot is free. On the right it moves the slots $q..g-1$ one place right and puts $k$ in $q$; on the left it moves the slots $g+1..i-1$ one place left and puts $k$ in $i - 1$. In both cases the order of the old keys does not change and $k$ is between the keys $< k$ and the keys $> k$, so (G1) holds.

For (G2): a gap value depends only on the next occupied slot to its right. On the right shift, the run of gaps just before $q$ now has $k$ as its next key, and `_refill_before` sets it. The gaps after $g$ do not change their next key. On the left shift, the run of gaps just before $g$ had the next key $vals[g + 1]$, which is now in slot $g$, so its value is still right; the slot $k$ goes to has no gap before it up to $g$. If no shift is needed, the gaps between $i$ and the new slot get the value $k$ from `_refill_before`, and the gaps after it keep the next key $vals[q]$. $\square$

Delete frees slot $j$, gives it the value of slot $j + 1$ (which is the next key by (G2)), and sets the run of gaps before it to the same value, which keeps (G1) and (G2).

**Lemma 6 (rebuild).** `DataNode._build` on $n$ sorted keys and $C \ge n$ slots puts the keys in strictly increasing slots and sets (G2).

*Proof.* The slot of the key with index $idx$ is at least one more than the slot of the key before, and at most $C - (n - idx)$, which leaves a slot for each later key. The previous slot is at most $C - (n - idx + 1)$, so the range is not empty. `_refill_all` then sets each gap to the next key from the right. $\square$

**Theorem 1.** After any sequence of bulk load, inserts and deletes, `contains(k)` is true exactly for the keys of the index, `keys()` lists them in increasing order, and `range(lo, hi)` returns the keys in $[lo, hi]$ in order.

*Proof.* We show that every operation keeps the invariant. The bulk load puts each key in the data node of its root slot, which is $leaf(k)$, and the rebuild of Lemma 6 gives (G1) and (G2). An insert goes to $leaf(k)$ (L6). If the node is too dense (L7), an expansion (L8) rebuilds the same node with more slots, which keeps (R1) and, by Lemma 6, (G1) and (G2). The new capacity is $\lceil (n + 1)/d_l \rceil$, so after the insert the density is at most $d_l < d_u$, and (D) holds. A split (L9) partitions the keys of the node with the routing function of the node that will route them: in a sideways split by the parent's slot, after the parent doubled if needed, and in a down split by the slot of the new inner node. So every key is again in its $leaf(k)$, (R1) holds, and the new nodes are built by Lemma 6. The loop then routes $k$ again. Each split either halves the run of slots of a node or makes a down split into two nonempty nodes, so the loop ends. When the node has room, Lemma 5 adds the key. The links of the new nodes replace the old node in the list, in slot order, which keeps (L).

By (R1), `contains(k)` checks the one node where $k$ can be, and by Lemmas 3 and 4 it answers correctly. By Lemma 2, all keys of an earlier leaf are smaller than all keys of a later leaf, so by (L) and (G1), `keys()` is sorted. `range` starts at $leaf(lo)$; by Lemma 2 every key $\ge lo$ is in that leaf or a later one, so the scan along the links, which stops at the first key $> hi$, returns exactly the keys in $[lo, hi]$. $\square$

The tests compare the gapped array and the whole index with a sorted Python list under random inserts, deletes, lookups and range queries, on uniform, narrow and sequential keys, and run `check`, which tests (R1), (G1), (G2), the runs of slots and the order of the links.
