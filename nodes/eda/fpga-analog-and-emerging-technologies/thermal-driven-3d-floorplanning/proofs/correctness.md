---
title: What thermal-driven 3D floorplanning guarantees
proves: [correctness]
status: full
---

The method is a heuristic, and there is no claim that it finds an optimal floorplan. This file proves the guarantees it does have, for the code of this page: every floorplan it sees is legal, its result is no worse than its start, the closed-form thermal model is exact for the model it stands for, and, with two layers, its moves can reach every floorplan. A floorplan is a list of layers, each with a sequence pair $(\Gamma_+, \Gamma_-)$ of the blocks on it, and a rotation flag per block. It is *well formed* if each block is in exactly one layer and the two orders of each layer hold the same blocks.

**Lemma 1 (moves keep a floorplan well formed).** If $F$ is well formed, so is every floorplan that PERTURB returns.

*Proof.* Look at each move. Rotation changes only a flag. Swap and interlayer swap exchange the names $a$ and $b$ in every sequence; a bijection on names keeps each block in exactly one layer, and each layer's two orders still hold the same set, with $a$ and $b$ exchanged in both. Reverse exchanges two entries of $\Gamma_+$ only, which does not change the set it holds. Move removes $b$ from both orders of its layer and inserts it again into both. Z-neighbor swap is a swap. Z-neighbor move removes $b$ from both orders of its layer and inserts it into both orders of one other layer: next to $z$, or, when there is no $z$, at random places of a random other layer. In every case, each block is in exactly one layer and both orders of each layer hold the same set. ∎

**Lemma 2 (packing has no overlap).** For a well-formed layer, the corners that PACK-LAYER computes give no two blocks of the layer a common interior point.

*Proof.* Take two blocks $a \ne b$ of the layer. Exactly one of these holds: $a$ is before $b$ in both orders, $b$ is before $a$ in both, $a$ is before $b$ in $\Gamma_-$ only, or $b$ is before $a$ in $\Gamma_-$ only. In the first case PACK-LAYER takes the maximum over all $a'$ before $b$ in both orders, so $x_b \ge x_a + w_a$ and $a$ is left of $b$, with no common interior point; the second case is the same with the names exchanged. If $a$ is before $b$ in $\Gamma_-$ and after $b$ in $\Gamma_+$, then $a$ is among the blocks before $b$ in $\Gamma_-$ that come after $b$ in $\Gamma_+$, so $y_b \ge y_a + h_a$ and $a$ is below $b$; the last case is the same with the names exchanged. The loops visit blocks in the order of $\Gamma_+$ for $x$ and of $\Gamma_-$ for $y$, so $x_a$ and $y_a$ are final when they are used. ∎

**Theorem 3 (every floorplan seen is legal).** Every floorplan that the annealing builds has each block on one layer and no overlap within a layer.

*Proof.* Line L1 puts each block in one layer and copies each $\Gamma_+$ into $\Gamma_-$ before shuffling, so the start is well formed. By Lemma 1 and induction on the moves, so is every floorplan after it, and by Lemma 2 none has an overlap. ∎

**Lemma 4 (the result is no worse than the start).** THERMAL-3D-FLOORPLAN returns a floorplan whose cost is at most the cost of the start, and the returned cost is the cost of the returned floorplan.

*Proof.* Line L2 sets the best floorplan to the start and the best cost to its cost. Line L8 replaces both only by a floorplan and its own cost, and only when that cost is lower. So the best cost never rises and always belongs to the best floorplan. ∎

**Lemma 5 (the closed form).** Take one tile stack with nodes $1, \dots, L$ from the sink up, joined by a chain of resistors: $R_b$ from the sink to a base node, $R_1$ from the base node to node 1, and $R_j$ from node $j-1$ to node $j$ for $j \ge 2$. Put a heat source $P_i \ge 0$ at node $i$, the sink at $T_s$, and no other path for heat. Then in steady state the top node has
$$T_L = T_s + R_b \sum_{i=1}^{L} P_i + \sum_{i=1}^{L} P_i \sum_{j=1}^{i} R_j,$$
and $T_L$ is the largest temperature in the stack.

*Proof.* In steady state the heat that enters a node equals the heat that leaves it. The only path to the sink goes down the chain, so the heat that flows through $R_j$ is the heat made at node $j$ and above, $\sum_{i \ge j} P_i$, and the heat through $R_b$ is $\sum_i P_i$. Each resistor raises the temperature by its resistance times the heat through it. Summing from the sink up,
$$T_L = T_s + R_b \sum_{i} P_i + \sum_{j=1}^{L} R_j \sum_{i \ge j} P_i.$$
Exchanging the order of the double sum, the pair $(i, j)$ with $j \le i$ appears once on each side, which gives the formula. Every term added on the way up is a resistance times a sum of powers, which is not negative, so the temperature does not fall from one node to the next and the top node is the hottest. ∎

Lemma 5 is what STACK-TOP-TEMPERATURE computes, with resistances per unit area and the mean power density of the tile, so the code computes the peak of the model exactly. It says nothing about how close the model is to a real chip: it leaves out lateral flow, which spreads heat from a hot tile to its cooler neighbors, so it overstates the peak of small hot blocks.

**Corollary 6 (hot blocks belong next to the sink).** In one tile stack, exchanging the powers $P_i$ and $P_k$ of two layers $i < k$ changes $T_L$ by $(P_i - P_k) \sum_{j=i+1}^{k} R_j$. So putting the larger power on the lower layer never raises the peak of that stack.

*Proof.* Write $S_i = \sum_{j \le i} R_j$. In Lemma 5 the power of layer $i$ has the weight $S_i$, and the other terms do not change. Before the exchange the two layers add $P_i S_i + P_k S_k$; after it they add $P_k S_i + P_i S_k$. The change is $P_k S_i + P_i S_k - P_i S_i - P_k S_k = (P_i - P_k)(S_k - S_i) = (P_i - P_k) \sum_{j=i+1}^{k} R_j$. If the larger power was on top, $P_k \ge P_i$, this is at most 0, which is the claim. ∎

In the example of the page, $P = 5$ and $1$, $R_2 = 1$, so the hot block next to the sink is cooler by $(5 - 1) \cdot 1 = 4$.

**Lemma 7 (reachability with two layers).** With two layers, from any well-formed floorplan the moves of the code can reach any other well-formed floorplan with the same blocks.

*Proof.* Let $F$ be the current floorplan and $G$ the target. First fix the layers. For each block whose layer differs in $F$ and $G$, take a z-neighbor move of that block. If it has a z-neighbor $z$, the move puts it in the layer of $z$, which is not its own and so is the other layer; if it has none, the move puts it on a random other layer, which with two layers is again the other one. So each such move changes the layer of one block, and after these moves every block is on its layer in $G$. Next fix the orders of each layer with $m \ge 2$ blocks (with one block there is only one sequence pair). A move of block $b$ removes it from both orders and inserts it at any place in each, chosen independently; inserting it at its old place in one order changes only the other. So a move can put any block at any place of $\Gamma_+$ alone, or of $\Gamma_-$ alone. Take the blocks in reverse order of $G$'s $\Gamma_+$ and move each to the front of $\Gamma_+$, keeping its place in $\Gamma_-$; then $\Gamma_+$ is $G$'s. Do the same for $\Gamma_-$, keeping the places in $\Gamma_+$. Last, rotate each block whose flag differs. Each step is a move the code can choose with positive probability. ∎

With three or more layers the lemma can fail: a z-neighbor move puts a block on the layer of its z-neighbor, so an empty layer is filled only when some block has no near block on any other layer. The tests use two layers.

**What is not proved.** Nothing here bounds how far the result is from an optimal floorplan, or how many moves the annealing needs. The test file measures the gap against an exhaustive search on tiny instances, and the page reports the numbers under "What is measured".
