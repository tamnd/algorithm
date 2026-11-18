---
tag: BAJBZ1
kind: algorithm
slug: punkt-sentence-tokenizer
name: Punkt sentence tokenizer
aliases:
- Kiss-Strunk sentence boundary detection
area: natural-language-and-speech/tokenization-and-text-normalization
level: core
summary: Unsupervised sentence boundary detection of Kiss and Strunk. It finds abbreviations, initials and ordinal numbers by collocation statistics on raw text.
solves: [sentence-boundary-detection]
model: word-ram
complexity:
  vars: {n: the number of characters of the text}
  time: {expected: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2006
  people: [Tibor Kiss, Jan Strunk]
  note: Kiss and Strunk described abbreviations as collocations of a word and a period in 2002, and published the full two-stage system Punkt in Computational Linguistics in 2006.
prereqs: [sentence-boundary-detection, likelihood-ratio-test]
see_also: [binomial-distribution, maximum-likelihood-estimation, chi-squared-test-of-independence, penn-treebank-tokenization, text-tokenization, truecasing, precision-and-recall, naive-bayes-classifier]
sources:
  - url: https://aclanthology.org/J06-4003/
    title: Tibor Kiss and Jan Strunk, Unsupervised multilingual sentence boundary detection, Computational Linguistics 32(4), 2006
    locator: pages 485 to 525; Section 2 (likelihood ratios), Section 3 (type-based stage, Table 2), Section 4 (token-based stage, Figure 3), Section 5 (development), Section 6 (evaluation)
  - url: https://aclanthology.org/J93-1003/
    title: Ted Dunning, Accurate methods for the statistics of surprise and coincidence, Computational Linguistics 19(1), 1993
    locator: pages 61 to 74 (the log likelihood ratio for bigrams)
  - url: https://www.nltk.org/api/nltk.tokenize.punkt.html
    title: NLTK documentation, module nltk.tokenize.punkt
    locator: the classes PunktTrainer and PunktSentenceTokenizer
---

The Punkt sentence tokenizer of Kiss and Strunk (2006) decides which periods in a text end a sentence, and it learns everything it needs from raw text, with no labeled data and no word lists. It treats an abbreviation as a collocation of a word and its period: a type that almost always has a period, is short, and has internal periods is an abbreviation. A second pass looks at the word after each doubtful period and uses its capitalization, collocations and the list of frequent sentence starters. Punkt is one algorithm for [sentence boundary detection](/sentence-boundary-detection/); the problem page also covers supervised and rule-based methods.

## In plain words

Most periods end a sentence. The hard cases are short words with a period, such as "Dr." or "etc.", initials such as "J.", and numbers such as "12." in a date.

Punkt first counts how often each word appears with a period and without one. A short word that nearly always has a period is taken as an abbreviation, and its period does not end the sentence.

Then it looks at the word after each doubtful period. If that word is capitalized but is normally written in lower case, a new sentence probably starts. If it is in lower case, the sentence goes on. If the pair of words, such as "J. Smith", occurs together often, the period is part of the name. Words that often start sentences, such as "However", also show a boundary.

## The problem

The input is a text. Tokens are the runs of characters between white space; quotes and brackets at the ends of a token are ignored. The output marks, for each token, whether a sentence ends after it. A token with a final ? or ! always ends a sentence, and the last token ends the last sentence. For a token with a final period, the procedure must decide between a sentence period and an abbreviation period, and an abbreviation period can also end a sentence ("We sold pears etc. However, ..."). The type of a token is its word in lower case without the final marks, and every number is folded into one type NUMBER. A possible initial is a single letter with a period.

## The algorithm

Let $N$ be the number of tokens, $C(w)$ the number of tokens of type $w$, $C(w, \bullet)$ the number of them with a final period, $C(w, \neg\bullet)$ the rest, and $C(\bullet)$ the number of tokens with a final period. The type stage uses the revised log likelihood ratio of the hypotheses $P(\bullet \mid w) = C(\bullet)/N$ and $P(\bullet \mid w) = 0.99$, with $k = C(w, \bullet)$ and $m = C(w, \neg\bullet)$:

$$\log\lambda(w) = -2\bigl(k \ln p + m \ln(1-p) - k \ln 0.99 - m \ln 0.01\bigr), \quad p = C(\bullet)/N.$$

The length $\mathrm{len}(w)$ is the number of characters other than periods.

```pseudo id=main
PUNKT(t[1..N])                               ▷ tokens with types, final marks and case
L1  count C(w), C(w, •), C(•) and N
L2  for each type w with a letter and C(w, •) > 0, other than NUMBER
L3      S(w) ← log λ(w) · e^(-len(w)) · (internal periods of w + 1) / len(w)^C(w, ¬•)
L4      w is an abbreviation if S(w) ≥ 0.3
L5  first pass: t[i] ends a sentence if it has a final ? or !, or a final period and a type that is not an abbreviation
L6  from the first pass, collect the case flags of each type, the frequent starters and the bigrams after a period
L7  for i ← 1 to N - 1 such that t[i] has a final period or is an ellipsis
L8      if t[i] is an ellipsis, or has an abbreviation type and is not a possible initial
L9          end[i] ← ORTHO(t[i+1]) = yes, or t[i+1] is capitalized and its type is a frequent starter
L10     else if t[i] is a possible initial or a number
L11         if COLLOC(t[i], t[i+1]) and t[i+1] is not a frequent starter, or ORTHO(t[i+1]) = no
L12             end[i] ← false
L13         else if t[i] is an initial, ORTHO(t[i+1]) = undecided, and t[i+1] is capitalized and its type is never seen in lower case
L14             end[i] ← false
L15 end[N] ← true; return end
```

Line L6 sets four flags for each type: seen with an upper case first letter at a sentence start, upper case inside a sentence, lower case at a start, and lower case inside. A token counts as a sentence start if the token before it is a first-pass boundary, and as inside a sentence if the token before it has no final mark. Tokens after an abbreviation, an ellipsis, an initial or a number are skipped, because their position is not yet known. The orthographic heuristic ORTHO (Figure 3 of the paper) says yes if the next token is capitalized, its type is seen in lower case, and it is never seen capitalized inside a sentence. It says no if the next token is in lower case and its type is seen capitalized or never seen in lower case at a sentence start, or if the next token is a punctuation mark. Otherwise it is undecided.

COLLOC and the frequent starters use Dunning's log likelihood ratio for a bigram, with $p = C(w_2)/N$, $p_1 = C(w_1, w_2)/C(w_1)$ and $p_2 = (C(w_2) - C(w_1, w_2))/(N - C(w_1))$, plus the one-sided condition $C(w_1, w_2)/C(w_1) > C(w_2)/N$. A pair is a collocation at $\log\lambda \ge 7.88$, the 99.5% point of the chi-squared distribution with one degree of freedom. For the starters, $w_1$ is a sure sentence boundary: a first-pass boundary period on a token that is not an initial or a number. A type is a frequent starter at $\log\lambda \ge 30$.

## Example

The text is a block of 15 lines repeated 5 times, so that the counts are large enough: N = 445 tokens, of which C(•) = 120 have a final period, and 74 are sure sentence boundaries. One block is: "The dog met Dr. Brown at the park. We saw Dr. Brown and the cat. They sold apples, pears etc. and the rest. She came home late. However, the dog ran to the park. J. Smith saw the cat. The cat saw J. Smith at home. We bought pears etc. Then we went home. On 12. May the shop was closed. The park was quiet. We ate and then we slept. However, it rained. However, we stayed home. We sold pears etc. However, the cat slept. Mo. Brown left."

The type stage gives $S$ = 3.52 for dr (10 times with a period, never without), 1.94 for etc, 9.57 for j and 1.76 for mo, so these four are abbreviations. The type park has 10 periods but also 5 tokens without one, so $\log\lambda = -16.9$ and it is not one. The type late has 5 periods and none without, but its length is 4 and $S = 0.238 < 0.3$. The frequent starters are however ($\log\lambda$ = 35.57) and we (33.17).

| period | next token | line | evidence | first pass | final |
|---|---|---|---|---|---|
| Dr. | Brown | L9 | ORTHO undecided (brown is never seen in lower case), not a starter | no | no |
| etc. | and | L9 | ORTHO no: and is in lower case and never seen in lower case at a sentence start | no | no |
| etc. | Then | L9 | ORTHO yes: then is seen in lower case and never capitalized inside a sentence | no | yes |
| etc. | However | L9 | ORTHO undecided, but However is capitalized and a frequent starter | no | yes |
| J. | Smith | L11 | collocation j, smith with $\log\lambda$ = 95.68 | no | no |
| 12. | May | L11 | collocation NUMBER, may with $\log\lambda$ = 54.83, may is not a starter | yes | no |
| Mo. | Brown | L9 | ORTHO undecided, not a starter | no | no |
| park. | However | none | park is not an abbreviation, initial or number | yes | yes |

The first pass makes 3 mistakes in each block (etc. Then, etc. However and 12. May), and the token stage corrects all 15 in the text. All 85 sentences are found. The same block repeated 8 times shows the weak point of the method: late, left and rest then reach $S \ge 0.3$ and become abbreviations, because they never occur without a period.

## Correctness

Punkt is a heuristic classifier, so there is no guarantee that a decision is right. The proof in proofs/correctness.md shows that the procedure computes the decision rules of the paper, case by case, and that the statistics behave as the rules assume. It proves that $\log\lambda(w) = 2k\ln(0.99/p) > 0$ for a type that never occurs without a period, which explains the pitfall above. It proves that Dunning's ratio is never negative and is 0 exactly when $p_1 = p_2$, and that the one-sided condition holds exactly when $p_1 > p_2$, so a frequent word that follows less often than expected is not taken as a collocation. The tests check the values of Table 1 and Table 2 of the paper and compare the procedure with a slow version that counts by scanning on 500 random texts.

## Complexity

- **Time.** Expected $O(n)$ for a text of $n$ characters. Tokenization is one pass. The counts, the case flags, the bigram counts and the starters are hash table updates, one or two per token. Each decision of lines L7 to L14 looks up a constant number of counts.
- **Space.** $O(n)$ for the tokens and the tables of types and bigrams.

## Properties

- **Unsupervised.** All statistics come from the text itself; the paper applies Punkt to the text that it splits.
- **Few parameters.** The values 0.99, 0.3, 7.88 and 30 are fixed. The paper found the scaling factors and thresholds by manual experiments on 10 MB of Wall Street Journal text and used them for all languages. They are rules of thumb, not derived values.
- **Language independent.** The paper evaluates Punkt on newspaper text in eleven languages, with a mean accuracy of 99.38%, which is a measurement.
- **One-sided reclassification of initials and numbers.** The token stage can only remove a boundary after an initial or a number, never add one.
- **Not online.** All counts must be known before the first decision.

## Variants and improvements

- **Separate training.** NLTK splits Punkt into a trainer and a tokenizer: PunktTrainer learns the abbreviations, collocations and sentence starters from a corpus, and PunktSentenceTokenizer applies them to new text. NLTK ships pre-trained models, which avoids the small-text problem. Its formulas and default settings differ from the paper in details, so results differ.
- **Supervised methods.** With labeled data, a classifier over features of the period context, such as the maximum entropy model of Reynar and Ratnaparkhi (1997), learns the decision directly. See [sentence boundary detection](/sentence-boundary-detection/).
- **Other marks.** The paper treats ? and ! as sure boundaries. Text with colons, semicolons or line breaks as boundaries, or with no punctuation at all, needs other methods.

## When to use it

Use Punkt for running text in a language that marks abbreviations with a period, when no labeled data and no abbreviation list are at hand, or when the text is from a new domain with its own abbreviations. Train it on a large amount of text from the same domain. For text that is all in upper case or all in lower case, the orthographic heuristic rarely decides, so expect more errors. For speech transcripts and text without punctuation, use a sequence model instead.

## Pitfalls

- **A small or repetitive text.** Line L4 classifies any short type that never occurs without a period as an abbreviation once it is frequent enough, so in a small text a word that always ends a sentence, such as "late", becomes an abbreviation. Train line L1 on a large text and apply the model to the target text.
- **The two-sided test.** If line L11 uses $\log\lambda \ge 7.88$ without the condition $C(w_1, w_2)/C(w_1) > C(w_2)/N$, a frequent word that follows $w_1$ less often than expected counts as a collocation. Table 1 of the paper shows this for the German "ist" after a sentence boundary, with $\log\lambda$ = 169.8. Keep the one-sided condition.
- **Numbers before frequent words.** Line L11 can find a collocation of NUMBER with a common word such as "the" if many sentences end in a number and the next starts with "The". The period after the number is then never a boundary. A frequent starter blocks the collocation, which is why line L11 checks it.
- **Initials in the abbreviation branch.** If line L8 also takes possible initials, an initial is judged only by ORTHO and the starters, and the collocation rule and the proper name rule of lines L11 and L13 are lost. Send single letters to line L10, as the paper does.
- **Counting unknown positions.** If line L6 counts the token after an abbreviation as inside a sentence, as the first pass says, then "etc. Then" gives the type then an upper case inside bit, and ORTHO can no longer say yes for it. Skip tokens whose position is not decided.

## Implementations

## History

Tibor Kiss and Jan Strunk first described abbreviation detection as collocation detection with a log likelihood ratio in 2002. Their 2006 paper in Computational Linguistics added the scaling factors, the token-based stage with the orthographic, collocation and frequent starter heuristics, and the special handling of initials and ordinal numbers. It reported error rates from 0.35% to 2.12% on newspaper corpora in eleven languages, with a mean of 1.26%, against a mean of 1.77% for the supervised MxTerminator, which the authors trained on the same corpora. NLTK later made Punkt its standard sentence splitter.

## References
