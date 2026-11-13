---
tag: 42G13F
kind: concept
slug: quantum-parallelism
name: Quantum parallelism
aliases:
- quantum parallel evaluation
area: quantum/quantum-primitives
level: intro
summary: "One application of an oracle U_f to a superposition of all inputs gives a state that holds every value f(x). A measurement reads only one pair (x, f(x)), so a speedup also needs interference."
prereqs: [quantum-superposition, quantum-oracle]
see_also: [quantum-interference, deutsch-jozsa-algorithm, simon-algorithm, shor-algorithm, grover-optimality, quantum-query-model, uncomputation, bqp]
sources:
  - paper: doi:10.1098/rspa.1985.0070
    title: "David Deutsch, Quantum theory, the Church-Turing principle and the universal quantum computer, Proceedings of the Royal Society of London A 400(1818):97-117, 1985"
    locator: "the universal quantum computer, and one run on a superposition of inputs that computes a function of all of them (general locator)"
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5):1510-1523, 1997"
    locator: the lower bound of order sqrt(N) queries for unstructured search, and an oracle relative to which NP is not in time o(2^(n/2)) on a quantum machine
  - paper: "Alexander S. Holevo, Bounds for the quantity of information transmitted by a quantum communication channel, Problemy Peredachi Informatsii 9(3):3-11, 1973; English translation in Problems of Information Transmission 9(3):177-183, 1973"
    locator: the bound on the information that a measurement can obtain from an ensemble of quantum states
  - paper: arxiv:1907.09415
    title: Ronald de Wolf, Quantum Computing, lecture notes
    locator: "Section 2.3 (quantum parallelism: one application of U gives f(z) for all 2^n inputs, but a measurement gives one random pair) and Section 15.2 (Holevo's theorem: m qubits carry at most m bits of information)"
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: "Section 1.4.2 (quantum parallelism) and Section 1.4.3 (Deutsch's algorithm, which adds interference)"
---

*Quantum parallelism* is the application of a bit [oracle](/quantum-oracle/) $U_f$, or any circuit for $f$, once to a [superposition](/quantum-superposition/) of all inputs, which gives the state $2^{-n/2}\sum_x |x\rangle|f(x)\rangle$ with every value $f(x)$ in it. The cost is one query, the same as for one input. A [measurement](/quantum-measurement/) of this state returns one pair $(x, f(x))$ for a uniformly random $x$, which a classical computer gets by picking $x$ at random. A quantum speedup comes only when [interference](/quantum-interference/) makes a global property of $f$ readable before the measurement.

## In plain words

A quantum computer can feed a function all of its inputs at the same time and get back one state that holds all the outputs. This sounds like a huge gain, but there is a catch. The state cannot be read out as a table. A measurement gives one input and its output, chosen at random, and destroys the rest. A coin flip that chooses the input does just as well.

The gain is real only when the question is about the function as a whole, for example whether two outputs are equal, or whether the outputs repeat with some period. Then more gates can make the outputs combine so that the answer to that one question becomes likely. Quantum parallelism prepares the material, and interference does the work.

## The idea

**The state.** Let $U_f|x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$ for $f\colon \{0,1\}^n \to \{0,1\}^m$. The [Hadamard gate](/hadamard-gate/) on each of the $n$ input qubits makes the uniform superposition, and by linearity

$$U_f\Bigl(\frac{1}{\sqrt{2^n}}\sum_{x} |x\rangle\Bigr)|0^m\rangle = \frac{1}{\sqrt{2^n}}\sum_{x} |x\rangle|f(x)\rangle.$$

One application of $U_f$ thus touches all $2^n$ inputs. The two registers are [entangled](/entanglement/) unless $f$ is constant.

**What a measurement gives.** By the [Born rule](/born-rule/), measuring both registers gives each pair $(x, f(x))$ with probability $2^{-n}$. Measuring only the output gives a value $v$ with probability $|f^{-1}(v)|/2^n$ and leaves the input register in the uniform superposition of $f^{-1}(v)$. Neither outcome tells more than one classical evaluation at a random point.

**Why the table cannot be read.** The table of $f$ has $m 2^n$ bits, but the state has only $n + m$ qubits. Holevo's theorem (1973) says that no measurement on $k$ qubits gives more than $k$ bits of information about how they were prepared. So the $2^n$ values are present as amplitudes, but at most $n + m$ bits about them can ever be read out.

**"It tries all answers at once" is wrong.** If a quantum computer could check all inputs at once and report a good one, unstructured search over $N$ items would take one query. Bennett, Bernstein, Brassard and Vazirani (1997) proved that it needs of order $\sqrt N$ queries ([optimality of Grover search](/grover-optimality/)), and relative to an oracle NP is not contained in [BQP](/bqp/). Parallelism is useful only together with a structure of $f$ that interference can use.

**What interference adds.** The amplitude of an outcome after more gates is a sum of contributions from all $x$. If the gates are chosen well, the sum is large for outcomes that encode the global property and cancels for the others. The examples below show this for Deutsch's problem and for a hidden period.

**Clean registers.** A circuit for $f$ in general needs work qubits. If they are not returned to $|0\rangle$ by [uncomputation](/uncomputation/), the state is $\sum_x |x\rangle|f(x)\rangle|g(x)\rangle$ with garbage $g(x)$, and the later interference between different $x$ is lost.

## Examples

**AND of two bits.** Let $n = 2$, $m = 1$ and $f(x_1, x_0) = x_1 \wedge x_0$. One query gives $\frac12(|00\rangle|0\rangle + |01\rangle|0\rangle + |10\rangle|0\rangle + |11\rangle|1\rangle)$. A measurement gives each of the four pairs with probability $\frac14$, so the value $1$ is seen with probability $\frac14$ only.

**Deutsch's problem.** For $f\colon \{0,1\} \to \{0,1\}$, decide whether $f(0) = f(1)$. A classical algorithm needs both values, so two queries. With the output qubit in $|{-}\rangle$, one query on $|{+}\rangle$ gives $\frac{1}{\sqrt2}\bigl((-1)^{f(0)}|0\rangle + (-1)^{f(1)}|1\rangle\bigr)|{-}\rangle$ by [phase kickback](/phase-kickback/). A Hadamard gate then makes the two terms interfere: the input qubit becomes $\pm|0\rangle$ if $f(0) = f(1)$ and $\pm|1\rangle$ otherwise. One query gives $f(0) \oplus f(1)$, but neither $f(0)$ nor $f(1)$.

**Simon's problem.** Let $f(x) = f(x')$ exactly when $x' \in \{x, x \oplus s\}$ for a hidden $s \ne 0$. After one query on the uniform superposition, measuring the output register leaves $\frac{1}{\sqrt2}(|x_0\rangle + |x_0 \oplus s\rangle)$ for a random $x_0$. Hadamard gates on the input then give only strings $y$ with $y \cdot s = 0 \pmod 2$. Order $n$ such strings determine $s$, while a classical algorithm needs of order $2^{n/2}$ queries ([Simon's algorithm](/simon-algorithm/)).

**Period finding.** [Shor's algorithm](/shor-algorithm/) prepares $\sum_x |x\rangle|a^x \bmod N\rangle$ with one run of a modular exponentiation circuit. The values repeat with the order $r$ of $a$, and the [quantum Fourier transform](/quantum-fourier-transform/) turns the period into peaks of amplitude near multiples of $2^n/r$.

**A non-example: search.** Let $f(x) = 1$ for one marked $x$ out of $N = 2^n$. One query gives $\sum_x |x\rangle|f(x)\rangle/\sqrt N$, and the marked item is measured with probability $1/N$, as for a random guess. [Grover search](/grover-search/) needs of order $\sqrt N$ queries, each followed by an interference step.

## Where it is used

- The first query of most oracle algorithms: [Deutsch-Jozsa](/deutsch-jozsa-algorithm/), [Bernstein-Vazirani](/bernstein-vazirani-algorithm/), Simon and Grover, studied in the [quantum query model](/quantum-query-model/).
- Period finding and the hidden subgroup problems that follow it, where the function is a modular exponentiation or a group homomorphism.
- [Quantum phase estimation](/quantum-phase-estimation/), where controlled powers $U^{2^j}$ act on a superposition of the control values.
- Arguments about what quantum computers cannot do: Holevo's theorem and the search lower bound limit how much of the parallel state can be used.

## References
