---
tag: W8KBGE
kind: algorithm
slug: chord
name: Chord
aliases:
- Chord DHT
area: systems/networking-algorithms
level: advanced
summary: "A distributed hash table on a ring of m-bit identifiers. Each key goes to its successor node, and finger pointers at distances 1, 2, 4, ... find it in O(log n) hops."
solves: [overlay-lookup]
model: asynchronous-model
complexity:
  vars: {n: the number of live nodes, m: the number of bits of an identifier, r: the length of the successor list}
  time: {worst: O(m), expected: O(log n)}
  space: {extra: O(m + r)}
properties: {deterministic: true, online: true, recursive: false}
history:
  year: 2001
  people: [Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek, Hari Balakrishnan]
  note: Presented at ACM SIGCOMM 2001. Zave showed in 2012 that the original ring maintenance is not correct, and gave a corrected protocol with a proof in 2017.
prereqs: [overlay-lookup, consistent-hashing, binary-search]
see_also: [kademlia, hash-ring, virtual-nodes, rendezvous-hashing, skip-list, churn, membership-management, kleinberg-small-world-model]
sources:
  - paper: doi:10.1145/383059.383071
    title: Ion Stoica, Robert Morris, David Karger, M. Frans Kaashoek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup service for Internet applications, ACM SIGCOMM 2001
    locator: pages 149 to 160; Section 4.3 (the finger table and Theorem 2, O(log N) nodes contacted w.h.p.), Section 4.4 (joins, Theorem 3), Section 5 (stabilization, successor lists, Theorems 7 and 8), Section 6.3 (mean path length about one half of log2 N)
  - paper: doi:10.1109/TNET.2002.808407
    title: Ion Stoica, Robert Morris, David Liben-Nowell, David R. Karger, M. Frans Kaashoek, Frank Dabek and Hari Balakrishnan, Chord, a scalable peer-to-peer lookup protocol for Internet applications, IEEE/ACM Transactions on Networking 11(1), 2003
    locator: pages 17 to 32 (the journal version, with the successor list and failure handling in full)
  - paper: doi:10.1145/2185376.2185383
    title: Pamela Zave, Using lightweight modeling to understand Chord, ACM SIGCOMM Computer Communication Review 42(2), 2012
    locator: the Alloy model of the original ring maintenance and its counterexamples
  - paper: doi:10.1109/TSE.2017.2655056
    title: Pamela Zave, Reasoning about identifier spaces, how to make Chord correct, IEEE Transactions on Software Engineering 43(12), 2017
    locator: pages 1144 to 1156; the join, stabilize and rectify operations, the operating assumption, the invariant with r + 1 principal nodes, and the proof
  - paper: doi:10.1145/571825.571863
    title: David Liben-Nowell, Hari Balakrishnan and David Karger, Analysis of the evolution of peer-to-peer systems, ACM PODC 2002
    locator: pages 233 to 242 (Chord under churn, the half-life and its lower bound on maintenance)
---

Chord is a [distributed hash table](/overlay-lookup/) by Stoica, Morris, Karger, Kaashoek and Balakrishnan (2001). Nodes and keys get $m$-bit identifiers on a ring modulo $2^m$, and a key belongs to its *successor*, the first node at or after it clockwise; this placement is [consistent hashing](/consistent-hashing/). To find the successor of a key without a global table, each node keeps a pointer to its next node and $m$ *fingers*, the successors of the points at distances $1, 2, 4, \ldots, 2^{m-1}$ ahead of it. A lookup jumps along the fingers, and each jump at least halves the distance that is left, so a lookup takes at most $m$ hops, and $O(\log n)$ hops with high probability for $n$ nodes with random identifiers. A periodic *stabilize* step repairs the successor pointers when nodes join and fail; the fingers only make lookups fast.

## In plain words

Put the numbers from 0 to 63 around a clock face. Each computer in the system takes one number, and each data item also gets a number. An item is kept by the first computer at or after its number, going clockwise.

Walking around the clock to find the keeper is slow with a million computers. So each computer also remembers who sits 1 step ahead, 2 steps ahead, 4 steps ahead, 8 steps ahead, and so on, up to half the clock. To find an item, a computer jumps to the remembered computer that is closest before the item without passing it, and that computer does the same. Each jump cuts the distance that is left at least in half, as in binary search, so a few jumps are enough.

Computers come and go, so each one checks its next neighbour from time to time and repairs its pointers.

## The problem

Chord solves the [overlay lookup](/overlay-lookup/) problem on a ring. Identifiers are the integers modulo $2^m$; a node identifier is a hash of the node's address, and a key identifier is a hash of the key, so both are close to uniform. For identifiers $a$ and $b$, let $\mathrm{dist}(a, b) = (b - a) \bmod 2^m$, the clockwise distance. Write $(a, c)$ for the open arc of identifiers strictly after $a$ and strictly before $c$ clockwise (the whole ring without $a$ when $a = c$), and $(a, c]$ for that arc with $c$.

For the set $L$ of live nodes, $\mathrm{succ}(k)$ is the first node of $L$ at or after $k$ clockwise. The task is: given a key $k$ and any live node $n_0$, return $\mathrm{succ}(k)$, by messages between nodes, where each node keeps only a small routing table. Nodes join and fail at any time.

## The algorithm

**State of a node $v$.** A predecessor $v.\mathit{prdc}$; a successor list $v.\mathit{succ}$ of the next $r$ nodes on the ring, with the successor first; and fingers $v.\mathit{finger}[i] = \mathrm{succ}(v + 2^i)$ for $0 \le i < m$. So $v.\mathit{finger}[0]$ is the successor, and $v.\mathit{finger}[m-1]$ is the first node at least half the ring away. The paper numbers the fingers from 1, with finger $i$ equal to $\mathrm{succ}(v + 2^{i-1})$; this page numbers them from 0.

```pseudo id=main
FIND-SUCCESSOR(n₀, k)                       ▷ the first live node at or after key k
L1  n ← n₀
L2  s ← the first live entry of n.succ
L3  while k ∉ (n, s] do                     ▷ when k ∈ (n, s], no live node is in (n, s)
L4      n ← CLOSEST-PRECEDING(n, k)         ▷ one hop
L5      s ← the first live entry of n.succ
L6  return s

CLOSEST-PRECEDING(n, k)                     ▷ the known live node in (n, k) closest to k
L7  c ← n
L8  for each entry x of n.finger and of n.succ do
L9      if x is live and x ∈ (c, k) then c ← x
L10 return c

JOIN(x, w)                                  ▷ a new node x, with any live member w
L11 p ← the node n at which FIND-SUCCESSOR(w, x) stops   ▷ the last live node before x
L12 x.succ ← p.succ, x.prdc ← p, each finger of x ← the head of x.succ

STABILIZE(v)                                ▷ each live node runs it periodically
L13 drop the dead entries at the head of v.succ
L14 h ← the head of v.succ, v.succ ← [h] + the first r − 1 entries of h.succ
L15 y ← h.prdc
L16 if y is live and y ∈ (v, h) then v.succ ← [y] + the first r − 1 entries of y.succ
L17 RECTIFY(the head of v.succ, v)           ▷ notify the successor

RECTIFY(u, v)                               ▷ v tells u that v may be its predecessor
L18 if u.prdc is dead or v ∈ (u.prdc, u) then u.prdc ← v

FIX-FINGER(v, i)                            ▷ each live node runs it periodically
L19 v.finger[i] ← FIND-SUCCESSOR(v, (v + 2^i) mod 2^m)
```

**Lookup.** The current node $n$ checks if the key lies between itself and its successor $s$. If so, $s$ is the answer. If not, $n$ forwards the lookup to the node it knows that lies closest before the key, without passing it. In the *iterative* style, the node that started the lookup asks each node in turn for this next node; in the *recursive* style, each node forwards the request itself. Both send the same number of hops.

**Ring maintenance.** The maintenance on this page is the corrected protocol of Zave (2017). A new node $x$ asks any member to find the last node $p$ before $x$, and copies its successor list (lines L11 and L12). At this point no other node knows $x$. STABILIZE then does the work. A node $v$ drops failed nodes at the head of its list, copies the list of its successor $h$, and asks $h$ for its predecessor $y$. If $y$ lies between $v$ and $h$, then $y$ joined there, and $v$ takes $y$ as its new successor (line L16). Finally $v$ notifies its successor, which takes $v$ as its predecessor if $v$ is closer than the old one (line L18). FIX-FINGER refreshes one finger at a time, with a normal lookup.

**Keys.** When $x$ joins between $p$ and $s$, it takes from $s$ the keys in $(p, x]$, and no other key moves. When a node fails, its keys belong to its successor. Applications keep replicas of each key on the $r$ nodes of the successor list, so the successor of a failed node already has a copy.

## Example

Take $m = 6$ (identifiers 0 to 63), $r = 2$, and ten nodes 1, 8, 14, 21, 32, 38, 42, 48, 51, 56. Key 10 belongs to node 14, key 24 to node 32, key 38 to node 38 and key 54 to node 56.

The fingers of node 8 point at the successors of $8 + 1, 8 + 2, \ldots, 8 + 32$:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $8 + 2^i$ | 9 | 10 | 12 | 16 | 24 | 40 |
| finger | 14 | 14 | 14 | 21 | 32 | 42 |

Node 42 has fingers 48, 48, 48, 51, 1, 14 (for the points 43, 44, 46, 50, 58, 10), and node 51 has fingers 56, 56, 56, 1, 8, 21.

*Lookup of key 54 from node 8.* The successor of 8 is 14, and 54 is not in $(8, 14]$. The fingers of 8 that lie in $(8, 54)$ are 14, 21, 32 and 42; the closest to 54 is 42. At node 42, the successor is 48, and 54 is not in $(42, 48]$; the closest finger in $(42, 54)$ is 51. At node 51, the successor is 56, and $54 \in (51, 56]$. So the answer is 56, after 2 hops: $8 \to 42 \to 51$.

*Lookup of key 3 from node 42.* The successor 48 does not cover 3. The arc $(42, 3)$ wraps past 63, and the closest finger of 42 in it is 1 (finger 4, for the point 58). At node 1 the successor is 8, and $3 \in (1, 8]$. The answer is 8, after 1 hop.

*A join.* Node 45 joins through node 8. The lookup for 45 stops at node 42, so 45 copies the list $[48, 51]$ of node 42 and sets its predecessor to 42. Then the nodes stabilize in the order 45, 42, 38:

| step | 38.succ | 42.succ | 45.succ | 48.prdc |
|---|---|---|---|---|
| after the join | [42, 48] | [48, 51] | [48, 51] | 42 |
| 45 stabilizes, notifies 48 | [42, 48] | [48, 51] | [48, 51] | 45 |
| 42 stabilizes, sees 48.prdc = 45 | [42, 48] | [45, 48] | [48, 51] | 45 |
| 38 stabilizes | [42, 45] | [45, 48] | [48, 51] | 45 |

After these three steps the ring is ideal again: each node lists the next two live nodes and points back at the one before it. Node 45 now owns keys 43 to 45, which move from node 48.

## Correctness

Correctness rests on the successor pointers, not on the fingers. If the first live entry of each node's successor list is the next live node, then each step of FIND-SUCCESSOR either stops with the right answer or moves to a live node strictly closer to the key, with the successor itself as a fallback candidate. So the lookup ends and returns $\mathrm{succ}(k)$ for any fingers, even stale ones. If the fingers are also correct, each hop more than halves the distance to the last node before the key, which bounds a lookup by $m$ hops. For maintenance, one join or one failure on an ideal ring is repaired within about $r$ rounds of STABILIZE. The [proof](proofs/correctness.md) gives the four claims, and its last section explains what Zave (2017) proves for any interleaving of joins and failures.

## Complexity

The cost of a lookup is the number of hops, each one message (and its reply, in the iterative style).

- **Worst case with correct fingers:** at most $m$ hops, by the halving argument.
- **With random identifiers:** $O(\log n)$ hops with high probability (Stoica et al., Theorem 2). After $\log_2 n$ halvings the arc that is left has length about $2^m / n$, and such an arc holds $O(\log n)$ nodes with high probability.
- **Mean:** about $\frac{1}{2} \log_2 n$. A hop follows the finger of the highest bit of the remaining distance, so the number of hops is about the number of 1 bits in the distance to the target, which is half of about $\log_2 n$ significant bits (Stoica et al., Section 6.3). For random rings with $m = 32$, the mean number of forwarding hops is 2.55 at $n = 64$, 3.61 at $n = 256$, 4.61 at $n = 1024$ and 5.58 at $n = 4096$, and the largest observed is 10.
- **Without fingers:** a lookup walks the successor lists, which takes $\Theta(n / r)$ hops. With $n = 1024$ and $r = 4$ the mean is 128 hops.

**State.** Each node keeps $m$ fingers, but many are equal: in a random ring of 1024 nodes with $m = 32$, a node has 10.3 distinct fingers on average. It also keeps $r$ successors. Stoica et al. (Theorems 7 and 8) show that with $r = \Omega(\log n)$, if each node fails with probability $\frac{1}{2}$ at the same time, a lookup still returns the closest live successor with high probability, in $O(\log n)$ expected time.

**Joins.** A join takes one lookup, $O(\log n)$ hops. The original join of Stoica et al. also updates the fingers of the nodes that should now point at the new node, with $O(\log^2 n)$ messages with high probability (Theorem 3). With stabilization, those fingers are fixed lazily by FIX-FINGER.

## Properties

- **Correct with any fingers.** Lookups need only correct successor pointers; fingers only change the speed.
- **Asymmetric distance.** $\mathrm{dist}(a, b) \ne \mathrm{dist}(b, a)$ in general, so a node learns nothing useful for its own fingers from the lookups that pass through it. [Kademlia](/kademlia/) uses a symmetric distance to fix this.
- **Rigid tables.** Finger $i$ must be exactly $\mathrm{succ}(v + 2^i)$. A node cannot pick a closer node in network terms for the same entry.
- **Minimal key movement.** A join or a failure moves only the keys between two neighbours, as in [consistent hashing](/consistent-hashing/).
- **Load.** With one point per node, the largest arc, and so the largest share of keys, is $\Theta(\log n / n)$ of the ring with high probability; [virtual nodes](/virtual-nodes/) even it out.

## Variants and improvements

- **Proximity neighbour selection.** Let finger $i$ be any node in $[v + 2^i, v + 2^{i+1})$, not only the first one, and choose the one with the lowest network delay. Lookups keep the $O(\log n)$ bound and get faster.
- **Successor list and replication.** Keep $r = \Theta(\log n)$ successors and copy each key to them, as in the journal version.
- **Virtual nodes.** Run several Chord nodes on one machine to balance the load; see [virtual nodes](/virtual-nodes/).
- **Koorde.** Kaashoek and Karger replace the fingers by de Bruijn edges, which gives $O(\log n)$ hops with only 2 neighbours, and $O(\log n / \log \log n)$ hops with $O(\log n)$ neighbours. See the [overlay lookup](/overlay-lookup/) page.
- **Zave's corrected protocol.** The join, stabilize and rectify steps of this page, with a start from at least $r + 1$ nodes.

## When to use it

Use Chord when a set of peers with no central directory must agree on who stores which key, and the peers change over time. Chord is simple and easy to analyse, and it is a common base for teaching and for research systems. In deployed open networks [Kademlia](/kademlia/) is more common, because its lookups run in parallel, it learns routes from normal traffic, and it can choose low-delay nodes. Inside one data centre, where the membership is known, a [hash ring](/hash-ring/) with a full table on each node is simpler and needs one hop.

## Pitfalls

- **Starting from one node.** The original protocol starts a ring from a single node. Zave (2017) shows that this is not safe: a successor list can hold the same node twice, and then one failure cuts a node off. Start from at least $r + 1$ nodes, or watch the ring until it has grown.
- **Trusting a stale pointer.** The original stabilize can replace a pointer to a live node with a pointer to a dead one. Check that a node is live before you adopt it (lines L9, L16, L18).
- **Successor lists too short.** If all $r$ successors of a node fail before it stabilizes, the ring breaks. Choose $r$ and the stabilize rate for the failure rate.
- **Fingers as the source of truth.** A lookup that only follows fingers can skip the right node when a new node has joined. The last step must use the successor (lines L3 and L6).
- **Off-by-one in the arcs.** The answer test uses the half-open arc $(n, s]$, and the forward test the open arc $(n, k)$. With $k = n$ the arc $(n, n)$ is the whole ring without $n$.
- **Chosen identifiers.** If nodes can choose their identifiers, an attacker can take over the arc of a key. Derive the identifier from a [cryptographic hash](/cryptographic-hash-function/) of the address, and limit the identities per address.

## Implementations

## History

Stoica, Morris, Karger, Kaashoek and Balakrishnan presented Chord at ACM SIGCOMM 2001, at the same conference as CAN (Ratnasamy et al.), and a journal version with Liben-Nowell and Dabek appeared in IEEE/ACM Transactions on Networking in 2003. The placement of keys came from the consistent hashing of Karger et al. (1997); the new part was the finger table, which routes in a logarithmic number of hops with a logarithmic table. The papers give theorems about the correctness of the ring maintenance. Liben-Nowell, Balakrishnan and Karger (2002) analysed Chord under churn. In 2012 Pamela Zave modelled the ring maintenance in Alloy and found that it is not correct under its own assumptions. In 2017 she published a corrected protocol with a proof of correctness.

## References
