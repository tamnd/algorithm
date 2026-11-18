---
tag: D4NEZV
kind: algorithm
slug: unicode-line-breaking-algorithm
name: Unicode line breaking algorithm
aliases:
- UAX 14
- line break opportunities
area: strings/text-processing-and-typesetting
level: core
summary: "Find the positions where a line may or must break, with the ordered rules LB1 to LB31 of UAX 14 on line break classes. A line breaker then picks some of these positions."
model: word-ram
complexity:
  vars: {n: the length of the text in code points}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [unicode-code-point]
see_also: [greedy-line-breaking, knuth-plass-line-breaking, unicode-text-segmentation, unicode-bidirectional-algorithm, hyphenation-problem, box-glue-penalty-model, text-shaping, regular-expression]
sources:
  - url: https://www.unicode.org/reports/tr14/tr14-53.html
    title: "Robin Leroy (editor), Unicode Standard Annex 14, Unicode Line Breaking Algorithm, revision 53, 2024-09-02"
    locator: "Sections 5 (Line Breaking Properties), 6.1 and 6.2 (the rules LB1 to LB31), 10 (Testing), 11 (History) and Modifications"
  - url: https://www.unicode.org/Public/16.0.0/ucd/LineBreak.txt
    title: "LineBreak-16.0.0.txt, Unicode Character Database"
    locator: the Line_Break property of each code point
  - url: https://www.unicode.org/Public/16.0.0/ucd/auxiliary/LineBreakTest.txt
    title: "LineBreakTest-16.0.0.txt, Unicode Character Database"
    locator: the conformance test lines
  - url: https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-data.txt
    title: "emoji-data-16.0.0.txt, Unicode Character Database"
    locator: the Extended_Pictographic property (rule LB30b)
---

The Unicode line breaking algorithm finds the positions in a text where a line may break, and the positions where it must break. It is Unicode Standard Annex 14 (UAX 14). Each [code point](/unicode-code-point/) has a line break class, such as AL for letters, NU for digits, OP for opening punctuation or SP for the space. At each position between two code points, a fixed list of rules is tried in order, and the first rule that matches decides: no break (×), a break opportunity (÷) or a mandatory break (!). The output is a set of break opportunities, not a layout. A line breaker, such as the [greedy method](/greedy-line-breaking/) or [Knuth and Plass](/knuth-plass-line-breaking/), then picks the breaks it takes from this set.

## In plain words

When a program wraps text to fit a width, it must know where a line can end. Between two words is usually fine, inside a word is not, and many cases are less clear. A closing bracket must stay with the text before it. A currency sign must stay with its number, and "12.50" must not split at the full stop. A space before a French closing guillemet must not leave the guillemet alone at the start of the next line. In Chinese, a line can break after most characters, but not before a comma. The algorithm gives each character a class and has a long list of rules, each of which says "break here" or "do not break here" for a pattern of classes. The first rule that fits wins. The result is the places where a break is allowed, and those where a new line is required.

## The problem

The input is a string $s = s[0] \cdots s[n-1]$ of code points with $n \ge 1$. Each code point $c$ has a value $\mathrm{lb}(c)$ of the Line_Break property, from the file LineBreak.txt. The output is the list of positions $i$ with $1 \le i \le n$ at which a break is allowed, each marked as mandatory or not. Position $i$ is between $s[i-1]$ and $s[i]$.

The rules have the form "left side, action, right side", for example `OP SP* ×` (rule LB14: no break after an opening bracket, even after spaces) or `SP ÷` (rule LB18: break after spaces). The left side is a pattern on the text before the position and the right side a pattern on the text after it. At each position, the rules are tried in the order of their numbers, and the action of the first one whose two sides both match is the answer. Rule LB2 says there is no break at the start of the text, rule LB3 says there is always a break at the end, and rule LB31 (`ALL ÷`, `÷ ALL`) makes a break wherever no earlier rule matched.

Two rules are not of this form. Rule LB1 resolves some classes that the algorithm does not handle directly: AI, SG and XX become AL, CJ becomes NS, and SA (Thai, Lao and other scripts that need a dictionary) becomes CM for marks and AL for the rest. Rules LB9 and LB10 handle combining marks: after LB4 to LB8a, a sequence `X (CM | ZWJ)*` counts as one character of class X, unless X is BK, CR, LF, NL, SP or ZW, and any CM or ZWJ that remains counts as AL. The rules from LB11 on see these units.

## The algorithm

Most rules look at one class on each side of the position. Some look further: LB14, LB15a, LB16 and LB17 skip back over spaces, LB25 matches numbers such as `NU (SY | IS)* CL × PO`, LB30a counts regional indicators, and LB15c, LB19a, LB20a and LB28a need a code point two places away. All these contexts are either a fixed number of units, or a run of one class that can be found by a single step back.

```pseudo id=main
LINE-BREAKS(s)                             ▷ s has n >= 1 code points
L1  c[i] <- the class of s[i] after LB1, for i <- 0 to n - 1
L2  U <- the units of LB9 and LB10; unit[i] <- the unit of s[i]
L3  B <- empty list
L4  for i <- 1 to n - 1 do
L5      if c[i-1] in {BK, LF, NL} or (c[i-1] = CR and c[i] ≠ LF) then append (i, mandatory) to B      ▷ LB4, LB5
L6      else if c[i-1] = CR or c[i] in {BK, CR, LF, NL, SP, ZW} then do nothing    ▷ LB5, LB6, LB7
L7      else if s[0 .. i-1] ends with ZW SP* then append (i, allowed) to B         ▷ LB8
L8      else if c[i-1] = ZWJ or unit[i] = unit[i-1] then do nothing              ▷ LB8a, LB9
L9      else if the first rule of LB11 to LB31 that matches at the unit border unit[i] is ÷ then append (i, allowed) to B
L10 append (n, mandatory) to B; return B
```

Line L9 is a chain of tests in rule order. Each test looks at the classes of the units $U[k-1]$ and $U[k]$ with $k = \mathrm{unit}[i]$, and some tests also look at $U[k-2]$, $U[k+1]$, $U[k+2]$, or back over a run of SP, SY or IS units. The implementation keeps the length of the run of RI units that ends at each unit, so LB30a takes constant time. Some rules need more than the class. LB15a and LB15b need the general category (Pi or Pf) of a quotation mark, and LB19a, LB21a and LB30 need the East Asian Width, through the set `$EastAsian` of the code points with width F, W or H.

## Example

Take the text `He said « oui » to $(12.50) for well-known goods.` The algorithm gives these pieces, with a break opportunity after each one:

`He ` | `said ` | `« oui » ` | `to ` | `$(12.50) ` | `for ` | `well-` | `known ` | `goods.`

- After each space, LB18 (`SP ÷`) gives a break, and LB7 (`× SP`) keeps each space with the word before it.
- After `« `, there is no break. The guillemet U+00AB has class QU and category Pi, and LB15a says `(sot | BK | CR | LF | NL | OP | QU | GL | SP | ZW) [\p{Pi}&QU] SP* ×`. Before ` »`, LB15b gives no break, because U+00BB is QU with category Pf and a space follows it.
- In `$(12.50)`, LB25 gives `PR × OP NU`, LB14 gives `OP ×`, LB15d gives `× IS` before the full stop, LB25 gives `IS × NU` after it, and LB13 gives `× CP` before the closing parenthesis.
- In `well-known`, LB21 (`× HY`) keeps the hyphen with `well`, and LB31 allows a break after it. LB20a does not apply, because this hyphen does not start a word.
- The end of the text is a mandatory break by LB3.

LineBreakTest.txt has the line `× 0073 × 0074 × 0061 × 0072 × 0074 × 0020 ÷ 002E × 0037 × 0038 × 0039 × 0020 ÷ 0065 × 006E × 0064 ÷`, that is `start .789 end`. Here LB15c (`SP ÷ IS NU`) gives a break before `.789`, and LB25 keeps `.789` together.

## Correctness

The rules define the answer: at each position, the action of the first matching rule. The algorithm is correct if, at each position, its chain of tests gives the action of that rule. Lines L5 to L8 test the rules LB4 to LB9 in order, on the code points, as the annex writes them. Each test in line L9 holds exactly when the left and right patterns of its rule match at the unit border, and the tests come in rule order, so the first test that holds belongs to the first rule that matches. The [proof](proofs/correctness.md) checks this for the rules with long contexts. The test file compares the implementation with the lines of LineBreakTest.txt, and with a second implementation that stores each rule as a pair of regular expressions and tries them in order on random strings.

## Complexity

Line L1 and line L2 take $\Theta(n)$ time. For each position, line L9 makes a constant number of tests, except the steps back over a run of SP, SY or IS units. A step back over spaces happens only at the position after the last space of a run, because positions before a space stop at line L6. A step back over SY or IS units happens only at a position where the next unit is not SY or IS, because LB13 and LB15d decide the positions before them. So each run is walked once from its end, and the total time is $\Theta(n)$. The classes and the units take $\Theta(n)$ extra space. A streaming form keeps only a bounded window plus counters for the runs, so it needs $O(1)$ space if the output goes out as it is found.

## Properties

- The result is a function of the classes, the categories Pi and Pf, and the East Asian Width. It does not depend on fonts, widths or the line length.
- Position $n$ is always a mandatory break and position 0 is never a break. The other mandatory breaks are the ends of the lines of the input, such as the positions after a line feed.
- CR LF counts as one hard break, after the LF.
- Spaces stay at the end of a line: there is never a break before a space (LB7), so a break comes after the last space of a run.
- A break never falls inside a sequence `X CM*` of a base and its combining marks, except where X is a space or a control (LB9).
- Rules from LB11 on look only at the units of LB9 and LB10, so a combining mark is transparent to them.

## Variants and improvements

- Older revisions of UAX 14 gave a pair table: for each pair of classes before and after the position, an action, plus special handling for spaces and combining marks. Section 7 of revision 53 now says "Deleted. (Formerly was: Pair Table-Based Implementation)", because several rules need more context than a pair.
- Tailoring is allowed for many rules and classes. Common tailorings resolve AI to ID in an East Asian context, resolve CJ to ID for loose Japanese line breaking, or keep words together in Korean. The CSS properties line-break and word-break select such tailorings.
- For SA scripts (Thai, Lao, Khmer, Myanmar) a real implementation finds the word boundaries with a dictionary, for example with [text segmentation by dynamic programming](/text-segmentation/), and adds them as break opportunities.
- [Hyphenation](/hyphenation-problem/) adds break opportunities inside words, each with a hyphen and a penalty, for line breakers that use the [box, glue and penalty model](/box-glue-penalty-model/).
- The rules can be compiled into a [regular expression](/regular-expression/) or a state machine over the classes, as for the rules of [UAX 29](/unicode-text-segmentation/).

## When to use it

Use it in every program that wraps Unicode text: editors, terminals, browsers, e-book readers and typesetting systems. It gives the candidate positions, and a line breaker such as the greedy method or Knuth-Plass chooses among them by width. Text inside code or identifiers can need other rules, and dictionary scripts need a word segmenter in addition.

## Pitfalls

- The algorithm does not choose line breaks. A program that breaks at every opportunity puts each word on its own line.
- Do not measure the trailing spaces of a line. They stay on the line before the break and do not count for the width in most layouts.
- Without a dictionary, LB1 resolves SA to AL, so a Thai sentence gets no break opportunities between its words and must be cut at the margin by force.
- A combining mark after a space does not attach to the space. By LB10 it counts as AL, and LB18 allows a break between the space and the mark.
- Quotation marks need care. LB19 forbids a break before a QU that is not Pi and after a QU that is not Pf. For the other cases, LB19a forbids the break unless East Asian characters are on both sides of the quotation mark. Code that treats all QU the same gives wrong breaks in Chinese text.
- Apply the rules to the text in logical order, before the [bidirectional algorithm](/unicode-bidirectional-algorithm/) reorders each line for display.
- The rules change with each version of Unicode. Revision 53 added LB20a and LB19a. Keep the version of the rules and of LineBreak.txt the same, and run LineBreakTest.txt of that version.

## Implementations

## History

UAX 14 was published in 1999 with Unicode 3.0.0. The annex says that it started with 29 line break classes and 23 rules that could be written as a pair table, with some special handling for combining marks and spaces. Now it has 48 classes and more than 40 rules, and many of them use a context that can be several characters away from the position. In Unicode 5.0 the rules were renumbered to reduce the number of letter suffixes on the rule numbers. Revision 53, for Unicode 16.0.0, added LB20a to keep a word-initial hyphen with its word, and changed LB19 and added LB19a for quotation marks in Simplified Chinese.

## References
