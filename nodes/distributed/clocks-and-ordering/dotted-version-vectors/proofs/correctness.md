---
title: Dotted version vectors keep exactly the concurrent writes
proves: [correctness]
status: full
---

We use the model of the page: a set of servers with identifiers, any number of clients, one key, asynchronous message passing and no failures during the run. A run is a sequence of GET at a server, PUT at a server with the context of the client's last GET (or the empty context), and SYNC between two servers. For an identifier $i$, let $I_i = \{(i, 1), (i, 2), \ldots\}$. A set $K$ of events is a *downset* if $K \cap I_i$ is a prefix $\{(i,1), \ldots, (i,c)\}$ for each $i$.

**Ground truth.** Each PUT creates a new event $u$. Its true causal history is $H(u) = \{u\} \cup R$, where $R$ is the union of the true histories of the siblings that the client read in its last GET ($R = \emptyset$ with no GET). A sibling set is correct if it holds exactly the maximal events, under inclusion of true histories, among the events written to the server or received by SYNC.

**Lemma 1 (order).** Let $X$ and $Y$ be in normal form, that is, a dot $(i, n)$ always has $n > vv[i] + 1$. Then lines L1 to L3 return true if and only if $C[X] \subseteq C[Y]$.

*Proof.* For each $i$, $C[Y] \cap I_i = \{(i,1), \ldots, (i, vv_Y[i])\}$, plus $(i, n_Y)$ if $Y$ has a dot at $i$, and then $n_Y > vv_Y[i] + 1$. The prefix $\{(i,1), \ldots, (i,m)\}$ of $X$ is inside this set if and only if $m \le vv_Y[i]$: if $m > vv_Y[i]$, the event $(i, vv_Y[i] + 1)$ is in the prefix, and it is not in $C[Y]$ because it is not the dot $n_Y > vv_Y[i] + 1$. This is the test of line L1 (its second clause never holds in normal form). The dot of $X$ is in $C[Y]$ if and only if it is in the prefix of $Y$ or equals the dot of $Y$, which is the test of line L2. These two tests cover all of $C[X]$. $\square$

For a server $r$ with sibling set $S_r$, let $K_r = \bigcup_{x \in S_r} C[x]$.

**Lemma 2 (invariants).** At every point of the run, for every server $r$:

1. (Exact clocks.) Each sibling $x$ in $S_r$, written by event $u$, has $C[x] = H(u)$.
2. (Downset.) $K_r$ is a downset.
3. (Own events.) $K_r$ contains every event created by a PUT at $r$, and $K_r \cap I_r$ holds no other event.
4. (Correct siblings.) $S_r$ is correct, and the events of $S_r$ are pairwise incomparable.

*Proof.* By induction over the run. At the start all sets are empty. Assume the claims before a step.

*GET at $r'$.* Line L5 returns, for each $i$, the largest counter $c_i$ of $i$ in a clock of $S_{r'}$. By claim 2, $K_{r'} \cap I_i = \{(i,1), \ldots, (i,c_i)\}$. So the events covered by the context are exactly $K_{r'}$, and by claim 1 this is the union $R$ of the true histories of the siblings read. Nothing changes at the servers.

*PUT at $r$ with context $ctx$.* By the GET case, the events covered by $ctx$ are $R$, a downset of an earlier point. Line L6 sets $n = c + 1$, where $c$ is the largest counter of $r$ in $S_r$. By claims 2 and 3, $c$ is the number of PUTs done at $r$ so far, so $u = (r, n)$ is a new event, in no history yet. Line L7 builds the clock with vector $ctx$ and dot $(r, n)$, so $C[u] = R \cup \{(r, n)\} = H(u)$. Normal form does not change $C$. This gives claim 1 for the new sibling.

Since $u$ is in no other history, no old sibling dominates the new clock, and line L9 keeps it. Line L9 drops exactly the old siblings whose history is strictly inside $H(u)$. The old siblings were pairwise incomparable and maximal, so the new set is the set of maximal events of the old set plus $u$, which gives claim 4. The new $K_r$ is $K_r \cup R \cup \{(r,n)\}$, since the dropped histories lie inside $H(u)$. All events of $R$ with identifier $r$ were created at $r$, so by claim 3 they are already in $K_r$. Hence $K_r \cup R$ is a union of two downsets, which is a downset, and its part in $I_r$ is $\{(r,1), \ldots, (r,c)\}$. Adding $(r, c+1)$ keeps a prefix, which gives claims 2 and 3. Other servers do not change.

*SYNC of $a$ and $b$.* Line L4 keeps an element of $S_a$ unless an element of $S_b$ strictly dominates it, and the same for $S_b$. Inside each set no element strictly dominates another, by claim 4. Two equal clocks have equal histories, and by claim 1 and the fresh dots they belong to the same event, so the set union stores them once. So the result is the set of maximal events of $S_a \cup S_b$, which is correct. Each dropped history lies inside a kept one, so the new $K$ is $K_a \cup K_b$, a union of downsets. Claim 3 holds for $a$ and for $b$ because both sets only grow. $\blacksquare$

**Theorem.** At every point of the run, the siblings at each server are exactly the maximal writes that the server knows of. So DVV loses no update (a write is dropped only when a kept write has it in its true history), and reports no false conflict (two siblings are never in each other's true history).

*Proof.* This is claim 4 of Lemma 2, with Lemma 1 for the comparisons and claim 1 for the histories that they compare. $\blacksquare$
