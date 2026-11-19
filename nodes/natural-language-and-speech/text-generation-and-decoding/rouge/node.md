---
tag: MTNGKQ
kind: definition
slug: rouge
name: ROUGE
aliases:
- ROUGE-N
- ROUGE-L
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: Recall-oriented summary metrics based on the overlap of n-grams, or the longest common subsequence, between a candidate and reference summaries.
prereqs: [longest-common-subsequence, precision-and-recall]
see_also: [bleu, bertscore, chrf, word-error-rate, automatic-summarization, porter-stemmer, text-tokenization]
sources:
  - paper: "Chin-Yew Lin, ROUGE: A Package for Automatic Evaluation of Summaries, Text Summarization Branches Out (ACL 2004 workshop), pages 74 to 81, ACL Anthology W04-1013"
    title: Lin 2004
    locator: "Section 2 (ROUGE-N, equation 1, and Section 2.1 on multiple references and the jackknife), Section 3 (ROUGE-L, the sentence level F measure in Section 3.1 and the union LCS in Section 3.2), Section 4 (ROUGE-W), Section 5 (ROUGE-S and ROUGE-SU)"
  - paper: doi:10.18653/v1/2023.acl-long.107
    title: Max Grusky, Rogue Scores, ACL 2023, pages 1914 to 1934
    locator: the study of how papers compute and report ROUGE, and the differences between packages
---

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a family of scores that compare a candidate summary with one or more reference summaries written by people. ROUGE-N counts the n-grams of the references that also occur in the candidate. ROUGE-L uses the [longest common subsequence](/longest-common-subsequence/) of the two texts. Chin-Yew Lin defined them in 2004 and released them as the ROUGE package, which the Document Understanding Conferences used to evaluate summarizers. Higher is better, every score is between 0 and 1, and the score is computed per summary and averaged over the test set. All scores depend on the tokenization, the lower casing, the stemming and the stop word list, so these must be stated with the numbers.

## Definition

Let the candidate and the references be lists of tokens. For a text $T$ and $n \ge 1$, let $\#_T(g)$ be the number of times the n-gram $g$ occurs in $T$.

**ROUGE-N.** For one reference $Y$ and a candidate $X$, the clipped match count is $\sum_g \min(\#_X(g), \#_Y(g))$, so each n-gram of the candidate matches at most as many times as it occurs in the reference. Then

$$R_N = \frac{\sum_g \min(\#_X(g), \#_Y(g))}{\sum_g \#_Y(g)}, \qquad P_N = \frac{\sum_g \min(\#_X(g), \#_Y(g))}{\sum_g \#_X(g)},$$

and $F_N = 2 P_N R_N / (P_N + R_N)$. Equation 1 of the paper is the recall with the numerator and the denominator summed over all references. ROUGE-N is a recall measure by design; reports today often give the F measure.

**ROUGE-L, sentence level.** Let $m = |Y|$, $n = |X|$ and $\ell$ the length of a longest common subsequence of $X$ and $Y$. Then

$$R_{\mathrm{lcs}} = \frac{\ell}{m}, \qquad P_{\mathrm{lcs}} = \frac{\ell}{n}, \qquad F_{\mathrm{lcs}} = \frac{(1 + \beta^2)\, R_{\mathrm{lcs}}\, P_{\mathrm{lcs}}}{R_{\mathrm{lcs}} + \beta^2 P_{\mathrm{lcs}}}.$$

A common subsequence keeps the order of the words but allows gaps, so ROUGE-L rewards the same words in the same order without asking for consecutive n-grams. The paper sets $\beta$ to a very large number for DUC, so that only recall counts; most later work uses $\beta = 1$.

**ROUGE-L, summary level.** For reference sentences $r_1, \ldots, r_u$ with $m$ tokens in total and candidate sentences $c_1, \ldots, c_v$ with $n$ tokens in total, let $\mathrm{LCS}_\cup(r_i, C)$ be the number of tokens of $r_i$ that are in the union of the longest common subsequences of $r_i$ with each $c_j$. Then $R = \sum_i \mathrm{LCS}_\cup(r_i, C) / m$ and $P = \sum_i \mathrm{LCS}_\cup(r_i, C) / n$, with the same F. Google's rouge-score package calls this form ROUGE-Lsum; it splits the summaries into sentences at newlines.

**Other members.** ROUGE-W weights the common subsequence so that consecutive matches count more (Section 4). ROUGE-S counts skip-bigrams, pairs of words in order with any gap, and ROUGE-SU adds the unigrams (Section 5); the paper also limits the distance between the two words.

**Several references.** Section 2.1 takes the largest score over the references. The package uses a jackknife: with $M$ references, it takes the best score against each of the $M$ sets of $M - 1$ references, and averages these $M$ values, so that system scores are comparable with the scores of a human summary scored against the other references.

**Options of the package.** ROUGE-1.5.5 does no stemming and keeps stop words by default. Option -m applies the [Porter stemmer](/porter-stemmer/), -s removes the stop words of its list, -n sets the largest n, and -f chooses between the mean over references (A, the default) and the best reference (B).

## Examples and non-examples

The reference is "the cat sat on the mat" and the candidate is "the cat on the mat", split at spaces.

| score | matches | recall | precision | F ($\beta = 1$) |
|---|---|---|---|---|
| ROUGE-1 | the (2), cat, on, mat: 5 | 5/6 | 5/5 = 1 | 10/11 |
| ROUGE-2 | the cat, on the, the mat: 3 | 3/5 | 3/4 | 2/3 |
| ROUGE-L | the cat on the mat: $\ell = 5$ | 5/6 | 1 | 10/11 |

Clipping: the candidate "the the the" against the reference "the cat the" has three unigrams "the", but the reference has only two, so it matches 2, and the recall and the precision are both 2/3.

Lin's example for ROUGE-L. The reference S1 is "police killed the gunman". S2, "police kill the gunman", has the common subsequence "police the gunman", and $F_{\mathrm{lcs}} = 3/4$ with $\beta = 1$. S3, "the gunman kill police", has only "the gunman", and scores 1/2. ROUGE-2 gives both 1/3, since each shares only the bigram "the gunman", but S2 keeps the order of the sentence and S3 reverses its meaning. S4, "the gunman police killed", also scores 1/2 with ROUGE-L, because only one of the two orders "the gunman" and "police killed" can be in a common subsequence. Skip-bigrams tell S4 from S3: ROUGE-S gives S2 1/2, S3 1/6 and S4 1/3.

Lin's example for the union LCS. A reference sentence $w_1 w_2 w_3 w_4 w_5$ and a candidate of two sentences $w_1 w_2 w_6 w_7 w_8$ and $w_1 w_3 w_8 w_9 w_5$. The longest common subsequences are $w_1 w_2$ and $w_1 w_3 w_5$, their union is $w_1 w_2 w_3 w_5$, and the summary level recall is 4/5.

Several references. With references "the cat sat on the mat", "a cat sat on a mat" and "the dog sat", the candidate "the cat on the mat" has ROUGE-1 recall 5/6, 1/2 and 1/3. The largest is 5/6. Equation 1 pools the counts to $(5 + 3 + 1)/(6 + 6 + 3) = 3/5$. The jackknife averages the best of each pair, $(1/2 + 5/6 + 5/6)/3 = 13/18$. Three rules give three numbers.

Non-examples. ROUGE is not a measure of factual correctness: the candidate "the cat never sat on the mat" has ROUGE-1 recall 1 against the reference above, and "the mat sat on the cat" has ROUGE-1 recall and precision 1. It is not symmetric: recall and precision exchange when the candidate and the reference are exchanged. And a ROUGE number without its package, options and tokenization is not comparable with another ROUGE number; Grusky (2023) found that most papers do not report enough to reproduce their scores.

## Related definitions

- [BLEU](/bleu/) is the precision counterpart for translation, with clipped n-gram precisions, a geometric mean and a brevity penalty, computed at the corpus level.
- [BERTScore](/bertscore/) replaces exact matches by the cosine of contextual token embeddings.
- [chrF](/chrf/) uses character n-grams and an F measure.
- [Word error rate](/word-error-rate/) uses the edit distance instead of the longest common subsequence.
- The longest common subsequence is computed by the standard dynamic program in $O(mn)$ time, and the n-gram counts in $O(m + n)$ expected time with hash tables.
- ROUGE is the usual metric for [automatic summarization](/automatic-summarization/).

## References
