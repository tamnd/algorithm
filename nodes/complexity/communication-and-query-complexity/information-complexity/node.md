---
tag: 0NCHWQ
kind: concept
slug: information-complexity
name: Information complexity
aliases:
- internal information cost
area: complexity/communication-and-query-complexity
level: research
summary: "The information a protocol's transcript reveals about the inputs. It is a lower bound on communication, it adds up over independent copies, and it equals amortized communication."
prereqs: [randomized-communication-complexity, shannon-entropy, conditional-entropy]
see_also: [direct-sum-communication, disjointness-problem, simultaneous-message-model, corruption-bound, kullback-leibler-divergence, source-coding-theorem, frequency-moment-lower-bounds, discrepancy-method]
sources:
  - paper: "Amit Chakrabarti, Yaoyun Shi, Anthony Wirth and Andrew Chi-Chih Yao, Informational complexity and the direct sum problem for simultaneous message complexity, Proceedings of the 42nd IEEE Symposium on Foundations of Computer Science (FOCS 2001)"
    locator: the first definition of information cost (the external form, under product distributions) and its use for a direct sum theorem
  - paper: "Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar and D. Sivakumar, An information statistics approach to data stream and communication complexity, Journal of Computer and System Sciences 68(4) (2004), 702-732"
    locator: conditional information complexity, the direct sum for disjointness and the AND function; conference version FOCS 2002
  - paper: "Boaz Barak, Mark Braverman, Xi Chen and Anup Rao, How to compress interactive communication, SIAM Journal on Computing 42(3) (2013), 1327-1363"
    locator: the internal information cost and the compression of protocols to about sqrt(C I) bits, and to about I_ext bits; conference version STOC 2010
  - paper: "Mark Braverman and Anup Rao, Information equals amortized communication, IEEE Transactions on Information Theory 60(10) (2014)"
    locator: the internal information complexity equals the amortized distributional communication; conference version FOCS 2011
  - paper: "Mark Braverman, Ankit Garg, Denis Pankratov and Omri Weinstein, From information to exact communication, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC 2013), 151-160"
    locator: the exact information complexity of AND and the constant about 0.4827 for disjointness
  - paper: "Anat Ganor, Gillat Kol and Ran Raz, Exponential separation of information and communication, Proceedings of the 55th IEEE Symposium on Foundations of Computer Science (FOCS 2014)"
    locator: a communication task with information O(k) and distributional communication 2^Omega(k)
  - book: isbn:9781108497985
    title: Anup Rao and Amir Yehudayoff, Communication Complexity and Applications, Cambridge University Press, 2020
    locator: Chapter 6, Information, and Chapter 7, Compressing Communication
---

Information complexity measures how much a communication protocol reveals about the inputs, in the sense of Shannon's mutual information, instead of how many bits it sends. A transcript of $c$ bits can reveal at most $c$ bits, so information is a lower bound on communication. Unlike communication, information adds up exactly over independent copies of a problem, which makes it the main tool for [direct sum](/direct-sum-communication/) results and for the $\Omega(n)$ bound for [disjointness](/disjointness-problem/). Braverman and Rao proved that internal information equals the communication per copy needed to solve many copies at once.

## In plain words

When Alice and Bob talk, each of them learns something about the other's input. Information complexity counts how much they learn, measured in bits of information, and not how many bits they send.

A long talk can teach little, for example when Bob could already guess most of what Alice says. A talk that teaches a lot must be long. So if a task forces the players to learn much, it also forces them to talk much.

The useful feature is that learning adds up. If a task is made of many separate small tasks, the total learning is the sum of the learning for each one. This lets one prove a bound for a large task from a bound for a tiny task.

## The idea

**Setting.** Fix a distribution $\mu$ on inputs $(X, Y)$ and a two-way protocol $\pi$ with public coins and private coins. Let $\Pi$ be the transcript together with the public coins. For random variables $A, B, C$ write $I(A; B \mid C) = H(A \mid C) - H(A \mid B, C)$ for the conditional mutual information, with $H$ the [Shannon entropy](/shannon-entropy/) and [conditional entropy](/conditional-entropy/).

**Two measures.**

- The *internal information cost* is what each player learns about the other's input:
$$\mathrm{IC}_\mu(\pi) = I(\Pi; X \mid Y) + I(\Pi; Y \mid X).$$
- The *external information cost* is what an observer who sees only the transcript learns about both inputs:
$$\mathrm{IC}^{\mathrm{ext}}_\mu(\pi) = I(\Pi; X Y).$$

The information complexity of a function is the least cost over protocols that compute it with error at most $\varepsilon$:
$$\mathrm{IC}_\mu(f, \varepsilon) = \inf_\pi \mathrm{IC}_\mu(\pi).$$
Some authors ask for error $\varepsilon$ under $\mu$, others for error $\varepsilon$ on every input. Both are used, and the page says which one when it matters. The infimum is needed, since no single protocol may reach it.

**Basic facts.**

1. $\mathrm{IC}_\mu(\pi) \le \mathrm{IC}^{\mathrm{ext}}_\mu(\pi) \le \|\pi\|$, the worst-case length of the protocol. The second bound holds because $I(\Pi; XY) \le H(\Pi \mid R) \le \|\pi\|$, where $R$ are the public coins, which are independent of the inputs. The first bound follows from the chain rule, one message at a time: a message of Alice reveals nothing new about $Y$ to someone who knows $X$, and what it reveals about $X$ to Bob is at most what it reveals about $(X, Y)$ to an observer.
2. If $\mu$ is a product distribution, with $X$ and $Y$ independent, then the two costs are equal.
3. Public coins are part of $\Pi$. They are independent of $(X, Y)$, so they add nothing to either cost. Private coins can lower the information cost, and they are allowed.
4. **Additivity.** For $n$ independent copies, $\mathrm{IC}_{\mu^n}(f^n, \varepsilon) = n \cdot \mathrm{IC}_\mu(f, \varepsilon)$, with error $\varepsilon$ on each copy. See [direct sum for communication](/direct-sum-communication/) for the proof.
5. **Information equals amortized communication** (Braverman and Rao, 2011). $\mathrm{IC}_\mu(f, \varepsilon) = \lim_{n \to \infty} D^\mu_\varepsilon(f^n)/n$ for $\varepsilon > 0$, where $D^\mu_\varepsilon(f^n)$ is the distributional cost of $n$ copies with error $\varepsilon$ on each copy. This is the interactive analogue of Shannon's [source coding theorem](/source-coding-theorem/).
6. **Compression of one copy.** Barak, Braverman, Chen and Rao (2010) proved that a protocol with communication $C$ and internal cost $I$ can be simulated with $\tilde{O}(\sqrt{C \cdot I})$ bits, and one with external cost $I_{\mathrm{ext}}$ with $I_{\mathrm{ext}} \cdot \mathrm{polylog}(C)$ bits.
7. **No full compression.** Ganor, Kol and Raz (2014) gave a communication task with information cost $O(k)$ whose distributional communication is $2^{\Omega(k)}$. So information can be exponentially smaller than communication for one copy, and one copy cannot in general be compressed to a length polynomial in its information cost.

## Examples

All numbers below come from a direct computation of the entropies.

**AND with the trivial protocol.** Alice sends $x$ and Bob replies with $x \wedge y$. Under the uniform distribution on $\{0,1\}^2$:

| Distribution $\mu$ | $I(\Pi; X \mid Y)$ | $I(\Pi; Y \mid X)$ | internal | external |
|---|---|---|---|---|
| uniform on $\{0,1\}^2$ | 1 | 0.5 | 1.5 | 1.5 |
| $X = Y$, a uniform bit | 0 | 0 | 0 | 1 |
| uniform on $\{(0,0), (0,1), (1,0)\}$ | 0.6667 | 0 | 0.6667 | 0.9183 |

- Under the uniform distribution, Bob learns $x$ (1 bit), and Alice learns $y$ only when $x = 1$ (half a bit on average). The distribution is a product, so internal and external costs agree. A "lazy" protocol in which Bob sends $y$ only if $x = 1$ has the same costs.
- When $X = Y$, each player already knows the other's input, so the internal cost is 0. An observer still learns the bit, so the external cost is 1. This shows that the internal cost can be much smaller than the external cost when the inputs are correlated.
- On the three inputs where $\mathrm{AND} = 0$, Bob learns $x$ only when $y = 0$, which gives $2/3$ of a bit, and Alice learns nothing. The external cost is the entropy $H_2(1/3) \approx 0.9183$ of Alice's bit.

**Disjointness from AND (Bar-Yossef, Jayram, Kumar and Sivakumar).** $\mathrm{DISJ}_n(x, y) = \neg \bigvee_i (x_i \wedge y_i)$. Take a distribution $\mu$ on $\{0,1\}^2$ supported on the three inputs with $\mathrm{AND} = 0$, as in the last row above, and put $\mu^n$ on the $n$ coordinates. Every input then has disjoint sets. A two-way protocol for disjointness that is correct on every input must also be correct when one coordinate is changed to $(1, 1)$. Embedding an AND instance in coordinate $i$ and sampling the other coordinates from $\mu$ with public and private coins gives

$$R_\varepsilon(\mathrm{DISJ}_n) \ge \mathrm{IC}_{\mu^n}(\pi) \ge n \cdot \mathrm{IC}_\mu(\mathrm{AND}, \varepsilon),$$

where the AND protocols must be correct on all four inputs although the information is measured only on $\mu$. To make the sampling work, BJKS condition on an extra hidden variable that tells which player holds the 0 in each coordinate; this is their conditional information complexity. They then show that $\mathrm{IC}_\mu(\mathrm{AND}, \varepsilon)$ is a positive constant, using the Hellinger distance between transcript distributions. This gives $R(\mathrm{DISJ}_n) = \Omega(n)$. The condition "correct on every input" is essential: under $\mu$ alone, the protocol that always answers 0 for AND is never wrong and reveals nothing.

**The exact constant.** Braverman, Garg, Pankratov and Weinstein (2013) computed the information complexity of AND exactly, and from it $R_\varepsilon(\mathrm{DISJ}_n) = C_{\mathrm{DISJ}}\, n \pm o(n)$ as $\varepsilon \to 0$, with $C_{\mathrm{DISJ}} \approx 0.4827$. The optimal AND protocol is not a finite protocol: it has the players raise a counter continuously, and finite protocols only approach its cost.
## Where it is used

- **Direct sum and direct product.** Information is additive, so a bound on one copy gives a bound on $k$ copies. With compression, this gives communication direct sum theorems. See [direct sum for communication](/direct-sum-communication/).
- **Lower bounds for disjointness and its relatives.** The proofs for disjointness, for its multi-party number-in-hand form and for [frequency moments](/frequency-moment-lower-bounds/) in streams all go through information complexity.
- **Simultaneous and one-way models.** The first use was the direct sum theorem of Chakrabarti, Shi, Wirth and Yao (2001) in the [simultaneous message model](/simultaneous-message-model/). The one-way bound for [index](/index-problem/) is the simplest information argument.
- **Exact bounds.** Information complexity is the only known method that gives exact leading constants, as for disjointness.
- **Data structures and streaming.** Cell probe and streaming lower bounds often reduce to bounds on information revealed by a short protocol.

## References
