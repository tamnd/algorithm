---
tag: K2Q0FZ
kind: technique
slug: query-biased-snippet
name: Query-biased snippet generation
aliases:
- query-biased summaries
- dynamic snippets
- result snippets
- keyword-in-context snippets
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Picks the sentences of a result page that best match the query to show under the link, so the user can judge relevance quickly.
prereqs: [inverted-index, tf-idf, ranked-retrieval]
see_also: [positional-index, stemming, bm25, vector-space-model, maximal-marginal-relevance, greedy-max-coverage, search-result-diversification, query-auto-completion]
sources:
  - paper: doi:10.1145/290941.290947
    title: Anastasios Tombros and Mark Sanderson, Advantages of query biased summaries in information retrieval, Proceedings of the 21st Annual International ACM SIGIR Conference (SIGIR 1998), 2-10
    locator: Section 2.1 (the title score), Section 2.2 (the location score), Section 2.3 (the term occurrence score after Luhn's clusters of significant words), Section 2.4 (the query score, the square of the number of query terms in a sentence divided by the number of terms in the query), summaries of up to five sentences, and the user study with 20 participants on TREC ad hoc data
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Section 8.7 (results snippets, static and dynamic summaries, and the need to keep the text of the documents for dynamic summaries)
---

Query-biased snippet generation is the technique of choosing, for each result on a search page, the few sentences or text fragments of the document that best match the query, and showing them under the link with the query terms highlighted. A static summary, such as the first lines of the page, is the same for every query; a query-biased snippet changes with the query, so that it shows why the page was retrieved. Anastasios Tombros and Mark Sanderson described the method and tested it with users in 1998. It reuses the term matching of [ranked retrieval](/ranked-retrieval/) on sentences instead of documents, and its redundancy problem is a small version of [search result diversification](/search-result-diversification/).

## In plain words

A results page shows ten links. To decide which one to open, you read the few lines under each link. If those lines are just the start of the page, they often say nothing about what you searched for. A better way is to look inside the page for the sentences that contain your search words, and to show those. Then you can see at once whether the page talks about your topic in the way you mean. You open fewer wrong pages and decide faster. The engine has to do this for every result of every search, so the method must be simple and quick.

## When it applies

- A ranked list is shown to a person, who must judge from a short text which results to open.
- The text of each result is available at query time, in a document cache. A [positional index](/positional-index/) tells where the query terms occur, but it does not keep the full text with stop words and punctuation, so it cannot print the snippet alone (Section 8.7 of Manning, Raghavan and Schütze).
- The documents have structure that can be split into sentences or short windows. For pages with little text, such as product pages or images, other fields such as the title or attributes serve instead.

## The template

1. **Split** the document into units: sentences, or windows of a fixed number of words around query term occurrences.
2. **Score** each unit. Tombros and Sanderson combine four scores:
   - a title score, from the title of the document (Section 2.1);
   - a location score, from the position of the sentence in the document (Section 2.2);
   - a term occurrence score for sentences with clusters of significant words, after Luhn (Section 2.3);
   - a query score, $t^2 / |q|$, where $t$ is the number of query terms in the sentence and $|q|$ the number of terms in the query (Section 2.4).
3. **Select** the best units within a length budget; Tombros and Sanderson use up to five sentences. Break ties by position in the document.
4. **Present** the chosen units in document order, mark the gaps with ellipses, and highlight the query terms.

For a document of $N$ words and a query held in a hash set, steps 1 and 2 take $O(N)$ time and step 3 takes $O(u \log u)$ time for $u$ units. The cost is paid for each shown result, so for long documents the scan can be limited to their first part. The squared count in the query score rewards a sentence that contains several query terms together far more than a sentence with one; for a fixed query, the divisor $|q|$ does not change the order of sentences, and it only makes the scores of different queries comparable.

## Classic examples

**Scoring one document.** The query is "binary search tree" and the document has five sentences:

| | sentence | query terms | query score |
|---|---|---|---|
| S1 | A tree is a data structure made of nodes and edges. | 1 | $1/3 \approx 0.33$ |
| S2 | Binary search finds a key in a sorted array in logarithmic time. | 2 | $4/3 \approx 1.33$ |
| S3 | A binary search tree keeps keys in order so that each lookup follows one path. | 3 | $9/3 = 3$ |
| S4 | Balanced trees such as red-black trees keep the height logarithmic. | 0 | 0 |
| S5 | Insertion into a search tree may need rotations to restore balance. | 2 | $4/3 \approx 1.33$ |

A two-sentence snippet takes S3 and then S2, which ties with S5 and comes first in the document. In document order it reads "Binary search finds a key in a sorted array in logarithmic time. ... A binary search tree keeps keys in order so that each lookup follows one path." S4 scores 0 only because "trees" does not match "tree"; with [stemming](/stemming/) it would score $1/3$.

**The user study.** Tombros and Sanderson compared query-biased summaries with static summaries, with 20 participants on TREC ad hoc data. With query-biased summaries the participants judged relevance more accurately and faster. These are measurements of one laboratory study.

**Web result pages.** Search engines show the title, the URL and a snippet of a few fragments with the query terms in bold. Manning, Raghavan and Schütze (Section 8.7) describe these as dynamic summaries and contrast them with static summaries stored once per document.

## Variations

- **Weighted terms.** Weigh each query term by its [idf](/tf-idf/), so that a rare term counts more than a common one, or score windows with [BM25](/bm25/) or [cosine similarity](/cosine-similarity/) in the [vector space model](/vector-space-model/).
- **Fixed windows.** Take a window of a few words on each side of each query term occurrence, the keyword-in-context form, and merge overlapping windows.
- **Coverage of query terms.** Choose fragments greedily so that each new fragment adds query terms not yet shown, in the way of [maximal marginal relevance](/maximal-marginal-relevance/). With 0 or 1 values per term this is [greedy maximum coverage](/greedy-max-coverage/) with the query terms as elements.
- **Static and mixed summaries.** Use a stored summary or a meta description when no sentence contains the query terms, or when the stored text is better written.
- **Learned scoring.** Train a model on features such as the query score, the position, the length and the readability of each fragment.
- **Abstractive answers.** Generate a new sentence from the document instead of copying one. This can state the answer directly, but the shown text is then not a quote from the page.

## Pitfalls

- **Matching rules.** Different tokenization, case or stemming in the snippet and in the index gives snippets without the matched terms, as with S4 above.
- **Redundant fragments.** Two fragments that both contain the same query terms waste space; prefer fragments that add new terms.
- **Broken sentences.** Fragments cut in the middle of a word, a number or a URL are hard to read. Cut at sentence or phrase boundaries.
- **Boilerplate.** Menus, cookie notices and footers often contain query terms. Remove them before splitting.
- **Cost.** Every shown result needs a scan of its text, so long documents and large result pages need a cache of the text and a limit on the scanned part.
- **Stale caches.** A snippet built from an old copy of the page may show text that the page no longer has.
- **Misleading snippets.** A sentence that contains the query terms can still be about something else, and a page can place text only to match queries. The snippet shows matches, not relevance.

## Exercises

1. In the example, the stemmer maps "trees" to "tree". Compute the query score of S4 when $t$ counts distinct query terms and when it counts occurrences. Which reading is closer to the intent of the squared count?
2. Show that for one fixed query, ranking the sentences by $t^2/|q|$ gives the same order as ranking them by $t$.
3. Write the greedy fragment choice that adds, at each step, the fragment with the most query terms not yet shown, and show that it is the greedy algorithm for maximum coverage. Give a document on which it beats choosing the top fragments by query score.
4. Explain why a positional index alone cannot produce a snippet, and estimate the extra storage for a document cache that keeps the first 2000 words of each page.

## References
