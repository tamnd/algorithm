---
tag: ATATC2
kind: concept
slug: root-hermite-factor
name: Root Hermite factor
aliases:
- root-Hermite factor delta
- Hermite factor
- root Hermite factor delta_0
area: number-theory/lattice-reduction
level: advanced
summary: Constant delta such that a reduced basis first vector has length about delta to the n times det^(1/n).
prereqs: [lattice-determinant, hermite-constant, lll-approximation-guarantee]
see_also: [lll-algorithm, bkz-algorithm, gaussian-heuristic, approximate-svp, lattice-based-cryptography, short-integer-solution, learning-with-errors, unique-svp]
sources:
  - paper: "Nicolas Gama and Phong Q. Nguyen, Predicting lattice reduction, Advances in Cryptology, Eurocrypt 2008, LNCS 4965"
    locator: pages 31 to 51 (the Hermite factor as the measure of reduction quality, and the experimental root Hermite factors of about 1.0219 for LLL and 1.0128 for BKZ-20 on random lattices)
  - paper: "Yuanmi Chen and Phong Q. Nguyen, BKZ 2.0, better lattice security estimates, Advances in Cryptology, Asiacrypt 2011, LNCS 7073"
    locator: the simulation of BKZ for large block sizes from the Gaussian heuristic, and the resulting root Hermite factors
  - paper: "Daniele Micciancio and Oded Regev, Lattice-based cryptography, in Post-Quantum Cryptography, Springer, 2009"
    locator: the section on attacks (security estimates from the root Hermite factor and the optimal subdimension for SIS)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (Hermite SVP and the proved factors of LLL and block reductions)
---

The root Hermite factor $\delta_0$ measures how good a reduced basis is: its first vector has length $\|b_1\| = \delta_0^n \det(L)^{1/n}$ in a lattice of rank $n$. The quantity $\delta_0^n$ is the Hermite factor. For a fixed reduction algorithm on random lattices, $\delta_0$ is observed to be nearly a constant that does not depend on $n$: about $1.0219$ for [LLL](/lll-algorithm/) and $1.0128$ for [BKZ](/bkz-algorithm/) with block size 20. This makes it the standard way to predict what a lattice attack can achieve, and so to choose parameters in [lattice-based cryptography](/lattice-based-cryptography/).

## In plain words

Every lattice has a typical length set by the size of its cells: the volume of one cell, spread evenly over all the directions. A reduction algorithm returns a short vector, and we compare its length with this typical length. The ratio grows with the dimension, roughly by the same factor each time one more dimension is added.

That factor per dimension is the root Hermite factor. A value close to 1 means a strong reduction. Experiments show that each algorithm has its own value, almost the same for all random inputs of all sizes. So one number describes the algorithm, and it predicts how short a vector it will find in a new lattice before running it.

## The idea

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n$ of a lattice $L$ of rank $n$, Gram-Schmidt vectors $b_i^*$, first minimum $\lambda_1$, determinant $\det(L)$, and the LLL parameter $\delta$. To keep $\delta$ for LLL, we write $\delta_0$ for the root Hermite factor, as is common in the literature.

**Definition.** For a basis $b_1, \ldots, b_n$ of $L$,

$$\text{Hermite factor} = \frac{\|b_1\|}{\det(L)^{1/n}}, \qquad \delta_0 = \left( \frac{\|b_1\|}{\det(L)^{1/n}} \right)^{1/n}.$$

The root Hermite factor of an algorithm is the value of $\delta_0$ for its output, either as a proved worst-case bound or as the typical value on a class of random lattices. The task "find a nonzero $v \in L$ with $\|v\| \le \gamma \det(L)^{1/n}$" is called Hermite SVP, a variant of [approximate SVP](/approximate-svp/) where the target is the determinant instead of $\lambda_1$; the Hermite factor is its approximation factor.

**Why it is measured against the determinant.** The determinant can be computed from any basis, while $\lambda_1$ is hard to compute. And for random lattices the [Gaussian heuristic](/gaussian-heuristic/) gives $\lambda_1 \approx \sqrt{n / (2 \pi e)} \det(L)^{1/n}$, so the Hermite factor and the ratio $\|b_1\| / \lambda_1$ differ by a factor of order $\sqrt n$, which changes $\delta_0$ only by a factor $n^{1/(2n)} \to 1$.

**Proved values.**

- *LLL.* By the [LLL approximation guarantee](/lll-approximation-guarantee/), $\|b_1\| \le \alpha^{(n-1)/4} \det(L)^{1/n}$ with $\alpha = 1 / (\delta - 1/4)$, so $\delta_0 \le \alpha^{1/4}$: $2^{1/4} \approx 1.189$ for $\delta = 3/4$, $1.078$ for $\delta = 0.99$, and close to $(4/3)^{1/4} \approx 1.075$ as $\delta \to 1$.
- *The limit of any method.* A shortest vector has $\lambda_1 \le \sqrt{\gamma_n} \det(L)^{1/n}$, with $\gamma_n$ the [Hermite constant](/hermite-constant/), and $\gamma_n \le n$. So an exact SVP solver reaches $\delta_0 \le \gamma_n^{1/(2n)}$, which tends to 1.

**Observed values (heuristic).** Gama and Nguyen ran LLL and BKZ on many random lattices in dimensions up to a few hundred and found that $\delta_0$ is almost independent of $n$ and of the input distribution: about $1.0219$ for LLL and $1.0128$ for BKZ-20, with larger block sizes giving smaller values at a cost that grows quickly. These are measurements, not theorems; the proved LLL bound is much weaker. For large block sizes $\beta$, the BKZ simulation of Chen and Nguyen, based on the Gaussian heuristic for the projected blocks, gives the estimate

$$\delta_0 \approx \left( \frac{\beta}{2 \pi e} (\pi \beta)^{1/\beta} \right)^{1/(2(\beta - 1))},$$

which is used for $\beta$ above about 50 and is inaccurate for small $\beta$: at $\beta = 20$ it gives $1.0096$, below the observed $1.0128$.

**The shape of the basis.** Experiments also show that the Gram-Schmidt lengths of a reduced random basis decrease roughly geometrically, $\|b_{i+1}^*\| / \|b_i^*\| \approx r$ for a constant $r$ (the geometric series assumption). Since $\prod_i \|b_i^*\| = \det(L)$, this gives $\|b_1\| \approx r^{-(n-1)/2} \det(L)^{1/n}$, so $r \approx \delta_0^{-2}$ for large $n$. The geometric series assumption is a heuristic; it is used to predict the success of [Babai's nearest plane](/babai-nearest-plane/) method, of enumeration and of attacks on [unique SVP](/unique-svp/).

## Examples

- **Small dimension.** The LLL output $(0, 1, 0), (1, 0, 1), (-2, 0, 1)$ of a lattice with $\det(L) = 3$ has Hermite factor $1 / 3^{1/3} \approx 0.693$ and $\delta_0 \approx 0.885 < 1$. In small dimension $\delta_0$ says little; it is meant for large $n$, where the observed values are stable.
- **LLL in dimension 200.** With $\delta_0 = 1.0219$, LLL is expected to find $\|b_1\| \approx 1.0219^{200} \det(L)^{1/n} \approx 76 \det(L)^{1/n}$. The proved bound for $\delta = 0.99$ is $\alpha^{199/4} \approx 3.2 \times 10^6$ times $\det(L)^{1/n}$. By the Gaussian heuristic a shortest vector has length about $3.42 \det(L)^{1/n}$, which corresponds to $\delta_0 \approx 1.0062$.
- **BKZ-20 in dimension 200.** With $\delta_0 = 1.0128$, the prediction is $1.0128^{200} \approx 12.7$ times $\det(L)^{1/n}$, six times shorter than LLL.
- **An SIS estimate.** For the [short integer solution](/short-integer-solution/) lattice $\{x \in \mathbb{Z}^m : A x \equiv 0 \pmod q\}$ with $A \in \mathbb{Z}_q^{n \times m}$ of full rank, $\det = q^n$. A reduction with root Hermite factor $\delta_0$ applied to a sublattice of dimension $m$ finds a vector of length about $\delta_0^m q^{n/m}$. This is smallest at $m = \sqrt{n \log_2 q / \log_2 \delta_0}$, where it equals $2^{2 \sqrt{n \log_2 q \log_2 \delta_0}}$. For $n = 256$, $q = 7681$ and $\delta_0 = 1.0128$, the best $m$ is about 424 and the length about $4.9 \times 10^4$; with $\delta_0 = 1.005$, it is about 860. A scheme is secure against this attack if its SIS bound is below the length that feasible values of $\delta_0$ reach.

## Where it is used

- **Comparing reduction algorithms.** [LLL](/lll-algorithm/), [deep LLL](/deep-lll/) and [BKZ](/bkz-algorithm/) are compared by their observed $\delta_0$ against their running time.
- **Security estimates.** Parameters for [LWE](/learning-with-errors/), [SIS](/short-integer-solution/) and [NTRU](/ntru-encrypt/) schemes are chosen so that the $\delta_0$ needed for an attack would require a block size whose cost is out of reach.
- **[Unique SVP](/unique-svp/).** Gama and Nguyen also observed that lattice reduction finds the unique shortest vector when the gap $\lambda_2 / \lambda_1$ exceeds a constant fraction of the Hermite factor $\delta_0^n$.
- **[Gaussian heuristic](/gaussian-heuristic/) and [Hermite constant](/hermite-constant/).** They give the target value: no basis can do better than $\lambda_1$, and for random lattices $\lambda_1$ itself has $\delta_0 \approx (n / (2 \pi e))^{1/(2n)}$.

## References
