---
title: AODV with destination sequence numbers never forms a routing loop
proves: [correctness]
status: full
---

**Model.** Nodes exchange messages over links. Each directed link delivers its messages in the order they were sent (FIFO), but may lose any of them, and a link may fail or appear at any time. Messages on different links are delivered in any order. Each node $u$ has its own sequence number $\mathit{seq}_u$, which never decreases, and for each destination $d \ne u$ at most one route entry $(\mathit{next}, h, s, \mathit{valid})$: next hop, hop count, sequence number and a valid flag. The protocol is the pseudocode of the page:

- (U) *Update rule.* A node replaces its entry for $d$ by $(v, h, s, \mathrm{true})$, where $v$ is the sender of the message, only if it has no entry, or $s$ is larger than the entry's number, or $s$ equals it and the entry is invalid or has more than $h$ hops.
- (B) *Invalidation.* When a link $u v$ fails, $u$ marks invalid every valid entry with next hop $v$ and adds one to its number. When $u$ gets an RERR from $v$ for $d$ with number $r$ and its valid entry for $d$ has next hop $v$, it marks the entry invalid and sets its number to $\max(s, r)$. In both cases $u$ sends an RERR with the new number.
- (M) *Messages.* An RREQ forwarded by $k$ carries the originator $o$, the originator's number $\sigma$ and the hop count $\eta$ of the path it took to $k$; a receiver treats it as a route to $o$ with $(\sigma, \eta + 1)$. An RREP sent by $k$ for $d$ carries $(\sigma, \eta)$, where $(\sigma, \eta) = (\mathit{seq}_d, 0)$ if $k = d$ and otherwise is $k$'s current valid entry for $d$; the receiver treats it as a route to $d$ with $(\sigma, \eta + 1)$.

For a destination $d$, define the *state* of node $j$ as $(s_j, h_j, \mathit{valid}_j)$: its entry for $d$, or $(\mathit{seq}_d, 0, \mathrm{true})$ if $j = d$. Say that $(s', h', \mathit{valid}')$ is *ahead of* $(s, h)$ if $s' > s$, or $s' = s$, $\mathit{valid}'$ and $h' < h$; and *weakly ahead* if $s' > s$, or $s' = s$, $\mathit{valid}'$ and $h' \le h$.

**Invariant.** At all times, for every destination $d$:

- (I1) for every valid entry of a node $i$ with next hop $j$, the state of $j$ is ahead of $(s_i, h_i)$;
- (I2) for every RREQ or RREP about $d$ in flight from $k$ carrying $(\sigma, \eta)$, the state of $k$ is weakly ahead of $(\sigma, \eta)$;
- (I3) every invalid entry, and every invalidation of (B), has a number larger than the number the entry had while it was last valid.

**Lemma 1.** The state of a node only moves forward: each change takes it to a state whose number is larger, or whose number is equal with the node valid both before and after and the hop count no larger, or from an invalid state to any state with a number at least as large.

*Proof.* The destination's state changes only when $\mathit{seq}_d$ grows. An entry changes only by (U) or (B). By (U), a valid entry is replaced only by one with a larger number or with the same number and fewer hops; an invalid entry by one with a number at least as large. By (B), a valid entry becomes invalid with a larger number, by (I3). $\square$

**Lemma 2.** Each relation "ahead of $(s, h)$" and "weakly ahead of $(s, h)$" is preserved by every move of Lemma 1.

*Proof.* Let the old state be ahead (or weakly ahead) of $(s, h)$. If the new number is larger than the old one, it is larger than $s$ unless the old number was $s$, and then it is larger than $s$ anyway. If the number is the same and the node stays valid with no more hops, the hop condition still holds. If the old state was invalid, the relation held through the first clause, so the old number was larger than $s$, and the new number is at least as large. $\square$

**Proof of the invariant.** Initially there are no entries and no messages. We check each event.

*A node $i$ sets a valid entry from a message of $k$ carrying $(\sigma, \eta)$.* The new entry is $(k, \eta + 1, \sigma, \mathrm{true})$. By (I2) at the time of delivery, the state of $k$ is weakly ahead of $(\sigma, \eta)$, so it is ahead of $(\sigma, \eta + 1)$: a larger number, or the same number with $k$ valid and $h_k \le \eta < \eta + 1$. So (I1) holds for the new entry.

*A node sends a message.* An RREP from $d$ carries exactly the state of $d$; an RREP from an intermediate node carries exactly its valid entry; an RREP forwarded by $u$ carries the entry that $u$ has just set from it. The originator $o$ of an RREQ sends $(\mathit{seq}_o, 0)$, its own state. A node $k$ that forwards an RREQ with $(\sigma, \eta)$ has just applied (U) to $(\sigma, \eta)$: either it set its entry to $(\sigma, \eta)$, or it kept an entry that (U) ranks at least as good, that is, a valid entry with number $\sigma$ and at most $\eta$ hops, or a number larger than $\sigma$. In each case (I2) holds for the new message.

*A state changes.* By Lemmas 1 and 2, every (I1) and (I2) relation that involves the changed node as next hop or sender stays true. An (I1) relation in which the changed node is the holder $i$ is either dropped (the entry became invalid) or set afresh, which was checked above.

*Invalidation by a link failure* raises the number by one, so (I3) holds.

*Invalidation by an RERR from $v$ with number $r$.* Let the entry of $u$ for $d$ be valid with next hop $v$ and number $s$. Its last change set it from a message $M$ of $v$ (by (U) the next hop is always the sender), and $M$ was sent before the RERR, since $M$ was delivered first on the FIFO link from $v$ to $u$. When $v$ sent $M$, the number of $v$ for $d$ was at least $s$, by (I2). The RERR was sent when $v$ invalidated its own entry, later than $M$, and by (I3) for $v$ and the fact that numbers never decrease, $r$ is larger than the number $v$ had when it sent $M$. So $r > s$ and $\max(s, r) > s$: (I3) holds for $u$.

*Loss of a message* only removes (I2) obligations, and the appearance of a link changes no state. $\square$

**Theorem (loop freedom).** At all times, for every destination $d$, following valid next hops from any node never returns to a node already visited.

*Proof.* Along a path $i_0 \to i_1 \to \dots$ of valid entries, (I1) says that each pair $(s, -h)$ of a node is lexicographically smaller than that of the next node. A strictly increasing sequence of pairs has no repeated element, so no node appears twice. $\square$

**Remarks.** The argument needs FIFO links only for the RERR case, and it allows lost messages; the tests drop whole link queues at random and check (I1) and loop freedom after every event. Without sequence numbers the same scene of a lost RERR on a line produces a two-node loop, which one of the tests reproduces. The destination's rule of the page, $\mathit{seq}_d \leftarrow \max(\mathit{seq}_d, \text{requested})$, only raises $\mathit{seq}_d$, which is all the proof uses; RFC 3561 increments the number by one when the request carries the next value. Loop freedom says nothing about delivery: a route request can fail, and the originator then tries again.
