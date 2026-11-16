---
title: The maximum overlap matching and the minimum cost form of the paper give the same IDTP, and IDF1 is at most the F1 score of detections
proves: [correctness]
status: full
---

Notation as on the page. True trajectories $o_1, \ldots, o_t$ have lengths $|o_i|$, computed trajectories $h_1, \ldots, h_c$ have lengths $|h_j|$, and $n_{ij} = n(o_i, h_j)$ is the number of frames in which they agree. Let $L = \sum_i |o_i| + \sum_j |h_j|$.

## Claim 1: line L2 finds IDTP

The Hungarian algorithm on the costs $-n_{ij}$, with the pairs of $n_{ij} = 0$ then removed, returns a one-to-one matching with the largest total $\sum n_{ij}$.

*Proof.* Every one-to-one matching $\mu$ of rows and columns extends to a full assignment of the smaller side by adding pairs, and since $n_{ij} \ge 0$ this does not lower the total. So the largest total over matchings equals the largest total over assignments, which the Hungarian algorithm finds (its optimality is proved on the [SORT proof](/sort-tracker/) and the [Hungarian algorithm](/hungarian-algorithm/) page). Removing pairs with $n_{ij} = 0$ does not change the total. $\square$

## Claim 2: the form of the paper gives the same IDTP

Build the square cost matrix of size $t + c$ of the code. Rows are $o_1, \ldots, o_t$ and the false positive nodes $\bar h_1, \ldots, \bar h_c$; columns are $h_1, \ldots, h_c$ and the false negative nodes $\bar o_1, \ldots, \bar o_t$. The costs are $|o_i| + |h_j| - 2 n_{ij}$ for $(o_i, h_j)$, $|o_i|$ for $(o_i, \bar o_i)$, $|h_j|$ for $(\bar h_j, h_j)$, 0 for $(\bar h_j, \bar o_i)$, and a cost $\beta > L$ for every other pair. Then the minimum cost of a perfect assignment is $L - 2\, \mathrm{IDTP} = \mathrm{IDFN} + \mathrm{IDFP}$.

*Proof.* First, every matching $\mu$ of true to computed trajectories gives a perfect assignment of cost $L - 2 \sum_{(i,j) \in \mu} n_{ij}$. Take the pairs of $\mu$; match each unmatched $o_i$ to $\bar o_i$ and each unmatched $h_j$ to $\bar h_j$. The $\bar h_j$ of the matched $h_j$ and the $\bar o_i$ of the matched $o_i$ are left; there are $|\mu|$ of each, and they pair up at cost 0. Every trajectory appears in exactly one paid pair, so the cost is $\sum_i |o_i| + \sum_j |h_j| - 2 \sum_\mu n_{ij}$.

Second, every perfect assignment $\pi$ of cost at most $L$ is of this form. A cost of $\beta > L$ is too much, so $\pi$ uses only the allowed pairs. Then each $o_i$ goes to some $h_j$ or to $\bar o_i$, and each $h_j$ comes from some $o_i$ or from $\bar h_j$. The pairs $(o_i, h_j)$ of $\pi$ form a matching $\mu$, and the cost is, as above, $L - 2 \sum_\mu n_{ij}$ plus the zero pairs.

The matching with no pairs gives cost $L$, so the minimum is at most $L$, and by the two parts it is $\min_\mu (L - 2 \sum_\mu n_{ij}) = L - 2\, \mathrm{IDTP}$. Finally $\mathrm{IDFN} + \mathrm{IDFP} = (\sum_i |o_i| - \mathrm{IDTP}) + (\sum_j |h_j| - \mathrm{IDTP}) = L - 2\, \mathrm{IDTP}$. $\square$

The paper links two regular nodes only when the trajectories overlap in time. Here every pair has an edge, but a pair with $n_{ij} = 0$ costs $|o_i| + |h_j|$, the same as leaving both unmatched, so the minimum does not change. The tests compute both forms on random sequences.

## Claim 3: IDF1 is at most the F1 score of detections

For each frame $f$, let $m_f$ be the size of a largest one-to-one matching of the true and the computed detections of the frame with IoU at least $\Delta$, and let $\mathrm{TP} = \sum_f m_f$. Then $\mathrm{IDTP} \le \mathrm{TP}$, so $\mathrm{IDF1} = 2\, \mathrm{IDTP} / L \le 2\, \mathrm{TP} / L$.

*Proof.* Fix the matching $\mu$ of IDTP. In frame $f$, take the pairs $(o, h) \in \mu$ that agree in $f$. Since $\mu$ is one-to-one, these pairs form a one-to-one matching of the detections of $f$, and each has IoU at least $\Delta$. So their number is at most $m_f$. Summing over the frames, the number of agreeing frames of the pairs of $\mu$, which is IDTP, is at most $\sum_f m_f$. $\square$

## Claim 4: symmetry and the harmonic mean

Exchanging the ground truth and the tracker keeps IDTP and IDF1 and swaps IDP and IDR. If $\mathrm{IDTP} > 0$, IDF1 is the harmonic mean of IDP and IDR.

*Proof.* IoU is symmetric, so the exchange turns the matrix $n$ into its transpose, and a matching of the transpose has the same total. So IDTP is the same, $L$ is the same, and IDF1 is the same. IDP divides IDTP by the computed detections and IDR by the true ones, so they swap. For the harmonic mean, $\mathrm{IDTP} + \mathrm{IDFP} = \sum_j |h_j|$ and $\mathrm{IDTP} + \mathrm{IDFN} = \sum_i |o_i|$, so $1/\mathrm{IDP} + 1/\mathrm{IDR} = L / \mathrm{IDTP}$, and $2 / (1/\mathrm{IDP} + 1/\mathrm{IDR}) = 2\, \mathrm{IDTP} / L = \mathrm{IDF1}$. $\square$
