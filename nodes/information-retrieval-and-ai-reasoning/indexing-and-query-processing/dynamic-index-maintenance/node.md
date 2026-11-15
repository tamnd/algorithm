---
tag: N1B6Q8
kind: problem
slug: dynamic-index-maintenance
name: Dynamic index maintenance
aliases:
- incremental index update
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Keep an inverted index current while documents are added and deleted, with fast queries and low merge cost.
prereqs: [inverted-index]
see_also: [logarithmic-merging, geometric-partitioning, single-pass-in-memory-indexing, blocked-sort-based-indexing, log-structured-merge-tree, decomposable-searching-problem, tombstone, posting-list]
sources:
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 7 (dynamic inverted indices), Section 7.2 (incremental index updates), Section 7.3 (document deletions), with Section 7.3.1 (the invalidation list) and Section 7.3.2 (garbage collection)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 4, Section 4.5 (dynamic indexing, the auxiliary index, the invalidation bit vector for deleted documents, and logarithmic merging)
  - paper: doi:10.1145/1099554.1099739
    title: Nicholas Lester, Alistair Moffat and Justin Zobel, Fast on-line index construction by geometric partitioning, Proceedings of the 14th ACM International Conference on Information and Knowledge Management (CIKM 2005), pages 776 to 783
    locator: Section 3 (the update strategies rebuild, in-place update and remerge, and their costs)
  - paper: doi:10.1145/1386118.1386125
    title: Nicholas Lester, Alistair Moffat and Justin Zobel, Efficient online index construction for text databases, ACM Transactions on Database Systems 33(3), Article 19, 2008
    locator: the comparison of in-place, remerge and geometric strategies on growing collections
---

Dynamic index maintenance asks how to keep an [inverted index](/inverted-index/) correct while documents are added, deleted and changed, and while queries keep arriving. Every query must see the index of the documents that exist at that moment. The costs are the work spent on the index files, mostly the postings written by merges, the number of separate pieces a query must read, and the delay before a new document can be found. This page states the problem and compares the strategies. The strategies with their own pages are [logarithmic merging](/logarithmic-merging/) and [geometric partitioning](/geometric-partitioning/). The static build of one index, with no updates, is the subject of [single-pass in-memory indexing](/single-pass-in-memory-indexing/) and [blocked sort-based indexing](/blocked-sort-based-indexing/).

## In plain words

An index for a fixed set of documents is built once. But many collections change: new pages, new mail, edited files. Building the whole index again after every change is far too slow. Adding new entries into the middle of the stored lists is slow too, because the lists are packed tight on disk. The usual answer is to collect new entries in memory and, when memory is full, write them out as a new small index. Queries then read the big index and the small ones. With time there are too many small ones, so they are merged. The question is when to merge, so that merging is cheap and queries stay fast. Deleted documents are first only marked as deleted, and removed for real at the next merge.

## Definition

The collection changes by a sequence of operations:

- `add(d)`: add a new document $d$ with a new id, larger than all ids so far;
- `delete(d)`: remove document $d$;
- `update(d)`: replace the text of $d$, which is a `delete` followed by an `add`;
- `postings(t)`: return the posting list of term $t$ over the documents that exist now.

The answer to `postings(t)` must be the list that an index built from scratch over the current documents would give. The machine has a memory of $M$ postings and a disk. After $T$ postings have been added, a strategy is measured by:

- **merge cost**, the total number of postings it has written to disk, at least $T$;
- **query cost**, the number of partitions, separate pieces of the index on disk, that `postings(t)` must read;
- **freshness**, the time from `add(d)` until a query can find $d$.

The goal is a low merge cost and a low query cost at once. The two pull in opposite directions.

## Variants

- **Append only.** Documents are only added, as in an archive or a crawl that grows. This is the case most of the analysis treats.
- **With deletions.** Deleted documents are kept in a list of invalid ids, and every query removes them from its results. A merge drops their postings, which is garbage collection. A collection with many updates holds many invalid postings between merges.
- **In memory or on disk.** If the whole index fits in memory, the lists can grow in place, and the problem is the cost of reallocation. The classic problem is the on-disk index, where lists are stored contiguous for fast reading.
- **Contiguous or split lists.** A strategy may require that each list sits in one place on disk, or allow it to be spread over partitions, at the cost of more seeks per query.

## Examples

Let the memory hold $b$ postings, and let each flush write a full memory of $b$ new postings. After $m = 8$ flushes:

| strategy | postings written | partitions per query |
|---|---|---|
| no merge, keep every flush as a partition | $8b$ | 8 |
| immediate merge, merge each flush into the one main index | $b(1 + 2 + \cdots + 8) = 36b$ | 1 |

No merge writes each posting once but makes a query read 8 pieces. Immediate merge keeps one piece but rewrites the whole index at each flush, so its cost grows with the square of $m$. Logarithmic and geometric schemes sit between them.

Deletions. Let documents 1, 2 and 3 contain the term *sort*, so its list is 1, 2, 3, and let `delete(2)` arrive. The list on disk stays 1, 2, 3, and id 2 goes into the invalidation list. A query for *sort* reads 1, 2, 3 and removes 2, so it returns 1, 3. At the next merge that touches the list, the merge writes 1, 3 and id 2 can leave the invalidation list for this list.

## Known algorithms

| strategy | merge cost after $T$ postings | partitions per query | notes |
|---|---|---|---|
| rebuild from scratch | $\Theta(T)$ per rebuild | 1 | stale between rebuilds |
| no merge | $\Theta(T)$ | $\lceil T/M \rceil$ | queries slow down without bound |
| immediate merge (remerge) | $\Theta(T^2 / M)$ | 1 | lists stay contiguous |
| in-place update | depends on free space | 1 | lists keep spare room at the end and move when full |
| [logarithmic merging](/logarithmic-merging/) | $O(T \log(T/M))$ | $O(\log(T/M))$ | partitions of sizes that are powers of 2 |
| [geometric partitioning](/geometric-partitioning/), ratio $r$ | $O(r T \log_r(T/M))$ | $O(\log_r(T/M))$ | a larger $r$ means fewer partitions and more merging |
| geometric partitioning, at most $p$ partitions | $O(T (T/M)^{1/p})$ | $p$ | the ratio grows with the index |

The rebuild and remerge strategies come first in the comparison of Lester, Moffat and Zobel, and the in-place strategy goes back to earlier work on updates of inverted lists. Büttcher, Clarke and Lushman also proposed hybrid schemes that keep the long lists in place and merge the short ones.

## Bounds

- **Every posting is written at least once.** So the merge cost is at least $T$, and no merge reaches it with an unbounded number of partitions.
- **One partition costs quadratic merging with merge-based updates.** If every query must read one contiguous partition and the only update is a merge of the in-memory buffer into the index, then flush $i$ writes at least $ib$ postings, and the total is $b \, m(m+1)/2 = \Theta(T^2/M)$.
- **Logarithmic schemes balance the two costs.** Each posting takes part in $O(\log(T/M))$ merges and a query reads $O(\log(T/M))$ partitions, the same balance as the binary counter, whose increments cost $O(1)$ amortized each as in [binary counter increment](/binary-counter-increment/).

## Reductions

- **To a decomposable searching problem.** The postings of a term over the whole collection are the concatenation of its postings in each partition, in the order of age, since each partition holds a range of ids. So `postings(t)` is a [decomposable searching problem](/decomposable-searching-problem/), and the static-to-dynamic transformation of Bentley and Saxe applies. Logarithmic merging is that transformation applied to inverted indexes.
- **To a log-structured merge tree.** The same scheme of a memory buffer and merged sorted runs on disk is the [log-structured merge tree](/log-structured-merge-tree/) of key-value stores, with posting lists in place of sorted keys.
- **Deletions as marks.** A deletion is kept as a [tombstone](/tombstone/) in the invalidation list until a merge removes it, as in other systems that never rewrite data in place.

## Applications

- **Web search.** New and changed pages must appear soon after a crawl, while the main index serves queries.
- **Mail and desktop search.** The collection changes all the time, and each new item should be searchable almost at once.
- **Log and event search.** Data only grows, which fits the append-only form.

## References
