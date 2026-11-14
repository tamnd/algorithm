---
tag: RF40PK
kind: algorithm
slug: thermal-driven-3d-floorplanning
name: Thermal-driven 3D floorplanning
aliases:
- Cong-Wei-Zhang 3D floorplanning
area: eda/fpga-analog-and-emerging-technologies
level: research
summary: Cong, Wei and Zhang's 3D floorplanner that anneals the CBA representation, a TCG per layer plus buckets, with a cost that includes the peak temperature from a thermal model.
solves: [floorplanning, tier-partitioning]
model: word-ram
complexity:
  vars: {n: the number of blocks, p: the number of pins, L: the number of device layers, g: the number of tiles on each side of the thermal grid, M: the number of moves of the annealing}
  time: {one move with the closed-form model: O(n^2 + p + g^2 L + n g^2), annealing: O(M (n^2 + p + g^2 L + n g^2))}
  space: {total: O(n^2 + p + g^2 L)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 2004
  people: [Jason Cong, Jie Wei, Yan Zhang]
  note: By the authors' account the first thermal-driven floorplanner for 3D ICs; it added a bucket structure and z-neighbor moves to a 2D representation of each layer, and put a thermal model inside the annealing.
prereqs: [floorplanning, simulated-annealing, three-dimensional-integrated-circuit, compact-thermal-model]
see_also: [sequence-pair, b-star-tree-floorplan, floorplan-constraint-graphs, tier-partitioning, through-silicon-via, shrunk-2d, simulated-annealing-placement, heat-equation]
sources:
  - paper: doi:10.1109/ICCAD.2004.1382591
    title: "Jason Cong, Jie Wei and Yan Zhang, A thermal-driven floorplanning algorithm for 3D ICs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2004), pages 306 to 313"
    locator: Section 2 (the problem, room temperature 27 C at the sink), Section 3.1 (CBA, a TCG per layer and a bucket structure), Section 3.2 (the seven moves, the z-axis neighbor cost), Section 3.3 (Equation 1, the weighted cost), Section 4 (10 x 10 tiles; 4.1 CBA-T, the resistive network; 4.2 CBA-T-Fast, Equations 2 and 3; 4.3 CBA-T-Hybrid; 4.4 white space), Section 5 (MCNC and GSRC benchmarks, four layers, Tables 1 to 3)
  - paper: doi:10.1109/DAC.2001.935608
    title: "Jai-Ming Lin and Yao-Wen Chang, TCG, a transitive closure graph-based representation for non-slicing floorplans, Proceedings of the 38th Design Automation Conference (DAC 2001), pages 764 to 769"
    locator: the transitive closure graph of each layer and its moves rotation, swap, reverse and move (general locator)
---

Thermal-driven 3D floorplanning is the method of Cong, Wei and Zhang (ICCAD 2004) for placing the blocks of a block-level [3D IC](/three-dimensional-integrated-circuit/), a topic of 3D integration in EDA. Each block gets a device layer and a place in that layer. The goal is a small footprint, short wires and few interlayer vias, with the peak temperature kept low. The method is [simulated annealing](/simulated-annealing/) over a representation called CBA, *combined bucket and 2D array*: a 2D floorplan for each layer, written as a transitive closure graph (TCG), and a grid of buckets over the stack that records which blocks of different layers lie above one another. The buckets make *z-neighbor* moves possible, which move a block to a nearby place in another layer. The cost includes the peak temperature from a thermal model. A closed-form model, CBA-T-Fast, gives each layer a weight that grows with its distance from the heat sink, so the search puts hot blocks next to the sink.

## In plain words

You have a set of rectangular blocks and a few stacked layers of silicon, with the heat sink under the bottom layer. You want to place every block on some layer, with no two blocks of one layer overlapping, so that the stack is small, connected blocks are close, few connections go between layers, and nothing gets too hot.

Heat leaves through the bottom. A hot block on the top layer must push its heat through every layer below it, so it gets much hotter than the same block on the bottom layer. The method tries many small changes to the floorplan, such as swapping two blocks or moving one to a nearby spot in another layer, and keeps changes that make a mix of size, wires, vias and temperature better, plus some worse ones early on so it does not get stuck.

## The problem

**Input.** A set of $n$ rectangular blocks, block $b_i$ with width $w_i$, height $h_i$ and a fixed power density $q_i$; each block may rotate. A set of nets over the blocks. A number of device layers $L$ (the paper uses 4), with layer 1 next to the heat sink.

**Output.** For each block a layer $l_i$ and a lower-left corner $(x_i, y_i)$, with no two blocks of one layer overlapping.

**Goal.** The paper minimizes chip area, wirelength and the number of interlayer vias, under a limit $T_0$ on the peak temperature. The chip area is the largest area among the layers. An interlayer via goes through a device layer, and at that time its pitch was about 25 µm, against below 0.5 µm for a via between metal layers, so vias are costly. The bottom of the stack is held at room temperature, 27 °C, and the sides and top are insulated. The problem contains 2D floorplanning, which is NP-hard, so the method is a heuristic.

## The algorithm

The cost of a floorplan $F$ (Equation 1 of the paper) is

$$\mathrm{cost}(F) = \alpha \cdot \mathrm{nwl} + \beta \cdot \mathrm{narea} + \gamma \cdot \mathrm{nvc} + \delta \cdot C_T,$$

where nwl, narea and nvc are the wirelength, the chip area and the number of interlayer vias, each normalized, and $C_T$ is a cost of the peak temperature $T$. In the paper, $C_T$ is a function of $T$ in three tiers that rises steeply past the limit $T_0$.

```pseudo id=main
THERMAL-3D-FLOORPLAN(blocks, nets, L, weights)
L1  put the blocks on the layers, build a 2D floorplan of each layer, and pack it
L2  compute the cost of the floorplan, with the temperature from the thermal model
L3  for each temperature τ of the annealing schedule:
L4      repeat a fixed number of times:
L5          perturb: rotation, swap, reverse, move, interlayer swap, z-neighbor swap or z-neighbor move; global moves more often while τ is high, local moves as τ falls
L6          pack the changed layers, update the buckets, and compute the new cost
L7          accept the new floorplan if its cost is lower, or else with probability exp(−Δ/τ)
L8          keep the best floorplan seen
L9  return the best floorplan
```

**CBA.** Each layer is a 2D floorplan in its own TCG, and a packing gives the places in that layer. Over the stack lies a grid of buckets. Bucket $i$ holds the set $IB(i)$ of blocks of any layer that meet it, and block $j$ holds the set $IBT(j)$ of buckets it meets. After every move only the moved blocks are updated, and every 20 moves or so all buckets are built again, since the buckets only point to blocks that are likely close.

**The seven moves.** Rotation, swap (two blocks of one layer), reverse (the relation of two blocks in one layer) and move (a block from one side of another to a different side) are the moves of TCG, inside one layer. Interlayer swap exchanges two random blocks of different layers. The z-axis neighbor of block $j$ is the block $k$ of another layer, among the blocks that share a bucket with $j$, of least cost $\alpha |A_k - A_j| + \beta (|x_k - x_j| + |y_k - y_j|)$: close and of similar area. Z-neighbor swap exchanges $j$ with it. Z-neighbor move takes $j$ out of its layer and puts it next to $k$, to its right or above it, in $k$'s layer. Rotation, swap and interlayer swap are global and are used more at high temperature; the others change the floorplan locally and are used more as it cools.

**Thermal models.** The stack is cut into a grid of tiles, $10 \times 10$ in the paper, and the power of a tile in a layer is the sum of the power densities times the overlap areas of the blocks that meet it.

- **CBA-T** uses a compact resistive [thermal model](/compact-thermal-model/): one node per tile per layer, lateral resistors between neighbor tiles in a layer, a vertical resistor $R_i$ per layer and $R_b$ for the bottom, with values from finite-element simulation. The tile powers are current sources, and the temperatures are the node voltages. The matrix does not change between floorplans, so its LU factors are reused. To save time, the temperature is computed only after moves that change it much: global moves and moves between layers.
- **CBA-T-Fast** looks at each tile stack alone and uses only vertical heat flow. With the sink at room temperature $T_s$, the top node of a stack has
$$T_{\mathrm{top}} = T_s + R_b \sum_{i=1}^{L} P_i + \sum_{i=1}^{L} P_i \sum_{j=1}^{i} R_j,$$
which is Equation 3 of the paper written with the layers counted from the sink. The power of layer $i$ is multiplied by the resistances of all layers up to $i$, so a block costs more the farther it is from the sink. The peak is the largest $T_{\mathrm{top}}$ over the tile stacks. For the spread within a layer, the paper adds the largest difference of temperature among the tiles of each layer, normalized, as a weight on the peak.
- **CBA-T-Hybrid** uses the closed form during the annealing and the resistive network 20 times at each annealing temperature.

**After the annealing.** White space is added around each block for the interlayer vias, in proportion to its number of connections, and more around hot blocks for thermal vias; then the layers are packed again with the TCG relations kept.

**The code.** The implementation is a small model of the method. It uses a [sequence pair](/sequence-pair/) for each layer in place of a TCG, which the paper allows ("any 2D floorplan representation can be used"); swap, reverse and move are the sequence pair versions. It builds the buckets again after every move, on a $3 \times 3$ grid. When a z-neighbor move finds no near block in another layer, for example because the other layers are empty, it moves the block to a random place on another layer; without this, a layer that becomes empty can never be filled again. With two layers, every z-neighbor move then takes the block to the other layer. The area is that of the bounding box of all layers, the via count of a net is its largest layer minus its smallest, and each term is divided by its value at the start. **The thermal model is a toy:** it is CBA-T-Fast with the same area-specific resistances in every tile, the tile power taken as a mean power density, no lateral flow, no temperature spread term, and resistances that are not calibrated to any process. The cost uses the peak rise itself, not the three-tier function.

## Example

Take two blocks of $2 \times 2$, one hot with power density 5 and one cool with power density 1, two layers, and the toy model with $R_b = 0.5$ and $R_1 = R_2 = 1$ per unit area.

| floorplan | area | peak rise above the sink |
|---|---|---|
| stacked, hot block on layer 1 (next to the sink) | 4 | $0.5 \cdot 6 + 1 \cdot 6 + 1 \cdot 1 = 10$ |
| stacked, hot block on layer 2 | 4 | $0.5 \cdot 6 + 1 \cdot 6 + 1 \cdot 5 = 14$ |
| side by side on layer 1 | 8 | $(0.5 + 1) \cdot 5 = 7.5$ |

Stacking halves the area. With the blocks stacked, the hot block next to the sink is 4 units cooler, because its power passes through $R_b$ and $R_1$ only, while the power of the top layer passes through $R_2$ as well. Spreading the blocks side by side is cooler still, but doubles the area. The weights $\beta$ and $\delta$ decide which floorplan wins. The test file checks the first two rows.

## Correctness

There is no optimality claim to prove: the method is a heuristic for an NP-hard problem, and Cong, Wei and Zhang give none. The [proof file](proofs/correctness.md) proves what the method does guarantee. Every move keeps each block on exactly one layer and in both orders of that layer's pair, and every packing of a sequence pair has no overlap, so every floorplan seen is legal. The returned floorplan is the best one seen, so its cost is at most the cost of the start. The closed form of CBA-T-Fast is exactly the top temperature of a chain of resistors with the tile powers as sources, and in a chain the top node is the hottest one. With two layers and the empty-layer rule of the code, every floorplan can be reached from every other one by moves, so the move set does not shut the search out of the optimum. That is not a promise that a finite run finds it.

## Complexity

Packing one layer with $m$ blocks takes $O(m^2)$ for a sequence pair or TCG by longest paths ($O(m \log m)$ with the weighted longest common subsequence). The wirelength and via count take $O(p)$ for $p$ pins. The closed-form thermal model spreads each block over the tiles it meets, $O(n g^2)$ at most, and sums each of the $g^2$ stacks in $O(L)$. So a move costs $O(n^2 + p + g^2 L + n g^2)$, and the annealing with $M$ moves costs $M$ times that. CBA-T solves the resistive network of $g^2 L$ nodes; with a reused LU factorization of a dense matrix, each solve is $O(g^4 L^2)$, which is why the paper computes it only after some moves. The paper reports that its 25 by 25 by 4 network takes a few milliseconds per solve.

## Properties

**What is proved.** Every floorplan seen is legal (no overlap within a layer, each block on one layer), the result is no worse than the start, the closed form is exact for a vertical chain of resistors and its top node is the hottest, and with two layers the moves of the code can reach every floorplan.

**What is cited.** Cong, Wei and Zhang (2004, Section 5) test on MCNC and GSRC benchmarks with four layers, and give each block a random power density in a fixed range of W/m². Without the thermal term, CBA gives 29% less wirelength and 7% less area than the multi-layer floorplanner of Shiu, Ravichandran, Easwar and Lim (2004), and 3% less wirelength and 5% less area than an array of TCGs without the z-neighbor moves (on GSRC, 5.5% less wirelength). CBA-T lowers the peak temperature by 56% on average, at 21% more area, about the same wirelength and via count, and 9 times the run time. CBA-T-Fast lowers it by 40% at 2 times the run time, and CBA-T-Hybrid by 50% at 3 times. A finite-element check of ami33 gives a peak of 587.2 K without the thermal term and 425.1 K with it.

**What is measured.** The tests use the code and its toy model, with two layers and a $4 \times 4$ tile grid. On 15 random instances of 3 blocks (seed 3) and 2 of 4 blocks (seed 4), the annealing reaches the cost of an exhaustive search over every layer assignment, sequence pair and rotation, on all of them; a longer run with 30 and 6 instances gave the same. On 10 random instances of 8 blocks (seed 8), a thermal weight of 3 against 0 lowers the mean peak rise from 12.98 to 5.94 (54%) and raises the mean area from 13.3 to 18.3 (38%). These numbers come from a toy model on random blocks; they show the trend, not the values of a real chip.

## Variants and improvements

- **Other representations.** The layers can use a [sequence pair](/sequence-pair/), a [B*-tree](/b-star-tree-floorplan/) or any 2D representation, as the paper says. "True 3D" representations such as the 3D TCG or the sequence triple add the third axis but, as the paper argues, carry more information than a few discrete layers need.
- **Thermal vias.** Later work inserts thermal vias in white space to lower the vertical resistance of hot stacks, either after floorplanning or inside it.
- **TSV-aware floorplanning.** With [TSVs](/through-silicon-via/), the vias take area and need keep-out zones, so later floorplanners place the TSVs and count their area, not only their number.
- **Gate-level 3D.** For monolithic 3D, the layer of each cell is set by [tier partitioning](/tier-partitioning/), as in [Shrunk-2D](/shrunk-2d/), not by a block floorplanner.
- **Fast thermal analysis.** Better compact models and model order reduction give accurate temperatures at a cost close to the closed form.

## When to use it

Use it for block-level 3D integration with a few layers and tens to a few hundred blocks, when heat matters and the power of each block is known. Use the closed form or a hybrid inside the annealing and an accurate model at the end. For millions of cells, use a placer and a partitioner instead.

## Pitfalls

- **Hot blocks on top.** Without a thermal term, the search places blocks for area and wires only, and a hot block on the top layer can be far hotter than the same block next to the sink.
- **Area against heat.** Lowering the peak usually spreads hot blocks apart and raises the area; the paper reports 21% more area for a 56% lower peak. The weights must reflect what the design can afford.
- **A closed form without lateral flow.** It ignores heat that spreads within a layer, so it misjudges small hot blocks next to cool ones. Check the final floorplan with an accurate model.
- **Empty layers.** If the only moves between layers are swaps and moves to a neighbor in another layer, a layer that becomes empty can never be filled again.
- **Kelvin and Celsius.** The finite-element results of the paper are in kelvin, while its tables are in degrees Celsius. A percentage of a temperature depends on the scale, so compare temperature rises.

## Implementations

## History

Floorplanning by annealing over a representation began with slicing trees and the [sequence pair](/sequence-pair/) (1995), and TCG (Lin and Chang, DAC 2001) was one of several non-slicing representations. Thermal placement for 2D chips was studied in the late 1990s and early 2000s. Earlier 3D floorplanners either used a "true 3D" representation or one 2D representation per layer with few moves between layers. In 2004, Cong, Wei and Zhang combined a TCG per layer with buckets to get local moves between layers, and put a thermal model into the cost. This was, as they wrote, the first thermal-driven floorplanner for 3D ICs, and later 3D floorplanners added thermal vias and TSV planning.

## References
