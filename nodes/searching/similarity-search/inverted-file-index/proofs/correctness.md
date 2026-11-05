---
title: The inverted file index is exact when it probes every cell, and its stopping rule is safe
proves: [correctness]
status: full
---

Let the centroids be $c_1, \dots, c_m \in \mathbb{R}^d$ and let the index satisfy (V): each stored vector $x$ is in exactly one list $I_j$, and $\|x - c_j\| \le \|x - c_i\|$ for all $i$. Distances are Euclidean.

**Lemma 1 (heap).** After a sequence of offers, $H$ holds $\min(k, N)$ pairs, where $N$ is the number of offers, and they are pairs of least distance among all offered pairs (with ties broken in some fixed way).

*Proof.* By induction on the offers. An offer either fills a free place, or replaces the pair of largest distance in $H$ when the new pair is smaller, or is dropped. In each case the $k$ least pairs among the offers so far are kept, since a dropped or removed pair has at least $k$ offered pairs at most as large. $\square$

**Theorem 1.** IVF-SEARCH$(q, k, m)$ returns the $k$ nearest stored vectors to $q$, with their distances.

*Proof.* With $n_{\text{probe}} = m$, the set $J$ of line L3 is all of $\{1, \dots, m\}$. By (V) each stored vector is in exactly one list, so line L5 offers each stored vector exactly once with its true distance. By Lemma 1, $H$ then holds the $k$ least pairs. $\square$

**Theorem 2.** For $J \subseteq J'$, let $D_k(J)$ be the $k$-th distance returned when the probed set is $J$, if at least $k$ vectors are offered. Then $D_k(J') \le D_k(J)$.

*Proof.* The vectors offered with $J'$ include those offered with $J$. The $k$-th least value of a superset of numbers is at most the $k$-th least value of the subset. $\square$

**Lemma 2 (bisector bound).** Let $c_a$ be a nearest centroid to $q$ and $j \ne a$ with $c_j \ne c_a$. Every $x$ with $\|x - c_j\| \le \|x - c_a\|$ satisfies $\|q - x\| \ge \beta_j$, where $\beta_j = \max\big(0, (\|q - c_j\|^2 - \|q - c_a\|^2)/(2\|c_j - c_a\|)\big)$.

*Proof.* Let $u = (c_j - c_a)/\|c_j - c_a\|$ and $f(y) = \|y - c_a\|^2 - \|y - c_j\|^2$. Expanding the squares, $f(y) = 2 y \cdot (c_j - c_a) + \|c_a\|^2 - \|c_j\|^2$, an affine function with gradient $2(c_j - c_a)$. So $f(y) - f(z) = 2\|c_j - c_a\| \, u \cdot (y - z)$ for all $y, z$. The condition on $x$ says $f(x) \ge 0$, and $f(q) = \|q - c_a\|^2 - \|q - c_j\|^2 \le 0$. Then
$$\|q - x\| \ge u \cdot (x - q) = \frac{f(x) - f(q)}{2\|c_j - c_a\|} \ge \frac{-f(q)}{2\|c_j - c_a\|} = \frac{\|q - c_j\|^2 - \|q - c_a\|^2}{2\|c_j - c_a\|},$$
using the Cauchy-Schwarz inequality and $\|u\| = 1$ in the first step. With $\|q - x\| \ge 0$ this gives $\|q - x\| \ge \beta_j$. $\square$

If $c_j = c_a$, put $\beta_j = 0$, which is a valid bound. For $j = a$, $\beta_a = 0$.

**Theorem 3.** IVF-SEARCH-EXACT$(q, k)$ returns the $k$ nearest stored vectors to $q$.

*Proof.* The cells are visited in the order of nondecreasing $\beta_j$. If the loop never stops at line L8, every vector is offered, and Lemma 1 ends the proof as in Theorem 1. Suppose it stops at cell $j$. Then $H$ holds $k$ pairs, and $\beta_j > D$, where $D$ is the largest distance in $H$. Every cell $j'$ not yet visited has $\beta_{j'} \ge \beta_j > D$. By (V) and Lemma 2, each vector $x$ of such a cell has $\|q - x\| \ge \beta_{j'} > D$. So at least $k$ offered vectors are strictly closer than every vector not offered, and the $k$ least pairs among the offered vectors, which $H$ holds by Lemma 1, are the $k$ least pairs among all stored vectors. $\blacksquare$
