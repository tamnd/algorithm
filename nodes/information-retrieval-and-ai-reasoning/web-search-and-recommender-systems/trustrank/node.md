---
tag: Y8VX0X
kind: algorithm
slug: trustrank
name: TrustRank
aliases:
- Gyongyi-Garcia-Molina-Pedersen TrustRank
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Propagates trust from a hand-checked seed set of good pages by a biased PageRank, so spam pages get low trust scores.
solves: [link-analysis-ranking]
model: word-ram
complexity:
  vars: {n: the number of pages, m: the number of links, M: the number of rounds of each power iteration}
  time: {worst: O(M (n + m) + n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, directed: true, weighted: false}
history:
  year: 2004
  people: [Zoltan Gyongyi, Hector Garcia-Molina, Jan Pedersen]
  note: Gyongyi, Garcia-Molina and Pedersen presented TrustRank at VLDB 2004 and tested it on an AltaVista graph of about 31 million web sites.
prereqs: [pagerank, personalized-pagerank, link-spam]
see_also: [salsa-algorithm, hits-algorithm, link-analysis-ranking, power-iteration, markov-chain, bow-tie-web-structure, anchor-text-indexing]
sources:
  - paper: "Zoltan Gyongyi, Hector Garcia-Molina and Jan Pedersen, Combating Web spam with TrustRank, Proceedings of the 30th International Conference on Very Large Data Bases (VLDB 2004), 576-587"
    locator: Section 4.2 (trust dampening and trust splitting), Section 4.3 and Figure 5 (the algorithm with alpha_B = 0.85 and M_B = 20), Section 5.1 (inverse PageRank for seed selection) and Section 6 (the AltaVista experiments)
  - paper: doi:10.1145/511446.511513
    title: Taher H. Haveliwala, Topic-sensitive PageRank, Proceedings of the 11th International World Wide Web Conference (WWW 2002), 517-526
    locator: the PageRank vector biased toward a chosen set of pages by its jump vector, which is the computation that TrustRank runs with the good seeds
  - paper: "Zoltan Gyongyi, Pavel Berkhin, Hector Garcia-Molina and Jan Pedersen, Link spam detection based on mass estimation, Proceedings of the 32nd International Conference on Very Large Data Bases (VLDB 2006)"
    locator: the definition of spam mass, the part of the PageRank of a page that comes from spam pages, estimated with a biased PageRank on a good core
---

TrustRank is a link analysis algorithm that gives each web page a trust score by spreading trust from a small seed set of pages that a person has checked and found good. Zoltán Gyöngyi, Hector Garcia-Molina and Jan Pedersen published it in 2004 as a defence against [link spam](/link-spam/). The computation is a [personalized PageRank](/personalized-pagerank/) whose jump vector is uniform on the good seeds, with two differences from the usual personalized PageRank: a human oracle picks the seeds from the pages with the highest inverse PageRank, and the trust that reaches a page with no out-link is dropped instead of being sent back, so the scores sum to at most 1. Spam pages get low trust because good pages seldom link to spam.

## In plain words

Spam pages try to look important by collecting many links. TrustRank starts from a few pages that a person has checked and found good, such as the home pages of universities or of large companies. Each of these pages gets an equal share of trust. In each round, every page passes most of its trust along its links, in equal parts, and the seed pages get a fresh share again. Good pages seldom link to spam, so trust flows mostly to good pages. Spam pages can link to each other as much as they like, but this makes no new trust. Trust also gets weaker at each link it crosses, so a page far from all seeds gets little. To choose the seeds, the method looks for pages from which many other pages can be reached, and asks a person to check only the best of them.

## The problem

The input is a directed graph $G = (V, E)$ of web pages (or of web sites, as in the paper), with $V = \{0, \ldots, n - 1\}$ and $m$ links, an oracle $O$ that says for a page whether it is good ($O(p) = 1$) or spam ($O(p) = 0$), a limit $L$ on the number of oracle calls, a decay factor $\alpha_B \in [0, 1)$ and a number of rounds $M_B$. Self links are removed and repeated links count once. The output is a trust score $t(p) \ge 0$ for each page. Pages are ranked by trust, highest first, and equal scores go to the smaller page number.

The oracle is expensive: in practice it is a person who looks at the page. So the method may call it only $L$ times, and the rest of the graph is judged by its links alone. The method rests on one assumption, which the paper calls approximate isolation of the good set: good pages seldom link to spam pages, while spam pages may link to good pages. This is a property of the web that the paper observes, not a theorem.

## The algorithm

Let $\omega(q)$ be the out-degree of page $q$. The transition matrix is $T_{pq} = 1/\omega(q)$ if $(q, p) \in E$ and $0$ otherwise. A column of a page with no out-link is all zero, so $T$ loses the mass that reaches such a page. Inverse PageRank is PageRank on the graph with every link reversed: the same update as line L6, with the transition matrix of the reversed graph and the uniform vector $(1/n, \ldots, 1/n)$ in place of $d$. A page with a high inverse PageRank reaches many pages in few steps, which makes it a useful seed.

```pseudo id=main
TRUSTRANK(G, O, L, αB, MB)
L1  s ← INVERSE-PAGERANK(G)                 ▷ seed desirability, αI = 0.85 and MI = 20 rounds
L2  σ ← the pages in order of s, highest first, ties to the smaller page
L3  d ← 0; for i ← 1 to L: if O(σ(i)) = 1 then d(σ(i)) ← 1
L4  d ← d / |d|                             ▷ |d| is the number of good seeds; fail if 0
L5  t ← d
L6  repeat MB times: t ← αB · T · t + (1 - αB) · d
L7  return t
```

Lines L1 to L4 choose the seeds and cost $L$ oracle calls. Lines L5 and L6 are the biased PageRank: the walker follows a random out-link with probability $\alpha_B$ and jumps to a random good seed with probability $1 - \alpha_B$. The paper uses $\alpha_B = 0.85$ and $M_B = 20$. As $M_B$ grows, $t$ tends to the fixed point

$$t^* = \alpha_B T t^* + (1 - \alpha_B) d = (1 - \alpha_B) \sum_{k \ge 0} \alpha_B^k T^k d.$$

Each term of the sum is the trust that arrives along walks of exactly $k$ links from the seeds, multiplied by $\alpha_B^k$. The factor $\alpha_B^k$ is the trust dampening of the paper, and the division by $\omega(q)$ inside $T$ is its trust splitting: a page that links to many pages gives each of them a smaller part.

## Example

Take seven pages. Pages 0 to 3 are good and pages 4 to 6 form a small link farm. The links are $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 0$, $3 \to 4$, $4 \to 0$, $4 \to 5$, $5 \to 4$, $5 \to 6$ and $6 \to 4$. The link $3 \to 4$ is a good page that points to spam, for example through a comment that a spammer posted. The farm also links back to page 0 to look normal. Every page has an out-link, so no trust leaks.

With $L = 3$ and 20 rounds of inverse PageRank, the three pages with the highest inverse PageRank are 4, 2 and 1. The oracle rejects page 4 and accepts the other two, so $d = (0, \tfrac12, \tfrac12, 0, 0, 0, 0)$. The first round of line L6 gives page 2 the value $0.15 \cdot \tfrac12 + 0.85 \cdot \tfrac12 = \tfrac12$ (page 1 sends its whole trust to page 2), pages 0 and 3 each get $0.85 \cdot \tfrac12 \cdot \tfrac12 = \tfrac{17}{80}$ from page 2, and page 1 keeps only its jump share $\tfrac{3}{40}$. The table gives the exact fixed point $t^*$ and, for comparison, the PageRank with a uniform jump vector and the same $\alpha = 0.85$, both to 4 places.

| page | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| inverse PageRank (20 rounds) | 0.1608 | 0.1639 | 0.1676 | 0.1184 | 0.1816 | 0.1348 | 0.0729 |
| PageRank | 0.2108 | 0.2006 | 0.1919 | 0.1030 | 0.1506 | 0.0854 | 0.0577 |
| TrustRank $t^*$ | 0.2088 | 0.2524 | 0.2896 | 0.1231 | 0.0786 | 0.0334 | 0.0142 |

PageRank puts the spam page 4 above the good page 3. TrustRank puts every good page above every spam page, and page 4 keeps about half of its PageRank. The trust sums to exactly 1, as Theorem 4 of the proof file says for a graph with no dangling page in reach. After the 20 rounds of the paper, the sum of the errors is about 0.0001, well inside the bound $2 \cdot 0.85^{20} \approx 0.078$.

## Correctness

The file proofs/correctness.md proves five facts. The fixed point $t^*$ exists, is unique and is nonnegative, because $\lVert \alpha_B T x \rVert_1 \le \alpha_B \lVert x \rVert_1$. After $M$ rounds the sum of the errors is at most $\alpha_B^M \lVert d - t^* \rVert_1 \le 2 \alpha_B^M$. A page has positive trust exactly when it can be reached from a seed, and a page at link distance $k$ from the nearest seed has trust at most $\alpha_B^k$. The total trust is 1 when no page in reach is dangling, and less than 1 otherwise. A set of pages with no seed holds at most $\alpha_B / (1 - \alpha_B)$ times the trust that links from outside bring into it.

The last fact is the formal side of approximate isolation. With $\alpha_B = 0.85$, a link farm can hold at most $17/3$ times the trust that its links from good pages carry in, however many pages it adds. These facts hold for every seed set. Whether the seeds cover the good web well, and whether good pages really avoid linking to spam, are questions that only measurement can answer.

## Complexity

Each round of line L6 reads every link once, so it costs $\Theta(n + m)$ time on the word RAM with floating point numbers. Line L1 costs the same for each of its rounds, and line L2 sorts the pages in $O(n \log n)$. With $M$ rounds in each of the two iterations, the total time is $O(M (n + m) + n \log n)$, plus $L$ oracle calls. Removing repeated links costs $O(n + m)$ by counting sort on the pairs; the implementation sorts the links instead, in $O(m \log m)$, so that the sums run in a fixed order. Besides the graph, the method keeps the out-degrees and two vectors of length $n$, so the extra space is $\Theta(n)$. The human work, $L$ checks, is the real cost: the paper evaluated 1,250 sites by hand to get its seeds.

## Properties

- **Linear in the seeds.** $t^*$ is a linear function of $d$, so $t^* = \sum_{s} d(s)\, t^*_s$, where $t^*_s$ is the vector for the single seed $s$. A new seed can be added without a full new run, if the single-seed vectors are kept.
- **No trust from nothing.** A page that no seed reaches has trust exactly 0, so an isolated farm gets nothing, whatever its size or structure.
- **Leaks are allowed.** The scores sum to at most 1, and the sum is below 1 when a dangling page is in reach. The paper keeps this leak; it does not send the lost trust back to the seeds.
- **Deterministic.** With a fixed oracle and the tie rule of line L2, the output depends only on the graph.

## Variants and improvements

- **Other seed choices.** Section 5.2 of the paper also tries the pages with the highest PageRank as seed candidates. Inverse PageRank prefers pages from which many pages are reachable, which is closer to the goal of covering the good web.
- **Spam mass.** Gyöngyi, Berkhin, Garcia-Molina and Pedersen (2006) compare the PageRank of a page with its biased PageRank from a large set of known good pages. The difference estimates how much of the PageRank comes from spam, which finds spam that low trust alone does not mark.
- **Distrust.** Later methods also spread distrust from known spam pages, along the links in reverse, because a page that links to spam is suspect. This uses the same biased PageRank on the reversed graph.
- **Exact solution.** For a small graph, the linear system $(I - \alpha_B T) t = (1 - \alpha_B) d$ gives $t^*$ directly by [Gaussian elimination](/gaussian-elimination/). The test file uses this, in rational numbers, as the reference.

## When to use it

Use TrustRank when you can pay for some hundreds of human checks and you need a signal that demotes pages which gain their rank from link farms. It works as one feature among many, next to content features and [anchor text](/anchor-text-indexing/). It is a poor tool to label single pages: low trust means only that a page is far from the seeds, which is also true of many good pages in parts of the web that the seeds do not reach.

## Pitfalls

- **One bad seed spoils the result.** A spam page in the seed set gives trust to its whole farm. The oracle must be a careful human check, and seeds must be pages that stay under the same control over time.
- **The dangling rule changes the numbers.** If an implementation sends the trust of dangling pages back to the seeds, or spreads it uniformly, the scores differ from the paper's. Say which rule you use.
- **Twenty rounds are not convergence.** The bound after $M_B = 20$ rounds is $2 \cdot 0.85^{20} \approx 0.078$ on the sum of the errors. That is enough to rank, but not to compare scores across runs with different $M_B$.
- **Coverage gaps look like spam.** Good pages in a region with no seed get trust near 0. Pick seeds from many topics and regions, or combine trust with other signals.
- **Spammers can buy good links.** Links from blog comments, wikis and expired domains carry trust into a farm. The leak bound limits the gain from each such link, but it does not stop it.
- **Pages or sites.** The paper runs on the graph of web sites, in which a link between two sites counts once. On the page graph, links inside one site add weight that the site owner controls.

## Implementations

## History

Gyöngyi, Garcia-Molina and Pedersen presented TrustRank at the VLDB conference in 2004; the work was done at Stanford University and Yahoo!. They tested it on a graph of 31,003,946 web sites that the AltaVista search engine had crawled in August 2003. To get seeds, they ran inverse PageRank, kept the top 25,000 sites, checked by hand the first 1,250 of those that major web directories listed, and kept 178 of them as good seeds. They then judged a sample of sites from each range of scores, and reported that the high trust ranges held fewer spam sites than the high PageRank ranges. These results are measurements on that one graph and one sample.

## References
