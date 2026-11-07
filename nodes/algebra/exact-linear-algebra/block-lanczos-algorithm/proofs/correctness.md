---
title: Block Lanczos returns independent kernel vectors, and it stops
proves: [correctness, termination]
status: full
---

Let $B$ be an $m \times n$ matrix over $\mathbb{F}_2$, $A = B^T B$, $s \ge 1$ the block width and $Y \in \mathbb{F}_2^{n \times s}$. The iteration produces blocks $V_0, \dots, V_m$ and a block $X$, and the final step works with the $n \times 2s$ matrix $Z = [X + Y \mid V_m]$.

**Claim.** (1) The algorithm stops. (2) It returns a basis of the space $\operatorname{col}(Z) \cap \ker B$. In particular every returned vector $x$ is nonzero with $Bx = 0$, the returned vectors are independent, and if $\ker B = 0$ it returns nothing. (3) If the selection on line L5 succeeds, the matrix $W_i^{\mathrm{inv}}$ it returns satisfies $W_i^{\mathrm{inv}} = S_i (S_i^T T_i S_i)^{-1} S_i^T$, where $T_i = V_i^T A V_i$.

Claim (2) does not depend on how $X$ and $V_m$ were computed, and it holds for every random choice. How large $\operatorname{col}(Z) \cap \ker B$ is, which decides how many vectors are found, is a probabilistic question. The remark at the end explains it but does not prove it.

**(1) Termination.** The loop of line L2 runs at most $n + 10$ times. Each step does a fixed number of block products and $s \times s$ operations. The selection on line L5 is a loop over $s$ columns. Each inner reduction loop of line L10 clears the top bit of `img`, so it runs at most $m$ times. The final echelon loop clears the top bit of `vec` in each pass, so it runs at most $n$ times per vector.

**(2) The final step.** Write $z_0, \dots, z_{2s-1}$ for the columns of $Z$. Line L10 treats them in order and keeps a table `basis` of pairs $(g, h)$ that are indexed by distinct leading positions. Two invariants hold:

- (J1) every stored pair has $g = Bh$ and $g \ne 0$, and $h$ is a sum of columns of $Z$;
- (J2) every pair $(g, h)$ handled during the reduction of column $c$ has $g = Bh$, and $h = z_c + (\text{a sum of } z_{c'} \text{ with } c' < c)$.

At the start of column $c$, the pair is $(Bz_c, z_c)$, and (J2) holds. A reduction step adds a stored pair $(g', h')$. By (J1), $g' = Bh'$, so $g + g' = B(h + h')$. Also $h'$ is a sum of earlier columns, because a pair is stored only when its column is finished. So (J2) still holds. If the reduced image is nonzero, the pair is stored with the leading position of $g$. That position is not in the table, because the loop stopped exactly there. So (J1) holds and the positions stay distinct.

When the image reduces to $0$, (J2) gives $Bh = 0$, and the vector $h$ is put in the list `kernel` if it is nonzero. So every vector in `kernel` lies in $\operatorname{col}(Z) \cap \ker B$.

Conversely, let $P$ be the set of columns whose reduced image is nonzero (the pivot columns) and $Q$ the rest. For $c \in Q$, the reduction gives a coefficient vector $u_c \in \mathbb{F}_2^{2s}$ with $Z u_c = h_c$, $B Z u_c = 0$, a $1$ in position $c$ and zeros in the later positions of $Q$. The images $B z_c$ for $c \in P$ are independent, because their reduced forms have distinct leading positions. So the rank of $BZ$ is $|P|$, and $\ker(BZ)$ has dimension $|Q|$. The $u_c$ for $c \in Q$ are independent, since their entries on $Q$ form a triangular pattern. So they form a basis of $\ker(BZ)$. Every $x \in \operatorname{col}(Z) \cap \ker B$ is $x = Zu$ for some $u$ with $BZu = 0$, which is a combination of the $u_c$. Hence $x$ is a combination of the $h_c = Z u_c$. So the vectors $h_c$ span $\operatorname{col}(Z) \cap \ker B$, and leaving out the zero ones does not change the span.

The last loop of the algorithm reduces each vector of `kernel` against a table `out` with distinct leading positions. Each stored vector is nonzero, and each lies in the span of `kernel`, since it is a sum of vectors of `kernel`. The span of the table is the span of `kernel`: a vector that reduces to zero is a sum of stored vectors. Vectors with distinct leading positions are independent. So `out` is a basis of $\operatorname{col}(Z) \cap \ker B$.

If $\ker B = 0$, this space is $0$, and the algorithm returns nothing. If all tries return nothing, the algorithm returns the empty list. That answer is allowed, and the algorithm never reports a wrong vector. $\square$

**(3) The selection.** The procedure runs Gauss-Jordan elimination on the $s \times 2s$ matrix $[T_i \mid I]$. It takes the columns not in $S_{i-1}$ first. A column $c$ with a pivot in the left half is put in $S_i$. For a column without a left pivot, the row that has a $1$ in position $s + c$ of the right half is used to clear that position in the other rows, and then it is set to zero. Montgomery (1995, Section 8) proves that this produces $W_i^{\mathrm{inv}} = S_i (S_i^T T_i S_i)^{-1} S_i^T$ and a set $S_i$ with $|S_i| = \operatorname{rank} T_i$. The cover condition $S_i \cup S_{i-1} = \{0, \dots, s - 1\}$ is checked explicitly, and the procedure reports a breakdown if it fails. The tests check both identities against a dense inverse, on $400$ random symmetric matrices. Claim (2) does not use (3): a wrong $W_i^{\mathrm{inv}}$ could only lower the number of vectors found.

**Remark: why $Z$ contains kernel vectors.** Write $W_i = \operatorname{col}(V_i S_i)$. Montgomery (1995, Sections 4 to 6) shows that, with the recurrence of lines L7 and L8 and no breakdown:

- the spaces $W_i$ are pairwise $A$-orthogonal, that is, $W_j^T A W_i = 0$ for $i \ne j$;
- each $W_i^T A W_i$ is invertible;
- $W_0 + \dots + W_{i}$ is the Krylov space spanned by $V_0, AV_0, \dots$ up to that step.

The tests check the first property directly on the iterates.

Since the $W_i$ are independent, the dimensions $|S_i|$ add up to at most $n$, so with no breakdown there are at most $n$ iterations. $X = \sum_i V_i W_i^{\mathrm{inv}} V_i^T V_0$ is the $A$-orthogonal projection of $Y$ onto the Krylov space. If the iteration ends with $V_m = 0$, then $AX = V_0 = AY$, so $A(X + Y) = 0$ over $\mathbb{F}_2$. Then $B(X + Y)$ lies in $\ker B^T \cap \operatorname{im} B$, which is usually small, and the elimination of line L10 removes it.

Over $\mathbb{F}_2$, the iteration usually ends instead with $V_m^T A V_m = 0$ but $V_m \ne 0$. Montgomery argues that then $A(X + Y)$ and $A V_m$ together have small rank, so that combinations of the columns of $X + Y$ and $V_m$ lie in $\ker A$, and most of them in $\ker B$. In the worked example on the page, $A(X + Y) = A V_1$ exactly. That is why $Z$ has both. This explanation and the expected count of about $n / (s - 0.76)$ iterations are Montgomery's analysis, not proved here. The page reports the measured counts. $\blacksquare$
