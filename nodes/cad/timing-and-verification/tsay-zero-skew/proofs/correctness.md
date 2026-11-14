---
title: Tsay's merge gives every subtree zero Elmore skew, and the tapping point formula is the unique balance point
proves: [correctness, uniqueness of the tapping point, elongation, complexity]
status: full
---

Wires have resistance $r > 0$ and capacitance $c \ge 0$ per unit length, in the pi model: a wire of length $\ell$ is a resistor $r \ell$ with a capacitor $c \ell / 2$ at each end. Every sink has a load $c_s > 0$. A subtree $A$ has a root point $p_A$, a total capacitance $C_A$ (all its sink loads and wire capacitances) and a delay $t_A$. We say that $A$ is *balanced* when the [Elmore delay](/elmore-delay/) from $p_A$ to every sink of $A$ equals $t_A$. A single sink is balanced with $t = 0$ and $C = c_s$.

**Lemma 1 (adding a wire above a subtree).** Let $A$ be balanced, and connect a new point $u$ to $p_A$ by a wire of length $\ell$. Then the Elmore delay from $u$ to every sink of $A$ is $t_A + r \ell (c \ell / 2 + C_A)$.

*Proof.* Use the downstream form of the Elmore delay: the delay from $u$ to a sink $s$ is the sum, over the resistors on the path from $u$ to $s$, of the resistance times the capacitance below it. The first resistor is $r \ell$, and below it lie the capacitor $c \ell / 2$ at $p_A$ and all of $A$, so it adds $r \ell (c \ell / 2 + C_A)$. Every later resistor lies inside $A$, and the capacitance below it is the same as in $A$ alone, because the new capacitors sit at $u$ and at $p_A$, which are above it. So the later resistors add the Elmore delay from $p_A$ to $s$ in $A$, which is $t_A$. The capacitor $c \ell / 2$ at $u$ is above the first resistor and adds nothing. $\square$

**Lemma 2 (the skew is linear in the tap position).** Let $A$ and $B$ be balanced, at L1 distance $L > 0$, and put the tapping point $u$ on a shortest rectilinear path between $p_A$ and $p_B$, at wire length $s$ from $p_A$ and $L - s$ from $p_B$, with $0 \le s \le L$. The skew $f(s)$, the delay from $u$ to the sinks of $A$ minus that to the sinks of $B$, is
$$ f(s) = t_A - t_B - r L \Big( C_B + \frac{c L}{2} \Big) + r s \,(c L + C_A + C_B). $$
It is strictly increasing, and it is 0 only at $s = x L$ with
$$ x = \frac{t_B - t_A + r L (C_B + c L / 2)}{r L (c L + C_A + C_B)}. $$

*Proof.* By Lemma 1, $f(s) = t_A + r s (c s / 2 + C_A) - t_B - r (L - s)(c (L - s)/2 + C_B)$. The terms in $s^2$ are $r c s^2 / 2 - r c s^2 / 2 = 0$. Collecting the rest: $r c (L - s)^2 / 2 = r c L^2 / 2 - r c L s + r c s^2 / 2$ and $r (L - s) C_B = r L C_B - r s C_B$, which gives the formula. The coefficient of $s$ is $r (c L + C_A + C_B) > 0$, since $C_A > 0$. Solving $f(s) = 0$ gives $s = x L$. $\square$

**Lemma 3 (elongation).** In Lemma 2, if $x < 0$, then $f(s) > 0$ for every $s \in [0, L]$, so no tapping point on a shortest path between the roots balances the merge. With the tap at $p_A$ and a wire of length
$$ \ell^* = \frac{\sqrt{(r C_B)^2 + 2 r c (t_A - t_B)} - r C_B}{r c} \quad (c > 0), \qquad \ell^* = \frac{t_A - t_B}{r C_B} \quad (c = 0) $$
from $p_A$ to $p_B$, the merge is balanced, and $\ell^* > L$. The case $x > 1$ is the mirror image, with the tap at $p_B$.

*Proof.* $x < 0$ means $f(0) > 0$, and $f$ is increasing, so $f > 0$ on $[0, L]$. With the tap at $p_A$, the sinks of $A$ have delay $t_A$, and by Lemma 1 the sinks of $B$ have delay $g(\ell) = t_B + r \ell (c \ell / 2 + C_B)$. The function $g$ is continuous and strictly increasing on $\ell \ge 0$, with $g(L) = t_A - f(0) < t_A$ and $g(\ell) \to \infty$. So $g(\ell) = t_A$ has one root $\ell^* > L$. For $c > 0$ the equation is $\frac{r c}{2} \ell^2 + r C_B \ell - (t_A - t_B) = 0$, whose positive root is the formula, and for $c = 0$ it is linear. A wire of length $\ell^* > L$ between two points at distance $L$ is possible as a detour (a snaked wire). $\square$

**Theorem 1 (zero skew).** Every subtree built by the algorithm is balanced, with the values $C$ and $t$ that the algorithm stores. So the whole tree has zero skew under the Elmore delay, and its delay from the root to every sink is $t$ at the root.

*Proof.* By induction on the topology. A sink is balanced. Let $A$ and $B$ be balanced and $L = d(p_A, p_B)$. If $L > 0$ and $0 \le x \le 1$, Lemma 2 puts the tap at $s = x L$, a point at distance $x L$ from $p_A$ and $(1 - x) L$ from $p_B$, and both sides have the same delay $t_A + r x L (c x L / 2 + C_A)$. If $x < 0$ or $x > 1$, Lemma 3 gives the balanced merge with the stated wire lengths. If $L = 0$, the tap is the common point. When $t_A \ge t_B$, the wire to $B$ gets the length $\ell^*$ of Lemma 3: the same argument holds, since $g(0) = t_B \le t_A$, and $\ell^* = 0$ when $t_A = t_B$. The case $t_A < t_B$ is the mirror image. In all cases the new total capacitance is $C_A + C_B + c (\ell_A + \ell_B)$, which the algorithm stores. $\square$

**Theorem 2 (wire use).** When no merge needs elongation, each merge uses wire of length exactly $d(p_A, p_B)$, the least length that joins the two roots, so the total wire is the sum of these distances. The tree is not always the shortest zero skew tree for the topology, because the roots of the subtrees are fixed when they are merged; [deferred-merge embedding](/deferred-merge-embedding/) delays this choice.

*Proof.* The tap lies on a shortest path between the roots, at distances $x L$ and $(1 - x) L$, which sum to $L$. Any connected wiring that joins two points has length at least their L1 distance. $\square$

**Theorem 3 (time).** For $n$ sinks and a given binary topology the algorithm does $n - 1$ merges, each with $O(1)$ arithmetic operations and at most one square root, so it runs in $O(n)$ time in the real RAM model.

*Proof.* A binary tree with $n$ leaves has $n - 1$ internal nodes, and each merge uses a constant number of operations on the stored values of its two children. $\square$
