---
tag: P6K020
kind: concept
slug: quorum-certificate
name: Quorum certificate
aliases:
- QC
- commit certificate
area: distributed/byzantine-agreement
level: advanced
summary: A set of 2f + 1 signed votes for one value in one view among 3f + 1 replicas; two such sets share an honest replica, so they cannot conflict.
prereqs: [byzantine-quorum-system, digital-signature, view-change]
see_also: [byzantine-quorum-system, quorum-intersection, hotstuff, pbft, tendermint, zyzzyva, threshold-signature, aggregate-signature]
sources:
  - paper: doi:10.1145/3293611.3331591
    title: Maofan Yin, Dahlia Malkhi, Michael K. Reiter, Guy Golan Gueta and Ittai Abraham, HotStuff, BFT consensus with linearity and responsiveness, ACM Symposium on Principles of Distributed Computing (PODC), 2019
    locator: the quorum certificate as a (n - f, n) threshold signature over the message type, view number and node, and its use in each phase
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the prepared and committed certificates of 2f + 1 matching messages, and the intersection argument
  - paper: doi:10.1007/s004460050050
    title: Dahlia Malkhi and Michael Reiter, Byzantine quorum systems, Distributed Computing 11(4), 1998
    locator: dissemination quorum systems with intersections of at least f + 1 servers
---

A quorum certificate (QC) is a set of signed votes from a quorum of replicas, all for the same value in the same view, that any process can check on its own. With $n = 3f + 1$ replicas of which at most $f$ are Byzantine, a QC has $2f + 1$ votes. Two QCs always share at least one honest replica, and an honest replica votes for at most one value per view and phase, so two QCs for different values in the same view cannot exist. A QC is therefore a portable proof that a quorum agreed. [HotStuff](/hotstuff/) made the term standard and builds each QC as one [threshold signature](/threshold-signature/), so a certificate has constant size.

A quorum certificate differs from a [Byzantine quorum system](/byzantine-quorum-system/). The quorum system is the family of sets, with its rule on overlaps. A QC is one piece of evidence: signatures of one particular quorum on one particular message.

## In plain words

A group of $3f + 1$ computers votes on proposals, and up to $f$ of them may cheat. A quorum certificate is a bundle of $2f + 1$ signed "yes" votes for one proposal in one voting round. Anyone can check the signatures, so anyone who sees the bundle knows that a large part of the group said yes.

Two bundles of $2f + 1$ votes always have at least $f + 1$ voters in common. At most $f$ of them cheat, so at least one honest computer is in both bundles. An honest computer votes once per round. So there cannot be bundles for two different proposals in the same round.

## The idea

**Definition.** Let $n = 3f + 1$ replicas each have a signing key, and let a vote be a signature of a replica on a tuple (phase, view $v$, value $x$). A quorum certificate for (phase, $v$, $x$) is a set of valid votes on that tuple from $2f + 1$ different replicas. For general $n > 3f$ the size is $n - f$, or any size $q$ with $2q - n \ge f + 1$ and $q \le n - f$.

**Claim.** If every honest replica signs at most one vote per phase and view, there are no QCs for (phase, $v$, $x$) and (phase, $v$, $x'$) with $x \ne x'$.

*Proof.* Let $A$ and $B$ be the sets of signers of the two QCs. Then $|A \cap B| \ge |A| + |B| - n = 2(2f + 1) - (3f + 1) = f + 1$. At most $f$ replicas are faulty, so some honest replica is in $A \cap B$. It signed votes for both $x$ and $x'$ in the same phase and view, which an honest replica does not do. The signatures cannot be forged, so the faulty replicas cannot add votes in the name of honest ones. $\blacksquare$

The same count with $n - f$ votes gives $|A \cap B| \ge n - 2f \ge f + 1$ for every $n \ge 3f + 1$.

**What a QC gives across views.** Within a view the claim makes a QC unique. Across views, protocols add a rule: an honest replica that saw a QC (or locked on one) refuses to vote for a conflicting value later unless it sees a QC from a higher view. Since $f + 1$ honest replicas that know of a QC are in every later quorum, a later QC for a conflicting value cannot form. This is the core of the safety proofs of [PBFT](/pbft/), [Tendermint](/tendermint/) and [HotStuff](/hotstuff/).

**Size.** A QC made of $2f + 1$ signatures has $O(n)$ size. With a $(2f + 1, n)$ threshold signature, any $2f + 1$ signature shares combine into one signature of constant size. With [aggregate](/aggregate-signature/) [BLS signatures](/bls-signature/) the size is one signature plus a bit vector of signers. Constant-size QCs let a leader collect votes and send one certificate to all, with $O(n)$ messages per phase.

## Examples

- **PBFT.** A replica is *prepared* for request $m$ at sequence number $s$ in view $v$ when it has the pre-prepare and $2f$ matching prepares, $2f + 1$ messages in all; this set is its prepared certificate. A *committed* certificate is $2f + 1$ commits. PBFT sends these messages all-to-all, and a view change carries prepared certificates to the new view.
- **HotStuff.** The leader collects $n - f$ votes in each of the phases prepare, pre-commit and commit, combines them into a prepareQC, precommitQC and commitQC, and sends each QC to all replicas. A replica locks on a precommitQC.
- **Tendermint.** A *polka* is $2f + 1$ prevotes for one block in one round, and a commit is $2f + 1$ precommits. Each process collects them itself, and a commit is stored with the block.
- **Zyzzyva.** A client that gets $2f + 1$ but fewer than $3f + 1$ matching speculative replies sends them to the replicas as a commit certificate. The view change of Zyzzyva gave a commit certificate priority over $f + 1$ matching logs, and this rule turned out to be unsafe; see the [Zyzzyva](/zyzzyva/) page.
- **Non-example.** $f + 1$ matching votes are not a QC. They prove that one honest replica voted, but two such sets for different values can coexist.

## Where it is used

- Leader-based BFT consensus: [PBFT](/pbft/), [HotStuff](/hotstuff/), [Tendermint](/tendermint/) and their descendants, to lock values and to justify proposals in a new view.
- [Byzantine state machine replication](/byzantine-state-machine-replication/), to prove to clients and to other replicas that an operation is committed.
- Light clients of blockchains, which check a QC on a block header instead of running the protocol.
- Checkpoints, where $2f + 1$ signatures on a state digest let replicas drop old log entries.

## References
