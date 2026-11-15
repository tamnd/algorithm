---
tag: VGF45W
kind: problem
slug: web-crawling
name: Web crawling
aliases:
- web crawler problem
- spidering
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: intro
summary: Fetch a large, changing set of web pages by following links from seed URLs, under politeness, freshness and coverage goals.
prereqs: [directed-graph, breadth-first-search, graph-traversal]
see_also: [url-frontier, focused-crawling, crawl-revisit-policy, near-duplicate-document-detection, bow-tie-web-structure, link-spam, pagerank, inverted-index]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 20, Section 20.1 (the features a crawler must provide, robustness and politeness, and should provide) and Section 20.2 (the crawler architecture, the URL-seen test, robots.txt, distributing the crawl and the URL frontier)
  - paper: "Marc Najork, Web crawler architecture, in Ling Liu and M. Tamer Oezsu (eds), Encyclopedia of Database Systems, Springer, 2009"
    locator: the definition of a web crawler, the estimate of over 4,000 pages per second for ten billion pages refreshed every 4 weeks, politeness policies, partitioning by host name, and the history from the World Wide Web Wanderer of 1993
  - paper: "Christopher Olston and Marc Najork, Web crawling, Foundations and Trends in Information Retrieval 4(3), 175-246, 2010"
    locator: the survey of crawler architecture, crawl ordering for coverage and freshness, politeness, and the problems of spam, duplicates and the deep web
  - paper: "Marc Najork and Janet L. Wiener, Breadth-first crawling yields high-quality pages, Proceedings of the Tenth International World Wide Web Conference (WWW10), 2001"
    locator: the measurement on a large Mercator crawl that a breadth-first crawl finds pages of high PageRank early
---

Web crawling is the problem of collecting web pages by following links. A crawler starts from a set of seed URLs, fetches each page, finds the links in it, and adds the new URLs to a list of pages to fetch. In principle this is a [graph traversal](/graph-traversal/) of the [directed graph](/directed-graph/) whose nodes are pages and whose edges are links. In practice the graph is huge, unknown in advance, changing all the time, and spread over millions of servers that do not want to be overloaded. So crawling is mostly an engineering problem with several measured goals that pull against each other: coverage, page quality, freshness, politeness and throughput. No single crawl order is best for all of them.

## In plain words

A crawler is a program that reads the web for a search engine. It starts with a few page addresses. It downloads each page, reads the addresses of the links on it, and puts the new ones on its list. Then it takes the next address from the list, and so on. The idea is simple, but the web is so big that a real crawler must download thousands of pages every second on many computers. It must not ask one website for pages too often, or the site slows down. It must obey the rules that sites publish for robots. It must skip pages it has already seen and endless traps of generated pages. It must also come back to pages that change, so its copy stays up to date. The goals are measured, not proved.

## Definition

The web is a directed graph $G = (V, E)$ that the crawler does not know. Each page $u$ has a URL and a host $h(u)$. A fetch of $u$ takes time and returns the content of $u$ and its out-links $\mathrm{out}(u)$; it can also fail. The crawler gets a set $S \subseteq V$ of seeds.

A crawl is a sequence of fetches with start times. It must respect these rules:

- **Discovery.** A URL can be fetched only if it is a seed or appeared in a page that was fetched before.
- **Politeness.** Two fetches from the same host start at least $\delta(h)$ apart, and no fetch asks for a URL that the robots.txt file of its host excludes.
- **Resources.** At most $c$ fetches run at the same time, and the total bandwidth and storage are bounded.

The goals are measured on the result:

- **Coverage.** The number or share of the pages reachable from $S$ that the crawl fetched, perhaps weighted by an importance score such as [PageRank](/pagerank/), within a time or page budget.
- **Freshness.** The share of the stored copies that still match the live pages, averaged over time. Its scheduling side is the [crawl revisit policy](/crawl-revisit-policy/) problem.
- **Quality.** Little effort on spam, duplicates and pages that nobody will search for.
- **Throughput.** Pages per second per machine.

Because the web has pages that generate links to new pages without end, such as calendars with a link to the next month, the reachable set can be infinite, and complete coverage is not a well-posed goal. Crawlers stop by budget, by depth, or by limits per host.

## Variants

- **Batch crawl.** Collect a snapshot once, then start again from scratch. The goal is coverage within a budget.
- **Incremental crawl.** Run without end, keep a collection up to date, and mix new pages with revisits of known ones. The goal is freshness.
- **Focused crawl.** Fetch only pages on one topic. See [focused crawling](/focused-crawling/).
- **Distributed crawl.** Split the work over many machines, usually by host, so that politeness decisions stay local and most new URLs belong to the machine that found them.
- **Deep web crawl.** Reach pages that no link points to, but that appear as results of forms, by filling in the forms with suitable queries.
- **Archival crawl.** Keep every version of every page, as web archives do, so storage and duplicate handling matter more than freshness.

## Examples

**Breadth-first crawl of a small site.** Take the seed a/0 with links a/0 → a/1, a/2 and a/1 → a/3, b/0. A crawler with a FIFO queue and a set of seen URLs fetches a/0, a/1, a/2, a/3, b/0, the order of [breadth-first search](/breadth-first-search/). If a/3 links back to a/0, the seen set stops the crawler from fetching a/0 twice.

**Politeness sets the pace.** Suppose the crawler knows 4 URLs of host a and 2 of host b, a fetch takes 0.2 s, and each host needs a gap of 1 s between fetches. With one connection, the best schedule is a at 0, b at 0.2, a at 1.0, b at 1.2, a at 2.0 and a at 3.0, and it ends at 3.2 s. Six fetches need only 1.2 s of connection time, but host a needs three gaps after its first fetch. More connections do not help: the crawl cannot end before $3 \cdot 1 + 0.2 = 3.2$ s. This is why a crawler must work on many hosts at once, and why the [URL frontier](/url-frontier/) has one queue for each host.

**Scale.** Najork gives an example: to keep ten billion pages fresh with each page refreshed every 4 weeks on average, a crawler must fetch $10^{10} / (28 \cdot 86400) \approx 4134$ pages per second, which is more than 4,000 pages per second.

## Known algorithms

**The basic loop.** Take a URL from the frontier, check robots.txt for its host, resolve the host name (with a cache of DNS answers), fetch the page, parse it, extract and normalize the links, test each link against the set of seen URLs, and add the new ones to the frontier. Manning, Raghavan and Schuetze (Section 20.2) describe this loop and each of its modules. The seen set is a [hash table](/hash-table/) of URL fingerprints, often kept on disk with a cache, or a [Bloom filter](/bloom-filter/) when a few lost URLs are acceptable.

**Order of the frontier.** A FIFO frontier gives breadth-first order, and Najork and Wiener measured that it finds pages of high PageRank early in the crawl. Cho, Garcia-Molina and Page ordered the frontier by backlink counts or by an estimate of PageRank computed on the pages fetched so far. A [focused crawler](/focused-crawling/) orders it by a topic classifier.

**Politeness.** The two-stage [URL frontier](/url-frontier/) of Najork and Heydon keeps one back queue for each host and a heap of the times at which each host may be contacted again. A common rule makes the gap a multiple of the time that the last fetch from the host took.

**Distribution.** Assign each host to one machine by a hash of the host name, or by [consistent hashing](/consistent-hashing/) so that machines can join and leave. A machine sends each URL of a host it does not own to the owner, in batches.

**Duplicates and traps.** Detect pages that are almost the same as pages already fetched, by [near-duplicate document detection](/near-duplicate-document-detection/), and drop or demote them. Limit the depth of URLs, the number of pages per host, and the length of URLs to escape traps.

**Revisits.** Schedule the refetch of known pages by their rates of change, as in the [crawl revisit policy](/crawl-revisit-policy/) problem.

## Bounds

These bounds are simple, but they explain the design of real crawlers.

- **Every page costs a fetch.** The crawler sees an edge only after it fetches its source, so any crawl that covers a set $U$ of pages makes at least $|U|$ fetches.
- **Politeness bound.** If the crawl must fetch $n_h$ pages of host $h$, it takes at least $(n_h - 1)\, \delta(h)$ time after the first fetch of $h$, for every $h$. So the time is at least $\max_h (n_h - 1)\, \delta(h)$, whatever the number of machines. A crawl of a site with millions of pages at one fetch per second takes weeks.
- **Bandwidth bound.** With $c$ parallel connections and a mean fetch time $\tau$, $|U|$ fetches take at least $|U| \tau / c$ time.
- **Reachability.** The crawl can find only pages reachable from the seeds by links. On the 1999 crawl measured in the [bow-tie study](/bow-tie-web-structure/), a path existed from a random page to another random page only about a quarter of the time, so the choice of seeds matters.

## Reductions

- Crawling without limits is graph search: with a FIFO frontier it is breadth-first search, with a priority frontier it is [best-first search](/best-first-search/).
- The order of the frontier is a ranking problem. With PageRank as the priority it uses [link analysis](/link-analysis-ranking/) on a partial graph.
- The revisit schedule is a resource allocation problem: split a fixed fetch rate over pages with different rates of change.
- The seen-URL test is the set membership problem, solved by hashing.

## Applications

- **Web search engines.** The crawl gives the pages for the [inverted index](/inverted-index/), the link graph for PageRank and the [anchor text](/anchor-text-indexing/) of links.
- **Web archives.** The Internet Archive and national libraries crawl the web to keep a record of it; the Heritrix crawler of the Internet Archive is open source.
- **Research corpora.** Open crawls give text and link data for research in information retrieval and language processing.
- **Monitoring and data mining.** Price comparison, copyright monitoring and the study of the [structure of the web](/bow-tie-web-structure/) all start with a crawl.

## References
