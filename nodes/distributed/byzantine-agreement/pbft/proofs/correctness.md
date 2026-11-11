---
title: PBFT is safe in every run and live after GST
proves: [correctness]
status: full
---

**Claim.** Let $n = 3f + 1$ replicas run PBFT, with at most $f$ Byzantine replicas, unforgeable signatures and any number of faulty clients. (Safety) In every run, no two honest replicas execute different requests at the same sequence number. (Liveness) If the network is partially synchronous and the timeouts grow without bound while views fail, every request that a correct client keeps sending is executed by at least $f + 1$ honest replicas, so the client gets $f + 1$ matching replies.

Safety does not use any timing. Liveness uses the global stabilization time (GST), after which every message between honest replicas arrives within a bound $\Delta$ that the replicas do not know.

**Setup.** A *quorum* is a set of $2f + 1$ different replicas. Two quorums $Q_1, Q_2$ satisfy $|Q_1 \cap Q_2| \ge 2(2f + 1) - (3f + 1) = f + 1$, so they share an honest replica. A quorum and a set of $f + 1$ honest replicas share at least $(2f + 1) + (f + 1) - (3f + 1) = 1$ replica, which is honest.

$prepared_i(m, v, s)$ holds when replica $i$ has the PRE-PREPARE $\langle v, s, m \rangle$ from the primary of view $v$ and $2f$ matching PREPARE messages from different backups (line L3). These $2f + 1$ signed messages form a *prepared certificate* for $(m, v, s)$, and their senders form a quorum. $committed\text{-}local_i(m, v, s)$ holds when $prepared_i(m, v, s)$ holds and $i$ has $2f + 1$ matching COMMIT messages from different replicas (line L5).

The rules of an honest replica that the proof uses:

- (R1) In view $v$ it accepts at most one PRE-PREPARE for each $(v, s)$, and it sends a PREPARE only for the one it accepted. An honest primary signs at most one PRE-PREPARE for each $(v, s)$.
- (R2) It sends a COMMIT for $(m, v, s)$ only when $prepared_i(m, v, s)$ holds and it has not sent VIEW-CHANGE for a view above $v$.
- (R3) Its VIEW-CHANGE for $v'$ carries, for each $s$ above its stable checkpoint, the prepared certificate of the highest view below $v'$ in which it was prepared at $s$.
- (R4) It enters view $v'$ only with a NEW-VIEW that holds $2f + 1$ valid VIEW-CHANGE messages for $v'$ and a set $O$ of PRE-PREPARE messages that it recomputes from them. In view $v'$ it handles the messages of $O$ before any other PRE-PREPARE of view $v'$, so by (R1) it accepts no other PRE-PREPARE for a sequence number of $O$.
- (R5) A checkpoint is stable when $2f + 1$ replicas signed the same state digest for it. A replica copies a state only from a stable checkpoint.

## Safety within one view

**Lemma 1.** If $prepared_i(m, v, s)$ and $prepared_j(m', v, s)$ hold for honest $i$ and $j$, then $m = m'$. The same holds for any two prepared certificates for view $v$ and sequence number $s$, wherever they are found.

*Proof.* The two certificates come from quorums $Q$ and $Q'$, which share an honest replica $r$. If $r$ is the primary of $v$, it signed PRE-PREPARE messages for $m$ and $m'$ at $(v, s)$. Otherwise it signed PREPARE messages for both. By (R1) both cases need $m = m'$. The signatures cannot be forged, so the faulty replicas cannot put the name of $r$ on a message. $\square$

**Lemma 2.** If $committed\text{-}local_i(m, v, s)$ holds for an honest $i$, then a set $R$ of at least $f + 1$ honest replicas has $prepared(m, v, s)$.

*Proof.* Replica $i$ has $2f + 1$ COMMIT messages for $(m, v, s)$, and at most $f$ of them come from faulty replicas. By (R2) each honest sender was prepared for $(m, v, s)$ when it sent. $\square$

## Safety across views

**Lemma 3.** Let $committed\text{-}local_i(m, v, s)$ hold for an honest $i$. Then for every view $w \ge v$, every prepared certificate for $(m', w, s)$ has $m' = m$, and every honest replica that enters view $w > v$ either accepts the PRE-PREPARE $\langle w, s, m \rangle$ from $O$ or has a stable checkpoint at or above $s$.

*Proof.* By induction on $w$. For $w = v$, Lemma 1 with the prepared certificate of $i$ gives $m' = m$.

Let $w > v$ and assume the claim for all views in $[v, w)$. Let $R$ be the honest replicas of Lemma 2. Take a NEW-VIEW for $w$ that an honest replica accepts. Its $2f + 1$ VIEW-CHANGE messages form a quorum, so one of them comes from some $r \in R$. Replica $r$ was prepared for $(m, v, s)$ in view $v$. By (R2) and the view order, $r$ was prepared before it sent its VIEW-CHANGE for $w$. Two cases.

*Case A: the largest stable checkpoint $min\text{-}s$ in the NEW-VIEW is at least $s$.* Then $O$ has no entry for $s$, and a replica that enters $w$ copies or already has a stable checkpoint at or above $s$.

*Case B: $min\text{-}s < s$.* The checkpoint of $r$ is at most $min\text{-}s < s$, so by (R3) the VIEW-CHANGE of $r$ carries a prepared certificate for $s$ in some view $u$ with $v \le u < w$. By the induction hypothesis it is for $m$. Every other certificate for $s$ in the NEW-VIEW is either from a view below $v$, which is below $u$, or from a view in $[v, w)$, which is for $m$ by the induction hypothesis. The rule for $O$ takes the certificate of the highest view, so $O$ holds $\langle w, s, m \rangle$. An honest replica recomputes $O$ by (R4), so it rejects a NEW-VIEW with another entry, and in view $w$ it accepts no other PRE-PREPARE for $s$.

A prepared certificate for $(m', w, s)$ contains a quorum, so an honest replica in it accepted a PRE-PREPARE $\langle w, s, m' \rangle$ in view $w$ (as primary or as backup). In Case B that is the entry of $O$, so $m' = m$. In Case A, that replica had a stable checkpoint at or above $s$ and does not accept PRE-PREPARE messages for $s$, since $s$ is below its low watermark. So no certificate for $s$ forms in view $w$ in Case A. $\square$

**Lemma 4 (checkpoints).** Suppose all honest committed-local events at $s$ are for $m$. Then every stable checkpoint at $s' \ge s$ has $m$ at $s$ in its state.

*Proof.* By induction on the time at which checkpoints become stable. A stable checkpoint has $2f + 1$ signatures on one digest, so at least $f + 1$ honest replicas signed it, and at least one of them built the state at $s'$ itself. That replica executed $s$ either after a committed-local event, which is for $m$, or by copying an earlier stable checkpoint, which has $m$ at $s$ by the induction hypothesis. The digest fixes the state, so all signers of the checkpoint hold the same state. $\square$

**Theorem (safety).** No two honest replicas execute different requests at the same sequence number $s$.

*Proof.* An honest replica executes $s$ after a committed-local event at $s$ (line L6) or by copying a stable checkpoint at or above $s$ (R5). Take the first committed-local event at $s$ in the run, for $(m, v, s)$ at replica $i$. A later committed-local event for $(m', w, s)$ at an honest $j$ needs a prepared certificate for $(m', w, s)$. If $w \ge v$, Lemma 3 gives $m' = m$. If $w < v$, apply Lemma 3 to the event at $j$: the certificate of $i$ in view $v > w$ is then for $m'$, so again $m' = m$. So all committed-local events at $s$ are for one request $m$, and by Lemma 4 every stable checkpoint has $m$ at $s$. $\blacksquare$

## Liveness after GST

The assumptions: after GST every message between honest replicas arrives within $\Delta$; a correct client sends its request to all replicas again when it does not get $f + 1$ matching replies in time, so the request stays pending at every honest replica until that replica executes it; and a replica doubles its timeout each time a view change does not finish in time.

**Lemma 5.** The faulty replicas alone cannot make honest replicas leave a view.

*Proof.* An honest replica sends VIEW-CHANGE either when its own timer expires or when it gets VIEW-CHANGE messages for higher views from $f + 1$ other replicas, and at least one of those is honest. A NEW-VIEW needs $2f + 1$ VIEW-CHANGE messages, so at least $f + 1$ honest ones. So a view change completes only if some honest replica timed out on its own. $\square$

**Lemma 6.** After GST, if at least $f + 1$ honest replicas send VIEW-CHANGE for views above $v$, then within bounded time every honest replica sends VIEW-CHANGE for a view above $v$.

*Proof.* Their messages reach every honest replica within $\Delta$, and the join rule (on $f + 1$ VIEW-CHANGE messages for higher views from others) makes each honest replica send VIEW-CHANGE for the smallest such view. $\square$

**Theorem (liveness).** Every request that a correct client keeps sending is executed by at least $f + 1$ honest replicas.

*Proof.* Suppose not, and take a request $m$ after GST. Each honest replica that has not executed $m$ keeps $m$ pending and keeps its timer running.

If fewer than $f + 1$ honest replicas start a view change, then by Lemma 5 the view does not change, and at least $f + 1$ honest replicas stay in the view and keep taking part. They do not execute $m$, so their timers expire and they start a view change, which is a contradiction. So at least $f + 1$ honest replicas start view changes again and again, and by Lemma 6 all $2f + 1$ honest replicas follow within bounded time.

A replica that has $2f + 1$ VIEW-CHANGE messages for $v'$ waits for NEW-VIEW until its timer expires, then moves to $v' + 1$ with a doubled timeout. The primaries rotate as $v \bmod n$, so among any $f + 1$ views in a row one has an honest primary. After GST the honest replicas reach a common target view within bounded time, and once the timeout is larger than the time that a view change and three phases need after GST (a constant number of $\Delta$ plus the time to reach the view), a view $v^*$ with an honest primary completes: the primary gets $2f + 1$ VIEW-CHANGE messages, sends a valid NEW-VIEW, and every honest replica enters $v^*$ before its timer expires.

In $v^*$ the honest primary assigns a sequence number in the window to $m$ (requests from earlier numbers in $O$ are proposed again and commit first), and $2f + 1$ honest replicas prepare, commit and execute within $3\Delta$ of the PRE-PREPARE. At least $f + 1$ of them are honest, which contradicts the assumption. Timers restart on each execution, so the honest replicas do not leave $v^*$ while requests keep being executed in time. $\blacksquare$

A replica that fell behind, for example one that sent VIEW-CHANGE while the others committed, can stay behind until the next stable checkpoint, where it copies the state (R5). For this reason the claim is for $f + 1$ honest replicas, which is what a client needs, and not for all of them.

## Where the bounds are used

- $n \ge 3f + 1$ makes two quorums of $2f + 1$ share an honest replica (Lemmas 1 and 3) and lets $2f + 1$ honest replicas form a quorum without the faulty ones (liveness).
- Signatures on the VIEW-CHANGE messages and on the certificates inside them stop a faulty new primary from inventing or hiding certificates. A faulty replica can leave out its own certificates, but Lemma 3 needs only the certificate of one honest replica in $R$.
- The rule (R2) that a replica stops voting in view $v$ once it sent VIEW-CHANGE is needed. Without it, a replica can report no certificate for $s$ in its VIEW-CHANGE and then help to commit at $s$ in the old view, and the new view can assign another request to $s$.
