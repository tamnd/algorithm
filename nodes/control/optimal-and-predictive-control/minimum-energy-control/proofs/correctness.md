---
title: The Gramian formula gives the unique input of least energy, and Van Loan's block exponential gives the Gramian
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $x_0, x_1 \in \mathbb{R}^n$ and $t_1 > 0$. The inputs are the square integrable functions $u : [0, t_1] \to \mathbb{R}^m$, with the inner product $\langle u, v \rangle = \int_0^{t_1} u(t)^T v(t)\, dt$ and the energy $\|u\|^2 = \langle u, u \rangle$. The solution of $\dot x = A x + B u$, $x(0) = x_0$ at time $t_1$ is

$$x(t_1) = e^{A t_1} x_0 + \mathcal{L} u, \qquad \mathcal{L} u = \int_0^{t_1} e^{A (t_1 - s)} B u(s)\, ds.$$

So $x(t_1) = x_1$ holds if and only if $\mathcal{L} u = d$, with $d = x_1 - e^{A t_1} x_0$. The controllability Gramian is

$$W = \int_0^{t_1} e^{A s} B B^T e^{A^T s}\, ds.$$

## Step 1: the adjoint and the Gramian

For $\eta \in \mathbb{R}^n$ let $(\mathcal{L}^* \eta)(t) = B^T e^{A^T (t_1 - t)} \eta$. Then for every input $u$,

$$\eta^T \mathcal{L} u = \int_0^{t_1} \eta^T e^{A (t_1 - s)} B u(s)\, ds = \langle \mathcal{L}^* \eta, u \rangle,$$

so $\mathcal{L}^*$ is the adjoint of $\mathcal{L}$. Also $\mathcal{L} \mathcal{L}^* \eta = \int_0^{t_1} e^{A (t_1 - s)} B B^T e^{A^T (t_1 - s)} \eta\, ds = W \eta$, by the substitution $\sigma = t_1 - s$.

## Step 2: the formula is optimal when W is invertible

Assume $W$ is invertible and put $\eta = W^{-1} d$ and $u^* = \mathcal{L}^* \eta$, that is $u^*(t) = B^T e^{A^T (t_1 - t)} W^{-1} d$. By Step 1, $\mathcal{L} u^* = W \eta = d$, so $u^*$ reaches $x_1$.

Let $u$ be any input with $\mathcal{L} u = d$, and let $v = u - u^*$. Then $\mathcal{L} v = 0$ and $\langle u^*, v \rangle = \langle \mathcal{L}^* \eta, v \rangle = \eta^T \mathcal{L} v = 0$. Hence

$$\|u\|^2 = \|u^* + v\|^2 = \|u^*\|^2 + 2 \langle u^*, v \rangle + \|v\|^2 = \|u^*\|^2 + \|v\|^2 \ge \|u^*\|^2,$$

with equality only if $\|v\| = 0$, that is, $u = u^*$ almost everywhere. So $u^*$ is the unique input of least energy. Its energy is $\|u^*\|^2 = \langle \mathcal{L}^* \eta, \mathcal{L}^* \eta \rangle = \eta^T \mathcal{L} \mathcal{L}^* \eta = \eta^T W \eta = d^T W^{-1} d$.

## Step 3: when W is singular

$W$ is symmetric and positive semidefinite, since $\eta^T W \eta = \int_0^{t_1} |B^T e^{A^T s} \eta|^2\, ds \ge 0$. If $W$ is singular, take $\eta \ne 0$ with $W \eta = 0$. The integrand is continuous and nonnegative, so $B^T e^{A^T s} \eta = 0$ for all $s \in [0, t_1]$, which means $\mathcal{L}^* \eta = 0$ and $\eta^T \mathcal{L} u = \langle \mathcal{L}^* \eta, u \rangle = 0$ for every input. So every reachable $d$ lies in the hyperplane $\eta^T d = 0$, and a target $x_1$ with $\eta^T (x_1 - e^{A t_1} x_0) \ne 0$ cannot be reached. This is why the code stops with an error when $W$ is not positive definite. ($W$ is singular exactly when $(A, B)$ is not controllable, but this proof does not need that fact.)

## Step 4: Van Loan's block exponential

Let $M = \begin{bmatrix} -A & B B^T \\ 0 & A^T \end{bmatrix}$ and write $e^{M t} = \begin{bmatrix} E(t) & G(t) \\ 0 & F(t) \end{bmatrix}$; the lower left block is 0 because $M$ is block upper triangular. From $\frac{d}{dt} e^{M t} = M e^{M t}$ and $e^{M 0} = I$, the blocks satisfy $\dot F = A^T F$ with $F(0) = I$, so $F(t) = e^{A^T t}$; $\dot E = -A E$ with $E(0) = I$, so $E(t) = e^{-A t}$; and

$$\dot G = -A G + B B^T F = -A G + B B^T e^{A^T t}, \qquad G(0) = 0.$$

By variation of constants, $G(t) = \int_0^t e^{-A (t - s)} B B^T e^{A^T s}\, ds$. Multiply by $e^{A t} = F(t)^T$:

$$F(t)^T G(t) = \int_0^t e^{A s} B B^T e^{A^T s}\, ds = W(t).$$

So the code computes $W(t_1) = F^T G$ from one exponential of $M t_1$, as in line L1. It then makes the result exactly symmetric by averaging with its transpose, which changes nothing in exact arithmetic.

## Theorem

Let $t_1 > 0$ and let $W$ be the Gramian. If $W$ is invertible, then the input $u^*(t) = B^T e^{A^T (t_1 - t)} W^{-1} (x_1 - e^{A t_1} x_0)$ steers $x_0$ to $x_1$ at time $t_1$, every other input that does so has larger energy, and the least energy is $d^T W^{-1} d$. If $W$ is singular, some target cannot be reached. The lines L1 to L6 of the page compute exactly these quantities, in exact arithmetic.

*Proof.* Line L1 computes $W$ by Step 4. Line L2 stops when $W$ is singular, which is right by Step 3. Lines L3 and L4 compute $d$ and $\eta = W^{-1} d$. Line L5 is the input $u^* = \mathcal{L}^* \eta$ and line L6 the energy $d^T \eta$, both optimal by Step 2. $\blacksquare$

## The discrete-time version

For $x_{k+1} = A x_k + B u_k$, the state after $N$ steps is $x_N = A^N x_0 + C u$ with $C = \begin{bmatrix} A^{N-1} B & \cdots & A B & B \end{bmatrix}$ and $u = (u_0, \dots, u_{N-1})$ stacked. The same argument with the Euclidean inner product on $\mathbb{R}^{N m}$, $\mathcal{L} = C$ and $\mathcal{L}^* = C^T$ gives: if $W_N = C C^T = \sum_{j=0}^{N-1} A^j B B^T (A^T)^j$ is invertible, the unique input of least $\sum_k |u_k|^2$ is $u = C^T W_N^{-1} d$ with $d = x_1 - A^N x_0$, that is $u_k = B^T (A^T)^{N-1-k} W_N^{-1} d$, and the least energy is $d^T W_N^{-1} d$. All quantities are rational for rational data, so the function `minimum_energy_discrete` computes them exactly.

## Floating point

The continuous-time code is in floating point. The relative error of the Gramian is that of the exponential of $M t_1$, near $10^{-14}$ when $M t_1$ is not far from normal and has small norm. The solve with $W$ multiplies the error by about the condition number of $W$, which is large when the target is hard to reach (a short horizon $t_1$, or a direction that $B$ excites weakly). The code refuses $W$ when $W - \epsilon I$ is not positive definite, with $\epsilon$ equal to $10^{-12}$ times the largest entry of $W$.
