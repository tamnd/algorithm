---
tag: MEW7V2
kind: technique
slug: tolerant-modeling
name: Tolerant modeling
aliases:
- tolerant geometry
- tolerant modelling
area: cad/solid-modeling
level: advanced
summary: Stores a tolerance with each vertex and edge of a B-rep, so geometry that misses by a small gap still counts as connected, as Jackson described for solid modelers.
prereqs: [boundary-representation, trimmed-surface, geometric-robustness-problem]
see_also: [brep-healing, exact-geometric-computation, interval-arithmetic, surface-surface-intersection, solid-boolean-operations, minimum-enclosing-ball, hausdorff-distance, offset-surface]
sources:
  - paper: doi:10.1145/218013.218067
    title: David J. Jackson, Boundary representation modelling with local tolerances, Proceedings of the Third ACM Symposium on Solid Modeling and Applications, 247 to 254, 1995
    locator: the local tolerances on edges and vertices of a B-rep, which let faces whose boundaries do not meet exactly form a valid solid, and the handling of tolerances in modeling operations
  - paper: doi:10.1145/97879.97891
    title: Mark Segal, Using tolerances to guarantee valid polyhedral modeling results, Proceedings of SIGGRAPH 90, Computer Graphics 24(4), 105 to 114, 1990
    locator: a tolerance on each vertex, edge and face of a polyhedral modeler, kept and updated so that topological decisions on imprecise data are consistent
  - paper: "Gill Barequet and Subodh Kumar, Repairing CAD models, Proceedings of IEEE Visualization 1997, 363 to 370"
    locator: the alternative to tolerances, closing cracks between faces by stitching
---

Tolerant modeling lets a [boundary representation](/boundary-representation/) be valid when its geometry does not quite fit together. In an exact B-rep, an edge is a curve that lies on both of its faces, and a vertex is a point that lies on all of its edges. In real models this is false. The edge between two curved faces is the [intersection curve](/surface-surface-intersection/) of their surfaces, which is computed only approximately. Each face also has its own [trim curves](/trimmed-surface/) in its parameter domain, which map to slightly different space curves. A model read from another system has its own precision. Tolerant modeling gives every edge and vertex its own *tolerance*: the radius of a tube around the edge curve, or of a ball around the vertex point. The model counts as connected when every face boundary lies in the tube of its edge and every edge end lies in the ball of its vertex. Segal used per-entity tolerances in a polyhedral modeler in 1990, and Jackson described local tolerances for a general B-rep modeler in 1995. The technique is now standard in commercial kernels. Its proved content is simple geometry about tubes and balls. Its value is that a model with small gaps works without moving any geometry.

## In plain words

Two tiles are laid next to each other, but their edges do not quite touch: there is a hair-thin gap. An exact program says the tiles are not joined, so the floor has a hole.

A tolerant program draws a thin tube around the shared edge and says: any edge that runs inside this tube is the same edge. The tube is just thick enough to swallow the gap. Each corner gets a small ball in the same way. The floor is now closed, and nothing was moved.

The price is that the tubes and balls must be kept honest. If two tubes are merged, the new tube must hold both. Tubes that grow with every operation can end up swallowing real details of the shape.

## When it applies

- The model is a B-rep with curved faces, whose edges are intersection curves or trim curves that do not exactly lie on the surfaces. This holds for almost every model in a CAD kernel built on floating point.
- The gaps are small compared with the features of the model, by several orders of magnitude, so that a tolerance can cover the gaps without covering any feature.
- The model comes from another system, or from operations such as [offsets](/offset-surface/) and blends, whose results are approximations. Moving the geometry to close the gaps, as [healing](/brep-healing/) does, would change the shape or fail.
- It does not apply when the gaps are of the same size as real features, such as thin walls and narrow slots, or when exact answers are required. Then use exact geometry, as in [exact geometric computation](/exact-geometric-computation/), or heal with a smaller tolerance and repair by hand.

## The template

Each edge $e$ stores a curve $C_e$ and a tolerance $t_e \ge 0$. Each vertex $v$ stores a point $p_v$ and a tolerance $t_v \ge 0$. A face stores its surface and its boundary loops, where each boundary piece is a curve $\gamma_{F,e}$ for the edge $e$, for example a trim curve mapped into space. The model is *tolerantly valid* when, for every face $F$, edge $e$ and vertex $v$ that are incident:

- (T1) the curve $\gamma_{F,e}$ lies inside the tube $\{x : d(x, C_e) \le t_e\}$;
- (T2) the ball $B(p_v, t_v)$ contains the end of the tube at $v$, which holds when $\lvert c - p_v \rvert + t_e \le t_v$ for the end point $c$ of $C_e$ at $v$.

So every point of the model that is said to coincide with another lies within a tolerance of it. The operations keep (T1) and (T2) true.

```pseudo id=main
TOLERANT-SEW(faces, t₀, s)              ▷ t₀ default tolerance, s sewing limit
L1  give each boundary edge and vertex the tolerance t₀
L2  for each pair of vertices u, v with |p_u − p_v| ≤ t_u + t_v + s do
L3      replace u, v by the smallest ball that holds B(p_u, t_u) and B(p_v, t_v)
L4  for each pair of edges e, f whose ends were merged do
L5      h ← the Hausdorff distance between C_e and C_f
L6      if h ≤ t_e + t_f + s then
L7          C ← a curve between them; t ← max(dist(C, tube_e), dist(C, tube_f))
L8          replace e, f by one edge with curve C and tolerance t
L9  for each vertex v and each edge e at v do
L10     t_v ← max(t_v, |c_e(v) − p_v| + t_e)   ▷ restore (T2)
L11 return the sewn model
```

**Line L3.** The smallest ball containing $B(p, s)$ and $B(q, t)$, with $d = \lvert p - q \rvert$, is the larger ball if it contains the other ($d + t \le s$, or $d + s \le t$). Otherwise it has radius $R = (d + s + t)/2$ and centre $p + (R - s)(q - p)/d$. *Proof.* Let $u = (q - p)/d$. Any ball that contains both balls contains the points $p - s u$ and $q + t u$, which are $d + s + t$ apart, so its radius is at least $R$. The given ball has its centre $c$ on the segment between those two points, at distance $R$ from each. For $x \in B(p, s)$, $\lvert x - c \rvert \le \lvert x - p \rvert + \lvert p - c \rvert \le s + (R - s) = R$, and the same holds for $B(q, t)$. This is the two-ball case of the [minimum enclosing ball](/minimum-enclosing-ball/).

**Line L7.** If the new edge keeps the curve $C_e$, its tolerance must be $t = \max(t_e, h + t_f)$. *Proof.* A point $x$ within $t_f$ of $C_f$ has a point $y \in C_f$ with $\lvert x - y \rvert \le t_f$, and $y$ has a point $z \in C_e$ with $\lvert y - z \rvert \le h$, so $\lvert x - z \rvert \le h + t_f$. A curve between the two can do better. Take two parallel segments at distance $h$. A cross-section perpendicular to them shows two discs, of radii $t_e$ and $t_f$, with centres $h$ apart. By the argument of line L3, the best parallel segment has tolerance $(h + t_e + t_f)/2$ when neither tube contains the other. When $t_e = t_f$, that segment is the midline.

**Line L10.** After the merges, an edge end may lie off its vertex centre, and (T2) asks for the vertex ball to cover the end of the tube. Raising $t_v$ restores it. Then (T1) and (T2) hold for every sewn pair: (T1) by line L7, since both old face curves lay in the old tubes, which lie in the new one, and (T2) by line L10.

## Classic examples

- **Edges of curved faces.** The edge between two NURBS faces is the [surface intersection curve](/surface-surface-intersection/), approximated by a spline. The approximation and the two trim curves differ by up to the fitting tolerance. Storing that difference as $t_e$ makes the edge valid without an exact curve, which usually has no closed form.
- **Imported models.** A model from another system arrives with gaps of the size of that system's precision. Instead of [healing](/brep-healing/) by moving faces, a tolerant kernel sews it by L2 to L10 and raises the tolerances of the affected edges and vertices. This is the use that Jackson describes.
- **Booleans on near-coincident faces.** Two faces that are almost coplanar meet in a curve that is badly conditioned. A tolerant [Boolean](/solid-boolean-operations/) treats them as coincident within the tolerances of their edges, merges them, and records the larger tolerance. This avoids the inconsistent decisions described under the [geometric robustness problem](/geometric-robustness-problem/).
- **Offsets and blends.** The faces of an [offset solid](/offset-surface/) or a rolling-ball blend are approximations of exact offsets. Their edges get tolerances equal to the fitting error.
- **Polyhedral modeling.** Segal attached a tolerance to every vertex, edge and face of a polyhedral modeler. When the geometry did not support a decision, he enlarged tolerances so that all the topological decisions agreed. In this way every result was the boundary of a solid.

**A worked case.** The default tolerance is $t_0 = 0.001$ mm. A box edge is stored in one face as the segment from $(0, 0, 0)$ to $(1, 0, 0)$, and in the next face as the parallel segment from $(0, 0.003, 0.004)$ to $(1, 0.003, 0.004)$. The gap is $0.005$ mm, larger than $2 t_0$. So without sewing the edges do not coincide. With the sewing limit $s = 0.01$, line L3 merges the vertices $(0, 0, 0)$ and $(0, 0.003, 0.004)$ into the ball of radius $(0.005 + 0.001 + 0.001)/2 = 0.0035$ centred at $(0, 0.0015, 0.002)$, and the same at the other end. If line L7 keeps the first segment, $t = 0.005 + 0.001 = 0.006$, and line L10 raises each vertex to $0.0025 + 0.006 = 0.0085$. If it takes the midline, $t = 0.0025 + 0.001 = 0.0035$, and the vertex balls stay at $0.0035$. The midline gives tolerances less than half as large.

## Variations

- **Global tolerance.** One $\varepsilon$ for the whole model. This is simple, but too large for small features and too small for the worst gap, and the relation "within $\varepsilon$" is not transitive. Local tolerances avoid a global choice.
- **Edge tolerances only, vertex tolerances only.** Some systems store tolerances only on edges, or only on vertices, and derive the others.
- **Tolerant faces.** A face may also carry a tolerance, when its surface is an approximation, as in Segal's polyhedral modeler.
- **Healing instead.** [B-rep healing](/brep-healing/) moves the geometry so that exact incidence holds and tolerances can stay small. Many kernels do both: heal what can be healed, and store tolerances for the rest.
- **Exact or interval geometry.** [Interval arithmetic](/interval-arithmetic/) gives each computed point an enclosing box, which is a tolerance that comes from the computation itself and not from a choice. Exact geometric computation needs no tolerance at all, but works only on geometry that can be computed exactly.

## Pitfalls

- **Tolerance creep.** Every merge enlarges a tolerance, and later operations inherit the enlarged value. Merging $k$ vertices of tolerance $t$ in a chain with spacing $d$ gives a ball of radius $((k - 1) d + 2t)/2$, so the tolerance grows linearly with the chain. A model whose tolerances have grown to the size of its features is wrong, and every later operation on it is unreliable.
- **Swallowing features.** An edge tolerance larger than half the width of a slot makes the slot's walls coincide. Check that no tolerance tube meets a non-adjacent entity.
- **Using the tolerance in some tests and not in others.** If a Boolean classifies a point against a face with the face tolerance, but against the edge with zero tolerance, the decisions can disagree, which is the robustness problem again. Every test that involves an entity must use its tolerance.
- **Export to exact systems.** A model that is valid only with its tolerances is invalid in a system that ignores them. Heal before exporting to systems that do not read the tolerances.
- **Units.** A tolerance of $0.001$ is a micron in millimetres and a millimetre in metres. Store tolerances in the model's units and check them against the model's size.

## Exercises

1. Two vertex balls $B((0,0,0), 1)$ and $B((4,0,0), 2)$ are merged. Find the smallest enclosing ball. *Answer:* radius $(4 + 1 + 2)/2 = 3.5$, centre $(2.5, 0, 0)$.
2. Show that tolerant coincidence of vertices, "$\lvert p_u - p_v \rvert \le t_u + t_v$", is not transitive, and give three vertices that show it.
3. Prove the claim of line L7 for parallel segments: among segments parallel to both, the least tolerance that covers both tubes is $(h + t_e + t_f)/2$, unless one tube contains the other.
4. In the worked case, suppose a third face brings a third copy of the edge at $(0, -0.003, 0.004)$ to $(1, -0.003, 0.004)$. Find a curve and a tolerance for the merged edge.

## References
