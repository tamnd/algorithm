---
tag: V85QPB
kind: algorithm
slug: randomized-motif-search
name: Randomized motif search
aliases:
- random restart motif search
area: biology/gene-finding-and-motifs
level: intro
summary: Start from random l-mers, then repeat build a profile and pick the most probable l-mer in each sequence until the score stops improving.
solves: [motif-finding-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, W: "the number of windows per sequence, G - L + 1", R: the number of restarts}
  time: {worst: O(R L^2 n^2 W), per_step: O(n W L)}
  space: {extra: O(n L)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Phillip Compeau, Pavel Pevzner]
  note: Compeau and Pevzner gave RandomizedMotifSearch as a simple randomized local search for motifs, between the greedy search and the Gibbs sampler. Its profile step is a hard form of the EM approach.
prereqs: [motif-finding-problem, position-specific-scoring-matrix, randomized-algorithm]
see_also: [greedy-motif-search, gibbs-motif-sampler, meme-algorithm, local-search, hill-climbing, monte-carlo-algorithm, laplace-smoothing, k-means]
sources:
  - book: isbn:9780990374619
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, 2nd edition, Active Learning Publishers, 2015
    locator: Chapter 2, Section 2.7 (randomized motif search) and Section 2.8 (how a randomized algorithm can perform so well)
  - paper: doi:10.1126/science.8211139
    title: Charles E. Lawrence, Stephen F. Altschul, Mark S. Boguski, Jun S. Liu, Andrew F. Neuwald and John C. Wootton, Detecting subtle sequence signals, a Gibbs sampling strategy for multiple alignment, Science 262(5131), 1993
    locator: pp. 208 to 214, the profile and site update that the randomized search makes deterministic
---

Randomized motif search is a local search for the [motif finding problem](/motif-finding-problem/). It picks one random window in each sequence, builds a profile of these windows, and replaces every window by the window of its sequence that is most probable under the profile. It repeats the profile step while the motif score drops, and it restarts from new random windows many times. Each restart ends in a local optimum after at most $L(n - \lceil n/4 \rceil) + 1$ steps; the restarts make it likely that one of them reaches a good motif.

## In plain words

Pick one piece at random from each sequence. Most of the pieces are noise, but by chance a few may be copies of the hidden word. Count the letters in each column of the pieces, and use the counts to pick the best fitting piece of every sequence again. The copies that you picked by luck pull the counts toward the hidden word, so the new pieces fit it better. Repeat until the pieces stop getting better.

One try usually ends in a poor answer. So try again from new random pieces, a few hundred or a few thousand times, and keep the best answer of all tries.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$, each of length $G$, a motif length $L$, a number of restarts $R$ and a seed for the random number generator. Each sequence has $W = G - L + 1$ windows. Positions are 1-based on this page and 0-based in the code.

**Output.** One window $t_i$ in each sequence, with a small motif score $\mathrm{Score}(t_1, \ldots, t_n) = \sum_j (n - \max_a c_j(a))$, where $c_j(a)$ counts the letter $a$ in column $j$ of the windows. The result depends on the seed, and it need not be optimal.

## The algorithm

The profile of windows $t_1, \ldots, t_n$ with pseudocount 1 is $P_j(a) = (c_j(a) + 1)/(n + 4)$. All rows have the same sum, so the most probable window of a sequence is the window with the largest product of counts $\prod_j (c_j(w_j) + 1)$, an exact integer.

```pseudo id=main
RANDOMIZED-MOTIF(s[1 .. n], L, R, rng)
L1  best ← none
L2  for r ← 1 to R do
L3      t_i ← s_i[q_i .. q_i + L - 1] with q_i uniform in 1 .. W, for i ← 1 to n
L4      sc ← Score(t_1, ..., t_n)
L5      loop
L6          P ← the profile of t_1, ..., t_n with pseudocount 1
L7          t'_i ← the first most probable window of s_i under P, for i ← 1 to n
L8          if Score(t') < sc then t ← t', sc ← Score(t')
L9          else exit the loop
L10     if best = none or sc < Score(best) then best ← t
L11 return best
```

Line L3 is the only random step. The code draws the starts with `rng.randrange(W)` once per sequence, in the order of the sequences, from `random.Random(seed)`, so a seed fixes the whole run. Lines L5 to L9 are the deterministic local search: the profile picks new windows (line L7), and the search goes on only while the score drops strictly (line L8). Line L10 keeps the first restart with the smallest score.

## Example

Take the five sequences of Rosalind problem BA2F, each 32 letters long, with $L = 8$, so $W = 25$:

```
CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA
GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG
TAGTACCGAGACCGAAAGAAGTATACAGGCGT
TAGATCAAGTTTCAGGTGCACGTCGGTGAACC
AATCCACCAGCTCCACGTGCAATGTTGGCCTA
```

With seed 0 and $R = 1000$, restart 316 draws the 1-based starts 6, 3, 22, 21 and 6:

| step | starts | windows | score |
|---|---|---|---|
| start | 6, 3, 22, 21, 6 | CTCTCGGG GCGAGGTA TATACAGG CGTCGGTG ACCAGCTC | 19 |
| 1 | 7, 21, 22, 11, 12 | TCTCGGGG CCAAGGTG TATACAGG TTCAGGTG TCCACGTG | 12 |
| 2 | 7, 21, 24, 11, 12 | TCTCGGGG CCAAGGTG TACAGGCG TTCAGGTG TCCACGTG | 9 |
| 3 | 7, 21, 24, 11, 12 | the same windows | 9 |

The start has little agreement, but the profile of its five windows already moves four of them to their final places. Step 3 makes no change, so the restart stops with score 9. This is the sample answer of BA2F, and score 9 is the optimum of this input: the [branch and bound median search](/branch-and-bound-motif-search/) finds the median string AAGTGCCA with total distance 9.

Most restarts end worse. Over the 1000 restarts of seed 0, the final scores range from 9 to 21, and only 2 restarts reach 9. The two runs reach different optimal choices: the second is AACGGCCA, AAGTGCCA, TAGTACCG, AAGTTTCA, ACGTGCAA. Line L10 keeps the first of them. Over 2000 more restarts with seed 1, 8 reach score 9, a measured rate of 0.4 percent per restart. At that rate, the chance that 1000 restarts reach the optimum at least once is $1 - 0.996^{1000} \approx 0.98$.

**Measured success on planted motifs.** The test generator plants a motif with exactly $d$ changes in each of 10 random sequences. A run counts as a success when the consensus of the output equals the planted motif. With 20 seeds (0 to 19):

| $G$ | $(L, d)$ | $R = 10$ | $R = 100$ | $R = 1000$ |
|---|---|---|---|---|
| 100 | (8, 1) | 3 of 20 | 20 of 20 | 20 of 20 |
| 100 | (10, 2) | 2 of 20 | 8 of 20 | 16 of 20 |
| 200 | (12, 3) | 0 of 20 | 0 of 20 | 2 of 20 |

These are measurements on these seeds, not guarantees. The same inputs in the [greedy search](/greedy-motif-search/) with pseudocount 1 give 19, 10 and 4 of 20.

## Correctness

The claims are about what a run returns and how long it takes; the method is a heuristic and does not promise an optimum.

**Theorem (valid output and local optimum).** Each restart ends with one window from each sequence, and its score is at most the score of its random start. When it stops, one more profile step from its windows does not lower the score.

*Proof.* Line L3 picks windows. Line L7 picks a window of each $s_i$, and line L8 accepts the new windows only when the score drops, so the score never rises. The loop exits at line L9 exactly when the profile step does not lower the score. $\square$

**Theorem (step bound).** A restart makes at most $\mathrm{Score}(\text{start}) + 1 \le L(n - \lceil n/4 \rceil) + 1$ profile steps.

*Proof.* Each step but the last lowers the integer score by at least 1, and the score is at least 0, so there are at most $\mathrm{Score}(\text{start})$ such steps. In each column the most common of the four letters occurs at least $\lceil n/4 \rceil$ times, so the score of any choice is at most $L(n - \lceil n/4 \rceil)$. $\square$

Line L7 picks a most probable window because the rows of the profile have equal sums, so the order of the probabilities is the order of the integer products. The tests check the step bound and the local optimum on 60 random inputs, the draw order against a manual replay, and that the score is never below the brute-force optimum. The proof of the facts about the profile step is in proofs/correctness.md.

## Complexity

- **Time.** A profile step builds the counts in $O(nL)$ time and scans the $W$ windows of each of the $n$ sequences at $O(L)$ each, so it costs $O(n W L)$. By the step bound, a restart makes $O(nL)$ steps, so the worst case is $O(R L^2 n^2 W)$. In practice a restart makes few steps: on the BA2F sample the mean is 2.2 steps and the most is 5.
- **Space.** The counts take $4L$ integers and the windows $nL$ letters, so $O(nL)$ besides the input.
- **Randomness.** Each restart draws $n$ integers.

## Properties

- **Randomized.** The output depends on the seed. It is a [Monte Carlo algorithm](/monte-carlo-algorithm/): it always stops in bounded time, but its answer may not be optimal.
- **Local search.** Each restart is a [hill climbing](/hill-climbing/) search that moves to the windows its own profile picks. It stops in the first local optimum.
- **Moves all windows at once.** A step can change every window, which lets it jump far in one step, as the example shows. The [Gibbs sampler](/gibbs-motif-sampler/) changes one window per step instead.
- **Needs pseudocounts.** Without them a letter that does not occur in a column gives probability 0 to many windows, and the search gets stuck.

## Variants and improvements

- **The Gibbs sampler.** Replace one window at a time, chosen by a random draw from the probabilities of the profile of the other windows, not by the largest one. Compeau and Pevzner present it next, and it is less likely to get stuck.
- **Hard EM.** The profile step is the hard form of [expectation maximization](/expectation-maximization/): line L7 is a hard E step that picks one site per sequence, and line L6 is the M step. [MEME](/meme-algorithm/) uses soft weights for all windows instead. The same pattern, with points and means, is the [k-means](/k-means/) algorithm.
- **A better start.** Start from the output of the [greedy search](/greedy-motif-search/), or from windows near a candidate string.
- **More restarts in parallel.** The restarts are independent, so they can run on many cores, each with its own seed.

## When to use it

Use randomized motif search when the motif is strong enough that a few correct windows in a random start pull the profile toward it, and when you can afford hundreds or thousands of restarts. It is easy to write and to check, and it usually beats the greedy search, as the table shows. For subtle motifs, such as the [planted (15, 4) motif](/planted-motif-problem/), use [PROJECTION](/random-projection-motif-finding/) or a Gibbs sampler with many iterations, or [MEME](/meme-algorithm/).

## Pitfalls

- **Too few restarts.** Most restarts end in a poor local optimum; on BA2F only 0.4 percent reach the optimum. Measure the rate on your data and pick $R$ from it.
- **Stopping on a tie.** The loop stops when the score does not drop strictly. Accepting equal scores can loop for ever between two choices with the same score.
- **Floating point products.** The product of $L$ probabilities underflows for long motifs. Compare integer products of counts, or sums of logarithms with a fixed tie rule.
- **Reusing one seed.** Restarts that share a seed repeat the same starts. Use one generator for all restarts, or a different seed for each.
- **A wrong motif length.** A run with the wrong $L$ still returns windows with a low score, often a shifted or a partial copy of the true motif.

## Implementations

## History

Lawrence and others (1993) built the Gibbs sampler on a random form of the same update: the profile of the other sites gives the probabilities of the windows of one sequence, and a draw picks the new site. Compeau and Pevzner (2015) gave the randomized motif search in its present form as a teaching step between the greedy search and the Gibbs sampler. The Rosalind problem BA2F asks for it. Compeau and Pevzner explain in Section 2.8 why a few correct windows in a random start are enough to pull the profile toward the motif.

## References
