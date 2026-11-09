---
title: The revised simplex method keeps the basis inverse and follows the simplex method
proves: [correctness, termination]
status: full
---

**Statement.** Let $A \in \mathbb{Q}^{m \times n}$ have rank $m$ and let $B$ be a feasible basis. At line L2 of every iteration of REVISED-SIMPLEX$(A, b, c, B)$, the stored matrix $W$ equals $A_B^{-1}$ and the stored vector $x_B$ equals $A_B^{-1} b$, for the current basis $B$. Hence the method chooses the same entering column and leaving row as the [simplex method](/simplex-method/) with the same rule, its answers are correct, and it stops under Bland's rule.

**Proof.** By induction on the number of pivots. Line L1 sets $W = A_B^{-1}$ and $x_B = W b$, so the claim holds before the first pivot.

Assume $W = A_B^{-1}$ and $x_B = A_B^{-1} b$ at line L2. Then line L3 computes $y^\top = c_B^\top A_B^{-1}$ and line L4 computes $r_j = c_j - y^\top A_j$, which are the multipliers and the reduced costs of the simplex method. Line L6 computes $d = A_B^{-1} A_q$, and line L7 is the ratio test on $x_B$ and $d$. So the iteration makes the same decision as the simplex method, and if it returns, it returns the same answer with the same certificate.

Assume the iteration pivots on $(p, q)$, with $d_p > 0$. Let $B'$ be $B$ with $B(p)$ replaced by $q$, and let $E$ be the identity matrix with column $p$ replaced by $\eta$, where $\eta_p = 1/d_p$ and $\eta_i = -d_i / d_p$ for $i \ne p$. Then $E d = e_p$: row $p$ gives $d_p / d_p = 1$, and row $i \ne p$ gives $d_i - (d_i / d_p) d_p = 0$. For $k \ne p$, the matrix $A_B^{-1}$ maps the column $A_{B(k)}$ to $e_k$, and $E e_k = e_k$ because $k \ne p$. So $E A_B^{-1}$ maps column $k$ of $A_{B'}$, which is $A_{B(k)}$ for $k \ne p$ and $A_q$ for $k = p$, to $e_k$ in both cases:

$$E A_B^{-1} A_{B'} = I.$$

Since $A_{B'}$ is square, $E A_B^{-1} = A_{B'}^{-1}$. Line L9 computes $E W$: row $p$ of $EW$ is $W_p / d_p$, and row $i \ne p$ is $W_i - d_i W_p / d_p$, which is the formula of the implementation. So $W = A_{B'}^{-1}$ after line L9.

For $x_B$: the new basic solution is $A_{B'}^{-1} b = E A_B^{-1} b = E x_B$. Its row $p$ is $x_{B(p)} / d_p = \theta$, and its row $i \ne p$ is $x_{B(i)} - d_i \theta$, which is line L8. So $x_B = A_{B'}^{-1} b$ after line L8.

This completes the induction. Since every iteration matches an iteration of the simplex method from the same basis with the same rule, the correctness and termination theorem of the simplex method (feasible bases, monotone objective, correct certificates, and no repeated basis under Bland's rule) applies to the revised method. $\blacksquare$
