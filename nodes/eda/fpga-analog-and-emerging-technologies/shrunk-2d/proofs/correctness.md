---
title: Shrunk-2D scales the wirelength by 1/sqrt(2), and its split is balanced in every bin, never raises the cut, ends, and gives an MIV to every cut net
proves: [correctness]
status: full
---

We use the notation of the page: $s = 1/\sqrt{2}$, $n$ cells with areas $a(v) > 0$, nets $e$ that are sets of cells and fixed pads, $k \times k$ bins, and for a bin $b$ its cell area $A_b$, its largest cell area $a_b$, and the limit $\lambda_b = \max(\varepsilon A_b, 2 a_b)$. A split $t : V \to \{0, 1\}$ is *balanced* if $|\delta_b| \le \lambda_b$ for every bin, where $\delta_b = \sum_{v \in b,\, t(v) = 0} a(v) - \sum_{v \in b,\, t(v) = 1} a(v)$. The cut $\mathrm{cut}(t)$ is the number of nets with cells on both tiers.

**Lemma 1 (scaling).** Call a placer *scale-equivariant* if, when every pad and the die side are multiplied by $c > 0$, every cell coordinate it returns is multiplied by $c$. If the placer is scale-equivariant, then after line L1 every net has half-perimeter wirelength exactly $s$ times its value in the 2D placement, so the total is $s \approx 0.7071$ times the 2D total, a decrease of $1 - s \approx 29.29\%$.

*Proof.* The half-perimeter wirelength of a net is $\max x - \min x + \max y - \min y$ over its pins. If every pin coordinate is multiplied by $s$, each max and min is multiplied by $s$, and so is the sum. Pads are scaled at line L1 and cell coordinates are scaled by the assumption. Summing over the nets gives the total. $\square$

**Lemma 2 (the placer of the code is scale-equivariant).** The quadratic placement with the clique model, solved by Gauss-Seidel from the die center, and the spreading by rank are both scale-equivariant.

*Proof.* The clique weights $1/(p - 1)$ depend only on the net sizes, which do not change. A Gauss-Seidel step sets $x_i$ to a weighted mean of the current coordinates of its neighbors and of its pads, with fixed weights. If the start point and all pads are multiplied by $c$, then by induction every iterate is too, because a weighted mean of values that are all multiplied by $c$ is multiplied by $c$. The stop test compares the change with $\mathrm{tol} \cdot W$, and both sides scale by $c$, so the same iterate is returned. (The same holds for the exact solution, since $L x = b$ with the Laplacian $L$ fixed gives $L (c x) = c b$.) The rank spreading orders the cells by $x_i / W$, which does not change, and puts rank $r$ at $(r + 1/2) W / n$, which scales with $W$. $\square$

In floating point, Lemma 2 holds up to rounding; the code rounds $x_i / W$ to nine digits before ranking, so the order is the same unless two cells are within $10^{-9} W$ of each other. The tests check the ratio $s$ to a relative error of $10^{-9}$.

**Lemma 3 (the start is balanced).** After line L5, $|\delta_b| \le a_b \le \lambda_b$ for every bin.

*Proof.* Fix a bin. Its cells are added one at a time, each to the tier with less area. Before the first cell, $\delta_b = 0$. Suppose $|\delta_b| \le a_b$ before a cell of area $a \le a_b$ is added, and say $\delta_b \ge 0$, so the cell goes to tier 1 (if $\delta_b = 0$ it goes to tier 0, the same case by symmetry). The new difference is $\delta_b - a$, and $-a \le \delta_b - a \le \delta_b$, so $|\delta_b - a| \le \max(a, \delta_b) \le a_b$. The order of the cells does not matter for this bound. $\square$

**Lemma 4 (FM keeps balance).** Every split that line L7 produces, and the split after line L8, is balanced.

*Proof.* Line L7 moves a cell $v$ of bin $b$ only if the new difference, $\delta_b \mp 2 a(v)$, has absolute value at most $\lambda_b$; the differences of the other bins do not change. So every split in the sequence of moves of a pass is balanced if the first one is. Line L8 keeps a prefix of the moves, so its split is one of the splits in the sequence. By Lemma 3 the first pass starts balanced, and each later pass starts from the split of the last one. $\square$

**Lemma 5 (gain).** The gain of a cell $v$ on tier $t$, $g(v) = |\{e \ni v : e \text{ has one cell on tier } t\}| - |\{e \ni v : e \text{ has no cell on tier } 1 - t\}|$, counted over nets with at least two cells, is the decrease of the cut when $v$ moves.

*Proof.* Moving $v$ changes only the nets that contain it. A net in which $v$ is the only cell on its tier, and which has cells on the other tier, becomes uncut; if it has no cell on the other tier, it has only one cell, which the count excludes. A net with no cell on the other tier is uncut and becomes cut, since it has another cell left on tier $t$. Every other net stays cut. The code updates the counts of each net after every move, so it uses the gain of the current split. $\square$

**Lemma 6 (the cut never rises, and the loop ends).** The cut after each pass is at most the cut before it, and the loop ends after at most $\mathrm{cut}_{L5} + 1$ passes.

*Proof.* By Lemma 5, the cut after the first $j$ moves of a pass is the cut at its start minus the sum of the first $j$ gains. Line L8 keeps the prefix with the largest sum, and the empty prefix has sum 0, so the kept sum $G$ is at least 0 and the cut does not rise. If $G \le 0$, the loop stops at line L9. Otherwise $G \ge 1$, because gains are integers, and the cut falls by at least 1. The cut is a nonnegative integer, so at most $\mathrm{cut}_{L5}$ passes have $G \ge 1$. Each pass is finite, because each move locks a cell. $\square$

**Theorem 7.** Line L11 returns a split that is balanced in every bin, whose cut is at most that of line L5, with one MIV for each cut net, and the two tiers together with the MIVs connect exactly the nets of the input.

*Proof.* Balance is Lemma 4, the cut and termination are Lemma 6. Line L10 adds an MIV for every net with cells on both tiers, so each such net is joined across the tiers; a net with all cells on one tier is routed in that tier. No cell or net is added or removed by the split, so the netlist is the same. $\square$

**What is not proved.** The cut is not shown to be the least balanced cut; bisection with a balance rule is NP-hard (see the reduction on [tier partitioning](/tier-partitioning/)), and the tests measure the gap on small cases. Lemma 1 is about the ideal placer; a real 2D tool legalizes and optimizes timing and is not scale-equivariant, which is why Panth et al. measure 27.05% and not 29.3%. The power results are measurements of the paper.
