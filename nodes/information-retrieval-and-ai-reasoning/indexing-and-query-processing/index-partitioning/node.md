---
tag: Z8DQ5M
kind: concept
slug: index-partitioning
name: Index partitioning
aliases:
- document-partitioned index
- term-partitioned index
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Distributes an index over machines either by documents, each node holding a full local index, or by terms, each node holding whole posting lists.
prereqs: [inverted-index, sharding]
see_also: [hash-partitioning, range-partitioning, load-skew, tf-idf, bm25, document-at-a-time-evaluation, posting-list-intersection, geometric-partitioning]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 20, Section 20.3 (distributing indexes, partitioning by terms and by documents, and the need for global statistics)
  - book: isbn:9780262026512
    title: Stefan Buettcher, Charles L. A. Clarke and Gordon V. Cormack, Information Retrieval, Implementing and Evaluating Search Engines, MIT Press, 2010
    locator: Chapter 14 (parallel information retrieval), Section 14.1.1 (document partitioning) and Section 14.1.2 (term partitioning)
  - paper: doi:10.1109/MM.2003.1196112
    title: Luiz Andre Barroso, Jeffrey Dean and Urs Hoelzle, Web search for a planet, the Google cluster architecture, IEEE Micro 23(2), 2003
    locator: the index split into shards by document, each shard served by a pool of replicas, and the merge of the results of all shards
  - paper: "Alistair Moffat, William Webber, Justin Zobel and Ricardo Baeza-Yates, A pipelined architecture for distributed text query evaluation, Information Retrieval 10(3), 2007"
    title: A pipelined architecture for distributed text query evaluation
    locator: the term-partitioned index with queries passed from node to node, and its load balance compared with document partitioning
---

Index partitioning splits one [inverted index](/inverted-index/) over the machines of a cluster. In a document-partitioned index, each node holds a full index of its own subset of the documents, every query goes to every node, and the results are merged. In a term-partitioned index, each node holds the whole posting lists of a subset of the terms, and a query goes only to the nodes of its terms, which then combine the lists. The general idea of splitting a data set by a key is [sharding](/sharding/). This page is about the two ways to apply it to an index and their trade-offs. It is not about [geometric partitioning](/geometric-partitioning/), which splits one index into pieces by age on one machine, or about the chunks inside one list of [partitioned Elias-Fano](/partitioned-elias-fano/).

## In plain words

When an index is too large or too busy for one machine, it has to be split. There are two natural cuts. The first cut gives each machine a pile of documents, and each machine makes a small complete index of its own pile. A query is sent to all machines, each finds its best documents, and a front machine picks the best of these. The second cut gives each machine a set of words, with the full list of documents for each of its words. A query is sent only to the machines that own its words, and those machines must send whole lists to each other to find the answer. The first cut is simpler and spreads the work evenly. The second cut asks fewer machines, but it moves more data and can overload the machines that hold common words.

## The idea

Let the collection have documents $D$ and terms $V$, and let there be $k$ nodes.

**Document partitioning.** Split $D$ into $D_1, \ldots, D_k$, and let node $i$ build the inverted index of $D_i$ alone. To answer a query, a broker sends it to all $k$ nodes. Each node runs the whole query on its local index, for example by [document-at-a-time evaluation](/document-at-a-time-evaluation/), and returns its top results. The broker merges the $k$ result lists. The properties are:

- every node takes part in every query, so the work of a query is spread evenly, and the time of a query is the time of the slowest node;
- the network carries only short lists of results;
- each node can be built and updated alone, and a lost node loses only a part of the documents, so the engine still answers;
- ranking functions such as [tf-idf](/tf-idf/) and [BM25](/bm25/) need collection statistics such as the document frequency of a term, and the local values differ from the global ones. The nodes must share the global statistics, or the scores of different nodes are not comparable.

**Term partitioning.** Split $V$ into $V_1, \ldots, V_k$, and let node $i$ hold the full posting lists of the terms in $V_i$. A query with terms $t_1, \ldots, t_q$ goes only to the nodes that own them. The lists must then meet in one place, either by sending them to the broker or by passing a partial result from node to node in a pipeline. The properties are:

- a query uses at most $q$ nodes, so more queries can run at the same time when queries are short;
- whole posting lists, or large partial results, cross the network, which costs a lot for common terms;
- the load is uneven: the nodes that own frequent terms get most of the work, a case of [load skew](/load-skew/), and the split of terms must be tuned to the query log;
- the global statistics of a term are on its own node, so the scores need no extra exchange;
- adding a document changes the lists of all its terms, so an update touches many nodes.

**Replication.** Both forms are usually combined with copies. Each partition is served by several replicas, so that the cluster can answer more queries per second and survive failures. Partitioning sets the size of the index each node holds, and replication sets the query rate.

## Examples

The toy collection of the information retrieval pages has 8 documents, 50 distinct terms and 74 postings. Split it over two nodes.

- **By documents.** Node 1 holds documents 1 to 4, with 35 postings, and node 2 holds documents 5 to 8, with 39. For the query *posting list merge*, node 1 finds *posting* in 3 and 4, *list* in 3 and 4 and *merge* in 2, and node 2 finds *posting* and *merge* in 5. Both nodes work on the query, and each returns a short list of ranked results.
- **By terms.** Node 1 holds the 26 terms that start with *a* to *l*, with 38 postings, and node 2 holds the 24 terms that start with *m* to *z*, with 36. For *posting list merge*, node 1 sends the list of *list*, which is 3, 4, and node 2 holds *merge*, which is 2, 5, and *posting*, which is 3, 4, 5. The lists must be brought together on one node. For the query *merge sort*, both terms are on node 2, so node 1 does no work at all, while with document partitioning both nodes would work.
- **Local statistics.** With $\text{idf} = \lg(N/\text{df})$, the term *posting* is in 3 of the 8 documents, so its global idf is $\lg(8/3) \approx 1.42$. On node 1 it is in 2 of 4 documents, with a local idf of 1, and on node 2 it is in 1 of 4, with a local idf of 2. Without global statistics, document 5 on node 2 gets a higher weight for *posting* than documents 3 and 4 on node 1, only because of the split.

## Where it is used

- **Web search engines.** Large engines split the index by documents into many shards, each served by a pool of replicas, and a tree of brokers merges the results, as Barroso, Dean and Hoelzle describe for Google in 2003.
- **Research on term partitioning.** Pipelined query evaluation over a term-partitioned index, as studied by Moffat and others, sends a growing set of candidate documents from the node of one term to the next, and balances the load by moving or copying the lists of busy terms.
- **Selective search.** The documents are split into topical shards, by clustering, and a query is sent only to the shards most likely to hold good results. This keeps the simple build of document partitioning and asks fewer nodes, like term partitioning.
- **Hybrid splits.** Some systems partition by documents and then, inside each group of nodes, by terms, to trade network traffic against the number of nodes per query.

## References
