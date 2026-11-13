---
title: HMT keeps exactly the pixels where the template matches, and equals the intersection of two erosions
proves: [correctness, two-erosions, complement-swap]
status: full
---

**Notation.** The image domain is $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$, the foreground is $X \subseteq D$, and a pixel outside $D$ has the value $o \in \{0, 1\}$; the default $o = 0$ counts the outside as background. Write $\tilde X = X$ if $o = 0$ and $\tilde X = X \cup (\mathbb{Z}^2 \setminus D)$ if $o = 1$, so that a point $q \in \mathbb{Z}^2$ has the value 1 if and only if $q \in \tilde X$. The hit set $B_1$ and the miss set $B_2$ are finite subsets of $\mathbb{Z}^2$ with $B_1 \cap B_2 = \emptyset$. The claim is

$$\mathrm{HMT}(X; B_1, B_2) = \{p \in D : p + b \in \tilde X \text{ for all } b \in B_1, \text{ and } p + b \notin \tilde X \text{ for all } b \in B_2\}. \tag{M}$$

**Lemma 1 (HMT is correct).** The pseudocode returns the indicator of (M).

*Proof.* Line L1 sets $r(p) = 1$ for each $p \in D$. A pixel $p$ is set to 0 only in two places: at line L3, for some $b \in B_1$ with $p + b \notin \tilde X$, and at line L5, for some $b \in B_2$ with $p + b \in \tilde X$. A value set to 0 never returns to 1. The loops of lines L2 to L5 visit every pair of a pixel and an offset of $B_1$ or $B_2$. So at line L6, $r(p) = 0$ exactly when some $b \in B_1$ has $p + b \notin \tilde X$ or some $b \in B_2$ has $p + b \in \tilde X$, and $r(p) = 1$ exactly when $p$ satisfies the two conditions of (M). $\square$

**Theorem 2 (two erosions).** Let $X \ominus_o B = \{p \in D : p + b \in \tilde X \text{ for all } b \in B\}$ be the erosion with the outside value $o$, and let $X^c = D \setminus X$. Then

$$\mathrm{HMT}(X; B_1, B_2) = (X \ominus_o B_1) \cap (X^c \ominus_{1-o} B_2).$$

*Proof.* The first condition of (M) is the definition of $X \ominus_o B_1$. For the second, the complement image $X^c$ with outside value $1 - o$ has the extended foreground $\widetilde{X^c} = \mathbb{Z}^2 \setminus \tilde X$: a pixel of $D$ is in it if and only if it is not in $X$, and a pixel outside $D$ is in it if and only if $1 - o = 1$, that is $o = 0$, that is the pixel is not in $\tilde X$. So $p + b \notin \tilde X$ for all $b \in B_2$ says $p \in X^c \ominus_{1-o} B_2$. $\square$

**Corollary 3 (swap).** $\mathrm{HMT}(X; B_1, B_2)$ with outside value $o$ equals $\mathrm{HMT}(X^c; B_2, B_1)$ with outside value $1 - o$.

*Proof.* By Theorem 2 the right side is $(X^c \ominus_{1-o} B_2) \cap ((X^c)^c \ominus_{o} B_1)$, and $(X^c)^c = X$. The intersection does not depend on the order. $\square$

**Remark (disjointness).** If some $b$ lies in $B_1 \cap B_2$, the two conditions of (M) at $p + b$ contradict each other, so the transform is empty for every image. This is why the pair must be disjoint, and why the implementation rejects a pair that is not. $\blacksquare$
