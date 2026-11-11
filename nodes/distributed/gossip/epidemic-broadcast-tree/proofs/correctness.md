---
title: Plumtree builds a spanning tree with its first broadcast, sends n - 1 payloads on the tree, and delivers to every node of a connected live overlay
proves: [correctness]
status: full
---

**Setting.** The overlay is a connected undirected graph $G$ with $n$ nodes and $m$ links, and every node starts with all its neighbors in the eager set. Links are reliable and keep each message; a link that fails drops everything sent on it and both ends get NeighborDown (line L8) before the broadcast that we look at. Each node handles one event at a time. "Live overlay" means $G$ without the failed links. A node $v$ receives its *first copy* of a message $M$ from its *parent* $\pi(v)$: the sender of the first GOSSIP for $M$ that $v$ handles. Lines L1 to L8 are those of the page.

**Lemma 1 (the sets).** At all times, the eager and lazy sets of a node are disjoint and together hold exactly its live neighbors.

*Proof.* At the start, the eager set is all neighbors and the lazy set is empty. Lines L2, L3, L4, L6 and L7 move a neighbor from one set to the other, and line L8 removes a failed neighbor from both. Nothing else changes the sets. $\square$

**Theorem 1 (the first broadcast builds a tree).** Let there be no failures, let all links be eager at both ends, and let node $s$ broadcast $M$. Then every node delivers $M$, no IHAVE or GRAFT is sent, and when no message is in transit:

1. A link $\{u, v\}$ is eager at both ends if $u = \pi(v)$ or $v = \pi(u)$, and lazy at both ends otherwise.
2. The eager links form a spanning tree $T$, with the parent links as edges.
3. Exactly $2m - (n - 1)$ GOSSIP messages and $2(m - n + 1)$ PRUNE messages are sent.
4. If every message takes exactly one step, $v$ delivers $M$ at step $d_G(s, v)$, so $T$ is a shortest path tree from $s$ and LDH is the eccentricity of $s$.

*Proof.* *No IHAVE.* A node sends IHAVE only to lazy peers, at line L1 or L2, when it first gets $M$. Before $v$ first gets $M$, its lazy set is empty: a peer $w$ enters it only at line L3 (on a duplicate from $w$, so $v$ already has $M$) or at line L4 (on a PRUNE from $w$, which $w$ sends only after a duplicate from $v$, so again $v$ already has $M$). Without IHAVE there are no timers and no GRAFT.

*Delivery.* Each node that gets $M$ sends GOSSIP to all neighbors except its parent. By induction along a path from $s$ in the connected graph $G$, every node gets $M$.

*Parent links.* Let $u = \pi(v)$. Then $v$ never sends GOSSIP to $u$ (line L2 skips the parent), so $u$ never gets a duplicate from $v$ and never moves $v$ to lazy. And $u$ never gets a PRUNE from $v$: $v$ sends PRUNE to $u$ only on a duplicate from $u$, and $u$ sends $M$ to $v$ only once. Node $v$ puts $u$ in its eager set at line L2. So the link is eager at both ends. It cannot also be that $v = \pi(u)$, because $u$ forwards only after its first copy, which then came before $v$'s first copy, and the other way round.

*Other links.* Let $\{u, v\}$ be a link with $u \ne \pi(v)$ and $v \ne \pi(u)$. Both nodes get $M$, and each sends GOSSIP to the other at line L2, since neither is the other's parent. When $v$ handles the copy from $u$, it is not the first copy (the first came from $\pi(v) \ne u$), so $v$ moves $u$ to lazy and sends PRUNE; the PRUNE makes $u$ move $v$ to lazy. The same holds with $u$ and $v$ swapped. No later event in this broadcast moves them back: only a first copy (from the parent) or a GRAFT moves a peer to eager.

*The tree.* Every node except $s$ has one parent, which got $M$ before it, so the parent links have no cycle and connect every node to $s$; with $n - 1$ links they form a spanning tree.

*Counts.* The source sends GOSSIP on all its $\deg(s)$ links, and every other node $v$ on its $\deg(v) - 1$ non-parent links, so the total is $\sum_v \deg(v) - (n - 1) = 2m - (n - 1)$. Each of the $m - (n - 1)$ links outside $T$ carries exactly two duplicates and so two PRUNE messages; parent links carry none.

*Unit delays.* By induction on $d$, a node at distance $d$ from $s$ first gets $M$ at step $d$: some neighbor at distance $d - 1$ sends at step $d - 1$, and no copy can arrive earlier, because a copy at step $t$ needs a path of $t$ links from $s$. So the parent of $v$ is at distance $d_G(s, v) - 1$, and the tree paths are shortest paths. $\square$

**Theorem 2 (broadcasts on the tree).** Suppose the eager links form a spanning tree $T$, eager at both ends, and all other live links are lazy at both ends. Let node $s$ broadcast $M$, and suppose no GRAFT is sent. Then every node gets exactly one GOSSIP, from its tree neighbor on the path to $s$, so there are $n - 1$ payloads and $\mathrm{RMR} = 0$; there are $2(m' - n + 1)$ IHAVE messages, where $m'$ is the number of live links; no PRUNE is sent; and the eager and lazy sets do not change.

In lock-step, with unit delays, no GRAFT is sent if $\text{timeout}_1 \ge d_T(s, v) - 1$ for every node $v$. This holds for every sender if $\text{timeout}_1 \ge 2h - 1$, where $h$ is the depth of $T$ from some node (for example from $s_0$), and it holds for the sender $s_0$ that built $T$ with any $\text{timeout}_1 \ge 1$.

*Proof.* GOSSIP goes only on eager links, that is on $T$. By induction along $T$ from $s$, a node $v$ gets its first GOSSIP from its tree neighbor $w$ toward $s$ and forwards it on its other tree links; $w$ is the only tree neighbor that sends to $v$, because a tree neighbor sends GOSSIP only after its own first copy, on its tree links other than its sender, and the tree has no cycle. So each node gets exactly one GOSSIP, and with no duplicate, no PRUNE. Line L2 moves $w$ to eager, where it already is. IHAVE goes on every lazy link in both directions (neither end is the other's sender), which gives $2(m' - (n - 1))$ messages; an IHAVE changes no set (line L5). With no GRAFT, the sets do not change.

*The timer.* In lock-step, $v$ gets the GOSSIP at step $d_T(s, v)$. An IHAVE reaches $v$ at the earliest at step $a \ge 1$, and the timer it starts fires at step $a + \text{timeout}_1$, after the messages of that step are handled. So no GRAFT is sent if $d_T(s, v) \le a + \text{timeout}_1$, which holds when $\text{timeout}_1 \ge d_T(s, v) - 1$. For any $s$ and $v$, the tree path goes through their lowest common ancestor in $T$ rooted at that node, so $d_T(s, v) \le 2h$. For $s_0$, $T$ is a shortest path tree (Theorem 1), and an IHAVE from a neighbor $u$ arrives at step $d_G(s_0, u) + 1 \ge d_G(s_0, v) = d_T(s_0, v)$, so the GOSSIP is there no later than any IHAVE, and a timer started in the same step fires at least one step later. $\square$

**Theorem 3 (delivery with failures).** Let the live overlay be connected, let links be reliable, let every node keep each message it delivered so that it can answer GRAFT, and let the eager and lazy sets be any sets that satisfy Lemma 1. If node $s$ broadcasts $M$, every node delivers $M$ exactly once, and a finite number of messages is sent.

*Proof.* *At most once.* Line L2 delivers only a new message.

*Every node.* Let $R$ be the set of nodes that ever deliver $M$, and suppose that some node is not in $R$. The live overlay is connected, so there is a live link $\{u, w\}$ with $u \in R$ and $w \notin R$. When $u$ first got $M$ (line L1 or L2), $w$ was not its sender, since $w$ never has $M$, and $w$ was in the eager or the lazy set of $u$ (Lemma 1). If eager, $u$ sent GOSSIP to $w$ on a live, reliable link, so $w$ gets $M$, which is a contradiction. If lazy, $u$ sent IHAVE, and $w$, which never has $M$, records $(M, u)$ at line L5, with a timer for $M$ running or started. A record is removed only at line L6, when it is used, or at line L8, which does not happen for a live link. Each time the timer fires (line L6) and a record is left, $w$ takes one record $(M, x)$, sends GRAFT to $x$ and restarts the timer. The node $x$ sent IHAVE only after it delivered $M$, it keeps $M$, and its link to $w$ is live, so it answers with GOSSIP (line L7), and $w$ gets $M$. So the first record that $w$ uses already gives $w$ the message; since the record from $u$ stays until it is used, the timer fires with at least one record, which is again a contradiction. Hence $R$ is all nodes.

*Finitely many messages.* Each node sends GOSSIP or IHAVE to each neighbor at most once at its first copy. Each IHAVE gives at most one record and so at most one GRAFT, and each GRAFT at most one GOSSIP. Each GOSSIP gives at most one PRUNE. So at most $2m$ IHAVE or first-copy GOSSIP messages, $2m$ GRAFT, $2m$ GRAFT replies and $4m$ PRUNE messages are sent, and the timers stop when no records are left. $\square$

**What is not proved.** That the eager links form a tree again after a repair is checked by the tests on random overlays with 30 failed tree links, and the paper argues that duplicates prune the cycles that repairs create, but this file gives no proof. Message loss on live links, failures during a broadcast, NeighborUp, and the optimization of Algorithm 4 are not covered. The numbers of the paper's evaluation are cited, not proved.
