---
title: Timsort sorts the array stably
proves: [correctness]
status: full
---

We say that a segment $A[p \ldots q-1]$ is *sorted stably* when it is sorted by key and items with equal keys are in their input order. We use the four helper procedures of the implementation, and prove each one first. Every comparison is $x < y$, and "$x \le y$" means "not $y < x$".

**Lemma 1 (runs).** COUNT-RUN at $lo$ returns $\ell \ge 1$, and after it $A[lo \ldots lo + \ell - 1]$ is sorted stably.

*Proof.* If $\ell = 1$ or the run is non-decreasing, the segment is sorted, and its items are in input order. If the run is strictly decreasing, its items are pairwise different in key, so after the reversal the segment is sorted and has no two equal items, and stability holds trivially. $\square$

**Lemma 2 (binary insertion sort).** If $A[lo \ldots s-1]$ is sorted stably and the items of $A[s \ldots h-1]$ come after it in the input, then after BINARY-INSERTION-SORT$(A, lo, h, s)$ the segment $A[lo \ldots h-1]$ is sorted stably.

*Proof.* For each $i$ from $s$ to $h - 1$, the binary search finds the least index $\ell$ with $A[i] < A[\ell]$ in the sorted prefix, so the new item goes after all items with key at most its key, in particular after its equal items, which are earlier in the input. The prefix stays sorted stably. $\square$

**Lemma 3 (gallop searches).** For a sorted segment $a[lo \ldots lo+n-1]$, GALLOP-LEFT returns the number of its items less than the key, and GALLOP-RIGHT the number of its items at most the key, for each hint in $[0, n)$.

*Proof.* The exponential phase keeps $a[lo + \text{last}] \prec \text{key}$ and $\text{key} \preceq a[lo + \text{ofs}]$ for the relevant order ($\prec$ is $<$ and $\preceq$ is $\le$ for GALLOP-LEFT; $\prec$ is $\le$ and $\preceq$ is $<$ for GALLOP-RIGHT), with $\text{last} = -1$ and $\text{ofs} = n$ standing for the two ends. The binary phase keeps the same relation and halves $\text{ofs} - \text{last}$ until they meet. The index where they meet is the boundary between the items that are $\prec$ the key and the rest, which is the claimed count. $\square$

**Lemma 4 (merge).** Let $A[p \ldots m-1]$ and $A[m \ldots q-1]$ be neighbouring runs, each sorted stably, with every item of the first earlier in the input than every item of the second. Then after MERGE-AT, $A[p \ldots q-1]$ is sorted stably.

*Proof.* By Lemma 3, the first $k$ items of the first run are at most the first item of the second run, so they are in their final places and come before all equal items of the second run, which is right for stability. In the same way, the items of the second run that are at least the last item of the first run, and so not less than any item of the first run, are in their final places. Ties between such an item and the last item of the first run put the first-run item first, which is again right. It remains to merge the middle parts.

For MERGE-LO, the invariant of the main loops is: $A[p' \ldots \text{dest} - 1]$ holds the $\text{dest} - p'$ items that come first in the stable order among the items of both middle parts, in that order; the rest are $\text{tmp}[i \ldots]$ and $A[j \ldots]$; and $\text{dest} \le j$, so no item is overwritten before it is read. A step of one item at a time takes $A[j]$ only if $A[j] < \text{tmp}[i]$, and otherwise $\text{tmp}[i]$, so the item that comes first in the stable order is output, and a tie goes to the first run. In galloping mode, GALLOP-RIGHT$(A[j], \text{tmp}, i)$ returns the number $k$ of items of $\text{tmp}[i \ldots]$ at most $A[j]$; these all come before $A[j]$ in the stable order, and they are copied in order. Then $A[j]$ is the next item, because $\text{tmp}[i]$, if any, is greater than it. GALLOP-LEFT$(\text{tmp}[i], A, j)$ returns the number $k_2$ of items of $A[j \ldots]$ less than $\text{tmp}[i]$, which come before it; then $\text{tmp}[i]$ is next. Each step keeps the invariant. When one part is empty, the rest of $\text{tmp}$, if any, is copied to the end, and the rest of the second run, if any, is already in place. MERGE-HI is the mirror image: it fills the segment from the right, outputs at each step the item that comes last in the stable order, takes the item of the first run only if the buffer item is less than it, so that a tie puts the second-run item last, and uses the two gallops with the roles exchanged. $\square$

**Theorem.** After TIMSORT$(A)$, the array is sorted stably.

*Proof.* Invariant of the loop of line L3: the runs on the stack are, from the bottom, consecutive segments that cover $A[0 \ldots lo-1]$, each sorted stably, and $A[lo \ldots n-1]$ is unchanged. Line L4 and Lemma 1, and then line L5 and Lemma 2, give a new run at $lo$ that is sorted stably, and line L6 pushes it. Each merge of line L7 joins two neighbouring runs of the stack; by Lemma 4 the result is sorted stably, and it covers the same segment. So the invariant holds after each step. Each step increases $lo$ by at least 1, so the loop ends with $lo = n$. Line L8 then merges neighbours until one run covers $A[0 \ldots n-1]$, and by Lemma 4 it is sorted stably. $\blacksquare$

**The depth of the stack.** If the invariants $Y > Z$, $X > Y + Z$ and $W > X + Y$ hold for each four consecutive runs from the top, then, from the top, the $i$-th run has length at least the $i$-th Fibonacci number $F_i$, up to the run on top. Since $F_i$ grows as $\phi^i$ and the lengths sum to at most $n$, the stack holds $O(\log n)$ runs. The check of four runs in merge_collapse is what makes the invariant hold for the whole stack, and not only at the top.
