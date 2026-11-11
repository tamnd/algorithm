---
title: The ABP deque is a linearizable work-stealing deque, its tag prevents ABA, and each of its operations ends in a bounded number of steps
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode of the page and its model: one owner, any number of thieves, asynchronous processes that may crash, atomic read, write and CAS, sequential consistency, and a tag that does not wrap. This is a proof sketch; some routine cases are only outlined, and the tests check the claims on all interleavings of small cases.

A *period* is the time between two writes of `age` by the owner (at L19 or L20); in a period, `tag` is fixed. Write $T$ for `top` and $B$ for `bot` at a time.

**Lemma 1 (age).** Within a period, `age` changes only by a successful CAS at L9, which adds one to `top`. A CAS at L9 or L19 succeeds only if its expected value was read in the same period.

*Proof.* The owner writes `age` only at L19 and L20, and both writes start a new period with a tag that was never used before (the tag only grows). A thief writes `age` only at L9, from (`tag`, $t$) to (`tag`, $t + 1$). So a value of `age` from an earlier period never comes back, and a CAS that expects it fails. ∎

**Lemma 2 (no theft below the owner).** If the owner's popBottom reads `age` with $b >$ `top` at L16, then no CAS of a thief takes index $b$ while $B = b$ after it.

*Proof.* A thief that takes index $b$ read `age` with `top` $= b$ at L4 and then `bot` $> b$ at L5. Since $B = b$ from the owner's L13 on (until the owner pushes again), the read of `bot` came before L13, so the read of `top` $= b$ came before L13 too, in the same period by Lemma 1. Within a period `top` only grows, so the owner's read at L15 sees `top` $\ge b$, which contradicts $b >$ `top`. ∎

**Lemma 3 (the right item).** A thief whose CAS at L9 succeeds returns the item of the push that wrote `deq[t]` last before the thief's read of `bot`, where $t$ is its `top`.

*Proof.* The thief read `bot` $> t$ at L5, so the push of index $t$ had done L3, and its write of `deq[t]` came before. The owner writes `deq[t]` again only by a push with $b = t$, which needs $B = t$ first. Within one period, $B$ falls to $t$ only by pops; a pop that lowers $B$ to $t$ either finds $t >$ `top`, and then by Lemma 2 index $t$ is not taken by the thief, which contradicts its success, or finds `top` $= t$ and ends the period at L19 or L20, so the thief's CAS fails by Lemma 1. Hence a successful CAS means the slot was not written again between the read of `bot` and the read of `deq[t]`. ∎

**Theorem 1 (linearizability).** Each history of the ABP deque is linearizable with respect to the work-stealing deque specification in which steal may return ABORT with no effect.

*Proof sketch.* Take the points of the page: push at L3; pop with $b >$ `top` at L13; pop that returns EMPTY at L12 or at its read at L15 when $b <$ `top`; if `top` $= b$ at the owner's L13, the winner of the CAS on `age` from (`tag`, $b$) takes effect at the owner's L13 (this winner exists: either the owner's CAS at L19 succeeds, or a thief's CAS succeeded first, after L13, since `top` $= b$ at the owner's read at L15), and a losing owner takes effect at its failed CAS with EMPTY; any other successful popTop at its CAS; a popTop that returns EMPTY at L5; ABORT anywhere in its interval, with no effect.

Claim: at every time, the abstract sequence is `deq[T]`, ..., `deq[B-1]`, or empty when $T \ge B$. A push appends at index $B$. The owner's L13 removes index $b$ when $T \le b$: by the pop (Lemma 2: nobody else takes it) or by the unique winner of the race (Lemma 1). A thief's successful CAS from $t < B$ removes the front item, which it returns by Lemma 3. The resets at L17, L19 and L20 happen when $T \ge B$ in the abstract sense (the item at index $b = T$ already went to the winner at L13), so they keep the sequence empty. An EMPTY of a thief: it read $T = t$ at L4 and then $B \le t$ at L5; within the period $T \ge t \ge B$, and if a reset happened in between, the deque was empty at the reset, which is a time inside the thief's interval. So each operation returns what the specification returns at its point. ∎

**Theorem 2 (the tag is needed).** Without the new tag at L18, there is a run in which one item is returned twice.

*Proof.* The run of the example on the page: the thief reads `age` $= (0, 0)$ and `deq[0]` $= 1$; the owner pops 1 and sets `age` to $(0, 0)$ again, then pushes 2 at index 0; the thief's CAS from $(0, 0)$ to $(0, 1)$ succeeds and it returns 1. The test `test_aba_without_the_tag` replays this run. ∎

**Theorem 3 (progress).** pushBottom takes 3 steps, popTop at most 4, popBottom at most 7. A popTop returns ABORT only if another operation removed an item during its call.

*Proof.* The code has no loops; the counts follow by inspection. If the CAS at L9 fails, `age` changed after the read at L4: by a thief's successful CAS, which removed an item, or by the owner at L19 or L20, which happens in a pop that found `top` $\ge b$; such a pop either removed the last item itself, or follows a removal by a thief, or reset a deque that a thief had already emptied, in which case the thief's own read of `bot` at L5 was made before that removal. ∎
