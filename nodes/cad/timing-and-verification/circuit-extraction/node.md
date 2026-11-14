---
tag: 1BPKEA
kind: problem
slug: circuit-extraction
name: Circuit extraction
aliases:
- layout extraction
- netlist extraction
area: cad/timing-and-verification
level: core
summary: Recover the transistors, their connections and their sizes from the layer polygons of a layout, as a netlist.
prereqs: [rectilinear-polygon, disjoint-set, connected-components]
see_also: [union-find-connectivity, flood-fill, connected-component-labeling, corner-stitching, rectangle-intersection-reporting, polygon-clipping, design-rule-checking, parasitic-extraction]
sources:
  - paper: doi:10.1109/MDT.1986.294914
    title: Walter S. Scott and John K. Ousterhout, Magic's circuit extractor, IEEE Design and Test of Computers 3(1), 1986
    locator: the extraction of transistors and nets from the corner-stitched tile planes of Magic, and the hierarchical extraction of cells (general locator)
  - paper: doi:10.1109/TCAD.1984.1270061
    title: John K. Ousterhout, Corner stitching, a data-structuring technique for VLSI layout tools, IEEE Transactions on Computer-Aided Design 3(1), 87 to 100, 1984
    locator: the tile planes on which the extractor walks, and the search for connected tiles
  - paper: "Toshihide Imai and Takao Asano, Finding the connected components and a maximum clique of an intersection graph of rectangles in the plane, Journal of Algorithms 4(4), 310 to 323, 1983"
    locator: the connected components of the intersection graph of n rectangles in O(n log n) time, without listing all intersecting pairs
  - paper: doi:10.1145/321879.321884
    title: Robert Endre Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2), 215 to 225, 1975
    locator: the bound for union by rank with path compression, used for the net merging
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: the sections on physical verification and extraction (general locator)
---

Circuit extraction recovers the circuit that a chip layout draws. It reads the polygons of the mask layers and returns a netlist: the transistors and other devices, the nets that join their terminals, and the sizes of the devices, such as the width and the length of each transistor gate. It is an EDA problem. In EDA "extraction" means netlist extraction, the subject of this page, or [parasitic extraction](/parasitic-extraction/) of wire resistance and capacitance. In mechanical CAD the same word means feature extraction from a solid model, which is a different problem. Extraction does not know the intended circuit. Comparing its output with the schematic is [layout versus schematic](/layout-versus-schematic/), a separate step.

## In plain words

A chip drawing is a pile of colored shapes, one color per layer. Where a strip of polysilicon crosses a strip of diffusion, there is a transistor. Shapes on a metal layer that touch form one wire. A small square on the contact layer joins the metal above it to the shape below it.

Extraction turns these facts into a list. It finds every transistor and measures how wide and how long its gate is. It groups all the shapes that are joined, through touching or through contacts, into wires. Then it writes, for each transistor, which wire is at its gate and which wires are at its two other ends. The labels that the designer put on some shapes, such as the names of the supply wires, become the names of those wires.

## Definition

**Input.**

- A *layout*: for each layer a finite set of polygons with integer coordinates, mostly [rectilinear](/rectilinear-polygon/), with $n$ edges in all, and text labels at some points.
- A *technology description*: which layers conduct; which pairs of conducting layers a cut layer (contact or via) joins where it lies inside both; and which layer combinations form devices. For a MOS process, the *gate* region is polysilicon $\cap$ diffusion, the *source and drain* regions are diffusion minus polysilicon, and the type of the transistor comes from the diffusion type or the well.

**Model.** The *conductor regions* are the conducting layers, with the gate regions removed from the diffusion layers. Two points are *connected* when a path joins them inside one conductor region, or a cut joins the two regions in which they lie. A *net* is a class of this equivalence relation. A *device* is a connected part of the gate region. Its *terminals* are the nets of the conductor regions that touch it: the polysilicon over it is the gate, and the diffusion parts on its two sides are the source and the drain.

**Output.** A netlist: for each device its type, the net at each terminal, and its parameters (gate width $W$ and length $L$; for MOS also the area and the perimeter of the source and drain regions), and for each net the labels inside it. Two nets with the same label, or one net with two different labels, are reported.

## Variants

- **Hierarchical extraction.** Each cell is extracted once, and the netlist of a placement of cells is built from the netlists of the cells and the connections where cells overlap or abut. The flat result is the same.
- **Devices other than MOS transistors.** Resistors from marked polysilicon or diffusion, capacitors from overlapping plates, diodes and bipolar transistors, each with its own recognition rule and parameters.
- **Bent and odd-shaped gates.** For a gate that is not a rectangle, $W$ and $L$ come from a rule, for example the mean of the lengths of the two edges where the gate meets the source and the drain.
- **Well and substrate connectivity.** The bodies of the transistors connect through the wells and the substrate, which do not conduct as well as metal. Checkers report wells with no tie to a supply.
- **With parasitics.** The netlist is annotated with the resistance and capacitance of the nets. That is [parasitic extraction](/parasitic-extraction/), which runs on the nets found here.

## Examples

**A CMOS inverter.** The layers and rectangles $(x_0, y_0, x_1, y_1)$ are:

| layer | shapes |
| --- | --- |
| n-diffusion | $(0, 2, 10, 6)$ |
| p-diffusion | $(0, 12, 10, 16)$ |
| polysilicon | $(4, 0, 6, 22)$ |
| contact | $(1, 3, 3, 5)$, $(7, 3, 9, 5)$, $(1, 13, 3, 15)$, $(7, 13, 9, 15)$, $(4, 19, 6, 21)$ |
| metal 1 | GND $(0, 0, 3, 5)$, Y $(7, 3, 9, 15)$, VDD $(0, 13, 3, 18)$, A $(3, 19, 7, 21)$ |

The polysilicon crosses each diffusion strip once, so there are two gate regions, $(4, 2, 6, 6)$ and $(4, 12, 6, 16)$. Each has $W = 4$, the extent of the diffusion along the gate, and $L = 2$, the width of the polysilicon. Removing the gates cuts each diffusion strip into a left part and a right part. The contacts then join: the left n part to the metal GND, the right n part and the right p part both to the metal Y, the left p part to the metal VDD, and the polysilicon to the metal A. So there are 4 nets, and the netlist is

- an n-transistor with gate A, source and drain GND and Y, $W = 4$, $L = 2$;
- a p-transistor with gate A, source and drain VDD and Y, $W = 4$, $L = 2$.

**A short.** If the metal Y is drawn as $(6, 3, 9, 20)$, it overlaps the metal A in the square $(6, 19, 7, 20)$. The two become one net, which carries both labels Y and A, and the netlist has 3 nets, with each gate tied to its own drain. Extraction reports this circuit as it is drawn, with a warning for the net with two labels. Finding that it is not the intended inverter is the job of layout versus schematic. A scratch script checked both results by a cell-by-cell flood fill of the layers.

## Known algorithms

| Method | Idea | What is known |
| --- | --- | --- |
| Overlaps plus [disjoint sets](/disjoint-set/) | find the touching pairs of shapes with a sweep, and merge their nets | $O(n \log n + k)$ for the $k$ touching pairs by [rectangle intersection reporting](/rectangle-intersection-reporting/), plus near-linear time for the unions |
| Components without the pairs | the connected components of the intersection graph of rectangles (Imai and Asano 1983) | $O(n \log n)$ for $n$ rectangles, even when $k$ is quadratic |
| Tile walks | store each layer as a [corner-stitched](/corner-stitching/) plane and [flood fill](/flood-fill/) across neighbor tiles and contacts (Magic) | time proportional to the tiles visited, measured |
| Raster labeling | draw the layers into pixels and run [connected component labeling](/connected-component-labeling/) | time proportional to the number of pixels; exact only when coordinates lie on the pixel grid |
| Layer operations | gate and source and drain regions by [polygon clipping](/polygon-clipping/) of layers | the sweep bounds of the [DRC](/design-rule-checking/) page |
| Hierarchical extraction | extract each cell once and stitch the cells | the gain depends on the reuse of cells, measured |

The union step is [union-find connectivity](/union-find-connectivity/): the net of a shape is found after the overlaps are merged, so the order of the overlaps does not matter.

## Bounds

**Proved.** Deciding whether a layout has any transistor at all, that is whether polysilicon meets diffusion, needs $\Omega(n \log n)$ steps in the algebraic decision tree model, by the two-layer argument on the [design rule checking](/design-rule-checking/) page with rule distance 0. In the other direction, for layouts of $n$ rectangles the nets and the devices are found in $O((n + p) \log (n + p))$ time, where $p$ is the number of rectangles in the gate and in the source and drain regions that the layer operations produce: the layer operations by sweeps on rectilinear shapes, and the nets by the method of Imai and Asano on the rectangles of all conductor regions and cuts. The term $p$ is needed: $n/2$ polysilicon strips that cross $n/2$ diffusion strips make $n^2/4$ transistors.

**Measured.** On real layouts the number of touching pairs is linear in $n$, and tile walks and hierarchical extraction run in near-linear time. This is an observation from practice, not a theorem.

## Reductions

- **To connected components.** The nets are the [connected components](/connected-components/) of the graph with one vertex per shape and one edge per touching pair or per cut.
- **To layer operations.** Gate regions and source and drain regions are Boolean operations on layers, as in [DRC](/design-rule-checking/).
- **To layout versus schematic.** The output netlist is one input of [layout versus schematic](/layout-versus-schematic/). Extraction builds a netlist from geometry; LVS compares two netlists and never reads the geometry.
- **To parasitic extraction.** The nets found here are the input of [parasitic extraction](/parasitic-extraction/), which computes their resistance and capacitance.

## Applications

- **Physical verification.** Extraction followed by LVS shows that the layout implements the schematic.
- **Simulation of the layout.** The extracted netlist, with device sizes and parasitics, is simulated to confirm timing and function.
- **Antenna and well checks.** Rule checks that depend on connectivity, such as the antenna rules of [DRC](/design-rule-checking/), use the nets.
- **Reverse engineering and failure analysis.** Images of the layers of a manufactured chip are turned into polygons and then into a netlist.

## References
