---
tag: ST3J66
kind: definition
slug: unicode-normalization-forms
name: Unicode normalization forms
aliases:
- NFC
- NFD
- NFKC
- NFKD
area: strings/text-processing-and-typesetting
level: core
summary: "NFD, NFC, NFKD and NFKC pick one string from each class of canonically or compatibly equivalent strings, in decomposed or composed form, so that equal text compares equal."
prereqs: [canonical-equivalence]
see_also: [canonical-equivalence, unicode-normalization-algorithm, hangul-syllable-composition, canonical-form, unicode-case-folding, unicode-collation-algorithm, unicode-confusable-detection, punycode]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3: Section 3.7 Decomposition (D65 to D70) and Section 3.11 Normalization Forms (3.11.1 Normalization Stability, 3.11.6 Canonical Composition Algorithm with D114 to D117, 3.11.7 Definition of Normalization Forms with D118 to D121)"
  - url: https://www.unicode.org/reports/tr15/
    title: Mark Davis and Ken Whistler, Unicode Standard Annex 15, Unicode Normalization Forms, revision 56
    locator: "Section 1.1 to 1.4 (equivalence, the four forms and their examples), Section 3 (versioning and stability), Section 4 (conformance, UAX15-C1 to C5), Section 9 (detecting normalization forms) and Section 13 (Stream-Safe Text Format)"
  - url: https://docs.python.org/3/library/unicodedata.html
    title: Python documentation, unicodedata
    locator: unicodedata.normalize and unicodedata.is_normalized
---

A Unicode normalization form is a rule that picks one string from each class of equivalent strings, so that text that is the same compares equal code point by code point. There are four forms. NFD and NFC are for [canonical equivalence](/canonical-equivalence/): NFD takes every character apart into a base and combining marks, and NFC puts it back together where possible. NFKD and NFKC do the same for the coarser compatibility equivalence, which also maps ligatures, full-width letters, superscripts and similar variants to their plain forms.

## Definition

The definitions are from section 3.11.7 of the core specification of Unicode 16.0.0. For a sequence $s$ of code points:

- **NFD (D118)** is the canonical decomposition of $s$ (D68): apply the canonical decomposition mappings until none applies, then sort each run of combining marks by canonical combining class, keeping the order of marks of the same class.
- **NFKD (D119)** is the compatibility decomposition of $s$ (D65): the same, with the compatibility mappings applied too.
- **NFC (D120)** is the canonical composition (D117) of NFD$(s)$.
- **NFKC (D121)** is the canonical composition of NFKD$(s)$.

The canonical composition algorithm goes through the decomposed string from left to right. It replaces a starter $L$ and a later character $C$ by the primary composite (D114) that decomposes to $L\,C$, when such a composite exists and $C$ is not blocked from $L$ (D115). A character is blocked when a character between them is a starter or has a combining class at least as high as its own. Characters with the property Full_Composition_Exclusion are never produced. The [normalization algorithm](/unicode-normalization-algorithm/) gives the steps.

The forms are canonical forms in the exact sense:

$$s \equiv t \iff \mathrm{NFD}(s) = \mathrm{NFD}(t) \iff \mathrm{NFC}(s) = \mathrm{NFC}(t),$$

and the same holds for compatibility equivalence with NFKD and NFKC. Each form $X$ is idempotent: $X(X(s)) = X(s)$. A string $s$ is *in* form $X$ when $X(s) = s$.

## Examples and non-examples

The values were checked with Python's `unicodedata.normalize` on data version 16.0.0. Code points are hexadecimal.

| input | NFD | NFC | NFKD | NFKC |
|---|---|---|---|---|
| 00E9 é | 0065 0301 | 00E9 | 0065 0301 | 00E9 |
| 0065 0301 | 0065 0301 | 00E9 | 0065 0301 | 00E9 |
| 212B Å (angstrom sign) | 0041 030A | 00C5 | 0041 030A | 00C5 |
| 1E9B 0323 | 017F 0323 0307 | 1E9B 0323 | 0073 0323 0307 | 1E69 |
| FB01 ﬁ | FB01 | FB01 | 0066 0069 | 0066 0069 |
| 00BD ½ | 00BD | 00BD | 0031 2044 0032 | 0031 2044 0032 |
| 01C4 Ǆ | 01C4 | 01C4 | 0044 005A 030C | 0044 017D |
| 0958 क़ | 0915 093C | 0915 093C | 0915 093C | 0915 093C |
| D55C 한 | 1112 1161 11AB | D55C | 1112 1161 11AB | D55C |

- **NFC is not always the shortest form.** U+0958 is excluded from composition, so NFC writes it as two code points, and the one-code-point form is in none of the four forms.
- **NFC can leave marks apart.** In the row of U+1E9B U+0323, the long s with dot above (ẛ) has no precomposed form with a dot below as well, so NFC keeps U+0323 apart. NFKC first turns the long s into s, and then ṩ U+1E69 exists.
- **Compatibility forms lose information.** NFKC maps ½ to 1, the fraction slash and 2, and ① to 1. Text that is shown to readers keeps its meaning only in NFC or NFD.
- **ASCII and Latin-1.** Every string of code points below U+0100 is in NFC, and every ASCII string is in all four forms. Latin-1 is not in NFKC: for example U+00A0 NO-BREAK SPACE becomes U+0020, and U+00BD ½ changes as above.
- **Not closed under concatenation.** "a" and U+0301 are both in NFC, but their concatenation is not, because NFC("a" U+0301) is U+00E1. A program that joins normalized strings must normalize the seam again.
- **Lengths.** One code point can grow to at most 4 code points under NFD, and to at most 18 under NFKD, for U+FDFA ARABIC LIGATURE SALLALLAHOU ALAYHE WASALLAM. These maxima were found by checking every scalar value with `unicodedata`.

## Related definitions

- **Canonical and compatibility equivalence (D70, D67).** The relations that the forms decide. See [canonical equivalence](/canonical-equivalence/).
- **Stability.** Section 3.11.1 and section 3 of UAX 15 restrict how later versions may change the data, so that a string of assigned characters that is in a form stays in that form under later versions. Strings with unassigned code points have no such promise.
- **Quick check.** Section 9 of UAX 15 defines the properties NFC_Quick_Check and the like, with the values Yes, No and Maybe, so that a program can often decide that a string is already in a form without normalizing it.
- **Stream-Safe Text Format.** Section 13 of UAX 15 limits a run of non-starters to 30 code points by inserting U+034F COMBINING GRAPHEME JOINER, so that normalization can run with a buffer of bounded size.
- **Conformance.** Section 4 of UAX 15, clauses UAX15-C1 to UAX15-C5, requires that a process that claims to produce a form produces exactly the result of the definition, for every input.
- **Other uses.** [Case folding](/unicode-case-folding/) is often combined with NFKC for matching identifiers, [Punycode](/punycode/) labels are encoded after the IDNA mapping that includes NFC, and the [collation algorithm](/unicode-collation-algorithm/) gives equivalent strings the same sort keys. A [canonical form](/canonical-form/) in general is a chosen representative of each class of an equivalence relation.

## References
