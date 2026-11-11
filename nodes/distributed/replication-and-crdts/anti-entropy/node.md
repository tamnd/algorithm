---
tag: E24PC5
kind: algorithm
slug: anti-entropy
name: Anti-entropy
aliases:
- anti-entropy repair
- epidemic anti-entropy
- replica synchronization
- state reconciliation by gossip
area: distributed/replication-and-crdts
level: advanced
summary: Each replica regularly picks another one, finds where their states differ, for example with Merkle trees, and merges the differences, so all replicas converge in O(log n) rounds.
model: asynchronous-model
complexity:
  vars: {n: the number of replicas, d: the number of keys whose entries differ between two replicas, B: the number of buckets at the leaves of the Merkle tree}
  messages: {session: O(d log B)}
  time: {rounds: Θ(log n)}
  space: {extra: O(B)}
properties: {deterministic: false, recursive: false}
history:
  year: 1987
  people: [Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart, Doug Terry]
  note: Demers et al. named anti-entropy and analysed push, pull and push-pull exchanges for the Clearinghouse name service at Xerox PARC; Dynamo (2007) and Cassandra compare replicas with Merkle trees.
prereqs: [eventual-consistency, merkle-tree, last-writer-wins, random-phone-call-model]
see_also: [push-pull-gossip, rumor-mongering, gossip-protocol, death-certificates, scuttlebutt-reconciliation, set-reconciliation, read-repair, hinted-handoff]
sources:
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: the section on anti-entropy (push, pull and push-pull, the recurrences p_{i+1} = p_i^2 for pull and p_{i+1} ≈ p_i e^{-1} for push, checksums and recent update lists), the section on deletion and death certificates, and the section on spatial distributions
  - paper: doi:10.1137/0147013
    title: Boris Pittel, On spreading a rumor, SIAM Journal on Applied Mathematics 47(1), 213-223, 1987
    locator: the main theorem, push spreading in log2 n + ln n + O(1) rounds with high probability
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: the analysis of push-pull, log3 n + O(log log n) rounds, and the message bounds
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia and others, Dynamo, Amazon's highly available key-value store, Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220, 2007
    locator: Section 4.7 (handling permanent failures, replica synchronization with a Merkle tree per key range)
  - url: https://cassandra.apache.org/doc/latest/cassandra/managing/operating/repair.html
    title: Apache Cassandra documentation, Repair
    locator: repair compares replicas of token ranges with Merkle trees and streams the differences; full and incremental repair; running repair within the gc grace period
  - paper: doi:10.1007/3-540-48184-2_32
    title: Ralph C. Merkle, A digital signature based on a conventional encryption function, Advances in Cryptology (CRYPTO 1987), Lecture Notes in Computer Science 293, 369-378, 1988
    locator: the tree of hashes now called a Merkle tree
---

Anti-entropy is the background repair process of a replicated store. Every so often, each replica chooses another replica, the two compare their states, and they copy to each other what one has and the other lacks or has in an older version. The comparison is cheap when the replicas are almost equal: they compare a [Merkle tree](/merkle-tree/) of hashes over their keys, top down, and descend only where the hashes differ. The merge keeps the newer entry for each key, as in [last-writer-wins](/last-writer-wins/), with deletions kept as [tombstones](/tombstone/). Demers et al. (1987) named the process and showed that with random partners an update reaches all $n$ replicas in $O(\log n)$ rounds, and that "pull" and "push-pull" finish much faster than "push" at the end. Unlike [read repair](/read-repair/) and [hinted handoff](/hinted-handoff/), anti-entropy repairs every key, including keys that are never read and writes that no node knew were missed, so it is what guarantees convergence.

## In plain words

Two friends keep the same address book. Once a day, each calls a friend picked at random, and they compare. They do not read out every entry. They first compare a short fingerprint of the whole book. If it matches, they are done. If not, they compare fingerprints of the first half and the second half, then of quarters, and so on, until they find the few pages that differ, and they fix only those pages. For each entry, they keep the newer one.

A change made by one friend reaches everyone after a small number of days, because the number of people who know about it roughly doubles each day.

## The problem

Keep the replicas of a key-value store convergent: once writes stop and failures heal, all replicas must hold the same entry for each key, namely the newest one written. Replicas can miss writes for any reason: they were down, a message was lost, a hint was lost. The process must not need to know which writes were missed, and its cost should depend on how much the replicas differ, not on their size.

The model is the [asynchronous model](/asynchronous-model/) with message passing and [crash-recovery](/crash-recovery/) failures: replicas go down and come back with their stored state, and messages can be lost. The analysis of the number of rounds uses synchronous rounds in the [random phone call model](/random-phone-call-model/): in each round every replica calls one replica chosen uniformly at random.

## The algorithm

Each replica stores entries (stamp, value) per key; a stamp is a pair (time, replica id), and a deletion is an entry with value $\bot$. The key space is split into $B = 2^h$ buckets by a hash of the key, and each replica keeps a complete binary Merkle tree whose leaves hold the hashes of the buckets' contents and whose inner nodes hold the hash of their two children. Both replicas use the same buckets, so the trees have the same shape.

```pseudo id=main
ANTI-ENTROPY-ROUND at replica p, once per period
L1  q ← a replica chosen uniformly at random, other than p
L2  D ← MERKLE-DIFF(root of T_p, root of T_q)          ▷ the keys whose entries differ
L3  if mode is push or push-pull then for each k in D held by p: MERGE(q, k, entry_p(k))
L4  if mode is pull or push-pull then for each k in D held by q: MERGE(p, k, entry_q(k))

MERGE(x, k, e)
L5  if x has no entry for k, or e has a larger stamp, then x stores e for k and updates the hashes on the path to the root

MERKLE-DIFF(u, v)
L6  if hash(u) = hash(v) then return ∅
L7  if u and v are leaves then return the keys whose entries differ in the two buckets, a missing entry counting as different
L8  return MERKLE-DIFF(u.left, v.left) ∪ MERKLE-DIFF(u.right, v.right)
```

The merge of line L5 is commutative, associative and idempotent, so the result of any sequence of sessions does not depend on their order or on repeats. **Push** sends p's newer entries to q, **pull** fetches q's newer entries to p, and **push-pull** does both in one session. Without a Merkle tree, line L2 can compare a checksum of the whole state first and send everything when it differs, which is what Demers et al. describe; they also send a list of recent updates first, so that the checksums usually agree.

## Example

**A Merkle comparison.** Replicas A and B hold the same 2000 keys in $B = 4$ buckets, except that B missed one write to a key in bucket 3. The trees are numbered as in a heap: node 1 is the root, nodes 2 and 3 its children, and the leaves 4 to 7 cover buckets 0 to 3.

1. The roots differ, so compare nodes 2 and 3.
2. Node 2 is equal on both sides: buckets 0 and 1 hold the same data, and nothing below node 2 is sent.
3. Node 3 differs, so compare leaves 6 and 7. Leaf 6 is equal. Leaf 7 differs.
4. The replicas compare the entries of bucket 3 and find the one key. A sends its entry to B.

Five hashes were compared and one entry sent, in place of 2000 entries. With one differing key and $B = 2^h$ buckets, a comparison checks $1 + 2h$ nodes.

**The speed of spreading.** One replica out of $n$ has a new write, and all replicas run push-pull sessions. While few replicas have the write, each round roughly doubles or triples their number. At the end, pull is fast: if a fraction $p_i$ of the replicas lack the write, a replica still lacks it after its own pull only if it called another replica that lacks it, so $p_{i+1} = p_i^2$. Push is slow at the end: a replica that lacks the write gets it only if some replica calls it, so $p_{i+1} = p_i (1 - 1/n)^{n(1 - p_i)} \approx p_i e^{-1}$. For $p_i = 0.3$ and $n = 4000$, one round leaves about $0.09$ of the replicas without the write under pull, about $0.149$ under push, and about $0.045$ under push-pull. In the simulation, with $n = 512$ the mean number of rounds is about 16.3 for push, against $\log_2 n + \ln n \approx 15.2$, and about 8.4 for push-pull.

## Correctness

**Convergence.** Suppose writes stop, every replica recovers, and every pair of replicas keeps having sessions, which happens with probability 1 when partners are random. Then every replica ends with, for each key, the entry with the largest stamp written for that key.

*Proof sketch.* The entries for a key are totally ordered by stamp, and line L5 replaces an entry only by a larger one, so the entry of each replica only grows and is always one of the entries written. MERKLE-DIFF returns every key whose entries differ (below), so after a push-pull session between $p$ and $q$ both hold the larger of their two entries for every key. Let $e^*$ be the largest entry for key $k$, held by replica $r$. Each replica $x$ eventually has a session with $r$, or with a replica that already has $e^*$, after which $x$ holds $e^*$ and keeps it. With push only or pull only, the same holds as long as each replica is eventually the receiving side of a session with a holder of $e^*$. $\square$

**Exactness of the Merkle comparison.** Assume that the hash has no collisions on the data compared. Two subtrees with equal root hashes then have equal contents, so line L6 skips no difference. Line L7 compares entries exactly. A key with different entries lies in exactly one bucket, and every node on the path from the root to that leaf has different hashes, so line L8 reaches the leaf. Hence MERKLE-DIFF returns exactly the keys whose entries differ. With a $b$-bit hash, the chance that a difference is missed is about $2^{-b}$ per compared node.

**Rounds.** For push alone, Frieze and Grimmett (1985) and Pittel (1987) showed that a rumor reaches all $n$ nodes in $\log_2 n + \ln n + O(1)$ rounds with high probability. For push-pull, Karp et al. (2000) showed $\log_3 n + O(\log \log n)$ rounds. The full arguments and the derivation of the two recurrences are in the proof file and in [push rumor spreading time](/push-rumor-spreading-time/).

## Complexity

- **Per session.** With $d$ differing keys, the Merkle comparison visits at most $1 + 2 d \log_2 B$ nodes and sends the entries of at most $d$ buckets. When the replicas agree, it sends one hash. Without a tree, a checksum costs one hash when replicas agree and a full state transfer when they do not.
- **Rounds.** $\Theta(\log n)$ rounds until a write reaches all replicas, about $\log_2 n + \ln n$ for push and $\log_3 n + O(\log \log n)$ for push-pull.
- **Total traffic.** Every replica starts one session per round, so the cluster sends $\Theta(n)$ session requests per round whether or not anything changed; with Merkle trees the cost of a session with nothing to repair is one hash.
- **Space.** A tree has $2B - 1$ hashes. With buckets of about $k/B$ keys for $k$ keys, an update rehashes one bucket and $h = \log_2 B$ inner nodes.

## Properties

- **Repairs every key.** Unlike read repair, it repairs keys that are never read, and unlike hinted handoff, it needs no record of which writes were missed.
- **Order independent.** The merge is a join, so sessions can run in any order, be repeated, or be lost, and the result is the same.
- **Randomized.** Partners are random, which gives $O(\log n)$ rounds with high probability and needs no fixed topology. The rounds bound is probabilistic, so the algorithm is not deterministic.
- **Background cost.** Sessions run even when nothing has changed. Comparing trees is cheap, but building them can need a scan of the data.
- **Deletes need tombstones.** Without them, a session copies a deleted key back from a replica that still has it; see [death certificates](/death-certificates/).

## Variants and improvements

- **Rumor mongering.** Spread only new updates, and stop when a replica finds that its partners already know them. It is cheaper but can leave some replicas without an update, so it runs together with anti-entropy as a backup. See [rumor mongering](/rumor-mongering/).
- **Merkle trees per key range.** Dynamo keeps one tree per key range that a node holds and compares it with the other replicas of that range (Section 4.7). Cassandra's repair builds Merkle trees for the token ranges shared by the replicas and streams the parts that differ.
- **Version vectors and digests.** Exchange a summary of which updates each replica has, for example per writer the highest sequence number, and send only the missing updates. See [Scuttlebutt reconciliation](/scuttlebutt-reconciliation/) and [version vectors](/version-vectors/).
- **Set reconciliation.** Compute the symmetric difference of two sets with communication close to its size, without a tree. See [set reconciliation](/set-reconciliation/).
- **Spatial distributions.** Demers et al. choose partners with a bias toward nearby replicas, which cuts the traffic on long links while keeping convergence fast.
- **State-based CRDTs.** Anti-entropy of whole states with a join is the way [state-based CRDTs](/state-based-crdt/) are kept in sync.

## When to use it

Use anti-entropy in every eventually consistent replicated store, as the repair path that guarantees convergence. Use Merkle trees when the data is large and replicas usually agree, so that a session costs little. Combine it with read repair and hinted handoff, which repair the common cases faster. It is not a way to get strong consistency: it says nothing about what a read sees before the replicas converge.

## Pitfalls

- **Dropping tombstones too early.** Wrong: remove tombstones after a fixed time without regard to repair. Right: a replica that was down longer still holds the deleted value, and the next session copies it back. Cassandra requires repair within gc_grace_seconds.
- **Different bucket boundaries.** Wrong: let each replica choose its own buckets. Right: the trees must cover the same key ranges, or every node differs.
- **Rebuilding trees on each session.** Wrong: scan all data for every comparison. Right: keep the tree up to date on writes, or rebuild it on a schedule and accept that recent writes show up as differences.
- **Push alone at the end.** Wrong: rely on push to reach the last replicas. Right: the fraction that lacks an update falls only by a factor of about $e$ per round under push; use pull or push-pull.
- **Clock skew in the merge.** Wrong: compare wall clock stamps of writers whose clocks disagree. Right: the merge then keeps the wrong write on every replica; see [last-writer-wins](/last-writer-wins/).

## Implementations

The Python code keeps replicas with last-writer-wins entries and a Merkle tree over $2^h$ buckets, finds the differing keys by a top-down comparison, and runs push, pull and push-pull sessions. A separate function measures the number of rounds in the random phone call model.

## History

Demers et al. (1987) studied anti-entropy and rumor mongering for the Clearinghouse name service at Xerox PARC, where mail-based propagation of updates did not reach every server. They took the term "epidemic" from the theory of epidemics, analysed push, pull and push-pull, and introduced death certificates for deletions. Merkle (1987) introduced the tree of hashes for signatures. Frieze and Grimmett (1985) and Pittel (1987) gave the precise round count for push, and Karp et al. (2000) for push-pull. Dynamo (2007) used Merkle trees for anti-entropy between replicas of a key range, and Cassandra's repair does the same.

## References
