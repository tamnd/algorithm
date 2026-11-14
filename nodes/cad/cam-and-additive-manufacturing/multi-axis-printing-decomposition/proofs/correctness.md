---
title: A plan of support-free planar cuts prints every voxel with support and without head collision, and the cut test is exact for the voxel model
proves: [correctness, termination]
status: full
---

**Setting.** The model is a finite set $V \subset \mathbb Z^3$ of voxels with $z \ge 0$. The directions are $D = \{+z, +x, -x, +y, -y\}$, unit vectors of the grid. For $v \in \mathbb Z^3$ and $d \in D$ the layer of $v$ is $\langle v, d \rangle$, and the support block $S(v, d)$ is the set of the 9 voxels $w$ with $\langle w, d \rangle = \langle v, d \rangle - 1$ and $\max_i |w_i - v_i| \le 1$.

The printing model has three rules.

1. **Support.** A voxel $v$ printed in direction $d$ can be deposited only if a voxel of $S(v, d)$ is already solid, or $d = +z$ and $v_z = 0$ (the platform).
2. **Only the model.** No material outside $V$ is printed, so at every moment the solid set is a subset of $V$.
3. **Head.** While a voxel at layer $\ell$ of direction $d$ is deposited, the print head occupies the open half-space $\{p : \langle p, d \rangle > \ell\}$, and no solid voxel may be there. The platform is not an obstacle.

For a set $R$ and $d \in D$ let $U(R, d) = \{v \in R : S(v, d) \cap R = \emptyset\}$, without the voxels with $v_z = 0$ when $d = +z$. A cut of $R$ is a pair $(d, c)$, with the part $P = \{v \in R : \langle v, d \rangle \ge c\}$ and the rest $R \setminus P$. The cut is valid if $P \cap U(R, d) = \emptyset$ and both $P$ and $R \setminus P$ are nonempty. A plan is a sequence of valid cuts $R_0 = V$, $R_{i+1} = R_i \setminus P_i$ for $i = 0, \dots, m - 1$, with a base $R_m$ such that $U(R_m, +z) = \emptyset$. It is printed as $R_m$ in $+z$, then $P_{m-1}$, …, $P_0$, each part in the order of increasing layer.

**Claim.**

1. (Valid cuts.) The cut $(d, c)$ of $R$ with nonempty part and rest is valid if and only if $c > \max\{\langle v, d \rangle : v \in U(R, d)\}$, with the max of an empty set taken as $-\infty$. Lines L6 to L8 list exactly the valid cuts.
2. (Exactness of the test.) If $P \cap U(R, d) \ne \emptyset$, then under rules 1 and 2 there is no order in which $P$ can be printed in direction $d$ while only $R \setminus P$ is solid at the start and only voxels of $R$ are added.
3. (Soundness.) Every plan prints all of $V$ under rules 1, 2 and 3, every voxel once.
4. (Termination and optimality.) The beam search stops after at most $m + 1$ rounds and returns a plan or failure. The breadth first search returns the least number of parts over all plans, when that number is at most its limit.

**Proof of 1.** The condition $P \cap U(R, d) = \emptyset$ says that no voxel of $U(R, d)$ has layer at least $c$, that is, every voxel of $U(R, d)$ has layer less than $c$. This is $c > \max_{v \in U(R, d)} \langle v, d \rangle$. Line L6 computes this maximum, line L7 keeps the levels $c$ above it and above the lowest level of $R$ (so that the rest is not empty), and every level of $R$ at or below the top gives a nonempty part. A threshold that is not a level of $R$ gives the same part as the next level above it, so only levels need to be listed.

**Proof of 2.** Let $v \in P \cap U(R, d)$. Then $S(v, d) \cap R = \emptyset$, and for $d = +z$ also $v_z > 0$. By rule 2 the solid set at any moment is a subset of $R$ (the voxels already there, $R \setminus P$, and the voxels of $P$ added before $v$). So no voxel of $S(v, d)$ is ever solid when $v$ is deposited, and the platform does not help, so rule 1 fails for $v$ in every order.

**Proof of 3.** Induction over the print order.

*The base.* Print $R_m$ in $+z$, by increasing $z$. Let $v \in R_m$ be deposited at layer $\ell = v_z$. If $v_z = 0$ it rests on the platform. Otherwise $v \notin U(R_m, +z)$, so some $w \in S(v, +z) \cap R_m$ exists, and $w_z = \ell - 1$, so $w$ was deposited in an earlier layer. Rule 1 holds. The solid voxels at that moment are voxels of $R_m$ of layers at most $\ell$, so none is in $\{z > \ell\}$ and rule 3 holds.

*A part.* Assume that $R_{i+1}$ is printed. Print $P_i$ in direction $d = d_i$ by increasing layer. Let $v \in P_i$ at layer $\ell \ge c_i$. The cut is valid, so $v \notin U(R_i, d)$, and some $w \in S(v, d) \cap R_i$ exists, with $\langle w, d \rangle = \ell - 1$. Either $w \in R_{i+1}$, which is solid, or $w \in P_i$ at a lower layer, which was deposited before $v$. So rule 1 holds. The solid voxels at that moment are $R_{i+1}$ and voxels of $P_i$ at layers at most $\ell$. Every voxel of $R_{i+1} = \{u \in R_i : \langle u, d \rangle < c_i\}$ has layer less than $c_i \le \ell$. So no solid voxel is in $\{\langle p, d \rangle > \ell\}$, and rule 3 holds. After $P_i$ the solid set is $R_{i+1} \cup P_i = R_i$.

After the last part the solid set is $R_0 = V$. The sets $R_m, P_{m-1}, \dots, P_0$ are disjoint, because each $P_i \subseteq R_i$ and $R_{i+1} = R_i \setminus P_i$, so every voxel is printed once. Only voxels of $V$ are printed, so rule 2 holds.

**Proof of 4.** Each valid cut has a nonempty part, so $|R_{i+1}| < |R_i|$, and each region has at most $5(h - 1)$ valid cuts, where $h$ is the largest number of levels in one direction. The beam has at most $w$ states, so each round makes finitely many children. The loop of line L2 runs at most $m + 1$ times, and each round either returns at line L3 or replaces the beam. So the search stops. If it returns, the plan is made of valid cuts and a base with $U(R, +z) = \emptyset$, which is a plan in the sense above, so claim 3 applies to it. The breadth first search visits the regions reachable by $k$ valid cuts for $k = 0, 1, 2, \dots$ and stops at the first $k$ at which one of them is a base, so $k + 1$ is the least number of parts. It merges equal regions, which is safe, because the validity of later cuts depends only on the region.

**What is not proved.** The beam search can miss a plan that exists, because it keeps only $w$ regions per round. Rule 3 is a model of the head: a real nozzle has a finite cone, a real printer has a frame and a platform, and the robot that turns the part needs its own collision check. The 45° rule of the support block is a property of the process and is not proved here.
