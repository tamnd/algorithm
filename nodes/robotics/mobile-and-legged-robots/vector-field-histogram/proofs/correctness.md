---
title: The histogram sums every cell once and the steering rule always picks a free sector
proves: [correctness]
status: full
---

Line numbers refer to the pseudocode on the [vector field histogram](/vector-field-histogram/) page. VFH is a heuristic: nothing below says that the robot avoids every obstacle or reaches the goal. What can be proved is that the two data reductions do what they claim. The proof uses exact arithmetic; the code adds $10^{-9}$ degrees before it divides by $\alpha$, so that a direction that is a multiple of $\alpha$ up to roundoff goes to the upper sector, as it does in exact arithmetic.

Sectors are numbered $0, \dots, n - 1$ and taken modulo $n$. Sector $k$ holds the directions $\beta$ with $k\alpha \le \beta < (k + 1)\alpha$, for $\beta \in [0°, 360°)$. A valley is a maximal run of free sectors $s, s + 1, \dots, s + L - 1$ with $1 \le L < n$.

**Lemma 1 (the histogram).** After line L2, $\sum_k h[k] = \sum m_{ij}$, where the sum on the right is over the cells of the window other than the cell at the robot's position, and $m_{ij} = c_{ij}^2\max(0, a - bd_{ij})$.

*Proof.* Each such cell has $d_{ij} > 0$, so its direction $\beta_{ij} \in [0°, 360°)$ is defined, and $\lfloor\beta_{ij}/\alpha\rfloor$ is exactly one integer in $\{0, \dots, n - 1\}$. So line L2 adds $m_{ij}$ to exactly one sector. $\square$

**Lemma 2 (rotation).** Let the robot be at the center of its cell, let $4$ divide $n$, and rotate the grid by $90°$ about the robot: the cell at offset $(u, v)$ from the robot's cell moves to offset $(-v, u)$. Then the new histogram satisfies $h_{\text{new}}[k + n/4] = h[k]$ for every $k$.

*Proof.* The rotation maps the square window onto itself and keeps each distance $d_{ij}$, so each $m_{ij}$ moves to its image cell unchanged. The direction of the image is $\beta + 90°$ modulo $360°$, and $90° = (n/4)\alpha$, so its sector is $\lfloor\beta/\alpha\rfloor + n/4$ modulo $n$. By Lemma 1, each sector of the new histogram receives exactly the magnitudes that sector $k$ received before. $\square$

**Theorem (steering).** Assume at least one smoothed value is below $\tau$. Then the direction returned by lines L5 to L7 is the center of a free sector. If, moreover, the target sector $k_t$ and the sectors $k_t + j$ for $|j| \le \lceil s_{\max}/2\rceil$ are free, then the direction is the center of $k_t$.

*Proof.* If every sector is free, line L5 returns the center of $k_t$, which is free. Otherwise there is a free sector and a blocked one, so there is at least one valley, and line L6 chooses a valley $V$ with first sector $s$ and length $L$. Write the result of line L7 as $\theta = s + t$ with a real number $t$; the code returns the center of sector $s + \lfloor t + 1/2\rfloor$. It suffices to show $0 \le t \le L - 1$, because then $0 \le \lfloor t + 1/2\rfloor \le L - 1$ and the sector belongs to $V$.

If $L \le s_{\max}$, then $t = (L - 1)/2$, which is in $[0, L - 1]$. If $L > s_{\max}$, then $L - 1 \ge s_{\max}$, so the bounds $t_{\text{lo}} = s_{\max}/2$ and $t_{\text{hi}} = L - 1 - s_{\max}/2$ satisfy $0 \le t_{\text{lo}} \le t_{\text{hi}} \le L - 1$. Line L7 clamps $t$ into $[t_{\text{lo}}, t_{\text{hi}}]$: if the target is inside $V$, $t$ is its offset clamped to that interval; if it is outside, $t$ is $t_{\text{lo}}$ or $t_{\text{hi}}$. In both cases $t \in [0, L - 1]$. This proves the first claim.

For the second claim, let $r = \lceil s_{\max}/2\rceil$. If all sectors are free, the result is $k_t$ by line L5. Otherwise, the sectors $k_t - r, \dots, k_t + r$ are free and lie in one valley $V$, which contains $k_t$; line L6 picks it, since its distance to $k_t$ is 0 and a valley that does not contain $k_t$ has a positive distance. The offset $t$ of $k_t$ in $V$ satisfies $t \ge r \ge s_{\max}/2$ and $L - 1 - t \ge r \ge s_{\max}/2$, so $L \ge 2r + 1 > s_{\max}$, the valley is wide, and the clamp of line L7 leaves $t$ unchanged. The result is the center of $k_t$. $\square$

**The speed.** Line L8 gives $V_{\min} \le v \le V_{\max} + V_{\min}$, because $0 \le 1 - \min(h'_c, h_m)/h_m \le 1$ and $0 \le 1 - |\Omega|/\Omega_{\max} \le 1$ when $|\Omega| \le \Omega_{\max}$. The code clips $|\Omega|$ to $\Omega_{\max}$.

**The tests.** `test_histogram_matches_brute_force_and_rotates_with_the_grid` checks Lemmas 1 and 2 on 20 random grids. `test_steering_always_picks_a_free_sector` checks the theorem on 500 random histograms. `test_steering_hand_cases` and `test_smoothing_is_a_triangular_average` check the rules on small cases worked by hand, and `test_speed_rule` checks line L8.
