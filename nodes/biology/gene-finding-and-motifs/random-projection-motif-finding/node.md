---
tag: 24V46J
kind: algorithm
slug: random-projection-motif-finding
name: Random projection motif finding
aliases:
- PROJECTION algorithm
area: biology/gene-finding-and-motifs
level: advanced
summary: Hash all windows by k random positions into buckets, refine heavily filled buckets with EM, and repeat with new projections.
solves: [planted-motif-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, W: "the number of windows per sequence, G - L + 1", k: the number of projected positions, m: the number of trials, B: the number of buckets refined in a trial, I: the number of EM iterations per bucket}
  time: {worst: O(m (n W k + B I n W L)), hashing_per_trial: O(n W k)}
  space: {extra: O(n W + L)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Jeremy Buhler, Martin Tompa]
  note: Buhler and Tompa presented PROJECTION at RECOMB 2001 and in the Journal of Computational Biology in 2002, as a way to find good EM starts for the planted (15, 4) motif challenge.
prereqs: [planted-motif-problem, locality-sensitive-hashing, expectation-maximization]
see_also: [random-projection, winnower-algorithm, meme-algorithm, binomial-distribution, hamming-distance, kmer, monte-carlo-algorithm, gibbs-motif-sampler]
sources:
  - paper: doi:10.1089/10665270252935430
    title: Jeremy Buhler and Martin Tompa, Finding motifs using random projections, Journal of Computational Biology 9(2), 2002
    locator: pp. 225 to 242, the projection, the bucket threshold, the refinement by EM and the analysis of the number of trials
  - paper: doi:10.1145/369133.369172
    title: Jeremy Buhler and Martin Tompa, Finding motifs using random projections, Proceedings of the Fifth Annual International Conference on Computational Biology (RECOMB 2001), ACM, 2001
    locator: the conference version of the method
  - paper: "Pavel A. Pevzner and Sing-Hoi Sze, Combinatorial approaches to finding subtle signals in DNA sequences, Proceedings of the Eighth International Conference on Intelligent Systems for Molecular Biology (ISMB 2000), AAAI Press, 2000, pp. 269-278"
    title: Combinatorial approaches to finding subtle signals in DNA sequences
    locator: the planted (15, 4) motif challenge that PROJECTION addresses
---

PROJECTION, of Buhler and Tompa (2001, 2002), finds a planted motif by hashing. It picks $k$ of the $L$ positions of a window at random and puts every window of every sequence into the bucket given by its letters at these positions. A planted copy of the motif lands in the bucket of the motif whenever none of its changed positions is picked, so the bucket of the motif tends to fill up, while random buckets stay small. Each bucket that holds windows from enough sequences is a start for [EM](/expectation-maximization/), which refines it into a motif model. Many trials with new positions make it very likely that some trial puts enough copies into one bucket.

## In plain words

Two copies of the hidden word differ in a few places. If you look at only some of the places, chosen at random, you will often miss all the differences, and then the two copies look the same. So pick a few places at random and sort all the short pieces of all sequences by their letters at those places. Copies of the hidden word that agree at the chosen places end up in the same pile.

A pile with pieces from many sequences is a good lead. Use the pieces in it to make a first guess of the word, and improve the guess with EM over all the data. One choice of places may fail, so repeat with new places many times and keep the best guess.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$, each of length $G$, a motif length $L$, a projection size $k \le L$, a bucket threshold $s$, a number of trials $m$ and a seed. Each sequence has $W = G - L + 1$ windows. Positions are 1-based on this page and 0-based in the code.

**Output.** A motif model $\theta$ (letter probabilities for each column), its consensus and its most likely site in each sequence. The target is the [planted motif problem](/planted-motif-problem/): find the motif $M$ when each sequence holds a copy of $M$ with $d$ changes.

## The algorithm

For a set $I$ of positions, the projection of a window $x$ is $h_I(x) = (x_i)_{i \in I}$, the letters of $x$ at the positions in $I$. This is the bit sampling family of [locality sensitive hashing](/locality-sensitive-hashing/) for the Hamming distance: windows that are close agree at more positions, so they land in the same bucket more often.

```pseudo id=main
PROJECTION(s[1 .. n], L, k, s_min, m, rng)
L1  best ← none
L2  for trial ← 1 to m do
L3      I ← k distinct positions drawn uniformly from 1 .. L
L4      put every window x of every sequence into the bucket h_I(x)
L5      for each bucket B that holds windows of at least s_min sequences do
L6          θ ← the letter counts of the windows of B, plus prior counts βμ(a), as probabilities
L7          refine θ by EM with one site per sequence
L8          if the score of θ is above the score of best then best ← θ
L9  return best, its consensus, and the most likely site in each sequence
```

Line L3 is the only random step: the code draws `rng.sample(range(L), k)` once per trial from `random.Random(seed)`. Line L7 runs EM for the model with one occurrence per sequence (OOPS) and a fixed background $\mu$, the letter frequencies of the input. The E step gives each window of $s_i$ the weight $z_{iq} \propto \prod_j \theta_j(x_j)/\mu(x_j)$, normalized within the sequence; the M step sets $\theta_j(a) = (\sum z_{iq} [x_j = a] + \beta\mu(a))/(n + \beta)$. The score of line L8 is the log likelihood ratio of the OOPS model, $\sum_i \log(\frac{1}{W} \sum_q \prod_j \theta_j(x_j)/\mu(x_j))$. The code uses $\beta = 1$ and 10 EM iterations per bucket, and it counts the sequences of a bucket, not its windows, against $s_{\min}$; these are the choices of this code.

## Example

**One copy.** Let $L = 15$, $d = 4$ and $k = 7$. A copy of the motif with 4 changed positions lands in the motif's bucket when the 7 picked positions avoid the 4 changed ones:

$$p = \frac{\binom{L - d}{k}}{\binom{L}{k}} = \frac{\binom{11}{7}}{\binom{15}{7}} = \frac{330}{6435} = \frac{2}{39} \approx 0.0513.$$

**One trial.** With $n = 20$ sequences, the number of copies in the motif's bucket is $\mathrm{Bin}(20, p)$ when the changed positions are random, so a trial puts at least $s = 4$ copies there with probability $P = \Pr[\mathrm{Bin}(20, 2/39) \ge 4] \approx 0.0173$.

**The number of trials.** To reach a good bucket with probability at least $0.95$, PROJECTION needs $m$ trials with $1 - (1 - P)^m \ge 0.95$, so $m = \lceil \log 0.05 / \log(1 - P) \rceil = 172$.

**Random buckets.** For $G = 600$, there are $nW = 20 \cdot 586 = 11{,}720$ windows and $4^7 = 16{,}384$ buckets, so a random bucket holds $0.72$ windows on average. A bucket of random windows can still reach the threshold, which is why each candidate is checked by its EM score and not taken as it is.

**Measured runs.** The test generator plants a motif with exactly $d$ changes in each sequence. With $(n, G, L, d) = (8, 60, 10, 2)$, $k = 5$ and $s = 4$, the theory gives $p = 56/252 = 0.222$, $P \approx 0.079$ and $m = 37$ trials for 0.95. Over seeds 0 to 19, the consensus of the result equals the planted motif in 15 of 20 runs, and the sites equal the planted starts in 11; on average 33 buckets per run reach the threshold. These are measurements of this code on these seeds.

**A fixed input.** The formula for $P$ averages over the random changes as well as over the projections. On a fixed input the changes are fixed, and the hits of the copies are no longer independent, because they share one projection. For five inputs with $(n, G, L, d) = (20, 600, 15, 4)$ from the test generator (seeds 1 to 5), a count over all 6435 sets of 7 positions gives the chance of at least 4 copies in the motif's bucket as 1.48, 2.00, 1.85, 1.20 and 3.25 percent, against 1.73 percent from the formula. The mean rate per copy is exactly $2/39$ on each input, since every copy has exactly 4 changes.

## Correctness

PROJECTION is a heuristic with a probabilistic guarantee for its first stage.

**Theorem (the hit probability).** If the $d$ changed positions of a copy are a uniform random $d$-set and $I$ is a uniform random $k$-set, independent of each other, then the copy and the motif have the same projection with probability at least $p = \binom{L-d}{k}/\binom{L}{k}$, with equality when every change makes the letter differ from the motif.

*Proof.* The projections agree when every picked position has the same letter in the copy and the motif, which holds when $I$ avoids the changed positions. For a fixed $d$-set, $\binom{L-d}{k}$ of the $\binom{L}{k}$ choices of $I$ avoid it. In the generator every change makes the letter differ, so agreement holds exactly when $I$ avoids the set. $\square$

**Theorem (enough trials).** If the copies of the $n$ sequences have independent random changes, a trial puts at least $s$ copies into the motif's bucket with probability $P = \Pr[\mathrm{Bin}(n, p) \ge s]$, and $m$ independent trials do so at least once with probability $1 - (1 - P)^m$.

*Proof.* For a fixed $I$, each copy hits independently with probability $p$ by the first theorem, so the count is $\mathrm{Bin}(n, p)$ for every $I$. The trials use independent projections and are independent. $\square$

A good bucket is a good start for EM, not a proof that EM finds the motif; EM can still move to another local optimum, and line L8 can prefer a random bucket with a better score. The OOPS EM step does not lower its score plus the log prior term $\beta \sum_j \sum_a \mu(a) \log \theta_j(a)$, by the general ascent property of EM. The tests check $p$ by enumeration of all position sets for $L \le 8$ and by simulation within 4 standard deviations, check the formula for $m$, check that EM does not lower the score with and without the prior term, check the draw order, and measure the planted success rate. The proofs are in proofs/correctness.md.

## Complexity

- **Hashing.** A trial computes $nW$ keys of $k$ letters, $O(nWk)$ time, and stores them in $O(nW)$ space.
- **Refinement.** An EM iteration looks at all $nW$ windows of $L$ letters, $O(nWL)$. With $B$ buckets refined per trial and $I$ iterations each, a trial costs $O(nWk + BInWL)$, and $m$ trials $O(m(nWk + BInWL))$.
- **The choice of $k$.** A larger $k$ makes random buckets smaller, so $B$ drops, but it also lowers $p$, so $m$ grows. A good $k$ keeps the mean size of a random bucket, $nW/4^k$, below 1 while $k$ stays below $L - d$.
- **Space.** The buckets take $O(nW)$ and the model $O(L)$. There is no graph of close pairs, so the memory does not grow with the number of such pairs, as it does in [WINNOWER](/winnower-algorithm/).

## Properties

- **Randomized.** The result depends on the seed. The first stage has the guarantee of the trials theorem; the second does not.
- **Locality sensitive hashing.** The projection is a hash that sends close windows to the same bucket with a probability that falls with their distance. It is a [random projection](/random-projection/) onto $k$ coordinates.
- **Independent trials.** The trials do not depend on each other, so they can run in parallel.
- **Uses EM for the details.** The hashing only finds starts. The motif model comes from EM, as in [MEME](/meme-algorithm/).

## Variants and improvements

- **Other refinement.** Replace EM by a [Gibbs motif sampler](/gibbs-motif-sampler/) run or by a local search on the motif string.
- **Several motifs or no planted model.** Use the same buckets for real data, with a threshold set from the expected size of random buckets.
- **Gapped projections.** Choose the positions so that they cover the motif evenly, or use structured sets of positions in place of random ones, to raise the hit rate for the same $k$.
- **Exact methods.** For small $(L, d)$, exact algorithms for the planted motif problem enumerate candidate strings with pruning; PROJECTION scales to larger $L$.

## When to use it

Use PROJECTION for planted motif problems with subtle motifs, such as $(15, 4)$ or harder, where single windows are poor starts for EM. Work out $p$, $P$ and $m$ for your $(n, L, d)$ before the run, and pick $k$ so that random buckets are small. For short motifs with few changes, the [median string](/median-string-problem/) search is exact and cheap. When the motif is a profile and not a string with a fixed number of changes, run [MEME](/meme-algorithm/) or a Gibbs sampler directly.

## Pitfalls

- **A $k$ that is too large.** If $k > L - d$, a copy with $d$ changes never hits the motif's bucket, and $p = 0$.
- **A $k$ that is too small.** Random buckets fill up, and the refinement runs on many useless buckets.
- **Trusting the formula on a fixed input.** The trials theorem averages over the planting. On a fixed input the rate can be lower, as the example shows (1.20 percent in place of 1.73); add a margin to $m$.
- **Counting windows, not sequences.** A bucket with several overlapping windows of one sequence is weak evidence. This code counts sequences.
- **Reading the bucket as the answer.** The bucket is a start. Report the refined model and its sites, and check them.

## Implementations

## History

Pevzner and Sze (2000) posed the planted $(15, 4)$ motif challenge and solved it with WINNOWER and SP-STAR. Buhler and Tompa (2001, 2002) then gave PROJECTION, which uses random projections, an idea from locality sensitive hashing, to find good starting points for EM on the $(15, 4)$ challenge and other planted motif problems. Their analysis of the hit probability and of the number of trials is the one on this page.

## References
