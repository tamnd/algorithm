---
title: The view change of Viewstamped Replication never loses a committed operation
proves: [correctness]
status: full
---

The model is asynchronous, with $n = 2f + 1$ replicas and messages that can be delayed, reordered and duplicated but not changed. The primary of view $v$ is $v \bmod n$. We prove safety for replicas that crash and stop, or that keep their state across a restart; the recovery of a replica that lost its state is discussed at the end.

**Notation.** An op $x$ is *committed at position $j$ in view $v$* when the primary of $v$, in view $v$ with normal status, sets $k \ge j$ with $x$ at position $j$ of its log, at line L3 or line L8. For each replica, $v'$ is the last view in which it had normal status. The view number of a replica never decreases.

**Lemma 1 (logs in one view).** While the primary of view $v$ is in view $v$, it only appends to the log it started $v$ with. Every replica that is in view $v$ with normal status holds a prefix of that log.

*Proof.* The primary of $v$ starts the view with a log $L$ at line L8 and then only appends (line L1). A backup enters view $v$ with normal status only at line L9, with the log $L$ of StartView$(v)$, and then appends only ops of Prepare messages of view $v$, each at the position $n$ that the primary gave it, and in order (line L2). Messages of other views are dropped or held back. $\square$

**Lemma 2 (a commit leaves $f + 1$ copies).** If $x$ is committed at position $j$ in view $v$, there is a set $S$ of $f + 1$ replicas, each of which, at some moment in view $v$ with normal status, had $x$ at position $j$.

*Proof.* At line L3 the primary has PrepareOK$(v, n)$ with $n \ge j$ from $f$ backups. A backup sends PrepareOK$(v, n)$ only in view $v$ with normal status, and only when it holds positions $1$ to $n$ (lines L2 and L9), which by Lemma 1 agree with the primary's log. With the primary, that is $f + 1$ replicas. At line L8, the primary chose $k$ as the largest commit-number in its DoViewChange messages; that number was set by an earlier commit at the same positions, and we apply the lemma to that earlier commit, by induction on time. $\square$

**Theorem (committed ops survive view changes).** If $x$ is committed at position $j$ in view $v$, then for every view $w > v$ whose primary reaches line L8, the log it starts $w$ with has $x$ at position $j$.

*Proof.* By strong induction on $w$. Fix $w > v$ and assume the claim for every view $u$ with $v < u < w$.

*Claim A.* Let $r \in S$. At every moment after $r$ held $x$ at $j$ in view $v$ and before it sends DoViewChange$(w)$, its log has $x$ at position $j$ and its $v'$ is at least $v$.

Its $v'$ was $v$ then and only grows. Its log changes only at line L2, which appends and so keeps position $j$; at line L9, where it takes the log of StartView$(u)$ for some $u$ with $v < u < w$; and at line L7, if it is itself the new primary of such a view $u$. In the last two cases the log is the one the primary of $u$ starts $u$ with, which has $x$ at $j$ by the induction hypothesis. (Line L9 for $u = v$ cannot happen again once $r$ is in view $v$ with normal status.)

*Claim B.* Some replica in $S$ is among the $f + 1$ replicas $D$ whose DoViewChange$(w)$ messages the new primary used at line L7, and it sent that message after it held $x$ at $j$ in view $v$.

$|S| + |D| = 2f + 2 > n$, so some $r$ is in both. Replica $r$ was in view $v$ when it held $x$, and in view $w > v$ when it sent DoViewChange$(w)$. View numbers never decrease, so the send came later.

*The chosen log.* By Claims A and B, the replica $r$ reported $v'_r \ge v$ and a log with $x$ at $j$. Line L7 takes a log with the largest $v'$, say $v^*$, so $v^* \ge v'_r \ge v$.

- If $v^* = v$, then $v'_r = v$, and both $r$'s log and the chosen log were held in view $v$ with normal status, so by Lemma 1 both are prefixes of the log of the primary of $v$. Line L7 breaks ties by the longest log, so the chosen log is at least as long as $r$'s, and it is a prefix of the same log, so it has $x$ at $j$.
- If $v^* > v$, the replica that reported it was last normal in view $v^*$ with $v < v^* < w$. The primary of $v^*$ started $v^*$ with a log that has $x$ at $j$ by the induction hypothesis, and by Lemma 1 the reported log is a prefix of the primary's log in $v^*$ that is at least as long as the log the replica received at line L9. So it has $x$ at $j$.

In both cases the new primary of $w$ starts with $x$ at $j$. $\square$

**Lemma 3 (no commit in a view after its quorum left).** The proof above does not need this, but it explains line L6: a replica in view-change status sends no PrepareOK, so once $f + 1$ replicas have moved to view $w$, the primary of an older view can never again collect $f$ PrepareOK messages from them.

**Corollary 1 (one op per position).** No two different ops are committed at the same position.

*Proof.* Let $x$ be committed at $j$ in view $v$ and $y$ at $j$ in view $w$. If $w = v$, both are in the log of the primary of $v$, which by Lemma 1 only appends, so $x = y$. If $w > v$, the primary of $w$ started with $x$ at $j$ by the theorem, and only appends, so $y = x$. $\square$

**Corollary 2 (the same sequence).** Every replica runs a prefix of one sequence of ops.

*Proof.* A replica runs ops only at positions up to its commit-number (lines L3, L4, L8 and L9). A backup sets its commit-number only from a Commit, Prepare or StartView message of the primary of its current view, and runs only ops of its log, which by Lemma 1 is a prefix of that primary's log. So every op it runs at position $j$ is the op committed at $j$, which is unique by Corollary 1. $\blacksquare$

**Replicas that lose their state.** The argument uses Claim A: a member of $S$ keeps $x$ until it reports to the next view. A replica that crashes and forgets its log breaks Claim A, and with it the theorem: this is the failure that the tests show for a replica that rejoins with an empty log. Lines L10 to L12 are there to restore Claim A. The recovering replica takes no part in any quorum, and it copies the state of the primary of the latest view that it hears of from $f + 1$ replicas, under the assumption that at most $f$ replicas are crashed or recovering at one time. Liskov and Cowling argue this case informally. A full proof must follow states across many crashes and restarts, and Michael, Ports, Sharma and Szekeres (DISC 2017) show that recovery without stable storage is subtle; we do not claim a proof for it here, and the tests check it only by simulation.
