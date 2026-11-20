---
title: The iterative cancellation decoder of coded slotted ALOHA resolves exactly the users outside the largest stopping set, in any order, in linear time
proves: [correctness]
status: full
---

The notation is that of the page. A frame is a bipartite graph between the users $u = 1, \ldots, K$ and the slots $s = 1, \ldots, M$, with an edge for each copy, $E$ edges in all; user $u$ has its copies in the set $N(u)$ of distinct slots. The channel is the collision channel with perfect cancellation: a slot whose copies all belong to known users, except one, gives the packet of that one user after the known copies are subtracted, and a slot with two or more unknown copies gives nothing. During the run, $D$ is the set of resolved users (line L9), and the **residual** of a slot $s$ is $r(s) = \{u \notin D : s \in N(u)\}$, the users of $s$ whose copy has not been cancelled. Lines L10 and L11 keep the stored set of slot $s$ equal to $r(s)$.

A **stopping set** is a set $S$ of users such that every slot used by a user of $S$ holds at least two users of $S$. The empty set is a stopping set, and the union of two stopping sets is a stopping set, because each slot of a user in $S_1 \cup S_2$ holds two users of $S_1$ or two users of $S_2$. So there is a unique largest stopping set $S^*$, the union of all of them.

**Lemma 1 (soundness).** Every user added to $D$ at line L9 is decoded correctly under the channel model.

*Proof.* User $u$ is added when a slot $s$ has $r(s) = \{u\}$ (lines L7 and L8). Every other copy in $s$ belongs to a user already in $D$, whose packet is known, so it can be rebuilt and subtracted. What remains is the copy of $u$ alone. $\square$

**Lemma 2 (queue invariant).** At each test of line L5, every slot $s$ with $|r(s)| = 1$ is in the queue.

*Proof.* It holds after line L4. Residuals only shrink, at line L11. A slot whose residual drops to size 1 is pushed at line L13. A slot that is popped at line L6 with $|r(s)| = 1$ has its only user $u$ resolved, and $s \in N(u)$, so line L11 empties $r(s)$ in the same pass. A slot popped with $|r(s)| \ne 1$ is not of size 1 at that moment, and it can reach size 1 later only through line L13, which pushes it again. $\square$

**Lemma 3 (termination and cost).** The loop runs at most $M$ times, each user is resolved at most once, and the total work is $O(K + M + E)$.

*Proof.* The size of a residual only decreases, so it becomes equal to 1 at most once; a slot enters the queue at line L4 if it starts at size 1, or at line L13 when it drops to size 1, and not both. So there are at most $M$ pushes and $M$ pops. Once $u$ is resolved, it leaves the residual of each of its slots (line L11), so it can never again be the only member of a residual, and it is resolved once. Line L3 does $E$ insertions. Lines L10 to L13 run once per edge of a resolved user, so at most $E$ times in total. Each set operation is $O(1)$ expected with hashing, or $O(1)$ worst case with counters and a sum of user identifiers per slot, which recovers the last user of a slot as the sum. $\square$

**Theorem.** When the decoder stops, the set of unresolved users is $U \setminus D = S^*$, the largest stopping set. In particular the resolved set does not depend on the order in which line L6 takes the slots from the queue.

*Proof.* Let $F = U \setminus D$ at the end.

First, $F$ is a stopping set. The queue is empty at the end, so by Lemma 2 no slot has a residual of size 1. Take $u \in F$ and a slot $s \in N(u)$. User $u$ is not in $D$, so $u \in r(s)$, and $|r(s)| \ge 1$, hence $|r(s)| \ge 2$. Every user of $r(s)$ is unresolved, so it lies in $F$. So $s$ holds at least two users of $F$.

Second, every stopping set $S$ lies inside $F$. Suppose not, and let $u$ be the first user of $S$ that line L9 resolves. At that moment some slot $s \in N(u)$ has $r(s) = \{u\}$. Since $S$ is a stopping set, $s$ holds another user $v \in S$ with $v \ne u$. User $v$ is not yet resolved, because $u$ is the first of $S$, so $v \in r(s)$. This contradicts $r(s) = \{u\}$.

So $F$ is a stopping set that contains every stopping set, which is $S^*$. The set $S^*$ depends only on the graph, so the result does not depend on the queue order. $\square$

**Remark (no decoder does better in the model).** In the collision channel, a user of $S^*$ has no slot that is clean even after every user outside $S^*$ is cancelled, because each of its slots holds a second unknown copy from $S^*$. A slot with two unknown copies gives nothing in this model, so no receiver, however complex, can recover any user of $S^*$. The decoder therefore resolves every user that the model allows. A receiver that can decode two overlapping packets (capture, or multiuser detection in a slot) works in a different model.

**What is not proved here.** The asymptotic threshold of a degree distribution comes from density evolution (Paolini, Liva and Chiani 2015, Corollary 3.1), which tracks the probability that an edge is still unresolved when $K$ and $M$ grow with $K/M = G$ fixed and the graph is locally a tree. The tests check the recursion against the published thresholds; this file proves only the finite-frame statements above.
