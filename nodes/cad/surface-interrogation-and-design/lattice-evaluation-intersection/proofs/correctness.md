---
title: Lattice evaluation finds every crossing on the lattice lines, links them correctly in a cell under stated conditions, and finds exactly the components that meet a lattice line
proves: [correctness]
status: full
---

Let $r$ be a polynomial patch on $\Omega = [0, 1]^2$, let $f$ be a polynomial in $x, y, z$, and let $g = f \circ r$, a polynomial in $(u, v)$. The intersection curve in the parameter plane is $Z = \{(u, v) \in \Omega : g(u, v) = 0\}$. The lattice has the lines $u = i / N$ and $v = j / N$ for $0 \le i, j \le N$, and its cells are the squares $C_{ij} = [i/N, (i+1)/N] \times [j/N, (j+1)/N]$. The proof uses exact arithmetic for the roots of line L1 and L2; the code finds them in floating point, and the tests compare them with the sign changes of a dense sampling.

**Claim 1 (lattice points).** Assume that $g$ is not identically zero on any lattice line. Then lines L1 and L2 report exactly the points of $Z$ on the lattice lines, each once.

*Proof.* On the line $u = i/N$ the function $t \mapsto g(i/N, t)$ is a polynomial, the one that line L1 forms, and it is not the zero polynomial by assumption, so it has finitely many roots in $[0, 1]$. The root finder splits $[0, 1]$ at the real roots of the derivative, so the polynomial is monotone on each piece and has at most one root in it. A root in the open part of a piece is a sign change and is found by bisection. A root at an end of a piece is a root of the derivative as well, a multiple root, and is found by the test at that end. So all roots are found, and none twice. The same holds for line L2. A point on two lattice lines, a lattice node, is stored once under its key. $\square$

**Claim 2 (parity).** Call a cell *clean* if no lattice point is at one of its corners and every lattice point on its boundary is a simple root of $g$ along its edge. A clean cell has an even number of lattice points on its boundary.

*Proof.* Go once around the boundary of the cell, starting at a corner. Since $g$ is not zero at the corners, $g$ has a sign there. Along each edge, $g$ changes sign at each simple root and nowhere else, so the sign changes once at each lattice point on the boundary. The walk ends at the start corner with the start sign, so the number of changes is even. $\square$

So an odd count at line L7 means that a lattice point lies at a corner or is a touching point.

**Claim 3 (linking in a cell).** Let $C$ be a clean cell on which $0$ is a regular value of $g$, that is, $\nabla g \ne 0$ at every point of $Z \cap C$, and assume that $Z \cap C$ has no closed component. Let $p_0, \dots, p_{k-1}$ be the boundary points in counterclockwise order. If $k = 2$, line L5 links the two ends of the one arc of $Z \cap C$. If $k = 4$, the arcs of $Z \cap C$ join $p_0$ to $p_1$ and $p_2$ to $p_3$, or $p_1$ to $p_2$ and $p_3$ to $p_0$, and line L6 chooses the right pair whenever the center of $C$ lies in the region of $C \setminus Z$ that touches two opposite pieces of the boundary.

*Proof.* Since $0$ is a regular value, $Z \cap C$ is a compact curve without self crossings, by the implicit function theorem. At a boundary point the zero is simple along the edge, so $Z$ crosses the edge there and the point is an end of the curve. A compact connected curve with ends is an arc with two ends, and since no component is closed, $Z \cap C$ is a set of disjoint arcs whose ends are exactly the $k$ boundary points, so they pair the points.

For $k = 2$ there is one arc, and it joins $p_0$ and $p_1$.

For $k = 4$, two disjoint arcs in the square cannot join $p_0$ to $p_2$ and $p_1$ to $p_3$: the arc from $p_0$ to $p_2$ cuts the square into two parts, by the [Jordan curve theorem](/jordan-curve-theorem/) applied to the arc closed by a piece of the boundary, and $p_1$ and $p_3$ lie in different parts, so an arc that joins them meets it. That leaves the two pairings of the claim. Write $A_{01}$, $A_{12}$, $A_{23}$, $A_{30}$ for the four pieces of the boundary between the points. The function $g$ has no zero on them, so it has a constant sign $s$ on $A_{01}$, then $-s$ on $A_{12}$, $s$ on $A_{23}$ and $-s$ on $A_{30}$, by Claim 2. The two arcs cut $C$ into three regions. On each region $g \ne 0$, and the region is connected, so $g$ has one sign there, the sign on the boundary pieces that the region touches.

If the arcs join $p_0$ to $p_1$ and $p_2$ to $p_3$, the middle region touches $A_{12}$ and $A_{30}$, and $g$ has the sign $-s$ on it. If they join $p_1$ to $p_2$ and $p_3$ to $p_0$, the middle region touches $A_{01}$ and $A_{23}$, with sign $s$. Line L6 evaluates $g$ at a point of $A_{01}$, which gives $s$, and at the center. If the center lies in the middle region, the two signs agree exactly in the second case, which is the pairing line L6 then chooses. $\square$

The condition on the center is not checked by the method. When it fails, the center lies in one of the two outer regions, and line L6 can link the wrong pairs. A closed component inside the cell can also flip the sign at the center.

**Claim 4 (which components are found).** A connected component $K$ of $Z$ has a point on a lattice line exactly when its projection on the $u$ axis contains some $i/N$ or its projection on the $v$ axis contains some $j/N$. In particular, every component whose extent in $u$ or in $v$ is at least $1/N$ is met, and a component inside the interior of one cell is missed.

*Proof.* The projection of a connected set on an axis is connected, so it is an interval $[a, b]$. If it contains $i/N$, some point of $K$ has $u = i/N$, and it lies on the lattice line $u = i/N$. Conversely, a point of $K$ on a lattice line has $u = i/N$ or $v = j/N$, which is in the projection. An interval of length at least $1/N$ in $[0, 1]$ contains a multiple of $1/N$. A component in the interior of a cell has both projections inside open intervals between consecutive lattice values. $\square$

**Claim 5 (what the polylines are).** Each vertex of a polyline is a point of $Z$, and each edge joins two points on the boundary of one cell, so the edge lies in that cell. If every cell is clean, satisfies the conditions of Claim 3, and has at most four boundary points, each polyline has the vertices of one component of $Z$ that meets a lattice line, in the order of the component.

*Proof.* The first part follows from Claim 1 and lines L5 and L6. For the second, by Claim 3 each link of line L5 or L6 is an arc of $Z$ inside a cell between consecutive lattice points of a component. An interior lattice point lies on the common edge of two cells and is the end of one arc in each, so it has two links; a point on the boundary of $\Omega$ has one. Line L8 walks these links, so it follows each component from end to end, or around a closed component back to its start. $\square$

Claim 5 says nothing about the distance between an edge of a polyline and the true curve between its ends. That distance is not bounded by the method, and the page reports it only as a measurement. $\blacksquare$
