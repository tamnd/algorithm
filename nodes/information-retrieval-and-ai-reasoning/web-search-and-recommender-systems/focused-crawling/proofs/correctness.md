---
title: The best-first focused crawler fetches the page of largest priority at each step
proves: [correctness]
status: full
---

The input is a directed graph given by the out-links $\mathrm{out}(u)$ of each page, a set $S$ of seeds, a relevance score $R(u) \in [0, 1]$, a budget $k \ge 0$, and, for hard focus, a threshold $\theta$. Page ids are totally ordered. The line numbers are those of the pseudocode on the page. This file proves what the crawler does. It does not prove that the crawler finds more relevant pages than another order: that is a measured property of the web and of the classifier.

Call a fetched page $u$ *expanded* if its links are followed: always for soft focus, and when $R(u) \ge \theta$ for hard focus. For a set $D$ of fetched pages, the priority of a page $v \notin D$ is

$$\pi_D(v) = \max\left(\{1 : v \in S\} \cup \{R(u) : u \in D \text{ expanded},\ v \in \mathrm{out}(u)\}\right),$$

defined when the set is not empty, that is, when $v$ is a seed or has a link from an expanded page of $D$. These $v$ are the *discovered* pages.

**Lemma 1 (invariant).** Let $D$ be the set fetched so far. At each test of line L3:

1. The keys of prio are the pages that are seeds or are linked from an expanded page of $D$ (fetched or not), and for each discovered $v \notin D$, $\mathrm{prio}(v) = \pi_D(v)$.
2. For each discovered $v \notin D$, the heap holds the entry $(\mathrm{prio}(v), v)$.
3. Every other heap entry $(p, v)$ has $v \in D$ or $p < \mathrm{prio}(v)$.

*Proof.* After line L1 no page is fetched, prio is 1 on the seeds, and the heap holds $(1, s)$ for each seed once. So the claims hold.

Suppose they hold and lines L4 to L10 run. If line L5 skips the entry $(p, u)$, then $u \in D$ or $p < \mathrm{prio}(u)$, so by claim 2 the entry is not the one that claim 2 needs, and removing it keeps all three claims. Else $u \notin D$ and $p = \mathrm{prio}(u)$; line L6 fetches $u$, and $D$ grows to $D' = D \cup \{u\}$. The entry for $u$ is gone, and $u \in D'$, so claims 2 and 3 do not speak of $u$ any more. If $u$ is not expanded (line L7), then $\pi_{D'}(v) = \pi_D(v)$ for all $v \notin D'$, and nothing else changes. If $u$ is expanded, then for $v \in \mathrm{out}(u)$ with $v \notin D'$, $\pi_{D'}(v) = \max(\pi_D(v), R(u))$, or $R(u)$ if $v$ was not discovered. Lines L9 and L10 set prio$(v)$ to exactly this value, and push a new entry when it changes. The old entry of $v$ now has a key less than prio$(v)$, which meets claim 3. Priorities of other pages do not change. $\square$

**Theorem 2 (the rule of choice).** The $j$-th page that the crawler fetches is the discovered page $v \notin D$ with the largest $\pi_D(v)$, ties to the smallest id, where $D$ is the set of the first $j - 1$ fetched pages. The crawler stops when it has fetched $k$ pages or no discovered page is left.

*Proof.* The heap returns the entry with the largest key, ties to the smallest id. By claims 2 and 3 of Lemma 1, the entries with $v \notin D$ and key prio$(v)$ are exactly one for each discovered unfetched page, and every other entry is skipped at line L5. A stale entry $(p, v)$ with $v \notin D$ has $p < \mathrm{prio}(v)$, and the current entry of $v$ is also in the heap, so a stale entry never hides a page. The first entry that passes line L5 therefore belongs to the page described. When the heap is empty, no discovered page is unfetched. $\square$

**Corollary 3.** Each page is fetched at most once, and only pages reachable from $S$ are fetched. With soft focus and $k$ at least the number of reachable pages, every page reachable from $S$ is fetched. With hard focus, each fetched page that is not a seed has a link from a fetched page $u$ with $R(u) \ge \theta$.

*Proof.* Line L5 rejects pages of $D$. A discovered page is a seed or has a link from a fetched page, so by induction it is reachable. With soft focus every fetched page is expanded; if a reachable page were never fetched, the first such page on a path from a seed would have a fetched predecessor and so be discovered, against Theorem 2. For hard focus, a non-seed page is discovered only through an expanded page. $\square$

Lazy deletion is what keeps the update of line L10 cheap. A heap with a decrease-key operation and a map from pages to heap positions gives the same order.

**Cost.** Line L1 pushes $|S|$ entries. Each expanded page $u$ pushes at most $|\mathrm{out}(u)|$ entries. So the heap gets at most $|S| + m'$ entries in total, where $m'$ is the number of links of the fetched pages, and each push and pop costs $O(\log(|S| + m'))$. With hash tables for prio and $D$, the crawl costs $O((|S| + m') \log(|S| + m'))$ expected time and $O(|S| + m')$ space, plus $k$ fetches and $k$ calls of $R$, which in practice cost far more than the heap.

**Measured, not proved.** The crawl reaches more relevant pages early only if relevant pages tend to link to relevant pages and if $R$ is a good classifier. The test file plants such a graph: 1000 pages, 20% on topic, 6 links per page, each link staying in the class of its page with probability 0.6, and a naive Bayes classifier trained on separate pages. On ten fixed seeds and a budget of 200, the share of on-topic pages among the fetched pages is between 0.58 and 0.635 for the focused crawler and between 0.275 and 0.48 for breadth-first search. When the links go to random pages (probability 0 of staying in the class), the same run gives a mean of 0.2175 for the focused crawler and 0.203 for breadth-first search, close to the 20% base rate.
