---
tag: 01YMRN
kind: algorithm
slug: noisy-channel-spelling-correction
name: Noisy channel spelling correction
aliases:
- Kernighan-Church-Gale correction
- noisy channel model of spelling
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Chooses the correction w that maximizes P(w) P(typed word | w), from a language model and an error model of single edits.
solves: [approximate-dictionary-lookup]
model: word-ram
complexity:
  vars: {n: the length of the typed string, s: the size of the alphabet}
  time: {expected: O(n^2 s)}
  space: {extra: O(n s)}
properties: {deterministic: true, recursive: false}
history:
  year: 1990
  people: [Mark D. Kernighan, Kenneth W. Church, William A. Gale]
  note: Kernighan, Church and Gale described the program correct at COLING 1990, with candidates one edit away and four confusion matrices; Brill and Moore generalized the edits in 2000.
prereqs: [edit-distance, damerau-levenshtein-distance, bayes-theorem]
see_also: [weighted-edit-distance, levenshtein-automaton, approximate-dictionary-lookup, naive-bayes-classifier, maximum-likelihood-estimation, expectation-maximization, query-auto-completion, most-popular-completion]
sources:
  - paper: doi:10.3115/997939.997975
    title: Mark D. Kernighan, Kenneth W. Church and William A. Gale, A spelling correction program based on a noisy channel model, Proceedings of the 13th International Conference on Computational Linguistics (COLING 1990), volume 2, 205-210
    locator: the candidates that differ from the typo by one insertion, deletion, substitution or reversal, the scoring by prior times channel, the four confusion matrices, and their estimation by iteration from equal starting values
  - paper: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, 3rd edition draft, Appendix D: Spelling Correction and the Noisy Channel, https://web.stanford.edu/~jurafsky/slp3/D.pdf"
    locator: Equation D.6 (the channel probability of each edit type from the del, ins, sub and trans matrices and the letter counts), the acress example with its candidates and scores (Figures D.3 to D.5), and the section on the Brill and Moore error model
  - paper: doi:10.3115/1075218.1075255
    title: Eric Brill and Robert C. Moore, An improved error model for noisy channel spelling correction, Proceedings of the 38th Annual Meeting of the Association for Computational Linguistics (ACL 2000), 286-293
    locator: the partition model, in which a word is split into parts and each part is rewritten as a string of any length, with probabilities that depend on the position in the word
---

Noisy channel spelling correction is a method that corrects a typed string $x$ that is not a word by choosing the word $w$ that maximizes $P(w)\, P(x \mid w)$. The prior $P(w)$ comes from word counts in a corpus, and the channel $P(x \mid w)$ is the probability that a writer who meant $w$ typed $x$. Kernighan, Church and Gale described it in 1990 for words one edit away from $x$, with the channel read from four confusion matrices of typing errors. The [edit distance](/edit-distance/) and [Damerau-Levenshtein distance](/damerau-levenshtein-distance/) pages count edits with fixed costs; this page puts probabilities on the edits and on the words, and the [weighted edit distance](/weighted-edit-distance/) page covers costs that vary by letter.

## In plain words

When someone types a word that is not in the dictionary, the program asks two questions about each nearby word. How common is this word? And how likely is this particular slip, if the person meant this word? Some slips are common, such as missing a letter after "t" or hitting a key next to the right one, and some are rare. The program multiplies the two answers and picks the word with the best result. A rare word can win when the slip that leads to it is very common, and a common word can win even with an odd slip.

## The problem

The input is a typed string $x$, a vocabulary $V$ with counts $c(w)$ and total $N$, and an error model. If $x \in V$, keep it; correcting real words needs context and is a variant. Otherwise return

$$\hat w = \arg\max_{w \in V} P(w)\, P(x \mid w), \qquad P(w) = \frac{c(w)}{N},$$

with ties to the smaller word in string order. By [Bayes' theorem](/bayes-theorem/), $P(w \mid x) = P(w) P(x \mid w) / P(x)$, and $P(x)$ is the same for every $w$, so $\hat w$ is also the most probable intended word.

The error model allows one edit. Following Jurafsky and Martin's Equation D.6, with $\#$ before the first letter, the channel of one edit is a confusion count over the corpus count of the intended letters:

| edit from $w$ to $x$ | table entry | divided by |
|---|---|---|
| delete $c$ after $p$ ("pc" typed as "p") | $\mathrm{del}[p, c]$ | $\mathrm{count}[pc]$ |
| insert $c$ after $p$ ("p" typed as "pc") | $\mathrm{ins}[p, c]$ | $\mathrm{count}[p]$ |
| substitute $c$ by $e$ ($c$ typed as $e$) | $\mathrm{sub}[c, e]$ | $\mathrm{count}[c]$ |
| swap "cd" into "dc" | $\mathrm{trans}[c, d]$ | $\mathrm{count}[cd]$ |

When several edits turn $w$ into $x$, $P(x \mid w)$ is the sum of their probabilities.

## The algorithm

The candidates are found from $x$ by undoing each possible edit, so the vocabulary is only used for lookups:

```pseudo id=main
NOISY-CHANNEL-CORRECT(x, V, c, M)      ▷ M: the four tables and the letter counts
L1  if x ∈ V then return x
L2  C ← empty map from words to channel probabilities
L3  for each position i from 0 to |x| and each letter a:           ▷ a was deleted
L4      add del[x(i−1), a] / count[x(i−1) a] to C[x(<i) a x(≥i)]
L5  for each position i of x:
L6      add ins[x(i−1), x(i)] / count[x(i−1)] to C[x without x(i)]     ▷ x(i) was inserted
L7      for each letter a ≠ x(i): add sub[a, x(i)] / count[a] to C[x with a at i]
L8  for each i with x(i) ≠ x(i+1):                                   ▷ two letters were swapped
L9      add trans[x(i+1), x(i)] / count[x(i+1) x(i)] to C[x with x(i), x(i+1) swapped]
L10 keep in C only the words of V with a positive value
L11 for each w in C: score(w) ← c(w)/N · C[w]
L12 return the w of C with the largest score, ties to the smaller word
```

Here $x(-1)$ is $\#$. A zero count in a table, or a zero letter count, gives the probability 0, and such a candidate is dropped at line L10.

## Example

Use the eight documents of the shared toy collection as the corpus: 79 tokens of 50 words, with $\#$ before each token for the letter counts. Take these confusion counts, which stand for a small log of typing errors:

| table | entries |
|---|---|
| del | [t, e] = 6, [t, i] = 3, [e, r] = 2, [r, a] = 1 |
| ins | [t, d] = 1, [s, s] = 2 |
| sub | [h, m] = 1, [e, a] = 4, [a, e] = 3 |
| trans | [i, s] = 2, [e, i] = 1 |

The corpus has $\mathrm{count}[t] = 31$, $\mathrm{count}[te] = 9$, $\mathrm{count}[ti] = 4$ and $\mathrm{count}[h] = 9$.

For $x$ = "sortd", lines L3 to L9 find two words of the vocabulary. "sorted" lost an "e" after "t", with the channel $6/9 \approx 0.6667$ and the prior $5/79$, so the score is $0.04219$. "sort" got an extra "d" after "t", with the channel $1/31 \approx 0.03226$ and the prior $1/79$, so the score is $0.000408$. The answer is "sorted", which both factors favour.

For $x$ = "tme" the two factors disagree:

| candidate | edit | $P(x \mid w)$ | $P(w)$ | score |
|---|---|---|---|---|
| the | h typed as m | $1/9 = 0.1111$ | $3/79$ | 0.004219 |
| time | i deleted after t | $3/4 = 0.75$ | $1/79$ | 0.009494 |

"the" is three times as common as "time", but losing an "i" after "t" is much more likely than typing "m" for "h" in this error log, so the answer is "time". Jurafsky and Martin show the same effect on real data: for "acress" with COCA counts, "across" scores about $2.8 \times 10^{-9}$ and "actress" about $2.7 \times 10^{-9}$, so a unigram prior picks "across" although the writer meant "actress" in their example sentence. Only context can settle such cases.

## Correctness

The file proofs/correctness.md gives the proof. Each tuple that lines L3 to L9 enumerate is the inverse of exactly one single edit from some string $w$ to $x$: the kind of edit, its position and its letter fix both the string and the confusion entry. So the value that line L10 keeps for $w$ is the sum of the probabilities of all derivations of $x$ from $w$, which is $P(x \mid w)$, and every word with $P(x \mid w) > 0$ appears. Words that do not appear have score 0. Line L12 scans the candidates in string order and replaces the best only on a strictly larger score, which gives the tie rule.

## Complexity

For $|x| = n$ and an alphabet of $s$ letters, lines L3 to L9 build $O(ns)$ strings of length at most $n + 1$. Each costs $O(n)$ to build and to look up in hash tables for $V$ and for the confusion tables, so a correction takes $O(n^2 s)$ expected time and $O(ns)$ extra space, independent of the size of the vocabulary. Building the letter counts is one pass over the corpus, and the confusion tables have at most $(s + 1)^2$ entries each.

## Properties

- **Two independent parts.** The language model and the error model are trained apart, from text and from pairs of typos and corrections, and either can be replaced.
- **Exact for its model.** The answer is the exact argmax over the vocabulary for a one-edit channel, not an approximation; words two edits away are never proposed.
- **Context-free.** The unigram prior ignores the surrounding words, so it cannot tell "across" from "actress" by meaning.
- **Deterministic.** The tie rule fixes the answer when two scores are equal.

## Variants and improvements

- **Context.** Replace $P(w)$ by the probability of $w$ given the neighbouring words, as from a bigram model. This also makes it possible to correct real words, such as "there" for "their", by adding $x$ itself to the candidates with a probability of no error.
- **Generic edits.** Brill and Moore's partition model splits $w$ into parts and lets each part become any string, such as "ph" typed as "f" or "al" typed as "le", with probabilities that depend on the position in the word (beginning, middle or end). It takes the probability of the best partition in place of a sum over all of them, as Jurafsky and Martin's Equation D.11 writes it.
- **Learning the tables.** Kernighan, Church and Gale also estimated the confusion matrices by iteration: start from equal values, correct a corpus of typos, count the edits of the chosen corrections, and repeat. This is close in spirit to [expectation maximization](/expectation-maximization/).
- **Candidates at distance two.** Apply the edits twice, or search the vocabulary with a [Levenshtein automaton](/levenshtein-automaton/) or another [approximate dictionary lookup](/approximate-dictionary-lookup/) method. The channel of two edits is the product of their probabilities.
- **Query spelling.** For a search box, train the prior on past queries, so that names and new words that a dictionary lacks are known, and correct whole queries word by word with a model of the query.
- **Smoothing.** Add a small constant to every count, so that an edit or a word that the training data did not show still gets a small probability.

## When to use it

Use the noisy channel when you have word counts from the target domain and some data about typing errors, and you want a ranked list of corrections with a clear meaning. It suits search boxes, form fields and text editors, where most errors are one edit away. When the errors depend on context or on sound, add a context model or generic edits.

## Pitfalls

- **Zero counts.** An edit that the error log never shows gets probability 0, which hides the right word. Smooth the tables.
- **Order of the indexes.** Papers write the confusion matrices with different index orders, such as $\mathrm{sub}[x, w]$ or $\mathrm{sub}[w, x]$. State which letter is the intended one and which is the typed one, as the table of this page does.
- **Unknown words.** A correct word that is not in the vocabulary, such as a new product name, is "corrected" to a known one. Keep $x$ unless the best candidate beats it by a margin, or ask the user.
- **Mixing the two models.** The prior and the channel are on very different scales. Many systems put a weight on the log of one of them, tuned on held-out data.
- **Several derivations.** One word can reach $x$ by two edits of the same kind, as "acres" reaches "acress" by two deletions. Add their probabilities, or the channel is too small.

## Implementations

## History

Kernighan, Church and Gale wrote the program correct at Bell Labs and described it at COLING 1990. It took typos flagged by the Unix spell program and ranked the words one edit away by a prior times a channel probability from four confusion matrices of deletions, insertions, substitutions and reversals. The method is the noisy channel model of Shannon applied to spelling, the same model that speech recognition and machine translation used at the time. Brill and Moore generalized the error model to string-to-string edits in 2000. The method is now a standard textbook example, as in Appendix D of Jurafsky and Martin.

## References
