---
tag: TJVQ07
kind: theorem
slug: karlin-altschul-statistics
name: Karlin-Altschul statistics
aliases:
- Karlin-Altschul theorem
- extreme value distribution of local scores
- Karlin-Altschul formula
area: biology/sequence-alignment
level: advanced
summary: For random sequences and ungapped scores with negative mean and some positive score, the count of HSPs scoring at least S is about Poisson with mean Kmn e^(-λS).
prereqs: [high-scoring-segment-pair, substitution-matrix, poisson-distribution]
see_also: [e-value, bit-score, blast, martingale, optional-stopping-theorem, maximum-subarray-problem, database-similarity-search, markov-chain]
sources:
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, PNAS 87(6), 1990
    locator: pages 2264 to 2268 (the conditions on the scores, the equation for λ, the constant K, the Poisson number of high-scoring segments and the target frequencies)
  - paper: "Samuel Karlin and Amir Dembo, Limit distributions of maximal segmental score among Markov-dependent partial sums, Advances in Applied Probability 24(1), 1992, pages 113 to 140"
    title: Karlin and Dembo 1992
    locator: the limit law of the maximal segment score for one sequence and for the comparison of two sequences
  - paper: "Amir Dembo, Samuel Karlin and Ofer Zeitouni, Limit distribution of maximal non-aligned two-sequence segmental score, Annals of Probability 22(4), 1994, pages 2022 to 2039"
    title: Dembo, Karlin and Zeitouni 1994
    locator: the proof of the extreme value limit for the comparison of two sequences of growing lengths
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997
    locator: pages 3389 to 3402, Statistical Preliminaries (gapped scores follow the same form with λ and K from simulation)
  - paper: "Richard Arratia and Michael S. Waterman, A phase transition for the score in matching random sequences allowing deletions, Annals of Applied Probability 4(1), 1994, pages 200 to 225"
    title: Arratia and Waterman 1994
    locator: the linear and the logarithmic growth of the best local score, and the line between them
  - url: https://raw.githubusercontent.com/ncbi/ncbi-cxx-toolkit-public/master/src/algo/blast/core/blast_stat.c
    title: NCBI C++ Toolkit, BLAST core, blast_stat.c
    locator: the computation of λ, H and K for integer scores (the series for K), and the table of BLOSUM62 parameters
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, the section on the significance of scores (the extreme value distribution of local scores)
---

The Karlin-Altschul statistics describe the scores of the best ungapped local alignments between two random sequences. If each letter pair has a negative expected score and some pair has a positive score, then the number of [high-scoring segment pairs](/high-scoring-segment-pair/) with score at least $S$ is approximately a Poisson variable with mean $E = K m n\, e^{-\lambda S}$, and the best score has an extreme value (Gumbel) distribution. Here $m$ and $n$ are the lengths, $\lambda$ is the unique positive root of $\sum_{a,b} p_a p'_b e^{\lambda s(a,b)} = 1$, and $K$ is a second constant of the scoring scheme. This result gives [E-values](/e-value/) and [bit scores](/bit-score/) to [BLAST](/blast/) and other search tools.

## Statement

**The model.** Two sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$ (DNA or the 20 amino acids). All letters are independent; the letters of $x$ have the frequencies $p_a$ and the letters of $y$ the frequencies $p'_b$. A scoring matrix $s(a, b)$ has integer values; let $\delta$ be the greatest common divisor of its values that occur with positive probability. Let $X = s(A, B)$ for independent $A \sim p$ and $B \sim p'$: the score of one random aligned pair. Only ungapped alignments are scored.

**Conditions.**

1. $\mathbb{E}[X] = \sum_{a,b} p_a p'_b\, s(a, b) < 0$.
2. $\Pr(X > 0) > 0$: some pair with $p_a p'_b > 0$ has a positive score.

**Claims.**

- **(A) The parameter λ.** The equation
$$\sum_{a,b} p_a p'_b\, e^{\lambda s(a,b)} = 1$$
has exactly one root $\lambda > 0$.
- **(B) Target frequencies.** The numbers $q_{ab} = p_a p'_b\, e^{\lambda s(a,b)}$ are positive where $p_a p'_b > 0$ and sum to 1. Their relative entropy to the background is $H = \sum_{a,b} q_{ab}\, \lambda s(a, b) > 0$ (in nats). In the high-scoring segments of long random sequences, the aligned pairs occur with the frequencies $q_{ab}$, and a segment with score $S$ has about $\lambda S / H$ pairs.
- **(C) One walk.** On one diagonal, let $S_k = X_1 + \cdots + X_k$ be the running sum of independent copies of $X$. For each integer $s \ge 1$,
$$e^{-\lambda (s + c - 1)} \le \Pr(S_k \ge s \text{ for some } k \ge 1) \le e^{-\lambda s},$$
where $c$ is the largest score.
- **(D) The Poisson limit.** As $m, n \to \infty$ at comparable rates, the number of distinct HSPs with score at least $S$ tends to a Poisson variable with mean
$$E = K m n\, e^{-\lambda S},$$
and the maximal segment pair score $M$ satisfies $\Pr(M \ge S) \approx 1 - \exp(-K m n\, e^{-\lambda S})$, for $S$ on the lattice $\delta \mathbb{Z}$. Equivalently, $\lambda M - \ln(Kmn)$ has approximately the Gumbel law $\Pr(\cdot \le x) = \exp(-e^{-x})$, up to the lattice effect.
- **(E) The constant K.** For integer scores with $\delta = 1$,
$$K = \frac{\exp\left(-2 \sum_{k \ge 1} \frac{1}{k}\left(\mathbb{E}\left[e^{\lambda S_k}; S_k < 0\right] + \Pr(S_k \ge 0)\right)\right)}{\mathbb{E}[X e^{\lambda X}]\,(1 - e^{-\lambda})},$$
with $\mathbb{E}[X e^{\lambda X}] = H/\lambda$. Scaling all scores by a factor $t > 0$ divides $\lambda$ by $t$ and leaves $K$ the same.

Claims (A), (B) and (C) are proved below in full. Claim (D) is the theorem of Karlin and Altschul (1990), with the proof for two sequences by Dembo, Karlin and Zeitouni (1994); we give a sketch. Claim (E) is the formula of the 1990 paper in the form used by the NCBI BLAST code.

**Gapped scores.** No such theorem is known for alignments with gaps. Simulations show that the best gapped scores follow the same form when the gap costs are high enough, and BLAST uses $\lambda$ and $K$ estimated by simulation for each matrix and pair of gap costs.

## In plain words

Compare two random sequences that have nothing to do with each other. Along each diagonal the running score goes down on average, because the scoring table gives a negative score to a typical pair. But now and then a lucky run of good pairs pushes it up for a while. Each such rise is a chance match.

The theorem says how high these chance rises go. A rise of a given height is rare, and each extra point of height makes it rarer by the same factor. The number of tries grows with the product of the two lengths. Put together, the expected number of chance matches above a score is the product of the lengths times a factor that falls exponentially with the score. Two numbers, fixed by the scoring table and the letter frequencies, set the speed of the fall and the overall level.

## Proof

**(A) λ exists and is unique.** Let $f(\lambda) = \mathbb{E}[e^{\lambda X}] - 1 = \sum_{a,b} p_a p'_b e^{\lambda s(a,b)} - 1$. It is a finite sum of exponentials, so it is smooth, and $f''(\lambda) = \mathbb{E}[X^2 e^{\lambda X}] > 0$ because $X$ is not always 0 (condition 2). So $f$ is strictly convex. Also $f(0) = 0$ and $f'(0) = \mathbb{E}[X] < 0$ by condition 1, so $f < 0$ just to the right of 0. By condition 2 some term has $s(a,b) > 0$ and $p_a p'_b > 0$, so $f(\lambda) \ge p_a p'_b e^{\lambda s(a,b)} - 1 \to \infty$. By continuity $f$ has a root $\lambda > 0$. A strictly convex function has at most two roots, and 0 is one of them, so the positive root is unique. $\square$

**(B) Target frequencies.** Each $q_{ab}$ is positive where $p_a p'_b > 0$, and $\sum q_{ab} = f(\lambda) + 1 = 1$ by (A). So $q$ is a distribution, and $H = \sum_{a,b} q_{ab} \ln\frac{q_{ab}}{p_a p'_b} = \sum q_{ab}\, \lambda s(a,b)$ is its relative entropy to $p \otimes p'$, which is positive because $q \ne p \otimes p'$ (the scores are not all 0). Also $\sum q_{ab}\, s(a,b) = f'(\lambda) > 0$, because $f$ is convex and rises through its root $\lambda$. So the pairs drawn from $q$ have a positive mean score $H/\lambda$, and a segment of score $S$ made of such pairs has about $S/(H/\lambda) = \lambda S/H$ pairs. The statement that high-scoring segments have the composition $q$ is a part of the 1990 theorem that we do not prove here. $\square$

**(C) Bounds for one walk.** The process $Z_k = e^{\lambda S_k}$ is a martingale: $\mathbb{E}[Z_{k+1} \mid Z_k] = Z_k\, \mathbb{E}[e^{\lambda X}] = Z_k$. Let $\tau$ be the first $k \ge 1$ with $S_k \ge s$, and $\tau = \infty$ if there is none. By the [optional stopping theorem](/optional-stopping-theorem/) for the bounded time $\tau \wedge N$, $\mathbb{E}[Z_{\tau \wedge N}] = Z_0 = 1$.

Before $\tau$ the walk is below $s$, so $Z_k < e^{\lambda s}$. At $\tau$ the walk was at most $s - 1$ one step before, and one step adds at most $c$, so $s \le S_\tau \le s - 1 + c$. Thus $Z_{\tau \wedge N} \le e^{\lambda (s + c - 1)}$ for all $N$. By the strong law of large numbers $S_k \to -\infty$, because $\mathbb{E}[X] < 0$, so on $\{\tau = \infty\}$ we have $Z_N \to 0$. Bounded convergence gives

$$1 = \lim_{N \to \infty} \mathbb{E}[Z_{\tau \wedge N}] = \mathbb{E}\left[e^{\lambda S_\tau};\ \tau < \infty\right].$$

Since $e^{\lambda s} \le e^{\lambda S_\tau} \le e^{\lambda(s + c - 1)}$ on $\{\tau < \infty\}$, we get $e^{\lambda s} \Pr(\tau < \infty) \le 1 \le e^{\lambda(s+c-1)} \Pr(\tau < \infty)$, which is the claim. $\square$

So the chance that one excursion of the walk climbs $s$ above its start is $e^{-\lambda s}$ up to a constant factor. This is the source of the factor $e^{-\lambda S}$ in $E$.

**(D) Sketch of the Poisson limit.** On each diagonal, run the recursion $h_k = \max(0, h_{k-1} + X_k)$ of [Kadane's algorithm](/kadane-algorithm/), which queueing theory calls the Lindley recursion. Its excursions away from 0 are independent, and the peak of each excursion is the score of a locally maximal segment pair. The number of excursions on a diagonal of length $L$ is about $L / \mathbb{E}[T]$, where $T$ is the length of one excursion, which has finite mean because the drift is negative. By (C) and a renewal argument (the Cramér-Lundberg estimate), the peak $Y$ of one excursion satisfies $\Pr(Y \ge s) \sim C e^{-\lambda s}$ for a constant $C$, along the lattice. Over all diagonals there are about $mn / \mathbb{E}[T]$ excursions, and the ones with a high peak are rare and almost independent, so their number is approximately Poisson with mean $(C/\mathbb{E}[T])\, mn\, e^{-\lambda S} = K m n\, e^{-\lambda S}$. The hard part, which Dembo, Karlin and Zeitouni (1994) carry out, is to control the dependence between diagonals, which share letters, and to show that the high peaks are not clustered. The best score $M$ is at least $S$ exactly when this count is at least 1, so $\Pr(M \ge S) \approx 1 - e^{-E}$.

**(E) The constant.** $K$ collects $C$ and $\mathbb{E}[T]$. For integer scores the ladder heights of the walk give the series in (E) (Karlin and Altschul 1990). We do not derive it here; for $X = \pm 1$ it gives the closed form below, which can be checked against (C) and the gambler's ruin.

## Consequences

**Closed forms for $\pm 1$ scores.** Let $X = +1$ with probability $p$ and $X = -1$ with probability $q = 1 - p > p$. The equation of (A) is $p e^{\lambda} + q e^{-\lambda} = 1$, so $e^{\lambda} = q/p$ and $\lambda = \ln(q/p)$. The series of (E) gives $K = (q - p)^2/q$. For DNA with uniform bases and $+1/-1$ scores, $p = 1/4$, so $\lambda = \ln 3 = 1.0986$ and $K = 1/3$. For $\pm 1$ scores (C) is exact at the upper end: the gambler's ruin gives $\Pr(\text{reach } s) = (p/q)^s = e^{-\lambda s}$.

**DNA with $+1/-2$.** With uniform bases, $p = 1/4$ for $+1$ and $3/4$ for $-2$. Put $x = e^{\lambda}$: $\frac14 x + \frac34 x^{-2} = 1$, so $x^3 - 4x^2 + 3 = 0$, which is $(x - 1)(x^2 - 3x - 3) = 0$. The positive root other than 1 is $x = (3 + \sqrt{21})/2$, so $\lambda = \ln\frac{3 + \sqrt{21}}{2} = 1.3327$. The series gives $K = 0.621$, and $H = 1.124$ nats $= 1.62$ bits per pair.

| scheme (uniform DNA) | $\mathbb{E}[X]$ | $\lambda$ | $K$ | $H$ (nats) |
|---|---|---|---|---|
| $+1/-1$ | $-0.5$ | 1.0986 | 0.3333 | 0.549 |
| $+1/-2$ | $-1.25$ | 1.3327 | 0.6210 | 1.124 |
| $+5/-4$ | $-1.75$ | 0.1915 | 0.1755 | 0.357 |

For [BLOSUM62](/blosum-matrix/) with the background frequencies that BLAST uses, the NCBI code lists $\lambda = 0.3176$, $K = 0.134$ and $H = 0.4012$ for ungapped scores, and $\lambda = 0.267$, $K = 0.041$ for gapped scores with the gap cost $11 + L$.

**E-values and bit scores.** The mean $E = Kmn e^{-\lambda S}$ is the [E-value](/e-value/), and $P = 1 - e^{-E}$ is the P-value of the best score. Rescaling to $S' = (\lambda S - \ln K)/\ln 2$ gives the [bit score](/bit-score/) with $E = mn\, 2^{-S'}$.

**Scale.** $\lambda$ is the factor that turns raw scores into nats. If all scores are multiplied by $t$, the same alignments have the same significance, $\lambda$ becomes $\lambda / t$ and $K$ does not change. A matrix built as $s(a,b) = \frac{1}{\lambda_0} \ln\frac{q_{ab}}{p_a p_b}$ has $\lambda = \lambda_0$ and target frequencies $q_{ab}$: every scoring matrix of this kind is a log-odds matrix for some target frequencies.

**Edge effects.** The limit assumes that an HSP can start anywhere. In finite sequences an HSP of score $S$ needs about $\ell = \lambda S/H$ letters, so BLAST replaces $m$ and $n$ by effective lengths about $\ell$ shorter, with $\ell = \ln(Kmn)/H$, the length at the score where $E = 1$.

**The growth of the best score.** Since $E = 1$ when $S = \ln(Kmn)/\lambda$, the best chance score grows like $\ln(mn)/\lambda$, logarithmically in the lengths.

## Tightness

- **Both conditions are needed.** If $\Pr(X > 0) = 0$, no segment has a positive score and $M = 0$. If $\mathbb{E}[X] > 0$, the score of the whole diagonal grows linearly, so $M$ grows like $\mathbb{E}[X] \min(m, n)$ and the logarithmic law fails. At $\mathbb{E}[X] = 0$ the equation of (A) has no positive root.
- **The lattice effect.** For integer scores the law holds along the lattice $\delta \mathbb{Z}$. Between lattice points the distribution of $M$ has jumps, so the Gumbel form is an approximation of a step function.
- **The bounds of (C) are tight.** For $\pm 1$ scores the upper bound is attained, and the gap between the two bounds is the factor $e^{\lambda(c-1)}$ for overshoot, which cannot be removed in general.
- **Gaps.** With gaps allowed, Arratia and Waterman (1994) showed that the best score of random sequences has a phase transition: for low gap costs it grows linearly in the length, and for high gap costs logarithmically. The Karlin-Altschul form can hold only in the logarithmic phase, and there it is used as an empirical fit.
- **Finite lengths.** The theorem is a limit. For short sequences the edge correction matters; in the simulation on the [E-value](/e-value/) page, lengths of 400 give counts within about 15% of the formula.
- **Dependent letters.** Real sequences have composition bias and repeats. Karlin and Dembo (1992) extend the limit to Markov-dependent letters, with $\lambda$ from a matrix eigenvalue equation in place of (A).

## History

The longest run of heads in $n$ coin tosses grows like $\log_{1/p} n$ (Erdős and Rényi 1970), and Arratia and Waterman studied the longest exact match of two random sequences in the 1980s. Karlin and Altschul (1990) gave the law for general scoring schemes with a negative mean: the Poisson count with mean $Kmn e^{-\lambda S}$, the formula for $K$, and the target frequencies that make every scoring matrix a log-odds matrix. It used the extreme value theory of random walks with negative drift, the same mathematics as the waiting times of a queue. Karlin and Dembo (1992) and Dembo, Karlin and Zeitouni (1994) proved the limits in full for one sequence with Markov letters and for two sequences. BLAST (1990) used the theorem to set its score cutoff. Gapped BLAST (1997) extended the formula to gapped scores by fitting $\lambda$ and $K$ in simulations.

## References
