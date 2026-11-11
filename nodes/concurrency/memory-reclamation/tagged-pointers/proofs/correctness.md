---
title: Correctness of the tagged Treiber stack
proves: [correctness]
status: full
---

We prove that the Treiber stack with a tagged root is linearizable when no pop sees $2^w$ or more changes of the root between its L1 and its L5. We also show that the bound on the number of changes cannot be dropped.

**Model.** Processes run asynchronously on a sequentially consistent memory. The root $X$ is one double-width word $(top, tag)$ with $tag \in \{0, \ldots, 2^w - 1\}$. It is read in one step (L1) and changed only by a successful DWCAS, which writes the pointer it was given and $(tag + 1) \bmod 2^w$. Nodes come from a type-stable pool: a node that was recycled at L6 can be read without a fault, and only a push writes the $next$ field of a node, after it got the node from the pool and before its DWCAS. A push loops: read $(p, c)$ from $X$, set $node.next = p$, DWCAS $X$ from $(p, c)$ to $(node, c + 1)$. A pop is the template L1 to L6 with NEW-POINTER reading $p.next$ and $p.val$.

**Invariant I.** The chain $X.top, X.top.next, \ldots$ ends at nil, its nodes are pairwise distinct, none of them is in the pool, and the $next$ field of a node in the chain does not change while the node stays in the chain.

*Proof.* At the start the chain is the initial stack and the pool is empty. Only a successful DWCAS changes $X$. A push DWCAS puts in front a node that the push took from the pool, so it was in no chain and is distinct from all chain nodes; its $next$ is the old top, by the DWCAS check. A pop DWCAS replaces the top by a value $q$; we show in Lemma 2 that $q = top.next$ at that time, so the chain loses its first node and nothing else. Nodes go to the pool only at L6, after their pop DWCAS removed them from the chain, and the chain is a list with distinct nodes, so the node is no longer in the chain. Last, only a push writes $next$, and only on a node it took from the pool, which is not in the chain. $\square$

**Lemma 1 (tag counting).** Let $X = (p, c)$ at time $t_1$ and $X = (p', c')$ at a later time $t_2$, and let $k$ be the number of successful DWCAS steps on $X$ between them. Then $c' = (c + k) \bmod 2^w$. In particular, if $0 < k < 2^w$, then $c' \ne c$.

*Proof.* Each successful DWCAS adds one modulo $2^w$, and nothing else writes $X$. For $0 < k < 2^w$, $k$ is not a multiple of $2^w$. $\square$

**Lemma 2 (a successful pop DWCAS sees no change).** Let a pop read $(p, c)$ at L1 at time $t_1$ and succeed at L5 at time $t_5$, and suppose fewer than $2^w$ successful DWCAS steps on $X$ happened between $t_1$ and $t_5$. Then none happened, and $q = p.next$ at time $t_5$, where $q$ is the value the pop read at L3.

*Proof.* The DWCAS at $t_5$ succeeds, so $X = (p, c)$ just before it. By Lemma 1 with $k < 2^w$, $k = 0$: $X$ held $(p, c)$ during the whole interval. So $p$ was the top during the whole interval, and by Invariant I its $next$ field did not change in that time. The read at L3 is in the interval, so it returned the value of $p.next$ at $t_5$. $\square$

**Theorem 1 (linearizability).** If every pop sees fewer than $2^w$ successful updates of $X$ between its L1 and its L5, the stack is linearizable, with each operation linearized at its successful DWCAS, and an empty pop at its L1.

*Proof.* By Invariant I and Lemma 2, every successful DWCAS changes the chain exactly as the sequential push or pop would at that moment. A pop returns the value it read at L3 from $p$, and $p.val$ is written only by the push that put $p$ in the chain, before that push's DWCAS; $p$ stays in the chain over the interval of Lemma 2, so the value is the value at the top at $t_5$. A pop that reads nil at L1 sees an empty chain at that time. A failed DWCAS changes nothing. So the sequence of DWCAS steps, in time order, is a legal sequential history, and each linearization point is inside its operation. $\square$

**Theorem 2 (stale reads are harmless).** A read at L3 of a node that is in the pool returns some value but never affects the result.

*Proof.* If $p$ is in the pool at L3, then $p$ was removed from the chain after $t_1$ by a successful DWCAS, so at least one update happened after $t_1$. Under the hypothesis of Theorem 1, Lemma 2 says that a successful L5 sees no update, so this L5 fails and the values read at L3 are dropped. The type-stable pool makes the read itself safe. $\square$

**Theorem 3 (the bound is needed).** For every $w \ge 1$ there is a schedule with exactly $2^w$ updates between L1 and L5 of one pop in which the stack loses a value.

*Proof.* Start with the chain $A \to B$ and $X = (A, 0)$, and a LIFO pool. Process $p$ runs L1 and L3 of a pop: it reads $(A, 0)$ and $q = B$. Process $r$ then runs $2^{w-1}$ rounds of a pop followed by a push of a new value. Each pop removes the top node, which is $A$ in every round, and recycles it; the next push takes $A$ from the pool, so after each round the chain is $A \to B$ again. That is $2^w$ updates, so $X = (A, 2^w \bmod 2^w) = (A, 0)$. Now $p$'s DWCAS succeeds and writes $(B, 1)$. The value pushed by $r$ in the last round is in $A$, which is no longer in the chain and was never returned by a pop. So a value is lost. $\square$

The test file checks Theorem 1 by running every interleaving of small runs with 16-bit tags, and Theorem 3 for $w = 1$ (one round) and $w = 2$ (two rounds), where $w = 2$ and $w = 3$ fix the two runs. The Michael and Scott queue has the same argument for each of its three kinds of tagged words (head, tail and the $next$ field of a node), with the extra rule that the tag of a $next$ field keeps counting when the node is recycled; the test file checks the queue in the same way. $\blacksquare$
