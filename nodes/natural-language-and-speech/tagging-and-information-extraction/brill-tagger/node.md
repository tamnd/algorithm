---
tag: W3YAEV
kind: algorithm
slug: brill-tagger
name: Brill tagger
aliases:
- transformation-based tagging
- transformation-based learning
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Start from the most frequent tag of each word, then apply learned rewrite rules in order, each chosen greedily to fix the most errors."
solves: [part-of-speech-tagging]
model: word-ram
complexity:
  vars: {n: the number of training tokens, k: the number of tags, r: the number of learned rules}
  time: {worst: "O(r n k)"}
  space: {extra: "O(n k)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Eric Brill]
  note: "Brill described transformation-based error-driven learning and its use for part-of-speech tagging in Computational Linguistics in 1995, after earlier versions in 1992 and 1994."
prereqs: [part-of-speech-tagging, greedy-algorithm]
see_also: [hmm-part-of-speech-tagger, decision-tree, out-of-vocabulary-word, text-chunking, maximum-entropy-markov-model, structured-perceptron, universal-pos-tagset, conditional-random-field]
sources:
  - paper: "Eric Brill, Transformation-based error-driven learning and natural language processing: a case study in part-of-speech tagging, Computational Linguistics 21(4), 1995, pages 543 to 565"
    title: Brill 1995
    locator: "Section 2 and Figures 1 and 2 (the learning scheme, and the A A A A A A example of delayed and immediate effect), Section 4.1 (the initial annotator, the lexicon rule, the nonlexicalized templates, Figure 3 with the learning pseudocode, Figure 4 with the first rules), Section 4.2 and Table 1 (lexicalized templates and closed-vocabulary results), Section 4.3 (unknown words and the open-vocabulary results)"
  - book: isbn:9780262133609
    title: "Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999"
    locator: Chapter 10 (part-of-speech tagging)
---

The Brill tagger tags a sentence in two stages. First it gives each word its most frequent tag in the training corpus. Then it runs an ordered list of rewrite rules over the tags, such as "change NN to VB when the previous tag is TO". The rules are learned by transformation-based error-driven learning: at each step the learner picks the rule that removes the most errors on the training corpus, applies it, and repeats. Unlike the [HMM tagger](/hmm-part-of-speech-tagger/), it has no probabilities and no search over tag sequences; the model is a short list of rules that a person can read.

## In plain words

Start with a simple guess: every word gets the tag it had most often in a corpus that people have already tagged. This guess is right most of the time, but it is wrong whenever a word changes its role with the context, as "race" does in "to race" and "the race". The learner now looks at every rule of a few fixed shapes, such as "change tag A to tag B when the previous tag is C". For each rule it counts how many wrong tags the rule would fix and how many right tags it would break. It keeps the rule with the best balance, applies it to the whole corpus, and does the same again on the corrected tags. It stops when no rule helps. To tag new text, it makes the same first guess and applies the rules in the order they were learned.

## The problem

Input: a training corpus of sentences with gold tags from a tag set of $k$ tags, a set of rule templates, and a threshold $\theta \ge 1$. Output: an initial annotator and an ordered list of rules $r_1, \ldots, r_R$. A rule $(e, a, b)$ changes tag $a$ to tag $b$ at each position where the environment $e$ is true. The templates are the eleven nonlexicalized templates of Brill (1995, Section 4.1), where $z$ and $w$ are tags: the previous (next) tag is $z$; the tag two before (after) is $z$; one of the two previous (next) tags is $z$; one of the three previous (next) tags is $z$; the previous tag is $z$ and the next tag is $w$; the previous (next) two tags are $z$ and $w$. The code adds the lexicalized template "the current word is $w$" from Section 4.2. Positions before the sentence read the tag `<s>` and positions after it read `</s>`.

The learner is greedy. Each step chooses the rule $r$ with the largest score $E(c) - E(r(c))$, where $E(c)$ is the number of training errors of the current tags $c$. It stops when the best score is below $\theta$. The rule list is not optimal in any sense: the template set is a heuristic, and so is the greedy choice. Only the single step is exact.

Brill fixes two details that change the result (Section 2). Rules are applied with delayed effect: all positions where the rule fires are found first, and then all of them are changed. And under the lexicon rule of Section 4.1, a word seen in training may only change to a tag it had at least once in training. An unknown word may change to any tag.

## The algorithm

For a rule $r = (e, a, b)$, $\mathrm{good}(r)$ counts the positions with current tag $a$, gold tag $b$, environment $e$ true and $b$ allowed for the word, and $\mathrm{bad}(r)$ counts the positions with current tag $a$, gold tag $a$, environment $e$ true and $b$ allowed. Under delayed effect the score of $r$ is exactly $\mathrm{good}(r) - \mathrm{bad}(r)$. The search is data-driven, as Brill notes: only rules with $\mathrm{good}(r) \ge 1$ can have a positive score, and each such rule is found from a wrong position where it would fix the tag.

```pseudo id=main
BRILL-TRAIN(corpus, θ)
L1  c ← the most frequent training tag of each word (the most frequent tag overall for an unknown word)
L2  rules ← empty list
L3  repeat
L4      for each wrong position p and each environment e true at p: good(e, c_p → gold_p) += 1, if the lexicon allows gold_p for the word
L5      for each right position p, each environment e true at p and each b with good(e, c_p → b) > 0: bad(e, c_p → b) += 1, if the lexicon allows b
L6      r ← a rule with the largest good(r) - bad(r), ties to the smallest rule in a fixed order
L7      if there is no r or good(r) - bad(r) < θ then return rules
L8      c ← apply r to every sentence with delayed effect
L9      append r to rules
```

To tag a sentence, give each word its initial tag and apply $r_1, \ldots, r_R$ in order, each with delayed effect and the lexicon rule. The tie order of the code compares the template index first, then the arguments, then $a$, then $b$. Brill does not state a tie rule.

## Example

Take six tagged sentences: "we/PRP want/VBP to/TO race/VB", "the/DT race/NN ended/VBD", "the/DT race/NN", "a/DT race/NN is/VBZ fun/JJ", "they/PRP like/VBP to/TO race/VB" and "we/PRP went/VBD to/TO the/DT race/NN". The word "race" is NN four times and VB twice, so the initial annotator tags it NN everywhere. Every other word has one tag. The initial tagging has 2 errors, both on "race" after "to".

The learner scores the candidates. Seven rules change NN to VB with $\mathrm{good} = 2$ and $\mathrm{bad} = 0$, for score 2:

| rule | good | bad | score |
|---|---|---|---|
| previous tag is TO | 2 | 0 | 2 |
| tag two before is VBP | 2 | 0 | 2 |
| one of the two previous tags is VBP | 2 | 0 | 2 |
| one of the three previous tags is PRP | 2 | 0 | 2 |
| one of the three previous tags is VBP | 2 | 0 | 2 |
| previous tag is TO and next tag is `</s>` | 2 | 0 | 2 |
| previous two tags are VBP and TO | 2 | 0 | 2 |
| one of the two previous tags is TO | 2 | 1 | 1 |
| the current word is race | 2 | 4 | -2 |

"One of the two previous tags is TO" also fires on "went to the race", where NN is right, so it loses one. The tie rule picks "previous tag is TO", the first template. This is also the first rule Brill learned from the Penn Treebank (Figure 4). After it, the training error is 0 and learning stops. The table shows why the templates are a heuristic: "one of the three previous tags is PRP" fits this corpus as well as the linguistically sensible rule. On "they want to race" the learned tagger gives PRP VBP TO VB, and on "the race" it gives DT NN.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows three things. Under delayed effect, whether a rule fires at a position depends only on the old tags, so the change in the error count is a sum over positions: $+1$ where a wrong $a$ becomes the gold $b$, $-1$ where a right $a$ becomes $b$, and 0 elsewhere. So the score is exactly $\mathrm{good} - \mathrm{bad}$. Lines L4 and L5 compute good and bad exactly for every rule with $\mathrm{good} \ge 1$, and every rule with a positive score is among them, so L6 returns the best rule with the stated tie rule (a theorem about one step). Each learned rule removes at least $\theta \ge 1$ errors, so training ends after at most $E_0$ rules, where $E_0$ is the initial error count. The test file checks one step against a brute force that applies every instantiated rule, for several steps on random corpora.

## Complexity

Let $n$ be the number of training tokens. Each environment set has a constant size (at most 18 environments per position with the twelve templates), so L4 takes $O(n)$ time and L5 takes $O(n k)$ time with hash tables, and L6 and L8 take time linear in the number of candidates and in $n$. With $r$ learned rules, training takes $O(r n k)$ time and $O(n k)$ space for the counts. Since each rule removes at least one error, $r$ is at most the initial number of errors. Tagging a sentence of $m$ words with $r$ rules takes $O(r m)$ time, since each rule is one pass with a constant-time test per word. Brill points to an indexed training method of Ramshaw and Marcus (1994) that is much faster in practice (Section 4.1).

## Properties

- Greedy: each step is an exact maximization of the training error reduction (a theorem), but the list as a whole is not optimal (the greedy choice and the templates are heuristics).
- Deterministic: with a fixed tie rule, the same corpus always gives the same list.
- Readable: the model is a short list of rules such as "change NN to VB if the previous tag is TO".
- Not probabilistic: it gives one tag per word, with no score, so it cannot give a k-best list or a confidence.
- Measured accuracy (Brill 1995, Table 1, with no unknown words in the test set): 97.2% with 447 contextual rules learned from 600,000 words of the Penn Treebank Wall Street Journal corpus, 97.0% without the lexicalized templates (378 rules), and 96.7% with 215 rules from 64,000 words. The first 200 rules alone give 97.0%.
- Measured open-vocabulary accuracy (Section 4.3): 96.6% overall and 82.2% on unknown words, with 243 rules for unknown words and 447 contextual rules. The initial annotator alone gives 92.4%.

## Variants and improvements

- Immediate effect. Applying each change at once, left to right, lets one change trigger the next. On A A A A A A with "change A to B if the previous tag is A", delayed effect gives A B B B B B, while immediate left-to-right effect gives A B A B A B (Brill 1995, Section 2). The score is then no longer a sum over independent positions.
- Lexicalized templates. Brill adds templates that refer to words, such as "the word two after is $w$"; they reduce the error rate by 6.7% in his test (Section 4.2).
- Unknown words. A second learner starts unknown words as proper nouns if capitalized and common nouns otherwise, and learns rules from prefixes, suffixes, characters and neighbouring words, such as "change NN to NNS if the word has suffix -s" (Section 4.3).
- Other initial annotators. The initial state can be the output of an [HMM tagger](/hmm-part-of-speech-tagger/) or any other tagger; the learner then fixes its typical errors.
- Other tasks. The same learner works for any labeling task with a gold standard, for example [text chunking](/text-chunking/) with BIO tags, and Brill also applied it to parsing.
- Relation to [decision trees](/decision-tree/). Brill proves that for a fixed set of questions, every binary decision tree can be converted into a transformation list (Section 3.1). A transformation list can also use the result of earlier rules at nearby positions, which a tree trained on fixed features cannot.

## When to use it

Use a Brill tagger when you want a model that people can read and edit, when you need to fix the errors of another tagger with a few rules, or when you work with a small tagged corpus and want a simple baseline. For the best accuracy, a discriminative sequence model such as the [structured perceptron](/structured-perceptron/), a [conditional random field](/conditional-random-field/) or a neural tagger is a better choice, and training them is much faster than the plain Brill learner on a large corpus.

## Pitfalls

- Delayed and immediate effect give different results. Train and tag with the same choice; the score formula $\mathrm{good} - \mathrm{bad}$ is exact only for delayed effect.
- Rule order matters. A later rule was learned on the output of the earlier rules, so the list must be applied in order and cannot be sorted or pruned in the middle without a loss.
- Spurious rules. When many rules tie, the tie rule decides which one is learned, and a rule may fit the training corpus by accident. The example above has a tie between "previous tag is TO" and "one of the three previous tags is PRP".
- Training cost. A plain implementation scans the whole corpus for every rule, which is slow on a million words. Use an index of where each rule fires.
- Low thresholds overfit. Rules learned at the end of the list fix one or two training errors each and add little on new text; Brill reports that the first 200 of 447 rules give almost all of the gain.
- The lexicon rule needs the full tag list of each training word, not only its most frequent tag.

## Implementations

## History

Before statistical taggers, taggers used hand-written rules. Church (1988) and DeRose (1988) showed that Markov model taggers trained on a tagged corpus did better. Brill proposed transformation-based error-driven learning as a way to learn rules automatically, with earlier versions in 1992 and 1994 (Brill 1995, footnote 9). His 1995 paper in Computational Linguistics describes the general method, proves that transformation lists are at least as expressive as decision trees, and reports results on the Penn Treebank that were better than those of the Markov model tagger it compares with, with a few hundred rules instead of thousands of probabilities. The method was later used for chunking, parsing and other labeling tasks.

## References
