---
title: The operations of a binary heap keep the heap invariant and return a minimum
proves: [correctness, termination]
status: full
---

We write $n$ for $H.n$, $p(j) = \lfloor j/2 \rfloor$ for the parent of $j \ge 2$, and $C(j)$ for the set of children of $j$ that exist, a subset of $\{2j, 2j+1\}$ that holds only indices at most $n$. An *edge* is a pair $(p(j), j)$ with $2 \le j \le n$, and it *holds* when $A[p(j)] \le A[j]$. The invariant (H) says that each edge holds. Each operation changes $A$ only by swaps and by the writes of lines L12, L18 and L23, which we follow one by one.

**Lemma 1 (sift-up).** Let $1 \le i \le n$. Assume

> **(U)** each edge $(p(j), j)$ with $j \ne i$ holds, and if $i \ge 2$, then $A[p(i)] \le A[c]$ for each $c \in C(i)$.

Then SIFT-UP$(A, i)$ stops after at most $\lfloor \lg i \rfloor$ iterations, permutes the keys of $A[1 \ldots n]$, and after it (H) holds.

*Proof.* We show that (U) is a [loop invariant](/loop-invariant/) of line L1 for the current $i$. It holds at the start by assumption.

*Maintenance.* Let the test of line L1 be true, so $i \ge 2$ and, with $q = p(i)$, $x = A[q] > A[i] = y$. Line L2 swaps them, so afterwards $A[q] = y$ and $A[i] = x$. We check each edge that has $q$ or $i$ as an end, other than the edge into $q$, which (U) for the new value $i = q$ excludes.

- The edge $(q, i)$: $y \le x$, since $y < x$.
- The edges $(i, c)$ for $c \in C(i)$: the second part of (U) gave $x = A[q] \le A[c]$ before the swap, and $A[c]$ did not change.
- The edge $(q, s)$ for the other child $s$ of $q$, if it exists: the edge held before, so $x \le A[s]$, and now $A[q] = y < x \le A[s]$.

No other edge has an end at $q$ or $i$, except the edge $(p(q), q)$ when $q \ge 2$. So after line L3 sets $i \leftarrow q$, each edge except the one into the new $i$ holds. For the second part of (U) at the new $i = q \ge 2$: the edge $(p(q), q)$ held before the swap, because (U) excluded only the edge into the old $i$, so $A[p(q)] \le x$. The children of $q$ now hold $x$ (at the old $i$) and $A[s] \ge x$. So $A[p(q)]$ is at most each child of $q$.

*Termination.* Each iteration replaces $i$ by $\lfloor i/2 \rfloor$, so $\lfloor \lg i \rfloor$ drops by exactly 1, and the test $i > 1$ fails after at most $\lfloor \lg i \rfloor$ iterations. When the loop stops, either $i = 1$, and then (U) says that each edge holds because the root has no edge into it, or $A[p(i)] \le A[i]$, and then the one excluded edge holds too. In both cases (H) holds. Each change is a swap, so the keys are permuted. $\square$

**Lemma 2 (sift-down).** Let $1 \le i \le n$. Assume

> **(D)** each edge $(p(j), j)$ with $p(j) \ne i$ holds, and if $i \ge 2$, then $A[p(i)] \le A[c]$ for each $c \in C(i)$.

Then SIFT-DOWN$(A, n, i)$ stops after at most $h$ swaps, where $h = \lfloor \lg(n/i) \rfloor$ is the height of $i$, permutes the keys of $A[1 \ldots n]$, changes only the cells of the subtree of $i$, and after it (H) holds.

*Proof.* (D) is a loop invariant of line L4. It holds at the start by assumption. In an iteration, lines L5 to L7 set $m$ to an index of a smallest key among $A[i]$ and $A[c]$ for $c \in C(i)$: line L6 compares $A[2i]$ with $A[i]$, and line L7 compares $A[2i+1]$ with the smaller of the two, and each test is done only for a child that exists.

*Stop.* If $m = i$, then $A[i] \le A[c]$ for each $c \in C(i)$, so the edges out of $i$ hold, and with (D) each edge holds: (H) is true, and line L8 returns.

*Maintenance.* If $m \ne i$, let $x = A[i]$ and $y = A[m]$, so $y < x$ and $y \le A[s]$ for the other child $s$ of $i$. Line L9 swaps them. We check the edges with an end at $i$ or $m$, except the edges out of $m$, which (D) for the new value $i = m$ excludes.

- The edge $(i, m)$: $A[i] = y \le x = A[m]$.
- The edge $(i, s)$: $A[i] = y \le A[s]$.
- The edge $(p(i), i)$ if $i \ge 2$: the second part of (D) gave $A[p(i)] \le y$, because $m \in C(i)$, and $A[i]$ is now $y$.

For the second part of (D) at the new $i = m$: its parent is the old $i$, which now holds $y$, and each child $c$ of $m$ had $y = A[m] \le A[c]$ before the swap, because the edges out of $m$ were not excluded by (D). So line L10 keeps (D).

*Termination.* Each swap moves $i$ to a child, so the depth of $i$ grows by exactly 1. A node of the subtree of the first $i$ has depth at most $h$ below it, so there are at most $h$ swaps, and after them the next iteration stops at line L8 or finds no child. The changed cells are $i$ and its descendants. $\square$

**Insert.** Before line L11, (H) holds on $A[1 \ldots n]$. Lines L11 and L12 add the cell $n + 1$ with the key $k$. Each old edge holds, and the new node has no children. So (U) holds with $i = n + 1$, and Lemma 1 gives (H) on the new heap, whose keys are the old keys and $k$.

**Find-min.** By (H) and the global form of the [heap property](/heap-property/), $A[1] \le A[j]$ for each $j \le n$, because the root is an ancestor of each node. So line L15 returns a minimum. Nothing changes.

**Extract-min.** Let $n \ge 1$ and let $\mu = A[1]$, a minimum by the claim on find-min. Lines L18 and L19 write the last key $A[n]$ into the root and drop the cell $n$, so the keys of $A[1 \ldots n-1]$ are the old keys with one copy of $\mu$ removed. If $n - 1 = 0$, the heap is empty and (H) holds. Else each edge with $p(j) \ne 1$ is an old edge between two unchanged cells, so it holds, and the root has no parent. So (D) holds with $i = 1$, and Lemma 2 gives (H). Line L21 returns $\mu$.

**Decrease-key.** Let $k \le A[i]$, as line L22 checks, and let $a = A[i]$ before line L23. Each edge not into $i$ and not out of $i$ is unchanged. The edges $(i, c)$ held with $a$, and $k \le a$, so they still hold. If $i \ge 2$, then $A[p(i)] \le a \le A[c]$ for each $c \in C(i)$, by the old edges. So (U) holds, and Lemma 1 gives (H). The keys are the old keys with $a$ replaced by $k$.

**Build.** We claim that, before the iteration of line L26 for $i$, the subtree of each index $j > i$ is a heap, that is, each edge inside that subtree holds. At the start $i = \lfloor n/2 \rfloor$, and each $j > \lfloor n/2 \rfloor$ is a leaf, whose subtree has no edges. In the iteration for $i$, the subtrees of the children of $i$ have indices larger than $i$, so they are heaps. Consider the subtree of $i$ alone as a heap with root $i$: the only edges that may fail are the ones out of $i$, and $i$ has no parent inside it. So (D) holds for it, and by Lemma 2 the subtree of $i$ becomes a heap. Now take an index $j > i$, so that the claim must hold for the next iteration. If $j$ is in the subtree of $i$, its subtree is part of a heap, so it is a heap. Else the subtree of $j$ is disjoint from the subtree of $i$: an index $j > i$ is not an ancestor of $i$, because an ancestor has a smaller index. Lemma 2 says that only cells of the subtree of $i$ change, so the subtree of $j$ is unchanged and stays a heap. When the loop ends with $i = 1$, the subtree of $1$ is the whole tree, and (H) holds. Each step is a swap, so the keys of $A$ are the keys of $B$.

**Theorem.** If (H) holds before an operation, it holds after it; FIND-MIN and EXTRACT-MIN return a minimum key of the heap; and each operation changes the multiset of keys exactly as the [priority queue](/priority-queue/) type says (insert adds $k$, extract-min removes one minimum, decrease-key replaces the key at $i$ by $k$, build makes the multiset of $B$). Each operation stops.

*Proof.* The claims above, for each operation, together with Lemmas 1 and 2. $\blacksquare$
