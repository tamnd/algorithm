---
title: A Bloomier filter returns the stored value of each key of the set
proves: [correctness, invariant, termination]
status: full
---

Let BUILD succeed with the peeling order $(x_1, c_1), \ldots, (x_n, c_n)$, and write $H(x) = \{h_0(x), h_1(x), h_2(x)\}$. The three cells are in different thirds of the table, so they are distinct. All arithmetic on $T$ is bitwise exclusive or $\oplus$ on $q$-bit values.

**Lemma 1 (the peeling order).** PEEL returns a sequence of all $n$ keys in which each key appears once, $c_i \in H(x_i)$, and $c_i \notin H(x_j)$ for each $j > i$.

*Proof.* Let $K_i$ be the set of keys not yet in the order when the $i$-th pair is appended, so $x_i \in K_i$ and $K_{i+1} = K_i \setminus \{x_i\}$. Line L13 picks $c_i$ with exactly one key of $K_i$ having $c_i$ as a cell, and that key is $x_i$. Each later key $x_j$, $j > i$, lies in $K_{i+1} \subseteq K_i$ and is not $x_i$, so $c_i \notin H(x_j)$. A removed key is never chosen again, so each key appears at most once, and line L14 checks that all $n$ keys appear. $\square$

**Lemma 2 (cells written).** In the loop of lines L4 to L7, the iteration for $x_i$ writes only $T[c_i]$ and $R[c_i]$. The cells $c_1, \ldots, c_n$ are distinct, and $T[c_i]$ is 0 just before the iteration for $x_i$.

*Proof.* The first claim is lines L6 and L7. If $c_i = c_j$ with $i < j$, then $c_i \in H(x_j)$, against Lemma 1. Before the iteration for $x_i$ only the cells $c_j$ with $j > i$ have been written, and these differ from $c_i$. $\square$

**Lemma 3 (invariant (E) after BUILD).** For each $i$,
$$ \mu(x_i) \oplus \bigoplus_{c \in H(x_i)} T[c] = \tau(x_i), \qquad R[c_i] = f(x_i), $$
where $c_i = h_{\tau(x_i)}(x_i)$.

*Proof.* Right after the iteration for $x_i$, line L6 gives $T[c_i] = \tau \oplus \mu(x_i) \oplus \bigoplus_{c \in H(x_i), c \ne c_i} T[c]$, and xoring both sides with $\mu(x_i) \oplus \bigoplus_{c \ne c_i} T[c]$ gives the first equation at that moment. Line L5 chose $\tau$ with $h_\tau(x_i) = c_i$. The later iterations are for $x_{i-1}, \ldots, x_1$, and by Lemma 2 they write only the cells $c_{i-1}, \ldots, c_1$. By Lemma 1, none of them is in $H(x_i)$. So the cells of $x_i$ in $T$ do not change again, and $R[c_i]$ is written only in the iteration for $x_i$, by the distinctness of Lemma 2. $\square$

**Theorem.** After BUILD and any sequence of SET operations on keys of $S$, LOOKUP$(x)$ returns the current value $f(x)$ for each $x \in S$. Each operation ends, and BUILD ends with probability 1.

*Proof.* By Lemma 3, line L8 computes $\tau = \tau(x) \in \{0, 1, 2\}$ for each $x \in S$, so line L9 returns $R[h_{\tau(x)}(x)]$, which is $f(x)$ after BUILD. SET$(x, v)$ computes the same $\tau(x)$ and writes $v$ to $R[h_{\tau(x)}(x)]$, the own cell of $x$. It writes no cell of $T$, so the equations of Lemma 3 stay true for all keys. Its write to $R$ is at the own cell of $x$, which by Lemma 2 is not the own cell of another key, so the values of other keys do not change. LOOKUP and SET take constant time and PEEL takes $O(M + n)$ steps, since each key is removed once and each cell enters the queue at most once per decrease of its count. Each attempt of line L1 uses new random hash functions; after each 10 failures the table grows by 10 percent, so after finitely many failures $s \ge n$. A table with $s \ge n$ peels with positive probability: with positive probability the values $h_0(x)$ of the $n$ keys are distinct, and then each key has a cell of its own. This probability only grows with $s$, so each attempt from then on succeeds with at least a fixed positive probability, and BUILD ends with probability 1. $\blacksquare$
