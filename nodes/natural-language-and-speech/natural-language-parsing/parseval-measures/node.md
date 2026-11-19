---
tag: KB4Z5N
kind: definition
slug: parseval-measures
name: PARSEVAL measures
aliases:
- labeled bracket F1
- bracketing precision and recall
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "Precision, recall and F1 of the labeled constituent spans of a predicted tree against a gold tree, the standard score of constituency parsers."
prereqs: [parse-tree, treebank, precision-and-recall]
see_also: [constituency-parsing, span-f1-score, attachment-score, smatch, head-rules, span-based-constituency-parsing, parent-annotation, latent-variable-pcfg]
sources:
  - paper: "E. Black, S. Abney, D. Flickenger and others, A Procedure for Quantitatively Comparing the Syntactic Coverage of English Grammars, Speech and Natural Language Workshop, Pacific Grove, February 1991"
    title: "Black et al., A Procedure for Quantitatively Comparing the Syntactic Coverage of English Grammars"
    locator: "the bracket comparison procedure (ACL Anthology H91-1060)"
  - url: https://github.com/nikitakit/self-attentive-parser/tree/master/EVALB
    title: "Satoshi Sekine and Michael Collins, EVALB, a bracket scoring program (copy of the 1997 distribution)"
    locator: "the README (the definitions of recall, precision and crossing brackets) and the parameter file COLLINS.prm"
  - paper: "Eugene Charniak, Tree-bank Grammars, Proceedings of AAAI-96"
    title: "Eugene Charniak, Tree-bank Grammars"
    locator: "the evaluation by bracket precision and recall of a treebank grammar"
---

The PARSEVAL measures score a predicted [parse tree](/parse-tree/) against the gold tree of the same sentence by comparing their constituents. Each constituent is written as a labeled bracket: its label and the span of words it covers. Labeled precision is the fraction of predicted brackets that are also gold brackets, labeled recall is the fraction of gold brackets that are also predicted, and F1 is their harmonic mean, as on the [precision and recall](/precision-and-recall/) page. The measures go back to a 1991 workshop procedure of Black and others, and the program EVALB of Sekine and Collins fixed the details that most papers use. They are the standard score of [constituency parsing](/constituency-parsing/). Dependency parsers are scored by the [attachment score](/attachment-score/) instead, and general span tasks such as named entities by the [span F1 score](/span-f1-score/), which uses the same counting on spans that do not nest.

## Definition

A sentence has $n$ words, and a fencepost span $(i, j)$ with $0 \le i < j \le n$ covers the words $i + 1$ to $j$. Let $t$ be a tree over the sentence. The **brackets** of $t$ are the multiset

$$B(t) = \{ (\ell, i, j) : t \text{ has a phrasal node with label } \ell \text{ over the span } (i, j) \},$$

with one element for each node that is not a preterminal and not a word. Preterminals, the part-of-speech tags, are not brackets; their accuracy is reported separately as tagging accuracy. A multiset is used because a unary chain such as (NP (NP ...)) gives the same bracket twice.

For a predicted tree $p$ and a gold tree $g$ of the same sentence, the number of **matched brackets** is the size of the multiset intersection, $m = |B(p) \cap B(g)|$, where a bracket that occurs $a$ times in $B(p)$ and $b$ times in $B(g)$ counts $\min(a, b)$ times. Then

$$\mathrm{LP} = \frac{m}{|B(p)|}, \qquad \mathrm{LR} = \frac{m}{|B(g)|}, \qquad F_1 = \frac{2\,\mathrm{LP}\,\mathrm{LR}}{\mathrm{LP} + \mathrm{LR}} = \frac{2m}{|B(p)| + |B(g)|}.$$

On a test set the counts are added over all sentences before the division: $\mathrm{LP} = \sum m / \sum |B(p)|$ and $\mathrm{LR} = \sum m / \sum |B(g)|$. This is a micro average, and it is not the mean of the per-sentence scores.

**Settings.** The scores depend on what is removed before the brackets are counted. This page uses the settings of the EVALB parameter file COLLINS.prm, which most Penn Treebank papers use:

- the label TOP, the unlabeled outer bracket that wraps each tree, is deleted, so the root span of TOP is not counted; the S bracket over the whole sentence is counted;
- the empty elements (tag -NONE-) are deleted and do not count toward the sentence length;
- the words tagged with the punctuation tags , : `` '' and . are deleted, and the spans are counted again on the remaining words;
- the labels ADVP and PRT are treated as equal;
- the scores are given for all sentences and again for the sentences of at most 40 words.

Other tags, such as the brackets -LRB- and -RRB- and the tag #, are kept by COLLINS.prm. Function tags such as -SBJ are usually removed from the gold trees before training and evaluation, so NP-SBJ counts as NP. The root bracket S may have any number of children; the measures do not depend on it.

**Related counts.** **Unlabeled** precision and recall ignore the label and compare spans only. A predicted bracket **crosses** a gold bracket if the two spans overlap and neither contains the other; the crossing brackets count is the number of predicted brackets that cross at least one gold bracket. **Exact match** is the fraction of sentences with $B(p) = B(g)$.

Precision rewards trees with few brackets and recall rewards trees with many. A parser can raise precision by predicting a flat tree, which is why the two are reported together or as $F_1$.

## Examples and non-examples

The examples use two gold trees, in Penn Treebank form:

- $g_1$ = (TOP (S (NP (NNS astronomers)) (VP (VBD saw) (NP (NP (NNS stars)) (PP (IN with) (NP (NNS ears))))) (. .)))
- $g_2$ = (TOP (S (NP (PRP she)) (VP (VBD gave) (PRT (RP up))) (. .)))

and three predicted trees:

- $p_1$ = (TOP (S (NP (NNS astronomers)) (VP (VP (VBD saw) (NP (NNS stars))) (PP (IN with) (NP (NNS ears)))) (. .))), where *with ears* modifies *saw*;
- $f_1$ = (TOP (S (NP (NNS astronomers)) (VP (VBD saw) (NP (NNS stars)) (PP (IN with) (NP (NNS ears)))) (. .))), a flat VP;
- $p_2$ = (TOP (S (NP (PRP she)) (VP (VBD gave) (ADVP (RB up)) (. .)))), with the period inside the VP.

After the COLLINS.prm deletions, $g_1$ has 5 words and the 7 brackets S(0,5), NP(0,1), VP(1,5), NP(2,5), NP(2,3), PP(3,5), NP(4,5). All values below are exact fractions.

| gold | predicted | $\lvert B(p) \rvert$ | $\lvert B(g) \rvert$ | $m$ | LP | LR | $F_1$ |
|---|---|---|---|---|---|---|---|
| $g_1$ | $p_1$ | 7 | 7 | 6 | 6/7 | 6/7 | 6/7 |
| $g_1$ | $f_1$ | 6 | 7 | 6 | 1 | 6/7 | 12/13 |
| $g_2$ | $p_2$ | 4 | 4 | 4 | 1 | 1 | 1 |
| both | $p_1$, $p_2$ | 11 | 11 | 10 | 10/11 | 10/11 | 10/11 |

- **An attachment error costs one bracket each way.** $p_1$ has VP(1,3) instead of NP(2,5). VP(1,3) also crosses NP(2,5), so $p_1$ has one crossing bracket.
- **A flat tree has perfect precision.** $f_1$ misses NP(2,5) and predicts nothing wrong, so its precision is 1, though it does not say what *with ears* modifies.
- **The settings matter.** For $g_2$ and $p_2$, the period lies inside the VP of $p_2$, and $p_2$ says ADVP where $g_2$ says PRT. With the COLLINS.prm settings the period is deleted, VP covers (1,3) in both trees, and ADVP equals PRT, so all 4 brackets match. With no deletion and no label merge, TOP is counted, the VP spans are (1,3) and (1,4), and only 3 of 5 brackets match, $F_1 = 3/5$. For both sentences together, the raw counts give $10/13$ instead of $10/11$.
- **Micro average.** The per-sentence $F_1$ values $6/7$ and $1$ have the mean $13/14$, but the corpus $F_1$ is $10/11$, because the longer sentence has more brackets and more weight.
- **Non-example: a different sentence.** PARSEVAL compares trees over the same words. If the parser tokenizes the sentence differently from the gold tree, the spans do not line up, and EVALB counts the sentence as an error instead of scoring it.
- **Non-example: dependency trees.** A dependency tree has no phrase nodes, so it has no brackets. Its score is the attachment score. Converting it to brackets, or converting the constituency tree to dependencies with [head rules](/head-rules/), gives a different measure.

## Related definitions

- [Precision and recall](/precision-and-recall/): the general definitions, of which LP and LR are the case of brackets.
- [Span F1 score](/span-f1-score/): the same counting for flat spans with labels, such as named entities.
- [Attachment score](/attachment-score/): the fraction of words with the right head, the score of dependency parsers.
- [Smatch](/smatch/): an F1 over the triples of a semantic graph, with a search for the best match of the variables.
- [Treebank](/treebank/): the source of the gold trees and of the conventions that the settings depend on.

## References
