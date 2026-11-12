---
tag: 7A99T5
kind: concept
slug: linear-separability
name: Linear separability
aliases:
- linearly separable data
- linearly separable sets
area: machine-learning/supervised-learning
level: intro
summary: Two labelled point sets are linearly separable when a hyperplane has all positive points strictly on one side and all negative points strictly on the other.
prereqs: [linear-feasibility]
see_also: [perceptron, perceptron-convergence-theorem, support-vector-machine, halfspace-learning, separating-hyperplane-theorem, fourier-motzkin-elimination, vc-dimension, kernel-trick]
sources:
  - paper: doi:10.1109/PGEC.1965.264137
    title: Thomas M. Cover, Geometrical and statistical properties of systems of linear inequalities with applications in pattern recognition, IEEE Transactions on Electronic Computers EC-14(3), 1965
    locator: pp. 326 to 334; the function counting theorem (Theorem 1) and the capacity 2d
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 2.5 (separating hyperplanes) and Section 8.6 (classification, linear discrimination as a feasibility problem)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 9.1 (halfspaces, the realizable case, and ERM by linear programming)
  - book: isbn:9780262631112
    title: Marvin Minsky and Seymour Papert, Perceptrons, expanded edition, MIT Press, 1988
    locator: the predicates that a single linear threshold unit cannot compute, such as parity
---

Two finite sets of labelled points are linearly separable when some hyperplane has every positive point strictly on one side and every negative point strictly on the other. It is the condition under which the [perceptron](/perceptron/) stops and the hard margin [support vector machine](/support-vector-machine/) has a solution. Deciding it is a [linear feasibility](/linear-feasibility/) problem, so linear programming answers it exactly. XOR is the classic set that is not separable, and Cover's function counting theorem says how many labelings of points in general position are.

## In plain words

Put red and blue dots on a sheet of paper. If you can draw one straight line with all the red dots on one side and all the blue dots on the other, the two colors are linearly separable. In three dimensions the line becomes a flat plane, and in more dimensions a hyperplane.

Some patterns are not separable. Put red dots on two opposite corners of a square and blue dots on the other two corners. Every straight line leaves a red and a blue dot on the same side. This is the XOR pattern.

The more dots you have compared with the number of dimensions, the fewer colorings can be split by a hyperplane. With twice as many dots as dimensions, about half of the colorings can.

## The idea

**Definition.** Let $S = ((x_1, y_1), \ldots, (x_n, y_n))$ with $x_i \in \mathbb{R}^d$ and $y_i \in \{-1, +1\}$. The set $S$ is *linearly separable* if there are $w \in \mathbb{R}^d$ and $b \in \mathbb{R}$ with

$$y_i (w \cdot x_i + b) > 0 \quad \text{for } i = 1, \ldots, n.$$

It is *homogeneously separable* if this holds with $b = 0$, that is, by a hyperplane through the origin. The augmentation $x \mapsto (x, 1)$ turns the first case into the second in $\mathbb{R}^{d+1}$.

**Margin.** For a separating $(w, b)$, the geometric margin is $\gamma = \min_i y_i (w \cdot x_i + b)/\lVert w \rVert$, the distance from the hyperplane to the nearest point. A finite separable set has a separator with a positive margin, and a largest one; the [support vector machine](/support-vector-machine/) finds it.

**Convex hulls.** $S$ is linearly separable if and only if the convex hulls of the positive points and of the negative points are disjoint. If a point $p$ lies in both hulls, $p = \sum_{y_i = +1} \mu_i x_i = \sum_{y_j = -1} \nu_j x_j$ with nonnegative weights that sum to 1 on each side, then any $(w, b)$ gives $w \cdot p + b = \sum \mu_i (w \cdot x_i + b)$, which is positive for a separator, and also $\sum \nu_j (w \cdot x_j + b)$, which is negative. So no separator exists. The other direction is the [separating hyperplane theorem](/separating-hyperplane-theorem/) for two disjoint compact convex sets.

**The test by linear programming.** Strict inequalities are not allowed in a linear program, but scaling removes them. If $(w, b)$ separates $S$, let $m = \min_i y_i (w \cdot x_i + b) > 0$; then $(w/m, b/m)$ satisfies

$$y_i (w \cdot x_i + b) \ge 1 \quad \text{for } i = 1, \ldots, n,$$

and every solution of this system separates $S$. So separability is the feasibility of $n$ linear inequalities in $d + 1$ unknowns. An LP solver such as the [simplex method](/simplex-method/) decides it, and an interior point method decides it in time polynomial in the input size. For tiny systems, [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) decides it with exact rational arithmetic: it removes one unknown at a time by combining each lower bound with each upper bound, and back substitution gives a separator with rational entries. Its cost can grow doubly exponentially in the number of unknowns, so it suits only small $d$. When the system is infeasible, [Farkas' lemma](/farkas-lemma/) gives a certificate: nonnegative $\lambda$, not all zero, with $\sum_i \lambda_i y_i x_i = 0$ and $\sum_i \lambda_i y_i = 0$. After scaling, these $\lambda$ are the weights of a common point of the two hulls.

**Cover's function counting theorem (Cover 1965).** Vectors $x_1, \ldots, x_n \in \mathbb{R}^d$ are in *general position* if every subset of at most $d$ of them is linearly independent. For such vectors, the number of labelings $y \in \{-1, +1\}^n$ that are homogeneously separable is

$$C(n, d) = 2 \sum_{k=0}^{d-1} \binom{n-1}{k}.$$

The number does not depend on where the vectors are, only on $n$ and $d$.

*Proof.* Each labeling is a *dichotomy*. Induct on $n$. For $n = 1$, a nonzero $x_1$ gets either label from $w = \pm x_1$, so $C(1, d) = 2$, which matches the formula. For $d = 1$ and $n \ge 1$, the points are nonzero reals, and $w \in \{-1, +1\}$ gives exactly the two labelings $y_i = \pm \operatorname{sign}(x_i)$, so $C(n, 1) = 2$.

Now let $d \ge 2$ and add a vector $x_{n+1}$ to $n$ vectors so that all $n + 1$ are in general position. Take a separable dichotomy $D$ of $x_1, \ldots, x_n$. Its separators form a convex cone $K_D$, open in $\mathbb{R}^d$. If $K_D$ contains a $w$ with $w \cdot x_{n+1} = 0$, then $w \pm \epsilon x_{n+1}$ for a small $\epsilon > 0$ separates $D$ with either label on $x_{n+1}$, so $D$ extends in two ways. If not, then $w \cdot x_{n+1}$ has the same sign on all of $K_D$, because a cone that contains $w_1$ and $w_2$ of opposite signs contains a point of the segment between them where the sign is zero. Then $D$ extends in exactly one way. So

$$C(n+1, d) = C(n, d) + N,$$

where $N$ is the number of dichotomies of $x_1, \ldots, x_n$ that a $w \perp x_{n+1}$ separates. Let $P$ be the orthogonal projection onto the hyperplane $x_{n+1}^\perp \cong \mathbb{R}^{d-1}$. For $w \perp x_{n+1}$, $w \cdot x_i = w \cdot P x_i$, so $N$ counts the homogeneously separable dichotomies of $P x_1, \ldots, P x_n$ in $\mathbb{R}^{d-1}$. These are in general position: if $d - 1$ or fewer of them had a nontrivial linear relation $\sum c_i P x_i = 0$, then $\sum c_i x_i$ would be a multiple of $x_{n+1}$, a relation among at most $d$ of the original vectors. So $N = C(n, d-1)$ by induction, and

$$C(n+1, d) = C(n, d) + C(n, d-1).$$

The formula satisfies the same recursion, by Pascal's rule $\binom{n}{k} = \binom{n-1}{k} + \binom{n-1}{k-1}$, and the same values at $n = 1$ and at $d = 1$. So it holds for all $n, d \ge 1$. $\square$

**Consequences of the count.** If $n \le d$, then $C(n, d) = 2^n$: all labelings are separable. At $n = 2d$, exactly half are, because $\sum_{k=0}^{d-1}\binom{2d-1}{k} = 2^{2d-2}$; Cover calls $2d$ the capacity of a linear threshold unit with $d$ weights. For hyperplanes with a bias in $\mathbb{R}^d$, apply the theorem to the vectors $(x_i, 1)$ in $\mathbb{R}^{d+1}$: when every $d + 1$ of the points are affinely independent, $C(n, d+1)$ labelings are separable. In particular, $C(n, d + 1) = 2^n$ exactly when $n \le d + 1$, which gives the [VC dimension](/vc-dimension/) $d + 1$ of halfspaces in $\mathbb{R}^d$.

## Examples

**AND and OR.** On the square $\{0, 1\}^2$, AND (only $(1, 1)$ positive) is separated by $w = (2, 2)$, $b = -3$, and OR (only $(0, 0)$ negative) by $w = (2, 2)$, $b = -1$. These are the separators that Fourier-Motzkin back substitution returns for the system $y_i(w \cdot x_i + b) \ge 1$. The values $y_i (w \cdot x_i + b)$ are $3, 1, 1, 1$ for AND and $1, 1, 1, 3$ for OR.

**XOR is not separable.** Let $(0, 0)$ and $(1, 1)$ be negative and $(1, 0)$ and $(0, 1)$ positive. A separator would satisfy $w_1 + b > 0$ and $w_2 + b > 0$, so $w_1 + w_2 + 2b > 0$, and also $b < 0$ and $w_1 + w_2 + b < 0$, so $w_1 + w_2 + 2b < 0$. The Farkas certificate is $\lambda = (1, 1, 1, 1)$: the point $(1/2, 1/2)$ is the midpoint of both diagonals, so it lies in both hulls. Of the 16 labelings of the square, exactly 14 are separable; XOR and its complement are the two that are not.

**XOR after a feature map.** Add the feature $x_1 x_2$. In $\mathbb{R}^3$ the points become $(0,0,0)$, $(1,1,1)$, $(1,0,0)$, $(0,1,0)$, and $w = (2, 2, -4)$, $b = -1$ separates XOR. The values $w \cdot x + b$ are $-1$, $-1$, $1$, $1$. This is the idea of the [kernel trick](/kernel-trick/).

**Cover's counts.** For $d = 3$ and $n = 1, \ldots, 6$ the formula gives $2, 4, 8, 14, 22, 32$. Enumerating all $2^n$ labelings of random integer vectors in general position, with an exact feasibility test for each, gives the same numbers. For $d = 2$ the counts are $2n$: the labelings of $n$ directions in the plane that a line through the origin separates.

**A non-example of general position.** The vectors $(1, 0)$, $(2, 0)$ and $(-1, 0)$ lie on one line through the origin, so two of them are dependent. Only 2 of the 8 labelings are homogeneously separable, fewer than $C(3, 2) = 6$. The theorem needs general position.

**Why the inequality is strict.** If the definition used $y_i (w \cdot x_i + b) \ge 0$, then $w = 0$ and $b = 0$ would pass for every labeled set, XOR included. A weak version needs an extra condition such as $w \ne 0$, and even then the points $(0, 0)$ labeled $+1$ and $(1, 0)$ labeled $-1$ are weakly separated by the line $x_1 = 0$, which touches the positive point.

## Where it is used

- **The [perceptron](/perceptron/).** It stops on a finite set if and only if the set is linearly separable, after at most $(R/\gamma)^2$ mistakes by the [perceptron convergence theorem](/perceptron-convergence-theorem/).
- **The hard margin [support vector machine](/support-vector-machine/).** Its constraints $y_i (w \cdot x_i + b) \ge 1$ are the LP test above, so it is feasible exactly when the data is separable. The soft margin version exists for all data.
- **[Halfspace learning](/halfspace-learning/).** In the realizable case, empirical risk minimization over halfspaces is this feasibility problem, solvable in polynomial time. In the agnostic case it is NP-hard.
- **[Logistic regression](/logistic-regression/).** On separable data the logistic loss has no minimizer: scaling a separator up drives the loss to 0, so the weights diverge without regularization.
- **The [kernel trick](/kernel-trick/).** A feature map can make data separable, and Cover's theorem explains why: in a higher dimension, more labelings are separable.
- **The [VC dimension](/vc-dimension/) of halfspaces.** It is $d + 1$ in $\mathbb{R}^d$, the largest $n$ with $C(n, d+1) = 2^n$.

## References
