---
title: The Porter-Duff operators equal the coverage algebra, stay premultiplied, and over is associative
proves: [correctness]
status: full
---

A premultiplied pixel is a tuple $p = (r, g, b, \alpha)$ of reals with $0 \le r, g, b \le \alpha \le 1$. If $\alpha > 0$, its straight color is $x = (r, g, b)/\alpha$, so $p = (\alpha x, \alpha)$. We write $a$ and $b$ for the pixels of $A$ and $B$ at one position, with coverages $\alpha_a, \alpha_b$ and straight colors $x_a, x_b$.

**Assumption (Porter and Duff, Section 4.1).** Inside one pixel, $A$ covers a part of area $\alpha_a$, $B$ covers a part of area $\alpha_b$, and $B$ divides both the part covered by $A$ and the part not covered by $A$ in the ratio $\alpha_b : 1 - \alpha_b$. So the four parts have the areas $s_0 = (1-\alpha_a)(1-\alpha_b)$ (neither), $s_A = \alpha_a(1-\alpha_b)$ ($A$ only), $s_B = (1-\alpha_a)\alpha_b$ ($B$ only) and $s_{AB} = \alpha_a\alpha_b$ (both). These are nonnegative and sum to 1.

An operator is a choice of contents for the parts: nothing in "neither", nothing or $A$ in "$A$ only", nothing or $B$ in "$B$ only", and nothing, $A$ or $B$ in "both". Its *exact result* is the area-weighted sum: the color is the sum over the parts of the area times the straight color shown there, and $\alpha$ is the total area of the parts that show a picture.

**Lemma 1.** For each operator, the exact result equals $f_a\, a + f_b\, b$ with the factors of the table.

*Proof.* The parts that can show $A$ are "$A$ only" and "both". Let $S_A$ be the total area of the parts that show $A$. There are four cases. If $A$ shows in both parts, $S_A = s_A + s_{AB} = \alpha_a$. If $A$ shows only in "$A$ only", $S_A = \alpha_a(1-\alpha_b)$. If $A$ shows only in "both", $S_A = \alpha_a \alpha_b$. If $A$ shows nowhere, $S_A = 0$. In each case $S_A = F_A \alpha_a$ with $F_A$ equal to $1$, $1-\alpha_b$, $\alpha_b$ or $0$, the value that the table gives for that choice. The same argument with $A$ and $B$ exchanged gives $S_B = F_B \alpha_b$, with $F_B$ equal to $1$, $1-\alpha_a$, $\alpha_a$ or $0$.

The exact color is $S_A x_a + S_B x_b = F_A \alpha_a x_a + F_B \alpha_b x_b$, which is the color part of $F_A a + F_B b$. The exact coverage is $S_A + S_B = F_A \alpha_a + F_B \alpha_b$, which is the $\alpha$ part of $F_A a + F_B b$. If $\alpha_a = 0$, then $a = 0$ and $S_A = 0$, so the term of $A$ is zero on both sides and the straight color $x_a$ is not needed; the same holds for $b$. Line L5 computes $F_A a + F_B b$ on all four channels, so it computes the exact result. Comparing the twelve rows of the table with the twelve choices of contents completes the proof. $\square$

**Lemma 2.** Each result $c = F_A a + F_B b$ is a premultiplied pixel.

*Proof.* Each factor in the table lies in $[0, 1]$, because $\alpha_a, \alpha_b \in [0, 1]$. So each channel of $c$ is a sum of nonnegative terms, and each color channel satisfies $F_A r_a + F_B r_b \le F_A \alpha_a + F_B \alpha_b = \alpha_c$. By Lemma 1, $\alpha_c$ is the total area of some of the four disjoint parts, so $\alpha_c \le s_0 + s_A + s_B + s_{AB} = 1$. $\square$

**Lemma 3.** For premultiplied pixels $a, b, c$, $(a \text{ over } b) \text{ over } c = a \text{ over } (b \text{ over } c)$, and the pixel $0 = (0, 0, 0, 0)$ satisfies $0 \text{ over } a = a \text{ over } 0 = a$.

*Proof.* By the table, $a \text{ over } b = a + (1-\alpha_a) b$ on all four channels. Its coverage is $\alpha_{ab} = \alpha_a + (1-\alpha_a)\alpha_b$, so

$$1 - \alpha_{ab} = 1 - \alpha_a - \alpha_b + \alpha_a\alpha_b = (1-\alpha_a)(1-\alpha_b).$$

Then

$$(a \text{ over } b) \text{ over } c = a + (1-\alpha_a) b + (1 - \alpha_{ab}) c = a + (1-\alpha_a) b + (1-\alpha_a)(1-\alpha_b) c.$$

The coverage of $b \text{ over } c$ is $\alpha_b + (1-\alpha_b)\alpha_c$, which is not used, and

$$a \text{ over } (b \text{ over } c) = a + (1-\alpha_a)\big(b + (1-\alpha_b) c\big) = a + (1-\alpha_a) b + (1-\alpha_a)(1-\alpha_b) c.$$

The two right sides are equal. For the identity, $0 \text{ over } a = 0 + (1 - 0) a = a$ and $a \text{ over } 0 = a + (1-\alpha_a) 0 = a$. By Lemma 2 all intermediate pixels are premultiplied, so each step applies the table to valid inputs. $\square$

**Theorem.** PORTER-DUFF$(op, A, B)$ returns the image $C$ whose pixel at each position is the exact result of $op$ on the pixels of $A$ and $B$ at that position, under the coverage assumption. Each pixel of $C$ is premultiplied, and for $op = $ over the operation is associative with identity $0$.

*Proof.* Line L1 selects the factors of $op$. The loop of line L2 visits each position once, and lines L3 to L5 write $F_A a + F_B b$ there. No other position is read, so the order of the visits does not matter. By Lemma 1 each written value is the exact result, by Lemma 2 it is premultiplied, and Lemma 3 gives the last statement. $\blacksquare$
