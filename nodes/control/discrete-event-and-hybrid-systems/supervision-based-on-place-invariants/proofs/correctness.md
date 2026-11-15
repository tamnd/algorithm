---
title: The monitor places enforce L mu <= b, and they block only the firings that would break it
proves: [correctness]
status: full
---

Let the plant be a Petri net with $n$ places and $q$ transitions, with nonnegative integer matrices $\mathrm{Pre}, \mathrm{Post} \in \mathbb{N}^{n \times q}$ and incidence matrix $D = \mathrm{Post} - \mathrm{Pre}$. A marking is $\mu \in \mathbb{N}^n$. Transition $t$ is enabled at $\mu$ if $\mu \ge \mathrm{Pre}_{\cdot t}$ (entrywise), and firing it gives $\mu' = \mu + D_{\cdot t}$. The specification is $L \mu \le b$ with $L \in \mathbb{Z}^{c \times n}$ and $b \in \mathbb{Z}^c$, and the initial marking $\mu_0$ satisfies $L \mu_0 \le b$.

The algorithm adds $c$ monitor places with incidence $D_c = -L D$, arcs $\mathrm{Pre}_c = \max(0, -D_c)$ and $\mathrm{Post}_c = \max(0, D_c)$ (entrywise), and initial marking $\mu_{c,0} = b - L \mu_0$. The closed loop is the net with places $(\mu, \mu_c)$ and the matrices $\mathrm{Pre}$ and $\mathrm{Post}$ stacked on $\mathrm{Pre}_c$ and $\mathrm{Post}_c$.

Note that $\mathrm{Post}_c - \mathrm{Pre}_c = D_c$, because $\max(0, x) - \max(0, -x) = x$ for every integer $x$, and that no monitor place has both an input arc and an output arc with the same transition.

## Lemma 1: the place invariant

Every marking $(\mu, \mu_c)$ that is reachable in the closed loop satisfies $L \mu + \mu_c = b$.

*Proof.* By induction on the length of the firing sequence. At the start, $L \mu_0 + \mu_{c,0} = L \mu_0 + b - L \mu_0 = b$. If $t$ fires at $(\mu, \mu_c)$, the new marking is $(\mu + D_{\cdot t}, \mu_c + (D_c)_{\cdot t})$, and

$$L(\mu + D_{\cdot t}) + \mu_c + (D_c)_{\cdot t} = L \mu + \mu_c + L D_{\cdot t} - L D_{\cdot t} = b. \qquad \square$$

In the terms of the [petri-net](/petri-net/) page, the vector $y = (L_j, e_j)$ is a place invariant of the closed loop for each row $j$: $y^T [D; D_c] = L_j D - L_j D = 0$.

## Lemma 2: the constraint holds

Every reachable closed-loop marking satisfies $L \mu \le b$.

*Proof.* Markings of a Petri net are nonnegative, so $\mu_c \ge 0$, and Lemma 1 gives $L \mu = b - \mu_c \le b$. $\square$

## Lemma 3: the enabling rule of the closed loop

Let $(\mu, \mu_c)$ be reachable in the closed loop. Then $t$ is enabled in the closed loop if and only if $t$ is enabled at $\mu$ in the plant and $L(\mu + D_{\cdot t}) \le b$.

*Proof.* In the closed loop, $t$ is enabled if and only if $\mu \ge \mathrm{Pre}_{\cdot t}$ and $\mu_c \ge (\mathrm{Pre}_c)_{\cdot t}$. The first condition is plant enabling. Take one monitor $j$ and write $d = (D_c)_{jt} = -L_j D_{\cdot t}$.

- If $d < 0$, the monitor condition is $\mu_{c,j} \ge -d$, that is $\mu_{c,j} + d \ge 0$. By Lemma 1, $\mu_{c,j} = b_j - L_j \mu$, so the condition is $b_j - L_j \mu - L_j D_{\cdot t} \ge 0$, that is $L_j(\mu + D_{\cdot t}) \le b_j$.
- If $d \ge 0$, there is no arc from monitor $j$ to $t$, so the monitor condition always holds. The constraint also holds: $L_j(\mu + D_{\cdot t}) = L_j \mu - d \le L_j \mu \le b_j$ by Lemma 2.

So in both cases the condition of monitor $j$ is equivalent to $L_j(\mu + D_{\cdot t}) \le b_j$, and the claim follows by taking all $j$. $\square$

## Theorem: maximal permissiveness

Let $R$ be the set of plant markings that can be reached from $\mu_0$ by a firing sequence whose markings all satisfy $L \mu \le b$ (the legal reachable set). Then the projection of the closed-loop reachable set on the plant places is exactly $R$. More strongly, a firing sequence $\sigma$ can fire in the closed loop if and only if it can fire in the plant and every marking along it satisfies $L \mu \le b$.

*Proof.* By induction on the length of $\sigma$, with the claim that after $\sigma$ the closed loop is at $(\mu, b - L\mu)$, where $\mu$ is the plant marking after $\sigma$. The empty sequence is the base case. For the step, let $\sigma$ satisfy the claim and add $t$. By Lemma 3, $t$ fires in the closed loop after $\sigma$ if and only if it fires in the plant and the new plant marking satisfies the constraint. The new plant part is $\mu + D_{\cdot t}$ in both nets, and Lemma 1 fixes the monitor part as $b - L(\mu + D_{\cdot t})$. $\square$

Any supervisor that observes and can disable all transitions and enforces $L \mu \le b$ must disable $t$ at every reachable $\mu$ with $L(\mu + D_{\cdot t}) \not\le b$. By Lemma 3 the monitors disable exactly these firings and no other. So no supervisor of this kind allows a larger set of sequences: the monitor solution is maximally permissive.

## Uncontrollable and unobservable transitions

Suppose some transitions are uncontrollable (the supervisor cannot disable them) or unobservable (the supervisor does not see them fire).

- If $(L D)_{\cdot t} \le 0$, then $(D_c)_{\cdot t} \ge 0$, so $(\mathrm{Pre}_c)_{\cdot t} = 0$. No monitor arc leads into $t$, so the monitors never disable $t$, and they may treat it as uncontrollable.
- If $(L D)_{\cdot t} = 0$, then $(D_c)_{\cdot t} = 0$, so no monitor arc touches $t$. The monitor marking does not depend on whether $t$ fired, and $t$ may be unobservable.

These are the sufficient conditions of Moody and Antsaklis (1998). When they fail, the monitor built from $(L, b)$ is not admissible. A common repair is to replace the constraint by a stricter one $L' \mu \le b'$ that implies $L \mu \le b$ on the reachable markings and meets the conditions; the result may then be less permissive than the best admissible supervisor.

## Termination and cost

The algorithm has no loop with a data-dependent bound. Line L1 takes $nq$ subtractions. Line L2 computes the $c \times q$ matrix $-L D$ with $c n q$ multiplications and additions. Line L3 takes $c n$ operations, and lines L4 and L5 take $c$ and $c q$ operations. The total is $O(c n q)$ word operations, with integers that fit in a word when the entries of $L$, $b$, $D$ and $\mu_0$ are bounded by a constant. The output has $2 c q + c$ integers.
