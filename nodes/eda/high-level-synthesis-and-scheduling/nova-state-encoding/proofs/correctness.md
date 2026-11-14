---
title: Correctness of the NOVA encoder and the cube count bound
proves: [correctness]
status: full
---

We use the notation of the page and of the [KISS proof](/kiss-symbolic-minimization/). The machine has $n$ states, $k = \lceil \log_2 n \rceil$ (at least 1), and $S$ is a correct minimum symbolic cover. Each cube $c$ of $S$ has an input part $I_c$, a group $G_c$ of present states and a set of asserted outputs (next states $N_t$ and primary outputs $Z_j$). A code $\mathrm{enc}$ is injective from the states to $\{0, 1\}^k$. It meets the face constraint of $G$ when the least subcube $\mathrm{face}(G)$ that holds the codes of $G$ holds no code of a state outside $G$.

For a group $G$, $\kappa(G)$ is the least number of subcubes of $\{0, 1\}^k$ whose union holds every code of $G$ and no code of a state outside $G$. It exists, since the single points $\mathrm{enc}(s)$, $s \in G$, form such a family, so $\kappa(G) \le |G|$.

## Lemma 1 (met means one cube)

$\kappa(G) = 1$ if and only if $\mathrm{enc}$ meets the face constraint of $G$, or $|G| \in \{1, n\}$.

*Proof.* If the constraint is met, $\mathrm{face}(G)$ is one such cube. If $G = \{t\}$, the point $\mathrm{enc}(t)$ is one; if $|G| = n$, the whole cube is one. Conversely, let one cube $D$ hold every code of $G$ and no code outside $G$. Every cube that holds the codes of $G$ contains the least one, so $\mathrm{face}(G) \subseteq D$, and $\mathrm{face}(G)$ holds no code outside $G$ either. $\square$

## Theorem 1 (the cube count bound)

For every injective code, the encoded function has a correct two-level cover with at most $\sum_{c \in S} \kappa(G_c)$ cubes.

*Proof.* For each cube $c$ of $S$, choose subcubes $D_{c,1}, \ldots, D_{c,\kappa(G_c)}$ as in the definition of $\kappa$. Form the encoded cubes $I_c \times D_{c,i}$, each with the output part that the KISS construction gives $c$: the next-state bits $b$ with $\mathrm{enc}(t)_b = 1$ for each state $t$ that $c$ asserts, and the primary outputs that $c$ asserts. Drop those whose output part is empty.

Take a specified pair $(x, s)$, and let $A$ be the set of cubes of $S$ that contain it. An encoded cube from $c$ contains $(x, \mathrm{enc}(s))$ only if $x \in I_c$ and $\mathrm{enc}(s) \in D_{c,i}$ for some $i$. The second holds for some $i$ exactly when $s \in G_c$: if $s \in G_c$ some $D_{c,i}$ holds $\mathrm{enc}(s)$, and if $s \notin G_c$ none does. So the cubes of $S$ that have an encoded cube at $(x, \mathrm{enc}(s))$ are exactly the cubes of $A$, and every output part at that point is the union of the output parts of the cubes from $A$. This is the situation of Lemma 1 of the KISS proof, and the argument of its theorem applies word for word: the next-state bits set at $(x, \mathrm{enc}(s))$ are the 1 bits of $\mathrm{enc}(\delta(x, s))$, and each primary output has the value it has in $S$ at $(x, s)$. Points at unspecified pairs or at unused codes are don't cares. So the cover is correct, and it has at most $\sum_c \kappa(G_c)$ cubes. $\blacksquare$

By Lemma 1, each met group contributes $w(G)$ to the sum and each unmet group with $1 < |G| < n$ contributes $w(G) \kappa(G) \ge 2 w(G)$. When every group is met, the bound is $|S|$, the KISS bound.

## Theorem 2 (what the encoder returns)

Line L8 returns an injective code of $k$ bits that meets every group in kept. Every dropped group $G$ has the property that no injective code of $k$ bits meets every group in kept together with $G$.

*Proof.* We show by induction over the loop that some injective code of $k$ bits meets every group in kept. At the start kept is empty, and an injective code exists because $2^k \ge n$. Line L6 adds a group only when the test succeeds, so the property is kept. At line L8 the property holds, so a code exists, and the reference code finds one, since its backtracking tries every injective code and prunes only partial codes in which the face of the placed members of a group already holds the code of a placed state outside it; faces only grow as more members are placed, so a pruned partial code has no valid completion.

For the second claim, let $G$ be dropped, and let $K_G$ be the set kept before $G$ was tested. No code meets $K_G$ together with $G$. The final kept set contains $K_G$, and a code that meets a set of constraints meets every subset of it, so no code meets the final kept set together with $G$. $\square$

So the kept set is maximal: every group of $S$ is either kept or dropped, and no dropped group can join it.

## What is not proved

Nothing here bounds the weight of the kept set against the largest weight that any code of $k$ bits can meet; a greedy order gives no such guarantee in general, and the tests only measure it. Nothing here says that the returned code makes the final logic small. Theorem 1 is an upper bound for every code, and the codes that meet the same groups can differ in cost; the page shows a machine on which 8 classes of codes meet the same two groups and their minimum covers range from 4 to 6 cubes, found by exhaustive search over all two-bit codes.
