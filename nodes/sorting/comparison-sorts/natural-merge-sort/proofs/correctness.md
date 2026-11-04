---
title: Natural merge sort sorts the array stably
proves: [correctness]
status: full
---

Tag each input item with its index. We say that a part $A[b \ldots e-1]$ is *stably sorted* when its keys are non-decreasing and, for equal keys, the tags are increasing.

**Lemma 1 (the runs).** After line L1, $B = [b_0, \ldots, b_r]$ with $0 = b_0 < b_1 < \cdots < b_r = n$ for $n \ge 1$, and each part $A[b_{t-1} \ldots b_t - 1]$ is stably sorted.

*Proof.* The scan adds the index $i$ to $B$ exactly when $A[i] < A[i-1]$, then adds $n$. So between two neighbouring bounds, $A[i-1] \le A[i]$ for each $i$, and the keys are non-decreasing. Nothing has moved yet, so the tags increase along each part. $\square$

**Lemma 2 (the merge).** If $A[lo \ldots mid-1]$ and $A[mid \ldots hi-1]$ are stably sorted, and each tag in the left part is less than each tag in the right part, then after MERGE$(A, lo, mid, hi)$ the part $A[lo \ldots hi-1]$ holds the same items and is stably sorted. Nothing outside it changes.

*Proof.* This is the merge of [merge sort](/merge-sort/). Its invariant is that $A[lo \ldots k-1]$ holds the $k - lo$ least items of the two parts in stably sorted order, where an item of the left part counts as less than an item of the right part with an equal key. A step takes the right head only if it is strictly less than the left head, and else the left head, so it takes the least remaining item in this order. The loop ends when one part is used up, and the rest of the other part is already in place or is copied in order. The tags of the left part are all less than those of the right part, so on equal keys the tags increase. $\square$

**Theorem.** NATURAL-MERGE-SORT$(A)$ stops, and after it $A$ holds the input items and is stably sorted.

*Proof.* If $n = 0$, then $B = [0]$, the loop does not run, and the empty array is sorted. Let $n \ge 1$. We use this invariant before each test of line L2:

> $B = [b_0, \ldots, b_s]$ with $0 = b_0 < \cdots < b_s = n$, $A$ holds the input items, each part $A[b_{t-1} \ldots b_t - 1]$ is stably sorted, and each tag in a part is less than each tag in each later part.

By Lemma 1 it holds at the start, since the parts are the runs in input order and nothing has moved. Assume it before a pass with $s \ge 2$. For $t = 2, 4, \ldots$, line L5 merges the parts $t - 1$ and $t$, which are neighbours with the tags of the first less than the tags of the second. By Lemma 2 the merged part is stably sorted and holds the same items. Its tags are those of the two parts, so they are still less than the tags of all later parts and larger than the tags of all earlier parts. If $s$ is odd, the last part does not change. Line L6 and line L7 put into $C$ exactly the bounds of the new parts, ending with $n$. So the invariant holds for $C$, which has $\lceil s/2 \rceil + 1$ entries. Since $\lceil s/2 \rceil < s$ for $s \ge 2$, the number of parts falls in each pass, and the loop stops with $s = 1$. Then $A[0 \ldots n-1]$ is one part, which is stably sorted. $\blacksquare$
