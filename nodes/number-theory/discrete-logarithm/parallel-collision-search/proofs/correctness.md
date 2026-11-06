---
title: Correctness of parallel collision search
proves: [correctness, termination]
status: full
---

Let $p$ be prime, $g \in (\mathbb{Z}/p\mathbb{Z})^*$ of order $n$, $h \in (\mathbb{Z}/p\mathbb{Z})^*$, and $N \ge 1$. The group $(\mathbb{Z}/p\mathbb{Z})^*$ is cyclic of order $p - 1$, so for each divisor $n$ of $p - 1$ it has exactly one subgroup of order $n$, namely $\{y : y^n = 1\}$, and this subgroup is $\langle g \rangle$. For termination we treat the random choices of lines L4, L6 and L17 as independent and uniform.

**Lemma 1 (membership).** Line L1 returns NONE exactly when $h \notin \langle g \rangle$.

*Proof.* $h \in \langle g \rangle$ if and only if $h^n = 1$, by the description of the unique subgroup of order $n$. $\square$

From now on $h = g^{x^*}$ with $0 \le x^* < n$; $x^*$ is unique in this range because $g$ has order $n$. If $h = 1$ then $x^* = 0$ and line L2 is correct, so assume $h \ne 1$, which forces $n \ge 2$.

**Lemma 2 (labels).** At every moment of an epoch, each client satisfies $x_i = g^{a_i} h^{b_i}$, and every entry $T[x] = (a, b)$ satisfies $x = g^a h^b$.

*Proof.* Line L6 and line L17 set $x_i$ from $(a_i, b_i)$ by that formula. Line L18 multiplies $x_i$ by $M_j = g^{u_j} h^{v_j}$ and adds $u_j$ to $a_i$ and $v_j$ to $b_i$, which keeps the relation since exponents of $g$ and $h$ only matter modulo $n$. Line L16 is the only line that writes to $T$, and it writes the current point and label of a client. Line L5 empties $T$ at the start of each epoch. $\square$

**Lemma 3 (soundness).** Any value returned at line L15 equals $x^*$.

*Proof.* At line L10 the client has $x_i = g^{a_i} h^{b_i}$ and the table has $x_i = g^{a'} h^{b'}$, by Lemma 2. Then $g^{a_i - a'} = h^{b' - b_i} = g^{x^*(b' - b_i)}$, so $(b_i - b') x^* \equiv a' - a_i \pmod n$, that is, $s x^* \equiv a' - a_i \pmod n$ with $s$ from line L12. If $s \ne 0$ and $d = \gcd(s, n)$, then $d$ divides $a' - a_i$ because $d$ divides $s x^*$ and $n$, and the solutions of the congruence modulo $n$ are $y + t n/d$ for $0 \le t < d$ with $y$ from line L13. All of these lie in $[0, n)$. Line L15 returns a candidate $z$ only if $g^z = h$, and $x^*$ is the only element of $[0, n)$ with that property, so $z = x^*$. $\square$

So every value the algorithm returns is correct, and by Lemma 1 it returns NONE exactly when there is no solution. It remains to show that, for $h \in \langle g \rangle$ with $h \ne 1$, the algorithm stops with probability $1$.

**Lemma 4 (one epoch succeeds with positive probability).** There is a $q > 0$, depending only on $p$, $n$ and $N$, such that each epoch returns with probability at least $q$, whatever happened in earlier epochs.

*Proof.* Consider client 1 in the first two rounds of an epoch. Let $x_1 = g^{a_1} h^{b_1}$ be its start from line L6 and let $(a_1', b_1')$ be its first restart label from line L17, giving $x_1' = g^{a_1'} h^{b_1'}$. Consider the event $E$ that

1. $x_1 \in D$, and
2. $b_1' \equiv b_1 + 1 \pmod n$ and $a_1' \equiv a_1 - x^* \pmod n$.

Part 2 gives $x_1' = g^{a_1 - x^*} h^{b_1 + 1} = g^{a_1} h^{b_1} = x_1$. The labels of line L17 are uniform on $(\mathbb{Z}/n\mathbb{Z})^2$ and independent of everything else, so part 2 has probability $1/n^2$. In the implementation, $x \in D$ means that $x \kappa \bmod p$ is divisible by $1/\theta$, for a key $\kappa$ uniform on $\{1, \dots, p - 1\}$ drawn at line L4; for fixed $x \ne 0$ the value $x \kappa \bmod p$ is then uniform on $\{1, \dots, p - 1\}$, so part 1 has probability $\lfloor (p - 1)\theta \rfloor / (p - 1)$, which is positive because $1/\theta \le \sqrt n \le p - 1$. The two parts are independent, so $\Pr[E] = q > 0$.

Suppose $E$ holds. In round 1 client 1 is processed first, the table is empty, and since $x_1 \in D$ line L16 stores $T[x_1] = (a_1, b_1)$ and line L17 restarts client 1 at $x_1'$ with label $(a_1', b_1')$. The other clients in round 1 either return, which by Lemma 3 is a correct answer, or leave the entry $T[x_1]$ unchanged, since line L16 writes only to points not in $T$. In round 2, which exists because $B \ge 16$, client 1 stands at $x_1' = x_1 \in D$, line L10 finds $T[x_1] = (a_1, b_1)$, and line L12 computes $s = b_1' - b_1 \equiv 1$, so $d = 1$. Lines L13 to L15 then test the single candidate, which is $x^*$ by Lemma 3, and return it. $\square$

**Termination.** Each epoch is a finite computation of at most $B$ rounds of $N$ clients, and each client action costs at most $O(\log n + \sqrt n)$ group operations, so each epoch ends. The random choices of different epochs are independent, so by Lemma 4 the probability that the first $e$ epochs all fail is at most $(1 - q)^e$, which tends to $0$. Hence the algorithm stops with probability $1$, and the expected number of epochs is at most $1/q$. The heuristic analysis, under which an epoch fails with small probability, is not part of this proof.

**Conclusion.** By Lemmas 1 and 3, when the algorithm returns, it returns $x^*$ if $h \in \langle g \rangle$ and NONE otherwise, and by Lemma 4 it returns with probability $1$. $\blacksquare$
