---
tag: FCNPC6
kind: concept
slug: algebrization-barrier
name: Algebrization barrier
aliases:
- algebrizing proofs
area: complexity/complexity-classes
level: research
summary: "Aaronson and Wigderson: a proof algebrizes if it holds when one side gets an oracle and the other side its low-degree extension. IP = PSPACE algebrizes, but no such proof settles P versus NP."
prereqs: [relativization, ip-equals-pspace]
see_also: [relativization, baker-gill-solovay-theorem, natural-proofs-barrier, ip-equals-pspace, mip-equals-nexp, schwartz-zippel-lemma, reed-muller-code, algorithmic-method]
sources:
  - paper: doi:10.1145/1490270.1490272
    title: Scott Aaronson and Avi Wigderson, Algebrization, a new barrier in complexity theory, ACM Transactions on Computation Theory 1(1) (2009), Article 2
    locator: Section 2 (extension oracles and the definition of algebrizing inclusions and separations), Section 3 (results that algebrize, including PSPACE in IP and NEXP in MIP) and Section 5 (oracles that block algebrizing proofs of P versus NP and other questions); conference version in STOC 2008, doi 10.1145/1374376.1374481
  - paper: doi:10.1016/0020-0190(88)90199-8
    title: Lance Fortnow and Michael Sipser, Are there interactive protocols for co-NP languages?, Information Processing Letters 28(5) (1988)
    locator: pp. 249 to 251 (the oracle that shows that IP = PSPACE does not relativize)
  - paper: doi:10.1145/2559903
    title: Ryan Williams, Nonuniform ACC circuit lower bounds, Journal of the ACM 61(1) (2014), Article 2
    locator: the section "How do we avoid the barriers?" (oracles relative to which NEXP has ACC circuits, also with an extension oracle)
---

The algebrization barrier is a result of Aaronson and Wigderson (STOC 2008, journal version 2009). It explains why the algebraic methods that proved $\mathsf{IP} = \mathsf{PSPACE}$ cannot settle P versus NP either. Those methods are known not to relativize, so the [relativization](/relativization/) barrier does not apply to them. Aaronson and Wigderson give a finer test. An inclusion *algebrizes* if it holds when the machines of one class get an oracle $A$ and the machines of the other class get a low-degree polynomial extension $\tilde{A}$ of $A$. The known non-relativizing results, such as $\mathsf{IP} = \mathsf{PSPACE}$ and $\mathsf{MIP} = \mathsf{NEXP}$, algebrize. But there are oracles and extensions relative to which $\mathsf{NP} \subseteq \mathsf{P}$, and others relative to which $\mathsf{NP} \not\subseteq \mathsf{P}$. So P versus NP needs methods that do not algebrize.

## In plain words

Some famous proofs get past the old oracle barrier with a trick: they turn a logical formula into a polynomial and evaluate it at numbers other than 0 and 1. A plain oracle answers only yes or no questions, so the trick cannot see inside it. The new test gives one side a richer oracle that also answers questions about the polynomial version of the oracle. With this richer oracle, the famous proofs still work. Then the authors build pairs of oracles of this kind where finding a solution is as easy as checking it, and other pairs where it is not. A proof that uses only the trick works the same way with every such pair, so it cannot settle the question. A new proof must use some other idea.

## The idea

**Extension oracles.** Let $A$ be an oracle, given as Boolean functions $A_m : \{0, 1\}^m \to \{0, 1\}$, one for each length $m$. An *extension* $\tilde{A}$ of $A$ gives, for each $m$ and each finite field $\mathbb{F}$, a polynomial $\tilde{A}_{m, \mathbb{F}} : \mathbb{F}^m \to \mathbb{F}$ that agrees with $A_m$ on $\{0, 1\}^m$ and has degree at most a constant $c$ in each variable. An oracle machine with oracle $\tilde{A}$ can ask for the value of $\tilde{A}_{m, \mathbb{F}}$ at any point of $\mathbb{F}^m$, at the cost of one step. The simplest extension is the *multilinear extension*, which is unique:
$$\tilde{A}_m(x) = \sum_{b \in \{0, 1\}^m} A_m(b) \prod_{i=1}^m \bigl(x_i b_i + (1 - x_i)(1 - b_i)\bigr).$$
The polynomials of degree at most $c$ in each variable form a [Reed-Muller code](/reed-muller-code/), and two different ones agree on a small fraction of points by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/).

**Algebrizing statements.** Aaronson and Wigderson define (Section 2):

- An inclusion $\mathsf{C} \subseteq \mathsf{D}$ *algebrizes* if $\mathsf{C}^A \subseteq \mathsf{D}^{\tilde{A}}$ for every oracle $A$ and every extension $\tilde{A}$ of $A$.
- A separation $\mathsf{C} \not\subseteq \mathsf{D}$ *algebrizes* if $\mathsf{C}^{\tilde{A}} \not\subseteq \mathsf{D}^A$ for every $A$ and every $\tilde{A}$.

The extension always goes to the side that must be stronger. Every relativizing inclusion algebrizes, because $\tilde{A}$ answers every Boolean query of $A$. The definition is not symmetric, and so it is not the same as relativizing with the single oracle $\tilde{A}$.

**Why IP = PSPACE algebrizes.** The proof of [IP = PSPACE](/ip-equals-pspace/) arithmetizes a quantified formula and runs a sumcheck protocol on the polynomial. At the end, the verifier must evaluate the polynomial at one random point of $\mathbb{F}^m$. Fortnow and Sipser (1988) gave an oracle $A$ relative to which coNP has no interactive proof, so this proof does not relativize: if the formula contains oracle gates, then the verifier needs the polynomial version of $A$ at a non-Boolean point, and a Boolean oracle cannot give it. An extension oracle $\tilde{A}$ gives exactly this value. Aaronson and Wigderson show in this way that $\mathsf{PSPACE}^A \subseteq \mathsf{IP}^{\tilde{A}}$ and $\mathsf{NEXP}^A \subseteq \mathsf{MIP}^{\tilde{A}}$ for all $A$ and $\tilde{A}$. They also show that the circuit lower bounds $\mathsf{MA}_{\mathsf{EXP}} \not\subseteq \mathsf{P/poly}$ and $\mathsf{PromiseMA} \not\subseteq \mathsf{SIZE}(n^k)$ algebrize (Section 3).

**The barrier for P versus NP** (Section 5).

- *There are $A$ and $\tilde{A}$ with $\mathsf{NP}^{\tilde{A}} \subseteq \mathsf{P}^A$.* Take $A$ PSPACE-complete and $\tilde{A}$ its multilinear extension. The multilinear extension of a PSPACE language can be computed in polynomial space, by the sum in the formula above over all Boolean points, so $\mathsf{NP}^{\tilde{A}} \subseteq \mathsf{PSPACE} \subseteq \mathsf{P}^A$. This is the collapsing oracle of the [Baker-Gill-Solovay theorem](/baker-gill-solovay-theorem/), made to work with an extension. So $\mathsf{P} \ne \mathsf{NP}$ has no algebrizing proof.
- *There are $A$ and $\tilde{A}$ with $\mathsf{NP}^A \not\subseteq \mathsf{P}^{\tilde{A}}$.* The language is again "is there a string $w$ of length $n$ with $A_n(w) = 1$?", and $A$ is built by diagonalization as in the Baker-Gill-Solovay theorem. The new part is that the deterministic machine can now query the extension at non-Boolean points, and one such value depends on all of $A_n$. Aaronson and Wigderson use extensions of degree 2 in each variable. They show that the oracle can answer the polynomially many queries of the machine consistently while still choosing whether a marked string exists. So $\mathsf{P} = \mathsf{NP}$ has no algebrizing proof either.

They prove similar results for other questions. There are oracles and extensions with $\mathsf{RP}^A \not\subseteq \mathsf{P}^{\tilde{A}}$, so derandomization of RP needs non-algebrizing methods, and with $\mathsf{NEXP}^{\tilde{A}} \subseteq \mathsf{P}^A/\mathsf{poly}$, so a proof that NEXP lacks polynomial-size circuits must also be non-algebrizing. This last result sits next to the algebrizing lower bound for $\mathsf{MA}_{\mathsf{EXP}}$, which shows where the barrier begins.

**What the barrier does not say.** It does not show that P versus NP is independent of any theory, and it says nothing about which answer is true. It shows that arithmetization and the methods built on it are not enough alone.

## Examples

**A multilinear extension over $\mathbb{F}_7$.** Take the oracle on 2 bits that is OR: $A(0, 0) = 0$ and $A(0, 1) = A(1, 0) = A(1, 1) = 1$. The formula above gives the weights $(1 - x_1)(1 - x_2)$, $(1 - x_1) x_2$, $x_1 (1 - x_2)$ and $x_1 x_2$ for the four Boolean points, and the extension is
$$\tilde{A}(x_1, x_2) = x_1 + x_2 - x_1 x_2.$$
It agrees with OR on the four Boolean points. At the point $(2, 3)$ over $\mathbb{F}_7$ the four weights are $2, 4, 3, 6$ for the points $00, 01, 10, 11$, and the value is $4 + 3 + 6 = 13 \equiv 6 \pmod 7$. The formula gives $2 + 3 - 6 = -1 \equiv 6$ too. Now change the oracle at one point, setting $A(1, 1) = 0$. The value at $(2, 3)$ drops by the weight 6 to $0$. One query at a non-Boolean point gives a combination of all four Boolean values, while one Boolean query gives only one of them. For the 3-bit majority function the extension is $x_1 x_2 + x_1 x_3 + x_2 x_3 - 2 x_1 x_2 x_3$, and its value at $(2, 3, 4)$ over $\mathbb{F}_7$ is $6 + 8 + 12 - 48 = -22 \equiv 6$. A script that sums over the Boolean points gives the same values.

**Where the extra power is used.** The value $\tilde{A}(2, 3)$ above is what the IP verifier needs at the last step of a sumcheck protocol that involves the oracle. Without the extension oracle, it would have to compute this value from the Boolean values, and for an oracle on $m$ bits that takes up to $2^m$ queries.

**A result that avoids the barrier.** Williams (2014) proved that NEXP does not have polynomial-size ACC circuits. He writes that the proof avoids relativization and algebrization, because there are oracles $A$ with $\mathsf{NEXP}^A \subseteq \mathsf{ACC}^A$, and even with $\mathsf{NEXP}^{\tilde{A}} \subseteq \mathsf{ACC}^A$ (credited to Aaronson). The proof uses a satisfiability algorithm for ACC circuits that depends on properties of ACC that do not relativize. See [algorithmic method](/algorithmic-method/).

## Where it is used

- **Judging new proof methods.** A method for P versus NP, for NEXP versus P/poly or for derandomization should be checked against both relativization and algebrization. If it only uses black-box simulation, diagonalization and arithmetization, it cannot succeed.
- **Interactive proofs and PCPs.** The results on [interactive proofs](/interactive-proofs/), [MIP = NEXP](/mip-equals-nexp/) and the low-degree methods behind the [low-degree test](/low-degree-test/) are the main examples of algebrizing proofs.
- **The P versus NP problem.** Together with [relativization](/relativization/) and [natural proofs](/natural-proofs-barrier/), it is one of the three known barriers, summarized on the [P versus NP problem](/p-versus-np-problem/) page.
- **Communication complexity.** Aaronson and Wigderson prove some of their oracle results with lower bounds in communication complexity, so new oracle results of this kind often reduce to such lower bounds. See [communication complexity](/communication-complexity/).

## References
