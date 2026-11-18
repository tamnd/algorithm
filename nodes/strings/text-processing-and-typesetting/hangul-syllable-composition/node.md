---
tag: QKVWX9
kind: algorithm
slug: hangul-syllable-composition
name: Hangul syllable composition
aliases:
- Hangul syllable decomposition
area: strings/text-processing-and-typesetting
level: core
summary: "Map each of the 11,172 precomposed Hangul syllables to its leading consonant, vowel and optional trailing consonant jamo by arithmetic on the code point, and back, with no data table."
model: word-ram
complexity:
  vars: {n: the number of code points of the input}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [unicode-code-point, canonical-equivalence]
see_also: [unicode-normalization-algorithm, unicode-normalization-forms, canonical-equivalence, extended-grapheme-cluster, unicode-text-segmentation, unicode-collation-algorithm]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3, Section 3.12 Conjoining Jamo Behavior: 3.12.1 Definitions (D122 to D134), 3.12.2 Hangul Syllable Decomposition, 3.12.3 Hangul Syllable Composition, 3.12.4 Hangul Syllable Name Generation, 3.12.5 Sample Code for Hangul Algorithms"
  - url: https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/
    title: The Unicode Standard, Version 16.0.0, core specification, chapter 3 (online)
    locator: Section 3.12 and Section 3.11.6 Canonical Composition Algorithm (D114 to D117)
  - url: https://www.unicode.org/Public/16.0.0/ucd/Jamo.txt
    title: Unicode Character Database 16.0.0, Jamo.txt
    locator: Jamo_Short_Name values of the 67 modern jamo
  - url: https://www.unicode.org/reports/tr15/
    title: Mark Davis and Ken Whistler, Unicode Standard Annex 15, Unicode Normalization Forms, revision 56
    locator: Section 1.3 (Canonical composition) and the Hangul part of the decomposition data
---

The 11,172 precomposed Hangul syllables U+AC00..U+D7A3 are not listed in the decomposition data of Unicode. Their [canonical](/canonical-equivalence/) decompositions into conjoining jamo follow from a formula instead. Each syllable is one leading consonant (19 choices), one vowel (21 choices) and zero or one trailing consonant (27 choices), and the syllables are numbered in this mixed radix from U+AC00. So decomposition, composition and even the character name are a few divisions and additions, as section 3.12 of the core specification defines them.

## In plain words

Korean writing groups letters, called jamo, into square blocks, one block per syllable. Unicode has a code for every possible modern block, and also codes for the single letters.

The block codes are in a fixed order: first by the first consonant, then by the vowel, then by the final consonant or none. So the number of a block tells you its letters, in the same way that the number 347 tells you its hundreds, tens and ones. To split a block into letters you divide. To join letters into a block you multiply and add.

Because of this, programs need no list of the 11,172 blocks. They compute the parts when they normalize Korean text and when they print the names of the characters.

## The problem

The constants of section 3.12 are $S_B = \mathtt{AC00}$, $L_B = \mathtt{1100}$, $V_B = \mathtt{1161}$, $T_B = \mathtt{11A7}$, $L_C = 19$, $V_C = 21$, $T_C = 28$, $N_C = V_C T_C = 588$ and $S_C = L_C N_C = 11{,}172$. The modern leading consonants (L, D122) are U+1100..U+1112, the vowels (V, D125) U+1161..U+1175 and the trailing consonants (T, D128) U+11A8..U+11C2. $T_B$ itself is not a trailing consonant: the trailing index 0 means "no trailing consonant".

**Decomposition.** Given a precomposed syllable $s$ (D132), return its full canonical decomposition, $L\,V$ or $L\,V\,T$.

**Composition.** Given a sequence of code points, compose each $L\,V$ into an LV syllable (D130) and each LV syllable followed by $T$ into an LVT syllable (D131), as the canonical composition algorithm (D117) does.

**Name.** Given $s$, return its character name.

## The algorithm

```pseudo id=main
HANGUL-DECOMPOSE(s)
L1  i <- s - 0xAC00
L2  l <- i div 588
L3  v <- (i mod 588) div 28
L4  t <- i mod 28
L5  if t = 0 then return [0x1100 + l, 0x1161 + v]
L6  return [0x1100 + l, 0x1161 + v, 0x11A7 + t]

HANGUL-COMPOSE(c[1..n])
L7  out <- empty list
L8  for each code point c of the input, in order do
L9      if the last code point of out is an L and c is a V then
L10         replace the last code point by 0xAC00 + ((last - 0x1100) * 21 + (c - 0x1161)) * 28
L11     else if the last code point of out is a syllable with (last - 0xAC00) mod 28 = 0 and c is a T then
L12         replace the last code point by last + (c - 0x11A7)
L13     else append c to out
L14 return out

HANGUL-NAME(s)
L15 parts <- HANGUL-DECOMPOSE(s)
L16 return "HANGUL SYLLABLE " followed by the Jamo_Short_Name of each part
```

Lines L2 to L4 read the three digits of the syllable index in the mixed radix $(19, 21, 28)$. Line L10 builds the LV syllable, whose trailing digit is 0. Line L11 accepts a trailing consonant only after an LV syllable, so an LVT syllable never takes a second one. Line L13 appends every other code point.

The Unicode Character Database gives the decomposition mapping of a syllable in two parts: an LV syllable maps to $L, V$, and an LVT syllable maps to $LV, T$. Applying the mapping twice gives the result of line L6. The short names in line L16 come from Jamo.txt, where U+110B HANGUL CHOSEONG IEUNG has the empty name.

## Example

Decompose U+D55C 한. Line L1 gives $i = \mathtt{D55C} - \mathtt{AC00} = 10{,}588$. Then $l = 10{,}588 \operatorname{div} 588 = 18$, the remainder is 4, so $v = 0$ and $t = 4$. Line L6 returns U+1112 U+1161 U+11AB, the jamo ᄒ, ᅡ and ᆫ.

| syllable | index | $(l, v, t)$ | jamo | name |
|---|---|---|---|---|
| U+AC00 가 | 0 | (0, 0, 0) | 1100 1161 | HANGUL SYLLABLE GA |
| U+AC01 각 | 1 | (0, 0, 1) | 1100 1161 11A8 | HANGUL SYLLABLE GAG |
| U+C544 아 | 6,468 | (11, 0, 0) | 110B 1161 | HANGUL SYLLABLE A |
| U+D55C 한 | 10,588 | (18, 0, 4) | 1112 1161 11AB | HANGUL SYLLABLE HAN |
| U+D7A3 힣 | 11,171 | (18, 20, 27) | 1112 1175 11C2 | HANGUL SYLLABLE HIH |

Compose U+1112 U+1161 U+11AB. Line L13 appends U+1112. Then U+1161 is a vowel after a leading consonant, so line L10 writes $\mathtt{AC00} + (18 \cdot 21 + 0) \cdot 28 = \mathtt{D558}$, which is 하. Then U+11AB follows an LV syllable, so line L12 writes $\mathtt{D558} + 4 = \mathtt{D55C}$.

## Correctness

The map $(l, v, t) \mapsto (21 l + v) \cdot 28 + t$ is the mixed radix representation, so it is a bijection from the triples of digits onto $0..11{,}171$, and lines L2 to L4 are its inverse. This gives decomposition and shows that the syllables and the sequences $L\,V$ and $L\,V\,T$ of modern jamo correspond one to one. For composition, every jamo and every syllable has combining class 0, so it is a starter (D107), and by D115 a starter can only combine with the starter directly before it in the result. The primary composites (D114) with a Hangul first part are exactly $L + V \to LV$ and $LV + T \to LVT$, so lines L9 to L13 do what D117 does. The proof in proofs/correctness.md gives the details and the proof of the names.

## Complexity

In the [word-RAM model](/word-ram/), decomposing a syllable and computing its name take $O(1)$ time. Composition is one pass with $O(1)$ work per code point, so it takes $\Theta(n)$ time and $O(1)$ extra space besides the output.

| claim | value |
|---|---|
| decomposition of one syllable | $O(1)$ |
| composition of $n$ code points | $\Theta(n)$ |
| data | 9 constants and 67 short names, instead of 11,172 table entries |

## Properties

- **Bijective.** Each precomposed syllable has exactly one jamo sequence, and composition gives the syllable back. The test `test_every_syllable` checks all 11,172 syllables against `unicodedata.normalize` and `unicodedata.name`.
- **Same as NFC and NFD on Hangul.** On text made of jamo and syllables, composition gives NFC and decomposition gives NFD. The test `test_random_text_against_nfc_and_nfd` checks 4,000 random strings.
- **No exclusions.** No syllable is a composition exclusion, so NFC always composes a modern $L\,V$ or $L\,V\,T$ into one syllable.
- **Left to right.** A composition depends only on the last code point of the result, so the algorithm runs on a stream.

## Variants and improvements

- **Inside normalization.** The [normalization algorithm](/unicode-normalization-algorithm/) calls the decomposition when it finds a syllable in the input and the composition step when it tries to combine a starter with the next character. Its data tables then need no Hangul entries.
- **Old Hangul.** The jamo outside the modern ranges, such as the archaic consonants U+1113..U+115F, U+A960..U+A97C and the extended vowels and trailing consonants of U+D7B0..U+D7C6 and U+D7CB..U+D7FB, do not compose. A sequence with them stays a sequence of jamo, and a font must lay it out as a syllable block (D133).
- **Fillers.** U+115F HANGUL CHOSEONG FILLER and U+1160 HANGUL JUNGSEONG FILLER (D124, D127) stand for a missing L or V in a syllable block. They do not compose.

## When to use it

Use it inside any implementation of [Unicode normalization](/unicode-normalization-forms/), to avoid a table of 11,172 entries, and in tools that need the jamo of a syllable, such as Korean input methods, search by initial consonant, and spelling checkers. Use the name formula when a program must print character names without the full name list. For the visible boundaries of Korean text, use the rules of [text segmentation](/unicode-text-segmentation/), which treat a syllable block of jamo as one [grapheme cluster](/extended-grapheme-cluster/) even when it does not compose.

## Pitfalls

- **Treating U+11A7 as a trailing consonant.** $T_B$ is one below the first trailing consonant, so $t = 0$ can mean "none". Line L11 must reject U+11A7. The test `test_no_composition_cases` checks it.
- **A second trailing consonant.** An LVT syllable followed by a $T$ does not compose, even when a double consonant exists for the pair. The same test checks it.
- **V and T without L.** A vowel that does not follow a leading consonant stays a jamo, and so does a T after it.
- **Checking the range of the result.** Line L11 must test that the last code point is a syllable, in U+AC00..U+D7A3. A code point above that range can have an index divisible by 28 too.
- **The empty short name.** The leading consonant IEUNG has the empty short name, so 아 is HANGUL SYLLABLE A. Code that expects three nonempty parts gets this wrong.

## Implementations

## History

Unicode 1.1 had 6,656 Hangul syllables in another place of the codespace. Unicode 2.0 (1996) removed them and encoded all 11,172 modern syllables at U+AC00..U+D7A3 in the order that the formula of this page uses. This change is the only time Unicode moved characters, and the stability policies of later versions forbid it. The decomposition and composition formulas have been part of the standard since then, and section 3.12 gives them with sample code.

## References
