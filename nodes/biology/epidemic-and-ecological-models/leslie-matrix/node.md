---
tag: V3XCAW
kind: model
slug: leslie-matrix
name: Leslie matrix
aliases:
- Leslie matrix model
area: biology/epidemic-and-ecological-models
level: core
summary: An age-structured population model n_(t+1) = L n_t with fertilities in the first row and survival rates below the diagonal.
history:
  year: 1945
  people: [Patrick H. Leslie]
  note: Leslie set out the matrix form of the age-structured population model and its stable age distribution in 1945.
prereqs: [eigenvalue, perron-frobenius-theorem]
see_also: [power-iteration, characteristic-polynomial, next-generation-matrix, galton-watson-process, matrix-power, markov-chain, logistic-map, ricker-model]
sources:
  - paper: doi:10.1093/biomet/33.3.183
    title: "P. H. Leslie, On the use of matrices in certain population mathematics, Biometrika 33(3), 1945"
    locator: "pages 183 to 212 (the matrix of fertilities and survival rates, its latent roots and the stable age distribution)"
  - book: isbn:9780878930968
    title: "Hal Caswell, Matrix Population Models, Construction, Analysis, and Interpretation, 2nd ed., Sinauer Associates, 2001"
    locator: "the chapters on age-classified models, on the growth rate and stable structure, and on sensitivity analysis"
---

The Leslie matrix model follows a population that is divided into age classes. The vector $n_t = (n_{1,t}, \ldots, n_{k,t})$ holds the number of individuals in each of $k$ age classes at census $t$, and one step is $n_{t+1} = L n_t$. The first row of $L$ holds the fertilities $F_i$, the number of newborns per individual of class $i$ that enter class 1 at the next census. The subdiagonal holds the survival rates $P_i$, the chance that an individual of class $i$ lives to class $i + 1$. Leslie (1945) set out this matrix form and showed that the long-run growth rate and the stable age distribution are the dominant [eigenvalue](/eigenvalue/) and eigenvector of $L$. Because $L$ is nonnegative, the [Perron-Frobenius theorem](/perron-frobenius-theorem/) tells when this dominant eigenvalue exists and when every start converges to the stable distribution.

## The machine

**The state.** A vector $n_t \in \mathbb{R}_{\ge 0}^k$. The entry $n_{i,t}$ is the number of individuals, usually females only, in age class $i$ at census $t$. Each class is one time step wide, so class $i$ holds the individuals of age $i - 1$ to $i$ steps.

**The parameters.** The fertilities $F_1, \ldots, F_k \ge 0$, in newborns per individual per step, counted as the newborns that are alive at the next census. The survival rates $P_1, \ldots, P_{k-1} \in (0, 1]$, with no unit. The survivorship to class $i$ is $l_1 = 1$ and $l_i = P_1 P_2 \cdots P_{i-1}$.

**The update rule.** $n_{t+1} = L n_t$ with

$$L = \begin{pmatrix} F_1 & F_2 & \cdots & F_{k-1} & F_k \\ P_1 & 0 & \cdots & 0 & 0 \\ 0 & P_2 & \cdots & 0 & 0 \\ \vdots & & \ddots & & \vdots \\ 0 & 0 & \cdots & P_{k-1} & 0 \end{pmatrix},$$

that is, $n_{1,t+1} = \sum_i F_i n_{i,t}$ and $n_{i+1,t+1} = P_i n_{i,t}$.

**The assumptions.** The rates are constant in time and do not depend on the density, so the model is linear. The population is closed. No individual lives past class $k$. The model is deterministic: it gives expected numbers. The value of $F_i$ depends on when the census is taken relative to the breeding season, and it must include the survival of the newborns to the next census.

```pseudo id=main
PROJECT(F, P, n_0, T)
L1  n ← n_0
L2  for t ← 1 to T do
L3      n ← (F_1 n_1 + ... + F_k n_k, P_1 n_1, ..., P_(k-1) n_(k-1))      that is, n ← L n
L4      record n_t ← n
L5  return n_1, ..., n_T
```

Line L3 uses the structure of $L$: it costs $\Theta(k)$ per step, not the $\Theta(k^2)$ of a general matrix times a vector. So $T$ steps cost $\Theta(kT)$.

## What it counts

- The vector $n_t$ and the total population $N_t = \sum_i n_{i,t}$.
- The asymptotic growth rate $\lambda_1$ per step, the dominant eigenvalue of $L$. The population grows when $\lambda_1 > 1$ and declines when $\lambda_1 < 1$.
- The stable age distribution $w$, the right eigenvector of $\lambda_1$, scaled to sum 1.
- The reproductive values $v$, the left eigenvector of $\lambda_1$, scaled so that $v_1 = 1$. The value $v_i$ is the relative contribution of one individual of class $i$ to the future population.
- The net reproductive rate $R_0 = \sum_i F_i l_i$, the expected number of offspring of a newborn over its whole life.
- The generation time $\bar T = \sum_i i F_i l_i \lambda_1^{-i}$, the mean age of the mothers of the newborns in the stable population.
- The damping ratio $\lambda_1 / |\lambda_2|$, which sets how fast the age structure approaches $w$.
- The sensitivities $s_{ij} = \partial \lambda_1 / \partial L_{ij}$ and the elasticities $e_{ij} = (L_{ij} / \lambda_1) s_{ij}$.

## Relation to other models

- **[Power iteration](/power-iteration/).** Projecting the population is power iteration on $L$. The ratio $N_{t+1}/N_t$ tends to $\lambda_1$, and $n_t / N_t$ tends to $w$, at the rate $|\lambda_2 / \lambda_1|^t$.
- **[Characteristic polynomial](/characteristic-polynomial/).** For a Leslie matrix it has a closed form, $\lambda^k - \sum_i F_i l_i \lambda^{k-i}$, so the growth rate is the root of one equation in one unknown.
- **[Next-generation matrix](/next-generation-matrix/).** Both models have a threshold at 1. For the Leslie model, $R_0 = \sum_i F_i l_i$ is the next-generation count of newborns per newborn, and $\lambda_1 > 1$ exactly when $R_0 > 1$.
- **[Galton-Watson process](/galton-watson-process/).** In a branching process with several types, where an individual of class $i$ has a random number of offspring with mean $F_i$ and survives with probability $P_i$, the expected numbers follow the Leslie model, by linearity of expectation.
- **[Markov chain](/markov-chain/).** The survival part of $L$ is the transition matrix of the life of one individual, with death as an absorbing state. Its columns sum to less than 1.
- **[Matrix power](/matrix-power/).** $n_t = L^t n_0$. Repeated squaring gives $L^t$ in $O(k^3 \log t)$ operations, which helps for large $t$ and exact rational entries.
- **[Logistic map](/logistic-map/) and [Ricker model](/ricker-model/).** These models have one class but density dependence. If the fertilities of the Leslie model fall with the density, the age-structured model can also have cycles and chaos (heuristic).

## Known results in the model

**The characteristic equation (theorem).** $\det(\lambda I - L) = \lambda^k - \sum_{i=1}^{k} F_i l_i \lambda^{k-i}$. For $\lambda \ne 0$ the equation $\det(\lambda I - L) = 0$ is the Euler-Lotka equation $\sum_i F_i l_i \lambda^{-i} = 1$. If some $F_i > 0$, it has exactly one positive root, and the eigenvector of this root is $w_i \propto l_i \lambda^{-(i-1)}$.

*Proof.* Expand $\det(\lambda I - L)$ along the first row. If row 1 and column $i$ are removed, the rest is block diagonal with two triangular blocks, with $-P_1, \ldots, -P_{i-1}$ and then $k - i$ copies of $\lambda$ on the diagonal. So the minor is $(-1)^{i-1} l_i \lambda^{k-i}$, and with the sign $(-1)^{1+i}$ of the cofactor the expansion is $\lambda \cdot \lambda^{k-1} - \sum_i F_i l_i \lambda^{k-i}$. Division by $\lambda^k$ gives the Euler-Lotka form. For the eigenvector, suppose $L w = \lambda w$ with $\lambda \ne 0$. The rows 2 to $k$ give $w_{i+1} = P_i w_i / \lambda$, so $w_i = l_i \lambda^{-(i-1)} w_1$. The function $\varphi(\lambda) = \sum_i F_i l_i \lambda^{-i}$ is strictly decreasing on $(0, \infty)$ from $+\infty$ to 0, so it takes the value 1 exactly once. $\square$

**The threshold (theorem).** $\lambda_1 > 1$ if and only if $R_0 > 1$, and $\lambda_1 = 1$ if and only if $R_0 = 1$.

*Proof.* $\varphi(1) = R_0$ and $\varphi$ is decreasing, so its root lies above 1 exactly when $\varphi(1) > 1$. $\square$

**Perron-Frobenius for Leslie matrices (theorem and known result).** If $F_k > 0$, then $L$ is irreducible: every class leads to every other class. By the Perron-Frobenius theorem, $\lambda_1$ is then positive and simple, no other eigenvalue has a larger modulus, and $w$ and $v$ are positive. If $L$ is also primitive, then $|\lambda_j| < \lambda_1$ for every other eigenvalue and, for every nonzero $n_0 \ge 0$, $n_t / \lambda_1^t \to (v^\top n_0 / v^\top w)\, w$ (theorem). It is a known result that an irreducible Leslie matrix is primitive exactly when the [greatest common divisor](/greatest-common-divisor/) of the ages $i$ with $F_i > 0$ is 1. In particular, two adjacent fertile classes are enough.

**Sensitivity and elasticity (theorem).** $\partial \lambda_1 / \partial L_{ij} = v_i w_j / (v^\top w)$, and the elasticities sum to 1.

*Proof.* Differentiate $L w = \lambda_1 w$ and multiply on the left by $v^\top$. The terms with the derivative of $w$ cancel because $v^\top L = \lambda_1 v^\top$, which leaves $v^\top (\partial L) w = (\partial \lambda_1)\, v^\top w$. The sum of the elasticities is $\sum_{ij} L_{ij} v_i w_j / (\lambda_1 v^\top w) = v^\top L w / (\lambda_1 v^\top w) = 1$. $\square$

**An example with three classes.** Take $F = (0, 1.5, 1.0)$ and $P = (0.5, 0.25)$, so

$$L = \begin{pmatrix} 0 & 1.5 & 1.0 \\ 0.5 & 0 & 0 \\ 0 & 0.25 & 0 \end{pmatrix}, \qquad l = (1, 0.5, 0.125).$$

The characteristic equation is $\lambda^3 - 0.75 \lambda - 0.125 = 0$. Multiplied by 4 it is $4\lambda^3 - 3\lambda = 0.5$, and with $\lambda = \cos\theta$ the identity $4\cos^3\theta - 3\cos\theta = \cos 3\theta$ gives $\cos 3\theta = 1/2$. So the eigenvalues are $\cos(\pi/9) = 0.939693$, $\cos(7\pi/9) = -0.766044$ and $\cos(13\pi/9) = -0.173648$ (theorem). The net reproductive rate is $R_0 = 0.75 + 0.125 = 0.875 < 1$, and as the threshold theorem says, $\lambda_1 < 1$: the population declines by about 6 percent per step. The fertile ages are 2 and 3 with greatest common divisor 1, so $L$ is primitive.

- The stable age distribution is $w = (0.597497, 0.317922, 0.084581)$.
- The reproductive values are $v = (1, 1.879385, 1.064178)$. An individual of class 2 is worth almost two newborns, because it is about to breed and a newborn may die first.
- The generation time is $\bar T = 2.150644$ steps.
- The elasticities of $\lambda_1$ are $0.464977$ for $P_1$, $0.394931$ for $F_2$, and $0.070046$ for both $F_3$ and $P_2$. So a given relative change in the survival of the young changes the growth rate most.
- The damping ratio is $0.939693 / 0.766044 = 1.226682$.

From $n_0 = (100, 0, 0)$ the projection gives:

| $t$ | $n_{1,t}$ | $n_{2,t}$ | $n_{3,t}$ | $N_t$ |
|---|---|---|---|---|
| 1 | 0 | 50 | 0 | 50 |
| 2 | 75 | 0 | 12.5 | 87.5 |
| 3 | 12.5 | 37.5 | 0 | 50 |
| 4 | 56.25 | 6.25 | 9.375 | 71.875 |
| 5 | 18.75 | 28.125 | 1.5625 | 48.4375 |

The total oscillates because $\lambda_2 = -0.766044$ is negative and not much smaller than $\lambda_1$ in modulus. The oscillation dies out only by a factor of about $1.23$ per step.

**An imprimitive example (theorem).** Take $F = (0, 0, 6)$ and $P = (1/2, 1/3)$. Then $L^3 = F_3 P_1 P_2 I = I$, so the population repeats with period 3 and never reaches a stable distribution: $(6, 0, 0)$, $(0, 3, 0)$, $(0, 0, 1)$, $(6, 0, 0)$, and so on. Here $R_0 = 1$, $\lambda_1 = 1$, and the other two eigenvalues are the complex cube roots of 1, with the same modulus.

**Slow convergence near an imprimitive matrix (measurement).** In a random test with six classes, $F = (0, 2.481212, 0, 0.603468, 0.973731, 2.571316)$ and $P = (0.739222, 0.363252, 0.069093, 0.588705, 0.566179)$, the matrix is primitive, since the fertile ages 2, 4, 5 and 6 have greatest common divisor 1. But the odd ages add very little, and after 2000 steps the ratio $N_{t+1}/N_t$ was $1.369866$, still $0.7$ percent away from $\lambda_1 = 1.359817$. For such matrices, solve the Euler-Lotka equation, for example by the [bisection method](/bisection-method/), in place of projection.

## References
