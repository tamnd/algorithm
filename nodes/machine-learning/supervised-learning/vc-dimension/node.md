---
tag: 08SW3R
kind: concept
slug: vc-dimension
name: VC dimension
aliases:
- Vapnik-Chervonenkis dimension
- shattering dimension
area: machine-learning/supervised-learning
level: advanced
summary: "The size of the largest set of points on which a binary hypothesis class realizes all labelings. It is finite exactly when the class is PAC learnable."
prereqs: [hypothesis-class, pac-learning]
see_also: [sauer-shelah-lemma, fundamental-theorem-of-statistical-learning, epsilon-net-theorem, range-space, radon-theorem, halfspace-learning, rademacher-complexity, margin-generalization-bound]
sources:
  - paper: doi:10.1137/1116025
    title: V. N. Vapnik and A. Ya. Chervonenkis, On the uniform convergence of relative frequencies of events to their probabilities, Theory of Probability and Its Applications 16(2), 1971
    locator: pp. 264 to 280 (the growth function, the index of a class, and uniform convergence)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Chapter 6 (Sections 6.2 and 6.3, shattering and the examples of thresholds, intervals, rectangles, finite classes and the sine class; Theorem 6.6), Section 9.1.3 (Theorems 9.2 and 9.3, halfspaces)
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Section 3.3 (VC dimension, with Theorem 3.13, Radon's theorem, for halfspaces)
  - paper: doi:10.1145/76359.76371
    title: A. Blumer, A. Ehrenfeucht, D. Haussler and M. K. Warmuth, Learnability and the Vapnik-Chervonenkis dimension, Journal of the ACM 36(4), 1989
    locator: pp. 929 to 965 (finite VC dimension characterizes PAC learnability)
---

The VC dimension of a binary [hypothesis class](/hypothesis-class/) $H$ is the size of the largest finite set of points that $H$ *shatters*: on that set, every one of the $2^k$ ways to label the points with 0 and 1 is the restriction of some $h \in H$. Vapnik and Chervonenkis introduced it in 1971 to bound uniform convergence of frequencies to probabilities. Blumer, Ehrenfeucht, Haussler and Warmuth (1989) showed that it decides [PAC learnability](/pac-learning/): a class is learnable exactly when its VC dimension $d$ is finite, and then, for a fixed confidence, on the order of $d/\varepsilon$ examples are needed and $O(d \ln(1/\varepsilon)/\varepsilon)$ are enough (realizable), and on the order of $d/\varepsilon^2$ are needed and enough (agnostic). The number counts capacity, not parameters: halfspaces in $\mathbb{R}^d$ have VC dimension $d + 1$, and a class with one real parameter can have infinite VC dimension.

## In plain words

Put some points on the table. The class "shatters" them if, for any way you colour the points black and white, some rule in the class gives exactly that colouring. A class that can do this for very many points can fit any pattern on them, including noise, so a fit on that many points proves nothing. The VC dimension is the largest number of points the class can shatter. If it is small, any data set much larger than it is a real test of the class, and good training accuracy then predicts good accuracy on new data. If it is infinite, no amount of data is enough.

## The idea

**Shattering.** Let $H$ be a set of functions $X \to \{0, 1\}$ and let $C = (c_1, \ldots, c_k)$ be points of $X$. The restriction of $H$ to $C$ is $H_C = \{(h(c_1), \ldots, h(c_k)) : h \in H\}$. The class shatters $C$ when $|H_C| = 2^k$.

**Definition.** $\mathrm{VC}(H)$ is the largest $k$ such that some set of $k$ points is shattered by $H$. If sets of every size are shattered, $\mathrm{VC}(H) = \infty$. To prove $\mathrm{VC}(H) = d$, show two things: *some* set of $d$ points is shattered, and *no* set of $d + 1$ points is shattered. One bad set of size $d$ proves nothing.

**Growth function.** $\tau_H(n) = \max_{|C| = n} |H_C|$ counts the most labelings $H$ realizes on $n$ points. $\tau_H(n) = 2^n$ for $n \le \mathrm{VC}(H)$. The [Sauer-Shelah lemma](/sauer-shelah-lemma/) shows that past the VC dimension the growth is polynomial: $\tau_H(n) \le \sum_{i=0}^{d} \binom{n}{i} \le (en/d)^d$ for $n \ge d$. This is the step that turns a finite VC dimension into a finite effective size of the class on a sample, and so into a bound of the form "$L_D(h) - L_S(h) \le O(\sqrt{(d \ln(n/d) + \ln(1/\delta))/n})$ for all $h \in H$".

**Simple facts.**

- A subset of a shattered set is shattered. So the sizes of shattered sets form an interval $\{0, 1, \ldots, d\}$.
- If $H \subseteq H'$ then $\mathrm{VC}(H) \le \mathrm{VC}(H')$.
- If $H$ is finite, shattering $k$ points needs $2^k$ different functions, so $\mathrm{VC}(H) \le \lfloor \log_2 |H| \rfloor$.
- The complement class $\{1 - h : h \in H\}$ has the same VC dimension.

**Brute force on a finite domain.** If $X$ is a finite set of points $P$ and there is a test that says whether some $h \in H$ gives labels $y$ to points $C$, the VC dimension on $P$ is found by search.

```pseudo id=main
VC-DIMENSION(P, REALIZABLE)                   ▷ REALIZABLE(C, y): some h in H gives labels y to C
L1  best ← 0
L2  for k = 1, 2, …, |P| do
L3      found ← false
L4      for each set C of k points of P do
L5          if REALIZABLE(C, y) for all y in {0, 1}^k then found ← true   ▷ C is shattered
L6      if not found then return best         ▷ no larger set can be shattered either
L7      best ← k
L8  return best
```

Line L6 uses the first simple fact. The search makes at most $\sum_{k \le d+1} \binom{|P|}{k} 2^k$ calls of the test, so it is practical only for small $P$. The implementation uses exact tests: an interval or a rectangle test by the bounding box of the points labelled 1, and for halfspaces a feasibility test of the system $y_i(\langle w, x_i \rangle + b) \ge 1$ by Fourier-Motzkin elimination over the rationals. Computing the VC dimension of a finite class given as a table is not known to be in polynomial time; the brute force above takes time $|P|^{O(\log |H|)}$, since $d \le \log_2 |H|$.

## Examples

| Class | VC dimension | Shattered set | Why no larger set |
|---|---|---|---|
| thresholds $1[x \ge t]$ on $\mathbb{R}$ | 1 | any one point | labels $(1, 0)$ on $a < b$ |
| intervals $1[a \le x \le b]$ | 2 | any two points | labels $(1, 0, 1)$ on $a < b < c$ |
| axis aligned rectangles in $\mathbb{R}^2$ | 4 | a diamond | the extreme point argument |
| halfspaces $1[\langle w, x \rangle + b \ge 0]$ in $\mathbb{R}^d$ | $d + 1$ | $0, e_1, \ldots, e_d$ | Radon's theorem |
| homogeneous halfspaces in $\mathbb{R}^d$ | $d$ | $e_1, \ldots, e_d$ | Shalev-Shwartz and Ben-David, Theorem 9.2 |
| finite class | at most $\lfloor \log_2 \lvert H \rvert \rfloor$ | | counting |
| $1[\sin(\theta x) > 0]$, $\theta \in \mathbb{R}$ | $\infty$ | $10^{-1}, \ldots, 10^{-k}$ | |

**Intervals.** Two points $a < b$ get the labels $(0, 0)$ from an empty interval, $(1, 0)$ and $(0, 1)$ from a small interval around one point, and $(1, 1)$ from $[a, b]$. For three points $a < b < c$, an interval that contains $a$ and $c$ contains $b$, so $(1, 0, 1)$ is missing.

**Rectangles.** The four points $(1, 0), (-1, 0), (0, 1), (0, -1)$ are shattered: for any subset, the bounding box of that subset contains no other of the four points. Now take any five points. Choose a point with the least $x$, one with the largest $x$, one with the least $y$ and one with the largest $y$. These are at most four points, so some fifth point $p$ is not among them. Label the chosen points 1 and $p$ with 0. Every rectangle that contains the chosen points contains their bounding box, and $p$ lies in that box. So no five points are shattered.

**Halfspaces.** *Lower bound.* For labels $y_0, \ldots, y_d$ of the points $0, e_1, \ldots, e_d$, take $w_i = 1$ if $y_i = 1$ and $w_i = -1$ otherwise, and $b = 1/2$ if $y_0 = 1$ and $b = -1/2$ otherwise. Then $\langle w, e_i \rangle + b = w_i + b$ is positive exactly when $y_i = 1$, and the value $b$ at 0 is positive exactly when $y_0 = 1$. *Upper bound.* By [Radon's theorem](/radon-theorem/), any $d + 2$ points of $\mathbb{R}^d$ split into two sets $A$ and $B$ whose [convex hulls](/convex-hull/) meet. Label $A$ with 1 and $B$ with 0. A halfspace that contains $A$ contains its convex hull, and the open complement that contains $B$ contains the convex hull of $B$. Both sets cannot hold the common point. See [linear separability](/linear-separability/) and [halfspace learning](/halfspace-learning/).

**The sine class.** Let $x_i = 10^{-i}$ for $i = 1, \ldots, k$, and let $y_1, \ldots, y_k$ be labels. Take $\theta = \pi\big(1 + \sum_{i : y_i = 0} 10^i\big)$. Then for each $j$,
$$\frac{\theta x_j}{\pi} = \sum_{i > j,\ y_i = 0} 10^{i - j} \;+\; 1[y_j = 0] \;+\; \Big(10^{-j} + \sum_{i < j,\ y_i = 0} 10^{i - j}\Big).$$
The first sum is an even integer. The last bracket is at least $10^{-j} > 0$ and less than $1/10 + 1/9 < 1$. So $\lfloor \theta x_j/\pi \rfloor$ is even when $y_j = 1$ and odd when $y_j = 0$, and $\theta x_j$ is not a multiple of $\pi$. Hence $\sin(\theta x_j) > 0$ exactly when $y_j = 1$. Every $k$ points of this form are shattered, so the class of one real parameter has infinite VC dimension. For labels $(1, 0, 0, 1)$ this gives $\theta = 1101\pi$.

**Exact checks.** The implementation finds, by the brute force search with exact arithmetic, VC dimension 2 for intervals on $\{0, \ldots, 5\}$; 4 for rectangles on a grid of 12 points, with no 5-point subset shattered; 2, 3 and 4 for halfspaces with bias on small point sets in $\mathbb{R}^1$, $\mathbb{R}^2$ and $\mathbb{R}^3$; and 2 for homogeneous halfspaces in the plane. In the plane, the four corners of a square with labels 1 on one diagonal and 0 on the other (the XOR pattern) are not realizable, as Radon's theorem says. On random finite classes the VC dimension never exceeds $\lfloor \log_2 |H| \rfloor$, and the sine witness shatters $10^{-1}, \ldots, 10^{-k}$ for $k = 1, \ldots, 6$.

**Conjunctions.** Conjunctions of literals over $\{0, 1\}^d$ have VC dimension $d$, although there are $3^d + 1$ of them, so the counting bound gives only $\lfloor \log_2(3^d + 1) \rfloor$, about $1.58d$.

## Where it is used

- **Characterization of learnability.** The [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/) says that for binary classes under the 0-1 loss, uniform convergence, agnostic PAC learnability, PAC learnability and finite VC dimension are equivalent, with sample sizes $\Theta((d + \ln(1/\delta))/\varepsilon)$ up to a $\ln(1/\varepsilon)$ factor for ERM in the realizable case, and $\Theta((d + \ln(1/\delta))/\varepsilon^2)$ in the agnostic case. A class of infinite VC dimension is not PAC learnable (Shalev-Shwartz and Ben-David, Theorem 6.6).
- **Lower bounds.** A shattered set of size $d$ carries a uniform distribution on which any learner can be fooled, which gives the $d/\varepsilon$ and $d/\varepsilon^2$ lower bounds; see the [no-free-lunch theorem](/no-free-lunch-theorem-learning/).
- **Model selection.** [Structural risk minimization](/structural-risk-minimization/) penalizes each class in a nested family by its VC dimension.
- **Geometry.** A binary class is a [range space](/range-space/), and the VC dimension of a range space bounds the size of $\varepsilon$-nets by the [$\varepsilon$-net theorem](/epsilon-net-theorem/). This drives random sampling algorithms in computational geometry.
- **Other capacity measures.** The [Rademacher complexity](/rademacher-complexity/) of a class of VC dimension $d$ is $O(\sqrt{d \ln(n/d)/n})$ by Massart's lemma and the Sauer-Shelah lemma. For real valued classes the fat-shattering dimension at scale $\gamma$ plays the role of the VC dimension, and gives the [margin bound](/margin-generalization-bound/). For multiclass labels the Natarajan dimension is used, and for online learning the Littlestone dimension, which can be infinite when the VC dimension is 1 (thresholds on $[0, 1]$).

## References
