---
tag: JX112C
kind: algorithm
slug: luhn-summarization
name: Luhn summarization
aliases:
- Luhn auto-abstract
area: natural-language-and-speech/text-generation-and-decoding
level: intro
summary: "Luhn's 1958 extractive method: words of medium frequency are significant, and a sentence scores the best (significant words)^2 / length over its clusters of close significant words."
model: word-ram
complexity:
  vars: {N: the number of words in the document, n: the number of sentences}
  time: {expected: "O(N + n log n)"}
  space: {extra: "O(N)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1958
  people: [Hans Peter Luhn]
  note: Luhn of IBM ran the method on an IBM 704 and published it in the IBM Journal of Research and Development in April 1958. It is the first published automatic summarizer.
prereqs: [automatic-summarization, zipfs-law]
see_also: [tf-idf, stop-word-removal, stemming, textrank, lexrank, rouge, maximal-marginal-relevance, sentence-boundary-detection]
sources:
  - paper: doi:10.1147/rd.22.0159
    title: H. P. Luhn, The automatic creation of literature abstracts, IBM Journal of Research and Development 2(2), 1958, pages 159 to 165
    locator: "pages 160 and 161 with Figure 1 (the frequency cut offs C and D), page 161 (the limit of four or five non-significant words), page 162 with Figure 2 (the score 4^2 / 7 = 2.3, the machine procedure, the merging of words and the cut off on the sentence scores), page 165 (the premium weight for a class of words)"
  - paper: doi:10.1561/1500000015
    title: Ani Nenkova and Kathleen McKeown, Automatic Summarization, Foundations and Trends in Information Retrieval 5(2-3), 2011, pages 103 to 233
    locator: the survey of extractive methods based on word frequency
---

Luhn summarization picks the sentences of a document that contain dense groups of its important words. A word is important (significant) when it is not a common word and its frequency in the document is neither too high nor too low. In each sentence, the significant words that stand close together form clusters, and a cluster with $m$ significant words over a span of $\ell$ words scores $m^2 / \ell$. A sentence scores its best cluster, and the sentences with the highest scores form the extract. Hans Peter Luhn described the method in 1958. It is a heuristic: no objective is optimized, and its quality is only measured.

## In plain words

An author repeats the words of the topic. "Solar" and "cell" come back many times in an article on solar cells, while "the" is everywhere and "weather" appears once. So Luhn counts the words of the document, drops a list of common words, and keeps the words with a medium count. These are the significant words.

A sentence where several significant words stand close together is likely to state a main point. Luhn looks for runs of significant words with at most four other words between two neighbours. A run with many significant words in a short span gets a high score. The sentence takes the score of its best run.

Then the program prints the sentences with the highest scores, in the order of the document. This is the abstract.

## The problem

The input is a document $D$ split into sentences $s_1, \ldots, s_n$, each a list of words, together with a list of stop words, two frequency cut offs $lo \le hi$, a gap limit $g$ (Luhn used 4) and a number $k$ of sentences to extract. A word $w$ is mapped to a key $\kappa(w)$, for example its lower-case form or its stem. Let $f(v)$ be the number of words of $D$ with key $v$ that are not stop words. The set of significant keys is

$$\mathrm{Sig} = \{ v : lo \le f(v) \le hi \}.$$

In a sentence, let $p_1 < \cdots < p_r$ be the positions of the words with a key in $\mathrm{Sig}$. A cluster is a maximal run $p_a, \ldots, p_b$ such that $p_{t+1} - p_t - 1 \le g$ for every $t$ from $a$ to $b - 1$, so that two neighbours in it have at most $g$ non-significant words between them. Its score is $(b - a + 1)^2 / (p_b - p_a + 1)$, and the score of the sentence is the largest score of its clusters, or 0 if it has no significant word. The task is to output the $k$ sentences with the highest scores, in document order. Luhn's own rule outputs every sentence whose score is above a fixed cut off instead.

## The algorithm

```pseudo id=main
LUHN(D, stop, lo, hi, g, k)        ▷ D: a list of sentences, each a list of words
L1  f ← an empty table of counts
L2  for each word w of D with κ(w) not in stop do f(κ(w)) ← f(κ(w)) + 1
L3  Sig ← the keys v with lo ≤ f(v) ≤ hi
L4  for each sentence s of D do
L5      p_1 < ... < p_r ← the positions of s whose key is in Sig
L6      score(s) ← 0; a ← 1
L7      for b ← 1 to r do
L8          if b = r or p_(b+1) - p_b - 1 > g then        ▷ the cluster p_a .. p_b ends here
L9              m ← b - a + 1; len ← p_b - p_a + 1
L10             score(s) ← max(score(s), m² / len)
L11             a ← b + 1
L12 return the k sentences with the highest score, in document order
```

Lines L1 to L3 find the significant words. Luhn's program deleted the common words by a table lookup and then the words of low frequency. His Figure 1 also draws an upper cut off C, because the most frequent words carry little information about the topic, but he left the place of both cut offs to experience. Lines L5 to L11 scan one sentence from left to right. Line L8 closes a cluster when the next significant word is too far away or when there is no next word. Line L12 breaks ties by the earlier sentence and never picks a sentence with score 0.

**Merging words.** Luhn sorted the words alphabetically and compared neighbours letter by letter. From the first letter where two words differed, he counted the remaining letters of both words, and if there were six or fewer he treated them as one notion, as with "similar" and "similarity". The key function $\kappa$ plays this role here; a [stemmer](/stemming/) such as the [Porter stemmer](/porter-stemmer/) is the usual modern choice.

## Example

The document has five sentences. The stop words are the, a, into, from, to, was, that, is and less. With $lo = 2$, $hi = 3$ and $g = 4$, the counts are solar 3, cell 3, light 2, power 2, thin 2 and silicon 2, and every other word occurs once. So these six words are significant.

| # | sentence (significant words in bold) | cluster span | $m$ | score |
|---|---|---|---|---|
| 1 | The new **solar cell** turns **light** into **power** | words 3 to 8 | 4 | $16/6 = 2.667$ |
| 2 | Engineers built the **solar cell** from **thin silicon** | words 4 to 8 | 4 | $16/5 = 3.2$ |
| 3 | The weather was cold that week | none | 0 | 0 |
| 4 | A **thin silicon solar cell** costs less to build | words 2 to 5 | 4 | $16/4 = 4$ |
| 5 | **Power** from **light** is clean | words 1 to 3 | 2 | $4/3 = 1.333$ |

For $k = 2$ the extract is sentences 2 and 4, printed in that order. With Luhn's rule and a cut off of 2, sentences 1, 2 and 4 are printed.

Luhn's Figure 2 has a cluster of seven words with four significant words, for example S x S S x x S, with score $4^2 / 7 = 2.3$. The gap limit matters: in S a b c d S the two significant words have four words between them and form one cluster with score $2^2 / 6 = 0.667$, while in S a b c d e S they are five words apart and form two clusters, each with score $1^2 / 1 = 1$.

## Correctness

The algorithm computes the scores of the definition exactly. Lines L1 to L3 count each key once for each of its occurrences, so $\mathrm{Sig}$ is the set of the definition. In a sentence, the loop of lines L7 to L11 keeps the invariant that $p_a, \ldots, p_b$ is the current run with all inner gaps at most $g$, and that $p_a$ starts a cluster (it is $p_1$, or the gap before it is larger than $g$). Line L8 ends the run exactly where the gap to the next position is larger than $g$, or at the last position, so every cluster is scored once and nothing else is scored. Line L12 then sorts by score. This is a theorem; the full proof is in the proofs file.

Whether the chosen sentences make a good abstract is a different matter. The significance factor is a heuristic: it does not maximize a stated objective, and its value was judged only by reading the output. Luhn reported encouraging results on about 50 articles of 300 to 4,500 words and planned a test with 100 readers.

## Complexity

With a hash table, lines L1 to L3 take $O(N)$ expected time and $O(V) \subseteq O(N)$ space for the $V$ distinct keys. Lines L5 to L11 visit each word of a sentence a constant number of times, so all sentences take $O(N)$ time. Line L12 sorts the $n$ scores in $O(n \log n)$ time, or selects the top $k$ in $O(n)$ time. In total this is $O(N + n \log n)$ expected time and $O(N)$ space for the document and the counts. Luhn's program sorted the words alphabetically to count them, which costs $O(N \log N)$ comparisons.

## Properties

- **Range.** A cluster with $m$ significant words has length $\ell$ with $m \le \ell \le m + (m - 1) g$, so its score is in $(m / (g + 1), m]$. A sentence score is 0 or at least $1/(g + 1)$, and at most the number of significant words in the sentence.
- **Maximal clusters, not the best span.** The score uses whole clusters. In S a b c d S S S the cluster has score $4^2 / 8 = 2$, although its last three words alone would give $3^2 / 3 = 3$.
- **Long sentences.** The score grows with $m$, so long sentences with many significant words tend to win. Luhn did not normalize by the sentence length.
- **Document only.** The counts come from the document itself, with no corpus statistics. A word that is frequent in every document of a collection still counts as significant if it passes the cut offs. [tf-idf](/tf-idf/) weights fix this with a document frequency from a corpus.
- **Deterministic and fast.** One pass over the words and one sort.

## Variants and improvements

- **Fixed length.** Luhn noted that the program could print a fixed number of the best sentences instead of all sentences above the cut off. The code offers both.
- **Emphasis.** Luhn proposed a premium weight for a given class of words, to bias the abstract to the interests of a reader. Later systems use a query in the same way.
- **Sections.** For a long article, Luhn proposed to run the method on overlapping parts of the text, so that each part gets its own significant words.
- **Frequency weights.** Later extractive systems replaced the binary test of significance with weights such as [tf-idf](/tf-idf/) or word probabilities, and added a step against redundancy such as [maximal marginal relevance](/maximal-marginal-relevance/).
- **Graph centrality.** [TextRank](/textrank/) and [LexRank](/lexrank/) score a sentence by its similarity to the other sentences instead of by its own words.

## When to use it

Use Luhn's method as a baseline for extractive summarization, or when you need a summarizer with no training data, no corpus and no model. It works best on technical text with a clear topic vocabulary. For news, the first sentences of the article are a hard baseline to beat: on CNN/Daily Mail the first three sentences scored higher on [ROUGE](/rouge/) than the neural models of See et al. (2017), a measurement. Compare Luhn's method with that baseline and with graph methods on your own data before you use it.

## Pitfalls

- **No stop list.** Without a stop list, or with $hi$ too high, line L2 makes "the" and "of" significant, and every long sentence wins. Set $hi$ or a stop list.
- **Low cut off of 1.** With $lo = 1$ every content word is significant, and the score mostly measures sentence length. Luhn deleted the words of low frequency.
- **Gap counted wrong.** Line L8 tests the number of words between two significant words, $p_{b+1} - p_b - 1$, not the distance $p_{b+1} - p_b$. With the distance, the limit is one word smaller than intended.
- **Length counted wrong.** Line L9 counts the cluster from its first to its last significant word. Counting the whole sentence gives another method.
- **Best span instead of clusters.** Taking the maximum of $m^2 / \ell$ over all spans of a cluster gives higher scores than Luhn's method; see the example under Properties.
- **Tokens and keys.** Counting "Cell" and "cell" or "cell" and "cells" as different words splits the counts. Fix the key function before you compare results.

## Implementations

## History

Hans Peter Luhn worked on information retrieval at IBM. In "The automatic creation of literature abstracts" (April 1958) he described a program for the IBM 704 that read an article from punched cards, deleted the common words, merged words with the same beginning, counted the rest and printed the sentences with the highest significance factor. He argued from the shape of the word frequency curve, the subject of [Zipf's law](/zipfs-law/), that words of medium frequency mark the topic, while the most frequent words are too common and the rarest are too few to matter. He tested the program on about 50 articles and found the results good enough to plan a test with readers. Edmundson (1969) later added cue words, title words and the position of the sentence to Luhn's frequency feature. Word frequency is still a feature of most extractive methods.

## References
