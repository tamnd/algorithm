---
tag: DB4AFE
kind: algorithm
slug: unicode-text-segmentation
name: Unicode text segmentation
aliases:
- UAX 29
- grapheme cluster boundaries
- Unicode word boundaries
area: strings/text-processing-and-typesetting
level: core
summary: "Find grapheme cluster, word and sentence boundaries with the ordered rules of UAX 29 on break properties. Some rules look at long contexts on both sides of a position."
model: word-ram
complexity:
  vars: {n: the length of the text in code points}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [extended-grapheme-cluster, unicode-code-point]
see_also: [text-segmentation, unicode-line-breaking-algorithm, deterministic-finite-automaton, regular-expression, finite-state-transducer, unicode-normalization-algorithm]
sources:
  - url: https://www.unicode.org/reports/tr29/tr29-45.html
    title: "Josh Hadley (editor), Unicode Standard Annex 29, Unicode Text Segmentation, revision 45, 2024-08-28"
    locator: "Sections 3.1.1 (grapheme rules GB1 to GB999), 4.1 and 4.1.1 (word rules WB1 to WB999), 5.1 and 5.1.1 (sentence rules SB1 to SB998), 6.2 (Replacing Ignore Rules), 6.3 (State Machines) and 7 (Testing)"
  - url: https://www.unicode.org/Public/16.0.0/ucd/auxiliary/
    title: "Unicode Character Database 16.0.0, auxiliary folder"
    locator: "GraphemeBreakProperty.txt, WordBreakProperty.txt, SentenceBreakProperty.txt and the test files GraphemeBreakTest.txt, WordBreakTest.txt and SentenceBreakTest.txt"
  - url: https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-data.txt
    title: "emoji-data-16.0.0.txt, Unicode Character Database"
    locator: the Extended_Pictographic property
  - book: isbn:9781936213344
    title: "The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024"
    locator: "Chapter 3, definitions D60 and D61 (grapheme clusters as defined by UAX 29)"
---

Unicode text segmentation finds the boundaries of grapheme clusters, words and sentences in a string of [code points](/unicode-code-point/), with the rules of Unicode Standard Annex 29 (UAX 29). Each code point has a break property, such as GCB=Extend for a combining mark or WB=Numeric for a digit. At each position between two code points, a fixed list of rules is tried in order, and the first rule that matches says boundary or no boundary. This is a rule system over character properties. It is a different problem from [text segmentation by dynamic programming](/text-segmentation/), which splits a text without spaces into dictionary words. UAX 29 uses no dictionary, so its default word rules do not split Thai or Chinese into words.

## In plain words

A program must often cut text into pieces: the characters that a cursor moves over, the words that a double click selects, the sentences that a reader sees. In English, spaces and full stops do most of the work, but they are not enough. An accent can be a separate code point that must stay with its letter. A flag is two code points. "3.14" is one word, but "end.Next" is not one word. A full stop after "Mr" is not always the end of a sentence.

Unicode gives each character a few labels. For each kind of piece, it gives an ordered list of rules. Each rule looks at the labels on both sides of a gap and says "cut" or "do not cut". At each gap, the first rule that fits decides. Some rules look a long way back, for example to count flag letters.

## The problem

The input is a string $s$ of $n$ code points. A boundary is a position $b$ with $0 \le b \le n$, the place between $s[b-1]$ and $s[b]$. The output, for each of the three kinds of segments, is the sorted list of boundaries. Position 0 and position $n$ are always boundaries of a non-empty string (rules GB1 and GB2, WB1 and WB2, SB1 and SB2).

The properties are Grapheme_Cluster_Break (GCB), Word_Break (WB) and Sentence_Break (SB), from the files GraphemeBreakProperty.txt, WordBreakProperty.txt and SentenceBreakProperty.txt, plus Indic_Conjunct_Break (InCB) and Extended_Pictographic (ExtPict). Each rule has the form "left × right" or "left ÷ right", where left and right are regular expressions over property values. The left side must match a suffix of $s[0 \ldots b-1]$ and the right side a prefix of $s[b \ldots n-1]$. The rule numbers give the order, and the first rule that matches at $b$ decides. A short summary of the three lists:

- **Grapheme clusters, GB1 to GB999.** No boundary inside CR LF (GB3), boundaries around other controls (GB4, GB5), none inside Hangul syllables (GB6 to GB8), none before Extend, ZWJ and SpacingMark or after Prepend (GB9, GB9a, GB9b), none inside Indic conjuncts (GB9c), none inside emoji ZWJ sequences (GB11), and regional indicators in pairs (GB12, GB13). The [extended grapheme cluster](/extended-grapheme-cluster/) page lists them in full.
- **Words, WB1 to WB999.** WB4 says that Extend, Format and ZWJ are ignored after any code point except sot, CR, LF and Newline: the rule "X (Extend | Format | ZWJ)* → X" makes the rest of the rules see the sequence without them. Then letters stay together (WB5), letters stay together across one MidLetter or MidNumLetQ such as the apostrophe in "can't" (WB6, WB7), digits stay together across one MidNum or MidNumLetQ such as "3.14" (WB11, WB12), letters and digits stay together (WB8 to WB10), and so on. Here AHLetter = (ALetter | Hebrew_Letter) and MidNumLetQ = (MidNumLet | Single_Quote).
- **Sentences, SB1 to SB998.** SB4 puts a boundary after each paragraph separator, SB5 ignores Extend and Format, and the main rules are about terminators: ATerm is the full stop, STerm the other terminators. SB8 says "ATerm Close* Sp* × (¬(OLetter | Upper | Lower | ParaSep | SATerm))* Lower": no boundary after a full stop if the next letter is lowercase. SB11 says "SATerm Close* Sp* ParaSep? ÷": otherwise a boundary after the terminator, its closing punctuation and its spaces. The last rule SB998 is "Any × Any", so a sentence boundary is the exception.

Several rules are not pairwise. GB9c, GB11 and GB12 look an unbounded way to the left, WB6 and WB12 look one code point to the right past the next one, and SB8 looks an unbounded way to the right.

## The algorithm

The rules are evaluated at each position from left to right. A direct evaluation of the left-hand regular expressions at each position would cost $O(n)$ per position. Instead, the algorithm keeps a few counters and flags that summarize the text to the left, in the spirit of the state machines of UAX 29 section 6.3. For grapheme clusters three are enough: the number $ri$ of regional indicators that end at the position, a flag $pict$ that says whether the text ends with ExtPict Extend* before the last code point, and the state $conj$ of the conjunct rule GB9c.

```pseudo id=main
GRAPHEME-BOUNDARIES(s)                     ▷ s has n >= 1 code points
L1  B <- [0]; ri <- 0; ep <- false; pict <- false; conj <- none
L2  for i <- 1 to n - 1 do
L3      a <- GCB(s[i-1]); b <- GCB(s[i])
L4      update pict, ep, ri and conj with s[i-1]          ▷ see the rules below
L5      if a = CR and b = LF then x <- false                          ▷ GB3
L6      else if a or b is in {Control, CR, LF} then x <- true          ▷ GB4, GB5
L7      else if (a, b) is a Hangul pair of GB6, GB7 or GB8 then x <- false
L8      else if b in {Extend, ZWJ, SpacingMark} or a = Prepend then x <- false   ▷ GB9, GB9a, GB9b
L9      else if conj = linked and InCB(s[i]) = Consonant then x <- false ▷ GB9c
L10     else if pict and a = ZWJ and ExtPict(s[i]) then x <- false     ▷ GB11
L11     else if a = b = RI and ri is odd then x <- false               ▷ GB12, GB13
L12     else x <- true                                                 ▷ GB999
L13     if x then append i to B
L14 append n to B
L15 return B
```

The update of line L4, with $c = s[i-1]$:

- $pict \leftarrow ep$, then $ep \leftarrow \mathrm{ExtPict}(c)$ or ($ep$ and GCB($c$) = Extend). So $ep$ says that $s[0 \ldots i-1]$ ends with ExtPict Extend*, and $pict$ says the same of $s[0 \ldots i-2]$. With $a$ = ZWJ, the left side of GB11 matches exactly when $pict$ holds.
- $ri \leftarrow ri + 1$ if GCB($c$) = RI, else $ri \leftarrow 0$.
- $conj \leftarrow$ consonant if InCB($c$) = Consonant; $conj \leftarrow$ linked if InCB($c$) = Linker and $conj \ne$ none; $conj$ unchanged if InCB($c$) = Extend; $conj \leftarrow$ none otherwise.

Legacy grapheme clusters drop GB9a, GB9b and GB9c, so lines L8 and L9 lose those tests.

Word and sentence boundaries follow the same pattern. Their rules before WB4 and SB5 work on the raw code points. After them, the implementation finds the previous code point that is not ignored (walking back over Extend, Format and ZWJ for words, Extend and Format for sentences), and the next one, and tests the remaining rules on those. When the walk back reaches sot or a line or paragraph separator, the first ignored code point stands for itself, as WB4 and SB5 require.

## Example

Grapheme clusters of $s$ = U+0915 U+094D U+0937 U+093F U+1F1EB U+1F1F7 U+1F1E9 (the Devanagari syllable क्षि and three regional indicators), $n = 7$:

| $i$ | $s[i-1]$, $s[i]$ | GCB | state after L4 | rule | result |
|---|---|---|---|---|---|
| 1 | 0915, 094D | Other, Extend | conj = consonant | GB9 | × |
| 2 | 094D, 0937 | Extend, Other | conj = linked | GB9c | × |
| 3 | 0937, 093F | Other, SpacingMark | conj = consonant | GB9a | × |
| 4 | 093F, 1F1EB | SpacingMark, RI | conj = none, ri = 0 | GB999 | ÷ |
| 5 | 1F1EB, 1F1F7 | RI, RI | ri = 1 | GB12 | × |
| 6 | 1F1F7, 1F1E9 | RI, RI | ri = 2 | GB999 | ÷ |

The boundaries are 0, 4, 6 and 7: the syllable, the French flag, and a lone regional indicator. The legacy rules give 0, 2, 3, 4, 6 and 7.

Words in "can't 3.14 a_b": the boundaries are 0, 5, 6, 10, 11 and 14, so the segments are "can't", " ", "3.14", " " and "a_b". The apostrophe U+0027 is WB=Single_Quote, part of MidNumLetQ, so WB6 and WB7 keep "can't" together. WB11 and WB12 keep "3.14". U+005F LOW LINE is WB=ExtendNumLet, and WB13a and WB13b keep "a_b". A program that wants only the words drops the segments of spaces and punctuation.

Sentences in "The U.S. team won. it is 3.5 km." form one sentence: after "won." the next letter is lowercase, so SB8 forbids a boundary. In `Mr. Smith said: "Go." Then he left.` the boundaries are 0, 4, 22 and 35, and the first sentence is "Mr. ", because the default rules do not know abbreviations.

## Correctness

For each kind of boundary, the claim is that the procedure returns exactly the positions where the first matching rule of UAX 29 is a ÷ rule. For grapheme clusters, an induction on $i$ shows that after line L4 the variables describe the left context: $ri$ is the number of RI code points at the end of $s[0 \ldots i-1]$, $pict$ is true exactly when $s[0 \ldots i-2]$ ends with ExtPict Extend*, and $conj$ is linked exactly when $s[0 \ldots i-1]$ matches the left side of GB9c. With these facts, each line from L5 to L12 is true exactly when its rule matches, and the order of the lines is the order of the rules. The full proof is in proofs/correctness.md. The implementation is also tested on quoted lines of the three conformance files and against a brute-force evaluation of the grapheme rules as regular expressions.

## Complexity

In the [word-RAM model](/word-ram/), a property lookup is $O(1)$: a table indexed by code point, or a binary search over a fixed number of ranges. The constant is large in practice, and real implementations use two-stage tables.

- **Grapheme clusters.** GRAPHEME-BOUNDARIES does $O(1)$ work per position, so it takes $\Theta(n)$ time and $O(1)$ extra space besides the output.
- **Words and sentences.** All left contexts of the rules are regular languages, and the right contexts are regular too. UAX 29 section 6.3 notes that the rules can be compiled into state machines. With counters for the RI run, the run of ignored code points and the chain SATerm Close* Sp*, and one backward pass that records for each position whether the next letter after it is Lower (for SB8), the time is $\Theta(n)$. The direct code in the implementation walks back over runs and forward for SB8 at each position, which is $O(n^2)$ in the worst case, for example on a long run of spaces after a full stop.
- **Space.** $O(1)$ extra for the state, $O(n)$ for the property array if it is stored.

| claim | value |
|---|---|
| grapheme boundaries | $\Theta(n)$ time, $O(1)$ extra space |
| word and sentence boundaries with state | $\Theta(n)$ time |
| direct evaluation of the rules at each position | $O(n^2)$ time |

## Properties

- **First match wins.** The rules are an ordered list, not a set. Changing the order changes the result: GB4 before GB9 puts a boundary between LF and a combining mark.
- **Not a pair table.** The decision at a position can depend on text far away: on the parity of a run of regional indicators (GB12, GB13, WB15, WB16), on a conjunct (GB9c), or on the next letter after any amount of punctuation (SB8).
- **Independent rule sets.** Word boundaries are not always grapheme cluster boundaries. In U+0061 U+1F1E6 U+200D U+1F1E7 U+1F1E8 U+0062, the word rules ignore the ZWJ and pair U+1F1E6 with U+1F1E7, so position 4 is a word boundary, but the grapheme rules end a cluster after the ZWJ and pair U+1F1E7 with U+1F1E8.
- **Default rules.** These are the default boundaries. UAX 29 allows tailoring, for example dictionary-based word breaking for Thai, or a list of abbreviations for sentences.
- **Stable over versions in spirit, not in detail.** New characters and new rules change results: GB9c is new in Unicode 15.1, and the emoji rules changed several times.

## Variants and improvements

- **State machines and regular expressions.** UAX 29 section 6.3 describes the compilation of the rules into a state machine, a [deterministic finite automaton](/deterministic-finite-automaton/) over property values. ICU builds its break iterators from rule files in this way. A [regular expression](/regular-expression/) engine with \X matches one extended grapheme cluster.
- **Replacing the ignore rules.** Section 6.2 shows how to rewrite WB4 and SB5 into rules that do not need the "X Extend* → X" step, which makes the rules pairwise in more places.
- **Backward and random access.** Editors need the boundary before or after a given offset. Starting at an arbitrary offset needs a safe starting point; the annex discusses this in its implementation notes.
- **Tailoring.** CLDR adds language rules, for example suppressions for sentence breaks after common abbreviations. Dictionary-based word breaking for languages without spaces is a separate method; see [text segmentation by dynamic programming](/text-segmentation/).

## When to use it

Use grapheme clusters for anything a user sees as one character: cursor movement, deletion, selection, and the truncation of a string for display. Never cut a string for display at an arbitrary code point or byte offset. Use the word rules for double-click selection, "whole word" search and word counts in languages with spaces. Use the sentence rules as a first pass, and add tailoring for abbreviations when the result matters. For line wrapping, use the [line breaking algorithm](/unicode-line-breaking-algorithm/) instead: word boundaries are not line break opportunities.

## Pitfalls

- **Pairwise tables.** A table indexed by the properties of the two neighbours gets GB12, GB13 and GB9c wrong. The test `test_grapheme_conformance_lines` has regional indicator lines that catch this.
- **The exceptions of WB4 and SB5.** An Extend code point after LF or at the start of the text is not ignored. The line `÷ 000D × 000A ÷ 0061 ÷ 000A ÷ 0308 ÷` checks this for graphemes, and the sentence line `÷ 2060 × 0061 × 2060 × 002E × 2060 × 000D ÷ 2060 × 000A ÷ 2060 ÷` checks it for sentences.
- **Old data.** GB9c is new in Unicode 15.1. Code written for older versions splits Devanagari conjuncts. The check `test_legacy_clusters_differ` shows the difference.
- **Counting characters with len.** In Python, len counts code points; in Java and JavaScript, the length counts UTF-16 code units. Neither is the number of grapheme clusters.
- **Abbreviations.** The default sentence rules end a sentence after "Mr." followed by an uppercase letter. This is expected behaviour, not a bug of the implementation.
- **Words as dictionary words.** The default word rules do not split "日本語" into words; they need a dictionary.

## Implementations

## History

UAX 29 gets a new revision with each version of the Unicode Standard, and the rules change with the character repertoire. The annex keeps the legacy form of grapheme clusters for compatibility with older implementations. The emoji rules changed several times, and the current GB11 uses the Extended_Pictographic property. GB9c for Indic conjuncts, with the new property Indic_Conjunct_Break, came in Unicode 15.1 (2023). Revision 45 is the version for Unicode 16.0.0.

## References
