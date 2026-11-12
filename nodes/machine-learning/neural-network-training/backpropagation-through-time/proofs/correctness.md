---
title: Backpropagation through time returns the gradient of the sequence loss
proves: [correctness, termination]
status: full
---

We use the pseudocode BPTT of the page. The network is $h_t = \tanh(a_t)$ with $a_t = W h_{t-1} + U x_t + b$, and $o_t = V h_t + c$, for $t = 1, \ldots, T$. The loss is $L = \sum_{t=1}^{T} \ell_t$ with $\ell_t = \frac12 \lVert o_t - y_t \rVert^2$. The inputs $x_t$, the targets $y_t$ and the initial state $h_0$ are fixed.

**The unrolled graph.** Give each step its own copies $W^{(t)}, U^{(t)}, b^{(t)}, V^{(t)}, c^{(t)}$ of the parameters, and let $\tilde L$ be the loss as a function of all the copies. The original loss is $L(\theta) = \tilde L(\theta, \theta, \ldots, \theta)$. By the chain rule for this composition with the diagonal map,

$$\frac{\partial L}{\partial W} = \sum_{t=1}^{T} \frac{\partial \tilde L}{\partial W^{(t)}},$$

and the same for $U, b, V, c$. So it is enough to find the derivative for each copy and add them.

**Notation.** Let $L_{\ge t} = \sum_{s = t}^{T} \ell_s$ and $L_{> t} = L_{\ge t+1}$. For a fixed $t$, the terms $\ell_s$ with $s \ge t + 1$ depend on $h_0, \ldots, h_{t-1}$ only through $h_t$. So we can view $L_{>t}$ as a function of $h_t$, with $h_{t+1}, \ldots, h_T$ recomputed from it. Write $\rho_t = \partial L_{>t} / \partial h_t$ for this derivative, so $\rho_T = 0$.

**Invariant.** At the start of the round with index $t$ of the loop at line L4, the variable $r$ equals $\rho_t$.

*Base, $t = T$.* Line L3 sets $r = 0 = \rho_T$, since $L_{>T}$ is the empty sum.

*Step.* Assume $r = \rho_t$ at the start of round $t$. Line L5 computes $e_t = o_t - y_t = \partial \ell_t / \partial o_t$. Since $\ell_t$ depends on $h_t$ only through $o_t = V h_t + c$, its derivative is $\partial \ell_t / \partial h_t = V^\top e_t$. Then

$$\frac{\partial L_{\ge t}}{\partial h_t} = \frac{\partial \ell_t}{\partial h_t} + \frac{\partial L_{>t}}{\partial h_t} = V^\top e_t + \rho_t,$$

which is the value of $r$ after line L6. As $h_t = \tanh(a_t)$ acts on each coordinate and $\tanh' = 1 - \tanh^2$,

$$\frac{\partial L_{\ge t}}{\partial a_t} = \frac{\partial L_{\ge t}}{\partial h_t} \odot (1 - h_t \odot h_t),$$

which is $\delta$ after line L7. The state $h_{t-1}$ affects $L_{\ge t}$ only through $a_t = W h_{t-1} + U x_t + b$, so $\partial L_{\ge t} / \partial h_{t-1} = W^\top \delta$. Line L9 stores this in $r$. Since $L_{\ge t} = L_{> t-1}$, this is $\rho_{t-1}$, the value the invariant needs at the start of round $t - 1$.

**The parameter gradients.** In round $t$:

- The copy $V^{(t)}$ and $c^{(t)}$ enter $\tilde L$ only in $o_t$, so $\partial \tilde L / \partial V^{(t)} = e_t h_t^\top$ and $\partial \tilde L / \partial c^{(t)} = e_t$. Line L5 adds these.
- The copies $W^{(t)}, U^{(t)}, b^{(t)}$ enter $\tilde L$ only in $a_t$, and only the terms $\ell_s$ with $s \ge t$ depend on $a_t$. So the derivative is $\partial L_{\ge t} / \partial a_t = \delta$ times the partial derivative of $a_t$: $\delta h_{t-1}^\top$, $\delta x_t^\top$ and $\delta$. Line L8 adds these.

Each copy is visited exactly once, in round $t$. After the last round, $t = 1$, the accumulators hold $\sum_t \partial \tilde L / \partial \theta^{(t)} = \partial L / \partial \theta$ for each parameter, and $r = \rho_0 = \partial L / \partial h_0$, since $L_{>0} = L$.

All the values the backward loop reads, $h_t$, $h_{t-1}$, $o_t$, $x_t$ and the parameters, were written by lines L1 and L2 and are not changed by lines L4 to L9.

**Termination.** Both loops run $T$ rounds of a fixed number of matrix and vector operations, so BPTT stops after $\Theta(T)$ rounds and returns $\nabla L$ and $\partial L / \partial h_0$.

**Truncated BPTT.** On each chunk of $k$ steps, truncated BPTT calls BPTT with the start state $\hat h$ that the previous chunk computed, and treats $\hat h$ as a constant. By the result above, each call returns the exact gradient of the chunk loss as a function of $\theta$ with $\hat h$ fixed. So truncated BPTT returns the exact gradient of $\sum_{\text{chunks}} L_{\text{chunk}}(\theta; \hat h_{\text{chunk}})$, and it equals $\nabla L$ when $k \ge T$, since then there is one chunk with $\hat h = h_0$. $\blacksquare$
