---
title: The detector scores every window of the pyramid, its HOG vector has the stated size and invariances, and mining reaches the SVM of all negatives
proves: [correctness]
status: full
---

We use the notation of the page. A pyramid level is a gray image with $n_y \times n_x$ whole cells of $c \times c$ pixels; the window has $w_c \times h_c$ cells; the histograms have $B$ orientation bins of width $180/B$ degrees; a block is $2 \times 2$ cells and blocks start at every cell. The detector is a linear function $f(x) = w \cdot \phi(x) + b$ of the HOG vector $\phi(x)$ of a window $x$. A detector is not "correct" in the sense of a theorem: its error rate is a benchmark result. What can be proved is that the program computes the function that the page describes, and that its training loop reaches the SVM that it claims to reach.

**Claim 1 (the size of the vector).** $\phi(x)$ has $(w_c - 1)(h_c - 1) \cdot 4B$ entries. For the default window of $64 \times 128$ pixels, $c = 8$ and $B = 9$, this is $7 \cdot 15 \cdot 36 = 3780$.

*Proof.* Blocks start at every cell whose block of $2 \times 2$ cells lies inside the window, so there are $w_c - 1$ block columns and $h_c - 1$ block rows. Each block is the concatenation of four histograms of $B$ entries. $\square$

**Claim 2 (the votes).** Every pixel whose centre lies at least half a cell from the border of the cell grid adds exactly its gradient magnitude to the sum of all histogram entries. Its vote goes to at most two bins and at most four cells, with the bilinear (tent) weights $\max(0, 1 - |p - q|/c)$ in each spatial axis and $\max(0, 1 - d/(180/B))$ in angle, where $d$ is the circular distance from the angle of the pixel to the bin centre.

*Proof.* In the $x$ axis, write $t = (x + 0.5)/c - 0.5$ and $c_0 = \lfloor t \rfloor$, $f = t - c_0$. The cell centres $(c_0 + 0.5)c$ and $(c_0 + 1.5)c$ are the two nearest centres to the pixel centre $x + 0.5$, at distances $fc$ and $(1 - f)c$, and the code gives them the weights $1 - f$ and $f$, which are the tent weights; every other cell centre is at least $c$ away and has tent weight 0. The same holds in the $y$ axis and, with the circular distance on $[0, 180)$, in angle, where the index $b_0 + 1$ is taken modulo $B$. The three pairs of weights each sum to 1, so the eight products sum to 1. When the pixel is at least half a cell inside the grid, both cell neighbours in each axis exist, and no vote is dropped. $\square$

The tests compare the code with a direct sum of the three tent functions over all pixels, cells and bins, which is the definition of the trilinear vote and shares no index arithmetic with the code.

**Claim 3 (contrast).** If every pixel value $I$ is replaced by $aI + k$ with $a > 0$, every block vector before normalization is multiplied by $a$, and with $\varepsilon = 0$ the normalized block vector, and so $\phi$, does not change. With $\varepsilon > 0$ the change is at most of the order of $\varepsilon^2 / \|v\|^2$ in each block.

*Proof.* The centred differences cancel $k$ and scale by $a$, so the angles do not change and the magnitudes scale by $a$. The votes are linear in the magnitude. L2-Hys divides by the norm, clips at $0.2$, and divides by the norm again; for $\varepsilon = 0$ each step maps $av$ to the same vector as $v$, because $av / \|av\| = v / \|v\|$. With $\varepsilon > 0$ the factor $1/\sqrt{\|v\|^2 + \varepsilon^2}$ differs from $1/\|v\|$ by a relative amount of order $\varepsilon^2/\|v\|^2$. $\square$

**Claim 4 (the scan is exhaustive).** For each pyramid level, line L5 of DETECT visits every window position on the cell grid, $(n_y - h_c + 1)(n_x - w_c + 1)$ of them, and line L6 computes $w \cdot \phi + b$ with $\phi$ equal to the HOG vector of that window, computed as if the window were cut out of the level with its surrounding pixels.

*Proof.* The loops of line L5 range over all top-left cells $(b_y, b_x)$ with the window inside the grid. The block grid of line L4 is computed once for the whole level, and the window reads the $(w_c - 1)(h_c - 1)$ blocks that start inside it, in the same order as Claim 1. Each block depends only on its four cells, and each cell histogram only on the pixels within one cell of it, so the vector is that of the window in its surroundings. It differs from the vector of the window cut out alone only in the outer half cell, where the cut-out window would repeat its own border pixels; this is why the tests compare shifted crops only away from the crop borders. $\square$

**Claim 5 (mining).** Let $D$ be a finite pool of negative windows, $P$ the positives, and for a set $S \subseteq D$ let $\beta^*(S)$ be the minimizer of
$$L_S(\beta) = \tfrac12 \|\beta\|^2 + C \sum_{x \in P} \max(0, 1 - f_\beta(x)) + C \sum_{x \in S} \max(0, 1 + f_\beta(x)),$$
with $\beta = (w, b)$ and the bias as an extra feature. If no $x \in D \setminus S$ has $f_{\beta^*(S)}(x) > -1$, then $\beta^*(S) = \beta^*(D)$. The loop of TRAIN-WITH-MINING that adds all such $x$ and trains again stops after at most $|D|$ rounds with $\beta^*(D)$.

*Proof.* $L_S$ is strictly convex because of the term $\frac12 \|\beta\|^2$, so it has one minimizer. For every $\beta$, $L_D(\beta) \ge L_S(\beta)$, since $L_D$ adds nonnegative terms. Under the hypothesis, every $x \in D \setminus S$ has $f(x) \le -1$ at $\beta^*(S)$ and adds $\max(0, 1 + f(x)) = 0$, so $L_D(\beta^*(S)) = L_S(\beta^*(S))$. Then for every $\beta$, $L_D(\beta^*(S)) = L_S(\beta^*(S)) \le L_S(\beta) \le L_D(\beta)$, so $\beta^*(S)$ minimizes $L_D$, and by uniqueness it is $\beta^*(D)$. Each round that does not stop adds at least one new element of $D$ to the cache, so there are at most $|D|$ such rounds, and the round that stops meets the hypothesis. This is the argument of Felzenszwalb et al. (2010), Section 4.4. $\square$

With an approximate solver, the result is $\beta^*(D)$ up to the tolerance of the solver; the tests check the duality gap of the solver and compare the mined SVM with the SVM on the whole pool. The detector of Dalal and Triggs makes one round of mining, so it does not reach the hypothesis of Claim 5 in general, and its SVM is only the SVM of the cache.

**Claim 6 (the output).** Line L8 returns the boxes of greedy non-maximum suppression, so no two kept boxes overlap with IoU above the threshold, and every window above the score threshold is either kept or overlaps a kept box with a higher score above the threshold. This is the correctness claim of [box non-maximum suppression](/box-non-maximum-suppression/).

**Cost.** For a level of $m$ pixels, lines L2 and L3 cost $O(m)$ (a constant number of votes per pixel), line L4 costs $O(m B / c^2)$, and lines L5 to L7 cost $O(m/c^2)$ windows times $O(w_c h_c B)$ for each dot product. A pyramid with scale step $s > 1$ has a total of at most $m s^2/(s^2 - 1)$ pixels, so the whole scan is $O(m)$ for the votes and $O(m\, w_c h_c B / c^2)$ for the scores. Line L8 adds the cost of greedy NMS on the windows above the threshold.
