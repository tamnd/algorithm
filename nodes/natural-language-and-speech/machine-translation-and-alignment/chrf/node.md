---
tag: TFBFZV
kind: algorithm
slug: chrf
name: chrF
aliases:
- character n-gram F-score
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: An F-score of character n-gram precision and recall between a translation and a reference, weighting recall more. Higher is better, from 0 to 1, at the corpus level.
model: word-ram
complexity:
  vars: {L: the number of characters in all hypotheses and references, N: the largest n-gram order}
  time: {worst: "O(N² L log L)"}
  space: {extra: "O(N L)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2015
  people: [Maja Popović]
  note: Popović proposed chrF at the WMT 2015 metrics task and added word n-grams as chrF++ in 2017. sacreBLEU made chrF with six character orders and beta 2 a standard score next to BLEU.
prereqs: [precision-and-recall, machine-translation]
see_also: [bleu, translation-edit-rate, comet-metric, word-error-rate, rouge, bertscore, subword-tokenization, edit-distance]
sources:
  - paper: doi:10.18653/v1/W15-3049
    title: Maja Popović, chrF, character n-gram F-score for automatic MT evaluation, Tenth Workshop on Statistical Machine Translation, 2015, pages 392 to 395
    locator: "Equation 1 (the F-score of the averaged precision and recall), and the experiments on WMT12 to WMT14 (six-grams best, spaces ignored, beta 3 the most promising)"
  - paper: "Maja Popović, chrF++, words helping character n-grams, Second Conference on Machine Translation (WMT), 2017, pages 612 to 618"
    title: Popović 2017
    locator: the word n-grams of order 1 and 2 added to the average
  - paper: doi:10.18653/v1/W18-6319
    title: Matt Post, A Call for Clarity in Reporting BLEU Scores, Third Conference on Machine Translation (WMT), 2018, pages 186 to 191
    locator: sacreBLEU, which provides the reference implementation of chrF used here
---

chrF scores a [machine translation](/machine-translation/) output against a reference by its character n-grams. It averages the precision and the recall of the character n-grams of orders 1 to 6, with white space removed, and combines them into an F-score that weights recall $\beta$ times as much as precision. The score goes from 0 to 1 (sacreBLEU prints it times 100), higher is better, and sacreBLEU computes it at the corpus level from summed counts. It needs no word tokenizer, so it is less sensitive than [BLEU](/bleu/) to tokenization and to word endings.

## In plain words

Remove the spaces from the machine output and from the human translation. Then look at every piece of 1 character, 2 characters, and so on up to 6 characters.

Precision asks what share of the pieces of the output also appear in the reference. Recall asks what share of the pieces of the reference also appear in the output. A piece counts at most as often as it appears on the other side.

chrF averages the precision over the six piece lengths, and the recall too, and then combines the two numbers. With the usual setting the recall counts more, so missing content costs more than extra content.

Because the pieces are short, "read" and "reads" share most of their pieces, and a wrong word ending loses only a little.

## The problem

A hypothesis $y$ and a reference $x$ are strings. Let $h$ and $r$ be the same strings with all white space removed. For a string $z$, $\mathrm{count}_z(g)$ is the number of times the character $n$-gram $g$ occurs in $z$. Summed over the corpus, the matches, the hypothesis $n$-grams and the reference $n$-grams of order $n$ are

$$M_n = \sum \sum_g \min\bigl(\mathrm{count}_h(g), \mathrm{count}_r(g)\bigr), \qquad H_n = \sum \max(|h| - n + 1, 0), \qquad E_n = \sum \max(|r| - n + 1, 0).$$

Let $K$ be the set of orders $n \le N$ with $H_n > 0$ and $E_n > 0$. Then

$$P = \frac{1}{|K|}\sum_{n \in K} \frac{M_n}{H_n}, \qquad R = \frac{1}{|K|}\sum_{n \in K} \frac{M_n}{E_n}, \qquad \mathrm{chrF}_\beta = \frac{(1 + \beta^2)\, P\, R}{\beta^2 P + R},$$

and the score is 0 if $K$ is empty or $P + R = 0$. Popović (2015) wrote the formula with the averages over the orders as in her Equation 1. The settings here are those of sacreBLEU: $N = 6$, $\beta = 2$, the case kept, and white space removed. Higher is better.

**Tokenization.** There is no word tokenization. The only step is to delete every white-space character, so "the cat" and "thecat" give the same n-grams. The text is not lowercased.

## The algorithm

The input is a list of hypotheses, each with its references, the order $N$ and $\beta$. With several references, each sentence uses the reference that gives it the highest sentence chrF.

```pseudo id=main
CHRF(Y, X, N, β)                ▷ Y: hypotheses, X_y: the chosen reference of y
L1  M_n ← 0, H_n ← 0, E_n ← 0 for n = 1 .. N
L2  for each hypothesis y with its reference x do
L3      h ← y without white space; r ← x without white space
L4      for n ← 1 to N do
L5          M_n ← M_n + Σ over distinct n-grams g of h of min(count_h(g), count_r(g))
L6          H_n ← H_n + max(|h| - n + 1, 0); E_n ← E_n + max(|r| - n + 1, 0)
L7  K ← the orders n with H_n > 0 and E_n > 0
L8  if K is empty then return 0
L9  P ← (1/|K|) Σ_{n in K} M_n / H_n; R ← (1/|K|) Σ_{n in K} M_n / E_n
L10 if P + R = 0 then return 0
L11 return (1 + β²) P R / (β² P + R)
```

Lines L1 to L6 collect $3N$ integers. Line L5 takes the size of the multiset intersection of the two sets of $n$-grams, which is the clipped match count of [BLEU](/bleu/) with one reference. Line L7 is the effective order of sacreBLEU: an order where one side has no $n$-gram at all (a text shorter than $n$ characters) is left out of both averages, instead of adding a precision of 0. Line L11 is the weighted harmonic mean of $P$ and $R$.

**chrF++.** Popović (2017) adds word $n$-grams of orders 1 and 2. Their statistics are computed in the same way, on words, and lines L7 to L11 average over all 8 orders together. sacreBLEU splits words on white space and then splits one punctuation mark off the end of a word, or else off its start.

## Example

The hypothesis "the cats" has the reference "the cat". Without spaces, $h$ = "thecats" (7 characters) and $r$ = "thecat" (6 characters). Every $n$-gram of $r$ occurs in $h$.

| $n$ | $M_n$ | $H_n$ | $E_n$ | precision | recall |
|---|---|---|---|---|---|
| 1 | 6 | 7 | 6 | 6/7 | 1 |
| 2 | 5 | 6 | 5 | 5/6 | 1 |
| 3 | 4 | 5 | 4 | 4/5 | 1 |
| 4 | 3 | 4 | 3 | 3/4 | 1 |
| 5 | 2 | 3 | 2 | 2/3 | 1 |
| 6 | 1 | 2 | 1 | 1/2 | 1 |

So $P = 0.734524$ and $R = 1$. With $\beta = 2$, $\mathrm{chrF} = 5 \cdot 0.734524 / (4 \cdot 0.734524 + 1) = 0.932588$. With $\beta = 1$ it is $0.846946$. The extra "s" costs little under $\beta = 2$, because it lowers only the precision.

A short check: the hypothesis "ab" against "abc" with $N = 2$ gives $P = 1$, $R = (2/3 + 1/2)/2 = 7/12$ and $\mathrm{chrF}_2 = 7/11$.

## Correctness

The claim is that the procedure returns the value of the formula and that it is in $[0, 1]$. Line L5 sums over the distinct $n$-grams of $h$, which equals the sum over all $n$-grams because the others add 0. Each match count is at most both totals, so $P$ and $R$ are in $[0, 1]$. When both are positive, $1/\mathrm{chrF}_\beta = \frac{1}{1 + \beta^2} \cdot \frac{1}{P} + \frac{\beta^2}{1 + \beta^2} \cdot \frac{1}{R}$, so the score is a weighted harmonic mean and lies between $P$ and $R$. With $\beta = 1$ it is symmetric in the hypothesis and the reference. These are theorems; the full proof is in the proofs file.

How well the score agrees with human judgments is measured, not proved.

## Complexity

Let $L$ be the number of characters in all hypotheses and references. Order $n$ counts $n$-grams of $n$ characters, so the counting costs $O(N^2 L)$ expected time with a hash table, or $O(N^2 L \log L)$ in the worst case with sorting. With $k$ references per sentence, each reference is scored once, and $L$ includes all of them. One sentence at a time needs $O(N L)$ space for its counts, and the corpus needs only $3N$ numbers.

## Properties

- **Range and direction.** From 0 to 1, higher is better (a theorem). sacreBLEU prints it times 100.
- **Corpus level.** sacreBLEU sums the counts over the corpus and computes the score once. The sentence score is the same formula on one sentence.
- **Recall weighted.** With $\beta = 2$ the recall has four times the weight of the precision in the harmonic mean (a theorem about the formula). In Popović (2015), chrF3 agreed better with human judgments than chrF1 (a measurement).
- **No tokenizer.** Without word orders, the score does not change if spaces are added or removed. It does change with the case and with punctuation.
- **Morphology.** Words with the same stem share most of their n-grams, so a wrong inflection is only a small error. This helps for languages with rich morphology.
- **Symmetric for beta 1.** chrF1 does not change if the hypothesis and the reference change places.

## Variants and improvements

- **The beta.** Popović (2015) found chrF3 the most promising on the WMT14 data, with $\beta = 3$ chosen without tuning. sacreBLEU and the WMT tasks use $\beta = 2$.
- **chrF++.** Word unigrams and bigrams in the average. Popović (2017) found that this agrees better with human judgments in many language pairs (a measurement).
- **White space as a character.** sacreBLEU can keep the spaces. Popović (2015) found no gain from this.
- **Per-order averaging of F.** sacreBLEU has an option that computes an F-score per order and averages the F-scores, to match older scripts. It gives other numbers from the same counts.
- **Other scores.** [BLEU](/bleu/) uses word n-grams and only precision. [TER](/translation-edit-rate/) counts edits. [COMET](/comet-metric/) is a trained model.

## When to use it

Use chrF next to BLEU when the target language has rich morphology or no spaces between words, and when you do not want to depend on a word tokenizer. It is cheap and needs no model. Report the sacreBLEU signature, because $N$, $\beta$, the word order and the white-space setting all change the number. For final claims about quality, a trained metric or a human evaluation is better.

## Pitfalls

- **Settings not stated.** chrF1, chrF2, chrF3 and chrF++ are different scores. State $\beta$ and the word order.
- **Mean of sentence scores.** The mean of sentence chrF is not corpus chrF. Use one of the two and say which.
- **Short texts.** For a text shorter than six characters, the effective order leaves out the higher orders. Without this rule the precision of those orders would be 0 and the score would drop.
- **Case and punctuation.** They count as characters. Lowercasing or removing punctuation gives another score.
- **Spaces are lost.** "a part" and "apart" give the same n-grams, so an error in word boundaries is not seen.

## Implementations

## History

Maja Popović proposed chrF at the WMT 2015 metrics task. She tested n-grams of up to 6 characters and several values of $\beta$, and found that six-grams worked best and that $\beta = 3$ looked most promising on the WMT14 data. She added word n-grams as chrF++ in 2017. Matt Post included chrF in sacreBLEU in 2018 with $\beta = 2$, and since then many papers report chrF next to BLEU.

## References
