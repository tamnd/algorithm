---
title: Each part of the Viola-Jones detector computes what it claims, from the corner sums of the features to the optimal stump, the AdaBoost reweighting, the early exit of the cascade and the grouping of detections
proves: [correctness]
status: full
---

No theorem says that a trained cascade finds faces. That is an empirical property of the training data and the cascade. What can be proved is that each line of DETECT and TRAIN-STAGE computes the quantity it is meant to compute.

Let $S(x, y) = \sum_{j < y} \sum_{i < x} I(i, j)$ for $0 \le x \le W$ and $0 \le y \le H$, the integral image of line L1. Let $\mathrm{sum}(x_0, y_0, x_1, y_1)$ be the sum of $I$ over the half-open box $[x_0, x_1) \times [y_0, y_1)$.

**Lemma 1 (rectangle sums).** $\mathrm{sum}(x_0, y_0, x_1, y_1) = S(x_1, y_1) - S(x_0, y_1) - S(x_1, y_0) + S(x_0, y_0)$.

*Proof.* $S(x_1, y_1)$ counts the pixels with $i < x_1$ and $j < y_1$. Subtracting $S(x_0, y_1)$ removes those with $i < x_0$, and subtracting $S(x_1, y_0)$ removes those with $j < y_0$. The pixels with $i < x_0$ and $j < y_0$ are removed twice, and adding $S(x_0, y_0)$ puts them back once. $\square$

**Lemma 2 (feature values).** Let a feature have cells $c_1, \ldots, c_k$ with weights $\omega_1, \ldots, \omega_k \in \{1, -1\}$. Collect the four corner terms of Lemma 1 for each cell into one coefficient per corner point, and drop the points whose coefficient is $0$. Then $\sum_{\text{points}} \text{coefficient} \cdot S(\text{point}) = \sum_i \omega_i \, \mathrm{sum}(c_i)$. The number of points that remain is $6$ for the two-rectangle features, $8$ for the three-rectangle features and $9$ for the four-rectangle feature.

*Proof.* The first claim is Lemma 1 for each cell, multiplied by $\omega_i$ and summed, with the terms regrouped; a point with coefficient $0$ adds nothing. For the count, the corner points lie on a grid of $a + 1$ columns and $b + 1$ rows for a pattern of $a \times b$ cells, so there are $(a + 1)(b + 1)$ candidates: $6$, $8$ and $9$. Each candidate keeps a nonzero coefficient. An outer corner belongs to one cell and gets $\pm 1$. For two cells side by side with weights $+1$ and $-1$, a shared corner gets $+1$ from the right edge of the first cell and $(-1)(-1) = +1$ from the left edge of the second, so $\pm 2$. In the three-rectangle pattern with weights $-1, +1, -1$, a shared corner gets $\pm 2$ in the same way. In the four-rectangle pattern the center point gets $+1$ from each of the four cells, so $4$, and the edge midpoints get $\pm 2$. $\square$

The implementation computes the coefficients in `corner_refs`, and the tests compare every feature of a small window with a direct sum over the pixels and check the counts $6$, $8$, $9$.

**Lemma 3 (scaled features fit).** For $s \ge 1$ and a feature with cells of $w \times h$ pixels at $(x, y)$ inside an $n \times n$ window, the scaled feature with corner $(\lfloor xs \rfloor, \lfloor ys \rfloor)$ and cells of $\lfloor ws \rfloor \times \lfloor hs \rfloor$ pixels lies inside the window of size $\lfloor ns \rfloor$, and its cells are not empty.

*Proof.* $w \ge 1$ and $s \ge 1$ give $\lfloor ws \rfloor \ge 1$. Along $x$ the pattern has $a$ cells and $x + aw \le n$. Since $\lfloor u \rfloor + \lfloor v \rfloor \le \lfloor u + v \rfloor$, $\lfloor xs \rfloor + a \lfloor ws \rfloor \le \lfloor (x + aw) s \rfloor \le \lfloor ns \rfloor$. The same holds along $y$. $\square$

**Lemma 4 (deviation of the window).** Let $S_1$ and $S_2$ be the integral images of $I$ and $I^2$, and let a window have $a$ pixels with values $v_1, \ldots, v_a$. With $t_1$ and $t_2$ the box sums of $S_1$ and $S_2$ by Lemma 1, $a t_2 - t_1^2 = a^2 \sigma^2$, where $\sigma^2 = \frac{1}{a} \sum v_i^2 - \left(\frac{1}{a}\sum v_i\right)^2$ is the population variance. So line L5 returns $\sigma = \sqrt{a t_2 - t_1^2} / a$.

*Proof.* By Lemma 1, $t_1 = \sum v_i$ and $t_2 = \sum v_i^2$. Then $a^2 \sigma^2 = a \sum v_i^2 - (\sum v_i)^2 = a t_2 - t_1^2$. $\sigma^2 = \frac{1}{a}\sum (v_i - m)^2 \ge 0$ with $m$ the mean, so the root is real. For integer pixels $a t_2 - t_1^2$ is an exact integer. $\square$

**Lemma 5 (optimal stump).** For one feature with values $v_1, \ldots, v_K$, labels $y_i \in \{0, 1\}$ and weights $w_i \ge 0$, the sweep of line L13 returns a stump $(p, \theta)$ whose weighted error $\sum_i w_i [h(v_i) \ne y_i]$ is the least over all $\theta \in \mathbb{R}$ and $p \in \{1, -1\}$.

*Proof.* Sort the examples by value. For $p = 1$ the stump outputs $1$ exactly on $\{i : v_i < \theta\}$, and for $p = -1$ exactly on $\{i : v_i > \theta\}$. Call a set of examples a cut if it is the set of the first $k$ examples in sorted order, where $k = 0$, $k = K$, or the values at positions $k$ and $k + 1$ differ. For every $\theta$, $\{i : v_i < \theta\}$ is a cut, and $\{i : v_i > \theta\}$ is the complement of a cut, namely of $\{i : v_i \le \theta\}$. So every stump outputs $1$ on a cut (for $p = 1$) or on the complement of a cut (for $p = -1$). The sweep visits every cut: it starts with the empty cut and moves all examples with the next distinct value at once. At each cut it uses a $\theta$ strictly between the last value in the cut and the first value after it, or below all values or above all values at the ends. With this $\theta$ the stump with $p = 1$ outputs $1$ exactly on the cut and the stump with $p = -1$ exactly on its complement. With $S^+$, $S^-$ the positive and negative weight in the cut, the errors are $S^- + (T^+ - S^+)$ and $S^+ + (T^- - S^-)$, which are the two values the sweep compares. So the sweep evaluates every possible output set of a stump and keeps the least error. $\square$

The tests compare the sweep with a brute force over all thresholds at the midpoints and outside the range, with random weights.

**Lemma 6 (the error is at most one half).** With normalized weights, the least error $\varepsilon$ of line L13 satisfies $\varepsilon \le \frac12$.

*Proof.* At a fixed cut, the stump with $p = 1$ and the stump with $p = -1$ output complementary values on every example, so their errors add to $\sum w_i = 1$. One of them has error at most $\frac12$. $\square$

So the implementation stops boosting only at $\varepsilon = \frac12$, where no stump helps. At $\varepsilon = 0$ a single stump classifies every example of the stage, and the implementation uses it as the whole stage.

**Lemma 7 (reweighting).** Let $0 < \varepsilon < \frac12$ be the error of the chosen stump $h_t$ with the weights $w$ of line L12, which sum to $1$. After line L14 and the normalization of the next line L12, the weighted error of $h_t$ is exactly $\frac12$. Also $\alpha_t = \log \frac{1 - \varepsilon}{\varepsilon} > 0$.

*Proof.* The examples that $h_t$ misses have weight $\varepsilon$ and keep it. The others have weight $1 - \varepsilon$ and are multiplied by $\beta = \varepsilon / (1 - \varepsilon)$, so their weight becomes $(1 - \varepsilon)\beta = \varepsilon$. The new total is $2\varepsilon$, and after normalization the missed examples have weight $\varepsilon / (2\varepsilon) = \frac12$. Finally $\alpha_t = \log(1/\beta) = \log((1 - \varepsilon)/\varepsilon)$, which is positive because $\varepsilon < \frac12$ gives $(1 - \varepsilon)/\varepsilon > 1$. $\square$

The implementation keeps the weights as exact fractions, and the tests check both the sum $1$ and the value $\frac12$ exactly.

**Lemma 8 (stage threshold).** Let a stage have scores $u_1 \le \cdots \le u_P$ on the $P$ positives that reach it, and let $0 < d \le 1$. With $k = P - \lceil dP \rceil$ and $\Theta = \min\left(\frac12 \sum \alpha_t, u_{k+1}\right)$ (with indices from $1$), the stage accepts at least $\lceil dP \rceil \ge dP$ of the positives.

*Proof.* $0 < d \le 1$ gives $1 \le \lceil dP \rceil \le P$, so $0 \le k \le P - 1$ and $u_{k+1}$ exists. The positives with scores $u_{k+1}, \ldots, u_P$ have a score $\ge u_{k+1} \ge \Theta$ and are accepted; there are $P - k = \lceil dP \rceil$ of them. $\square$

Line L15 also stops adding stumps when the false positive rate of the stage on its negatives is at most $f_{\max}$. The implementation adds a cap on the number of rounds, so a stage can end with a higher rate; then the next stages must reject the rest.

**Lemma 9 (early exit).** Lines L6 and L7 accept a window exactly when every stage gives $\sum_t \alpha_t h_t \ge \Theta$. If stage $r$ is the first that rejects, the features of the stages after $r$ are not computed.

*Proof.* The loop visits the stages in order and returns "reject" at the first stage whose score is below its threshold, so it reaches the end, and accepts, exactly when no stage is below. A stage computes its feature values only inside its own score, and after the return no later stage runs. $\square$

**Lemma 10 (rates and cost).** Let windows be drawn from any distribution, let $R_i$ be the event that a window reaches stage $i$, with $R_1$ always true, and let $p_j = \Pr(\text{stage } j \text{ accepts} \mid R_j)$. If stage $i$ has $n_i$ features, the mean number of features per window is $\sum_i n_i \prod_{j < i} p_j$. With $f_i$ and $d_i$ the same conditional rates over the negative and the positive windows, the false positive rate of the cascade is $\prod_i f_i$ and its detection rate is $\prod_i d_i$.

*Proof.* By Lemma 9 the number of features computed is $\sum_i n_i [R_i]$, and $R_{i+1}$ is the event "$R_i$ and stage $i$ accepts". So $\Pr(R_{i+1}) = \Pr(R_i) p_i$ and by induction $\Pr(R_i) = \prod_{j < i} p_j$. Linearity of expectation gives the mean. A window is accepted exactly when it reaches the end (Lemma 9), so the rate of acceptance is $\Pr(R_{K+1}) = \prod_{j \le K} p_j$ for $K$ stages; restricting the distribution to negatives or to positives gives the two products. $\square$

With the empirical distribution of a test set, this is an exact identity of counts, and the tests check it so.

**Lemma 11 (merging).** Line L9 returns one box for each connected part of the graph whose vertices are the detections and whose edges join two detections with overlapping boxes, and that box has the average corners of the part.

*Proof.* Two boxes $[x_a, x_a + s_a) \times [y_a, y_a + s_a)$ and $[x_b, x_b + s_b) \times [y_b, y_b + s_b)$ overlap exactly when $x_a < x_b + s_b$, $x_b < x_a + s_a$ and the same two inequalities hold in $y$, which is the test of the implementation. It visits every pair and joins the sets of the two detections when they overlap. Union by joining roots keeps the invariant that two detections are in the same set exactly when a path of the edges seen so far joins them: a join adds the edge and merges the two sets of its ends, and path halving changes parents but not the root of any element. After all pairs, the sets are the connected parts. Each part gives the averages of the four corner values, computed as exact fractions. $\square$

**Theorem.** DETECT returns, for each connected part of the overlap graph of the accepted windows, the box with the average corners, where a window is accepted exactly when it lies on the scan grid of lines L2 to L4 and every stage accepts the feature values of Lemma 2 at its scale divided by $\sigma$ of Lemma 4 and by the area ratio of the scaled cells. TRAIN-STAGE returns a stage that accepts at least the fraction $d_{\min}$ of its training positives. The mean cost per window is $\sum_i n_i \prod_{j<i} p_j$ features.

*Proof.* Lemmas 1 to 4 give the values that each stage tests, Lemma 9 the accepted windows, and Lemma 11 the output. Lemmas 5 to 8 give the stage, and Lemma 10 the cost. $\square$

**Invariance to gain.** If $I$ is replaced by $cI$ with $c > 0$, every raw feature value and $\sigma$ are multiplied by $c$, so their ratio does not change, and every stump gives the same output. The exception is a flat window, where the implementation uses $\sigma = 1$; there the zero-sum features are $0$ for any $c$, but a three-rectangle feature is not. Adding a constant $b$ does not change $\sigma$ and does not change a feature whose weights sum to zero. The three-rectangle feature with weights $-1, +1, -1$ on equal cells changes by $-b \cdot wh$, so it is not invariant to an offset.
