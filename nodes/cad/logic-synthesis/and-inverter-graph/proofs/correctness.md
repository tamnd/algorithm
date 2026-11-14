---
title: AND keeps the AIG hashed and acyclic, and SIMULATE computes the truth tables
proves: [correctness]
status: full
---

The inputs are $x_1, \ldots, x_n$. For a literal $\ell = 2u + c$ we write $f_\ell$ for its function: $f_\ell = f_u$ if $c = 0$ and $f_\ell = \neg f_u$ if $c = 1$. The node 0 has $f_0 = 0$, the input node $i$ has $f_i = x_i$, and an AND node $v$ with fanins $a, b$ has $f_v = f_a \wedge f_b$. So $f_1 = 1$, and $f_{\ell \oplus 1} = \neg f_\ell$ for every literal.

**Invariant (H).** For every AND node $v$: (a) its fanins satisfy $2 \le a < b$ and $a \ne b \oplus 1$; (b) $a$ and $b$ are literals of nodes with numbers smaller than $v$; (c) the table $T$ maps $(a, b)$ to $v$. And $T$ has no key other than the fanin pairs of the AND nodes.

At the start there are no AND nodes and $T$ is empty, so (H) holds. Only line L7 adds a node or a key.

**Lemma 1.** If (H) holds before a call AND(a, b), it holds after the call, and the call returns a literal $r$ with $f_r = f_a \wedge f_b$.

*Proof.* Line L1 swaps the arguments, which does not change $f_a \wedge f_b$. So assume $a \le b$ from now on. If $a = 0$, then $f_a = 0$ and the result 0 is right. If $a = 1$, then $f_a = 1$ and the result $b$ is right. If $a = b$, then $f_a \wedge f_a = f_a$. If $a = b \oplus 1$, then $f_a = \neg f_b$ and $f_a \wedge f_b = 0$. None of these cases changes the graph or $T$, so (H) still holds.

Otherwise $2 \le a < b$ and $a \ne b \oplus 1$. If $T$ holds the key $(a, b)$, then by (H) the key belongs to a node $v$ with fanins exactly $a$ and $b$, so $f_{2v} = f_v = f_a \wedge f_b$, and line L6 returns $2v$ with no change. If $T$ does not hold the key, line L7 makes a node $v$ with the fanins $(a, b)$. Part (a) of (H) holds for $v$ by the cases just ruled out. The literals $a$ and $b$ were made before this call, so their nodes have numbers smaller than $v$, which is part (b). Line L7 adds the key $(a, b)$ with the value $v$, which is part (c), and this key is new, so it does not change the value of any older key. The result $2v$ has the function $f_a \wedge f_b$. $\square$

**Corollary 2.** No two AND nodes have the same pair of fanins, and the graph has no directed cycle.

*Proof.* If two nodes $v \ne v'$ had the same pair $(a, b)$, then by part (c) the table would map $(a, b)$ to both, which a table cannot do. Every edge goes from a node to a node with a smaller number by part (b), so every directed path has strictly falling numbers and cannot close. $\square$

**Lemma 3.** SIMULATE returns, for each $o_j$, the integer whose bit $m$ is $f_{o_j}$ at the input point $m$.

*Proof.* We show by induction on $v$ that after line L9 has handled node $v$, $\mathrm{val}[v]$ has bit $m$ equal to $f_v$ at point $m$, for every node up to $v$. Line L8 sets this for the node 0 and the inputs. For an AND node $v$ with fanins $a$ and $b$, both fanin nodes are smaller than $v$ by part (b), so their values are already right. The value of a literal $2u + c$ is $\mathrm{val}[u]$ when $c = 0$ and its bitwise complement in $2^n$ bits when $c = 1$, so it is the table of $f_{2u + c}$. The bitwise AND of the two fanin tables is the table of $f_a \wedge f_b = f_v$. Line L10 reads the literal tables in the same way. $\blacksquare$
