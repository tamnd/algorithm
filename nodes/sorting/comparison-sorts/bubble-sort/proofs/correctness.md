---
title: Bubble sort sorts the array and stops
proves: [correctness, termination]
status: full
---

Each change of $A$ is an exchange of two items, so the multiset of the items never changes. We prove that the order is correct and that the loop stops.

**Invariant of the outer loop.** At each test of line L2:

> **(B)** $A[bound+1 \ldots n-1]$ is sorted in non-decreasing order, and each of its items is at least each item of $A[0 \ldots bound]$.

**Lemma (one pass).** Assume (B) at the start of a pass, with $bound \ge 1$. Let $A_0$ be the array at the start of the pass. Then during the pass, just before the comparison of line L5 for index $j$, $A[j]$ is a largest item of $A_0[0 \ldots j]$. After the pass, with the value $last$ of line L8:

1. $A[last+1 \ldots bound]$ is sorted;
2. each item of $A[0 \ldots last]$ is at most $A[last+1]$.

*Proof.* The first claim is by induction on $j$. For $j = 0$ no exchange has happened yet, so $A[0] = A_0[0]$. Assume it for $j$. Lines L5 and L6 put the larger of $A[j]$ and $A[j+1]$ at $j+1$. The item $A[j+1]$ was not touched before step $j$, so it is $A_0[j+1]$. So after the step, $A[j+1]$ is a largest item of $A_0[0 \ldots j+1]$, and the item at $j+1$ is not changed again before the comparison for $j + 1$.

Now the two claims. After the last step of the pass, $A[bound]$ is a largest item of $A_0[0 \ldots bound]$ by the first claim. Consider the steps $j = last+1, \ldots, bound-1$. By the definition of $last$, line L5 found no pair out of order in these steps, so $A[j] \le A[j+1]$ at each of them, and these positions were not changed after their step. So $A[last+1] \le A[last+2] \le \cdots \le A[bound]$, which is claim 1. For claim 2, there are two cases. If the pass made an exchange, the last one was at $j = last$, and it put at $last + 1$ a largest item of $A_0[0 \ldots last+1]$, which is at least each item now in $A[0 \ldots last]$, because those items are a sub-multiset of $A_0[0 \ldots last+1]$ minus this one item. If the pass made no exchange, then $last = 0$, and the step $j = 0$ found $A[0] \le A[1]$. $\square$

**Theorem.** BUBBLE-SORT$(A)$ stops after at most $n - 1$ passes, and after it $A$ is sorted.

*Proof.* *Initialization.* Line L1 sets $bound = n - 1$. Then $A[bound+1 \ldots n-1]$ is empty, so (B) holds.

*Maintenance.* Assume (B) and $bound \ge 1$, and let $last$ be the value after the pass. The pass changes only $A[0 \ldots bound]$, so $A[bound+1 \ldots n-1]$ is unchanged and still sorted, and its items are still at least each item of $A[0 \ldots bound]$, since this part holds the same multiset as before. By the lemma, $A[last+1 \ldots bound]$ is sorted. Its last item $A[bound]$ is an item of $A[0 \ldots bound]$, so it is at most $A[bound+1]$. So $A[last+1 \ldots n-1]$ is sorted. Each item of $A[0 \ldots last]$ is at most $A[last+1]$ by claim 2 of the lemma, and so at most each item of $A[last+1 \ldots n-1]$. Line L8 sets $bound \leftarrow last$, and (B) holds.

*Termination.* In a pass, line L7 sets $last$ only to values $j \le bound - 1$, and line L3 sets it to $0 \le bound - 1$. So each pass makes $bound$ smaller by at least 1. It starts at $n - 1$ and the loop runs while $bound > 0$, so there are at most $n - 1$ passes. When the loop stops, $bound \le 0$. If $n \ge 1$, then $bound = 0$, and (B) says that $A[1 \ldots n-1]$ is sorted and that $A[0]$ is at most each of its items, so $A$ is sorted. If $n = 0$, the array is empty. $\blacksquare$

**Stability.** Line L5 exchanges two items only when the left one is strictly larger. So two equal items are never exchanged. An item moves only by exchanges with its neighbour, so it can pass an equal item only by an exchange with it. So equal items keep their relative order.

**Exchanges.** Each exchange of line L6 swaps a pair $A[j] > A[j+1]$ of neighbours. This pair is an inversion, and the exchange changes no other pair of items, so it lowers the number of inversions by exactly 1. The sorted array has none. So the number of exchanges equals the number of inversions of the input.
