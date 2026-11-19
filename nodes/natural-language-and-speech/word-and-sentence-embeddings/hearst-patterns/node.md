---
tag: B0F1S5
kind: algorithm
slug: hearst-patterns
name: Hearst patterns
aliases:
- lexico-syntactic hyponymy patterns
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: Extract hyponym and hypernym pairs from text with six hand-chosen lexico-syntactic patterns, such as X such as Y and Y and other X.
model: word-ram
complexity:
  vars: {n: the number of items (noun phrases and words) of the sentence}
  time: {worst: "O(n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false, supervised: false}
history:
  year: 1992
  people: [Marti A. Hearst]
  note: Hearst listed six patterns around noun phrases that signal the hyponym relation, described a manual procedure for finding more, and compared the pairs she found in an encyclopedia with WordNet.
prereqs: [regular-expression]
see_also: [text-chunking, part-of-speech-tagging, relation-extraction, dipre, distant-supervision, finite-state-transducer, yarowsky-algorithm, distributional-hypothesis]
sources:
  - paper: "Marti A. Hearst, Automatic acquisition of hyponyms from large text corpora, Proceedings of COLING-92, 1992, pages 539 to 545"
    title: Hearst 1992
    locator: the six patterns numbered 1 to 6 with their examples, the three properties a pattern should have, the five step procedure for finding new patterns, and the results on Grolier's encyclopedia and the New York Times compared with WordNet
  - paper: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft, https://web.stanford.edu/~jurafsky/slp3/"
    title: Jurafsky and Martin, SLP3 draft of August 2025
    locator: the chapter on information extraction, the section on relation extraction with patterns
---

Hearst patterns find pairs of noun phrases where one names a kind of the other, the hyponym relation, as in "France" and "European countries". Hearst 1992 listed six patterns that are made of a few fixed words and slots for noun phrases. "NP such as NP, NP and NP" is one of them: every noun phrase in the list after "such as" is a hyponym of the noun phrase before it. The patterns are found by hand. A matcher that runs them is a single left to right scan over a sentence whose noun phrases a [chunker](/text-chunking/) has already marked. The patterns are a heuristic: a match is evidence for the relation, not a proof of it. They find few pairs per million words, and Hearst judged the quality of the pairs she found high.

## In plain words

People write sentences such as "most European countries, especially France, England and Spain". Without knowing anything about geography, a reader can tell from the words "especially" and the list that France, England and Spain are European countries.

Hearst picked six such fixed phrases: "such as", "such ... as", "or other", "and other", "including" and "especially". The method first groups the words of a sentence into noun phrases. Then it looks for one of the fixed phrases with a noun phrase on one side and a list of noun phrases on the other side. Each noun phrase in the list is reported as a kind of the single noun phrase. The method needs no training data and no dictionary, but it only finds pairs that a writer happened to state in one of these six ways.

## The problem

The input is a sentence as a list of $n$ items, where each item is a noun phrase (NP) from a chunker or a single word, and the comma is a word. The output is every triple (hyponym, hypernym, pattern) that one of the six patterns matches. With CONJ for "and" or "or", the patterns of Hearst 1992 are:

| pattern | form | hypernym | hyponyms |
| --- | --- | --- | --- |
| 1 | NP$_0$ [,] such as LIST | NP$_0$ | the NPs of LIST |
| 2 | such NP$_0$ as LIST | NP$_0$ | the NPs of LIST |
| 3 | LEFT [,] or other NP$_0$ | NP$_0$ | the NPs of LEFT |
| 4 | LEFT [,] and other NP$_0$ | NP$_0$ | the NPs of LEFT |
| 5 | NP$_0$ [,] including LIST | NP$_0$ | the NPs of LIST |
| 6 | NP$_0$ [,] especially LIST | NP$_0$ | the NPs of LIST |

A LIST is NP ("," NP)$^*$ [[","] CONJ NP], and a LEFT is NP ("," NP)$^*$. Brackets mark an optional part. Each list is read as far as it goes: to the right after the trigger words, to the left before them. With these rules the output is well defined, and the matcher below computes it exactly.

## The algorithm

RIGHT-LIST($q$) returns the positions of the NPs of the longest LIST that starts at item $q$. It reads ", NP" as long as it can, then one "CONJ NP" or ", CONJ NP" if it is there. LEFT-LIST($p$) skips one comma before $p$ if there is one, then reads NP and ", NP" pairs to the left. NP-BEFORE($p$) is the NP at $p - 1$, or at $p - 2$ with a comma at $p - 1$, or nothing.

```pseudo id=main
HEARST(a_0 .. a_{n-1})
L1  R ← empty list
L2  for p ← 0 to n - 1 do
L3      if a_p a_{p+1} = "such as" and h ← NP-BEFORE(p) exists then add (x, h, 1) to R for each x in RIGHT-LIST(p + 2)
L4      else if a_p = "such", a_{p+1} is an NP and a_{p+2} = "as" then add (x, p + 1, 2) to R for each x in RIGHT-LIST(p + 3)
L5      else if a_p ∈ {"including", "especially"} and h ← NP-BEFORE(p) exists then add (x, h, 5 or 6) to R for each x in RIGHT-LIST(p + 1)
L6      else if a_p ∈ {"or", "and"}, a_{p+1} = "other" and a_{p+2} is an NP then add (x, p + 2, 3 or 4) to R for each x in LEFT-LIST(p)
L7  return R
```

Words are compared in lowercase. Each position triggers at most one line, since lines L3 and L4 differ in the item after "such", and lines L5 and L6 test other words.

## Example

The sentences below are the examples of Hearst 1992, with the noun phrases in brackets as a chunker could mark them.

| sentence | line | output pairs |
| --- | --- | --- |
| [the bow lute] , such as [the Bambara ndang] , is plucked | L3 | (the Bambara ndang, the bow lute) |
| works by such [authors] as [Herrick] , [Goldsmith] , and [Shakespeare] | L4 | (Herrick, authors), (Goldsmith, authors), (Shakespeare, authors) |
| [bruises] , [wounds] , [broken bones] or other [injuries] | L6 | (bruises, injuries), (wounds, injuries), (broken bones, injuries) |
| [temples] , [treasuries] , and other [important civic buildings] | L6 | (temples, important civic buildings), (treasuries, important civic buildings) |
| [all common-law countries] , including [Canada] and [England] | L5 | (Canada, all common-law countries), (England, all common-law countries) |
| [most European countries] , especially [France] , [England] , and [Spain] | L5 | (France, most European countries), (England, most European countries), (Spain, most European countries) |

A trace of the last sentence, with the items numbered from 0: [most European countries] is 0, "," is 1, "especially" is 2, [France] is 3, "," is 4, [England] is 5, "," is 6, "and" is 7 and [Spain] is 8.

| p | item | what happens |
| --- | --- | --- |
| 0, 1 | NP, "," | no trigger |
| 2 | especially | line L5: NP-BEFORE(2) skips the comma at 1 and gives 0; RIGHT-LIST(3) reads 3, then ", NP" at 4 and 5, then ", and NP" at 6 to 8, and stops |
| 3 to 6 | NPs and commas | no trigger |
| 7 | and | line L6 is false, since item 8 is an NP and not "other" |
| 8 | NP | no trigger |

The output is (3, 0, 6), (5, 0, 6) and (8, 0, 6).

## Correctness

The claim is exact about the patterns and says nothing about the meaning of the sentence: HEARST returns exactly the triples of the six patterns, with the longest lists, in the order of the trigger position. The key step is that a list can grow in only one way at each point. After a list of NPs separated by commas, the next items are ", NP", "CONJ NP" or ", CONJ NP", and these cases exclude each other, so the lists that start at one position form a chain and the scan of RIGHT-LIST stops at the longest one. The same holds for LEFT-LIST to the left. Each position triggers at most one of lines L3 to L6, and each line tests exactly the condition of its pattern. The full proof is below.

Whether a match is a true hyponym pair is a different question. The patterns are a heuristic, and their quality is a measurement on a corpus.

## Complexity

The model is the [word-RAM](/word-ram/), with each item a word or an NP whose kind is known in constant time.

- **Triggers.** Lines L3 to L6 test a constant number of items at each position: $O(n)$ for the loop of line L2.
- **Lists.** A list holds only NPs, commas and one conjunction followed by an NP. None of these is a trigger, since a trigger conjunction is followed by "other". So two right lists never share an item, two left lists never share an item, and each item is read by at most two lists. All the calls of RIGHT-LIST and LEFT-LIST together take $O(n)$ time.
- **Total.** $O(n)$ time per sentence, and $O(n)$ space for the output, which has at most one triple per item for each kind of list. Over a corpus the cost is linear in its size, plus the cost of the chunker.

## Properties

- **No training data.** The six patterns are fixed in advance, and the matcher needs no labeled pairs and no lexicon.
- **Domain independent.** Hearst chose patterns that occur often and in many kinds of text, that almost always indicate the relation, and that can be found with little knowledge in advance. These are the three properties she asked of a pattern, and the second one is a heuristic.
- **Low recall.** A pair is found only if one sentence states it in one of the six forms. Hearst 1992 reports, as a measurement, 7067 sentences with "such as" in the 8.6 million words of Grolier's encyclopedia and 152 relations that met her restrictions on the noun phrases, or 330 with looser restrictions, and 46 relations from 3178 sentences in about 20 million words of the New York Times.
- **Checked against WordNet.** Of 226 unique words in the encyclopedia pairs, 180 were in WordNet, and of the 106 relations whose words were both in WordNet, 61 were already there. Hearst judged the quality of the pairs high overall, without a precision figure.
- **Order of the output.** The hypernym of patterns 1, 2, 5 and 6 comes before the list, and that of patterns 3 and 4 after it.

## Variants and improvements

- **More patterns.** Hearst 1992 gives a manual procedure: take a relation and pairs known to have it, find sentences where the two words occur close together, find what these sentences have in common, and use a new pattern to find new pairs. She did not automate it, because the step of finding what the sentences have in common was not well defined.
- **Learned patterns.** Later work learns patterns from dependency paths between known pairs, with known pairs from a lexicon as the training data, which is the idea of [distant supervision](/distant-supervision/). [DIPRE](/dipre/) grows patterns and pairs in a loop, starting from a few seed pairs.
- **Counts over a corpus.** Pairs from a large corpus can be scored by how often each pattern links them, for example with [PPMI](/positive-pointwise-mutual-information/), and smoothed by a low-rank factorization, which finds pairs that no single sentence states.
- **Regular expressions over tags.** Without a chunker, the patterns can be written as [regular expressions](/regular-expression/) over [part-of-speech tags](/part-of-speech-tagging/), with an NP as a run of determiners, adjectives and nouns.

## When to use it

Use the patterns to seed a taxonomy or to extend a lexicon such as WordNet from a large corpus, when high precision matters more than coverage and there is no labeled data. They are also a simple baseline for hypernym detection. When the relation is stated in many ways, or when the pairs must come from a small corpus, learned patterns or [distributional](/distributional-hypothesis/) methods find more pairs.

## Pitfalls

- **The wrong noun phrase before the trigger.** Lines L3 and L5 take the NP just before the trigger as the hypernym. In "[countries] with [large populations] , such as [India]", line L3 reports India as a kind of large populations, while the hypernym is "countries". Attach prepositional phrases to the NP before matching, or check the head of the larger phrase.
- **A left list that reads too far.** Line L6 reads NPs and commas to the left as far as it can. In "after [the storm] , [roads] , [bridges] and other [structures] were closed", it reports the storm as a kind of structure, since the comma after "the storm" ends a clause and not a list item. A chunker that marks clauses, or a limit on the list, helps.
- **Part of instead of kind of.** "Including" also introduces parts and members. In "[the kit] , including [a hammer] and [nails]", line L5 reports a hammer as a kind of kit. Check the pairs against a lexicon, or keep pattern 5 only for high-count pairs.
- **The list without its last comma.** A RIGHT-LIST that does not accept ", CONJ NP" stops before "Spain" in the example above, and loses the last item of every list written with a serial comma. Accept both "CONJ NP" and ", CONJ NP".
- **Full phrases as the pair.** The output pairs are noun phrases such as "important civic buildings". A lexicon has "building". Reduce each NP to its lemmatized head noun before comparing it with a lexicon, as Hearst did for the WordNet check.

## Implementations

## History

Hearst 1992 presented the patterns at COLING as a way to acquire hyponyms from text with no pre-encoded knowledge, and to check and extend hand-built lexicons. She found the six patterns by hand, partly with the procedure above, and noted that she had not implemented an automatic version. The patterns became a standard baseline for hypernym detection and a common way to seed taxonomies, and later work learned more patterns from data.

## References
