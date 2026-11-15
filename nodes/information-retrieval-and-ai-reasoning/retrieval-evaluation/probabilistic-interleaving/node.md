---
tag: 5WYWSE
kind: algorithm
slug: probabilistic-interleaving
name: Probabilistic interleaving
aliases:
- Hofmann probabilistic interleave
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: research
summary: Draws each shown document from a softmax over a ranking picked by a fair coin, then credits clicks by the exact posterior of which ranking drew each document.
model: word-ram
complexity:
  vars: {n: the number of documents in each ranking, c: the number of clicks}
  time: {worst: O(n^2)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [team-draft-interleaving, conditional-expectation]
see_also: [interleaved-evaluation, balanced-interleaving, roulette-wheel-selection, importance-sampling, off-policy-evaluation, click-model, position-bias, sign-test]
sources:
  - paper: doi:10.1145/2063576.2063618
    title: Katja Hofmann, Shimon Whiteson and Maarten de Rijke, A probabilistic method for inferring preferences from clicks, CIKM 2011, pp. 249-258
    locator: the probabilistic interleave method with the softmax of rank to the power minus tau, tau = 3, the marginalized comparison and its example in Figure 5; Sections 3.1 and 3.2 for the faults of balanced and team-draft interleaving
---

Probabilistic interleaving is an [interleaved evaluation](/interleaved-evaluation/) method that builds the shown list at random from both rankings. For each position a fair coin picks one of the two rankings, and a document that is not yet shown is drawn from a softmax over that ranking, which gives the top documents most of the weight but every document some weight. Hofmann, Whiteson and de Rijke introduced it in 2011 to fix two faults of the older methods: [balanced interleaving](/balanced-interleaving/) is biased when the rankings are close, and [team-draft interleaving](/team-draft-interleaving/) can miss a real difference. Because every document can reach every position, the clicks can be credited not only by the coin results that were drawn but by their exact posterior given the shown list, which removes noise and keeps the outcome unbiased.

## In plain words

Two search engines each give their result list. To fill each slot of the page, flip a coin to pick an engine, then let that engine pick a result that is not yet on the page. The engine does not always take its best result: it takes its first one most of the time, its second one less often, and so on.

After the user clicks, give each click to the engine that most likely filled that slot. For each slot you can work out how likely each engine was to put that result there, given the page as a whole. The engine with more expected clicks wins. A wrong guess about who filled a slot cannot make a winner from a loser on average, and the guess is less noisy than the coin that was really flipped.

## The problem

The input is two rankings $A$ and $B$ of the same $n$ documents for one query, a parameter $\tau > 0$, and a source of random numbers. Let $r_1(d)$ and $r_2(d)$ be the ranks of document $d$ in $A$ and $B$, from 1. The method shows a list $L$, an ordering of the documents, and keeps an assignment $a \in \{1, 2\}^n$ that says which ranking drew each position. After the user clicks the set $C$ of positions of $L$, the output is a preference in $[-1, 1]$, where a positive value means that $A$ is preferred. Over many queries, a [sign test](/sign-test/) on the signs of the preferences, or a mean, decides if one ranking wins more often than chance.

## The algorithm

```pseudo id=main
PROBABILISTIC-INTERLEAVE(A, B, τ)
L1  w_x(d) ← 1 / r_x(d)^τ for x ∈ {1, 2} and every document d
L2  R ← the documents of A, L ← empty list, a ← empty list
L3  while R ≠ ∅ do
L4      x ← 1 or 2, each with probability 1/2
L5      draw d from R with probability w_x(d) / Σ_{e ∈ R} w_x(e), remove d from R
L6      append d to L, append x to a
L7  return L, a

OUTCOME(a, C)                              ▷ C: the clicked positions of L
L8  c1 ← |{r ∈ C : a_r = 1}|, c2 ← |{r ∈ C : a_r = 2}|
L9  return 1 if c1 > c2, -1 if c1 < c2, else 0

MARGINAL(A, B, L, C, τ)
L10 for r ← 1 to n: f_x ← w_x(L_r) / Σ_{s ≥ r} w_x(L_s) for x ∈ {1, 2}, q_r ← f_1 / (f_1 + f_2)
L11 P ← the table {0: 1}
L12 for each r ∈ C: P'[k + 1] ← P'[k + 1] + q_r P[k] and P'[k - 1] ← P'[k - 1] + (1 - q_r) P[k] for each k, then P ← P'
L13 return Σ_{k > 0} P[k] - Σ_{k < 0} P[k]
```

Lines L1 to L7 are the sampler of Hofmann, Whiteson and de Rijke, who use $\tau = 3$. Line L5 is a [roulette wheel](/roulette-wheel-selection/) draw over the documents that are left, so the softmax is taken again over a smaller set at each position. OUTCOME is the plain credit by the assignment that was drawn. MARGINAL is the credit that the paper prefers: the expected value of OUTCOME over all assignments $a$, weighted by their probability given the shown list $L$.

The paper writes this marginal as a sum over assignments. The sum does not need $2^n$ terms. Given $L$, the probability of a pair $(L, a)$ is a product of one factor $f_{a_r}(r)/2$ per position, where the denominator of $f_x(r)$ is the weight of the documents at positions $r$ to $n$ and depends only on $L$. So given $L$, the components of $a$ are independent, and position $r$ came from $A$ with probability $q_r$ (line L10). The outcome depends only on the sign of the sum of $\pm 1$ over the clicked positions, and lines L11 to L13 compute the distribution of that sum with a [dynamic program](/dynamic-programming/).

## Example

This is the example of Figure 5 of Hofmann, Whiteson and de Rijke, with $\tau = 3$. Let $A = (d_1, d_2, d_3, d_4)$ and $B = (d_2, d_3, d_4, d_1)$. The softmax of $A$ over all four documents is $0.849, 0.106, 0.031, 0.013$. Suppose the sampler shows $L = (d_1, d_2, d_3, d_4)$, which has probability $0.2487$, and the user clicks positions 2 and 3. Line L10 gives:

| position | document | $w_1$ | weight of $A$ left | $f_1$ | $w_2$ | weight of $B$ left | $f_2$ | $q_r$ |
|---|---|---|---|---|---|---|---|---|
| 1 | $d_1$ | 1 | 1.1777 | 0.8491 | 0.0156 | 1.1777 | 0.0133 | 0.9846 |
| 2 | $d_2$ | 0.125 | 0.1777 | 0.7036 | 1 | 1.1620 | 0.8606 | 0.4498 |
| 3 | $d_3$ | 0.0370 | 0.0527 | 0.7033 | 0.125 | 0.1620 | 0.7714 | 0.4769 |
| 4 | $d_4$ | 0.0156 | 0.0156 | 1 | 0.0370 | 0.0370 | 1 | 0.5 |

Only positions 2 and 3 are clicked. $A$ gets both clicks with probability $q_2 q_3 = 0.2145$, $B$ gets both with probability $(1 - q_2)(1 - q_3) = 0.2878$, and the clicks split one and one with probability $0.4977$, a tie. MARGINAL returns $0.2145 - 0.2878 = -0.0733$, a small preference for $B$, which ranks the two clicked documents higher. In the figure of the paper the two win probabilities are half of these values; the sign and the ratio are the same.

The sampled assignment would give $1$, $-1$ or $0$ for this page, depending on two coins and two draws that the user cannot see. MARGINAL replaces that random value by its mean given what the user saw.

## Correctness

The proof is in `proofs/correctness.md`. Lines L1 to L7 return an ordering $L$ and an assignment $a$ with $\Pr[L, a] = 2^{-n} \prod_r f_{a_r}(r)$. Summing over $a$ gives $\Pr[L] = 2^{-n} \prod_r (f_1(r) + f_2(r)) > 0$, so the posterior of $a$ given $L$ is a product of independent Bernoulli terms with parameters $q_r$. The table of lines L11 and L12 is the exact distribution of the difference of credited clicks over the clicked positions seen so far, so MARGINAL returns $\mathbb{E}[\mathrm{OUTCOME}(a, C) \mid L, C]$. When the clicks depend on the shown page but not on $a$, which the user cannot see, the tower rule of [conditional expectation](/conditional-expectation/) gives $\mathbb{E}[\mathrm{MARGINAL}] = \mathbb{E}[\mathrm{OUTCOME}]$: the marginalized outcome is unbiased for the expected outcome of the method, and its variance is no larger. The tests check this equality exactly, with fractions, over all pairs of rankings of at most 3 documents and all relevance labels.

## Complexity

- **Time.** The sampler makes $n$ draws, and each scans the documents that are left, so it takes $O(n^2)$ time. A balanced tree of partial sums would make each draw $O(\log n)$. Line L10 takes $O(n)$ time with suffix sums. After $j$ clicks the table has at most $j + 1$ keys, so lines L11 to L13 take $O(c^2)$ time for $c$ clicks, and MARGINAL takes $O(n + c^2)$ in total.
- **Space.** The weights, $L$, $a$ and the suffix sums take $O(n)$ space, and the table takes $O(c)$.
- **Random numbers.** Two per position: one coin and one draw.

## Properties

- **Every page is possible.** All weights are positive, so every ordering of the documents is shown with positive probability. This is what makes the posterior defined for every page, and it is also the cost of the method: users sometimes see a poor ordering.
- **Fair under random clicks.** Each coin of line L4 is fair and independent of the earlier draws, so the assignment is uniform over $\{1, 2\}^n$. Swapping 1 and 2 at every position negates the outcome, so clicks that depend only on positions give an expected outcome of 0, with OUTCOME and with MARGINAL. The tests check this exactly for all pairs of rankings of at most 3 documents and one pair of 4.
- **Unbiased marginal.** The marginalized outcome has the same expected value as the sampled one for every click model that does not see the assignment.
- **A dominating ranking wins here.** Call $A$ dominant over $B$ if, at every depth, the top of $A$ holds at least as many relevant documents as the top of $B$, and more at some depth. Let the user click position $i$ with probability $1/i$ for a relevant document, and $1/(5i)$ or 0 for a document that is not relevant. For all pairs of rankings of at most 4 documents, the expected outcome is then strictly positive when $A$ dominates $B$. With $A = (d_2, d_3, d_1)$, $B = (d_1, d_2, d_3)$ and only $d_3$ relevant, where team draft gives a tie, it is $0.1138$. With $A = (b, c, a, d)$, $B = (c, a, d, b)$ and only $a$ not relevant, where balanced interleaving prefers $B$, it is $0.0620$. The sources give no proof of this for longer lists or other click models.

## Variants and improvements

- **Credit by the sampled assignment.** Return OUTCOME instead of MARGINAL. It has the same expected value and needs no posterior, but it is noisier, so more queries are needed for the same confidence.
- **The softmax parameter.** A large $\tau$ puts almost all the weight on the top document of each ranking, and the shown list comes close to a team-draft list, with its blind spots and with posteriors near 0 or 1. A small $\tau$ shows more varied pages and gives more information per click, but the pages are worse for the user.
- **Reuse of logged clicks.** Since every page has a known, positive probability under any pair of rankings, clicks logged while comparing one pair can be reweighted by the ratio of the probabilities of the shown page, as in [importance sampling](/importance-sampling/), to estimate a comparison of another pair. Hofmann, Whiteson and de Rijke continued this line in later work on interleaving with historical data.
- **More than two rankings.** The same sampler works with one softmax per ranker and a fair die in line L4, which gives a probabilistic form of multileaved comparison.

## When to use it

Use probabilistic interleaving when the rankers to compare are close, so that team draft often gives ties, or when you want to reuse logged clicks for comparisons that were not run live. It needs the full rankings of both rankers at serving time and shows more varied pages than team draft, so it costs some user experience. For a plain A/B choice between two rankers that differ clearly, team draft is simpler and shows better pages.

## Pitfalls

- **Drawing from the full ranking.** Line L5 must take the softmax over the documents that are left. If it draws from the full softmax and redraws on a repeat, the draw has the same distribution, but if it takes the next document of the ranking after a repeat, the probability of the page is no longer the product of line L10 and the posterior is wrong.
- **The wrong denominator in line L10.** The denominator of $f_x$ is the weight of the documents at positions $r$ to $n$ of $L$. Using the weight of all documents, as for position 1, gives posteriors that do not match the sampler, and the marginal is then biased.
- **A different $\tau$ at serving and at credit time.** Lines L1 and L10 must use the same $\tau$ and the same rankings. If the ranker changes between serving and credit, the posterior belongs to another sampler.
- **Using clicks that see the assignment.** The unbiased property needs clicks that depend only on the page. If the page shows which ranker filled a slot, for example by a different style of snippet, the clicks are no longer independent of $a$ given $L$.
- **Summing over all assignments.** Code that enumerates $\{1, 2\}^n$ to compute the marginal is correct but takes $2^n$ steps. Use the factorized posterior and the dynamic program of lines L10 to L13.

## Implementations

## History

Hofmann, Whiteson and de Rijke presented probabilistic interleaving at CIKM 2011. They showed that balanced interleaving can prefer a ranker under random clicks, and that team draft can fail to see a ranker that places the only relevant document higher. Their method draws the page from softmax functions of the ranks, and they argued that it is fair under random clicks and that it detects such differences. They also introduced the marginalized comparison, which credits clicks by the posterior over assignments, and compared it with the older methods in experiments with simulated clicks. As for every interleaving method, the agreement of its outcomes with offline metrics is a measured property, not a proved one. Later work by the same authors used the known page probabilities to reuse logged clicks for new comparisons.

## References
