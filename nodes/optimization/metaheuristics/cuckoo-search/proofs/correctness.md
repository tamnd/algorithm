---
title: Cuckoo search keeps its nests in the box, its nests only improve, the best nest does not move in the Lévy phase, and it returns the best point it evaluated
proves: [correctness]
status: full
---

We use the pseudocode of the page for minimizing $f$ on the box $B = \prod_{j=1}^D [\ell_j, u_j]$ with $\ell_j < u_j$ and $n \ge 2$. Let $x_i^{(t)}$ be nest $i$ and $g^{(t)}$ the stored best point after iteration $t$, with $t = 0$ for line L1.

**Claim 1 (feasibility).** Every nest and every proposal lies in $B$.

*Proof.* Line L1 draws the nests in $B$. Lines L3 and L6 clip each coordinate of the proposal to $[\ell_j, u_j]$, so every proposal lies in $B$. A nest is only ever set to a start point or to a proposal. $\square$

**Claim 2 (monotone nests).** For each $i$, $f(x_i)$ never increases, and every change of $x_i$ lowers $f(x_i)$ strictly.

*Proof.* Only lines L4 and L7 change $x_i$, and each sets $x_i \leftarrow y$ only if $f(y) < f(x_i)$. $\square$

**Claim 3 (the best point).** After line L1 and after each iteration, $f(g) = \min\{f(z) : z \text{ evaluated so far}\}$, and $g$ is one of these points. So $f(g)$ never increases.

*Proof.* After line L1, $g$ is the best start point, which is the only kind of point evaluated so far. Consider iteration $t$. Each proposal $y$ of line L3 or line L6 for nest $i$ is either accepted, so that $x_i = y$ right after, or rejected because $f(y) \ge f(x_i)$ at that time. In both cases, by Claim 2, $f(x_i)$ at line L8 is at most $f(y)$. Lines L5 and L8 set $g$ to the best of the old $g$ and the current nests. At line L8 this is at most $f(y)$ for every proposal $y$ of the iteration, and by induction at most the value of every earlier point. Also $g$ is the old $g$ or a nest, so it was evaluated. $\square$

**Claim 4 (the best nest does not move in line L3).** If $x_i = g$ at the start of line L3 for nest $i$, the proposal is $y = x_i$, and $x_i$ does not change in lines L3 and L4.

*Proof.* Every coordinate of the step is $\alpha L_j (x_{ij} - g_j) N_j = \alpha L_j \cdot 0 \cdot N_j = 0$, so $y_j = x_{ij}$, and clipping leaves $y_j$ unchanged because $x_{ij} \in [\ell_j, u_j]$ by Claim 1. Then $f(y) = f(x_i)$, so line L4 rejects $y$. $\square$

**Claim 5 (the second phase is a DE step).** In line L6, given $x_i$, $x_p$, $x_q$ and $r$, the proposal before clipping is $y = x_i + r \, K \odot (x_p - x_q)$, where $K \in \{0, 1\}^D$ has independent entries equal to 1 with probability $p_a$ and $\odot$ is the product by coordinates. The proposal equals $x_i$ with probability at least $(1 - p_a)^D$.

*Proof.* The first statement is line L6 written with the mask $K$. If $K = 0$, then $y = x_i$, and $P(K = 0) = (1 - p_a)^D$ because the entries are independent. The proposal also equals $x_i$ when $x_{pj} = x_{qj}$ in every chosen coordinate, for example when $p = q$, which has probability $1/n$. $\square$

The vector $x_i + r(x_p - x_q)$ is the mutant of DE with base vector $x_i$ and factor $F = r$, the mask $K$ is a crossover that takes the mutant in each coordinate with probability $p_a$, and line L7 is the one-to-one selection of DE. Claims 4 and 5 show that a part of the evaluations is spent on proposals equal to their nest.

**Remark.** No claim here says that $g$ approaches a global minimizer. The steps of line L3 are proportional to the distances $|x_{ij} - g_j|$, and the steps of line L6 to the differences between nests. If all nests come close to one point, both kinds of step become small, and a better region far away is reached only by a rare very large Lévy step. The heavy tail makes such steps possible, but their size is still scaled by the small distances, so no positive lower bound on the probability of reaching a fixed far region follows. $\blacksquare$
