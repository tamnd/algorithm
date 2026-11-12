---
tag: DVYT84
kind: problem
slug: isotonic-regression
name: Isotonic regression
aliases:
- monotone regression
- isotonic least squares
area: machine-learning/supervised-learning
level: advanced
summary: Find the non-decreasing sequence nearest to given values in weighted squared error. The solution is unique and has a max-min formula.
prereqs: [regression, quadratic-programming]
see_also: [pool-adjacent-violators, regression, kkt-conditions, quantile-regression, linear-regression]
sources:
  - book: isbn:9780471049708
    title: R. E. Barlow, D. J. Bartholomew, J. M. Bremner and H. D. Brunk, Statistical Inference under Order Restrictions, Wiley, 1972
    locator: Chapter 1 (the isotonic regression problem, its existence and uniqueness, the max-min formulas, and the pool adjacent violators algorithm)
  - book: isbn:9780471917878
    title: Tim Robertson, F. T. Wright and R. L. Dykstra, Order Restricted Statistical Inference, Wiley, 1988
    locator: Chapter 1 (isotonic regression on a partial order, the characterization of the solution, the min-max formulas, and the solution for other loss functions)
  - paper: doi:10.1214/aoms/1177728423
    title: Miriam Ayer, H. D. Brunk, G. M. Ewing, W. T. Reid and Edward Silverman, An empirical distribution function for sampling with incomplete information, Annals of Mathematical Statistics 26(4), 1955
    locator: pp. 641 to 647
  - paper: doi:10.1007/BF01580873
    title: Michael J. Best and Nilotpal Chakravarti, Active set algorithms for isotonic regression; a unifying framework, Mathematical Programming 47, 1990
    locator: pp. 425 to 439
---

Isotonic regression is the problem of fitting a non-decreasing sequence to given values by weighted least squares. On data $(x_i, y_i)$ with the $x_i$ sorted, it gives the best monotone step function of $x$, with no other assumption on its shape. The solution is unique, it is constant on blocks of consecutive points, and each block value is the weighted mean of its points. The [pool adjacent violators](/pool-adjacent-violators/) algorithm computes it in linear time.

## In plain words

You measure something that you know can only go up: the dose of a drug and the effect, or a score and the chance that the score is right. The measurements have noise, so the row of values goes down in some places. You want the row that never goes down and is as close as possible to the measurements, with the closeness measured by the sum of the squared differences.

The answer is made of flat steps. Where the data goes down, the answer joins the nearby points into one flat step at their average. Where the data already goes up, the answer follows the data.

## Definition

**Input.** Values $y = (y_1, \dots, y_n) \in \mathbb{R}^n$ and weights $\omega_1, \dots, \omega_n > 0$. The index order is the order of the constraint. For data $(x_i, y_i)$, it is the order of the $x_i$.

**Output.** The vector

$$\hat y = \arg\min_{z \in \mathbb{R}^n} \sum_{i=1}^{n}\omega_i (y_i - z_i)^2 \quad \text{subject to} \quad z_1 \le z_2 \le \dots \le z_n .$$

The feasible set $K = \{z : z_1 \le \dots \le z_n\}$ is a closed convex cone, and the objective is strictly convex. So the minimizer exists and is unique: $\hat y$ is the projection of $y$ onto $K$ in the inner product $\langle u, v \rangle = \sum_i \omega_i u_i v_i$. This is a [quadratic program](/quadratic-programming/) with $n - 1$ linear constraints.

**The block structure.** Group the indices into maximal runs where $\hat y$ is constant. For a run $B$, write $\operatorname{Av}(B) = \sum_{i \in B}\omega_i y_i / \sum_{i \in B}\omega_i$. Then the value of $\hat y$ on $B$ is $\operatorname{Av}(B)$, and each prefix of $B$ has weighted mean at least $\operatorname{Av}(B)$. Conversely, a monotone $z$ that is constant on consecutive blocks with these two properties is $\hat y$. The proof is on the [pool adjacent violators](/pool-adjacent-violators/) page: these are the [KKT conditions](/kkt-conditions/) of the quadratic program.

**The max-min formula.** Write $\operatorname{Av}(j, k)$ for the weighted mean of $y_j, \dots, y_k$. For each $i$,

$$\hat y_i = \max_{j \le i} \; \min_{k \ge i} \; \operatorname{Av}(j, k) = \min_{k \ge i} \; \max_{j \le i} \; \operatorname{Av}(j, k).$$

*Proof.* Let $i$ lie in the block $B = \{a, \dots, b\}$ of $\hat y$, with value $v$. By the block structure, each prefix of a block has mean at least the block value, so each suffix of a block has mean at most the block value, and the block values do not decrease.

- Fix $j \le i$. The set $\{j, \dots, b\}$ is a suffix of the block of $j$, followed by whole blocks up to $B$. Each of these parts has mean at most $v$, so $\operatorname{Av}(j, b) \le v$, and $\min_{k \ge i}\operatorname{Av}(j,k) \le v$. So the max-min is at most $v$.
- Take $j = a$. For each $k \ge i$, the set $\{a, \dots, k\}$ is a prefix of $B$, or $B$ followed by whole blocks and a prefix of a later block. Each part has mean at least $v$, so $\operatorname{Av}(a, k) \ge v$. So $\min_{k \ge i} \operatorname{Av}(a,k) \ge v$, and the max-min is at least $v$.

So the max-min equals $v = \hat y_i$. The min-max form follows by the same two steps with the roles of $j$ and $k$, and of prefixes and suffixes, exchanged. $\blacksquare$

The formula gives a direct $O(n^3)$ algorithm, and it shows that $\hat y_i$ depends on $y$ in a monotone way: if $y$ grows in one place, no value of $\hat y$ goes down.

## Variants

- **Non-increasing (antitonic) regression.** Fit $-y$ and negate the answer.
- **Other losses.** With $\sum_i \omega_i |y_i - z_i|$ (the $L_1$ isotonic problem) the block values are weighted medians, and the solution need not be unique. With $\max_i \omega_i |y_i - z_i|$ (the $L_\infty$ problem) the solution need not be unique either.
- **Other divergences.** The least squares solution $\hat y$ also minimizes a wide class of other criteria under the same order, for example the Bregman divergences of a convex function. In particular, for binomial proportions $y_i$ with trial counts $\omega_i$, $\hat y$ is the monotone maximum likelihood estimate (Robertson, Wright and Dykstra 1988, Chapter 1).
- **Partial orders.** The constraint set can be any partial order on the indices: $z_i \le z_j$ for each pair $i \preceq j$, for example on a tree or on a grid of two features. The solution is still a unique projection onto a convex cone, and it still has a min-max formula over upper and lower sets, but the pooling algorithm does not apply directly.
- **Unimodal regression.** The fit goes up and then down, with an unknown turning point. It can be solved with prefix and suffix runs of PAV.

## Examples

- $y = (1, 3, 2)$ with unit weights. The pair $(3, 2)$ violates the order, so it is pooled: $\hat y = (1, 5/2, 5/2)$, with error $1/2$. In the max-min formula for $i = 2$: with $j = 1$ the means $\operatorname{Av}(1,2) = 2$ and $\operatorname{Av}(1,3) = 2$ give the minimum 2; with $j = 2$ the means 3 and $5/2$ give $5/2$. The maximum is $5/2$.
- $y = (3, 1, 2)$ with weights $(1, 2, 1)$. The first two points pool to $(3 + 2)/3 = 5/3$, and $2 \ge 5/3$, so $\hat y = (5/3, 5/3, 2)$ with weighted error $8/3$. With unit weights the answer is $(2, 2, 2)$: the weights change the blocks.
- $y = (2, 1, 4, 3)$ with unit weights gives $\hat y = (3/2, 3/2, 7/2, 7/2)$, with error 1.
- $y = (4, 5, 7, 2, 3, 8, 6, 9)$ gives $(4, 17/4, 17/4, 17/4, 17/4, 7, 7, 9)$. This is the worked example of [pool adjacent violators](/pool-adjacent-violators/).
- **Non-example of uniqueness.** For the $L_1$ loss and $y = (1, 3, 2)$, each $(1, t, t)$ with $2 \le t \le 3$ has error 1, the least possible. So the $L_1$ problem can have many solutions, but the least squares problem has one.

## Known algorithms

- [Pool adjacent violators](/pool-adjacent-violators/): $\Theta(n)$ arithmetic operations on a total order, with a stack of blocks. It is exact with exact arithmetic.
- The max-min formula: $O(n^3)$ operations directly, or $O(n^2)$ with prefix sums. It is useful as a test oracle.
- A general [quadratic programming](/quadratic-programming/) solver, such as an [interior point method](/interior-point-method/), for any partial order. Active set methods for the partial order case are studied by Best and Chakravarti (1990).

## Bounds

On a total order, PAV takes $\Theta(n)$ time in the worst case on a [real RAM](/real-ram/). This is optimal: each of the $n$ values can change the answer, so each algorithm must read all of them, which costs $\Omega(n)$.

## Reductions

- Isotonic regression is the Euclidean projection onto the monotone cone $K$, so it is a [quadratic program](/quadratic-programming/) with $n$ variables and $n - 1$ constraints.
- Projection onto the cone of monotone sequences is a step of [projected gradient descent](/projected-gradient-descent/) for any smooth objective under a monotone constraint. PAV computes that step in linear time.
- The $L_2$ fit of a monotone step function is the special case of [regression](/regression/) with the hypothesis class of all non-decreasing functions of one variable.

## Applications

- **Calibration of classifier scores.** Fit the observed labels in 0 and 1 against the order of the scores. The isotonic fit maps each score to a probability that does not decrease with the score.
- **Dose response and survival.** Monotone estimates of a response curve or of a distribution function, which was the first use (Ayer et al. 1955).
- **Shape constrained statistics.** Estimates of a monotone density or failure rate, and the monotone step of single index models.

## References
