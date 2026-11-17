---
title: VOXEL-DOWNSAMPLE returns one point per occupied voxel, the centroid of the input points in that voxel, and every input point is within s√3 of its representative
proves: [correctness]
status: full
---

Let $P = (p_1, \ldots, p_n)$ be the input points, $s > 0$ the voxel size and $o$ the origin. For an integer triple $c = (i, j, k)$ the voxel is the half-open box

$$V(c) = [o_x + i s, o_x + (i+1) s) \times [o_y + j s, o_y + (j+1) s) \times [o_z + k s, o_z + (k+1) s).$$

Line L3 computes $\mathrm{key}(p) = (\lfloor (p_x - o_x)/s \rfloor, \lfloor (p_y - o_y)/s \rfloor, \lfloor (p_z - o_z)/s \rfloor)$.

**Lemma 1.** $p \in V(c)$ if and only if $\mathrm{key}(p) = c$. So the voxels $V(c)$ partition $\mathbb{R}^3$, and each point lies in exactly one of them.

*Proof.* For a real $t$ and an integer $i$, $\lfloor t \rfloor = i$ holds exactly when $i \le t < i + 1$. Apply this to $t = (p_x - o_x)/s$ and multiply by $s > 0$, which keeps the order: $\lfloor (p_x - o_x)/s \rfloor = i$ exactly when $o_x + i s \le p_x < o_x + (i+1) s$. The same holds for $y$ and $z$. The floor is a function, so each point has one key. $\square$

For a key $c$ and $0 \le t \le n$ let $G_t(c) = \{ m \le t : \mathrm{key}(p_m) = c \}$, the indices of the first $t$ points that fall in $V(c)$.

**Lemma 2 (invariant of the loop at line L2).** After $t$ passes of the loop, the keys of the table $\mathrm{cells}$ are exactly the keys $c$ with $G_t(c) \ne \emptyset$, in the order of the first index in $G_t(c)$, and the entry of each such key holds $\sum_{m \in G_t(c)} p_m$ and $|G_t(c)|$.

*Proof.* By induction on $t$. For $t = 0$ the table is empty (line L1) and every $G_0(c)$ is empty. Assume the claim after $t$ passes and let $c = \mathrm{key}(p_{t+1})$. Then $G_{t+1}(c) = G_t(c) \cup \{t+1\}$, and $G_{t+1}(c') = G_t(c')$ for every other key $c'$. If $G_t(c)$ is empty, $c$ is not in the table, line L4 creates the entry with zero sum and zero count, and the insertion puts $c$ last, which is the order of first indices since $t + 1$ is larger than all earlier first indices. Line L5 then adds $p_{t+1}$ to the sum and $1$ to the count of $c$ only. So the entry of $c$ holds the sum and the size of $G_{t+1}(c)$, and the other entries do not change. $\square$

**Theorem.** VOXEL-DOWNSAMPLE returns, for each voxel $V(c)$ that holds at least one input point, the single point

$$q(c) = \frac{1}{|P \cap V(c)|} \sum_{p \in P \cap V(c)} p,$$

and no other point. The points come in the order in which their voxels are first met in the input. Each $q(c)$ lies in $V(c)$, and every input point $p$ satisfies $\| p - q(\mathrm{key}(p)) \| < s \sqrt{3}$.

*Proof.* After the loop, $t = n$. By Lemma 1, $G_n(c)$ is the set of indices of the points in $V(c)$, so by Lemma 2 the table has one entry for each occupied voxel, with the sum and the count of its points. Each count is at least $1$, so the division at line L8 is defined, and lines L6 to L8 emit the quotient for each entry, in table order. This is the first claim, and the order claim follows from Lemma 2.

$V(c)$ is a product of half-open intervals, so it is convex. The point $q(c)$ is a convex combination of points of $V(c)$, with weights $1/|G_n(c)|$, so $q(c) \in V(c)$. Coordinate by coordinate: each $p_x$ in the voxel satisfies $o_x + i s \le p_x < o_x + (i+1) s$, and an average of numbers in $[a, b)$ lies in $[a, b)$. Two points of one voxel differ by less than $s$ in each coordinate, so their distance is less than $\sqrt{3 s^2} = s \sqrt{3}$. Both $p$ and $q(\mathrm{key}(p))$ lie in $V(\mathrm{key}(p))$, which gives the last claim. The loops run over $n$ points and over at most $n$ entries, so the procedure terminates. $\blacksquare$

The bound $s\sqrt{3}$ is the diameter of a voxel. It is the guarantee a user gets: replacing the cloud by the output moves no point by more than one voxel diagonal, so the one-sided [Hausdorff distance](/hausdorff-distance/) from the input to the output is below $s\sqrt{3}$. The other direction is also below $s \sqrt{3}$, since each output point lies in a voxel with an input point.
