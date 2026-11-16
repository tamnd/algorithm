---
title: Space carving returns the photo hull of the volume whenever a photo-consistent shape exists
proves: [correctness]
status: full
---

We use the discrete model and the pseudocode of the page. Each pixel $p$ of each image has a value $I(p)$, which is a gray value or the background mark $\bot$. Each pixel has a ray, which is an ordered list of voxels. For a set of voxels $V$, the owner $o_V(p)$ is the first voxel of the ray of $p$ that is in $V$, or nothing if no voxel of the ray is in $V$. The pixels of $v$ in $V$ are $P_V(v) = \{p : o_V(p) = v\}$.

The test $c(A)$ on a multiset $A$ of pixel values is true if $\bot \notin A$ and $\max A - \min A \le \tau$, and it is true for the empty multiset. A voxel $v \in V$ passes in $V$ if $c(I(P_V(v)))$ is true. We call $V$ *locally consistent* if every voxel of $V$ passes in $V$, and we say that $V$ *covers* the images if every pixel with $I(p) \ne \bot$ has an owner in $V$. $V$ is *photo-consistent* if it is locally consistent and covers the images. The *photo hull* of the volume $U$ is the union of all photo-consistent subsets of $U$.

**Lemma 1 (monotone test).** If $B \subseteq A$ and $c(A)$ is true, then $c(B)$ is true.

*Proof.* If $\bot \notin A$ then $\bot \notin B$. If $B$ is empty, $c(B)$ is true. Otherwise $\min A \le \min B \le \max B \le \max A$, so $\max B - \min B \le \max A - \min A \le \tau$. $\square$

**Lemma 2 (visibility).** If $V' \subseteq V$ and $v \in V'$, then $P_V(v) \subseteq P_{V'}(v)$.

*Proof.* Let $o_V(p) = v$. The voxels before $v$ on the ray of $p$ are not in $V$, so they are not in $V'$. Since $v \in V'$, the first voxel of the ray in $V'$ is $v$. $\square$

**Lemma 3 (subset).** Let $v \in V$ fail in $V$. Then no locally consistent $S \subseteq V$ contains $v$.

*Proof.* Suppose $v \in S \subseteq V$. By Lemma 2, $P_V(v) \subseteq P_S(v)$. If $v$ passed in $S$, Lemma 1 would make it pass in $V$. So $v$ fails in $S$, and $S$ is not locally consistent. $\square$

**Lemma 4 (largest locally consistent set).** The union $L$ of all locally consistent subsets of $U$ is locally consistent.

*Proof.* Let $v \in L$. Then $v \in S$ for some locally consistent $S \subseteq L$. By Lemma 2, $P_L(v) \subseteq P_S(v)$, and $v$ passes in $S$, so it passes in $L$ by Lemma 1. $\square$

**Lemma 5 (invariant of lines L2 to L6).** At the start of every iteration, $L \subseteq V$.

*Proof.* At line L1, $V = U \supseteq L$. Line L6 removes only voxels that fail in the current $V$. By Lemma 3, no such voxel lies in a locally consistent subset of $V$. $L$ is a locally consistent subset of $V$ by the induction hypothesis and Lemma 4, so no voxel of $L$ is removed. $\square$

**Lemma 6 (termination).** The loop ends after at most $|U| + 1$ iterations.

*Proof.* Each iteration that does not exit at line L5 removes at least one voxel at line L6, and $V$ starts with $|U|$ voxels. $\square$

**Theorem.** SPACE-CARVE returns $V = L$, the largest locally consistent subset of $U$. If $U$ has a photo-consistent subset, then the returned flag is true and $V$ is the photo hull of $U$, and the photo hull is itself photo-consistent. If $U$ has no photo-consistent subset, the flag is false.

*Proof.* By Lemma 6 the loop ends, at line L5, with no failing voxel, so the final $V$ is locally consistent and $V \subseteq L$. Lemma 5 gives $L \subseteq V$. So $V = L$.

Covering is monotone upward: if $S \subseteq T$ and $S$ covers the images, so does $T$, since the ray of each pixel meets $S$ and so meets $T$. Let $S \subseteq U$ be photo-consistent. Then $S \subseteq L = V$, so $V$ covers the images and the flag of line L7 is true. Then $V$ is photo-consistent, so $V$ is contained in the photo hull. Each photo-consistent subset is in $L = V$, so the photo hull is contained in $V$. Thus $V$ is the photo hull, and it is photo-consistent.

If the flag is true, $V$ is a photo-consistent subset of $U$. So if $U$ has no photo-consistent subset, the flag is false. $\blacksquare$

**Order of removal.** The proof of Lemma 5 uses only the fact that each removed voxel fails in the current set, and the final step uses only the fact that no voxel fails when the loop stops. So any schedule gives the same result: one voxel at a time, all failing voxels at once, or the plane sweeps of Kutulakos and Seitz. This is their statement that the order of removal does not matter for correctness.

**A test that is not monotone.** Kutulakos and Seitz require the test to be monotone. A threshold on the standard deviation of the colors is not. The values $\{0, 10\}$ have a standard deviation of 5, and the larger set $\{0, 10, 5, 5, 5\}$ has a standard deviation of $\sqrt{10} \approx 3.16$. With a threshold of 4, a voxel can fail with few visible pixels and pass when it sees more pixels. Then Lemma 1 and Lemma 3 fail, and carving can remove a voxel of a photo-consistent shape. The range test used here is monotone, so the theorem holds for it.

**What is not proved.** The theorem is about the images, not the scene. The photo hull contains every shape that explains the images under the test, including the true scene when the true scene passes the test, but it can be much larger than the true scene where the surface has no texture. The model also treats a pixel as a single ray and a voxel as having one color, so voxels that are partly visible in a pixel are not modeled.
