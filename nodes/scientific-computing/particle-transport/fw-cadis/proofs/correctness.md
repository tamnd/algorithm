---
title: FW-CADIS is unbiased in every bin, and its estimated response is the number of bins
proves: [correctness]
status: full
---

We assume exact arithmetic and exact independent uniform random numbers. The slab, the cells, the bins and the lines L1 to L8 are those of the page, and the lines of CADIS-RUN are those of the [CADIS](/cadis/) page.

**Theorem 1 (unbiased bins).** Assume that the forward estimates $\hat T_j$ of line L2 are positive, that the adjoint flux $\phi^+_i$ of line L3 is positive in every cell with $q_i > 0$, and that the expected number of flights of one history is finite. Then for every bin $j$, the mean of the score $S_j$ of one history is the exact $T_j$, whatever the errors of the two deterministic solves.

*Proof.* Fix a bin $j$, and let $\sigma_{d,i} = 1$ for the cells $i$ of bin $j$ and $\sigma_{d,i} = 0$ for all other cells. With this response function, the CADIS score of line L10 is the sum of $w$ times the track length in the cells of bin $j$, which is the score $S_j$ that line L7 adds. The exact CADIS response is then the expected analog track length in bin $j$ per source particle, which is $T_j$.

Lines L4 and L5 of FW-CADIS are lines L4 and L5 of CADIS with the adjoint $\phi^+$ of line L3, and the run of line L6 is CADIS-RUN with these parameters. Theorem 1 of the CADIS proof holds for any positive values of the adjoint in the source cells: the proof uses only that $p_i > 0$ where $q_i > 0$, that the birth weight is $q_i h/p_i$, that the window targets are finite, and that the flights and collisions keep their analog laws. The adjoint that CADIS takes from a solve with the source $\sigma_d$ can therefore be replaced by the adjoint of line L3, whose source is $1/\hat T$, without a change in the proof. The theorem gives $E[S_j] = T_j$.

All bins use the same run, so the theorem holds for every $j$ at the same time. Line L8 adds the scores of one history, so the bin means are means of independent and identically distributed scores, and the standard error of each bin is the usual one. $\square$

**Theorem 2 (the estimated response).** Let the forward and the adjoint solves of lines L1 and L3 be the same discrete operator and its adjoint, so that the discrete reciprocity $\sum_i q_i \phi^+_i h = \sum_i q^+_i \phi_i h$ holds. Then $\hat R = B$.

*Proof.* By line L2, $q^+_i = 1/\hat T_{j(i)}$. So
$$\hat R = \sum_i q_i \phi^+_i h = \sum_i q^+_i \phi_i h = \sum_{j = 1}^{B} \frac{1}{\hat T_j} \sum_{i \in \text{bin } j} \phi_i h = \sum_{j = 1}^{B} \frac{\hat T_j}{\hat T_j} = B. \qquad \square$$

In a slab with isotropic scattering, the discrete adjoint of the $S_N$ sweep with the symmetric quadrature is the forward sweep with the directions reversed, and the scalar fluxes agree, which is why the code of the page uses one solver for both. The value $15.999999999$ for $B = 16$ in the example is a check of this.

**The track density (a heuristic).** Suppose that each particle at a point $P$ has exactly the target weight $\hat R/\phi^+(P)$. A tally of the physical flux is the sum of the weights times the track lengths, so the expected track length of the Monte Carlo particles per unit volume at $P$ is the flux divided by the weight, $\phi(P)\phi^+(P)/\hat R$. If $\phi\phi^+$ is constant over the tally region, every bin of the same size gets the same expected number of tracks, each with a weight that follows the flux, and the relative errors of the bins are then about equal. The window of finite width, the correlation between the copies of one history, and an adjoint that does not make $\phi\phi^+$ constant make this an approximation. It is not a theorem, and the example of the page measures how far a real run is from it.
