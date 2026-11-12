---
tag: Z8T5G5
kind: algorithm
slug: kademlia
name: Kademlia
aliases:
- Kademlia DHT
area: systems/networking-algorithms
level: advanced
summary: "A distributed hash table that measures distance between identifiers by XOR. Nodes keep k contacts per distance range and find the k closest nodes to a key by parallel queries."
solves: [overlay-lookup]
model: asynchronous-model
complexity:
  vars: {n: the number of live nodes, b: the number of bits of an identifier, k: the bucket size and replication parameter}
  time: {expected: O(log n)}
  space: {extra: O(b k)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 2002
  people: [Petar Maymounkov, David Mazières]
  note: Presented at the first International Workshop on Peer-to-Peer Systems (IPTPS 2002). Variants of it run the BitTorrent distributed hash table and other large open networks.
prereqs: [overlay-lookup, trie, metric-space]
see_also: [chord, consistent-hashing, hash-ring, rendezvous-hashing, ultrametric, lru, churn, membership-management]
sources:
  - paper: doi:10.1007/3-540-45748-8_5
    title: Petar Maymounkov and David Mazières, Kademlia, a peer-to-peer information system based on the XOR metric, Peer-to-Peer Systems (IPTPS 2002), LNCS 2429
    locator: pages 53 to 65; Section 2.1 (the XOR metric, page 56), Section 2.2 (k-buckets and the eviction rule, pages 56 and 57), Section 2.3 (the four calls and the node lookup with alpha, pages 57 to 59), Section 2.4 (the routing tree, pages 59 and 60), Section 3 (the sketch of proof, pages 62 and 63), Section 4.2 (accelerated lookups, page 64)
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, ACM SIGCOMM 2001
    locator: pages 149 to 160 (the ring and finger table that Kademlia compares itself with)
  - paper: doi:10.1007/3-540-45518-3_18
    title: Antony Rowstron and Peter Druschel, Pastry, scalable, decentralized object location and routing for large-scale peer-to-peer systems, Middleware 2001, LNCS 2218
    locator: pages 329 to 350 (routing by prefixes of digits of 2^b values, as in the accelerated lookups of Kademlia)
---

Kademlia is a [distributed hash table](/overlay-lookup/) by Petar Maymounkov and David Mazières (2002). Nodes and keys get $b$-bit identifiers ($b = 160$ in the paper), and the distance between two identifiers is their bitwise exclusive or, read as an integer. A key is stored on the $k$ nodes closest to it in this distance. Each node keeps one list of up to $k$ contacts, a *k-bucket*, for each range of distances $[2^i, 2^{i+1})$. To find the $k$ closest nodes to a key, a node asks the closest nodes it knows for the closest nodes they know, $\alpha$ requests at a time, until the $k$ closest nodes it has heard of have all answered. Each round fixes at least one more leading bit of the target, and a lookup takes $O(\log n)$ rounds for $n$ nodes with random identifiers.

## In plain words

Give every computer and every data item a long number written in binary. Two numbers are close when they start with the same bits: agreeing on the first ten bits is closer than agreeing on the first three.

Each computer keeps a short list of contacts for each level of closeness: a few computers that differ from it in the first bit, a few that agree on the first bit but differ in the second, and so on. So it knows many computers near itself and a few far away.

To find the computers closest to an item, ask the closest computers you know which computers they know that are closer still. Each answer brings you at least one more matching bit. You keep a few questions open at the same time, so a slow or dead computer does not hold you up.

## The problem

Kademlia solves the [overlay lookup](/overlay-lookup/) problem with the XOR distance. Identifiers are $b$-bit integers, and $d(x, y) = x \oplus y$. Node identifiers are random, and a key identifier is a hash of the key. For a target $t$ and the set $N$ of live nodes, the task is to find the $k$ nodes of $N$ closest to $t$, starting from any live node and using only messages between nodes. A value with key $t$ is stored on these $k$ nodes, so $k$ is also the replication factor. Nodes join and leave at any time, and some of them fail without notice.

## The algorithm

**The XOR metric.** $d(x, x) = 0$, $d(x, y) > 0$ for $x \ne y$, $d(x, y) = d(y, x)$, and $d(x, z) \le d(x, y) + d(y, z)$. It is also *unidirectional*: for a point $x$ and a distance $\Delta$ there is exactly one $y$ with $d(x, y) = \Delta$, namely $x \oplus \Delta$. The distance is small when the common prefix is long: if $x$ and $y$ first differ at bit $i$ (bits numbered from 0 at the low end), then $2^i \le d(x, y) < 2^{i+1}$. So the identifiers form the leaves of a binary [trie](/trie/), and the distance grows with the height of the lowest common subtree.

**The k-buckets.** A node $v$ keeps, for each $0 \le i < b$, a bucket of up to $k$ contacts $c$ with $2^i \le d(v, c) < 2^{i+1}$, the nodes that share the top $b - i - 1$ bits of $v$ and differ at bit $i$. Each bucket is in the order of the time last seen, with the oldest contact at the head. A node updates the bucket of the sender each time it receives any message (lines L1 to L5). A contact is evicted only when it does not answer a ping, so live old contacts stay. The paper chooses this rule because, in Gnutella traces, a node that has been up for a long time is more likely to stay up another hour. The rule also means that a flood of new identities cannot push out the old contacts.

**The lookup.** FIND_NODE asks a node for the $k$ contacts it knows closest to a target. The lookup keeps a shortlist $S$ of the nodes it has heard of. In each round it sends FIND_NODE to the $\alpha$ closest nodes of the shortlist that it has not asked yet, among the $k$ closest. The calls of one round run in parallel. A node that does not answer leaves the shortlist. If a round brings no node closer than the closest one seen, the next round asks all of the $k$ closest that have not been asked. The lookup stops when the $k$ closest nodes of the shortlist have all been asked and have answered.

```pseudo id=main
UPDATE(v, c)                                ▷ v received a message from contact c
L1  B ← the bucket of v with index i, where 2^i ≤ d(v, c) < 2^(i+1)
L2  if c ∈ B then move c to the tail of B
L3  else if |B| < k then append c at the tail of B
L4  else if the head h of B answers a PING then move h to the tail of B, drop c
L5  else remove h, append c at the tail of B

NODE-LOOKUP(u, t)                           ▷ the k live nodes closest to t
L6  S ← {u} ∪ the k contacts of u closest to t        ▷ the shortlist
L7  Q ← {u}, F ← ∅, best ← the node of S closest to t, width ← α
L8  loop
L9      K ← the k nodes of S closest to t, in order of distance
L10     C ← the first width nodes of K that are not in Q
L11     if C = ∅ then return K
L12     for each x ∈ C, in parallel do
L13         Q ← Q ∪ {x}
L14         if x answers FIND-NODE(x, u, t) with a list A then S ← S ∪ (A \ F), UPDATE(u, x)
L15         else S ← S \ {x}, F ← F ∪ {x}
L16     if the node of S closest to t is closer than best then best ← that node, width ← α
L17     else width ← k

FIND-NODE(x, u, t)                          ▷ runs at x, called by u
L18 UPDATE(x, u)
L19 return the k contacts of x closest to t
```

**The other calls.** PING checks that a node is live. STORE asks a node to keep a key and value; a node stores a value on the $k$ nodes that a lookup returns. FIND_VALUE is FIND_NODE, except that a node that has the value returns it, and the lookup then stops. The searcher then stores the value at the closest node it saw that did not have it, which caches popular values along the path. The node that published a value republishes it every 24 hours, and the $k$ nodes that hold it republish it every hour.

**Joins and refresh.** A new node $u$ must know one live node $w$. It puts $w$ in its buckets, runs NODE-LOOKUP for its own identifier, and then refreshes every bucket farther away than its closest neighbour, by a lookup for a random identifier in the range of the bucket. The lookups put $u$ into the buckets of the nodes they reach (line L18). A node also refreshes each bucket in which it has not done a lookup in the past hour.

**Defaults in the paper.** $b = 160$, $k = 20$ and $\alpha = 3$.

## Example

Take $b = 4$ (identifiers 0 to 15), $k = 2$, $\alpha = 2$ and eight nodes 1, 3, 4, 6, 9, 10, 12, 15. Node 3 is 0011 in binary, and its buckets are:

| bucket | distances | range | contacts |
|---|---|---|---|
| 0 | 1 | node 2, not present | none |
| 1 | 2 to 3 | 1 | 1 |
| 2 | 4 to 7 | 4, 6 | 4, 6 |
| 3 | 8 to 15 | 9, 10, 12, 15 | 9, 10 (the bucket is full) |

Node 3 looks up $t = 13$ (1101). The distances to 13 are:

| node | 1 | 3 | 4 | 6 | 9 | 10 | 12 | 15 |
|---|---|---|---|---|---|---|---|---|
| $d(\cdot, 13)$ | 12 | 14 | 9 | 11 | 4 | 7 | 1 | 2 |

So the answer must be 12 and 15.

*Start (lines L6 and L7).* The 2 contacts of node 3 closest to 13 are 9 and 10, so $S = \{3, 9, 10\}$ and $\mathit{best} = 9$.

*Round 1.* $K = [9, 10]$, and node 3 asks both in parallel. Node 9 (1001) knows 12 and 15 in its bucket 2, and it answers $[12, 15]$; node 10 answers the same. Now $S = \{3, 9, 10, 12, 15\}$, and 12 is closer than 9, so $\mathit{best} = 12$ and the width stays 2.

*Round 2.* $K = [12, 15]$, and neither has been asked. Node 12 answers $[15, 9]$ and node 15 answers $[12, 9]$. No node is closer than 12, so the width becomes $k = 2$.

*End.* $K = [12, 15]$ and both have answered, so the lookup returns $[12, 15]$ after 2 rounds and 4 FIND_NODE calls.

*The bucket rule.* When the answers of round 2 arrive, node 3 updates its bucket 3, which holds $[9, 10]$. For 12, the bucket is full, so node 3 pings the head 9; 9 answers, so it moves to the tail and 12 is dropped. The same happens for 15 with the head 10. Node 3 keeps its old contacts even though it has just met closer ones.

## Correctness

The [proof](proofs/correctness.md) has four parts. First, XOR is a metric, and the nodes that share a prefix form one consecutive block in the order of distance to any target. A bucket range is such a block. Second, the bucket rule never evicts a contact that answers. Third, if every bucket of every node holds $\min(k, \text{size of its range})$ live nodes of its range, the lookup returns exactly the $k$ closest nodes. If a missing node $y$ belonged to the result, take the node $x$ that answered and is closest to $y$; the bucket of $x$ that contains $y$ would put $y$, or a node of the same block, into the shortlist, and the block argument rules both out. Fourth, with only the weaker invariant of the paper, at least one contact in each bucket whose range has a node, the closest node of the shortlist moves into a smaller subtree around the true closest node in each round. So the lookup finds the closest node within $b$ rounds, and within $O(\log n)$ rounds with high probability for random identifiers.

## Complexity

**Rounds.** The analysis of the paper gives $\lceil \log n \rceil + c$ steps for most operations, for a small constant $c$. Each round of the lookup fixes at least one more leading bit of the closest node, and full buckets let a round fix several bits at once. For random networks with $b = 32$:

| $n$ | full buckets, $k = 20$, $\alpha = 3$: mean rounds | max | mean FIND_NODE calls | one contact per bucket, $k = \alpha = 1$: mean rounds | max |
|---|---|---|---|---|---|
| 64 | 2.17 | 3 | 19.7 | 2.92 | 6 |
| 256 | 2.61 | 3 | 20.2 | 4.03 | 8 |
| 1024 | 2.89 | 4 | 21.5 | 4.66 | 9 |
| 4096 | 3.20 | 4 | 22.4 | 5.92 | 11 |

With full buckets, all 300 lookups at each size returned the exact 20 closest nodes. With $k = \alpha = 1$ the lookup is greedy and asks one node per round; it then costs about the same as [Chord](/chord/), close to half of $\log_2 n$ hops plus one last call.

**Messages.** A round sends at most $\max(\alpha, k)$ calls. The lookup ends only after the $k$ closest nodes have answered, so it makes at least about $k$ calls, as the table shows.

**State.** A node has at most $b k$ contacts. With random identifiers, only about $\log_2 n$ buckets have contacts: in random networks with $k = 20$, a node has 10.36 non-empty buckets and 131.9 contacts on average at $n = 1024$, and 12.34 buckets and 171.7 contacts at $n = 4096$.

**Failures.** With 30% of 1024 nodes failed and the failed nodes left in the tables, no lookup returned a failed node, and all 300 lookups found the closest live node. Only 100 of them returned the exact 20 closest live nodes, because a dead contact takes the place of a live node in a full bucket until a ping finds it dead.

## Properties

- **Symmetric.** $d(x, y) = d(y, x)$, so the nodes that send queries to $v$ are the nodes that $v$ would like in its own buckets. Kademlia learns contacts from the lookups it serves, with no extra messages. [Chord](/chord/) measures distance one way round the ring and cannot do this.
- **Unidirectional.** All lookups for the same key converge on the same nodes near the end of their paths, which makes caching along the path work.
- **Prefix structure.** The bucket index, the position of the first differing bit, gives an [ultrametric](/ultrametric/) on identifiers: the node trie is the tree of this ultrametric.
- **Free choice inside a bucket.** Any node of the range is a valid contact. A node can prefer contacts with low delay or a long uptime without changing the bounds.
- **Parallel and fault tolerant.** With $\alpha > 1$, a slow or failed node delays a lookup by less than a timeout, and the lookup routes around it.
- **Live contacts are never evicted.** The bucket rule is [least recently used](/lru/) replacement, except that a contact that answers a ping stays.

## Variants and improvements

- **Routing tree (Section 2.4).** The table starts as one bucket for the whole space. When a full bucket gets a new contact and its range contains the own identifier, the bucket splits in two; otherwise the contact is dropped. The result is a bucket per common-prefix length, as above. The paper also keeps all valid contacts in a subtree of at least $k$ nodes around the own identifier, even if that needs buckets that do not contain it, so that a node knows its whole neighbourhood when the tree is unbalanced.
- **Accelerated lookups (Section 4.2).** Use digits of $2^\beta$ values, not bits: a bucket also splits when its depth is not a multiple of $\beta$. The table grows to about $2^\beta \log_{2^\beta} n$ buckets and a lookup takes about $\log_{2^\beta} n$ hops. The paper's implementation uses $\beta = 5$ (the paper calls this parameter $b$). This is the prefix routing of Pastry.
- **Replacement cache (Section 4.1).** Keep the new contacts that a full bucket drops in a side list, and use them when a contact goes stale, for example after 5 failed calls in a row, with exponential backoff.
- **Recursive and iterative styles.** The paper uses iterative lookups: the searcher talks to every node. Some implementations forward the request from node to node.
- **Hardened variants.** S/Kademlia adds identifiers that cost work to make and disjoint lookup paths, to resist nodes that choose their own identifiers and nodes that answer falsely.

## When to use it

Use Kademlia for an open peer-to-peer network with many nodes and frequent joins and failures: file sharing, content addressed storage, and node discovery in block chains. Its parallel lookups hide slow and dead nodes, and it keeps its tables full from normal traffic. When the full membership is known, a [hash ring](/hash-ring/) or [rendezvous hashing](/rendezvous-hashing/) with one hop is simpler and faster. When you need a simple structure to reason about, [Chord](/chord/) has fewer moving parts.

## Pitfalls

- **Small k.** The bucket rule only adds the nodes that a node hears from. With small $k$ and few lookups, a node may never hear from the nodes in some range. In a network of 401 nodes built by joins with $k = 2$ and $\alpha = 1$, the nodes had 180 empty buckets whose range was not empty, and 41 of 300 lookups missed the closest node. With $k = 4$ and $k = 20$ no bucket was empty and all lookups were exact. Refresh the buckets.
- **Stopping too early.** Stopping when a round brings nothing closer finds the closest node but can miss some of the $k$ closest. The paper's rule asks all of the $k$ closest before it stops (lines L11 and L17).
- **Dead nodes in the result.** Drop a node that does not answer and never add it back in the same lookup (the set $F$ of line L15), or the result can list a failed node.
- **Evicting old contacts.** A plain least recently used bucket drops the oldest contact, which is usually the most reliable one, and lets an attacker flush a bucket with new identities.
- **Chosen identifiers.** If nodes can choose their identifiers, an attacker can place many nodes next to a key and take over its $k$ replicas. Bind identifiers to addresses or make them costly.
- **Bit order.** Number the bits so that bucket $i$ holds the distances in $[2^i, 2^{i+1})$; with the opposite order, the prefix structure and the proofs no longer match the code.

## Implementations

## History

Petar Maymounkov and David Mazières, then at New York University, presented Kademlia at the first International Workshop on Peer-to-Peer Systems (IPTPS) in 2002. It came after [Chord](/chord/), CAN, Pastry and Tapestry, and shared with Pastry and Tapestry the idea of routing by prefixes of identifiers. The new part was the XOR metric: one symmetric distance gave one routing rule for the whole lookup, and let nodes learn contacts from the queries they serve. The paper also used measurements of Gnutella to choose an eviction rule that keeps long-lived contacts. Variants of Kademlia became the distributed hash tables of the eMule and BitTorrent file sharing networks, and later of IPFS and the node discovery of Ethereum.

## References
