---
title: Correctness of the modular linear equation solver
proves: [correctness, termination, sorted-output]
status: full
---

Let $a$, $b$ be integers and $n \ge 1$. Write $S = \{ x \in \mathbb{Z} : n \mid ax - b \}$ for the set of integer solutions. We prove that MODULAR-LINEAR-EQUATION-SOLVER$(a, b, n)$ terminates and returns the elements of $S \cap [0, n)$ in increasing order.

**Line L1.** Let $\bar a = a \bmod n$ and $\bar b = b \bmod n$. Since $\bar a \equiv a$ and $\bar b \equiv b \pmod n$, we have $ax - b \equiv \bar a x - \bar b \pmod n$ for every $x$, so the set $S$ does not change. Also $\gcd(\bar a, n) = \gcd(a, n)$. From here on, $a$ and $b$ denote the reduced values, with $0 \le a, b < n$.

**Lemma 1 (line L2).** The loop form of EXTENDED-EUCLID on $(a, n)$ with $a, n \ge 0$, not both 0, terminates and returns $(d, x', y')$ with $d = \gcd(a, n) \ge 1$ and $a x' + n y' = d$.

*Proof.* The loop keeps the invariant $r_0 = a s_0 + n t_0$, $r_1 = a s_1 + n t_1$ and $\gcd(r_0, r_1) = \gcd(a, n)$. It holds at the start, with $(r_0, r_1) = (a, n)$, $(s_0, s_1) = (1, 0)$ and $(t_0, t_1) = (0, 1)$. One pass replaces $(r_0, r_1)$ by $(r_1, r_0 - q r_1)$ with $q = \lfloor r_0 / r_1 \rfloor$, and each coefficient pair by the same linear combination, so both identities hold after the pass; and $\gcd(r_1, r_0 - q r_1) = \gcd(r_0, r_1)$. All remainders are non-negative. From the second pass on, $r_1$ strictly decreases, since $0 \le r_0 \bmod r_1 < r_1$; so the loop stops, with $r_1 = 0$. Then $\gcd(r_0, 0) = r_0$, so $r_0 = \gcd(a, n)$, and $r_0 = a s_0 + n t_0$. Since $n \ge 1$, $d \ge 1$. $\square$

**Lemma 2 (structure of S).** Let $d = \gcd(a, n)$ and $m = n/d$.

1. If $d \nmid b$, then $S = \emptyset$.
2. If $d \mid b$, then $x' (b/d) \in S$, and for any $x^* \in S$, $S = \{ x : x \equiv x^* \pmod m \}$.

*Proof.* (1) If $x \in S$, then $ax - b = nk$ for an integer $k$, so $b = ax - nk$ is a multiple of $d$, because $d$ divides $a$ and $n$.

(2) By Lemma 1, $a x' = d - n y'$. Multiplying by $b/d$ gives $a \cdot x'(b/d) = b - n y'(b/d)$, so $n \mid a \cdot x'(b/d) - b$, and $x'(b/d) \in S$.

Let $x^* \in S$. For any integer $x$, $x \in S$ if and only if $n \mid a(x - x^*)$, since $ax - b = a(x - x^*) + (a x^* - b)$ and $n \mid a x^* - b$. Write $a = d a_1$ and $n = d m$, with $\gcd(a_1, m) = 1$. Then $n \mid a(x - x^*)$ if and only if $m \mid a_1 (x - x^*)$, and, as $\gcd(a_1, m) = 1$, by [Euclid's lemma](/euclids-lemma/) in its general form, if and only if $m \mid x - x^*$. $\square$

**Line L3.** If $d \nmid b$, by Lemma 2(1) $S \cap [0, n) = \emptyset$, and the algorithm returns the empty list, which is correct. From here on, $d \mid b$.

**Line L5.** $x_0 = (x' (b/d)) \bmod m$ satisfies $0 \le x_0 < m$ and $x_0 \equiv x'(b/d) \pmod m$. By Lemma 2(2), with $x^* = x'(b/d)$, $x_0 \in S$ and $S = \{ x_0 + j m : j \in \mathbb{Z} \}$.

**Lines L6 to L9.** We claim the following loop invariant: at the start of the pass with index $i$, for $0 \le i \le d$, the list $X$ holds the elements of $S \cap [0, i m)$ in increasing order, and these are $x_0, x_0 + m, \ldots, x_0 + (i - 1) m$.

*Initialization.* For $i = 0$, $X$ is empty and $[0, 0)$ is empty.

*Maintenance.* The elements of $S$ in $[i m, (i + 1) m)$ are the $x_0 + j m$ with $i m \le x_0 + jm < (i + 1) m$. Since $0 \le x_0 < m$, this holds exactly for $j = i$. So $S \cap [0, (i+1) m)$ is $S \cap [0, im)$ with the one element $x_0 + i m$ added, and that element is larger than all earlier ones. Line L8 appends exactly this element.

*Termination.* The loop runs for $i = 0, \ldots, d - 1$ and stops with $i = d$. Since $d m = n$, the invariant gives that $X$ is $S \cap [0, n)$ in increasing order, with $d$ elements. Line L9 returns it.

Every loop terminates: the gcd loop by Lemma 1, and the final loop after $d$ passes. So the algorithm returns, in increasing order, exactly the residues $x \in \{0, \ldots, n - 1\}$ with $ax \equiv b \pmod n$. $\blacksquare$
