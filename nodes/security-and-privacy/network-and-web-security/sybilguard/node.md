---
tag: QFN0T8
kind: algorithm
slug: sybilguard
name: SybilGuard
aliases:
- random route Sybil defense
area: security-and-privacy/network-and-web-security
level: research
summary: Limits Sybil nodes by random routes on a social graph, since few attack edges link the Sybil region to honest nodes.
model: word-ram
complexity:
  vars: {n: the number of honest nodes, m: the number of edges, w: the route length, d: the degree of the verifier}
  time: {worst: O(w^2 m), average: O(w^2 m), best: O(w^2 m)}
  space: {extra: O(w m)}
properties: {decentralized: true, randomized: true, sybil_bound: g w per verifier}
history:
  year: 2006
  people: [Haifeng Yu, Michael Kaminsky, Phillip B. Gibbons, Abraham Flaxman]
  note: Yu, Kaminsky, Gibbons and Flaxman presented SybilGuard at ACM SIGCOMM 2006, the first defense against Sybil attacks that uses a social network.
prereqs: [sybil-attack, mixing-time, birthday-paradox]
see_also: [sybilrank, sybil-impossibility-theorem, random-permutation, bloom-filter, message-authentication-code, public-key-cryptography, small-world-network, byzantine-fault-tolerance]
sources:
  - paper: "Haifeng Yu, Michael Kaminsky, Phillip B. Gibbons and Abraham Flaxman, SybilGuard: defending against Sybil attacks via social networks, ACM SIGCOMM 2006, pages 267 to 278"
    locator: Section 2 (the guarantees on the number and size of Sybil groups), Section 3 (overview, convergence and back-traceability), Sections 4.3 to 4.5 (random routes, redundancy, registry tables, witness tables and verification), Sections 4.6 and 4.7 (Theorem 1 and the route length), Section 5.2 (incremental routing tables)
  - paper: "Haifeng Yu, Phillip B. Gibbons, Michael Kaminsky and Feng Xiao, SybilLimit: a near-optimal social network defense against Sybil attacks, IEEE Symposium on Security and Privacy 2008, pages 3 to 17, doi:10.1109/SP.2008.13"
    locator: the abstract and the conclusion (O(log n) Sybil nodes per attack edge, against O(sqrt(n) log n) for SybilGuard)
---

SybilGuard is a decentralized protocol that lets an honest node, the verifier, decide whether to accept another node, the suspect, in a peer-to-peer system that is open to the [Sybil attack](/sybil-attack/). It uses the social network of the users: an edge means a real trust relationship, so an attacker can create many identities but only a few edges, the attack edges, to honest users. Every node sends random routes of length $w$ along the graph, built from a fixed random [permutation](/random-permutation/) at each node, and a verifier accepts a suspect whose routes meet a majority of its own. Yu, Kaminsky, Gibbons and Flaxman showed that a verifier then accepts at most $g w$ Sybil identities when there are $g$ attack edges.

## In plain words

Each person in a network of friends keeps a fixed rule card: "if a message comes from this friend, pass it to that friend." Everyone sends a message along each of their friendships, and the message is passed on by the rule cards for a fixed number of steps. Each person on the way writes down who sent it.

To check a stranger, you ask whether the stranger's messages crossed the path of your own messages, and whether the person at the crossing really wrote the stranger's name down. Honest people's paths cross often, because they move among many honest friends. A cheater with many fake names has only a few real friends. All the fake names' messages must pass through those few friendships, and the fixed rule cards then send them along the same paths. So only a few fake names can ever be written down by honest people.

## The problem

**Input.** An undirected social graph whose nodes are identities. The honest region has $n$ honest nodes; the Sybil region holds every identity that the adversary creates, with any edges among them. There are $g$ attack edges between the two regions. Each pair of friends shares a secret edge key, used with a [message authentication code](/message-authentication-code/), so an honest node knows from which edge each message comes and can share at most one edge with the adversary per real friendship. Each node has a key pair of [public-key cryptography](/public-key-cryptography/); its public key is its identity. The route length is $w$.

**Adversary** (Yu et al., Section 2). The adversary controls every Sybil node, knows the whole graph, may deviate from the protocol in any way, and may send any tables over the attack edges. It cannot add attack edges, which need real trust, and cannot forge the edge keys or private keys of honest nodes.

**Output.** For a verifier $V$ and a suspect $S$: accept or reject. The goal is that honest verifiers accept most honest suspects and only a bounded number of Sybil identities.

## The algorithm

```pseudo id=main
SETUP(G, w)
L1  every node x picks a uniformly random permutation π_x of its edges: a route that enters x on edge i leaves on edge π_x(i)
L2  repeat w rounds
L3      for each directed edge (p, x), let (q, p) be the edge that π_p maps to (p, x)
L4          p sends R[p, x] ← [p] followed by the first w - 1 entries of R[q, p] to x
VERIFY(V, S)
L5  accepted ← 0
L6  for each of the deg(V) routes r of V, one along each edge of V, of w hops
L7      X ← the first node of r that appears in the witness lists sent by S
L8      if X exists and the key of S is in one of the registry tables of X: accepted ← accepted + 1
L9  accept S if and only if accepted ≥ deg(V) / 2
```

The table $R[p, x]$ is the registry table that $x$ keeps for its edge from $p$: entry $i$ is the identity whose route enters $x$ from $p$ at hop $i$. Lines L2 to L4 fill it by shifting, as in Section 4.5 of Yu et al. A node of degree $d$ performs $d$ random routes, one along each edge, so it is registered at every node on its routes. In the same way, witness tables propagate backward and tell each node the $w$ nodes on each of its own routes, which is what $S$ sends in line L7. A Sybil node may send any table in line L4; honest nodes still run lines L3 and L4.

## Example

Honest nodes $A$ to $F$ have edges $A$-$B$, $A$-$C$, $B$-$C$, $B$-$D$, $C$-$E$, $D$-$E$, $D$-$F$ and $E$-$F$. Sybil identities $X$, $Y$ and $Z$ have edges $X$-$Y$, $X$-$Z$ and $Y$-$Z$, and the only attack edge is $F$-$X$. Take $w = 3$. The routing tables of the honest nodes, drawn with seed 4 in the code, are:

| node | entered from, leaves to |
|---|---|
| $A$ | $B \to C$, $C \to B$ |
| $B$ | $A \to D$, $C \to A$, $D \to C$ |
| $C$ | $A \to A$, $B \to B$, $E \to E$ |
| $D$ | $B \to F$, $E \to B$, $F \to E$ |
| $E$ | $C \to D$, $D \to F$, $F \to C$ |
| $F$ | $D \to X$, $E \to E$, $X \to D$ |

The route of $A$ along its edge to $B$ visits $B$, then $D$ (since $B$ maps $A \to D$), then $F$: its witness list is $(B, D, F)$. The other route of $A$ is $(C, A, B)$.

The adversary sends the table $(X, Y, Z)$ over the attack edge into $F$. By its routing table, $F$ passes routes from $X$ on to $D$, so $D$ stores $(F, X, Y)$ for its edge from $F$. Then $D$ passes routes from $F$ on to $E$, so $E$ stores $(D, F, X)$. These $3 + 2 + 1 = 6$ entries are the only Sybil entries among the 51 entries of the honest registry tables, and they name only $X$, $Y$ and $Z$: $g w = 3$ names.

- **Honest suspect $E$.** The routes of $E$ are $(C, E, D)$, $(D, B, C)$ and $(F, E, C)$. The route $(B, D, F)$ of $A$ first meets them at $B$, whose table for its edge from $D$ is $(D, E, C)$ and contains $E$. The route $(C, A, B)$ first meets them at $C$, whose table for its edge from $E$ is $(E, F, E)$. Both routes accept, so $A$ accepts $E$.
- **Sybil suspect $Z$, claiming the route $(F)$.** The first route of $A$ meets $F$ at hop 3, and $F$ lists $Z$ in its table for the edge from $X$; the second route of $A$ never meets $F$. One route of two accepts, which is half, so $A$ accepts $Z$.
- **The same $Z$, claiming all honest nodes.** Both routes of $A$ now first meet the claim at hop 1, at $B$ and at $C$, and neither lists $Z$. $A$ rejects. The adversary picks its claim, so the bound below counts the worst claim.
- **Any other Sybil name $W$.** No honest table lists $W$, so every route of $A$ rejects it, whatever $W$ claims.

## Correctness

**Theorem 1 (back-traceability, honest region).** If every node follows lines L1 to L4, then for each hop $i$ from 1 to $w$, every directed edge is crossed at hop $i$ by exactly one route, and after $w$ rounds entry $i$ of $R[p, x]$ is the start of that route. A route that crosses some directed edge twice first repeats its own first edge.

**Theorem 2 (Sybil bound).** Against the adversary above, once the tables are stable (the adversary has sent the same table over each attack edge for $w$ rounds), the honest registry tables name at most $g w$ Sybil identities, and at most $w(w + 1) / 2$ entries are copied from each attack edge. An honest verifier, fewer than half of whose routes reach the Sybil region, accepts only those identities, so at most $g w$ Sybil identities, whatever the suspects claim. While the adversary changes its tables, old names can stay downstream for up to $w$ rounds.

The proofs are in [proofs/correctness.md](proofs/correctness.md). Theorem 2 is the size bound of Section 3 of Yu et al., "at most $g$ Sybil groups, each of at most $w$ nodes", in a form that holds for every protocol deviation by the Sybil nodes.

**Theorem (Yu et al., Theorem 1, cited).** For a connected, non-bipartite social network, a random walk of length $w$ from a uniformly random honest node crosses one of the $g$ attack edges with probability at most $g w / n$. With $w = \Theta(\sqrt{n} \log n)$ and $g = o(\sqrt{n} / \log n)$ this is $o(1)$. The theorem is about random walks; that it carries over to random routes is a heuristic, supported by the experiments of Yu et al.

**Heuristic (honest acceptance).** In a fast-mixing honest region (mixing time $O(\log n)$), a walk of $\Theta(\sqrt{n} \log n)$ steps holds about $\sqrt{n}$ nearly independent samples of the [stationary distribution](/stationary-distribution/), so two honest routes meet with probability $1 - o(1)$ by the [birthday paradox](/birthday-paradox/). Yu et al. give this as a high-level review of known results for random walks, not as a proof for random routes.

## Complexity

In the [word RAM](/word-ram/) model, with one word per identity:

- **Setup.** Each of the $w$ rounds of lines L2 to L4 copies $w$ entries for each of the $2m$ directed edges: $O(w^2 m)$ time over the whole network, and $O(w)$ words for each edge of a node. Per node of degree $d$, the tables hold $d w$ entries. Yu et al. estimate about 256 KB per registry table for $w = 2000$ and 1024-bit keys, and less with 160-bit hashes of the keys.
- **Verification.** $V$ walks its $\deg(V)$ witness lists of $w$ nodes and looks each node up in a hash set of the claimed nodes: $O(d w)$ expected time plus the size of the claim, and one query to each intersection node.
- **Updates.** Tables change only when users or edges are created or deleted, not when nodes go offline (Section 5).

## Properties

- **Convergence.** Two routes that cross the same directed edge at any hops follow the same path from then on, because each node forwards by a fixed table.
- **Back-traceability.** Because each table is a permutation, the edge out of a node fixes the edge in, so a route is fixed by one of its edges and the hop number.
- **Sybil groups.** Yu et al. group the accepted nodes by the intersection node and the edge into it. At most $g$ groups hold Sybil nodes, and each group has at most $w$ nodes.
- **Decentralized.** Each node keeps only its routing table, registry tables and witness tables, and talks only to its friends and to intersection nodes.
- **Not every honest node.** Honest nodes near attack edges have a higher chance that their routes enter the Sybil region; the majority rule of line L9 limits the harm.

## Variants and improvements

- **SybilLimit** (Yu, Gibbons, Kaminsky and Xiao, 2008) uses $\Theta(\sqrt{m})$ routes of length $\Theta(\log n)$ per node and registers keys on edges instead of nodes. It accepts $O(\log n)$ Sybil nodes per attack edge, against $O(\sqrt{n} \log n)$ for SybilGuard, and keeps the guarantee for $g = o(n / \log n)$ attack edges (theorem of Yu et al., 2008).
- **[SybilRank](/sybilrank/)** (2012) replaces random routes by a short power iteration of trust from honest seeds and ranks all accounts, for an operator who holds the whole graph.
- **Local choice of $w$** (Section 4.7). A node estimates the length at which two honest routes meet from short random walks, takes the median of several samples and sets $w$ to 2.1 times the median.
- **[Bloom filters](/bloom-filter/)** can summarize the witness tables sent in line L7 (Section 4.5).
- **Incremental routing tables** (Section 5.2). When an edge is added or deleted, a node changes its permutation so that only routes entering by one edge are redirected.

## When to use it

Use SybilGuard in an open peer-to-peer system without a central authority, when users can name a few real friends and exchange edge keys out of band, and when the honest social graph is fast mixing. It suits tasks that need a bound on Sybil identities per verifier, such as placing replicas or voting. It does not help when the adversary has compromised many honest nodes, since those already have real friends, and its bound becomes weak when $g$ approaches $\sqrt{n} / \log n$; SybilLimit is the better choice there.

## Pitfalls

- **Coin flips instead of tables.** If line L1 lets a node pick a fresh random next hop each time a route passes, routes from the Sybil region no longer merge after the attack edge, and each Sybil identity can reach a different part of the honest region. Fix the permutation once in line L1.
- **A table that is not a permutation.** If line L1 maps two incoming edges to the same outgoing edge, back-tracing is ambiguous, two routes compete for one registry entry in line L4, and Sybil groups are no longer bounded by $w$. Use a bijection in line L1.
- **Trusting the claim.** If line L8 accepts as soon as $X$ appears in the witness lists of $S$, a Sybil suspect claims every node and is accepted. Line L8 must also check that $X$ lists the key of $S$ in its registry tables.
- **Any route suffices.** If line L9 accepts when one route of $V$ accepts, a single route of $V$ that enters the Sybil region accepts every Sybil identity. Keep the majority threshold of line L9.
- **Wrong route length.** If line L2 runs far more than $\Theta(\sqrt{n} \log n)$ rounds, Sybil groups grow with $w$ and the verifier's routes enter the Sybil region more often; with too few rounds, honest routes do not meet and line L9 rejects honest suspects. Choose $w$ as in Section 4.7.

## Implementations

The code is a synthetic, single-process model on graphs of at most 60 nodes: identities are node names instead of public keys, and there are no messages, edge keys or signatures. A route of the verifier that reaches a Sybil node counts as accepting, the worst case. The tests reproduce the example, compare the registry tables with a forward walk of every route on 500 random graphs, check Theorem 2 against random forged tables and claims on 100 graphs with two regions, and measure honest acceptance: on three random 60-node graphs with $w = 16$, 1765 of 1770 sampled honest pairs, 99.7%, accepted each other (measurement).

## History

Douceur showed in 2002 that without a trusted authority a system cannot prevent Sybil identities under his resource model, the [Sybil impossibility theorem](/sybil-impossibility-theorem/). Yu, Kaminsky, Gibbons and Flaxman, at Intel Research Pittsburgh and Carnegie Mellon University, presented SybilGuard at SIGCOMM 2006 in Pisa. They added the trust of a social network to the model and tested the protocol on a synthetic social network with one million nodes, where they used $w$ of about 2000. SybilLimit (2008) improved the bound by a factor of about $\sqrt{n}$, and later work such as SybilRank (2012) moved the idea to fake-account detection by operators.

## References
