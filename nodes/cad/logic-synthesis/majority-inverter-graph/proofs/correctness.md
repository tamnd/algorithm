---
title: MAJ keeps the normal form, computes the majority and merges permuted and complemented calls
proves: [correctness]
status: full
---

We use the literal code of the page: literal $2u + c$ names node $u$ with phase $c$, node 0 is the constant 0, and $f_\ell$ is the function of a literal $\ell$ over the primary inputs, so $f_{\ell \oplus 1} = \neg f_\ell$. Write $\mathrm{node}(\ell) = \lfloor \ell / 2 \rfloor$ and $\langle x y z \rangle = xy + xz + yz$.

**Invariant (N).** Every node $v > n$ has fanins $(a, b, c)$ with $a < b < c$, with $\mathrm{node}(a)$, $\mathrm{node}(b)$ and $\mathrm{node}(c)$ distinct and smaller than $v$, and with at most one of $a, b, c$ odd. The table $T$ maps each such triple to its node and holds no other key.

**Lemma 1 (pairs on one node).** After line L1 sorts $a \le b \le c$, if two of the three literals lie on one node, then line L2 or line L3 returns.

*Proof.* The two literals of node $u$ are $2u$ and $2u + 1$, and no other literal lies between them. If $a$ and $b$ lie on one node, then $a = b$ or $b = a \oplus 1$ with $a$ even, and lines L2 or L3 apply. The same holds for $b$ and $c$. If $a$ and $c$ lie on one node, then $a \le b \le c \le a + 1$, so $b = a$ or $b = c$, and line L2 applies. $\square$

**Lemma 2 (the function).** MAJ(a, b, c) returns a literal $r$ with $f_r = \langle f_a f_b f_c \rangle$, and it keeps (N).

*Proof.* Sorting at line L1 does not change the function, since $\langle x y z \rangle$ is symmetric. Line L2 returns $b$ when two inputs are equal, and $\langle x x z \rangle = x$, since at least two of the three values are the value of $x$. Line L3 returns the third input when two inputs are complements, and $\langle x \bar{x} z \rangle = z$, since exactly one of $x, \bar{x}$ is 1. Past line L3, by Lemma 1, the three literals lie on three different nodes. If two or more are odd, line L4 calls MAJ on the three complements. These lie on the same three nodes, and at most one of them is odd, so the inner call passes lines L2 to L4 and reaches line L5. By induction on the depth of the calls, it returns a literal $s$ with $f_s = \langle \bar{f_a} \bar{f_b} \bar{f_c} \rangle$, and $f_{s \oplus 1} = \overline{\langle \bar{f_a} \bar{f_b} \bar{f_c} \rangle} = \langle f_a f_b f_c \rangle$, because complementing all three values of a majority complements the result: two or more ones become two or more zeros. At line L5 the triple is sorted, on three distinct nodes and has at most one odd literal. If $T$ holds it, $T$ maps it to a node whose fanins are exactly $(a, b, c)$ by (N), and that node computes $\langle f_a f_b f_c \rangle$. Otherwise line L6 makes a node with these fanins, which all lie on older nodes, and adds its key, so (N) holds again. $\square$

**Lemma 3 (permutations and complements).** For all literals, MAJ returns the same literal for every order of $a, b, c$, and MAJ($a \oplus 1, b \oplus 1, c \oplus 1$) $=$ MAJ($a, b, c$) $\oplus 1$.

*Proof.* After line L1 the computation depends only on the sorted triple, which is the same for every order. For the second claim, let $(a, b, c)$ be sorted. If two literals lie on one node, complementing all three keeps each pair on its node and keeps the sorted order up to a swap inside a pair, which the tests of lines L2 and L3 do not see. So both calls return at the same test, one with the result $b$ or the third literal and the other with its complement. Otherwise the three nodes are distinct, so complementing every literal keeps the order of the nodes and the sorted order. Let $k$ be the number of odd literals in $(a, b, c)$, so the complements have $3 - k$. Exactly one of $k$ and $3 - k$ is at least 2. The call with the larger count goes through line L4 to the call with the smaller count and flips its result, so the two results differ exactly in the phase. $\square$

**Theorem.** Starting from an empty graph, every sequence of INPUT and MAJ calls keeps (N), each call returns a literal with the right function, and no two nodes have the same triple of fanins. SIMULATE returns the truth table of each requested literal.

*Proof.* The empty graph satisfies (N), and Lemma 2 keeps it and gives the functions. Line L6 adds a key only when $T$ does not hold it, so no two nodes share a triple. For SIMULATE, the fanins of node $v$ lie on nodes smaller than $v$ by (N), so when line L8 reaches $v$ the values of its fanins are their truth tables, by induction on $v$, and the bitwise $(x \wedge y) \vee (x \wedge z) \vee (y \wedge z)$ is the majority at each point. Line L9 complements the table of a node for an odd literal. $\blacksquare$
