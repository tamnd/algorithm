---
tag: HJ50HJ
kind: concept
slug: discrete-global-grid-system
name: Discrete global grid system
aliases:
- DGGS
- hexagonal global index
area: data-structures/spatial-structures
level: research
summary: Hierarchical tessellation of the Earth's surface into cells, such as H3's hexagons.
prereqs: [quadtree, space-filling-curve]
see_also: [s2-cell-hierarchy, geohash, hilbert-curve, linear-quadtree, z-order-curve, uniform-grid, spatial-index, nearest-neighbor-search]
sources:
  - paper: doi:10.1559/152304003100011090
    title: Kevin Sahr, Denis White and A. Jon Kimerling, Geodesic discrete global grid systems, Cartography and Geographic Information Science 30(2), 2003
    locator: the whole paper (the design choices of a geodesic grid system, namely the base polyhedron, its orientation, the cell shape, the refinement and its aperture, and the projection between the faces and the sphere, and the ISEA grids)
  - paper: doi:10.1086/427976
    title: Krzysztof M. Górski, Eric Hivon, Anthony J. Banday, Benjamin D. Wandelt, Frode K. Hansen, Martin Reinecke and Matthias Bartelmann, HEALPix, a framework for high-resolution discretization and fast analysis of data distributed on the sphere, The Astrophysical Journal 622, 2005
    locator: the sections on the hierarchical equal-area tessellation of the sphere into 12 base pixels and the nested numbering scheme
  - paper: "John P. Snyder, An equal-area map projection for polyhedral globes, Cartographica 29(1), 1992"
    title: John P. Snyder, An equal-area map projection for polyhedral globes, Cartographica 29(1), 1992
    locator: the whole paper (the equal-area projection of the faces of a polyhedron onto the sphere, used by the ISEA grids)
---

A discrete global grid system (DGGS) divides the whole surface of the Earth into cells, then divides each cell into smaller cells, and so on for a fixed number of *resolutions*. Each cell has a short integer or string index, and the index says where the cell is, how large it is, and which cell contains it at the coarser resolution. Most systems start from a polyhedron, such as an icosahedron or a cube, and map its faces onto the sphere, so the cells have nearly equal size and shape everywhere, with no poles or seams in the grid. Data at a point is stored under the index of its cell, so the grid works as a [spatial index](/spatial-index/) for the whole globe. Well known systems are Google's [S2](/s2-cell-hierarchy/), which uses squares on a cube, Uber's H3, which uses hexagons on an icosahedron, and HEALPix, which is used for maps of the sky.

## In plain words

A map with lines of latitude and longitude makes cells that get very thin near the poles. That is bad for counting, for averages, and for finding neighbors.

A global grid starts with a simple solid, such as a cube or a 20-sided solid, inside the Earth. Each face is blown out onto the surface, so the surface is split into a few large cells of about the same size. Each cell is then split into smaller cells, again and again.

Every cell gets a number. Nearby places get cells with related numbers, and the number of a small cell tells you the larger cell around it. To store data for a place, find its cell and use the number as the key.

## The idea

**Design choices.** Sahr, White and Kimerling describe a geodesic grid system by five choices.

1. **A base polyhedron.** The tetrahedron, cube, octahedron and icosahedron are used. The icosahedron has the most faces of the regular solids, so its faces are distorted least when mapped onto the sphere.
2. **Its orientation.** The polyhedron can be turned so that its vertices, where the distortion is worst, fall in the oceans.
3. **The cell shape.** Triangles, squares or diamonds, and hexagons.
4. **The refinement.** How a cell at one resolution becomes cells at the next. The *aperture* is the ratio of the area of a cell to that of a cell one resolution finer. Squares and triangles split into 4 (aperture 4); hexagons can use aperture 3, 4 or 7.
5. **The projection** between a face and the sphere. An equal-area projection, such as Snyder's for polyhedral globes, makes all cells of a resolution the same area; a gnomonic projection keeps cell edges as great circle arcs but lets the areas vary.

**Hierarchy and index.** With squares on a cube face, as in S2, each cell has exactly 4 children inside it, and the grid on a face is a [quadtree](/quadtree/). A cell is named by its face and the path of child numbers from the face down, which is a [linear quadtree](/linear-quadtree/) code. If the children are numbered along a [space-filling curve](/space-filling-curve/), such as the [Hilbert curve](/hilbert-curve/) in S2, the indexes of all cells inside a cell form one interval of integers, so a region is a short list of intervals and a range scan in a sorted table returns its data.

**Why hexagons.** A hexagon has 6 neighbors, all across an edge and all at the same distance from its center. A square has 4 neighbors across an edge and 4 more at a corner, at a larger distance. So hexagons give simpler neighbor rules, smoother distance rings, and better sampling. The cost is the hierarchy: 7 hexagons do not tile a larger hexagon exactly, so in H3 the children of a cell only approximately cover it, and the index is a hierarchy of approximate containment.

**Pentagons.** A sphere cannot be tiled by hexagons alone. If a tiling has only pentagons and hexagons, with three cells at each vertex, then with $p$ pentagons and $h$ hexagons there are $F = p + h$ faces, $E = (5p + 6h)/2$ edges and $V = (5p + 6h)/3$ vertices, and Euler's formula $V - E + F = 2$ gives $p/6 = 2$. So every such grid has exactly 12 pentagons at every resolution, one at each vertex of the icosahedron, and code must treat them as special cells.

**Operations.** A DGGS library provides: the cell of a point at a given resolution; the center and boundary of a cell; the parent and the children of a cell; the neighbors of a cell, and the ring of cells at grid distance $k$; and a set of cells that covers a polygon. All of them work on the indexes with bit operations and a small amount of spherical geometry.

## Examples

- **S2.** A cube with each face split as a quadtree for 30 levels, so level $k$ has $6 \cdot 4^k$ cells. A cell index is a 64-bit integer: 3 bits for the face, 2 bits per level along a Hilbert curve on the face, and a final 1 bit that marks the level. A transform of the coordinates makes the cells of one level close in area.
- **H3.** An icosahedron with hexagonal cells, aperture 7, and 16 resolutions, numbered 0 to 15. Resolution 0 has 122 cells, 110 hexagons and 12 pentagons, and resolution $r$ has $2 + 120 \cdot 7^r$ cells. The Earth has about $510$ million km² of surface, so a cell at resolution 9, one of about $4.8 \times 10^9$, covers about $0.1$ km² on average.
- **HEALPix.** 12 base cells of equal area, each split as a quadtree, so there are $12 N^2$ cells of equal area for $N$ a power of 2. The nested numbering gives each cell the index of its parent followed by two bits.
- **ISEA grids.** The icosahedral Snyder equal-area grids, such as ISEA3H with hexagons of aperture 3, which Sahr and others use in their DGGRID software.
- **Not a DGGS in this sense.** [Geohash](/geohash/) splits the latitude and longitude rectangle by [Z-order](/z-order-curve/). It is hierarchical and covers the globe, but its cells shrink toward the poles and its order has jumps.

## Where it is used

- **Aggregation and analytics.** Counting trips, sales or sensor readings per cell, at several resolutions, with cells of nearly equal size, as in ride sharing and delivery.
- **Database indexes.** Storing the cell index of each object in a B-tree turns region and [nearest neighbor](/nearest-neighbor-search/) queries on the sphere into a few range scans, as in S2 based geographic indexes.
- **Earth and sky science.** Climate and ocean models on icosahedral grids, and maps of the cosmic microwave background in HEALPix.
- **Data exchange.** The Open Geospatial Consortium has an abstract specification for DGGS, so that data from different sources can be joined on the same cells.

## References
