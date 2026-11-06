---
tag: DQAC4V
kind: definition
slug: lovasz-condition
name: Lovász condition
aliases:
- Lovász exchange condition
- Lovász criterion
area: number-theory/lattice-reduction
level: advanced
summary: Inequality between consecutive Gram-Schmidt norms that triggers a swap in LLL.
prereqs: [gram-schmidt-orthogonalization, lattice-basis, size-reduction]
see_also: [lll-reduction, lll-algorithm, lll-approximation-guarantee, deep-lll, lagrange-gauss-reduction, hkz-reduction, bkz-algorithm]
sources:
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982
    locator: Section 1 (condition (1.5) with the constant 3/4, and the remark that any constant between 1/4 and 1 can be used)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 2, Approximation algorithms (the LLL reduced basis, with the condition written through projections)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 17, Lattice basis reduction (the Lovász condition and the effect of a swap on the Gram-Schmidt vectors)
---

The Lovász condition at index $k$ says that swapping the basis vectors $b_{k-1}$ and $b_k$ would not shorten the Gram-Schmidt vector $b_{k-1}^*$ by more than a factor $\delta$, a parameter with $1/4 < \delta \le 1$. It is the order condition of an [LLL-reduced basis](/lll-reduction/), and the [LLL algorithm](/lll-algorithm/) swaps exactly where it fails. Together with [size reduction](/size-reduction/) it forces the Gram-Schmidt lengths to drop by at most a constant factor from one index to the next, which is the source of all LLL bounds.

## Definition

**Notation.** As on all pages of this area: basis rows $b_1, \ldots, b_n$, [Gram-Schmidt](/gram-schmidt-orthogonalization/) vectors $b_i^*$, coefficients $\mu_{ij}$ with $b_i = b_i^* + \sum_{j < i} \mu_{ij} b_j^*$, and the parameter $\delta$. Let $\pi_i$ be the orthogonal projection onto $\operatorname{span}(b_1, \ldots, b_{i-1})^\perp$, so $\pi_i(b_i) = b_i^*$ and $\pi_1$ is the identity.

Fix $\delta$ with $1/4 < \delta \le 1$. The basis satisfies the **Lovász condition at index $k$**, for $2 \le k \le n$, if

$$\delta\, \|b_{k-1}^*\|^2 \;\le\; \|b_k^* + \mu_{k,k-1} b_{k-1}^*\|^2 = \|b_k^*\|^2 + \mu_{k,k-1}^2 \|b_{k-1}^*\|^2.$$

Since $\pi_{k-1}(b_{k-1}) = b_{k-1}^*$ and $\pi_{k-1}(b_k) = b_k^* + \mu_{k,k-1} b_{k-1}^*$, the condition is the same as

$$\delta\, \|\pi_{k-1}(b_{k-1})\|^2 \le \|\pi_{k-1}(b_k)\|^2.$$

It satisfies the Lovász condition if it does so at every $k = 2, \ldots, n$. The value $\delta = 3/4$ is the one of the original paper.

**Meaning.** If $b_{k-1}$ and $b_k$ are exchanged, the new Gram-Schmidt vector at position $k - 1$ is $\pi_{k-1}(b_k)$, and all $b_i^*$ with $i \ne k - 1, k$ stay the same. So the condition says that the exchange would not shrink $\|b_{k-1}^*\|^2$ by a factor below $\delta$. When it fails, the exchange multiplies $\|b_{k-1}^*\|^2$ by less than $\delta$ and leaves the product $\|b_{k-1}^*\|^2 \|b_k^*\|^2$ unchanged, because the determinant of the first $k$ vectors does not change. The new lengths are

$$\|b_{k-1}^{*\prime}\|^2 = \|b_k^*\|^2 + \mu_{k,k-1}^2 \|b_{k-1}^*\|^2, \qquad \|b_k^{*\prime}\|^2 = \frac{\|b_{k-1}^*\|^2\, \|b_k^*\|^2}{\|b_{k-1}^{*\prime}\|^2}.$$

**The consequence with size reduction.** If also $|\mu_{k,k-1}| \le 1/2$, then $\|b_k^*\|^2 \ge (\delta - \mu_{k,k-1}^2) \|b_{k-1}^*\|^2$, so

$$\|b_k^*\|^2 \ge \Big(\delta - \frac14\Big) \|b_{k-1}^*\|^2 = \frac{1}{\alpha} \|b_{k-1}^*\|^2, \qquad \alpha = \frac{1}{\delta - 1/4}.$$

For $\delta = 3/4$ this gives $\alpha = 2$: each Gram-Schmidt length squared is at least half of the one before. This weaker inequality is sometimes called the **Siegel condition**.

## Examples and non-examples

**Examples.**

- **An orthogonal basis sorted by length.** For $(1, 0), (0, 3)$: $\mu_{21} = 0$ and $\delta \cdot 1 \le 9$. The condition holds for every $\delta \le 1$.
- **A failing pair and its swap.** For $b_1 = (4, 0)$, $b_2 = (1, 1)$: $\|b_1^*\|^2 = 16$, $\mu_{21} = 1/4$, $\|b_2^*\|^2 = 1$. With $\delta = 3/4$, $\frac34 \cdot 16 = 12 > 1 + \frac{1}{16} \cdot 16 = 2$, so the condition fails. After the swap, $b_1 = (1, 1)$ has $\|b_1^*\|^2 = 2 = 1 + \frac1{16} \cdot 16$, and $\|b_2^*\|^2 = 16 \cdot 1 / 2 = 8$, as the formulas predict. Size reduction then gives $b_2 = (4, 0) - 2 (1, 1) = (2, -2)$, and $\frac34 \cdot 2 \le 8$: the new basis satisfies the condition.
- **Dimension 2 with $\delta = 1$.** Since $\pi_1$ is the identity, the condition at $k = 2$ reads $\|b_1\| \le \|b_2\|$. So a size-reduced basis of rank 2 satisfies it with $\delta = 1$ exactly when it is [Lagrange-Gauss reduced](/lagrange-gauss-reduction/), and then $\|b_1\| = \lambda_1$.

**Non-examples.**

- **The condition is about projections, not lengths.** For $b_1 = (1, 0, 0)$, $b_2 = (0, 1, 0)$, $b_3 = (0, 1, 1/10)$, the vectors $b_2$ and $b_3$ have lengths 1 and about 1.005, in increasing order, but $\pi_2(b_2) = (0, 1, 0)$ and $\pi_2(b_3) = (0, 1, 1/10)$ give $\|b_2^*\|^2 = 1$, $\mu_{32} = 1$, $\|b_3^*\|^2 = 1/100$. The condition at $k = 3$ holds (as $\delta \le 1 + 1/100$), but the basis is not size-reduced, and after size reduction $b_3 = (0, 0, 1/10)$, $\mu_{32} = 0$ and the condition fails for every allowed $\delta$, since $\delta > 1/4 > 1/100$.
- **$\delta > 1$ cannot always be met.** For $\mathbb{Z}^2$ with $b_1 = (1, 0)$, $b_2 = (0, 1)$, the condition with $\delta > 1$ fails, and so it does after the swap: an algorithm that swaps whenever it fails would loop forever. This is one reason for the bound $\delta \le 1$, and LLL needs $\delta < 1$ to stop in polynomial time.
- **$\delta \le 1/4$ gives nothing.** With $|\mu_{k,k-1}| \le 1/2$, the bound $\|b_k^*\|^2 \ge (\delta - 1/4) \|b_{k-1}^*\|^2$ is empty for $\delta \le 1/4$, and the Gram-Schmidt lengths may fall as fast as they like.

## Related definitions

- **[LLL-reduced basis](/lll-reduction/).** A basis that is size-reduced and satisfies the Lovász condition with parameter $\delta$.
- **[Size reduction](/size-reduction/).** The companion condition $|\mu_{ij}| \le 1/2$; the Lovász condition is applied to size-reduced bases, since it depends on $\mu_{k,k-1}$.
- **Deep insertion condition.** The [deep LLL](/deep-lll/) variant asks $\delta \|\pi_i(b_i)\|^2 \le \|\pi_i(b_k)\|^2$ for all $i < k$, not only for $i = k - 1$: inserting $b_k$ at any earlier position would not help.
- **[HKZ reduction](/hkz-reduction/) and [BKZ](/bkz-algorithm/).** These replace the comparison of two projected vectors by the requirement that $b_i^*$ be a shortest vector, or nearly so, of the projected lattice $\pi_i(L(b_i, \ldots, b_{\min(i + \beta - 1, n)}))$. The Lovász condition is the case of blocks of size 2 with the factor $\delta$.
- **[LLL approximation guarantee](/lll-approximation-guarantee/).** The bounds $\|b_1\| \le \alpha^{(n-1)/2} \lambda_1$ and $\|b_1\| \le \alpha^{(n-1)/4} \det(L)^{1/n}$ follow from the Siegel form above.

## References
