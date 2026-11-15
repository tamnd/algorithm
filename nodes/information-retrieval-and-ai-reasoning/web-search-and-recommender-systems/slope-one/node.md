---
tag: 2RYX1J
kind: algorithm
slug: slope-one
name: Slope One
aliases:
- weighted Slope One
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Predicts a rating from the average rating difference between each pair of items, a simple scheme that updates online.
solves: [recommendation-problem]
model: word-ram
complexity:
  vars: {n: the number of items, s: the number of known ratings, d: the number of items rated by the user}
  time: {worst: O(d)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2005
  people: [Daniel Lemire, Anna Maclachlan]
  note: Lemire and Maclachlan (SIAM Data Mining 2005) proposed Slope One, Weighted Slope One and Bi-Polar Slope One as predictors that are easy to build, update online and explain.
prereqs: [rating-matrix, collaborative-filtering, item-based-collaborative-filtering]
see_also: [user-based-collaborative-filtering, matrix-factorization-recommendation, linear-regression, cold-start-problem]
sources:
  - paper: doi:10.1137/1.9781611972757.43
    title: Daniel Lemire and Anna Maclachlan, Slope One predictors for online rating-based collaborative filtering, Proceedings of the 2005 SIAM International Conference on Data Mining (SDM 2005), 471-475
    locator: Section 3.4 (the Slope One scheme, the average deviation of two items and its least squares derivation), Section 3.5 (Weighted Slope One), Section 3.6 (Bi-Polar Slope One), Section 4 and Table 1 (All But One mean absolute error on EachMovie and MovieLens)
  - url: https://arxiv.org/abs/cs/0702144
    title: Daniel Lemire and Anna Maclachlan, Slope One predictors for online rating-based collaborative filtering, arXiv preprint cs/0702144
    locator: the same paper; Section 3.2 (the baselines Per User Average and Bias From Mean) and Section 3.3 (the Pearson reference scheme)
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 2 (neighborhood-based collaborative filtering and its item-based forms)
---

Slope One predicts the rating of a user $u$ for an item $j$ from the average difference between the ratings of $j$ and of each other item $i$, taken over the users who rated both: each item $i$ that $u$ rated gives the guess $r_{ui} + \operatorname{dev}(j, i)$, and the prediction is the mean of these guesses, or in Weighted Slope One their mean weighted by the number of users behind each difference. Lemire and Maclachlan published it in 2005. Like [item-based collaborative filtering](/item-based-collaborative-filtering/) it works on pairs of items, but it stores a fitted offset in place of a similarity, so it needs no similarity measure and no neighborhood size, and a new rating updates the model in time linear in the number of items its user rated.

## In plain words

Suppose that people who saw two films rated the second one, on average, half a point higher than the first. If you gave the first film a 3, a fair guess for the second is 3.5. Each film that you rated gives one such guess for the target film. Slope One takes the average of all these guesses.

Some guesses rest on many people and some on only one or two. The weighted version gives each guess a weight equal to the number of people behind its average difference, so guesses from well-known pairs count more.

The model is a table of sums and counts, one entry for each pair of films. A new rating only adds to the entries of the pairs it forms with the other films of its user.

## The problem

The input is a set $K$ of known ratings over $m$ users and $n$ items, and a pair $(u, j)$ to predict. Let $I_u$ be the set of items that $u$ rated. For items $j \ne i$, let $S(j, i)$ be the set of users who rated both, $c(j, i) = |S(j, i)|$, and, when $c(j, i) > 0,$

$$\operatorname{dev}(j, i) = \frac{1}{c(j, i)} \sum_{w \in S(j, i)} (r_{wj} - r_{wi}).$$

Let $R_j = \{ i \in I_u : i \ne j,\ c(j, i) > 0 \}$. Slope One and Weighted Slope One predict

$$\hat r_{uj} = \frac{1}{|R_j|} \sum_{i \in R_j} \bigl(\operatorname{dev}(j, i) + r_{ui}\bigr), \qquad \hat r^{\,w}_{uj} = \frac{\sum_{i \in R_j} \bigl(\operatorname{dev}(j, i) + r_{ui}\bigr)\, c(j, i)}{\sum_{i \in R_j} c(j, i)}.$$

When $R_j$ is empty, the paper gives no rule; this page returns the mean of $u$, or the mean of all ratings if $u$ has none. The name comes from the predictor $f(x) = x + b$ of the rating of $j$ from the rating of $i$: a line of slope one. For the pairs $(r_{wi}, r_{wj})$ with $w \in S(j, i)$, the offset $b$ that minimizes $\sum_w (r_{wi} + b - r_{wj})^2$ is $\operatorname{dev}(j, i)$ (Lemire and Maclachlan, Section 3.4; proof in `proofs/correctness.md`). It is [linear regression](/linear-regression/) with the slope fixed to 1.

## The algorithm

The model is two tables over ordered pairs of items, $\mathit{diff}(j, i) = \sum_{w \in S(j, i)} (r_{wj} - r_{wi})$ and $\mathit{count}(j, i) = c(j, i)$, plus the ratings of each user.

```pseudo id=main
ADD(u, i, v)                                   ▷ the new rating r_ui = v
L1  if u already rated i then REMOVE(u, i)
L2  for each item j that u rated do
L3      diff(i, j) ← diff(i, j) + (v - r_uj); diff(j, i) ← diff(j, i) + (r_uj - v)
L4      count(i, j) ← count(i, j) + 1; count(j, i) ← count(j, i) + 1
L5  store r_ui ← v

PREDICT(u, j, weighted)
L6  R ← the items i ≠ j that u rated with count(j, i) > 0
L7  if R is empty then return the mean of u (the global mean if u has no rating)
L8  for each i in R do g_i ← diff(j, i) / count(j, i) + r_ui; c_i ← count(j, i) if weighted, else 1
L9  return Σ_{i ∈ R} c_i g_i / Σ_{i ∈ R} c_i
```

REMOVE$(u, i)$ deletes the stored rating $v = r_{ui}$ and runs lines L2 to L4 with the signs reversed; an entry whose count reaches 0 is deleted. A batch build is a call of ADD for each rating.

## Example

The toy rating matrix of this group:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 |
| $u_2$ | 4 | 5 | 4 | 2 |
| $u_3$ | 1 | 2 | 2 | 5 |
| $u_4$ | - | 1 | 1 | 4 |

Predict $r_{u_1 i_3}$. User $u_1$ rated $i_1$, $i_2$ and $i_4$.

| $i$ | users in $S(i_3, i)$ | differences $r_{w i_3} - r_{w i}$ | $c$ | $\operatorname{dev}(i_3, i)$ | guess $\operatorname{dev} + r_{u_1 i}$ |
|---|---|---|---|---|---|
| $i_1$ | $u_2, u_3$ | 0, 1 | 2 | 1/2 | 11/2 |
| $i_2$ | $u_2, u_3, u_4$ | $-1$, 0, 0 | 3 | $-1/3$ | 11/3 |
| $i_4$ | $u_2, u_3, u_4$ | 2, $-3$, $-3$ | 3 | $-4/3$ | $-1/3$ |

Slope One gives $(11/2 + 11/3 - 1/3) / 3 = 53/18 \approx 2.944$. Weighted Slope One gives $(2 \cdot 11/2 + 3 \cdot 11/3 - 3 \cdot 1/3) / 8 = 21/8 = 2.625$. The guess from $i_4$ is below the scale: users rate $i_3$ and $i_4$ in opposite ways, and an offset cannot express that the two ratings move in opposite directions. On the same matrix, [user-based collaborative filtering](/user-based-collaborative-filtering/) predicts 3.934, because a negative correlation can turn a low rating into evidence for a high one.

An online step: if $u_1$ now rates $i_3$ with 4, line L3 adds $4 - 5$, $4 - 4$ and $4 - 1$ to $\mathit{diff}(i_3, i_1)$, $\mathit{diff}(i_3, i_2)$ and $\mathit{diff}(i_3, i_4)$, and the opposite values to the reverse entries, and line L4 adds 1 to the six counts. Nothing else changes.

## Correctness

The proof in `proofs/correctness.md` shows three facts. First, $\operatorname{dev}(j, i)$ is the least squares offset of the line of slope one, and $\operatorname{dev}(j, i) = -\operatorname{dev}(i, j)$. Second, by induction over any sequence of ADD and REMOVE calls, the tables hold $\mathit{diff}(j, i) = \sum_{w \in S(j, i)} (r_{wj} - r_{wi})$ and $\mathit{count}(j, i) = c(j, i)$ for the current ratings, so the result does not depend on the order in which the ratings arrived. Third, PREDICT returns the two formulas, and Weighted Slope One equals the plain mean of the votes $r_{ui} + r_{wj} - r_{wi}$ over all pairs $(i, w)$ with $i \in R_j$ and $w \in S(j, i)$.

## Complexity

The model is the word RAM with hash tables, so each table access costs $O(1)$ expected time. Let $d = |I_u|$ be the number of items rated by the user of the call.

- **ADD and REMOVE.** Lines L2 to L4 do $O(1)$ work for each item that $u$ rated: $O(d)$.
- **PREDICT.** Lines L6 to L9 do $O(1)$ work for each item that $u$ rated: $O(d)$, independent of the number of users.
- **Batch build.** The ratings of user $u$ touch each ordered pair of items of $I_u$ once, so the build costs $O(\sum_u |I_u|^2)$, at most $O(n s)$.
- **Space.** At most $n(n - 1)$ ordered pairs, $O(n^2)$. Since $\mathit{diff}(i, j) = -\mathit{diff}(j, i)$ and the counts are symmetric, half of the entries are enough, $n(n-1)/2$ pairs. Only pairs with a common user are stored, so on sparse data the table is often much smaller.

## Properties

- **Online.** A new rating, a changed rating and a deleted rating cost $O(d)$ each, and the model after any sequence of updates is the same as the one built from scratch.
- **No parameters.** There is no similarity measure, neighborhood size, learning rate or penalty to choose.
- **Additive.** Adding a constant to all ratings of one user does not change any $\operatorname{dev}$, and shifts that user's predictions by the same constant, because each guess is $r_{ui}$ plus a difference.
- **Dense case.** If every item $i \in I_u$ has $c(j, i) > 0$ and $j \notin I_u$, then $R_j = I_u$ and Slope One equals $\mu_u + \frac{1}{|I_u|} \sum_{i \in I_u} \operatorname{dev}(j, i)$. The paper uses this form as an approximation when most pairs have common users.
- **Blind to the sign of the relation.** All lines have slope one. Two items that users rate in opposite ways give a large offset of the wrong kind, as for $i_4$ in the example.

## Variants and improvements

- **Weighted Slope One.** The weights $c(j, i)$ of the problem section (Section 3.5 of the paper).
- **Bi-Polar Slope One.** Section 3.6 splits the items of each user into those rated above and below the user's mean, and computes the differences separately on the liked and on the disliked items, so that a pair is used only when the user's opinion of the two items agrees in kind.
- **Baselines of the paper.** PER USER AVERAGE predicts $\mu_u$. BIAS FROM MEAN predicts $\mu_u$ plus the average over the users of item $j$ of their rating of $j$ minus their mean (Section 3.2). Slope One adds the pairwise item offsets to this idea.
- **Distributed update.** The tables are sums, so partial tables from parts of the data add up to the full table.

## When to use it

Use it when the model must take new ratings at once, when the system must be easy to build, check and explain ("users who rated this item rated the other one half a point higher"), and when tuning is not possible. The Table 1 of Lemire and Maclachlan reports All But One mean absolute errors, measured on EachMovie and MovieLens with the MovieLens values divided by 4: on EachMovie 0.194 for Bi-Polar, 0.198 for Weighted and 0.200 for plain Slope One, against 0.194 for their Pearson scheme and 0.203 for BIAS FROM MEAN; on MovieLens 0.188 for all three Slope One schemes and 0.190 for Pearson. These are measurements on two data sets, not guarantees. For the best accuracy on large data, factor models such as [matrix factorization](/matrix-factorization-recommendation/) are the usual choice.

## Pitfalls

- **Float drift under updates.** REMOVE subtracts in floating point, so after many updates $\mathit{diff}$ can differ from the exact sum by rounding. With integer ratings, keep the sums as integers.
- **Updating only one direction.** Lines L3 and L4 must update both $(i, j)$ and $(j, i)$, or keep one triangle and read the other with a minus sign. Mixing the two conventions doubles or cancels the offsets.
- **Including the target item.** If $u$ already rated $j$, the pair $(j, j)$ must not enter $R_j$; the test $i \ne j$ in line L6 does this.
- **Empty $R_j$.** A user whose items share no rater with $j$ gets no Slope One prediction. Return a fallback, such as the mean of $u$, and do not divide by zero.
- **Opposite items.** As in the example, a strongly opposite pair gives guesses outside the scale. Clip the result, or use Bi-Polar Slope One.

## Implementations

## History

Lemire and Maclachlan presented Slope One at the SIAM International Conference on Data Mining in 2005, with the aim of predictors that are easy to implement, update on the fly and explain, and that are accurate with little data from a new user. They compared the three schemes with PER USER AVERAGE, BIAS FROM MEAN, adjusted cosine item-based filtering and a Pearson scheme, on EachMovie and MovieLens. The paper reports that the Weighted scheme was used by the music site inDiscover.net in November 2004.

## References
