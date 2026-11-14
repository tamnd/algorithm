---
title: SAT sweeping keeps the output functions and returns a functionally reduced AIG
proves: [correctness]
status: full
---

Let $G$ be an AIG with inputs $x_1, \ldots, x_n$, AND nodes in topological order and output literals. For a literal $\ell$ of $G$ or of $H$, write $[\ell]$ for the Boolean function of $\ell$ over $\{0,1\}^n$, so $[2v + 1] = \neg [2v]$ and node 0 is the constant 0. Call two functions $f$ and $g$ *alike* if $f = g$ or $f = \neg g$. During the run, a node of $H$ is *live* if it is the constant, an input, or an AND node that was not dropped at line L9. Let $P$ be the current set of patterns, and $\mathrm{sig}(u)$ the vector of values of node $u$ on $P$. The key of $u$ is $\mathrm{sig}(u)$, complemented if its bit for pattern 0 is 1.

**Lemma 1 (keys).** If $[u]$ and $[u']$ are alike, then $u$ and $u'$ have the same key for every $P$. If $u$ and $u'$ have the same key, then $\mathrm{sig}(u) = \mathrm{sig}(u')$ or $\mathrm{sig}(u) = \neg\mathrm{sig}(u')$, and the phase bit $b$ of line L6, the bit for pattern 0 of $\mathrm{sig}(u) \oplus \mathrm{sig}(u')$, gives $\mathrm{sig}(u) = \mathrm{sig}(u') \oplus b$ on every pattern.

*Proof.* If $[u] = [u']$, the signatures are equal. If $[u] = \neg[u']$, they are complements, and exactly one of them has bit 1 for pattern 0, so after the normalization both keys are the same. Conversely, the key determines the signature up to complement. If the keys agree, the signatures agree or are complements; in the first case the bit for pattern 0 of the XOR is 0, in the second it is 1. $\square$

**Lemma 2 (the miter).** For live nodes $w$ and $r$ and a bit $b$, the miter CNF of line L8 is satisfiable if and only if $[2w] \ne [2r + b]$. A model restricted to the input variables is a pattern on which the two literals differ.

*Proof.* The Tseitin clauses of an AND node $v$ with fanins $a, b$ say $v \leftrightarrow (a \land b)$, and the unit clause of the constant fixes it to 0. Every assignment to the inputs extends to exactly one assignment of the cone variables that meets these clauses, the values computed by the gates. The two last clauses say that the values of $w$ and $r$ with the phase differ. So a model is an input vector, with its gate values, on which the two literals differ, and such a vector gives a model. Inputs outside both cones do not change either value, so any value for them works. $\square$

**Invariant.** After each step of the outer loop, for every node $v$ of $G$ that is done:

- (I1) $\mathrm{image}(v)$ is a literal of a live node of $H$, and $[\mathrm{image}(v)] = [2v]$;
- (I2) the live nodes of $H$ are pairwise not alike;
- (I3) every fanin of a live AND node of $H$ is a literal of a live node, and every entry of the structural hash table points at a literal of a live node with the function of the AND of the entry's fanins;
- (I4) the table of keys used at line L6 maps each key to a live node with that key, and its keys are exactly the keys of the live nodes under the current $P$.

The table of keys keeps one node per key. Two live nodes can share a key, for example two inputs that the starting patterns do not tell apart, and then only one of them is in the table. The proof does not need the keys to be different.

*Base.* Before line L2, $H$ has the constant and the inputs, with $\mathrm{image}(x_i) = 2i$ and $\mathrm{image}(0) = 0$. These functions are pairwise not alike, since $x_i$ is not constant and $x_i$ is neither $x_j$ nor $\neg x_j$ for $i \ne j$. The structural hash table is empty, and the table of keys is built from all of these nodes.

*Step.* Let $v$ be the next AND node of $G$, with fanin literals $a$ and $b$. By (I1) the images $a'$ and $b'$ of the fanins, with their complement bits, are literals of live nodes with $[a'] = [a]$ and $[b'] = [b]$. Line L3 applies three rules. If $a' = 0$ or $a' = \neg b'$, the AND is the constant 0. If $a' = 1$ or $a' = b'$, the AND is the other fanin. If the pair is in the hash table, the AND is the stored literal, which by (I3) is live and has the function $[a'] \land [b']$. In each of these cases line L4 sets an image with $[\mathrm{image}(v)] = [a] \land [b] = [2v]$, and $H$ does not change, so (I1) to (I3) hold.

Otherwise line L3 makes a new AND node $w$ with fanins $a', b'$, which are live, and $[2w] = [2v]$. During the loop of lines L5 to L10, the live nodes other than $w$ are those of before the step, and (I4) holds for them: the code rebuilds the table of keys from them, without $w$, each time $P$ changes. At line L6, $r$ is the node that the table gives for the key of $w$.

If there is no such $r$ (line L7), then by (I4) no live node other than $w$ has the key of $w$, and by Lemma 1 no live node is alike to $w$. So (I2) holds with $w$ added, and $\mathrm{image}(v) = 2w$ gives (I1). The new hash entry points at $w$, so (I3) holds. The key of $w$ goes into the table, so (I4) holds.

If the miter is unsatisfiable (lines L8 and L9), then $[2w] = [2r + b]$ with the phase $b$ of Lemma 1, by Lemma 2. The image of $v$ is $2r + b$, a literal of a live node with $[2r + b] = [2v]$, so (I1) holds. The node $w$ is dropped, and the live nodes are those of before, so (I2) and (I4) hold. No live node has $w$ as a fanin, since $w$ was made in this step and nothing was built after it. The hash entry of the fanins of $w$ now points at $2r + b$, which has the function of the AND of those fanins, so (I3) holds.

If the miter is satisfiable (line L10), the model gives a pattern $p$ with $[2w](p) \ne [2r + b](p)$. Add it to $P$. On the old patterns, $\mathrm{sig}(w) = \mathrm{sig}(r) \oplus b$, and on $p$ this fails, so under the new $P$ the signatures of $w$ and $r$ are neither equal nor complements, and their keys differ. The loop goes back to line L6.

*The loop ends.* Two nodes with different keys under $P$ have different keys under every larger set of patterns, since the signature on more patterns extends the signature on fewer, and pattern 0, which fixes the phase, stays the same. So the node $r$ of a pass through line L10 never again has the key of $w$, and it is never again returned at line L6 in this step. There are finitely many live nodes, so after at most that many passes the loop leaves through line L7 or line L9. This gives the bound on SAT calls of the page.

**Theorem.** SAT-SWEEP returns an AIG whose outputs compute the output functions of $G$, and no two of its nodes are alike.

*Proof.* After the last step, (I1) holds for every node of $G$, so the image of each output literal of $G$, with its complement bit, has the function of that output. Line L11 copies the cones of these literals. By (I3), the cones contain only live nodes, and the copy rebuilds each AND from the copies of its fanins, so each copied node keeps its function, and the outputs keep theirs.

Each copied node is the copy of a different live node, and by (I2) the live nodes are pairwise not alike, so neither are the copies. The constant and the inputs are live nodes too, so no AND node of the result is constant, equal to an input, or equal to the complement of an input. If the copy step meets a pair of fanins that is already in its table, or a constant rule, the result would be a node alike to an existing one, which (I2) rules out, so each live node of the cones gives exactly one node of the result. $\blacksquare$

**Remark.** If a new node $w$ is alike to a live node $u$ that is hidden in the table of keys behind another node $u_2$ with the same key, line L6 returns $u_2$, the miter is satisfiable, and the counterexample separates $w$ from $u_2$. Since $w$ and $u$ are alike, it separates $u$ from $u_2$ too, and the rebuilt table no longer has $u_2$ under the key of $w$. The loop does not end at line L7 while $u$ has the key of $w$, which by Lemma 1 is always, so it ends at line L9 with a node alike to $w$.
