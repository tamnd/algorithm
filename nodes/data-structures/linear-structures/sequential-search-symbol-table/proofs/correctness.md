---
title: The sequential search symbol table returns the stored values and keeps its invariant
proves: [correctness, termination]
status: full
---

**Statement.** Let $T$ satisfy (I1) to (I3) for a map $M$ with $n = T.n$ keys. Then GET, PUT and DELETE stop, and:

- GET$(T, k)$ returns $M(k)$ if $k \in M$ and nil otherwise, and changes nothing;
- after PUT$(T, k, v)$, (I1) to (I3) hold for the map $M[k \mapsto v]$;
- after DELETE$(T, k)$, (I1) to (I3) hold for the map $M$ without $k$.

**Setup.** By (I1), the nodes from $T.first$ are $N_1, \ldots, N_n$ in order, with $N_n.next = nil$. Write $N_{n+1}$ for nil.

**Lemma (the scan).** In GET, each time line L2 tests its condition, $x = N_j$ for some $j$ with $1 \le j \le n + 1$, and no node among $N_1, \ldots, N_{j-1}$ has key $k$. The loop runs at most $n$ rounds.

*Proof.* Line L1 sets $x = T.first = N_1$, and the range of earlier nodes is empty. Assume the claim with $x = N_j$ and that the test $x \ne nil$ succeeds, so $j \le n$. If line L3 finds $N_j.key = k$, the procedure returns. Otherwise $N_j.key \ne k$, and line L4 sets $x = N_j.next = N_{j+1}$, so the claim holds for $j + 1$. The number $n + 1 - j \ge 0$ drops by exactly 1 per round, so there are at most $n$ rounds. $\square$

**GET.** If line L3 returns, it returns $N_j.value$ with $N_j.key = k$. By (I2) $N_j$ is the only node with key $k$, and by (I3) its value is $M(k)$. If the loop ends, $x = nil$, so $j = n + 1$, and by the lemma no node has key $k$; by (I3), $k \notin M$, and line L5 returns nil. GET writes no field.

**PUT.** Lines L6 to L9 are the scan of the lemma, with line L8 in place of line L3. If line L8 finds the node of $k$, it sets its value to $v$ and returns. The keys and the list do not change, so (I1) and (I2) hold, and the pairs are those of $M$ with the pair of $k$ replaced by $(k, v)$, which is (I3) for $M[k \mapsto v]$. Otherwise the scan ends with no node of key $k$, so $k \notin M$. Line L10 makes a node $N_0$ with key $k$, value $v$ and $N_0.next = N_1$ (or nil when $n = 0$), sets $T.first = N_0$ and $T.n = n + 1$. The list from $T.first$ is $N_0, N_1, \ldots, N_n$, which has $n + 1$ nodes and ends in nil (I1). The keys are distinct, because $k$ differs from every key of $N_1, \ldots, N_n$ (I2). The pairs are those of $M$ plus $(k, v)$, and this is $M[k \mapsto v]$ since $k \notin M$ (I3).

**DELETE.** Each time line D2 tests its condition, $x = N_j$ with $1 \le j \le n + 1$, $prev = N_{j-1}$ (nil for $j = 1$), and no node before $N_j$ has key $k$; this holds after line D1 and is kept by each round, which moves both pointers one node forward, and the rounds end after at most $n$ steps as in the lemma. If the loop ends with $x = nil$, then $k \notin M$, line D3 returns, and the map without $k$ is $M$. Otherwise $x = N_j$ is the only node with key $k$. If $j = 1$, line D4 sets $T.first = N_2$; else it sets $N_{j-1}.next = N_{j+1}$. In both cases the list from $T.first$ is $N_1, \ldots, N_{j-1}, N_{j+1}, \ldots, N_n$, and line D5 sets $T.n = n - 1$, which is its length (I1). Its keys are a subset of distinct keys (I2), and its pairs are those of $M$ without the pair of $k$ (I3). $\blacksquare$

**Compare counts.** In the scan, each round makes one compare of $k$ with a key. A hit at $N_i$ ends in round $i$, after $i$ compares; a miss makes $n$ rounds and $n$ compares. This gives the counts of the Complexity section.
