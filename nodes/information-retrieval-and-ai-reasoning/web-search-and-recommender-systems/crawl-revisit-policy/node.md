---
tag: 31V6NY
kind: problem
slug: crawl-revisit-policy
name: Crawl revisit policy
aliases:
- page refresh scheduling
- crawl freshness optimization
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Choose how often to refetch each page, given its change rate, so that the average freshness of the local copy is highest.
prereqs: [web-crawling, poisson-distribution, convex-function, jensens-inequality]
see_also: [url-frontier, focused-crawling, markov-chain, near-duplicate-document-detection, pagerank]
sources:
  - paper: "Junghoo Cho and Hector Garcia-Molina, Effective page refresh policies for Web crawlers, ACM Transactions on Database Systems 28(4), 390-426, 2003"
    locator: the definitions of freshness and age, the Poisson model of change, the time-averaged freshness and age of fixed-order, random-order and purely random refresh, the comparison of uniform and proportional allocation, and the optimal allocation
  - paper: "Junghoo Cho and Hector Garcia-Molina, Synchronizing a database to improve freshness, Proceedings of the 2000 ACM SIGMOD International Conference on Management of Data"
    locator: the first statement of the freshness and age measures and of the result that uniform allocation is better than proportional allocation
  - paper: "Junghoo Cho and Hector Garcia-Molina, Estimating frequency of change, ACM Transactions on Internet Technology 3(3), 2003"
    locator: the estimators of the change rate of a page from repeated visits that see only whether the page changed
  - paper: "Christopher Olston and Marc Najork, Web crawling, Foundations and Trends in Information Retrieval 4(3), 175-246, 2010"
    locator: the chapter on revisiting pages for freshness, which surveys the Poisson model, the policies and later work on weighting by importance and content change
---

The crawl revisit policy problem asks how often a [crawler](/web-crawling/) should fetch each page again, so that its stored copies stay close to the live web. The crawler can fetch only a fixed number of pages per day, and pages change at very different rates: a news front page changes every few minutes, and an old paper never changes. Junghoo Cho and Hector Garcia-Molina modelled the changes of each page as a Poisson process, defined the freshness and the age of a copy, and proved a result that surprised many people: spreading the fetches evenly over all pages gives a higher average freshness than fetching each page in proportion to how often it changes. The best policy even gives up on pages that change too often. Real crawlers estimate the rates from past visits, weigh pages by importance, and measure how well the policy does.

## In plain words

A search engine keeps a copy of each page it has read, but the real pages keep changing, so some copies go out of date. The crawler can only reread a fixed number of pages each day. The question is how to share those rereads between the pages. It seems natural to reread a page more often if it changes more often. But a page that changes all the time is out of date again a moment after the reread, so time spent on it is mostly wasted. A page that changes now and then stays good for a long time after each reread. So it is better to spend the effort on pages that you can actually keep up to date. Giving every page the same share already beats giving shares by change rate, and a careful split does a bit better still.

## Definition

There are $N$ pages. Page $i$ changes at the times of a Poisson process with rate $\lambda_i > 0$, independently of the other pages. The crawler refreshes page $i$ at rate $f_i \ge 0$, at equal intervals of length $I_i = 1/f_i$ (fixed-order refresh), and the total rate is fixed: $\sum_i f_i = F$. A refresh copies the live page at that moment.

- The **freshness** of page $i$ at time $t$ is $F_i(t) = 1$ if the copy equals the live page, and 0 if not.
- The **age** of page $i$ at time $t$ is $A_i(t) = 0$ if the copy is fresh, and else $t$ minus the time of the first change since the last refresh.

The freshness of the collection is $\frac{1}{N} \sum_i F_i(t)$ and its age is $\frac{1}{N} \sum_i A_i(t)$. Their long-run time averages are $\bar F$ and $\bar A$. The task is to choose the rates $f_i$ that maximize $\bar F$, or minimize $\bar A$, under $\sum_i f_i = F$.

For one page with rate $\lambda$ and refresh interval $I$, the copy is fresh at time $t \in [0, I)$ after a refresh with probability $e^{-\lambda t}$, the chance of no change in $[0, t]$. So the expected fraction of time it is fresh is

$$\frac{1}{I} \int_0^I e^{-\lambda t}\, dt = \frac{1 - e^{-r}}{r} =: g(r), \qquad r = \lambda I = \lambda / f.$$

If the first change after the refresh is at time $s \le t$, the age at time $t$ is $t - s$. Averaging over $s$ and over $t \in [0, I)$ gives the expected time-averaged age

$$\bar A = \frac{1}{f} \left( \frac{1}{2} - \frac{1}{r} + \frac{1 - e^{-r}}{r^2} \right) =: \frac{\varphi(r)}{f}.$$

Both depend on the page only through $r$, the expected number of changes between two refreshes. With $f = 0$ the page is never fresh in the long run.

## Variants

- **Order of refreshes.** Cho and Garcia-Molina also study random-order refresh, which refreshes each page once per cycle in a new random order, and purely random refresh, which picks the next page at random. For purely random refresh at rate $f$, the copy is a two-state [Markov chain](/markov-chain/) that goes stale at rate $\lambda$ and fresh at rate $f$, so $\bar F = f/(f + \lambda) = 1/(1 + r)$. Fixed order gives the highest freshness of the three.
- **Weights.** Weigh page $i$ by an importance $w_i$, such as its [PageRank](/pagerank/) or how often users click it, and maximize $\sum_i w_i \bar F_i$.
- **Unknown rates.** The rates are not given and must be estimated from past visits, which show only whether the page changed since the last visit, not how many times.
- **Degree of change.** Count a change only if it matters, for example if the page is no longer a [near duplicate](/near-duplicate-document-detection/) of the copy, or if the change affects search results.
- **Politeness.** The refreshes must also respect a gap per host, so the schedule feeds a [URL frontier](/url-frontier/).

## Examples

Take two pages with $\lambda_1 = 9$ and $\lambda_2 = 1$ changes per day, and $F = 2$ refreshes per day.

| policy | $f_1, f_2$ | freshness of page 1, 2 | mean freshness | mean age (days) |
|---|---|---|---|---|
| uniform | 1, 1 | 0.1111, 0.6321 | 0.3716 | 0.2667 |
| proportional | 1.8, 0.2 | 0.1987, 0.1987 | 0.1987 | 0.9437 |
| best for freshness | 0.2359, 1.7641 | | 0.3948 | |
| best for age | 1.1514, 0.8486 | | | 0.2570 |

The proportional policy gives both pages $r = 5$, so both are fresh only about a fifth of the time. The uniform policy lets page 2 stay fresh 63% of the time and loses little on page 1, which would be stale most of the time anyway. The best policy for freshness gives the fast page only about one refresh in four days, while the best policy for age gives it more refreshes than the slow page, because age punishes a copy more the longer it has been stale.

## Known algorithms

**Uniform allocation.** Set $f_i = F/N$. It needs no estimates of the rates and is at least as good as proportional allocation for both freshness and age (see Bounds).

**Optimal allocation.** For freshness, maximize $\sum_i \bar F_i(f_i)$ with $\bar F_i(f) = \frac{f}{\lambda_i}\left(1 - e^{-\lambda_i/f}\right)$, subject to $\sum_i f_i = F$ and $f_i \ge 0$. Each $\bar F_i$ is concave and increasing in $f$, so the optimum has the same marginal gain $\bar F_i'(f_i) = \mu$ on every page with $f_i > 0$, and a page gets $f_i = 0$ when even its first refresh gains less than $\mu$. Find $\mu$ by bisection, and each $f_i$ by a one-dimensional search. Cho and Garcia-Molina solve it this way and show that the optimal $f_i$ first grows with $\lambda_i$ and then falls, so that the pages that change fastest get few refreshes or none.

**Estimating the rates.** A crawler that visits page $i$ every $I$ days and sees a change in $X$ of $n$ visits can use $\hat\lambda = -\ln(1 - X/n)/I$, since the chance of at least one change in an interval is $1 - e^{-\lambda I}$. Cho and Garcia-Molina give corrected estimators for small $n$ and for visits at irregular times.

**In practice.** Crawlers sort known pages into tiers by estimated change rate and importance, and refresh each tier at its own rate. The tiers then set priorities in the frontier.

## Bounds

**Theorem.** For all rates $\lambda_1, \ldots, \lambda_N > 0$ and budget $F > 0$, uniform allocation gives at least the mean freshness and at most the mean age of proportional allocation $f_i = F \lambda_i / \sum_j \lambda_j$. Both comparisons are strict unless all $\lambda_i$ are equal.

*Proof.* Let $\bar f = F/N$, $r_i = \lambda_i / \bar f$ and $\bar r = \frac{1}{N} \sum_i r_i$. Under proportional allocation, $\lambda_i / f_i = \sum_j \lambda_j / F = \bar r$ for every page.

First, $g$ is strictly convex and $\varphi$ is strictly concave on $(0, \infty)$, because

$$g(r) = \int_0^1 e^{-rs}\, ds, \qquad \varphi(r) = \int_0^1 (1 - s)\left(1 - e^{-rs}\right) ds.$$

The first identity is direct integration. For the second, the age at time $\tau / f$ after a refresh, times $f$, has expectation $\tau - (1 - e^{-r\tau})/r = \int_0^\tau (1 - e^{-rs})\, ds$; its mean over $\tau \in [0, 1]$ is $\int_0^1 (1 - s)(1 - e^{-rs})\, ds$, and integration confirms that this equals $\frac{1}{2} - \frac{1}{r} + \frac{1 - e^{-r}}{r^2}$. Each $e^{-rs}$ with $s > 0$ is strictly convex in $r$, the weights $1$ and $1 - s$ are positive on $(0, 1)$, and an integral of convex functions with positive weights is convex. The second derivatives are $\int_0^1 s^2 e^{-rs} ds > 0$ and $-\int_0^1 (1 - s) s^2 e^{-rs} ds < 0$.

Freshness. Uniform gives $\frac{1}{N} \sum_i g(r_i)$ and proportional gives $g(\bar r)$. By [Jensen's inequality](/jensens-inequality/) for the convex $g$, $\frac{1}{N} \sum_i g(r_i) \ge g(\bar r)$, with equality only if all $r_i$ are equal.

Age. Uniform gives $\frac{1}{N} \sum_i \varphi(r_i) / \bar f$. Proportional gives $\frac{1}{N} \sum_i \varphi(\bar r)/f_i$, and $f_i = \lambda_i / \bar r = \bar f r_i / \bar r$, so it equals $\frac{\varphi(\bar r)}{\bar f} \cdot \bar r \cdot \frac{1}{N} \sum_i \frac{1}{r_i}$. By Jensen for the concave $\varphi$, $\frac{1}{N} \sum_i \varphi(r_i) \le \varphi(\bar r)$. By the inequality of the arithmetic and harmonic means, $\bar r \cdot \frac{1}{N} \sum_i 1/r_i \ge 1$, and $\varphi(\bar r) > 0$ because the integrand is positive. Together, the uniform age is at most the proportional age, with equality only if all $r_i$ are equal. $\square$

**Other facts.** $g(r) \le 1$ and $g(r) \ge 1 - r/2$, so a page with $r$ well below 1 is almost always fresh; and $g(r) < 1/r$, so a page refreshed at rate $f$ adds less than $f/\lambda$ to the freshness sum, which is why fast pages are a poor use of the budget. Under the same constraints, fixed-order refresh gives at least the freshness of purely random refresh: $g(r) \ge 1/(1 + r)$ for all $r > 0$, which is $e^{r} \ge 1 + r$ rearranged.

## Reductions

- The optimal allocation is a separable concave resource allocation problem: maximize a sum of concave functions of $f_i$ under one linear budget. Greedy allocation in small units, or a search on the common marginal gain, solves it.
- With weights $w_i$, the same method applies with $w_i \bar F_i$ in place of $\bar F_i$.
- The schedule of refresh times for given rates is a scheduling problem with a gap per host, handled by the frontier.

## Applications

- **Incremental crawlers of web search engines.** The revisit policy decides which known pages to fetch again, and splits the crawl budget between new and known pages.
- **Caches and replicas.** The same model applies to caches that poll an origin server, to mirrors of databases, and to feeds that must be polled for new items.
- **Web archives.** An archive that wants to keep many versions of each page chooses revisit rates by change rate and by how much each version is worth.

## References
