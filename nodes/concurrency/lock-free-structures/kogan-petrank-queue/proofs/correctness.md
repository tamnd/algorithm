---
title: The Kogan-Petrank queue is linearizable and wait-free, with an explicit step bound
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode of the page and its model: $n$ asynchronous processes with ids $0, \ldots, n-1$ that may crash, atomic read, write and CAS, sequential consistency, and no reuse of nodes or descriptors. This file is an outline. The linearizability part follows the structure of the full proof of Kogan and Petrank (PPoPP 2011, Section 4), which we cite for the details. The explicit step bound in Theorem 3 is our own derivation; the paper proves wait-freedom without, as far as we found, this constant.

For a published operation $O$ we write $\mathrm{own}(O)$ for its process, $ph(O)$ for its phase and $t_O$ for the time of its write at L2 or L6. $O$ is *pending* while `state[own(O)]` holds a pending descriptor with phase $ph(O)$.

**Lemma 1 (descriptors).** (a) `state[p]` changes from a pending descriptor of $O$ to a descriptor that is not pending exactly once, and no step makes it pending again, except the next publication of $p$. (b) The phase in `state[p]` changes only at a publication of $p$. (c) The owner of $O$ returns only after $O$ is not pending.

*Proof sketch.* (a) and (b): the only steps that write `state[p]` are the publication of $p$ and the CASes at L32, D8, D14 and D21. Each CAS copies the phase of the descriptor it replaces. The CASes at L32, D8 and D21 install a descriptor that is not pending, and D14 replaces a pending descriptor by a pending one. A CAS succeeds only on the exact descriptor it read, so a CAS based on a descriptor of an older operation fails after a new publication. (c) The owner calls HELP($ph(O)$) after $t_O$. When the loop reaches index $\mathrm{own}(O)$, it reads a descriptor of $O$ that is pending with phase $ph(O) \le ph(O)$, unless $O$ is already done, and it calls HELPENQ or HELPDEQ, whose loop runs while $O$ is pending. ∎

**Lemma 2 (list).** The invariants (Q1) to (Q3) of the Michael-Scott queue hold, and (K1) to (K3) of the page hold.

*Proof sketch.* `Head`, `Tail` and `next` fields change only by the CASes at L23, L33 and D22, which are the CASes of the Michael-Scott queue. L33 moves `Tail` only from `last` to `last.next`. D22 moves `Head` from `first` to its successor, and only if `first` $\ne$ `Tail` when the iteration began (D4), so `Head` never passes `Tail`. (K1): L23 links the node of a descriptor that was pending at L22. Assume that node $x$ is linked a second time. Between the two links, `Tail` must have moved past $x$ (a CAS at L23 needs `last.next` = NULL, and $x$ is not last once a later node is linked). The step L33 that moved `Tail` past $x$ came after L32 or after a check that the descriptor no longer holds $x$ as pending, so the second helper read a descriptor that is not pending at L22, or its CAS at L23 read the descriptor after the change, which contradicts the check. (K2) and (K3) hold because the descriptor is marked done (L32, D21) before `Tail` or `Head` moves past the node (L33, D22). ∎

**Theorem 1 (linearizability).** Each history of the queue is linearizable.

*Proof sketch.* Choose these linearization points:

- an enqueue: the successful CAS at L23 that links its node;
- a dequeue that returns an item: the successful CAS at D15 that writes its id into `first.deqTid`;
- a dequeue that returns EMPTY: the read of `first.next` at D2 in the iteration whose CAS at D8 succeeds.

By (K1) each enqueue has at most one point, and by the CAS at D15 each dummy is claimed by at most one dequeue. Each point lies after the publication of the operation (helpers act only after they read a pending descriptor) and, by Lemma 1(c), before its return. The order of enqueue points is the order of the nodes in the list. A dequeue point at D15 claims the current dummy `first`, which is `Head` at that time: the dummy is claimed before `Head` moves (D22 follows D21), and `first.next` is not NULL since `first` $\ne$ `Tail`. So the dequeues take the nodes after the dummies in list order, which gives FIFO results; the owner returns `d.node.next.value` at L11, the value of the node after the dummy it claimed. For EMPTY, `Head` = `first` at the read at D2, since `Head` was `first` just before (D2) and just after (D3) and moves only forward, and `first.next` = NULL, so the list has no item at that point. ∎

**Lemma 3 (helping by later operations).** Let $O$ be a published operation, and let $O'$ be an operation of another process whose MAXPHASE reads `state[own(O)]` after $t_O$. Then $O'$ does not return while $O$ is pending.

*Proof.* By Lemma 1(b), that read returns phase $ph(O)$, so $ph(O') \ge ph(O) + 1$. The HELP scan of $O'$ reads `state[own(O)]` later still. If $O$ is pending then, HELP of $O'$ calls HELPENQ or HELPDEQ for it, and that loop ends only when $O$ is no longer pending (or by the break at D12, which also tests that). ∎

**Lemma 4 (few operations take effect).** While a published operation $X$ is pending, each process other than $\mathrm{own}(X)$ has at most two operations whose linearization points fall in this time, and $\mathrm{own}(X)$ has only $X$. So at most $2(n-1) + 1 = 2n - 1$ points fall in it.

*Proof.* Let $q \ne \mathrm{own}(X)$. A linearization point of an operation of $q$ lies in its interval. At time $t_X$, $q$ has at most one operation in progress. Every later operation of $q$ runs MAXPHASE after $t_X$, so by Lemma 3 it does not return while $X$ is pending, and $q$ cannot start a third one. ∎

**Theorem 2 (wait-freedom, outline).** Each operation of a process that keeps taking steps returns within $B(n) = 2n + 12 + 20n(6n + 2)$ of its own steps.

*Proof sketch.* Count the steps of an operation $O$. MAXPHASE, the allocation and the publication take $n + 2$ steps, the $n$ reads at L13 take $n$ steps, and the final HELPFINISHENQ or HELPFINISHDEQ with L9 to L11 takes at most $10$ steps. The rest is at most $n$ calls of HELPENQ or HELPDEQ, one for each index. We show that each such call does at most $6n + 2$ iterations, and each iteration takes at most $20$ steps (the longest path, through D15 and HELPFINISHDEQ, takes 16).

Consider one call for an entry that holds operation $X$, which was pending when the call began. Every iteration but the last one starts while $X$ is pending. By Lemma 4, while $X$ is pending at most $2n - 1$ enqueues and $2n - 1$ dequeues take effect. So at most $2n - 1$ nodes are linked, `Tail` moves at most $2n$ times (it may lag by one at the start), and `Head` moves at most $2n - 1$ times. The descriptor of $X$ changes at most $H + 2$ times, where $H$ is the number of `Head` moves: D14 changes it only to the current `Head`, and only if it held another node, and L32, D8 or D21 change it once to done.

Now look at an iteration that does not end the loop.

- In HELPENQ, it fails because `Tail` changed (L20), or `Tail` lagged and L25 moved it, or the CAS at L23 failed because another node was linked. Each case contains a `Tail` move or a link in the iteration. So there are at most $2n + (2n - 1) + 1 \le 6n + 2$ iterations.
- In HELPDEQ, it fails because `Head` changed (D3), or `Tail` lagged and D9 moved it, or the CAS at D8 or D14 failed or was skipped because `Tail` or the descriptor changed, or it ran D15 and HELPFINISHDEQ, after which `Head` is no longer `first`. Each case contains a `Head` move, a `Tail` move or a change of the descriptor of $X$ in the iteration. So there are at most $(2n - 1) + 2n + (2n + 1) + 1 \le 6n + 2$ iterations.

The iterations of one call are disjoint in time, so each change is counted once. Summing, $O$ takes at most $n + 2 + n + 20n(6n + 2) + 10 = B(n)$ steps. ∎

The constants are loose: the tests in the implementation find at most 48 steps for $n = 2$, where $B(2) = 576$. The order $O(n^2)$ is what the argument gives; we do not claim that it is tight.
