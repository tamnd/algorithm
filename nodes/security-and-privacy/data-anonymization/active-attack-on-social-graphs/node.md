---
tag: PWX4NG
kind: technique
slug: active-attack-on-social-graphs
name: Active attack on anonymized social graphs
aliases:
- Backstrom-Dwork-Kleinberg attack
area: security-and-privacy/data-anonymization
level: advanced
summary: "Shows that replacing names by random IDs does not protect a released social graph: a few accounts added before release let an attacker learn edges between chosen users."
prereqs: [linkage-attack, simple-graph]
see_also: [social-network-deanonymization, sparse-dataset-deanonymization, sybil-attack, k-degree-anonymization, linkage-attack, differential-privacy-definition, subgraph-isomorphism, graph-isomorphism-problem]
sources:
  - paper: doi:10.1145/1242572.1242598
    title: "Lars Backstrom, Cynthia Dwork and Jon Kleinberg, Wherefore art thou r3579x? Anonymized social networks, hidden patterns, and structural steganography, 16th International World Wide Web Conference (WWW 2007), pages 181-190"
    locator: the abstract and introduction (the threat model, the active, passive and semi-passive attacks, the number of created accounts needed in theory, and the measurement on a graph of 4.4 million nodes)
  - paper: doi:10.1145/2043174.2043199
    title: "Lars Backstrom, Cynthia Dwork and Jon Kleinberg, Wherefore art thou r3579x? Anonymized social networks, hidden patterns, and structural steganography, Communications of the ACM 54(12), 2011"
    locator: the later magazine version of the same results
  - paper: doi:10.14778/1453856.1453873
    title: "Michael Hay, Gerome Miklau, David Jensen, Don Towsley and Philipp Weis, Resisting structural re-identification in anonymized social networks, PVLDB 1(1), 2008"
    locator: the models of structural knowledge and the defense that publishes a generalized graph of supernodes with at least k nodes each
  - paper: doi:10.1109/icdm.2009.11
    title: "Michael Hay, Chao Li, Gerome Miklau and David Jensen, Accurate estimation of the degree distribution of private networks, IEEE International Conference on Data Mining (ICDM 2009)"
    locator: the release of the degree distribution under differential privacy with edge neighbors, and the improvement of the noisy answer by constrained inference
---

An anonymized social graph is a network of people and their links, such as friendships or e-mail contacts, released with each name replaced by a random identifier. Backstrom, Dwork and Kleinberg (WWW 2007) showed that this naive anonymization does not hide the edges. In their active attack, the attacker joins the network before the release and adds a few accounts and links of their own; after the release, the attacker can find these accounts again from the shape of the graph alone, and so learn whether chosen target users are linked to each other. The lesson for data release is that a relabeled graph keeps all of its structure, and structure identifies people. This page describes the threat model, the published results and the defenses at the level of the paper's abstract. It does not describe how to carry out the attack.

## In plain words

Removing names from a social graph is like shuffling the labels on a map: every road is still there. If an attacker can put a small, recognizable mark on the map before it is published, the attacker can find the mark afterwards and read off the roads near it. The fix is not a better shuffle. The publisher must either change the structure so that many places look the same, or release only statistics with a formal guarantee, such as [differential privacy](/differential-privacy-definition/).

## When it applies

The threat model of Backstrom, Dwork and Kleinberg has these parts.

- **The release.** The publisher releases one copy of the graph, with the nodes relabeled by random identifiers and the edges unchanged. No attributes are needed for the attack.
- **The goal.** The attacker picks some target users in advance and wants to learn whether there is an edge between pairs of them. A link between two people can be sensitive on its own, for example in an e-mail or a contact network.
- **The power.** In the active attack, the attacker can create accounts and links in the system before the data is collected. This is the [Sybil attack](/sybil-attack/) setting: one party controls several identities. Without that power, the passive and semi-passive variants below still apply.
- **The limit.** The attack needs the release to keep the structure that the attacker added. It does not apply to releases that change or hide that structure enough, or that release only noisy statistics.

The paper's title refers to this setting: the attacker hides a pattern in the graph, much as steganography hides a message in a file.

## The template

The template is the abstract shape of the threat, with a named hole at each point where a defense can break it. It is not a procedure. Each stage is named only at the level of the paper's abstract.

```pseudo id=main
ACTIVE-THREAT-SHAPE(system, release policy)
L1  before collection, the attacker adds structure to the graph    ▷ hole ADMISSION: account and link controls, Sybil detection
L2  the publisher replaces names by random identifiers             ▷ hole RELEASE: what the publisher puts out at all
L3  the release keeps the structure the attacker added             ▷ hole PERTURB: generalization, edge changes, noise
L4  that structure is distinct in the released graph               ▷ hole AMBIGUITY: each structure occurs in at least k places
L5  the attacker reads edges near the structure                    ▷ hole DP: the edge itself has bounded influence on the output
```

Each hole is a defense, and the attack needs all lines to go through.

- **ADMISSION (line L1).** If the system can stop one party from creating many linked accounts, the active variant fails. Sybil defenses are heuristics: they raise the cost but give no guarantee, and the passive variant does not need new accounts at all.
- **RELEASE (line L2).** The strongest choice is not to release the graph, and to answer queries about it instead.
- **PERTURB and AMBIGUITY (lines L3 and L4).** Structural anonymization changes the graph so that a given kind of structural knowledge matches at least $k$ nodes. [k-degree anonymization](/k-degree-anonymization/) does this for the degree of a node. Hay et al. (PVLDB 2008) publish a generalized graph in which nodes are grouped into supernodes of at least $k$ nodes each, with only the edge counts inside and between groups. These defenses protect against the knowledge they model. They say nothing about a structure that they do not model, and an active attacker chooses the structure.
- **DP (line L5).** If the output is produced by a mechanism that is $\varepsilon$-differentially private with edge neighbors, the presence of any single edge changes the probability of every output by a factor of at most $e^{\varepsilon}$, whatever the attacker added at line L1.

**Why the DP hole closes the threat (a theorem about the defense).** Two graphs are **edge neighbors** if they have the same nodes and differ in one edge. Let $M$ be $\varepsilon$-DP for edge neighbors, and let $G_1$ and $G_0$ be the graph with and without the edge $\{u, v\}$, with all other edges, including the attacker's own, the same. Any test that looks at the output of $M$ and says "edge present" on a set $S$ of outputs has

$$P[M(G_1) \in S] \le e^{\varepsilon} P[M(G_0) \in S].$$

So the true positive rate of any test is at most $e^{\varepsilon}$ times its false positive rate, and the attacker's prior odds that the edge exists change by a factor of at most $e^{\varepsilon}$. This holds for every set of edges that the attacker controls, because those edges are part of both $G_1$ and $G_0$. The guarantee is about one edge. It does not hide whether a person is in the network at all; that needs **node neighbors**, graphs that differ in one node and all its edges, which is a much stronger and costlier requirement (see Pitfalls).

## Classic examples

- **The original measurement (Backstrom, Dwork and Kleinberg, 2007).** On a social network of 4.4 million nodes, the paper reports that 7 created accounts were enough to learn on average about 2400 edge relations between targets. This is a measurement on one network.
- **The theory in the same paper.** The paper proves that on the order of $\sqrt{\log n}$ created accounts can suffice with high probability, under the assumptions of its analysis, where $n$ is the number of nodes. This is a theorem under those assumptions, not a measurement on a real network.
- **Re-identification without created accounts.** Narayanan and Shmatikov (IEEE S&P 2009) re-identified a large share of users of an anonymized graph using a second, public network as outside knowledge, with no accounts added. See [social network de-anonymization](/social-network-deanonymization/). It showed that the passive threat is practical at scale.
- **The same lesson for tables.** In [sparse dataset de-anonymization](/sparse-dataset-deanonymization/), a few known items re-identify a record in a large table with the names removed. In both cases, the data is identifying by itself, so removing the identifier column is not anonymization. This is the general [linkage attack](/linkage-attack/) setting.
- **The defense response.** [k-degree anonymization](/k-degree-anonymization/) (Liu and Terzi, 2008) and the generalized graphs of Hay et al. (2008) were designed against structural knowledge such as degrees and neighborhoods. Hay, Li, Miklau and Jensen (ICDM 2009) released the degree distribution with edge differential privacy and reported that the noisy answer becomes much more accurate after a post-processing step by by [isotonic regression](/isotonic-regression/), since a sorted degree sequence must be monotone.

## Variations

- **Passive attack.** The attacker creates nothing. A small coalition of existing users, who know their own links, find themselves in the released graph and then learn whether there are edges between other users they are linked to. The paper shows that this also works, but the attackers cannot choose their targets.
- **Semi-passive attack.** Existing users add a few links to targets before the release, without creating new accounts. The structure that the attack needs is then part of real accounts, which makes admission controls on new accounts useless.
- **Large-scale passive re-identification.** With a second, overlapping network as outside knowledge, the attacker needs no planted structure and no coalition. See [social network de-anonymization](/social-network-deanonymization/).

## Pitfalls

- **Treating relabeling as anonymization.** A random relabeling is a graph isomorphism: the released graph has exactly the same structure as the original. Any structure that occurs once in the original occurs once in the release. The fix is to change or hide the structure, or to release statistics under DP.
- **Defending against a fixed kind of knowledge only.** k-degree anonymity makes every degree shared by at least $k$ nodes, but an active attacker plants a structure that is larger than one degree, and the condition says nothing about it. A structural defense is only as good as its model of the attacker's knowledge, and the active attacker writes that knowledge.
- **Relying on Sybil detection.** Detecting fake accounts is a heuristic. It does not stop the passive and semi-passive variants, which use real accounts.
- **Confusing edge and node privacy.** Edge differential privacy protects each link, not each person. A person with many links can still be inferred to be in the network from aggregate statistics. Node differential privacy protects a person and all their links, but one node can change up to $n - 1$ degrees, so the noise needed for simple statistics such as the degree distribution is far larger.
- **Assuming one release is safe because it is the only one.** The attack needs only one copy of the graph. Releasing a graph "once, to trusted researchers" is still a release of the structure.

## Exercises

1. In the hypothesis test of The template, suppose a test says "edge present" with probability $0.9$ when the edge is there. With $\varepsilon = 0.1$, give a lower bound on the probability that it says "edge present" when the edge is absent.
2. Under node neighbors, adding one node joined to $d$ existing nodes changes the degree sequence. By how much can the $L_1$ distance between the two degree sequences, padded with a 0 for the new node in the smaller graph, grow? Compare it with the value 2 for edge neighbors.

## References
