---
tag: STWF16
kind: technique
slug: what-if-index-analysis
name: What-if index analysis
aliases:
- hypothetical indexes
- what-if optimizer calls
area: databases/storage-and-indexing
level: advanced
summary: "Estimate the benefit of an index without building it by giving the optimizer statistics of a hypothetical index and costing the plans."
prereqs: [query-optimization, cost-model, histogram]
see_also: [index-selection, autoadmin-index-selection, access-path-selection, selectivity, cardinality-estimation, reservoir-sampling, partial-index, view-selection]
sources:
  - paper: doi:10.1145/276304.276337
    title: "Surajit Chaudhuri and Vivek Narasayya, AutoAdmin what-if index analysis utility, Proceedings of ACM SIGMOD 1998"
    locator: pp. 367 to 378, hypothetical indexes with metadata and sampled statistics only, the interface that makes the optimizer cost a query under a chosen configuration, and the analysis of workloads with it
  - url: http://www.vldb.org/conf/1997/P146.PDF
    title: "Surajit Chaudhuri and Vivek Narasayya, An efficient, cost-driven index selection tool for Microsoft SQL Server, Proceedings of VLDB 1997"
    locator: pp. 146 to 155, the index selection tool that gets all its costs from the optimizer and reduces the number of these calls
---

What-if index analysis asks the query optimizer what a query would cost if some indexes existed, without building them. The optimizer of a relational database chooses plans by a [cost model](/cost-model/) that reads only the *metadata* of an index (its columns, its number of entries and pages, its height) and the *statistics* of its columns, such as a [histogram](/histogram/). It never reads the index data while it plans. So a tool can add a *hypothetical index* to the catalog, with metadata computed from the table size and statistics built from a sample, call the optimizer, and read the cost and the plan. Building the real index needs a sort of the whole table; a hypothetical one needs a small sample. Chaudhuri and Narasayya made this interface for SQL Server in 1998, and index advisors such as the [AutoAdmin tool](/autoadmin-index-selection/) get all their costs this way.

## In plain words

Before you buy a new shelf for a shop, you want to know how much time it would save. You do not build it to find out. You tell the planner "imagine a shelf here, this tall, with these items", and the planner works out the new walking routes on paper. The planner only ever looks at the drawing and at counts of the items, never at a real shelf, so the answer on paper is the same as the answer with a real shelf. Then you rub the drawing out.

The counts are the weak point. If you count only a sample of the items, the planner's answer can be off, most of all for rare items.

## When it applies

- The optimizer is cost-based, and its cost model uses only metadata and statistics of indexes, not their contents.
- Many index configurations must be compared, as in [index selection](/index-selection/), and building each one would take far too long or disturb the running system.
- The question is a comparison of plans and costs, not a measured run time. What-if analysis answers "what would the optimizer do", which is also the plan the system would run.

## The template

```pseudo id=main
WHAT-IF(Q, C)                                    ▷ the cost and plan of query Q if the hypothetical indexes C existed
L1  for each index h in C that does not exist: add to the catalog its metadata (columns, entries, pages, height), marked hypothetical
L2      build the statistics of the columns of h from a sample of the table
L3  (plan, cost) ← OPTIMIZE(Q)                   ▷ the optimizer sees the real and the hypothetical indexes, and runs nothing
L4  remove the hypothetical metadata and statistics from the catalog; return (plan, cost)
```

A call can also hide real indexes, so that a tool can ask what happens if an index is dropped. The hypothetical indexes must be visible only to the optimizer calls of the tool, so that no other query ever plans with them.

**Why it is exact for the optimizer.** The cost of a plan is a function of the metadata and the statistics alone. If a hypothetical index gets the same metadata and statistics as the real index would have, the optimizer gives the same plan and the same cost for it as for the real index. Only the statistics from a sample can differ, and that difference is the only error of the method, besides the error of the cost model itself.

**Cost.** The metadata of a B+ tree follow from the table size and the key width: $\lceil N / L \rceil$ leaf pages for $L$ entries per leaf and a height of about $\log_F$ of that for fanout $F$. A sample of $s$ rows costs $O(s \log s)$ to make a histogram from, against $\Theta(N \log N)$ to build the index. Each call then costs one optimization.

## Classic examples

These come from the code on this page: a table of $N = 100{,}000$ rows (seed 7), 50 rows per page, so a full scan reads 2,000 pages; a B+ tree with 200 entries per leaf and fanout 200, so 500 leaf pages and height 3; histograms with 20 buckets; and one page read per row fetched by an index.

| query on column $a$ (uniform) | what-if, 5% sample | what-if, all rows | with the built index | pages read when run |
|---|---|---|---|---|
| $1000 \le a \le 1999$ (101 rows) | index, 106.4 | index, 102.1 | index, 102.1 | 104 |
| $0 \le a \le 49999$ (4,961 rows) | scan, 2,000 | scan, 2,000 | scan, 2,000 | 2,000 |

The what-if call with a 5% sample read 5,000 rows; building the index read all 100,000 and sorted them. With statistics from all rows, the hypothetical cost equals the cost with the built index exactly, as the template says, and the tests check this on 200 random queries over two columns. The estimate is a measurement of the cost model, so it can differ from the pages a run reads (102.1 against 104).

**Skewed data.** On a second column with a heavy-tailed (Pareto) distribution, over 300 small range queries, the median ratio of the sampled estimate to the pages read was 1.0. For 10% of the queries the estimate was more than 2.8 times too large, and in the worst case it was about 100 times too small (a measurement). A 5% sample sees too few rows of the rare values.

**Index advisors.** The AutoAdmin tool of SQL Server makes thousands of what-if calls to compare configurations, and reduces their number with atomic configurations. Later tools work the same way, and the PostgreSQL extension HypoPG adds hypothetical indexes for the same purpose.

## Variations

- **Hiding indexes.** A call can pretend that a real index is gone, to estimate the effect of dropping it.
- **Other structures.** The same idea applies to materialized views ([view selection](/view-selection/)), partitionings and [partial indexes](/partial-index/): anything whose effect on the optimizer goes through metadata and statistics.
- **Virtual indexes.** Some systems store hypothetical indexes in the catalog with no storage, for example Oracle's `NOSEGMENT` indexes, so that the normal `EXPLAIN` uses them.
- **Statistics reuse.** Indexes with the same leading column share the statistics of that column, so a tool builds them once.
- **Plan inspection.** Besides the cost, a call returns the plan, so a tool can see which indexes a query uses and build reports, such as which queries an index would serve.

## Pitfalls

- **Bad statistics.** The estimate is only as good as the statistics. A small sample misses rare values and the tail of a skewed column; correlated columns break the independence assumption of the [cardinality estimates](/cardinality-estimation/). The what-if cost can then be far from the real one.
- **The cost model is not the run time.** A what-if call says what the optimizer believes, not what will happen. Caching, concurrency and the real layout of the data on disk are not in the estimate. Check important choices with real runs.
- **Missing maintenance cost.** A select-only what-if call does not show the cost of keeping the index up to date. Include the inserts, updates and deletes of the workload.
- **Leaking hypothetical indexes.** If a hypothetical index stays in the catalog, other sessions can get plans that use an index that does not exist. Keep them private to the session of the tool and remove them after the call.
- **Too many calls.** Each call is a full optimization. A tool that costs every configuration of every query makes far too many calls; derive costs from those of smaller configurations where the optimizer model allows it.

## Exercises

1. A table has $10^7$ rows; a leaf holds 300 entries and an inner page 300 children. Compute the leaf pages and the height of the hypothetical index that L1 puts in the catalog.
2. Show that if the cost of every plan depends only on metadata and statistics, a hypothetical index with exact statistics gets the same plan and cost as the real index.
3. A column has 1,000,000 rows, and one value occurs in 50 of them. What is the chance that a uniform sample of 5% contains none of those rows? What does the optimizer then estimate for an equality query on that value, and what would it choose?

## References
