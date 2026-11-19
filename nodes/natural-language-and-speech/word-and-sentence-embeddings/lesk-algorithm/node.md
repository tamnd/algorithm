---
tag: JX07Y6
kind: algorithm
slug: lesk-algorithm
name: Lesk algorithm
aliases:
- simplified Lesk
- gloss overlap disambiguation
area: natural-language-and-speech/word-and-sentence-embeddings
level: intro
summary: Choose the sense whose dictionary gloss shares the most words with the context of the ambiguous word.
solves: [word-sense-disambiguation]
model: word-ram
complexity:
  vars: {n: the number of context tokens, r: the number of senses of the target word, g: the largest number of words in the gloss and examples of one sense}
  time: {average: "O(n + r g)", worst: "O(n + r g log g)"}
  space: {extra: "O(n + g)"}
properties: {deterministic: true, exact: false, online: false, recursive: false, supervised: false}
history:
  year: 1986
  people: [Michael Lesk]
  note: Lesk used machine-readable dictionaries to choose senses by counting the words that the definitions share, with the pine cone and ice cream cone of his title as the example.
prereqs: [word-sense-disambiguation]
see_also: [yarowsky-algorithm, resnik-similarity, stop-word-removal, stemming, lemmatization, jaccard-similarity, naive-bayes-classifier, distributional-hypothesis]
sources:
  - paper: doi:10.1145/318723.318728
    title: Michael Lesk, Automatic sense disambiguation using machine readable dictionaries, how to tell a pine cone from an ice cream cone, Proceedings of SIGDOC '86, 1986, pages 24 to 26
    locator: the method of counting the words shared by the dictionary definitions of the senses of words that occur together
  - paper: "Adam Kilgarriff and Joseph Rosenzweig, Framework and results for English SENSEVAL, Computers and the Humanities 34(1-2), 2000"
    title: Kilgarriff and Rosenzweig 2000
    locator: the simplified Lesk baseline, which compares each sense definition with the words of the context
  - paper: doi:10.1145/1459352.1459355
    title: Roberto Navigli, Word sense disambiguation, a survey, ACM Computing Surveys 41(2), 2009, article 10
    locator: the section on knowledge-based disambiguation by overlap of sense definitions
  - paper: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft, https://web.stanford.edu/~jurafsky/slp3/"
    title: Jurafsky and Martin, SLP3 draft of August 2025
    locator: Appendix Word Senses and WordNet, the sections on word sense disambiguation and the simplified Lesk algorithm
---

The Lesk algorithm solves [word sense disambiguation](/word-sense-disambiguation/) with a dictionary and no training data. For each sense of the ambiguous word it takes the words of the dictionary entry, the gloss and the example sentences, and it counts how many of them also occur in the context. It returns the sense with the largest count. The form on this page is the simplified Lesk algorithm, which compares each entry with the context words. Lesk's original form compares the entries of two words that occur together with each other. Both are heuristics: they choose the sense with the most shared words, and nothing proves that this is the intended sense. The [Yarowsky algorithm](/yarowsky-algorithm/) learns its evidence from a corpus instead.

## In plain words

A dictionary explains each sense of a word with other words. If a sentence talks about a river, boats and water, the sense of "bank" whose explanation also talks about water is probably the right one.

So the method takes the sentence, drops small words such as "the" and "of", and keeps the rest. For each sense it looks at the definition and the example sentences of that sense, also without the small words. It counts the words that the sense and the sentence have in common. The sense with the highest count wins. If no sense shares any word with the sentence, it keeps the first sense of the dictionary, which is usually the most common one. Lesk's own version does the same with two words at once, for example "pine" and "cone", and picks the two senses whose definitions share the most words.

## The problem

The input is a target word $w$, its context (a list of tokens, for example the sentence), and the senses $s_1, \ldots, s_r$ of $w$ in a dictionary, in dictionary order with the most frequent sense first. Each sense has a gloss and possibly example sentences. A stop list of function words is fixed. The output is one sense of $w$. This is the per-occurrence classification of the [word sense disambiguation](/word-sense-disambiguation/) problem, solved with the dictionary as the only knowledge.

The signature of a sense is the set of words of its gloss and examples, lowercased, minus the stop words. The context set $C$ is the set of context words, lowercased, minus the stop words and minus $w$ itself. The overlap of $s_i$ is $|S_i \cap C|$.

## The algorithm

```pseudo id=main
SIMPLIFIED-LESK(w, context, s_1 .. s_r)
L1  best ← s_1                          ▷ the most frequent sense
L2  maxoverlap ← 0
L3  C ← set of the context words, minus stop words and minus w
L4  for i ← 1 to r do
L5      S ← set of the words in the gloss and examples of s_i, minus stop words
L6      overlap ← |S ∩ C|
L7      if overlap > maxoverlap then
L8          maxoverlap ← overlap; best ← s_i
L9  return best
```

The strict test of line L7 gives each tie to the earlier sense, and the start values of lines L1 and L2 make the first sense the answer when no sense overlaps the context. With hash sets, line L6 costs time proportional to the smaller set.

**The original form.** For two words $a$ and $b$ that occur together, GLOSS-PAIR-LESK compares the signature of each sense of $a$ with the signature of each sense of $b$ and returns the pair of senses with the largest overlap, the first pair on ties. For more than two words, the joint choice of one sense per word that maximizes the sum of the pairwise overlaps must try every combination, which grows as the product of the numbers of senses; the code has this as all_pairs_lesk for a few words.

## Example

The sense inventory for "bank", written for this page:

| sense | gloss | example |
| --- | --- | --- |
| bank.1 | a financial institution that accepts deposits and lends money | she opened an account at the bank |
| bank.2 | sloping land beside a body of water | they sat on the bank of the river and watched the boats |
| bank.3 | a row of similar objects | a bank of switches |

With the stop list of the code, the signature of bank.2 is {sloping, land, beside, body, water, sat, river, watched, boats}. Four contexts:

| context | overlaps (1, 2, 3) | shared words | result |
| --- | --- | --- | --- |
| the fishermen pulled their boats onto the bank when the river rose | 0, 2, 0 | boats, river | bank.2 |
| I went to the bank to deposit my money | 1, 0, 0 | money | bank.1 |
| the bank was closed | 0, 0, 0 | none | bank.1 (the default) |
| a body of water and a bank of switches | 0, 2, 1 | body, water; switches | bank.2 |

In the second context, "deposit" does not match "deposits" in the gloss, so only "money" counts. In the third context nothing matches, and line L1 decides.

For the original form, take two words with senses written for this page: pine.1 "an evergreen tree with needle shaped leaves", pine.2 "to waste away from sorrow or longing", cone.1 "a solid body that narrows to a point from a round base", cone.2 "the woody fruit of an evergreen tree" and cone.3 "a crisp wafer shaped to hold ice cream". Of the six pairs, only (pine.1, cone.2) shares words, namely "evergreen" and "tree", so GLOSS-PAIR-LESK returns that pair with overlap 2.

## Correctness

The claim is exact about what the algorithm computes, not about the sense the writer meant: SIMPLIFIED-LESK returns the first sense with the largest overlap, or $s_1$ when every overlap is 0. The loop of line L4 keeps the invariant that after $i$ senses, $maxoverlap$ is the largest of 0 and the first $i$ overlaps, and $best$ is the first sense that reaches it, or $s_1$ if it is 0. Line L7 changes them only for a strictly larger overlap, which is exactly what keeps the "first" in the invariant. The full proof, with the pair form, is below.

Whether the chosen sense is the right one is an empirical question. The overlap rule is a heuristic, and its accuracy is a measurement that depends on the dictionary, the stop list and the test set.

## Complexity

The model is the [word-RAM](/word-ram/) with hash sets of words, so a set insertion and a lookup take expected constant time.

- **Context set.** Line L3 inserts $n$ words: $O(n)$ expected time and $O(n)$ space.
- **One sense.** Line L5 builds a set of at most $g$ words and line L6 looks each of them up in $C$: $O(g)$ expected time.
- **All senses.** $O(n + r g)$ expected time. With sorted lists instead of hash sets, the intersections cost $O(g \log g)$ each, which gives the worst case of the front matter. Only one signature is kept at a time, so the extra space is $O(n + g)$.
- **Pair form.** $O(r_a r_b g)$ for words with $r_a$ and $r_b$ senses, after building the signatures. The joint form for $m$ words tries $\prod_i r_i$ combinations.

## Properties

- **Unsupervised.** It needs no sense-tagged text, only a dictionary with glosses.
- **Deterministic.** The answer depends on the order of the senses only through the tie rule.
- **Sparse evidence.** Glosses are short, so most overlaps are 0 or 1, and many decisions fall back to the first sense.
- **Bag of words.** The order of the words and their distance from the target do not count.

## Variants and improvements

- **Original Lesk.** Compare the glosses of the senses of the target with the glosses of the senses of the context words, as in the pair form above.
- **Extended gloss overlap.** Banerjee and Pedersen 2002 add the glosses of related WordNet senses (hypernyms, hyponyms and others) to each signature, and score longer shared phrases higher.
- **Weighted overlap.** Weight each shared word by its inverse document frequency, as in [tf-idf](/tf-idf/), so that a shared rare word counts more than a shared common one.
- **Corpus Lesk.** Add the words of sense-tagged example sentences from a corpus to the signatures, which is a step toward a supervised classifier such as [naive Bayes](/naive-bayes-classifier/).
- **Joint choice.** Choosing the senses of all the words of a sentence at once makes the search exponential; Cowie, Guthrie and Guthrie 1992 searched it with simulated annealing.

## When to use it

Use simplified Lesk as a baseline, or when there is a dictionary but no sense-tagged corpus. It is easy to explain, since the shared words are the reason for the answer. When sense-tagged data exist, a supervised classifier is usually better, and the most frequent sense alone is a strong baseline that simplified Lesk must beat to be worth its cost (see [word sense disambiguation](/word-sense-disambiguation/)).

## Pitfalls

- **The target word in the signature.** The example sentences of a dictionary usually contain the target word, as all three examples above do. If line L3 keeps $w$ in the context, every sense with an example gets one free point. Remove $w$ in line L3, as the pseudocode does.
- **No stop list.** If lines L3 and L5 keep function words, "the", "of" and "a" decide many choices. Remove the stop words on both sides (see [stop word removal](/stop-word-removal/)).
- **Word forms.** Line L6 matches exact strings, so "deposit" does not match "deposits". Apply [stemming](/stemming/) or [lemmatization](/lemmatization/) to both sides before line L6.
- **The tie rule.** With "≥" in line L7, ties go to the last sense, and a context with no overlap returns the last sense instead of the most frequent one. Keep the strict test, with the senses in frequency order.
- **Counting tokens instead of types.** If the signature or the context is a list and not a set, a word repeated in a gloss counts several times. Use sets in lines L3 and L5, or say that the page uses multisets.

## Implementations

## History

Lesk 1986 proposed the method at SIGDOC, using machine-readable dictionaries, and named the paper after the pine cone and ice cream cone example of the title. Later work kept the idea and changed what is compared: Cowie, Guthrie and Guthrie 1992 chose all the senses of a sentence at once, Kilgarriff and Rosenzweig 2000 used the simplified form, which compares the definitions with the context words, as a baseline in the first SENSEVAL evaluation, and Banerjee and Pedersen 2002 extended the signatures with WordNet relations.

## References
