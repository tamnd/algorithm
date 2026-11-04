---
title: Green's network sorts each input of 16 items
proves: [correctness]
status: full
---

Call the network $N$. It is a fixed list of standard comparators, so its output is a permutation of its input. By the [zero-one principle](/zero-one-principle/) it is enough to show that $N$ sorts each $x \in \{0, 1\}^{16}$. For wires $w, w' \in \{0, \ldots, 15\}$ write $w \subseteq w'$ when each bit of $w$ is also a bit of $w'$.

**Lemma 1 (the filter).** After lines L1 to L4, for each input over a totally ordered set, the item on wire $w$ is at most the item on wire $w'$ whenever $w \subseteq w'$.

*Proof.* Let $B$ be a set of bits, and say that $x$ is *monotone in $B$* when $x_w \le x_{w + 2^b}$ for each $b \in B$ and each $w$ with bit $b$ equal to 0. The layer for bit $c$ makes $x$ monotone in $c$. We show that it keeps $x$ monotone in each other bit $b$. Take $w$ with bits $b$ and $c$ equal to 0, and let $\beta = 2^b$ and $\gamma = 2^c$. The layer for $c$ replaces the pairs $(x_w, x_{w+\gamma})$ and $(x_{w+\beta}, x_{w+\beta+\gamma})$ by their minimum and maximum. If $x_w \le x_{w+\beta}$ and $x_{w+\gamma} \le x_{w+\beta+\gamma}$ before, then

$$\min(x_w, x_{w+\gamma}) \le \min(x_{w+\beta}, x_{w+\beta+\gamma}), \qquad \max(x_w, x_{w+\gamma}) \le \max(x_{w+\beta}, x_{w+\beta+\gamma}),$$

so the order in bit $b$ holds after the layer. So after the four layers $x$ is monotone in all four bits. If $w \subseteq w'$, add the bits of $w'$ that are not in $w$ one at a time; each step does not decrease the item. $\square$

So for $x \in \{0, 1\}^{16}$, the set $Z$ of wires that hold a 0 after line L4 is a *down-set*: if $w' \in Z$ and $w \subseteq w'$, then $w \in Z$. Let $z = |Z|$. The network sorts $x$ if and only if, at the end, the zeros are on the wires $0, \ldots, z - 1$.

**Lemma 2 (symmetry).** Let $\varphi(x)_w = 1 - x_{15 - w}$. Then $N(\varphi(x)) = \varphi(N(x))$, and $\varphi$ maps sorted sequences to sorted sequences.

*Proof.* For a comparator $[i{:}j]$ let $c'$ be $[15 - j : 15 - i]$. On $\varphi(x)$, the comparator $c'$ writes $\min(1 - x_j, 1 - x_i) = 1 - \max(x_i, x_j)$ to wire $15 - j$ and $1 - \min(x_i, x_j)$ to wire $15 - i$, which is $\varphi$ of the result of $[i{:}j]$ on $x$. Each layer is mapped to itself by $c \mapsto c'$: in lines L1 to L4, $[i : i + 2^b]$ maps to $[15 - i - 2^b : 15 - i]$, which is in the same layer; in lines L5 to L10 the pairs map as $[1{:}2] \leftrightarrow [13{:}14]$, $[4{:}8] \leftrightarrow [7{:}11]$, $[1{:}4] \leftrightarrow [11{:}14]$, $[2{:}8] \leftrightarrow [7{:}13]$, $[10{:}12] \leftrightarrow [3{:}5]$, $[2{:}4] \leftrightarrow [11{:}13]$, $[7{:}9] \leftrightarrow [6{:}8]$, $[7{:}10] \leftrightarrow [5{:}8]$, $[9{:}12] \leftrightarrow [3{:}6]$, $[9{:}10] \leftrightarrow [5{:}6]$, $[11{:}12] \leftrightarrow [3{:}4]$, $[6{:}7] \leftrightarrow [8{:}9]$, and $[3{:}12]$, $[5{:}10]$, $[6{:}9]$, $[7{:}8]$ map to themselves. The comparators of one layer have disjoint wires, so their order does not matter. $\square$

The input $\varphi(x)$ has $16 - z'$ zeros if $x$ has $z'$ zeros. So by Lemma 2 it is enough to show that $N$ sorts each 0-1 input with at most 8 zeros. From now on $z \le 8$.

**The groups.** Let $I = \{1, 2, 4, 8\}$, $M = \{3, 5, 6, 9, 10, 12\}$ and $III = \{7, 11, 13, 14\}$, and let $z_1 = |Z \cap I|$, $z_2 = |Z \cap M|$ and $z_3 = |Z \cap III|$. If $z \ge 1$ then $0 \in Z$. A wire of $III$ in $Z$ brings the three wires of $M$ and the three wires of $I$ below it, and wire 0, so $z_3 \ge 1$ forces $z \ge 8$. Hence $z_3 \le 1$, $z_3 = 1$ only if $z = 8$, $z_1 = z_2 = 3$, and wire $15 \notin Z$. Also a wire of $M$ in $Z$ brings its two wires of $I$, so $z_2 \le \binom{z_1}{2}$.

**Lemma 3 (the four sorts).** Wires 0 and 15 are not touched after line L4. In lines L5 to L7, the comparators on the wires of $I$ are exactly $[1{:}2], [4{:}8], [1{:}4], [2{:}8], [2{:}4]$, and they sort $I$ in the order $1, 2, 4, 8$; wire 8 holds the largest item of $I$ after line L6, and wires 1 and 2 are not touched after line L7. In the same way $III$ is sorted in the order $7, 11, 13, 14$, wire 7 holds its smallest item after line L6, and wires 13 and 14 are not touched after line L7. After line L5, the comparators $[3{:}5]$ (L6), $[6{:}8]$ (L7), $[3{:}6], [5{:}8]$ (L8), $[5{:}6]$ (L9) sort the wires $D = (3, 5, 6, 8)$ in this order, and $[10{:}12]$ (L6), $[7{:}9]$ (L7), $[7{:}10], [9{:}12]$ (L8), $[9{:}10]$ (L9) sort the wires $U = (7, 9, 10, 12)$. After line L8, wire 3 holds the smallest and wire 8 the largest item of $D$, and wire 7 the smallest and wire 12 the largest item of $U$.

*Proof.* Read the layers. Each of the named groups of five comparators is the standard sorter $[a{:}b], [c{:}d], [a{:}c], [b{:}d], [b{:}c]$ on four wires $a, b, c, d$, which sorts each input, and after its third and fourth comparators $a$ holds the minimum and $d$ the maximum. No other comparator touches these wires between the comparators of the group, except that the comparator $[6{:}8]$ of $D$ comes after wire 8 has its final value from $I$ (line L6), and $[7{:}9]$ of $U$ comes after wire 7 has its final value from $III$. In line L9 the comparators $[3{:}4]$, $[7{:}8]$ and $[11{:}12]$ run at the same time as $[5{:}6]$ and $[9{:}10]$, on other wires. $\square$

Now we follow a 0-1 input with $z \le 8$ zeros. Write $\bar{x}_w$ for the bit on wire $w$ after line L4.

Line L5 compares the complementary pairs $(3, 12)$, $(5, 10)$, $(6, 9)$ of $M$. Both wires of such a pair in $Z$ would bring all four wires of $I$ into $Z$. Let $p$ be the number of these pairs with two zeros and $q$ the number with one zero, so $z_2 = 2p + q$, and $p \ge 1$ only if $z_1 = 4$. After line L5, wires 3, 5, 6 hold $p + q$ zeros and wires 9, 10, 12 hold $p$ zeros. With Lemma 3, the group $D$ holds $d = p + q + [z_1 = 4]$ zeros, because wire 8 holds a zero only if all of $I$ is zero, and $U$ holds $u = p + z_3$ zeros. After the sort of $I$, wires $1, 2, 4, 8$ hold $0^{z_1} 1^{4 - z_1}$, and after the sort of $III$, wire 7 holds a 0 if and only if $z_3 = 1$, and wires 11, 13, 14 hold 1.

In each case below $u \le 1$, so wire 12, which holds the largest item of the four wires of $U$, holds 1, and the comparator $[11{:}12]$ of line L9 changes nothing. It remains to follow $[3{:}4]$, $[7{:}8]$ (line L9) and $[6{:}7]$, $[8{:}9]$ (line L10), with $D$ and $U$ sorted. We use $z = 1 + z_1 + z_2 + z_3$ for $z \ge 1$.

*Case $z \le 3$*, so $z_1 \le 2$ and $z_2 = z_3 = 0$. The zeros are on wire 0 and on the first $z - 1$ wires of $I$, that is, on wires $1$ and $2$, and no other wire holds a 0. Every later comparator sees two ones or a 0 on its lower wire. So the output has the zeros on wires $0, \ldots, z - 1$.

*Case $z_1 = 2$, $z_2 = 1$*, so $z = 4$, $p = 0$, $q = 1$, $d = 1$, $u = 0$. Wire 3 holds the only zero of $D$, wires 4 and 8 hold 1, and $U$ holds no zero. The comparators $[3{:}4]$, $[7{:}8]$, $[6{:}7]$, $[8{:}9]$ change nothing. The zeros are on wires 0 to 3.

*Case $z_1 = 3$.* Then $p = 0$, $q = z_2 \le 3$, $d = z_2$, $u = z_3$, wire 4 holds 0 and wire 8 holds 1. So $D$ holds zeros on its first $z_2$ wires in the order $3, 5, 6, 8$, and wire 8 holds 1.

- $z_2 = 0$: wire 3 holds 1 and wire 4 holds 0, so $[3{:}4]$ exchanges them. The zeros are on wires 0 to 3, and $z = 4$.
- $z_2 = 1$: zeros on wires 0, 1, 2, 3, 4, and $z = 5$.
- $z_2 = 2$: zeros on wires 0 to 5, and $z = 6$.
- $z_2 = 3$, $z_3 = 0$: zeros on wires 0 to 6, and wire 7 holds 1. So $z = 7$.
- $z_2 = 3$, $z_3 = 1$: zeros on wires 0 to 6, and wire 7 holds the smallest item of $U$, a 0. So the zeros are on wires 0 to 7, and $z = 8$.

In each subcase, $[7{:}8]$, $[6{:}7]$ and $[8{:}9]$ see a 0 on the lower wire or two equal bits, so they change nothing.

*Case $z_1 = 4$.* Then $z = 5 + z_2 + z_3 \le 8$, so $z_2 \le 3$, and $z_3 = 0$ because $z_3 = 1$ needs $z_1 = 3$. So $(p, q)$ is one of $(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)$, with $d = p + q + 1$ and $u = p$. Wires 1, 2, 4 hold 0, so $[3{:}4]$ changes nothing.

- $(0, 0)$: $d = 1$, a zero on wire 3. Zeros on wires 0 to 4, and $z = 5$.
- $(0, 1)$: $d = 2$, zeros on wires 3 and 5. Zeros on wires 0 to 5, and $z = 6$.
- $(0, 2)$: $d = 3$, zeros on wires 3, 5, 6. Zeros on wires 0 to 6, and $z = 7$.
- $(0, 3)$: $d = 4$, zeros on wires 3, 5, 6, 8, and $u = 0$, so wire 7 holds 1. The comparator $[7{:}8]$ exchanges them. Then the zeros are on wires 0 to 7, wire 8 holds 1, and $[6{:}7]$ and $[8{:}9]$ change nothing. So $z = 8$.
- $(1, 0)$: $d = 2$, zeros on wires 3 and 5; $u = 1$, a zero on wire 7. Wire 8 holds 1, so $[7{:}8]$ changes nothing. Before line L10 the zeros are on wires 0 to 5 and 7, and wire 6 holds 1. The comparator $[6{:}7]$ exchanges them, and $[8{:}9]$ sees two ones. The zeros are on wires 0 to 6, and $z = 5 + 2 = 7$.
- $(1, 1)$: $d = 3$, zeros on wires 3, 5, 6; $u = 1$, a zero on wire 7. Zeros on wires 0 to 7, and $z = 5 + 3 = 8$.

In each case the zeros end on the wires $0, \ldots, z - 1$, so $N$ sorts each 0-1 input with at most 8 zeros. By Lemma 2 it sorts each 0-1 input, and by the zero-one principle it sorts each input. $\blacksquare$
