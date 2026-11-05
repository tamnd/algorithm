---
tag: 7VYWRW
kind: concept
slug: structural-holes
name: Structural holes
aliases:
- Burt's structural holes
area: graphs/network-analysis
level: advanced
summary: Gaps between disconnected groups whose bridging nodes gain advantage.
prereqs: [ego-network, neighborhood, clustering-coefficient]
see_also: [weak-ties, triadic-closure, betweenness-centrality, ego-network, clustering-coefficient, structural-equivalence, bridge, centrality]
sources:
  - book: isbn:9780674843714
    title: Ronald S. Burt, Structural Holes, The Social Structure of Competition, Harvard University Press, 1992
    locator: Chapter 1 (the argument that brokerage across holes gives information and control benefits) and Chapter 2 (the measures of redundancy, effective size and constraint)
  - paper: doi:10.1086/421787
    title: Ronald S. Burt, Structural holes and good ideas, American Journal of Sociology 110(2), 349 to 399 (2004)
    locator: the study of managers in a supply-chain organization, in which those whose networks spanned structural holes had their ideas judged more valuable, with network constraint as the measure
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 3, Strong and weak ties (Section 3.5, closure, structural holes, and social capital)
---

A structural hole is a gap between two groups of people who are not connected to each other, and a person whose contacts lie on both sides of the gap spans it, as a broker. Burt (1992) argued that such brokers get earlier and more varied information and more control over what passes between the groups, and he measured how much a person's network spans holes by the *effective size* of the [ego network](/ego-network/) and by *network constraint*. Holes are the gaps that [weak ties](/weak-ties/) bridge, and they are the opposite of the closure produced by [triadic closure](/triadic-closure/).

## In plain words

Imagine two teams in a company that never talk to each other. Someone who knows people in both teams hears news from both sides, can carry ideas from one team to the other, and can decide what to pass on. The gap between the teams is a structural hole, and that person is a broker across it.

Compare two people with the same number of contacts. The first has contacts who all know each other: they share the same news, so most contacts repeat what the others say. The second has contacts who do not know each other: each one brings something new. Burt's measures count how much of a person's network is repetition and how much is reach across gaps. Studies found that people with more reach got better reviews, promotions and ideas, while groups with many closed ties were better at trust and cooperation.

## The idea

Let $G = (V, E)$ be an undirected graph without weights, and fix an *ego* $i$ with neighbourhood $N(i)$ of size $k$. A *structural hole* is a pair of contacts $j, q \in N(i)$ that are not adjacent; the ego is the only short link between them. The measures below look only at the ego network of $i$ ($i$, its contacts, and the ties among them), so they are defined for every vertex with $k \ge 1$, whether or not $G$ is connected.

**Proportional tie strength.** Let $p_{ij} = a_{ij} / \sum_q a_{iq}$ be the share of $i$'s ties that go to $j$; without weights, $p_{ij} = 1/k$ for every contact. For a weighted or directed network, Burt uses $p_{ij} = (z_{ij} + z_{ji}) / \sum_q (z_{iq} + z_{qi})$, with $z$ the tie strengths in both directions.

**Effective size.** The *redundancy* of contact $j$ is the share of $i$'s ties that go to contacts also tied to $j$. The effective size is the number of contacts minus their redundancy:

$$\mathrm{ES}(i) = \sum_{j \in N(i)} \Bigl(1 - \sum_{q \in N(i),\, q \ne j} p_{iq}\, m_{jq}\Bigr),$$

where $m_{jq} = a_{jq} / \max_r a_{jr}$, which is 1 or 0 without weights. For an undirected graph without weights this simplifies to

$$\mathrm{ES}(i) = k - \frac{2t}{k},$$

where $t$ is the number of ties among the contacts of $i$. It ranges from 1, when the contacts form a clique, to $k$, when no two contacts are tied. The *efficiency* is $\mathrm{ES}(i)/k$.

**Constraint.** Contact $j$ constrains $i$ when $i$ has put a large share of its ties into $j$, directly or through other contacts:

$$c_{ij} = \Bigl(p_{ij} + \sum_{q \in N(i),\, q \ne i, j} p_{iq}\, p_{qj}\Bigr)^2, \qquad C(i) = \sum_{j \in N(i)} c_{ij}.$$

Low constraint means many contacts that are not tied to each other: a network rich in holes. A single contact gives $C(i) = 1$. With $k$ contacts that are not tied to each other, $C(i) = 1/k$. Constraint grows when contacts are tied to each other and when ties are concentrated on few contacts, and it can be slightly above 1.

**Relation to other measures.** Constraint and effective size are both functions of the ego network, and so is the local [clustering coefficient](/clustering-coefficient/), which equals $t / \binom{k}{2}$: an ego with low clustering has high effective size. Spanning holes is a local form of [betweenness](/betweenness-centrality/), since the ego lies on the short paths between its unconnected contacts. When the ego has two or more contacts, a tie of the ego that is a local bridge (a tie whose ends have no common neighbour, a weaker form of a [bridge](/bridge/)) spans a hole, since that contact is tied to no other contact of the ego, and by the strong triadic closure argument of the [weak ties](/weak-ties/) page, such ties tend to be weak.

**Directed graphs, ties and components.** For a directed graph the measures use $p_{ij}$ with both directions combined, as above, so a one-way tie counts. Vertices with equal measures tie; a ranking breaks ties by the vertex number. An isolated vertex has no contacts, and its effective size and constraint are undefined.

## Examples

Take two closed groups, the triangle $\{1, 2, 3\}$ and the triangle $\{4, 5, 6\}$, and a person 0 tied to 1, 2 and 4. Persons 0 and 1 both have three contacts.

- **The broker 0.** Its contacts are 1, 2 and 4, with one tie among them (1 and 2), so $t = 1$ and $\mathrm{ES}(0) = 3 - 2/3 = 7/3$. Each $p_{0j} = 1/3$. For $j = 1$: $c_{01} = (1/3 + p_{02}\, p_{21})^2 = (1/3 + 1/9)^2 = 16/81$, and the same for $j = 2$; for $j = 4$, no other contact is tied to 4, so $c_{04} = 1/9$. So $C(0) = 41/81 \approx 0.506$.
- **The insider 1.** Its contacts are 0, 2 and 3, with ties 0-2 and 2-3, so $t = 2$ and $\mathrm{ES}(1) = 3 - 4/3 = 5/3$, and $C(1) = 83/108 \approx 0.769$.
- **The others.** Person 3, with the two tied contacts 1 and 2, has $\mathrm{ES} = 1$ and $C = 8/9 \approx 0.889$. Persons 5 and 6 have $C = 145/144 \approx 1.007$, above 1, because their two contacts are tied to each other and one of them, 4, is also tied to the broker 0.

Person 0 spans the hole between the two triangles: it has the lowest constraint in the graph and, with person 4, the largest effective size. Person 4 also spans the hole, but from the other side and with only one tie into the first group.

**Burt's managers.** In the supply-chain study of Burt (2004), the managers whose networks had low constraint were more likely to have their ideas for improving the supply chain judged valuable by senior managers, and the same paper reports that compensation, good evaluations and promotions also went disproportionately to people whose networks spanned holes.

**Non-examples.**

- A person with many contacts who all know each other (a clique) has high degree but effective size 1: the size of a network is not the same as its reach.
- A gap between two groups that no one spans is not a brokerage opportunity for anyone; a structural hole is defined relative to an ego whose contacts are on both sides.

## Where it is used

- **Social capital.** Burt's brokerage view against Coleman's closure view: holes give access to new information, closure gives trust and enforcement of norms. Studies use constraint as the measure of brokerage.
- **Organizations and innovation.** Managers, inventors and teams who span holes produce more novel ideas, while dense teams carry them out better.
- **[Weak ties](/weak-ties/) and [triadic closure](/triadic-closure/).** Holes are the gaps that closure fills in and that weak ties bridge.
- **[Betweenness centrality](/betweenness-centrality/) and [centrality](/centrality/) measures.** A global measure of brokerage, compared with the local measures of Burt.
- **Network design and influence.** Choosing seeds that span holes reaches more distinct groups, and removing a broker can cut communication between groups.

## References
