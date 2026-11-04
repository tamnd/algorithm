---
title: The gap buffer operations keep the sequence and move the cursor correctly
proves: [correctness]
status: full
---

**Invariant (I).** $cap \ge 1$, $0 \le g \le e \le cap$, and the sequence held is $S = \langle A[0], \ldots, A[g-1], A[e], \ldots, A[cap-1] \rangle$, with the cursor at position $g$. Write $n = cap - (e - g)$ for its length, and $w = e - g$ for the width of the gap.

**Reading by position.** Under (I), the first $g$ items of $S$ are $A[0..g-1]$, and item $i \ge g$ is $A[e + (i - g)] = A[i + w]$. So line L7 returns item $i$ of $S$ for each $0 \le i < n$.

**MOVE-TO$(B, p)$, $0 \le p \le n$.** We show that each pass of either loop keeps (I), keeps $S$ and $w$, and changes $g$ by one toward $p$.

*A pass of line L1*, with $g > p \ge 0$. Before it, $S = \langle A[0], \ldots, A[g-1], A[e], \ldots \rangle$. The pass sets $e' = e - 1$, $g' = g - 1$, then writes $A[e'] \leftarrow A[g']$, the old $A[g-1]$. Since $g \le e$, we have $g' \le e'$ and $0 \le g'$. Cell $e'$ was a gap cell if $w \ge 1$, and is cell $g'$ itself if $w = 0$; in both cases no item other than $A[g-1]$ is overwritten. The new sequence is $\langle A[0], \ldots, A[g'-1], A[e'], A[e], \ldots \rangle$ with $A[e'] = $ the old $A[g-1]$, which is the old $S$. The width is $e' - g' = w$.

*A pass of line L2*, with $g < p \le n$. Then $g < n$, so $e < cap$ and $A[e]$ is the first item after the gap. The pass writes $A[g] \leftarrow A[e]$ and sets $g' = g + 1$, $e' = e + 1 \le cap$. Cell $g$ was a gap cell, or is cell $e$ itself if $w = 0$. The new sequence is $\langle A[0], \ldots, A[g-1], A[g], A[e'], \ldots \rangle$ with $A[g]$ the old $A[e]$, which is the old $S$. The width is unchanged.

Line L1 runs exactly $g - p$ passes when $g > p$, and then line L2 runs none; line L2 runs exactly $p - g$ passes when $g < p$. Afterwards $g = p$. So MOVE-TO keeps $S$, puts the cursor at $p$, and moves $\lvert p - g \rvert$ items.

**GROW$(B)$**, called with $g = e$. Line L8 makes $C$ of size $2 \cdot cap$, copies $A[0..g-1]$ to $C[0..g-1]$, and copies $A[e..cap-1]$, which has $cap - e$ items, to $C[2cap - (cap - e) .. 2cap - 1] = C[e + cap .. 2cap - 1]$. It sets $e' = e + cap$ and $cap' = 2cap$. Then $g \le e'$, $e' \le cap'$, and the sequence $\langle C[0], \ldots, C[g-1], C[e'], \ldots, C[cap'-1] \rangle$ is the old $S$. The new width is $cap \ge 1$.

**INSERT$(B, x)$.** After line L3, (I) holds with the same $S$ and $g < e$: either $g < e$ already, or GROW made the width $cap \ge 1$. Line L4 writes $x$ into $A[g]$, a gap cell, and sets $g' = g + 1 \le e$. The new sequence is $\langle A[0], \ldots, A[g-1], x, A[e], \ldots \rangle$: $x$ is inserted at the old cursor position, and the cursor is just after it.

**DELETE-BEFORE$(B)$, $g > 0$.** Line L5 sets $g' = g - 1$ and returns $A[g']$, the item just before the cursor. Now $0 \le g' < e$, and the sequence is $S$ without that item. No cell is written.

**DELETE-AFTER$(B)$, $e < cap$.** Line L6 sets $e' = e + 1 \le cap$ and returns $A[e]$, the item just after the cursor. The sequence is $S$ without that item, and the cursor stays at $g$.

**Amortized cost of INSERT.** Let $\Phi = 2n - cap$ when it is positive, and 0 otherwise. An insert without a grow costs 1 and raises $\Phi$ by at most 2. A grow happens when $n = cap$, so $\Phi = cap$ before it; it copies $cap$ items, and afterwards $\Phi = 2cap - 2cap = 0$, so the copies are paid by the drop in $\Phi$. Deletes and moves do not raise $\Phi$. So each insert costs at most 3 amortized, and $m$ operations with a total cursor distance $D$ cost $O(m + D)$, from an initial state with $\Phi = 0$. $\blacksquare$
