---
tag: M3H1CF
kind: model
slug: island-style-fpga
name: Island-style FPGA
aliases:
- island-style FPGA
- mesh FPGA architecture
area: eda/fpga-analog-and-emerging-technologies
level: intro
summary: The FPGA architecture model with a grid of logic blocks in a sea of routing channels, joined by connection blocks and switch blocks, on which FPGA CAD tools work.
prereqs: [lut-mapping]
see_also: [fpga-logic-cluster, fpga-switch-block, universal-switch-block, routing-resource-graph, minimum-channel-width, fpga-packing, negotiated-congestion-routing, global-routing]
sources:
  - book: isbn:9780792384601
    title: Vaughn Betz, Jonathan Rose and Alexander Marquardt, Architecture and CAD for Deep-Submicron FPGAs, Kluwer, 1999 (doi 10.1007/978-1-4615-5145-4)
    locator: Chapter 2, Section 2.1 FPGA Architecture; Chapter 4, Section 4.2 Architecture Parameterization and Generation; Chapters 5 to 7 on the global routing, cluster and detailed routing architecture
  - paper: doi:10.1145/2617593
    title: Jason Luu and others, VTR 7.0, next generation architecture and CAD system for FPGAs, ACM Transactions on Reconfigurable Technology and Systems 7(2), 2014
    locator: the description of the flagship architecture k6_frac_N10_mem32K_40nm (general locator)
  - paper: doi:10.1145/225871.225886
    title: Yao-Wen Chang, D. F. Wong and C. K. Wong, Universal switch modules for FPGA design, ACM Transactions on Design Automation of Electronic Systems 1(1), 80 to 101, 1996
    locator: the model of the routing channels, the switch modules with W tracks on each side and the flexibility Fs
  - paper: "Jonathan Rose, Abbas El Gamal and Alberto Sangiovanni-Vincentelli, Architecture of field-programmable gate arrays, Proceedings of the IEEE 81(7), 1013 to 1029, 1993"
    locator: the survey of FPGA architectures, with the symmetrical array (island) form and its row-based and hierarchical alternatives (general locator)
  - paper: "Yu-Liang Wu, Shuji Tsukiyama and Malgorzata Marek-Sadowska, Graph based analysis of 2-D FPGA routing, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 15(1), 33 to 44, 1996"
    locator: the NP-completeness of detailed routing of a given global routing in an array with the Xilinx-style switch blocks (general locator)
---

An island-style FPGA is the architecture model of a field-programmable gate array in which logic blocks sit in a two-dimensional grid, like islands, and routing channels run between all rows and all columns of blocks. A *connection block* joins the pins of a block to the tracks of the channel next to it, and a *switch block* at each crossing of two channels joins the tracks of the channels. The model belongs to the FPGA CAD topic of this sub-area. It is a representation, not a cost model: it fixes the structure and its parameters, on which packing, placement and routing tools work, and it counts the resources that a design uses.

## The machine

The model fixes a structure with a few integer and fractional parameters. All symbols below are definitions of the model. The values in the next subsection are typical values of named architectures.

- **Grid.** The logic blocks have positions $(x, y)$ with $1 \le x \le n_x$ and $1 \le y \le n_y$. Positions on the border, $x \in \{0, n_x + 1\}$ or $y \in \{0, n_y + 1\}$, hold I/O blocks, each with a fixed number of pads. In a heterogeneous array, some columns hold other block types, such as memories or multipliers, and a block of such a column may span several rows.
- **Logic block.** Each logic block is an [FPGA logic cluster](/fpga-logic-cluster/) of $N$ elements, each with a $K$-input lookup table (LUT) and a flip-flop, and with $I$ input pins and $N$ output pins.
- **Channels.** A horizontal channel runs between rows $y$ and $y + 1$ for $0 \le y \le n_y$, and a vertical channel runs between columns $x$ and $x + 1$ for $0 \le x \le n_x$. Every channel has the same number $W$ of parallel *tracks*, the channel width.
- **Segments.** A track is cut into wire segments. A segment of length $L$ spans $L$ logic blocks. With $L = 1$, every segment ends at the next switch block.
- **Connection block.** Each input pin of a block can connect to $F_{c,in}$ of the tracks of an adjacent channel, and each output pin to $F_{c,out}$ of them. Each $F_c$ is either an absolute number of tracks or a fraction of $W$.
- **Switch block.** At each crossing of a horizontal and a vertical channel, a switch block joins the ends of the segments that meet there. The *flexibility* $F_s$ is the number of segment ends that one segment end can connect to. The pattern of these connections is the subject of [FPGA switch block](/fpga-switch-block/).
- **Switches.** A switch is a pass transistor or a buffer that a configuration bit turns on. With bidirectional wires, one switch can drive either way. With single-driver wires, each segment is driven by one multiplexer at its start.

The model assumes that the tracks of a channel are equivalent, so a net can use any free track, and that every channel has the same width. A routing of a design must give each net its own set of segments and switches: two nets never share a segment. The [routing resource graph](/routing-resource-graph/) turns all of this into one directed graph.

### Typical values of named architectures

These numbers are not part of the model. They are the parameters of two well-known architectures.

| parameter | VTR 7.0 flagship (k6_frac_N10_mem32K_40nm) | studies of Betz, Rose and Marquardt (1999) |
| --- | --- | --- |
| LUT size $K$ | 6 (fracturable into two 5-LUTs) | 4 in most experiments |
| elements per cluster $N$ | 10 | 1 to 20 in the cluster study |
| cluster inputs $I$ | 40 | $I = K(N + 1)/2$, for example 22 for $K = 4$, $N = 10$ |
| segment length $L$ | 4, single-driver wires | 1 and longer lengths in the routing study |
| $F_{c,in}$, $F_{c,out}$ | 0.15 and 0.10 of $W$ | studied as parameters |
| $F_s$ | 3 | 3 |

The VTR flagship also has columns of 32 Kbit memories and of multipliers. Betz, Rose and Marquardt chose $I = K(N + 1)/2$ because, in their experiments, this many inputs let about 98% of the elements in the clusters be used.

## What it counts

The model counts the resources of the array and the resources that a mapped design uses.

- **Blocks.** The design needs $n_x n_y$ at least as large as the number of clusters, and enough I/O positions for its pads. Tools usually pick the smallest square array that fits.
- **Channel width.** The smallest $W$ for which a router finds a legal routing, $W_{min}$, is the main measure of how hard a design is to route. It is defined on [minimum channel width](/minimum-channel-width/).
- **Segments.** With $L = 1$, the array has $n_x (n_y + 1)$ horizontal and $n_y (n_x + 1)$ vertical channel pieces, each with $W$ segments, so it has $W \left( n_x (n_y + 1) + n_y (n_x + 1) \right)$ segments.
- **Switch block switches.** A switch block with $s$ sides and the usual $F_s = 3$ pattern has one switch for each track and each pair of sides, so $W s (s - 1)/2$ switches: $6W$ inside the array, $3W$ on an edge and $W$ at a corner.
- **Connection block switches.** A block with $p$ pins, each on $F_c W$ tracks, adds $p F_c W$ switches.
- **Area.** Betz, Rose and Marquardt measure the area as the number of minimum-width transistor areas of all switches, buffers and configuration bits, so the counts above, weighted by the size of each switch, give the routing area.
- **Delay.** Each segment and switch has a resistance and a capacitance, and the delay of a routed net is the Elmore delay of its tree. The critical path delay comes from [static timing analysis](/static-timing-analysis/) with these delays.

**Example.** Take $n_x = n_y = 2$, $W = 2$ and $L = 1$. The array has $2 (2 \cdot 3 + 2 \cdot 3) = 24$ segments. Its $3 \times 3 = 9$ switch blocks are one inner block with $6W = 12$ switches, four edge blocks with $3W = 6$ each and four corner blocks with $W = 2$ each, so $12 + 24 + 8 = 44$ switches. If each logic block has 4 input pins and 1 output pin, all with $F_c = 1$ (every track of one adjacent channel), the pins of the four logic blocks add $4 \cdot 5 \cdot 2 = 40$ switches. For a $10 \times 10$ array with $W = 40$, the same formulas give 8800 segments and 23,920 switch block switches.

## Relation to other models

- **Routing resource graph.** The [routing resource graph](/routing-resource-graph/) is the island-style array written as a directed graph. Routers such as [negotiated congestion routing](/negotiated-congestion-routing/) work on that graph and never see the grid.
- **ASIC routing grid.** The gcell grid of [global routing](/global-routing/) for standard cells also has rows and columns with a capacity, but a capacity is a count of free tracks. In the FPGA every track and every switch is a fixed object, so the routing must also fit the switch patterns, which [detailed routing](/detailed-routing/) of an ASIC does not have.
- **Row-based and hierarchical FPGAs.** Row-based FPGAs put blocks in rows with horizontal channels between them, as in mask-programmed gate arrays. Hierarchical FPGAs join blocks by a tree of local and global buses. Rose, El Gamal and Sangiovanni-Vincentelli survey these forms. Most academic tools and many commercial families use the island form.
- **Packing, placement and mapping.** The logic of a design reaches the array in three steps: [LUT mapping](/lut-mapping/) into $K$-input LUTs, [FPGA packing](/fpga-packing/) into clusters, and placement of the clusters on the grid, with [annealing](/fpga-timing-driven-annealing-placement/) or [analytical](/heap-fpga-placement/) methods.

## Known results in the model

- **Switch blocks.** For four sides with $W$ tracks each and $F_s = 3$, a [universal switch block](/universal-switch-block/) with $6W$ switches routes every set of two-pin connections that the side widths allow, and no switch block with fewer switches does so (Chang, Wong and Wong 1996). The planar pattern of the Xilinx XC4000 family is not universal.
- **Detailed routing is hard.** Given a global routing, deciding whether it can be completed on the tracks of an array with the planar switch pattern is NP-complete (Wu, Tsukiyama and Marek-Sadowska 1996). See [SAT-based FPGA routing](/sat-based-fpga-routing/).
- **Cluster inputs.** In the experiments of Betz, Rose and Marquardt (Chapter 6), $I = K(N + 1)/2$ inputs per cluster suffice for about 98% use of the logic elements. This is a measured result.
- **Measured trade-offs.** The same book measures the area and the delay of the array as functions of $K$, $N$, $L$, $F_c$ and the switch type, on the MCNC benchmarks with the VPR tools. These are measured results for the process and the circuits of the study, not theorems.

## References
