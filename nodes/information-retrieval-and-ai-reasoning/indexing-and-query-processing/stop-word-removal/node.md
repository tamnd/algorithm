---
tag: 2G54CK
kind: technique
slug: stop-word-removal
name: Stop word removal
aliases:
- stop list
- stopword filtering
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: Drops the most frequent function words from the index or the query, to save space and time at a small cost in recall.
prereqs: [zipfs-law, posting-list]
see_also: [stemming, tf-idf, bm25, positional-index, phrase-query, postings-gap-encoding, inverted-index, heaps-law]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.2.2 (the definition of stop words, the stop list built from the terms of highest collection frequency with hand filtering, Figure 2.5 with 25 words common in Reuters-RCV1, the phrase queries that stop words help, and the trend from lists of 200 to 300 terms to lists of 7 to 12 terms to none), and Chapter 5, Section 5.1 (Table 5.1 with the effect of 30 and 150 stop words on Reuters-RCV1, and the remark that the saving does not carry over to the compressed index)
---

Stop word removal is the technique of leaving out of the index, or out of the query, a fixed set of very frequent words such as "the", "of" and "a", the *stop list*. These words occur in almost every document, so as single query words they select almost nothing, while their posting lists are the longest of the index. By [Zipf's law](/zipfs-law/), a few such words make up a large share of all tokens, which is why a short list saves much space. The price is that queries in which these words matter, such as phrases, can no longer be answered exactly, and modern systems use small lists or none.

## In plain words

Some words appear in nearly every text: "the", "a", "of", "to". A search for "the" would return everything, so the word tells the engine nothing about what the user wants. Yet these words are so common that their lists in the index are the longest of all. Stop word removal keeps a short list of such words and skips them, both when the documents are indexed and when a query is read.

This makes the index smaller and many queries faster. It also loses information. A search for the song title "Let It Be" may find nothing, because every word of it is on a typical list, and "flights to London" loses the word that gives the direction. So the list should be short and chosen with care, and phrase searches need special handling.

## When it applies

- **Keyword queries over an uncompressed or slow index.** The longest posting lists cost the most to store and to read, and they belong to words that rarely help a keyword query.
- **Scoring without good weights.** With plain Boolean matching or raw term counts, a frequent word adds noise. With [tf-idf](/tf-idf/) or [BM25](/bm25/) weights, such a word gets a weight near zero by itself, and removal gains little.
- **A known domain.** The list is built for one collection and one language. A word that is empty in one domain, such as "patient" in a hospital archive, is a content word in another.

It does not apply when the system must answer phrase queries, exact titles or queries made only of frequent words. Manning, Raghavan and Schuetze report that the trend in IR systems has gone from lists of 200 to 300 terms to lists of 7 to 12 terms to no stop list, and that web search engines generally do not use stop lists.

## The template

Build the list once, then filter the token stream at indexing time and at query time. The holes to fill are in capitals.

```pseudo id=main
BUILD-STOP-LIST(collection)
L1  count cf(t), the number of tokens of each term t
L2  C ← the K terms of highest cf
L3  S ← FILTER(C)                        ▷ keep only words with no content in this domain
L4  return S

INDEX-WITH-STOP-LIST(d, S)
L5  for each token t of document d, at position p do
L6      if t is not in S then add (d, p) to the postings of t   ▷ p still counts stop words

QUERY-WITH-STOP-LIST(q, S)
L7  if q is a PHRASE or every word of q is in S then return QUERY-POLICY(q)
L8  return q without the words of S
```

**The holes.** K is the size of the list, from a few words to a few hundred. FILTER is the review of the candidates by hand or against a standard list: the most frequent terms of a collection include content words of its domain. QUERY-POLICY decides what to do with queries that the list would change too much: run them against a full index, against a separate index of phrases, or with the stop words kept.

**The invariant.** For each term $t$ not in $S$, the posting list of $t$ is the same as without removal, positions included, because line L6 counts every token, stop word or not. So a query with no stop words gets the same answer, and a phrase query can still require that two words be separated by exactly one word. The only queries that change are those that use words of $S$.

**Walk-through on the toy collection.** The 25 words of the RCV1 list of Manning, Raghavan and Schuetze are "a an and are as at be by for from has he in is it its of on that the to was were will with". On the 8 toy documents, 10 of them occur: "a" (8 tokens), "the" and "of" (3 each), "in" and "is" (2 each), and "to", "with", "by", "an" and "for" (1 each). Removing them drops 23 of the 79 tokens and 20 of the 74 postings, and the vocabulary goes from 50 to 40 terms. None of the four toy queries uses a stop word, so their answers do not change. A list built only by frequency would be wrong here: the second most frequent toy term is "sorted", with 5 tokens, which line L3 must remove from the candidates.

## Classic examples

- **A fixed English list in an [inverted index](/inverted-index/).** The 25-word list above, applied at indexing time and to keyword queries. Table 5.1 of Manning, Raghavan and Schuetze shows the effect on Reuters-RCV1 after case folding: 30 stop words cut the nonpositional postings from 96,969,056 to 83,390,443, 14 percent, and 150 stop words to 67,001,847, 31 percent, while the vocabulary loses only 30 and 150 of its 391,523 terms.
- **Stop words kept in a [positional index](/positional-index/).** Remove them from keyword queries only, and keep them in the index so that [phrase queries](/phrase-query/) such as "President of the United States" stay exact. The index is as large as without a list, and keyword queries still gain speed.
- **No list, with weights.** Index every word, and let [tf-idf](/tf-idf/) give the frequent words a low weight. On the toy collection, "a" occurs in 5 of the 8 documents, so its idf is $\log(8/5)$, the lowest of the collection. Compression of the [gaps](/postings-gap-encoding/) makes its long posting list cheap: the gaps of a frequent word are small.

## Variations

- **Lists by document frequency.** Rank the candidates by the number of documents that contain them, not by the number of tokens, so that a word repeated in a few long documents does not enter the list.
- **Query-time lists only.** Keep the full index and remove stop words only from queries that are not phrases. This keeps every query answerable.
- **Lists per field or per domain.** Use one list for titles, another for body text, or a list built for a medical or legal collection.
- **Stop words in pairs.** Index frequent pairs such as "of the" as single terms (a biword index), so that phrases with stop words remain cheap.

## Pitfalls

- **Queries made of stop words.** "To be or not to be", "Let It Be" and "As We May Think" lose all or most of their words. Detect a query whose words are all on the list, and run it against an index that keeps them.
- **Positions that skip stop words.** If line L6 also stops the position counter, two words with a stop word between them look adjacent: $d_4$ says "sorted list of document ids", and the phrase query "list document" would match it, though $d_4$ does not contain that phrase. Count every token.
- **A list built from frequency alone.** The most frequent words of a domain include content words: "sorted" on the toy collection. Review the list.
- **A list that differs between the index and the query.** A word that is removed from queries but kept in the index, or the other way round, gives no error and silently changes the answers. Store the list with the index.
- **Expecting the saving to stay after compression.** Manning, Raghavan and Schuetze note that a list of 150 words removes a quarter or more of the postings, but that this does not carry over to the compressed index, because the postings of frequent words need only a few bits each after compression.

## References
