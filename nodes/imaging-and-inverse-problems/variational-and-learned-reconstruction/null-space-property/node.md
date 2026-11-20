---
tag: PPTQNH
kind: definition
slug: null-space-property
name: Null space property
aliases:
- NSP
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: A matrix has the null space property of order s if every null space vector has less L1 mass on any s entries than off them, which is exactly what basis pursuit needs.
prereqs: [sparse-signal-recovery, basis-pursuit]
see_also: [restricted-isometry-property, mutual-coherence, donoho-tanner-phase-transition, compressed-sensing, candes-romberg-tao-theorem, linear-programming-problem, convex-polytope, np-hard]
sources:
  - paper: doi:10.1090/S0894-0347-08-00610-3
    title: Albert Cohen, Wolfgang Dahmen and Ronald DeVore, Compressed sensing and best k-term approximation, Journal of the American Mathematical Society 22(1), 2009
    locator: pages 211 to 231 (the null space property, its name, and its equivalence with instance optimality in l1)
  - paper: doi:10.1109/TIT.2003.820031
    title: Remi Gribonval and Morten Nielsen, Sparse representations in unions of bases, IEEE Transactions on Information Theory 49(12), 2003
    locator: pages 3320 to 3325 (the condition on the null space for l1 minimization to recover every s-sparse vector)
  - paper: doi:10.1109/TIT.2013.2290112
    title: Andreas M. Tillmann and Marc E. Pfetsch, The computational complexity of the restricted isometry property, the nullspace property, and related concepts in compressed sensing, IEEE Transactions on Information Theory 60(2), 2014
    locator: pages 1248 to 1259 (testing the null space property is NP-hard)
  - paper: doi:10.1109/TIT.2013.2288639
    title: T. Tony Cai and Anru Zhang, Sparse representation of a polytope and recovery of sparse signals and low-rank matrices, IEEE Transactions on Information Theory 60(1), 2014
    locator: pages 122 to 132 (delta_2s < 1/sqrt(2) is enough for exact recovery, and the constant is sharp)
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhauser, 2013
    locator: the chapter on basis pursuit (the null space property and its stable and robust forms)
---

The null space property is the exact condition on a matrix $A$ under which $\ell_1$ minimization, [basis pursuit](/basis-pursuit/), recovers every $s$-sparse vector from $y = Ax$. It looks only at the null space of $A$: no nonzero vector that $A$ maps to 0 may put half or more of its $\ell_1$ mass on $s$ entries. It is weaker than the [restricted isometry property](/restricted-isometry-property/), which also gives recovery but is only sufficient, and it is weaker than a bound on the [mutual coherence](/mutual-coherence/), which is cheap to check but gives recovery only for small $s$. Like the restricted isometry property, it is NP-hard to check in general. The [Donoho-Tanner phase transition](/donoho-tanner-phase-transition/) describes for which sizes a random Gaussian matrix has it.

## Definition

Let $A \in \mathbb{R}^{m \times n}$ (or $\mathbb{C}^{m \times n}$) and $1 \le s \le n$. For $S \subseteq \{1, \dots, n\}$ let $v_S$ keep the entries of $v$ in $S$ and set the others to 0, and let $S^c$ be the complement. $A$ has the null space property of order $s$ if

$$\|v_S\|_1 < \|v_{S^c}\|_1 \quad\text{for every } v \in \ker A \setminus \{0\} \text{ and every } S \text{ with } |S| \le s.$$

Adding $\|v_S\|_1$ to both sides gives the equivalent form $\|v_S\|_1 < \tfrac12\|v\|_1$. So with the null space constant

$$\theta_s(A) = \max_{v \in \ker A \setminus \{0\}}\ \max_{|S| \le s}\frac{\|v_S\|_1}{\|v\|_1},$$

the property holds exactly when $\theta_s(A) < \tfrac12$. The inner maximum is the sum of the $s$ largest $|v_i|$. If $A$ is injective, there is no such $v$, and the property holds for every $s$. The property depends only on $\ker A$, so it does not change when $A$ is replaced by $GA$ for an invertible $G$.

**Theorem (Donoho and Huo 2001, Gribonval and Nielsen 2003, Cohen, Dahmen and DeVore 2009).** Every $s$-sparse $x$ is the unique solution of $\min\|z\|_1$ subject to $Az = Ax$ if and only if $A$ has the null space property of order $s$.

*Proof.* Assume the property. Let $x$ have support $S$ with $|S| \le s$, and let $z \ne x$ with $Az = Ax$. Then $v = x - z$ is a nonzero null vector, and

$$\|z\|_1 = \|x_S - v_S\|_1 + \|v_{S^c}\|_1 \ge \|x\|_1 - \|v_S\|_1 + \|v_{S^c}\|_1 > \|x\|_1.$$

Conversely, let $v \in \ker A \setminus \{0\}$ and $|S| \le s$. The vector $x = v_S$ is $s$-sparse and $z = -v_{S^c}$ satisfies $Az = Ax$, because $A(v_S + v_{S^c}) = 0$. Also $z \ne x$, because $v \ne 0$. If $x$ is the unique minimizer, then $\|v_S\|_1 = \|x\|_1 < \|z\|_1 = \|v_{S^c}\|_1$. $\square$

The proof of the converse gives a certificate of failure: if $\|v_S\|_1 \ge \|v_{S^c}\|_1$, the $s$-sparse vector $v_S$ and the vector $-v_{S^c}$ have the same measurements, and the second one has no larger $\ell_1$ norm.

**Stable and robust forms.** $A$ has the stable null space property of order $s$ with constant $0 < \rho < 1$ if $\|v_S\|_1 \le \rho\|v_{S^c}\|_1$ for all $v \in \ker A$ and $|S| \le s$; this is $\theta_s \le \rho/(1 + \rho)$. It gives an error bound for vectors that are only close to sparse: the solution $x^\sharp$ of basis pursuit satisfies $\|x - x^\sharp\|_1 \le \frac{2(1 + \rho)}{1 - \rho}\sigma_s(x)_1$, where $\sigma_s(x)_1$ is the $\ell_1$ error of the best $s$-term approximation of $x$. The robust form adds a term $\tau\|Av\|$ on the right and covers noisy measurements. Cohen, Dahmen and DeVore showed that a bound of this type, called instance optimality in $\ell_1$, holds for some decoder if and only if a null space property of order $2s$ holds.

**Checking it on a small matrix.** The function $v \mapsto \max_{|S| \le s}\|v_S\|_1$ is convex, and the set $\{v \in \ker A : \|v\|_1 \le 1\}$ is a polytope, so the maximum in $\theta_s$ is reached at a vertex of that polytope. A vertex lies in a face of the $\ell_1$ ball with support $T$ and spans the null space of the columns $A_T$, which must then have dimension 1; this needs $|T| \le \operatorname{rank}(A) + 1$. So an exhaustive check is:

```pseudo id=main
NSP-CONSTANT(A, s)
L1  r ← rank(A), θ ← 0
L2  for each set T of at most r + 1 columns
L3      if the null space of A_T has dimension 1 and is spanned by v with support exactly T
L4          θ ← max(θ, (sum of the s largest |v_i|) / ‖v‖₁)
L5  return θ                ▷ the property of order s holds if and only if θ < 1/2
```

The number of sets $T$ grows exponentially with $n$, and this is not an accident: Tillmann and Pfetsch (2014) proved that deciding the null space property is NP-hard when the rational matrix and $s$ are both part of the input. The implementation does the check in exact rational arithmetic, and its tests compare the result with an exhaustive $\ell_1$ minimization over all basic solutions of $Az = y$.

## Examples and non-examples

**A $2 \times 3$ matrix.** Let

$$A = \begin{pmatrix}1 & 0 & 1\\ 0 & 1 & 1\end{pmatrix}.$$

The null space is spanned by $v = (1, 1, -1)$. Every entry has absolute value 1, so one entry carries $\tfrac13$ of the mass and two entries carry $\tfrac23$. So $\theta_1 = \tfrac13 < \tfrac12$ and $A$ has the property of order 1: basis pursuit recovers every 1-sparse vector. But $\theta_2 = \tfrac23$, so the property of order 2 fails. The certificate is $x = v_{\{1,2\}} = (1, 1, 0)$ and $z = -v_{\{3\}} = (0, 0, 1)$: both give $y = (1, 1)$, and $\|z\|_1 = 1 < 2 = \|x\|_1$. Basis pursuit returns $z$, not $x$.

**A row of ones.** $A = (1\ 1\ 1)$ has the null vector $(1, -1, 0)$, with exactly half of its mass on one entry. So $\theta_1 = \tfrac12$ and the property of order 1 fails, at the boundary: $x = e_1$ and $z = e_2$ give the same measurement and the same $\ell_1$ norm, so the minimizer is not unique.

**Identity and Hadamard.** For $A = [\,I \mid \tfrac12H\,]$ in $\mathbb{R}^4$, with the $4 \times 4$ Sylvester Hadamard matrix $H$, the exact check gives $\theta_1 = \tfrac13$ and $\theta_2 = \tfrac12$. So the property of order 1 holds and the property of order 2 fails, again at the boundary: the null vector $(-1, -1, 0, 0, 1, 0, 1, 0)$ says that $e_1 + e_2$ and the sum of the first and third Hadamard columns, $\tfrac12(h_1 + h_3)$, are the same vector.

**Coherence implies the property.** Let the columns have norm 1 and coherence $\mu$. For $v \in \ker A$, the equation $\langle a_i, Av\rangle = 0$ gives $v_i = -\sum_{j \ne i}\langle a_i, a_j\rangle v_j$, so $|v_i| \le \mu(\|v\|_1 - |v_i|)$ and $|v_i| \le \frac{\mu}{1 + \mu}\|v\|_1$. Hence $\theta_s \le \frac{s\mu}{1 + \mu}$, which is below $\tfrac12$ when $(2s - 1)\mu < 1$, the classical coherence condition. In the Hadamard example $\mu = \tfrac12$, the bound gives $\theta_1 \le \tfrac13$, and the exact value is $\tfrac13$.

**Restricted isometry implies the property.** By the theorem above, every condition on $\delta_{2s}$ that gives exact recovery of all $s$-sparse vectors by basis pursuit implies the null space property of order $s$. Cai and Zhang (2014) proved that $\delta_{2s} < 1/\sqrt2$ is enough, and that the constant cannot be improved. The converse is false: the property is invariant under $A \mapsto GA$, and a badly conditioned $G$ can make every restricted isometry constant large without changing the null space.

**Non-example: a sparse null vector.** If some null vector has at most $2s$ nonzero entries, then some $s$ of them carry at least half of its mass, and the property of order $s$ fails. So the property of order $s$ needs $\operatorname{spark}(A) > 2s$, and therefore $m \ge 2s$.

## Related definitions

- **Restricted isometry property.** A condition on all $2s$-column submatrices. It implies the null space property and also stability under noise, and random matrices with $m$ of order $s\log(n/s)$ have it.
- **Mutual coherence.** A cheap sufficient condition, $(2s - 1)\mu < 1$.
- **Spark.** The least number of dependent columns. $\operatorname{spark}(A) > 2s$ is the condition for uniqueness of the sparsest solution, which is necessary for the null space property but not sufficient.
- **Neighborliness.** The property of order $s$ holds if and only if the image $AB_1^n$ of the $\ell_1$ ball, a [convex polytope](/convex-polytope/), is centrally $s$-neighborly: every set of $s$ vertices that does not contain an antipodal pair spans a face. Donoho used this form to count when random matrices have the property; see the [Donoho-Tanner phase transition](/donoho-tanner-phase-transition/).
- **Nonuniform recovery.** Recovery of one fixed $s$-sparse vector, with its sign pattern, needs only a dual certificate for that vector, not the property for all of them. Results such as the [Candes-Romberg-Tao theorem](/candes-romberg-tao-theorem/) are of this kind.

## References
