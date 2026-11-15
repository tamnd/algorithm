---
tag: 761E1Z
kind: problem
slug: federated-search
name: Federated search
aliases:
- distributed information retrieval
- resource selection
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: advanced
summary: Send a query to several independent search engines, choose which to ask, and merge their result lists into one.
prereqs: [ranked-retrieval, tf-idf, inverted-index]
see_also: [cori-resource-selection, rank-aggregation, combmnz, reciprocal-rank-fusion, borda-count, index-partitioning, query-likelihood-model, precision-at-k]
sources:
  - paper: doi:10.1007/0-306-47019-5_5
    title: Jamie Callan, Distributed information retrieval, in W. Bruce Croft (editor), Advances in Information Retrieval, Kluwer Academic Publishers, 2000, Chapter 5
    locator: Section 1 (the three subproblems of description, selection and merging), Section 4 (the ranking of databases with the inference network), Section 5 (merging document rankings, Equations 5.10 to 5.15) and Section 6 (cooperative descriptions with the STARTS protocol, and query-based sampling with samples of 300 documents)
  - paper: doi:10.1145/215206.215328
    title: James P. Callan, Zhihong Lu and W. Bruce Croft, Searching distributed collections with inference networks, Proceedings of the 18th Annual International ACM SIGIR Conference (SIGIR 1995)
    locator: the ranking of collections as if each were one document of an inference network, and the merge of the returned lists by document scores weighted by collection scores
  - paper: doi:10.1561/1500000010
    title: Milad Shokouhi and Luo Si, Federated search, Foundations and Trends in Information Retrieval 5(1), 2011
    locator: the chapters on collection representation (query-based sampling and size estimation), collection selection (CORI, GlOSS, ReDDE and learned methods), result merging (CORI merging and the semi-supervised method) and testbeds
  - paper: "Jamie Callan and Margaret Connell, Query-based sampling of text databases, ACM Transactions on Information Systems 19(2), 2001"
    locator: the sampling procedure, which sends single-term queries and keeps the top documents, and the comparison of the learned language models with the complete ones
---

Federated search answers a query from many independent search engines through one broker. Each engine has its own collection, its own index and often its own ranking function, and the broker cannot read the collections directly. Jamie Callan split the problem into three parts in 2000: source representation, which describes what each collection holds; collection selection, which chooses the few engines that are likely to have relevant documents for the query; and result merging, which turns the ranked lists that come back into one list. The engines may cooperate by exporting their statistics, or the broker may have to learn about them by sending queries. When the engines index the same documents, as general web engines do, the task is called metasearch, and merging becomes [rank aggregation](/rank-aggregation/).

## In plain words

Think of a librarian who cannot see the shelves of a hundred other libraries but can phone any of them and ask for their best books on a subject. Calling all of them is slow and costly, so the librarian first guesses which few libraries are likely to have good books on that subject, using notes about what each library holds. Then the librarian calls those few, gets a short list from each, and must put the lists together into one list for the reader. That last step is hard, because each library rates its books on its own scale: one library's "very good" can be worth less than another's "fair". A federated search system does the same with search engines that it does not control.

## Definition

There are $N$ collections $C_1, \ldots, C_N$, each behind an engine $E_i$. Given a query $q$, $E_i$ returns a [ranked list](/ranked-retrieval/) of its top $m$ documents, sometimes with scores. The broker keeps a description $S_i$ of each collection, such as the document frequency of each term and the number of documents. Given $q$, a limit $k$ on the number of engines to ask, and an output length $n$, the broker must:

1. **Select** a set $S \subseteq \{1, \ldots, N\}$ with $|S| \le k$, using only $q$ and the descriptions.
2. **Search** by sending $q$ to each $E_i$ with $i \in S$ and receiving its list $L_i$.
3. **Merge** the lists $L_i$ into one list of $n$ documents.

The goal is a merged list as good as a search of the union of all collections by one engine, measured by [precision at $n$](/precision-at-k/) on judged queries. Selection alone is measured by the share of the relevant documents of the query that lie in the chosen collections, compared with the best possible choice of $k$ collections. The scores of different engines are not comparable in general. Each engine computes [tf-idf](/tf-idf/) or [BM25](/bm25/) weights from its own collection, so the same document gets different scores in different collections, and an engine may use another ranking function or return no scores at all.

## Variants

- **Cooperative and uncooperative engines.** Cooperative engines export their term statistics in an agreed format, such as the STARTS protocol that Callan cites. Uncooperative engines only answer queries, so the broker must estimate their contents.
- **Disjoint and overlapping collections.** In distributed information retrieval the collections are mostly disjoint. In metasearch, engines that index the same web return the same documents, and a document found by several engines is evidence for it.
- **One engine with a split index.** A large engine that splits its documents over many machines, as in [index partitioning](/index-partitioning/), solves the same problem with full cooperation: all shards share the same statistics and ranking function, and it usually asks every shard.
- **Aggregated search.** A web engine chooses which verticals, such as news, images, video or maps, to ask for a query, and where to place their results on the page. This is collection selection with very different kinds of collections.
- **Hidden web.** Many databases can be searched only through a query form. A broker over them must sample them through the form.
- **Peer-to-peer search.** There is no central broker, and each peer routes the query to the peers that are likely to have matches.

## Examples

A broker has chosen engines A and B for a query, and merges their lists with the method of Callan's Equations 5.13 to 5.15. For this query, the collection scores of the [CORI](/cori-resource-selection/) formula can lie between $R_{\min} = 0.40$ and $R_{\max} = 0.60$. A scores $0.56$ and B scores $0.48$, so the normalized collection scores are $R'_i = (R_i - R_{\min})/(R_{\max} - R_{\min})$, which gives $R'_A = 0.8$ and $R'_B = 0.4$. Each document score $D$ is normalized by the lowest and highest scores possible in its collection, $D' = (D - D_{\min,i})/(D_{\max,i} - D_{\min,i})$, with the range $[0.40, 0.70]$ for A and $[0.40, 1.00]$ for B. The merged score is $D'' = (D' + 0.4\, D' R'_i)/1.4$.

| document | engine | $D$ | $D'$ | $D''$ |
|---|---|---|---|---|
| a1 | A | 0.62 | 0.7333 | 0.6914 |
| a2 | A | 0.50 | 0.3333 | 0.3143 |
| b1 | B | 0.90 | 0.8333 | 0.6905 |
| b2 | B | 0.70 | 0.5000 | 0.4143 |

A merge by the raw scores gives b1, b2, a1, a2: both documents of B come first only because B scores on a wider scale. The normalized merge gives a1, b1, b2, a2. Document b1 has the higher normalized score, but the better collection score of A lifts a1 just above it. A round-robin merge that starts with A gives a1, b1, a2, b2. The CORI page works out the selection step for a small example with three collections.

## Known algorithms

**Source representation.** Cooperative engines export, for each term, its document frequency and the size of the collection. For uncooperative engines, Callan and Connell proposed query-based sampling: send a one-term query, keep the top few documents, choose the next query term from the text already sampled, and stop after a fixed number of distinct documents. Callan reports samples of 300 documents with 4 documents for each query. The learned language models were close to the complete ones, and selection and merging with the learned descriptions were nearly as accurate as with the complete ones. Shokouhi and Si also review methods that estimate the size of a collection from such samples.

**Collection selection.**

- **CORI.** Callan, Lu and Croft rank collections as if each collection were one large document of an inference network, with document frequency in the place of term frequency. See [CORI](/cori-resource-selection/).
- **GlOSS.** Gravano and his coauthors estimate, from the term statistics, how many documents of each collection score above a threshold.
- **Language models.** Rank collections by the [likelihood of the query](/query-likelihood-model/) under a smoothed language model of each collection.
- **ReDDE.** Si and Callan put the samples of all collections into one central index, run the query on it, and count each sampled document near the top as $|C_i|/s_i$ documents of its collection $C_i$, where $s_i$ is the size of the sample of $C_i$. This estimates the number of relevant documents in each collection and helps when collection sizes differ greatly.
- **Learned selection.** Classifiers combine features of the query, the samples and past logs. This is the usual method in aggregated search.

**Result merging.**

- **Round robin.** Take the top document of each list in turn. It ignores both the scores and the quality of the collections.
- **Raw scores.** Merge by score. This is correct only when all engines use the same ranking function and the same statistics.
- **Global statistics.** With cooperation, the broker computes term weights from the statistics of all collections, or downloads the documents and scores them again itself.
- **CORI merging.** Weight each document score by the score of its collection, as in the example. Callan's Equation 5.12 applies the weight to the raw document score, $D'' = (D + 0.4\, D R'_i)/1.4$. Equations 5.13 to 5.15 first normalize the document score by $D_{\min,i}$ and $D_{\max,i}$, which requires cooperation.
- **Semi-supervised merging.** Si and Callan use the documents that appear both in a returned list and in the central sample index. For each engine, they fit a linear regression from its scores to the scores of the central index, and map all of its scores with it.
- **Fusion of overlapping lists.** For metasearch, [CombMNZ](/combmnz/), the [Borda count](/borda-count/) and [reciprocal rank fusion](/reciprocal-rank-fusion/) reward documents that several engines return.

## Bounds

- **Recall ceiling.** A relevant document in a collection that is not selected cannot be in the merged list. So the recall of the system is at most the share of relevant documents that lie in the selected collections.
- **Exact merging with full cooperation.** Let the collections be disjoint, and let every engine score with the same function and the same global statistics. If each engine returns its top $n$ documents, the merged top $n$ by score is the top $n$ of the union, because no collection holds more than $n$ of the global top $n$ and each of those is in the top $n$ of its collection. The broker then handles $Nn$ results for all collections, or $kn$ for $k$ selected ones.
- **No exact merging without scores that agree.** If an engine may apply any increasing function to its scores, its list carries only the order of its documents. Then no merge rule can recover the global order in general, and every uncooperative method is an estimate.
- **Cost of selection.** With term statistics in hash tables, ranking $N$ collections for a query of $t$ terms takes $O(Nt + N \log N)$ expected time, which is small next to sending queries to the engines.
- **Cost of sampling.** With 300 documents for each collection and at most 4 new documents for each query, each collection needs at least 75 sample queries, and 100 collections need 30,000 sampled documents. This cost is paid once, before any user query, and again when the collections change.

## Reductions

- Collection selection reduces to document ranking, with each collection treated as one document whose text is the union of its documents, as in CORI and the language model methods.
- Merging overlapping lists is an instance of [rank aggregation](/rank-aggregation/), with the engines as voters.
- Search over a document-partitioned index is federated search with full cooperation and $k = N$, so the exact merge above applies.
- Semi-supervised merging reduces merging to one regression for each engine, from its scores to the scores of a common reference index.

## Applications

- **Digital libraries and catalogs.** Portals that search the catalogs and databases of many libraries and publishers, which are run by different owners.
- **Hidden web.** Search over databases that are reached only through query forms, such as patent, legal and medical databases.
- **Enterprise search.** One query over mail, document stores, wikis and databases inside an organization, each with its own search engine and access rules.
- **Aggregated web search.** Web engines decide for each query whether to show news, images, videos, maps or shopping results, and where to put them.
- **Metasearch engines.** Services that send each query to several general web engines and fuse their lists.
- **Evaluation.** Testbeds that split standard collections into many collections by source, and the TREC Federated Web Search track, which used real web engines.

## References
