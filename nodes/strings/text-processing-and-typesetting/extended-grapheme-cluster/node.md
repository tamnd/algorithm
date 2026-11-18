---
tag: EFGEH8
kind: definition
slug: extended-grapheme-cluster
name: Extended grapheme cluster
aliases:
- grapheme cluster
- user-perceived character
area: strings/text-processing-and-typesetting
level: core
summary: "The text between two boundaries of the UAX 29 grapheme rules, which a reader sees as one character, such as a letter with combining marks or an emoji ZWJ sequence."
prereqs: [unicode-code-point]
see_also: [unicode-text-segmentation, canonical-equivalence, unicode-normalization-forms, unicode-line-breaking-algorithm, utf-16, alphabet]
sources:
  - url: https://www.unicode.org/reports/tr29/tr29-45.html
    title: "Josh Hadley (editor), Unicode Standard Annex 29, Unicode Text Segmentation, revision 45, 2024-08-28"
    locator: Section 3 Grapheme Cluster Boundaries (the legacy and extended forms) and Section 3.1.1 Grapheme Cluster Boundary Rules (GB1 to GB999)
  - book: isbn:9781936213344
    title: "The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024"
    locator: "Chapter 3, definitions D56 (combining character sequence), D58 (grapheme base), D59 (grapheme extender), D60 (grapheme cluster) and D61 (extended grapheme cluster)"
  - url: https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakProperty.txt
    title: "GraphemeBreakProperty-16.0.0.txt, Unicode Character Database"
    locator: the values of the Grapheme_Cluster_Break property
  - url: https://www.unicode.org/Public/16.0.0/ucd/auxiliary/GraphemeBreakTest.txt
    title: "GraphemeBreakTest-16.0.0.txt, Unicode Character Database"
    locator: the test lines for extended grapheme cluster boundaries
---

An extended grapheme cluster is a run of [code points](/unicode-code-point/) that a reader sees as one character: a letter with its accents, a Korean syllable written as three jamo, a flag made of two regional indicator symbols, or an emoji made of several emoji joined by U+200D ZERO WIDTH JOINER. Unicode Standard Annex 29 defines it by a list of rules that say where a boundary is. Cursor movement, deletion with the backspace key, text selection and the truncation of strings for display should work in whole clusters, not in code points or bytes. In this encyclopedia, "grapheme cluster" alone means the extended form.

## Definition

Let $s$ be a string of $n$ code points. A position $b$ with $0 \le b \le n$ is the place between $s[b-1]$ and $s[b]$. Each code point $c$ has a value of the property Grapheme_Cluster_Break (GCB), for example GCB=Extend for most combining marks and GCB=Regional_Indicator for the flag letters. The rules also use the properties Indic_Conjunct_Break (InCB) and Extended_Pictographic (ExtPict). The values are in the files GraphemeBreakProperty.txt, DerivedCoreProperties.txt and emoji-data.txt of the Unicode Character Database.

**Grapheme cluster boundary.** UAX 29 section 3.1.1 gives the rules GB1 to GB999. For each position, the first rule that matches the text around it decides: ÷ means a boundary and × means no boundary. GB1 and GB2 put a boundary at the start and at the end of the text, and GB999 puts a boundary everywhere else that no earlier rule covers. The rules between them forbid a boundary in these places:

- inside CR LF (GB3), but there is a boundary on each side of every other control character, CR and LF (GB4, GB5);
- inside a Hangul syllable written with conjoining jamo (GB6, GB7, GB8);
- before GCB=Extend and GCB=ZWJ (GB9), before GCB=SpacingMark (GB9a) and after GCB=Prepend (GB9b);
- between two consonants of an Indic conjunct, \p{InCB=Consonant} [\p{InCB=Extend}\p{InCB=Linker}]* \p{InCB=Linker} [\p{InCB=Extend}\p{InCB=Linker}]* × \p{InCB=Consonant} (GB9c);
- inside an emoji ZWJ sequence, \p{ExtPict} Extend* ZWJ × \p{ExtPict} (GB11);
- inside a pair of regional indicators: an odd number of RI before the position and one RI after it (GB12, GB13).

**Extended grapheme cluster.** The text between two adjacent grapheme cluster boundaries (D61 in the core specification, which refers to UAX 29). The clusters of $s$ are $s[b_0 \ldots b_1 - 1], s[b_1 \ldots b_2 - 1], \ldots$ for the boundaries $0 = b_0 < b_1 < \cdots < b_k = n$. The empty string has no clusters, and a non-empty string has at least one.

**Legacy grapheme cluster.** The same definition without the rules GB9a, GB9b and GB9c. Legacy clusters exist for compatibility with old implementations. They split some Indic syllables that readers see as one unit. Definition D60 of the core specification defines a grapheme cluster as the text between grapheme cluster boundaries of UAX 29, and D61 defines the extended form in the same way.

The computation of the boundaries is on the page [Unicode text segmentation](/unicode-text-segmentation/), with the rules in order, a trace and an implementation.

## Examples and non-examples

These examples use the property values of Unicode 16.0.0. Lengths are in code points.

| text | code points | clusters | rule |
|---|---|---|---|
| é (decomposed) | U+0065 U+0301 | 1 | GB9, U+0301 is GCB=Extend |
| CR LF | U+000D U+000A | 1 | GB3 |
| 각 (decomposed) | U+1100 U+1161 U+11A8 | 1 | GB6 then GB7 (GCB=L, V, T) |
| family emoji | U+1F468 U+200D U+1F469 U+200D U+1F467 | 1 | GB9 and GB11 |
| two flags | U+1F1EB U+1F1F7 U+1F1E9 U+1F1EA | 2 | GB12 and GB13 pair the RI code points |
| क्षि | U+0915 U+094D U+0937 U+093F | 1 | GB9 for U+094D, GB9c for U+0937, GB9a for U+093F |

- The French flag and the German flag above are 4 code points and 2 clusters. A cut after the first or the third code point breaks a flag into two letters that show as boxes or as letters in a frame.
- U+0915 U+094D U+0937 U+093F is 1 extended cluster but 3 legacy clusters: क्, ष and ि. The legacy rules have a boundary before U+0937, because GB9c is missing, and a boundary before the vowel sign U+093F, because GB9a is missing. GB9c is new in Unicode 15.1.
- Not a cluster: a lone U+0301 after U+000A. GB4 puts a boundary after the LF, so the mark starts a cluster of its own, a "defective" combining sequence.
- A cluster is not the same as a code point or a UTF-16 code unit. "é" in the decomposed form is 2 code points, 2 UTF-16 code units, 3 bytes in UTF-8, and 1 cluster. The family emoji is 5 code points, 8 UTF-16 code units, 18 bytes in UTF-8 and 1 cluster.
- A cluster is not a glyph. A font can draw one cluster with several glyphs, or a ligature such as "fi" as one glyph for two clusters.

## Related definitions

- **Combining character sequence (D56).** A base character followed by combining characters. An extended grapheme cluster is a larger unit: it also covers Hangul syllables, emoji sequences, flags and Indic conjuncts.
- **Grapheme base and grapheme extender (D58, D59).** The properties Grapheme_Base and Grapheme_Extend. GCB=Extend contains the code points with Grapheme_Extend and the emoji modifiers U+1F3FB..U+1F3FF.
- **Canonical equivalence.** Most combining marks, and all marks with gc=Mn (Nonspacing_Mark) or gc=Me (Enclosing_Mark), have GCB=Extend, so a cluster keeps a base letter together with the marks that [canonical equivalence](/canonical-equivalence/) can reorder or compose. U+00E9 and U+0065 U+0301 are both one cluster.
- **Word and sentence boundaries.** The same annex defines them with other rules, on [Unicode text segmentation](/unicode-text-segmentation/). They mostly fall on cluster boundaries, but not always.
- **Line break opportunities.** The [line breaking algorithm](/unicode-line-breaking-algorithm/) has its own classes. Its rule LB9 keeps combining marks with their base, as the cluster rules do.
- **Code point and code unit.** The [code point](/unicode-code-point/) is the unit of the rules. A program that counts [UTF-16](/utf-16/) code units counts something else again.
- **Alphabet.** In the theory of strings, a string is a sequence over an [alphabet](/alphabet/). For Unicode text the alphabet is the set of code points. Clusters are not a fixed alphabet, because their number is not bounded.

## References
