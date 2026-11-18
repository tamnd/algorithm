---
tag: 4QV0CN
kind: problem
slug: text-shaping
name: Text shaping
aliases:
- glyph shaping
area: strings/text-processing-and-typesetting
level: core
summary: Turn a run of characters of one script and font into a sequence of positioned glyphs, applying ligatures, contextual forms, reordering and kerning.
model: word-ram
complexity:
  vars: {n: the number of characters in the run, L: the number of lookups that the font applies}
  time: {worst: O(n L)}
prereqs: [unicode-code-point, extended-grapheme-cluster, kerning]
see_also: [unicode-bidirectional-algorithm, unicode-line-breaking-algorithm, knuth-plass-line-breaking, greedy-line-breaking, tex-math-layout, liang-hyphenation]
sources:
  - url: https://harfbuzz.github.io/what-is-harfbuzz.html
    title: The HarfBuzz Manual, What is HarfBuzz?
    locator: the section What is text shaping?
  - url: https://learn.microsoft.com/en-us/typography/opentype/spec/chapter2
    title: OpenType specification, OpenType Layout Common Table Formats
    locator: Features and lookups, the overview and the lookup table (lookups in LookupList order, subtables tried in order, the first match wins)
  - url: https://learn.microsoft.com/en-us/typography/opentype/spec/gsub
    title: OpenType specification, GSUB, the Glyph Substitution Table
    locator: the list of lookup types, and lookup type 4, ligature substitution
  - url: https://learn.microsoft.com/en-us/typography/opentype/spec/gpos
    title: OpenType specification, GPOS, the Glyph Positioning Table
    locator: the list of lookup types (pair adjustment, mark-to-base and the others)
---

Text shaping is the problem of turning a run of characters into the glyphs that draw it, each with a position. The run has one script, one direction and one font, and the output is a list of glyph identifiers from the font with their advances and offsets, plus a map from each glyph back to the characters it came from. The font itself holds most of the rules, as tables of substitutions and positionings, and the shaper applies them in a fixed order with some fixed logic for each script. Shaping sits between the Unicode algorithms that split text into runs and the line breaking that puts the shaped runs into lines.

## In plain words

A letter in a text file is just a number. To show it, a program must pick the picture of that letter from a font and decide where to draw it.

For English this is almost one picture per letter, side by side. But "f" and "i" can join into one picture, the letters of Arabic change their shape when they join their neighbors, and in Hindi a vowel can be drawn before the letter it follows in the text. Accents must sit on top of the right letter, and some pairs of letters look better a little closer together.

Text shaping does all of this, using the rules that the font carries.

## Definition

**Input.** A run of Unicode characters $c_1, \ldots, c_n$, with its script, its direction (left to right or right to left), its language, a font, and a set of features to turn on or off (for example the standard ligatures `liga` or kerning `kern`).

**Output.** A sequence of glyphs $g_1, \ldots, g_k$, where each glyph has:

- a glyph identifier in the font;
- an advance $(a_x, a_y)$, the move of the pen after the glyph;
- an offset $(o_x, o_y)$, a shift of the glyph from the pen position that does not move the pen;
- a cluster value, the index of the first character that the glyph came from.

The pen starts at 0, glyph $i$ is drawn at the pen position plus its offset, and then the pen moves by its advance. The number of glyphs $k$ can be smaller than $n$ (ligatures), larger (a character drawn as two glyphs), or the same.

**The steps.** An OpenType shaper does, in this order:

1. map each character to a glyph through the `cmap` table of the font, after composing or decomposing characters where the font lacks a glyph for one form;
2. for complex scripts, reorder glyphs and assign the features of each position by the rules of the script, for example the initial, medial, final and isolated forms of Arabic letters;
3. apply the substitution lookups of the GSUB table for the chosen features, which replace one glyph by one, one by many, or many by one (ligatures);
4. set each advance from the `hmtx` table of the font;
5. apply the positioning lookups of the GPOS table, such as pair kerning and the attachment of marks to base glyphs.

Within each table, the lookups run in the order of the lookup list of the font. Each lookup goes over the whole glyph sequence before the next one starts, and at each position the first subtable whose pattern matches is used.

## Variants

- **Simple scripts.** For Latin, Greek or Cyrillic text, steps 1 and 3 to 5 are enough: ligatures, kerning and mark positioning.
- **Complex scripts.** Arabic needs joining forms, Indic scripts need reordering of vowel signs and of the forms of consonant clusters, and many other scripts have their own rules. A general shaping engine, such as the Universal Shaping Engine of Microsoft, covers many scripts with one model.
- **Other font formats.** Apple Advanced Typography and Graphite put state machines or rule programs in the font, so that the font, not the shaper, holds the logic of the script.
- **Vertical text.** Some scripts are also set from top to bottom, with other glyphs and vertical advances.
- **Font fallback.** When the font has no glyph for a character, the run is split and part of it is shaped with another font.

## Examples

- **A ligature.** "office" in a font with an `ffi` ligature gives the glyphs o, ffi, c, e, with clusters 0, 1, 4, 5. A cursor placed in the ligature must use the clusters to find characters 1 to 3.
- **Kerning.** "AV" gives two glyphs, and a pair adjustment in GPOS makes the advance of A smaller, so V moves in under the arm of A. See [kerning](/kerning/).
- **A mark.** "e" followed by U+0301 COMBINING ACUTE ACCENT gives either one precomposed glyph é, or the glyph e and an accent glyph with advance 0 and an offset that a mark-to-base lookup takes from anchor points on both glyphs.
- **Arabic joining.** The same Arabic letter takes up to four forms, isolated, initial, medial or final, depending on whether it joins the letter before it and the letter after it.
- **Reordering.** In Devanagari, कि is U+0915 KA followed by U+093F VOWEL SIGN I, but the vowel sign is drawn to the left of the consonant, so the shaper moves its glyph before the glyph of KA.
- **Not shaping.** Choosing where a line ends, or the order of runs in a line of mixed directions, is not part of shaping; these are done by the [line breaking](/unicode-line-breaking-algorithm/) and [bidirectional](/unicode-bidirectional-algorithm/) algorithms around it.

## Known algorithms

| method | where the logic is | used in |
|---|---|---|
| OpenType layout with script shapers | the shaper for the script, and the GSUB and GPOS tables | HarfBuzz, DirectWrite, Core Text |
| Universal Shaping Engine | one general model of clusters, and the tables | many complex scripts in OpenType engines |
| Apple Advanced Typography | state machines in the font | Core Text |
| Graphite | rule programs in the font | Graphite engine, LibreOffice |

All of them are a pass over the glyph sequence for each lookup or rule. Each match tests a pattern of bounded length, so for a fixed font the time is $O(nL)$ for $L$ lookups, as long as no lookup grows the sequence without bound.

## Bounds

The output can be as long as the input, and every character must be read, so $\Omega(n)$ time is needed. For a fixed font, the time is $O(n)$, with a constant that depends on the number and the size of the lookups of the font. The rules of a font can be complex (contextual lookups can call other lookups), so engines limit the number of operations per run to avoid very long runs on bad fonts.

## Reductions

- Shaping needs runs of one script, direction and font. These come from the [bidirectional algorithm](/unicode-bidirectional-algorithm/), from the script property of the characters and from font selection.
- Line breaking needs the widths of the shaped words, so shaping comes before [Knuth-Plass line breaking](/knuth-plass-line-breaking/) or [greedy line breaking](/greedy-line-breaking/). A break can change the shape (for example a hyphen or a different joining form at the end of a line), so a word at a break may have to be shaped again.
- [Kerning](/kerning/) is one positioning step of shaping.
- Clusters connect glyphs to characters, in the same way that [grapheme clusters](/extended-grapheme-cluster/) connect what a user sees as one character to code points.

## Applications

- Every program that draws text: browsers, word processors, operating systems and e-book readers.
- Typesetting systems such as XeTeX and LuaTeX with HarfBuzz, so that TeX can use OpenType fonts and complex scripts.
- Text measurement, for example the width of a label or of a table cell, which depends on the shaped glyphs and not on the number of characters.

## References
