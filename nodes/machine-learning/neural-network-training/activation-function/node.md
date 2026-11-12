---
tag: CX5V0X
kind: concept
slug: activation-function
name: Activation function
aliases:
- neural network activation
area: machine-learning/neural-network-training
level: intro
summary: "The scalar nonlinear function f applied to each unit after the linear map of a layer, a = f(Wx + b): sigmoid, tanh, ReLU, GELU and others."
prereqs: [perceptron]
see_also: [relu, vanishing-gradient-problem, backpropagation, he-initialization, xavier-initialization, logistic-regression, softmax-regression, piecewise-linear-interpolation]
sources:
  - book: isbn:9780262035613
    title: Ian Goodfellow, Yoshua Bengio and Aaron Courville, Deep Learning, MIT Press, 2016
    locator: Section 6.3 (hidden units; rectified linear units, logistic sigmoid and hyperbolic tangent) and Section 6.4.1 (universal approximation properties and depth)
  - paper: doi:10.1007/BF02551274
    title: "George Cybenko, Approximation by superpositions of a sigmoidal function, Mathematics of Control, Signals, and Systems 2(4), 1989"
    locator: pp. 303 to 314; Theorem 2 (finite sums of continuous sigmoidal units are dense in C([0,1]^n))
  - paper: doi:10.1016/S0893-6080(05)80131-5
    title: "Moshe Leshno, Vladimir Ya. Lin, Allan Pinkus and Shimon Schocken, Multilayer feedforward networks with a nonpolynomial activation function can approximate any function, Neural Networks 6(6), 1993"
    locator: pp. 861 to 867; the main theorem (density if and only if the activation is not a polynomial)
  - paper: "Dan Hendrycks and Kevin Gimpel, Gaussian error linear units (GELUs), arXiv:1606.08415, 2016"
    locator: Section 2 (the definition x Phi(x) and the tanh approximation)
  - paper: "Djork-Arné Clevert, Thomas Unterthiner and Sepp Hochreiter, Fast and accurate deep network learning by exponential linear units (ELUs), ICLR 2016, arXiv:1511.07289"
    locator: Section 3 (the definition of the ELU)
  - paper: doi:10.1016/j.neunet.2017.12.012
    title: "Stefan Elfwing, Eiji Uchibe and Kenji Doya, Sigmoid-weighted linear units for neural network function approximation in reinforcement learning, Neural Networks 107, 2018"
    locator: pp. 3 to 11; Section 2 (the SiLU x sigma(x) and its derivative)
  - paper: "Prajit Ramachandran, Barret Zoph and Quoc V. Le, Searching for activation functions, arXiv:1710.05941, 2017"
    locator: Section 4 (the Swish function x sigma(beta x))
---

An activation function is the scalar nonlinear function $f$ that a neural network layer applies to each coordinate after its linear map: $a = f(Wx + b)$. Without it, a stack of layers is one linear map, whatever its depth. With any continuous activation that is not a polynomial, one hidden layer of enough units can approximate any continuous function on a compact set. The choice of $f$ also sets how gradients flow through the layer during [backpropagation](/backpropagation/), through the derivative $f'$.

## In plain words

Each unit of a network adds up its weighted inputs and then passes the sum through a fixed function, the activation. The linear part can only stretch, turn and shift its input. The activation bends it: it can cut off negative values, squash large ones, or switch smoothly between off and on.

The bend is what lets the network learn curved decision boundaries and complex functions. If every activation were a straight line, the whole network would be a single straight-line function, however many layers it had.

## The idea

A layer computes $z = Wx + b$ and then $a_i = f(z_i)$ for each unit $i$, with the same scalar function $f : \mathbb{R} \to \mathbb{R}$ for all units of the layer.

**Why it must be nonlinear.** If $f(z) = cz + d$ for every layer, then the composition of two layers is $W_2(c W_1 x + c b_1 + d) + b_2 = (c W_2 W_1) x + (\text{const})$, an affine map. By induction, any depth gives an affine map, so a deep linear network can represent no more than the [linear model](/linear-regression/) it replaces.

**Universal approximation.** Let $\sigma$ be the activation of one hidden layer and consider the functions $g(x) = \sum_{j=1}^{N} \alpha_j \sigma(w_j^\top x + \theta_j)$ with $x \in \mathbb{R}^n$.

- Cybenko (1989): if $\sigma$ is continuous and sigmoidal, that is $\sigma(t) \to 1$ as $t \to +\infty$ and $\sigma(t) \to 0$ as $t \to -\infty$, then for every continuous $F$ on $[0,1]^n$ and every $\varepsilon > 0$ some $g$ satisfies $\lvert g(x) - F(x) \rvert < \varepsilon$ for all $x \in [0,1]^n$.
- Leshno, Lin, Pinkus and Schocken (1993): if $\sigma$ is locally bounded and piecewise continuous, the functions $g$ are dense in $C(\mathbb{R}^n)$ in the topology of uniform convergence on compact sets if and only if $\sigma$ is not a polynomial (almost everywhere). This covers ReLU and all the functions below.

A polynomial of degree $d$ fails because each $g$ is then a polynomial of degree at most $d$, a closed finite-dimensional space. These theorems say nothing about how many units are needed or whether training finds them; depth often needs far fewer units than width.

**Gradient flow.** Backpropagation multiplies the error signal by $f'(z)$ at every unit. Where $\lvert f' \rvert$ is small, the unit is saturated and passes little gradient. Since the sigmoid has $f' \le 1/4$, a deep stack of sigmoid units can shrink the gradient geometrically: the [vanishing gradient problem](/vanishing-gradient-problem/). Activations whose derivative is 1 on a half line, such as ReLU, avoid this for active units.

## Examples

| name | $f(x)$ | $f'(x)$ | range |
|---|---|---|---|
| logistic sigmoid | $\sigma(x) = 1 / (1 + e^{-x})$ | $\sigma(x)(1 - \sigma(x)) \le 1/4$ | $(0, 1)$ |
| hyperbolic tangent | $\tanh x = 2\sigma(2x) - 1$ | $1 - \tanh^2 x \le 1$ | $(-1, 1)$ |
| [ReLU](/relu/) | $\max(0, x)$ | 0 for $x < 0$, 1 for $x > 0$ | $[0, \infty)$ |
| leaky ReLU | $x$ for $x > 0$, $\alpha x$ for $x \le 0$, often $\alpha = 0.01$ | 1 or $\alpha$ | $\mathbb{R}$ |
| ELU | $x$ for $x > 0$, $\alpha(e^x - 1)$ for $x \le 0$ | 1 or $\alpha e^x$ | $(-\alpha, \infty)$ |
| GELU | $x \Phi(x)$, $\Phi$ the standard normal CDF | $\Phi(x) + x \varphi(x)$ | about $[-0.17, \infty)$ |
| softplus | $\log(1 + e^x)$ | $\sigma(x)$ | $(0, \infty)$ |
| swish, SiLU | $x \sigma(x)$; swish is $x \sigma(\beta x)$ | $\sigma(x)(1 + x(1 - \sigma(x)))$ | about $[-0.28, \infty)$ |

Values at $x = -2, 0, 2$, rounded to 4 places:

| name | $f(-2)$ | $f(0)$ | $f(2)$ | $f'(-2)$ | $f'(0)$ | $f'(2)$ |
|---|---|---|---|---|---|---|
| sigmoid | 0.1192 | 0.5 | 0.8808 | 0.1050 | 0.25 | 0.1050 |
| tanh | −0.9640 | 0 | 0.9640 | 0.0707 | 1 | 0.0707 |
| ReLU | 0 | 0 | 2 | 0 | (0 by convention) | 1 |
| leaky ReLU, $\alpha = 0.01$ | −0.02 | 0 | 2 | 0.01 | (convention) | 1 |
| ELU, $\alpha = 1$ | −0.8647 | 0 | 2 | 0.1353 | 1 | 1 |
| GELU | −0.0455 | 0 | 1.9545 | −0.0852 | 0.5 | 1.0852 |
| softplus | 0.1269 | 0.6931 | 2.1269 | 0.1192 | 0.5 | 0.8808 |
| SiLU | −0.2384 | 0 | 1.7616 | −0.0908 | 0.5 | 1.0908 |

Notes on the table:

- The sigmoid and tanh **saturate**: at $\lvert x \rvert = 2$ their slopes are already 0.105 and 0.071. Tanh is centered at 0, which makes the inputs of the next layer centered too.
- The derivative of softplus is the sigmoid, so softplus is a smooth ReLU: $\log(1 + e^x) - \max(0, x) \in (0, \log 2]$.
- GELU and SiLU are smooth, not monotone, and slightly negative for negative inputs. GELU has its minimum $-0.1700$ near $x = -0.7518$, and SiLU its minimum $-0.2785$ near $x = -1.2785$. GELU is often computed by the approximation $0.5 x (1 + \tanh(\sqrt{2/\pi}(x + 0.044715 x^3)))$, which differs from $x \Phi(x)$ by less than $10^{-3}$.
- ELU with $\alpha = 1$ has a continuous derivative at 0; leaky ReLU and ReLU do not.

**Non-examples.** The identity is a valid output activation for regression, but as a hidden activation it makes the network linear. A polynomial such as $x^2$ gives networks that compute only polynomials of bounded degree. Softmax is not an elementwise activation: it maps a whole vector to a probability vector and is used at the output, as in [softmax regression](/softmax-regression/).

## Where it is used

- **Hidden layers.** ReLU is the default for feedforward and convolutional networks; GELU and SiLU are common in transformers; tanh and the sigmoid are used inside the gates of recurrent cells such as the LSTM, where a value in $(0, 1)$ acts as a soft switch.
- **Output layers.** The output activation matches the loss: the sigmoid with binary cross-entropy as in [logistic regression](/logistic-regression/), softmax with categorical cross-entropy, the identity with the squared loss, softplus or exp for a positive output such as a variance.
- **Initialization.** The scale of good initial weights depends on $f$. [Xavier initialization](/xavier-initialization/) assumes an activation that is near linear at 0, such as tanh; [He initialization](/he-initialization/) doubles the variance for ReLU, which zeros half of its inputs on average.
- **Piecewise linear networks.** With ReLU or leaky ReLU, the network is a continuous [piecewise linear](/piecewise-linear-interpolation/) function, which can be analysed region by region and verified exactly.
- **History.** The perceptron used a step function, which has derivative 0 almost everywhere and cannot be trained by gradients. The smooth sigmoid made backpropagation possible in the 1980s, and the move to ReLU around 2010 made deep networks easier to train.

## References
