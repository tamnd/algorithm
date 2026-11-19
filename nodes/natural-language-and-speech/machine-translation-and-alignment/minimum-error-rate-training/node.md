---
tag: P668TA
kind: algorithm
slug: minimum-error-rate-training
name: Minimum error rate training
aliases:
- MERT
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Tune the weights of a log-linear model to maximize BLEU on n-best lists by exact line search along one direction at a time.
solves: [machine-translation]
model: word-ram
complexity:
  vars: {n: the total number of candidates in all n-best lists, p: the number of features}
  time: {worst: "O(n (p + log n))"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Franz Josef Och]
  note: Och (2003) proposed to tune the weights of a log-linear translation model directly for the evaluation metric, and gave the exact line search on n-best lists by the upper envelope. It was the standard tuning method of phrase-based and syntax-based systems for about ten years.
prereqs: [log-linear-translation-model]
see_also: [bleu, phrase-based-stack-decoding, convex-hull-trick, coordinate-descent, minimum-risk-training, structured-perceptron, translation-edit-rate, word-lattice]
sources:
  - paper: "Franz Josef Och, Minimum error rate training in statistical machine translation, ACL 2003, pages 160 to 167, ACL Anthology P03-1021"
    title: Och 2003
    locator: the training criterion on n-best lists, the observation that the error is piecewise constant along a line, and the exact line search
  - paper: "Kishore Papineni, Salim Roukos, Todd Ward and Wei-Jing Zhu, BLEU: a method for automatic evaluation of machine translation, ACL 2002, pages 311 to 318, ACL Anthology P02-1040"
    title: Papineni et al. 2002
    locator: the definition of BLEU from clipped n-gram precisions and the brevity penalty, summed over the corpus
  - paper: "Philipp Koehn, Amittai Axelrod, Alexandra Birch Mayne, Chris Callison-Burch, Miles Osborne and David Talbot, Edinburgh system description for the 2005 IWSLT speech translation evaluation, IWSLT 2005, ACL Anthology 2005.iwslt-1.8"
    title: Koehn et al. 2005
    locator: "Section 2.7 (minimum error rate training: a line search for one weight at a time on n-best lists)"
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 9 (discriminative training: parameter tuning and minimum error rate training)"
---

Minimum error rate training (MERT) sets the weights of a [log-linear translation model](/log-linear-translation-model/) so that the translations the model prefers score well under an evaluation metric such as [BLEU](/bleu/). It works on fixed n-best lists of candidate translations and changes one direction of the weight vector at a time. Along one direction, the metric is a step function of the step size, and MERT finds its exact maximum by computing where the model's choice changes. The line search is exact, but the whole method is a heuristic: the objective is not smooth and not concave, so the search can stop at a local optimum.

## In plain words

A translation system has a few knobs: how much to trust the language model, how much to punish reordering, and so on. For each tuning sentence, the decoder gives a list of candidate translations, and the knobs decide which candidate wins. We want the knob setting whose winners get the best score against the reference translations.

Turn one knob slowly. The winner of a sentence changes only at a few points, where another candidate overtakes it. Between those points nothing changes, so the score of the whole set is flat in pieces. MERT finds all the points where some winner changes, checks the score once in each piece, and moves the knob to the middle of the best piece. Then it does the same for the next knob, and repeats until no knob helps. New candidate lists are then made with the new knobs.

## The problem

Translation runs from source sentences $f^{(1)}, \ldots, f^{(S)}$ to target sentences, each with reference translations. The model scores a candidate $e$ by $w \cdot h(e, f)$ with weights $w \in \mathbb{R}^p$ and feature vector $h$. For sentence $i$ the decoder has produced an n-best list $C_i$; each candidate $c$ has features $h_{i,c}$ and sufficient statistics $\phi_{i,c}$ for the metric. For BLEU these are the clipped n-gram matches and the n-gram counts for $n = 1, \ldots, 4$, the candidate length and the reference length. The model picks $\hat c_i(w) = \arg\max_c w \cdot h_{i,c}$, and the goal is

$$\max_w \; M(w) = \mu\Bigl(\sum_i \phi_{i, \hat c_i(w)}\Bigr),$$

where $\mu$ turns summed statistics into the corpus score. For an error count, $\mu$ is minus the sum. The function $M$ is piecewise constant in $w$, so its gradient is zero almost everywhere and gradient methods do not apply.

**The line search.** Given $w$ and a direction $d$, find $\gamma$ that maximizes $F(\gamma) = M(w + \gamma d)$. Each candidate's model score along the line is $a_{i,c} + \gamma \, b_{i,c}$, a line with $a_{i,c} = w \cdot h_{i,c}$ and $b_{i,c} = d \cdot h_{i,c}$. The winner of sentence $i$ at $\gamma$ is the highest of its lines, so the winners change only where the *upper envelope* of the lines changes.

## The algorithm

UPPER-ENVELOPE sorts the lines by slope and keeps a stack of the lines on the envelope, each with the point where it starts to be highest, as in the [convex hull trick](/convex-hull-trick/).

```pseudo id=main
UPPER-ENVELOPE(lines)                          ▷ each line: slope b, intercept a, candidate c
U1  sort lines by slope; for equal slopes keep only the highest
U2  H ← empty stack of (line, start)
U3  for each line ℓ = (b, a, c) in order do
U4      while H is not empty do
U5          x ← the γ where ℓ passes the top line of H
U6          if x ≤ start of the top line then pop H else break
U7      push (ℓ, x) on H, with start −∞ if H was empty
U8  return the starts and the candidates of H

LINE-SEARCH(w, d, n-best lists, μ)
L1  events ← empty list
L2  for each sentence i do
L3      lines ← (d · h_{i,c}, w · h_{i,c}, c) for each candidate c
L4      E ← UPPER-ENVELOPE(lines)
L5      add φ of the first candidate of E to the running total Φ
L6      for each later envelope point g with candidates c_prev, c: add event (g, φ_c − φ_{c_prev})
L7  sort events by g
L8  best ← μ(Φ); γ* ← (first event) − 1, or 0 if there are no events
L9  for each group of events at the same g, in order: add them to Φ; if μ(Φ) > best then best ← μ(Φ); γ* ← middle of g and the next event, or g + 1 after the last
L10 return γ*, best
```

MERT itself is [coordinate ascent](/coordinate-descent/): for each unit direction (and optionally some random directions), run LINE-SEARCH and move to $w + \gamma^* d$ if it improves $M$. Repeat until no direction improves. The outer loop then decodes the tuning set again with the new weights, merges the new candidates into the n-best lists, and tunes again, until the lists stop growing.

## Example

Two sentences, two features, and three candidates each. The metric counts errors (fewer is better). The candidates have features and errors:

| sentence | candidate | $h$ | errors | score on the line $w = (1, 0)$, $d = (0, 1)$ |
|---|---|---|---|---|
| 1 | 1 | $(-1, 0)$ | 2 | $-1$ |
| 1 | 2 | $(-2, 1)$ | 0 | $-2 + \gamma$ |
| 1 | 3 | $(-4, 2)$ | 1 | $-4 + 2\gamma$ |
| 2 | 1 | $(-1, 0)$ | 1 | $-1$ |
| 2 | 2 | $(-2.5, 2)$ | 0 | $-2.5 + 2\gamma$ |
| 2 | 3 | $(-5, 4)$ | 2 | $-5 + 4\gamma$ |

For sentence 1, line 2 passes line 1 at $\gamma = 1$ and line 3 passes line 2 at $\gamma = 2$, so the envelope is candidate 1, then 2 from 1, then 3 from 2. For sentence 2, line 2 passes line 1 at $0.75$, and line 3 passes line 2 at $1.25$. The sweep over the merged points $0.75, 1, 1.25, 2$ gives the total errors

| interval of $\gamma$ | below 0.75 | 0.75 to 1 | 1 to 1.25 | 1.25 to 2 | above 2 |
|---|---|---|---|---|---|
| winners | 1, 1 | 1, 2 | 2, 2 | 2, 3 | 3, 3 |
| errors | 3 | 2 | 0 | 2 | 3 |

The best interval is $(1, 1.25)$ with 0 errors, and the line search returns its middle, $\gamma = 1.125$, so $w = (1, 1.125)$. At the starting point $\gamma = 0$ there were 3 errors. Only 4 points were needed; a grid search would need a step finer than $0.25$ to find this interval at all.

**BLEU as $\mu$.** For the candidate "the cat sat on the mat" and the reference "the cat sat on the red mat", the statistics are 6, 4, 3, 2 matches out of 6, 5, 4, 3 n-grams, a candidate length 6 and a reference length 7. BLEU is $e^{1 - 7/6}$ times the geometric mean of $6/6, 4/5, 3/4, 2/3$, which is $0.673$. Over a corpus, the statistics of the chosen candidates are added first, and BLEU is computed once from the sums. This is why the sweep keeps a running total of statistics and not a sum of sentence scores.

## Correctness

The line search returns the exact maximum of $F$ over all $\gamma$ that are not breakpoints (a theorem, proved in the proofs file). The two facts behind it are that the upper envelope gives, for each sentence, the winner on every interval between its breakpoints, and that adding the changes of statistics at each breakpoint in sorted order gives the summed statistics on every interval. The value at a breakpoint itself depends on how ties are broken; MERT returns a point in the middle of an interval so that a small change of the weights does not change the result.

Coordinate ascent never lowers $M$ and stops after finitely many improvements, because $M$ takes finitely many values. It is a heuristic: it stops at a point that no single line search improves, which need not be a global maximum. Implementations restart from random points to reduce this problem. The test file checks the line search against a grid of 2001 steps on random n-best lists, with BLEU and with smoothed BLEU.

## Complexity

Count in the [word RAM](/word-ram/) model, with metric statistics of constant size. For sentence $i$ with $n_i$ candidates, line L3 costs $O(n_i p)$ and the envelope $O(n_i \log n_i)$ for the sort; the stack loop is linear, because each line is pushed and popped at most once. There are at most $n = \sum_i n_i$ events, sorted in $O(n \log n)$, and the sweep evaluates $\mu$ once per group. So one line search costs $O(n (p + \log n))$, and one round of coordinate ascent costs $p$ line searches. The space is $O(n)$ for the events. The expensive part in practice is not MERT but the decoding that produces the n-best lists, repeated in the outer loop.

## Properties

- **Exact line search.** Along a line the result is the true maximum on the n-best lists, not an approximation from a grid.
- **Any corpus metric.** It needs only that the metric is a function of summed statistics. BLEU, [TER](/translation-edit-rate/) and error counts all work.
- **Scale invariant.** Multiplying $w$ by a positive number does not change the winners, so the weights are found only up to scale. Implementations normalize them.
- **Unstable with many features.** With more than about 20 to 30 features the result varies much between runs and overfits the tuning set; this is a measurement reported in later work, not a theorem.
- **Only the n-best lists.** It optimizes the metric on the lists, not on the full search space. The outer loop of decoding again narrows this gap.

## Variants and improvements

- **Random directions and restarts.** Search along random directions as well as the unit vectors, and start from several random points. This is the usual defence against local optima.
- **Lattice MERT.** Macherey and others (2008) computed the envelope over all paths of a [word lattice](/word-lattice/) instead of an n-best list, which gives many more candidates at a modest cost.
- **Regularized MERT.** Smoothing the objective, or choosing a point far from the interval ends, makes the result more stable.
- **Other tuning methods.** Pairwise ranking optimization, MIRA and [minimum risk training](/minimum-risk-training/) scale to many more features. The [structured perceptron](/structured-perceptron/) updates the weights from the best candidate and an oracle candidate.

## When to use it

Use MERT to tune a log-linear model with a small number of dense features, up to about 20, for a corpus metric such as BLEU, on a tuning set of a few hundred to a few thousand sentences. Run it several times with different seeds and keep the weights that do best on a held-out set. For models with many sparse features, use a ranking or margin method instead.

## Pitfalls

- **Sentence-level metric sums.** BLEU of a corpus is not the sum or the mean of sentence BLEU. Add the statistics, then compute the metric.
- **Evaluating at a breakpoint.** At the exact $\gamma$ where two candidates tie, the winner depends on the tie rule. Return a point inside the interval.
- **Equal slopes.** Two candidates with the same $d \cdot h$ give parallel lines, and the formula for the crossing divides by zero. Keep only the higher of them, as in line U1.
- **Too few candidates.** With short n-best lists, the tuned weights can choose candidates the decoder would never find with new weights. Merge the lists over iterations and decode again until they stop changing.
- **Overfitting.** On a small tuning set the metric gain is partly noise. Compare on held-out data.

## Implementations

## History

Before MERT, the weights of log-linear translation models were set by hand or trained for likelihood, as in the maximum entropy training of Och and Ney (2002). Och (2003) observed that the error count of an n-best list is piecewise constant along any line in weight space, gave the exact line search, and showed in his measurements that training for the evaluation metric gave better scores on that metric than likelihood training. MERT became the standard tuning method of the Moses and Joshua toolkits. From about 2008, methods such as MIRA and pairwise ranking took over for models with many features.

## References
