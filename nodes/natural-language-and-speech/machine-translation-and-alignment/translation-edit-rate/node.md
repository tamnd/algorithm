---
tag: EWE8J4
kind: algorithm
slug: translation-edit-rate
name: Translation edit rate
aliases:
- TER
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Word insertions, deletions, substitutions and block shifts from a translation to its closest reference, over the reference length. Greedy shifts make it an upper bound on the fewest edits.
model: word-ram
complexity:
  vars: {n: "the larger of the hypothesis length and the reference length, in words"}
  time: {worst: "O(n^6)"}
  space: {extra: "O(n²)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Matthew Snover, Bonnie Dorr, Richard Schwartz, Linnea Micciulla, John Makhoul]
  note: Snover and colleagues defined TER and the human-targeted HTER at AMTA 2006, for the DARPA GALE evaluations. Their tool tercom finds the shifts greedily.
prereqs: [edit-distance, machine-translation]
see_also: [wagner-fischer-algorithm, word-error-rate, bleu, chrf, comet-metric, np-complete, damerau-levenshtein-distance, traceback]
sources:
  - paper: "Matthew Snover, Bonnie Dorr, Richard Schwartz, Linnea Micciulla and John Makhoul, A Study of Translation Edit Rate with Targeted Human Annotation, Proceedings of AMTA 2006, pages 223 to 231"
    title: Snover et al. 2006
    locator: "Section 3, pages 225 and 226 (the definition, the example with 4 edits over 13 words, the three constraints on shifts and Algorithm 1, the greedy search), Section 4 (HTER)"
  - paper: doi:10.1007/3-540-45452-7_9
    title: Dana Shapira and James A. Storer, Edit Distance with Move Operations, CPM 2002, LNCS 2373, pages 85 to 98
    locator: the NP-completeness of edit distance with block moves, and a greedy approximation
  - paper: doi:10.1016/S0304-3975(96)00268-X
    title: Daniel Lopresti and Andrew Tomkins, Block edit models for approximate string matching, Theoretical Computer Science 181(1), 1997, pages 159 to 179
    locator: the NP-completeness of several block edit models
  - paper: doi:10.18653/v1/W18-6319
    title: Matt Post, A Call for Clarity in Reporting BLEU Scores, Third Conference on Machine Translation (WMT), 2018, pages 186 to 191
    locator: sacreBLEU, which includes a port of tercom
---

Translation edit rate (TER) counts the word edits needed to turn a [machine translation](/machine-translation/) output into a reference translation, and divides by the reference length. The edits are the insertion, deletion and substitution of one word, as in [edit distance](/edit-distance/), plus the shift of a block of words to another place, each at cost 1. Lower is better, 0 means an exact match, and the value can exceed 1. Finding the fewest edits with shifts is NP-hard, so TER chooses the shifts greedily, and the computed value is an upper bound on the true minimum.

## In plain words

Take the machine output and a human translation of the same sentence. Count how many small changes a person would make to turn the output into the human translation: put a word in, take a word out, change one word into another, or move a group of words to another place. Each change counts 1. Divide the count by the number of words in the human translation.

Moving a group of words counts as one change, so an output with the right phrases in the wrong order is not punished as hard as by plain edit distance.

The search for moves is greedy. It keeps making the move that helps most, while some move helps. It can miss a cheaper set of moves, so the count can be a little too high, but never below the true fewest changes.

## The problem

A hypothesis $h$ and a reference $r$ are lists of words. The allowed edits on $h$ are: insert a word, delete a word, substitute a word, and shift a block of consecutive words to another position. Each costs 1. TER of a hypothesis with references $r_1, \ldots, r_K$ is

$$\mathrm{TER} = \frac{\min_k \mathrm{edits}(h, r_k)}{\frac{1}{K}\sum_k |r_k|},$$

the fewest edits to the closest reference over the mean reference length (Snover et al. 2006, Section 3). At the corpus level, sacreBLEU divides the sum of the edits by the sum of the mean reference lengths. Lower is better. The range is from 0 up; a long wrong hypothesis needs more edits than the reference has words, so TER can exceed 1.

The exact minimum of $\mathrm{edits}(h, r)$ is hard: edit distance with block moves is NP-complete (Shapira and Storer 2002), and Snover et al. cite this. TER as defined in practice is the value of the greedy search below. It is an upper bound on the minimum.

**Tokenization.** The words are the white-space tokens of the text. In the paper, punctuation marks count as words and a difference of case counts as an error, so the text must be tokenized first. sacreBLEU by default ignores case and splits on white space only, and it has options for punctuation and tokenization.

## The algorithm

EDIT-DISTANCE is the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) on words with a [traceback](/traceback/). It returns the distance $d$ and flags, for one optimal alignment, which words of $h'$ and of $r$ are errors (not matched with an equal word). SHIFT$(h', i, k, p)$ removes the block $h'[i .. i+k-1]$ and puts it back so that it starts at index $p$.

```pseudo id=main
TER(h, R)                          ▷ R: the references
L1  best ← +∞
L2  for each reference r in R do
L3      h' ← h; s ← 0
L4      (d, errors) ← EDIT-DISTANCE(h', r)
L5      loop
L6          G ← the blocks (i, k) of h' that equal some r[j .. j+k-1], with an error word in both
L7          for each block in G and each destination p ≠ i do d' ← EDIT-DISTANCE(SHIFT(h', i, k, p), r)
L8          pick the try with the largest d - d', then the largest k, the smallest i, the smallest p
L9          if no try has d - d' ≥ 1 then leave the loop
L10         h' ← SHIFT(h', i, k, p); s ← s + 1
L11         (d, errors) ← EDIT-DISTANCE(h', r)
L12     best ← min(best, s + d)
L13 ℓ ← the mean length of the references in R
L14 if ℓ = 0 then return 0 if best = 0, else 1
L15 return best / ℓ
```

Line L6 is how the paper limits the shifts. Snover et al. ask that (1) the shifted words match the reference words at the destination exactly, (2) the words at the old place do not already match the reference, and (3) the reference words at the destination are not already matched. Line L6 keeps (1) as "the block occurs in $r$" and checks (2) and (3) with the error flags of one optimal alignment, as the tercom port of sacreBLEU does. Line L9 is the greedy rule of Algorithm 1 of the paper: a shift is applied while it lowers the edit distance, even by only 1, which leaves the total count unchanged.

**Limits in tercom.** tercom and sacreBLEU try blocks of at most 10 words, moved at most 50 positions, and compute the edit distance in a beam of width 25. This implementation tries every block and every destination, so on long sentences it can find shifts that tercom does not, and its value can differ from tercom.

## Example

The example of Snover et al. (Section 3), lowercased:

- reference: "saudi arabia denied this week information published in the american new york times" (13 words)
- hypothesis: "this week the saudis denied information published in the new york times" (12 words)

The plain edit distance is 6. The greedy search shifts "this week" to after "denied", which gives "the saudis denied this week information published in the new york times". Now three edits remain: substitute "the" by "saudi", "saudis" by "arabia", and insert "american". So TER = (1 + 3)/13 = 4/13 = 0.31.

A second example from the paper: for the reference "a b c d e f c" and the hypothesis "a d e b c f", the shift of "b c" to after "a" gives "a b c d e f", and one insertion finishes the job. TER counts 2 edits, against an edit distance of 4.

**Greedy is not optimal.** For $h$ = "a a b b" and $r$ = "b c c a", the edit distance is 4. Moving "b b" to the front gives "b b a a" at distance 2, so 3 edits suffice. But "b b" does not occur in $r$, so line L6 does not allow it. The search moves "a" to the end (distance 3) and then "b" to the front (distance 2), and reports $2 + 2 = 4$ edits.

## Correctness

The claim is that for each reference the search ends and returns the cost $e$ of a real sequence of edits from $h$ to $r$, with $\mathrm{OPT} \le e \le \mathrm{ED}(h, r)$. The search ends because each applied shift lowers the edit distance by at least 1, so there are at most $\mathrm{ED}(h, r)$ shifts. The shifts followed by an optimal alignment of $h'$ with $r$ are a valid sequence of $e$ edits, which gives the lower bound. Each shift adds 1 to $s$ and takes at least 1 from $d$, which gives the upper bound. These are theorems; the full proof is in the proofs file.

The value is not exact: the example above has $e = 4$ and $\mathrm{OPT} = 3$. How close the greedy count is to the minimum on real text is not known in general.

## Complexity

In the [word RAM](/word-ram/) model with words compared in $O(1)$, let $n$ be the larger of the two lengths. One round tries $O(n^2)$ blocks with $O(n)$ destinations each, and each try costs an $O(n^2)$ edit distance, so a round costs $O(n^5)$. There are at most $n$ rounds with a shift, so the worst case is $O(n^6)$ per reference, and $K$ references multiply it by $K$. The space is the $O(n^2)$ table. tercom's limits of 10 words per block and 50 positions per move, and its beam, bring a round down to $O(n^2)$ tries of $O(n)$ each in practice. Snover et al. state the beam cuts the edit distance from $O(n^2)$ to $O(n)$.

## Properties

- **Direction and range.** Lower is better. The value is 0 for an exact match and has no fixed upper limit.
- **Sentence and corpus.** It is defined per sentence. The corpus value divides the summed edits by the summed lengths, so it is not the mean of the sentence values.
- **An upper bound.** The greedy count is at least the fewest edits and at most the plain edit distance (a theorem).
- **Not symmetric.** The length in the denominator is the reference length, so exchanging the hypothesis and the reference changes the value.
- **Word level.** A wrong word ending is a full substitution, unlike in [chrF](/chrf/).
- **Several references.** The edits are counted to the closest reference only, but the length is the mean of all of them.

## Variants and improvements

- **HTER.** Human-targeted TER (Section 4 of the paper): a fluent speaker edits the output into a correct translation with as few changes as possible, and TER is computed against that targeted reference. It measures the post-editing work and is expensive.
- **No shifts.** Without lines L5 to L11, TER becomes the [word error rate](/word-error-rate/) of speech recognition: the edit distance over the reference length.
- **Normalization and case.** tercom and sacreBLEU have options for case, punctuation removal and a tokenizer for Asian scripts. Each option gives another number.
- **Exact or approximate moves.** Shapira and Storer (2002) give a greedy algorithm with an $O(\log n)$ approximation factor for a restricted form of moves. TER does not use it.
- **Other scores.** [BLEU](/bleu/) and [chrF](/chrf/) count n-grams, and [COMET](/comet-metric/) is a trained model.

## When to use it

Use TER when the question is how much work it takes to fix the output, for example in post-editing studies, where HTER is the standard. It is also reported next to BLEU and chrF in evaluation campaigns. Report the tool and its options, since the shift search and the normalization change the value. Do not treat it as an exact minimum, and do not compare TER from tools with different shift limits.

## Pitfalls

- **Exact minimum.** The value is a greedy upper bound. Claims that TER is the fewest edits are wrong in general.
- **Different tools.** tercom, sacreBLEU and other ports differ in shift limits, tie rules and normalization, so their values can differ on the same text.
- **Case.** The paper counts a case difference as an edit, while tercom and sacreBLEU ignore case unless asked. State which.
- **Empty reference.** The ratio has a zero denominator. sacreBLEU returns 1 if there are edits and 0 if not; this implementation does the same.
- **Higher is worse.** Unlike BLEU and chrF, a lower TER is better. Tables that mix them need a clear direction for each column.
- **Long sentences.** Without limits, the search is $O(n^6)$. Use the tercom limits for long text.

## Implementations

## History

TER grew out of word error rate and of edit distances with moves. Snover, Dorr, Schwartz, Micciulla and Makhoul defined TER and HTER at AMTA 2006 for the DARPA GALE program, where HTER became an official measure. They chose a greedy search for shifts because the exact problem is NP-complete (Shapira and Storer 2002), and released tercom. Their paper reports that HTER agrees better with human judgments than BLEU and other automatic scores (a measurement). Matt Post added a port of tercom to sacreBLEU, so that TER can be computed with the same settings as BLEU and chrF.

## References
