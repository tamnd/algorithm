---
tag: GS7516
kind: algorithm
slug: unicode-case-folding
name: Unicode case folding
aliases:
- caseless matching
- full case folding
area: strings/text-processing-and-typesetting
level: core
summary: "Map each code point to its folding from CaseFolding.txt, so that strings that differ only in case become equal. Full folding can change the length: ß becomes ss."
model: word-ram
complexity:
  vars: {n: the length of the input in code points}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [unicode-code-point, unicode-normalization-algorithm]
see_also: [canonical-equivalence, unicode-normalization-forms, unicode-collation-algorithm, unicode-confusable-detection, alphabet, hash-table]
sources:
  - book: isbn:9781936213344
    title: "The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024"
    locator: "Chapter 3, Section 3.13 Default Case Algorithms: 3.13.3 Default Case Folding (R4, toCasefold) and 3.13.5 Default Caseless Matching (D144 to D147)"
  - url: https://www.unicode.org/versions/Unicode16.0.0/core-spec/
    title: "The Unicode Standard, Version 16.0.0, core specification (online)"
    locator: "Chapter 3, Section 3.13"
  - url: https://www.unicode.org/Public/16.0.0/ucd/CaseFolding.txt
    title: "CaseFolding-16.0.0.txt, Unicode Character Database"
    locator: "the header (the status values C, F, S and T) and the data lines"
  - url: https://docs.python.org/3/library/stdtypes.html#str.casefold
    title: "Python documentation, Built-in Types"
    locator: str.casefold
---

Unicode case folding maps a string to a form in which the differences of letter case are gone, so that two strings that differ only in case become equal. It replaces each [code point](/unicode-code-point/) by its mapping in the file CaseFolding.txt of the Unicode Character Database, and keeps code points that have no mapping. Full folding can make a string longer: U+00DF LATIN SMALL LETTER SHARP S (ß) becomes "ss". Simple folding keeps the length in code points. Folding is the base of caseless matching, and the canonical form of caseless matching also needs [normalization](/unicode-normalization-algorithm/) before and after the folding.

## In plain words

To compare words without caring about capital letters, people often turn both words into small letters first. For English this is enough. For other languages it is not. The German letter ß has no single capital form in common use, and its capital spelling is "SS", so "Straße" and "STRASSE" must become the same. Greek has two small forms of sigma, one used only at the end of a word, and both must become the same letter.

Unicode publishes one table that says, for each character, what it becomes in the case-free form. The method is to look up each character in the table and write down the result. A few results are two or three characters long. The table is fixed and the same for all languages, except an optional rule for the Turkish dotted and dotless i.

## The problem

The input is a string $X$ of $n$ code points. The output is $\mathrm{toCasefold}(X)$, defined by rule R4 of the core specification, section 3.13.3: "Map each character C in X to Case_Folding(C)." Here Case_Folding(C) is the mapping of C in CaseFolding.txt, or C itself if the file has no line for C.

Each line of CaseFolding.txt has the form `code; status; mapping; # name`. The status says which kind of folding uses the line:

- **C** (common): a mapping to one code point, used by full and by simple folding.
- **F** (full): a mapping to two or three code points, used by full folding.
- **S** (simple): a mapping to one code point, used by simple folding where an F line exists for the same code point.
- **T** (Turkic): a special mapping for U+0049 and U+0130, used only if the caller asks for it. It is not part of the default folding.

Full folding uses the lines with status C and F. Simple folding uses C and S. The default case folding of the standard is full folding without the T lines. Python's `str.casefold` computes it.

Two strings are a *default caseless match* (D144) if $\mathrm{toCasefold}(X) = \mathrm{toCasefold}(Y)$. They are a *canonical caseless match* (D145) if

$$\mathrm{NFD}(\mathrm{toCasefold}(\mathrm{NFD}(X))) = \mathrm{NFD}(\mathrm{toCasefold}(\mathrm{NFD}(Y))).$$

D146 (compatibility caseless match) uses NFKD in the same way, and D147 (identifier caseless match) uses the derived mapping toNFKC_Casefold. Here NFD is the canonical decomposition of the [normalization algorithm](/unicode-normalization-algorithm/).

## The algorithm

```pseudo id=main
TO-CASEFOLD(X, full, turkic)
L1  Y <- empty string
L2  for each code point c of X do
L3      if turkic and c has a line with status T then append its mapping to Y
L4      else if full and c has a line with status F then append its mapping to Y
L5      else if not full and c has a line with status S then append its mapping to Y
L6      else if c has a line with status C then append its mapping to Y
L7      else append c to Y
L8  return Y

CANONICAL-CASELESS-MATCH(X, Y)
L9  return NFD(TO-CASEFOLD(NFD(X))) = NFD(TO-CASEFOLD(NFD(Y)))
```

The table is a [hash table](/hash-table/) or a two-stage array keyed by code point. For each code point, CaseFolding.txt has at most one line of each status, and it never has both an F line and a C line for the same code point, so lines L3 to L7 pick exactly one result. The implementation copies the lines it uses verbatim from CaseFolding-16.0.0.txt, among them the C, F, S and T lines of ß, U+1E9E LATIN CAPITAL LETTER SHARP S (ẞ), U+0130 LATIN CAPITAL LETTER I WITH DOT ABOVE (İ), U+0049, U+03C2 GREEK SMALL LETTER FINAL SIGMA (ς), U+01C5 LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON (ǅ) and U+0345 COMBINING GREEK YPOGEGRAMMENI.

## Example

The values below come from the lines of CaseFolding-16.0.0.txt in the implementation, and `str.casefold` gives the same full foldings.

| input | code points | full folding | simple folding |
|---|---|---|---|
| Straße | 0053 0074 0072 0061 00DF 0065 | 0073 0074 0072 0061 0073 0073 0065 (strasse) | 0073 0074 0072 0061 00DF 0065 (straße) |
| STRASSE | 0053 0054 0052 0041 0053 0053 0045 | strasse | strasse |
| ẞ | 1E9E | 0073 0073 | 00DF |
| ﬃ | FB03 | 0066 0066 0069 | FB03 |
| İ | 0130 | 0069 0307 | 0130 |
| ǅ | 01C5 | 01C6 | 01C6 |
| ς | 03C2 | 03C3 | 03C3 |

"Straße" and "STRASSE" are a default caseless match under full folding, but not under simple folding. Folding is not lowercasing: U+00DF is already small and still changes, and U+0130 has no simple folding at all, so simple folding keeps it. With the Turkic option, U+0049 folds to U+0131 LATIN SMALL LETTER DOTLESS I and U+0130 folds to U+0069.

Why D145 normalizes first. Take $X$ = U+03B1 U+0345 U+0301 and $Y$ = U+03B1 U+0301 U+0345. The marks U+0345 and U+0301 have the canonical combining classes 240 and 230, so NFD puts U+0301 first, and $X$ and $Y$ are canonically equivalent. U+0345 folds to U+03B9 GREEK SMALL LETTER IOTA, which is a starter. Folding first gives U+03B1 U+03B9 U+0301 for $X$ and U+03B1 U+0301 U+03B9 for $Y$. NFD cannot move the acute accent across the starter U+03B9, so the two results stay different. With NFD first, both strings become U+03B1 U+0301 U+0345, and both fold to U+03B1 U+0301 U+03B9. The core specification gives this case as the reason: "Normalization is not required before case folding, except for the character U+0345".

Why D145 normalizes after. U+00C5 LATIN CAPITAL LETTER A WITH RING ABOVE folds to U+00E5, but U+0041 U+030A folds to U+0061 U+030A. The two folded strings are canonically equivalent but not equal, so only the final NFD makes them match. Also, U+0390 GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS is in NFC, but its full folding U+03B9 U+0308 U+0301 is not: folding does not keep a string normalized.

## Correctness

TO-CASEFOLD computes R4 directly. The loop of lines L2 to L7 keeps the invariant that $Y$ is the concatenation of Case_Folding(c) over the code points already read, where Case_Folding is taken with the statuses that the options select. The selection is well defined because the file has at most one line per code point and status, and never both C and F for one code point. At the end, $Y = \mathrm{toCasefold}(X)$. Simple folding keeps the length because every C and S mapping is one code point. The canonical caseless match of line L9 is an equivalence relation, because it compares the values of one function, and it contains canonical equivalence, because canonically equivalent strings have the same NFD. The full proof is in proofs/correctness.md.

## Complexity

In the [word-RAM model](/word-ram/), one lookup in a table indexed by code point costs $O(1)$. The constant is large in practice: real tables use two or three levels of arrays to cover the 1,114,112 code points of the codespace.

- **Folding.** Each code point costs one lookup and appends at most 3 code points, because no F mapping in CaseFolding.txt is longer than 3 code points. So TO-CASEFOLD takes $\Theta(n)$ time, and the output has at most $3n$ code points.
- **Space.** The output takes $O(n)$ space. A comparison that folds both strings lazily, one code point at a time, needs only $O(1)$ extra space.
- **Canonical caseless match.** NFD costs $O(n)$ lookups, plus the canonical ordering of each run of combining marks, which costs $O(k \log k)$ for a run of $k$ marks. Line L9 runs NFD twice and the folding once on each string.

| claim | value |
|---|---|
| time of TO-CASEFOLD | $\Theta(n)$ lookups |
| output length, full folding | at most $3n$ code points |
| output length, simple folding | exactly $n$ code points |

## Properties

- **Context-free.** Each code point folds alone. There is no rule for the end of a word, unlike the lowercase mapping of U+03A3 GREEK CAPITAL LETTER SIGMA, which depends on the context.
- **Concatenation.** $\mathrm{toCasefold}(XY) = \mathrm{toCasefold}(X)\,\mathrm{toCasefold}(Y)$. This makes the folding online and lets a program fold a stream in pieces.
- **Idempotent on the data.** Folding a folded string changes nothing. The tests check this on every line of the table.
- **Not normalization-preserving.** A string in NFC can fold to a string that is not in NFC, as U+0390 above.
- **Language-independent.** The default folding is the same for all languages. Only the T lines depend on the language.

## Variants and improvements

- **Simple folding.** Statuses C and S. It keeps the length in code points and suits fixed-size buffers and regular expression engines that compare one code point with one code point.
- **Turkic folding.** Put the T lines before the others, for Turkish and Azerbaijani.
- **Compatibility caseless match (D146).** $\mathrm{NFKD}(\mathrm{toCasefold}(\mathrm{NFKD}(\mathrm{toCasefold}(\mathrm{NFD}(X)))))$. It also matches compatibility variants, for example U+FB03 and "ffi", and the full-width letters.
- **Identifier caseless match (D147).** It uses toNFKC_Casefold, a derived property of the Unicode Character Database that combines NFKC, folding and the removal of default ignorable code points in one mapping.
- **Lazy comparison.** Compare two strings by folding each one code point at a time and comparing the outputs as streams. This needs no allocation.

## When to use it

Use full default folding with the canonical match D145 when you compare user text without regard to case: search, deduplication of names, keys of a [hash table](/hash-table/) that must ignore case. Use simple folding when the length must not change. Use the Turkic option only when you know the language of the text. Do not use folding to produce text for display: the folded string is a comparison key, not a lowercase version of the text. For sorting, use the [collation algorithm](/unicode-collation-algorithm/), which treats case as a level 3 difference. For security checks of look-alike strings, use [confusable detection](/unicode-confusable-detection/), which goes further than case.

## Pitfalls

- **Lowercasing instead of folding.** A lowercase mapping keeps ß and maps ẞ to ß, so "STRASSE" and "Straße" do not match. The test `test_check_values` checks the full foldings of ß and ẞ.
- **Folding without normalization.** U+00C5 and U+0041 U+030A do not match by D144. Use D145. The test `test_default_match_misses_decomposed_forms` shows this case.
- **Normalizing only after folding.** The U+0345 example above fails. The test `test_ypogegrammeni_needs_nfd_first` checks it.
- **Turkic lines by default.** Taking the T lines for all text makes "I" fold to dotless ı and breaks English. The test `test_turkic_option` checks both settings.
- **Fixed-size output buffers.** Full folding can triple the length in code points, and more in bytes.
- **Characters that look cased but fold elsewhere.** U+212A KELVIN SIGN folds to "k" and U+2126 OHM SIGN folds to U+03C9. A table built only from the letters A to Z misses them.

## Implementations

## History

In ASCII, case-insensitive comparison only maps A to Z onto a to z. Unicode added the file CaseFolding.txt to its Character Database so that all programs fold the same characters in the same way, with the full mappings for ß, the ligatures and the Greek letters with iota subscript. U+1E9E LATIN CAPITAL LETTER SHARP S came in Unicode 5.1 (2008). It folds to "ss" like ß, so the folding of German text did not change. Python added `str.casefold` in version 3.3.

## References
