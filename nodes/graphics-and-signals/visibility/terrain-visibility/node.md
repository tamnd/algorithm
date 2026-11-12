---
tag: 8KXVPH
kind: problem
slug: terrain-visibility
name: Terrain visibility
aliases:
- viewshed
- line-of-sight on terrain
- horizon computation
area: graphics-and-signals/visibility
level: core
summary: Given a terrain as a height field and a viewer above it, find which terrain points the viewer sees, as one line of sight, the whole viewshed, or the horizon in each direction.
prereqs: [hidden-surface-removal, visibility-polygon]
see_also: [hidden-surface-removal, visibility-polygon, lower-envelope-of-segments, all-prefix-sums, rotational-sweep, shadow-mapping, bresenham-line-algorithm, delaunay-triangulation]
sources:
  - paper: doi:10.1068/b12979
    title: Leila De Floriani and Paola Magillo, Algorithms for visibility computation on terrains, a survey, Environment and Planning B, Planning and Design 30(5), 2003, pages 709 to 728
    locator: the whole survey (terrain models, line of sight, viewsheds and horizons)
  - paper: doi:10.1016/S0747-7171(89)80003-3
    title: Richard Cole and Micha Sharir, Visibility problems for polyhedral terrains, Journal of Symbolic Computation 7(1), 1989, pages 11 to 30
    locator: ray shooting from a fixed viewer, a viewer on a vertical line, and the placement of viewers that see the whole terrain
  - paper: doi:10.1016/0895-7177(95)00016-U
    title: John H. Reif and Sandeep Sen, An efficient output-sensitive hidden-surface removal algorithm for polyhedral terrains, Mathematical and Computer Modelling 21(5), 1995, pages 89 to 104
    locator: the whole paper (the visible parts of a polyhedral terrain in time that depends on the output size)
  - paper: doi:10.1145/1412228.1412233
    title: Herman Haverkort, Laura Toma and Yi Zhuang, Computing visibility on terrains in external memory, ACM Journal of Experimental Algorithmics 13, 2009
    locator: the viewshed of a grid terrain that does not fit in main memory
---

Terrain visibility asks which points of a terrain a viewer sees. The terrain is a height field: a surface $z = f(x, y)$ that each vertical line meets once, given as a grid of heights or as a triangulated irregular network (TIN). The viewer stands at a point of the terrain, at some height above it. There are three standard questions. *Line of sight* asks if the viewer sees one given point. The *viewshed* is the set of all terrain points that the viewer sees. The *horizon* gives, for each direction around the viewer, the highest angle at which the terrain is seen. It is a special case of [hidden-surface removal](/hidden-surface-removal/). Since the scene is a height field, the visibility along each ray from the viewer is a running maximum of slopes, and this makes simpler and faster algorithms possible. It differs from the [visibility polygon](/visibility-polygon/), which is a 2D problem inside a polygon and always gives one star-shaped region, while a viewshed can have many parts and holes. In real-time graphics, [shadow mapping](/shadow-mapping/) computes the same set, the region that a point light at the viewer lights, one pixel at a time. Geographic information systems (GIS) compute it as a map of the terrain.

## In plain words

Stand on a hill and look around. Some valleys and slopes you can see, and some are behind a ridge. A place is visible if a straight line from your eyes to it never goes into the ground. Along each straight path away from you, a place is visible when it shows up higher in your view than everything in front of it. So you can walk outward, remember the highest angle so far, and mark the places that reach above it. The set of all places you see is your viewshed, and it can be made of many separate patches. The line along the tops of the farthest ridges that you see, all around you, is the horizon. Towers, lookouts and antennas are placed by these maps.

## Definition

**Terrain.** A function $f$ on a region $D$ of the plane, with one of two models.

- **Grid, or digital elevation model.** Heights at the points of a regular grid with $n$ points, and a rule for the height between them, for example a constant height per cell, linear interpolation along the grid lines, or two triangles per cell.
- **TIN, or polyhedral terrain.** A triangulation of $n$ points in the plane with a height at each point. $f$ is linear on each triangle, so the terrain is a surface made of triangles. Often the triangulation is the [Delaunay triangulation](/delaunay-triangulation/) of the points.

**Viewer and target.** The viewer is the point $v = (x_0, y_0, f(x_0, y_0) + h)$, with an observer height $h \ge 0$. A target at $(x, y)$ is the point $p = (x, y, f(x, y) + t)$, with a target height $t \ge 0$. Often $t = 0$.

**Line of sight.** $v$ sees $p$ if no point of the segment $vp$ is below the terrain: each point $(x', y', z')$ of $vp$ has $z' \ge f(x', y')$. A line of sight that touches the terrain and does not go below it counts as visible.

**The three outputs.**

- *Line of sight:* given $v$ and $p$, decide whether $v$ sees $p$.
- *Viewshed:* the set of $(x, y) \in D$ whose target $p$ the viewer sees. For a grid, it is a yes or no value at each grid point. For a TIN, it is the visible part of each triangle, a subdivision of $D$ into visible and hidden regions.
- *Horizon:* for each direction $\theta$ around $v$, the largest elevation angle at which the viewer sees the terrain in that direction, and the terrain point where it is reached.

**The profile rule.** Fix a direction from $v$ and let $r$ be the distance from $(x_0, y_0)$ in that direction. Write $g(r)$ for the height of the terrain at distance $r$, and $z_0 = f(x_0, y_0) + h$. The point at distance $r$, with target height $t$, is visible exactly when

$$\frac{g(r) + t - z_0}{r} \ge \max_{0 < r' < r} \frac{g(r') - z_0}{r'}.$$

The left side is the slope of the line of sight, and the right side is the steepest slope from $v$ to the terrain in front of the target. So visibility along one ray is a running maximum, a max-prefix scan ([all prefix sums](/all-prefix-sums/)).

## Variants

- **Range limit.** Only targets up to a distance $R$ from the viewer count.
- **Curvature of the earth.** Over long distances, GIS programs lower far heights to model the curvature of the earth and the bending of light in air. The algorithms stay the same.
- **Many viewers.** A *cumulative viewshed* counts, for each point, how many viewers in a given set see it.
- **Placement of viewers.** Find one viewer, or the fewest viewers, whose viewsheds cover the terrain. For a polyhedral terrain, Cole and Sharir (1989) decide in $O(n \log n)$ time if one viewing point on the surface sees all of it, and they show that the fewest points that together see all of it is NP-hard to find.
- **A moving viewer.** A viewer that moves on a vertical line or along a path, as in a flight or on a road. Cole and Sharir study the viewer on a vertical line.
- **A view of the terrain.** Drawing the terrain from the viewer, as a picture, is [hidden-surface removal](/hidden-surface-removal/) for a terrain. Output-sensitive algorithms take time that depends on the size of the visible part (Reif and Sen).

## Examples

**One profile.** Take a terrain profile along one ray from the viewer, with the heights $0, 1, 1, 3, 1, 2, 6, 2, 4$ at the distances $0, 1, \dots, 8$ and straight lines between them. The viewer stands at distance $0$ with $h = 2$, so its eye is at $(0, 2)$. The slope from the eye to the vertex at distance $j$ is $(g(j) - 2)/j$:

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| height | 1 | 1 | 3 | 1 | 2 | 6 | 2 | 4 |
| slope | $-1$ | $-1/2$ | $1/3$ | $-1/4$ | $0$ | $2/3$ | $0$ | $1/4$ |
| running maximum before $j$ | none | $-1$ | $-1/2$ | $1/3$ | $1/3$ | $1/3$ | $2/3$ | $2/3$ |
| visible | yes | yes | yes | no | no | yes | no | no |

The visible vertices are the ones that set a new maximum. Between the vertices, the line of sight over the peak at distance 3 is $z = 2 + r/3$. It meets the rising edge from $(5, 2)$ to $(6, 6)$ at $r = 60/11$. So the visible part of the profile is the two pieces $0 \le r \le 3$ and $60/11 \le r \le 6$, and the rest is hidden. The horizon in this direction is the peak at distance 6, with slope $2/3$. Over that peak, the line of sight is $z = 2 + 2r/3$, which is at height $22/3$ at distance 8. The terrain there has height 4, so a target at distance 8 is visible only if its target height is at least $10/3$.

**A viewshed with many parts.** On a real terrain, a viewer on a hill sees its own slopes, the far side of the valley, and the tops of ridges behind it, but not the slopes that face away. So the viewshed is often a set of many separate patches with holes, unlike the visibility polygon in a room.

## Known algorithms

| question | model | method | time |
|---|---|---|---|
| line of sight | grid or TIN | walk along the projected segment through the cells or triangles that it crosses (as in [Bresenham's algorithm](/bresenham-line-algorithm/)) and compare the heights | $O(m)$ for $m$ cells or triangles crossed |
| one profile | polyline with $n$ vertices | one scan outward with the running maximum of slopes | $O(n)$ |
| viewshed | grid with $n$ points | line of sight to each grid point, often called R3 | $O(n^{3/2})$, since each line crosses $O(n^{1/2})$ cells |
| viewshed | grid | lines of sight only to the points on the border of the grid, and each point takes the answer of the nearest line, often called R2 | $O(n)$, approximate |
| viewshed | grid | radial sweep: turn a ray around the viewer and keep the cells that it crosses in a balanced search tree by distance, with the steepest slope in each subtree (van Kreveld 1996) | $O(n \log n)$ |
| viewshed | grid larger than main memory | Haverkort, Toma and Zhuang | efficient in transfers between disk and memory |
| viewshed | TIN | process the triangles from near to far and clip each one against the horizon of the part done so far, kept as an upper envelope | depends on the method; the output can have $\Theta(n^2)$ size |
| horizon | TIN | the upper envelope of the edges as the viewer sees them, by the methods for the [lower envelope of segments](/lower-envelope-of-segments/) | $O(n \log n)$ |
| first point hit along a ray | TIN | the data structure of Cole and Sharir (1989) | preprocessing $O(n \alpha(n) \log n)$ |

The radial sweep is the [rotational sweep](/rotational-sweep/) of the visibility polygon, used on a height field. The events are the cells that enter and leave the ray, and the tree answers "is this cell above the steepest slope in front of it" in $O(\log n)$ time.

## Bounds

- **One profile.** $\Theta(n)$ for a profile with $n$ vertices, by the scan.
- **Grid.** The output has one value per grid point, so $\Omega(n)$ time is needed. The radial sweep takes $O(n \log n)$ time and is exact for its cell model.
- **TIN viewshed.** The visible region can have $\Theta(n^2)$ vertices. Put a long wall near the viewer with $m$ narrow notches in its top, and behind it $m$ long ridges. As the viewer sees them, each ridge crest is higher than the one in front of it, all crests are higher than the bottoms of the notches, and all are lower than the top of the wall. The crest of each ridge shows through each notch, so the viewshed has $\Theta(m^2)$ pieces with $n = \Theta(m)$ triangles. This matches the $O(n^2)$ bound of hidden-surface removal for $n$ triangles.
- **Horizon.** Split the directions around the viewer into a few sectors less than a half turn wide. In each sector, a central projection onto a vertical plane in front of the viewer maps each terrain edge to a segment and keeps vertical lines vertical, so the horizon is the upper envelope of $O(n)$ segments. By Davenport-Schinzel theory, it has $O(n \alpha(n))$ pieces, where $\alpha$ is the inverse Ackermann function, and Hershberger's algorithm finds it in $O(n \log n)$ time.
- **Placement.** The fewest viewers that see a whole polyhedral terrain is NP-hard to find (Cole and Sharir).

## Reductions

- **To prefix maxima.** Along each ray from the viewer, visibility is the max-prefix scan of the slopes, as in the profile rule. In parallel, an [all prefix sums](/all-prefix-sums/) scan with the operator max solves a profile in $O(\log n)$ steps.
- **To an upper envelope.** The horizon is the upper envelope of the terrain edges as projected for the viewer ([lower envelope of segments](/lower-envelope-of-segments/), turned upside down). In the plane, the 1.5D terrain seen from a point is the same problem with $n$ segments.
- **To hidden-surface removal.** A terrain point is in the viewshed exactly when it is in the visible part of the scene seen from $v$. So any object-space algorithm for [hidden-surface removal](/hidden-surface-removal/) gives the viewshed.
- **To shadows.** The viewshed is the lit region of a point light at the viewer. [Shadow mapping](/shadow-mapping/) computes it on a GPU: draw the depth of the terrain as seen from $v$ in all directions, and mark a terrain point visible when its distance to $v$ is not greater than the stored depth. This gives an image-precision viewshed.

## Applications

- **Siting.** Towers for radio and mobile phones, fire lookouts and radar are placed where their viewsheds cover a region.
- **Planning and landscape.** The visual impact of a wind farm, a building or a road is judged by the area of the terrain from which it is seen.
- **Defense and navigation.** Line of sight between two points, and the region hidden from a radar, depend on the terrain.
- **Sun and sky.** The horizon around a site tells at which times the sun is behind the hills, which matters for solar panels and for the light on a slope.
- **Games and simulation.** Units on a height map see only their viewshed, and terrain renderers draw the parts in front first.

## References
