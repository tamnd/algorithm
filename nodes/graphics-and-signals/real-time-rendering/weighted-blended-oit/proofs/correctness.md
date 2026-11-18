---
title: What weighted blended OIT gets exactly right
proves: [correctness]
status: full
---

**Setting.** A pixel has an opaque background color $C_0$ and $k \ge 1$ fragments $(c_i, \alpha_i, z_i)$ with premultiplied colors $c_i$, opacities $\alpha_i \in (0, 1]$ and distinct depths. Rename them so that $z_1 < z_2 < \dots < z_k$ (front to back). Let $T_i = \prod_{j < i} (1 - \alpha_j)$ be the transmittance in front of fragment $i$, so $T_1 = 1$, and let $R = T_{k+1} = \prod_{i=1}^{k} (1 - \alpha_i)$. The exact composite is

$$C = \sum_{i=1}^{k} c_i T_i + C_0 R.$$

The method takes weights $w_i > 0$ and returns

$$\tilde C = \frac{\sum_i c_i w_i}{\sum_i \alpha_i w_i} (1 - R) + C_0 R.$$

All claims are in exact arithmetic, as in the tests, which use fractions. The guard $\varepsilon$ of line L6 is assumed to be smaller than $\sum_i \alpha_i w_i$, so it does not change the result. Fragments with $\alpha_i = 0$ add nothing to any of the sums and are left out.

**Lemma 1 (telescoping).** $\sum_{i=1}^{k} \alpha_i T_i = 1 - R$.

*Proof.* $T_{i+1} = T_i (1 - \alpha_i)$, so $\alpha_i T_i = T_i - T_{i+1}$. The sum telescopes to $T_1 - T_{k+1} = 1 - R$. $\square$

**Theorem 1 (order independence and exact coverage).** $\tilde C$ does not depend on the order in which the fragments arrive, and its background term $C_0 R$ is the background term of $C$.

*Proof.* Lines L4 and L5 build two sums and a product. Addition and multiplication are commutative and associative, so the order of the loop does not change $\sum_i c_i w_i$, $\sum_i \alpha_i w_i$ or $R$, provided that each $w_i$ depends only on its own fragment. $R$ is the same product as in $C$. $\square$

In floating point, the sums and the product round differently for different orders, so the result depends on the order at the level of rounding.

**Theorem 2 (the color is a weighted mean).** Let $\hat c_i = c_i / \alpha_i$ be the unpremultiplied color of fragment $i$ and $\lambda_i = \alpha_i w_i / \sum_j \alpha_j w_j$. Then $\lambda_i > 0$, $\sum_i \lambda_i = 1$ and

$$\tilde C - C_0 R = (1 - R) \sum_i \lambda_i \hat c_i.$$

So in each channel, $(1 - R) \min_i \hat c_i \le \tilde C - C_0 R \le (1 - R) \max_i \hat c_i$.

*Proof.* $c_i w_i = \hat c_i \alpha_i w_i$, so $\sum_i c_i w_i / \sum_j \alpha_j w_j = \sum_i \lambda_i \hat c_i$. The weights $\lambda_i$ are positive and sum to 1. A convex combination lies between the smallest and the largest value in each channel, and $1 - R \ge 0$. $\square$

The exact composite has the same form. By Lemma 1, $C - C_0 R = \sum_i \hat c_i \alpha_i T_i = (1 - R) \sum_i \mu_i \hat c_i$ with $\mu_i = \alpha_i T_i / (1 - R)$. The two results differ only in the mixing weights: $\mu_i$ is proportional to $\alpha_i T_i$, and $\lambda_i$ is proportional to $\alpha_i w_i$.

**Theorem 3 (exact weights).** If $w_i = K T_i$ for a constant $K > 0$, then $\tilde C = C$.

*Proof.* Then $\lambda_i = \alpha_i T_i / \sum_j \alpha_j T_j = \mu_i$ by Lemma 1, and the two expressions of Theorem 2 are equal. $\square$

The weight $T_i$ needs the fragments in front of fragment $i$, so it depends on the order that the method avoids. A weight that falls with depth is an approximation of $T_i$ by a function of $z_i$ alone, and how well it works depends on the scene.

**Theorem 4 (special cases).** $\tilde C = C$ for every choice of positive weights when (a) $k = 1$, or (b) all fragments have the same unpremultiplied color $\hat c$.

*Proof.* (a) With one fragment, $\lambda_1 = \mu_1 = 1$. (b) Both convex combinations of Theorem 2 equal $\hat c$. $\square$

**Theorem 5 (a counterexample).** The method is not exact in general. Over a black background, let a red fragment $c = (1/2, 0, 0)$, $\alpha = 1/2$ lie in front of a blue fragment $c = (0, 0, 1/2)$, $\alpha = 1/2$. Then $C = (1/2, 0, 1/4)$. With equal weights, $\tilde C = (3/8, 0, 3/8)$. With the weights 3 for red and 1 for blue, $\tilde C = (9/16, 0, 3/16)$.

*Proof.* $R = 1/4$. Equal weights give the mean $(1/2, 0, 1/2)$ of the unpremultiplied colors $(1, 0, 0)$ and $(0, 0, 1)$, times $3/4$. The weights 3 and 1 give $\lambda = (3/4, 1/4)$, so the mean is $(3/4, 0, 1/4)$, times $3/4$. The exact weights are $T = (1, 1/2)$, which give $\lambda = (2/3, 1/3)$ and $(2/3, 0, 1/3) \cdot 3/4 = (1/2, 0, 1/4)$. $\square$

**Theorem 6 (cost).** For a pixel with $k$ fragments and $n$ color channels, the method does $O(n k)$ arithmetic and keeps $n + 2$ numbers.

*Proof.* Each fragment costs one weight evaluation, $n + 1$ multiply-adds and one multiplication. The state is the $n$ color sums, the alpha sum and $R$. Line L7 costs $O(n)$. $\square$
