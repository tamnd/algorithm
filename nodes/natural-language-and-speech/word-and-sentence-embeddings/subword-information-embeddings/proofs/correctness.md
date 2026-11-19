---
title: The subword skip-gram lists the right n-grams, takes exact gradient steps and gives every nonempty word a vector
proves: [correctness]
status: full
---

The training minimizes a nonconvex loss by stochastic gradient descent, so there is no claim of a global optimum. We prove what each line computes: the rows of a word (line L1), the gradient used in a training step (lines L3 to L8), and the existence of the output vector (line L9).

**Notation.** For a word $w$ of $m \ge 0$ characters, let $s = $ "<" $w$ ">", a string of length $m + 2$. Let $V$ be the vocabulary, with words numbered $0$ to $|V| - 1$, and $B \ge 1$ the number of buckets. The row list $\mathcal{G}_w$ is the own row of $w$ if $w \in V$, followed by $|V| + (h(g) \bmod B)$ for each n-gram $g$ in the order of line L1, where $h$ is the hash. The vector of $w$ is $\vec h_w = \sum_{r \in \mathcal{G}_w} \vec z_r$, a sum over the list, so a row that occurs twice counts twice.

## Claim 1. Line L1 lists each n-gram occurrence once and maps it to a bucket row.

The loop takes each start position $i = 0, \ldots, m + 1$ and each length $n = n_{\min}, \ldots, n_{\max}$ with $i + n \le m + 2$, and emits $s[i, i + n)$. A substring occurrence of $s$ is fixed by its start and its length, so each occurrence of length $n_{\min}$ to $n_{\max}$ is emitted exactly once. For a fixed $n$, the starts are $0, \ldots, m + 2 - n$, so there are $\max(0, m + 3 - n)$ of them, and the total is $\sum_{n = n_{\min}}^{n_{\max}} \max(0, m + 3 - n)$. For "where" ($m = 5$) and $n$ from 3 to 6 this is $5 + 4 + 3 + 2 = 14$.

The hash $h(g)$ is a nonnegative integer, so $h(g) \bmod B \in \{0, \ldots, B - 1\}$, and the row $|V| + (h(g) \bmod B)$ lies in $[|V|, |V| + B)$. These rows are disjoint from the own rows $0, \ldots, |V| - 1$, so an n-gram never shares a row with a whole word. $\square$

## Claim 2. Lines L3 to L8 take an exact gradient step of the pair loss.

Fix a pair $(w, c)$ with noise words $n_1, \ldots, n_k$, and write $x_0 = c$, $y_0 = 1$, and $x_i = n_i$, $y_i = 0$. The loss is

$$\ell = \sum_{i=0}^{k} \Big(-y_i \log\sigma(\vec h_w \cdot \vec v_{x_i}) - (1 - y_i)\log\sigma(-\vec h_w \cdot \vec v_{x_i})\Big).$$

For one term with $t = \vec h_w \cdot \vec v_x$, the derivative of $-\log\sigma(t)$ is $\sigma(t) - 1$ and that of $-\log\sigma(-t)$ is $\sigma(t)$. Both are $e = \sigma(t) - y$, which line L6 computes. By the chain rule,

$$\frac{\partial \ell}{\partial \vec v_x} = \sum_{i : x_i = x} e_i\, \vec h_w, \qquad \frac{\partial \ell}{\partial \vec h_w} = \sum_{i=0}^{k} e_i\, \vec v_{x_i} = \vec g_h.$$

Line L7 accumulates $\vec g_h$ from the values of $\vec v_{x_i}$ before their own update, and moves $\vec v_{x_i}$ by $-\eta e_i \vec h_w$. A noise word that appears twice is moved twice, which matches the sum over $i$ with $x_i = x$.

The loss depends on the rows only through $\vec h_w = \sum_{r \in \mathcal{G}_w} \vec z_r$. If row $r$ occurs $\mu_r$ times in the list, then $\partial \vec h_w / \partial \vec z_r = \mu_r I$, so $\partial \ell / \partial \vec z_r = \mu_r \vec g_h$. Line L8 runs over the list and subtracts $\eta \vec g_h$ once per occurrence, that is $\eta \mu_r \vec g_h$ in total. All of $\vec g_h$, $e_i$ and $\vec h_w$ are computed at the parameters before the step, so the step is $-\eta \nabla \ell$ in the context vectors and the rows of $Z$, and every other parameter has zero gradient and does not move.

For a small enough $\eta$, such a step lowers $\ell$ unless $\nabla \ell = 0$, because $\ell(\theta - \eta\nabla\ell) = \ell(\theta) - \eta\|\nabla\ell\|^2 + o(\eta)$ for the differentiable $\ell$. $\square$

## Claim 3. Every word with at least one character has a vector, and the vector of a seen word includes its own row.

Assume $n_{\min} \le 3 \le n_{\max}$, as in the paper. If $m \ge 1$, then $s$ has length at least 3, so the start $0$ with the length $n_{\min}$ is emitted, and $\mathcal{G}_w$ has at least one row whether $w \in V$ or not. Line L9 returns the sum over a nonempty list. If $w \in V$, the list starts with its own row by definition, so the vector of a seen word is its own row plus its n-gram rows. For $m = 0$ the string "<>" has length 2, and with $n_{\min} = 3$ it has no n-gram, so the empty word outside the vocabulary gets the zero vector. $\square$

With $n_{\min} > n_{\max}$, Claim 1 gives no n-grams, the list of a vocabulary word is its own row, $\vec h_w = \vec z_w$, and Claim 2 reduces to the negative sampling step of the skip-gram model. $\blacksquare$
