---
title: Stickel's algorithm returns a complete set of AC-unifiers for elementary AC unification with constants
proves: [correctness]
status: full
---

We use the notation of the page. There is one AC symbol $+$. The inputs $s$ and $t$ are sums of variables and free constants. A term that is not a sum is an **atom**. Modulo AC, a term is determined by the multiset of its atoms, so $u =_{AC} u'$ if and only if the two multisets of atoms are equal. We write $|u|_w$ for the number of times the atom $w$ occurs in $u$. A substitution maps each variable to a nonempty sum, since there is no unit element.

## Step 1: cancellation

L1 removes the arguments that occur on both sides, with their common multiplicity. For every substitution $\theta$, $(s' + r)\theta =_{AC} (t' + r)\theta$ if and only if $s'\theta =_{AC} t'\theta$, because the multiset of atoms of $(s' + r)\theta$ is the multiset sum of those of $s'\theta$ and $r\theta$, and multiset sum can be cancelled. So cancellation keeps the set of unifiers.

After cancellation, if both sides are empty, every substitution is a unifier, and the identity is the most general one (L2). If exactly one side is empty, there is no unifier, because the other side becomes a nonempty sum. So assume both sides are nonempty. Each argument now occurs on one side only. The distinct arguments are the **columns**: $c_1, \ldots, c_p$ on the left with multiplicities $a_1, \ldots, a_p$, and $d_1, \ldots, d_q$ on the right with multiplicities $b_1, \ldots, b_q$.

## Step 2: the Diophantine equation

Let $S$ be the set of vectors $v \in \mathbb{N}^{p+q}$ with

$$L(v) = \sum_i a_i v(c_i) = \sum_j b_j v(d_j) = R(v).$$

$S$ is closed under addition. A nonzero $v \in S$ is **minimal** if no nonzero $w \in S$ with $w \ne v$ has $w \le v$ in every coordinate. Let $B = \{v_1, \ldots, v_r\}$ be the set of minimal vectors (L4).

**Lemma 1.** $B$ is finite, and every $v \in S$ is a sum of elements of $B$, with repetitions allowed.

*Proof.* $B$ is an antichain under the coordinatewise order on $\mathbb{N}^{p+q}$, so it is finite by Dickson's lemma. For the second claim, use induction on the sum of the coordinates of $v$. If $v = 0$, it is the empty sum. Otherwise there is a minimal $w \le v$ with $w \in S$ nonzero (take a nonzero element of $S$ below $v$ with the smallest coordinate sum). Then $v - w \ge 0$ and $L(v - w) = L(v) - L(w) = R(v) - R(w) = R(v - w)$, so $v - w \in S$ with a smaller sum, and the induction hypothesis applies. $\square$

Each $v_k$ gets a new variable $z_k$ that does not occur in $s$ or $t$.

## Step 3: soundness

Fix a subset $K \subseteq B$ that passes L7, L8 and L10. For $k \in K$, let $w_k$ be the constant assigned to $z_k$ at L9 if there is one, and $w_k = z_k$ otherwise. L11 defines $\sigma(x) = \sum_{k \in K} v_k(x) \cdot w_k$ for each variable column $x$. This sum is nonempty, because column $x$ has a positive sum over $K$ (L7).

Consider a constant column $c$. By L8 there is exactly one $k_c \in K$ with $v_{k_c}(c) > 0$, and $v_{k_c}(c) = 1$. By L9 and L10, $w_{k_c} = c$. So for a constant column, $c = \sum_{k \in K} v_k(c) \cdot w_k$ as multisets.

Now the multiset of atoms of $s\sigma$ is

$$\sum_i a_i \sum_{k \in K} v_k(c_i)\, w_k = \sum_{k \in K} L(v_k)\, w_k,$$

using the formula for $\sigma(x)$ at variable columns and the identity above at constant columns. In the same way, $t\sigma$ has the multiset $\sum_{k \in K} R(v_k)\, w_k$. Since $L(v_k) = R(v_k)$ for every $k$, $s\sigma =_{AC} t\sigma$. So every element of the output is an AC-unifier.

## Step 4: completeness

Let $\theta$ be an AC-unifier of $s$ and $t$. Let $X = \mathrm{Var}(s, t)$. We find an output $\sigma$ and a substitution $\lambda$ with $x\sigma\lambda =_{AC} x\theta$ for each $x \in X$. By Step 1, $\theta$ also unifies the two sides after cancellation. A variable of $X$ that is not a column is not bound by $\sigma$, and we set $\lambda(x) = x\theta$ for it. So it is enough to treat the variable columns.

For each atom $u$ that occurs in some $x\theta$, or that is one of the constant columns, define the vector $v^u$ by $v^u(x) = |x\theta|_u$ for a variable column $x$ and $v^u(c) = 1$ if $u = c$, and $0$ otherwise, for a constant column $c$. Then $L(v^u)$ is the number of occurrences of $u$ in $s\theta$, and $R(v^u)$ is the number in $t\theta$. These are equal, because $s\theta =_{AC} t\theta$. So $v^u \in S$, and it is nonzero. By Lemma 1, write

$$v^u = \sum_k m_{u,k}\, v_k, \qquad m_{u,k} \in \mathbb{N}.$$

Let $K = \{k : m_{u,k} > 0 \text{ for some } u\}$.

- *L7 passes.* A variable column $x$ has a nonempty $x\theta$, so some atom $u$ has $v^u(x) > 0$, and then some $k$ with $m_{u,k} > 0$ has $v_k(x) > 0$. A constant column $c$ has $v^c(c) = 1$, and the same argument applies.
- *L8 and L10 pass.* Fix a constant column $c$. For $u \ne c$, $v^u(c) = 0$, so every $k$ with $m_{u,k} > 0$ has $v_k(c) = 0$. For $u = c$, $1 = v^c(c) = \sum_k m_{c,k} v_k(c)$, so exactly one $k$ with $m_{c,k} > 0$ has $v_k(c) > 0$, and for it $m_{c,k} = 1$ and $v_k(c) = 1$. So over $K$ the column $c$ has the sum 1, and the vector $v_k$ with $v_k(c) = 1$ is used only by the atom $c$. If this $v_k$ were also positive at another constant column $c'$, then $v^c(c') > 0$, which is false. So $z_k$ gets only the constant $c$.

So $K$ produces an output $\sigma$. Define $\lambda(z_k) = \sum_u m_{u,k} \cdot u$ for each $k \in K$ with $w_k = z_k$. This is a nonempty sum because $k \in K$. For $k$ with $w_k = c$, only the atom $c$ uses $k$, with $m_{c,k} = 1$, so $w_k = \sum_u m_{u,k} \cdot u$ as well. Then for each variable column $x$,

$$x\sigma\lambda = \sum_{k \in K} v_k(x) \sum_u m_{u,k}\, u = \sum_u \Big(\sum_k m_{u,k} v_k(x)\Big) u = \sum_u v^u(x)\, u = x\theta$$

as multisets of atoms. So $\sigma \le_{AC}^X \theta$.

## Termination

$B$ is finite by Lemma 1, so L6 runs over finitely many subsets, and each step of the loop is finite. The implementation finds $B$ by searching the box $v(c_i) \le \max_j b_j$, $v(d_j) \le \max_i a_i$, which contains every minimal solution by Huet's bound (1978). $\blacksquare$
