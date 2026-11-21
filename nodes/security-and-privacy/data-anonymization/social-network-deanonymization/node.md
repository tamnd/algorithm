---
tag: YJBPHR
kind: technique
slug: social-network-deanonymization
name: Social network de-anonymization
aliases:
- seed-and-propagate graph matching
area: security-and-privacy/data-anonymization
level: research
summary: "Shows that a social graph with names removed can be re-identified at scale from its structure and a second overlapping network, so name removal does not protect graph data."
prereqs: [linkage-attack, simple-graph]
see_also: [active-attack-on-social-graphs, sparse-dataset-deanonymization, k-degree-anonymization, linkage-attack, differential-privacy-definition, entity-resolution, graph-isomorphism-problem, isotonic-regression]
sources:
  - paper: doi:10.1109/SP.2009.22
    title: "Arvind Narayanan and Vitaly Shmatikov, De-anonymizing social networks, IEEE Symposium on Security and Privacy (S&P 2009), pages 173-187"
    locator: the abstract and introduction (the threat model, the use of a second network as outside knowledge, the measurement on two public networks, and the claim that the method needs no created accounts and resists the defenses of that time)
  - paper: doi:10.1145/1242572.1242598
    title: "Lars Backstrom, Cynthia Dwork and Jon Kleinberg, Wherefore art thou r3579x? Anonymized social networks, hidden patterns, and structural steganography, WWW 2007, pages 181-190"
    locator: the earlier active and passive attacks on one anonymized copy of a graph
  - paper: doi:10.14778/1453856.1453873
    title: "Michael Hay, Gerome Miklau, David Jensen, Don Towsley and Philipp Weis, Resisting structural re-identification in anonymized social networks, PVLDB 1(1), 2008"
    locator: the models of structural knowledge and the defense by generalized graphs
  - paper: doi:10.1109/icdm.2009.11
    title: "Michael Hay, Chao Li, Gerome Miklau and David Jensen, Accurate estimation of the degree distribution of private networks, IEEE International Conference on Data Mining (ICDM 2009)"
    locator: the sorted degree sequence with sensitivity 2 under edge neighbors, the Laplace noise, and the constrained inference that makes the noisy sequence monotone
  - paper: doi:10.1007/s00778-010-0210-x
    title: "Michael Hay, Gerome Miklau, David Jensen, Don Towsley and Chao Li, Resisting structural re-identification in anonymized social networks, The VLDB Journal, 2010"
    locator: the journal version of the structural knowledge models and the generalized graph defense
---

Social network de-anonymization is the re-identification of people in a social graph that was released with the names removed, using only the shape of the graph and a second network that the attacker can see. Narayanan and Shmatikov (IEEE S&P 2009) showed that this works at large scale. With a public network as outside knowledge, they re-identified about one third of the users who could be verified to have accounts in both networks, with an error rate of 12%, although the two networks shared only a small part of their edges. The lesson for data release is that a social graph is identifying by itself, so removing names, and even the structural defenses of that time, do not make it safe to publish. This page describes the threat model, the published results and the defenses. It does not describe how the re-identification was done, and it gives no method to apply to a real graph.

## In plain words

Many people are in more than one network: an e-mail contact list, a photo-sharing site, a microblog. Their friends overlap across these networks. So the pattern of links around a person is a kind of fingerprint, even without a name. If a company releases one network with the names replaced by numbers, and another network with names is public, the two can be lined up, and the numbers get their names back. The protection must therefore come from what is released, not from removing the names.

## When it applies

The threat model of Narayanan and Shmatikov has these parts.

- **The release.** The operator of a network shares a version of the graph with the names removed, for example with advertisers, with researchers, or with third-party applications. The release may also be perturbed by a structural defense.
- **The outside knowledge.** The attacker has a second graph with identities, such as a different public network, whose members overlap with the released one. The two graphs need not be the same: people and links can be in one and not the other.
- **The goal.** The attacker wants to map nodes of the released graph to identities. Each correct mapping exposes the person's links and any attributes released with the node.
- **The power.** No accounts need to be created, unlike in the [active attack](/active-attack-on-social-graphs/). The attacker needs only data that is public or shared.
- **The limit.** The attack depends on the overlap between the two graphs and on the structure surviving the release. It does not apply to releases that contain only statistics computed with a formal guarantee.

## The template

The template is the abstract shape of the threat, with a named hole at each point where a defense can act. It is not a procedure, and it does not describe the matching method of the paper.

```pseudo id=main
PASSIVE-THREAT-SHAPE(released graph, outside knowledge)
L1  the attacker has a second graph with identities              ▷ hole AUX: what is public, and how much it overlaps
L2  the publisher releases the structure with names removed      ▷ hole RELEASE: graph, perturbed graph, or statistics only
L3  structure is compared across the two graphs                  ▷ hole AMBIGUITY: many nodes look alike under the release
L4  the attacker gets a partial mapping with some errors         ▷ hole DP: no single link or person changes the output much
```

- **AUX (line L1).** The publisher does not control what other networks expose. A release that is safe only if no similar data exists is not safe. This is the main lesson of the paper, and the same lesson as for [sparse datasets](/sparse-dataset-deanonymization/).
- **RELEASE (line L2).** Releasing aggregate statistics instead of the graph removes the structure that line L3 needs.
- **AMBIGUITY (line L3).** Structural anonymization, such as [k-degree anonymization](/k-degree-anonymization/) or the generalized graphs of Hay et al., makes a chosen kind of structural knowledge match at least $k$ nodes. Narayanan and Shmatikov argued, and supported with experiments, that the perturbations of the defenses of that time did not stop their method, because an attacker with a whole second graph uses more structure than the defenses model.
- **DP (line L4).** A differentially private release bounds what the output says about one link or one person, whatever the outside knowledge.

**Why the DP release is safe for the degree distribution (a theorem about the defense).** Hay, Li, Miklau and Jensen (ICDM 2009) release the degree sequence of a graph, sorted in non-increasing order, with noise. Two graphs are **edge neighbors** if they have the same $n$ nodes and differ in one edge. Adding the edge $\{u, v\}$ raises the degrees of $u$ and $v$ by 1 each, so the unsorted degree vectors differ by 2 in $L_1$ distance. Sorting does not increase $L_1$ distance between vectors of the same length, so the sorted sequences also differ by at most 2. The sensitivity is 2, and adding independent Laplace noise of scale $2/\varepsilon$ to each entry is $\varepsilon$-DP for edge neighbors by the [Laplace mechanism](/laplace-mechanism/). The true sorted sequence is non-increasing, so the publisher can replace the noisy answer by the closest non-increasing sequence, computed by [isotonic regression](/isotonic-regression/) with [pool adjacent violators](/pool-adjacent-violators/). This step reads only the noisy answer, so it keeps the guarantee, and the paper reports much lower error after it.

**An abstract example.** Take made-up nodes $p, q, r, s, w$ and edges $pq, pr, ps, qr, sw$. The degrees are $p: 3$, $q: 2$, $r: 2$, $s: 2$, $w: 1$, so the sorted sequence is $(3, 2, 2, 2, 1)$. Adding the edge $qw$ gives degrees $3, 3, 2, 2, 2$ and the sorted sequence $(3, 3, 2, 2, 2)$, at $L_1$ distance 2 from the first, as the bound says. The release is these five numbers with noise, not the graph, so there is no structure around a node to compare with a second network.

**Edge neighbors and node neighbors.** The guarantee above is for edge neighbors: it hides each link. Graphs are **node neighbors** if they differ in one node and all its edges. Under node neighbors, one person with $d$ links changes $d$ other degrees and adds or removes an entry of degree $d$, so the sensitivity of the degree sequence grows with the largest degree, up to about $2(n - 1)$. Hiding whether a person is in the network at all needs node-level privacy, which costs far more noise for the same statistics.

## Classic examples

- **The measurement of Narayanan and Shmatikov (2009).** With Flickr as outside knowledge, about one third of the users who could be verified to have accounts on both Twitter and Flickr were re-identified in an anonymized Twitter graph, with an error rate of 12%. The paper reports that the edge overlap between the two networks was under 15%. These are measurements on those networks at that time.
- **The earlier active and passive attacks.** The [active attack on anonymized social graphs](/active-attack-on-social-graphs/) of Backstrom, Dwork and Kleinberg (2007) showed that a single relabeled copy of a graph exposes links between chosen targets, but it needed accounts in the system before the release. The 2009 result removed that need.
- **Sparse tables.** Narayanan and Shmatikov had earlier shown that a few known items re-identify records in a large table of movie ratings with the names removed ([sparse dataset de-anonymization](/sparse-dataset-deanonymization/)). The graph result applies the same lesson to network data.
- **Record linkage.** Lining up two datasets about the same people is [entity resolution](/entity-resolution/). In a [linkage attack](/linkage-attack/), it is done against the people's wishes, and the quasi-identifier here is the structure of the graph.
- **Structural defenses.** [k-degree anonymization](/k-degree-anonymization/) and the generalized graphs of Hay et al. (2008, and the journal version of 2010) were designed against attackers who know a node's degree or neighborhood. They show both the value and the limit of defenses that model a fixed kind of knowledge.

## Variations

- **Attributes as well as structure.** A release that keeps profile attributes, such as a city or an age range, gives more to compare, and the attributes act as [quasi-identifiers](/quasi-identifier/).
- **Several releases.** Releasing new versions of a graph over time gives more structure to compare, much as in [m-invariance](/m-invariance/) for tables.
- **Mapping to communities instead of people.** Even a mapping with many errors can reveal which group a person is in, which may be sensitive.

## Pitfalls

- **Treating name removal as anonymization.** Relabeling keeps every edge. The structure is the identifier.
- **Assuming the outside data does not exist.** The safety of a release must not depend on the absence of other public networks; the attacker in the paper used a second public network.
- **Defending against one kind of structural knowledge only.** k-degree or neighborhood defenses protect against the knowledge they model. An attacker with a whole second graph is outside that model.
- **Confusing edge and node privacy.** Edge DP hides each link, not each person. A promise to protect people needs node-level privacy, with its much larger noise.
- **Reading a low error rate on some users as safety for the rest.** The measured re-identification covered a part of the users. The others are not shown to be safe; they may be re-identified with more outside data.

## Exercises

1. Prove that sorting does not increase $L_1$ distance: for vectors $x, y$ of length $n$ with sorted versions $x^{\downarrow}$ and $y^{\downarrow}$, $\|x^{\downarrow} - y^{\downarrow}\|_1 \le \|x - y\|_1$.
2. In the abstract example, remove node $w$ and its edge instead of adding $qw$. Pad the shorter sorted sequence with a 0 and compute the $L_1$ distance between the two sorted sequences. Compare it with the bound for node neighbors.

## References
