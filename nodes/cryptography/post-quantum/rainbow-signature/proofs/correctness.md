---
title: A Rainbow signature verifies, because the signer solves the two layers of the central map one after the other and the public map is the central map between two changes of variables
proves: [correctness]
status: full
---

We use the notation of the page. $q$ is odd, $n = v_1 + o_1 + o_2$ and $m = o_1 + o_2$. Coordinates $1..v_1$ are the vinegar of layer 1, the next $o_1$ are the oil of layer 1, and the last $o_2$ are the oil of layer 2. The vinegar of layer 2 is the first $v_2 = v_1 + o_1$ coordinates. Each central form is $f_j(x) = x^T F_j x$ with $F_j$ symmetric. For $j \le o_1$ (layer 1), $F_j$ is zero outside the first $v_2$ rows and columns, and its oil 1 $\times$ oil 1 block is zero. For $j > o_1$ (layer 2), the oil 2 $\times$ oil 2 block of $F_j$ is zero. $S$ is an invertible $n \times n$ matrix, $T$ an invertible $m \times m$ matrix, and $P_k = \sum_j T_{kj} S^T F_j S$.

**Lemma 1 (public map).** For every $s$, $(s^T P_k s)_{k} = T\,(f_j(Ss))_{j}$.

*Proof.* $s^T P_k s = \sum_j T_{kj} (Ss)^T F_j (Ss) = \sum_j T_{kj} f_j(Ss)$. $\square$

**Lemma 2 (each layer is linear in its oil).** Let $p$ be the number of vinegar coordinates of a layer and $r$ its number of oil coordinates, and fix the first $p$ coordinates to $z$. For a central form $F$ of that layer, $f(z, y, 0) = z^T A z + 2 z^T B y$, where $A$ is the top left $p \times p$ block and $B$ the $p \times r$ block next to it. For layer 1 the value does not depend on the last $o_2$ coordinates at all.

*Proof.* Expand $(z, y)^T F (z, y)$ as in the UOV proof: the $y \times y$ block is zero, and the two cross terms are equal scalars. A layer 1 form has zero rows and columns for the last $o_2$ coordinates, so those coordinates never appear. $\square$

**Theorem (correctness).** If SIGN returns $(s, \mathrm{salt})$ for a message $M$, then VERIFY$(pk, M, (s, \mathrm{salt}))$ accepts.

*Proof.* Line L6 sets $t = T^{-1} H(M \,\|\, \mathrm{salt})$. Take the last pass through lines L7 to L9, with vinegar $x_v$. By Lemma 2 with $p = v_1$, $r = o_1$, line L8 builds the $o_1 \times o_1$ system whose solutions are the $x_1$ with $f_j(x_v, x_1, \cdot) = t_j$ for $j \le o_1$, whatever the last $o_2$ coordinates are. SIGN goes on only if the solution is unique. By Lemma 2 with $z = (x_v, x_1)$, $p = v_2$, $r = o_2$, line L9 gives $x_2$ with $f_j(x_v, x_1, x_2) = t_j$ for $j > o_1$. So $x = (x_v, x_1, x_2)$ satisfies $f_j(x) = t_j$ for all $j$. Line L10 returns $s = S^{-1} x$, and Lemma 1 gives $(s^T P_k s)_k = T t = H(M \,\|\, \mathrm{salt})$, which line L11 checks. $\blacksquare$

**Termination.** A pass succeeds when the two square systems are invertible. For uniform matrices this has probability $\prod_{i=1}^{o_1}(1 - q^{-i}) \prod_{i=1}^{o_2}(1 - q^{-i}) > (1 - 1/(q-1))^2$. The matrices are not exactly uniform, so this is a heuristic; the tests confirm that signing is fast.

## The structure that the attacks use

Let $O_2 = S^{-1}\{x : x_i = 0 \text{ for } i \le v_2\}$, of dimension $o_2$, and $W = T\{y \in \mathbb{F}_q^m : y_j = 0 \text{ for } j \le o_1\}$, of dimension $o_2$. Write $P'(y, s) = (2 y^T P_k s)_k$ for the polar form.

**Lemma 3.** For $o \in O_2$: $\mathcal{P}(o) = 0$, and $P'(y, o) \in W$ for every $y$. So the $m \times n$ matrix with rows $(P_k o)^T$ has rank at most $o_2$.

*Proof.* $P'(y, o) = T\,(2 (Sy)^T F_j (So))_j$. The vector $So$ is zero outside the oil 2 coordinates. Layer 1 forms have zero columns there, so the entries $j \le o_1$ are 0, and the vector lies in $W$. For $y = o$ the layer 2 entries vanish too, because the oil 2 $\times$ oil 2 blocks are zero; so $2\mathcal{P}(o) = P'(o, o) = 0$, and $q$ is odd. $\square$

**Lemma 4 (the simple attack finds a vector of $O_2$).** For any $x$, the map $D_x : o \mapsto P'(x, o)$ sends $O_2$ into $W$, two spaces of dimension $o_2$. If this restricted map is singular, some nonzero $o \in O_2$ lies in $\ker D_x$, and it satisfies $\mathcal{P}(o) = 0$ and the rank condition of Lemma 3.

*Proof.* Lemma 3 and $D_x(o) = P'(x, o)$. $\square$

The code searches $\ker D_x$ (dimension $n - m$ for a generic $x$) for a nonzero $o$ with $\mathcal{P}(o) = 0$ and the rank condition. Both tests use only the public key. The theorem below does not need the found $o$ to be in $O_2$; the tests check that it is.

**Lemma 5 (from one vector to $W$ and $O_2$).** Let $o \in O_2$ be such that the vectors $P'(y, o)$ span all of $W$. Then the $c \in \mathbb{F}_q^m$ with $\sum_k c_k P_k o = 0$ are exactly the $c$ orthogonal to $W$, and for those $c$, $\sum_k c_k P_k = S^T G S$ with $G$ a combination of layer 1 forms. The common kernel of these matrices contains $O_2$.

*Proof.* $c^T P'(y, o) = 2 y^T (\sum_k c_k P_k) o$ for all $y$, so $\sum_k c_k P_k o = 0$ if and only if $c$ is orthogonal to the span of the $P'(y, o)$, which is $W$. Then $\sum_k c_k P_k = S^T (\sum_j (T^T c)_j F_j) S$, and $c \perp W$ means $(T^T c)_j = 0$ for $j > o_1$. Layer 1 forms have zero columns at the oil 2 coordinates, so $S^T G S$ kills $O_2$. $\square$

For a generic key the common kernel is exactly $O_2$; the code checks the dimension and the tests compare it with the true $O_2$.

**Theorem (forging with a recovered key).** Let $C$ be a basis of $W^\perp$ with $L_c = \sum_k c_k P_k$, let $O_2$ be as above, and let $U$ be a subspace on which every $L_c$ vanishes. Then the procedure FORGE in the code outputs only valid signatures.

*Proof.* FORGE picks $y$ and solves for $u \in U$ the equations $c^T \mathcal{P}(y + u) = c^T t$ for $c \in C$. Since $L_c$ vanishes on $U$, $(y + u)^T L_c (y + u) = y^T L_c y + 2 y^T L_c u$, which is linear in $u$, so a solution, when the code finds one, gives $z = y + u$ with $\mathcal{P}(z) - t \perp C$, that is $\mathcal{P}(z) - t \in W$. Then it solves for $u_2 \in O_2$ the equations $\mathcal{P}(z + u_2) = t$. By Lemma 3, $\mathcal{P}(u_2) = 0$, so $\mathcal{P}(z + u_2) = \mathcal{P}(z) + P'(z, u_2)$, with $P'(z, u_2) \in W$, linear in $u_2$. So a solution gives $\mathcal{P}(z + u_2) = t$, and VERIFY accepts. $\blacksquare$

The toy code finds $U$ (of dimension $o_1$, inside a complement of $O_2$) by exhaustive search, and checks the vanishing condition from the public key, so the theorem applies to whatever it returns.
