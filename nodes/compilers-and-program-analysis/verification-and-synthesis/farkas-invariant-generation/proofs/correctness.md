---
title: Constraint-based invariant generation is sound, and complete for the template over the rationals
proves: [correctness]
status: full
---

**Setting.** The states are the points of $\mathbb{Q}^n$. The initial set is $\mathit{Init} = \{x : Px \le p\}$. There are $k$ transitions, and transition $i$ is the relation $\tau_i = \{(x, x') : A_i x + A'_i x' \le t_i\}$. Equalities are written as two inequalities. The template is the inequality $\varphi_{c,d} : c \cdot x + d \le 0$ with unknown $c \in \mathbb{Q}^n$ and $d \in \mathbb{Q}$. The inequality is *inductive over $\mathbb{Q}$* when

- (I) every $x \in \mathit{Init}$ satisfies $c \cdot x + d \le 0$, and
- (C) for every $i$ and every $(x, x') \in \tau_i$ with $c \cdot x + d \le 0$, also $c \cdot x' + d \le 0$.

All multipliers below are row vectors of rationals, and $\lambda \ge 0$ means every entry is nonnegative.

## Lemma 1: affine Farkas lemma

**Claim.** Let $Ay \le b$ be a system over $\mathbb{Q}^m$.

1. If the system has a solution, then every solution satisfies $w \cdot y \le \delta$ if and only if there is $\lambda \ge 0$ with $\lambda A = w$ and $\lambda b \le \delta$.
2. The system has no solution if and only if there is $\lambda \ge 0$ with $\lambda A = 0$ and $\lambda b < 0$.

**Proof.** The "if" parts are one line each. In part 1, a solution $y$ gives $w \cdot y = \lambda A y \le \lambda b \le \delta$, because $\lambda \ge 0$ and $Ay \le b$. In part 2, a solution $y$ would give $0 = \lambda A y \le \lambda b < 0$, which is false.

For the "only if" parts, use the duality theorem of linear programming, see [the dual linear program](/dual-linear-program/). The primal problem is to maximize $w \cdot y$ subject to $Ay \le b$, with $y$ free. Its dual is to minimize $\lambda b$ subject to $\lambda A = w$ and $\lambda \ge 0$. Part 1: the primal is feasible and its values are bounded above by $\delta$, so it has an optimum $v \le \delta$, and the dual has an optimal $\lambda$ with $\lambda b = v \le \delta$. Part 2: take $w = 0$. The dual is feasible, with $\lambda = 0$, and the primal is infeasible, so the dual is unbounded below, and some feasible $\lambda$ has $\lambda b < 0$. In both parts the data are rational and the simplex method finds an optimal or unbounded basic solution, so $\lambda$ can be taken rational. This is the form of [Farkas' lemma](/farkas-lemma/) that Colon, Sankaranarayanan and Sipma state as their Theorem 1. $\square$

## Lemma 2: the exact conditions

Assume $\mathit{Init}$ is not empty and no $\tau_i$ is empty. For transition $i$ let $S_i = \{(x, x') \in \tau_i : c \cdot x + d \le 0\}$.

**Claim.** $\varphi_{c,d}$ is inductive over $\mathbb{Q}$ if and only if

- (I') there is $\lambda_0 \ge 0$ with $\lambda_0 P = c$ and $\lambda_0 p \le -d$, and
- (C') for each $i$, one of the two cases holds:
  - **cons with $\mu$:** there are $\mu \ge 0$ and $\lambda \ge 0$ with $\mu c + \lambda A_i = 0$, $\lambda A'_i = c$ and $\lambda t_i \le (\mu - 1) d$;
  - **dis:** there is $\lambda \ge 0$ with $c + \lambda A_i = 0$, $\lambda A'_i = 0$ and $\lambda t_i - d < 0$.

**Proof.** (I) and (I'): $\mathit{Init}$ is the solution set of $Px \le p$, it is not empty, and (I) says that every solution satisfies $c \cdot x \le -d$. By Lemma 1, part 1, this holds if and only if (I') holds.

(C) and (C') for one transition $i$. $S_i$ is the solution set of the system with the rows $c \cdot x \le -d$ and $A_i x + A'_i x' \le t_i$ over the unknowns $(x, x')$. Give the first row the multiplier $\mu$ and the other rows the multipliers $\lambda$.

- Suppose $S_i$ is not empty. Condition (C) for $i$ says that every point of $S_i$ satisfies $c \cdot x' \le -d$, that is, $0 \cdot x + c \cdot x' \le -d$. By Lemma 1, part 1, this holds if and only if there are $\mu, \lambda \ge 0$ with $\mu c + \lambda A_i = 0$ on the $x$ part, $\lambda A'_i = c$ on the $x'$ part, and $-\mu d + \lambda t_i \le -d$. The last inequality is $\lambda t_i \le (\mu - 1) d$. This is the case cons with $\mu$.
- Suppose $S_i$ is empty. Then (C) holds for $i$ with nothing to check. By Lemma 1, part 2, there are $\mu, \lambda \ge 0$ with $\mu c + \lambda A_i = 0$, $\lambda A'_i = 0$ and $-\mu d + \lambda t_i < 0$. If $\mu = 0$, these say $\lambda [A_i \; A'_i] = 0$ and $\lambda t_i < 0$, so $\tau_i$ is empty by Lemma 1, part 2, against the assumption. So $\mu > 0$. Divide $\mu$ and $\lambda$ by $\mu$; the equalities stay true and the strict inequality keeps its sign. This is the case dis.

Conversely, if the case cons holds for $i$, the "if" part of Lemma 1, part 1, gives (C) for $i$ directly: for $(x, x') \in S_i$, $c \cdot x' = \lambda A'_i x' = \lambda (A_i x + A'_i x') - \lambda A_i x \le \lambda t_i + \mu c \cdot x \le (\mu - 1) d - \mu d = -d$, where the step $\mu c \cdot x \le -\mu d$ uses $\mu \ge 0$. If the case dis holds for $i$, then for $(x, x') \in S_i$, $0 = (c + \lambda A_i) x + \lambda A'_i x' = c \cdot x + \lambda (A_i x + A'_i x') \le -d + \lambda t_i < 0$, which is false, so $S_i$ is empty and (C) holds for $i$. $\square$

The case cons is nonlinear in the unknowns, because of the product $\mu c$. Once $\mu$ is a fixed number, all the conditions of Lemma 2 are linear in $c$, $d$ and the multipliers. The case dis needs only $\mu = 1$, by the proof above; only the consecution multiplier $\mu$ of the case cons is a real restriction.

## The algorithm

The algorithm gets a finite set $M$ of nonnegative rationals, the allowed values of $\mu$, and a point $x_{\mathrm{bad}}$. It first returns the inequality $1 \le 0$ (that is, $c = 0$, $d = 1$) if $\mathit{Init}$ is empty, and drops every empty $\tau_i$; both checks are linear programs. Then, for each choice of one case per remaining transition, cons with some $\mu \in M$ or dis, it builds the linear system $L$ of (I'), of the chosen cases, with the strict inequality of dis written as $\lambda t_i - d \le -1$, and of the target row $c \cdot x_{\mathrm{bad}} + d \ge 1$. It returns $(c, d)$ from the first $L$ that has a solution, and "none" if no $L$ has one. The linear programs are solved exactly over $\mathbb{Q}$.

## Theorem 1: soundness

**Claim.** If the algorithm returns $(c, d)$, then $\varphi_{c,d}$ is inductive over $\mathbb{Q}$ and $c \cdot x_{\mathrm{bad}} + d > 0$. Hence $\varphi_{c,d}$ holds in every state that a run reaches, over the rationals and over the integers, and $x_{\mathrm{bad}}$ is not reachable.

**Proof.** If $\mathit{Init}$ is empty, the answer is $1 \le 0$: (I) holds because there is no initial state, (C) holds because no state satisfies $1 \le 0$, and $x_{\mathrm{bad}}$ violates it. An empty $\tau_i$ satisfies (C) with nothing to check, so dropping it changes nothing. Otherwise the solution of $L$ satisfies (I'), and for each remaining transition the chosen case of (C'); the row $\lambda t_i - d \le -1$ implies $\lambda t_i - d < 0$. By the "if" direction of Lemma 2, $\varphi_{c,d}$ is inductive over $\mathbb{Q}$. The target row gives $c \cdot x_{\mathrm{bad}} + d \ge 1 > 0$. Normalizing $(c, d)$ to coprime integers multiplies it by a positive number, which changes none of this.

Every reachable state satisfies $\varphi_{c,d}$ by [induction](/induction/) on the length of the run: the first state by (I), and each step by (C). An integer program is the same system with states in $\mathbb{Z}^n \subseteq \mathbb{Q}^n$; its initial states and its steps are among the rational ones, so (I) and (C) hold for it too. $\square$

## Theorem 2: completeness relative to $M$

**Claim.** Suppose $\mathit{Init}$ is not empty and some inequality $\varphi_{c,d}$ is inductive over $\mathbb{Q}$, false at $x_{\mathrm{bad}}$, and has, for every nonempty transition $i$ with $S_i$ not empty, a cons multiplier $\mu_i \in M$. Then the algorithm does not return "none".

**Proof.** Drop the empty transitions; the inequality is still inductive for the rest. By Lemma 2 there are multipliers for (I') and, for each remaining $i$, for the case cons with $\mu_i$ when $S_i$ is not empty, and for the case dis when $S_i$ is empty. Let $v = c \cdot x_{\mathrm{bad}} + d > 0$ and, over the dis transitions, $\varepsilon = \min_i (d - \lambda_i t_i) > 0$, with $\varepsilon = 1$ if there are none. Let $s = \max(1/v, 1/\varepsilon) > 0$, and multiply $c$, $d$ and every $\lambda$ by $s$, but not the $\mu_i$. Every equality of (I') and of the cases is homogeneous in $(c, d, \lambda)$ once $\mu_i$ is fixed, and so are the inequalities $\lambda_0 p \le -d$ and $\lambda t_i \le (\mu_i - 1) d$; they stay true. The dis rows become $s(\lambda_i t_i - d) \le -s \varepsilon \le -1$, and the target becomes $s v \ge 1$. So the system $L$ of this choice of cases has a solution. The algorithm tries every choice of cases, so it stops at this choice or at an earlier one, and the exact solver finds the solution. $\square$

## Corollary: exactness over the rationals

With $\mu$ left as an unknown, the conditions of Lemma 2 describe exactly the inductive inequalities over $\mathbb{Q}$ of the template; this is Theorem 2 of Colon, Sankaranarayanan and Sipma. So the method with $M = \mathbb{Q}_{\ge 0}$, which needs a solver for the nonlinear products $\mu c$, finds an inductive inequality false at $x_{\mathrm{bad}}$ whenever one exists. With a finite $M$ it is complete for the inequalities whose consecution multipliers lie in $M$, and no more: for $x := 1$ followed by the loop $x := 2x$, the inequalities $x \ge 0$ and $x \ge 1$ are inductive, but every certificate of consecution has $\mu = 2$, because $\lambda A'_i = c$ and $\mu c + \lambda A_i = 0$ force $\mu c = 2c$. The tests check this case with $M = \{0, 1\}$ and with $M = \{0, 1, 2\}$.

## What completeness does not give

The result is about inductive inequalities over $\mathbb{Q}$. An inequality can be inductive over $\mathbb{Z}$ but not over $\mathbb{Q}$. For $x := 0$ followed by the loop $\mathbf{while}\ 2x \le 1\ \mathbf{do}\ x := 2x + 1$, the reachable states are $0$ and $1$, and $x \le 1$ is inductive over $\mathbb{Z}$, since an integer with $2x \le 1$ has $x \le 0$. Over $\mathbb{Q}$, the state $x = 1/2$ satisfies $x \le 1$ and the guard and goes to $2$. Every rational inductive inequality $c x + d \le 0$ holds at $0$ and $1$, hence at $1/2$ by convexity, hence at $2$ by consecution. So no rational inductive inequality excludes $x = 2$, and the algorithm correctly returns "none" for it. Replacing the guard by its [integer hull](/integer-hull/) $x \le 0$ restores the integer invariant. $\blacksquare$
