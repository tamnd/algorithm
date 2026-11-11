---
tag: 3NRQ8G
kind: concept
slug: death-certificates
name: Death certificates
aliases:
- tombstones in gossip
area: distributed/gossip
level: advanced
summary: Demers et al.'s deletion markers for epidemic replication. Every site keeps one for τ1; a few random sites keep a dormant copy until τ1 + τ2 and wake it if an old copy of the item returns.
prereqs: [tombstone, anti-entropy, rumor-mongering, last-writer-wins]
see_also: [hinted-handoff, read-repair, eventual-consistency, dynamo-style-replication, crash-recovery, version-vectors, scuttlebutt-reconciliation, push-pull-gossip]
sources:
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 2 (resurrection, the fixed threshold, the snapshot approach of Sarin and Lynch), Section 2.1 (dormant death certificates, τ1, τ2, r retention sites, the 2^(-r) loss bound, the scaling limit), Sections 2.2 and 2.3 (the activation timestamp, with anti-entropy and with rumor mongering)
---

A death certificate is the deletion marker of the epidemic replication protocols of Demers et al. (1987): a deleted item is replaced by a timestamped certificate that spreads like an update and cancels older copies. It is a [tombstone](/tombstone/), and this page is about the two things Demers et al. add to the plain tombstone: **dormant** certificates kept at a few random sites after the others drop them, and a second **activation timestamp** that wakes a dormant certificate without cancelling newer writes. With these, a store can guard against old copies over a period about $n/r$ times longer than one fixed timeout allows with the same space.

## In plain words

When you delete an entry in a store with many copies, you cannot just erase it. Another copy still has the old entry, and the copies that talk to each other would bring it back. So you leave a note that says "deleted at this time", and the note spreads like any change.

The notes take space, so they cannot stay forever. Every site throws its note away after some time. But a few sites, picked at random, keep a sleeping copy for much longer. If an old copy of the entry turns up at one of those sites, the sleeping note wakes up and spreads to everyone again. It still carries its first time, so it does not erase a newer, valid value of the same entry.

## The idea

**Setting.** $n$ sites replicate a database. Updates spread by [anti-entropy](/anti-entropy/) or [rumor mongering](/rumor-mongering/), and two entries for the same key are merged by keeping the one with the larger timestamp, as in [last-writer-wins](/last-writer-wins/). Sites can be down for days and come back with old state, as in the [crash-recovery](/crash-recovery/) model. Demers et al. assume that the clocks differ by at most $\varepsilon$, with $\varepsilon$ much smaller than $\tau_1$, and ignore the difference.

| Symbol | Meaning |
|---|---|
| $n$ | the number of sites |
| $r$ | the number of retention sites of each certificate |
| $\tau_1$ | the time for which every site keeps an active certificate |
| $\tau_2$ | the extra time for which the retention sites keep a dormant copy |
| $\tau$ | the timeout of the plain scheme with one threshold |
| $f$ | the number of sites that are down or have failed |
| $m$, $D$, $\Delta$ | not used: the sites talk to random partners, as on the complete graph |

**The problem with plain deletion.** If a site deletes an item by removing its copy, anti-entropy copies the item back from a site that still has it. So the delete writes a death certificate with the timestamp of the delete. Certificates spread like updates, and a certificate beats every copy of the item with an older timestamp. The [tombstone page](/tombstone/) explains this part and why removing the marker too early brings the item back.

**When to drop a certificate.** Demers et al. discuss two choices. One is to keep a certificate until all sites are known to have it; they cite a protocol of Sarin and Lynch, based on a distributed snapshot, and note that one site that is down for days blocks it. The other is to drop every certificate after a fixed time $\tau$, such as 30 days. Then an old copy that comes back after $\tau$ is resurrected, and a longer $\tau$ costs more space at every site.

**Dormant certificates.** A certificate older than the time needed to reach all sites has almost surely cancelled every copy, so most sites do not need it. The scheme of Demers et al., Section 2.1:

1. When a certificate is created, $r$ retention sites are chosen at random and their names go into the certificate.
2. Every site keeps the certificate while it is younger than $\tau_1$. Then the sites that are not on the list drop it, and the retention sites keep a **dormant** copy.
3. A dormant copy is not sent in anti-entropy exchanges.
4. A dormant copy is dropped when it is older than $\tau_1 + \tau_2$.
5. When an obsolete copy of the item reaches a site that has a dormant certificate, the certificate is **activated**: it becomes active again and spreads to all sites. With rumor mongering, it also becomes a hot rumor again.

Demers et al. compare the woken certificates to antibodies in an immune reaction.

**Two timestamps.** Activation must not simply move the certificate's timestamp to the current time. A site could hold a valid write of the same key with a timestamp between the delete and the activation, for example a write that puts the item back. A certificate with a new timestamp would cancel it. So each certificate has an **ordinary timestamp**, the time of the delete, and an **activation timestamp**, which starts equal to it (Section 2.2):

- The ordinary timestamp decides which entry wins in a merge: the certificate cancels an item only if its ordinary timestamp is larger.
- The activation timestamp decides the life cycle: active while it is younger than $\tau_1$, dormant at the retention sites until it is older than $\tau_1 + \tau_2$, and sent only when active.
- Activation sets the activation timestamp to the current time and leaves the ordinary timestamp as it is.

**Space against history.** Suppose deletions happen at a steady rate $\rho$. With one threshold, each site holds about $\rho \tau$ certificates. With dormant certificates, each site holds about $\rho \tau_1$ active ones, and the $r$ dormant copies of each certificate are spread over $n$ sites, which gives about $\rho r \tau_2 / n$ dormant ones per site. Equal space means
$$\tau_1 + \frac{r}{n}\tau_2 = \tau, \qquad \tau_1 + \tau_2 = \tau_1 + \frac{n}{r}(\tau - \tau_1),$$
so for $\tau_1 < \tau$ the guarded history grows by a factor of order $n/r$. Demers et al. state the $O(n)$ improvement and say that in their system it would raise the history from 30 days to several years. This derivation of the equal-space condition is this page's own, in the same model.

**Loss of the dormant copies.** All $r$ copies are lost if all retention sites fail for good. Demers et al. note that after one server half-life this has probability $2^{-r}$, so $r$ sets the risk.

**The scaling limit.** $\tau_1$ must stay larger than the time a new certificate needs to reach all sites. That time grows with $n$, as $O(\log n)$ cycles for anti-entropy. If it passes $\tau_1$, old items keep meeting dormant certificates, the activations add load, the load slows propagation further, and Demers et al. expect a catastrophic failure. So $\tau_1$, and with it the space at each site, must grow like $\log n$.

**How this differs from the tombstone page.** The [tombstone](/tombstone/) page defines the marker in general: its merge rule, when it is stable, and two ways to remove it, by knowing that all replicas have it or by a grace period as in Cassandra. A death certificate in the sense of Demers et al. is a tombstone with a time-based life cycle and three additions: the dormant copies at $r$ random sites, the second timestamp, and the activation that turns an attempted resurrection into a new spread of the certificate. The plain scheme with one threshold $\tau$ is the grace period of the tombstone page; the dormant scheme guards a much longer period without knowing which sites have the certificate.

## Examples

**A site that returns late.** The implementation on [the rumor mongering page](/rumor-mongering/) runs push-pull anti-entropy on 20 replicas. All hold $x$ with timestamp 1. Replica 19 goes down, replica 0 deletes $x$ at time 2, and replica 19 comes back at time 80 with its old copy. The parameters are $\tau_1 = 30$, $\tau_2 = 400$ and $r = 3$, and the run ends at time 200.

| Deletion | Replicas holding $x$ at time 200 (5 seeds) |
|---|---|
| remove the copy | 20, 20, 20, 20, 20 |
| certificate dropped at $\tau_1$ by every site | 20, 20, 20, 20, 20 |
| dormant certificates | 0, 0, 0, 0, 0 |

Without a certificate, $x$ comes back at once. With one threshold, the certificate reaches all 19 live replicas by time 4 to 6 in the first three seeds and is dropped by all of them at time 33, so the old copy from replica 19 spreads again from time 80. With dormant certificates, three sites still hold a dormant copy at time 80. With seed 0, a retention site meets the old copy at time 81 and wakes its certificate. The old copy still reaches 10 replicas at time 82, but it is gone from all 20 replicas at time 85. The woken certificate becomes dormant again about $\tau_1$ later, and the retention sites keep it until the end.

**The second timestamp.** A replica holds a dormant certificate for $x$ with ordinary timestamp 2. Elsewhere, $x$ is written again with value $v_2$ and timestamp 15. At time 20 an old copy of $x$ with timestamp 1 arrives, and the certificate is woken.

- Right: the activation timestamp becomes 20 and the ordinary timestamp stays 2. The certificate beats the copy with timestamp 1, and $v_2$ with timestamp 15 beats the certificate.
- Wrong: the timestamp becomes 20. The certificate then beats $v_2$, and the valid write is lost.

The tests of the implementation check both the right case and the case that the newer write still wins.

**Choosing the parameters.** Take $n = 300$, $r = 3$, $\tau = 30$ days and $\tau_1 = 15$ days. Equal space gives $\tau_2 = (300/3)(30 - 15) = 1500$ days, so old copies are stopped for $1515$ days, about 4.1 years, with the space of a 30 day timeout. With $r = 3$ the dormant copies are all lost after one server half-life with probability $2^{-3} = 1/8$; with $r = 10$ the probability is $2^{-10} \approx 0.001$, and $\tau_2$ falls to 450 days.

## Where it is used

- **The Xerox Clearinghouse.** Demers et al. designed dormant certificates for the Clearinghouse name service, which used anti-entropy and kept certificates for a fixed 30 days.
- **Stores with background repair.** [Dynamo-style](/dynamo-style-replication/) stores reconcile replicas in the background and need the same markers. Cassandra, as described on the [tombstone page](/tombstone/), drops tombstones after a fixed grace period and requires repair within it, which is the scheme with one threshold.
- **Any epidemic protocol with deletion.** A gossip protocol that removes entries, for example from a membership list or from the state exchanged by [Scuttlebutt reconciliation](/scuttlebutt-reconciliation/), has the same problem: a removed entry must be marked, and the mark must outlive the old copies.

## References
