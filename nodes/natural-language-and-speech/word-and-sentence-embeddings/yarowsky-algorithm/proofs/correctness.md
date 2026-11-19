---
title: The Yarowsky loop keeps its seeds, stops, and stops early only at a fixed point
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. There are $n$ examples with feature sets $F_1, \ldots, F_n$, a list of senses $\sigma_1, \ldots, \sigma_m$ in a fixed order, a smoothing constant $\alpha > 0$, a threshold $\theta$ and a bound $T \ge 1$ on the rounds. Let $z_i$ be the seed label of example $i$: the one sense of the seed collocations in $F_i$, or $\bot$ if there is none or there are two different ones. A labeling is a vector $y = (y_1, \ldots, y_n)$ with each $y_i$ a sense or $\bot$.

The algorithm makes no claim that the labels are the right senses. That part is a heuristic, measured on test data. What can be proved is what the loop computes.

**Lemma 1 (the decision list).** For a labeling $y$, let $c_y(f, \sigma)$ be the number of examples $i$ with $f \in F_i$ and $y_i = \sigma$. Line L3 gives one rule $(f, s_f, \lambda_f)$ for each feature $f$ with $\sum_\sigma c_y(f, \sigma) > 0$, where $s_f$ is the first sense in the list with the largest count and

$$ \lambda_f = \ln \frac{c_y(f, s_f) + \alpha}{\sum_{\sigma \ne s_f} c_y(f, \sigma) + \alpha}, $$

and it sorts the rules by decreasing $\lambda_f$, ties by the smaller feature string. Then the classification of line L4 for a set $F$ returns $s_{f^*}$ if $\lambda_{f^*} \ge \theta$ and $\bot$ otherwise, where $f^*$ is the feature of $F$ with a rule that has the largest $\lambda$, the smallest string on ties; it returns $\bot$ if no feature of $F$ has a rule.

*Proof.* Since $\alpha > 0$, both parts of the ratio are positive and $\lambda_f$ is a real number. The classification scans the sorted list and stops at the first rule whose feature is in $F$. In the sorted order, rule $f$ comes before rule $g$ exactly when $(-\lambda_f, f) < (-\lambda_g, g)$, so the first rule with a feature in $F$ is the rule of the feature $f^*$ that is smallest in this order, which is the description above. The test of the threshold is made on that rule only. If no rule has a feature in $F$, the scan ends without a match and returns $\bot$. $\square$

Write $U(y)$ for the labeling that one round makes from $y$: lines L3 and L4, and line L5 when one sense per discourse is on. In line L4, example $i$ gets $z_i$ if $z_i \ne \bot$ and the classification of Lemma 1 otherwise. In line L5, each example $i$ with $z_i = \bot$ and a known discourse $d$ gets the sense that has strictly the most votes among the line L4 labels of discourse $d$, if there is such a sense; otherwise it keeps its line L4 label.

**Lemma 2 (the seeds stay).** For every labeling $y$ and every $i$ with $z_i \ne \bot$, $U(y)_i = z_i$.

*Proof.* Line L4 gives $z_i$ to example $i$. Line L5 changes only examples with $z_i = \bot$. $\square$

**Claim.** The loop stops after at most $T$ rounds and returns a labeling $y$ with $y_i = z_i$ for every seeded example. If it returns at line L6 in round $t$, then $U(y) = y$, the returned list $D$ is the decision list of $y$, and classifying every unseeded example with $D$ by Lemma 1, followed by line L5, gives $y$ again.

*Proof.* Let $y^{(0)}$ be the labeling of line L1 and $y^{(t)} = U(y^{(t-1)})$. We show by induction on $t$ that, at the start of round $t + 1$, the variable $y$ holds $y^{(t)}$ and $y^{(t)}_i = z_i$ for every seeded example.

*Base.* Line L1 sets $y = y^{(0)}$, and $y^{(0)}_i = z_i$ for every $i$ by definition.

*Step.* In round $t + 1$, lines L3 to L5 compute $y' = U(y^{(t)}) = y^{(t+1)}$ from the current $y$. Lemma 2 gives $y'_i = z_i$ on the seeded examples. If line L7 runs, it sets $y = y^{(t+1)}$.

*Termination.* The rounds are the values $t = 1, \ldots, T$ of line L2. Each round is finite: line L3 counts over $n$ finite sets and sorts a finite list, line L4 scans that list once per example, and line L5 counts votes once. So the loop stops at line L6 or after round $T$, and line L8 returns. In both cases the returned labeling is some $y^{(t)}$, which keeps the seeds by the induction.

*The early stop.* Line L6 returns in round $t$ only when $y' = y$, that is $U(y^{(t-1)}) = y^{(t-1)}$, and it returns $y = y^{(t-1)}$ with the list $D$ that line L3 built from it in the same round. By the definition of $U$ and Lemma 1, applying $D$ to the unseeded examples and then line L5 gives $y'$, which equals $y$. $\square$

**What is not proved.** The claim does not say that the loop reaches a fixed point within $T$ rounds, and Yarowsky 1995 gives no proof that it converges. The update $U$ is not monotone: an example labeled in one round can lose its label in the next. Take $\alpha = 0.1$, $\theta = 2$, one sense per discourse off, and five examples: example 1 has $\{a, f\}$ and the seed $a \to \sigma_1$; example 2 has $\{f\}$; example 3 has $\{f, g\}$; examples 4 and 5 have $\{g, b\}$ and the seed $b \to \sigma_2$. In round 1, $\lambda_f = \ln 11 \approx 2.40$ and $\lambda_g = \ln 21 \approx 3.04$, so example 2 gets $\sigma_1$ by $f$ and example 3 gets $\sigma_2$ by $g$. In round 2, $f$ occurs in two examples labeled $\sigma_1$ and one labeled $\sigma_2$, so $\lambda_f = \ln(2.1/1.1) \approx 0.65 < \theta$, and example 2 goes back to $\bot$. So the labeled set need not grow, and the bound $T$ of line L2 is what makes the loop stop in all cases. Abney 2004 studies variants of the algorithm that do have a decreasing objective. $\blacksquare$
