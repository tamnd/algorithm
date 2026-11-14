---
tag: 7385QD
kind: technique
slug: conformal-cooling-design
name: Conformal cooling channel design
aliases:
- conformal cooling
area: cad/manufacturing-process-planning
level: research
summary: Designs mold cooling channels that follow the cavity surface at a near constant distance, made by 3D printing, as in the automatic design of Wang, Yu, Wang and Zhang.
prereqs: [offset-surface, heat-equation]
see_also: [centroidal-voronoi-tessellation, lloyds-algorithm, medial-axis, finite-element-method, gate-location-optimization, casting-hot-spot-detection, fermat-spiral-toolpath, support-structure-generation]
sources:
  - paper: doi:10.1016/j.cad.2011.04.011
    title: Yu Wang, Kai-Ming Yu, Charlie C. L. Wang and Yunbo Zhang, Automatic design of conformal cooling circuits for rapid tooling, Computer-Aided Design 43(8), 2011, 1001 to 1010
    locator: the offset of the mold surface to a working surface, the centroidal Voronoi diagram on it computed with Lloyd's iteration, and the cooling circuits built from it
  - title: Yu Wang, Kai-Ming Yu and Charlie C. L. Wang, Spiral and conformal cooling in plastic injection molding, Computer-Aided Design 63, 2015, 1 to 11
    locator: spiral cooling circuits on the working surface, as an alternative layout to the circuits of the 2011 paper (general locator)
  - title: K. M. Au, K. M. Yu and W. K. Chiu, Visibility-based conformal cooling channel generation for rapid tooling, Computer-Aided Design 43, 2011, 356 to 373
    locator: the placement of cooling channels from the visibility between the cavity surface and the channel positions (general locator)
---

Conformal cooling channel design places the cooling channels of an injection mold or a die so that they follow the shape of the cavity at a nearly constant distance. In a mold made by machining, channels are straight drilled holes, so on a curved part some regions are near a channel and others are far, and the far regions cool last. They set the cycle time and cause uneven shrinkage and warpage. A mold insert made by metal additive manufacturing can have curved channels, and the design problem is then to choose their path. The methods are geometric constructions on a surface offset from the cavity, followed by a cooling simulation that checks the result. They are heuristics: the target, an even and fast cooling, is measured by simulation or on the press, and there is no standard benchmark to compare methods.

## In plain words

A plastic part must cool in its mold before it comes out. Water runs through holes in the mold to take the heat away. With drilled holes, the holes are straight, so a curved part is close to the water in some places and far from it in others. The far places stay hot longest, and the whole part must wait for them.

If the mold is 3D printed, the water channels can bend and follow the shape of the part, like a pipe laid at the same depth under a curved floor. The design task is to choose where these channels go, so that every part of the surface is cooled about the same, and then to check the result in a simulation.

## When it applies

- The mold insert can be made with curved internal channels, usually by powder bed metal printing, or by joining machined layers.
- Cooling is a large part of the cycle time, or uneven cooling causes warpage, for example on deep cores, domes and parts with large changes of curvature.
- A thermal simulation of the mold is available to check a design. Without it, the constant-distance rule is a guide, not a guarantee.

## The template

**Why a constant distance.** In the simplest model, heat flows by steady conduction straight from the cavity surface to the nearest channel through a slab of thickness $\delta$, as in the one-dimensional [heat equation](/heat-equation/). Then the heat flux is $q = k\,\Delta T / \delta$ for the conductivity $k$ of the mold and the temperature difference $\Delta T$. A constant $\delta$ gives a constant flux along the surface. The model ignores the curvature of the surface, the spacing between channels, the heat stored in the mold, and the change of $\Delta T$ along the channel as the coolant warms up. So the rule is a design aim, and a simulation must check it.

```pseudo id=main
CONFORMAL-COOLING(M, δ, D, s, simulate, criteria)
L1  W ← the offset of the cavity surface M into the mold by the distance δ (the working surface)
L2  choose a layout of channel paths on W with spacing about s: loops, a spiral, or circuits from a partition of W
L3  build the channel centrelines from the layout and sweep a section of diameter D along them
L4  check the walls: the distance from each channel to the cavity, to the other channels and to ejectors and inserts
L5  check that the channels can be printed and cleaned, and that the coolant pressure drop is acceptable
L6  r ← simulate(the mold with the channels); if r meets the criteria then return the channels
L7  change δ, s, D or the layout, and go to L1
```

The holes are the offset distance $\delta$, the spacing $s$ and the diameter $D$ (design guides give them as multiples of the channel diameter), the layout rule at line L2, and the criteria at line L6, such as the cooling time and the spread of the surface temperature.

**Line L1.** An [offset surface](/offset-surface/) at a distance $\delta$ can have self-intersections where the cavity has concave regions with a radius of curvature less than $\delta$. They must be trimmed, and in those regions the channel cannot keep the distance $\delta$ from every point of the cavity. Narrow regions of the mold, near its [medial axis](/medial-axis/), may not have room for a channel at all.

**Line L2.** Wang, Yu, Wang and Zhang (2011) partition the working surface with a [centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/), computed by [Lloyd's algorithm](/lloyds-algorithm/), so that the cells have about equal size, and build the circuits from this partition. Wang, Yu and Wang (2015) use spiral circuits on the working surface, which give one long channel with no sharp turns, like a [Fermat spiral toolpath](/fermat-spiral-toolpath/) on a surface. Au, Yu and Chiu (2011) place the channels by the visibility between the cavity surface and the possible channel positions, so that each region of the surface has a channel in view.

## Classic examples

**A curved corner, drilled and conformal.** Take a section through a mold with a cavity wall that is a quarter circle of radius 40 mm, and the aim $\delta = 10$ mm. A conformal channel runs on the circle of radius 50 mm, at a distance of 10 mm from every point of the wall. A straight drilled channel that touches the circle of radius 50 at the middle of the arc (at 45 degrees) is at the distance $50 - 40\cos(\varphi - 45^\circ)$ from the wall point at the angle $\varphi$. This is 10 mm at the middle and $50 - 40 \cos 45^\circ = 21.7$ mm at the ends of the arc. In the one-dimensional model the heat flux at the ends is less than half of that at the middle, so the ends cool last. This is a geometric comparison only. The real difference comes from a simulation.

**What is measured.** Wang, Yu, Wang and Zhang evaluate their circuits with a simulation of the cooling, in terms of the cooling time and the uniformity of the temperature of the part. Other authors measure the cycle time and the warpage of molded parts on a press. Each study uses its own parts, materials and simulator, so their numbers do not compare from one study to another, and there is no standard set of test parts.

## Variations

- **Layout rule.** Loops parallel to the parting plane, a spiral, circuits from a surface partition, or a branching network. A spiral or a single circuit has an even flow; a network has a lower pressure drop but uneven flow between its branches.
- **Cooling layers and lattices.** Instead of pipes, a thin cooling chamber with a supporting lattice follows the cavity, which gives a near constant distance everywhere at the cost of a weaker mold.
- **Optimization around a simulation.** The parameters $\delta$, $s$ and $D$, or the full path, are tuned by a search with a thermal [finite element](/finite-element-method/) model in the loop. This finds better designs for one part but costs many simulations.
- **Combined with the gate.** The region near the gate and the regions that fill last are hot, so the layout can put channels closer there. See [gate location optimization](/gate-location-optimization/).

## Pitfalls

- **Wall too thin.** A channel too close to the cavity can crack the mold under the injection pressure. Line L4 must check the smallest wall, not only the mean distance.
- **Printability.** A horizontal channel with a round section can sag when it is printed, and powder must be removed from long channels. Teardrop sections and self-supporting paths avoid [support structures](/support-structure-generation/) inside the channel.
- **Pressure drop and flow.** A long conformal channel has a large pressure drop, so the flow may be too slow for turbulent flow, and the coolant warms up along it. The last part of a long channel then cools less.
- **The model is not the mold.** Equal distance does not mean equal cooling: thick regions of the part hold more heat, and corners have more mold metal around them. Find thick regions with a [hot spot](/casting-hot-spot-detection/) proxy and check the design with a simulation.

## References
