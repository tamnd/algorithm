---
title: Dynamo-style replicas converge, and strict quorums with R + W > N give fresh reads
proves: [correctness]
status: full
---

**Setting.** The algorithm of lines L1 to L10 runs in the asynchronous model with crash-recovery failures and partitions. A node keeps what it has stored across a crash. A version is a pair $(c, x)$ of a vector clock $c$ and a value $x$; clocks are maps from node names to natural numbers, with missing entries read as 0. Write $c \ge d$ if $c[i] \ge d[i]$ for every $i$, and say that version $u$ *descends from* version $u'$ if $c(u) \ge c(u')$. We assume that distinct versions of a key have distinct clocks. Line L3 gives this when the context of each put includes the coordinator's latest clock for the key; in general a coordinator can keep a counter per key that only grows.

For a finite set $S$ of versions, let $\max(S)$ be the set of $u \in S$ such that no $u' \in S$ has $c(u') \ge c(u)$ and $c(u') \ne c(u)$. Every operation that changes a node's versions for a key (the store of line L4, the repair of line L8, the handoff of line L10, and an anti-entropy exchange) replaces its set $S$ by $\max(S \cup S')$ for some set $S'$ of versions.

**Lemma 1 (the merge is a join).** On finite antichains of versions, the operation $S \sqcup S' = \max(S \cup S')$ is commutative, associative and idempotent. Moreover $\max(S_1 \sqcup S_2 \sqcup \dots \sqcup S_k) = \max(S_1 \cup \dots \cup S_k)$.

*Proof.* Commutativity and idempotence are immediate from the definition. For the last claim, it suffices to show $\max(\max(A) \cup B) = \max(A \cup B)$ for finite $A, B$. Every element of $A$ is below or equal to some element of $\max(A)$, because the order on clocks is a partial order on a finite set. So an element of $A \cup B$ is dominated in $A \cup B$ if and only if it is dominated in $\max(A) \cup B$, and the elements of $A$ removed by $\max(A)$ are dominated in both. Hence the two sets of maximal elements are equal. Associativity follows by applying this twice. $\square$

**Lemma 2 (versions only grow).** If node $x$ holds a version that descends from $u$ at some time, then at every later time $x$ holds a version that descends from $u$.

*Proof.* Let $v$ descend from $u$ and be held by $x$. A merge replaces the set $S \ni v$ by $\max(S \cup S')$. Either $v$ stays, or some $v'$ in the new set strictly dominates $v$, and then $c(v') \ge c(v) \ge c(u)$. The operations other than merges are the removals of line L10 at a stand-in, which affect only a node outside the preference list of the key. For a home node the claim follows by induction on the number of merges. $\square$

**Theorem (a), convergence.** Fix a key $k$ with preference list $P$. Suppose that after some time no puts of $k$ occur, every node is up, no partition remains, every pending hint has been handed off (line L10), and anti-entropy has run between every pair of nodes of $P$ until no exchange changes any set. Then every node of $P$ holds $\max(U)$, where $U$ is the set of versions of $k$ stored at line L4 by any node.

*Proof.* Each version $u \in U$ was stored at some node $y$. If $y \in P$, $u$ or a version above it stays at $y$ by Lemma 2. If $y \notin P$, $y$ is a stand-in and holds a hint for a home $z \in P$; the handoff of line L10 merges $y$'s versions into $z$, so $z$ holds $u$ or a version above it. So every $u \in U$ is below some version held at some home. When anti-entropy between two homes $z_1, z_2$ changes nothing, their sets $S_1, S_2$ satisfy $\max(S_1 \cup S_2) = S_1 = S_2$. Since this holds for every pair, all homes hold the same set $S$. Every element of $S$ is in $U$, since merges create no new versions, and every element of $U$ is below some element of $S$. An element of $S$ is maximal in $S$, and if some $u \in U$ strictly dominated it, then $u$ would be below some $s' \in S$, which would strictly dominate an element of $S$, a contradiction. So $S \subseteq \max(U)$. Conversely, each $u \in \max(U)$ is below some $s \in S \subseteq U$, and maximality forces $s = u$. Hence $S = \max(U)$. $\square$

By Lemma 1 the result does not depend on the order of the merges, the duplication of messages, or which repair path delivered a version. This is the convergence part of eventual consistency.

**Theorem (b), strict quorums.** Use strict quorums: the target set $T$ is the set of reachable nodes of $P$. Assume $R + W > N$ and that nodes keep their data. Let a put of $k$ store version $u$ and return success, and let a get of $k$ start after that. If the get returns, its result contains a version that descends from $u$.

*Proof.* The put returned success, so at line L5 $u$ was stored at a set $Q_w \subseteq P$ with $|Q_w| \ge W$. The get reads at line L6 the versions of a set $Q_r \subseteq P$ with $|Q_r| = R$. Both are subsets of $P$, which has $N$ elements, and $|Q_r| + |Q_w| > N$, so some node $z$ is in both. By Lemma 2, $z$ holds a version $v$ that descends from $u$ when it replies. Line L7 computes $\max$ of the union of the replies, which contains $v$, so the result contains $v$ or a version that strictly dominates $v$; both descend from $u$. $\square$

**Sloppy quorums break (b).** With sloppy quorums the sets $T$ of the put and of the get need not be subsets of $P$, and the intersection argument fails. The run on the page is a counterexample: five nodes, $N = 3$, $R = W = 2$, preference list B, A, C. During the partition {B, D, E} | {A, C} the put of "new" is stored at B, D and E and succeeds; the get on the other side reads A and C, whose sets contain only "old", so the result does not descend from the successful put. Theorem (a) still holds once the partition heals, because handoff carries "new" to A and C.

**Not linearizable.** Even with strict quorums, Theorem (b) gives only that each get sees each put that finished before it started. Two gets that overlap a put can return the new version and then the old one, because line L8 does not finish before line L9 returns. Concurrent puts produce siblings by design. So Dynamo-style replication is not a linearizable register, and it is not meant to be.
