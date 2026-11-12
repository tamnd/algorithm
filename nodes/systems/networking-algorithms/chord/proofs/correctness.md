---
title: Chord lookups are correct and take at most m hops, and a join or a failure is repaired by stabilization
proves: [correctness]
status: full
---

We use the notation of the page. Identifiers are integers mod $2^m$. For identifiers $a, b$, let $\mathrm{dist}(a, b) = (b - a) \bmod 2^m$, the clockwise distance. $\mathrm{between}(a, b, c)$ is true when $0 < \mathrm{dist}(a, b) < \mathrm{dist}(a, c)$, or when $a = c$ and $b \ne a$. For the set $L$ of live nodes, $\mathrm{succ}_L(k)$ is the first node of $L$ at or after $k$ clockwise, and $\mathrm{next}(n)$ is the first node of $L$ after $n$. A node $v$ has a predecessor $v.\mathit{prdc}$, a successor list $v.\mathit{succ}$ of length at most $r$, and fingers $v.\mathit{finger}[0 .. m-1]$.

**Ideal state (Zave).** Every live node $v$ has $v.\mathit{succ}$ equal to the next $\min(r, |L| - 1)$ live nodes after $v$ in clockwise order, and $v.\mathit{prdc}$ equal to the last live node before $v$.

Line numbers refer to the pseudocode on the page. The arc $(a, c)$ is the set of $b$ with $\mathrm{between}(a, b, c)$, and $(a, c] = (a, c) \cup \{c\}$.

## 1. Lookups are correct

**Claim 1.** Suppose that for every live node $v$, the first live entry of $v.\mathit{succ}$ is $\mathrm{next}(v)$ (this holds in the ideal state). Then FIND-SUCCESSOR$(n_0, k)$ from any live $n_0$ ends, and returns $\mathrm{succ}_L(k)$.

*Proof.* Let $s = \mathrm{next}(n)$ be the first live entry of the current node $n$ (lines L2 and L5). If $k \in (n, s]$ (the test of line L3), then no live node lies in $(n, s)$, so the first live node at or after $k$ is $s$, and line L6 returns $s$. Otherwise $k \notin (n, s]$, and $s \in (n, k)$: if $k = n$, the arc $(n, n)$ is the whole ring without $n$, and $s \ne n$; if $k \ne n$, then $\mathrm{dist}(n, k) > \mathrm{dist}(n, s) \ge 1$. Lines L7 to L10 return the live node $c$ of $n.\mathit{finger} \cup n.\mathit{succ}$ in $(n, k)$ that is closest to $k$: line L9 replaces $c$ only by a live node of $(c, k)$, and $s$ is one of the candidates, so the result is in $(n, k)$. For the potential, let $D(n) = \mathrm{dist}(n, k)$ if $n \ne k$ and $D(k) = 2^m$. Since $c \in (n, k)$, we have $c \ne k$ and $D(c) = D(n) - \mathrm{dist}(n, c) \le D(n) - 1$. So $D$ is a positive integer at most $2^m$ that falls by at least 1 at each hop, and the loop of line L3 ends after at most $2^m$ hops. Every node it visits is live, because line L9 only picks live nodes. $\square$

Fingers only change the speed: Claim 1 holds for any fingers, even stale ones that point to failed nodes, because line L9 skips dead nodes and the successor is always a candidate.

## 2. With correct fingers, a lookup takes at most $m$ hops

**Claim 2.** If in addition $v.\mathit{finger}[i] = \mathrm{succ}_L(v + 2^i)$ for every live $v$ and every $i$, then each hop more than halves the distance from the current node to $p$, the last live node before $k$, and a lookup takes at most $m$ hops.

*Proof.* Let $\delta = \mathrm{dist}(n, p)$. If $\delta = 0$, then $n = p$ and $k \in (n, \mathrm{next}(n)]$, so the lookup stops at line L3. Otherwise $\delta \ge 1$; let $j$ be the largest index with $2^j \le \delta$, so $\delta < 2^{j+1}$. The live node $p$ lies at or after $n + 2^j$, so $f = \mathrm{succ}_L(n + 2^j)$ satisfies $2^j \le \mathrm{dist}(n, f) \le \delta$, and $f$ is inside the arc from $n$ to $k$. Line L4 picks a node $c$ at least as close to $k$ as $f$, and $c$ is not after $p$ because no live node lies strictly between $p$ and $k$. So $\mathrm{dist}(n, c) \ge 2^j > \delta / 2$, and the new distance $\mathrm{dist}(c, p) = \delta - \mathrm{dist}(n, c) < \delta / 2$. Since $\delta < 2^m$ at the start and is an integer, after at most $m$ hops it is 0, and the lookup stops. $\square$

Stoica et al. (2001, Theorem 2) also show that with $n$ nodes with random identifiers, the number of hops is $O(\log n)$ with high probability: after $\log_2 n$ halvings the remaining arc has length less than $2^m / n$, and such an arc holds $O(\log n)$ nodes with high probability.

## 3. Stabilization repairs one join

**Claim 3.** Start from an ideal ring with live set $L$, $|L| \ge r + 1$. A new node $x$ joins: it finds the last node $p$ of $L$ before $x$, sets $x.\mathit{succ} = p.\mathit{succ}$ and $x.\mathit{prdc} = p$. Then every live node runs stabilize once per round, in any order. After at most $r + 1$ rounds the ring is ideal for $L \cup \{x\}$.

*Proof.* Let $s = \mathrm{next}(p)$ in $L$; then $x$ lies strictly between $p$ and $s$. Number the nodes before $x$ as $q_1 = p, q_2, \ldots$ (so $q_{t+1}$ is the node before $q_t$). In the ideal state for $L \cup \{x\}$, the list of a node $v$ changes only if $x$ is among the next $r$ nodes of $v$, that is, only for $q_1, \ldots, q_r$ (and $x$ itself). We show four facts.

(a) A stabilize step of a node $v$ whose successor's list is already ideal, and whose successor's $\mathit{prdc}$ is not strictly between $v$ and the successor, sets $v.\mathit{succ} = [\mathrm{head}] + $ (the first $r - 1$ entries of the head's list), which is the ideal list of $v$. This is the code of stabilize.

(b) Nodes other than $q_1, \ldots, q_r$ and $x$ stay ideal. For such a node $v$, by induction over the steps, the head is $\mathrm{next}(v)$, its list is ideal, and its $\mathit{prdc}$ is $v$ or $x$; $x$ is strictly between $v$ and its head only if $v = p$. So by (a) $v$ keeps its ideal list. Rectify at a node $u$ changes $u.\mathit{prdc}$ only if the notifier is strictly between $u.\mathit{prdc}$ and $u$; in this run the only new candidate is $x$, at $u = s$, which is the right change.

(c) In round 1, $x$ stabilizes: its head is $s$, and $s.\mathit{prdc}$ is $p$ or $x$, not strictly between $x$ and $s$. So $x$ gets the list $[s] + $ (the first $r-1$ entries of $s$'s list), which is ideal by (b). Then $x$ notifies $s$, and since $x$ is strictly between $p$ and $s$, $s.\mathit{prdc}$ becomes $x$. From now on $x$ and $s$ are ideal.

(d) Once $s.\mathit{prdc} = x$ and $x$ is ideal, the next stabilize of $p$ sees $\mathrm{between}(p, x, s)$ and sets $p.\mathit{succ} = [x] + $ (the first $r - 1$ entries of $x$'s list), which is ideal; it notifies $x$, whose $\mathit{prdc}$ is already $p$. So $p = q_1$ is ideal by the end of round 2. If $q_t$ is ideal at the end of round $t + 1$, then in round $t + 2$ the node $q_{t+1}$ runs stabilize with an ideal head and by (a) becomes ideal. So $q_t$ is ideal by the end of round $t + 1$, and all of $q_1, \ldots, q_r$ by the end of round $r + 1$. $\square$

## 4. Stabilization repairs one failure

**Claim 4.** Let $r \ge 2$. Start from an ideal ring with $|L| \ge r + 2$, and let one node $f$ fail. Run stabilize rounds as above. After at most $r$ rounds the ring is ideal for $L \setminus \{f\}$.

*Proof.* Let $q_1$ be the node before $f$, and $q_2, \ldots$ the nodes before it, and let $s = \mathrm{next}(f)$. The ideal list changes only for $q_1, \ldots, q_r$, whose lists contain $f$, and the ideal $\mathit{prdc}$ changes only for $s$. When $q_1$ stabilizes, its head $f$ is dead, so it drops it. Its list was $[f, s, \ldots]$, because $r \ge 2$ and $|L| \ge r + 2$, so its new head is the live node $s$. (With $r = 1$ the list would become empty, which is why the successor list must be long enough for the failures that can happen between two rounds.) The node $s$ has $s.\mathit{prdc} = f$, which is dead, so $q_1$ gets the list $[s] + $ (the first $r - 1$ entries of $s$'s list), which is ideal because $s$ is unaffected, and its notification sets $s.\mathit{prdc} = q_1$. So $q_1$ and $s$ are ideal after round 1. The same chain argument as in (d) makes $q_t$ ideal by the end of round $t$, and nodes not in $q_1, \ldots, q_r$ stay ideal by (a). $\square$

## Scope

Claims 3 and 4 cover one change at a time. Zave (2017) proves the general case, with any interleaving of joins, failures and stabilize steps, for the protocol that this page uses. Her inductive invariant has two parts: every successor list has a live entry, and at least $r + 1$ nodes are *principal*, that is, no extended successor list (a node followed by its list) skips them. An ideal ring of $r + 1$ nodes satisfies it. From any state that satisfies the invariant, once the joins and failures stop, the ring becomes ideal and stays ideal. The original protocol of Stoica et al. does not have this property. With the Alloy Analyzer, Zave (2012) showed that under its own operating assumptions it does not always reach a ring again, and that none of the seven properties that Liben-Nowell, Balakrishnan and Karger (2002) list as invariants is an invariant. Her bad runs include rings that break, rings that become disordered, and a network that splits into two rings. Zave (2017) also shows that the original start from a single node is not safe: a successor list can then hold the same node twice, and one failure can cut a node off.
