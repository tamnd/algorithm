---
tag: 8WQ3ZQ
kind: definition
slug: word-error-rate
name: Word error rate
aliases:
- WER
area: natural-language-and-speech/speech-recognition
level: intro
summary: The number of substitutions, deletions and insertions in the minimum edit alignment of hypothesis to reference, over reference length.
prereqs: [edit-distance, automatic-speech-recognition]
see_also: [wagner-fischer-algorithm, perplexity, confusion-network, mcnemar-test, bootstrap-method, lattice-rescoring, dynamic-time-warping, forced-alignment]
sources:
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974, pages 168 to 173
    locator: the dynamic program for the least number of edit operations
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall PTR, 2001
    locator: Chapter 9 (acoustic modeling), the measurement of recognition errors
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the word error rates of the systems that the survey compares
---

The word error rate (WER) measures how far the output of a speech recognizer is from a reference transcript. Align the hypothesis to the reference with the least number of word substitutions $S$, deletions $D$ and insertions $I$, and divide that number by the number $N$ of words in the reference: $\mathrm{WER} = (S + D + I) / N$. The numerator is the word level [edit distance](/edit-distance/), computed by the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/). Lower is better, 0 means a perfect match, and the value can exceed 1.

## Definition

Let the reference be $r = r_1 \ldots r_N$ with $N \ge 1$ and the hypothesis be $h = h_1 \ldots h_M$ with $M \ge 0$, both sequences of words after the same text normalization. An alignment of $h$ to $r$ is a sequence of operations that reads both sequences from left to right. Each operation is one of

- a match or a substitution, which pairs $r_i$ with $h_j$ (a substitution if $r_i \ne h_j$),
- a deletion, which leaves $r_i$ without a partner in $h$,
- an insertion, which leaves $h_j$ without a partner in $r$.

The cost of an alignment is the number of substitutions, deletions and insertions, with cost 1 each. Let $E(r, h)$ be the least cost of an alignment; this is the Levenshtein distance between the two sequences of words. Then

$$\mathrm{WER}(r, h) = \frac{S + D + I}{N} = \frac{E(r, h)}{N},$$

where $S$, $D$ and $I$ are the counts of one alignment of least cost. The sum $S + D + I = E(r, h)$ is the same for every alignment of least cost, but the split into $S$, $D$ and $I$ can differ between them. For example, $r = (a, b)$ and $h = (b, a)$ have $E = 2$ by two substitutions, or by one deletion and one insertion. A scoring tool fixes a tie rule. The code of this page prefers a match or a substitution, then a deletion, then an insertion. Every alignment satisfies $D - I = N - M$.

For a test set of utterances $(r^1, h^1), \ldots, (r^K, h^K)$, the corpus WER is the total number of errors over the total number of reference words:

$$\mathrm{WER} = \frac{\sum_k E(r^k, h^k)}{\sum_k N_k}.$$

This is the number that papers report. It is not the mean of the sentence WERs. Word accuracy is $1 - \mathrm{WER}$, and the word correct rate $(N - S - D)/N$ ignores insertions.

WER is undefined for an empty reference. The value depends on the text normalization: case, punctuation, numbers, hyphens, contractions and filler words must be handled the same way in the reference and the hypothesis, and the normalization is part of the definition of any reported number.

## Examples and non-examples

- **One substitution and one deletion.** $r$ = "the cat sat on the mat", $h$ = "the cat sit on mat". One alignment of least cost substitutes "sit" for "sat" and deletes the second "the". So $S = 1$, $D = 1$, $I = 0$, $N = 6$ and $\mathrm{WER} = 2/6 = 1/3 \approx 0.333333$.
- **Above 1.** $r$ = "a b", $h$ = "x y z w". The best alignment has 2 substitutions and 2 insertions, so $\mathrm{WER} = 4/2 = 2$. A recognizer that outputs many extra words can have a WER above 100 percent. Similarly $r$ = "a" and $h$ = "a x y" give 2.
- **Empty output.** If $h$ is empty, every reference word is deleted and $\mathrm{WER} = 1$. So a recognizer that outputs nothing beats one that outputs many wrong words.
- **Corpus against sentence average.** Take one utterance "a" recognized as "b", and one of 9 words recognized without errors. The corpus WER is $1/10$. The mean of the sentence WERs is $(1 + 0)/2 = 1/2$, which gives the short utterance the same weight as the long one.
- **Normalization.** $r$ = "The cat sat." and $h$ = "the cat sat" give $\mathrm{WER} = 2/3$ if the words are compared as written, because "The" and "sat." do not match. After lower casing and stripping the punctuation, the WER is 0.
- **Not a WER: the edit distance of the characters.** The character error rate uses the same formula over characters. It is the usual measure for languages written without spaces between words, and it is not comparable with WER.
- **Not a WER: the sentence error rate.** The fraction of utterances with at least one error ignores how many errors each one has.
- **Not a metric.** WER divides by the length of the reference, so $\mathrm{WER}(r, h) \ne \mathrm{WER}(h, r)$ in general. In the first example, $\mathrm{WER}(h, r) = 2/5$.

The tests in the code check these values with exact fractions, and compare the alignment with a brute force recursion on random word sequences.

## Related definitions

- **[Edit distance](/edit-distance/).** WER is the word level Levenshtein distance divided by the reference length. The [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) computes it in $\Theta(N M)$ time, and its traceback gives the alignment and the counts $S$, $D$ and $I$.
- **Character, phone and token error rates.** The same formula over characters, phones or subword tokens.
- **Expected WER.** Decoders that output a [confusion network](/confusion-network/) or rescore a [word lattice](/word-lattice/) choose the hypothesis with the least expected number of word errors in place of the most probable word sequence.
- **[Perplexity](/perplexity/).** A measure of a language model on text. Lower perplexity often goes with lower WER, but this is an observation about language models and not a rule, so WER is measured directly.
- **Significance of a difference.** Two systems on the same test set are compared by tests on paired errors, such as the [McNemar test](/mcnemar-test/) on the utterances or the [bootstrap method](/bootstrap-method/) on the per utterance error counts. A small difference in WER on a small test set is often not significant.
- **[Automatic speech recognition](/automatic-speech-recognition/).** WER is the main measure of this problem. A reported WER names its test set, for example the Wall Street Journal Nov'93 evaluation, where Young, Odell and Woodland 1994 reported 4.90 percent on the 5k task and 12.67 percent on the 20k task (measurements).

## References
