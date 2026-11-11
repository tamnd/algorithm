---
title: The Michael-Scott queue is linearizable and lock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page and its model: asynchronous processes that may crash, atomic read, write and CAS, sequential consistency, and no reuse of a node while a process holds it. Let $L$ be the list of nodes reachable from `Head`, and let abs be the sequence of the values of the nodes of $L$ after the first one (the dummy).

**Lemma 1 (invariants).** In each state: (a) $L$ is finite, it has no repeated node, and only its last node has `next` = NULL; (b) `Tail` points to the last node of $L$ or to the node before it; (c) a `next` field that is not NULL never changes again, and a node that left $L$ never comes back; (d) a node allocated at L1 whose CAS at L7 has not yet succeeded is not reachable from any node.

*Proof.* By induction on the steps. At the start $L$ is the dummy and the setup nodes, `Tail` is the last node, and (a) to (d) hold. Only CAS steps change shared words (L1 writes only a fresh node).

*CAS at L7, $t.next$ from NULL to $n$.* By (a), the only node with `next` = NULL that is reachable is the last node of $L$; but $t$ may have left $L$. If $t$ left $L$, it was the dummy and `Head` moved past it; `Head` moves only by L19, from $h$ to $h.next \ne$ NULL, so a node that left $L$ has a non-NULL `next`, and by (c) the CAS fails. So a successful CAS acts on the last node of $L$, and $n$ (fresh and unreachable by (d)) becomes the new last node. Now `Tail` points to the old last node, which is the node before the last one, so (b) holds.

*CAS at L8, L9 or L17 on `Tail`, from $t$ to a node $x$.* At L8 and L17, $x$ was read as $t.next$; at L9, $x = n$ and the CAS at L7 set $t.next = n$. By (c), $x = t.next$ still holds. If the CAS succeeds, `Tail` was $t$, and by (b) $t$ is the last node or the one before. It cannot be the last node, since $t.next = x \ne$ NULL; so $t$ is the node before the last, and $x$ is the last node. (b) holds.

*CAS at L19, `Head` from $h$ to $nx$.* If it succeeds, `Head` was $h$. The test at L14 found `Head` $= h$ after the read of $nx = h.next$ at L13, so $nx$ was read while $h$ was in $L$, and by (c) $nx = h.next$ now. The process reached L18 only if $h \ne t$, where $t$ is the value of `Tail` read at L12 while `Head` was $h$ (L11 and L14 both saw $h$, and `Head` only moves forward, so `Head` $= h$ at L12). At L12, by (b), `Tail` was $h$'s successor or a later node, and `Tail` only moves forward; so after the CAS, `Tail` is at or after $nx$, and (b) still holds for the new $L$. (a) and (c) hold because $L$ loses its first node only. ∎

**Lemma 2 (effects).** A successful CAS at L7 of enq$(v)$ appends $v$ to abs. A successful CAS at L19 removes the first value of abs, and the dequeue returns that value. A read at L13 whose dequeue then returns EMPTY happens in a state where abs is empty. No other step changes abs.

*Proof.* The first claim is the L7 case of Lemma 1: $n$ becomes the last node of $L$ and $n.val = v$. For L19, the new dummy is $nx$, the first node after $h$, so abs loses its first value, $nx.val$; L18 read $nx.val$ before the CAS, and the value of a node never changes after L1. For the empty case: the dequeue returns EMPTY at L16 after it saw `Head` $= h$ at L11 and at L14 and $h.next$ = NULL at L13. As `Head` only moves forward and never returns, `Head` $= h$ at the time of L13, so $L$ was the dummy alone and abs was empty. CASes on `Tail` and failed CASes do not change $L$. ∎

**Theorem (linearizability).** Each history is linearizable.

*Proof.* Assign to each enqueue its successful CAS at L7, to each dequeue that returns an item its successful CAS at L19, and to each dequeue that returns EMPTY its last read at L13. A pending enqueue that has done its CAS at L7 gets that step; a pending dequeue that has done its CAS at L19 gets that step; other pending operations are dropped, as they changed nothing (Lemma 2). Each point lies inside the interval of its operation, so the order of the points respects real time. By Lemma 2 and induction over the points, a sequential queue that applies the operations in this order has the content abs after each point and returns the same results. ∎

**Theorem (lock-freedom).** In each infinite run in which some process takes infinitely many steps, infinitely many operations complete.

*Proof.* Assume that after some time $T$ no operation completes, while process $p$ takes infinitely many steps. Each loop iteration takes at most 6 steps, so $p$ runs infinitely many iterations, each of which fails. Look at why an iteration fails. In ENQUEUE it fails if `Tail` changed between L3 and L5, if $nx \ne$ NULL (then `Tail` lags, so L8 or someone moves `Tail`), or if the CAS at L7 fails (then some `next` became non-NULL, a successful L7). In DEQUEUE it fails if `Head` changed between L11 and L14, if $h = t$ and $nx \ne$ NULL (`Tail` lags), or if the CAS at L19 fails (a successful L19). So each failed iteration is matched with a successful L7 or L19, or with a state in which `Tail` lags, or with a change of `Tail`.

After $T$, each process performs at most one successful L7 or L19, because the operation then returns within 2 more steps, and no operation returns. So after some time $T' \ge T$ no successful L7 or L19 happens, and $L$ does not change. Then `Tail` can move at most once more (from the node before the last to the last), and after that `Tail` does not lag and does not change. From then on, each iteration of $p$ meets none of the reasons to fail, and its operation completes. Contradiction. ∎
