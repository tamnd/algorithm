---
title: OPEN returns the maximum of the translates that fit under the image, and opening is increasing, anti-extensive and idempotent
proves: [correctness, increasing, anti-extensive, idempotent]
status: full
---

**Notation.** The image domain is $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ and the values lie in $\{0, \dots, \top\}$. The structuring element is a finite set $B \subset \mathbb{Z}^2$; it need not hold the origin. For $z \in D$ let $T_z = \{z + b : b \in B\} \cap D$, the translate of $B$ to $z$ cut to the image, and let $\mathcal T = \{T_z : z \in D\}$. For an image $h$ and a nonempty $T \subseteq D$ write $m_h(T) = \min_{q \in T} h(q)$.

**Lemma 1 (what OPEN computes).** For each $p \in D$,

$$\mathrm{OPEN}(f, B)(p) = \max\bigl(\{0\} \cup \{m_f(T) : T \in \mathcal T,\ p \in T\}\bigr). \tag{O}$$

*Proof.* Lines L1 to L3 are the erosion with the outside ignored. With the loop invariant used for ERODE (each round of line L2 takes the minimum with one shifted copy and writes only at the pixel it visits), they leave $e(z) = \min(\{\top\} \cup \{f(z + b) : b \in B,\ z + b \in D\}) = \min(\{\top\} \cup \{f(q) : q \in T_z\})$ for each $z \in D$. Lines L4 to L6 are the dilation with the outside ignored, and by the same invariant they leave $g(p) = \max(\{0\} \cup \{e(p - b) : b \in B,\ p - b \in D\})$.

Put $z = p - b$. The map $b \mapsto p - b$ is a bijection from $\{b \in B : p - b \in D\}$ onto $\{z \in D : p \in T_z\}$: if $z = p - b \in D$ then $p = z + b$ with $p \in D$, so $p \in T_z$; and if $p \in T_z$ then $b = p - z \in B$ and $p - b = z \in D$. So $g(p) = \max(\{0\} \cup \{e(z) : z \in D,\ p \in T_z\})$. For such $z$ the set $T_z$ holds $p$ and is not empty, so $e(z) = m_f(T_z)$. Several $z$ can give the same set $T$, but this does not change the maximum. $\square$

For a binary image, (O) says that $\mathrm{OPEN}(X, B) = \bigcup \{T \in \mathcal T : T \subseteq X\}$, the union of the cut translates of $B$ that fit inside $X$. On the whole plane, without the cut, this is the classical identity $(X \ominus B) \oplus B = \bigcup \{B_z : B_z \subseteq X\}$.

**Theorem 2.** Let $\gamma(h)$ denote the right side of (O) with $h$ in place of $f$. Then for all images $h, h_1, h_2$:

1. $h_1 \le h_2$ implies $\gamma(h_1) \le \gamma(h_2)$ (increasing);
2. $\gamma(h) \le h$ (anti-extensive);
3. $\gamma(\gamma(h)) = \gamma(h)$ (idempotent).

*Proof.* (1) For each $T$, $m_{h_1}(T) \le m_{h_2}(T)$, and a maximum of smaller terms over the same index set is smaller.

(2) Fix $p$. The term 0 is at most $h(p)$. For a term $m_h(T)$ with $p \in T$, the minimum over $T$ is at most the value at $p$, so $m_h(T) \le h(p)$.

(3) Let $g = \gamma(h)$. By (2), $g \le h$, and by (1), $\gamma(g) \le \gamma(h) = g$. For the other direction fix $p$. If $g(p) = 0$ then $\gamma(g)(p) \ge 0 = g(p)$. Otherwise $g(p) = m_h(T)$ for some $T \in \mathcal T$ with $p \in T$. Each $q \in T$ has $T$ among its own terms in (O), so $g(q) \ge m_h(T)$. Hence $m_g(T) = \min_{q \in T} g(q) \ge m_h(T) = g(p)$, and $\gamma(g)(p) \ge m_g(T) \ge g(p)$. So $\gamma(g) = g$. $\blacksquare$

The proof uses only the form of (O): a maximum, over a fixed family of sets that hold $p$, of the minimum of the image on the set. Any operator of this form is increasing, anti-extensive and idempotent. The three properties hold for every finite $B$, with or without the origin, and with the outside ignored in both steps. If the erosion counts the outside as background, the family changes to $\{B_z : z \in D,\ B_z \subseteq D\}$, and the proof is the same.
