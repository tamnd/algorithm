---
title: PatchMatch stereo builds correct planes, transfers them correctly between views, and never increases a cost
proves: [correctness]
status: full
---

We use the pseudocode of the page. A plane $f = (a, b, c)$ of a view gives the disparity $f(x, y) = a x + b y + c$ at the pixel $(x, y)$ of that view. A left point $(x, y)$ with disparity $d$ matches the right point $(x - d, y)$, and a right point $(x', y)$ with disparity $d$ matches the left point $(x' + d, y)$.

**Lemma 1 (plane from point and normal).** Let $n = (n_x, n_y, n_z)$ with $n_z \ne 0$, and set $a = -n_x / n_z$, $b = -n_y / n_z$, $c = (n_x x_0 + n_y y_0 + n_z z_0) / n_z$. Then $a x_0 + b y_0 + c = z_0$, and the set $\{(x, y, z) : z = a x + b y + c\}$ is the plane through $(x_0, y_0, z_0)$ with normal $n$.

*Proof.* $a x_0 + b y_0 + c = (-n_x x_0 - n_y y_0 + n_x x_0 + n_y y_0 + n_z z_0) / n_z = z_0$. Multiply $z = a x + b y + c$ by $n_z$ and rearrange: $n_x (x - x_0) + n_y (y - y_0) + n_z (z - z_0) = 0$, which is the plane through the point with normal $n$. $\square$

So line L1 and line L11 give a plane with disparity $z_0$ at $p$. In particular line L1 gives $0 \le f(p) \le D$, since $z_0 \in [0, D]$.

**Lemma 2 (transfer).** Let $f = (a, b, c)$ be a plane of the right view with $1 + a \ne 0$, and let $g = (a, b, c) / (1 + a)$. For every right point $(x', y)$ with disparity $d = f(x', y)$, the matching left point $x = x' + d$ has $g(x, y) = d$. Symmetrically, for a left plane $f$ with $1 - a \ne 0$ and $g = (a, b, c) / (1 - a)$, every left point $(x, y)$ with $d = f(x, y)$ has $g(x - d, y) = d$. The two maps are inverse to each other.

*Proof.* Right to left: $(1 + a)\, g(x, y) = a (x' + d) + b y + c = (a x' + b y + c) + a d = d + a d$, so $g(x, y) = d$. Left to right: $(1 - a)\, g(x - d, y) = a (x - d) + b y + c = d - a d$, so $g(x - d, y) = d$. For the inverse, apply the right to left map to $g = (a, b, c) / (1 - a)$. Its first entry is $a' = a / (1 - a)$, and $1 + a' = 1 / (1 - a)$, so $g / (1 + a') = (a, b, c)$. The other order is the same computation with $-a$. $\square$

So a plane offered in line L7 describes, in the coordinates of view $v$, the same set of scene points as the plane of $p'$ in the other view. The pixel $p$ is the rounded match of $p'$, so $p$ lies on that surface up to rounding.

**Lemma 3 (invariant).** At every point of the run, for each view $v$ and pixel $p$: (a) $m_v[p] = m(p, f_v[p])$; (b) $0 \le f_v[p](p) \le D$; (c) the value of $m_v[p]$ is never larger than an earlier value.

*Proof.* After line L1, (a) holds by the assignment and (b) by Lemma 1. Only TRY changes $f_v[p]$ or $m_v[p]$, and it changes both at once, to a plane $f$ and its cost $m(p, f)$, so (a) stays true. TRY accepts $f$ only when $0 \le f(p) \le D$, so (b) stays true. It accepts only when $m(p, f) < m_v[p]$, which gives (c). $\square$

**Theorem.** PATCHMATCH-STEREO returns for each pixel $p$ of each view a plane $f_v[p]$ with $0 \le f_v[p](p) \le D$ and

$$m(p, f_v[p]) = \min \{\, m(p, f) : f \text{ was passed to TRY at } p \text{ and } 0 \le f(p) \le D \,\} \cup \{ m(p, f_0) \},$$

where $f_0$ is the plane of line L1. The cost of each pixel does not increase from one iteration to the next.

*Proof.* By Lemma 3, $m_v[p]$ starts at $m(p, f_0)$ and is replaced by $m(p, f)$ exactly when a valid candidate $f$ is strictly better. So at the end it is the least value among $f_0$ and all valid candidates, and by Lemma 3 (a) it equals $m(p, f_v[p])$. The monotone part is Lemma 3 (c). $\blacksquare$

**What is not proved.** The theorem does not say that $f_v[p]$ minimizes $m(p, \cdot)$ over all planes. The function is a sum of truncated terms of an interpolated image and is not convex in $(a, b, c)$; the method finds the best plane among those it tried. How quickly good planes appear depends on the random numbers and on how much of the scene is made of planes, as in the analysis of PatchMatch.
