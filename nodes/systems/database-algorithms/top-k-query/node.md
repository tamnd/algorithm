---
tag: CPM00E
kind: problem
slug: top-k-query
name: Top-k query problem
aliases:
- top-k selection over aggregated scores
- top-k aggregation query
area: systems/database-algorithms
level: advanced
summary: "Given m lists that grade the same objects, each sorted by its grade, find the k objects with the highest combined score while reading as little of the lists as possible."
prereqs: [top-k-selection, priority-queue]
see_also: [fagin-algorithm, threshold-algorithm, no-random-access-algorithm, k-way-merge, pareto-front-computation, hash-table, selection-problem]
sources:
  - paper: doi:10.1145/1391729.1391730
    title: Ihab F. Ilyas, George Beskales and Mohamed A. Soliman, A survey of top-k query processing techniques in relational database systems, ACM Computing Surveys 40(4), Article 11 (2008)
    locator: Section 2 (the top-k problem, access models and a classification of techniques) and the sections on top-k over sorted lists
  - paper: doi:10.1016/S0022-0000(03)00026-6
    title: Ronald Fagin, Amnon Lotem and Moni Naor, Optimal aggregation algorithms for middleware, Journal of Computer and System Sciences 66(4), 614 to 656 (2003)
    locator: Section 2 (the model with sorted and random access and the middleware cost), Section 5 (instance optimality), Sections 6 and 8 (TA, NRA and CA results), Section 9 (lower bounds)
  - paper: doi:10.1006/jcss.1998.1600
    title: Ronald Fagin, Combining fuzzy information from multiple systems, Journal of Computer and System Sciences 58(1), 83 to 99 (1999)
    locator: the problem of combining graded sources with a monotone function, and the probabilistic upper and lower bounds
  - paper: "Michael J. Carey and Donald Kossmann, On saying \"enough already!\" in SQL, Proceedings of ACM SIGMOD 1997, 219 to 230"
    locator: the STOP AFTER clause for top-k queries in SQL and its processing
---

A top-k query asks for the $k$ best objects under a scoring function that combines several grades of each object. In the setting of Fagin's middleware model, each of $m$ sources holds the same $N$ objects as a list sorted by its own grade, and the score is a monotone function $t$ of the $m$ grades, such as their sum or minimum. The goal is to find the top $k$ while reading as few list entries as possible, usually far fewer than $m N$. The problem differs from [top-k selection](/top-k-selection/), where the scores are given and every item must be read: here the scores must be assembled from separate sorted sources, and the sorted order lets an algorithm stop early.

## In plain words

Several web sites each rank the same hotels: one by price, one by reviews, one by distance to the beach. Each site gives you its list from best to worst. You want the 3 hotels with the best total score.

You could read every list to the end, add up the scores of each hotel, and pick the best 3. But the lists are long, and the best hotels are probably near the top of most lists.

The question is how far down the lists you must read before you can be sure which 3 hotels are best. If a site can also tell you the score of one hotel when you ask, you may be able to stop sooner.

## Definition

A *database* has $N$ objects and $m$ lists $L_1, \ldots, L_m$. List $L_i$ holds each object $R$ once with a grade $x_i(R)$, usually in $[0, 1]$, sorted from the highest grade to the lowest. An *aggregation function* $t: \mathbb{R}^m \to \mathbb{R}$ is *monotone* if $x_i \le x'_i$ for all $i$ implies $t(x_1, \ldots, x_m) \le t(x'_1, \ldots, x'_m)$. The score of $R$ is $t(R) = t(x_1(R), \ldots, x_m(R))$.

Given $k \le N$, a *top $k$ set* is a set $Y$ of $k$ objects with $t(y) \ge t(z)$ for every $y \in Y$ and $z \notin Y$. Ties can make several sets valid; any one of them is a correct answer. Some versions also ask for the scores of the objects in $Y$, or for $Y$ in order of score.

An algorithm reaches the data in two ways:

- **Sorted access** reads the next entry $(R, x_i(R))$ of list $L_i$, from the top down.
- **Random access** asks list $L_i$ for the grade $x_i(R)$ of a given object $R$.

If an algorithm makes $s$ sorted and $r$ random accesses, its *middleware cost* is $s c_S + r c_R$ for fixed positive costs $c_S$ and $c_R$. Computation inside the algorithm is not counted. A function $t$ is *strict* if $t(x_1, \ldots, x_m) = 1$ only when every $x_i = 1$; min and the average are strict, max is not.

## Variants

- **Access model.** Both sorted and random access; sorted access only (sources that only stream results); random access only on some lists; or random access much more costly than sorted access.
- **Scores or set.** Return the top $k$ with exact scores, in rank order, or only the set.
- **Exact or approximate.** A $\theta$-approximation, for $\theta > 1$, returns $k$ objects $Y$ with $\theta \cdot t(y) \ge t(z)$ for all $y \in Y$, $z \notin Y$.
- **SQL top-k.** `ORDER BY ... LIMIT k` (or `FETCH FIRST k ROWS ONLY`) over a join or a scan, where the score is an expression over the columns of the result. When the lists are the inputs of a join on a key other than a shared object identity, this is a *top-k join* or *rank join*.
- **Distributed top-k.** The lists are on different machines, and the cost is the number of messages or rounds.

## Examples

Two lists, $t = $ sum, $k = 2$:

| depth | $L_1$ | $L_2$ |
|---|---|---|
| 1 | a 0.9 | c 0.9 |
| 2 | b 0.8 | a 0.8 |
| 3 | c 0.7 | e 0.7 |
| 4 | d 0.6 | b 0.4 |
| 5 | e 0.1 | d 0.2 |

The scores are a 1.7, c 1.6, b 1.2, e 0.8 and d 0.8, so the answer is a and c. [Fagin's algorithm](/fagin-algorithm/) reads to depth 3, the [threshold algorithm](/threshold-algorithm/) to depth 2, and a full scan to depth 5. With $t = \max$ and $k = 1$, the answer is a or c (both score 0.9), and the first entry of each list is enough.

A *non-monotone* $t$ shows why monotonicity matters. With $t(x_1, x_2) = 1 - |x_1 - x_2|$, an object at the bottom of both lists with two equal grades scores 1, the highest possible score, so grades read higher up say nothing about the objects below, and an algorithm must read every object.

## Known algorithms

| Algorithm | Access | Idea | Guarantee |
|---|---|---|---|
| Full scan and [top-k selection](/top-k-selection/) | sorted only | read all lists, compute every score | $m N$ sorted accesses |
| [Fagin's algorithm (FA)](/fagin-algorithm/), 1996 | sorted and random | read in parallel until $k$ objects are seen in every list, then look up missing grades | $O(N^{(m-1)/m} k^{1/m})$ with high probability for independent lists |
| [Threshold algorithm (TA)](/threshold-algorithm/), 2001 | sorted and random | score each object on first sight; stop when $k$ scores reach $t$ of the last grades read | instance optimal over algorithms without wild guesses |
| [No-random-access algorithm (NRA)](/no-random-access-algorithm/), 2001 | sorted only | keep lower and upper bounds on each seen score | instance optimal over algorithms without random access, ratio $m$ |
| Combined algorithm (CA), 2001 | sorted, costly random | run NRA, and every $\lfloor c_R / c_S \rfloor$ rounds look up the most promising object | on databases with distinct grades, instance optimal with a ratio that does not depend on $c_R / c_S$, for $t$ strictly monotone in each argument (ratio at most $4m + k$) and for min |

TA was also found, independently, by Nepal and Ramakrishna (1999) and by Güntzer, Balke and Kießling (2000). Many later algorithms adapt these to joins, to probabilistic data and to distributed settings.

## Bounds

- **Trivial.** $m N$ sorted accesses always suffice.
- **Worst case.** On some databases every correct algorithm without wild guesses reads $\Omega(N)$ entries. Take $t = \min$ and two lists in opposite orders: the best object is in the middle of both lists.
- **Random independent lists.** For a strict monotone $t$, constant $m$ and lists in independent random orders, every correct algorithm has cost $\Omega(N^{(m-1)/m} k^{1/m})$ with high probability, and Fagin's algorithm matches this.
- **Instance optimality.** TA's cost on every database is at most $m + m(m-1) c_R / c_S$ times the cost of any correct algorithm without wild guesses, plus a constant. NRA's cost is at most $m$ times that of any correct algorithm without random access, plus a constant. For strict $t$, both ratios are exact and best possible.
- **Wild guesses.** If algorithms may make random accesses to objects they have not yet seen, no algorithm is instance optimal: a lucky guess can find the answer at constant cost on some database.
- **Exact scores without random access.** Some databases force any algorithm without random access to read to the end of a list to learn the exact score of a top object, even though the top set is known much earlier.

## Reductions

- **From top-k selection.** With $m = 1$ and $t$ the identity, the answer is the first $k$ entries of the list. With all scores in memory, the problem is [top-k selection](/top-k-selection/) on the $N$ scores, solved in $O(m N)$ time.
- **To merging for max.** For $t = \max$, the top $k$ are the first $k$ distinct objects of a [k-way merge](/k-way-merge/) of the lists.
- **Relation to skylines.** For a strictly monotone $t$, every top-1 object is on the [Pareto front](/pareto-front-computation/) (the skyline) of the grade vectors. Conversely, on a finite set, each skyline point is a top-1 answer for some strictly monotone function. This is why skyline queries are used when no single $t$ is known; see [BNL](/bnl-skyline/) and [SFS](/sort-filter-skyline/).
- **To rank joins.** A top-k query is a rank join of the $m$ lists on the object identity; rank join algorithms generalize TA and NRA to arbitrary join keys.

## Applications

- **Multimedia middleware.** IBM's Garlic system combined graded results such as color and shape similarity from image search engines; this was the motivating application of Fagin's work.
- **Information retrieval.** Each query term has an inverted list sorted by term score, and the document score is a monotone sum; TA-style early stopping avoids reading full lists.
- **Databases.** `ORDER BY ... LIMIT k` queries, rank-aware query optimization and top-k joins.
- **Recommendation and metasearch.** Combine the rankings of several services or features for the same items.

## References
