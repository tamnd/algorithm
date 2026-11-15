---
tag: G8AJQK
kind: concept
slug: link-spam
name: Link spam
aliases:
- link farm
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Groups of pages that create links among themselves to raise their link-based scores, such as PageRank, above their merit.
prereqs: [pagerank, directed-graph]
see_also: [trustrank, salsa-algorithm, hits-algorithm, personalized-pagerank, link-analysis-ranking, anchor-text-indexing, near-duplicate-document-detection, bow-tie-web-structure]
sources:
  - paper: "Zoltán Gyöngyi and Hector Garcia-Molina, Web spam taxonomy, First International Workshop on Adversarial Information Retrieval on the Web (AIRWeb 2005)"
    locator: the split into boosting and hiding techniques, and the section on link spamming with outgoing links, incoming links, honey pots, directories, posts on blogs and wikis, link exchange, expired domains and spam farms
  - paper: "Zoltán Gyöngyi and Hector Garcia-Molina, Link spam alliances, Proceedings of the 31st International Conference on Very Large Data Bases (VLDB 2005)"
    locator: the model of a spam farm with one target and k boosting pages, the optimal farm structure and its PageRank, and alliances of several farms
  - paper: "Zoltán Gyöngyi, Hector Garcia-Molina and Jan Pedersen, Combating Web spam with TrustRank, Proceedings of the 30th International Conference on Very Large Data Bases (VLDB 2004)"
    locator: the description of link spam as the motive for TrustRank, and the observation that good pages seldom link to spam pages
  - paper: "Dennis Fetterly, Mark Manasse and Marc Najork, Spam, damn spam, and statistics: using statistical analysis to locate spam web pages, Seventh International Workshop on the Web and Databases (WebDB 2004)"
    locator: the finding that spam pages are outliers in statistics such as host names, degrees and the change of content over time
---

Link spam is the creation of links whose only purpose is to raise the link-based score of some target pages, such as their [PageRank](/pagerank/) or their authority score in [HITS](/hits-algorithm/). Ranking by links rests on the idea that a link is a vote by an independent author. Link spam breaks that idea: one person or group makes the pages that cast the votes. The classic form is a link farm, a set of pages that link to a target page and to each other. Zoltán Gyöngyi and Hector Garcia-Molina gave a taxonomy of link spam in 2005 and showed which farm structure gives the target the largest PageRank. Defences such as [TrustRank](/trustrank/) and spam mass use the fact that good pages seldom link to spam pages.

## In plain words

Search engines trust pages that many other pages link to, a bit like trusting a restaurant that many people recommend. Spammers fake the recommendations. They build hundreds of cheap pages whose only job is to link to the page they want to promote, and they make the promoted page link back so that none of the value leaks away. They also put links in places they can write to, such as comments on blogs, open wikis and guest books, and they buy old websites that still have many links pointing at them. A search engine fights back by giving less weight to links it cannot trust, by starting from pages it knows are good, and by spotting groups of pages that look and link in an odd, uniform way.

## The idea

**Where the links come from.** Gyöngyi and Garcia-Molina split spam techniques into boosting techniques, which raise the score of a page, and hiding techniques, which hide the boosting from users and from the search engine, such as cloaking and redirection. Boosting is either term spam, which stuffs the text, or link spam. For link spam, the spammer controls some pages, can add links to some pages that are open to anyone, and cannot change the rest of the web. In-links to a target come from:

- **Own pages.** A spam farm of pages that the spammer makes in any number, at almost no cost.
- **Open pages.** Posts on blogs, wikis, forums and guest books, and entries in open directories.
- **Honey pots.** Useful pages, such as copies of a popular reference, that attract real links and pass them on to the target.
- **Link exchange and bought domains.** Groups of spammers who link to each other, and expired domains that still have in-links from the time when a real site lived there.

For HITS, the spammer can also add out-links to good authorities from a page, which raises its hub score, for example by copying a web directory.

**The optimal farm.** Take PageRank with damping factor $\alpha$ on $n$ pages, with the scores summing to 1 and the teleport spread evenly. A farm has a target $t$ and $k$ boosting pages. Let $x$ be the PageRank that flows into $t$ from outside the farm, through links from open pages. Gyöngyi and Garcia-Molina show that the target gets the most PageRank when each boosting page links only to $t$, and $t$ links only to the boosting pages, so no PageRank leaves the farm. Then the scores satisfy

$$\mathrm{PR}(t) = x + \alpha k\, \mathrm{PR}(b) + \frac{1 - \alpha}{n}, \qquad \mathrm{PR}(b) = \frac{\alpha\, \mathrm{PR}(t)}{k} + \frac{1 - \alpha}{n},$$

for each boosting page $b$. Putting the second equation into the first gives

$$\mathrm{PR}(t) = \frac{x}{1 - \alpha^2} + \frac{(1 - \alpha)(1 + \alpha k)}{(1 - \alpha^2)\, n} = \frac{x}{1 - \alpha^2} + \frac{1 + \alpha k}{(1 + \alpha)\, n}.$$

Two things follow. The PageRank $x$ from outside is multiplied by $1/(1 - \alpha^2)$, which is about 3.6 for $\alpha = 0.85$, because it goes round the farm again and again. And each boosting page adds $\alpha / ((1 + \alpha) n)$, so the score of the target grows linearly in $k$. The farm cannot create PageRank: with $x = 0$, its pages hold exactly their teleport share $(k + 1)/n$. What it does is move almost half of that share, a fraction that tends to $\alpha/(1 + \alpha) \approx 0.46$, onto one page.

**Why it is hard to stop.** A link farm is a legal part of the graph, and many honest sites link among their own pages. A single link says nothing about its author. Defences look at the graph as a whole or at signs outside the graph:

- **Trust propagation.** [TrustRank](/trustrank/) runs a [personalized PageRank](/personalized-pagerank/) from a seed set of pages that people checked as good. A farm with no links from good pages gets no trust, however large it is.
- **Spam mass.** The share of the PageRank of a page that comes from pages without trust. A page that gets most of its PageRank from untrusted pages is suspect.
- **Statistics.** Fetterly, Manasse and Najork found that spam pages are outliers in simple statistics, such as the number of host names that map to one address, the degree distribution, and how fast the content changes.
- **Discounted links.** Search engines can ignore links in places that anyone can write to. The rel="nofollow" attribute, which sites put on links in user comments, asks engines not to count those links.
- **Less sensitive ranking.** [SALSA](/salsa-algorithm/) splits the score inside each connected component, which weakens the tightly knit community effect that lets a dense group of pages take over the HITS scores.

## Examples

**A farm of 100 pages.** Let $\alpha = 0.85$, $x = 0$, and multiply all scores by $n$, so that the average page has 1. A page with no in-links and with out-links has $n \cdot \mathrm{PR} = 1 - \alpha = 0.15$. With a farm of $k$ boosting pages, $n \cdot \mathrm{PR}(t) = (1 + 0.85k)/1.85$:

| k | n PR(t) | n PR(b) | share of the farm on t |
|---|---|---|---|
| 1 | 1.0000 | 1.0000 | 0.5000 |
| 10 | 5.1351 | 0.5865 | 0.4668 |
| 100 | 46.4865 | 0.5451 | 0.4603 |
| 1000 | 460.0000 | 0.5410 | 0.4595 |

With 100 boosting pages, the target has about 46 times the PageRank of an average page and about 310 times that of a page with no in-links. Each boosting page keeps about half of the average. The total of the farm is $46.4865 + 100 \cdot 0.5451 = 101$, its teleport share.

**Leaked PageRank is amplified.** If one comment on a blog gives the target $x = 2/n$ of PageRank, the target gets $2 \cdot 3.6036 \approx 7.21$ more units, on top of the farm. An honest page with the same link would get only the 2 units.

**Hub spam for HITS.** A page that copies the links of a large directory gets a high hub score at once, since its links point to many good authorities. If it also links to the target, the target gains authority from a strong hub.

## Where it is used

- **Search engine ranking.** Every engine that uses links for ranking must expect link spam and discount it. This is the main motive for [TrustRank](/trustrank/), spam mass and link-based spam classifiers.
- **Crawling.** A [crawler](/web-crawling/) can waste much of its budget on farms of generated pages. Limits per host and the detection of [near-duplicate](/near-duplicate-document-detection/) and generated pages save the budget.
- **Anchor text.** Spammers also choose the words of their links to push [anchor text indexing](/anchor-text-indexing/) toward a query, so anchor text from untrusted pages needs less weight.
- **Other networks.** Fake reviews, fake followers in social networks and citation rings in science are the same attack on other graphs, and the same defences, trust from known good nodes and statistics of odd groups, apply.

## References
