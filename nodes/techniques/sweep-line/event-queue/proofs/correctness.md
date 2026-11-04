---
title: The event queue keeps one entry per point and pops the smallest point with all its payloads
proves: [correctness]
status: full
---

We use the pseudocode of the page. The queue has a binary heap $H$ (an array with the heap order on the sweep order $<$, a total order on points) and a map $I$ from points to lists of payloads. The *abstract state* of the queue is a finite set $S$ of points and, for each $p \in S$, a list $A(p)$. The empty queue has $S = \emptyset$.

The abstract operations are defined as follows. INSERT$(p, a)$ sets $S \leftarrow S \cup \{p\}$; if $p$ was not in $S$ it sets $A(p) \leftarrow [\,]$; then, if $a \ne$ NIL, it appends $a$ to $A(p)$. POP-MIN, for $S \ne \emptyset$, returns $(p, A(p))$ with $p = \min S$ and sets $S \leftarrow S \setminus \{p\}$. CONTAINS$(p)$ returns whether $p \in S$, and IS-EMPTY returns whether $S = \emptyset$.

**Invariant.** The concrete state $(H, I)$ represents $(S, A)$ when:

> **(R1)** the entries of $H$ are pairwise distinct, and the set of entries of $H$ equals the set of keys of $I$, which equals $S$;
>
> **(R2)** $H$ has the heap order: for each index $j \ge 1$, $H[\lfloor (j-1)/2 \rfloor] \le H[j]$;
>
> **(R3)** $I[p] = A(p)$ for each $p \in S$.

**Claim.** If the queue starts empty, then after each sequence of operations (R1) to (R3) hold for the abstract state reached by the same sequence, and each operation returns the abstract result.

*Proof.* By induction on the number of operations.

*Base.* The empty queue has $H$ empty and $I$ empty. Both sets are $\emptyset = S$, so (R1) holds; (R2) holds with no index $j$; (R3) holds with no $p$.

*Step.* Assume (R1) to (R3) hold before an operation. We show that they hold after it, for the new abstract state, and that the result is right.

- **INSERT$(p, a)$, case $p \in S$.** By (R1), $p$ is a key of $I$, so line L1 is true. Line L2 appends $a$ to $I[p]$ when $a \ne$ NIL, which is what the abstract INSERT does to $A(p)$. $H$ and the set of keys of $I$ do not change, and the abstract $S$ does not change, so (R1) and (R2) hold. (R3) holds for $p$ by the above and for the other points because nothing else changed.
- **INSERT$(p, a)$, case $p \notin S$.** By (R1), $p$ is not a key of $I$ and not an entry of $H$, so line L1 is false. Line L3 makes $p$ a key with the list $[a]$, or $[\,]$ if $a = $ NIL, which is the new $A(p)$. Line L4 adds $p$ to $H$. The entries of $H$ stay pairwise distinct because $p$ was not one of them, and the sets of entries and of keys both become $S \cup \{p\}$, so (R1) holds. HEAP-INSERT restores the heap order (R2); this is the standard property of the sift-up of a binary heap (CLRS, Section 6.5). (R3) holds as in the first case.
- **POP-MIN, with $S \ne \emptyset$.** By (R1), $H$ is not empty. By (R2) and the transitivity of $\le$, each entry is at least the root, because the path from the root to it is non-decreasing. So the root is $\min$ of the entries of $H$, which by (R1) is $p = \min S$, and line L5 returns this $p$ and leaves a heap of the other entries in heap order (the sift-down of CLRS, Section 6.2 and 6.5). Since the entries were distinct, $p$ no longer occurs in $H$. Line L6 reads $I[p] = A(p)$ by (R3) and removes the key $p$. Both sets are now $S \setminus \{p\}$, so (R1) and (R2) hold, (R3) holds for the remaining points, and line L7 returns $(p, A(p))$ as required.
- **CONTAINS$(p)$.** Line L8 returns whether $p$ is a key of $I$, which by (R1) is whether $p \in S$. Nothing changes.
- **IS-EMPTY.** Line L9 returns whether $H$ is empty, which by (R1) is whether $S = \emptyset$. Nothing changes.

So the invariant holds after each operation, and each result equals the abstract result. $\square$

**Consequence for a sweep.** Let a sweep insert only points that are larger than the last popped point. Then the sequence of popped points is strictly increasing. Let $q$ be a popped point and $q'$ the next one. Just after the pop of $q$, each point of $S$ is larger than $q$, because $q$ was the minimum of a set of distinct points and was removed. Each point inserted after that is larger than $q$ by the rule. So $q' = \min S > q$ at the next pop. A popped point is then never inserted again, since each later insert is larger than it. So each event point is popped exactly once, with the payloads of all the inserts of that point. $\blacksquare$
