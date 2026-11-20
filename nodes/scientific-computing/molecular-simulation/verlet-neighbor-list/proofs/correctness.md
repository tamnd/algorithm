---
title: The Verlet list with the two-displacement test reports exactly the pairs within the cutoff
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode. The box is $[0, L)^3$ with periodic boundaries. For two points $a$ and $b$, let $\|a - b\|$ be the minimum image distance, the distance from $a$ to the nearest periodic image of $b$:
$$\|a - b\| = \min_{m \in \mathbb{Z}^3} |a - b - L m|.$$
In a cubic box this minimum splits into one term per axis, and the rounding $\Delta_q = (a_q - b_q) - L \, \mathrm{round}((a_q - b_q) / L)$ attains it on each axis, so the code computes exactly $\|a - b\|$. The cutoff is $r_c$, the skin is $s > 0$ and the list radius is $r_\ell = r_c + s$. A build at the positions $r^0$ stores the set $\mathcal{L} = \{(i, j) : i < j, \|r_i^0 - r_j^0\| < r_\ell\}$ and the reference positions $r^0$.

**Lemma 1 (triangle inequality on the torus).** For all points $a$, $b$ and $c$, $\|a - c\| \le \|a - b\| + \|b - c\|$. *Proof.* Choose $m_1$ and $m_2$ with $\|a - b\| = |a - b - L m_1|$ and $\|b - c\| = |b - c - L m_2|$. Then $|a - c - L(m_1 + m_2)| \le |a - b - L m_1| + |b - c - L m_2|$ by the triangle inequality in $\mathbb{R}^3$, and the left side is at least $\|a - c\|$. $\square$

**Lemma 2 (invariant V).** Let $r$ be the current positions, $d_i = \|r_i - r_i^0\|$, and let $d_{(1)} \ge d_{(2)}$ be the two largest values. If $d_{(1)} + d_{(2)} \le s$, then every pair $i < j$ with $\|r_i - r_j\| < r_c$ is in $\mathcal{L}$. *Proof.* Take a pair $i < j$ that is not in $\mathcal{L}$, so $\|r_i^0 - r_j^0\| \ge r_\ell$. By Lemma 1 applied twice,
$$\|r_i^0 - r_j^0\| \le \|r_i^0 - r_i\| + \|r_i - r_j\| + \|r_j - r_j^0\| = d_i + \|r_i - r_j\| + d_j.$$
Since $i \ne j$, $d_i + d_j \le d_{(1)} + d_{(2)} \le s$. So $\|r_i - r_j\| \ge r_\ell - s = r_c$, and the pair is not within the cutoff. $\square$

**Lemma 3 (the half-skin rule).** If $d_{(1)} \le s / 2$, then $d_{(1)} + d_{(2)} \le s$. So the half-skin rule rebuilds whenever the test of line L6 does, and Lemma 2 holds after it too. *Proof.* $d_{(2)} \le d_{(1)} \le s/2$. $\square$

**Theorem.** Each call of PAIRS reports each unordered pair $\{i, j\}$ with $\|r_i - r_j\| < r_c$ exactly once, and no other pair. *Proof.* After lines L5 to L7 there are two cases. If line L6 found $d_{(1)} + d_{(2)} > s$, line L7 rebuilt the list at the current positions, so now $r^0 = r$, all $d_i = 0$, and the hypothesis of Lemma 2 holds. Otherwise line L6 found $d_{(1)} + d_{(2)} \le s$. In both cases, by Lemma 2, every pair within $r_c$ is in $\mathcal{L}$. Line L8 visits each element of $\mathcal{L}$ once, and $\mathcal{L}$ holds each unordered pair at most once, as $(i, j)$ with $i < j$. Line L9 reports exactly the visited pairs with $\|r_i - r_j\| < r_c$. So the reported set is the set of pairs within the cutoff, each once. $\square$

The theorem does not need $r_\ell \le L/2$. That condition, which the implementation checks, makes the nearest image of each pair within $r_\ell$ unique, so that one stored pair stands for one interaction, as the force loop assumes. The theorem also does not assume that the atoms move by small steps: the displacement $d_i$ is the torus distance from the reference position, and Lemma 1 holds for any motion.

**Termination.** BUILD runs over the $N(N-1)/2$ pairs and the $N$ atoms. PAIRS computes $N$ displacements, finds the two largest in $O(N)$, calls BUILD at most once, and runs over the finite list. So each call stops. $\blacksquare$

**Remark (the wrong test).** The test "rebuild when $d_{(1)} > s$" is not safe. Two atoms at distance $r_\ell$ that each move $0.6 s$ toward each other have $d_{(1)} = 0.6 s \le s$, and they end at distance $r_\ell - 1.2 s = r_c - 0.2 s < r_c$, a pair not in the list. Lemma 2 needs the sum of the two displacements, because the gap closes from both ends.
