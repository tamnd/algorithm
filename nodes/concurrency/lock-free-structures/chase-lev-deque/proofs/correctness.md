---
title: The Chase-Lev deque is a linearizable work-stealing deque, and each of its operations ends in a bounded number of steps
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode of the page and its model: one owner, any number of thieves, asynchronous processes that may crash, atomic read, write and CAS, sequential consistency, and indices that do not wrap. This is a proof sketch: the lemmas give the key steps, and some routine cases (for example the bookkeeping of a growth that runs at the same time as several steals) are only outlined. The tests check the claims on all interleavings of small cases.

Write $T$ and $B$ for the values of `top` and `bottom` at a time. The *item of index $i$* is the argument of the push that wrote index $i$ last before the current time; the push with $b = i$ at L1 writes index $i$.

**Lemma 1 (top).** $T$ changes only by a successful CAS from $t$ to $t + 1$. So $T$ never decreases, and for each value $t$ at most one CAS on `top` that expects $t$ succeeds.

*Proof.* `top` is written only at L11 and L18, both CAS steps from $t$ to $t + 1$. After the first success from $t$, $T > t$ for ever, so no later CAS that expects $t$ succeeds. ∎

**Lemma 2 (bottom).** Only the owner writes `bottom`. Outside a pop, $T \le B$. Inside a pop, after L6 and before the pop returns, $B = b$ and $T \le b + 1$.

*Proof sketch.* By induction over the owner's operations. A push raises $B$ by one. A pop lowers $B$ by one at L6, from $b + 1$ to $b$, when $T \le b + 1$. While $B = b$, a successful CAS from $t$ belongs to a thief that read `bottom` $> t$ after it read $T = t$. If it read $b + 1$ before L6, then $t \le b$; if it read $b$ after L6, then $t < b$. (A thief that read a larger `bottom` from before an earlier pop also read $T = t$ before that pop, and the same argument applies to that pop.) So $T \le b + 1$ while $B = b$. If the pop returns at L10, it read $t < b$, and by Lemma 3 below no CAS from $b$ succeeds, so $T \le b = B$ at the end. If it writes $b + 1$ back at L8 or L12, then $T \le b + 1 = B$. ∎

**Lemma 3 (no theft below the owner).** If the owner's pop reads $t < b$ at L7, then no CAS on `top` from $b$ succeeds while $B = b$ after that pop.

*Proof.* Such a CAS belongs to a thief that read $T = b$ at L14 and then `bottom` $> b$ at L15. Since $B = b$ from L6 on, until the owner pushes again, the read of `bottom` $> b$ happened before L6, and so the read of $T = b$ happened before L6 too. Then by Lemma 1, $T \ge b$ at the owner's L7, after L6, which contradicts $t < b$. If the owner pushes again, $B = b + 1$ and the index $b$ holds a new item; this case is the ordinary steal of Lemma 4. ∎

Sequential consistency is used here: the owner's write at L6 comes before its read at L7, and the thief's read at L14 comes before its read at L15. With a store-load reordering in the owner, the proof fails at this point, and the test with `reorder_pop` finds the run in which an item is taken twice.

**Lemma 4 (the right item).** A thief whose CAS on `top` from $t$ succeeds returns the item of index $t$.

*Proof.* The thief read `bottom` $> t$ at L15, so the push of index $t$ had done L4, and its write of the slot (L3) came before. The thief then reads `array` and the slot at L17. Two things could make it read the wrong value. (a) The owner wrote a newer item into the same slot of the same array, that is, it pushed index $t + s$ into that array. That push found $b - t' < s - 1$ with $b = t + s$, so $t' > t + 1$, and by Lemma 1 the thief's CAS from $t$ then fails. (b) The thief read an array that was replaced. A growth copies indices $t'$ to $b - 1$ of the old array into the new one and never writes the old one again, so a thief that reads an old array finds the value that index $t$ had at the copy, or a value of case (a). In both cases a successful CAS means that the value read is the item of index $t$. ∎

**Theorem 1 (linearizability).** Each history of the deque is linearizable with respect to the work-stealing deque specification with ABORT.

*Proof sketch.* Choose the points:

1. push: L4.
2. pop that reads $t < b$: L6.
3. pop that reads $t > b$: L7, with result EMPTY.
4. If $T = b$ when the owner does L6 in a pop, the item of index $b$ goes to the process $W$ whose CAS on `top` from $b$ succeeds. Such a $W$ exists: if the owner reads $t = b$ at L7, it does this CAS itself and someone succeeds; if it reads $t = b + 1$, a thief did it between L6 and L7. In both cases the successful CAS comes after L6, and $W$ started before it, so L6 lies inside the interval of $W$ or is a step of $W$. The operation of $W$ takes effect at the owner's L6. If $W$ is a thief, the owner's pop takes effect at its L7 (when it reads $t > b$) or at its failed CAS at L11, with result EMPTY.
5. Any other successful steal: its CAS at L18.
6. A steal that returns EMPTY: its read of `bottom` at L15.
7. A steal that returns ABORT: its CAS at L18, with no effect.

Claim: at every time, the abstract sequence (the result of applying the operations in the order of their points) is the items of indices $T, \ldots, B - 1$, or empty when $T \ge B$. It holds at the start. A push at L4 appends the item of index $b = B$. A point of kind 2 or 4 is the owner's L6, which changes $B$ from $b + 1$ to $b$; it removes the item of index $b$, the last one, which the pop (kind 2, by Lemma 3 nobody else takes it) or the winner $W$ (kind 4, by Lemma 1 there is only one) returns. A CAS of kind 5 moves $T$ from $t$ to $t + 1$ with $t < B$ (the case $t = B$ is kind 4), so it removes the front item, and by Lemma 4 the thief returns it. A write of `bottom` back to $b + 1$ at L8 or L12 happens when $T = b + 1$, so the sequence stays empty. A failed CAS and the reads at L7 and L15 do not change $T$ or $B$. The results: at a point of kind 3, $T \ge b + 1 > B$, so the sequence is empty; at a point of kind 6, the thief read $T = t$ before and $B \le t$ now, so $T \ge t \ge B$ by Lemma 1 and the sequence is empty; the owner's EMPTY in kind 4 comes after $W$ took the only item. So each operation returns what the specification returns at its point, and each point lies within its operation. ∎

**Theorem 2 (progress).** Each operation ends within a bounded number of its own steps: push in at most $2n + 8$, pop in at most 8, steal in at most 6, where $n$ is the number of items. So the deque is wait-free with respect to the specification with ABORT. A thief that retries until it gets an item or EMPTY is lock-free: each ABORT is caused by a successful CAS on `top`, which ends another operation that took an item.

*Proof.* The code has no loops except the copy in GROW, which runs $b - t \le s - 1 = n$ times. The counts follow by inspection. A failed CAS from $t$ means that $T \ne t$; since $T$ was $t$ at L14 and only grows, some CAS on `top` succeeded in between, and the operation that did it returns an item within two more of its own steps (L19, or L12 and L13). ∎
