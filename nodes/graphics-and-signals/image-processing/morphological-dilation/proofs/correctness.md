---
title: DILATE computes the dilation, the Minkowski sum, and it is dual to erosion by the reflected element
proves: [correctness, minkowski-sum, duality, distributivity]
status: full
---

**Notation.** The image domain is $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ and the values lie in $\{0, \dots, \top\}$; a binary image has $\top = 1$. For an outside value $o$ the extended image is $\tilde f(q) = f(q)$ for $q \in D$ and $\tilde f(q) = o$ for $q \notin D$. The option "ignore the outside" is the case $o = 0$. The structuring element is a finite set $B \subset \mathbb{Z}^2$, possibly empty, and $\check B = \{-b : b \in B\}$. The claim of the algorithm is

$$\mathrm{DILATE}(f, B, o)(p) = \max\bigl(\{0\} \cup \{\tilde f(p - b) : b \in B\}\bigr) \quad \text{for each } p \in D. \tag{D}$$

**Lemma 1 (DILATE is correct).** DILATE returns the image (D).

*Proof.* Let $b_1, \dots, b_k$ be the offsets in the order of the loop of line L2. The invariant is: after $j$ rounds, $g(p) = \max(\{0\} \cup \{\tilde f(p - b_i) : i \le j\})$ for each $p \in D$.

- *Initialization.* Line L1 sets $g(p) = 0$, the claim for $j = 0$.
- *Maintenance.* In round $j + 1$ the loops of lines L3 and L4 visit each $p \in D$ once. Lines L5 and L6 set $t = \tilde f(p - b_{j+1})$. Line L7 replaces $g(p)$ by $\max(g(p), t)$. The round reads only $f$ and writes $g$ only at the pixel it visits, so the other values of $g$ do not change, and the claim holds for $j + 1$ because $\max$ is associative.
- *Termination.* After $k$ rounds the invariant is (D). $\square$

**Lemma 2 (the Minkowski sum).** Let $f$ be the indicator of $X \subseteq D$ and let the outside be ignored ($o = 0$). Then (D) is the indicator of $(X \oplus B) \cap D$, where $X \oplus B = \{x + b : x \in X, b \in B\}$.

*Proof.* A maximum of values in $\{0, 1\}$ together with 0 is 1 if and only if some value is 1. With $o = 0$, $\tilde f(p - b) = 1$ if and only if $p - b \in X$. So $p \in D$ is in the result if and only if $p = x + b$ for some $x \in X$ and $b \in B$. $\square$

With $o = 1$ the same argument gives $(\tilde X \oplus B) \cap D$, where $\tilde X$ adds every pixel outside $D$ to $X$.

**Theorem 3 (duality).** With $\bar f = \top - f$ and $\mathrm{ERODE}(h, C, o')(p) = \min(\{\top\} \cup \{\tilde h(p + c) : c \in C\})$,

$$\top - \mathrm{DILATE}(f, B, o)(p) = \mathrm{ERODE}(\bar f, \check B, \top - o)(p) \quad \text{for each } p \in D.$$

*Proof.* The map $t \mapsto \top - t$ reverses the order, so $\top - \max S = \min\{\top - s : s \in S\}$ for a finite nonempty set $S$. Apply it to the set in (D). The term 0 becomes $\top$. The term $\tilde f(p - b)$ becomes $\bar f(p - b)$ when $p - b \in D$ and $\top - o$ otherwise, which is the value at $p - b$ of $\bar f$ extended by $\top - o$. With $c = -b \in \check B$ we have $p - b = p + c$, and the result is the erosion of $\bar f$ by $\check B$. $\square$

In sets, $(X \oplus B)^c = X^c \ominus \check B$ inside $D$, where ignoring the outside on the left ($o = 0$) is ignoring it on the right ($\top - o = \top$).

**Theorem 4 (distributivity).** For images $f_1, f_2$ and elements $B, C$, with the same outside value throughout,

$$\mathrm{DILATE}(\max(f_1, f_2), B, o) = \max\bigl(\mathrm{DILATE}(f_1, B, o), \mathrm{DILATE}(f_2, B, o)\bigr),$$
$$\mathrm{DILATE}(f, B \cup C, o) = \max\bigl(\mathrm{DILATE}(f, B, o), \mathrm{DILATE}(f, C, o)\bigr).$$

*Proof.* Fix $p \in D$. For the first identity, the extension of $\max(f_1, f_2)$ by $o$ is $\max(\tilde f_1, \tilde f_2)$, so the left side is $\max_b \max(\tilde f_1(p - b), \tilde f_2(p - b))$ with the extra term 0, and a maximum of maxima can be taken in any order. For the second identity, the set of terms in (D) for $B \cup C$ is the union of the sets of terms for $B$ and for $C$, and the maximum of a union is the maximum of the two maxima. $\blacksquare$

Together with the increasing property, which follows from (D) because each term grows with $f$, Theorem 4 says that dilation commutes with the maximum of images. This is the property that makes dilation the left part of the adjunction with erosion: on the whole plane $X \oplus B \subseteq Y$ holds exactly when $x + b \in Y$ for all $x \in X$ and $b \in B$, which is $X \subseteq Y \ominus B$.
