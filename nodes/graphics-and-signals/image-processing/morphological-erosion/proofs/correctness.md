---
title: ERODE computes the erosion, and erosion is dual to dilation by the reflected element
proves: [correctness, duality, chain-rule]
status: full
---

**Notation.** The image domain is $D = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$. The values lie in $\{0, \dots, \top\}$; a binary image has $\top = 1$. For a value $o$ (the outside value) the extended image is $\tilde f(q) = f(q)$ for $q \in D$ and $\tilde f(q) = o$ for $q \notin D$. The option "ignore the outside" is the case $o = \top$. The structuring element is a finite set $B \subset \mathbb{Z}^2$ of offsets, possibly empty, and $\check B = \{-b : b \in B\}$. The claim of the algorithm is

$$\mathrm{ERODE}(f, B, o)(p) = \min\bigl(\{\top\} \cup \{\tilde f(p + b) : b \in B\}\bigr) \quad \text{for each } p \in D. \tag{E}$$

**Lemma 1 (ERODE is correct).** ERODE returns the image (E).

*Proof.* Let $b_1, \dots, b_k$ be the offsets of $B$ in the order of the loop of line L2. We show the invariant: after $j$ rounds of the loop, $g(p) = \min(\{\top\} \cup \{\tilde f(p + b_i) : i \le j\})$ for each $p \in D$.

- *Initialization.* Line L1 sets $g(p) = \top$, which is the claim for $j = 0$.
- *Maintenance.* In round $j + 1$ the loops of lines L3 and L4 visit each $p = (x, y) \in D$ exactly once. Lines L5 and L6 set $t = f(p + b_{j+1})$ when $p + b_{j+1} \in D$ and $t = o$ otherwise, so $t = \tilde f(p + b_{j+1})$. Line L7 replaces $g(p)$ by $\min(g(p), t)$. A round reads only $f$ and writes only $g(p)$ at the pixel it visits, so the value of $g$ at other pixels does not change. The invariant holds for $j + 1$ because $\min$ is associative.
- *Termination.* The loops are bounded, and after $k$ rounds the invariant is (E). $\square$

**Lemma 2 (the binary case).** If $f$ is the indicator of $X \subseteq D$ and $o \in \{0, 1\}$, then (E) is the indicator of $\{p \in D : p + b \in \tilde X \text{ for all } b \in B\}$, where $\tilde X = X$ when $o = 0$ and $\tilde X = X \cup (\mathbb{Z}^2 \setminus D)$ when $o = 1$.

*Proof.* A minimum of values in $\{0, 1\}$ together with $\top = 1$ is 1 if and only if every value is 1. The value $\tilde f(p + b)$ is 1 if and only if $p + b \in \tilde X$. $\square$

**Theorem 3 (duality).** Write $\bar f = \top - f$ for the complement. Let $\mathrm{DILATE}(h, C, o')(p) = \max(\{0\} \cup \{\tilde h(p - c) : c \in C\})$, with $\tilde h$ extended by $o'$. Then for each $p \in D$

$$\top - \mathrm{ERODE}(f, B, o)(p) = \mathrm{DILATE}(\bar f, \check B, \top - o)(p).$$

*Proof.* The map $t \mapsto \top - t$ reverses the order, so it turns a minimum into a maximum: $\top - \min S = \max\{\top - s : s \in S\}$ for a finite nonempty set $S$. Apply this to the set in (E). The term $\top$ becomes $0$. A term $\tilde f(p + b)$ becomes $\top - \tilde f(p + b)$. If $p + b \in D$ this is $\bar f(p + b)$, and otherwise it is $\top - o$; so it is the value at $p + b$ of $\bar f$ extended by $\top - o$. Put $c = -b$, so that $c$ runs over $\check B$ and $p + b = p - c$. The result is $\max(\{0\} \cup \{\tilde{\bar f}(p - c) : c \in \check B\})$, the dilation. $\square$

In the binary case this is $(X \ominus B)^c = X^c \oplus \check B$ inside $D$. Ignoring the outside on the left ($o = \top$) is ignoring it on the right ($\top - o = 0$, the neutral value of a maximum).

**Theorem 4 (chain rule for a rectangle).** Let $B = R = [x_0, x_1] \times [y_0, y_1]$ (integer intervals), $B_1 = [x_0, x_1] \times \{0\}$ and $B_2 = \{0\} \times [y_0, y_1]$, so that $R = B_1 \oplus B_2$. Then $\mathrm{ERODE}(\mathrm{ERODE}(f, B_1, o), B_2, o) = \mathrm{ERODE}(f, R, o)$.

*Proof.* Fix $p = (x, y) \in D$. Let $U = \{u \in [x_0, x_1] : 0 \le x + u < W\}$ and $V = \{v \in [y_0, y_1] : 0 \le y + v < H\}$. Since $D$ is a product of two intervals, $(x + u, y + v) \in D$ if and only if $u \in U$ and $v \in V$. By (E), the right side is the minimum of $\top$, of $f(x + u, y + v)$ over $U \times V$, and of $o$ when $U \times V \neq [x_0, x_1] \times [y_0, y_1]$. Let $g = \mathrm{ERODE}(f, B_1, o)$. For a row $y'$ inside the image, $g(x, y')$ is the minimum of $\top$, of $f(x + u, y')$ over $u \in U$, and of $o$ when $U \neq [x_0, x_1]$. The left side is the minimum of $\top$, of $g(x, y + v)$ over $v \in V$, and of $o$ when $V \neq [y_0, y_1]$. If $V$ is empty, both sides are $\min(\top, o)$, because then $U \times V$ is empty while the full rectangle is not. Otherwise expand $g$: the left side is the minimum of $\top$, of $f$ over $U \times V$, of $o$ when $U \neq [x_0, x_1]$, and of $o$ when $V \neq [y_0, y_1]$. The product $U \times V$ differs from the full rectangle if and only if $U$ or $V$ differs from its full interval. So the two minima range over the same values. $\blacksquare$
