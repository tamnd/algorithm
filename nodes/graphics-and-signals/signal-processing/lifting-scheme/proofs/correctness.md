---
title: Correctness of the lifting scheme
proves: [correctness]
status: full
---

We prove three facts: LIFT-INVERSE undoes LIFT-FORWARD for every step list, including rounded steps; the 5/3 step list computes the 5/3 analysis filters; and a composition of lifting steps computes the filter bank whose polyphase matrix is the product of the step matrices.

## Notation

Let $h \ge 1$ and work with pairs $(s, d)$ of vectors of length $h$, indexed modulo $h$. For a finite set of taps $c$, let $(c \star v)[i] = \sum_k c_k\, v[(i + k) \bmod h]$. A P step with taps $c$ and a function $r$ (the identity, or a rounding) is the map

$$P_{c,r}(s, d) = (s,\ d + r(c \star s)),$$

where $r$ acts on each entry. A U step is $U_{c,r}(s, d) = (s + r(c \star d),\ d)$. Lines L3 to L6 with $\sigma = +1$ compute one of these maps, because line L5 reads only `src`, which is not written during the step.

## Lemma 1 (each step is invertible)

Let $P^{-}_{c,r}(s, d) = (s,\ d - r(c \star s))$. Then $P^{-}_{c,r}(P_{c,r}(s, d)) = (s, d)$ for all $(s, d)$, and the same holds for U steps.

*Proof.* $P_{c,r}(s, d) = (s, d')$ with $d' = d + r(c \star s)$. The first component is still $s$, so $P^{-}_{c,r}$ computes $r(c \star s)$ from the same vector and returns $(s,\ d' - r(c \star s)) = (s, d)$. The U case swaps the roles of $s$ and $d$. $\square$

Nothing is assumed about $r$. It may be a rounding, or any function of the half that the step does not write.

## Theorem 1 (exact inverse)

Let the steps be $E_1, \ldots, E_n$ and the scale factors $K_s, K_d \ne 0$. LIFT-FORWARD computes $D \circ E_n \circ \cdots \circ E_1 \circ \Pi$, where $\Pi$ splits $x$ into its even and odd places and $D$ scales the halves. LIFT-INVERSE computes $\Pi^{-1} \circ E_1^{-} \circ \cdots \circ E_n^{-} \circ D^{-1}$. Their composition is the identity.

*Proof.* Line L8 applies $D^{-1}$, which cancels line L7. The loop of line L9 runs the inverse steps in reverse order. By induction on $j$ from $n$ down to $1$: before the inverse of $E_j$ runs, the state is $E_j \circ \cdots \circ E_1 (\Pi x)$, and by Lemma 1 after it the state is $E_{j-1} \circ \cdots \circ E_1(\Pi x)$. After $j = 1$ the state is $\Pi x$, and line L11 interleaves it back into $x$. $\square$

With rounding in each step and $K_s = K_d = 1$, every intermediate value is an integer when $x$ is, so the integer transform maps integers to integers and back.

## Theorem 2 (the 5/3 steps compute the 5/3 filters)

With the steps P: $c_0 = c_1 = -\tfrac12$ and U: $c_{-1} = c_0 = \tfrac14$, no rounding and no scaling, the output is

$$d[i] = \sum_l \tilde g[l]\, x[(2i + l) \bmod N], \qquad s[i] = \sum_l \tilde h[l]\, x[(2i + l) \bmod N],$$

with $\tilde g = (-\tfrac12, 1, -\tfrac12)$ at $l = 0, 1, 2$ and $\tilde h = (-\tfrac18, \tfrac14, \tfrac34, \tfrac14, -\tfrac18)$ at $l = -2, \ldots, 2$.

*Proof.* Before the steps, $s[i] = x[2i]$ and $d[i] = x[2i + 1]$. The P step gives

$$d[i] = x[2i+1] - \tfrac12 x[2i] - \tfrac12 x[2i+2],$$

which is the $\tilde g$ sum. Indices of $s$ wrap modulo $h$ and indices of $x$ modulo $N = 2h$, and $s[(i+1) \bmod h] = x[(2i + 2) \bmod N]$, so the wrap agrees. The U step gives

$$s[i] = x[2i] + \tfrac14\big(x[2i-1] - \tfrac12 x[2i-2] - \tfrac12 x[2i]\big) + \tfrac14\big(x[2i+1] - \tfrac12 x[2i] - \tfrac12 x[2i+2]\big),$$

and collecting terms gives $-\tfrac18 x[2i-2] + \tfrac14 x[2i-1] + (1 - \tfrac18 - \tfrac18) x[2i] + \tfrac14 x[2i+1] - \tfrac18 x[2i+2]$, which is the $\tilde h$ sum. When $h$ is small, several of these indices are the same place, and both sides add the coefficients of that place, so the identity still holds. $\square$

## Theorem 3 (composition in polyphase form)

For a vector $v$ indexed by $\mathbb Z$ with finite support, let $V(z) = \sum_i v[i] z^{-i}$, and for taps $c$ let $C(z) = \sum_k c_k z^{k}$. Then the sequence $c \star v$ has the transform $C(z) V(z)$. So on the transforms of the halves, a P step is multiplication of the column $(S, D)^{\mathsf T}$ by $\begin{pmatrix} 1 & 0 \\ C & 1 \end{pmatrix}$, a U step by $\begin{pmatrix} 1 & C \\ 0 & 1 \end{pmatrix}$, and the scaling by $\operatorname{diag}(K_s, K_d)$. The whole level is multiplication by the product of these matrices, in the order of the steps from right to left.

*Proof.* $\sum_i (c \star v)[i] z^{-i} = \sum_k c_k \sum_i v[i+k] z^{-i} = \sum_k c_k z^{k} \sum_j v[j] z^{-j} = C(z) V(z)$, with $j = i + k$. A P step replaces $D$ by $D + C S$ and keeps $S$, which is the stated matrix, and a U step is the same with the halves swapped. The composition of linear maps is the product of their matrices. $\square$

For the periodic signals of the algorithm, the same identities hold with $z^h = 1$. The product matrix is the polyphase matrix of the analysis filters: the entries of its first row are built from the even-indexed and the odd-indexed taps of $\tilde h$, and those of its second row from the taps of $\tilde g$. This is how the theorem of Daubechies and Sweldens (1998) is used in the other direction: a factorization of the polyphase matrix of a filter bank into such triangular matrices and a diagonal gives a step list that computes that filter bank.
