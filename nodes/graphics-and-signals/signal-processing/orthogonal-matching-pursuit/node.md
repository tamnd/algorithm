---
tag: DHYVW6
kind: algorithm
slug: orthogonal-matching-pursuit
name: Orthogonal matching pursuit
aliases:
- OMP
area: graphics-and-signals/signal-processing
level: advanced
summary: Greedy selection of columns with orthogonal residual projection.
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {m: the number of measurements, n: the number of columns, s: the number of steps}
  time: {worst: Θ(s m n), average: Θ(s m n), best: Θ(m n)}
  space: {extra: Θ(m s)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true}
history:
  year: 1993
  people: [Yagyensh Pati, Ramin Rezaiifar, P. S. Krishnaprasad, Stéphane Mallat, Zhifeng Zhang]
  note: Pati, Rezaiifar and Krishnaprasad (1993) added a least squares refit to each step of matching pursuit, which Mallat and Zhang (1993) had introduced. Tropp (2004) gave exact recovery conditions.
prereqs: [sparse-signal-recovery, least-squares-problem, greedy-algorithm]
see_also: [basis-pursuit, restricted-isometry-property, iterative-shrinkage-thresholding, compressed-sensing, gram-schmidt-process, qr-decomposition, normal-equations, lasso-regression]
sources:
  - paper: doi:10.1109/ACSSC.1993.342465
    title: Y. C. Pati, R. Rezaiifar and P. S. Krishnaprasad, Orthogonal matching pursuit, recursive function approximation with applications to wavelet decomposition, Proceedings of the 27th Asilomar Conference on Signals, Systems and Computers, 1993
    locator: pages 40 to 44 (the algorithm, with an orthogonal projection at each step, and its finite convergence)
  - paper: doi:10.1109/78.258082
    title: Stéphane G. Mallat and Zhifeng Zhang, Matching pursuits with time-frequency dictionaries, IEEE Transactions on Signal Processing 41(12), 1993
    locator: pages 3397 to 3415 (matching pursuit without the refit, over dictionaries of Gabor atoms)
  - paper: doi:10.1109/TIT.2004.834793
    title: Joel A. Tropp, Greed is good, algorithmic results for sparse approximation, IEEE Transactions on Information Theory 50(10), 2004
    locator: pages 2231 to 2242, Section 3 (the exact recovery condition, sufficient for both orthogonal matching pursuit and basis pursuit, and the coherence bound that implies it)
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhäuser, 2013
    locator: Chapter 3 (orthogonal matching pursuit) and Chapter 5 (recovery under a coherence condition)
---

Orthogonal matching pursuit (OMP) builds the support of a sparse solution of $Ax = y$ one column at a time. At each step it adds the column most correlated with the current residual, then refits all chosen coefficients by [least squares](/least-squares-problem/), so the new residual is orthogonal to every chosen column. After $s$ steps it has an $s$-sparse approximation, and when the columns are incoherent enough, $\mu < 1/(2s - 1)$, it finds the support of every $s$-sparse vector exactly. It is a fast [greedy method](/greedy-algorithm/) for [sparse signal recovery](/sparse-signal-recovery/), and it neither dominates nor is dominated by [basis pursuit](/basis-pursuit/).

## In plain words

You want to explain a measurement as a mix of only a few known patterns. Start with the whole measurement as the part still to explain. Find the pattern that best matches that part, and add it to your chosen set. Then find the best mix of all the chosen patterns at once, and see what part of the measurement is still left over. Repeat with the leftover part.

Because the mix is redone each time, the leftover part has nothing in common with the patterns already chosen, so the same pattern is never chosen twice. Stop after a fixed number of patterns, or when nothing is left over. If the patterns are different enough from each other, each choice is a correct one, and the method ends with exactly the right patterns.

## The problem

**Input.** A matrix $A \in \mathbb R^{m \times n}$ with nonzero columns $a_1, \ldots, a_n$, a vector $y \in \mathbb R^m$, a number of steps $s \le m$, and a tolerance $\tau \ge 0$ for the squared residual.

**Output.** A support list $S$ in the order of selection, with $|S| \le s$, and a vector $x$ that is zero off $S$ and minimizes $\|Ax - y\|_2$ among such vectors.

**Goal.** For $y = Ax_0$ with $x_0$ $s$-sparse, return $S = \operatorname{supp}(x_0)$ and $x = x_0$.

**Cost model.** The [real RAM](/real-ram/). For rational data, exact rational arithmetic gives the exact choices and coefficients.

## The algorithm

```pseudo id=main
OMP(A, y, s, τ)
L1  r ← y; S ← the empty list
L2  repeat s times, and stop early when ‖r‖² ≤ τ:
L3      j ← the index not in S with the largest ⟨a_j, r⟩² / ‖a_j‖²     ▷ the smallest index on ties
L4      append j to S
L5      x_S ← argmin_z ‖A_S z − y‖₂                                     ▷ least squares on the chosen columns
L6      r ← y − A_S x_S
L7  return (x, S), with x zero off S
```

Line L3 compares squared correlations divided by squared column norms, which is the same as comparing $|\langle a_j, r \rangle| / \|a_j\|_2$ but needs no square root. Line L5 refits every chosen coefficient, not only the new one. This is the "orthogonal" in the name: plain matching pursuit only adds the new coefficient $\langle a_j, r \rangle / \|a_j\|_2^2$ and keeps the old ones, so it can pick the same column again.

## Example

**A one-step stop.** Let $A = \begin{pmatrix} 1 & 0 & 1 \\ 0 & 1 & 1 \end{pmatrix}$ and $y = (2, 2)$, with $s = 2$. The scores of line L3 are $4$, $4$ and $\tfrac{16}{2} = 8$, so OMP picks column $3$. The least squares fit gives $x_3 = 2$ and $r = 0$, so the loop stops after one step with $x = (0, 0, 2)$.

**Success where basis pursuit fails.** Let the columns be

$$a_1 = \tfrac19(7, 4, 4), \quad a_2 = \tfrac17(-3, 2, 6), \quad a_3 = \tfrac19(1, 8, 4), \quad a_4 = \tfrac19(8, 1, -4),$$

all of norm $1$, and $x_0 = (2, -1, 0, 0)$, so $y = \tfrac1{63}(125, 38, 2)$.

| step | correlations $\langle a_j, r \rangle$ for $j = 1, 2, 3, 4$ | choice | residual $r$ after the refit |
|---|---|---|---|
| 1 | $\tfrac{1035}{567}, -\tfrac{41}{63}, \tfrac{437}{567}, \tfrac{1030}{567}$ | $a_1$ | $\tfrac1{567}(320, -118, -442)$ |
| 2 | $0, -\tfrac{3848}{3969}, -\tfrac{2392}{5103}, \tfrac{4210}{5103}$ | $a_2$ | $0$ |

The first choice is close: $1035$ against $1030$. At step 2 the correlation with $a_1$ is $0$, because the residual is orthogonal to the chosen column. The refit on $\{a_1, a_2\}$ gives $x_0$ exactly. Basis pursuit, on the same data, returns a denser vector with smaller $\ell_1$ norm (see its page).

**Failure where basis pursuit succeeds.** Let the columns be $e_1, e_2, e_3$ and $w = \tfrac1{11}(6, 6, 7)$, and $x_0 = e_1 + e_2$, so $y = (1, 1, 0)$. Step 1 scores $1, 1, 0, \tfrac{144}{121}$, so OMP picks $w$, which is wrong. The residual is $\tfrac1{121}(49, 49, -84)$, and step 2 picks $e_3$, since $\tfrac{84}{121} > \tfrac{49}{121}$. The fit on $\{w, e_3\}$ gives $x = (0, 0, -\tfrac76, \tfrac{11}6)$, which solves $Ax = y$ but is not $x_0$. Here $\mu = \tfrac7{11}$, so the coherence condition fails even for $s = 1$.

## Correctness

Two facts carry the proof, which is given in full below.

**The residual is orthogonal to the chosen columns.** Line L5 solves the normal equations $A_S^{\mathsf T}(A_S x_S - y) = 0$, so $A_S^{\mathsf T} r = 0$ after line L6. So chosen columns score $0$ on line L3, and a column is never chosen twice while $r \ne 0$.

**Each step picks a correct column.** Let the columns have norm $1$, let $x_0$ have support $T$ with $|T| \le s$, and let $\mu < 1/(2s - 1)$. If $S \subseteq T$, the residual $r = y - A_S x_S$ lies in the span of the columns in $T$, so $r = A_T c$ for some $c$. Let $k \in T$ have $|c_k| = \|c\|_\infty$. Then

$$|\langle a_k, r \rangle| \ge |c_k| - \sum_{j \in T, j \ne k} \mu |c_j| \ge \big(1 - (s - 1)\mu\big)\|c\|_\infty, \qquad |\langle a_i, r \rangle| \le s\mu \|c\|_\infty \text{ for } i \notin T.$$

Since $1 - (s - 1)\mu > s\mu$ exactly when $(2s - 1)\mu < 1$, the best score is in $T$. By induction, after $|T|$ steps $S = T$, the residual is $0$, and the fit is $x_0$, since the columns in $T$ are independent. With $\tau = 0$ the loop then stops. Tropp (2004) proves the sharper exact recovery condition $\max_{i \notin T} \|A_T^{+} a_i\|_1 < 1$, which the coherence bound implies.

## Complexity

Line L3 computes $A^{\mathsf T} r$ in $\Theta(mn)$ time. If line L5 keeps a QR factorization of $A_S$ and adds one column per step by [Gram-Schmidt](/gram-schmidt-process/) orthogonalization, the refit costs $O(mk)$ at step $k$, and line L6 costs $O(mk)$. So $s$ steps take $\Theta(smn)$ time, with $\Theta(ms)$ extra space for the factors. Solving the [normal equations](/normal-equations/) from scratch at each step, as a short reference code does, costs $O(mk^2 + k^3)$ at step $k$, which is still small next to $mn$ when $s$ is small. If $A$ has a fast transform, such as a partial Fourier or wavelet matrix, line L3 costs the time of that transform. The best case is one step, when $y$ is a multiple of one column.

## Properties

- **Finite.** At most $s \le m$ steps, and with $\tau = 0$ and $Ax = y$ solvable, at most $m$ steps reach $r = 0$.
- **Monotone residual.** Each refit is over a larger set of columns, so $\|r\|_2$ never grows.
- **No repeats.** The residual is orthogonal to the chosen columns, so they score $0$ and are not chosen again while $r \ne 0$.
- **Needs the sparsity or a tolerance.** OMP must be told when to stop: after $s$ steps, or when $\|r\|_2^2 \le \tau$. Basis pursuit needs neither.
- **Guarantees with random matrices.** With a random Gaussian $A$ and a fixed $x_0$, OMP succeeds with high probability when $m$ is of order $s \log n$. A guarantee for every $s$-sparse vector at once through the [restricted isometry property](/restricted-isometry-property/) needs $\delta_{s+1}$ below a bound of order $1/\sqrt s$, which is stronger than the condition for basis pursuit.
- **Scale.** Line L3 divides by the column norms, so the choice does not depend on the scale of each column.

## Variants and improvements

- **Matching pursuit.** No refit: add $\langle a_j, r \rangle / \|a_j\|^2$ to $x_j$ and subtract that multiple of $a_j$ from $r$. Each step is cheaper, but columns repeat and convergence is slower.
- **Orthogonal least squares.** Choose the column that gives the smallest residual after the refit, not the largest correlation. This costs more per step and differs when the columns are far from orthogonal.
- **Stagewise OMP.** Add all columns whose correlation passes a threshold at once, which needs fewer steps.
- **CoSaMP and subspace pursuit.** Add $2s$ or $s$ candidates, refit, then keep the best $s$. These can remove wrong choices and have guarantees under the restricted isometry property that hold for every sparse vector.
- **Simultaneous OMP.** For several measurement vectors with a common support, score each column by the sum of its correlations.
- **Weak selection.** Accept any column whose score is within a factor of the best. This keeps the guarantees with a stronger condition and allows approximate search over very large dictionaries.

## When to use it

Use OMP when the sparsity is small and known, or when a residual tolerance is natural, and when speed matters more than the last bit of recovery power. It is simple, has no parameters to tune beyond the stopping rule, and only needs products with $A^{\mathsf T}$ and small least squares solves. It is a standard step in dictionary learning, where it is run on many signals. For noisy data or larger sparsity, [basis pursuit](/basis-pursuit/) or the [lasso](/lasso-regression/) usually recovers more, and CoSaMP gives stronger uniform guarantees.

## Pitfalls

- **One bad pick is permanent.** OMP never removes a column. A wrong first choice, as in the failure example, leaves a wrong support.
- **Unnormalized columns.** Without the division by $\|a_j\|^2$, a column with a large norm wins too often.
- **Stopping rule.** Too few steps miss part of the support. Too many steps fit the noise and add wrong columns. With noise, stop at a residual near the noise level.
- **Ill-conditioned refit.** If two chosen columns are nearly parallel, the least squares step is unstable. Use QR updates, not the normal equations, in floating point.
- **Ties.** With exact arithmetic, ties in line L3 do occur. Fix a rule, such as the smallest index, so that runs are repeatable.

## Implementations

## History

Mallat and Zhang (1993) introduced matching pursuit for adaptive time-frequency decompositions over dictionaries of Gabor atoms. In the same year, Pati, Rezaiifar and Krishnaprasad (1993) added the orthogonal projection at each step, which makes the method converge in a finite number of steps, and applied it to wavelet decompositions. Similar forward selection methods with refits had long been used in statistics for regression. Tropp (2004) gave the exact recovery condition, which is sufficient for both OMP and basis pursuit, and showed that the coherence bound $\mu < 1/(2s - 1)$ implies it. Later work studied OMP with random measurement matrices.

## References
