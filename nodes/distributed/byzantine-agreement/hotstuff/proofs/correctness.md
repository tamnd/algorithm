---
title: Basic HotStuff never commits two conflicting nodes, and decides after GST
proves: [correctness]
status: full
---

**Claim.** Let $n = 3f + 1$ replicas run Basic HotStuff with at most $f$ Byzantine replicas and unforgeable threshold signatures. (Safety) In every run, if honest replicas execute the branches of two commitQCs, one of the two nodes extends the other, so the executed logs are prefixes of one another. (Liveness) Under partial synchrony, after GST every view with an honest leader that all honest replicas enter in time ends with a decision, and the pacemaker brings such a view.

**Setup.** A node is a pair (command, parent). Node $b$ *extends* node $a$ if $a$ is $b$ or an ancestor of $b$. Two nodes *conflict* if neither extends the other. A QC of type $\tau$ for $(v, b)$ is a $(n - f, n)$ threshold signature on $(\tau, v, b)$; write $qc.view$ and $qc.node$. A quorum is $n - f = 2f + 1$ replicas, and two quorums share at least $f + 1$ replicas, so an honest one.

The rules of an honest replica that the proof uses:

- (H1) It votes at most once per type and view, and only in its current view. Its current view never decreases.
- (H2) It votes PREPARE for $b$ in view $v$ only if the justify QC is a prepareQC with $justify.view < v$, $b.parent = justify.node$, and $safeNode(b, justify)$: $b$ extends $lockedQC.node$ or $justify.view > lockedQC.view$ (line L4).
- (H3) It votes PRE-COMMIT in view $v$ only on a prepareQC of view $v$, and COMMIT in view $v$ only on a precommitQC of view $v$, and then it sets $lockedQC$ to that precommitQC (line L8). So the view of its lock never decreases.

**Lemma 1.** Two QCs of the same type and view are for the same node.

*Proof.* Their signer sets are quorums and share an honest replica, which by (H1) voted once for that type and view. $\square$

**Lemma 2.** If a precommitQC for $(v, b)$ exists, a prepareQC for $(v, b)$ exists. If a commitQC for $(v, b)$ exists, a precommitQC for $(v, b)$ exists, and at least $f + 1$ honest replicas set their lock to it.

*Proof.* A QC has $f + 1$ honest signers, and by (H3) each of them voted on a QC of the type before for $(v, b)$. For a commitQC, by (H3) each honest signer set its lock to the precommitQC for $(v, b)$ before it voted. $\square$

## Safety

**Theorem 1.** If commitQCs exist for $(v_1, w)$ and $(v_2, b)$, then $w$ and $b$ do not conflict.

*Proof.* If $v_1 = v_2$, Lemma 1 gives $w = b$. Let $v_1 < v_2$ (the other case is symmetric). Let $S$ be the set of prepareQCs with view greater than $v_1$ whose node does not extend $w$. By Lemma 2 there is a prepareQC for $(v_2, b)$. If $b$ conflicts with $w$, then $b$ does not extend $w$, so $S$ is not empty. Take $qc_s \in S$ with the smallest view $v_s$, for node $b_s$.

The $2f + 1$ signers of the commitQC for $(v_1, w)$ and the $2f + 1$ signers of $qc_s$ share an honest replica $r$. By (H3), $r$ locked on the precommitQC for $(v_1, w)$ when it voted COMMIT. Replica $r$ voted COMMIT in view $v_1$ and PREPARE in view $v_s > v_1$, so by (H1) it voted in $v_1$ first, and when it voted for $b_s$ its lock had view at least $v_1$.

*The lock of $r$ extends $w$.* By (H3) the lock of $r$ at the time of its vote in $v_s$ is a precommitQC of some view $u$ with $v_1 \le u < v_s$. If $u = v_1$, it is for $w$ by Lemma 1. If $v_1 < u < v_s$, then by Lemma 2 there is a prepareQC of view $u$ for the same node, and it is not in $S$ because $u < v_s$, so the node extends $w$.

*The vote of $r$ is impossible.* By (H2), $safeNode(b_s, justify)$ held for $r$. If $b_s$ extends the lock of $r$, it extends $w$, which contradicts $qc_s \in S$. Otherwise $justify.view > lockedQC.view \ge v_1$, and $justify.view < v_s$ by (H2). The justify is a prepareQC for $b_s.parent$. If $b_s.parent$ extended $w$, so would $b_s$. So the justify is in $S$ with a view smaller than $v_s$, which contradicts the choice of $qc_s$.

So $S$ is empty, every prepareQC of a view above $v_1$ is for a node that extends $w$, and $b$ extends $w$. $\blacksquare$

**Corollary.** An honest replica executes the branch from the root to the node of a commitQC (line L10). By Theorem 1 any two such nodes lie on one path, so the executed logs of honest replicas are prefixes of one another.

The proof uses the third phase only through Lemma 2: the lock is set on a precommitQC, which exists only after a prepareQC formed. The next section shows why this matters for liveness.

## Liveness

Assume that after GST every message between honest replicas arrives within $\Delta$, and that the timeout of a replica doubles each time it gives up on a view.

**Lemma 3 (an honest leader can make every honest replica vote).** Let the leader $L$ of view $v$ be honest and let it get NEW-VIEW messages from a quorum $N$. Let $highQC$ be the prepareQC of the highest view among them. Then every honest replica in view $v$ accepts the proposal $b$ with $b.parent = highQC.node$.

*Proof.* Let $p$ be honest with $lockedQC$ for $(u, a)$. By Lemma 2, $f + 1$ honest replicas hold a prepareQC of view $u$ for $a$, since they voted PRE-COMMIT on it. They and $N$ share a replica, and that replica sent a prepareQC of view at least $u$ in its NEW-VIEW (an honest replica keeps the highest prepareQC it saw). So $highQC.view \ge u$. If $highQC.view > u$, the second clause of $safeNode$ holds. If $highQC.view = u$, Lemma 1 gives $highQC.node = a$, so $b$ extends the lock. Also $highQC.view < v$, since honest replicas send NEW-VIEW for $v$ before they vote in $v$. $\square$

**Theorem 2.** After GST, if all honest replicas are in view $v$ with an honest leader and none gives up on $v$ for $7\Delta$ after the leader proposes, all honest replicas execute a new node in view $v$.

*Proof.* By Lemma 3 all $2f + 1$ honest replicas vote PREPARE, so the leader forms a prepareQC. Each later phase needs only the honest votes on the QC of the phase before, so the leader forms a precommitQC and a commitQC and sends DECIDE. The seven message delays from PREPARE to DECIDE take at most $7\Delta$. $\square$

**The pacemaker.** A replica that times out in view $v$ sends TIMEOUT for $v$ to all. A replica that gets TIMEOUT for $v$ from $f + 1$ others sends its own, and a replica with $2f + 1$ TIMEOUT messages for $v$ moves to $v + 1$. A view ends by timeout only if $2f + 1$ replicas, so $f + 1$ honest ones, timed out, and then within $2\Delta$ after GST all honest replicas have $2f + 1$ TIMEOUT messages and move to $v + 1$ within $2\Delta$ of each other. Each failed view doubles the timeouts, so after GST they pass $7\Delta$ plus the gaps between replicas. Leaders rotate, so among any $f + 1$ views in a row one leader is honest, and Theorem 2 applies to it. $\blacksquare$

**Why three phases.** With only two phases (lock on the prepareQC), Lemma 3 fails: one honest replica can hold a lock of view $u$ that the $n - f$ NEW-VIEW messages do not show, because only that replica saw the prepareQC. A leader that proposes from $highQC$ then gets no vote from that replica, and with $f$ faulty replicas silent it cannot form a QC. Two-phase protocols such as [Tendermint](/tendermint/) fix this by waiting for the maximal network delay before they propose, so they are not responsive. In HotStuff the lock is on a precommitQC, and by Lemma 2 its prepareQC is known to $f + 1$ honest replicas, one of which is in every quorum of NEW-VIEW messages.

## Where the bounds are used

- $n \ge 3f + 1$, with quorums of $n - f$, gives the honest replica in every intersection (Lemmas 1 and 3 and Theorem 1) and lets the honest replicas form a quorum alone (Theorem 2).
- The test of the tests: if $safeNode$ always returns true, a faulty leader that proposes a fork from the root and shows its prepareQC to one honest replica makes honest replicas execute two conflicting branches, and the tests find this.
