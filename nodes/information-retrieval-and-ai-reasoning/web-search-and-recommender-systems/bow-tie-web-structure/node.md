---
tag: FXT0DN
kind: concept
slug: bow-tie-web-structure
name: Bow-tie structure of the web
aliases:
- web bow-tie model
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: The web graph has a giant strongly connected core, pages that reach it, pages it reaches, and tendrils and tubes outside them.
prereqs: [directed-graph, strongly-connected-components, breadth-first-search, web-crawling]
see_also: [tarjan-scc, connected-components, scale-free-network, preferential-attachment, small-world-network, pagerank, webgraph-compression, link-spam]
sources:
  - paper: "Andrei Broder, Ravi Kumar, Farzin Maghoul, Prabhakar Raghavan, Sridhar Rajagopalan, Raymie Stata, Andrew Tomkins and Janet Wiener, Graph structure in the web, Computer Networks 33(1-6), 309-320, 2000 (Proceedings of the Ninth International World Wide Web Conference)"
    locator: Section 2 (the AltaVista crawl of May 1999 with 203 million URLs and 1466 million links, the degree distributions, the weak and strong components and the BFS runs from 570 random pages), Section 3 (the table of region sizes and Figure 9 of the bow-tie) and Section 3.4 (diameter and average connected distance)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 19, Section 19.2 (the web graph, its power law degree distributions and its bow-tie shape)
  - paper: "Robert Meusel, Sebastiano Vigna, Oliver Lehmberg and Christian Bizer, Graph structure in the web, revisited: a trick of the heavy tail, Companion Proceedings of the 23rd International World Wide Web Conference (WWW 2014)"
    locator: the bow-tie decomposition of a 2012 Common Crawl graph and the argument that the sizes of the regions depend on the crawl
---

The bow-tie structure is a way to split a directed graph, and in particular the web graph, into parts by how they connect to its largest [strongly connected component](/strongly-connected-components/). Andrei Broder and seven coauthors described it in 2000, from a [crawl](/web-crawling/) of about 203 million pages made by the AltaVista search engine in May 1999. Their picture shows a central core, a set IN of pages that can reach the core, a set OUT of pages that the core can reach, tendrils and tubes that miss the core, and disconnected pieces. The split itself is a fact about any directed graph. The sizes of the parts, about a quarter of the pages in each of four parts, are measurements of that one crawl and change from crawl to crawl.

## In plain words

Think of the web as pages joined by one-way links. In the middle is a big group of pages where you can get from any page to any other by following links. Some pages lead into this group, but you cannot get back to them from it, such as a new page that links to famous sites but that no one links to yet. Other pages can be reached from the group but lead nowhere back, such as a company site that has no links out. Drawn on paper, the middle group with the two sides looks like a bow tie. There are also strands that hang off the sides without touching the middle, and small islands that are not joined to the rest at all. The sizes were measured on one large crawl in 1999 and are not a law.

## The idea

Let $G = (V, E)$ be a directed graph, and let $C$ be its largest strongly connected component, the core (SCC in the paper). Write $u \leadsto v$ if there is a directed path from $u$ to $v$. Let $W$ be the weakly connected component that contains $C$, the set of nodes joined to $C$ when links are followed in either direction. Then each node of $V$ is in exactly one of these sets:

- **CORE:** $C$.
- **IN:** the nodes $u \notin C$ with $u \leadsto c$ for some (and so for every) $c \in C$.
- **OUT:** the nodes $v \notin C$ with $c \leadsto v$ for some $c \in C$.
- **TENDRILS:** the other nodes of $W$. They cannot reach $C$ and $C$ cannot reach them. A tendril can hang off IN (reachable from IN) or lead into OUT (able to reach OUT). A node that is reachable from IN and can reach OUT without passing through the core lies on a **tube**. Broder and his coauthors count tubes as part of TENDRILS.
- **DISCONNECTED:** the nodes outside $W$.

IN and OUT cannot meet: a node in both would reach $C$ and be reached from it, so it would be in $C$. The split follows from the definitions, for every directed graph; what is special about the web is that $C$ is large. A [Tarjan SCC](/tarjan-scc/) pass finds $C$, a forward and a backward [breadth-first search](/breadth-first-search/) from $C$ give $C \cup \mathrm{OUT}$ and $C \cup \mathrm{IN}$, and a search over the links in both directions gives $W$. Each step takes $O(|V| + |E|)$ time.

A path from $u$ to $v$ exists in two main cases: when $u \in C \cup \mathrm{IN}$ and $v \in C \cup \mathrm{OUT}$, or through the small tendrils and tubes. This is why a random pair of pages is often not connected even though most pages are in one weak component.

**The 1999 measurement.** Broder and his coauthors could not run a full graph search for each node of a 203 million node graph, so they combined the components with breadth-first searches from 570 random start pages, once along the links and once against them. Each search either stopped after a few pages or exploded to about 100 million pages. Every start page in the core reached exactly 99,807,161 pages against the links and 99,630,178 pages along them, which gave $|C \cup \mathrm{IN}|$ and $|C \cup \mathrm{OUT}|$. For the crawl of May 1999, with 1466 million links:

| region | pages | share |
|---|---|---|
| CORE (SCC) | 56,463,993 | 27.7% |
| IN | 43,343,168 | 21.3% |
| OUT | 43,166,185 | 21.2% |
| TENDRILS (with tubes) | 43,797,944 | 21.5% |
| DISCONNECTED | 16,777,756 | 8.2% |
| total | 203,549,046 | |

The weak component $W$ holds the other 186,771,290 pages. The product of the shares of $C \cup \mathrm{IN}$ and $C \cup \mathrm{OUT}$ is $(99{,}807{,}161 \cdot 99{,}630{,}178) / 203{,}549{,}046^2 \approx 0.240$, which matches the paper's estimate that a path exists from a random page to another random page only 24% of the time. The paper also reports that the directed diameter of the core is at least 28, that some shortest paths have a length of at least 503, that the mean length of a directed path between connected pairs is about 16 (16.12 and 16.18 for the two directions), and that it is 6.83 when links can be followed both ways. The in-degrees follow a power law with exponent about 2.1 and the out-degrees one with exponent about 2.72. An October 1999 crawl of 271 million pages gave the same shape.

## Examples

Take twelve pages with the links $1 \to 2 \to 3 \to 1$, $11 \to 0 \to 1$, $3 \to 4 \to 10$, $0 \to 5$, $6 \to 4$, $0 \to 7 \to 4$ and $8 \to 9 \to 8$. The core is $\{1, 2, 3\}$, the largest strongly connected component.

| region | pages | why |
|---|---|---|
| CORE | 1, 2, 3 | a cycle |
| IN | 0, 11 | they reach page 1, and nothing in the core links back |
| OUT | 4, 10 | page 3 reaches them, and they have no path back |
| TENDRILS | 5, 6, 7 | 5 hangs off IN, 6 leads into OUT, and 7 is a tube from 0 to 4 |
| DISCONNECTED | 8, 9 | a separate cycle |

Page 0 reaches page 4 through the tube $0 \to 7 \to 4$ and through the core, but page 4 reaches nothing outside OUT. A crawler that starts at page 4 finds only pages 4 and 10; a crawler that starts at page 11 finds every page of the bow tie except 6, since nothing links to 6.

## Where it is used

- **Choice of crawl seeds.** A [crawler](/web-crawling/) reaches the core and OUT from any seed in IN or the core, but no crawl from the core reaches IN. Seeds must therefore come from many sources, such as submitted URLs and old crawls.
- **Link analysis.** [PageRank](/pagerank/) needs a teleport step because OUT and the tendrils contain sinks and closed groups of pages that a pure random surfer cannot leave. Without the teleport step, a surfer that starts in IN or the core ends up in OUT or in the tendrils and stays there.
- **Models of web growth.** The shape and the power laws are tests for random graph models of the web, such as [preferential attachment](/preferential-attachment/) and copying models.
- **Studies of other graphs.** The same split is used for citation graphs, social networks, trade networks and metabolic networks, with the warning that the sizes depend on how the graph was sampled.
- **Later crawls.** Meusel, Vigna, Lehmberg and Bizer split a 2012 Common Crawl graph in the same way and found a different balance of the regions; they argue that the sizes reflect the way a crawl is made more than a stable law of the web.

## References
