---
tag: T1YMPJ
kind: definition
slug: alignment-error-rate
name: Alignment error rate
aliases:
- AER
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: 1 - (|A and S| + |A and P|) / (|A| + |S|) for predicted links A, sure gold links S and possible gold links P.
history:
  year: 2000
  people: [Franz Josef Och, Hermann Ney]
  note: Och and Ney defined AER at ACL 2000 for gold alignments with sure and possible links, and used it in 2003 to compare the IBM models and the HMM model. Fraser and Marcu showed in 2007 that it does not predict translation quality well.
prereqs: [word-alignment, precision-and-recall]
see_also: [precision-and-recall, word-alignment, grow-diag-final-symmetrization, fast-align, hmm-alignment-model, ibm-model-1, bleu, jaccard-similarity]
sources:
  - paper: "Franz Josef Och and Hermann Ney, Improved statistical alignment models, ACL 2000, pages 440 to 447, ACL Anthology P00-1056"
    title: Och and Ney 2000
    locator: the evaluation with sure and possible links and the definition of the alignment error rate
  - paper: "Franz Josef Och and Hermann Ney, A systematic comparison of various statistical alignment models, Computational Linguistics 29(1), 2003, pages 19 to 51"
    title: Och and Ney 2003
    locator: "Section 5 (the annotation with sure and possible links, precision, recall and the alignment error rate)"
  - paper: doi:10.1162/coli.2007.33.3.293
    title: Alexander Fraser and Daniel Marcu, Measuring word alignment quality for statistical machine translation, Computational Linguistics 33(3), 2007, pages 293 to 303
    locator: the example of two alignments with the same AER, the weighted F measure, and the correlation of the measures with BLEU
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Section 4.5 (word alignment and its evaluation)"
---

The alignment error rate (AER) measures how well a predicted [word alignment](/word-alignment/) matches a gold alignment made by people. The annotators mark two kinds of links: sure links $S$, on which they agree, and possible links $P \supseteq S$, which are acceptable but not certain, for example for words of an idiom. For a predicted set of links $A$, $\mathrm{AER} = 1 - (|A \cap S| + |A \cap P|) / (|A| + |S|)$. A predicted link in $P$ is not an error, and a sure link that $A$ misses is an error. Och and Ney (2000) defined it, and for some years it was the standard measure of word aligners. It is a mix of [precision and recall](/precision-and-recall/), but not a proper F measure when $S \ne P$, and Fraser and Marcu (2007) showed that a lower AER does not reliably give better translations.

## Definition

A link is a pair $(j, i)$ of a source position $j$ and a target position $i$. Let $S \subseteq P$ be the sure and possible gold links of a sentence pair, and $A$ the predicted links. Then

$$\mathrm{precision}(A, P) = \frac{|A \cap P|}{|A|}, \qquad \mathrm{recall}(A, S) = \frac{|A \cap S|}{|S|},$$

$$\mathrm{AER}(A; S, P) = 1 - \frac{|A \cap S| + |A \cap P|}{|A| + |S|}.$$

Precision is measured against the possible links and recall against the sure links, so a link in $P \setminus S$ can raise precision but is never required. For a test set, the code of this page sums the four counts over all sentence pairs before the division. This value is not the mean of the sentence values, so a report should say which of the two it gives.

Three facts follow from the definition.

- **Range.** $|A \cap S| \le |S|$ and $|A \cap P| \le |A|$, so $0 \le \mathrm{AER} \le 1$. AER is 1 when $A$ has no link in $P$.
- **Zero error.** AER is 0 exactly when both inequalities are equalities, that is when $S \subseteq A \subseteq P$. So every $A$ between the sure and the possible links is perfect.
- **A weighted mean.** $1 - \mathrm{AER} = (|A| \cdot \mathrm{precision} + |S| \cdot \mathrm{recall}) / (|A| + |S|)$, a mean of precision and recall weighted by the sizes of $A$ and $S$. If $S = P$, it is $2|A \cap S| / (|A| + |S|)$, the Dice coefficient, which equals the F1 score $2 p r / (p + r)$. If $S \ne P$, the weights depend on $A$, and $1 - \mathrm{AER}$ is not the harmonic mean of the two.

The pseudocode below computes AER for one sentence pair.

```pseudo id=main
AER(A, S, P)
L1  check that S ⊆ P
L2  hit_S ← |A ∩ S|
L3  hit_P ← |A ∩ P|
L4  return 1 - (hit_S + hit_P) / (|A| + |S|)
```

With hash sets the cost is $\Theta(|A| + |S| + |P|)$ expected time.

## Examples and non-examples

- **A small case.** Let $S = \{(1,1), (2,2)\}$, $P = S \cup \{(3,2)\}$ and $A = \{(1,1), (3,2), (3,3)\}$. Then $|A \cap S| = 1$, $|A \cap P| = 2$, and $\mathrm{AER} = 1 - (1 + 2)/(3 + 2) = 2/5$. Precision is $2/3$ and recall is $1/2$, so F1 is $4/7$ and $1 - \mathrm{F1} = 3/7$, which is not $2/5$.
- **Perfect alignments.** With $S = \{(1,1), (2,2)\}$ and $P = S \cup \{(3,2), (3,3)\}$, the sets $A = S$, $A = P$ and $A = S \cup \{(3,3)\}$ all have AER 0.
- **One error of each kind.** With the same $S$ and $P$, the prediction $S \cup \{(5,5)\}$ has one wrong link and AER $1/5$; the prediction $\{(1,1)\}$ misses one sure link and has AER $1/3$. An empty $A$ has AER 1.
- **Same AER, different quality (Fraser and Marcu 2007).** Let $|A| = |S| = 100$. In the first alignment, 50 links are sure and the other 50 are outside $P$: precision and recall are both $0.5$. In the second, 25 links are sure, 50 are possible and 25 are outside $P$: precision is $0.75$ and recall $0.25$. Both have $1 - \mathrm{AER} = (50 + 50)/200 = (25 + 75)/200 = 0.5$, but the balanced F is $0.5$ and $0.375$.
- **Sentence and corpus values.** For two pairs with sentence AERs 0 and $3/4$, where the second has 3 predicted and 1 sure link, the corpus value with summed counts is $1 - 3/6 = 1/2$, not the mean $3/8$.
- **Non-example: a gold set with $S \not\subseteq P$.** The definition needs every sure link to be possible. The code rejects such a gold set.
- **Non-example: an empty $A$ and an empty $S$.** The fraction is $0/0$, and AER has no value.

## Related definitions

- [Precision and recall](/precision-and-recall/) are the two measures that AER mixes. Fraser and Marcu (2007) proposed the weighted F measure $1 / (\alpha / \mathrm{precision} + (1 - \alpha) / \mathrm{recall})$ instead, with $\alpha$ tuned for each language pair and task. In their experiments the squared correlation $r^2$ with [BLEU](/bleu/) was 0.16 for $1 - \mathrm{AER}$, 0.20 for F with sure and possible links, and 0.67 for F on gold links without the sure and possible distinction.
- When $S = P$, $1 - \mathrm{AER}$ is the Dice coefficient of $A$ and $S$, which is a monotone function of their [Jaccard similarity](/jaccard-similarity/) $J$: Dice $= 2J/(1 + J)$.
- The aligners evaluated with AER include [IBM Model 1](/ibm-model-1/), the [HMM alignment model](/hmm-alignment-model/) and [fast_align](/fast-align/). Symmetrization heuristics such as [grow-diag-final](/grow-diag-final-symmetrization/) trade precision for recall, and AER is one way to compare them.

## References
