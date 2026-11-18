---
tag: N2QXMJ
kind: algorithm
slug: unicode-confusable-detection
name: Unicode confusable detection
aliases:
- confusable skeleton
- homoglyph detection
area: strings/text-processing-and-typesetting
level: advanced
summary: "Map each string to a skeleton by NFD, removal of default ignorable code points and the prototypes of confusables.txt. Two strings are confusable when their skeletons are equal."
model: word-ram
complexity:
  vars: {n: the length of the input in code points}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [unicode-normalization-algorithm, unicode-code-point]
see_also: [punycode, unicode-case-folding, unicode-collation-algorithm, unicode-bidirectional-algorithm, equivalence-relation, hash-table, edit-distance, unicode-normalization-forms]
sources:
  - url: https://www.unicode.org/reports/tr39/tr39-30.html
    title: "Mark Davis and Michel Suignard (editors), Unicode Technical Standard 39, Unicode Security Mechanisms, revision 30, 2024-09-03"
    locator: "Section 4 Confusable Detection (internalSkeleton, bidiSkeleton and skeleton), Section 4.1 Whole-Script Confusables and Section 4.2 Mixed-Script Confusables"
  - url: https://www.unicode.org/Public/security/16.0.0/confusables.txt
    title: "confusables.txt, Unicode security data, version 16.0.0, 2024-08-14"
    locator: the header (the format of the lines) and the data lines
  - url: https://www.unicode.org/Public/16.0.0/ucd/DerivedCoreProperties.txt
    title: "DerivedCoreProperties-16.0.0.txt, Unicode Character Database"
    locator: the lines of Default_Ignorable_Code_Point
  - url: https://www.unicode.org/reports/tr36/
    title: "Unicode Technical Report 36, Unicode Security Considerations"
    locator: the discussion of visual spoofing
---

Unicode confusable detection decides whether two strings can look the same to a reader, for example "paypal" in Latin letters and "pаypаl" with U+0430 CYRILLIC SMALL LETTER A in place of both letters a. Unicode Technical Standard 39 maps each string to a skeleton: the string in NFD, without default ignorable code points, with each character replaced by a prototype from the file confusables.txt. Two strings are confusable when their skeletons are equal. Registries of domain names, user names and identifiers use this to refuse a new name that looks like an existing one. The skeleton is only a key for comparison: it is not meant for display, and it is not stable across versions of the data.

## In plain words

Many characters look alike. The Cyrillic "а" and the Latin "a" look the same in most fonts, the digit one looks like a small letter l, and "rn" looks like "m" at small sizes. An attacker can use this to make a fake name that a person reads as a real one.

Unicode keeps a list that maps each such character to one chosen look-alike, its prototype. To test two strings, replace every character by its prototype, drop the invisible characters, and compare the results. If they are the same, the strings can fool a reader. A second step looks at the writing systems of the two strings, to tell a simple slip inside one script from a fake made with another script.

## The problem

The input is two strings $X$ and $Y$. The output is whether $X$ and $Y$ are confusable, and if so, which kind of confusable they are.

The data file confusables.txt has lines of the form

    0430 ;  0061 ;  MA  # ( а → a ) CYRILLIC SMALL LETTER A → LATIN SMALL LETTER A  #

with a source code point, a prototype of one or more code points, and the type MA. The source is always one code point. The prototype can be longer: U+006D LATIN SMALL LETTER M has the prototype U+0072 U+006E ("rn"). Code points without a line are their own prototype. In the file, a tab follows each semicolon and each field; the line above shows the tabs as two spaces.

UTS 39 section 4 defines:

- **internalSkeleton(X).** (1) Convert $X$ to NFD. (2) Remove every code point with Default_Ignorable_Code_Point (DICP), such as U+00AD SOFT HYPHEN and U+200B ZERO WIDTH SPACE. (3) Replace each code point by its prototype. (4) Convert the result to NFD again.
- **bidiSkeleton(d, X).** Reorder $X$ for display with the [bidirectional algorithm](/unicode-bidirectional-algorithm/) and the paragraph direction $d$, through rule L2, apply L3 and the mirroring of L4, then compute internalSkeleton of the result.
- **skeleton(X)** = bidiSkeleton(LTR, X). $X$ and $Y$ are confusable, $X \cong Y$, when skeleton($X$) = skeleton($Y$).

The kinds depend on the resolved script set of a string: the intersection of the script sets of its code points, where Common (digits, most punctuation) and Inherited (most combining marks) count as the set of all scripts. A string is single-script if its resolved script set is not empty.

- **Single-script confusables.** $X \cong Y$ and the resolved script sets of $X$ and $Y$ have a script in common. Example: "rn" and "m", both Latin.
- **Mixed-script confusables.** $X \cong Y$ and the resolved script sets have no script in common (section 4.2).
- **Whole-script confusables.** Mixed-script confusables where $X$ and $Y$ are both single-script (section 4.1). Example: "сор" in Cyrillic and "cop" in Latin.

## The algorithm

The implementation computes skeleton(X) for text where bidiSkeleton(LTR, X) is the same as internalSkeleton(X): text with no code point of bidi class R, AL or AN, no explicit directional formatting character, and no code point of class BN that is not default ignorable. On such text the bidirectional algorithm puts every character at level 0, so the reordering of L2 and the mirroring of L4 do nothing. Other text needs the full bidirectional algorithm, and the implementation raises an error for it.

```pseudo id=main
INTERNAL-SKELETON(X)
L1  X <- NFD(X)
L2  X <- X without the code points that have Default_Ignorable_Code_Point
L3  Y <- the concatenation of PROTOTYPE(c) for each code point c of X   ▷ c if c has no line
L4  return NFD(Y)
SKELETON(X)                                                 ▷ bidiSkeleton(LTR, X)
L5  if X has a code point of class R, AL or AN, or an explicit formatting character, then use the full bidiSkeleton
L6  return INTERNAL-SKELETON(X)
CONFUSABLE(X, Y)
L7  return SKELETON(X) = SKELETON(Y)
CLASSIFY(X, Y)
L8  if not CONFUSABLE(X, Y) then return none
L9  RX <- RESOLVED-SCRIPT-SET(X); RY <- RESOLVED-SCRIPT-SET(Y)
L10 if RX ∩ RY is not empty then return single-script
L11 if RX and RY are both not empty then return whole-script
L12 return mixed-script
```

To find all names in a registry that are confusable with a new name, store the skeleton of each name in a [hash table](/hash-table/). One lookup of the skeleton of the new name finds them all.

## Example

The prototypes below are copied from confusables.txt 16.0.0. Take $X$ = "pаypаl" with U+0430 at offsets 1 and 4, and $Y$ = "paypa1" with U+0031 DIGIT ONE at offset 5.

| step | $X$ | $Y$ |
|---|---|---|
| input | p U+0430 y p U+0430 l | p a y p a U+0031 |
| 1. NFD | no change | no change |
| 2. remove DICP | no change | no change |
| 3. prototypes | U+0430 → a, so "paypal" | U+0031 → l, so "paypal" |
| 4. NFD | "paypal" | "paypal" |

Both skeletons are "paypal", the skeleton of the real name "paypal", so all three strings are confusable. The kinds differ:

| pair | resolved script sets | kind |
|---|---|---|
| "paypa1", "paypal" | {Latin} and {Latin} (U+0031 is Common) | single-script |
| "pаypаl", "paypal" | {} and {Latin} | mixed-script |
| "сор", "cop" | {Cyrillic} and {Latin} | whole-script |
| "rn", "m" | {Latin} and {Latin} | single-script |

"pаypаl" mixes Cyrillic and Latin, so its resolved script set is empty. Such a string is suspicious on its own, without any comparison. A name in only Cyrillic letters that looks like a Latin name, such as "сор", passes a mixed-script check, and only the whole-script test finds it.

Some pairs that are not confusable: "paypal" and "paypai", "e" and "é", "a b" and "ab" (U+0020 is not default ignorable), and "O" and "o".

## Correctness

The function INTERNAL-SKELETON is the four steps of UTS 39 written out, so it is correct by definition. Two facts need proof. First, for text with no code point of class R, AL or AN and no explicit formatting character, bidiSkeleton(LTR, X) = internalSkeleton(X). The rules of the bidirectional algorithm with paragraph level 0 then give every remaining character the level 0, so L2 reverses nothing and L4 mirrors nothing. Second, $\cong$ is an [equivalence relation](/equivalence-relation/), because it compares the values of one function. The proof is in proofs/correctness.md. The tests check the four steps one by one, the pairs above, idempotence, a second implementation of the steps on random strings, and the equivalence on a set of random words.

## Complexity

In the [word-RAM model](/word-ram/), the lookups of DICP, of the prototype and of the script cost $O(1)$ each, with a large constant: confusables.txt has thousands of lines. Prototypes have bounded length. So each step is linear:

- NFD is $\Theta(n)$ for text with short runs of combining marks.
- Removing DICP and mapping by prototypes are $\Theta(n)$, and the result has $O(n)$ code points.
- Comparing two skeletons is linear in their length.

| operation | time | extra space |
|---|---|---|
| skeleton | $\Theta(n)$ | $\Theta(n)$ |
| CONFUSABLE, CLASSIFY | $\Theta(n)$ for strings of total length $n$ | $\Theta(n)$ |
| test a new name against a registry of $N$ names | $\Theta(n)$ expected with a hash table of skeletons | $\Theta(N n)$ for the table |

## Properties

- **An equivalence relation.** $\cong$ is reflexive, symmetric and transitive. UTS 39 notes that this imposes transitivity on the data: if "a" looks like "b" and "b" like "c", then "a" and "c" are confusable, even if they do not look alike. So the test can be too broad.
- **Idempotent mapping.** The data maps each prototype to itself, so skeleton(skeleton(X)) = skeleton(X).
- **Not about case or accents.** The skeleton keeps case: "O" and "o" have different skeletons. It keeps combining marks that have no line in the data. Use [case folding](/unicode-case-folding/) first if case must not count.
- **Not for display, not stable.** Skeletons can contain odd prototypes ("m" becomes "rn"), and they change when the data changes. Store the names, and recompute the skeletons after an update.

## Variants and improvements

- **Restriction levels and mixed-script detection.** UTS 39 also defines restriction levels for identifiers, from ASCII-only to unrestricted, based on the resolved script sets. Many registries combine them with the confusable test.
- **Augmented script sets.** For Han, Hiragana, Katakana and Hangul, UTS 39 adds the sets for Japanese and Korean writing, so that text that mixes Han and Kana counts as single-script.
- **Bidirectional text.** bidiSkeleton exists because a string with right-to-left characters can display in a different order from its logical order. Two strings with different logical orders can then look the same.
- **Fuzzy matching.** For names that differ by one character, a registry can add an [edit distance](/edit-distance/) test on the skeletons.
- **Domain names.** IDNA processing maps the labels of a domain name and encodes them with [Punycode](/punycode/). The confusable test is a separate policy check of the registry or of the browser.

## When to use it

Use the skeleton test when a system gives out unique names that people read: domain names, user names, package names, file names in a shared folder. Compute the skeleton of each new name and refuse the name if the skeleton is taken. Add a check that refuses mixed-script names unless there is a good reason. Do not use the skeleton as a normal form for search or for display; use NFC and [case folding](/unicode-case-folding/) for that.

## Pitfalls

- **Skipping the NFD steps.** Without step 1, "é" as U+00E9 and as U+0065 U+0301 give different skeletons. Without step 4, a prototype that decomposes can stay composed. The test `test_four_steps_of_internal_skeleton` checks each step.
- **Comparing internalSkeleton on right-to-left text.** Display order differs from logical order there. Use bidiSkeleton, or reject the text, as the implementation does with ValueError.
- **Showing the skeleton.** The skeleton of "mom" is "rnorn". It is a key, not a name.
- **Old data.** The data changes with every version, so skeletons in a database must be recomputed after an upgrade.
- **Expecting accents to count as confusable.** "e" and "é" are not confusable by this test. If a font makes a mark hard to see, that needs another rule.

## Implementations

## History

UTS 39 and confusables.txt are published with each version of the Unicode Standard. Older versions of the file had four tables with the types SL, SA, ML and MA; the current file has one table, and every line has the type MA. Since Unicode 7.0 the mapping is idempotent. Recent revisions added bidiSkeleton, and skeleton is now defined as bidiSkeleton with a left-to-right paragraph. Revision 30 is the version for Unicode 16.0.0.

## References
