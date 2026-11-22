---
tag: RSR0DF
kind: algorithm
slug: pcfg-password-model
name: Probabilistic context-free grammar password model
aliases:
- PCFG password cracking
- Weir password grammar
area: security-and-privacy/network-and-web-security
level: advanced
summary: "Estimates password strength with a grammar of letter, digit and symbol runs learned from a password list. A password scores -log2 of its probability, and its guess number is its rank."
model: word-ram
complexity:
  vars: {n: the length of the password, N: the number of characters in the training list}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: false}
history:
  year: 2009
  people: [Matt Weir, Sudhir Aggarwal, Breno de Medeiros, Bill Glodek, Patrick Gage Kelley, Saranga Komanduri, Michelle Mazurek]
  note: "Weir, Aggarwal, de Medeiros and Glodek introduced the grammar of base structures in 2009. Kelley et al. used it with letter runs learned from the training list to measure password policies in 2012."
prereqs: [probabilistic-context-free-grammar, context-free-grammar, maximum-likelihood-estimation]
see_also: [markov-password-model, honeywords, password-hashing, n-gram-language-model, priority-queue, min-entropy, shannon-entropy]
sources:
  - paper: "Matt Weir, Sudhir Aggarwal, Breno de Medeiros and Bill Glodek, Password cracking using probabilistic context-free grammars, IEEE Symposium on Security and Privacy 2009, pages 391 to 405"
    locator: "the base structures of letter, digit and symbol runs, the learned probabilities of structures and of digit and symbol runs, and the order of guesses by probability"
  - paper: "Patrick Gage Kelley, Saranga Komanduri, Michelle L. Mazurek, Richard Shay, Timothy Vidas, Lujo Bauer, Nicolas Christin, Lorrie Faith Cranor and Julio Lopez, Guess again (and again and again), measuring password strength by simulating password-cracking algorithms, IEEE Symposium on Security and Privacy 2012, pages 523 to 537"
    locator: "the guess number calculator, the PCFG with letter runs learned from training data, and the comparison of password policies"
  - paper: "Jerry Ma, Weining Yang, Min Luo and Ninghui Li, A study of probabilistic password models, IEEE Symposium on Security and Privacy 2014, pages 689 to 704, doi:10.1109/SP.2014.50"
    locator: the comparison of PCFG and Markov models with probability threshold graphs
  - paper: "Matteo Dell'Amico and Maurizio Filippone, Monte Carlo strength evaluation, fast and reliable password checking, ACM CCS 2015, pages 158 to 169, doi:10.1145/2810103.2813631"
    locator: "the estimate of guess numbers from a sample, applied to PCFG and other models"
---

The PCFG password model estimates how strong a password is. It treats a password as a sequence of runs of letters, digits and other symbols, so that `love12` is the letter run `love` followed by the digit run `12`, with the base structure L4 D2. A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) learned from a password list gives each base structure a probability and, for each tag and length, each run a probability. The probability of a password is the product of the probability of its structure and of its runs, its strength is $-\log_2 P(w)$ bits, and its guess number is $1$ plus the number of strings with a higher probability. Scoring takes $\Theta(n)$ time for a password of $n$ characters. The numbers are estimates under the model and its training list, not a guarantee against all attackers. Weir et al. (2009) introduced the grammar to order guesses for password recovery; this page uses it only to score passwords and to count more likely strings.

## In plain words

Many people build a password from parts: a word, then some digits, then maybe a symbol. The model learns two things from a list of passwords. It learns how common each pattern of parts is, such as "four letters then two digits". It also learns how common each part is, such as the digits `12` among all two-digit parts.

To judge a password, the model cuts it into parts, looks up the chance of its pattern and the chance of each part, and multiplies them. A password that follows a common pattern with common parts gets a high chance and is weak. A password with a rare pattern or rare parts gets a small chance and is strong. A meter can also count how many passwords the model thinks are more likely, which estimates how many guesses a careful guesser would need.

## The problem

Each character has a tag: L for a letter, D for a digit and S for any other character. A run of a string is a maximal block of characters with the same tag, and the base structure $\mathrm{st}(w)$ is the list of (tag, length) pairs of the runs of $w$. The input is a training list of $T$ non-empty passwords and a password $w$. Training counts $N(s)$, the number of passwords with structure $s$, and $N_{t,\ell}(x)$, the number of times $x$ is a run with tag $t$ and length $\ell$ in the list. The model is

$$ P(s) = \frac{N(s)}{T}, \qquad P(x \mid t, \ell) = \frac{N_{t,\ell}(x)}{\sum_y N_{t,\ell}(y)}, \qquad P(w) = P(\mathrm{st}(w)) \prod_{i=1}^{r} P(x_i \mid t_i, \ell_i), $$

where $x_1, \ldots, x_r$ are the runs of $w$. The outputs are the strength $-\log_2 P(w)$ and the guess number $1 + |\{v : P(v) > P(w)\}|$.

## The algorithm

```pseudo id=main
PCFG-SCORE(w, P)
L1  x_1, ..., x_r ← the maximal runs of w
L2  s ← ((tag(x_1), |x_1|), ..., (tag(x_r), |x_r|))
L3  p ← P(s)                          ▷ 0 if s was not seen
L4  for i ← 1 to r do
L5      p ← p · P(x_i | tag(x_i), |x_i|)   ▷ 0 if x_i was not seen
L6  return p
```

Training is one pass over the list. It splits each password as line L1 does, adds 1 to the count of its structure and to the count of each run in its slot, and divides each count by the total of its group. The strength is $-\log_2 p$, and the code computes it from the numerator and denominator of the exact fraction $p$.

**Guess numbers.** A string has a positive probability only if its structure and all its runs were seen, so there are finitely many such strings. For each structure the code sorts the runs of each slot by decreasing probability and does a depth-first search over the choices of runs. It stops a branch as soon as the partial product, times the best choice for each remaining slot, is at most $P(w)$. The search counts the strings above the threshold and never lists them. For large models, the Monte Carlo estimate of Dell'Amico and Filippone (2015), described on the [Markov password model](/markov-password-model/) page, works for this model as well.

## Example

The training list is made up: `love12`, `love12`, `star12`, `love!`, `star99`, `moon1`, `love99` and `sun!!`. There are four structures: L4 D2 with 5 passwords, and L4 S1, L4 D1 and L3 S2 with 1 each. Among the 7 letter runs of length 4, `love` occurs 4 times, `star` 2 times and `moon` once. Among the 5 digit runs of length 2, `12` occurs 3 times and `99` 2 times. Scoring $w =$ `love12` goes as follows.

| line | step | factor | $p$ |
| --- | --- | --- | --- |
| L1, L2 | runs `love`, `12`; structure L4 D2 | | |
| L3 | $P(\text{L4 D2})$ | 5/8 | 5/8 |
| L5 | $P(\texttt{love} \mid \text{L}, 4)$ | 4/7 | 5/14 |
| L5 | $P(\texttt{12} \mid \text{D}, 2)$ | 3/5 | 3/14 |

So $P(\texttt{love12}) = 3/14$, the strength is about 2.22 bits, and no string is more likely, so its guess number is 1. The model gives a positive probability to exactly 13 strings, and their probabilities add up to 1. Some of them score as follows.

| password | $P(w)$ | strength in bits | guess number |
| --- | --- | --- | --- |
| `love12` | 3/14 | 2.22 | 1 |
| `sun!!` | 1/8 | 3.00 | 3 |
| `star99` | 1/14 | 3.81 | 5 |
| `love1` | 1/14 | 3.81 | 5 |
| `moon99` | 1/28 | 4.81 | 9 |
| `moon1` | 1/56 | 5.81 | 12 |
| `lovestar` | 0 | infinite | none |

The string `love1` was never in the list, but its structure and runs were, so it gets the same probability as `star99`, which was. The string `lovestar` has the structure L8, which was never seen, so its probability is 0.

## Correctness

Because each run is a maximal block of one tag, and two neighbouring slots of a learned structure have different tags, each string has at most one derivation in the grammar. So the product of lines L3 to L5 is the probability of the string, not of one of several parses. The same fact gives a one to one map from the choices of a structure and its runs to the strings with a positive probability, so the probabilities of all strings add up to 1. The relative frequencies are the maximum likelihood rule probabilities for the training list. The guess number search is exact, because the runs of each slot are sorted, so once a choice cannot beat the threshold, no later choice can. The full proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Scoring.** Line L1 reads $w$ once, line L3 hashes a structure of at most $n$ slots, and the lookups of line L5 hash runs whose lengths add up to $n$. So the time is $\Theta(n)$ on the word-RAM, with $O(n)$ extra space for the runs.
- **Training.** The same work for each password, so $O(N)$ time for $N$ characters. The tables hold at most one entry for each distinct structure and each distinct run.
- **Exact guess numbers.** Each node of the search is a prefix of a counted string, so the time is $O(r^2 G)$ plus the sorting, for structures of at most $r$ slots and a count $G$. It grows with the guess number and is only for small models, as in the test.

## Properties

- **Unambiguous.** Each string has at most one parse, so there is no sum over parses and no choice of the best parse.
- **A proper distribution with finite support.** The probabilities add up to 1, but only over the strings built from seen structures and seen runs. Every other string has probability 0.
- **Exact arithmetic.** The code multiplies fractions, so ties are exact, as for `star99` and `love1` above.
- **An estimate, not a measure.** The scores depend on the training list. A password unlike the list can still be weak against another list.

## Variants and improvements

- **Dictionaries for letters.** In Weir et al. (2009) the probabilities of structures and of digit and symbol runs were learned, and the letter runs came from dictionaries. Kelley et al. (2012) learned the letter runs from the training data, as on this page. A dictionary covers more words, but its probabilities do not come from the list.
- **Case and other tags.** Later work adds a separate pattern for upper and lower case, and tags for keyboard patterns, dates or multi-word runs. Each new tag must keep the segmentation unique, or the grammar becomes ambiguous.
- **Smoothing.** Giving unseen runs and structures a small probability removes the infinite scores. Ma et al. (2014) compared smoothed PCFG and [Markov](/markov-password-model/) models and found that well-smoothed Markov models did at least as well in their study.
- **Order of guesses.** Weir et al. listed strings in decreasing probability with a [priority queue](/priority-queue/) over partly filled structures. This page does not list strings; a strength meter needs only the count.

## When to use it

Use a PCFG model to estimate strength in a meter, or to compare password policies on a test list, when passwords are made of words, digits and symbols. It is simple to train, it scores in one pass, and its parts are easy to explain to a user, for example "a common word followed by a common number". It gives probability 0 to strings outside its support, so a meter needs smoothing or a fallback. A [Markov model](/markov-password-model/) gives a probability to every string. Neither model protects stored passwords; for that use slow [password hashing](/password-hashing/), and to detect a stolen password file use [honeywords](/honeywords/).

## Pitfalls

- **Runs that are not maximal.** If line L1 splits a block of one tag into smaller pieces, a string has several parses, and the product of line L5 is the probability of one parse, not of the string. The probabilities then add up to more or less than 1. Line L1 must cut only where the tag changes.
- **No structure factor.** If line L3 sets $p \leftarrow 1$ instead of $P(s)$, every structure counts as if it were certain, and a rare pattern such as L3 S2 scores as weak as a common one. Line L3 must start from $P(s)$.
- **Runs not split by length.** If line L5 uses $P(x \mid t)$ over runs of all lengths instead of $P(x \mid t, \ell)$, the mass of a slot spreads over runs that cannot fill it, and the probabilities add up to less than 1. Line L5 must condition on the tag and the length.
- **Zero for new words.** Without smoothing, line L5 gives 0 for a run not seen in training, so a weak password with one new word scores as infinitely strong. A meter must smooth or fall back to another model.
- **Floating point underflow.** A product of many small factors can round to 0. Add logarithms or keep exact fractions.

## Implementations

## History

Weir, Aggarwal, de Medeiros and Glodek (IEEE Symposium on Security and Privacy 2009) learned a probabilistic grammar of base structures from a password list and used it to order guesses by probability. Kelley et al. (2012) built a guess number calculator on this grammar, with letter runs learned from training data, to compare password composition policies. Ma, Yang, Luo and Li (2014) compared PCFG and Markov models with probability threshold graphs. Dell'Amico and Filippone (2015) gave a Monte Carlo estimate of guess numbers that applies to this model and makes strength estimates for large models practical.

## References
