---
title: The scattered inverse tool gives the lowest tip height at each grid point that leaves every sample under the tool, with contact at one sample
proves: [correctness, termination]
status: full
---

**Setting.** The grid points are $G = \{0, \dots, n_x - 1\} \times \{0, \dots, n_y - 1\}$ and $f : G \to \mathbb{R}$ gives the sampled heights of the part. The tool is a finite footprint $O \subset \mathbb{Z}^2$ with $(0, 0) \in O$, symmetric ($o \in O$ implies $-o \in O$), and a height function $T : O \to \mathbb{R}_{\ge 0}$ with $T(-o) = T(o)$ and $T(0, 0) = 0$. The tool with its tip at height $z$ above grid point $p$ has its surface at height $z + T(q - p)$ above the grid point $q$, for $q - p \in O$. For $p \in G$ let $N(p) = \{q \in G : q - p \in O\}$, the samples under the tool. Let $Z$ be the array that INVERSE-TOOL-OFFSET returns.

**Claim.** For every $p \in G$:

(a) $Z[p] = \max_{q \in N(p)} \big(f(q) - T(q - p)\big)$;

(b) with the tip at $Z[p]$, the tool surface is at or above every sample in $N(p)$, and it touches at least one of them;

(c) $Z[p]$ is the lowest tip height with property (b): every lower tip height puts some sample of $N(p)$ above the tool surface.

The loops stop after $n_x n_y |O|$ passes of line L5.

**Termination.** Lines L2 and L3 run over the finite sets $G$ and $O$, so line L5 runs at most $n_x n_y |O|$ times.

**Proof of (a).** Line L5 at sample $q$ and offset $o$ with $p = q + o \in G$ compares the value $f(q) - T(o)$ into $Z[p]$. Fix $p$. The pairs $(q, o)$ that reach $p$ are those with $q = p - o \in G$ and $o \in O$, which by the symmetry of $O$ are exactly the $q \in N(p)$, with $o = p - q$. Their values are $f(q) - T(p - q) = f(q) - T(q - p)$ by the symmetry of $T$. Line L1 starts $Z[p]$ empty, and line L5 keeps the largest value seen, so after the loops $Z[p]$ is the maximum of these values. The set $N(p)$ holds $p$ itself, since $(0, 0) \in O$, so the maximum is over a nonempty set.

**Proof of (b).** For $q \in N(p)$, (a) gives $Z[p] \ge f(q) - T(q - p)$, so $Z[p] + T(q - p) \ge f(q)$: the tool surface above $q$ is at or above the sample. For a $q^*$ that attains the maximum, equality holds, so the tool touches $q^*$.

**Proof of (c).** Let $z < Z[p]$. Then $z + T(q^* - p) < Z[p] + T(q^* - p) = f(q^*)$, so the sample $q^*$ lies above the tool surface. $\blacksquare$

**Remarks.** (1) Claim (a) says that $Z$ is the grayscale dilation of $f$ by the structuring function $-T$ on $O$, so INVERSE-TOOL-OFFSET is a [morphological dilation](/morphological-dilation/) of the height field. (2) The claims are about the samples. Between grid points the part can rise above the tool, for example a thin rib that lies between samples, so the method is gouge-free only at the samples. (3) Each value is computed by the same expression $f(q) - T(o)$ in the scatter loop and in a direct maximum, so with floats the two give equal results, and the tests compare them for equality.
