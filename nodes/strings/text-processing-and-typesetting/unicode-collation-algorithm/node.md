---
tag: 7HSE2K
kind: algorithm
slug: unicode-collation-algorithm
name: Unicode collation algorithm
aliases:
- UCA
- multilevel collation
area: strings/text-processing-and-typesetting
level: core
summary: "Map strings to collation elements with primary, secondary and tertiary weights from a table such as the DUCET, then compare sort keys level by level. Tailorings adapt it to a language."
model: word-ram
complexity:
  vars: {n: the length of the input in code points}
  time: {worst: O(n^2), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [unicode-normalization-algorithm, unicode-code-point]
see_also: [string-sorting, lexicographic-order, msd-radix-sort, canonical-equivalence, unicode-case-folding, unicode-confusable-detection, trie, comparison-sort]
sources:
  - url: https://www.unicode.org/reports/tr10/tr10-51.html
    title: "Ken Whistler and Markus Scherer (editors), Unicode Technical Standard 10, Unicode Collation Algorithm, revision 51, 2024-08-22"
    locator: "Section 1.1 (Table 2, Comparison Levels), Section 4 and 4.1 (Variable Weighting, Table 11 and Table 12), Section 7 (Main Algorithm, steps S1 to S4), Section 10.1.3 (Implicit Weights, Table 16) and Section 12.1 (Allkeys File Format)"
  - url: https://www.unicode.org/Public/UCA/16.0.0/allkeys.txt
    title: "allkeys-16.0.0.txt, the Default Unicode Collation Element Table (DUCET), 2024-04-25"
    locator: "the data lines, in the format of UTS 10 section 12.1"
  - url: https://www.unicode.org/Public/UCA/16.0.0/CollationTest.zip
    title: "CollationTest 16.0.0 (CollationTest_NON_IGNORABLE and CollationTest_SHIFTED, with _SHORT variants)"
    locator: "the lines of CollationTest_NON_IGNORABLE_SHORT.txt, which are in increasing order"
  - url: https://www.unicode.org/reports/tr35/tr35-collation.html
    title: "Unicode Technical Standard 35, Unicode Locale Data Markup Language (LDML), Part 5: Collation"
    locator: the CLDR root collation and the syntax of tailoring rules
---

The Unicode collation algorithm (UCA) of Unicode Technical Standard 10 compares two strings in the order that people expect in a dictionary or a phone book, not in the order of their [code points](/unicode-code-point/). Each string is first put in NFD by the [normalization algorithm](/unicode-normalization-algorithm/), then mapped to a sequence of collation elements. A collation element has a primary weight for the base letter, a secondary weight for accents and a tertiary weight for case and variants. The algorithm compares all the primary weights first, then the secondary weights, then the tertiary weights. The weights come from a table. The Default Unicode Collation Element Table (DUCET) is independent of language. A tailoring, for example from CLDR, changes the table for one language, such as Swedish, where "ä" sorts after "z".

## In plain words

Sorting text by the numbers of its characters gives strange results. "Role" comes before "role" because capital letters have smaller numbers, and "rôle" goes after every word that starts with "ro" plus a plain letter. People compare words in steps. First they look only at the letters and ignore accents and case. Only if the letters are the same do they look at the accents. Only if the accents are the same too do they look at case.

The algorithm gives each character three numbers, one for each step. For a word, it lists all the first numbers, then all the second numbers, then all the third numbers, in one long key. Comparing two keys number by number then gives the order of the steps. Spaces and punctuation get special treatment, so that "de-luge" and "deluge" can sort together.

## The problem

The input is two strings $A$ and $B$, a collation element table $T$ and a variable weighting option. The output is $-1$, $0$ or $1$ for $A < B$, $A = B$ and $A > B$.

The table maps a sequence of one or more code points to a list of collation elements. In the allkeys.txt format of UTS 10 section 12.1, a line such as

    0061  ; [.2380.0020.0002] # LATIN SMALL LETTER A

gives U+0061 LATIN SMALL LETTER A one element with the primary weight 2380, the secondary weight 0020 and the tertiary weight 0002, all in hexadecimal. A `*` instead of the `.` marks a variable element, which is used for spaces, punctuation and most symbols: U+0020 SPACE is `[*0209.0020.0002]`. A sequence of several code points on the left is a contraction, and several elements on the right are an expansion. For example U+00E6 LATIN SMALL LETTER AE has three elements, `[.2380.0020.0004][.0000.011E.0004][.23E7.0020.0004]`, so it sorts with "ae" at the first level. An element with primary weight 0000 is ignorable at the first level. The weights in this page are copied from allkeys-16.0.0.txt.

UTS 10 Table 2 shows the levels. Here U+0022 stands in for the curly quotation marks of the table:

| level | difference | example |
|---|---|---|
| L1 | base letters | role < roles < rule |
| L2 | accents | role < rôle < roles |
| L3 | case and variants | role < Role < rôle |
| L4 | punctuation, with a variable option | role < "role" < Role |

The rows show that a difference at a lower level counts only if all higher levels are equal: rôle is after Role because the accent is a level 2 difference and the case a level 3 difference. Python's sorted() uses code point order and gives Role, role, rôle.

## The algorithm

UTS 10 section 7 gives four steps: S1 normalize, S2 produce the collation element array, S3 form the sort key, S4 compare the sort keys.

```pseudo id=main
SORT-KEY(X, T, mode)
L1  X <- NFD(X)                                                        ▷ S1
L2  C <- []; i <- 0
L3  while i < |X| do
L4      j <- the largest end such that X[i..j-1] is a key of T, or i + 1 if there is none   ▷ S2.1
L5      for each later non-starter c of X that is unblocked: if X[i..j-1] + c is a key of T, extend the match with c and remove c from X   ▷ S2.1.1 to S2.1.3
L6      if the match S is a key of T then append T[S] to C else append IMPLICIT(X[i]) to C   ▷ S2.2, S2.4
L7      i <- j                                                         ▷ S2.5
L8  W <- VARIABLE-WEIGHTING(C, mode)                                   ▷ S2.3
L9  K <- []
L10 for level <- 1 to the number of levels do                          ▷ S3
L11     if level > 1 then append 0000 to K
L12     append the non-zero weights of this level of W to K, in order
L13     if level = 4 and mode = shift-trimmed then remove the trailing FFFF weights of this level
L14 return K
COMPARE(A, B, T, mode)
L15 return the binary comparison of SORT-KEY(A, T, mode) and SORT-KEY(B, T, mode)   ▷ S4
```

**Longest match and discontiguous contractions (lines L4 and L5).** A non-starter is a code point with a non-zero canonical combining class (ccc). A non-starter $c$ after the match is unblocked if no code point between the match and $c$ has ccc 0 or a ccc greater than or equal to the ccc of $c$. Because the text is in NFD, the non-starters after a base are in canonical order, and line L5 can add a mark to a contraction even if another mark with a lower ccc stands between them.

**Implicit weights (line L6).** A code point that is not in the table gets two elements $[.AAAA.0020.0002][.BBBB.0000.0000]$ (UTS 10 section 10.1.3, Table 16). For core Han ideographs, those with Unified_Ideograph=True in the blocks CJK Unified Ideographs and CJK Compatibility Ideographs, $AAAA = \mathrm{FB40} + (cp \gg 15)$ and $BBBB = (cp \mathbin{\&} \mathrm{7FFF}) \mathbin{|} \mathrm{8000}$. Other Han ideographs use the base FB80, and any other code point the base FBC0. Tangut, Nushu and Khitan Small Script have their own bases FB00, FB01 and FB02. So U+4E00 gets [.FB40.0020.0002][.CE00.0000.0000], and Han ideographs sort in code point order after all letters of the table.

**Variable weighting (line L8).** UTS 10 section 4 gives four options for the variable elements:

- **Non-ignorable.** Variable elements are used as they are. Spaces and punctuation then sort like letters, with low primary weights.
- **Blanked.** Variable elements, and the primary ignorable elements that follow them, get all weights 0. Punctuation is then ignored.
- **Shifted.** A fourth level is added, with the rules of Table 11: a variable element becomes $[.0000.0000.0000.pppp]$ with its old primary weight at level 4; a primary ignorable element after a variable one becomes all zero; a completely ignorable element stays all zero; every other element gets FFFF at level 4.
- **Shift-Trimmed.** As Shifted, but the trailing FFFF weights are removed from level 4.

**Sort key (lines L9 to L13).** The key holds the non-zero weights of level 1, the separator 0000, the non-zero weights of level 2, and so on. The separator 0000 is lower than any weight, so a shorter level wins as in a [lexicographic order](/lexicographic-order/). Section 7.3 also allows a level to be backwards (step S3.6), which is used for French accents, and an identical level that appends the NFD string (step S3.10).

## Example

The weights below are copied from allkeys-16.0.0.txt. With the non-ignorable option, rôle in NFD is U+0072 U+006F U+0302 U+006C U+0065, and step S2 gives

$$[.2584.0020.0002]\,[.252C.0020.0002]\,[.0000.0027.0002]\,[.24BC.0020.0002]\,[.23E7.0020.0002].$$

The sort keys, with | for the separator 0000:

| string | sort key (non-ignorable) |
|---|---|
| role | 2584 252C 24BC 23E7 \| 0020 0020 0020 0020 \| 0002 0002 0002 0002 |
| Role | 2584 252C 24BC 23E7 \| 0020 0020 0020 0020 \| 0008 0002 0002 0002 |
| rôle | 2584 252C 24BC 23E7 \| 0020 0020 0027 0020 0020 \| 0002 0002 0002 0002 0002 |

All three agree at level 1. At level 2, role and Role have 0020 at the third place, and rôle has 0027, so rôle is last. At level 3, Role has 0008 for the capital R and role has 0002, so role < Role < rôle.

The options give different orders of the strings of UTS 10 Table 12:

| option | order |
|---|---|
| non-ignorable | de luge, de Luge, de-luge, de-Luge, death, deluge, deLuge, demark |
| shifted | death, de luge, de-luge, deluge, de Luge, de-Luge, deLuge, demark |
| shift-trimmed | death, deluge, de luge, de-luge, deLuge, de Luge, de-Luge, demark |
| blanked | death, {de luge, de-luge, deluge}, {de Luge, de-Luge, deLuge}, demark |

With the non-ignorable option, the space (primary 0209) and the hyphen (020D) sort before every letter, so all forms with a space or a hyphen come before death. With shifted, the level 4 key of de-luge is FFFF FFFF 020D FFFF FFFF FFFF FFFF and that of deluge is FFFF FFFF FFFF FFFF FFFF FFFF, so de-luge < deluge. With shift-trimmed, the key of deluge has an empty level 4 and comes first. In braces, blanked gives equal strings.

The L4 row of Table 2 needs care. With U+0022 QUOTATION MARK, the level 4 key of "role" under shifted is 033A FFFF FFFF FFFF FFFF 033A, which is lower than FFFF FFFF FFFF FFFF for role, so shifted gives "role" < role. The order role < "role" holds with shift-trimmed, where the level 4 key of role is empty.

## Correctness

The claim is that COMPARE gives the order of UTS 10: first by the level 1 weights, then level 2, and so on. Each level of the sort key is the sequence of non-zero weights of that level, and two keys agree up to the separator of a level exactly when all earlier levels are equal. The separator 0000 is lower than any non-zero weight, so a level that is a proper prefix of the other ends first and is smaller. So binary comparison of the keys is the same as a comparison level by level. The proof is in proofs/correctness.md, together with the invariant of step S2. The tests check this equivalence on random strings for all four options, and check the order of a run of 19 lines of CollationTest_NON_IGNORABLE_SHORT.txt.

## Complexity

In the [word-RAM model](/word-ram/), a table lookup costs $O(1)$, with a large constant: real tables have tens of thousands of entries, stored in a [trie](/trie/) or a two-stage array. Let $m$ be the length of the longest contraction and $e$ the largest expansion, both constants of the table.

- **NFD.** Linear in $n$ for text with short runs of combining marks.
- **Step S2.** The longest match tries at most $m$ lengths at each start. The scan for discontiguous contractions walks over the run of non-starters after the match. On a run of $k$ non-starters this costs $O(k)$ per start, so $O(k^2)$ in total, and $O(n^2)$ for a pathological string of one base and $n - 1$ marks. On text in the Stream-Safe Text Format of UAX 15, which has at most 30 non-starters in a row, step S2 is $\Theta(n)$.
- **Sort key.** At most $e \cdot n$ elements and 4 weights each, so $O(n)$ weights. Comparing two keys is linear in their length.
- **Space.** $\Theta(n)$ for the NFD string, the element array and the key.

| case | time |
|---|---|
| typical text, bounded runs of marks | $\Theta(n)$ |
| one base followed by $n - 1$ marks | $O(n^2)$ |
| compare two precomputed keys | $O(n)$ |

Sorting $N$ strings costs $O(N \log N)$ comparisons. Building each key once and sorting the keys with a [string sort](/string-sorting/) such as [MSD radix sort](/msd-radix-sort/) is usually faster than comparing strings directly.

## Properties

- **Total preorder.** COMPARE is reflexive and transitive, and any two strings are comparable. Different strings can be equal, for example under blanked, or "a" and a string with a completely ignorable code point. An identical level breaks such ties.
- **Canonical equivalence.** Because of step S1, [canonically equivalent](/canonical-equivalence/) strings get the same key: U+00E9 and U+0065 U+0301 sort as one string.
- **Not case folding.** Case is only a level 3 difference. A comparison at strength 2 ignores case, but it is not the same as [case folding](/unicode-case-folding/): ß and ss are equal at level 1, but differ at level 2 in the DUCET, because ß has the extra element [.0000.011E.0004].
- **Language independent, then tailored.** The DUCET gives one order for all scripts. No single order is right for all languages, so real systems use tailorings.
- **Not stable across versions.** New characters and changes to the DUCET change the keys. Stored sort keys must be rebuilt when the table changes.

## Variants and improvements

- **CLDR root collation and tailorings.** CLDR (UTS 35 part 5) defines a root collation, which differs from the DUCET in a few places, and tailoring rules such as `&z < å` for each language. ICU implements this.
- **Parameters.** CLDR adds options for strength, case first (uppercase before lowercase), backwards secondary weights, and numeric ordering of digit runs.
- **Incremental comparison.** A comparison can stop at the first difference without building full keys. This is faster when strings differ early, and gives the same result.
- **ISO/IEC 14651.** The international standard for the same ordering. The DUCET is kept aligned with its common template table.

## When to use it

Use the UCA, or a library that implements it with CLDR data, whenever a list of strings is shown to people in sorted order: names, file lists, index entries. Use the language of the reader. Do not use it for keys of a data structure that only needs some fixed order: binary code point comparison is faster and stable across versions. For caseless matching, use [case folding](/unicode-case-folding/); for spoof detection, use [confusable detection](/unicode-confusable-detection/).

## Pitfalls

- **Skipping NFD.** Without step S1, U+00E9 and U+0065 U+0301 get different keys if the table has no entry for one of them. The test `test_expansions_and_nfd` compares their keys.
- **Comparing level by level per element.** The keys compare all level 1 weights before any level 2 weight. Comparing elements one by one with all three weights at once gives rôle < Role, because the first elements differ at level 3.
- **Mixing options.** Keys built with different variable options or table versions cannot be compared.
- **Assuming the L4 row of Table 2 under shifted.** As the example shows, under shifted "role" < role.
- **Missing the discontiguous rule.** A contraction with a mark can be split by another mark with a lower ccc. The test `test_contractions_made_up_for_this_test` has a case where U+0323 stands between the base and U+0301.
- **Tables of a different version.** The weights and the implicit weight ranges in this page follow Unicode 16.0.0. Keys from another version of the table can give a different order.

## Implementations

## History

UTS 10 gets a new revision with each version of the Unicode Standard, and the DUCET is updated in step. Revision 51, edited by Ken Whistler and Markus Scherer, is the version for Unicode 16.0.0. The ordering is kept aligned with ISO/IEC 14651. CLDR builds its root collation and its language tailorings on the UCA.

## References
