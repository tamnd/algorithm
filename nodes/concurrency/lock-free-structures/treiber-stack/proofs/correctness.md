---
title: The Treiber stack is linearizable and lock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, the model of the page (asynchronous processes that may crash, atomic read, write and CAS, sequential consistency), and the plain version with no frees, or with a scheme under which an address is not reused while a process holds it (a garbage collector, hazard pointers or epochs). The tagged version is treated at the end.

Let $L$ be the sequence of nodes reached from `top` by `next` pointers, and let abs be the sequence of their `val` fields. A node is *published* when a CAS at L5 has made `top` point to it.

**Lemma 1.** In each state: (a) $L$ is finite and has no repeated node; (b) the `val` and `next` fields of a node in $L$ do not change while it stays in $L$; (c) a node allocated at L1 whose push has not yet done a successful CAS is not in $L$, and no node in $L$ points to it.

*Proof.* By induction on the steps. At the start, $L$ is the list of the setup and the claims hold. Only three kinds of steps write shared words. A write at L4 writes the `next` field of a node $n$ of an open push, and by (c) $n$ is not in $L$, so $L$ does not change and (b) holds. A successful CAS(`top`, $t$, $n$) at L5: at L4 this process wrote $n.next = t$, and by (c) nobody else wrote $n.next$ since, so the new $L$ is $n$ followed by the old $L$; $n$ was not in the old $L$, so (a) holds, and $n$ is no longer the node of an open push, so (c) holds for the other nodes. A successful CAS(`top`, $t$, $nx$) at L10: `top` $= t$, so $t$ is the first node of $L$. The value $nx$ was read from $t.next$ at L9, and we must show that $t.next = nx$ still holds. Between the read of L7 and the CAS, either $t$ stayed in $L$ the whole time, and then (b) gives $t.next = nx$; or $t$ left $L$ and came back. A node that left $L$ was removed by a pop, and only a new push can put an address into $L$ again, which needs the allocator to return the address of $t$; by the assumption on reclamation this does not happen while our pop holds $t$. So $t$ stayed in $L$, the new $L$ is the old $L$ without its first node, and (a), (b) and (c) hold. ∎

**Lemma 2.** A successful CAS at L5 of push$(v)$ changes abs to $v$ followed by the old abs. A successful CAS at L10 of a pop changes abs from $u$ followed by $R$ to $R$, and the pop then returns $u$. A read at L7 that returns NULL happens in a state where abs is empty. No other step changes abs.

*Proof.* The first two claims are the cases of the proof of Lemma 1, together with (b): after the CAS at L10, the pop reads $t.val$ at L11, and $t.val$ is the value $u$ that $t$ had while it was in $L$ (only a push writes the fields of a node, and only before it is published, by (c); the node $t$ is not freed before L11). For the third claim, `top` = NULL means $L$ is empty. Other steps write no shared word, or write the `next` field of an unpublished node, which is not in $L$. ∎

**Theorem (linearizability).** Each history of the stack is linearizable.

*Proof.* Assign each completed operation the step named on the page: the successful CAS for a push and for a pop that returns an item, and the read at L7 that returned NULL for a pop that returns EMPTY. Each such step lies between the invocation and the response of its operation. For a pending operation that has done its successful CAS, use that CAS; drop the other pending operations (they changed nothing, by Lemma 2). Order the operations by these steps. This order respects real time, because if one operation responds before another is invoked, its step comes first. By Lemma 2, applying the operations in this order to a sequential stack gives exactly the abs after each step and exactly the results that the operations return. So the order is a legal sequential history. ∎

**Theorem (lock-freedom).** In each infinite run in which some process takes infinitely many steps, infinitely many operations complete.

*Proof.* Suppose that after some time $T$ no operation completes, but some process $p$ takes infinitely many steps. Each loop iteration takes at most 4 steps, so $p$ runs infinitely many iterations after $T$, and each one ends with a failed CAS, or the operation of $p$ would complete. A CAS on `top` fails only if `top` changed after the read at L3 or L7 of the same iteration, and only a successful CAS changes `top`. So infinitely many CASes succeed after $T$. But each operation does at most one successful CAS, and a process starts a new operation only after the current one completes. So after $T$ each process does at most one successful CAS, and there are at most $n$ of them. Contradiction. ∎

**The tagged version.** Now let the allocator reuse addresses, but keep freed nodes in type-stable memory, so that a read of a freed node returns some node value and does not fault. The word `top` holds $(t, c)$, and each successful CAS on `top` makes $c$ one larger. Assume that $c$ does not wrap around during one operation. A CAS at L10 with the expected value $(t, c)$ succeeds only if no successful CAS hit `top` since the read at L7. So `top` pointed to $t$ during the whole interval, $t$ stayed in $L$, and by (b) $t.next$ did not change since L9. The rest of the proof is the same. The stale read at L9 of a freed node can return garbage, but then the CAS at L10 fails and the garbage is not used. ∎
