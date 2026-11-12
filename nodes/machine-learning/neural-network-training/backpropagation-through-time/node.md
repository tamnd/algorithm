---
tag: W0KS2M
kind: algorithm
slug: backpropagation-through-time
name: Backpropagation through time
aliases:
- BPTT
- truncated BPTT
area: machine-learning/neural-network-training
level: core
summary: "Unroll a recurrent network over the T steps of a sequence and run backpropagation on the unrolled graph: the exact gradient for O(T) memory."
model: real-ram
complexity:
  vars: {T: "the length of the sequence", H: "the number of hidden units", D: "the input dimension", M: "the output dimension", k: "the truncation window"}
  time: {worst: "Θ(T (H^2 + H D + M H))", best: "Θ(T (H^2 + H D + M H))"}
  space: {extra: "Θ(T H)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1990
  people: [Paul J. Werbos]
  note: "Werbos described BPTT in full in Proc. IEEE in 1990. Rumelhart, Hinton and Williams had shown the unfolding of a recurrent net in time in 1986, and Williams and Peng studied the truncated form in 1990."
prereqs: [backpropagation]
see_also: [teacher-forcing, vanishing-gradient-problem, exploding-gradient-problem, gradient-clipping, gradient-checkpointing, computational-graph, automatic-differentiation, hidden-markov-model]
sources:
  - paper: doi:10.1109/5.58337
    title: "Paul J. Werbos, Backpropagation through time: what it does and how to do it, Proceedings of the IEEE 78(10), 1990"
    locator: pp. 1550 to 1560 (the unrolled network, the backward recursion for the ordered derivatives, and its cost)
  - paper: doi:10.1162/neco.1990.2.4.490
    title: "Ronald J. Williams and Jing Peng, An efficient gradient-based algorithm for on-line training of recurrent network trajectories, Neural Computation 2(4), 1990"
    locator: pp. 490 to 501 (truncated BPTT with a window of h steps and the BPTT(h; h') family)
  - paper: doi:10.1162/neco.1989.1.2.270
    title: "Ronald J. Williams and David Zipser, A learning algorithm for continually running fully recurrent neural networks, Neural Computation 1(2), 1989"
    locator: pp. 270 to 280 (real-time recurrent learning, the forward alternative to BPTT)
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 10.1 (unfolding computational graphs) and Section 10.2.2 (computing the gradient in a recurrent neural network)
  - paper: "Razvan Pascanu, Tomas Mikolov and Yoshua Bengio, On the difficulty of training recurrent neural networks, Proceedings of the 30th International Conference on Machine Learning (ICML), PMLR 28(3), 2013"
    locator: pp. 1310 to 1318; Section 2 (the BPTT gradient as a sum of products of Jacobians)
---

Backpropagation through time (BPTT) computes the gradient of the loss of a recurrent network over a whole sequence. It unrolls the network: one copy of the cell for each of the $T$ time steps, all with the same weights. The result is a deep feedforward [computational graph](/computational-graph/), and BPTT runs [backpropagation](/backpropagation/) on it, then adds the gradients of the copies of each weight. The gradient is exact, the time is about three forward passes, and the memory is $\Theta(T)$ hidden states. Truncated BPTT limits the backward sweep to windows of $k$ steps, which bounds the memory by $\Theta(k)$ but gives a biased gradient.

## In plain words

A recurrent network reads a sequence one item at a time and keeps a hidden state, a memory vector that it updates at each step with the same weights. If you write out the computation for a sequence of length $T$, you get $T$ copies of the same layer stacked on top of each other, each feeding its state to the next. That stack is an ordinary deep network, so backpropagation applies to it.

The only new point is that the copies share their weights. The gradient for a shared weight is the sum of the gradients that each copy would get if it had its own weight. So BPTT runs backward from the last step to the first, carries the error signal through the hidden states, and adds the contribution of every step into one gradient per weight.

## The problem

The network is an Elman recurrent network with a $\tanh$ cell, hidden state $h_t \in \mathbb{R}^H$, input $x_t \in \mathbb{R}^D$ and output $o_t \in \mathbb{R}^M$:

$$a_t = W h_{t-1} + U x_t + b, \qquad h_t = \tanh(a_t), \qquad o_t = V h_t + c, \qquad t = 1, \ldots, T.$$

The parameters are $\theta = (W, U, b, V, c)$, the same at every step. The initial state $h_0$ is given. The loss is the sum of per-step losses, here $L = \sum_{t=1}^{T} \frac12 \lVert o_t - y_t \rVert^2$. The output is $\partial L / \partial \theta$ and also $\partial L / \partial h_0$, which is needed when $h_0$ comes from another network, such as an encoder.

## The algorithm

The variable $r$ carries the derivative of the loss of the later steps with respect to the current hidden state.

```pseudo id=main
BPTT(W, U, b, V, c, h_0, x_1..x_T, y_1..y_T)
L1  for t ← 1 to T do                          ▷ forward pass; keep every h_t
L2      h_t ← tanh(W h_{t−1} + U x_t + b);  o_t ← V h_t + c
L3  ∂W, ∂U, ∂b, ∂V, ∂c ← 0;  r ← 0              ▷ r = ∂(loss of steps after t)/∂h_t
L4  for t ← T down to 1 do                     ▷ backward pass through time
L5      e_t ← o_t − y_t;  ∂V += e_t h_tᵀ;  ∂c += e_t
L6      r ← r + Vᵀ e_t                          ▷ now r = ∂(loss of steps t..T)/∂h_t
L7      δ ← r ⊙ (1 − h_t ⊙ h_t)                 ▷ the derivative with respect to a_t
L8      ∂W += δ h_{t−1}ᵀ;  ∂U += δ x_tᵀ;  ∂b += δ
L9      r ← Wᵀ δ                                ▷ send the error back one step
L10 return (∂W, ∂U, ∂b, ∂V, ∂c, r)              ▷ r = ∂L/∂h_0
```

Lines L5 to L9 are backpropagation through one copy of the cell. Line L6 is where the two paths into $h_t$ meet: the loss at step $t$ through $o_t$, and all later losses through $h_{t+1}$. The `+=` in lines L5 and L8 is the sum over the copies of a shared weight.

**Truncated BPTT.** Cut the sequence into chunks of $k$ steps. For each chunk in order, run BPTT on the chunk, starting from the hidden state that the previous chunk ended in, and treat that start state as a constant: no error goes back into earlier chunks. Add the chunk gradients, or take an optimizer step after each chunk. The hidden state is carried forward across the cuts; the error signal $r$ is not carried backward.

## Example

A scalar network: $H = D = M = 1$, $W = 0.5$, $U = 1$, $b = 0$, $V = 1$, $c = 0$, $h_0 = 0$, inputs $x = (1, 0, 0)$ and targets $y = (0.5, 0.5, 0)$. The forward pass gives $h_1 = \tanh 1 = 0.761594$, $h_2 = \tanh(0.380797) = 0.363399$ and $h_3 = 0.179726$, with $o_t = h_t$ and $L = 0.059696$. The backward pass:

| $t$ | $e_t$ | $r$ after L6 | $1 - h_t^2$ | $\delta$ | $\delta h_{t-1}$ added to $\partial W$ | $r = 0.5\,\delta$ after L9 |
|---|---|---|---|---|---|---|
| 3 | 0.179726 | 0.179726 | 0.967698 | 0.173921 | 0.063203 | 0.086960 |
| 2 | −0.136601 | −0.049640 | 0.867941 | −0.043085 | −0.032813 | −0.021542 |
| 1 | 0.261594 | 0.240052 | 0.419974 | 0.100816 | 0 | 0.050408 |

So $\partial L / \partial W = 0.030390$, $\partial L / \partial U = 0.100816$ (only $x_1 \ne 0$), $\partial L / \partial b = 0.231652$ and $\partial L / \partial h_0 = 0.050408$. Each value agrees with a central difference of $L$.

Truncated BPTT with $k = 1$ drops the $r$ that line L9 sends back. Its estimate of $\partial L / \partial W$ is $-0.027093$: the wrong sign. Truncation keeps the term $\delta_3 h_2 = 0.063203$ of step 3, but it drops the $r = 0.086960$ that step 3 sends back to $h_2$. Without it, the term of step 2 becomes $-0.090295$ instead of $-0.032813$. With $k \ge 3$ the result is the exact gradient.

## Correctness

The invariant of the backward loop is: at the start of round $t$, $r = \partial L_{>t} / \partial h_t$, where $L_{>t}$ is the sum of the losses of the steps after $t$. Line L6 adds the direct term of step $t$, line L7 passes through $\tanh$, and line L9 passes through $a_t = W h_{t-1} + \cdots$, which gives the invariant for $t - 1$. For the shared weights, write $L$ as a function $\tilde L$ of one copy of $\theta$ per step evaluated at equal copies; the chain rule then gives $\partial L / \partial \theta = \sum_t \partial \tilde L / \partial \theta^{(t)}$, and line L8 adds exactly these terms. The full proof is in the proof file below.

Truncated BPTT returns the exact gradient of a different function: the sum of the chunk losses, each with its start state held fixed. This is a biased estimate of $\nabla L$. It misses every dependence longer than the window. The bias is small when the influence of $h_{t-k}$ on later losses decays fast, which is the [vanishing gradient](/vanishing-gradient-problem/) case, and the method then learns no dependency longer than $k$ steps.

## Complexity

Count multiply-adds on a [real RAM](/real-ram/).

- **Time.** Each step of the forward pass costs $H^2 + HD + MH$ multiply-adds. Each step of the backward pass costs about twice that: $MH$ for $\partial V$ and $MH$ for $V^\top e_t$, $H^2 + HD$ for the outer products at line L8, and $H^2$ for $W^\top \delta$. In total $\Theta(T(H^2 + HD + MH))$, in the best and the worst case, about three forward passes.
- **Memory.** The backward pass needs every $h_t$, so BPTT keeps $T + 1$ hidden vectors: $\Theta(TH)$ beyond the parameters. This is the cost of reverse mode, whose memory grows with the length of the trace.
- **Truncated BPTT.** Each chunk keeps at most $k + 1$ hidden vectors, so the memory is $\Theta(kH)$, and the time is the same as for full BPTT.
- **Real-time recurrent learning** (Williams and Zipser 1989) is the forward mode alternative. It carries the derivative of $h_t$ with respect to every weight forward in time: $\Theta(H^3)$ memory for the $H \times H^2$ sensitivity matrix and $\Theta(H^4)$ time per step, but no memory that grows with $T$, so it works online on unbounded streams.

## Properties

- **Exact for the unrolled program.** Full BPTT gives the exact gradient of $L$, up to rounding.
- **Sum of products of Jacobians.** Unrolling the recursion gives
  $$\frac{\partial L}{\partial h_s} = \sum_{t \ge s} \Big(\prod_{u = s+1}^{t} J_u\Big)^\top \frac{\partial \ell_t}{\partial h_t}, \qquad J_u = \frac{\partial h_u}{\partial h_{u-1}} = \mathrm{diag}(1 - h_u \odot h_u)\, W.$$
  The terms for long gaps $t - s$ are products of many Jacobians. They shrink or grow geometrically, which causes the [vanishing gradient problem](/vanishing-gradient-problem/) and the [exploding gradient problem](/exploding-gradient-problem/).
- **Sequential.** Both passes run in time order and cannot be parallelized over $t$ for a nonlinear recurrence.
- **Biased truncation.** Truncated BPTT is consistent only for dependencies shorter than $k$.

## Variants and improvements

- **BPTT(h; h').** Williams and Peng run a backward pass of $h$ steps every $h'$ steps, with $h' \le h$. The chunked form above is $h = h' = k$. With $h' = 1$ the network learns online, one step at a time, at $h$ times the cost.
- **Gradient checkpointing.** Store only every $\lceil \sqrt T \rceil$-th hidden state and recompute the others in the backward pass: $\Theta(\sqrt T H)$ memory for one extra forward pass and the exact gradient. See [gradient checkpointing](/gradient-checkpointing/).
- **Gated cells.** For LSTM and GRU cells, lines L5 to L9 become the backward pass of the cell, and $r$ carries the derivatives with respect to the cell state and the hidden state. The additive cell update of the LSTM keeps $\partial c_t / \partial c_{t-1}$ near the identity, which reduces vanishing gradients.
- **Clipping.** With long sequences, bound the gradient norm before the update; see [gradient clipping](/gradient-clipping/).
- **Training a sequence model.** For a network whose next input is its previous output, BPTT is often combined with [teacher forcing](/teacher-forcing/), which feeds the true previous output during training. This cuts the gradient path through the outputs. The steps become independent only when the outputs are the only recurrence; with a hidden state $h_t$ the gradient still runs back through it, and BPTT is still needed.

## When to use it

Use full BPTT when the sequences fit in memory, for example sentences or short time series: it gives the exact gradient. Use truncated BPTT for very long or unbounded streams, such as language modeling on a whole corpus, and pick $k$ larger than the longest dependency you need. Use checkpointing when you need the exact gradient on long sequences and can pay for a second forward pass. Use real-time recurrent learning only for small networks that must learn online.

## Pitfalls

- **Forgetting the direct term.** Line L6 must add $V^\top e_t$ to the error that comes from step $t + 1$. Dropping either term gives the gradient of a different loss.
- **Resetting the accumulators per step.** The gradients of the shared weights are sums over all steps; resetting $\partial W$ inside the loop keeps only the gradient of step 1.
- **The wrong state in the outer product.** Line L8 uses $h_{t-1}$, the input of step $t$, not $h_t$.
- **Gradients through the carried state.** In truncated BPTT with an autodiff framework, the carried state must be detached from the graph at each cut. Otherwise the graph grows over the whole stream and the memory with it.
- **Truncation that is too short.** A window shorter than the dependency makes the gradient blind to it, and the estimate can even have the wrong sign, as in the example.

## Implementations

## History

Rumelhart, Hinton and Williams showed in 1986 that a recurrent network can be trained by unfolding it in time into a layered network with shared weights. Werbos gave the general method, its name and its cost analysis in his 1990 Proceedings of the IEEE article, building on his work on ordered derivatives from 1974 on. In the same period, Williams and Zipser (1989) gave real-time recurrent learning as the online forward alternative, and Williams and Peng (1990) studied the truncated and the online variants of BPTT. Bengio, Simard and Frasconi (1994) and Hochreiter (1991) showed that the gradients that BPTT computes for long time gaps tend to vanish, which led to the LSTM.

## References
