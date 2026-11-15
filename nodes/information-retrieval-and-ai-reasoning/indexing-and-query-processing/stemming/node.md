---
tag: AWG102
kind: technique
slug: stemming
name: Stemming
aliases:
- suffix stripping
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: intro
summary: Maps the inflected and derived forms of a word to one stem before indexing and querying, so that a query word also matches its variants.
prereqs: [posting-list]
see_also: [porter-stemmer, stop-word-removal, query-expansion, precision-and-recall, inverted-index, k-gram-index, edit-distance, soundex]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.2.4 (stemming and lemmatization, the Porter, Lovins and Paice/Husk stemmers, the statement that stemming increases recall while harming precision, and the example of operate and oper with the queries about operational research, operating systems and operative dentistry)
  - paper: doi:10.1108/eb046814
    title: Martin F. Porter, An algorithm for suffix stripping, Program 14(3), 130 to 137, 1980
    locator: Section 1 (the reasons to conflate words with a common stem in information retrieval, and the smaller number of terms that results)
  - paper: "Julie Beth Lovins, Development of a stemming algorithm, Mechanical Translation and Computational Linguistics 11, 1968"
    locator: the list of endings, each with a condition, the removal of the longest ending whose condition holds, and the transformation rules applied to the stem afterwards, as described on the Snowball page of the Lovins stemmer
  - paper: doi:10.1145/101306.101310
    title: Chris D. Paice, Another stemmer, ACM SIGIR Forum 24(3), 56 to 61, 1990
    locator: the stemmer driven by a table of rules applied iteratively, known as the Paice/Husk or Lancaster stemmer
---

Stemming is the technique of replacing each word, in the documents and in the queries, by a *stem* that its variants share, so that "connected", "connecting" and "connections" become one index term. The stem is computed by rules on the letters of the word, without a dictionary, and it need not be a real word. It is applied by the same function at indexing time and at query time, so the [inverted index](/inverted-index/) has one posting list for the whole group of variants. Manning, Raghavan and Schuetze sum up its effect on retrieval: it raises recall and lowers precision.

## In plain words

A search for "connections" should usually also find a document that says "connected". The index sees only exact words, so the two forms would never meet. A stemmer cuts both down to "connect" before they go into the index, and it cuts the words of each query in the same way. Now one entry of the index covers all the forms.

The cut is made by fixed rules about word endings, not by looking words up. That is fast and works on new words, but it makes two kinds of mistakes. It can join words that are not related, such as "general" and "generous", and it can miss words that are related but end in a way the rules do not know. So a stemmer helps a search find more documents, and some of the extra documents are wrong.

## When it applies

- **Text with inflection.** The language has suffixes for number, tense and derivation, as English has, and the rules of the stemmer are written for that language.
- **Short queries and exact-match retrieval.** A query of two or three words that must match index terms exactly gains most, because one missed form can lose a relevant document.
- **Index and queries under one control.** The same stemmer, in the same version, runs on both sides. A stem from one stemmer does not match a stem from another.
- **Recall matters more than precision.** For a ranked list where the first results must all be right, the gain can be small or negative; measure it.

It does not apply to fields where the exact form matters, such as names, codes, or a phrase in quotation marks, and it does not reach irregular forms such as "went" and "go".

## The template

Stemming is a function STEM applied at two places of the indexing pipeline. The holes to fill are in capitals.

```pseudo id=main
BUILD-STEMMED-INDEX(collection)
L1  for each document d, in order of id do
L2      for each token w of d do
L3          t ← NORMALIZE(w)                    ▷ case folding, removal of punctuation
L4          if t is not in EXCEPTIONS then t ← STEM(t)
L5          add d to the posting list of t

STEMMED-QUERY(query)
L6  T ← ()
L7  for each token w of the query: t ← NORMALIZE(w); if t is not in EXCEPTIONS then t ← STEM(t); append t to T
L8  return the posting lists of the terms of T, for the query processor
```

**The holes.** STEM is the conflation function: a suffix stripper such as the [Porter stemmer](/porter-stemmer/), a stemmer driven by a table of rules, or a lookup in a table of word forms. NORMALIZE is everything that must happen before it, because a stemmer expects lower case letters only. EXCEPTIONS is a set of words that must stay as they are, such as names and short words.

**The invariant.** A document $d$ is in the posting list of a term $t$ exactly when some token $w$ of $d$ has STEM(NORMALIZE($w$)) $= t$, and the query looks up the same function of its words. So a query word matches a document word exactly when the two have the same stem. This holds only if lines L3 and L4 and line L7 use the same NORMALIZE, the same EXCEPTIONS and the same STEM.

**Walk-through on the toy collection.** Without stemming, the 8 documents have 50 terms. The Boolean AND of $q_2$, "posting list merge", is empty, because $d_5$, the most relevant document, says "lists" and not "list". With the Porter stemmer the collection has 46 terms, the query becomes "post list merg", and the AND gives $d_5$. The OR of $q_3$, "rank documents", gives only $d_7$ without stemming and $d_4$ and $d_7$ with it, because $d_4$ says "document". On this collection the plural rules alone (step 1a of the Porter stemmer) give the same answers to all four queries, with 47 terms.

**The cost.** STEM runs once per distinct word if its results are kept in a [hash table](/hash-table/), so the cost at indexing time is linear in the size of the vocabulary plus one table lookup per token. The index gets smaller: fewer terms, and fewer posting lists.

## Classic examples

- **Plural folding.** Only the rules for the plural s, such as step 1a of the Porter stemmer: sses to ss, ies to i, s removed. It is safe and it does most of the work on the toy collection above.
- **The [Porter stemmer](/porter-stemmer/).** Five phases of suffix rules, each with a condition on the length of the remaining stem. It is the usual English stemmer of information retrieval systems.
- **The Lovins stemmer.** The first published stemmer, from 1968: a long list of endings, each with a condition. It removes the longest ending whose condition holds, then applies transformation rules to the end of the stem, in two steps in all.
- **The Paice/Husk stemmer.** A table of suffix rules, applied iteratively: after one rule removes or replaces an ending, the stemmer looks in the table again for the new ending.
- **Stemming at query time.** Leave the index unstemmed and, for each query word, add the terms of the vocabulary that have the same stem, a form of [query expansion](/query-expansion/). The index keeps the exact forms for phrase and exact queries, and the query gets longer.

## Variations

- **Lemmatization.** Map each word to its dictionary form with a dictionary and a morphological analysis of the word, so that "saw" can become "see" or "saw" by its part of speech. Manning, Raghavan and Schuetze report that the gain over stemming for English retrieval is small.
- **Light and heavy stemming.** A light stemmer removes only inflection (plural, tense); a heavy one also removes derivational suffixes such as "-ation" and "-ness". The heavier the stemmer, the more words share a stem.
- **Stems kept next to the words.** Index both the word and its stem, and let the query choose. This costs space and keeps exact matching possible.
- **Other languages.** Each language needs its own rules. For languages with compound words or rich inflection, rule stemmers are weaker, and character [k-gram indexes](/k-gram-index/) are an alternative that needs no rules.

## Pitfalls

- **Over-stemming.** Unrelated words get one stem, and a query for one finds the other. Porter's stemmer maps "general" and "generous" to "gener", "university" and "universe" to "univers", and "organization" and "organ" to "organ". Manning, Raghavan and Schuetze show the same with "operate", "operating" and "operational", which all become "oper", so queries about operational research, operating systems and operative dentistry meet.
- **Under-stemming.** Related words keep different stems, and the stemmer does not help. Porter's stemmer gives "probe" and "probat" for "probe" and "probate", and it cannot reach irregular forms.
- **Different functions for the index and the query.** If the index was built with one stemmer, version or normalization and the query uses another, many words find nothing, with no error. Store the name and version of the stemmer with the index.
- **Stemming text that is not prose.** Names, product codes and identifiers must not be stemmed: a stemmer turns "Jones" into "jone".
- **Stems shown to users.** A stem such as "happi" is an index key, not a word. Show the words of the document, and use the stems only for matching.

## References
