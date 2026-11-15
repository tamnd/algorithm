---
title: CombSUM and CombMNZ compute their formulas, and min-max normalization makes them blind to the scale of each run
proves: [correctness]
status: full
---

Let $S_1, \ldots, S_m$ be the input runs. Each run $S_l$ maps the documents that it retrieved to real scores, higher is better. A document that a run did not retrieve has no entry in it. For a normalization $\nu$ (one of min-max, sum, z-score or none, as defined in line L1), write $\hat S_l = \nu(S_l)$. For a document $d$ in the union of the runs, let $H(d) = \{l : d \in S_l\}$ and $h(d) = |H(d)|$, and define

$$\mathrm{SUM}(d) = \sum_{l \in H(d)} \hat S_l(d), \qquad \mathrm{MNZ}(d) = h(d) \cdot \mathrm{SUM}(d).$$

**Lemma 1 (the code computes the formulas).** After line L2, the list stored for $d$ holds the values $\hat S_l(d)$ for $l \in H(d)$, one for each run that retrieved $d$, and no other values. Line L3 then sets the score of $d$ to $\mathrm{SUM}(d)$ for the rule SUM and to $\mathrm{MNZ}(d)$ for the rule MNZ (line L4), and line L5 returns the union sorted by the fused score, high first, with ties broken by the document id.

*Proof.* Line L1 replaces each run by its normalized run and keeps the same set of documents. The loop of line L2 visits each pair of a run and a document of that run exactly once and appends the score to the list of that document, so after it the list of $d$ is $(\hat S_l(d))_{l \in H(d)}$ in the order of the runs. Its sum is $\mathrm{SUM}(d)$ and its length is $h(d)$, which is what line L3 uses. The other rules of the code (ANZ, MAX, MIN, MED) read the same list. $\square$

The value $h(d)$ is the number of runs that *retrieved* $d$. Fox and Shaw define it as the number of nonzero similarities. The two agree when every retrieved document has a nonzero normalized score, which fails for min-max normalization at the lowest document of each run; the page discusses this case.

**Theorem 1 (min-max is blind to scale and shift).** Let $a > 0$ and $b$ be real, and replace one run $S_j$ by $S'_j(d) = a S_j(d) + b$. With min-max normalization, $\hat S'_j = \hat S_j$, so the SUM and MNZ scores of every document, and the output of line L5, do not change. The same holds for the sum normalization and for the z-score normalization.

*Proof.* Let $\ell = \min S_j$ and $u = \max S_j$. Then $\min S'_j = a \ell + b$ and $\max S'_j = a u + b$, because $a > 0$ keeps the order. If $u > \ell$, then $\hat S'_j(d) = \frac{a S_j(d) + b - a \ell - b}{a u + b - a \ell - b} = \frac{S_j(d) - \ell}{u - \ell} = \hat S_j(d)$. If $u = \ell$, both runs have all scores equal and min-max gives 1 to each. For the sum normalization, each shifted score $S'_j(d) - \min S'_j = a (S_j(d) - \ell)$, so the factor $a$ cancels in the ratio, and the special case of a zero sum is the same for both. For the z-score, the mean becomes $a \mu + b$ and the standard deviation $a \sigma$, so $(S'_j(d) - a\mu - b)/(a\sigma) = (S_j(d) - \mu)/\sigma$. The other runs do not change, and the sets $H(d)$ do not change, so by Lemma 1 nothing else changes. $\square$

Without normalization the claim is false: multiplying one run by 10 lets it decide the order alone.

**Lemma 2 (one run).** With $m = 1$ and min-max normalization, SUM and MNZ both return the documents of the run by decreasing score, with equal scores ordered by id.

*Proof.* Here $h(d) = 1$ for every document, so $\mathrm{MNZ} = \mathrm{SUM} = \hat S_1$, and min-max is a strictly increasing map of the scores when $u > \ell$ and a constant map when $u = \ell$. $\square$

**Theorem 2 (more runs never hurt, for nonnegative scores).** Suppose all normalized scores are nonnegative, as they are for min-max and sum normalization. If one more run is added that retrieves $d$, then $\mathrm{SUM}(d)$ and $\mathrm{MNZ}(d)$ do not decrease. If the new score of $d$ is positive, both strictly increase.

*Proof.* Adding a run with score $x \ge 0$ for $d$ changes $\mathrm{SUM}(d)$ to $\mathrm{SUM}(d) + x \ge \mathrm{SUM}(d)$, and $\mathrm{MNZ}(d) = h \cdot \mathrm{SUM}(d)$ to $(h + 1)(\mathrm{SUM}(d) + x) \ge h \cdot \mathrm{SUM}(d)$, since both factors grow and are nonnegative. If $x > 0$, the sum grows strictly, and so does the product. $\square$

With the z-score, normalized scores can be negative. Then a document with a negative sum loses when another run retrieves it: if $\mathrm{SUM}(d) = -1$ with $h(d) = 1$ and a new run gives $d$ the score $-0.5$, $\mathrm{MNZ}(d)$ falls from $-1$ to $-3$. The multiplier $h(d)$ is meant as a reward, so CombMNZ should be used with a normalization whose values are nonnegative.

The tests in `impl/python/test_combmnz.py` check each normalization against its definition, each rule against a direct computation of its formula on random runs, Theorem 1 with random $a$ and $b$, and the toy runs of the page.
