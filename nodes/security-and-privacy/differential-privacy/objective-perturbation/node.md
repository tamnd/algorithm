---
tag: HFPG7H
kind: algorithm
slug: objective-perturbation
name: Objective perturbation
aliases:
- Chaudhuri-Monteleoni-Sarwate perturbation
area: security-and-privacy/differential-privacy
level: advanced
summary: "Adds a random linear term to a strongly convex empirical risk before minimizing it, which gives differentially private learning."
model: real-ram
complexity:
  vars: {n: the number of examples, d: the dimension, K: the number of solver iterations}
  time: {worst: O(K n d)}
  space: {extra: O(d)}
properties: {deterministic: false, randomized: true}
history:
  year: 2008
  people: [Kamalika Chaudhuri, Claire Monteleoni, Anand D. Sarwate]
  note: "Chaudhuri and Monteleoni (NIPS 2008) introduced it for regularized logistic regression. Chaudhuri, Monteleoni and Sarwate (JMLR 2011) stated it for general convex ERM with a smooth loss as their Algorithm 2 and added the extra regularizer Delta."
prereqs: [output-perturbation, empirical-risk-minimization, convex-function]
see_also: [logistic-regression, laplace-mechanism, gaussian-mechanism, dp-sgd, global-sensitivity, differential-privacy-definition, approximate-differential-privacy, gradient-descent]
sources:
  - url: "https://www.jmlr.org/papers/v12/chaudhuri11a.html"
    title: "Kamalika Chaudhuri, Claire Monteleoni and Anand D. Sarwate, Differentially private empirical risk minimization, Journal of Machine Learning Research 12, 2011, pages 1069 to 1109"
    locator: "Algorithm 2 (Section 3.2) and Theorem 9 (its privacy, with Lemma 10 on the determinant), the logistic loss with c = 1/4, and the comparison with Algorithm 1"
  - paper: "Kamalika Chaudhuri and Claire Monteleoni, Privacy-preserving logistic regression, Advances in Neural Information Processing Systems 21 (NIPS 2008)"
    locator: the new method that perturbs the objective of regularized logistic regression
---

Objective perturbation trains a model privately by changing the training problem, not the trained model. It adds a random linear term $b^{\mathsf T} f / n$ to a strongly convex regularized [empirical risk](/empirical-risk-minimization/), and releases the exact minimizer of the new objective. The noise vector $b$ has a density proportional to $e^{-\beta\|b\|}$. Since the minimizer and the noise determine each other one to one, the density of the output has a closed form, and one example can change it by at most a factor $e^{\varepsilon}$. Chaudhuri and Monteleoni (2008) introduced the method for logistic regression, and Chaudhuri, Monteleoni and Sarwate (2011) stated it for convex losses with a bounded second derivative as their Algorithm 2. For those losses it usually gives better accuracy than [output perturbation](/output-perturbation/) at the same $\varepsilon$.

## In plain words

Output perturbation trains a model and then shakes the result. Objective perturbation shakes the question instead. Before training, it tilts the training goal by a small random amount, and then it trains as usual on the tilted goal.

The tilt is chosen so that any trained model could have come from many different tilts. If one person's data changes, a slightly different tilt gives the same model, and that tilt is almost as likely. So an observer cannot tell whether that person was in the data.

The tilt is divided by the number of examples, so with more data it has less effect on the model.

## The problem

The data is $D = ((x_1, y_1), \ldots, (x_n, y_n))$ with $x_i \in \mathbb R^d$, $\|x_i\| \le 1$ and $y_i \in \{-1, +1\}$. The neighbor relation is replace: $D'$ is $D$ with one example changed, and $n$ is public. The loss $\ell(y f^{\mathsf T} x)$ is convex and twice differentiable with $|\ell'| \le 1$ and $0 \le \ell'' \le c$; the code uses the logistic loss, with $c = 1/4$. The goal is an $\varepsilon$-[DP](/differential-privacy-definition/) vector $f$ with a small regularized risk

$$J_D(f) = \frac1n \sum_{i=1}^n \ell(y_i f^{\mathsf T} x_i) + \frac{\Lambda}{2}\|f\|^2.$$

## The algorithm

```pseudo id=main
OBJECTIVE-PERTURBATION(D, Lambda, epsilon, c)
L1  epsilon' <- epsilon - ln(1 + 2c/(n Lambda) + c^2/(n^2 Lambda^2))
L2  if epsilon' > 0 then Delta <- 0
L3  else Delta <- c / (n (e^(epsilon/4) - 1)) - Lambda;  epsilon' <- epsilon / 2
L4  b <- a vector with density proportional to exp(-(epsilon'/2) |b|)
L5  f_priv <- argmin over f of J_D(f) + (1/n) b.f + (Delta/2) |f|^2
L6  return f_priv
```

Lines L1 to L3 split the budget $\varepsilon$ between two sources of privacy loss. The noise term pays $\varepsilon'$. The curvature of the loss pays the rest: one example changes the Hessian of the objective by a rank-one matrix, and that changes the density of the output by the factor $\ln(1 + c/(n\Lambda))$ or less. Line L1 reserves twice that factor, as in the analysis of Chaudhuri, Monteleoni and Sarwate. When $n\Lambda$ is too small for that, $\varepsilon'$ is not positive, and line L3 adds the extra regularizer $\Delta > 0$, chosen so that the curvature part costs at most $\varepsilon/2$ and the noise gets the other half.

Line L4 draws the noise as in output perturbation: the norm is a sum of $d$ exponential draws of rate $\beta = \varepsilon'/2$ and the direction is uniform. Line L5 is a normal training run. The objective is $(\Lambda + \Delta)$-strongly convex, so the minimizer is unique; the code finds it by [gradient descent](/gradient-descent/) with the step $1/(1/4 + \Lambda + \Delta)$ and stops at a gradient norm of $10^{-11}$. The noise in line L5 enters through its gradient: the minimizer is the point where the gradient of $J_D + (\Delta/2)\|f\|^2$ equals $-b/n$.

The code uses floats and a seeded generator, so it shows the algorithm but is not a safe deployment. The analysis assumes exact real noise and an exact minimizer, and floating-point samplers can leak (Mironov 2012). A deployment needs a cryptographic source of randomness and samplers built for DP, such as the [discrete Gaussian](/discrete-gaussian-mechanism/) for the Gaussian variant.

## Example

Take the data of the output perturbation page: $n = 4$ examples in the plane, $\Lambda = 0.5$ and $\varepsilon = 1$.

| $i$ | $x_i$ | $y_i$ |
|---|---|---|
| 1 | (0.6, 0.8) | +1 |
| 2 | (1, 0) | +1 |
| 3 | (-0.6, 0) | -1 |
| 4 | (0, -1) | -1 |

Line L1 gives $\varepsilon' = 1 - 2\ln 1.125 = 0.7644$, so line L2 sets $\Delta = 0$, and line L4 uses $\beta = 0.3822$. With the seed 9 the code draws $b = (1.8363, 2.1787)$, of norm $2.8494$. Line L5 then gives $f_{\mathrm{priv}} = (-0.2786, -0.5192)$, against the non-private minimizer $(0.4368, 0.3532)$. With four examples the tilt $b/n$ is large, and the model even changes sign.

Replace example 4 by $((0, 1), -1)$. On a grid of models $f$, the largest log ratio of the two output densities is $0.3822$, below $\varepsilon = 1$. The table shows the budget split for other settings, with $c = 1/4$.

| $n$ | $\Lambda$ | $\varepsilon$ | branch | $\varepsilon'$ | $\Delta$ |
|---|---|---|---|---|---|
| 4 | 0.5 | 1 | L2 | 0.7644 | 0 |
| 4 | 0.05 | 0.5 | L3 | 0.25 | 0.4194 |
| 1000 | 0.01 | 0.1 | L2 | 0.0506 | 0 |
| 1000 | 0.001 | 0.1 | L3 | 0.05 | 0.0089 |

## Correctness

**Theorem (Chaudhuri, Monteleoni and Sarwate, Theorem 9).** Lines L1 to L6 are $\varepsilon$-DP under replace.

The proof has three steps. First, for each $b$ the objective has one minimizer, and $b$ can be recovered from it: $b = b_D(f) = -n(\nabla J_D(f) + \Delta f)$. So $f \mapsto b_D(f)$ is a bijection, and the change of variables formula gives the output density $p_D(f) = \nu(b_D(f)) \det A_D(f)$, where $A_D(f) = \sum_i \ell''(y_i f^{\mathsf T} x_i) x_i x_i^{\mathsf T} + n(\Lambda + \Delta) I$. Second, one example changes $b_D(f)$ by a vector of norm at most 2, since $|\ell'| \le 1$, so the factor $\nu$ changes by at most $e^{2\beta} = e^{\varepsilon'}$. Third, one example changes $A_D(f)$ by a rank-one term, and the matrix determinant lemma bounds the ratio of the determinants by $1 + c/(n(\Lambda + \Delta))$. Lines L1 to L3 make the two factors multiply to at most $e^{\varepsilon}$.

The correctness proof of this page gives all the steps. It bounds the determinant ratio by one factor of $1 + c/(n(\Lambda + \Delta))$, which is sharper than the squared factor of the paper, so the algorithm as stated has some slack. The tests check the minimizer against bisection in one dimension, the recovery of $b$ from the output, the density formula against the exact law in one dimension, and the density ratio on a grid in both branches.

## Complexity

The model is the [real RAM](/real-ram/), with one exponential or Gaussian draw counted as $O(1)$.

- **Training.** One gradient costs $O(nd)$. The objective of line L5 is $(\Lambda + \Delta)$-strongly convex and $(c + \Lambda + \Delta)$-smooth, so gradient descent needs $K = O((1 + c/(\Lambda + \Delta)) \ln(1/t))$ steps to reach the gradient norm $t$, and line L5 costs $O(Knd)$.
- **The rest.** Lines L1 to L3 cost $O(1)$ and line L4 costs $O(d)$.
- **Space.** The extra space is $O(d)$ beyond the data.

The cost is the cost of one non-private training run.

## Properties

- **Pure DP.** The guarantee is $\varepsilon$-DP with $\delta = 0$, under replace neighbors with a public $n$.
- **Needs a smooth loss.** The proof needs $\ell''$ to exist and be bounded. The logistic loss and the Huber loss qualify; the hinge loss of the standard support vector machine does not. Chaudhuri, Monteleoni and Sarwate use a Huber version of the SVM for this reason.
- **Needs the exact minimizer.** The density formula holds only for the exact minimizer of line L5. A solver that stops early, or a constrained problem, changes the output law and is not covered.
- **Better accuracy than output perturbation.** Chaudhuri, Monteleoni and Sarwate prove bounds on the number of examples needed for a given generalization error, and the bound for objective perturbation is smaller than the bound for output perturbation. Their experiments on real data show the same order.
- **The regularizer is part of the privacy.** $\Lambda$ must be fixed in advance. Picking it on the private data leaks, and the paper gives a private tuning method that uses held-out parts of the data.

## Variants and improvements

- **Gaussian noise.** Kifer, Smith and Thakurta (2012) gave an $(\varepsilon, \delta)$ version with Gaussian noise and support for convex constraints and some non-smooth regularizers. Its noise norm grows like $\sqrt d$, not $d$.
- **Approximate minimizers.** Iyengar et al. (2019) studied versions that allow an approximate solver for line L5, at the cost of extra noise on the output.
- **Other regularizers.** The analysis of Chaudhuri, Monteleoni and Sarwate allows any 1-strongly convex, twice differentiable regularizer $N(f)$ in place of $\|f\|^2/2$.
- **Kernels.** The paper also handles kernel methods by first mapping the data to random features, then running objective perturbation on them.
- **No convexity.** For non-convex models, [DP-SGD](/dp-sgd/) is the usual choice.

## When to use it

Use objective perturbation for a convex model with a smooth loss and an $L_2$ regularizer, such as regularized [logistic regression](/logistic-regression/), when a pure $\varepsilon$ guarantee is required and the solver can reach the minimizer to high precision. It usually beats output perturbation in accuracy. Use output perturbation when the training code cannot be changed, and DP-SGD when the model is not convex or the data is too large to solve to high precision.

## Pitfalls

- **Skipping the budget split.** Line L4 with $\beta = \varepsilon/2$ in place of $\varepsilon'/2$ ignores the loss through the determinant, and the result is not $\varepsilon$-DP. Lines L1 to L3 must run, and line L4 must use $\varepsilon'$.
- **A negative budget.** Line L2 run when $\varepsilon' \le 0$ gives a noise rate of zero or below, which has no meaning. Line L3 must replace $\varepsilon'$ by $\varepsilon/2$ and add $\Delta$ in that case.
- **Forgetting the extra regularizer.** Line L5 without the term $(\Delta/2)\|f\|^2$ after line L3 has set $\Delta > 0$ breaks the bound of the determinant. Line L5 must use the same $\Delta$.
- **Scaling the noise wrong.** Line L5 with the term $b^{\mathsf T} f$ in place of $b^{\mathsf T} f / n$ uses an objective whose risk part has a different scale from the one in the analysis. Keep the factor $1/n$ that matches $J_D$, or rescale both.
- **A non-smooth loss.** Line L5 with the hinge loss has no bounded $\ell''$, and the determinant bound fails. Use a smooth loss, such as the Huber loss, with its $c$ in line L1.
- **Early stopping.** Line L5 run for a fixed small number of steps does not return the minimizer that the proof needs. Run the solver to a tight tolerance, or use a variant built for approximate solvers.

## Implementations

## History

Chaudhuri and Monteleoni (NIPS 2008) studied private logistic regression. They bounded the sensitivity of the regularized minimizer for output perturbation, and they introduced objective perturbation as a new method with better accuracy. Chaudhuri, Monteleoni and Sarwate (JMLR 2011) extended it to convex losses with a bounded second derivative, added the extra regularizer $\Delta$ for small $n\Lambda$, gave a private method to tune $\Lambda$, extended it to kernels, and compared both methods on real data. Kifer, Smith and Thakurta (2012) extended it to constraints and to Gaussian noise.

## References
