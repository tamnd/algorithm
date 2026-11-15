---
tag: CT80NW
kind: algorithm
slug: focused-crawling
name: Focused crawling
aliases:
- topical crawling
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Orders the crawl frontier by a classifier score of page relevance to a topic, so the crawler fetches on-topic pages first.
solves: [web-crawling]
model: word-ram
complexity:
  vars: {S: the number of seeds, m: the number of links on the fetched pages, k: the budget of pages}
  time: {expected: O((S + m) log(S + m))}
  space: {extra: O(S + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1999
  people: [Soumen Chakrabarti, Martin van den Berg, Byron Dom]
  note: Chakrabarti, van den Berg and Dom named focused crawling at WWW8 in 1999, with a topic classifier that ordered the frontier and a distiller that found hub pages.
prereqs: [web-crawling, url-frontier, best-first-search, naive-bayes-classifier]
see_also: [breadth-first-search, priority-queue, binary-heap, hits-algorithm, pagerank, precision-and-recall, logistic-regression, crawl-revisit-policy]
sources:
  - paper: "Soumen Chakrabarti, Martin van den Berg and Byron Dom, Focused crawling: a new approach to topic-specific Web resource discovery, Computer Networks 31(11-16), 1999 (Proceedings of the Eighth International World Wide Web Conference)"
    locator: the description of the classifier, the soft and hard focus rules, the distiller, and the experiments that measure the harvest rate against an unfocused crawler
  - paper: "Junghoo Cho, Hector Garcia-Molina and Lawrence Page, Efficient crawling through URL ordering, Computer Networks 30(1-7), 161-172, 1998 (Proceedings of the Seventh International World Wide Web Conference)"
    locator: the ordering metrics for the frontier, including the similarity of a page to a driving query, and the experiments on the Stanford web
  - paper: "Filippo Menczer, Gautam Pant and Padmini Srinivasan, Topical web crawlers: evaluating adaptive algorithms, ACM Transactions on Internet Technology 4(4), 2004"
    locator: the comparison of best-first, breadth-first and adaptive topical crawlers, and the harvest rate and target recall measures
  - paper: "Christopher Olston and Marc Najork, Web crawling, Foundations and Trends in Information Retrieval 4(3), 175-246, 2010"
    locator: the section on scoped crawling, which covers topical crawlers
---

Focused crawling is a way to run a [web crawler](/web-crawling/) so that it fetches pages about one topic first and spends little of its budget on the rest of the web. A classifier gives each fetched page a relevance score, and the [URL frontier](/url-frontier/) is ordered so that the links of relevant pages are fetched before the links of irrelevant ones. Soumen Chakrabarti, Martin van den Berg and Byron Dom gave the method its name in 1999. The core is a [best-first search](/best-first-search/) over the web graph, in which the priority of a URL is the relevance of the pages that link to it. That the method finds more relevant pages for the same budget is a measured property, not a theorem: it holds when relevant pages tend to link to each other and the classifier is good.

## In plain words

A general crawler follows every link it finds, so it wanders all over the web. A focused crawler is for one subject, such as cycling. Each time it downloads a page, a program decides how much the page is about cycling. Links on a page that is about cycling are probably worth following soon, because pages on a subject tend to link to other pages on the same subject. Links on a page about something else can wait. So the crawler keeps its list of links to visit sorted by how good the page was where it found each link, and always visits the best one next. In a strict form, it does not follow the links of pages that are off the subject at all. The crawler is judged by the share of downloaded pages that are on the subject.

## The problem

The input is a set $S$ of seed URLs, a fetch operation that returns the out-links $\mathrm{out}(u)$ of a page $u$, a relevance function $R(u) \in [0, 1]$ computed from the fetched page, and a budget of $k$ fetches. The task is to choose which $k$ pages to fetch, one at a time, so that many of them are relevant. The crawler sees the web graph only through the pages it has fetched. The usual measure is the harvest rate, the fraction of fetched pages that are relevant. Since the true relevance is unknown, experiments estimate it with the classifier itself or with human judgments.

## The algorithm

The priority of an unfetched page $v$ is 1 if it is a seed, and else the largest $R(u)$ over fetched pages $u$ that link to $v$. This is the soft focus rule. With hard focus and threshold $\theta$, the links of a page $u$ are followed only if $R(u) \ge \theta$. The frontier is a max-heap of pairs (priority, URL), ties to the smaller URL. When a priority rises, a new entry is pushed and the old one is skipped later (lazy deletion).

```pseudo id=main
FOCUSED-CRAWL(S, R, k, θ)                 ▷ θ = none for soft focus
L1  for each seed s: prio(s) ← 1; push (1, s) on the max-heap
L2  D ← ∅; order ← empty list
L3  while the heap is not empty and |order| < k:
L4      (p, u) ← EXTRACT-MAX(heap)            ▷ ties to the smaller u
L5      if u ∈ D or p < prio(u) then continue  ▷ a stale entry
L6      fetch u; add u to D and to order; r ← R(u)
L7      if θ ≠ none and r < θ then continue    ▷ hard focus: do not follow the links
L8      for each v ∈ out(u) with v ∉ D:
L9          if v has no priority or r > prio(v):
L10             prio(v) ← r; push (r, v)
L11 return order
```

The relevance function in the implementation is a two-class multinomial [naive Bayes classifier](/naive-bayes-classifier/) trained on example pages, which returns the probability that a page is on the topic. Any score in $[0, 1]$ works, such as the output of [logistic regression](/logistic-regression/).

Chakrabarti, van den Berg and Dom used a hierarchical classifier over a topic taxonomy in which the user marks some classes as good. In their soft focus rule, the relevance of a page is the total probability of the good classes. In their hard focus rule, the crawler finds the most likely leaf class of the page and follows its links only if that class or one of its ancestors is good. The threshold rule of line L7 is a simple form of this.

## Example

Take eight pages with the links a → b, c; b → d, e; c → f, g; f → h, and the scores below. The seed is a, and a page counts as on the topic when its score is at least 0.5.

| page | a | b | c | d | e | f | g | h |
|---|---|---|---|---|---|---|---|---|
| R | 0.9 | 0.1 | 0.8 | 0.2 | 0.1 | 0.9 | 0.3 | 0.7 |

With soft focus:

| step | fetch | R | new priorities |
|---|---|---|---|
| 1 | a | 0.9 | b: 0.9, c: 0.9 |
| 2 | b (tie with c, smaller id) | 0.1 | d: 0.1, e: 0.1 |
| 3 | c | 0.8 | f: 0.8, g: 0.8 |
| 4 | f (tie with g) | 0.9 | h: 0.9 |
| 5 | h | 0.7 | |
| 6 | g | 0.3 | |
| 7, 8 | d, e | | |

The fetch order is a, b, c, f, h, g, d, e. [Breadth-first search](/breadth-first-search/) fetches a, b, c, d, e, f, g, h. With a budget of 5 pages, the focused crawler gets the four on-topic pages a, c, f and h, and breadth-first search gets only a and c. With hard focus and $\theta = 0.5$, the links of b are never followed, so d and e are never found, and the crawl is a, b, c, f, h, g.

On larger graphs the effect is measured. The test file plants a graph of 1000 pages, 20% of them on the topic, with 6 links per page, each of which stays in the class of its page with probability 0.6. A naive Bayes classifier trained on other pages of the same model labels about 1.5% of the pages wrongly. With 3 on-topic seeds and a budget of 200 pages, over ten fixed seeds of the generator, the harvest rate of the focused crawler is between 0.58 and 0.635 (mean 0.600), and that of breadth-first search is between 0.275 and 0.48 (mean 0.406). When the links go to random pages, both stay near the base rate of 20% (means 0.2175 and 0.203).

## Correctness

The file proofs/correctness.md proves that the crawler follows its rule. The invariant is that for every discovered unfetched page $v$, prio$(v)$ is the largest score of an expanded fetched page that links to $v$ (or 1 for a seed), the heap holds the entry (prio$(v)$, $v$), and every other entry of $v$ has a smaller key. A stale entry thus never hides a page, so each step fetches the discovered page of largest priority, ties to the smaller id. The test file checks this against a brute-force rule that recomputes all priorities at each step. It also follows that each page is fetched once and only pages reachable from the seeds are fetched, and that with soft focus and no budget limit every reachable page is fetched.

Nothing in the proof says that the crawl finds relevant pages. That depends on the web, through the tendency of pages to link to pages on the same topic, and on the quality of $R$.

## Complexity

The heap gets one entry per seed and at most one per link of an expanded page, so at most $S + m$ entries, where $m$ is the number of links on the fetched pages. Each push and pop costs $O(\log(S + m))$, and the hash tables for prio and $D$ cost $O(1)$ expected per lookup. So the crawl costs $O((S + m) \log(S + m))$ expected time and $O(S + m)$ extra space, plus $k$ fetches and $k$ calls of the classifier. In a real crawler the fetches and the classifier dominate by far.

## Properties

- **Deterministic.** With a fixed $R$ and the tie rule, the order is fixed.
- **Greedy and local.** The priority of a URL uses only the pages already fetched. A good page behind an off-topic page gets a low priority, and with hard focus it is never found.
- **The link of a good page is not always good.** Soft focus gives every link of a relevant page the same high priority, so the off-topic pages that relevant pages link to are fetched early too. This puts a ceiling on the harvest rate, as in the planted graph above.
- **Not polite by itself.** The algorithm orders URLs only. A real crawler puts the priorities into a two-stage frontier that also enforces a gap per host.

## Variants and improvements

- **Fish search and shark search.** Before the 1999 paper, De Bra and Post's fish search and the shark search of Hersovici and others ordered links by a text match of the page, and shark search also used the anchor text of each link. See [anchor text indexing](/anchor-text-indexing/) for why the anchor text is a good clue.
- **Distillation.** Chakrabarti, van den Berg and Dom also ran a distiller, a form of [HITS](/hits-algorithm/) on the fetched pages, to find hub pages that link to many relevant pages, and raised the priority of the links of the hubs.
- **Link scores from the anchor and the URL.** Later crawlers score each link and not only its page, from the anchor text, the words near the link, and the URL. Chakrabarti, Punera and Subramanyam trained a second classifier, an apprentice, on the links that led to relevant pages.
- **Context graphs.** Diligenti and others learned how many links away from a relevant page a page usually is, and ordered the frontier by this estimated distance.
- **Learning crawlers.** Reinforcement learning crawlers estimate the value of a link as the number of relevant pages that it leads to in the future, not just the relevance of its page.
- **Global ordering.** Cho, Garcia-Molina and Page ordered the frontier of a general crawler by backlink counts or an estimate of [PageRank](/pagerank/), which is the same best-first scheme with a different priority.

## When to use it

Use a focused crawler when you need pages on one subject and cannot or will not crawl the whole web, for example to build a topic search engine or a corpus for a domain. It needs a classifier with good accuracy on the topic and seeds inside the topic. If the topic is spread over unrelated sites with few links between them, start from many seeds or use a search engine to find more.

## Pitfalls

- **Tunnelling.** Relevant pages can sit behind one or two off-topic pages, such as a university home page that leads to a lab page. Hard focus never gets there, and soft focus gets there late. A tolerance for a few off-topic steps helps.
- **A drifting classifier.** A classifier trained on a few examples can rate pages with common words too high, and the crawl drifts away from the topic. Check samples of the fetched pages by hand.
- **Measuring with the same classifier.** A harvest rate computed with the classifier that steers the crawl rewards the crawler for agreeing with itself. Use held-out judgments or a second classifier.
- **Ties.** With coarse scores, many URLs tie, and the tie rule then decides much of the order. State it.
- **The benefit is not a guarantee.** On a graph without topical clustering, the focused crawler does no better than breadth-first search.

## Implementations

## History

Early topical crawlers include the fish search of De Bra and Post in 1994 and the shark search of Hersovici and others in 1998. In 1998, Cho, Garcia-Molina and Page studied how to order a crawl frontier by importance, including the similarity of a page to a query. Chakrabarti, van den Berg and Dom presented focused crawling at the WWW8 conference in 1999, with a taxonomy classifier, the soft and hard focus rules, and a distiller for hubs. In their experiments, the focused crawler kept finding relevant pages over long crawls, while an unfocused crawler from the same seeds soon moved away from the topic. Menczer, Pant and Srinivasan compared best-first and adaptive topical crawlers in 2004, and found that best-first crawlers are strong baselines.

## References
