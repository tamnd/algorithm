---
tag: 4VE8QP
kind: theorem
slug: lll-approximation-guarantee
name: LLL approximation guarantee
aliases:
- LLL approximation bound
- LLL bounds on reduced bases
area: number-theory/lattice-reduction
level: advanced
summary: The first LLL vector is within 2^((n-1)/2) of the shortest lattice vector.
prereqs: [lll-reduction, successive-minima, lattice-determinant]
see_also: [lll-algorithm, approximate-svp, hermite-constant, root-hermite-factor, babai-nearest-plane, minkowski-theorem, minkowski-second-theorem, bkz-algorithm]
sources:
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: Section 1 (the bounds on the vectors of a reduced basis in terms of the determinant and of the lengths of independent lattice vectors, with the constant 2 for delta = 3/4)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 2, Approximation algorithms (the approximation factor of LLL for SVP for a general parameter delta)
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (LLL as an algorithmic version of Hermite's inequality)
---

The LLL approximation guarantee bounds the vectors of an [LLL-reduced basis](/lll-reduction/) against the [successive minima](/successive-minima/) and the [determinant](/lattice-determinant/) of the lattice. For the classical parameter $\delta = 3/4$, the first vector satisfies $\|b_1\| \le 2^{(n-1)/2} \lambda_1$ and $\|b_1\| \le 2^{(n-1)/4} \det(L)^{1/n}$. Since the [LLL algorithm](/lll-algorithm/) computes such a basis in polynomial time, this solves [approximate SVP](/approximate-svp/) within an exponential factor, which is enough for many applications in algebra and cryptanalysis.

## Statement

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n$ of a lattice $L$ of rank $n$, [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors $b_i^*$, $B_i = \|b_i^*\|^2$, coefficients $\mu_{ij}$, successive minima $\lambda_1 \le \cdots \le \lambda_n$, determinant $\det(L)$ and the parameter $\delta$. Let $\alpha = 1 / (\delta - 1/4)$; so $\alpha = 2$ for $\delta = 3/4$, and $\alpha \to 4/3$ as $\delta \to 1$.

**Theorem.** Let $1/4 < \delta \le 1$ and let $b_1, \ldots, b_n$ be a $\delta$-LLL-reduced basis of $L$, that is, $|\mu_{ij}| \le 1/2$ for all $j < i$ and $\delta B_{k-1} \le B_k + \mu_{k,k-1}^2 B_{k-1}$ for all $k \ge 2$. Then

1. $\|b_1\| \le \alpha^{(n-1)/4} \det(L)^{1/n}$;
2. $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1(L)$;
3. $\|b_j\| \le \alpha^{(n-1)/2} \lambda_i(L)$ for all $1 \le j \le i \le n$;
4. $\prod_{i=1}^n \|b_i\| \le \alpha^{n(n-1)/4} \det(L)$.

More generally, in item 2 the factor bounds $\|b_1\|$ against every nonzero lattice vector, and in item 3 against any $i$ independent lattice vectors: if $x_1, \ldots, x_i \in L$ are independent, then $\|b_j\| \le \alpha^{(n-1)/2} \max_l \|x_l\|$ for $j \le i$.

## In plain words

An LLL-reduced basis is not the best basis, but it cannot be very bad. Its first vector is at most a fixed factor longer than the shortest vector of the lattice, and the factor depends only on the dimension. It doubles, roughly, every two dimensions for the usual setting, so it grows quickly, but it never depends on the size of the numbers in the input.

The same holds for every basis vector compared with the matching minimum, and for the product of all their lengths compared with the volume of a cell. All of this comes from one fact: in a reduced basis, the length of each new perpendicular direction is at least a fixed fraction of the previous one.

## Proof

**Step 1: the Gram-Schmidt lengths fall slowly.** From the two conditions, $B_k \ge (\delta - \mu_{k,k-1}^2) B_{k-1} \ge (\delta - \frac14) B_{k-1} = B_{k-1} / \alpha$. By induction, $B_j \le \alpha^{i-j} B_i$ for $j \le i$.

**Step 2: each basis vector is close to its Gram-Schmidt vector.** By orthogonality, $|\mu_{ij}| \le 1/2$ and Step 1,

$$\|b_i\|^2 = B_i + \sum_{j < i} \mu_{ij}^2 B_j \le B_i \Big(1 + \frac14 \sum_{t=1}^{i-1} \alpha^t\Big) = B_i \Big(1 + \frac{\alpha^i - \alpha}{4 (\alpha - 1)}\Big) \le \alpha^{i-1} B_i.$$

The last inequality, multiplied by $4 (\alpha - 1) > 0$, reads $3\alpha - 4 \le \alpha^{i-1} (3 \alpha - 4)$, which holds because $\alpha \ge 4/3$ and $\alpha^{i-1} \ge 1$. Combining with Step 1, for $j \le i$,

$$\|b_j\|^2 \le \alpha^{j-1} B_j \le \alpha^{j-1} \alpha^{i-j} B_i = \alpha^{i-1} B_i. \tag{$*$}$$

**Item 1.** By $(*)$ with $j = 1$, $\|b_1\|^2 \le \alpha^{i-1} B_i$ for every $i$. Multiply over $i = 1, \ldots, n$: $\|b_1\|^{2n} \le \alpha^{0 + 1 + \cdots + (n-1)} \prod_i B_i = \alpha^{n(n-1)/2} \det(L)^2$. Take the $2n$-th root.

**Item 4.** By Step 2, $\prod_i \|b_i\|^2 \le \prod_i \alpha^{i-1} B_i = \alpha^{n(n-1)/2} \det(L)^2$.

**Item 3 and the general form.** Let $x_1, \ldots, x_i \in L$ be independent. They do not all lie in $\operatorname{span}(b_1, \ldots, b_{i-1})$, which has dimension $i - 1$. So one of them, $x = \sum_{t \le k} c_t b_t$ with integers $c_t$ and $c_k \ne 0$, has $k \ge i$. Its component along $b_k^*$ is $c_k b_k^*$, so $\|x\|^2 \ge c_k^2 B_k \ge B_k$. For $j \le i \le k$, $(*)$ gives

$$\|b_j\|^2 \le \alpha^{k-1} B_k \le \alpha^{n-1} \|x\|^2 \le \alpha^{n-1} \max_l \|x_l\|^2.$$

Taking for $x_1, \ldots, x_i$ independent vectors of length at most $\lambda_i$, which exist by the definition of $\lambda_i$, gives item 3.

**Item 2.** This is item 3 with $i = j = 1$; the general form with $i = 1$ says $\|b_1\| \le \alpha^{(n-1)/2} \|x\|$ for every nonzero $x \in L$. $\blacksquare$

## Consequences

- **Approximate SVP in polynomial time.** The [LLL algorithm](/lll-algorithm/) returns a vector within $2^{(n-1)/2}$ of $\lambda_1$, and within $(4/3 + \varepsilon)^{(n-1)/2}$ for $\delta$ close to 1, in polynomial time. This solves [approximate SVP](/approximate-svp/) for exponential factors, and with item 3, the [shortest independent vectors problem](/shortest-independent-vectors-problem/) within the same factor.
- **Hermite's inequality.** Every lattice has a basis that is $\delta$-LLL-reduced for $\delta = 1$: an [HKZ-reduced basis](/hkz-reduction/) is one, since each $b_{k-1}^*$ is a shortest vector of a projected lattice that contains $\pi_{k-1}(b_k)$. Item 1 with $\alpha = 4/3$ then gives $\lambda_1 \le (4/3)^{(n-1)/4} \det(L)^{1/n}$, that is, $\gamma_n \le (4/3)^{(n-1)/2}$ for the [Hermite constant](/hermite-constant/). This is Hermite's bound of 1850; LLL can be seen as an algorithmic, relaxed version of Hermite's proof.
- **Babai's algorithms.** The analysis of [Babai's nearest plane](/babai-nearest-plane/) method uses Step 1 and gives a CVP approximation factor of $2^{n/2}$ on an LLL-reduced basis with $\delta = 3/4$.
- **Algebra.** Item 3 is the form that Lenstra, Lenstra and Lovász used to [factor polynomials over the integers](/polynomial-factorization-over-integers/): a short vector of a lattice built from a factor of the polynomial modulo $p^k$ reveals the factor over the integers.
- **Small roots.** Item 1, the bound against the determinant, is the one used in [Coppersmith's method](/coppersmith-method/), where the determinant of the lattice is known and $\lambda_1$ is not.
- **Better factors.** Block reductions such as [BKZ](/bkz-algorithm/) with block size $\beta$ replace the base $\alpha$ by one that depends on $\beta$ and tends to 1 as $\beta$ grows, at a cost exponential in $\beta$, and Schnorr's hierarchy of block reductions reaches factors $2^{O(n (\log \log n)^2 / \log n)}$ in polynomial time.

## Tightness

- **Item 1 is tight.** Fix $B_1 > 0$ and take orthogonal vectors $b_1^*, \ldots, b_n^*$ with $B_{i+1} = (\delta - \frac14) B_i$. Put $b_1 = b_1^*$ and $b_{i+1} = b_{i+1}^* + \frac12 b_i^*$. Then $\mu_{i+1,i} = 1/2$, all other $\mu_{ij} = 0$, and $B_{i+1} + \frac14 B_i = \delta B_i$, so the basis is $\delta$-LLL-reduced with equality in every Lovász condition. Here $\det(L)^2 = \prod_i B_i = B_1^n \alpha^{-n(n-1)/2}$, so $\|b_1\| = \sqrt{B_1} = \alpha^{(n-1)/4} \det(L)^{1/n}$ exactly. For $\delta = 3/4$ and $n = 3$, $B = (1, 1/2, 1/4)$ and $\det(L)^2 = 1/8$, so $\alpha^{(n-1)/2} \det(L)^{2/n} = 2 \cdot \frac12 = 1 = \|b_1\|^2$.
- **Item 2 is exponential but not known to be tight.** In the same lattice, $\lambda_1 \le \sqrt{\gamma_n} \det(L)^{1/n} \le \sqrt n \det(L)^{1/n}$ by [Minkowski's theorem](/minkowski-theorem/), so $\|b_1\| / \lambda_1 \ge \alpha^{(n-1)/4} / \sqrt{\gamma_n}$: the worst case ratio of an LLL-reduced basis grows at least like $\alpha^{n/4}$, an exponential, but this only shows the square root of the factor of item 2.
- **Item 2 is not tight in dimension 2.** For $n = 2$ and $\delta \ge 1/3$, every $\delta$-LLL-reduced basis has $\lambda_1^2 \ge \delta \|b_1\|^2$. Indeed, let $x = c_1 b_1 + c_2 b_2 \ne 0$. If $c_2 = 0$, $\|x\|^2 \ge B_1$; if $|c_2| = 1$, $\|x\|^2 \ge \mu_{21}^2 B_1 + B_2 = \|b_2\|^2 \ge \delta B_1$ by the Lovász condition, and if $|c_2| \ge 2$, $\|x\|^2 \ge 4 B_2 \ge 4 (\delta - \frac14) B_1 \ge \delta B_1$. For $\delta = 3/4$ the true worst factor $\|b_1\|^2 / \lambda_1^2$ is thus at most $4/3$, not $\alpha = 2$; it is reached by $b_1 = (1, 0)$, $b_2 = (1/2, 1/\sqrt 2)$, with $\lambda_1^2 = \|b_2\|^2 = 3/4$.
- **In practice.** On random lattices LLL behaves as if $\alpha^{1/4}$ in item 1 were about $1.02$ instead of $2^{1/4} \approx 1.19$; see [root Hermite factor](/root-hermite-factor/). This is an experimental observation, not a theorem.

## History

Hermite proved in 1850 that every lattice has a nonzero vector with $\lambda_1 \le (4/3)^{(n-1)/4} \det(L)^{1/n}$, by an induction on the dimension that is close to the reduction behind LLL. Lenstra, Lenstra and Lovász (1982) relaxed his notion of reduction with the factor $3/4$, proved the bounds above with the constant $2$, and showed that the relaxed reduction can be computed in polynomial time. The form with a general $\delta$ and $\alpha = 1/(\delta - 1/4)$ is standard in later texts, such as Micciancio and Goldwasser.

## References
