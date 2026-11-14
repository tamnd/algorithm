---
title: The edge table and the vertex table of an indexed face set answer the adjacency queries exactly
proves: [correctness, termination]
status: full
---

**Setup.** The input is a vertex array of length $n$ and a face list $F = (f_0, \ldots, f_{m-1})$, where each face $f = (f[0], \ldots, f[k-1])$ has $k \ge 3$ distinct indices in $\{0, \ldots, n-1\}$. Edge $i$ of $f$ is the undirected pair $\{f[i], f[(i+1) \bmod k]\}$. Write $\mathrm{inc}(e)$ for the list of all pairs $(f, i)$ such that edge $i$ of face $f$ is $e$, in the order of the scan.

**Claim.** After BUILD (lines L1 to L5):

1. For each undirected pair $e$, the table entry $E[e]$ is $\mathrm{inc}(e)$, and $E$ has no other keys.
2. For each vertex $v$, $VF[v]$ lists the faces that contain $v$, each one time, in increasing order.

So EDGE-FACES (line L6) returns the faces on the edge, FACE-NEIGHBORS (line L7) returns exactly the faces other than $f$ that share an edge with $f$, BOUNDARY-EDGES (line L8) returns exactly the edges with one incidence, and line L9 returns $V - E + F$ of the cell complex.

**Proof of 1.** The invariant of the loop of line L2 is: after the faces $f_0, \ldots, f_{j-1}$ and the first $i$ corners of $f_j$ are processed, $E[e]$ is the list of the pairs of $\mathrm{inc}(e)$ that come from those corners, in order, and $E$ has a key $e$ only if this list is not empty. It holds at the start, when $E$ is empty. Line L3 computes edge $i$ of $f_j$, and line L4 appends $(j, i)$ to the entry of exactly that edge, creating the key if it is new. No other entry changes. So the invariant holds after each step, and at the end it is claim 1. The key $\{u, v\}$ is normalized to $(\min, \max)$, so the two directions of an edge go to the same entry.

**Proof of 2.** Line L5 appends $f$ to $VF[u]$ once for each corner $i$ of $f$ with $f[i] = u$. The indices of a face are distinct, so this happens exactly once when $u \in f$ and never otherwise. Faces are processed in increasing order.

**The queries.** EDGE-FACES reads $E[\{u, v\}]$ and drops the corner index, so by claim 1 it returns the faces with $\{u, v\}$ as an edge. FACE-NEIGHBORS visits the entry of each edge of $f$ and keeps each face $g \ne f$ the first time it appears. A face $g \ne f$ is returned if and only if some edge of $f$ has an incidence in $g$, that is, if and only if $g$ and $f$ share an edge. The set $seen$ makes each face appear at most once. BOUNDARY-EDGES keeps the keys whose list has length 1, which by claim 1 are the edges used by exactly one corner of one face.

**Euler characteristic.** The cell complex of the mesh has one 0-cell for each vertex index, one 1-cell for each distinct undirected edge, and one 2-cell for each face. By claim 1 the keys of $E$ are exactly the distinct edges, so $n - |E| + m$ is $V - E + F$. A vertex that no face uses is a 0-cell by itself and adds 1, which is the Euler characteristic of a point.

**Termination.** BUILD runs line L4 once for each corner, that is $\sum_f |f|$ times. Each query loops over a finite list. So every operation stops. $\blacksquare$
