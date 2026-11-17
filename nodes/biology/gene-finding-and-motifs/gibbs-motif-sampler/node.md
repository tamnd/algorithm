---
tag: 2BA89G
kind: algorithm
slug: gibbs-motif-sampler
name: Gibbs motif sampler
aliases:
- Lawrence Gibbs sampler
area: biology/gene-finding-and-motifs
level: core
summary: Leave one sequence out, build a profile from the motif sites in the rest, and resample its site with probability given by the profile.
solves: [motif-finding-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, W: "the number of windows per sequence, G - L + 1", T: the number of iterations}
  time: {worst: O(T n W L), per_iteration: O(n W L)}
  space: {extra: O(n L + W)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 1993
  people: [Charles E. Lawrence, Stephen F. Altschul, Mark S. Boguski, Jun S. Liu, Andrew F. Neuwald, John C. Wootton]
  note: Lawrence and others introduced the site sampler for subtle motifs in protein sequences. Liu, Neuwald and Lawrence (1995) gave it a full Bayesian model, in which the update is a draw from an exact conditional distribution.
prereqs: [motif-finding-problem, position-specific-scoring-matrix, gibbs-sampling]
see_also: [randomized-motif-search, meme-algorithm, markov-chain, stationary-distribution, detailed-balance, conjugate-prior, mixing-time, simulated-annealing]
sources:
  - paper: doi:10.1126/science.8211139
    title: Charles E. Lawrence, Stephen F. Altschul, Mark S. Boguski, Jun S. Liu, Andrew F. Neuwald and John C. Wootton, Detecting subtle sequence signals, a Gibbs sampling strategy for multiple alignment, Science 262(5131), 1993
    locator: pp. 208 to 214, the predictive update step and the sampling step of the site sampler
  - paper: doi:10.1080/01621459.1995.10476622
    title: Jun S. Liu, Andrew F. Neuwald and Charles E. Lawrence, Bayesian models for multiple local sequence alignment and Gibbs sampling strategies, Journal of the American Statistical Association 90(432), 1995
    locator: pp. 1156 to 1170, the Bayesian model with Dirichlet priors and the collapsed sampler
  - book: isbn:9780990374619
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, 2nd edition, Active Learning Publishers, 2015
    locator: Chapter 2, Section 2.9, Gibbs sampling
---

The Gibbs motif sampler, or site sampler, of Lawrence and others (1993) solves the [motif finding problem](/motif-finding-problem/) with one site per sequence by a random walk over the choices of sites. In each step it takes one sequence out, builds a profile from the sites of the other sequences, gives each window of the left out sequence a weight that compares its probability under the profile with its probability under the background, and draws the new site with probability in proportion to the weight. The walk is a [Gibbs sampler](/gibbs-sampling/) for an exact posterior distribution of the sites, and the output is the best state the walk visits.

## In plain words

Guess one site in each sequence at random. Now take one sequence out and look at the sites of the others. Count the letters in each column of these sites. For every window of the sequence that you took out, ask how much better the counts explain it than random DNA does. A window that looks like the other sites gets a large weight. Pick the new site of this sequence at random, with chances in proportion to the weights, and put the sequence back. Then do the same for the next sequence, and go on.

A good window does not always win, and that is the point: because a worse window is picked now and then, the walk can leave a poor guess. Over many steps the walk spends most of its time on good choices of sites, and the best choice it visits is the answer.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$ with $n \ge 2$, each of length $G$, a motif length $L$, a number of iterations $T$, a pseudocount $b > 0$, background letter probabilities $q(a) > 0$ and a seed. Each sequence has $W = G - L + 1$ windows. Positions are 1-based on this page and 0-based in the code.

**The model.** Each sequence has exactly one site, at an unknown start $t_i$. The letters of the sites in column $j$ come from an unknown distribution $\theta_j$ with a symmetric Dirichlet prior of parameter $b$, and all other letters come from the fixed background $q$. With a uniform prior on the starts, integrating out the $\theta_j$ gives the posterior

$$\pi(t_1, \ldots, t_n) \propto \frac{\prod_{j=1}^{L} \prod_{a} (b)_{c_j(a)}}{\prod_{i=1}^{n} \prod_{j=1}^{L} q(s_i[t_i + j - 1])},$$

where $c_j(a)$ counts the letter $a$ in column $j$ of the sites and $(b)_m = b(b + 1) \cdots (b + m - 1)$ is the rising factorial. This is the collapsed model of Liu, Neuwald and Lawrence (1995) with one site per sequence.

**Output.** The state with the largest $\pi$ among the states that the walk visits.

## The algorithm

Let $c$ be the column counts of the current sites. To update sequence $i$, remove its site from $c$. Then the weight of the window that starts at $x$ is

$$A_x = \prod_{j=1}^{L} \frac{c_j(s_i[x + j - 1]) + b}{(n - 1 + 4b) \, q(s_i[x + j - 1])}.$$

The first factor of each term is the profile of the other $n - 1$ sites with pseudocount $b$; the second is the background.

```pseudo id=main
GIBBS-MOTIF(s[1 .. n], L, T, b, q, rng)
L1  t_i ← a uniform start in 1 .. W, for i ← 1 to n, and c ← the column counts of the sites
L2  best ← t
L3  for it ← 1 to T do
L4      for k ← 1 to n do (i ← k in the systematic scan, i uniform in 1 .. n in the random scan)
L5          remove the letters of the site t_i from c
L6          A_x ← Π_j (c_j(s_i[x + j - 1]) + b) / ((n - 1 + 4b) q(s_i[x + j - 1])) for x ← 1 to W
L7          draw the new t_i = x with probability A_x / Σ_y A_y
L8          add the letters of the new site t_i to c
L9      if log π(t) > log π(best) then best ← t
L10 return best
```

Line L6 is the predictive update of Lawrence and others, and line L7 is their sampling step. The code works with the logarithms of the weights and subtracts the largest before it takes the exponent, so long motifs do not underflow. Line L9 checks the state once per iteration, that is, once per $n$ updates.

**Random numbers.** The code uses `random.Random(seed)`. Line L1 draws one `rng.randrange(W)` per sequence, in order. Each update then draws one `rng.randrange(n)` in the random scan only, and one `rng.random()` for line L7, compared with the running sum of the weights.

## Example

Take the five sequences of Rosalind problem BA2D with $L = 3$, $b = 1$ and the uniform background $q(a) = 1/4$, and let the current sites be CAG, CAG, CAA, CAA and CAA (1-based starts 7, 7, 1, 6 and 1). Update $s_1 =$ GGCGTTCAGGCA. The other sites CAG, CAA, CAA, CAA have the counts C: 4 in column 1, A: 4 in column 2, and G: 1, A: 3 in column 3. With $n - 1 + 4b = 8$, each factor of $A_x$ is $(c + 1)/8 \div 1/4 = (c + 1)/2$:

| $x$ | window | $A_x$ | probability |
|---|---|---|---|
| 1 | GGC | 1/8 | 0.014 |
| 2 | GCG | 1/4 | 0.028 |
| 3 | CGT | 5/8 | 0.070 |
| 4 | GTT | 1/8 | 0.014 |
| 5 | TTC | 1/8 | 0.014 |
| 6 | TCA | 1/2 | 0.056 |
| 7 | CAG | 25/4 | 0.704 |
| 8 | AGG | 1/4 | 0.028 |
| 9 | GGC | 1/8 | 0.014 |
| 10 | GCA | 1/2 | 0.056 |

The weights sum to $71/8$, so the site stays at CAG with probability $50/71 \approx 0.704$, and moves elsewhere with probability $21/71$. A strict search, like the [randomized motif search](/randomized-motif-search/), would always take CAG.

**The sampler maximizes the posterior, not the motif score.** On the sample of Rosalind problem BA2F with $L = 8$, $b = 1$ and the letter frequencies of the input as background, runs of 2000 iterations from seeds 0 to 4 all end with the best state GTGTTCAG, GTGTAAGT, GTATACAG, GTGCACGT, GTGCAATG, with $\log \pi = 80.349$ and motif score 11. The optimum of the motif score is 9, but the two optimal choices have smaller $\log \pi$, 79.210 and 79.411. The sampler did its job; the two goals differ.

**Measured success on planted motifs.** The test generator plants a motif with exactly $d$ changes in each of 10 random sequences. A run counts as a success when the consensus of the best state equals the planted motif. With the systematic scan, $b = 1$, the input letter frequencies as background and seeds 0 to 19:

| $G$ | $(L, d)$ | $T = 20$ | $T = 100$ | $T = 1000$ |
|---|---|---|---|---|
| 100 | (8, 1) | 7 of 20 | 14 of 20 | 20 of 20 |
| 100 | (10, 2) | 1 of 20 | 7 of 20 | 12 of 20 |
| 200 | (12, 3) | 0 of 20 | 0 of 20 | 1 of 20 |

For $(10, 2)$ and $T = 1000$, the best state has $\log \pi$ at least that of the planted sites in 17 of 20 runs, so in 5 runs the model itself prefers another motif. These are measurements on these seeds, not guarantees. On seeds 0 to 9 with $(8, 1)$ and $T = 100$, the systematic scan succeeds in 7 runs and the random scan in 6.

## Correctness

**Theorem (the exact full conditional).** The probabilities of line L7 are the conditional distribution of $t_i$ given the other sites under $\pi$.

*Proof.* Fix $t_k$ for $k \ne i$ and let $c^{-i}$ be their column counts. If the site of $s_i$ is the window $w$, the count of $w_j$ in column $j$ is $c^{-i}_j(w_j) + 1$ and the other counts of column $j$ are those of $c^{-i}$. Since $(b)_{m+1} = (b)_m (b + m)$, the numerator of $\pi$ is $\prod_j \prod_a (b)_{c^{-i}_j(a)} \times \prod_j (b + c^{-i}_j(w_j))$. The first product and the background terms of the other sites do not depend on $w$. So $\pi(t_i = x \mid t_{-i}) \propto \prod_j (c^{-i}_j(w_j) + b)/q(w_j)$, and the constant $(n - 1 + 4b)^{-L}$ in $A_x$ does not change the normalized values. $\square$

So each update is a Gibbs step, and by the general theory of [Gibbs sampling](/gibbs-sampling/) it leaves $\pi$ invariant: it satisfies [detailed balance](/detailed-balance/) with respect to $\pi$. The systematic scan is a product of such steps and the random scan is their average, so both leave $\pi$ invariant. Every weight is positive, so one sweep of either scan can reach every state, the [Markov chain](/markov-chain/) is irreducible and aperiodic, and $\pi$ is its unique [stationary distribution](/stationary-distribution/). The state of the chain converges in distribution to $\pi$, and since the chain has finitely many states and is irreducible, it visits every state, the mode of $\pi$ too, with probability 1.

These are statements about the limit. They say nothing about how fast the chain mixes, and on real data it can stay in a poor mode for a long time. The tests check the theorem exactly with fractions on a small input, check that both scans leave $\pi$ invariant exactly, check the sampling step with a chi-square test, and measure the planted success rate. The proofs are in proofs/correctness.md.

## Complexity

- **Time.** An update removes and adds a site in $O(L)$ time and computes $W$ weights at $O(L)$ each, so it takes $O(WL)$. An iteration is $n$ updates, plus $O(nL)$ for $\log \pi$ at line L9, so $O(nWL)$. $T$ iterations take $O(T n W L)$.
- **Space.** The counts take $4L$ integers, the sites $n$ integers and the weights $W$ numbers, so $O(nL + W)$ with the windows of the best state.
- **Randomness.** One draw per update, plus one in the random scan.

## Properties

- **Randomized and approximate.** The output depends on the seed, and a finite run gives no guarantee.
- **Never stuck for good.** Every window has a positive weight, so the walk can leave any state. A strict local search stops in the first local optimum.
- **One site moves at a time.** The walk moves slowly, and a shifted copy of the motif, the true motif moved by one or two positions, is a strong trap: most single moves from it lower $\pi$.
- **The background matters.** The weights compare the profile with the background. A background that does not match the input, for example a uniform one on GC rich DNA, makes the sampler prefer windows rich in the common letters.

## Variants and improvements

- **Phase shifts.** Lawrence and others added a move that shifts all sites by the same small offset, to escape from a shifted copy of the motif. The code on this page does not include it.
- **Zero or one site per sequence.** The models of Liu, Neuwald and Lawrence allow sequences with no site and sequences with several sites, with a prior on the number of sites.
- **Several motifs.** Later samplers extend the model to several motifs at once, to sites on both strands, and to backgrounds that depend on the letters before them.
- **Restarts and annealing.** Run several chains from different seeds, or raise the weights to a power that grows over time, as in [simulated annealing](/simulated-annealing/), to find the mode faster.
- **The version of Compeau and Pevzner.** Their GibbsSampler uses the profile probability without the background, and keeps the state with the best motif score.

## When to use it

Use the Gibbs motif sampler when the motif is subtle, the sequences are long, and you want a method that does not stop in the first local optimum. The method works with proteins as well as DNA; proteins were its first use. The code on this page is for DNA. Run several seeds and compare the results; agreement between runs is a good sign. For short motifs on short sequences, an exact [median string](/median-string-problem/) search is cheaper and certain. For a single soft optimum, [MEME](/meme-algorithm/) is deterministic for a given start. For the planted $(15, 4)$ problem, [PROJECTION](/random-projection-motif-finding/) gives a better start than a uniform one.

## Pitfalls

- **Reading the last state as the answer.** The state at the end of the run is a random draw. Keep the best state, or count how often each site is picked.
- **Underflow.** The product of $L$ ratios can overflow or underflow. Work with logarithms and subtract the largest before the exponent.
- **Forgetting to remove the site.** The profile at line L6 must not include the site of the sequence being updated, or the current site gets an unfair bonus and the chain does not sample $\pi$.
- **Too few iterations.** On the planted $(10, 2)$ data, 20 iterations succeed once in 20 runs and 1000 iterations 12 times. Measure the rate on your data.
- **Comparing with the motif score.** The sampler maximizes $\pi$, not the motif score, as the BA2F example shows.

## Implementations

## History

Lawrence, Altschul, Boguski, Liu, Neuwald and Wootton (1993) introduced the site sampler to align subtle motifs in protein sequences. Their method alternates a predictive update, the profile of the other sites, with a sampling step. Liu, Neuwald and Lawrence (1995) set the method in a Bayesian model with Dirichlet priors, in which the update draws from the exact conditional of the collapsed model, and compared several sampling strategies. Compeau and Pevzner (2015) present a simple form of it after the randomized motif search.

## References
