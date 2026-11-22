---
tag: 53TPSG
kind: theorem
slug: sybil-impossibility-theorem
name: Douceur's Sybil theorem
aliases:
- Sybil impossibility
area: security-and-privacy/network-and-web-security
level: advanced
summary: Without a trusted authority, a system cannot prevent Sybil identities unless it makes unrealistic assumptions on resources and coordination.
history:
  year: 2002
  people: [John R. Douceur]
  note: Douceur proved the four lemmas at IPTPS 2002 in the paper that named the Sybil attack.
prereqs: [sybil-attack]
see_also: [sybil-attack, sybilguard, sybilrank, proof-of-work, byzantine-fault-tolerance, captcha, cryptographic-hash-function]
sources:
  - paper: "John R. Douceur, The Sybil attack, IPTPS 2002, LNCS 2429, pages 251 to 260"
    locator: Section 2 (the formal model), Section 3.1 (Lemmas 1 and 2, direct validation), Section 3.2 (Lemmas 3 and 4, indirect validation, and combined puzzles) and Section 5 (the three conditions)
  - paper: "Haifeng Yu, Michael Kaminsky, Phillip B. Gibbons and Abraham Flaxman, SybilGuard: defending against Sybil attacks via social networks, ACM SIGCOMM 2006, pages 267 to 278"
    locator: Section 1 (how a social network adds the trust that Douceur's model leaves out)
---

Douceur's Sybil theorem says that, in an open distributed system without a logically central trusted authority, a correct participant cannot prevent a faulty one from presenting many identities, unless every participant has nearly the same resources and all identities are tested at the same time by everyone. It is a set of four lemmas in Douceur's model of entities that talk through a broadcast medium. The result explains why defenses against the [Sybil attack](/sybil-attack/) need an authority, a resource assumption, or extra trust such as a social network.

## Statement

**The model** (Douceur, Section 2). The system has a set $E$ of entities, split into correct entities $C$, which follow the protocol, and faulty entities $F$, which may behave in any way within their resources. Entities send messages through a broadcast cloud: every message from a correct entity reaches all correct entities within a bounded time, but not necessarily in the same order. There are no direct links between entities, since a physical link would itself identify the remote entity. A security parameter $n$ bounds every entity's computation: every entity can do work polynomial in $n$, and none can do superpolynomial work, which allows public-key cryptography. An identity is an abstract name, such as the hash of a public key, that an entity presents. Each correct entity presents one identity; a faulty entity may present several. A fixed correct entity $l$ decides which identities to accept. Let $r_M$ be the resources of a minimally capable entity, the least needed to present one identity.

**Validation.** Entity $l$ accepts an identity either by direct validation, a test of the resources behind it, or by indirect validation: it accepts an identity that $q$ already accepted identities vouch for.

**Lemma 1.** If a faulty entity $f$ has resources $\rho$ times $r_M$, then $f$ can present $g = \lfloor \rho \rfloor$ distinct identities to $l$.

**Lemma 2.** If $l$ accepts identities that are not validated simultaneously, a single faulty entity can present an arbitrarily large number of distinct identities to $l$.

**Lemma 3.** If $l$ accepts any identity vouched for by $q$ accepted identities, a set $F$ of faulty entities can present an arbitrarily large number of distinct identities to $l$ if $|F| \ge q$, or if the total resources of $F$ are at least those of $q + |F|$ minimally capable entities.

**Lemma 4.** If the correct entities do not coordinate the time intervals in which they accept identities, and $l$ accepts any identity vouched for by $q$ accepted identities, then even a minimally capable faulty entity can present $g = \lfloor |C| / q \rfloor$ distinct identities to $l$.

**The conclusion** (Section 5). Without an identification authority, $l$ can limit the identities of faulty entities only if (1) all entities operate under nearly identical resource constraints, (2) all presented identities are validated simultaneously by all entities, coordinated across the system, and (3) when identities are accepted by vouching, the number of vouchers required exceeds the number of faulty entities in the whole system. Douceur argues that these conditions are neither justifiable as assumptions nor realizable in a large system; this last step is an argument about practice, not part of the theorem.

## In plain words

Imagine a town where nobody has an identity card and people talk only by shouting into a public square. A newcomer says "I am Bob". The only way to check that two voices belong to two people is to give each a task that one person could not do twice. But a strong person can do the task for several names. If the tasks are not given to everyone at once, a cheater can do them one after another under new names. If the town lets known members vouch for newcomers, a few cheaters can vouch for each other's fake names, and even a weak cheater can collect vouches from different groups at different times. The checks work only if everyone is equally strong, everyone is tested at the same moment, and the vouching rule asks for more vouchers than there are cheaters.

## Proof

**Lemma 1.** By the definition of $r_M$, $g$ minimally capable entities can present $g$ identities, so $g r_M$ resources are enough to present $g$ identities. Since $\rho \ge g$, the entity $f$ has at least $g r_M$ resources, so it can present $g$ identities to $l$.

**Lemma 2.** Entity $f$ presents identities one after another. It passes the test for the first identity with its resources, which are then free again, and it uses them for the test of the next identity. Since $l$ does not require the tests to overlap in time, nothing bounds the number of identities. (For storage, $l$ can keep re-testing accepted identities and drop those that fail later; Douceur notes that this ties up most of each entity's storage.)

**Lemma 3.** Let $r_F$ be the total resources of $F$ and $r_k$ those of the faulty entity $f_k$. Each $f_k$ can present $\lfloor r_k / r_M \rfloor \ge 1$ identities by Lemma 1, so $F$ can present $\sum_k \lfloor r_k / r_M \rfloor$ identities. If $|F| \ge q$, this is at least $|F| \ge q$. In the second case,

$$
q + |F| \le \frac{r_F}{r_M} = \sum_{f_k \in F} \frac{r_k}{r_M} < \sum_{f_k \in F} \left( \left\lfloor \frac{r_k}{r_M} \right\rfloor + 1 \right) = \sum_{f_k \in F} \left\lfloor \frac{r_k}{r_M} \right\rfloor + |F| ,
$$

so $\sum_k \lfloor r_k / r_M \rfloor > q$. In both cases $F$ can present at least $q$ identities that $l$ accepts by direct validation. These $q$ accepted identities can then vouch for any number of counterfeit identities, and $l$ accepts each of them.

**Lemma 4.** Partition $C$ into $g = \lfloor |C| / q \rfloor$ disjoint subsets $C_1, \ldots, C_g$, each with at least $q$ entities. Entity $f$ has $r_M$ resources. In a time interval $T_k$ it presents a new identity $i_k$ to every entity in $C_k$, using its $r_M$ resources, and passes their direct tests. The intervals $T_k$ for different $k$ do not need to overlap, because the correct entities do not coordinate their intervals, so the same $r_M$ resources are free again in each interval. Then at least $q$ entities of $C_k$ have accepted $i_k$ and vouch for it, for each $k$, so $l$ accepts all $g$ identities $i_1, \ldots, i_g$. $\blacksquare$

## Consequences

- **Amplification.** By Lemma 1 and Lemma 4, one faulty entity counts as $g$ identities. A protocol that tolerates a fraction $\varphi$ of faulty identities tolerates only a fraction $\varphi / g$ of faulty entities (Section 3.2). This is why [Byzantine fault tolerance](/byzantine-fault-tolerance/) in an open system needs a Sybil defense.
- **Resource tests need parity and simultaneity.** Computation tests such as [proof of work](/proof-of-work/) bound an attacker's identities by its share of total resources, which is a meaningful bound only when resources are spread evenly, the condition (1). Tests must also cover all identities at once, the condition (2).
- **Combined puzzles.** An entity can solve several of Douceur's computational puzzles with one search, which lets it answer concurrent challenges from many entities. If one challenger sends puzzles to several identities of the same entity, it detects the trick, because the combined solutions concatenate to the same string (Section 3.2).
- **Ways out.** A defense must add something the model lacks: a trusted authority for certificates; trust in a social network, where an edge is a real relationship that the attacker cannot create at will, as in [SybilGuard](/sybilguard/) and [SybilRank](/sybilrank/); or human effort, as in a [CAPTCHA](/captcha/), on the heuristic that human effort is spread more evenly than computation.

## Tightness

The lemmas are lower bounds on what a faulty entity can do. Matching upper bounds hold only when the conditions of Section 5 hold. For storage, an entity with $\rho r_M$ storage cannot pass more than $\lfloor \rho \rfloor$ simultaneous tests that each demand $r_M$ incompressible, unique data, because every stored bit serves only one challenger; so Lemma 1 is tight for simultaneous storage tests (an information-theoretic argument that Douceur sketches in Section 3.2, not one of the lemmas). Communication tests are weaker, because in the broadcast model one reply can answer many challengers at once. The bound $\lfloor |C| / q \rfloor$ of Lemma 4 is what the partition construction achieves; the paper does not prove that a minimally capable entity can do no better. The conclusion that the conditions are unrealistic is a heuristic about large systems, not a theorem.

## History

Douceur, at Microsoft Research, wrote the paper after Miguel Castro raised the question, and presented it at the first International Workshop on Peer-to-Peer Systems (IPTPS) in 2002. The name, suggested by Brian Zill, refers to the 1973 book Sybil by Flora Rheta Schreiber. The result shaped later work: SybilGuard (2006) and SybilLimit (2008) used social networks as the extra source of trust, and open blockchains rely on proof of work or stake, which assumes the resource parity of condition (1) in the form of an honest majority of resources.

## References
