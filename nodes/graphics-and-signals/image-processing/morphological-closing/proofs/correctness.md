---
title: CLOSE is the dual of the opening by the reflected element, and closing is increasing, extensive and idempotent
proves: [correctness, duality, increasing, extensive, idempotent]
status: full
---

**Notation.** The image domain is $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ and the values lie in $\{0, \dots, \top\}$. The structuring element is a finite set $B \subset \mathbb{Z}^2$, with or without the origin, and $\check B = \{-b : b \in B\}$. For $z \in D$ let $S_z = \{z - b : b \in B\} \cap D$, the translate of $\check B$ to $z$ cut to the image, and $\mathcal S = \{S_z : z \in D\}$. For an image $h$ and a nonempty $S \subseteq D$ write $M_h(S) = \max_{q \in S} h(q)$ and $m_h(S) = \min_{q \in S} h(q)$. The complement of an image is $\bar h = \top - h$.

**Lemma 1 (what CLOSE computes).** For each $p \in D$,

$$\mathrm{CLOSE}(f, B)(p) = \min\bigl(\{\top\} \cup \{M_f(S) : S \in \mathcal S,\ p \in S\}\bigr). \tag{C}$$

*Proof.* Lines L1 to L3 are the dilation with the outside ignored. Each round of line L2 takes the maximum with one shifted copy of $f$ and writes $d$ only at the pixel it visits, so by induction on the rounds $d(z) = \max(\{0\} \cup \{f(z - b) : b \in B,\ z - b \in D\}) = \max(\{0\} \cup \{f(q) : q \in S_z\})$. Lines L4 to L6 are the erosion with the outside ignored, and by the same induction $g(p) = \min(\{\top\} \cup \{d(p + b) : b \in B,\ p + b \in D\})$.

The map $b \mapsto z = p + b$ is a bijection from $\{b \in B : p + b \in D\}$ onto $\{z \in D : p \in S_z\}$: if $z = p + b \in D$ then $p = z - b \in D$, so $p \in S_z$; and if $p \in S_z$ then $p = z - b$ for some $b \in B$, so $p + b = z \in D$. For such $z$ the set $S_z$ holds $p$, so it is not empty and $d(z) = M_f(S_z)$. $\square$

**Theorem 2 (duality).** $\top - \mathrm{CLOSE}(f, B) = \mathrm{OPEN}(\bar f, \check B)$, where OPEN is the erosion followed by the dilation, both with the outside ignored.

*Proof.* The opening page proves that $\mathrm{OPEN}(h, C)(p) = \max(\{0\} \cup \{m_h(T) : T \in \mathcal T_C,\ p \in T\})$, where $\mathcal T_C = \{(z + C) \cap D : z \in D\}$. For $C = \check B$, $(z + \check B) \cap D = S_z$, so $\mathcal T_{\check B} = \mathcal S$. Apply $t \mapsto \top - t$ to (C). It reverses the order, so the minimum becomes a maximum, the term $\top$ becomes 0, and $\top - M_f(S) = m_{\bar f}(S)$. The result is the formula for $\mathrm{OPEN}(\bar f, \check B)(p)$. $\square$

In sets, $(X \bullet B)^c = X^c \circ \check B$.

**Theorem 3.** Let $\varphi(h)$ denote the right side of (C) with $h$ in place of $f$. For all images:

1. $h_1 \le h_2$ implies $\varphi(h_1) \le \varphi(h_2)$ (increasing);
2. $h \le \varphi(h)$ (extensive);
3. $\varphi(\varphi(h)) = \varphi(h)$ (idempotent).

*Proof.* (1) Each $M_{h_1}(S) \le M_{h_2}(S)$, and a minimum of smaller terms over the same index set is smaller.

(2) Fix $p$. The term $\top$ is at least $h(p)$, and a maximum over a set $S$ that holds $p$ is at least $h(p)$.

(3) Let $g = \varphi(h)$. By (2) and (1), $g \le \varphi(g)$. For the other direction fix $p$. If $g(p) = \top$ then $\varphi(g)(p) \le \top = g(p)$. Otherwise $g(p) = M_h(S)$ for some $S \in \mathcal S$ with $p \in S$. Each $q \in S$ has $S$ among its own terms in (C), so $g(q) \le M_h(S)$. Hence $M_g(S) \le M_h(S) = g(p)$, and $\varphi(g)(p) \le M_g(S) \le g(p)$. $\blacksquare$

The three properties hold for every finite $B$ and use only the form of (C), a minimum over a fixed family of sets that hold $p$ of the maximum of the image on the set. The proof does not use the border rule except through the family $\mathcal S$; with the outside ignored in both steps the family is the set of cut translates, and the closing can add foreground along the border of the image, where a cut translate of $\check B$ is small.
