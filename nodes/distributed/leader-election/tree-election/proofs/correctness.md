---
title: Saturation elects the largest identifier on a tree with exactly 3n + k − 4 messages
proves: [correctness, termination, complexity]
status: full
---

**Claim.** Run TREE-ELECTION on a tree $T$ with $n \ge 2$ processes and distinct identifiers, in the asynchronous model with reliable channels, FIFO or not, under any schedule, where a nonempty set of processes start on their own. Let $k$ be the number of processes that start before any message reaches them. Then (a) every process wakes up and sends exactly one report; (b) exactly two processes become saturated, and they are neighbours; (c) both saturated processes set $\mathit{leader}$ to the largest identifier $u_{\max}$, every other process receives exactly one announcement and sets $\mathit{leader} = u_{\max}$, so exactly one process, the owner of $u_{\max}$, is the leader; (d) the run sends exactly $n + k - 2$ wake-up messages, $n$ reports and $n - 2$ announcements, $3n + k - 4$ in all; (e) if every message takes at most one time unit, the run ends by time $3d + 1$, where $d$ is the diameter. For $n = 1$ the only process is saturated when it starts and is the leader, with no message.

For a link $\{u, v\}$ write $T_{u \setminus v}$ for the part of $T$ that contains $u$ when the link is removed.

**Lemma 1 (wake-up).** Every process wakes up, and the number of WAKE messages is $n + k - 2$.

*Proof.* A process that wakes sends WAKE on every link except the one it was woken by, so by induction along paths from a starter every process receives a message and wakes. A starter sends on $\deg(p)$ links and any other process on $\deg(p) - 1$ links; a process sends WAKE only in line L1, once. So the count is $\sum_p \deg(p) - (n - k) = 2(n - 1) - n + k$. $\square$

**Lemma 2 (at most one report).** A process sends at most one report, to its parent, and it is the neighbour from which it has not heard at that moment.

*Proof.* Lines L2 and L4 are the only lines that send a report; both need state *awake* and set state *processing*, and no line sets *awake* again. In line L2 the process has one neighbour, and in line L4 exactly one neighbour is not in $\mathit{heard}$. $\square$

**Lemma 3 (every process reports).** In every complete run, every process sends a report.

*Proof.* At the end of a run no message is in transit. Let $U$ be the set of processes that did not send a report, and suppose $U \ne \emptyset$. Take $u \in U$. It is awake (Lemma 1) and stayed *awake*, so by lines L2 and L4 it has $\deg(u) \ge 2$ and at least two neighbours $w$ with $w \notin \mathit{heard}_u$. Such a $w$ did not report to $u$. If $w$ sent a report, it went to its parent $\ne u$, and by Lemma 2 at that moment $w$ had heard from $u$, which is false because $u$ sent no report. So $w \in U$. Hence every vertex of $U$ has at least two neighbours in $U$, and the subgraph of $T$ induced by $U$ is a nonempty finite forest with minimum degree at least 2. Every nonempty finite forest has a vertex of degree at most 1, a contradiction. $\square$

**Lemma 4 (the saturated link).** Exactly one link carries two reports, one in each direction; every other link carries one. A process becomes saturated exactly when it receives a report over a link that carries two, and so exactly the two ends of that link become saturated.

*Proof.* Take a link $\{u, v\}$. If neither $u$ nor $v$ reported over it, then $u$ reported to some other neighbour and so had heard from $v$ (Lemma 2), so $v$ reported to $u$, a contradiction. So every link carries at least one report. There are $n$ reports (Lemmas 2 and 3) on $n - 1$ links, so exactly one link $\{s, s'\}$ carries two. Line L5 runs when a process in state *processing* receives a report. A process in state *processing* has sent its only report to its parent and had then heard from all other neighbours (Lemma 2), so any later report comes from its parent, over a link that carries two reports. A process receives a report over $\{s, s'\}$ after it has sent its own: before sending, it had not heard from that neighbour, which is why it chose it. So $s$ and $s'$ are both in state *processing* when the other's report arrives, and both become saturated; no other process does. $\square$

**Lemma 5 (reports carry the subtree maximum).** The report that $u$ sends to its parent $v$ carries $\max\{\mathrm{id}(x) : x \in T_{u \setminus v}\}$.

*Proof.* Induction on the order in which reports are sent. When $u$ reports to $v$, it has received reports from every other neighbour $w$, and by induction each of them carried the maximum of $T_{w \setminus u}$. These parts, together with $u$, make up $T_{u \setminus v}$. Line L3 takes the maximum, and line L1 started $\mathit{best}$ at $\mathrm{id}(u)$. $\square$

**Part (c).** Let $s$ and $s'$ be the saturated pair. When $s$ becomes saturated, it has received reports from all its neighbours, including $s'$. The parts $T_{w \setminus s}$ for $w \in N(s)$, together with $s$, cover $T$, so by Lemma 5 $\mathit{best}_s = u_{\max}$; the same holds for $s'$. Remove the link $\{s, s'\}$: the tree splits into two trees rooted at $s$ and $s'$. Line L5 sends the announcement to all neighbours except the parent, and line L6 forwards it to all neighbours except the sender, so the announcements are a broadcast from $s$ and from $s'$ in these two rooted trees. Every process other than $s$ and $s'$ receives exactly one, from its neighbour towards its root, and sets $\mathit{leader} = u_{\max}$. So exactly one process has $\mathit{leader} = \mathrm{id}(p)$, the owner of $u_{\max}$.

**Part (d).** Lemma 1 gives $n + k - 2$ wake-up messages, Lemmas 2 and 3 give $n$ reports, and the broadcast in part (c) gives one announcement to each of the $n - 2$ other processes. The sum is $3n + k - 4$.

**Termination.** All messages are of these three kinds, their number is finite by part (d), and a process sends only when it starts or receives. So every run is finite, and by Lemma 3 and part (c) it ends with every output written.

**Part (e).** Let the first start be at time 0. A process at distance $\delta$ from that starter is awake by time $\delta \le d$. Let $\mathrm{send}(u)$ be the time at which $u$ reports. A leaf reports when it wakes, and any other process reports at most one unit after the last report it needs arrives, so by induction $\mathrm{send}(u) \le \max_{x \in T_{u \setminus v}} (\mathrm{wake}(x) + \mathrm{dist}(x, u)) \le 2d$, where $v$ is the parent of $u$. Both saturated processes are saturated by time $2d + 1$, and an announcement reaches a process at distance $\delta \le d$ from its root $\delta$ units later. So the run ends by time $3d + 1$. $\blacksquare$
