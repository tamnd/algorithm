---
tag: TJBKG0
kind: definition
slug: canonical-equivalence
name: Canonical equivalence
aliases:
- Unicode canonical equivalence
area: strings/text-processing-and-typesetting
level: core
summary: "Two Unicode strings are canonically equivalent when their full canonical decompositions, with the combining marks in canonical order, are the same. Such strings show the same text."
prereqs: [unicode-code-point, equivalence-relation]
see_also: [unicode-normalization-forms, unicode-normalization-algorithm, hangul-syllable-composition, canonical-form, unicode-case-folding, unicode-confusable-detection, extended-grapheme-cluster, unicode-collation-algorithm]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3: Section 3.7 Decomposition (D62 to D70, 3.7.2 Canonical Decomposition), Section 3.11 Normalization Forms (3.11.2 Combining Classes, D104; 3.11.4 Starters, D107; 3.11.5 Canonical Ordering Algorithm, D108 and D109) and Section 3.12 Conjoining Jamo Behavior"
  - url: https://www.unicode.org/reports/tr15/
    title: Mark Davis and Ken Whistler, Unicode Standard Annex 15, Unicode Normalization Forms, revision 56
    locator: Section 1.1 (Canonical and Compatibility Equivalence) and Section 1.2 (Normalization Forms)
  - url: https://docs.python.org/3/library/unicodedata.html
    title: Python documentation, unicodedata
    locator: unicodedata.normalize, unicodedata.decomposition and unicodedata.combining
---

Canonical equivalence is the relation of Unicode that says when two different sequences of [code points](/unicode-code-point/) are the same text. The letter Å can be the one code point U+00C5, the letter A followed by the combining ring U+030A, or U+212B ANGSTROM SIGN, and all three are canonically equivalent. The standard defines the relation by a decomposition into the shortest building blocks and a fixed order of the combining marks, and programs that compare, search or index text must not treat equivalent strings as different. The [normalization forms](/unicode-normalization-forms/) NFC and NFD pick one string from each class.

## Definition

The definitions are from chapter 3 of the core specification of Unicode 16.0.0.

**Canonical decomposition mapping (D62).** Some characters have a decomposition mapping in the Unicode Character Database to a sequence of one or more characters. A mapping without a tag such as `<compat>` or `<font>` is canonical. For example, U+00E9 maps to U+0065 U+0301, U+212B maps to U+00C5, and U+0958 maps to U+0915 U+093C. The 11,172 Hangul syllables have canonical mappings given by the formula of [Hangul syllable composition](/hangul-syllable-composition/).

**Canonical combining class (D104).** Each code point has a number ccc in 0..254. Most characters, and all base letters, have class 0. A combining mark has a class that tells where it attaches: 220 for marks below, such as U+0323 COMBINING DOT BELOW, and 230 for marks above, such as U+0301 COMBINING ACUTE ACCENT and U+0307 COMBINING DOT ABOVE.

**Starter (D107).** A code point with class 0.

**Canonical ordering (D108, D109).** Two adjacent characters $A$, $B$ are a reorderable pair when $\mathrm{ccc}(A) > \mathrm{ccc}(B) > 0$. The canonical ordering algorithm exchanges reorderable pairs until none is left. The result is that each run of non-starters is sorted by class, and marks of the same class keep their order.

**Canonical decomposition (D68).** The result of applying the canonical mappings repeatedly, until no character can be decomposed further, and then putting the marks in canonical order. It is also called the full canonical decomposition, and it is the normalization form NFD.

**Canonical equivalence (D70).** Two sequences $s$ and $t$ are canonical equivalents when their full canonical decompositions are identical:

$$s \equiv t \iff \mathrm{NFD}(s) = \mathrm{NFD}(t).$$

Since the relation is defined by equality of a function value, it is an [equivalence relation](/equivalence-relation/), and $\mathrm{NFD}(s)$ is a [canonical form](/canonical-form/) for it. It is also a congruence for concatenation: if $s \equiv s'$ and $t \equiv t'$, then $st \equiv s't'$, because the decomposition of $st$ is the canonical ordering of the decompositions of $s$ and $t$ placed side by side.

The intent, as section 1.1 of UAX 15 explains, is that equivalent sequences stand for the same abstract characters and look and behave the same when they are shown correctly.

## Examples and non-examples

Each line gives the full canonical decomposition, checked with Python's `unicodedata.normalize("NFD", ...)` on data version 16.0.0.

- **A precomposed letter.** U+00E9 é and U+0065 U+0301 both decompose to 0065 0301, so they are equivalent.
- **A singleton.** U+212B ANGSTROM SIGN decomposes to U+00C5 and then to 0041 030A, so it is equivalent to U+00C5 and to A with a ring. In the same way U+2126 OHM SIGN is equivalent to U+03A9 GREEK CAPITAL LETTER OMEGA.
- **The order of marks of different classes.** s U+0307 U+0323, U+1E61 U+0323 (ṡ with a dot below added), U+1E63 U+0307 (ṣ with a dot above added) and U+1E69 ṩ all decompose to 0073 0323 0307. The dot below has class 220 and the dot above 230, so canonical ordering puts the dot below first.
- **Hangul.** U+D55C 한 and the jamo U+1112 U+1161 U+11AB are equivalent.
- **Not equivalent: marks of the same class.** a U+0301 U+0300 and a U+0300 U+0301 have different decompositions. Both marks have class 230 and go above the letter, so their order is visible: the second one stacks on the first.
- **Not equivalent: compatibility only.** U+FB01 ﬁ has the mapping `<compat>` 0066 0069. It is compatibility equivalent to "fi" (D67), but not canonically equivalent, and NFD keeps it.
- **Not equivalent: similar shapes.** The Latin A U+0041 and the Cyrillic А U+0410 look the same in most fonts but are different letters with no mapping between them. Such pairs are [confusables](/unicode-confusable-detection/).
- **Not equivalent: case.** é and É are different text. Equality without case uses [case folding](/unicode-case-folding/).

## Related definitions

- **Compatibility equivalence (D67).** Two sequences are compatibility equivalent when their full compatibility decompositions, which also apply the tagged mappings, are the same. It is coarser: canonical equivalence implies compatibility equivalence, and ﬁ, ① and ½ show that the converse fails.
- **Normalization forms.** NFD and NFC are the canonical representatives of each class, decomposed and composed. NFKD and NFKC do the same for compatibility equivalence. See [Unicode normalization forms](/unicode-normalization-forms/) and the [normalization algorithm](/unicode-normalization-algorithm/).
- **Primary composite (D114).** A canonical decomposable character that is not excluded from composition. NFC uses these to compose. U+212B and U+0958 are excluded, so NFC replaces them by other strings.
- **Grapheme cluster.** What a reader sees as one character is an [extended grapheme cluster](/extended-grapheme-cluster/). The two equivalent forms of é, one code point or two, are both one cluster.
- **Collation.** The [Unicode collation algorithm](/unicode-collation-algorithm/) gives equivalent strings the same sort keys, so it can sort text that is not normalized.

## References
