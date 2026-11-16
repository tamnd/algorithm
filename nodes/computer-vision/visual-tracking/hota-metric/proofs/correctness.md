---
title: HOTA_alpha is the geometric mean of DetA and AssA, the matching gives the most true positives, and DetA does not grow with the threshold
proves: [correctness]
status: full
---

Notation as on the page. Fix a threshold $\alpha$. $G$ and $P$ are the numbers of true and predicted detections over all frames, TP is the set of matches made by line L2, and $|\mathrm{FN}| = G - |\mathrm{TP}|$ and $|\mathrm{FP}| = P - |\mathrm{TP}|$.

## Claim 1: the sizes of FNA and FPA

For a true positive $c$ with identities $(g, p)$, $|\mathrm{FNA}(c)| = |g| - |\mathrm{TPA}(c)|$ and $|\mathrm{FPA}(c)| = |p| - |\mathrm{TPA}(c)|$. So $\mathcal{A}(c)$ depends only on the pair $(g, p)$, and $\sum_{c \in \mathrm{TP}} \mathcal{A}(c) = \sum_{(g, p)} k_{gp}^2 / (|g| + |p| - k_{gp})$, where $k_{gp}$ is the number of true positives with the identities $(g, p)$.

*Proof.* Each true detection of $g$ is either a true positive, with some predicted identity, or a miss. Those that are true positives with $p$ form $\mathrm{TPA}(c)$, and all the others form $\mathrm{FNA}(c)$ by its definition. So the two sets split the $|g|$ detections of $g$. The same argument on the predicted side gives the second formula. Then $\mathcal{A}(c) = k_{gp} / (k_{gp} + (|g| - k_{gp}) + (|p| - k_{gp}))$, and the $k_{gp}$ true positives with the pair $(g, p)$ each add this value. $\square$

The code uses this formula, and the tests compute $\mathcal{A}(c)$ again from the set definitions.

## Claim 2: the geometric mean

If $|\mathrm{TP}| > 0$, then $\mathrm{HOTA}_\alpha = \sqrt{\mathrm{DetA}_\alpha \cdot \mathrm{AssA}_\alpha}$.

*Proof.* $\mathrm{DetA}_\alpha \cdot \mathrm{AssA}_\alpha = \dfrac{|\mathrm{TP}|}{|\mathrm{TP}| + |\mathrm{FN}| + |\mathrm{FP}|} \cdot \dfrac{1}{|\mathrm{TP}|} \sum_{c \in \mathrm{TP}} \mathcal{A}(c) = \dfrac{\sum_{c} \mathcal{A}(c)}{|\mathrm{TP}| + |\mathrm{FN}| + |\mathrm{FP}|}$, the number under the square root in the definition of $\mathrm{HOTA}_\alpha$. $\square$

If there is no true positive, the sum is empty and $\mathrm{HOTA}_\alpha = 0$; the code then sets $\mathrm{AssA}_\alpha = 0$, so the formula holds in this case as well.

## Claim 3: the most true positives

Let $k$ be the largest number of pairs in a matching of one frame, and let $1/\varepsilon > k (1 + \varepsilon)$. Then the matching of line L2 has the largest number of pairs with $S \ge \alpha$ in its frame.

*Proof.* Line L2 gives each pair with $S \ge \alpha$ the weight $\mathrm{MS} = 1/\varepsilon + \mathcal{A}_{\max} + \varepsilon S$ and the other pairs the weight 0, finds a maximum weight assignment with the Hungarian algorithm (its optimality is proved on the [SORT proof](/sort-tracker/)), and removes the pairs of weight 0. As for the [CLEAR MOT matching](/clear-mot-metrics/), this gives a matching $M$ of allowed pairs with the largest total MS. Since $0 \le \mathcal{A}_{\max} \le 1$ and $0 \le S \le 1$, a matching with $m$ pairs has a total in $[m/\varepsilon, m/\varepsilon + m(1 + \varepsilon)]$. If some matching $M'$ had more pairs than $M$, say $m' \ge m + 1$, then
$$\mathrm{MS}(M) \le \frac{m}{\varepsilon} + k(1 + \varepsilon) < \frac{m}{\varepsilon} + \frac{1}{\varepsilon} \le \frac{m'}{\varepsilon} \le \mathrm{MS}(M'),$$
against the choice of $M$. $\square$

With equal numbers of pairs, the same argument shows that the term $\mathcal{A}_{\max}$ decides first when $\varepsilon k$ is below the smallest positive gap between two sums of $\mathcal{A}_{\max}$, and then the term $\varepsilon S$ decides. This order is the one that the paper asks for. The code uses $\varepsilon = 10^{-6}$ with exact fractions, and the tests compare the total MS and the number of pairs with all matchings.

## Claim 4: DetA does not grow with the threshold

If $\alpha < \alpha'$ and the condition of Claim 3 holds, then $\mathrm{DetA}_{\alpha'} \le \mathrm{DetA}_\alpha$.

*Proof.* Every pair with $S \ge \alpha'$ also has $S \ge \alpha$, so every matching allowed at $\alpha'$ is allowed at $\alpha$. By Claim 3, the number of true positives in each frame is the largest matching size, so it is at least as large at $\alpha$ as at $\alpha'$. Summing over the frames gives $T = |\mathrm{TP}_\alpha| \ge T' = |\mathrm{TP}_{\alpha'}|$. Now $\mathrm{DetA} = T / (T + (G - T) + (P - T)) = T / (G + P - T)$, which increases with $T$ for fixed $G + P$, since the numerator grows and the denominator falls. $\square$

AssA has no such order: a larger threshold can remove the true positives of a badly associated pair and raise the mean.

## Claim 5: the range

$0 \le \mathrm{HOTA}_\alpha \le 1$, and $\mathrm{HOTA}_\alpha = 1$ exactly when there are no misses and no false positives at $\alpha$ and every true positive $c$ has $\mathrm{FNA}(c) = \mathrm{FPA}(c) = \emptyset$, that is, each true identity is matched to one predicted identity in all its frames and that predicted identity is matched to it in all of its own frames.

*Proof.* Each $\mathcal{A}(c)$ is in $[0, 1]$, so the sum under the root is between 0 and $|\mathrm{TP}| / (|\mathrm{TP}| + |\mathrm{FN}| + |\mathrm{FP}|) \le 1$. It equals 1 exactly when both inequalities are equalities: $|\mathrm{FN}| = |\mathrm{FP}| = 0$ and $\mathcal{A}(c) = 1$ for every $c$, which means $\mathrm{FNA}(c) = \mathrm{FPA}(c) = \emptyset$. HOTA, a mean of numbers in $[0, 1]$, is also in $[0, 1]$. $\square$
