---
title: Three-way quicksort sorts the array and keeps its items
proves: [correctness]
status: full
---

We write $S$ for the multiset of the items of $A[lo \ldots hi-1]$ at the start of a call. All changes to the array are swaps of two items of the range, so the range always holds $S$, and items outside the range do not change.

**Lemma (the partition).** Assume $hi - lo \ge 1$, and let $v$ be the item read at line L2. When the loop of lines L4 to L9 stops, $lo \le lt < gt \le hi$, each item of $A[lo \ldots lt-1]$ is less than $v$, each item of $A[lt \ldots gt-1]$ is equal to $v$, and each item of $A[gt \ldots hi-1]$ is larger than $v$.

*Proof.* We use this invariant, before each test of line L4:

> **(I)** $lo \le lt \le i \le gt \le hi$. Each item of $A[lo \ldots lt-1]$ is less than $v$, each item of $A[lt \ldots i-1]$ is equal to $v$, and each item of $A[gt \ldots hi-1]$ is larger than $v$.

*Start.* Line L3 sets $lt = i = lo$ and $gt = hi$, so the three parts are empty.

*Step.* Assume (I) and $i < gt$, and let $x = A[i]$.

- If $x < v$ (line L5), line L6 swaps $A[lt]$ and $A[i]$. If $lt < i$, the old $A[lt]$ was equal to $v$, and it moves to index $i$; if $lt = i$, nothing moves. Now $A[lt] = x < v$ and $A[lt+1 \ldots i]$ are equal to $v$. After $lt$ and $i$ grow by one, (I) holds.
- If $v < x$ (line L7), line L8 makes $gt$ one smaller and swaps $A[i]$ with $A[gt]$. Now $A[gt] = x > v$, so the large part grows by one item. The new $A[i]$ came from the unseen part, and $i$ does not change. Since $i < gt$ held before the step, $i \le gt$ holds after it, and (I) holds.
- Otherwise neither $x < v$ nor $v < x$, so $x$ is equal to $v$ in the total order. Line L9 makes $i$ one larger, and the equal part grows by $x$. (I) holds.

*End.* Each step makes $gt - i$ smaller by exactly one, so the loop stops after $hi - lo$ steps with $i = gt$. Then (I) says that the range is the small part $A[lo \ldots lt-1]$, the equal part $A[lt \ldots gt-1]$ and the large part $A[gt \ldots hi-1]$. The item $v$ is in the range, and it is neither less than $v$ nor larger than $v$, so it is in the equal part, and $lt < gt$. $\square$

**Theorem.** After THREE-WAY-QUICKSORT$(A, lo, hi)$, the range $A[lo \ldots hi-1]$ is sorted and holds $S$, and no item outside the range changes.

*Proof.* By strong induction on $k = hi - lo$. If $k \le 1$, line L1 returns, and the range is sorted. Let $k \ge 2$, and assume the claim for all shorter ranges. By the lemma, the loop ends with the three parts and $lt < gt$. The ranges $[lo, lt)$ and $[gt, hi)$ have fewer than $k$ items each, because the equal part is not empty. By the hypothesis, line L10 sorts the small part and changes nothing else; it permutes the small part, so its items stay less than $v$. Line L11 does the same for the large part. So the range is a sorted part of items less than $v$, then items equal to $v$, then a sorted part of items larger than $v$, and it is sorted. It holds $S$, because all moves were swaps inside the range. $\blacksquare$

**Termination.** Each call on $k \ge 2$ items makes two calls on fewer items, and each loop runs $k$ steps, so the algorithm stops.
