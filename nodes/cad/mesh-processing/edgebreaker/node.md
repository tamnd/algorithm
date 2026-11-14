---
tag: 5F4MY3
kind: algorithm
slug: edgebreaker
name: Edgebreaker
aliases:
- Edgebreaker compression
area: cad/mesh-processing
level: advanced
summary: Rossignac's connectivity compression that visits the triangles of a mesh one by one and writes one of five symbols for each, using at most 2 bits per triangle on a closed genus 0 mesh.
model: word-ram
complexity:
  vars: {t: the number of triangles}
  time: {encode: O(t) expected, decode: O(t^2)}
  space: {extra: Θ(t)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1999
  people: [Jarek Rossignac]
  note: Rossignac published Edgebreaker in IEEE Transactions on Visualization and Computer Graphics in 1999, with the CLERS symbols and the bound of 2 bits per triangle for meshes with the topology of a sphere.
prereqs: [corner-table, manifold-mesh, euler-formula]
see_also: [progressive-mesh, huffman-coding, arithmetic-coding, shannon-entropy, indexed-face-set, spanning-tree, polygon-mesh, depth-first-search]
sources:
  - paper: doi:10.1109/2945.764870
    title: Jarek Rossignac, Edgebreaker, connectivity compression for triangle meshes, IEEE Transactions on Visualization and Computer Graphics 5(1), pages 47-61, 1999
    locator: the five symbols C, L, E, R and S, the traversal with a stack for S, the code with 1 bit for C and 3 bits for the other symbols, the 2t bit bound for meshes with the topology of a sphere, and the measured rates with entropy coding
---

Edgebreaker compresses the connectivity of a triangle mesh: the list of which vertices form each triangle, without the coordinates. It visits the triangles one by one, each next to one already visited, and writes one of five symbols, C, L, E, R or S, for each. The symbol says where the third vertex of the new triangle lies: a new vertex, or a vertex on the border of the visited part. On a closed mesh with the topology of a sphere, the code with 1 bit for C and 3 bits for the other symbols takes exactly $2t - 1$ bits for $t$ triangles, and the decoder rebuilds the same mesh with its vertices renumbered. Jarek Rossignac published the method in 1999, and it is a standard method of mesh compression.

## In plain words

Think of the surface as a ball covered with triangles. Paint one triangle. Then, again and again, paint a triangle next to the painted part, and write one letter that says what its far corner touches.

If the far corner was never painted, write C. If it is the painted corner just to the left or just to the right, write L or R. If the triangle fills the last gap of a hole, write E. If the corner is somewhere else on the edge of the paint, the unpainted part splits in two. Write S, finish one part, and come back for the other.

C is very common, so it gets a short word of one bit, and the other letters get three bits. A reader who gets only the letters can paint the same triangles in the same order, and so rebuild the whole mesh.

## The problem

The input is a mesh $M$ given as an [indexed face set](/indexed-face-set/): a list of $t$ triangles, each a triple of three different vertex ids, oriented by the right-hand rule so that every directed edge $a \to b$ is in exactly one triangle and its reverse $b \to a$ in exactly one other. So $M$ is closed, every edge has two triangles, and $M$ is oriented. We also need $M$ to be connected through its edges and to have $\chi = V - E + F = 2 - 2g = 2$, that is, genus $g = 0$. The proof shows that these conditions make $M$ a triangulated sphere. The goal is a short string from which a decoder can rebuild $M$ up to a renumbering of its vertices: the decoder must give the triangles of $M$ with each vertex $v$ replaced by $\varphi(v)$ for one bijection $\varphi$ of the vertex ids onto $0, 1, \dots, V - 1$. The vertex coordinates are sent separately, in the order of $\varphi$.

## The algorithm

The encoder keeps the triangles it has visited. The rest of the surface, the part not yet visited, is a set of pieces, and each piece is bounded by a closed *loop* of vertices and edges. The loop runs along the visited triangles in their own direction. One edge of the current loop is the *gate* $a \to b$. The triangle on the other side of the gate is $(b, a, x)$, and $x$ is its *tip*. The encoder looks up neighbours with a [corner table](/corner-table/). The five cases:

- **C**: $x$ is new. The loop gets the vertex $x$ between $a$ and $b$.
- **L**: $x$ is the vertex just before $a$ on the loop, so the triangle to the left is visited. The vertex $a$ leaves the loop.
- **R**: $x$ is the vertex just after $b$, so the triangle to the right is visited. The vertex $b$ leaves the loop.
- **E**: both; the loop was the triangle $a, b, x$ and it closes.
- **S**: $x$ is elsewhere on the loop. The loop splits into a right loop $x \to b \to \dots \to x$ and a left loop $a \to x \to \dots \to a$. The encoder finishes the right loop first and keeps the left one on a stack.

```pseudo id=main
ENCODE(M, f_0)
L1  mark f_0 and its vertices a, b, c;  push the triangle across the edge a → b;  for each triangle t = (b, a, x) taken from the stack or reached by "go on", with gate a → b, mark t and do:
L2      if x is not marked then write C;  mark x;  go on across x → b
L3      else if the triangles across a x and across x b are both marked then write E;  take the next triangle from the stack
L4      else if the triangle across a x is marked then write L;  go on across x → b
L5      else if the triangle across x b is marked then write R;  go on across a → x
L6      else write S;  push the triangle across a → x;  go on across x → b

DECODE(symbols)
L7  ℓ_i ← the length of the right loop of each S, from the counts of the symbols up to its E;  faces ← (0, 1, 2);  loop ← 0 → 1 → 2 → 0;  gate ← 0 → 1;  then for each symbol s_i, with the gate a → b:
L8      if s_i = C then x ← the next new vertex;  insert x between a and b;  gate ← x → b
L9      if s_i = L then x ← the vertex before a;  remove a from the loop;  gate ← x → b
L10     if s_i = R then x ← the vertex after b;  remove b from the loop;  gate ← a → x
L11     if s_i = E then x ← the vertex before a;  the loop a → b → x closes;  gate ← the gate taken from the stack (none at the end)
L12     if s_i = S then x ← the vertex ℓ_i − 1 steps after b;  split the loop into x → b → … → x and a → x → … → a;  gate ← x → b
L13         push the gate a → x
L14     append the face (b, a, x)
L15 return faces
```

**The bits.** The code is C = 0, S = 100, R = 101, L = 110, E = 111. It is a prefix code, so the bit string splits back into symbols without separators.

**Line L7.** The decoder must know where the tip of an S is. The encoder does not send it: the decoder finds it from the symbols that follow. Let a loop have $\ell$ edges. Then C adds one edge, L and R remove one, S makes $\ell + 1$ edges in two loops, and E removes a loop of 3 edges. The right loop of the S at position $i$ is finished by the symbols from $i + 1$ to the E at which, for the first time, the number of E symbols is one more than the number of S symbols. If these symbols have $n_C$ C, $n_L$ L, $n_R$ R and $n_S$ S, then $\ell_i = 3 + 2 n_S - n_C + n_L + n_R$. The code finds all the ends in one pass with a stack.

**Degenerate cases.** The encoder rejects a face that repeats a vertex, a directed edge used twice, a boundary edge, $V - E + F \ne 2$, and a mesh that is not connected. The smallest valid input is the *pillow*: two triangles $(0, 1, 2)$ and $(0, 2, 1)$ on the same three vertices, coded as the single symbol E.

## Example

Take the octahedron with the faces $(0, 2, 4)$, $(2, 1, 4)$, $(1, 3, 4)$, $(3, 0, 4)$, $(2, 0, 5)$, $(1, 2, 5)$, $(3, 1, 5)$, $(0, 3, 5)$, so $t = 8$ and $V = 6$. Start at $f_0 = (0, 2, 4)$. The encoder writes CCRCRRE and meets the vertices in the order $0, 2, 4, 5, 1, 3$, so $\varphi$ maps them to $0, 1, 2, 3, 4, 5$. The decoder sees only the symbols:

| step | symbol | gate $a \to b$ | tip $x$ | face $(b, a, x)$ | loop after |
|---|---|---|---|---|---|
| L7 | | | | $(0, 1, 2)$ | $0 \to 1 \to 2$ |
| 1 | C | $0 \to 1$ | new 3 | $(1, 0, 3)$ | $0 \to 3 \to 1 \to 2$ |
| 2 | C | $3 \to 1$ | new 4 | $(1, 3, 4)$ | $0 \to 3 \to 4 \to 1 \to 2$ |
| 3 | R | $4 \to 1$ | 2, after 1 | $(1, 4, 2)$ | $0 \to 3 \to 4 \to 2$ |
| 4 | C | $4 \to 2$ | new 5 | $(2, 4, 5)$ | $0 \to 3 \to 4 \to 5 \to 2$ |
| 5 | R | $5 \to 2$ | 0, after 2 | $(2, 5, 0)$ | $0 \to 3 \to 4 \to 5$ |
| 6 | R | $5 \to 0$ | 3, after 0 | $(0, 5, 3)$ | $3 \to 4 \to 5$ |
| 7 | E | $5 \to 3$ | 4, before 5 | $(3, 5, 4)$ | closed |

The eight faces are the input faces in the encoder's order, with each vertex renamed by $\varphi$: for example $(0, 2, 4)$ becomes $(0, 1, 2)$ and $(2, 0, 5)$ becomes $(1, 0, 3)$. The bit string is 0 0 101 0 101 101 111, which is $15 = 2 \cdot 8 - 1$ bits. Every one of the 8 start faces gives the same string CCRCRRE.

An S needs a less regular mesh. The tests make random edge flips on an octahedron, an icosahedron and a subdivided octahedron, and these meshes use all five symbols. On the icosahedron split twice into four and then changed by 200 random flips (seed 0, start face 0), the encoder writes 25 S symbols, and the longest right loop that line L7 finds has 28 edges.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows four facts for every valid input.

1. A valid input is a triangulated sphere. If the mesh is closed, oriented, connected through its edges and has $V - E + F = 2$, then no vertex is pinched and the genus is 0.
2. **Key invariant.** Before each step, every unvisited piece is a closed disk bounded by its loop, the loops are simple, and the triangles outside each disk next to its loop are visited. So the five cases are exactly the five places where the tip can be, and the encoder never reaches a visited triangle again.
3. The rule of line L7 gives the length of each right loop. With it, after each symbol the decoder has the same loops, gates and stack as the encoder, with each vertex renamed by $\varphi$. So decoding inverts encoding: DECODE(ENCODE($M$)) is $M$ renamed by $\varphi$, face by face in the encoder's order.
4. **Bit bound.** There are exactly $V - 3$ C symbols and $t - 1$ symbols in all, and $t = 2V - 4$. So the code has exactly $(V - 3) + 3(t - 1 - (V - 3)) = 2t - 1$ bits.

Fact 1 and the disk facts in fact 2 use the Jordan and Schoenflies theorems, which the proof cites. The rest is proved.

## Complexity

The encoder builds the corner table with a [hash table](/hash-table/) on the directed edges in $O(t)$ expected time and then does a constant amount of work for each triangle, so it takes $O(t)$ expected time. The decoder of this page does a constant amount of work for each symbol, plus the walk of line L12, which takes $\ell_i - 1$ steps for each S. A loop with $\ell$ edges bounds a disk of at least $\ell - 2$ triangles, so a right loop has at most $t + 2$ edges, and the walks take $O(t)$ each and $O(t^2)$ in all. This is the bound we prove; we did not build a mesh that reaches it. Both use $\Theta(t)$ space.

Measured on the code of this page (one run each, start face 0; ico$k$ is the icosahedron split $k$ times into four, and the last mesh is ico2 after 200 random edge flips with seed 0):

| mesh | $t$ | C | L | R | S | E | bits per triangle | entropy per triangle |
|---|---|---|---|---|---|---|---|---|
| icosahedron | 20 | 9 | 0 | 9 | 0 | 1 | 1.950 | 1.183 |
| ico1 | 80 | 39 | 1 | 36 | 1 | 2 | 1.988 | 1.297 |
| ico2 | 320 | 159 | 1 | 156 | 1 | 2 | 1.997 | 1.100 |
| ico3 | 1280 | 639 | 1 | 636 | 1 | 2 | 1.999 | 1.031 |
| ico4 | 5120 | 2559 | 1 | 2556 | 1 | 2 | 2.000 | 1.009 |
| ico2, flipped | 320 | 159 | 17 | 92 | 25 | 26 | 1.997 | 1.820 |

The bits per triangle are $(2t - 1)/t$, as proved. The last column is the order-0 [Shannon entropy](/shannon-entropy/) of the symbol string divided by $t$, which is about what an ideal [arithmetic coder](/arithmetic-coding/) with fixed symbol frequencies would need, not counting the frequencies themselves. On the regular subdivided meshes the string is almost only C and R in turn, the traversal goes round in a spiral, and the entropy falls to about 1 bit per triangle. After random flips it is 1.82.

## Properties

- **Proved.** Decoding inverts encoding for every closed connected oriented triangle mesh with $V - E + F = 2$, from every start face.
- **Proved.** The code takes exactly $2t - 1$ bits, so at most 2 bits per triangle, and exactly $V - 3$ symbols are C.
- **Proved.** The numbers of S and E symbols satisfy $n_E = n_S + 1$.
- **Measured.** The tests check DECODE(ENCODE($M$)) $= \varphi(M)$ from every start face of 17 meshes with up to 80 triangles (the pillow, the tetrahedron, octahedron and icosahedron, their subdivisions, 4 bipyramids, and 6 meshes made by random edge flips with seed 7), and from random starts after random renumbering (seed 11).
- **Proved.** Each triangle except the first is reached across its gate from a triangle visited before it, so the gates form a [spanning tree](/spanning-tree/) of the triangles, in which two triangles are joined when they share an edge.
- **Lossless.** The connectivity comes back exactly; only the vertex numbering changes, and $\varphi$ is the order in which the coordinates are sent.
- **Connectivity only.** The method says nothing about the coordinates. No geometric predicate is used.

## Variants and improvements

- **Entropy coding.** The symbols are far from equally likely, so a [Huffman code](/huffman-coding/) of symbol pairs or an arithmetic code does better than the fixed 1 and 3 bit code. Rossignac reports less than 1.5 bits per triangle in this way on large meshes. This is measured on his meshes, not a bound.
- **A better worst case.** King and Rossignac (1999) gave a code with at most $3.67$ bits per vertex, about $1.83$ bits per triangle (check). By Tutte's count of planar triangulations, about $\log_2 (256/27) \approx 3.245$ bits per vertex are needed in the worst case (check).
- **Linear time decoders.** The Wrap and Zip decoder of Rossignac and Szymczak (1999) puts the S tips in place afterwards by zipping the loops, and the Spirale Reversi decoder of Isenburg and Snoeyink (2000) reads the symbols backwards; both take $O(t)$ time (check).
- **Edgebreaker on a corner table.** Rossignac, Safonova and Szymczak (2001) wrote both coders in a few lines on the arrays of a corner table (check).
- **Holes and handles.** Rossignac's paper also handles meshes with boundaries, by one extra vertex in each hole, and meshes of higher genus, where an S can hit a loop that is still on the stack and needs extra information (check). The code of this page rejects these meshes.
- **Valence coding.** Touma and Gotsman (1998) code the degree of each vertex instead of one symbol per triangle; on regular meshes this takes much less than 1 bit per triangle (check).
- **Progressive coding.** A [progressive mesh](/progressive-mesh/) sends a coarse mesh first and then vertex splits, which Edgebreaker cannot do: its order is fixed by the traversal.

## When to use it

Use Edgebreaker to store or send the connectivity of a large triangle mesh in about 2 bits per triangle, or less with entropy coding, instead of the $3 \log_2 V$ bits per triangle of an indexed face set. It needs a manifold mesh; a mesh with non-manifold edges or vertices must be cut into manifold pieces first. The whole string must arrive before the mesh can be used. For streaming at several levels of detail, use a progressive mesh. For a guarantee below 2 bits per triangle, use a coder with a better worst case.

## Pitfalls

- **The wrong side first.** After an S the encoder must finish the right loop before the left one, and the decoder must assume the same. If the order or the side of "go on" in lines L2, L4 and L5 differs between the two, the lengths of line L7 are wrong and the decoder silently builds a different mesh.
- **Orientation.** The cases L and R are told apart by the orientation of the triangles. An input that is not oriented by one rule, for example with one face reversed, makes a directed edge appear twice; the encoder must reject it, and it can be fixed by [consistent mesh orientation](/consistent-mesh-orientation/).
- **Duplicate vertices.** A mesh whose shared vertices were stored twice, once per triangle, has boundaries everywhere and is rejected. Run [vertex welding](/vertex-welding/) first.
- **Testing only the Euler characteristic.** $V - E + F = 2$ alone is not enough. Two octahedra glued at two vertices also have $V - E + F = 2$, but they are not connected through edges, and the encoder must reject them. The tests include this case.
- **Visiting a triangle twice.** On a valid input the encoder never reaches a visited triangle; on a bad input it can, and without a check it may loop. The code of this page raises an error there.
- **Comparing with the input numbering.** The decoder numbers the vertices $0, 1, 2, \dots$ in the order of first visit. A test must rename the input by $\varphi$ before it compares faces.

## Implementations

## History

Jarek Rossignac introduced Edgebreaker in 1999, in IEEE Transactions on Visualization and Computer Graphics, one year after the valence-based coder of Touma and Gotsman (check). His paper gave the five CLERS symbols, the stack for S and the bound of 2 bits per triangle for meshes with the topology of a sphere. Later papers made the decoder run in linear time, lowered the guaranteed bound, and gave a short implementation on a corner table. Edgebreaker and its variants became a standard part of the compression of 3D triangle meshes.

## References
