---
title: The zero-order hold model is exact at the sampling instants, and one block exponential gives both of its matrices
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ and $h > 0$. The plant is $\dot x(t) = A x(t) + B u(t)$. The input is a zero-order hold signal: $u(t) = u_k$ for $t \in [kh, (k+1)h)$, with any vectors $u_k \in \mathbb{R}^m$. Write $x_k = x(kh)$ and

$$A_d = e^{Ah}, \qquad \Gamma(\tau) = \int_0^\tau e^{As}\, ds, \qquad B_d = \Gamma(h) B.$$

The matrix exponential is $e^{M} = \sum_{j \ge 0} M^j / j!$. The series converges absolutely for every square $M$, it can be differentiated term by term, and $\frac{d}{dt} e^{Mt} = M e^{Mt} = e^{Mt} M$.

## Lemma 1: existence and uniqueness

For every $x_0$ and every zero-order hold input, the plant has exactly one continuous solution on $[0, \infty)$ with $x(0) = x_0$, and on each interval $[kh, (k+1)h]$ it is the solution of $\dot x = A x + B u_k$ that starts at $x_k$.

*Proof.* On one interval the right side $A x + B u_k$ is affine in $x$, so it is globally Lipschitz with constant $\|A\|$. The [Picard-Lindelöf theorem](/picard-lindelof-theorem/) gives one solution on the closed interval. The solutions on consecutive intervals join at $x_{k+1}$, so the joined function is continuous and solves the equation at every $t$ that is not a sampling instant. Uniqueness on each interval gives uniqueness of the joined function, by induction on $k$. $\square$

## Lemma 2: the solution on one interval

For $\tau \in [0, h]$, $x(kh + \tau) = e^{A\tau} x_k + \Gamma(\tau) B u_k$.

*Proof.* Let $z(\tau)$ be the right side. Then $z(0) = x_k$, because $e^{0} = I$ and $\Gamma(0) = 0$. By the fundamental theorem of calculus, $\Gamma'(\tau) = e^{A\tau}$, so

$$z'(\tau) = A e^{A\tau} x_k + e^{A\tau} B u_k.$$

Also $A \Gamma(\tau) = \int_0^\tau A e^{As}\, ds = e^{A\tau} - I$, because $A e^{As}$ is the derivative of $e^{As}$. So

$$A z(\tau) + B u_k = A e^{A\tau} x_k + (e^{A\tau} - I) B u_k + B u_k = A e^{A\tau} x_k + e^{A\tau} B u_k = z'(\tau).$$

So $z$ solves $\dot x = A x + B u_k$ with the right initial value, and by Lemma 1 it is the solution. This is the [variation of constants formula](/variation-of-constants-formula/) for a constant input. $\square$

## Theorem 1: exactness at the samples

For every $k \ge 0$, $x_{k+1} = A_d x_k + B_d u_k$.

*Proof.* Put $\tau = h$ in Lemma 2. $\square$

No approximation enters. The only assumption is on the input: it must be constant on each interval. For any other input the samples satisfy $x_{k+1} = A_d x_k + \int_0^h e^{A(h - s)} B u(kh + s)\, ds$, and the model with $B_d u_k$ is exact only for the held part.

## Theorem 2: the block exponential (Van Loan 1978)

Let $N = n + m$ and

$$M = \begin{bmatrix} A & B \\ 0 & 0 \end{bmatrix} \in \mathbb{R}^{N \times N}.$$

Then for every $\tau$,

$$e^{M\tau} = \begin{bmatrix} e^{A\tau} & \Gamma(\tau) B \\ 0 & I_m \end{bmatrix}.$$

In particular, the top blocks of $e^{Mh}$ are $A_d$ and $B_d$.

*Proof.* Let $E(\tau)$ be the matrix on the right. Both $e^{M\tau}$ and $E(\tau)$ are equal to $I_N$ at $\tau = 0$. The function $e^{M\tau}$ is the unique solution of the linear matrix equation $Y' = M Y$, $Y(0) = I_N$ (Lemma 1 applied to each column). So it is enough to show $E' = M E$. Block by block:

$$E'(\tau) = \begin{bmatrix} A e^{A\tau} & e^{A\tau} B \\ 0 & 0 \end{bmatrix}, \qquad M E(\tau) = \begin{bmatrix} A e^{A\tau} & A \Gamma(\tau) B + B \\ 0 & 0 \end{bmatrix}.$$

The top right blocks agree, because $A \Gamma(\tau) + I = e^{A\tau}$ (proof of Lemma 2). The other blocks agree term by term. $\square$

A second proof uses the series. Induction on $j$ gives $M^j = \begin{bmatrix} A^j & A^{j-1} B \\ 0 & 0 \end{bmatrix}$ for $j \ge 1$. So the top right block of $e^{M\tau}$ is $\sum_{j \ge 1} \frac{\tau^j}{j!} A^{j-1} B$, and term by term integration of $e^{As} = \sum_{i \ge 0} \frac{s^i}{i!} A^i$ gives the same series for $\Gamma(\tau) B$.

## Theorem 3: the implementation returns $(A_d, B_d)$

The function `zoh(A, B, h)` builds $Mh$ (line L1), takes its exponential (line L2), and returns the top left $n \times n$ block (line L3) and the top right $n \times m$ block (line L4).

*Proof.* Line L1 builds the block matrix of Theorem 2 with $A h$ and $B h$ in place of $A$ and $B$, and $\begin{bmatrix} Ah & Bh \\ 0 & 0 \end{bmatrix} = Mh$. Lines L3 and L4 read the blocks of $e^{Mh}$, which are $A_d$ and $B_d$ by Theorem 2. In exact arithmetic the result is exact. In floating point the error is that of the matrix exponential of line L2: the helper `expm` scales $Mh$ by $2^{-s}$ until the infinity norm is at most $1/2$, sums the Taylor series until the next term is below $2^{-60}$ times the norm of the sum, and squares $s$ times. The truncation error of the series is far below the unit roundoff, and the rounding error grows with $s$ and with the norm of $Mh$. $\square$

## Checks used in the tests

- Double integrator, $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$: $M$ is nilpotent with $M^3 = 0$, so $e^{Mh} = I + Mh + M^2 h^2 / 2$, which gives $A_d = \begin{bmatrix} 1 & h \\ 0 & 1 \end{bmatrix}$ and $B_d = \begin{bmatrix} h^2/2 \\ h \end{bmatrix}$.
- Invertible $A$: $\Gamma(h) = A^{-1}(e^{Ah} - I)$, from $A \Gamma(h) = e^{Ah} - I$.
- Semigroup: two steps with period $h$ and the same held input equal one step with period $2h$: $A_d(2h) = A_d(h)^2$ and $B_d(2h) = A_d(h) B_d(h) + B_d(h)$. This follows from Theorem 1 applied to the two intervals.
- Simulation: a fine RK4 run of the plant with the input held over each sampling period agrees with $x_k$ to the RK4 error, which is $O(\mathrm{d}t^4)$.
