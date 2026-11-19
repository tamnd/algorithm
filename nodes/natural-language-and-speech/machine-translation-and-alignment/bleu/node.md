---
tag: FSSX1F
kind: algorithm
slug: bleu
name: BLEU
aliases:
- bilingual evaluation understudy
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: The geometric mean of clipped n-gram precisions for n = 1 to 4 against reference translations, times a brevity penalty. Higher is better, from 0 to 1, at the corpus level.
model: word-ram
complexity:
  vars: {L: the number of tokens in all candidates and references, N: the largest n-gram order}
  time: {worst: "O(N² L log L)"}
  space: {extra: "O(N L)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2002
  people: [Kishore Papineni, Salim Roukos, Todd Ward, Wei-Jing Zhu]
  note: The four authors at IBM published BLEU at ACL 2002, after an IBM research report of 2001. It became the standard automatic score of machine translation research and of the NIST and WMT evaluations.
prereqs: [machine-translation, precision-and-recall, text-tokenization]
see_also: [chrf, translation-edit-rate, comet-metric, word-error-rate, rouge, bertscore, minimum-error-rate-training, bootstrap-method]
sources:
  - paper: doi:10.3115/1073083.1073135
    title: Kishore Papineni, Salim Roukos, Todd Ward and Wei-Jing Zhu, BLEU, a method for automatic evaluation of machine translation, ACL 2002, pages 311 to 318
    locator: "Section 2.1 (modified n-gram precision and clipping), Section 2.2 (the brevity penalty and the effective reference length), Section 2.3 (the formula with N = 4 and uniform weights)"
  - paper: doi:10.18653/v1/W18-6319
    title: Matt Post, A Call for Clarity in Reporting BLEU Scores, Third Conference on Machine Translation (WMT), 2018, pages 186 to 191
    locator: "the abstract (differences of up to 1.8 points between common settings, mostly from the tokenization and normalization of the references) and the description of sacreBLEU"
  - paper: doi:10.3115/v1/W14-3346
    title: Boxing Chen and Colin Cherry, A Systematic Comparison of Smoothing Techniques for Sentence-Level BLEU, Ninth Workshop on Statistical Machine Translation, 2014, pages 362 to 367
    locator: "Section 2 (the smoothing methods, with method 3 as the exponential decay of the NIST tool)"
  - paper: "Chris Callison-Burch, Miles Osborne and Philipp Koehn, Re-evaluating the Role of BLEU in Machine Translation Research, EACL 2006, pages 249 to 256, ACL Anthology E06-1032"
    title: Callison-Burch, Osborne and Koehn 2006
    locator: the argument that a higher BLEU does not always mean a better translation
---

BLEU scores a [machine translation](/machine-translation/) output by counting how many of its word n-grams also occur in human reference translations. It clips each count, takes the geometric mean of the precisions for n = 1 to 4 over the whole test set, and multiplies by a penalty for output that is too short. The score goes from 0 to 1 (often printed times 100), higher is better, and it is defined at the corpus level, not as a mean of sentence scores. It depends on the tokenization, so a BLEU value means something only with its tokenizer and its test set.

## In plain words

You have a set of machine translations and, for each sentence, one or more translations by people. BLEU asks how many of the words and short word sequences of the machine output also appear in a human translation.

A word may count only as many times as it appears in one reference. Without this rule, an output that repeats "the" seven times would get full marks. BLEU does this for single words, pairs, triples and sequences of four words, and takes a kind of average of the four results.

Precision alone favors short output, because a three-word output can be all correct. So BLEU also lowers the score when the output is shorter in total than the references.

All counts are added over the whole test set before the score is computed. A single sentence often has no matching four-word sequence, and its unsmoothed score is then 0.

## The problem

A candidate $y$ is a list of tokens, and it comes with a non-empty list $R_y$ of references, each a list of tokens. For an $n$-gram $g$, $\mathrm{count}_x(g)$ is the number of times $g$ occurs in the list $x$. Over a corpus of candidates, define the clipped matches and the totals for $n = 1, \ldots, N$:

$$m_n = \sum_{y} \sum_{g} \min\Bigl(\mathrm{count}_y(g),\ \max_{x \in R_y} \mathrm{count}_x(g)\Bigr), \qquad t_n = \sum_y \max(|y| - n + 1, 0),$$

and the precision $p_n = m_n / t_n$. Let $c$ be the total candidate length and $r$ the sum over candidates of the reference length closest to $|y|$ (the effective reference length). Then

$$\mathrm{BP} = \begin{cases} 1 & c > r \\ e^{1 - r/c} & c \le r \end{cases}, \qquad \mathrm{BLEU} = \mathrm{BP} \cdot \exp\Bigl(\frac{1}{N}\sum_{n=1}^{N} \ln p_n\Bigr).$$

Papineni et al. (2002) use $N = 4$ and the uniform weights $1/N$. The task is to compute this number. Higher is better. The score is 0 when some $m_n$ is 0, and 1 only when every $n$-gram of the candidates is matched and $c \ge r$.

**Tokenization.** The tokens are part of the definition. The standard today is the `13a` tokenizer of sacreBLEU, which copies the NIST script mteval-v13a: it joins lines, unescapes `&quot;`, `&amp;`, `&lt;` and `&gt;`, puts spaces around punctuation and symbols, splits a period or a comma from a word unless it stands between two digits, splits a hyphen that follows a digit, and then splits on white space. The case is kept. The references must be tokenized the same way as the candidates, by the scorer and not by the system.

## The algorithm

The input is a list of candidates with their references and the order $N$. Distinct $n$-grams are found with a hash table.

```pseudo id=main
BLEU(Y, R, N)                  ▷ Y: candidates, R_y: the references of y
L1  m_n ← 0 and t_n ← 0 for n = 1 .. N
L2  c ← 0; r ← 0
L3  for each candidate y in Y do
L4      c ← c + |y|
L5      r ← r + the length in R_y closest to |y|, the shorter one on a tie
L6      for n ← 1 to N do
L7          for each distinct n-gram g of y do
L8              m_n ← m_n + min(count_y(g), max over x in R_y of count_x(g))
L9          t_n ← t_n + max(|y| - n + 1, 0)
L10 if some m_n = 0 then return 0            ▷ or smooth, see below
L11 BP ← 1 if c > r, else exp(1 - r / c)
L12 return BP · exp((1/N) Σ_n ln(m_n / t_n))
```

Lines L1 to L9 collect the sufficient statistics: $2N + 2$ integers. Line L8 is the clipping: a candidate $n$-gram counts at most as often as it occurs in the reference where it occurs most. The maximum is per reference, not a sum over references. Line L5 picks the effective reference length per sentence, and the sum over sentences is the $r$ of the brevity penalty. Lines L10 to L12 compute the score once from the sums.

**Tie rule.** When two references are equally close in length to the candidate, line L5 takes the shorter one, as sacreBLEU does. A longer $r$ gives a smaller BP, so the rule matters.

**Smoothing for one sentence.** For sentence BLEU, line L10 returns 0 too often. Method 3 of Chen and Cherry (2014), the one in the NIST tool, gives the $k$-th order with $m_n = 0$ the precision $1/(2^k t_n)$ instead. The implementation offers it for sentence scores and leaves corpus BLEU unsmoothed.

## Example

The candidate "the cat sat on the mat" (6 tokens) has the one reference "the cat sat on the red mat" (7 tokens), tokenized by white space.

| $n$ | candidate $n$-grams | matched | $p_n$ |
|---|---|---|---|
| 1 | the, cat, sat, on, the, mat | all 6 ("the" occurs twice in the reference) | 6/6 |
| 2 | the cat, cat sat, sat on, on the, the mat | all but "the mat" | 4/5 |
| 3 | the cat sat, cat sat on, sat on the, on the mat | all but "on the mat" | 3/4 |
| 4 | the cat sat on, cat sat on the, sat on the mat | all but "sat on the mat" | 2/3 |

The geometric mean is $(1 \cdot 0.8 \cdot 0.75 \cdot 0.6667)^{1/4} = 0.4^{1/4} = 0.795271$. With $c = 6$ and $r = 7$, $\mathrm{BP} = e^{1 - 7/6} = 0.846482$, so $\mathrm{BLEU} = 0.673182$, or 67.32 on the scale of 100.

Clipping: the candidate "the the the the the the the" against "the cat is on the mat" has 7 unigrams that all occur in the reference, but "the" occurs only twice there, so $p_1 = 2/7$ and not $7/7$.

Corpus level: add the pair "a dog ran in the park" with an identical reference. The sums are $m = (12, 9, 7, 5)$, $t = (12, 10, 8, 6)$, $c = 12$, $r = 13$, and corpus BLEU is 0.8281. The mean of the two sentence scores, 0.6732 and 1, is 0.8366.

## Correctness

The claim is that the procedure returns the value of the formula, and that this value is in $[0, 1]$. Lines L3 to L9 compute each sum of the definition, because the sum over the distinct $n$-grams of $y$ equals the sum over all $n$-grams (the others add 0), and a list of length $\ell$ has $\max(\ell - n + 1, 0)$ $n$-grams. Clipping gives $m_n \le t_n$, so each $\ln p_n \le 0$, and BP is at most 1, so the score is at most 1. It is 1 exactly when every $p_n = 1$ and $c \ge r$. These are theorems; the full proof is in the proofs file.

How well the score agrees with human judgments is a different question, and the answer is only measured.

## Complexity

Let $L$ be the number of tokens in all candidates and references. For each $n$, the $n$-grams of a sentence and of its references are counted, and each $n$-gram has $n$ tokens. With a hash table this takes $O(N^2 L)$ expected time. With sorting in place of hashing, the worst case is $O(N^2 L \log L)$. For $N = 4$ both are linear in practice. One sentence at a time needs $O(N L)$ space for its counts, and the corpus needs only the $2N + 2$ statistics.

## Properties

- **Range and direction.** From 0 to 1, higher is better (a theorem). Most papers print it times 100.
- **Corpus level.** The statistics add over sentences and the score is computed once. Corpus BLEU is not the mean of sentence BLEU.
- **Online.** The statistics of a new sentence are added in time linear in its length, and the score is updated from $2N + 2$ numbers.
- **Precision only.** There is no recall term. The brevity penalty works on the total length only, so one long sentence can hide a short one.
- **Order of words.** Only the higher-order $n$-grams see the order. Any permutation that keeps the same $n$-grams gets the same score.
- **More references, higher score.** A larger $R_y$ can only raise each clipped count, so scores with different numbers of references are not comparable.
- **Tokenization.** Post (2018) measured differences of up to 1.8 points between common settings on the same output (a measurement).

## Variants and improvements

- **Smoothed sentence BLEU.** Lin and Och (2004) added one to the counts for $n \ge 2$. Chen and Cherry (2014) compared seven methods. Sentence BLEU is used for tuning and for [minimum risk training](/minimum-risk-training/), where a zero score gives no signal.
- **sacreBLEU.** Post (2018) fixed the tokenization, the tie rule and the effective order in one tool, which prints a signature of its settings next to the score.
- **Other tokenizers.** For Chinese and Japanese, which have no spaces between words, sacreBLEU has tokenizers by character or by a morphological analyzer. The score then counts other units and is not comparable to a score of 13a.
- **NIST.** The NIST score of Doddington (2002) weights each matched $n$-gram by how rare it is and uses an arithmetic mean.
- **Character n-grams.** [chrF](/chrf/) uses character n-grams and both precision and recall. It is less sensitive to tokenization and morphology.
- **Edit-based and learned scores.** [TER](/translation-edit-rate/) counts edits, and [COMET](/comet-metric/) and [BERTScore](/bertscore/) use neural representations.

## When to use it

Use corpus BLEU to compare systems on the same test set, with the same references and the same tokenizer, and report the sacreBLEU signature. It is fast, needs no model and has a long record, so it works for tracking a system during development. Do not use it to compare scores across papers that do not state their settings, to compare scores across test sets or languages, or to judge single sentences. For final claims, measured agreement with human judgments is better for chrF and for learned scores such as COMET.

## Pitfalls

- **Your own tokenization.** Scoring tokenized or BPE-split output against tokenized references gives a higher number than sacreBLEU on detokenized text. Score the detokenized output.
- **Mean of sentence scores.** Averaging sentence BLEU does not give corpus BLEU, and unsmoothed sentence scores are often 0.
- **The scale.** Code that returns 0 to 1 and a table that prints 0 to 100 get mixed up. State the scale.
- **Sum over references.** Clipping at the sum of the reference counts, instead of the maximum, lets a repeated word score too often.
- **Shortest or closest.** Some old scripts used the shortest reference length for BP. With several references this gives another score.
- **Small differences.** A gap of a few tenths of a point can come from chance in the test set. Use paired [bootstrap resampling](/bootstrap-method/) before claiming a gain. Callison-Burch et al. (2006) also showed that a higher BLEU does not always mean a better translation.

## Implementations

## History

Kishore Papineni, Salim Roukos, Todd Ward and Wei-Jing Zhu of IBM described BLEU in a research report in 2001 and at ACL 2002. They wanted a cheap score that would let researchers test changes daily, and they showed that it ranked systems in the same order as human judges on their data. NIST adopted a variant for its evaluations, and BLEU became the main score of statistical and then neural machine translation. Its limits were known early: Callison-Burch, Osborne and Koehn (2006) showed cases where large BLEU differences did not match human judgments. In 2018 Matt Post released sacreBLEU to make reported scores comparable. Since about 2020 the WMT metrics tasks have found learned metrics to agree better with people, and many papers now report BLEU next to chrF and COMET.

## References
