---
title: The ISW AND gadget is correct, and secure against t probes with 2t + 1 shares
proves: [correctness]
status: full
---

All values are bits and $\oplus$ is XOR. The inputs are $a = (a_1, \ldots, a_n)$ and $b = (b_1, \ldots, b_n)$ with $\bigoplus_i a_i = a$ and $\bigoplus_i b_i = b$, where we use the same letter for the sharing and the secret when no confusion is possible. For each pair $i < j$, line L3 draws a bit $r_{ij}$, and line L4 makes the wires $w^1_{ij} = a_i b_j$, $w^2_{ij} = r_{ij} \oplus a_i b_j$, $w^3_{ij} = a_j b_i$ and $r_{ji} = w^2_{ij} \oplus w^3_{ij}$. Lines L6 and L7 make the partial sums $p_{i,0} = a_i b_i$ and $p_{i,q}$, the XOR of $a_i b_i$ and the first $q$ bits $r_{ij}$ with $j \ne i$ in increasing order of $j$; the output is $c_i = p_{i, n-1}$.

**Theorem 1 (correct output).** For every choice of the random bits, $\bigoplus_i c_i = a b$.

*Proof.* Fix $i < j$. By line L4, $r_{ji} = r_{ij} \oplus a_i b_j \oplus a_j b_i$, so $r_{ij} \oplus r_{ji} = a_i b_j \oplus a_j b_i$. Each $r_{ij}$ with $i \ne j$ appears in exactly one output, $c_i$. So

$$\bigoplus_i c_i = \bigoplus_i a_i b_i \oplus \bigoplus_{i < j} (r_{ij} \oplus r_{ji}) = \bigoplus_i a_i b_i \oplus \bigoplus_{i < j} (a_i b_j \oplus a_j b_i) = \bigoplus_{i, j} a_i b_j .$$

AND distributes over XOR on bits, so the last sum is $(\bigoplus_i a_i)(\bigoplus_j b_j) = a b$. $\square$

**Corollary (compiled circuits).** If each AND gate of a circuit is replaced by the gadget, each XOR by the share-wise XOR and each NOT by a flip of the first share, then the output shares XOR to the output of the circuit, for every choice of random bits. *Proof.* By induction on the gates: share-wise XOR gives $\bigoplus_i (x_i \oplus y_i) = x \oplus y$, a flip of one share gives $x \oplus 1$, and Theorem 1 covers AND. $\square$

**Lemma 2.** Let $x_1, \ldots, x_n$ be a uniform sharing of a bit $x$: the bits $x_1, \ldots, x_{n-1}$ are uniform and independent, and $x_n = x \oplus x_1 \oplus \cdots \oplus x_{n-1}$. For every set $I$ of indices with $|I| \le n - 1$, the bits $(x_i)_{i \in I}$ are uniform and independent, whatever $x$ is.

*Proof.* If $n \notin I$ the claim is the definition. If $n \in I$, pick an index $u \notin I$, which exists because $|I| < n$. The map that sends $(x_1, \ldots, x_{n-1})$ to the values $(x_i)_{i \in I}$ together with $(x_i)_{i \notin I, i \ne u, i < n}$ is a bijection of $\{0,1\}^{n-1}$, because $x_n$ determines $x_u$ given the other bits. A bijection maps the uniform distribution to the uniform distribution, so the values on $I$ are uniform and independent. $\square$

**Theorem 3 (probing security).** Let the sharings of $a$ and $b$ be uniform and independent, let the random bits be uniform and independent of them, and let $n \ge 2t + 1$. Then for every set $P$ of at most $t$ wires of the gadget, the joint distribution of the values on $P$ is the same for all four values of $(a, b)$.

*Proof.* We build a set $I$ of indices from $P$ and a simulator that computes the values on $P$ from $(a_i, b_i)_{i \in I}$ and fresh random bits only. For each wire in $P$:

- if it is $a_i$, $b_i$ or a partial sum $p_{i,q}$ (including $c_i$), add $i$ to $I$;
- if it is $r_{ij}$, $w^1_{ij}$, $w^2_{ij}$, $w^3_{ij}$ or $r_{ji}$ for a pair $i < j$, add $i$ and $j$ to $I$.

Then $|I| \le 2t \le n - 1$. By Lemma 2, applied to each input, and by the independence of the two sharings, the values $(a_i, b_i)_{i \in I}$ are uniform and independent bits, with the same distribution for every $(a, b)$.

The simulator. For each pair $i < j$ with both $i, j \in I$, it draws $r_{ij}$ uniformly and computes $w^1_{ij}, w^2_{ij}, w^3_{ij}, r_{ji}$ from the definitions. For each pair with exactly one index in $I$, say $e \in I$ and $f \notin I$, it draws a uniform bit $\rho_{ef}$ and uses it as $r_{ef}$, the bit that appears in the partial sums of $c_e$. Then it computes each probed $p_{e,q}$ with $e \in I$ from $a_e b_e$ and the bits $r_{ef}$ it has.

The simulation is exact. Fix the input shares. The probed wires use only the bits $r_{ef}$ with $e \in I$: the wires of a pair with an index outside $I$ are not probed, by the rule above, and $p_{e,q}$ uses only bits $r_{ef}$. For a pair with both indices in $I$, the simulator computes the real functions of the real distribution. For a pair $\{e, f\}$ with only $e \in I$, the bit $r_{ef}$ is either the random bit of the pair, if $e < f$, or that bit XOR $a_f b_e \oplus a_e b_f$, if $e > f$. In both cases it is uniform given everything else that is probed, because the random bit of the pair appears in no other probed wire: the only other wire that uses it is $r_{fe}$ or the partial sums of $c_f$, and those are not probed because $f \notin I$. Different pairs have independent random bits. So, given the input shares on $I$, the probed values in the real gadget and in the simulation have the same joint distribution.

The simulator never uses $a$, $b$ or a share outside $I$. So the distribution of the values on $P$ is a function of the distribution of $(a_i, b_i)_{i \in I}$, which does not depend on $(a, b)$. $\blacksquare$

**Remarks.** The bound $n \ge 2t + 1$ comes from the second rule, which adds two indices for one probe. Rivain and Prouff (2010) refine the assignment of indices and prove the same conclusion with $n \ge t + 1$; this page does not reproduce that proof, and the tests check that conclusion by exhaustive enumeration for $(n, t) = (2, 1)$ and $(3, 2)$, which is a complete proof for those two cases. With $n \ge 2t + 1$ the order of line L4 does not matter for this proof: the wire $a_i b_j \oplus a_j b_i$ of the wrong order would add $i$ and $j$ to $I$, like the other wires of the pair. The order matters for the tight bound $n = t + 1$. There the wrong order leaks with $t$ probes, as the tests show for $n = 2$ and $n = 3$, and it is still secure with $n = 2t + 1$, as the tests show for $n = 3$ and $t = 1$.
