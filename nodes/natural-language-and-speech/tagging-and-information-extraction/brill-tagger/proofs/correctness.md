---
title: "The learning step of the Brill tagger picks the rule with the largest error reduction, and learning stops"
proves: [correctness]
status: full
---

Setting. The training corpus has sentences $x^{(s)}$ with gold tags $g^{(s)}$ and current tags $c^{(s)}$. A position is a pair $(s, p)$. A rule is $r = (e, a, b)$ with $a \ne b$, where $e$ is a template with its arguments (an environment). Let $\mathrm{holds}(e, s, p)$ say that $e$ is true at $(s, p)$ on the current tags, and let $\mathrm{allows}(w, b)$ be the lexicon rule: $w$ is unknown, or $w$ was seen with tag $b$ in training. The rule fires at $(s, p)$ when $c^{(s)}_p = a$, $\mathrm{holds}(e, s, p)$ and $\mathrm{allows}(x^{(s)}_p, b)$. Application has delayed effect: all firing positions are found on the current tags first, and then each of them gets tag $b$. Let $E(c)$ be the number of positions with $c_p \ne g_p$.

This claim is about the learner as an optimizer of the training error, one step at a time. It does not claim that the list of rules is optimal, or that the rules improve accuracy on new text. Those are heuristic and measured questions.

## Lemma 1: the score of a rule is its exact error reduction

Define $\mathrm{good}(r)$ as the number of firing positions with $g_p = b$, and $\mathrm{bad}(r)$ as the number of firing positions with $g_p = a$. Then $E(c) - E(r(c)) = \mathrm{good}(r) - \mathrm{bad}(r)$.

Proof. Under delayed effect, whether a position fires depends only on the current tags $c$, not on the changes made at other positions, so each position can be looked at alone. A position that does not fire keeps its tag and its error status. A firing position changes from $a$ to $b$. If $g_p = b$, a wrong tag becomes right: the error count drops by 1. If $g_p = a$, a right tag becomes wrong: it rises by 1. If $g_p$ is a third tag, the tag is wrong before and after. Summing over positions gives the claim. $\square$

With immediate effect the lemma fails: a change at position $p$ can make a rule fire or not fire at $p + 1$, so the effect is not a sum over independent positions. Brill's A A A A A A example (and the first test in the test file) shows this.

## Lemma 2: the code computes good and bad exactly for every rule with good at least 1

Line L4 visits each wrong position $(s, p)$ whose word allows its gold tag. For each environment $e$ in instances$(s, p)$, which is the set of all environments true at $(s, p)$ (the test file checks this set against holds for every template and argument), it adds 1 to $\mathrm{good}(e, c_p, g_p)$. A position adds to $\mathrm{good}(e, a, b)$ exactly when $c_p = a \ne g_p = b$, $e$ holds, and the lexicon allows $b$, which is the definition. So the dictionary good holds exactly the rules with $\mathrm{good}(r) \ge 1$, with their values.

Line L5 visits each right position, with $c_p = g_p = a$. For each environment $e$ true there and each $b$ such that $(e, a, b)$ is in good, it adds 1 to $\mathrm{bad}(e, a, b)$ when the lexicon allows $b$. These are exactly the firing positions of $(e, a, b)$ with $g_p = a$. So $\mathrm{bad}(r)$ is exact for every rule in good. $\square$

## Theorem 1: one learning step

Let $S^* = \max_r (E(c) - E(r(c)))$ over all rules built from the templates, the tags and the training words. If $S^* \ge 1$, then L6 returns the rule $r^*$ with score $S^*$ that is smallest in the order of rule_key among all rules with score $S^*$.

Proof. A rule with $\mathrm{good}(r) = 0$ has score $-\mathrm{bad}(r) \le 0 < S^*$, so every rule with score $S^*$ is in the dictionary good. By Lemmas 1 and 2, L6 computes the true score of each rule in good. It scans them in rule_key order and replaces the current best only on a strict improvement, so it returns the first maximizer in that order. That is also the first maximizer among all rules. $\square$

If $S^* \le 0$, L6 returns a rule with score at most 0, or none, and L7 stops, since the threshold is at least 1. The test file checks Theorem 1 against a brute force that applies every one of the instantiated rules to the corpus, on random corpora with 3 tags and 4 words, for several steps in a row.

## Theorem 2: training ends, and the scores add up

Each rule appended at L9 has score $s_j \ge 1$ (the threshold), and L8 applies it, so by Lemma 1 the training error after $j$ rules is $E_j = E_0 - (s_1 + \cdots + s_j)$. Errors are nonnegative integers, so at most $E_0$ rules are learned, and the loop ends after at most $E_0 + 1$ calls of best_rule. The final training error is $E_0$ minus the sum of the scores. $\square$

Tagging new text with the function tag applies the initial annotator and then the same rules, in the same order, with the same application function. So on the training sentences it reproduces the tags that training ended with; the test file checks this.
