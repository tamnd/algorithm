---
tag: 75N9PB
kind: algorithm
slug: scuttlebutt-reconciliation
name: Scuttlebutt reconciliation
aliases:
- scuttlebutt
- scuttle-depth
area: distributed/gossip
level: advanced
summary: Anti-entropy in which each participant writes only its own keys with growing versions. Peers trade, per participant, the highest version they know and send newer deltas in version order.
model: random-phone-call-model
complexity:
  vars: {n: the number of participants, K: the keys per participant, M: the most deltas in one message (mtu)}
  messages: {per_exchange: O(n + M)}
  time: {rounds: O(log n)}
  space: {extra: Θ(n K)}
properties: {deterministic: false, recursive: false}
history:
  year: 2008
  people: [Robbert van Renesse, Dan Dumitriu, Valient Gough, Chris Thomas]
  note: Van Renesse, Dumitriu, Gough and Thomas (Amazon.com) gave the reconciliation with per-participant maximum versions, the scuttle-depth order and a flow control for anti-entropy at LADIS 2008.
prereqs: [anti-entropy, push-pull-gossip, random-phone-call-model, last-writer-wins]
see_also: [set-reconciliation, merkle-tree, version-vectors, aimd, rumor-mongering, death-certificates, eventual-consistency, read-repair]
sources:
  - paper: doi:10.1145/1529974.1529983
    title: Robbert van Renesse, Dan Dumitriu, Valient Gough and Chris Thomas, Efficient reconciliation and flow control for anti-entropy protocols, Proceedings of the 2nd Workshop on Large-Scale Distributed Systems and Middleware (LADIS), 2008
    locator: Section 2 (the state model and push-pull), Section 3.1 (precise reconciliation), Section 3.2 (Scuttlebutt, ordering constraint (1), invariant (2), property (3), Figure 1, scuttle-breadth and scuttle-depth), Section 3.3 (evaluation, Figure 2), Section 4 (flow control, Figure 3)
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.3 (anti-entropy with push, pull and push-pull)
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: the push-pull spreading time of log_3 n + O(log log n) rounds
---

Scuttlebutt is a reconciliation method for [anti-entropy](/anti-entropy/) gossip, from van Renesse, Dumitriu, Gough and Thomas (2008). Each participant writes only its own keys, and each write gets a version larger than every version that participant used before. Two gossip partners then compare one number per participant, the highest version each has seen from it, and send only the newer entries, in version order and at most $mtu$ of them per message. The version order keeps an invariant that makes a gossip exchange safe to cut short, so the method works when messages have a fixed maximum size.

## In plain words

Every member of a group keeps a notebook about each member. Only the owner may write in its own page, and it numbers each entry with a counter that only goes up.

When two members meet, they first say, for each page, the highest number they have seen. Each one then hands over the entries that the other has not seen, oldest numbers first. If there is not enough time to hand over all of them, they stop, but they never skip an older entry to give a newer one.

Because of this rule, "I have seen up to number 40 of Anna's page" always means "I have everything that Anna still has with numbers up to 40". So a short summary is enough to know what to send. Nothing that the other already knows is sent, and everyone ends up with the same notebook when the writing stops.

## The problem

There are $n$ participants. Participant $r$ owns the state $\mu_r(r)$, a map from keys to pairs (value, version), and every participant $p$ keeps a copy $\mu_p(r)$ of every state. Only $r$ writes $\mu_r(r)$; the copies change only by gossip. In each gossip interval, every participant picks a partner uniformly at random, as in the [random phone call model](/random-phone-call-model/), and the two do one push-pull exchange. A message holds at most $mtu$ deltas, where a delta $(r, k, v, n)$ says that $r$ mapped key $k$ to value $v$ with version $n$. Copies are merged by [last writer wins](/last-writer-wins/) on the version. The goal is that, after the writes stop, every copy $\mu_p(r)$ becomes equal to $\mu_r(r)$, with few deltas wasted on the way.

| Symbol | Meaning |
|---|---|
| $n$ | the number of participants |
| $K$ | the number of keys of each participant |
| $mtu$ | the most deltas in one gossip message, written $M$ in the complexity fields |
| $\mu_p(r)(k)$ | the pair (value, version) that $p$ holds for key $k$ of participant $r$ |
| $\max_p(r)$ | the largest version that $p$ has seen from $r$ |
| $\rho_p, \tau_p$ | the desired and the maximum update rate of $p$ (flow control) |
| $f$ | the number of participants that crash; crashed participants stop writing and gossiping |
| $D$, $\Delta$ | the diameter and the maximum degree; on the complete graph $D = 1$ and $\Delta = n - 1$ |

## The algorithm

```pseudo id=main
SCUTTLEBUTT at participant p
ON A LOCAL WRITE of key k with value v
L1  µp(p)(k) ← (v, n), with n larger than every version p has used; maxp(p) ← n
ONCE PER GOSSIP INTERVAL
L2  q ← a participant chosen uniformly at random, other than p
L3  p and q exchange digests: the list of max(r) for every participant r
TO BUILD THE DELTAS for a partner with digest d (p does this for q, and q for p)
L4  for every r: A(r) ← the deltas (r, k, v, n) of µ(r) with n > d(r), sorted by version
L5  order the participants r that have deltas: most deltas first (scuttle-depth), ties at random
L6  send the first mtu deltas of the list A(r1), A(r2), ... in that order
ON A DELTA (r, k, v, n) received
L7  if n is larger than the version of µ(r)(k) then µ(r)(k) ← (v, n)
L8  max(r) ← the larger of max(r) and n
```

The key rule is the **ordering constraint**, equation (1) of the paper: if a delta of $r$ is left out of a message, all deltas of $r$ with larger versions are left out as well. Lines L4 and L6 satisfy it, because the deltas of each $r$ are sorted by version and the message is a prefix of the list. Line L1 uses one counter for all keys of $p$, so no two keys of $p$ have the same version.

The digest at line L3 has $n$ numbers, not one per key. The partner sends only deltas newer than $d(r)$, so no delta that the receiver already has is sent. In the paper, the initiator sends its digest first and the partner answers with its digest and its deltas; the code computes both delta sets from the states at the start of the exchange, as in the simplified protocol of Section 3.2.

**The two orders.** The paper gives two orders that satisfy the constraint. *Scuttle-depth* (line L5) sends the deltas of the participants that are most behind first, all of one participant before the next. *Scuttle-breadth* gives each delta a rank, its position in $A(r)$, and sends all deltas of rank 0 first, then rank 1, and so on, with a new random order of the participants for each message. The paper found scuttle-depth the better of the two.

**Precise reconciliation** is the baseline of Section 3.1. It compares the full tables key by key and sends every mapping that is newer at the sender, ordered by the oldest first (precise-oldest) or the newest first (precise-newest). It needs digests with one version per key, and the two orders need a clock that is the same at all participants.

## Example

**Figure 1 of the paper.** Look at participant $r$ with keys $a$, $b$ and $c$. Participant $r$ has $a, b, c$ at versions 21, 22 and 23, participant $p$ has versions 1, 2 and 3, and participant $q$ has versions 11, 12 and 13. Let $mtu = 1$.

| Step | $p$: $a, b, c$ | $\max_p(r)$ | $q$: $a, b, c$ | $\max_q(r)$ |
|---|---|---|---|---|
| start | 1, 2, 3 | 3 | 11, 12, 13 | 13 |
| $p$ gossips with $r$: $r$ sends its oldest delta above 3, which is $a$ at 21 | 21, 2, 3 | 21 | 11, 12, 13 | 13 |
| $q$ gossips with $r$: $r$ sends $a$ at 21 | 21, 2, 3 | 21 | 21, 12, 13 | 21 |
| $p$ gossips with $q$ | 21, 2, 3 | 21 | 21, 12, 13 | 21 |

In the last exchange both digests say 21 for $r$, so neither sends anything for $r$, although $q$ has newer copies of $b$ and $c$ than $p$. This is correct: $r$ has already written $b$ and $c$ again, at 22 and 23, so the copies at $q$ are also stale, and sending them would use space in the message for values that must be replaced anyway. The invariant still holds: every key that $p$ or $q$ does not have in its current form has a version above 21. The test `test_figure_1_style_example` runs this case.

**What goes wrong without the order.** Suppose that in the first step $r$ sent $c$ at 23 instead of $a$ at 21. Then $\max_p(r) = 23$, and from then on every partner sends $p$ only deltas of $r$ with versions above 23. So $p$ never receives $a$ at 21 or $b$ at 22, and its copy of $r$ stays wrong for ever.

**A run under load.** The simulator has $n = 24$ participants with $K = 6$ keys each. In each of the first 20 rounds, 16 writes go to random keys of random participants; then the writes stop. In each round every participant gossips once with a random partner. The table gives the mean over seeds 0 to 4 of the number of stale mappings at the end of round 20 (a mapping $\mu_p(r)(k)$ is stale when it differs from $\mu_r(r)(k)$), and the range of the first round at whose end no mapping is stale.

| Order | $mtu = 8$: stale after round 20 | all equal at round | $mtu = 12$: stale after round 20 | all equal at round |
|---|---|---|---|---|
| scuttle-depth | 683 | 24 to 25 | 451 | 23 to 24 |
| scuttle-breadth | 828 | 25 to 27 | 502 | 23 to 24 |
| precise-oldest | 931 | 26 | 536 | 23 to 24 |
| precise-newest | 543 | 23 to 24 | 444 | 23 to 24 |

With messages of unbounded size (seed 1, scuttle-depth), the stale counts at the end of rounds 18 to 23 are 385, 401, 512, 195, 32 and 0, so the copies agree 3 rounds after the writes stop. In the simulator, the precise orders use the global write counter as the common clock.

The paper (Section 3.3, Figure 2) measures, with 128 participants and 64 keys each, the maximum staleness in seconds and the number of stale mappings. There, precise-newest has the fewest stale mappings but the largest maximum staleness, because old updates starve; precise-oldest has a better maximum staleness but many stale mappings; scuttle-depth does well on both. The simulator here counts stale mappings only. On that count it agrees with the paper: precise-newest has the fewest stale mappings and precise-oldest the most. It does not measure staleness in time, so it does not test the starvation result.

**Flow control.** With desired rates $\rho_p = 1$, $\rho_q = 3$ and maximum rates $\tau_p = 2$, $\tau_q = 4$, the sum $\rho_p + \rho_q = 4$ fits in $\tau_p + \tau_q = 6$, and the spare 2 is split: the new maxima are 2 and 4. With $\rho_p = \rho_q = 5$ the sum does not fit and both get $3$. With $\rho_p = 1$ and $\rho_q = 9$, $p$ keeps 1 and $q$ gets 5. In every case the sum stays 6. For the local rule with the parameters of the paper ($\varphi_1 = \varphi_2 = 3$, $\alpha = 0.75$, $\beta = 0.2$), a maximum rate of 10 falls to 7.5 after 3 exchanges in a row with an overflow, and then rises to 7.7 and 7.9 after two runs of 3 exchanges without one.

## Correctness

The proofs are in the proof file; here are the statements.

- **Every delta is news.** Each delta that a participant receives has a larger version than its copy of that key, so line L7 always changes the copy. (Proved.)
- **The invariant.** For all participants $p$ and $q$, the paper's invariant $C(p, q)$ holds at all times: for every key $k$ of $p$, either $\mu_q(p)(k) = \mu_p(p)(k)$, or the current version of $k$ at $p$ is larger than $\max_q(p)$. It holds at the start, a write at line L1 keeps it because the new version is larger than all others, and an exchange keeps it because of the ordering constraint. (Proved.)
- **Property (3).** If $\max_q(p) = \max_p(p)$, then $\mu_q(p) = \mu_p(p)$. This follows from the invariant, since no key of $p$ has a version above $\max_p(p)$. (Proved.)
- **Convergence.** After the writes stop, and for every $mtu \ge 1$, all copies become equal after a finite number of rounds with probability 1. (Proved.)
- **Speed.** With $mtu \ge nK$, the participants whose copy of $r$ is current form a set that grows at least as fast as the informed set of [push-pull gossip](/push-pull-gossip/) for a rumor that starts at $r$. (Proved.) Push-pull informs all participants in $\log_3 n + O(\log \log n)$ rounds with high probability (Karp et al. 2000, cited). The bound of $O(\log n)$ rounds for all $n$ participants at once also needs a union bound over the $n$ rumors; that step is a sketch.

## Complexity

- **Messages.** One exchange has two digests of $n$ versions each and two sets of at most $mtu$ deltas, so $O(n + mtu)$ numbers and deltas per exchange, and $n$ exchanges per round. Precise reconciliation needs digests with one version per key, $O(nK)$.
- **Time.** With unbounded messages, $O(\log n)$ rounds after the writes stop, by the comparison with push-pull above. With a bounded $mtu$ and $B$ stale mappings when the writes stop, at least $B / (2 n \cdot mtu)$ more rounds are needed, because each round has $n$ exchanges with at most $2 \cdot mtu$ deltas, and each delta makes at most one mapping current.
- **Space.** Each participant keeps a copy of every state, $\Theta(nK)$ mappings, and $n$ maximum versions.
- **Local work.** The code builds $A(r)$ by a scan over all $nK$ mappings, $O(nK \log(nK))$ per exchange with the sort. Lists of the keys of each $r$ kept in version order make this $O(n + mtu)$ per exchange.

## Properties

- Randomized: the partner choice and the tie breaks of the orders use the seeded random generator.
- Single writer per state: only $r$ writes $\mu(r)$, so there are no write conflicts to resolve, only old and new versions.
- No wasted deltas: a delta is never sent to a participant that already has it (relative to the digest of the exchange).
- An exchange does not have to remove all differences, even when the message has room (Figure 1).
- The digest grows with $n$ and not with the number of keys.

## Variants and improvements

- **Scuttle-breadth.** The rank order described above; it is fair to all participants but did worse in the paper.
- **Precise reconciliation.** The per-key baseline of Section 3.1, with the oldest-first and newest-first orders.
- **Partial digests.** When $n$ is too large for one message, Section 3.2 suggests several messages, a reconciliation of the digest itself, or a pseudo-random subset of the participants in each digest, which works but slows the spread.
- **Fair sharing of capacity.** In Section 4.1, two partners exchange their desired rates $\rho$ and maximum rates $\tau$ and split $\tau_p + \tau_q$: if $\rho_p + \rho_q \le \tau_p + \tau_q$, each gets its desired rate plus half the spare; if both want at least half, each gets half; otherwise the one that wants less gets its desired rate and the other gets the rest. The sum never changes.
- **Local rate control.** In Section 4.2, a participant lowers its maximum rate to $\alpha \tau$ after $\varphi_1$ exchanges in a row in which a delta set was larger than $mtu$, and raises it to $\min(\tau + \beta, mtu)$ after $\varphi_2$ exchanges in a row in which both sets were smaller than $mtu$. This is [AIMD](/aimd/), as in TCP. The paper used $\varphi_1 = \varphi_2 = 3$, $\alpha = 0.75$ and $\beta = 0.2$.

## When to use it

Use it to replicate state that each node owns, such as load, health or membership data, on all nodes, when the gossip messages have a fixed size and the update rate can be high. It is a poor fit when many nodes write the same key (then a per-key method such as [version vectors](/version-vectors/) is needed) or when the data per node is so large that a full copy at every node is too much. For one large data set, compare hashes with a [Merkle tree](/merkle-tree/) or use [set reconciliation](/set-reconciliation/) instead.

## Pitfalls

- **Out-of-order sending.** Sending a newer delta of $r$ before an older one breaks the invariant, and the older one is then never sent (see the Example).
- **One counter per participant.** The version must be larger than every version the participant used for any key, not only for the same key. Per-key counters give equal versions to different keys, and the digest no longer tells what is missing.
- **A restart that forgets the counter.** If a participant restarts and writes with versions that are not above its old maximum, the other participants already have digests at least that high, and the new writes are never sent. Keep the counter in stable storage or start above every old version.
- **Overload.** When the participants write faster than the gossip can carry, the backlog grows and staleness has no bound; this is why the paper adds flow control.
- **Digest size.** The digest has one entry per participant, so in large groups it may not fit in one message.

## Implementations

The Python code keeps the full table $\mu_p$ at every participant, as dictionaries from key to (value, version), with a list of maximum versions. The message types are DIGEST and DELTAS. `select` builds the delta set for one partner with the scuttle-depth or the scuttle-breadth order and cuts it at $mtu$; `apply` merges a delta set. `exchange` does one push-pull exchange, and `precise_exchange` is the baseline. `simulate` runs seeded rounds with random writes and returns the stale counts. `invariant_holds` checks $C(p, q)$, and the tests check it, and property (3), after every exchange of a random run. `share_rates` and `Aimd` are the flow control rules of Section 4.

## History

Demers et al. (1987) introduced anti-entropy with push, pull and push-pull exchanges for the Xerox Clearinghouse, where two sites compare their databases and keep the newer entries. Van Renesse, Dumitriu, Gough and Thomas, at Amazon.com, presented Scuttlebutt at LADIS 2008. They noted that anti-entropy has a limited capacity under a fixed message size, proposed the per-participant digest with the ordering constraint, compared it with precise reconciliation in simulation, and added a flow control for anti-entropy.

## References
