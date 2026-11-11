---
title: With leaf and node prefixes, a Merkle tree root binds the list, and inclusion proofs are complete and sound
proves: [correctness]
status: full
---

We use the notation of the page. $H$ is a hash function, and a *collision* is a pair $x \ne x'$ with $H(x) = H(x')$. All lists have known sizes; the shape of the tree of $n$ leaves is fixed by $n$ (split at $k$, the largest power of two below $n$).

**Lemma 1 (completeness of inclusion proofs).** For $0 \le m < n$, ROOT-FROM-PATH$(m, n, H(00 \| d_m), \mathrm{PATH}(m, D[n])) = \mathrm{MTH}(D[n])$.

*Proof.* Induction on $n$. For $n = 1$ the path is empty, $m = 0$, and both sides are $H(00 \| d_0)$. For $n \ge 2$, suppose $m < k$. Then PATH ends with $\mathrm{MTH}(D[k:n])$, and the part before it is $\mathrm{PATH}(m, D[0:k])$. ROOT-FROM-PATH takes the last hash as the right sibling and recurses with $(m, k)$ on the rest, which by induction returns $\mathrm{MTH}(D[0:k])$. It returns $H(01 \| \mathrm{MTH}(D[0:k]) \| \mathrm{MTH}(D[k:n]))$, which is $\mathrm{MTH}(D[n])$ by line L3. The case $m \ge k$ is the same with left and right exchanged and the recursion on $(m - k, n - k)$. $\square$

**Lemma 2 (two computations with equal outputs).** Take two evaluations of the tree hash, each a tree of calls $H(00 \| \cdot)$ and $H(01 \| \cdot \| \cdot)$. If their roots are equal and their inputs differ somewhere, then an algorithm that walks both trees from the root finds a collision of $H$ in time linear in the tree size.

*Proof.* Start at the two roots, which have equal outputs. At a pair of nodes with equal outputs, compare their inputs to $H$. If the inputs differ, they are a collision; stop. If they are equal, the first byte is equal, so both are leaves or both are inner nodes. If both are leaves, the data are equal. If both are inner nodes, the 32-byte left halves are equal and the 32-byte right halves are equal, so the two pairs of children have equal outputs. Continue into each pair of children. If the walk never finds a collision, then every pair of leaves met by the walk has equal data, so the two evaluations have the same inputs everywhere, against the assumption. $\square$

**Theorem 1 (binding of the root).** If $n = n'$ and $D[n] \ne D'[n]$ with $\mathrm{MTH}(D) = \mathrm{MTH}(D')$, then Lemma 2 gives a collision of $H$.

*Proof.* The trees have the same shape because $n = n'$, and the leaves differ at some position. Apply Lemma 2. $\blacksquare$

**Theorem 2 (soundness of inclusion proofs).** Suppose VERIFY-INCLUSION$(m, n, d, \pi, r)$ accepts, where $r = \mathrm{MTH}(D[n])$ and $d \ne d_m$. Then a collision of $H$ can be found from $(D, d, \pi)$ in time $O(n)$.

*Proof.* The accepted check is an evaluation of the path from leaf $m$ to the root, with $H(00 \| d)$ at the bottom and the hashes of $\pi$ as siblings. The honest evaluation of $\mathrm{MTH}(D[n])$ contains the same path with $H(00 \| d_m)$ at the bottom and the true siblings. Both have output $r$. Walk down the path from the root as in Lemma 2. At each level, either the two inputs to $H$ differ, which is a collision, or they are equal, in which case the next node on the path has equal outputs on both sides. The shape at each level is fixed by $(m, n)$, so both sides go to the same child. If no collision appears, the bottom inputs are equal, $00 \| d = 00 \| d_m$, against $d \ne d_m$. $\blacksquare$

**Why the prefixes are needed.** Without the prefix bytes, the walk of Lemma 2 can meet a leaf on one side and an inner node on the other with equal inputs, namely a 64-byte leaf $x = \text{left} \| \text{right}$. Equal inputs are not a collision, and the walk cannot continue, because one side has no children. This is exactly the second preimage of the example on the page: a list whose leaves are the inner nodes of another list. With the prefixes, a leaf input starts with `00` and a node input starts with `01`, so equal inputs force equal kinds.

**Tightness.** Each reduction runs the adversary once and makes at most $2n$ extra hash calls, and it succeeds whenever the adversary succeeds. So the advantage against binding is at most the collision advantage against $H$ of an adversary with about the same running time.

**Consistency proofs.** The verifier of consistency proofs rebuilds two roots from one list of hashes, each by an evaluation of the kind used in Theorem 2. If it accepts a proof for an old root $r_m$ that is not the root of the first $m$ entries of the new list, then the evaluation of the new root from the proof and the honest evaluation of $\mathrm{MTH}(D[n])$ differ in some input while their roots agree, and Lemma 2 gives a collision. Completeness follows by the same induction as Lemma 1, on the recursion of SUBPROOF.
