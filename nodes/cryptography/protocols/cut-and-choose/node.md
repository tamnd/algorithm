---
tag: QC3Y6Z
kind: technique
slug: cut-and-choose
name: Cut-and-choose
aliases:
- cut and choose technique
area: cryptography/protocols
level: advanced
summary: A party commits to many copies of an object, the other party opens a random subset to check them, and the unopened copies are used. A cheater who corrupts copies is caught with high probability.
prereqs: [yao-garbled-circuits, malicious-adversary-model]
see_also: [zero-knowledge-proof, chaum-blind-signature, blind-signature, oblivious-transfer-extension, commitment-scheme, secure-multiparty-computation, gmw-protocol, fair-coin-flipping]
sources:
  - paper: doi:10.1007/978-3-540-72540-4_4
    title: "Yehuda Lindell and Benny Pinkas, An efficient protocol for secure two-party computation in the presence of malicious adversaries, EUROCRYPT 2007, LNCS 4515, pages 52 to 78"
    locator: cut-and-choose on garbled circuits with a majority output, and the encoding of the evaluator's input against selective failure
  - paper: doi:10.1007/978-3-642-40084-1_1
    title: "Yehuda Lindell, Fast cut-and-choose based protocols for malicious and covert adversaries, CRYPTO 2013, LNCS 8043, pages 1 to 17"
    locator: independent checking of each circuit and the cheating-punishment step, so that s circuits give error 2 to the minus s
  - paper: doi:10.1007/0-387-34799-2_25
    title: "David Chaum, Amos Fiat and Moni Naor, Untraceable electronic cash, CRYPTO 1988, LNCS 403, pages 319 to 327"
    locator: the bank checks half of the blinded coin candidates before it signs the rest
  - paper: "Chih-hao Shen and abhi shelat, Two-output secure computation with malicious adversaries, EUROCRYPT 2011, LNCS 6632, pages 386 to 405"
    locator: the analysis that checks 60 percent of the circuits
  - paper: "Yonatan Aumann and Yehuda Lindell, Security against covert adversaries, efficient protocols for realistic adversaries, TCC 2007, LNCS 4392, pages 137 to 156"
    locator: covert security, where cheating is caught with a fixed probability, from cut-and-choose with few copies
  - paper: "Jesper Buus Nielsen and Claudio Orlandi, LEGO for two-party secure computation, TCC 2009, LNCS 5444, pages 368 to 386"
    locator: cut-and-choose on single gates, which are then soldered into a circuit
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 4.4 (zero-knowledge proofs for NP, with a commitment and a random challenge on one copy)
  - paper: doi:10.1561/3300000019
    title: "David Evans, Vladimir Kolesnikov and Mike Rosulek, A pragmatic introduction to secure multi-party computation, Foundations and Trends in Privacy and Security 2(2-3), 2018"
    locator: Section 6.1 (cut-and-choose for garbled circuits)
---

Cut-and-choose is a way to force a party to build an object honestly when the object cannot be checked without destroying it. The party makes many copies and commits to all of them. The other party picks a random subset and asks for those copies to be opened in full; it checks them and throws them away. The copies that are left are used, unopened. A cheater who corrupts a few copies is likely to have one of them opened; a cheater who corrupts many copies is sure to. The name comes from the old way to split a cake between two people: one cuts, and the other chooses. The technique appears in [zero-knowledge proofs](/zero-knowledge-proof/), in the electronic cash of Chaum, Fiat and Naor (1988), and most of all in [Yao's garbled circuits](/yao-garbled-circuits/) against a [malicious](/malicious-adversary-model/) garbler.

**Notation.** $s$ is the number of copies (the statistical security parameter is about $s$). $k$ is the number of bad copies the cheater makes. $c$ is the number of copies checked and $e = s - c$ the number evaluated, when the check set has a fixed size.

## In plain words

You want a friend to make a sealed box that does a job, but you cannot look inside without breaking it. So you ask for many boxes, all sealed. You pick some of them at random and break those open to check them. If any of them is faulty, your friend has cheated and you stop. If they are all fine, you use the boxes you did not open.

A friend who makes only one faulty box is likely to get away with it, but then most of the boxes you use are good. To make you use bad boxes, the friend must make many of them, and then you are almost sure to open one. The right way to combine the boxes you use, and the right number to open, decide how small the chance of escape is.

## When it applies

- **An object that is checked by opening it.** A garbled circuit, a blinded message, or a committed permutation can be verified once the hidden randomness is revealed, but then it can no longer be used in secret.
- **Cheap copies.** Making and sending $s$ copies must be affordable. For garbled circuits this is the main cost: $s$ times the honest protocol.
- **Commit before choose.** The checker's choice must be fixed after the builder is bound to all copies, by a [commitment](/commitment-scheme/) or by having already sent them, and it must be unpredictable to the builder.
- **A rule for the unopened copies.** The used copies must be combined so that a few bad ones do no harm: a majority vote, a check that all agree, or a step that punishes any disagreement.
- **Consistency between copies.** Each copy must be used with the same inputs, or the cheater can feed different inputs to different copies. This needs its own check.

## The template

```pseudo id=main
CUT-AND-CHOOSE(builder, checker, s)
L1  the builder makes s copies and commits to all of them
L2  the checker picks a random check set C ⊆ {1, ..., s}, after the commitments
L3  for each i ∈ C: the builder opens copy i in full; if it is wrong, the checker aborts and the cheat is caught
L4  for each i ∉ C: the copy is used in the protocol without opening it
L5  the results of the used copies are combined (by majority, or by "any good one wins")
```

**Escape probability with a majority (fixed check set).** Suppose the check set is a uniform set of $c$ copies, and the output is the majority of the $e$ evaluated ones. The cheater wins if no bad copy is checked and the bad copies are a strict majority of the evaluated ones: $e/2 < k \le e$. All $c$ checked copies must come from the $s - k$ good ones, and each set of $c$ copies is equally likely, so

$$\Pr[\text{escape} \mid k] = \frac{\binom{s-k}{c}}{\binom{s}{c}} \quad \text{if } \frac{e}{2} < k \le e, \text{ and } 0 \text{ otherwise}.$$

The cheater picks the best $k$, which is the smallest that wins the vote, $k = \lfloor e/2 \rfloor + 1$. For $s = 10$ and $c = 5$, the best is $k = 3$, with $\binom{7}{5} / \binom{10}{5} = 21/252 = 1/12$. The error decreases like $2^{-0.32 s}$ for large $s$, so about $120$ circuits are needed for $2^{-40}$ when 60 percent are checked.

**Escape probability with cheating punishment (Lindell 2013).** Each copy is checked on its own with probability $1/2$. If the evaluated copies give different outputs, the evaluator obtains the builder's input (by a small extra secure computation) and computes the right output itself; so a single good evaluated copy gives the right answer. The cheater wins only if every checked copy is good and every evaluated copy is bad: the evaluated set must be exactly the bad set. Its probability is

$$\Pr[\text{escape} \mid k] = \left(\tfrac12\right)^{s-k} \left(\tfrac12\right)^{k} = 2^{-s} \quad \text{for every } k \ge 1.$$

So $s = 40$ circuits give $2^{-40}$, about three times fewer than with a majority.

**The code.** The implementation runs the template on copies that are flags, good or bad, with a cheating garbler that corrupts $k$ of $s$ circuits. It computes the two exact formulas and compares them with Monte Carlo runs at $s = 10$: four $(c, k)$ pairs for the majority rule, and $k = 1, 5, 10$ plus a biased check probability for the Lindell rule. It also finds the smallest $s$ for $2^{-40}$: 40 with cheating punishment, and 120 with a majority and 60 percent checked. The simulation does not garble real circuits; the [garbled circuits page](/yao-garbled-circuits/) has that. There are no official test vectors. The code is for study only and is not constant time; use a maintained framework such as EMP-toolkit for real malicious two-party computation.

## Classic examples

**Garbled circuits against a malicious garbler.** A garbler can build a circuit that computes a different function, for example one that outputs the evaluator's input. The evaluator cannot see this from the garbled tables. Lindell and Pinkas (2007) have the garbler send $s$ circuits, open about half to check that they compute the agreed function, and evaluate the rest, taking the majority output. Lindell (2013) checks each circuit with probability $1/2$ and adds cheating punishment, which reduces $s$ to 40 for an error of $2^{-40}$.

**Electronic cash.** In the scheme of Chaum, Fiat and Naor (1988), a user asks the bank for a [blind signature](/chaum-blind-signature/) on a coin that must encode the user's identity, so that spending it twice reveals the identity. The bank cannot see the blinded coin. So the user prepares $2k$ blinded candidates, the bank asks for $k$ of them to be unblinded and checks that they are well formed, and it signs the product of the other $k$.

**Zero-knowledge proofs.** In Blum's protocol for Hamiltonian cycles, the prover commits to a randomly permuted copy of the graph. The verifier asks either to open the whole copy (to check that it is the graph) or to open only the cycle in it (to check that a cycle exists). Each challenge is a cut-and-choose with one copy and error $1/2$; $s$ independent rounds reduce the error to $2^{-s}$. Most [zero-knowledge proofs](/zero-knowledge-proof/) for NP have this form.

**Malicious OT extension.** The first actively secure versions of [OT extension](/oblivious-transfer-extension/) used cut-and-choose on the receiver's columns; the consistency check of Keller, Orsini and Scholl (2015) later replaced it.

## Variations

- **Fixed-size check set or independent coins.** A fixed number $c$ of checked copies gives the hypergeometric formula; independent coins for each copy give the clean $2^{-s}$ of Lindell (2013). Shen and Shelat (2011) showed that checking 60 percent, rather than half, is better for the majority rule.
- **Cheating punishment.** Instead of a majority, any disagreement among the evaluated copies lets the honest party learn the cheater's input. Then one good copy suffices.
- **Covert security.** With few copies, for example $s = 2$ with one checked, the cheater is caught with probability $1/2$. Aumann and Lindell (2007) define *covert* security for this case: cheating is possible but is caught with a fixed probability, which deters a party that cares about its reputation.
- **Batch and amortized.** When the same function is evaluated many times, the builder makes a large pool of circuits, a fraction is checked, and the rest are put into small random buckets, one bucket per evaluation. The number of circuits per evaluation then drops to a handful.
- **LEGO.** Nielsen and Orlandi (2009) apply cut-and-choose to single gates instead of whole circuits, and then join ("solder") the good gates into a circuit.
- **Input consistency and selective failure.** The builder can also attack through the evaluator's inputs: in the OT for an input wire, it offers a good key for bit 0 and a bad key for bit 1. The evaluator aborts exactly when its bit is 1, so the abort reveals the bit, and checking circuits does not help. Lindell and Pinkas (2007) encode each input bit as $s$ random bits whose XOR is the bit. Corrupting fewer than all $s$ encoded wires gives an abort probability that does not depend on the input; corrupting all of them leaks the bit only when no abort happens, with probability $2^{-(s-1)}$. The test checks these probabilities exactly and by sampling.

## Pitfalls

- **Predictable choice.** If the builder can predict the check set, it corrupts only the other copies. The checker's coins must be fresh and fixed after the commitments; if both parties must agree on them, use [coin flipping](/fair-coin-flipping/).
- **Inconsistent inputs.** The builder may use different inputs in different evaluated copies, for example to learn which one the majority comes from. The protocol must prove that all copies use the same input.
- **Selective failure.** An abort, or the lack of one, is information. An abort that depends on the honest party's input leaks it, as in the attack above.
- **Counting only the checked copies.** With a majority rule, the bound $\binom{s-k}{c}/\binom{s}{c}$ is not the whole story: the cheater only needs a majority of the evaluated copies, not all of them. Using the probability that all bad copies escape the check, with $k = e$, overstates security.
- **Cost.** $s$ copies cost $s$ times the work and the communication. At $s = 40$ this is still a large factor; protocols based on authenticated garbling or on [GMW](/gmw-protocol/) with MACs avoid it.

## Exercises

1. For $s = 10$ and $c = 6$, find the cheater's best $k$ and its escape probability under the majority rule. (The test checks it against sampling.)
2. Show that with independent checking with probability $q$ for each copy and cheating punishment, the escape probability with $k$ bad copies is $q^{s-k}(1-q)^k$, and that $q = 1/2$ minimizes its maximum over $k$ when $s$ is large.
3. In the selective failure attack with the XOR encoding of $s$ bits, prove that the abort probability is $1 - 2^{-|S|}$ for every input when the corrupted set $S$ has fewer than $s$ wires.
4. In the e-cash example, the bank opens $k$ of $2k$ candidates. What is the chance that a user who makes $j$ bad candidates gets a signature on a product that contains a bad one?
5. Explain why Blum's protocol needs both kinds of challenge: what can a cheating prover do if the verifier only ever asks to open the whole copy, and what if it only ever asks for the cycle?

## References
