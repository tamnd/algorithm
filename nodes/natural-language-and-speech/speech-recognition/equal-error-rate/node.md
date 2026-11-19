---
tag: QFSA7K
kind: definition
slug: equal-error-rate
name: Equal error rate
aliases:
- EER
- ROCCH-EER
area: natural-language-and-speech/speech-recognition
level: intro
summary: The error rate at the threshold where the false acceptance rate equals the false rejection rate, the usual single number for a verification system.
history:
  year: 1997
  people: [Alvin Martin, George Doddington, Niko Brümmer, Edward de Villiers]
  note: The EER is read off the DET curve that Martin et al. described in 1997 for the NIST evaluations. Brümmer and de Villiers defined it on the ROC convex hull in the BOSARIS toolkit (2011, on arXiv in 2013).
prereqs: [confusion-matrix, roc-auc]
see_also: [roc-auc, speaker-verification, gmm-ubm-speaker-verification, plda-scoring, x-vector, convex-hull, neyman-pearson-lemma, word-error-rate]
sources:
  - url: https://arxiv.org/abs/1304.2865
    title: Niko Brümmer and Edward de Villiers, The BOSARIS toolkit, theory, algorithms and code for surviving the new DCF, NIST SRE 2011 workshop, arXiv 1304.2865, 2013
    locator: "Section 2.2 (the Bayes threshold, equations 3 to 6) and Section 2.6.2 (the ROCCH-EER, equation 26)"
  - paper: doi:10.21437/Eurospeech.1997-504
    title: Alvin Martin, George Doddington, Terri Kamm, Mark Ordowski and Mark Przybocki, The DET curve in assessment of detection task performance, Eurospeech 1997
    locator: the DET curve with normal deviate scales and the operating points on it
---

The equal error rate (EER) is the error rate of a detector, such as a [speaker verification](/speaker-verification/) system, at the threshold where it makes the two kinds of error equally often. The two errors are a false acceptance (a false alarm: an impostor is accepted) and a false rejection (a miss: the true speaker is rejected). The EER lies between 0 and 1, and lower is better. It is a single number that does not depend on a choice of threshold, so it is the usual way to compare systems. It says nothing about how well a system sets its own threshold.

## Definition

A trial is a pair of an enrollment and a test. A target trial has the same speaker on both sides; a nontarget trial has two different speakers. The system gives each trial a score, and it accepts the trial when the score is at least a threshold $\theta$. For $N_t$ target scores $s_i$ and $N_n$ nontarget scores $r_j$, the two error rates are

$$P_{\text{miss}}(\theta) = \frac{|\{i : s_i < \theta\}|}{N_t}, \qquad P_{\text{fa}}(\theta) = \frac{|\{j : r_j \ge \theta\}|}{N_n}.$$

As $\theta$ grows, $P_{\text{miss}}$ goes up from 0 to 1 and $P_{\text{fa}}$ goes down from 1 to 0. The EER is the common value where they are equal.

On a finite trial list the rates move in steps of $1/N_t$ and $1/N_n$, so usually no threshold makes them exactly equal. A page or a paper must say how it fills the gap. Two conventions are common.

- **The ROC convex hull (ROCCH-EER).** Plot every operating point $(P_{\text{fa}}, P_{\text{miss}})$, take the lower [convex hull](/convex-hull/) of these points, and return the value where the hull crosses the line $P_{\text{miss}} = P_{\text{fa}}$. This is the convention of the BOSARIS toolkit (Brümmer and de Villiers). A point on the hull between two operating points can be reached by choosing between their two thresholds at random, so the ROCCH-EER is an error rate that a system can achieve.
- **The nearest point.** Take the threshold where $|P_{\text{fa}} - P_{\text{miss}}|$ is smallest and return $(P_{\text{fa}} + P_{\text{miss}})/2$. Ties need a rule; the code of this page takes the smallest such threshold.

The code computes the ROCCH-EER as follows. All rates are exact fractions.

```pseudo id=main
ROCCH-EER(target scores, nontarget scores)
L1  P ← the points (P_fa(θ), P_miss(θ)) for θ at every score and at +∞
L2  add the points (0, 1) and (1, 0)
L3  H ← the lower convex hull of P, from P_fa = 0 to the first vertex with P_miss = 0
L4  find the edge (f₁, m₁)-(f₂, m₂) of H with m₁ ≥ f₁ and m₂ ≤ f₂
L5  s ← (m₁ - f₁) / ((f₂ - f₁) - (m₂ - m₁))
L6  return f₁ + s (f₂ - f₁)
```

After sorting the scores in $O(N \log N)$ time, with $N = N_t + N_n$, the points, the hull and the crossing take $O(N)$ time.

Four facts follow from the definition.

- **Range.** The ROCCH-EER is at most $1/2$. The points $(0, 1)$ and $(1, 0)$ are operating points, so the hull lies on or below the line between them, which meets the diagonal at $(1/2, 1/2)$. A system with reversed scores has a nearest-point EER above $1/2$ but a ROCCH-EER of exactly $1/2$.
- **Only the order counts.** Both conventions depend only on the order of the scores. A strictly increasing map of all scores, such as $s \mapsto 3s + 1$ or $s \mapsto e^s$, does not change the EER. So the EER does not measure calibration.
- **The worst minimum cost (a theorem).** Let $\text{minDCF}(\pi) = \min_\theta [\pi P_{\text{miss}}(\theta) + (1 - \pi) P_{\text{fa}}(\theta)]$, the minimum detection cost with a target prior $\pi$ and unit costs. Then $\text{ROCCH-EER} = \max_{\pi \in [0, 1]} \text{minDCF}(\pi)$. Proof: a linear function has the same minimum over a finite point set as over its convex hull. The point $E = (e, e)$ on the hull gives the cost $e$ for every $\pi$, so $\text{minDCF}(\pi) \le e$. The edge of L4 lies on a supporting line of the convex hull; take $\pi^* = (f_2 - f_1) / ((f_2 - f_1) + (m_1 - m_2))$, which makes the cost constant along that line. Every point of the hull then has a cost of at least $e$, so $\text{minDCF}(\pi^*) = e$.
- **Gaussian scores.** If the target and nontarget scores are normal with equal variance and means $d'$ standard deviations apart, the threshold halfway between the means gives $\text{EER} = \Phi(-d'/2)$, where $\Phi$ is the standard normal distribution function. For $d' = 2$ this is $\Phi(-1) = 0.158655$.

## Examples and non-examples

A hand-made trial list. The target scores are $0.9, 0.8, 0.6, 0.45, 0.3$ and the nontarget scores are $0.7, 0.5, 0.4, 0.35, 0.1$. The operating points are:

| $\theta$ | 0.1 | 0.3 | 0.35 | 0.4 | 0.45 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | $+\infty$ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $P_{\text{fa}}$ | 1 | 4/5 | 4/5 | 3/5 | 2/5 | 2/5 | 1/5 | 1/5 | 0 | 0 | 0 |
| $P_{\text{miss}}$ | 0 | 0 | 1/5 | 1/5 | 1/5 | 2/5 | 2/5 | 3/5 | 3/5 | 4/5 | 1 |

At $\theta = 0.5$ the two rates are both $2/5$, so the nearest-point EER is $0.4$. The lower hull has the vertices $(0, 3/5)$, $(2/5, 1/5)$ and $(4/5, 0)$. Its first edge crosses the diagonal at $s = (3/5)/(2/5 + 2/5) = 3/4$, so the ROCCH-EER is $3/4 \cdot 2/5 = 0.3$. A system reaches this rate by using $\theta = 0.8$ on a random quarter of the trials and $\theta = 0.45$ on the rest: $P_{\text{fa}} = 3/4 \cdot 2/5 = 3/10$ and $P_{\text{miss}} = 1/4 \cdot 3/5 + 3/4 \cdot 1/5 = 3/10$. As the theorem says, $\text{minDCF}(1/2) = (1/5 + 2/5)/2 = 0.3$ at $\theta = 0.45$.

Other cases:

- **A tie.** For target scores $0.9, 0.8, 0.7, 0.4$ and nontarget scores $0.75, 0.5, 0.3, 0.2, 0.1, 0.05$, the thresholds $0.5$ and $0.7$ both give $|P_{\text{fa}} - P_{\text{miss}}| = 1/12$, with means $7/24$ and $5/24$. The ROCCH-EER is $0.2$. On small lists the convention changes the result a lot.
- **Perfect separation.** If every target score is above every nontarget score, a threshold between them gives no errors, and the EER is 0.
- **Non-example: the error rate at a fixed threshold.** A system that runs at $\theta = 0$ has an actual miss rate and false alarm rate, and they are usually not equal. The EER describes a threshold chosen afterward on the test data itself, so no deployed system reaches it unless its threshold happens to be right.
- **Non-example: the half total error rate.** $(P_{\text{fa}} + P_{\text{miss}})/2$ at a threshold fixed in advance is another number. It equals the EER only at the equal error threshold.

## Related definitions

- The **DET curve** (Martin et al. 1997) plots $P_{\text{miss}}$ against $P_{\text{fa}}$ on normal deviate scales, where Gaussian scores give straight lines. The EER is the point where the curve meets the diagonal. The [ROC curve](/roc-auc/) is the same set of operating points plotted as $1 - P_{\text{miss}}$ against $P_{\text{fa}}$.
- The **detection cost function** $C_{\text{det}} = C_{\text{miss}} \pi P_{\text{miss}} + C_{\text{fa}} (1 - \pi) P_{\text{fa}}$ is the measure of the NIST speaker recognition evaluations. For scores that are calibrated log likelihood ratios, the Bayes threshold is $\eta = \log(C_{\text{fa}} / C_{\text{miss}}) - \operatorname{logit} \pi$ (BOSARIS, Section 2.2). For example, $\pi = 0.01$, $C_{\text{miss}} = 10$ and $C_{\text{fa}} = 1$ give $\eta = \log 9.9 = 2.292535$. Unlike the EER, the actual cost at this threshold measures calibration.
- The EER is a point on the curve whose area is the [ROC AUC](/roc-auc/); two systems with the same EER can have different AUCs.
- In speech recognition, the [word error rate](/word-error-rate/) plays the role that the EER plays in verification, but it counts edits and is not a detection measure.

## References
