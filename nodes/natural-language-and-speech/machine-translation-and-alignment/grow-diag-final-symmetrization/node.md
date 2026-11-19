---
tag: 00FY52
kind: algorithm
slug: grow-diag-final-symmetrization
name: Grow-diag-final symmetrization
aliases:
- alignment symmetrization
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Combine the alignments of the two directions by starting from their intersection and adding neighbouring links from their union.
solves: [word-alignment]
model: word-ram
complexity:
  vars: {m: the source sentence length, l: the target sentence length}
  time: {worst: "O(m l (m + l))"}
  space: {extra: "O(m l)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Franz Josef Och, Hermann Ney, Philipp Koehn, Daniel Marcu]
  note: Och and Ney (2003) gave the refined method that grows the intersection with links of the union. Koehn, Och and Marcu (2003) compared heuristics of this kind for phrase-based translation, and the Moses toolkit made grow-diag-final its default.
prereqs: [word-alignment]
see_also: [ibm-model-1, hmm-alignment-model, fast-align, phrase-pair-extraction, phrase-based-translation-model, alignment-error-rate, precision-and-recall, greedy-algorithm]
sources:
  - paper: "Franz Josef Och and Hermann Ney, A systematic comparison of various statistical alignment models, Computational Linguistics 29(1), 2003, pages 19 to 51"
    title: Och and Ney 2003
    locator: "Section 4 (symmetrization: intersection, union and the refined method)"
  - paper: "Philipp Koehn, Franz Josef Och and Daniel Marcu, Statistical phrase-based translation, HLT-NAACL 2003, ACL Anthology N03-1017"
    title: Koehn, Och and Marcu 2003
    locator: the comparison of alignment heuristics for phrase extraction
  - paper: "Moses statistical machine translation system, documentation of the training step Align Words, http://www2.statmt.org/moses/?n=FactoredTraining.AlignWords"
    title: Moses documentation
    locator: the GROW-DIAG-FINAL pseudocode and the list of the other heuristics
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Section 4.5 (word alignment)"
---

Grow-diag-final is a heuristic that combines two one-directional [word alignments](/word-alignment/) of a sentence pair into one set of links. It starts from the links that both directions agree on, then adds links from either direction that touch an already aligned word through one of the 8 neighbouring cells (the *grow-diag* step), and at the end adds the remaining links whose words are still unaligned (the *final* step). It goes back to the refined method of Och and Ney (2003), and in the form of the Moses toolkit it is the usual input to [phrase pair extraction](/phrase-pair-extraction/). It optimizes no objective. Its result depends on the order of its loops, so this page follows the Moses pseudocode exactly.

## In plain words

Word alignment models such as [IBM Model 1](/ibm-model-1/) or the [HMM model](/hmm-alignment-model/) link words in one direction only. Each word of one side gets at most one partner on the other side, so the model cannot link one word to two words. Run the model in both directions and you get two different sets of links.

The links that both sets share are very likely right, but there are too few of them. All links of both sets together cover more, but many are wrong. Grow-diag-final starts from the shared links and adds more. A link from either set is added if it sits right next to a link already kept, also on a diagonal, and if one of its two words still has no partner. When nothing more can be added this way, any link that gives a partner to a word that still has none is added too.

## The problem

The input is a sentence pair with the source $f_1 \ldots f_m$ and the target $e_1 \ldots e_l$, and two link sets $A_1, A_2 \subseteq \{1, \ldots, m\} \times \{1, \ldots, l\}$ of pairs $(j, i)$. Usually $A_1 = \{(j, a_j) : a_j > 0\}$ comes from a model of $p(f \mid e)$, where each source word has at most one link, and $A_2 = \{(b_i, i) : b_i > 0\}$ from a model of $p(e \mid f)$, where each target word has at most one link. The output is one link set $A$ that can be many to many. The intersection $A_1 \cap A_2$ has high precision and the union $A_1 \cup A_2$ has high recall, in the measurements of Och and Ney (2003). A good $A$ lies between them.

There is no objective function here. The task is a design choice, and the quality of the result is measured with the [alignment error rate](/alignment-error-rate/) against hand alignments, or by the translation quality of a system trained on it.

## The algorithm

Moses writes the neighbours as offsets $(\Delta i, \Delta j)$ of the target and the source position, in the order $(-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)$: first the four direct neighbours, then the four diagonal ones. A word is *aligned* if it has a link in the current set $A$.

```pseudo id=main
GROW-DIAG-FINAL(A_1, A_2, m, l)                 ▷ links (j, i); Moses calls A_1 e2f and A_2 f2e
L1  A ← A_1 ∩ A_2; U ← A_1 ∪ A_2
L2  repeat
L3      added ← false
L4      for i ← 1 to l do for j ← 1 to m do                     ▷ target outer, source inner
L5          if (j, i) ∈ A then
L6              for each (Δi, Δj) in the 8 neighbour offsets, in the order above do
L7                  p ← (j + Δj, i + Δi)
L8                  if p ∈ U and (the source word of p or the target word of p is unaligned) then A ← A ∪ {p}; added ← true
L9  until not added
L10 for each B in (A_1, A_2) do                                 ▷ FINAL(e2f), then FINAL(f2e)
L11     for i ← 1 to l do for j ← 1 to m do
L12         if (j, i) ∈ B and (j or i is unaligned) then A ← A ∪ {(j, i)}
L13 return A
```

Line L1 starts from the intersection. Lines L2 to L9 are the grow-diag step: each pass walks over all cells, and for each kept link it tries the 8 neighbours. A neighbour is added only if it is a link of one of the two directions and it brings a new word into the alignment. A link added in a pass is visible at once, to the rest of the same pass. The passes repeat until one adds nothing. Lines L10 to L12 are the final step: for links that are not next to anything, the only test is that one of their words is still unaligned.

**The other heuristics of Moses.** The same documentation lists intersection (line L1 only), union, grow (only the four direct neighbours), grow-diag (no final step) and the two single directions. Grow-diag-final is the default there.

**Grow-diag-final-and.** A common variant asks at line L12 that both words are unaligned. It adds fewer isolated links. It is not on the Moses documentation page that this page follows; it is an option of the Moses training scripts.

## Example

Take $f$ = ich gehe nicht nach hause and $e$ = i do not go home ($m = l = 5$). The direction $p(f \mid e)$ gives $a = (1, 4, 3, 5, 5)$: ich to i, gehe to go, nicht to not, nach to home and hause to home. The direction $p(e \mid f)$ gives $b = (1, 2, 3, 2, 5)$: i to ich, do to gehe, not to nicht, go to gehe and home to hause. So

$A_1 = \{(1,1), (2,4), (3,3), (4,5), (5,5)\}$, $A_2 = \{(1,1), (2,2), (3,3), (2,4), (5,5)\}$, $A_1 \cap A_2 = \{(1,1), (2,4), (3,3), (5,5)\}$, and $U \setminus (A_1 \cap A_2) = \{(2,2), (4,5)\}$.

In the intersection, the target word do ($i = 2$) and the source word nach ($j = 4$) are unaligned. The first pass of lines L4 to L8 goes like this.

| visit $(j, i)$ | neighbour tried | in $U$? | unaligned word | action |
|---|---|---|---|---|
| (1, 1) ich, i | (1, 2), (2, 1) | no | | |
| (1, 1) | $(\Delta i, \Delta j) = (1, 1)$: (2, 2) gehe, do | yes | do | add (2, 2) |
| (2, 2) gehe, do | all 8 | (1, 1), (3, 3) are in $A$ | none | |
| (3, 3) nicht, not | (2, 2), (2, 4) | in $A$ | none | |
| (2, 4) gehe, go | all 8 | only (3, 3), which is in $A$ | none | |
| (5, 5) hause, home | $(0, -1)$: (4, 5) nach, home | yes | nach | add (4, 5) |

The second pass adds nothing, and the final step finds no link of $A_1$ or $A_2$ with an unaligned word. The result is $\{(1,1), (2,2), (2,4), (3,3), (4,5), (5,5)\}$, which here is the whole union: gehe is linked to both do and go, and home to both nach and hause. Without the diagonal neighbours (the grow heuristic), (2, 2) would not be added, because none of its four direct neighbours is a link; it would come back only in a final step.

On other inputs the result is strictly between the intersection and the union. For $a = (2, 4, 3, 1, 4)$ and $b = (5, 1, 1, 2, 1)$, the union has 8 links, the intersection 2, grow-diag keeps 5, grow-diag-final 7 and grow-diag-final-and 6. The link (5, 1) of $A_2$ is never added, because by then both of its words are aligned.

## Correctness

The procedure is a heuristic, so "correct" means it does what it states. Four facts hold, and the proofs file proves them. The working set always lies between the intersection and the union, because every added link is in the union and nothing is removed. The loop of lines L2 to L9 ends after at most $|U \setminus I| + 1$ passes, because each pass that goes on adds a new link of $U$. When it ends, no link of $U$ next to a kept link has an unaligned word. After the final step, every word that has a link in $A_1$ or in $A_2$ is aligned. The last fact fails for the variant with "and".

## Complexity

Count in the [word RAM](/word-ram/) model, with the link sets as hash sets or as $m \times l$ bit tables, and with a count of links per word so that "aligned" is an $O(1)$ test. One pass of lines L4 to L8 costs $O(m l)$: $m l$ cells and at most 8 neighbours each. The final step costs $O(m l)$. By the termination bound there are at most $|U| - |I| + 1$ passes. For two one-directional alignments, $|U| \le m + l$, so the time is $O(m l (m + l))$ in the worst case. In practice two or three passes are enough, so the cost is close to $O(m l)$. The space is $O(m l)$ for the tables, or $O(m + l)$ for the counts plus the size of the sets.

## Properties

- **Between intersection and union.** $A_1 \cap A_2 \subseteq A \subseteq A_1 \cup A_2$.
- **Covers what the union covers.** Every word linked by either direction is linked in the result, so no word that a model aligned is left out.
- **Many to many.** The result can link one word to several words on both sides, which neither direction can do alone.
- **Order dependent.** The loops of line L4 and the neighbour order of line L6 decide which link wins when two compete for the same unaligned word. For $a = (3, 2, 1, 1)$ and $b = (4, 4, 1)$ with $m = 4$ and $l = 3$, the target-outer order of line L4 adds (4, 2), and a source-outer order does not.
- **No objective.** It maximizes nothing, so there is no guarantee on the alignment error rate.

## Variants and improvements

- **Intersection and union.** The two extremes. Och and Ney (2003) measured higher precision for the intersection and higher recall for the union.
- **Grow, grow-diag.** Without the diagonal neighbours, or without the final step.
- **Grow-diag-final-and.** The final step needs both words unaligned, so it adds fewer isolated links. Its result is not always a subset of the grow-diag-final result: on $a = (4, 1, 3, 2)$, $b = (2, 1, 4, 4)$ it adds (4, 4), which grow-diag-final does not.
- **The refined method of Och and Ney.** It adds a link of $U$ if neither word is aligned, or if it has a horizontal or vertical neighbour in $A$ and the new set has no link with both a horizontal and a vertical neighbour. Grow-diag-final relaxes these tests.
- **Joint training.** Agreement-based training of the two directions and supervised or discriminative alignment models replace the heuristic by an objective.

## When to use it

Use grow-diag-final, or its "and" variant, to turn two directional alignments from [IBM models](/ibm-model-1/), the [HMM model](/hmm-alignment-model/) or [fast align](/fast-align/) into the input of [phrase pair extraction](/phrase-pair-extraction/) for a [phrase-based model](/phrase-based-translation-model/). Phrase extraction needs many to many links with good recall, and the intersection alone gives too few. Use the intersection when precision matters most, for example to build a bilingual dictionary. Use the union when recall matters most. The choice is a measurement on the final task: Koehn, Och and Marcu (2003) compared heuristics of this kind by the BLEU of the phrase-based system.

## Pitfalls

- **Another loop order.** If line L4 puts the source positions in the outer loop, or line L6 uses another neighbour order, the result can change, and it no longer matches Moses. Keep the stated order, or say which one you use.
- **Snapshot passes.** If a pass reads a copy of $A$ made at its start, links added at line L8 are not visible until the next pass, and the result can differ. In the Moses pseudocode they are visible at once.
- **The final step with "and".** If line L12 tests "j and i unaligned" but you expect every word of the union to be covered, the coverage property fails. Pick the variant knowingly.
- **Null links.** Links to the null word ($a_j = 0$) are not links. Drop them before line L1; otherwise a word linked to null in both directions counts as aligned.
- **Mixed up directions.** $A_1$ and $A_2$ must use the same coordinates $(j, i)$. The output of a model of $p(e \mid f)$ is a list indexed by $i$, and it must be turned into pairs $(b_i, i)$.

## Implementations

## History

Och and Ney (2003) noted that a one-directional model cannot link one word to several words and proposed to combine the two directions: by intersection, by union, or by a refined method that grows the intersection with links of the union. Koehn, Och and Marcu (2003) used such heuristics to build the alignments for phrase-based translation and compared them by translation quality. The Moses toolkit, released in 2007, wrote the grow-diag-final heuristic in the pseudocode that most later work follows and made it the default of its training pipeline.

## References
