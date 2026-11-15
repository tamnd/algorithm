---
tag: MAYHA4
kind: algorithm
slug: porter-stemmer
name: Porter stemmer
aliases:
- Porter stemming algorithm
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Removes English suffixes in five rule phases, each rule guarded by a condition on the measure of the remaining stem.
model: word-ram
complexity:
  vars: {n: the number of letters of the word}
  time: {worst: O(n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, comparison: false, recursive: false}
prereqs: [stemming]
see_also: [stop-word-removal, inverted-index, k-gram-index, soundex, edit-distance, noisy-channel-spelling-correction]
sources:
  - paper: doi:10.1108/eb046814
    title: Martin F. Porter, An algorithm for suffix stripping, Program 14(3), 130 to 137, 1980
    locator: Section 2, The algorithm (the definitions of consonant, vowel and the measure m, the conditions *S, *v*, *d and *o, the rule of the longest matching suffix, Steps 1a to 5b with their examples, and the counts of words reduced in each step for a vocabulary of 10,000 words)
  - paper: "Martin Porter, The Porter Stemming Algorithm, web page at tartarus.org/martin/PorterStemmer"
    locator: the note on the points where the ANSI C and BCPL versions depart from the published algorithm (the rule LOGI to LOG, the rule BLI to BLE in place of ABLI to ABLE, and words of length 1 or 2 left alone)
  - paper: "Martin Porter, The English (Porter2) stemming algorithm, web page at snowballstem.org/algorithms/english/stemmer.html"
    locator: the list of points where Porter2 departs from the 1980 algorithm, and the statement that the two stem slightly over 5 percent of the words of the sample vocabulary differently
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 2, Section 2.2.4 (stemming and lemmatization, the five phases of the Porter stemmer, the rule SSES to SS, the measure condition, and the comparison with the Lovins and Paice stemmers)
---

The Porter stemmer is a rule-based algorithm that maps an English word to a stem by removing its suffixes in five steps, so that words such as "connected", "connecting" and "connections" all map to "connect". Each rule has the form (condition) S1 → S2: if the word ends with S1 and the part before S1 meets the condition, S1 is replaced by S2. Most conditions test the *measure* $m$ of that part, a count of its vowel-consonant sequences, so that a suffix is removed only from a stem that is long enough. Martin Porter published it in 1980 as one algorithm for the technique of [stemming](/stemming/), and it is still the standard English stemmer of information retrieval.

## In plain words

Many English words share one root and differ only in their end: "hope", "hopeful", "hopefulness". A search for one form should usually find the others. The Porter stemmer cuts the end of a word in a fixed order of steps. The first step handles plurals and the endings "-ed" and "-ing". The middle steps turn long endings such as "-ational" or "-iveness" into shorter ones, or drop them. The last step removes a final "e" and one of two final "l" letters.

Each cut has a test. The part of the word that stays must be long enough, counted in groups of vowels followed by consonants. So one step turns "relational" into "relate", but "rational" keeps its "-ational", because "r" alone is too short. The result does not need to be a real word: "ponies" becomes "poni".

## The problem

**Input.** A word $w$ of lower case letters a to z.

**Output.** A string, the *stem* of $w$, such that words with the same root tend to get the same stem. Equal stems are what an [inverted index](/inverted-index/) uses: the index stores the stem in place of the word, and a query word is stemmed in the same way.

There is no exact specification of "the same root", so the algorithm is defined by its rules, and correctness means that the code does what the rules say. Porter gives these definitions.

- **Consonant and vowel.** A consonant is a letter other than a, e, i, o, u, and other than a y that follows a consonant. Every other letter is a vowel. In "toy" the consonants are t and y, and in "syzygy" they are s, z and g.
- **Measure.** Write C for a nonempty run of consonants and V for a nonempty run of vowels. Every string has the form $[C](VC)^m[V]$, where square brackets mean that the part may be missing. The number $m$ is the *measure*. For example $m = 0$ for "tr", "ee", "tree", "y", "by"; $m = 1$ for "trouble", "oats", "trees", "ivy"; $m = 2$ for "troubles", "private", "oaten", "orrery".
- **Conditions on the stem** $v$, the part before S1: $(m > k)$ and $(m = k)$ test the measure of $v$; \*S means $v$ ends with s (and so for every letter); \*v\* means $v$ contains a vowel; \*d means $v$ ends with a double consonant, such as tt or ss; \*o means $v$ ends consonant, vowel, consonant, and the last consonant is not w, x or y, as in "hop" or "wil".
- **One rule per step.** In each step, the rule with the longest S1 that ends the word is the only candidate. If its condition fails, the step does nothing; the step does not try a shorter S1.

## The algorithm

```pseudo id=main
PORTER-STEM(w)                       ▷ w is a word of lower case letters
L1  for each step s in 1a, 1b, 1c, 2, 3, 4, 5a, 5b, in this order do
L2      R ← the rule (C) S1 → S2 of step s with the longest S1 that ends w
L3      if there is no such rule then go on to the next step
L4      v ← w without its last |S1| letters               ▷ the stem before S1
L5      if C holds for v then
L6          w ← v · S2
L7          if s = 1b and S1 is "ed" or "ing" then w ← TIDY-1B(w)
L8  return w

TIDY-1B(w)                           ▷ after "ed" or "ing" is removed
L9   if w ends with "at", "bl" or "iz" then return w · "e"
L10  if w ends with a double consonant other than l, s or z then return w without its last letter
L11  if MEASURE(w) = 1 and w ends consonant, vowel, consonant (not w, x, y) then return w · "e"
L12  return w

MEASURE(v)
L13  m ← 0
L14  for i ← 1 to |v| - 1: if letter i of v is a vowel and letter i + 1 is a consonant then m ← m + 1
L15  return m
```

These are the rules of the paper, with Porter's own examples of what each step does to a word.

| step | rules | examples |
|---|---|---|
| 1a | sses → ss, ies → i, ss → ss, s → (none) | caresses → caress, ponies → poni, ties → ti, caress → caress, cats → cat |
| 1b | (m > 0) eed → ee, (\*v\*) ed → (none), (\*v\*) ing → (none) | feed → feed, agreed → agree, plastered → plaster, bled → bled, motoring → motor, sing → sing |
| 1b, tidy | at → ate, bl → ble, iz → ize, (\*d and not (\*L or \*S or \*Z)) → one letter less, (m = 1 and \*o) → add e | conflated → conflate, troubled → trouble, sized → size, hopping → hop, tanned → tan, falling → fall, hissing → hiss, fizzed → fizz, failing → fail, filing → file |
| 1c | (\*v\*) y → i | happy → happi, sky → sky |
| 2 | all (m > 0): ational → ate, tional → tion, enci → ence, anci → ance, izer → ize, abli → able, alli → al, entli → ent, eli → e, ousli → ous, ization → ize, ation → ate, ator → ate, alism → al, iveness → ive, fulness → ful, ousness → ous, aliti → al, iviti → ive, biliti → ble | relational → relate, conditional → condition, rational → rational, digitizer → digitize, callousness → callous, sensibiliti → sensible |
| 3 | all (m > 0): icate → ic, ative → (none), alize → al, iciti → ic, ical → ic, ful → (none), ness → (none) | triplicate → triplic, formative → form, electrical → electric, hopeful → hope, goodness → good |
| 4 | all (m > 1): al, ance, ence, er, ic, able, ible, ant, ement, ment, ent, ou, ism, ate, iti, ous, ive, ize → (none); (m > 1 and (\*S or \*T)) ion → (none) | revival → reviv, airliner → airlin, replacement → replac, adjustment → adjust, adoption → adopt, effective → effect |
| 5a | (m > 1) e → (none), (m = 1 and not \*o) e → (none) | probate → probat, rate → rate, cease → ceas |
| 5b | (m > 1 and \*d and \*L) → one letter less | controll → control, roll → roll |

**Walk-through.** Line L2 finds the candidate rule of a step by the longest match: "caresses" ends with both "sses" and "s", and the rule sses → ss wins. Lines L4 and L5 test the condition on the stem $v$, not on the whole word: in step 4, "replacement" has $v$ = "replac" with $m = 2$, so "ement" goes. If the condition fails, the step leaves $w$ alone: "feed" ends with "eed", its stem "f" has $m = 0$, and the rule (\*v\*) ed is not tried. Line L7 runs the second part of step 1b only after "ed" or "ing" was removed. That part puts back an "e" that the suffix took ("conflat" → "conflate"), undoes a doubled consonant ("hopp" → "hop"), or adds "e" to a short stem that ends like "fil" ("fil" → "file"). The two rules of step 5a share S1 = "e" and form one rule whose condition is the "or" of the two.

## Example

The state after each step, for eight words.

| word | 1a | 1b | 1c | 2 | 3 | 4 | 5a | 5b |
|---|---|---|---|---|---|---|---|---|
| caresses | caress | | | | | | | |
| ponies | poni | | | | | | | |
| hopping | | hop | | | | | | |
| happy | | | happi | | | | | |
| relational | | | | relate | | | relat | |
| connections | connection | | | | | connect | | |
| generalizations | generalization | | | generalize | general | gener | | |
| oscillators | oscillator | | | oscillate | | oscill | | oscil |

An empty cell is a step that did nothing. "Relational" shows that a word can lose parts of its suffix in several steps: Porter's example "relational → relate" is the effect of step 2 only, and the stem is "relat". The chains for "generalizations" and "oscillators" are the ones Porter gives in the paper.

**On the toy collection.** The 50 distinct terms of the toy collection of the information retrieval pages give 46 stems. Four pairs merge: "document" and "documents", "list" and "lists", "merge" and "merges", "sort" and "sorted". So the query word "documents" of $q_3$ now matches "document" in $d_4$, and the index entry for "list" also holds $d_5$, which has "lists" and is the most relevant document for $q_2$. Without stemming, neither of these words matches anything in those documents.

## Correctness

**Claim.** For every word $w$ of lower case letters, PORTER-STEM returns the string that the rules of Porter (1980) give: steps 1a to 5b in order, in each step only the rule with the longest matching S1, applied if and only if its condition holds for the stem.

The key facts are two. First, MEASURE counts the positions where a vowel is followed by a consonant, and in the form $[C](VC)^m[V]$ these are exactly the $m$ boundaries between a V and the C after it. Second, the consonant status of a letter depends only on the letters before it, so the status of the letters of a stem $v$ is the same in $v$ as in $w$, and the conditions can be evaluated on $v$ alone. With these, each step is a direct reading of the rule of the longest match. The full proof is in the proof file below.

## Complexity

- **Time, $O(n)$.** There are eight steps. Each one tests at most 21 suffixes of at most 7 letters, which is $O(1)$ work. The condition reads the stem once: MEASURE and the tests \*v\*, \*d and \*o are each one scan of at most $n$ letters. TIDY-1B does at most three such scans. So each step costs $O(n)$, and the whole word $O(n)$. Every word is read at least once, so the bound is also the best case.
- **Space, $O(n)$.** The stem and the table of consonant flags have at most $n$ entries. The rule tables have fixed size.
- **For a collection.** An indexer stems each distinct term once and keeps the result in a [hash table](/hash-table/), so the cost is linear in the length of the vocabulary, not of the text.

## Properties

- **Shorter or equal.** Every S2 is shorter than its S1 or as long, and TIDY-1B adds back at most one letter after removing at least two, so the stem has at most $n$ letters.
- **Not idempotent.** A stem can be stemmed again to a different stem: "agreed" gives "agre", and "agre" gives "agr". Stem the words of the text and the query once each, never a stored stem.
- **No dictionary.** The rules look only at letters, so the stems need not be words ("poni", "happi") and the stemmer works on new words. The measure prevents many errors: "wander" keeps its "er" because "wand" has $m = 1$, so it does not join "wand". But a letter rule cannot see meaning, so some words of one root stay apart ("probe" gives "probe" and "probate" gives "probat") and some unrelated words share a stem.
- **A remark in the paper that the rules do not meet.** Porter writes that RELATE and RELATIVITY are conflated by his algorithm. By the printed rules, "relate" gives "relat" (step 5a) and "relativity" gives "rel" (steps 1c, 2 and 3), so they are not.
- **English only.** The suffixes and the measure are for English. Other languages need their own rules.

## Variants and improvements

- **The definitive version.** Porter's ANSI C and BCPL code, which he calls the definitive version, departs from the paper in three points: it adds the step 2 rule (m > 0) logi → log, so "archaeology" and "archaeological" both give "archaeolog"; it replaces (m > 0) abli → able by (m > 0) bli → ble, so "possibly" and "possible" both give "possibl"; and it leaves words of one or two letters alone, so "as" and "is" keep their s. The code below supports both versions. In both, it reads \*d as the paper defines it, with both letters consonants; Porter's C code tests only the last letter, which gives a different answer only for a stem that ends with yy.
- **Porter2.** Porter's later English stemmer in the Snowball language replaces the measure by regions of the word, leaves words of length 2 alone, removes the suffix "ly" and a few others, and has a short list of exceptions. On the sample vocabulary of the Snowball site, Porter and Porter2 give different stems for slightly over 5 percent of the words.
- **Other suffix strippers.** The Lovins stemmer removes the longest ending from a long list in one pass and then repairs the stem with transformation rules; the Paice/Husk stemmer applies rules from a table iteratively. See [stemming](/stemming/) for the comparison.

## When to use it

Use it when the collection is English text, the queries are short, and the engine should match the inflected and derived forms of a query word without a dictionary. It is fast, has no data files, and its errors are well known. Manning, Raghavan and Schuetze report that stemming increases recall and harms precision, and that for English it helps some queries and hurts others, so the total gain is small; measure it on the target collection. For a lemma that is a real dictionary word, or for languages with rich inflection, use a lemmatizer or a stemmer written for that language. For index size alone, [front coding](/front-coding/) and other dictionary compression do not change the answers at all.

## Pitfalls

- **Falling through to a shorter suffix.** At line L5 a failed condition must end the step. If the code goes on to the next rule with a shorter S1, "feed" fails (m > 0) eed, then matches (\*v\*) ed with the stem "fe" and becomes "fe". The right code keeps only the rule of line L2 and leaves "feed" alone.
- **Running the tidy part every time.** Line L7 runs TIDY-1B only after "ed" or "ing" was removed. If it runs on every word, "hop" gets an "e" by line L11 and becomes "hope", and "bled", whose "ed" stays because "bl" has no vowel, becomes "blede".
- **Counting vowels instead of vowel-consonant pairs.** Line L14 counts a vowel only when a consonant follows it. If it counts every vowel, "tree" has a measure of 1 in place of 0, step 5a removes the e, and "tree" and "trees" become "tre".
- **Two different versions.** The paper rules and the definitive rules give different stems for words such as "possibly". An index built with one version and queried with the other misses matches. Fix one version for the index and the queries.
- **Input outside the precondition.** The rules assume lower case letters only. Fold case, and split or drop digits, apostrophes and hyphens, before the word reaches the stemmer.

## Implementations

## History

Julie Beth Lovins published an earlier stemmer in 1968. Porter wrote his algorithm in 1979 at the Computer Laboratory in Cambridge, as part of a larger IR project, and it appeared as Chapter 6 of the final project report by van Rijsbergen, Robertson and Porter before its publication in Program in 1980. In the paper he reports a test on the Cranfield 200 collection, where the new, simpler stemmer gave better retrieval than a much more elaborate program in use in IR research in Cambridge since 1971, and the effect of the rules on a vocabulary of 10,000 words: 3597 words were reduced in step 1, 766 in step 2, 327 in step 3, 2424 in step 4 and 1373 in step 5 (a word can be reduced in more than one step), 3650 were not reduced, and the result had 6370 distinct stems, about one third fewer than words. Porter later published the definitive C and BCPL versions and, in Snowball, the Porter2 stemmer.

## References
