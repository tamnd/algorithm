---
tag: YNZJ2F
kind: algorithm
slug: pwm-score-p-value
name: Weight matrix score p-value
aliases:
- PWM score distribution
- motif match p-value
area: biology/gene-finding-and-motifs
level: advanced
summary: Compute the exact distribution of a weight matrix score under a background model by dynamic programming over rounded scores.
model: floating-point-model
complexity:
  vars: {L: the number of columns, c: "the alphabet size, 4 for DNA", S: the largest number of partial scores kept after a column, r: the number of rounds, R: the largest entry minus the smallest entry of the matrix, h: the grid step of the last round}
  time: {worst: O(r L c S), per_round: O(L c S), grid_bound: O(L^2 c R / h)}
  space: {extra: O(S + L c)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [Hélène Touzet, Jean-Stéphane Varré]
  note: Staden (1989) gave methods for the probability of finding patterns in random sequences. Touzet and Varré (2007) rounded the matrix to a grid, bounded the error and refined the grid until the p-value is exact.
prereqs: [position-specific-scoring-matrix, p-value, convolution]
see_also: [motif-information-content, generating-functions, subset-sum-problem, pseudo-polynomial-time, counting-subset-sum, multiple-comparisons-problem, false-discovery-rate, np-hard]
sources:
  - paper: doi:10.1186/1748-7188-2-15
    title: Hélène Touzet and Jean-Stéphane Varré, Efficient and accurate P-value computation for Position Weight Matrices, Algorithms for Molecular Biology 2, article 15, 2007
    locator: the rounded matrix, the bound on the rounding error, the stopping rule, the cost of the dynamic programming and the NP-hardness by a reduction from SUBSET SUM
  - paper: doi:10.1093/bioinformatics/5.2.89
    title: Rodger Staden, Methods for calculating the probabilities of finding patterns in sequences, Computer Applications in the Biosciences 5(2), 1989
    locator: pp. 89 to 96, the probability of a pattern match in a random sequence
---

A position weight matrix gives a score to each word of length $L$, and a site is reported when the score reaches a threshold $\alpha$. The **p-value** of $\alpha$ is the chance that a random word from the background scores at least $\alpha$. For small $L$ you can list all $4^L$ words, but for a matrix of 20 columns this is $10^{12}$ words. The method of Touzet and Varré (2007) rounds the matrix entries down to a grid of step $\varepsilon$, computes the distribution of the rounded score by [convolution](/convolution/) one column at a time, and gets a lower and an upper bound on the p-value. When no rounded score is near the threshold, the two bounds are equal and the answer is exact; otherwise it makes the grid ten times finer and tries again.

## In plain words

The score of a word is a sum, one term per column. If each term can take only a few values, you can build the table of all possible sums and their chances, one column at a time, like adding dice. Real matrix entries are arbitrary numbers, so the table can grow to one entry per word.

So round every entry down to a multiple of a small step. Now the sums lie on a grid, and the table stays small. Rounding moves each score down by at most a known amount $E$. A word whose rounded score is at least $\alpha$ surely passes. A word whose rounded score is below $\alpha - E$ surely fails. Only the words in between are in doubt. If there are none, the answer is exact. If there are some, use a finer step.

## The problem

**Input.** A matrix $M$ with $L$ columns and one real entry $M_j(a)$ for each column $j$ and letter $a$, a background $p(a) \ge 0$ with $\sum_a p(a) = 1$, and a threshold $\alpha$. The score of a word $w = w_1 \cdots w_L$ is $S(w) = \sum_{j=1}^{L} M_j(w_j)$, and the letters of a random word are independent with probabilities $p$. Columns are numbered from 1 on this page and from 0 in the code.

**Output.** $P(\alpha) = \Pr[S(w) \ge \alpha]$, or bounds $\mathrm{lo} \le P(\alpha) \le \mathrm{hi}$ when a cap on the rounds is reached.

## The algorithm

For a grid step $\varepsilon > 0$, let $N_j(a) = \lfloor M_j(a)/\varepsilon \rfloor$, an integer, and let the rounded score be $S_\varepsilon(w) = \varepsilon \sum_j N_j(w_j)$. The largest rounding error is $E = \sum_j \max_a (M_j(a) - \varepsilon N_j(a))$, with the maximum over the letters with $p(a) > 0$. Then $S_\varepsilon(w) \le S(w) \le S_\varepsilon(w) + E$ for every word of positive probability.

```pseudo id=main
PWM-P-VALUE(M, p, α, ε0, rounds)
L1  ε ← ε0
L2  repeat
L3      N_j(a) ← ⌊M_j(a) / ε⌋ for every column j and letter a
L4      E ← Σ_j max_a (M_j(a) - ε N_j(a))
L5      A ← ⌈α / ε⌉
L6      B ← ⌈(α - E) / ε⌉
L7      (sure, middle) ← ROUND(N, p, A, B)
L8      lo ← sure
L9      hi ← sure + Σ_s middle[s]
L10     if middle is empty or this was the last allowed round then
L11         return lo, hi and whether middle is empty
L12     ε ← ε / 10
```

**ROUND** is the dynamic programming of line L7. It keeps a table $Q$ from integer partial scores to probabilities, starting with $Q = \{0 : 1\}$. For column $j$, each entry $(t, q)$ of $Q$ and each letter $a$, it forms $t' = t + N_j(a)$ with probability $q\,p(a)$. Let $\mathrm{best}_j$ and $\mathrm{worst}_j$ be the largest and the smallest sums of $N$ over the columns after $j$. If $t' + \mathrm{worst}_j \ge A$, every completion reaches $A$, so $q\,p(a)$ is added to `sure`. If $t' + \mathrm{best}_j < B$, no completion reaches $B$, and the mass is dropped. Otherwise it is added to the new table at $t'$. After the last column, the table holds exactly the rounded scores $s$ with $B \le s < A$, and `sure` is $\Pr[\sum_j N_j(w_j) \ge A]$.

Since $\varepsilon s \ge \alpha$ holds exactly when $s \ge A$ for an integer $s$, the lower bound is $\mathrm{lo} = \Pr[S_\varepsilon \ge \alpha] \le P(\alpha)$, and the upper bound is $\mathrm{hi} = \Pr[S_\varepsilon \ge \alpha - E] \ge P(\alpha)$. The code starts with $\varepsilon_0 = 0.1$, as in the paper, and stops after 8 rounds at most. It turns the matrix entries and the threshold into exact fractions, so the rounding and the bounds have no floating-point error; the probabilities are exact when $p$ is given as fractions.

## Example

**Two columns, integer entries.** Let $L = 2$ with the uniform background and

| | A | C | G | T |
|---|---|---|---|---|
| column 1 | 2 | -1 | -1 | 0 |
| column 2 | -1 | 3 | 0 | -1 |

The sums of one entry from each column give the distribution $\Pr[S = -2] = 1/4$, $\Pr[S = -1] = 1/4$, $\Pr[S = 0] = 1/16$, $\Pr[S = 1] = 1/8$, $\Pr[S = 2] = 3/16$, $\Pr[S = 3] = 1/16$ and $\Pr[S = 5] = 1/16$. For $\alpha = 3$, $P(3) = 1/16 + 1/16 = 1/8$, from the words AC (score 5) and TC (score 3). The entries lie on the grid of step 0.1, so $E = 0$, $A = B = 30$, the middle table is empty, and the first round returns $1/8$ as exact.

**A log-odds matrix.** Take the five sites TCTCGGGG, CCAAGGTG, TACAGGCG, TTCAGGTG and TCCACGTG, the answer of the Rosalind BA2F sample, and form $M_j(a) = \log_2(f_j(a)/0.25)$ with $f_j(a) = (\text{count} + 0.25)/6$. The entries take only the values $\log_2(21/6) = 1.807$, $\log_2(17/6) = 1.503$, $\log_2(13/6) = 1.115$, $\log_2(5/6) = -0.263$ and $\log_2(1/6) = -2.585$, for counts 5, 4, 3, 1 and 0. The best score is 11.469, from TCCAGGTG. With the uniform background and $\alpha = 6$:

| round | $\varepsilon$ | $E$ | lo $\cdot 4^8$ | hi $\cdot 4^8$ | exact |
|---|---|---|---|---|---|
| 1 | 0.1 | 0.251869 | 133 | 178 | no |
| 2 | 0.01 | 0.056503 | 133 | 178 | no |
| 3 | 0.001 | 0.006503 | 133 | 178 | no |
| 4 | 0.0001 | 0.000538 | 178 | 178 | yes |

So $P(6) = 178/65536 \approx 0.00272$, which a count of all 65,536 words confirms. The cause of the slow rounds is that 45 words, such as AACAGGTG, score 6.00267, just above the threshold. Their rounded score falls below 6 until the rounding error is under 0.00267, in round 4. For $\alpha = 4$ and $\alpha = 8$, two rounds give the exact values $586/65536$ and $40/65536$.

## Correctness

**Theorem.** In every round, $\mathrm{lo} \le P(\alpha) \le \mathrm{hi}$. If the middle table is empty, $\mathrm{lo} = P(\alpha) = \mathrm{hi}$.

*Proof sketch.* Each entry is rounded down by less than $\varepsilon$, so $S_\varepsilon(w) \le S(w) \le S_\varepsilon(w) + E$. A word with $S_\varepsilon(w) \ge \alpha$ has $S(w) \ge \alpha$, so $\mathrm{lo} \le P(\alpha)$. A word with $S(w) \ge \alpha$ has $S_\varepsilon(w) \ge \alpha - E$, so $P(\alpha) \le \mathrm{hi}$. ROUND sends each word of positive probability to exactly one of `sure`, the dropped mass and the final table, and only words with $B \le \sum N < A$ reach the table, so `sure` and the table give $\mathrm{lo}$ and $\mathrm{hi} - \mathrm{lo}$. If the table is empty, every word is either surely at least $\alpha$ or surely below $\alpha - E \le \alpha$, so $\mathrm{lo} = \mathrm{hi}$. $\square$

The loop stops after a finite number of rounds when no word of positive probability scores exactly $\alpha$: once $L\varepsilon$ is below the distance from $\alpha$ to the nearest score, no rounded score can be in $[\alpha - E, \alpha)$. A word that scores exactly $\alpha$ with an entry off every grid keeps the bracket open, which is why the code has a cap on the rounds. The full proof, with the invariant of ROUND, is in proofs/correctness.md. The tests compare the results with a count over all words for up to 5 columns, check the bracket in every round, check ROUND against the full distribution, and check the BA2F values above.

## Complexity

- **One round.** ROUND does $c$ updates for each kept partial score of each column, so $O(L c S)$ time, where $S$ is the largest table. The table never holds more than $c^j$ entries after $j$ columns.
- **The grid bound.** All partial scores after $j$ columns lie in an integer range of width at most $jR/\varepsilon + j$, so $S = O(LR/\varepsilon)$ and a round costs $O(L^2 c R/\varepsilon)$. This is pseudo-polynomial: it grows with $1/\varepsilon$, not with $\log(1/\varepsilon)$.
- **All rounds.** Each round makes $\varepsilon$ ten times smaller, so the grid bound of the last round dominates the sum, and $r$ rounds cost $O(r L c S)$ at most.
- **Pruning.** Partial scores that are sure to pass or sure to fail leave the table. For thresholds in the far tail, where p-values are small, most partial scores are dropped early.
- **Hardness.** Touzet and Varré show by a reduction from the [subset sum problem](/subset-sum-problem/) that the exact p-value is NP-hard to compute when the entries are given as arbitrary numbers. So no method is polynomial in $L$ and in the number of digits of the entries unless P = NP.

## Properties

- **Exact when it stops.** An empty middle table proves the answer. With the cap reached, the result is a proven bracket.
- **Floating-point free bounds.** The code rounds exact fractions, so the bracket holds for the matrix as given, not for a nearby one.
- **The lower bound never falls.** Each grid divides the previous one, so a finer grid rounds each entry down by less, and $\mathrm{lo}$ cannot go down from one round to the next. The upper bound has no such guarantee.
- **Any background of independent letters.** The background enters only as the factor $p(a)$ in ROUND.
- **The same table gives all thresholds.** Without the pruning, the final table is the whole distribution of the rounded score, so a run can answer many thresholds at once.

## Variants and improvements

- **The full distribution.** Drop the pruning and keep all partial scores. This is the [generating function](/generating-functions/) $\prod_j \sum_a p(a) x^{N_j(a)}$, and the code has it as `score_distribution`.
- **The threshold for a p-value.** The inverse problem asks for the smallest threshold whose p-value is at most a given level. The full rounded distribution answers it by a scan from the top, with the same bracket on the result.
- **Markov backgrounds.** A background of order $k$ needs the last $k$ letters in the state of the table, which multiplies the size by $c^k$.
- **One fixed grid.** A simpler method scales the matrix to integers once and accepts the rounding error. The bound $E$ of this page tells how large that error can be.

## When to use it

Use it to turn matrix scores into p-values when you scan sequences for sites, so that thresholds mean the same for matrices of different lengths and contents. A p-value of a single window does not account for the number of windows scanned; correct for the [multiple comparisons](/multiple-comparisons-problem/), for example with the [false discovery rate](/false-discovery-rate/). For a fixed matrix and many thresholds, compute the distribution once. To judge the quality of a matrix itself, look at its [information content](/motif-information-content/).

## Pitfalls

- **A threshold equal to a score.** If some word scores exactly $\alpha$ and its entries are not on any grid of step $10^{-r}$, the bracket never closes. Cap the rounds, or move $\alpha$ by a small amount.
- **Rounding in floating point.** Computing $\lfloor M/\varepsilon \rfloor$ and $E$ in floating point can break the bound $S_\varepsilon \le S \le S_\varepsilon + E$ by a rounding error. The code uses exact fractions for this reason.
- **Letters with zero probability.** Take the maximum error over the letters that can occur, or $E$ is larger than it needs to be.
- **Rounding to the nearest point.** Rounding to the nearest grid point, not down, gives errors of both signs, and then the bracket needs the error in each direction.

## Implementations

## History

Staden (1989) gave methods for the probability of finding a pattern in a random sequence. Touzet and Varré (2007) rounded the weight matrix to a grid, bounded the error of the rounded matrix, used the bound to decide when the rounded answer is exact, refined the grid when it is not, and showed that the general problem is NP-hard.

## References
