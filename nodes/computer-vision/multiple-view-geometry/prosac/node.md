---
tag: B0M487
kind: algorithm
slug: prosac
name: PROSAC
aliases:
- progressive sample consensus
area: computer-vision/multiple-view-geometry
level: advanced
summary: "RANSAC that draws samples first from the matches of best quality and grows the pool over time, which finds a good model much sooner when the ranking is good."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data items, k: "the number of samples drawn, at most a set cap"}
  time: {worst: Θ(k n + n²), average: Θ(k n + n²), best: Θ(k n + n²)}
  space: {extra: Θ(n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Ondrej Chum, Jiri Matas]
  note: "Chum and Matas presented PROSAC at CVPR 2005, for matching with many outliers where the matcher gives a similarity score for each tentative match."
prereqs: [ransac, ransac-iteration-bound]
see_also: [lo-ransac, msac, mlesac, preemptive-ransac, magsac, feature-matching, lowe-ratio-test, robust-model-fitting]
sources:
  - paper: doi:10.1109/CVPR.2005.221
    title: "Ondrej Chum and Jiri Matas, Matching with PROSAC: progressive sample consensus, IEEE Conference on Computer Vision and Pattern Recognition 2005, volume 1, 220-226"
    locator: "Section 2 (the growth function, T_n and T'_n, and the samples of eq. (6)), Section 2.2 (the stopping rule: non-randomness and maximality) and Algorithm 1"
  - paper: doi:10.1007/3-540-47969-4_6
    title: "Ben J. Tordoff and David W. Murray, Guided sampling and consensus for motion estimation, European Conference on Computer Vision 2002, Lecture Notes in Computer Science 2350, 82-96"
    locator: "Guided sampling with match scores as prior inlier probabilities, the earlier method that PROSAC compares with"
  - paper: doi:10.1109/TPAMI.2012.257
    title: "Rahul Raguram, Ondrej Chum, Marc Pollefeys, Jiri Matas and Jan-Michael Frahm, USAC: a universal framework for random sample consensus, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(8), 2013, 2022-2038"
    locator: "PROSAC as the sampling stage of the framework"
---

PROSAC (progressive sample consensus) is a variant of [RANSAC](/ransac/) that changes only which samples are drawn. In image matching, each tentative match comes with a quality score, for example the distance ratio of the [Lowe ratio test](/lowe-ratio-test/), and matches with good scores are more often correct. RANSAC ignores the scores and samples uniformly. PROSAC sorts the matches by score and draws its first samples from a small set of the best matches, then lets the set grow, so that after many samples it draws from all matches as RANSAC does. When the ranking is good, a sample of inliers comes up after very few draws, often orders of magnitude fewer than RANSAC needs. When the ranking is random, PROSAC behaves like RANSAC in experiments. Chum and Matas introduced it in 2005, with a stopping rule that also picks the size of the set of matches.

## In plain words

You must find a line among many dots, and someone has ranked the dots: the dots at the top of the list are probably good, the dots at the bottom are probably junk. The ranking is not perfect, but it helps.

RANSAC picks dots at random from the whole list. PROSAC starts at the top. Its first guesses use only the first few dots. Then, step by step, it lets one more dot from further down into the pool, and each new guess uses the newest dot together with dots from the pool. Over time the pool becomes the whole list.

If the top of the list is mostly good dots, an early guess is right, and PROSAC can stop. The stopping test also says how far down the list the good dots go.

## The problem

The input is as for [RANSAC](/ransac/), with the data $D = (u_1, \ldots, u_N)$ sorted by a quality score, best first, and a minimal sample size $m$. Write $U_n = \{u_1, \ldots, u_n\}$ for the $n$ best items. PROSAC has four more parameters: $T_N$, the number of samples after which it draws from all of $D$; $\beta$, the probability that an item is an inlier of a wrong model by chance; and $\Psi$ and $\eta_0$, the error probabilities of the two parts of the stopping rule. The goal is a model with a large consensus set, found with few samples.

## The algorithm

The growth function decides when the pool grows. Let $T_n = T_N \binom{n}{m} / \binom{N}{m}$, the expected number of samples, among $T_N$ uniform samples from $D$, that lie in $U_n$. Then $T_{n+1} = \frac{n+1}{n+1-m} T_n$. Let $T'_m = 1$ and $T'_{n+1} = T'_n + \lceil T_{n+1} - T_n \rceil$, and $g(t) = \min\{n : T'_n \ge t\}$. By eq. (6) of the paper, the $t$-th sample is $u_{g(t)}$ together with $m - 1$ items drawn at random from $U_{g(t)-1}$. Each new item thus enters with the share of samples that RANSAC would give to samples whose worst item is that one.

```pseudo id=main
PROSAC(u_1, …, u_N, m, ε, k_max)             ▷ sorted by quality, best first
L1  t ← 0, n ← m, n* ← N, k* ← k_max, θ* ← none, I* ← ∅
L2  while t < k* do
L3      t ← t + 1
L4      while t > T'_n and n < n* do          ▷ n becomes g(t)
L5          n ← n + 1
L6      if t ≤ T'_n then
L7          S ← {u_n} ∪ (m − 1 items of U_{n−1}, drawn at random)
L8      else S ← m items of U_n, drawn at random   ▷ the pool stopped at n*
L9      θ ← FIT-MINIMAL(S); if θ is none then continue
L10     I ← {x ∈ D : r(θ, x) ≤ ε}
L11     if |I| > |I*| then
L12         θ* ← θ, I* ← I
L13         (n*, k*) ← the prefix that passes the non-randomness test with the least k_n, with n* ≥ n
L14 return θ*, I*
```

The stopping rule of line L13 looks at the inliers of the best model in each prefix. Let $I_n = |I^* \cap U_n|$. **Non-randomness**: a wrong model also gets inliers by chance, and the number of such inliers in $U_n$, besides the $m$ items of its sample, is binomial with parameters $n - m$ and $\beta$. The test asks $I_n \ge I_n^{\min}$, the least $j$ such that the probability of $j$ or more chance inliers is below $\Psi$. **Maximality**: with $P_{I_n} = \prod_{j=0}^{m-1} \frac{I_n - j}{n - j}$, the probability that a sample from $U_n$ is all-inlier, the number of samples after which a better model in $U_n$ would have been missed with probability below $\eta_0$ is $k_n = \lceil \log \eta_0 / \log(1 - P_{I_n}) \rceil$. Among the prefixes that pass the first test, $n^*$ minimizes $k_n$, and PROSAC stops after $k^* = k_{n^*}$ samples. The paper uses $\Psi = \eta_0 = 0.05$ and $T_N = 200000$.

Read literally, the two branches of step 2 of Algorithm 1 in the paper are swapped with respect to eq. (6). The code and the pseudocode follow eq. (6): while the pool grows, each sample contains the newest item $u_n$. The paper prints the probability of $i$ chance inliers in $U_n$ as $\beta^{i-m}(1-\beta)^{n-i+m}\binom{n-m}{i-m}$; the exponent $n - i + m$ appears to be a typo, and the code uses the binomial form $(1-\beta)^{n-i}$, whose terms sum to 1.

## Example

Take $N = 10$ points sorted by quality: $(0,0), (0,3), (2,2), (5,5), (4,1), (1,1), (3,3), (2,5), (4,4), (5,2)$. Six of them lie on $y = x$; in the sorted order the inliers are at positions 1, 3, 4, 6, 7 and 9. Use $m = 2$, $\varepsilon = 0.1$, $\beta = \Psi = \eta_0 = 0.05$ and $T_N = \binom{10}{2} = 45$. Then $T_n = \binom{n}{2}$ and $T'_n = \binom{n}{2}$: the pool $U_n$ is complete after $\binom{n}{2}$ samples. With the seed 0 the code draws:

| $t$ | $n$ | sample | line | $\lvert I\rvert$ | $n^*$ | $k^*$ |
|---|---|---|---|---|---|---|
| 1 | 2 | $u_1, u_2$ | $x = 0$ | 2 | 10 | $k_{\max}$ |
| 2 | 3 | $u_3, u_2$ | $x + 2y = 6$ | 3 | 10 | $k_{\max}$ |
| 3 | 3 | $u_3, u_1$ | $y = x$ | 6 | 7 | 5 |
| 4 | 4 | $u_4, u_2$ | through $(5,5), (0,3)$ | 2 | 7 | 5 |
| 5 | 4 | $u_4, u_3$ | $y = x$ | 6 | 7 | 5 |

After round 2, no prefix passes the non-randomness test, so $k^*$ stays at the cap. After round 3, the inlier counts of the prefixes $n = 2, \ldots, 10$ are $1, 2, 3, 3, 4, 5, 5, 6, 6$, and the thresholds $I_n^{\min}$ are $3, 4, 4, 4, 4, 4, 4, 4, 5$. The prefixes $n \ge 6$ pass. For $n = 7$, $P_{I_7} = \frac{5 \cdot 4}{7 \cdot 6} = 0.476$ and $k_7 = \lceil 4.63 \rceil = 5$; for $n = 6$, $P_{I_6} = 0.4$ and $k_6 = 6$; the other prefixes need 6 or more. So $n^* = 7$ and $k^* = 5$, and PROSAC stops after 5 samples. The correct line came from the third sample. RANSAC with $w = 0.6$ and $p = 0.99$ would ask for 11 samples.

## Correctness

PROSAC keeps the invariant of RANSAC: $I^*$ is the largest consensus set among the sampled models. Each sample consists of $m$ distinct items of the current pool, and the loop ends after at most $k_{\max}$ rounds. The growth function has an exact meaning: by round $T'_n$, PROSAC has drawn $T'_n - T'_{n-1} = \lceil T_n - T_{n-1} \rceil$ samples whose worst item is $u_n$, the expected number of such samples in $T_N$ uniform samples rounded up. When the pool stops at $n^* = N$ after the schedule, PROSAC samples exactly as RANSAC does. The stopping rule is a test with error probabilities $\Psi$ and $\eta_0$ under its assumptions, not a bound. Chum and Matas state that they could not prove that PROSAC is never worse than RANSAC in the worst case; with a random ordering, the two performed the same in their experiments (a benchmark result). The proof of the invariants is below.

## Complexity

One round costs the minimal solver plus $N$ residuals, so $\Theta(N)$ in the [real RAM](/real-ram/), as in RANSAC. The schedule $T'_n$ costs $\Theta(N)$. The table of thresholds $I_n^{\min}$ costs $O(N^2)$ if each tail sum is computed directly; it depends only on $N$, $m$, $\beta$ and $\Psi$ and can be computed once. Each new best model costs $\Theta(N)$ for the prefix counts in line L13. With $k$ rounds, the time is $\Theta(k N + N^2)$ with the table, and $\Theta(k N)$ when the table is given. The extra space is $\Theta(N)$. Sorting by quality adds $O(N \log N)$ when the data are not sorted. The number of rounds $k$ is random and at most $k_{\max}$. With a good ranking it is usually far below the RANSAC count for the whole data (a benchmark result of Chum and Matas).

## Properties

- **Uses only the order of the scores.** PROSAC needs no calibrated probability for each match, only a ranking.
- **Draws the samples of RANSAC in a different order.** The growth function hands out samples to each prefix in proportion to what $T_N$ uniform samples would give it.
- **Repeats samples early.** For small $n$, the pool has few distinct samples, so some are drawn more than once. With $T_N = 200000$ and $N = 100$, the first 82 samples all come from the 3 best items; choose $T_N$ with the size of the data in mind.
- **Finds the extent of the inliers.** $n^*$ is an estimate of how far down the ranking the inliers reach.

## Variants and improvements

- **Guided sampling** of Tordoff and Murray (2002) turns the match scores into prior inlier probabilities and samples by them; it needs calibrated scores, PROSAC does not.
- **USAC** (Raguram et al., 2013) uses PROSAC as its sampling stage, together with [LO-RANSAC](/lo-ransac/) and early rejection of bad models.
- **Any score works.** The sampling of PROSAC can be combined with the costs of [MSAC](/msac/), [MLESAC](/mlesac/) or [MAGSAC](/magsac/), since it changes only which samples are drawn.
- **Spatial priors.** NAPSAC (Myatt et al., 2002) draws the items of a sample from a neighborhood, and progressive NAPSAC (Barath et al., 2020) grows these neighborhoods in the manner of PROSAC.

## When to use it

Use PROSAC when each datum has a score that correlates with being an inlier, as in [feature matching](/feature-matching/) with descriptor distances, and the outlier ratio is high. Without a meaningful score, it brings nothing over RANSAC and adds the cost of the stopping test. If the score is calibrated as a probability, guided sampling can also be used.

## Pitfalls

- **A misleading ranking.** If the best-scored matches are systematically wrong, for example repeated texture that gives confident false matches, the early samples are wasted. The growth function limits the damage, because the pool grows anyway.
- **Too large $T_N$ for small data.** The growth is slow, and early samples repeat (see Properties).
- **The swapped branches.** An implementation that copies step 2 of Algorithm 1 literally, instead of eq. (6), draws the samples in a different order than the paper describes.
- **A wrong $\beta$.** If $\beta$ is too small, the non-randomness test passes too easily and PROSAC can stop on a wrong model. Estimate $\beta$ from the threshold and the size of the region where outliers fall.

## Implementations

The Python code fits a line in the plane with $m = 2$. The functions `growth_schedule`, `min_inliers_table` and `choose_n_star` give the schedule $T'_n$, the thresholds $I_n^{\min}$ and the choice of $n^*$ separately, so the tests check each one, and a test checks that each sample contains $u_{g(t)}$.

## History

Chum and Matas presented PROSAC at CVPR 2005. Tordoff and Murray had used match scores in guided MLESAC in 2002, but they needed the scores as probabilities. PROSAC needed only the order, and it gave a stopping rule that finds the size of the reliable part of the ranking. It became the sampling stage of USAC (2013).

## References
