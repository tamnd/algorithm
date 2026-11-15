---
tag: WCARXK
kind: problem
slug: near-duplicate-document-detection
name: Near-duplicate document detection
aliases:
- near-duplicate web page detection
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Find pairs of documents whose content is almost the same, such as mirrored or templated pages, among billions of documents.
prereqs: [jaccard-similarity, shingling, hash-function]
see_also: [minhash, simhash, locality-sensitive-hashing, hamming-distance, cosine-similarity, fingerprinting, web-crawling, precision-and-recall]
sources:
  - paper: "Andrei Z. Broder, Steven C. Glassman, Mark S. Manasse and Geoffrey Zweig, Syntactic clustering of the Web, Computer Networks and ISDN Systems 29(8-13), 1157-1166, 1997 (Proceedings of the Sixth International World Wide Web Conference)"
    locator: the definitions of resemblance and containment over shingles, the sketches of minimum hash values, super shingles, and the clustering of a large AltaVista crawl
  - paper: "Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th Annual ACM Symposium on Theory of Computing (STOC 2002)"
    locator: the locality sensitive hash for the angle between vectors by random hyperplanes, which simhash fingerprints are built on
  - paper: "Gurmeet Singh Manku, Arvind Jain and Anish Das Sarma, Detecting near-duplicates for web crawling, Proceedings of the 16th International World Wide Web Conference (WWW 2007)"
    locator: Section 1 (64-bit simhash fingerprints and k = 3 for 8 billion pages), Section 3 (the Hamming distance problem, the permuted sorted tables and Example 3.1 with 20, 16, 10 and 4 tables, and the batch version with MapReduce) and Section 4.1 (precision and recall for k from 1 to 10 on hand-judged pairs, both near 0.75 at k = 3)
  - paper: "Monika Henzinger, Finding near-duplicate web pages: a large-scale evaluation of algorithms, Proceedings of the 29th Annual International ACM SIGIR Conference (SIGIR 2006)"
    locator: the comparison of Broder's shingle method and Charikar's random projection method on a large crawl, with precision measured on human-judged pairs
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 19, Section 19.6 (near-duplicates and shingling, with the sketch of minimum values of permuted shingle hashes)
---

Near-duplicate document detection is the problem of finding documents whose content is almost, but not exactly, the same: mirrors of a site, copies of a page with a different date or advert, versions of a news story, and pages made from one template. On the web it matters for crawlers, which should not fetch and index the same content many times, and for search results, which should not show the same thing ten times. The task has an exact form, find all pairs whose similarity under a chosen measure is at least a threshold, and an engineering form, choose the measure, the features and the threshold so that the pairs found are the ones people judge to be near duplicates. The second form is measured by precision and recall on judged pairs, not proved. At web scale, the standard tools are [shingling](/shingling/) with [MinHash](/minhash/) sketches and [simhash](/simhash/) fingerprints.

## In plain words

Many pages on the web are copies of other pages with small changes: a new date at the top, another advert at the side, or the same article on two sites. A search engine wants to keep one of them and skip the rest. Exact copies are easy to catch, because the same text always gives the same short code. Near copies are harder, because one changed word changes that code completely. The usual trick is to cut each page into short overlapping runs of words and compare the sets of runs: two pages that share most of their runs are near copies. With billions of pages, comparing every pair is impossible, so engines boil each page down to a small sketch that keeps this similarity, and compare sketches.

## Definition

The input is a collection of documents $D_1, \ldots, D_n$. Each document is turned into a set or a vector of features. The common choice is the set $S_w(D)$ of its $w$-shingles, the sequences of $w$ consecutive tokens. Broder and his coauthors define two measures on these sets:

$$r(A, B) = \frac{|S_w(A) \cap S_w(B)|}{|S_w(A) \cup S_w(B)|}, \qquad c(A, B) = \frac{|S_w(A) \cap S_w(B)|}{|S_w(A)|}.$$

The resemblance $r$ is the [Jaccard similarity](/jaccard-similarity/) of the shingle sets, and the containment $c$ measures how much of $A$ is inside $B$. Other choices are the [cosine similarity](/cosine-similarity/) of weighted term vectors, or the [Hamming distance](/hamming-distance/) of fingerprints.

- **Batch task.** Given a measure and a threshold $\tau$, output all pairs $\{i, j\}$ with $r(D_i, D_j) \ge \tau$, or the clusters of the graph that these pairs form.
- **Online task.** Given a stored collection and a new document $Q$, decide whether some stored document has similarity at least $\tau$ with $Q$, and find it.

Approximate versions allow the output to miss pairs a little above $\tau$ or to include pairs a little below, with stated probabilities. Which pages count as near duplicates is a judgment: two pages that differ only in a price can be the same for a crawler and different for a shopper. So the choice of $w$, the features, the cleaning of the text and $\tau$ is tuned on samples of pairs that people judged.

## Variants

- **Exact duplicates.** Pages with the same text after cleaning. A [fingerprint](/fingerprinting/) of each page, such as a 64-bit hash, finds them by sorting or with a hash table.
- **Containment.** Find pages that contain most of another page, such as an article copied into a larger page.
- **Clustering.** Group the pages into clusters of near duplicates and choose one representative per cluster.
- **Online detection in a crawler.** Decide for each new page, at crawl time, whether a near duplicate is already stored.
- **Boilerplate removal.** Find the parts of pages that a site repeats on every page, such as menus and footers, and leave them out before the comparison.
- **Plagiarism and reuse.** Find shared passages between documents, not whole-document similarity.

## Examples

Take three short texts and $w = 3$, with tokens as words:

- A: "the quick brown fox jumps over the lazy dog"
- B: "the quick brown fox jumped over the lazy dog"
- C: "a lazy dog sleeps under the quick brown tree"

A and B have 7 shingles each and share 4 of them ("the quick brown", "quick brown fox", "over the lazy", "the lazy dog"), so $r(A, B) = 4/10 = 0.4$. A and C share only "the quick brown", so $r(A, C) = 1/13 \approx 0.0769$. One changed word removes up to $w$ shingles, which is a large part of a short text. For a document of 1000 words whose 998 shingles are all distinct, one changed word removes 3 shingles and adds 3, so $r = 995/1001 \approx 0.9940$. The same pairs with $w = 1$, which is the Jaccard similarity of the word sets, give $7/9 \approx 0.7778$ for A and B and $5/12 \approx 0.4167$ for A and C: smaller $w$ makes everything look more alike.

## Known algorithms

**Fingerprints for exact duplicates.** Hash each cleaned document to 64 bits and group equal hashes. For $n$ documents of total length $L$, this costs $O(L)$ expected time.

**Shingles and MinHash sketches.** Broder, Glassman, Manasse and Zweig hash the shingles and keep, for each of several independent hash functions, the minimum hash value, which gives a sketch of each document. For one random permutation of the shingle universe, the probability that two sets have the same minimum is exactly their resemblance, so the share of equal entries in two sketches of $k$ values estimates $r$ with a standard deviation of $\sqrt{r(1 - r)/k}$, which is 0.05 for $r = 0.5$ and $k = 100$. To avoid comparing all pairs, they combined groups of sketch values into super shingles, so that only documents that share a super shingle are compared. The banding scheme of [locality-sensitive hashing](/locality-sensitive-hashing/) does the same job with a tunable threshold. See [MinHash](/minhash/).

**Simhash.** Charikar's hash for the angle between vectors gives, for each feature vector, a fingerprint of $f$ bits; two vectors at angle $\theta$ agree on each bit with probability $1 - \theta/\pi$. Manku, Jain and Das Sarma used 64-bit [simhash](/simhash/) fingerprints of weighted features at Google, with a pair counted as near duplicates when the fingerprints differ in at most $k = 3$ bits. They chose $k$ by hand-judging sampled pairs at each distance from 1 to 10: at $k = 3$, both precision and recall were near 0.75. For 8 billion pages the fingerprints take 64 GB.

**Search in Hamming distance.** Probing all fingerprints within distance 3 of a query takes $\binom{64}{0} + \binom{64}{1} + \binom{64}{2} + \binom{64}{3} = 43{,}745$ lookups. Manku, Jain and Das Sarma use the pigeonhole principle instead. Split the 64 bits into 4 blocks of 16 bits: two fingerprints within distance 3 agree exactly on at least one block. Keep a sorted copy of the table for each block, with that block moved to the front, and look up the query by its block in each copy. Their Example 3.1 also gives designs with 10, 16 and 20 tables, which trade memory for fewer matches per probe; with 16 tables and a match on the first 28 bits of $2^{34}$ fingerprints, a probe returns about $2^{34 - 28} = 64$ fingerprints on average. A batch of new fingerprints is checked against the whole table with MapReduce.

**Similarity joins.** Exact all-pairs algorithms for a cosine or Jaccard threshold use prefix filtering: sort the features of each document by rarity, and note that two documents above the threshold must share a feature among the first few of each. These algorithms find every pair above $\tau$ with no false negatives, at a cost that depends on the data.

**Signatures of selected terms.** I-Match and similar methods hash the set of terms of middle document frequency, so that small changes in rare or common words do not change the signature.

## Bounds

- **Output size.** All copies of one page are pairwise near duplicates, so a cluster of $m$ copies has $\binom{m}{2}$ pairs, and the output can have $\Theta(n^2)$ pairs. Algorithms that output clusters, or one representative per cluster, avoid this.
- **All pairs.** The naive method compares $\binom{n}{2}$ pairs, which for $n = 10^{10}$ is about $5 \cdot 10^{19}$ comparisons, far too many. Every practical method uses sketches or signatures to compare only candidate pairs.
- **Estimation error.** A MinHash sketch of $k$ values estimates $r$ with variance $r(1 - r)/k$, so halving the error needs four times as many values. With a fixed number of bits per document, false positives and false negatives trade off against each other through the threshold.
- **Search in Hamming distance.** With $t$ tables, a query costs $t$ lookups plus the scan of the matches; with the pigeonhole design for $k = 3$, at least 4 tables are needed for exact search, and each table holds a copy of all fingerprints.

## Reductions

- With the shingle sets, near-duplicate detection is a set similarity join under Jaccard similarity, which MinHash and locality-sensitive hashing reduce to finding equal hash values.
- With simhash, it is the Hamming distance problem on short bit strings, which the block tables reduce to exact matching on parts of the bits.
- Exact duplicate detection reduces to grouping equal hash values, like element distinctness.
- Clustering of near duplicates is finding the [connected components](/connected-components/) of the graph of near-duplicate pairs, though a chain of near duplicates can join pages that are not near duplicates of each other.

## Applications

- **Crawlers.** A [crawler](/web-crawling/) that finds a page to be a near duplicate of a stored page can skip its links and give its host a lower priority. Manku, Jain and Das Sarma made the decision at crawl time for each new page.
- **Index size and result quality.** Search engines index one page per cluster, and hide near duplicates in the results.
- **Link and anchor counting.** Mirrors repeat links, so near duplicates are removed before counting links for [PageRank](/pagerank/) and [anchor text](/anchor-text-indexing/).
- **Spam detection.** Many spam pages are made from one template with small changes, so large clusters of near duplicates are a sign of [link spam](/link-spam/).
- **News, archives and plagiarism.** Group versions of a news story, store repeated versions of a page once in a web archive, and find copied text in student work and in publications.

## References
