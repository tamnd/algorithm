---
tag: DVS3A2
kind: concept
slug: three-dimensional-integrated-circuit
name: Three-dimensional integrated circuit
aliases:
- 3D IC
- 3D integration
area: eda/fpga-analog-and-emerging-technologies
level: intro
summary: A chip built from stacked tiers of devices joined vertically by through-silicon vias or monolithic inter-tier vias, to shorten wires and mix technologies.
prereqs: [rents-rule, floorplanning]
see_also: [through-silicon-via, tier-partitioning, shrunk-2d, thermal-driven-3d-floorplanning, compact-thermal-model, hypergraph-partitioning, half-perimeter-wirelength, clock-tree-synthesis]
sources:
  - paper: doi:10.1109/5.929647
    title: "Kaustav Banerjee, Shukri J. Souri, Pawan Kapur and Krishna C. Saraswat, 3-D ICs, a novel chip design for improving deep-submicrometer interconnect performance and systems-on-chip integration, Proceedings of the IEEE 89(5), 602 to 633, 2001"
    locator: Section I (the motivation, heterogeneous integration), Section III (the wire-length distribution of 2-D and 3-D chips from Rent's rule), and the analytical model of the temperatures of the active layers
  - book: isbn:9781441995414
    title: Sung Kyu Lim, Design for High Performance, Low Power, and Reliable 3D Integrated Circuits, Springer, 2013 (doi 10.1007/978-1-4419-9542-1)
    locator: the physical design of TSV-based 3D ICs, with parts on performance, power and on electrical, thermal and mechanical reliability (general locator)
  - paper: doi:10.1145/2627369.2627642
    title: "Shreepad Panth, Kambiz Samadi, Yang Du and Sung Kyu Lim, Design and CAD methodologies for low power gate-level monolithic 3D ICs, Proceedings of the International Symposium on Low Power Electronics and Design (ISLPED 2014), La Jolla"
    locator: Section 1 (transistor-level, gate-level and block-level monolithic 3D) and Section 4 (a 100 nm monolithic inter-tier via against a 500 nm face-to-face via, half the footprint of 2D, 15.57% less total power for OpenSPARC T2)
---

A three-dimensional integrated circuit (3D IC) is a chip made of two or more *tiers* of devices stacked on top of each other and joined by vertical connections. It is a topic of 3D integration in EDA. In a stacked 3D IC, each tier is made on its own wafer, and the tiers are bonded and joined by [through-silicon vias](/through-silicon-via/) (TSVs) or by bonding pads between the faces of two dies. In a monolithic 3D IC, the upper tier is grown on top of the lower one in the same process, and the tiers are joined by monolithic inter-tier vias (MIVs), which are much smaller. Stacking makes the footprint smaller and the wires shorter, and it can put different technologies, such as logic, memory and sensors, in one package. It also makes heat harder to remove, and it adds new design problems that 2D tools do not solve.

## In plain words

A normal chip is flat: all transistors sit on one layer of silicon, and many layers of metal wires above them connect them. When a chip grows, its wires get longer, and long wires are slow and use power.

A 3D IC builds the chip in floors, like a building. Gates that talk to each other a lot can sit on top of each other instead of far apart on one floor. The floors are joined by vertical wires. These come in two sizes: thick ones that go through a whole slice of silicon, and very thin ones in chips where the upper floor is made directly on the lower one.

The price is heat, because the floors are packed close and only one side touches the cooler, and new design work: the tools must decide which gate goes on which floor and where the vertical wires go.

## The idea

### Kinds of 3D integration

| style | vertical link | typical link size | granularity |
|---|---|---|---|
| die or wafer stacking, face to back | TSV through the thinned substrate | micrometers | blocks or whole dies |
| die or wafer stacking, face to face | bonding pads or hybrid bonds between the top metals | below a micrometer to micrometers | blocks or gates |
| monolithic (sequential) 3D | MIV between the tiers, like a normal via | about 100 nm | gates, or the two transistor types of one gate |

The sizes are orders of magnitude. Panth, Samadi, Du and Lim (ISLPED 2014) use a 100 nm MIV and a 500 nm face-to-face via in their study. TSVs are larger still and need a zone around them where no transistor may go; the [TSV page](/through-silicon-via/) gives the model. The size of the vertical link decides how fine the split between tiers can be. With TSVs, a design usually splits whole blocks or memories from logic. With MIVs, the split can go down to single gates, and Panth et al. describe gate-level, transistor-level and block-level monolithic styles. A *2.5D* design places several dies side by side on a silicon interposer; it shares some tools with 3D, but the dies are not stacked.

### Why stacking shortens wires

Take a design of area $A$ and put it on $L$ tiers of equal area. Each tier has side $\sqrt{A / L}$, so every distance in the plane shrinks by the factor $1 / \sqrt{L}$, while the vertical distances are tiny. For two tiers the factor is $1/\sqrt{2} \approx 0.707$, so a wire that keeps its relative place gets 29.3% shorter. This is an ideal: it ignores the area of the vertical links and assumes the tiers can be packed as well as one die. The [Shrunk-2D](/shrunk-2d/) flow uses exactly this scaling to place a two-tier monolithic design with a 2D tool. A finer estimate uses [Rent's rule](/rents-rule/): Banerjee, Souri, Kapur and Saraswat (2001) derive the distribution of wire lengths for 2D and 3D chips from it, and find that the demand for long global wires drops the most, because many of them become short vertical links between blocks in different tiers.

### Why heat is the main cost

The power of $L$ tiers goes through a footprint that is $L$ times smaller, and in most stacks only one side touches the heat sink. The tier farthest from the sink must push its heat through all the others, so its temperature rises with the sum of the powers below it times the thermal resistances on the way. A [compact thermal model](/compact-thermal-model/) gives these temperatures quickly enough to use inside a floorplanner or placer. This is why [thermal-driven 3D floorplanning](/thermal-driven-3d-floorplanning/) puts the blocks of high power in the tier next to the sink.

### The design problems

A 3D flow keeps most 2D steps and adds these:

- **[Tier partitioning](/tier-partitioning/).** Assign each cell or block to a tier, with balanced area and few vertical links. It is a form of [hypergraph partitioning](/hypergraph-partitioning/) with extra costs for timing and temperature.
- **3D floorplanning and placement.** Place blocks or cells in every tier at once, often with a cost for the vertical links and for heat. Floorplan representations such as the [B*-tree](/b-star-tree-floorplan/) and the [sequence pair](/sequence-pair/) are extended with a tier index.
- **TSV planning.** Choose how many TSVs to use and where, since each one takes area and stresses the silicon near it.
- **Thermal analysis and cooling.** Estimate the temperature of each tier and insert thermal vias or spread the power.
- **3D clock trees, test and power delivery.** Build a [clock tree](/clock-tree-synthesis/) across tiers, test each die before stacking, and bring power to the upper tiers through the vertical links.

## Examples

- **High Bandwidth Memory (HBM).** A stack of DRAM dies on a base die, joined by TSVs, which sits next to a processor on an interposer. It is a widely used TSV product.
- **Stacked SRAM on a processor.** AMD's 3D V-Cache bonds an SRAM die on top of a processor die with hybrid bonding and TSVs, which triples the last-level cache of the processor in the same footprint.
- **Stacked image sensors.** A pixel die is stacked on a logic die, so the pixels can fill the whole top die and the logic can use a different process.
- **A monolithic 3D research design.** Panth et al. split the OpenSPARC T2 core over two monolithic tiers in a 28 nm process and report 15.57% lower total power than a 2D design at the same performance, with the same total silicon area.

A non-example: 3D NAND flash stacks many layers of memory cells in one process, but its layers are not tiers of logic that a placer assigns gates to, so the 3D IC design problems above do not apply to it.

## Where it is used

3D integration is used in memory stacks, in processors with stacked cache, in image sensors, and in chips that mix technologies, such as logic in an advanced node with analog or I/O in an older one. Monolithic 3D is still mostly in research. In EDA, the topic is the place where partitioning, floorplanning, placement and thermal models meet: [tier partitioning](/tier-partitioning/) and [Shrunk-2D](/shrunk-2d/) for gate-level designs, [thermal-driven 3D floorplanning](/thermal-driven-3d-floorplanning/) for block-level designs, and the [TSV model](/through-silicon-via/) for the cost of each vertical link. The book of Lim (2013) covers the physical design of TSV-based 3D ICs in full.

## References
