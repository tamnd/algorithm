---
tag: RM3ZE9
kind: model
slug: pair-hmm
name: Pair hidden Markov model
aliases:
- pair HMM
- pairwise HMM
area: biology/sequence-alignment
level: research
summary: "An HMM that emits two sequences at once through match, insert-in-x and insert-in-y states, so it defines a probability for each pairwise alignment and for each pair of sequences."
prereqs: [hidden-markov-model, affine-gap-alignment, viterbi-algorithm, forward-algorithm]
see_also: [forward-backward-algorithm, baum-welch-algorithm, gotoh-algorithm, needleman-wunsch, profile-hmm, probcons, edit-distance, finite-state-transducer]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: "Chapter 4 (pages 80 to 99): the pair HMM with states M, X and Y, its Viterbi equations and the mapping to affine gap scores against the random model, the Forward probability P(x, y), sampling of alignments, and the posterior probability that x_i is aligned to y_j"
  - paper: doi:10.1089/cmb.1998.5.493
    title: Ian Holmes and Richard Durbin, Dynamic programming alignment accuracy, Journal of Computational Biology 5(3), 1998, pages 493 to 504
    locator: expected accuracy of an alignment from pair-HMM posteriors and the dynamic program for the alignment of maximum expected accuracy
  - paper: doi:10.1101/gr.2821705
    title: Chuong B. Do, Mahathi S. P. Mahabhashyam, Michael Brudno and Serafim Batzoglou, ProbCons, probabilistic consistency-based multiple sequence alignment, Genome Research 15(2), 2005, pages 330 to 340
    locator: pair-HMM posterior match probabilities as the input of multiple alignment
  - paper: doi:10.1007/BF02193625
    title: Jeffrey L. Thorne, Hirohisa Kishino and Joseph Felsenstein, An evolutionary model for maximum likelihood alignment of DNA sequences, Journal of Molecular Evolution 33(2), 1991, pages 114 to 124
    locator: an insertion and deletion process in time whose alignment distribution is a pair HMM
  - paper: doi:10.1109/34.682181
    title: Eric Sven Ristad and Peter N. Yianilos, Learning string-edit distance, IEEE Transactions on Pattern Analysis and Machine Intelligence 20(5), 1998, pages 522 to 532
    locator: stochastic edit distance, a one-state pair model trained by expectation maximization
---

A pair hidden Markov model is a [hidden Markov model](/hidden-markov-model/) that emits two sequences $x$ and $y$ at the same time. Its match state emits one residue of each, and its two insert states emit a residue of one sequence only, so each state path is a pairwise alignment and the model gives a joint probability $P(x, y, \pi)$ to each alignment $\pi$. The most probable path is the optimal [affine gap alignment](/affine-gap-alignment/) for scores that the model fixes, and the sum over all paths, $P(x, y)$, scores the relation between $x$ and $y$ without choosing an alignment. Durbin, Eddy, Krogh and Mitchison (1998, Chapter 4) give the standard presentation.

## The machine

**States.** Besides a silent Begin and End, there are three emitting states.

| state | emits | probability of the emission |
|---|---|---|
| $M$ (match) | a pair $(x_i, y_j)$ | $p_{x_i y_j}$ |
| $X$ (insert in $x$) | $x_i$ against a gap | $q_{x_i}$ |
| $Y$ (insert in $y$) | $y_j$ against a gap | $q_{y_j}$ |

Here $p_{ab}$ is a joint distribution on pairs of residues, and $q_a$ is the background distribution.

**Transitions.** With gap-open probability $\delta$, gap-extend probability $\varepsilon$ and end probability $\tau$:

| from | to $M$ | to $X$ | to $Y$ | to End |
|---|---|---|---|---|
| Begin, $M$ | $1 - 2\delta - \tau$ | $\delta$ | $\delta$ | $\tau$ |
| $X$ | $1 - \varepsilon - \tau$ | $\varepsilon$ | 0 | $\tau$ |
| $Y$ | $1 - \varepsilon - \tau$ | 0 | $\varepsilon$ | $\tau$ |

Begin has the same transitions as $M$. The model has no transitions between $X$ and $Y$, so an insert column is never next to a delete column. This is Durbin's model; other pair HMMs allow $X \leftrightarrow Y$, use different parameters for $X$ and $Y$, or add more gap states for long and short gaps.

**A run.** Start in Begin. In each step move to a state by the transition probabilities. In $M$, emit a pair; in $X$, emit a residue of $x$; in $Y$, emit a residue of $y$. Stop at End. The sequence of states $\pi$ is the alignment: $M$ is a column with two residues, $X$ is a residue of $x$ over a gap, and $Y$ is a residue of $y$ over a gap. For sequences of lengths $n$ and $m$, a path that emits them goes from cell $(0, 0)$ to cell $(n, m)$ of the alignment grid; $M$ moves diagonally, $X$ down and $Y$ right.

**The joint probability.** For a path $\pi = \pi_1 \ldots \pi_L$ that emits $x$ and $y$,

$$P(x, y, \pi) = \Bigl(\prod_{t=1}^{L} a_{\pi_{t-1} \pi_t}\, e_{\pi_t}(\text{column } t)\Bigr)\, \tau,$$

with $\pi_0 = \text{Begin}$, transition probabilities $a$ and emissions $e$. The number of columns $L$ has a geometric distribution with mean $(1 - \tau)/\tau$.

**The random model.** To score, compare with a model $R$ that emits $x$ and then $y$ independently, each residue with probability $q_a$, and each sequence of length $k$ with probability $\eta (1 - \eta)^k$:

$$P(x, y \mid R) = \eta^2 (1 - \eta)^{n + m} \prod_i q_{x_i} \prod_j q_{y_j}.$$

**The example model.** For DNA take $\delta = 1/5$, $\varepsilon = 2/5$, $\tau = 1/10$, $q_a = 1/4$, $p_{aa} = 1/8$ and $p_{ab} = 1/24$ for $a \ne b$. A match column has two equal bases with probability 1/2. Then $1 - 2\delta - \tau = 1/2$ and $1 - \varepsilon - \tau = 1/2$.

## What it counts

**The Viterbi recurrences.** The general [Viterbi algorithm](/viterbi-algorithm/) becomes three tables over the grid. Let $v^M(i, j)$ be the largest probability of a path that emits $x_1 \ldots x_i$ and $y_1 \ldots y_j$ and ends in $M$, and so on, with $v^M(0, 0) = 1$ for Begin and all other entries with a negative index equal to 0:

$$v^M(i, j) = p_{x_i y_j} \max\bigl\{(1 - 2\delta - \tau)\, v^M(i-1, j-1),\; (1 - \varepsilon - \tau)\, v^X(i-1, j-1),\; (1 - \varepsilon - \tau)\, v^Y(i-1, j-1)\bigr\},$$

$$v^X(i, j) = q_{x_i} \max\bigl\{\delta\, v^M(i-1, j),\; \varepsilon\, v^X(i-1, j)\bigr\}, \qquad v^Y(i, j) = q_{y_j} \max\bigl\{\delta\, v^M(i, j-1),\; \varepsilon\, v^Y(i, j-1)\bigr\},$$

$$v^E = \tau \max\bigl\{v^M(n, m),\, v^X(n, m),\, v^Y(n, m)\bigr\}.$$

These are the recurrences of [Gotoh's algorithm](/gotoh-algorithm/) in the probability domain, and they take $O(nm)$ time.

**Viterbi equals affine alignment.** Divide a path probability by $P(x, y \mid R)$ and assign each factor to an alignment column. A match column of $a$ and $b$ entered from $M$ contributes $\frac{p_{ab}}{q_a q_b} \cdot \frac{1 - 2\delta - \tau}{(1 - \eta)^2}$. A gap of length $k$ between two match columns contributes $\frac{\delta\, \varepsilon^{k-1}}{(1-\eta)^k}$ for the gap and changes the factor $1 - 2\delta - \tau$ of the next match column into $1 - \varepsilon - \tau$. So, with logarithms,

$$s(a, b) = \log \frac{p_{ab}}{q_a q_b} + \log \frac{1 - 2\delta - \tau}{(1 - \eta)^2}, \quad d = -\log \frac{\delta (1 - \varepsilon - \tau)}{(1 - \eta)(1 - 2\delta - \tau)}, \quad e = -\log \frac{\varepsilon}{1 - \eta},$$

the log-odds of every path is the affine score $\sum s - \sum (d + (k-1) e)$ of its alignment, a gap of length $k$ costing $d + (k-1)e$, plus the constant $\log(\tau / \eta^2)$, plus a correction $c = \log \frac{1 - 2\delta - \tau}{1 - \varepsilon - \tau}$ if the alignment ends in a gap (that gap has no match column after it to absorb its factor). Taking the maximum over paths on both sides, when $c = 0$ the Viterbi path is an optimal alignment for $(s, d, e)$ among alignments with no insert column next to a delete column (for $c \ne 0$ it is optimal for the affine score plus $c$ on alignments that end in a gap), and its log-odds is the optimal score plus the constants. Read in reverse, a choice of affine scores is an implicit choice of $\delta$, $\varepsilon$ and $p_{ab}$.

For the example model with $\eta = 1/10$, in bits: $s(a, a) = 0.304$, $s(a, b) = -1.281$, $d = 2.170$, $e = 1.170$, $c = 0$ (because $\delta$ and $\varepsilon$ give the same exit probability 1/2 out of $M$ and out of a gap state), and the constant is $\log_2 10 = 3.322$.

**The Forward recurrences.** Replace each max by a sum; $f^M(i, j)$ is then the total probability of all paths that emit the prefixes and end in $M$:

$$f^M(i, j) = p_{x_i y_j}\bigl[(1 - 2\delta - \tau) f^M(i-1, j-1) + (1 - \varepsilon - \tau)\bigl(f^X(i-1, j-1) + f^Y(i-1, j-1)\bigr)\bigr],$$

and similarly for $f^X$ and $f^Y$. The total $P(x, y) = \tau \bigl(f^M(n, m) + f^X(n, m) + f^Y(n, m)\bigr) = \sum_\pi P(x, y, \pi)$ is the probability that the model emits $x$ and $y$ by any alignment. The ratio $P(x, y)/P(x, y \mid R)$ is a score of relatedness that does not commit to one alignment.

**Posterior match probabilities.** With the Backward tables $b^M, b^X, b^Y$ (the same recurrences run from $(n, m)$, starting from $\tau$),

$$P(x_i \diamond y_j \mid x, y) = \frac{f^M(i, j)\, b^M(i, j)}{P(x, y)}$$

is the probability that $x_i$ and $y_j$ are in the same match column, given the two sequences. These numbers measure how reliable each part of an alignment is.

**A small case by hand.** Let $x = \text{TAG}$ and $y = \text{TG}$. The alignment paths with no $X$ next to $Y$ are $MXM$, $MMX$, $XMM$, $XXMY$ and $YMXX$. The best is

$$P(x, y, MXM) = \tfrac12 \cdot \tfrac18 \cdot \tfrac15 \cdot \tfrac14 \cdot \tfrac12 \cdot \tfrac18 \cdot \tfrac1{10} = \tfrac{1}{51200},$$

for T-T, A over a gap, G-G and End. The sum of all five is $P(x, y) = 43/1280000$, so the Viterbi path carries only $25/43 \approx 0.581$ of the probability; $MMX$ and $XMM$ have 0.194 each and the two paths with one match 0.016 each. The posteriors are exact fractions: $P(x_1 \diamond y_1) = P(x_3 \diamond y_2) = 100/129 \approx 0.775$, and $P(x_2 \diamond y_1) = P(x_2 \diamond y_2) = 25/129 \approx 0.194$. All of these values agree with a sum over all five paths.

**A longer case.** Let $x = \text{GATTC}$ and $y = \text{GTTAC}$. The Viterbi path is $MMMMM$, with probability $1/94371840$ and log-odds 1.672 bits against $R$ with $\eta = 1/10$, which is the affine score $3(0.304) + 2(-1.281) + 3.322$. Forward gives $P(x, y) = 9417331/331776000000000$ and 3.094 bits, so the best path holds only 37 percent of the probability. The posterior table, rows $x_i$ and columns $y_j$:

| | G | T | T | A | C |
|---|---|---|---|---|---|
| G | **0.823** | 0.039 | 0.015 | 0.002 | 0.000 |
| A | 0.101 | **0.488** | 0.050 | 0.048 | 0.002 |
| T | 0.018 | 0.308 | **0.435** | 0.050 | 0.015 |
| T | 0.002 | 0.048 | 0.308 | **0.488** | 0.039 |
| C | 0.000 | 0.002 | 0.018 | 0.101 | **0.823** |

The ends are reliable. In the middle, the first T of $x$ goes with the second T of $y$ (0.435) or with the first (0.308): the alignment with one gap on each side, which matches both T pairs, is almost as likely as the gapless one. The alignment that maximizes the sum of posteriors of its match columns is again $MMMMM$, with an expected 3.056 correct pairs out of 5.

## Relation to other models

- **[Hidden Markov models](/hidden-markov-model/).** A pair HMM is an HMM whose states emit on two tapes. Forward, Backward, Viterbi and [Baum-Welch](/baum-welch-algorithm/) carry over, with a two-dimensional table in place of a one-dimensional one, because the position in each sequence is part of the state of the computation.
- **Affine gap alignment.** As shown above, the Viterbi path is the optimal [Gotoh](/gotoh-algorithm/) alignment for scores that the parameters fix. When $d = e$, that is $\delta (1 - \varepsilon - \tau) = \varepsilon (1 - 2\delta - \tau)$, the gap cost is linear and the Viterbi path is a [Needleman-Wunsch](/needleman-wunsch/) alignment. The probabilistic view adds the Forward score, the posteriors and a way to estimate the scores from data.
- **Stochastic edit distance.** A pair HMM with one state that emits matches, substitutions, insertions and deletions is the stochastic [edit distance](/edit-distance/) of Ristad and Yianilos (1998), trained by [expectation maximization](/expectation-maximization/).
- **Transducers.** A pair HMM is a probabilistic [finite-state transducer](/finite-state-transducer/): it reads $x$ and writes $y$, with weights that are probabilities.
- **Evolutionary models.** The insertion and deletion process of Thorne, Kishino and Felsenstein (1991) gives, for two sequences separated by time $t$, an alignment distribution that is a pair HMM whose parameters are functions of $t$ and the rates.
- **[Profile HMMs](/profile-hmm/).** If one sequence is fixed, the states of a pair HMM can be unrolled along it into match, insert and delete states for each position; this gives a profile HMM built from one sequence.

## Known results in the model

- **Complexity.** Viterbi, Forward and Backward take $O(nm)$ time and $O(nm)$ space; the score alone needs $O(\min(n, m))$ space, and the Viterbi path needs linear space with the divide and conquer of Hirschberg.
- **Normalization.** For fixed $\tau > 0$ the probabilities $P(x, y, \pi)$ add up to 1 over all triples, so $P(x, y)$ is a distribution on pairs of sequences, and the posterior distribution over alignments given $(x, y)$ is well defined.
- **Sampling.** A stochastic traceback through the Forward tables draws alignments from $P(\pi \mid x, y)$, which shows the region of good alignments, not only one (Durbin et al., Chapter 4).
- **Maximum expected accuracy.** For an alignment $\pi$, the expected number of match columns that are correct is $\sum_{(i, j) \in \pi} P(x_i \diamond y_j \mid x, y)$. Holmes and Durbin (1998) give the dynamic program that maximizes it. Such alignments can differ from the Viterbi path when the probability is spread over many paths.
- **Multiple alignment.** [ProbCons](/probcons/) (Do et al. 2005) computes pair-HMM posteriors for all pairs of sequences, makes them consistent through third sequences, and aligns by maximum expected accuracy.
- **Weak signals.** For distant sequences the best path can hold a small share of $P(x, y)$, as the 37 percent of the example above already shows for five bases. The Viterbi path is then a poor summary of the model's view, and the posteriors show which columns can be trusted.

## References
