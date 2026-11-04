---
title: The operations of a d-ary heap keep the heap property
proves: [correctness, termination]
status: full
---

Let $d \ge 2$. Write $p(j) = \lfloor (j - 2)/d \rfloor + 1$ for $j \ge 2$ and $C(j)$ for the set of children $d(j - 1) + 2, \ldots, dj + 1$ of $j$ that are at most $n$.

**The tree.** For each $j \ge 2$, $j$ is a child of $p(j)$, and each $c \in C(i)$ has $p(c) = i$: write $c = d(i - 1) + 1 + r$ with $1 \le r \le d$; then $c - 2 = d(i - 1) + (r - 1)$ with $0 \le r - 1 \le d - 1$, so $\lfloor (c - 2)/d \rfloor = i - 1$. Also $p(j) < j$ for $j \ge 2$. So the formulas define a rooted tree on $\{1, \ldots, n\}$ with root 1, in which each node has at most $d$ children, and the index of each node is larger than the index of its parent.

An *edge* is a pair $(p(j), j)$ with $2 \le j \le n$, and it *holds* when $A[p(j)] \le A[j]$. The invariant (H) says that each edge holds.

**Lemma 1 (sift-up).** If each edge $(p(j), j)$ with $j \ne i$ holds and, when $i \ge 2$, $A[p(i)] \le A[c]$ for each $c \in C(i)$, then SIFT-UP$(A, i)$ stops after at most the depth of $i$ iterations, only swaps keys, and afterwards (H) holds.

*Proof.* The proof of Lemma 1 on the [binary heap](/binary-heap/) proof page uses only these facts: the node $i$ has one parent $q$, the swap of line L4 exchanges $A[i]$ and $A[q]$ when $A[i] < A[q]$, the other children of $q$ held their edges to $q$, and the edges out of $i$ are covered by the second part of the hypothesis. All of them hold in a tree with any number of children per node, with "each other child $s$ of $q$" in place of "the other child". Each iteration moves $i$ to its parent, so it stops after at most the depth of $i$ iterations, at the root or when the edge into $i$ holds. $\square$

**Lemma 2 (sift-down).** If each edge $(p(j), j)$ with $p(j) \ne i$ holds and, when $i \ge 2$, $A[p(i)] \le A[c]$ for each $c \in C(i)$, then SIFT-DOWN$(A, n, i)$ stops after at most the height of $i$ swaps, changes only cells of the subtree of $i$, and afterwards (H) holds.

*Proof.* Lines L7 to L10 set $m$ to an index of a smallest key among $A[i]$ and $A[c]$ for $c \in C(i)$: the loop goes over all children $\mathrm{CHILD}(i, 1), \ldots, \mathrm{CHILD}(i, d)$, skips those beyond $n$, and keeps the index of the least key seen, with $m = i$ at the start. If $m = i$, the edges out of $i$ hold, and with the hypothesis each edge holds. Else let $x = A[i] > y = A[m]$, with $y \le A[s]$ for each other child $s$ of $i$. After the swap of line L12, the edge $(i, m)$ holds since $y \le x$, each edge $(i, s)$ holds since $y \le A[s]$, and the edge $(p(i), i)$, if $i \ge 2$, holds since the hypothesis gave $A[p(i)] \le y$. The hypothesis holds again at $m$: its parent $i$ now holds $y$, and the children $c$ of $m$ had $y \le A[c]$, since the edges out of $m$ were not excluded. Each swap moves $i$ one level down in the subtree of the first $i$, so there are at most as many swaps as its height. $\square$

**Insert.** After line L13 the new cell $n + 1$ is a leaf, and every old edge holds, so Lemma 1 applies to $i = n + 1$, and (H) holds after line L14. The keys are the old keys and $k$.

**Find-min and extract-min.** By (H) and induction along the path from the root, $A[1] \le A[j]$ for each $j$. So $A[1]$ is a minimum. Line L16 saves it, moves $A[n]$ to the root and drops the cell $n$. Every edge not out of the root joins two unchanged cells, so it holds, and the root has no parent. So Lemma 2 applies to $i = 1$, and (H) holds after line L17. The keys are the old keys with one copy of the minimum removed.

**Decrease-key.** If $k \le A[i]$, the edges out of $i$ still hold after line L20 writes $k$, the old edges give $A[p(i)] \le A[i] \le A[c]$ for each $c \in C(i)$, and every other edge is unchanged. So Lemma 1 applies, and (H) holds.

**Build.** Before the iteration of line L22 for $i$, the subtree of each $j > i$ is a heap. If $n \le 1$ there is no edge and nothing to do. Else, at the start, $i = p(n)$, and each $j > p(n)$ has no children: $d(p(n) - 1) = d\lfloor (n - 2)/d \rfloor \ge n - 1 - d$, so the first child of $j$ is $d(j - 1) + 2 \ge d\,p(n) + 2 \ge n + 1$. So the subtree of $j$ has no edges. In the iteration for $i$, the children of $i$ have larger indices, so their subtrees are heaps, and Lemma 2 applied to the subtree of $i$ makes it a heap. Lemma 2 changes only cells of that subtree. A $j > i$ is not an ancestor of $i$, so the subtree of $j$ is either inside the subtree of $i$, and then it is part of a heap, or disjoint from it, and then it did not change. After $i = 1$, the whole tree is a heap.

**Theorem.** Each operation keeps (H), FIND-MIN and EXTRACT-MIN return a minimum, the keys change as the [priority queue](/priority-queue/) type says, and each operation stops.

*Proof.* The cases above with Lemmas 1 and 2. $\blacksquare$
