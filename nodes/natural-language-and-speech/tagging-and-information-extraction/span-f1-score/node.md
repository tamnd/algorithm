---
tag: Q2NAGZ
kind: definition
slug: span-f1-score
name: Span-level F1 score
aliases:
- CoNLL F1
- exact-match entity F1
area: natural-language-and-speech/tagging-and-information-extraction
level: intro
summary: Precision and recall of predicted spans that match a gold span exactly in boundaries and type, combined as their harmonic mean.
prereqs: [precision-and-recall, bio-encoding]
see_also: [named-entity-recognition, text-chunking, sequence-labeling, b-cubed-metric, confusion-matrix, permutation-test, semi-markov-crf]
sources:
  - paper: "Erik F. Tjong Kim Sang and Sabine Buchholz, Introduction to the CoNLL-2000 shared task: chunking, Proceedings of CoNLL-2000 and LLL-2000, pages 127 to 132"
    title: Tjong Kim Sang and Buchholz 2000
    locator: "page 130 (the chunk tags, and the rule that an I-X tag after O or after a tag of another type starts a new chunk), and the evaluation by precision, recall and F of the chunks"
  - paper: "Erik F. Tjong Kim Sang and Fien De Meulder, Introduction to the CoNLL-2003 shared task: language-independent named entity recognition, Proceedings of CoNLL-2003, pages 142 to 147"
    title: Tjong Kim Sang and De Meulder 2003
    locator: the section on evaluation (a named entity counts as correct only if it matches the gold entity exactly)
---

The span-level F1 score measures how well a system finds labeled spans, such as the named entities of [named entity recognition](/named-entity-recognition/) or the chunks of [text chunking](/text-chunking/). It counts whole spans, not tokens: a predicted span is correct only when a gold span has exactly the same first token, the same last token and the same type. Precision is the share of predicted spans that are correct, recall is the share of gold spans that are found, and F1 is their harmonic mean. The CoNLL-2000 chunking task and the CoNLL-2003 named entity task used this score, computed by their script conlleval over the whole test set, and it is still the standard score for these tasks.

## Definition

Spans. A sentence has tokens $1, \ldots, n$. A span is a triple $(i, j, X)$ with $0 \le i < j \le n$ and a type $X$. It uses fencepost indices: $(i, j, X)$ covers the tokens $i + 1, \ldots, j$.

Counts. Let $G_s$ be the set of gold spans and $P_s$ the set of predicted spans of sentence $s$. Over a corpus, the counts are summed over the sentences:

$$\mathrm{TP} = \sum_s |G_s \cap P_s|, \qquad \mathrm{FP} = \sum_s |P_s \setminus G_s|, \qquad \mathrm{FN} = \sum_s |G_s \setminus P_s|.$$

Scores. Precision is $P = \mathrm{TP} / (\mathrm{TP} + \mathrm{FP})$, recall is $R = \mathrm{TP} / (\mathrm{TP} + \mathrm{FN})$, and

$$F_1 = \frac{2 P R}{P + R} = \frac{2\,\mathrm{TP}}{2\,\mathrm{TP} + \mathrm{FP} + \mathrm{FN}} \quad (\mathrm{TP} > 0).$$

A ratio with a zero denominator is taken as 0 in the code; state the convention when you report it. Since the counts are summed before the division, this is the micro average: each span counts once, so frequent types weigh more. The general $F_\beta = (1 + \beta^2) P R / (\beta^2 P + R)$ weighs recall $\beta$ times as much as precision; CoNLL used $\beta = 1$.

From tags. Taggers output tags, not spans. The CoNLL scripts read the spans from B, I and O tags with one rule (Tjong Kim Sang and Buchholz 2000, page 130): a B-X starts a span, and an I-X also starts a span when it follows O, the start of the sentence or a tag of another type. A span ends before an O, before a tag that starts a span, or at the end of the sentence. With this rule every tag sequence gives a span set, valid or not (see [BIO encoding](/bio-encoding/)).

```pseudo id=main
SPAN-F1(gold tags, predicted tags of each sentence)
L1  read the spans of each tag sequence: B-X, or I-X after O, the start or another type, starts a span
L2  a span ends before O, before a tag that starts a span, or at the end of the sentence
L3  TP ← Σ over sentences |G_s ∩ P_s|                  ▷ same i, same j, same type
L4  FP ← Σ |P_s| - |G_s ∩ P_s|
L5  FN ← Σ |G_s| - |G_s ∩ P_s|
L6  P ← TP / (TP + FP), or 0 if no span is predicted
L7  R ← TP / (TP + FN), or 0 if there is no gold span
L8  F1 ← 2 P R / (P + R), or 0 if P + R = 0
```

Properties (theorems, from the definition). $F_1$ lies between $\min(P, R)$ and $\max(P, R)$, and it is 1 only when the predicted spans equal the gold spans. A predicted span that overlaps a gold span but has a wrong boundary or a wrong type is one false positive and also one false negative, so a near miss costs more than predicting nothing at that place, which costs only the false negative. TN does not appear: the number of spans a system could have predicted and did not is not counted. The test file checks these facts and the identity $F_1 = 2\mathrm{TP} / (2\mathrm{TP} + \mathrm{FP} + \mathrm{FN})$ with exact fractions on random span sets, and checks the reading of tags against a second reader that first repairs the tags.

## Examples and non-examples

Take the sentence "John Smith works for Acme Corp in Paris" with 8 tokens:

| token | John | Smith | works | for | Acme | Corp | in | Paris |
|---|---|---|---|---|---|---|---|---|
| gold | B-PER | I-PER | O | O | B-ORG | I-ORG | O | B-LOC |
| predicted | B-PER | O | O | O | B-ORG | I-ORG | O | B-ORG |

The gold spans are $(0, 2, \mathrm{PER})$, $(4, 6, \mathrm{ORG})$ and $(7, 8, \mathrm{LOC})$. The predicted spans are $(0, 1, \mathrm{PER})$, $(4, 6, \mathrm{ORG})$ and $(7, 8, \mathrm{ORG})$. Only "Acme Corp" matches, so TP = 1, FP = 2 and FN = 2, and $P = R = F_1 = 1/3$. The predicted span "John" has the wrong end and "Paris" has the wrong type; each counts once as FP and once as FN. The token accuracy is $6/8 = 3/4$, much higher, because the 4 O tokens are easy.

Per type: PER and LOC have $F_1 = 0$, and ORG has $P = 1/2$ and $R = 1$, so $F_1 = 2/3$. The macro average, the mean of the per-type F1 values, is $2/9$; it gives each type the same weight, while the micro average $1/3$ gives each span the same weight.

Tags that are not valid IOB2 still have spans: O I-ORG I-ORG gives the span $(1, 3, \mathrm{ORG})$, and B-PER I-ORG gives two spans of one token. IOB1 tags are read by the same rule: I-X I-X B-X O gives $(0, 2, X)$ and $(2, 3, X)$.

Non-examples:

- Token-level F1 or accuracy, computed over tags, is not the span score: in the example it gives credit for "John" although the entity "John Smith" was not found.
- Overlap or partial match scores give credit when a predicted span overlaps a gold span. They are other scores, and a number from them cannot be compared with exact-match F1.
- Scores on gold spans only, such as the accuracy of typing given entities, measure classification, not finding.

## Related definitions

- [Precision and recall](/precision-and-recall/): the two ratios, here over spans. A span-level [confusion matrix](/confusion-matrix/) has no true negative cell.
- [BIO encoding](/bio-encoding/): how spans become tags and how invalid tag sequences are read.
- [B-cubed metric](/b-cubed-metric/): the coreference score that, like span F1, uses precision and recall, but over clusters of mentions.
- Significance: two systems on the same test set can be compared with a [permutation test](/permutation-test/) on sentences, since span F1 is not a mean of independent per-sentence scores.

## References
