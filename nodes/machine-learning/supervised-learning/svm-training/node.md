---
tag: WT03MH
kind: problem
slug: svm-training
name: Support vector machine training
aliases:
- SVM training problem
- SVM dual quadratic program
- SVM optimization problem
area: machine-learning/supervised-learning
level: advanced
summary: "Find the weights of a soft margin SVM: solve its convex quadratic program, in the primal or in the box-constrained dual, to a given KKT tolerance."
prereqs: [support-vector-machine, quadratic-programming]
see_also: [sequential-minimal-optimization, coordinate-descent, stochastic-gradient-descent, interior-point-method, kkt-conditions, hinge-loss, support-vector-regression, cutting-plane-method]
sources:
  - paper: doi:10.1109/NNSP.1997.622408
    title: Edgar Osuna, Robert Freund and Federico Girosi, An improved training algorithm for support vector machines, Neural Networks for Signal Processing VII, Proceedings of the 1997 IEEE Workshop, 1997
    locator: pp. 276 to 285 (the decomposition method with a fixed size working set and the proof that it improves the objective)
  - paper: "Rong-En Fan, Pai-Hsuen Chen and Chih-Jen Lin, Working set selection using second order information for training support vector machines, Journal of Machine Learning Research 6, 2005"
    locator: pp. 1889 to 1918 (the second order working set selection WSS3, its convergence and the comparison with first order selection)
  - paper: doi:10.1145/1961189.1961199
    title: Chih-Chung Chang and Chih-Jen Lin, LIBSVM, a library for support vector machines, ACM Transactions on Intelligent Systems and Technology 2(3), 2011
    locator: Article 27, Section 4 (the decomposition method, working set selection, shrinking and caching, and the stopping rule)
  - paper: doi:10.1145/1273496.1273598
    title: Shai Shalev-Shwartz, Yoram Singer and Nathan Srebro, Pegasos, primal estimated sub-gradient solver for SVM, Proceedings of the 24th International Conference on Machine Learning (ICML), 2007
    locator: pp. 807 to 814 (the algorithm with step size 1/(λt), the optional projection, mini-batches, and the Õ(1/(λε)) iteration bound)
  - paper: doi:10.1145/1390156.1390208
    title: Cho-Jui Hsieh, Kai-Wei Chang, Chih-Jen Lin, S. Sathiya Keerthi and S. Sundararajan, A dual coordinate descent method for large-scale linear SVM, Proceedings of the 25th International Conference on Machine Learning (ICML), 2008
    locator: pp. 408 to 415 (Algorithm 1 for the L1 and L2 loss SVM, the projected gradient, shrinking, and the linear convergence result)
  - paper: "Thorsten Joachims, Making large-scale SVM learning practical, in Advances in Kernel Methods: Support Vector Learning, MIT Press, 1999"
    locator: pp. 169 to 184 (SVMlight; working set selection by a feasible direction, shrinking and caching)
  - book: isbn:9780262026253
    title: Léon Bottou, Olivier Chapelle, Dennis DeCoste and Jason Weston (editors), Large-Scale Kernel Machines, MIT Press, 2007
    locator: Chapter 1, Léon Bottou and Chih-Jen Lin, Support vector machine solvers (a survey of the dual problem, decomposition, SMO, working set selection, shrinking and caching)
---

SVM training is the problem of computing the weights of a [support vector machine](/support-vector-machine/) from the data. It is a convex [quadratic program](/quadratic-programming/), so it is solvable in polynomial time, but a general solver needs the $n \times n$ kernel matrix and $\Theta(n^3)$ time, which is too much beyond a few thousand points. The practical methods use the structure of the problem: decomposition methods such as [SMO](/sequential-minimal-optimization/) change two dual variables at a time, while for linear SVMs dual coordinate descent and the stochastic sub-gradient method Pegasos change one variable or one random sample at a time.

## In plain words

Training an SVM means finding the widest street between two classes while paying for the points that enter it. This is a well behaved problem: it has one best answer, and you can check whether an answer is the best one. The difficulty is size. One number per pair of training points describes the problem, so a million points give a trillion numbers.

The good methods never look at the whole problem at once. They pick a few points, improve the answer for those points only, and repeat. Each small step is cheap, and the steps stop when no point breaks the rules of the best answer by more than a small amount.

## Definition

**Input.** Training points $(x_1, y_1), \ldots, (x_n, y_n)$ with $y_i \in \{-1, +1\}$, a positive semidefinite kernel $k$ (or $k(x, z) = x \cdot z$ for a linear SVM), a constant $C > 0$, and a tolerance $\varepsilon > 0$.

**The primal problem.**

$$\min_{w, b} \; \tfrac12 \lVert w \rVert^2 + C \sum_{i=1}^n \max\bigl(0, 1 - y_i (w \cdot \varphi(x_i) + b)\bigr).$$

**The dual problem.** With $Q_{ij} = y_i y_j k(x_i, x_j)$ and $e$ the vector of ones,

$$\min_\alpha \; \tfrac12 \alpha^\top Q \alpha - e^\top \alpha \quad \text{subject to } y^\top \alpha = 0, \; 0 \le \alpha_i \le C.$$

**Output.** A feasible $\alpha$, with $b$, that is optimal within $\varepsilon$. The usual measure is the largest KKT violation. With the gradient $G = Q\alpha - e$, define

$$I_{up} = \{t : \alpha_t < C, y_t = 1\} \cup \{t : \alpha_t > 0, y_t = -1\}, \quad I_{low} = \{t : \alpha_t < C, y_t = -1\} \cup \{t : \alpha_t > 0, y_t = 1\}.$$

Then $\alpha$ is optimal if and only if $m(\alpha) = \max_{t \in I_{up}} -y_t G_t$ is at most $M(\alpha) = \min_{t \in I_{low}} -y_t G_t$, and the solver stops when $m(\alpha) - M(\alpha) \le \varepsilon$. Another measure is the duality gap between the primal and dual values.

**Cost model.** The real RAM. The costs are the number of kernel evaluations, each costing $t$ (or $O(d)$ for a linear kernel with $d$ features), the arithmetic, and the memory. For large data the memory for $Q$ is often the binding cost.

## Variants

- **With or without the bias $b$.** The bias creates the equality constraint $y^\top \alpha = 0$. Without it, the dual has only box constraints, and a single variable can move alone. Linear solvers such as LIBLINEAR usually drop $b$ and add a constant feature instead, which regularizes the bias too.
- **Kernel or linear.** For a kernel SVM the solver works with $\alpha$ and kernel values. For a linear SVM it keeps $w = \sum_i \alpha_i y_i x_i$ explicitly, so the gradient of one dual variable costs $O(d)$ and not $O(n)$.
- **L1 or L2 loss.** The squared hinge loss $C \sum_i \xi_i^2$ gives the dual $\min \tfrac12 \alpha^\top (Q + I/(2C)) \alpha - e^\top \alpha$ with only $\alpha \ge 0$. The matrix is positive definite, so the solution is unique.
- **Exact or approximate.** In practice one solves to a tolerance $\varepsilon$ such as $10^{-3}$, because the classifier changes little after that. Stochastic methods give an $\varepsilon$ suboptimal primal value with high probability.
- **Other SVM problems.** The ν-SVM, the one-class SVM and [support vector regression](/support-vector-regression/) have duals of the same form, with different $Q$, linear term and constraints. The same solvers apply.

## Examples

**Dual coordinate descent by hand.** Take $x_1 = (1, 0)$ and $x_2 = (0, 1)$ with $y = +1$, $x_3 = (-1, -1)$ with $y = -1$, no bias and $C = 1$. Then $Q_{11} = Q_{22} = 1$ and $Q_{33} = 2$. Start with $\alpha = 0$ and $w = 0$, and visit the points in order. The step for point $i$ is $G = y_i w \cdot x_i - 1$ and $\alpha_i \leftarrow \min(\max(\alpha_i - G/Q_{ii}, 0), C)$, followed by $w \leftarrow w + (\Delta\alpha_i) y_i x_i$.

| step | $i$ | $G$ | new $\alpha_i$ | $w$ |
|---|---|---|---|---|
| 1 | 1 | $-1$ | 1 | $(1, 0)$ |
| 2 | 2 | $-1$ | 1 | $(1, 1)$ |
| 3 | 3 | $(-1)(-2) - 1 = 1$ | 0 (no change) | $(1, 1)$ |

In the second pass, points 1 and 2 have $G = 0$, and point 3 has $G = 1 > 0$ at $\alpha_3 = 0$, so every projected gradient is 0 and the method stops. The result $w = (1, 1)$ has primal value $\tfrac12 \cdot 2 + 0 = 1$ and dual value $2 - 1 = 1$, so it is optimal. With $C = 0.1$ the same three steps give $\alpha = (0.1, 0.1, 0.1)$ and $w = (0.2, 0.2)$, with primal and dual value $0.26$.

**Pegasos.** On 200 points from two overlapping Gaussian clouds, with $\lambda = 1/n$ (the same problem as $C = 1$), the Pegasos objective after 60000 single-sample steps is within 1% of the optimum found by dual coordinate descent. With mini-batches of 10 points, 6000 steps give the same accuracy.

**A hard case for dual coordinate descent.** On 80 overlapping points with $C = 1$, dual coordinate descent reaches a KKT violation of $10^{-9}$ in fewer than 200 passes. With $C = 100$ it does not reach it in 10000 passes. Large $C$ makes the dual badly conditioned, and the method then needs many passes.

## Known algorithms

| method | idea | cost per step | where it fits |
|---|---|---|---|
| general QP solver | interior point or active set on the full dual | $O(n^3)$ time, $\Theta(n^2)$ memory | $n$ up to a few thousand |
| chunking | solve the QP on a subset; keep the support vectors, add the worst violators, repeat | a QP on the chunk | few support vectors |
| decomposition (Osuna, Freund and Girosi 1997) | fixed size working set $B$; solve the subproblem in $\alpha_B$ with the rest fixed | a QP of size $|B|$ plus $O(n |B|)$ gradient update | kernel SVMs |
| SVMlight (Joachims 1999) | working set from a steepest feasible direction, with shrinking and caching | as above | kernel SVMs |
| [SMO](/sequential-minimal-optimization/) (Platt 1998) | $|B| = 2$, the smallest set that can keep $y^\top \alpha = 0$; closed form step | $O(n)$ with cached kernel columns | kernel SVMs |
| WSS3 (Fan, Chen and Lin 2005) | SMO with the pair chosen by second order information | $O(n)$ | LIBSVM's default |
| dual coordinate descent (Hsieh et al. 2008) | no bias, one variable at a time, explicit $w$ | $O(d)$ | linear SVMs, LIBLINEAR's default |
| Pegasos (Shalev-Shwartz, Singer and Srebro 2007) | stochastic sub-gradient steps on the primal with step $1/(\lambda t)$ | $O(d k)$ for a batch of $k$ | very large linear problems |
| primal Newton and cutting plane methods | Newton steps on the smooth L2 loss; cutting planes for the hinge loss (SVMperf) | varies | linear SVMs |

**Decomposition.** Osuna, Freund and Girosi split the variables into a working set $B$ and the fixed set $N$. The subproblem in $\alpha_B$ is again a QP of the same form, with linear term $Q_{BN} \alpha_N - e_B$ and equality constraint $y_B^\top \alpha_B = -y_N^\top \alpha_N$. They proved that moving a KKT violator into $B$ in exchange for a variable that is satisfied strictly decreases the objective. Each step needs only the columns of $Q$ for $B$.

**SMO and WSS3.** With $|B| = 2$ the subproblem is solved in closed form. The first order rule picks the maximal violating pair: $i = \arg\max_{t \in I_{up}} -y_t G_t$ and $j = \arg\min_{t \in I_{low}} -y_t G_t$. WSS3 keeps $i$ and picks $j$ to maximize the decrease of the objective in the quadratic model: among $t \in I_{low}$ with $b_t = -y_i G_i + y_t G_t > 0$, it minimizes $-b_t^2 / a_t$ with $a_t = Q_{ii} + Q_{tt} - 2 y_i y_t Q_{it}$. It needs only column $i$ of $Q$, which is already in the cache, and it usually needs fewer iterations than the first order rule. The [support vector machine](/support-vector-machine/) and [support vector regression](/support-vector-regression/) pages implement it.

**Shrinking and caching.** Many variables reach 0 or $C$ early and stay there. Shrinking (Joachims 1999) removes such variables from the working problem when their gradient shows they will most likely stay at the bound, and checks all variables again at the end. A cache of recently used kernel columns, typically managed least recently used, avoids recomputing them.

**Dual coordinate descent.** Without the bias the dual has only box constraints, so one variable can move alone. For variable $i$ the gradient is $G = y_i w \cdot x_i - 1 + D_{ii} \alpha_i$, with $D_{ii} = 0$ for the L1 loss and $1/(2C)$ for the L2 loss, and the exact one-variable minimizer is $\alpha_i \leftarrow \min(\max(\alpha_i - G/\bar Q_{ii}, 0), U)$ with $\bar Q_{ii} = x_i \cdot x_i + D_{ii}$ and $U = C$ or $\infty$. Updating $w$ by $(\Delta \alpha_i) y_i x_i$ keeps the cost at $O(d)$. Hsieh et al. visit the variables in a random order in each pass, stop when the spread of the projected gradients is small, and add shrinking. They prove that the method converges at least linearly.

**Pegasos.** At step $t$ pick a random point (or a batch $A_t$ of $k$ points), set $\eta_t = 1/(\lambda t)$, and update

$$w \leftarrow (1 - \eta_t \lambda) w + \frac{\eta_t}{k} \sum_{i \in A_t, \; y_i w \cdot x_i < 1} y_i x_i,$$

then optionally project $w$ onto the ball of radius $1/\sqrt\lambda$, which contains the optimum. It minimizes $\tfrac\lambda2 \lVert w \rVert^2 + \tfrac1n \sum_i \max(0, 1 - y_i w \cdot x_i)$, the problem above with $C = 1/(\lambda n)$ divided by $Cn$. It reaches an $\varepsilon$ accurate solution with high probability after $\tilde O(1/(\lambda \varepsilon))$ steps, which does not depend on $n$.

## Bounds

- **Polynomial time.** The dual is a convex QP with $n$ variables, so interior point methods solve it to accuracy $\varepsilon$ in polynomial time, roughly $O(n^{3.5} \log(1/\varepsilon))$ arithmetic in the classical analysis.
- **Kernel evaluations.** A solver that computes the full kernel matrix uses $\Theta(n^2)$ evaluations. Under the strong exponential time hypothesis, Backurs, Indyk and Schmidt (2017) showed that a kernel SVM with the Gaussian kernel cannot be solved to high accuracy in time $O(n^{2 - \delta})$ for any $\delta > 0$; see [SETH](/strong-exponential-time-hypothesis/).
- **Decomposition methods.** Every limit point of SMO type methods with the maximal violating pair or WSS3 is optimal, and the stopping rule $m(\alpha) - M(\alpha) \le \varepsilon$ is reached after a finite number of steps. The number of steps can be large when $C$ is large.
- **Linear SVMs.** Dual coordinate descent reaches an $\varepsilon$ accurate dual solution in $O(\log(1/\varepsilon))$ passes, with a constant that depends on the data and grows with $C$. Pegasos needs $\tilde O(1/(\lambda \varepsilon))$ steps of cost $O(d)$ each, independent of $n$.

## Reductions

- **To a QP.** SVM training is a special convex QP, so any QP solver solves it; see [quadratic programming](/quadratic-programming/).
- **Kernel to linear.** An explicit feature map, exact for low degree polynomial kernels or approximate for the Gaussian kernel (random Fourier features, the Nyström method), turns a kernel SVM into a linear SVM, which the fast linear solvers then train.
- **The bias to a feature.** Appending a constant feature $1$ to every $x_i$ gives a bias that is regularized together with $w$, and removes the equality constraint from the dual.
- **Multiclass to binary.** [One-vs-rest](/one-vs-rest/) and [one-vs-one](/one-vs-one/) train several binary SVMs; see [multiclass classification](/multiclass-classification/).
- **From other SVMs.** Support vector regression with $n$ points is a dual of the same form with $2n$ variables, so the same SMO type solver trains it.

## Applications

- **Text categorization.** Linear SVMs on sparse bag-of-words features, with millions of features, trained by dual coordinate descent or Pegasos.
- **Bioinformatics.** Kernel SVMs with string kernels for protein classification and with Gaussian kernels on gene expression data.
- **Vision.** Kernel and linear SVMs on image features, from handwritten digit recognition to object detection with histogram of oriented gradients features.
- **Inner loops.** Structured SVMs, multiple kernel learning and active learning solve many SVM problems, so a fast warm-started solver matters.

## References
