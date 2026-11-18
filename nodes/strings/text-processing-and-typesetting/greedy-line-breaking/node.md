---
tag: HF8Z28
kind: algorithm
slug: greedy-line-breaking
name: Greedy line breaking
aliases:
- first-fit line breaking
area: strings/text-processing-and-typesetting
level: intro
summary: Put as many words on each line as fit and then start a new line. With rigid or shrink-only spaces it uses the fewest lines, but it can leave very uneven lines.
solves: [optimal-text-wrapping]
model: word-ram
complexity:
  vars: {m: the number of items of the paragraph, K: the number of lines, B: the largest number of legal breaks that one scan can pass before it stops}
  time: {worst: O(m + K B), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1981
  people: [Donald E. Knuth, Michael F. Plass]
  note: Knuth and Plass named the method first fit and compared it with their total-fit method in 1981.
prereqs: [box-glue-penalty-model, greedy-algorithm]
see_also: [knuth-plass-line-breaking, printing-neatly, optimal-text-wrapping, greedy-stays-ahead, typesetting-badness, best-fit-page-breaking, unicode-line-breaking-algorithm, hyphenation-problem]
sources:
  - paper: doi:10.1002/spe.4380111102
    title: "Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software: Practice and Experience 11(11), 1119-1184, 1981"
    locator: "the first-fit method, its comparison with total fit, and the examples of bad lines that first fit makes"
  - book: isbn:0201134470
    title: "Donald E. Knuth, The TeXbook, Computers and Typesetting volume A, Addison-Wesley"
    locator: "Chapter 14, How TeX breaks paragraphs into lines"
---

Greedy line breaking fills a paragraph one line at a time: each line takes as many words as fit, and the next line starts after them. A line fits when its spaces can shrink enough to make it no wider than the column. The method never looks at later lines, so it is fast and simple, and the lines that it has made do not change when more text comes. When the spaces cannot stretch, it uses the fewest lines of all layouts with no overfull line. When the spaces can stretch, as in justified text, it can leave a line with very wide spaces, even when a better layout with the same number of lines exists. Knuth and Plass called it first fit and replaced it in TeX by the total-fit method of the [Knuth-Plass algorithm](/knuth-plass-line-breaking/).

## In plain words

Write words on a line until the next word does not fit, then go to a new line. This is what most people do by hand and what most text editors do.

It is the best way to use few lines, because each line ends as late as it can, so the next line never starts earlier than in any other layout. It is not the best way to get even lines. If a full line leaves a long word for the next line, and that word is followed by another long word that does not fit beside it, the line with the single word must stretch its spaces a lot, or it stays very short. A method that looks ahead could have moved one short word down and made both lines a little loose.

## The problem

The input is a paragraph $x_0, \ldots, x_{m-1}$ in the [box, glue and penalty model](/box-glue-penalty-model/), whose last item is a forced break, and the lengths $l_0, l_1, \ldots$ of the lines (often all equal to one $l$). A line from a break $a$ to a legal break $b$ is overfull when its width at full shrink is larger than its length, that is, when its adjustment ratio is less than $-1$. The output is a breaking $b_1 < \cdots < b_k = m - 1$ that holds every forced break. The greedy rule is: each line ends at the farthest legal break before the next forced break that does not make it overfull. With cost 1 per line, this is the [optimal text wrapping](/optimal-text-wrapping/) problem of using the fewest lines.

## The algorithm

```pseudo id=main
GREEDY-BREAK(x_0 .. x_{m-1}, l_0, l_1, ...)
L1  breaks ← empty list; a ← -1
L2  while a < m - 1 do
L3      best ← nil; l ← l_{|breaks|}
L4      for each legal break b > a, in increasing order do
L5          if the line (a, b) is not overfull at length l then
L6              best ← b
L7          if x_b is a forced break, or the line (a, b) without x_b is wider than l at full shrink, then stop the scan
L8      if best = nil then best ← the first legal break after a   ▷ the line is overfull
L9      append best to breaks; a ← best
L10 return breaks
```

The width, stretch and shrink of a line come from prefix sums over the items, so each test costs $O(1)$. Line L5 is the test "fits". Line L7 stops the scan when no later break can fit: the width at full shrink of the items before $x_b$ only grows as $b$ moves right, so once it is larger than $l$, every longer line is overfull. The test leaves out $x_b$, because a hyphen at $x_b$ has a width that a later break does not have. Line L8 handles a word that is wider than the line: the line ends at the first possible break and is overfull, as in TeX.

## Example

Take "the quick brown fox jumps over the lazy dog" with each word a box as wide as its number of letters, rigid spaces of width 1, and $l = 15$:

| line | text | width | next word |
|---|---|---|---|
| 1 | `the quick brown` | 15 | "fox" gives 19 > 15 |
| 2 | `fox jumps over` | 14 | "the" gives 18 > 15 |
| 3 | `the lazy dog` | 12 | end of the paragraph |

The words have 35 letters. On 2 lines they would need at least 7 spaces inside the lines, so 42 units, but 2 lines hold only 30. So 3 lines is the fewest, as the theorem below says.

**Stretchable spaces.** Now take the words "ab abc a abcd abcd" with glue of width 2, stretch 1 and shrink 1, $l = 8$, and the tolerance 200 of plain TeX:

| breaking | lines | $r$ of each line | badness of each line | total |
|---|---|---|---|---|
| greedy | `ab abc a` / `abcd` / `abcd` | $-1$, $\infty$, last line | 100, 10000, 0 | 10100 |
| best | `ab abc` / `a abcd` / `abcd` | $1$, $1$, last line | 100, 100, 0 | 200 |

The first greedy line has natural width 10 and shrink 2, so it just fits with $r = -1$. The second line can hold only "abcd", because "abcd abcd" is 10 wide with shrink 1. That line has no glue to stretch, so its badness is 10000. The other breaking has the same number of lines and every line within the tolerance; a search over all breakings shows it is the only one. A greedy method that tests "badness at most 200" instead of "not overfull" also fails here: no second line meets the test, so it must give an overfull or a very bad line.

## Correctness

The proof rests on two facts. First, a line that fits still fits if it starts at a later break (Lemma 1), because its content then is a final part of the old content, and every item adds a width of at least 0 at full shrink. Second, the scan of lines L4 to L7 finds the farthest break that fits (Lemma 2). Then greedy stays ahead: if $g_t$ and $o_t$ are the $t$-th breaks of the greedy breaking and of any breaking with no overfull line, then $g_t \ge o_t$ for every $t$, by induction, since the line from $g_t$ to $o_{t+1}$ fits by Lemma 1 and greedy takes the farthest break that fits. So greedy uses at most as many lines. With one length $l$, no greedy line is overfull when some breaking has no overfull line. This is the [greedy stays ahead](/greedy-stays-ahead/) argument. The full proof is in the proof file.

Lemma 1 is the reason for the condition in the summary. For the test "badness at most $\rho$", a line that starts later is shorter and must stretch more, so a good line can become a bad one, and the argument fails, as the example shows.

## Complexity

The prefix sums take $\Theta(m)$ time and space. The scan of a line visits the legal breaks from $a$ up to the first one where the line is too wide or a forced break, so at most $B + 1$ of them, and each test is $O(1)$. The time is $O(m + K B)$ for $K$ lines. In normal text, $B$ is the number of words and hyphen points that fit in one line, so the time is linear in $m$; the tests of this page count at most $2m$ tests on a paragraph of 2000 random words. The best case is $\Theta(m)$, since every item is read.

## Properties

- **Online.** Each line is fixed once its scan stops, before the rest of the paragraph is read. Adding text at the end never changes the earlier lines, which is why editors use it.
- **Fewest lines, not best lines.** It is optimal for the number of lines, in the sense of the proof, and for nothing else. It ignores the badness of the lines.
- **Stable.** A small change in the text moves line ends only from the change onward.
- **Local.** Each choice depends only on the current line, so it cannot trade a slightly worse line for a much better one later.

## Variants and improvements

- **Natural width.** Many tools test the natural width of a line instead of its width at full shrink, so the spaces never shrink. This is first fit with rigid spaces, and the theorem applies to it directly.
- **Best fit.** Among the breaks that fit, take the one whose line has the least cost, not the farthest one. The page builder of TeX works this way for pages, see [best-fit page breaking](/best-fit-page-breaking/).
- **Total fit.** Choose all breaks together to minimize the total cost: the [Knuth-Plass algorithm](/knuth-plass-line-breaking/), or [printing neatly](/printing-neatly/) for rigid spaces.
- **Hyphenation.** With the hyphen points of a word as flagged penalties, the greedy scan can end a line inside a word. The points come from a method for the [hyphenation problem](/hyphenation-problem/).
- **Break opportunities of Unicode.** For text in many scripts, the legal breaks come from the [Unicode line breaking algorithm](/unicode-line-breaking-algorithm/), and the greedy rule picks among them.

## When to use it

Use it when speed and stable lines matter more than even spacing: text editors and terminals, ragged-right text, code and plain text wrapping, and documents that are edited while they are shown. For justified text of high quality, or when hyphens should be few, use the [Knuth-Plass algorithm](/knuth-plass-line-breaking/), which looks at the whole paragraph.

## Pitfalls

- **"Fewest lines" with a badness test.** The theorem holds for the test "not overfull". With a tolerance on the badness, greedy can fail to find a breaking that exists, as in the example.
- **Different line lengths.** With lengths that change from line to line, greedy still uses at most as many lines as any breaking with no overfull line, but its own lines can be overfull: being ahead, it can reach a short line with more text than the other breaking puts there.
- **Stopping at the first line that does not fit.** A hyphen can be wider than the rest of its word. Then the break at the hyphen does not fit, but the break after the word does. Line L7 stops only when the width without $x_b$ is too large, and the test `test_greedy_takes_the_farthest_break_with_varying_lengths` checks that no later break fits.
- **A word wider than the line.** No break fits, so the loop must still move forward; line L8 makes an overfull line instead of an endless loop.
- **The glue at a break.** The glue at the break and the glue right after it belong to no line. Counting them makes some lines look too wide.

## Implementations

## History

Filling each line before starting the next is how text is set by hand and in most simple programs. Knuth and Plass gave it the name first fit in 1981, showed paragraphs where it makes much worse lines than total fit, and made total fit the method of TeX. The fact that first fit uses the fewest lines is a standard example of the greedy stays ahead argument.

## References
