---
tag: QPCY13
kind: model
slug: number-on-forehead-model
name: Number-on-forehead model
aliases:
- NOF model
area: complexity/communication-and-query-complexity
level: research
summary: "A multiparty communication model in which player i sees every input except x_i and the players write on a shared blackboard. Strong lower bounds in it would give new circuit lower bounds."
prereqs: [multiparty-communication-complexity]
see_also: [number-in-hand-model, inner-product-problem, discrepancy-method, ac0, circuit-complexity, boolean-circuit, nisan-prg, communication-matrix]
sources:
  - paper: doi:10.1145/800061.808737
    title: "Ashok K. Chandra, Merrick L. Furst and Richard J. Lipton, Multi-party protocols, 15th ACM Symposium on Theory of Computing (STOC 1983), pages 94-99"
    locator: the model, and the Exactly-N problem (Corollary 4.6, an O(sqrt(log N)) protocol for three players; a lower bound by a Ramsey argument)
  - paper: doi:10.1016/0022-0000(92)90047-M
    title: "László Babai, Noam Nisan and Mario Szegedy, Multiparty protocols, pseudorandom generators for logspace, and time-space trade-offs, Journal of Computer and System Sciences 45(2), 1992, pages 204-232"
    locator: cylinder intersections, the discrepancy bound, Omega(n/4^k) for the generalized inner product, and the uses for logspace generators and time-space trade-offs
  - paper: doi:10.1006/inco.1994.1051
    title: "Vince Grolmusz, The BNS lower bound for multi-party protocols is nearly optimal, Information and Computation 112(1), 1994, pages 51-54"
    locator: the O(kn/2^k) protocol for the generalized inner product
  - paper: doi:10.1007/BF01272517
    title: "Johan Håstad and Mikael Goldmann, On the power of small-depth threshold circuits, Computational Complexity 1(2), 1991, pages 113-129"
    locator: the NOF protocol for a threshold gate over gates of fan-in less than k, and the circuit lower bound for the generalized inner product
  - book: isbn:9780521560672
    title: Eyal Kushilevitz and Noam Nisan, Communication Complexity, Cambridge University Press (1997)
    locator: Chapter 6, Multiparty communication complexity
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press (2020)
    locator: Chapter 4, Numbers on Foreheads
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 13, Communication complexity (the multiparty model and its link to circuit lower bounds)
---

The number-on-forehead model (NOF) is the model of [multiparty communication complexity](/multiparty-communication-complexity/) in which input $x_i$ is written on the forehead of player $i$. Each player sees all the inputs except its own, the players write bits on a shared blackboard, and the cost is the number of bits written. Chandra, Furst and Lipton introduced the model in 1983. Because each input is seen by $k - 1$ of the $k$ players, protocols in this model are strong and lower bounds are hard to prove. The best known lower bounds for explicit functions become trivial once there are more than about $\log_2 n$ players, and a bound that holds for a polylogarithmic number of players would give lower bounds for the circuit class $\mathsf{ACC^0}$. Keep it apart from the [number-in-hand model](/number-in-hand-model/), where each player sees only its own input.

## The machine

There are $k \ge 2$ players and a function $f : X_1 \times \cdots \times X_k \to \{0,1\}$, often with $X_i = \{0,1\}^n$. Player $i$ sees $x_{-i} = (x_1, \ldots, x_{i-1}, x_{i+1}, \ldots, x_k)$.

A protocol is a rooted tree, as in the two-party [communication model](/communication-model/). Each inner node names the player who writes next, and that player's bit is a function of $x_{-i}$ and of the bits on the board. Each leaf holds an output. The protocol computes $f$ if every input reaches a leaf that holds its value.

**Cylinder intersections.** A **cylinder in direction $i$** is a set $C \subseteq X_1 \times \cdots \times X_k$ such that membership in $C$ does not depend on the coordinate $x_i$: if $x \in C$ and $x'$ differs from $x$ only in coordinate $i$, then $x' \in C$. A **cylinder intersection** is a set $C_1 \cap \cdots \cap C_k$ where $C_i$ is a cylinder in direction $i$. Each bit written by player $i$ cuts the set of inputs by a condition that does not depend on $x_i$, so the inputs that reach one leaf form a cylinder intersection. A protocol of cost $c$ splits the input space into at most $2^c$ cylinder intersections on which $f$ is constant. For $k = 2$ a cylinder intersection is a combinatorial rectangle, and the model is the two-party model.

## What it counts

The cost is the number of bits on the blackboard in the worst case. All computation is free. Write $D^{cc}_{\mathrm{NOF},k}(f)$ for the deterministic cost and $R^{cc}_{\mathrm{NOF},k}(f)$ for the cost with error at most $1/3$ on every input, with public randomness unless the text says private.

Every function with $n$-bit inputs costs at most $n + 1$: player 2 writes $x_1$, and then player 1 knows all the inputs and writes the answer. This bound does not grow with $k$, and for many functions the cost falls as $k$ grows, because each player sees more.

Small cases show how strong the model is:

- **Equality of two inputs**, $f = 1$ when $x_1 = x_2$, with $k = 3$: player 3 sees $x_1$ and $x_2$ and writes the answer, so the cost is 1 bit.
- **Parity of all bits**: player 1 writes the parity of $x_2, \ldots, x_k$, and player 2, who sees $x_1$, writes the parity of everything. The cost is 2 bits.
- **Exactly N**: three players hold numbers in $\{0, \ldots, N\}$ and decide whether the three sum to $N$. Chandra, Furst and Lipton showed that the cost is $O(\sqrt{\log N})$, with a protocol based on Behrend's sets with no three-term arithmetic progression, and that it is not bounded by a constant, with a Ramsey argument. The problem is equivalent to bounds on sets in $[N]^2$ with no corner, so its exact cost is open.

## Relation to other models

**Number in hand.** Any NIH protocol can be run in NOF at the same cost: the bit of NIH player $i$ depends on $x_i$ and the board, and any player $j \ne i$ sees both. So $D^{cc}_{\mathrm{NOF},k}(f) \le D^{cc}_{\mathrm{NIH},k}(f)$. The gap can be as large as $n + 1$ against 1, as for equality above.

**Circuits.** Håstad and Goldmann observed the following. Let $f$ be computed by a depth-2 circuit with a majority gate at the top, $s$ gates at the bottom, and bottom fan-in less than $k$. Then $f$ has a $k$-party NOF protocol with $O(k \log s)$ bits. The reason is that each bottom gate misses the input of at least one player, so some player can evaluate it; each player writes how many of its assigned gates output 1, and then every player can compare the total with $s/2$. A NOF lower bound of $c$ bits therefore gives $s \ge 2^{\Omega(c/k)}$. With the bound for GIP below, this gives an exponential size lower bound for such circuits.

The same idea reaches further. By results of Yao and of Beigel and Tarui, every function in $\mathsf{ACC^0}$ has a depth-2 circuit of this kind with a symmetric gate at the top, size $2^{\mathrm{polylog}(n)}$ and bottom fan-in $\mathrm{polylog}(n)$. So such a function has a NOF protocol with $\mathrm{polylog}(n)$ bits for some $k = \mathrm{polylog}(n)$ players. An explicit function that needs more than polylogarithmic communication with polylogarithmically many players would not be in $\mathsf{ACC^0}$. No such bound is known, which is one reason that NOF lower bounds for $k > \log_2 n$ are a central open problem. Compare [AC0](/ac0/) and the general study of [circuit complexity](/circuit-complexity/).

## Known results in the model

**Generalized inner product.** Let the inputs be the rows of a $k \times n$ 0-1 matrix, and let $\mathrm{GIP}_k(x_1, \ldots, x_k)$ be the parity of the number of columns that are all ones. For $k = 2$ this is the [inner product problem](/inner-product-problem/). Babai, Nisan and Szegedy proved that $\mathrm{GIP}_k$ has small discrepancy on every cylinder intersection, and so needs $\Omega(n/4^k)$ bits, even with randomness. This is the multiparty form of the [discrepancy method](/discrepancy-method/). Grolmusz gave a protocol with $O(kn/2^k)$ bits. So the cost of GIP falls exponentially in $k$, and the BNS method gives nothing for $k$ above about $\log_2 n$.

**Uses of the GIP bound.** Babai, Nisan and Szegedy used it to build pseudorandom generators that fool logspace machines, an early step before the [Nisan generator](/nisan-prg/), and to prove time-space trade-offs for branching programs. Håstad and Goldmann used it for the depth-2 circuit lower bound above.

**Open problems.** For $k$ well above $\log_2 n$ players, no explicit function is known to need more than polylogarithmically many bits. A bound of that kind with $k = \mathrm{polylog}(n)$ would separate a function from $\mathsf{ACC^0}$.

## References
