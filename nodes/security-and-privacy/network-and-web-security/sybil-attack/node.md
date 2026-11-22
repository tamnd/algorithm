---
tag: DNZFWQ
kind: concept
slug: sybil-attack
name: Sybil attack
aliases:
- Sybil identities
area: security-and-privacy/network-and-web-security
level: core
summary: One entity creates many identities in an open system to outvote or surround honest nodes.
history:
  year: 2002
  people: [John R. Douceur]
  note: Douceur named and analyzed the attack at IPTPS 2002. Brian Zill suggested the name, after the 1973 book Sybil about a woman with many personalities.
see_also: [sybil-impossibility-theorem, sybilguard, sybilrank, byzantine-fault-tolerance, proof-of-work, captcha, community-detection, trustrank]
sources:
  - paper: "John R. Douceur, The Sybil attack, IPTPS 2002, LNCS 2429, pages 251 to 260"
    locator: Section 1 (identities, redundancy and the name), Section 2 (the formal model), Section 3 (Lemmas 1 to 4 on direct and indirect validation) and Section 5 (the conditions needed without an authority)
  - paper: "Haifeng Yu, Michael Kaminsky, Phillip B. Gibbons and Abraham Flaxman, SybilGuard: defending against Sybil attacks via social networks, ACM SIGCOMM 2006, pages 267 to 278"
    locator: Section 1 and Section 3 (the social network model, attack edges and the honest and Sybil regions)
  - paper: "Qiang Cao, Michael Sirivianos, Xiaowei Yang and Tiago Pregueiro, Aiding the detection of fake accounts in large scale social online services, USENIX NSDI 2012, pages 197 to 210"
    locator: the deployment at Tuenti and its measurements
---

A Sybil attack is an attack on an open distributed system in which one entity presents many identities. Systems that spread work or votes over several identities, for redundancy or for fairness, assume that different identities belong to different entities; one entity with many identities breaks that assumption and can control a large share of the system. Douceur (IPTPS 2002) named the attack and proved, in the [Sybil impossibility theorem](/sybil-impossibility-theorem/), that without a trusted authority it cannot be ruled out except under unrealistic assumptions.

## In plain words

A club decides everything by a show of hands, and anyone may join by giving a name at the door. One person can come back many times with a new name each time, and soon that person has most of the hands in the room.

The club can ask for an identity card, which needs someone everybody trusts to issue cards. It can make joining cost time or money, which slows the cheater but does not stop a rich one. Or it can let members vouch only for people they really know, so that the cheater's fake members have few real friends inside the club.

## The idea

**The model** (Douceur, Section 2). Entities are the real participants: correct ones follow the protocol, faulty ones may do anything within their resources. Entities communicate through a broadcast cloud, and an identity is an abstract name, such as the hash of a public key, that an entity presents to others. A correct entity presents one identity; a faulty entity may present one legitimate identity and any number of counterfeit ones. A local entity wants to accept all legitimate identities and no counterfeit ones.

**Why redundancy fails.** A protocol that tolerates a fraction $\varphi$ of faulty identities, such as [Byzantine fault tolerance](/byzantine-fault-tolerance/) with $\varphi < 1/3$, tolerates only a fraction $\varphi / g$ of faulty entities when each faulty entity can present $g$ identities (Douceur, Section 3.2). Storage replicated on $r$ identities, chosen at random, can be held entirely by one entity.

**The three sources of trust** (Douceur, Section 3). An entity can learn about other identities from a trusted agency, from its own tests, or from other identities that vouch for them.

- **A trusted authority.** A certificate authority, a hardware key or a national identity issues one identity per entity. This works but needs a central party everyone trusts.
- **Resource tests.** Each identity must show some resource: computation, as in [proof of work](/proof-of-work/), storage, communication, or human effort, as in a [CAPTCHA](/captcha/). Douceur proved that an entity with $\rho$ times the minimal resources can always present $\lfloor \rho \rfloor$ identities, and that without simultaneous tests of all identities it can present any number (theorem, Lemmas 1 and 2). So tests help only if all entities have similar resources and all identities are tested at the same time.
- **Social trust.** Identities vouch for others they know. Social-graph defenses such as [SybilGuard](/sybilguard/) and [SybilRank](/sybilrank/) assume that honest users rarely befriend Sybil identities, so few attack edges join the Sybil region to the honest region, while the honest region is well connected. They bound the number of accepted Sybil identities by a function of the number $g$ of attack edges, not of the number of identities created.

**The adversary.** In every defense, the guarantee holds against an attacker with bounded resources: bounded computation for resource tests, no control of the authority for certificates, and few attack edges for social defenses. An attacker who breaks that bound, for example by buying many real accounts that already have honest friends, is outside the guarantee.

## Examples

**Votes and replicas.** A system has 100 honest identities, one per honest entity. One faulty entity adds $k$ identities. Each object is stored on 3 identities chosen uniformly at random, and the object is lost if all 3 are Sybil; it is corrupted by a majority vote if at least 2 are Sybil.

| Sybil identities $k$ | Sybil share of identities | all 3 replicas Sybil | at least 2 of 3 Sybil |
|---|---|---|---|
| 10 | 0.091 | 0.0006 | 0.0214 |
| 50 | 0.333 | 0.0356 | 0.2578 |
| 100 | 0.500 | 0.1231 | 0.5000 |
| 300 | 0.750 | 0.4208 | 0.8445 |
| 1000 | 0.909 | 0.7511 | 0.9769 |

The entity is still one of 101 entities, under 1%, but with 100 identities it controls half of all votes.

**Tolerance in entities.** A Byzantine agreement protocol tolerates a third of its identities being faulty. If identities are free, one faulty entity with 1000 identities in a system of 2000 identities already breaks it. If each identity costs one unit of a resource, and honest entities have 1 unit each, the attacker needs about half as many units as all honest entities together, which is the bound proof-of-work systems rely on.

**A social graph, abstract.** Honest users form a dense group. Sybil identities form another group of any size, and they connect to honest users only through the few friendships that honest users accept, the attack edges. A defense that walks or spreads trust from honest users along friendships rarely crosses those few edges, so it ranks or accepts few Sybil identities however many exist. The [SybilRank](/sybilrank/) page works such an example in numbers.

## Where it is used

- **Peer-to-peer systems and distributed hash tables.** Replication, routing tables and voting in open overlays are the setting of Douceur's paper.
- **Blockchains.** Proof of work and proof of stake are Sybil defenses by resource tests: influence follows computation or stake, not the number of identities.
- **Online social networks.** Fake accounts are Sybil identities. SybilRank was deployed at the Spanish social network Tuenti, where about 90% of the 200,000 lowest-ranked accounts were found to be fake (measurement, Cao et al.).
- **Reputation and recommendation.** Ratings, reviews and votes count identities, so they need Sybil resistance, for example through trust propagation such as [TrustRank](/trustrank/).
- **Anonymity networks and sensor networks.** Systems that pick relays or neighbors by identity limit how many identities one operator or one device may run.

## References
