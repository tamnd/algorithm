---
tag: 2X2V4H
kind: algorithm
slug: unicode-bidirectional-algorithm
name: Unicode bidirectional algorithm
aliases:
- UBA
- bidi algorithm
- UAX 9
area: strings/text-processing-and-typesetting
level: core
summary: "Give each character of mixed left-to-right and right-to-left text an embedding level by the explicit, weak, neutral and implicit rules of UAX 9, then reverse runs of each line by level."
model: word-ram
complexity:
  vars: {n: the length of the paragraph in code points}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [unicode-code-point, stack]
see_also: [unicode-line-breaking-algorithm, text-shaping, unicode-text-segmentation, unicode-confusable-detection, balanced-parentheses, canonical-equivalence]
sources:
  - url: https://www.unicode.org/reports/tr9/tr9-50.html
    title: "Manish Goregaokar and Robin Leroy (editors), Unicode Standard Annex 9, Unicode Bidirectional Algorithm, revision 50, 2024-09-02"
    locator: "Sections 3.1 (definitions BD1 to BD16), 3.3.1 to 3.3.6 (rules P1 to I2), 3.4 (rules L1 to L4), 4.4 (conformance testing) and 7 (mirroring)"
  - url: https://www.unicode.org/Public/16.0.0/ucd/BidiCharacterTest.txt
    title: "BidiCharacterTest-16.0.0.txt, Unicode Character Database"
    locator: the conformance test lines
  - url: https://www.unicode.org/Public/16.0.0/ucd/BidiBrackets.txt
    title: "BidiBrackets-16.0.0.txt, Unicode Character Database"
    locator: the Bidi_Paired_Bracket and Bidi_Paired_Bracket_Type properties
  - url: https://www.unicode.org/Public/16.0.0/ucd/extracted/DerivedBidiClass.txt
    title: "DerivedBidiClass-16.0.0.txt, Unicode Character Database"
    locator: "the Bidi_Class property, with the default values of unassigned code points"
---

The Unicode bidirectional algorithm (UBA) finds the display order of text that mixes left-to-right scripts, such as Latin, with right-to-left scripts, such as Hebrew and Arabic. It is Unicode Standard Annex 9 (UAX 9). Text is stored in logical order, the order in which it is read and typed. The algorithm gives each character an embedding level: even levels are left to right and odd levels are right to left. It then reverses runs of characters by level to get the visual order of each line. The levels come from the Bidi_Class of each [code point](/unicode-code-point/), from explicit formatting characters such as RLI and PDI, and from rules for numbers, neutral characters and paired brackets.

## In plain words

Hebrew and Arabic are written from right to left, but a Hebrew sentence can contain an English name or a number, which still go from left to right. The computer stores the text in the order that a person reads it. To show it, the program must decide, for each character, which way it runs, and then flip the right-to-left parts. Letters are easy: they carry their own direction. Spaces, punctuation and brackets have no direction, so they take one from their neighbours. Digits are special: a number stays left to right even inside Hebrew. Writers can also insert invisible control characters that say "this part is right to left" or "keep this part apart from the text around it". The algorithm gives every character a level number, and then reverses each stretch of text at an odd level.

## The problem

The input is a paragraph $s = s[0] \cdots s[n-1]$ of code points and a paragraph direction: left to right, right to left, or automatic. Each code point has a Bidi_Class: strong (L, R, AL), weak (EN, ES, ET, AN, CS, NSM, BN), neutral (B, S, WS, ON) or explicit formatting (LRE, RLE, LRO, RLO, PDF, LRI, RLI, FSI, PDI). The output is the paragraph level $p$, a level for each code point, and for each line the visual order: a permutation of the positions of the line from left to right. The explicit formatting characters other than the isolates, and the BN characters, are removed by rule X9 and get no level.

The levels must satisfy the rules of UAX 9 in their order: P2 and P3 for the paragraph level, X1 to X10 for the explicit levels, W1 to W7, N0 to N2, I1 and I2 for the implicit levels, and L1 to L4 for each line.

## The algorithm

The algorithm makes a fixed number of passes over the text:

- **P2, P3.** In automatic mode, the paragraph level is 1 if the first strong character, outside isolates, is R or AL, and 0 otherwise.
- **X1 to X8.** A [stack](/stack/) of directional status entries holds a level, an override status and an isolate flag. The embeddings and overrides (LRE, RLE, LRO, RLO) push an entry with the next even or odd level, PDF pops one, the isolates (LRI, RLI, FSI) push an entry that only the matching PDI pops, and each other character gets the level of the top entry. Levels stop at max_depth = 125; counters of overflow embeddings and overflow isolates keep the pushes and pops balanced beyond that depth. FSI looks at the text up to its matching PDI and acts as RLI or LRI by rules P2 and P3.
- **X9, X10.** The removed characters drop out. The rest splits into level runs, and a level run that ends with an isolate initiator joins the level run that starts with its matching PDI. These chains are the isolating run sequences (BD13). Each one gets a start type sos and an end type eos from the higher of its level and the level on the other side.
- **W1 to W7.** In each isolating run sequence, a mark (NSM) takes the type before it, a European number after Arabic letters becomes an Arabic number, AL becomes R, separators between numbers join them, terminators next to European numbers join them, other separators become neutral, and a European number after L becomes L.
- **N0.** Paired brackets (BD16) are found with a stack of 63 entries. A pair takes the embedding direction if a strong type of that direction is inside it, or the opposite direction if only the opposite direction is inside and the context before the pair has it too.
- **N1, N2.** A run of neutrals between two strong types of the same direction takes that direction, where numbers count as R. Other neutrals take the embedding direction.
- **I1, I2.** At an even level, R goes up by one and numbers by two. At an odd level, L and numbers go up by one.
- **L1 to L4.** On each line, separators and trailing white space go back to the paragraph level. Then, from the highest level down to the lowest odd level, every maximal run at that level or higher is reversed. L3 and L4 handle combining marks and mirrored glyphs.

```pseudo id=main
BIDI(s, d)                                  ▷ one paragraph shown as one line
L1  t[i] <- Bidi_Class(s[i]) for each i
L2  p <- d, or the level of rules P2 and P3 if d is automatic
L3  lev, t <- the levels and overrides of rules X1 to X8, with the directional status stack
L4  remove the characters of rule X9
L5  for each isolating run sequence S of rule X10, with its sos and eos, do
L6      apply W1 to W7 to the types of S
L7      apply N0 to the bracket pairs of S, found by BD16
L8      apply N1 and N2 to the runs of neutrals of S
L9      apply I1 and I2 to the levels of S
L10 apply rule L1: separators and trailing white space get level p
L11 order <- the kept positions in logical order
L12 for v <- the highest level down to the lowest odd level do reverse each maximal run of order with levels >= v
L13 return p, lev, order
```

## Example

Take the text `ab אב 12 cd` in a left-to-right paragraph, so $p = 0$. The classes are L L WS R R WS EN EN WS L L. There are no explicit formatting characters, so the whole text is one isolating run sequence at level 0, with sos = eos = L.

- W7 looks back from each EN for a strong type. It finds R, so the digits stay EN.
- N1: the space between `אב` and `12` lies between R and EN, and EN counts as R, so it becomes R. The space between `ab` and `אב` lies between L and R, and the space between `12` and `cd` lies between EN and L. They take the embedding direction L by N2.
- I1 at level 0: R goes to level 1 and EN goes to level 2. The levels are 0 0 0 1 1 1 2 2 0 0 0.
- L2: at level 2, the run `12` is reversed, which gives `21`. At level 1, the run `אב 21` is reversed, which gives `12 בא`.

The visual order is `ab 12 בא cd`. A reader of Hebrew reads the middle part from right to left: first `אב`, then `12`, which is the logical order.

For brackets, take `ab (אב) cd` with $p = 0$. The pair contains only R, which is opposite to the embedding direction L. The first strong type before the pair is L from `ab`, so by N0 the brackets take the embedding direction L and keep level 0. The result is `ab (בא) cd`, and the brackets stay outside the reversed Hebrew word.

## Correctness

The rules of UAX 9 define the result, so the algorithm is correct if each pass computes its rules exactly. The [proof](proofs/correctness.md) shows that the stack of line L3 gives the levels of X1 to X8, that the isolating run sequences of line L5 are those of BD13, that the passes of lines L6 to L9 apply each rule to the whole sequence before the next rule, as the annex requires, and that line L12 is rule L2. The tests run the first 40 lines of BidiCharacterTest.txt, a direct reference for text without explicit formatting, and a recursive form of rule L2 on random levels.

## Complexity

Each of the passes P2, X1 to X10, W1 to W7, N1, N2, I1, I2 and L1 takes $\Theta(n)$ time. The PDI pops of X6a remove at most as many entries as were pushed. N0 looks inside each bracket pair, and a position is inside at most 63 open pairs at a time, because BD16 stops at 63 open brackets; the search before an opening bracket stops at the first strong type, and the brackets of each pair that N0 resolves become strong, so two of these searches never cover the same position. Rule L2 makes at most 126 passes, one per level. So the time is $\Theta(n)$ with a constant that depends on max_depth, and the extra space is $\Theta(n)$ for the types and levels.

## Properties

- The levels lie between the paragraph level and max_depth + 1 = 126.
- Text with only L characters, European digits and neutrals in a left-to-right paragraph keeps its order.
- Isolates (LRI, RLI, FSI with PDI) do not affect the text around them: the text outside sees the isolate as one neutral character. Embeddings (LRE, RLE) do affect it.
- The levels are resolved per paragraph, but the reordering L1 to L4 is per line, after [line breaking](/unicode-line-breaking-algorithm/).
- Unmatched PDF and PDI characters are ignored, and a paragraph separator closes every open embedding and isolate.

## Variants and improvements

- Higher-level protocols (HL1 to HL6 of UAX 9) can override parts of the algorithm, for example to set the paragraph level from outside or to treat some characters as isolated. HTML and CSS use them through the dir attribute, the bdi element and unicode-bidi.
- Section 5.2 of UAX 9 describes how to keep the BN and explicit formatting characters in the text, with levels for them, instead of removing them by X9.
- Before Unicode 6.3, the annex had no isolates and no rule N0. Older implementations give different results for brackets and for inserted text of unknown direction.

## When to use it

Use it whenever right-to-left text is shown: in text editors, terminals, browsers and user interfaces. Wrap inserted text whose direction is not known, such as user names and file names, in FSI and PDI, so that it cannot change the order of the text around it. A [shaping engine](/text-shaping/) runs on the runs of one level and one script that the algorithm produces.

## Pitfalls

- Do not store text in visual order. Store it in logical order and run the algorithm at display time.
- Run line breaking on the logical text, and apply L1 to L4 to each line. If a whole paragraph is reordered first and then broken into lines, the lines come out in the wrong order.
- Rule L4 mirrors the glyphs of characters such as brackets at odd levels. The code point stays `(`, but the glyph is `)`. The visual order in the tests does not include this mirroring.
- Arabic-Indic digits are AN and European digits are EN, and W2 turns EN into AN after Arabic letters. Numbers next to Arabic text are not handled the same way as numbers next to Hebrew text.
- BD16 returns no pairs at all, not only the first 63, when the stack of opening brackets overflows.
- Override characters such as RLO can make a file name or a line of source code look different from its logical order. Tools that show such text should mark these characters. This is a problem of the same kind as the one that [confusable detection](/unicode-confusable-detection/) handles.

## Implementations

## History

The bidirectional algorithm has been part of the Unicode Standard since its early versions, and UAX 9 gets a new revision with each version. Directional isolates were introduced in Unicode 6.3 (2013), because embeddings often had too strong an effect on the text around them. The paired bracket rule N0 came in the same version. Revision 50, by Manish Goregaokar and Robin Leroy, is the version for Unicode 16.0.0.

## References
