---
tag: 34Q4BF
kind: problem
slug: halfspace-learning
name: Halfspace learning
aliases:
- linear threshold function learning
- learning halfspaces
area: machine-learning/supervised-learning
level: advanced
summary: "Learn a classifier sign(w . x + b) from labeled points. Consistent learning is a linear program, solvable in polynomial time; agnostic learning is NP-hard."
prereqs: [linear-separability, vc-dimension, linear-programming-problem]
see_also: [perceptron, perceptron-convergence-theorem, support-vector-machine, linear-feasibility, ellipsoid-method, radon-theorem, statistical-query-model, logistic-regression]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 9.1 (halfspaces, ERM by linear programming, the perceptron and its (R/gamma)^2 bound, the VC dimension of halfspaces)
  - paper: doi:10.1145/76359.76371
    title: Anselm Blumer, Andrzej Ehrenfeucht, David Haussler and Manfred K. Warmuth, Learnability and the Vapnik-Chervonenkis dimension, Journal of the ACM 36(4), 1989
    locator: PAC learning of halfspaces by a consistent linear programming learner and the VC dimension d + 1
  - paper: doi:10.1007/PL00013833
    title: Avrim Blum, Alan Frieze, Ravi Kannan and Santosh Vempala, A polynomial-time algorithm for learning noisy linear threshold functions, Algorithmica 22, 1998
    locator: learning halfspaces with random classification noise in polynomial time
  - paper: doi:10.1109/FOCS.2006.33
    title: Venkatesan Guruswami and Prasad Raghavendra, Hardness of learning halfspaces with noise, FOCS 2006
    locator: NP-hardness of finding a halfspace that agrees with a 1/2 + epsilon fraction when one agrees with 1 - epsilon
  - paper: doi:10.1109/FOCS.2006.51
    title: Vitaly Feldman, Parikshit Gopalan, Subhash Khot and Ashok Kumar Ponnuswami, New results for learning noisy parities and halfspaces, FOCS 2006
    locator: the same NP-hardness of proper agnostic learning of halfspaces, proved independently
  - paper: "Albert B. J. Novikoff, On convergence proofs on perceptrons, Proceedings of the Symposium on the Mathematical Theory of Automata, 1962"
    locator: the (R/gamma)^2 mistake bound of the perceptron
---

Halfspace learning is the problem of finding a linear threshold classifier $x \mapsto \mathrm{sign}(w \cdot x + b)$ that agrees with labeled examples. When some halfspace labels every example correctly (the realizable case), finding one is a [linear program](/linear-programming-problem/), so it can be done in polynomial time; with the [VC dimension](/vc-dimension/) $d + 1$ of halfspaces in $\mathbb{R}^d$, this makes halfspaces efficiently [PAC learnable](/pac-learning/). The [perceptron](/perceptron/) finds one too, after at most $(R/\gamma)^2$ mistakes when the data have margin $\gamma$. When no halfspace is consistent, the picture changes: with random label noise the problem is still polynomial (Blum, Frieze, Kannan and Vempala 1998), but finding a halfspace that is even slightly better than random, when a nearly perfect one exists, is NP-hard (Guruswami and Raghavendra 2006; Feldman, Gopalan, Khot and Ponnuswami 2006).

## In plain words

You have points in space, each colored red or blue, and you want a flat wall (a line in the plane, a plane in space) with all red points on one side and all blue points on the other. If such a wall exists, you can find one quickly by writing "every point is on its correct side, by at least a little" as a list of linear inequalities and solving them. A wall in $d$ dimensions has only $d + 1$ numbers to set, so a modest number of examples is enough for the wall to also work on new points. If no wall separates the colors, and you want the wall with the fewest mistakes, the problem becomes very hard.

## Definition

**Halfspaces.** A halfspace in $\mathbb{R}^d$ is the classifier $h_{w,b}(x) = \mathrm{sign}(w \cdot x + b)$ with $w \in \mathbb{R}^d$ and $b \in \mathbb{R}$. It is *homogeneous* if $b = 0$. The class of all halfspaces is $H_d$.

**Consistent halfspace learning (realizable).** Input: examples $(x_1, y_1), \ldots, (x_m, y_m)$ with $x_i \in \mathbb{Q}^d$ and $y_i \in \{-1, +1\}$. Output: $(w, b)$ with $y_i(w \cdot x_i + b) > 0$ for every $i$, or a report that none exists. Since there are finitely many examples, a strict separator can be scaled so that the smallest value is 1, so the task is the [linear feasibility](/linear-feasibility/) problem

$$y_i(w \cdot x_i + b) \ge 1, \qquad i = 1, \ldots, m.$$

**PAC halfspace learning.** For an unknown distribution $D$ on $\mathbb{R}^d$ and target $h^* \in H_d$, output with probability $1 - \delta$ a classifier with error at most $\varepsilon$.

**Agnostic halfspace learning.** For an arbitrary distribution on $\mathbb{R}^d \times \{-1, +1\}$, output $h$ with error at most $\mathrm{opt} + \varepsilon$, where $\mathrm{opt}$ is the smallest error of a halfspace. On a sample this is the problem of minimizing the number of disagreements.

## Variants

- **Homogeneous halfspaces.** Map $x$ to $(x, 1) \in \mathbb{R}^{d+1}$; then $b$ becomes a coordinate of $w$. Every result for one form transfers to the other.
- **Margin.** The data have margin $\gamma$ if some unit $w$ has $y_i (w \cdot x_i) \ge \gamma$ for all $i$, with $\lVert x_i \rVert \le R$. Then the complexity depends on $R/\gamma$, not on $d$; this is the setting of the perceptron and of the [support vector machine](/support-vector-machine/), which finds the largest margin.
- **Random classification noise.** Each label is flipped with probability $\eta < 1/2$. Solved in polynomial time by Blum, Frieze, Kannan and Vempala (1998), whose algorithm can also be written with [statistical queries](/statistical-query-model/).
- **Agnostic and adversarial noise.** Arbitrary labels. Hard in general (see Bounds); easier under assumptions on the distribution of $x$, such as uniform on the sphere or log-concave.
- **Online learning.** Examples arrive one at a time and the learner predicts before it sees the label; the perceptron and Winnow are mistake-bounded algorithms for this variant.
- **Improper learning.** The output may be any classifier, not a halfspace. The hardness results above are for proper learners; with improper learners the agnostic problem is also believed hard, but under other assumptions.

## Examples

**Exact simplex.** The code for this page solves the feasibility problem above with an exact two-phase [simplex method](/simplex-method/) in rational arithmetic, using [Bland's rule](/bland-rule/) against cycling. The free variables $w$ and $b$ are split as $w = w^+ - w^-$ and $b = b^+ - b^-$ with all parts nonnegative, and each inequality gets a surplus variable. [Phase 1](/two-phase-simplex-method/) finds a feasible point or proves that none exists. Phase 2 then minimizes $\lVert w \rVert_1 + |b|$, which picks a definite answer among the many separators. On random data with coordinates in $\{-1, -7/8, \ldots, 1\}$ labeled by an integer halfspace (seed 1):

| examples | $d$ | true $(w, b)$ | found $(w, b)$ | pivots |
|---|---|---|---|---|
| 10 | 2 | $(-2, 1)$, $-1/2$ | $(-160/51, 16/17)$, $-61/51$ | 12 |
| 30 | 2 | $(-3, 2)$, $1/2$ | $(-16, 8)$, $5$ | 41 |
| 30 | 5 | $(0, 1, -1, 3, 1)$, $0$ | 5 coordinates over 14587 | 62 |
| 60 | 5 | $(-1, -3, -1, -2, 3)$, $1/2$ | 5 coordinates over 25591 | 98 |

Every found halfspace satisfies $y_i (w \cdot x_i + b) \ge 1$ exactly. It is a different halfspace from the one that made the labels, since many halfspaces fit a finite sample. The tests check consistency on random separable data in dimensions 1 to 4, that the found $\lVert w \rVert_1 + |b|$ is never larger than that of the true separator scaled to margin 1, the 1D case against brute force, and the simplex itself against vertex enumeration on random small linear programs.

**XOR.** The points $(0, 0), (1, 1)$ labeled $+1$ and $(0, 1), (1, 0)$ labeled $-1$ cannot be separated: adding the two $+1$ inequalities gives $w_1 + w_2 + 2b \ge 2$, adding the two $-1$ inequalities gives $-(w_1 + w_2 + 2b) \ge 2$, and the sum is $0 \ge 4$. Phase 1 ends with a positive objective and reports this.

**Shattering.** The $d + 1$ points $0, e_1, \ldots, e_d$ can be given all $2^{d+1}$ labelings by halfspaces; the tests check this with the LP for $d = 1, 2, 3$. A triangle with one point inside cannot be shattered: the labeling with the inside point $-1$ and the corners $+1$ would need a halfspace containing the corners but not a convex combination of them.

## Known algorithms

| algorithm | setting | guarantee |
|---|---|---|
| linear programming ([ellipsoid](/ellipsoid-method/), [interior point](/karmarkar-algorithm/)) | consistent | polynomial in $m$, $d$ and the bit size ([LP is in P](/lp-in-p/)) |
| simplex method | consistent | exact and fast in practice; exponential in the worst case for the common pivot rules |
| [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) | consistent | exact, but the number of inequalities can grow doubly exponentially in $d$ |
| perceptron | margin $\gamma$, $\lVert x \rVert \le R$ | at most $(R/\gamma)^2$ mistakes ([perceptron convergence theorem](/perceptron-convergence-theorem/)); can be exponential in the bit size when $\gamma$ is tiny |
| support vector machine | margin | the maximum margin separator, by convex quadratic programming |
| Blum, Frieze, Kannan and Vempala | random classification noise | polynomial in $d$, $1/\varepsilon$, $1/(1 - 2\eta)$ and the bit size |
| surrogate losses ([logistic regression](/logistic-regression/), hinge loss) | agnostic, as a heuristic | convex and fast, but with no guarantee of error $\mathrm{opt} + \varepsilon$ in the worst case |

Any consistent learner, by the [fundamental theorem](/fundamental-theorem-of-statistical-learning/), PAC learns $H_d$ from $O\big((d \log(1/\varepsilon) + \log(1/\delta))/\varepsilon\big)$ examples, so the LP learner is an efficient PAC learner (Blumer, Ehrenfeucht, Haussler and Warmuth 1989).

## Bounds

- **VC dimension $d + 1$.** Lower bound: the set $\{0, e_1, \ldots, e_d\}$ is shattered. For a labeling $y$, take $b = y_0/2$ and $w_i = y_i - b$; then $\mathrm{sign}(b) = y_0$ and $\mathrm{sign}(w_i + b) = y_i$. Upper bound: by [Radon's theorem](/radon-theorem/), any $d + 2$ points split into two parts whose convex hulls meet. Label one part $+1$ and the other $-1$; a halfspace containing the first part contains its convex hull, so it contains a point of the other hull, and so it cannot exclude all of the second part. So no $d + 2$ points are shattered.
- **Sample complexity.** $\Theta\big((d + \log(1/\delta))/\varepsilon\big)$ examples are necessary and sufficient in the realizable case (up to the $\log(1/\varepsilon)$ factor for an arbitrary consistent learner); $\Theta\big((d + \log(1/\delta))/\varepsilon^2\big)$ in the agnostic case.
- **Perceptron.** At most $(R/\gamma)^2$ mistakes. Turned into a batch learner, this gives a margin-based sample bound of order $(R/\gamma)^2/\varepsilon$ up to logarithmic factors, independent of $d$.
- **Hardness of proper agnostic learning.** For every $\varepsilon > 0$, given examples on which some halfspace agrees with a $1 - \varepsilon$ fraction, it is NP-hard to find a halfspace that agrees with a $\frac12 + \varepsilon$ fraction (Guruswami and Raghavendra 2006; Feldman, Gopalan, Khot and Ponnuswami 2006). So minimizing disagreements cannot even be approximated well. Exactly minimizing disagreements was known to be NP-hard earlier.
- **Strongly polynomial time.** The consistent problem is polynomial in the bit size. Whether linear programming, and so this problem, has an algorithm whose number of arithmetic steps is polynomial in $m$ and $d$ alone is open.

## Reductions

- **To linear feasibility.** The consistent problem is the system $y_i(w \cdot x_i + b) \ge 1$. Conversely, a homogeneous system $A z > 0$ is strictly feasible exactly when the rows of $A$, all labeled $+1$, are separable by a homogeneous halfspace. So the two problems are the same.
- **From polynomial threshold functions.** A degree $k$ polynomial threshold function in $d$ variables is a halfspace over the $O(d^k)$ monomials. The kernel trick of the support vector machine works with this map without writing it out.
- **From conjunctions and decision lists.** A conjunction of literals over $\{0, 1\}^d$ is a halfspace: $x_1 \wedge \neg x_2$ is $\mathrm{sign}(x_1 - x_2 - 1/2)$. A decision list is also a halfspace, with exponentially decreasing weights. So hardness for halfspaces does not come from these classes, and learners for halfspaces also learn them.
- **To the statistical query model.** The noise-tolerant algorithm of Blum, Frieze, Kannan and Vempala can be cast with statistical queries, which is why it survives random classification noise.

## Applications

- **Linear classifiers.** Spam filters, credit scoring, text categorization and many other tasks use linear classifiers on hand-made or learned features; training them is a form of this problem with a loss function.
- **Building block of neural networks.** A neuron with a threshold activation is a halfspace; the perceptron was the first learning rule for it.
- **Kernel methods.** Learning a halfspace in a feature space gives nonlinear classifiers in the input space.
- **Learning theory.** Halfspaces are the standard test case for new noise models, and their hardness results are used to show that other classes, such as intersections of halfspaces and small neural networks, are hard to learn properly.

## References
