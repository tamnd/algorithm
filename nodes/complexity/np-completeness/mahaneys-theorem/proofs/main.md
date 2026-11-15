---
title: Proof of Mahaney's theorem by the left set
proves: [statement]
status: full
---

We give the left-set proof of Ogiwara and Watanabe (1991), as presented by Hemaspaandra and Ogihara (Section 1.1). Mahaney's original proof is different; see the History section of the main page. Throughout, $\le_m^p$ is the polynomial-time many-one (Karp) reduction, computed by a deterministic multitape Turing machine.

**Sparse sets.** A language $S \subseteq \{0,1\}^*$ is sparse when there is a polynomial $p$ such that, for every $\ell$, $S$ has at most $p(\ell)$ strings of length at most $\ell$.

**Theorem.** If $\mathrm{SAT} \le_m^p S$ for some sparse set $S$, then $\mathsf{P} = \mathsf{NP}$.

## The left set

Order $\{0,1\}^n$ lexicographically, which is the order of the strings as binary numbers. For a CNF formula $\varphi$ with variables $x_1, \ldots, x_n$, read an assignment as a string $z = z_1 \cdots z_n$. Define

$$\mathrm{LSAT} = \{\langle \varphi, w\rangle : w \in \{0,1\}^n \text{ and some satisfying assignment } z \text{ of } \varphi \text{ has } z \le w\}.$$

LSAT is in NP: the certificate is $z$, and the verifier checks that $z$ satisfies $\varphi$ and that $z \le w$. Since SAT is NP-complete, $\mathrm{LSAT} \le_m^p \mathrm{SAT}$, and composing with $\mathrm{SAT} \le_m^p S$ gives a reduction $h$ from LSAT to $S$. Let $h$ run in time $r(N)$ on inputs of length $N$, for a polynomial $r$; then $|h(y)| \le r(|y|)$.

## The algorithm

Input: a CNF formula $\varphi$ with $n$ variables. We assume that every pair $\langle \varphi, w\rangle$ with $|w| = n$ has the same length $N$, which is polynomial in $|\varphi|$. Let $q = p(r(N))$. For a string $u$ of length $i \le n$, let $\mathrm{ext}(u) = u 1^{n - i}$, the largest string of length $n$ with prefix $u$.

1. Let $P_0 = \{\varepsilon\}$, the set holding the empty prefix.
2. For $i = 1, \ldots, n$:
   1. Let $K$ be the list of the strings $u0$ and $u1$ for $u \in P_{i-1}$, in increasing order.
   2. For each $u$ in $K$, compute $h(\langle \varphi, \mathrm{ext}(u)\rangle)$.
   3. Scan $K$ in increasing order and delete $u$ if some earlier string in $K$ has the same image.
   4. If more than $q$ strings remain, keep only the $q$ largest. Call the result $P_i$.
3. Accept if some $z \in P_n$ satisfies $\varphi$; otherwise reject.

**Cost.** Each $P_i$ has at most $q$ strings, so each $K$ has at most $2q$, and step 2 makes at most $2qn$ calls to $h$, each on an input of length $N$. Sorting, comparing images and the final check take polynomial time. Since $q$ and $N$ are polynomial in $|\varphi|$, the algorithm runs in polynomial time.

## Correctness

If $\varphi$ is unsatisfiable, no string satisfies it, and step 3 rejects.

Assume $\varphi$ is satisfiable, and let $z^*$ be its smallest satisfying assignment. We show by induction on $i$ that the prefix $z^*_1 \cdots z^*_i$ is in $P_i$. For $i = 0$ this is the empty prefix. Assume it for $i - 1$, and let $u^* = z^*_1 \cdots z^*_i$; then $u^*$ is in the list $K$ at step $i$.

**Monotone membership.** Take $u$ in $K$, so $|u| = i$.

- If $u < u^*$, then every string with prefix $u$ is smaller than every string with prefix $u^*$, so $\mathrm{ext}(u) < z^*$. No satisfying assignment is at most $\mathrm{ext}(u)$, because $z^*$ is the smallest. So $\langle \varphi, \mathrm{ext}(u)\rangle \notin \mathrm{LSAT}$.
- If $u \ge u^*$, then $\mathrm{ext}(u) \ge \mathrm{ext}(u^*) \ge z^*$, since $z^*$ has prefix $u^*$. So $\langle \varphi, \mathrm{ext}(u)\rangle \in \mathrm{LSAT}$.

So along $K$, the strings below $u^*$ give no-instances and the strings from $u^*$ on give yes-instances.

**Step 3 keeps $u^*$.** Every string before $u^*$ in $K$ gives a no-instance, and $u^*$ gives a yes-instance. Since $h$ is a reduction, it maps a yes-instance into $S$ and a no-instance outside $S$, so their images differ. So no earlier string has the image of $u^*$.

**Step 4 keeps $u^*$.** After step 3, the strings $u \ge u^*$ that remain all give yes-instances, so their images are in $S$; the images are pairwise different, and each has length at most $r(N)$. Since $S$ is sparse, there are at most $p(r(N)) = q$ such strings. They are the largest strings left, so $u^*$ is among the $q$ largest, and step 4 keeps it.

So $u^* \in P_i$. For $i = n$ we get $z^* \in P_n$, and step 3 accepts.

Hence SAT is in P. Since SAT is NP-complete, $\mathsf{P} = \mathsf{NP}$. $\blacksquare$

## A run of the pruning

A script ran the algorithm on $\varphi = (x_1 \lor x_2) \land (\lnot x_1 \lor x_3) \land (x_2 \lor x_4) \land (\lnot x_3 \lor \lnot x_4)$. Its satisfying assignments are $0100$, $0101$, $0110$ and $1110$, so $z^* = 0100$. The script used the toy map $h(\langle\varphi, w\rangle)$ = the number of satisfying assignments $z \le w$. This map is not computable in polynomial time, so it does not prove anything; it is only a stand-in for $h$. It is a correct reduction from LSAT, restricted to this formula, to the set $\{1, 2, 3, 4\}$, so $q = 4$.

| Level | Strings in $K$ | Images | After step 3 | After step 4 |
|---|---|---|---|---|
| 1 | 0, 1 | 3, 4 | 0, 1 | 0, 1 |
| 2 | 00, 01, 10, 11 | 0, 3, 3, 4 | 00, 01, 11 | 00, 01, 11 |
| 3 | 000, 001, 010, 011, 110, 111 | 0, 0, 2, 3, 3, 4 | 000, 010, 011, 111 | 000, 010, 011, 111 |
| 4 | 0000, 0001, 0100, 0101, 0110, 0111, 1110, 1111 | 0, 0, 1, 2, 3, 3, 4, 4 | 0000, 0100, 0101, 0110, 1110 | 0100, 0101, 0110, 1110 |

The images are 0 exactly for the no-instances, as the monotone membership says: at level 3 the strings $000$ and $001$ give no-instances and all later strings give yes-instances. At each level the prefix of $z^* = 0100$ survives ($0$, $01$, $010$, $0100$). At level 4, five strings survive step 3, more than $q = 4$, so step 4 drops the smallest, $0000$. The final check finds that $0100$ satisfies $\varphi$ and accepts.
