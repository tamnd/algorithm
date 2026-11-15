---
title: The subspace recursion gives a deadbeat gain with the least number of steps, or proves that none exists
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$, and write $\mathcal{B} = \operatorname{range} B$. Define $S_0 = \{0\}$ and

$$S_j = \{x \in \mathbb{R}^n : Ax \in S_{j-1} + \mathcal{B}\}, \qquad j \ge 1.$$

Each $S_j$ is a subspace, because it is the preimage under $A$ of the subspace $S_{j-1} + \mathcal{B}$. Line L2 computes $S_j$: a null vector $(x, a, c)$ of $[A, -V, -B]$ satisfies $Ax = Va + Bc$, where the columns of $V$ span $S_{j-1}$, and the $x$-parts of the null vectors span $S_j$, because the projection of the null space onto the first $n$ coordinates is linear and onto $S_j$.

## Lemma 1: the subspaces grow, and stop growing for good

$S_{j-1} \subseteq S_j$ for all $j \ge 1$. If $S_j = S_{j-1}$ for some $j$, then $S_i = S_{j-1}$ for all $i \ge j - 1$.

*Proof.* $S_0 = \{0\} \subseteq S_1$. If $S_{j-2} \subseteq S_{j-1}$, then for $x \in S_{j-1}$ we have $Ax \in S_{j-2} + \mathcal{B} \subseteq S_{j-1} + \mathcal{B}$, so $x \in S_j$. For the second claim, $S_{j+1}$ is defined from $S_j$ by the same rule as $S_j$ from $S_{j-1}$, so $S_j = S_{j-1}$ gives $S_{j+1} = S_j$, and so on. $\square$

So the dimensions increase strictly until they stop, and the loop of line L1 runs at most $n$ rounds.

## Lemma 2: meaning of the subspaces

$x \in S_j$ if and only if there are inputs $u_0, \dots, u_{j-1}$ that bring $x_0 = x$ to $x_j = 0$.

*Proof.* By induction on $j$. For $j = 0$ both sides say $x = 0$. For $j \ge 1$: if $x \in S_j$, write $Ax = s + Bc$ with $s \in S_{j-1}$, and take $u_0 = -c$; then $x_1 = Ax - Bc = s$, which the induction hypothesis brings to 0 in $j - 1$ more steps. Conversely, if inputs bring $x$ to 0 in $j$ steps, then $x_1 = Ax + Bu_0$ is brought to 0 in $j - 1$ steps, so $x_1 \in S_{j-1}$ and $Ax = x_1 - Bu_0 \in S_{j-1} + \mathcal{B}$. $\square$

## Lemma 3: the gain is deadbeat

Suppose the loop ends with $S_N = \mathbb{R}^n$. Then the gain $K$ of line L5 satisfies $(A - BK) S_j \subseteq S_{j-1}$ for $j = 1, \dots, N$, and $(A - BK)^N = 0$.

*Proof.* Line L3 adds each new basis vector $v$ in the first round $j$ with $v \in S_j$, together with the $c$ of its null vector, so $Av = s + Bc$ with $s \in S_{j-1}$. Because the vectors added before round $j$ span $S_{j-1}$ (Lemma 1 and the fact that line L3 adds a maximal independent set of new vectors), the vectors added up to round $j$ span $S_j$. They are independent by construction, and after round $N$ they form a basis $v_1, \dots, v_n$ of $\mathbb{R}^n$, so $V$ is invertible and $K = C V^{-1}$ is the unique matrix with $K v_i = c_i$. For $v_i$ added in round $j$, $(A - BK) v_i = Av_i - Bc_i = s_i \in S_{j-1}$. Every vector of $S_j$ is a combination of basis vectors added in rounds up to $j$, each of which is mapped into $S_{j'-1} \subseteq S_{j-1}$ for its round $j' \le j$. So $(A - BK) S_j \subseteq S_{j-1}$. Applying this $N$ times gives $(A - BK)^N \mathbb{R}^n = (A - BK)^N S_N \subseteq S_0 = \{0\}$. $\square$

## Lemma 4: no gain needs fewer steps

If $(A - BK')^{N'} = 0$ for some $K'$, then $N' \ge N$.

*Proof.* The feedback inputs $u_k = -K' x_k$ bring every state to $x_{N'} = (A - BK')^{N'} x_0 = 0$. By Lemma 2, every state lies in $S_{N'}$, so $S_{N'} = \mathbb{R}^n$. Since $N$ is the first index with $S_N = \mathbb{R}^n$ and the subspaces grow, $N \le N'$. $\square$

The same argument with open-loop inputs shows that no input sequence brings every state to 0 in fewer than $N$ steps.

## Lemma 5: when the loop fails

If line L4 fails, no deadbeat gain exists, and this happens if and only if $A$ has an uncontrollable eigenvalue other than 0.

*Proof.* Line L4 fails when round $j$ adds no vector, that is, $S_j = S_{j-1} \ne \mathbb{R}^n$. By Lemma 1, $S_i \ne \mathbb{R}^n$ for all $i$, so by Lemma 2 some state cannot be brought to 0 in any number of steps, and by the proof of Lemma 4 no gain is deadbeat.

For the second statement, use the [Kalman decomposition](/kalman-decomposition/): in suitable coordinates $A = \begin{bmatrix} A_{11} & A_{12} \\ 0 & A_{22} \end{bmatrix}$ and $B = \begin{bmatrix} B_1 \\ 0 \end{bmatrix}$ with $(A_{11}, B_1)$ controllable, and the uncontrollable eigenvalues are the eigenvalues of $A_{22}$. For every $K = [K_1, K_2]$, $A - BK$ is block upper triangular with the diagonal blocks $A_{11} - B_1 K_1$ and $A_{22}$. If a deadbeat gain exists, $A - BK$ is nilpotent, so all its eigenvalues are 0, and so are those of $A_{22}$. Conversely, if all eigenvalues of $A_{22}$ are 0, then $A_{22}$ is nilpotent. By the [pole placement theorem](/pole-placement-theorem/) there is a $K_1$ that makes all eigenvalues of $A_{11} - B_1 K_1$ equal to 0, so this block is nilpotent too. With $K_2 = 0$, a block upper triangular matrix with nilpotent diagonal blocks is nilpotent, because its $k$-th power has the $k$-th powers of the diagonal blocks on its diagonal and is again block upper triangular. Then a deadbeat gain exists, and the loop does not fail. $\square$

## Theorem

For every $A$ and $B$, the algorithm either returns $K$ and $N$ with $(A - BK)^N = 0$ and $N$ the least such number over all gains and all input sequences, or it raises an error, and it raises an error exactly when no deadbeat gain exists.

*Proof.* Lemmas 1, 3, 4 and 5. $\square$

## Remarks

- **One input.** If $m = 1$ and $(A, b)$ is controllable, a matrix is nilpotent exactly when its characteristic polynomial is $z^n$, and the [Ackermann formula](/ackermann-formula/) page proves that exactly one gain gives this polynomial. So the algorithm returns the Ackermann gain for $p(z) = z^n$. In the coordinates of the controllable canonical form, $A - bK$ is the companion matrix of $z^n$, a single nilpotent Jordan block of size $n$, so $N = n$. The tests check that the two gains agree.
- **Invertible $A$.** By Lemma 2 and induction, $S_j = A^{-j} \operatorname{range}[B, AB, \dots, A^{j-1} B]$ when $A$ is invertible, so $\dim S_j = \operatorname{rank}[B, \dots, A^{j-1} B]$, and $N$ is the controllability index.
- **Exactness.** With integer or rational data the implementation uses exact fractions, so the rank decisions are exact and $(A - BK)^N = 0$ holds exactly, as the tests check.
