---
tag: STSGVR
kind: concept
slug: quantitative-information-flow
name: Quantitative information flow
aliases:
- QIF
- leakage quantification
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Measures how much a program leaks about its secret in bits, as the drop in an attacker's uncertainty after seeing the output.
prereqs: [shannon-entropy, min-entropy, noninterference]
see_also: [min-entropy-leakage, g-leakage, min-entropy-leakage-bound, conditional-entropy, channel-capacity, covert-channel, declassification, side-channel-attack]
sources:
  - paper: doi:10.1007/978-3-642-00596-1_21
    title: Geoffrey Smith, On the foundations of quantitative information flow, Proceedings of FoSSaCS 2009, LNCS 5504
    locator: pp. 288 to 302; Section 4 (programs on which Shannon leakage misjudges the one-guess threat) and Section 5 (vulnerability, min-entropy leakage, the password checker and the election example)
  - paper: doi:10.3233/JCS-2007-15302
    title: David Clark, Sebastian Hunt and Pasquale Malacaria, A static analysis for quantifying information flow in a simple imperative language, Journal of Computer Security 15(3), 2007
    locator: pp. 321 to 371, Shannon leakage of while programs and a static analysis that bounds it
  - paper: doi:10.1145/1315245.1315282
    title: Boris Köpf and David Basin, An information-theoretic model for adaptive side-channel attacks, Proceedings of ACM CCS 2007
    locator: pp. 286 to 296, the leakage of an adaptive attacker who chooses inputs and observes a side channel
  - paper: doi:10.1109/CSF.2012.26
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Catuscia Palamidessi and Geoffrey Smith, Measuring information leakage using generalized gain functions, Proceedings of CSF 2012
    locator: pp. 265 to 279, gain functions, g-leakage and the comparison of capacities
  - book: isbn:9783319961293
    title: Mario S. Alvim, Konstantinos Chatzikokolakis, Annabelle McIver, Carroll Morgan, Catuscia Palamidessi and Geoffrey Smith, The Science of Quantitative Information Flow, Springer, 2020
    locator: Part I and Part II (secrets, channels, vulnerability, leakage and capacity)
---

Quantitative information flow (QIF) measures how much a program or a system tells an observer about a secret. [Noninterference](/noninterference/) asks a yes or no question: can the public output depend on the secret at all? Most useful programs fail it on purpose. A password checker tells the user whether the guess was right, and an election reveals the tally. QIF replaces the yes or no answer with a number. It models the system as a channel from secrets to observations, models the attacker's knowledge as a probability distribution, and reports the leakage in bits as the drop in the attacker's uncertainty. The measure of uncertainty must fit the attacker. This choice is the main design decision in the field.

## In plain words

Before running the program, the attacker has some idea of what the secret could be. After seeing the output, the attacker knows more. QIF asks how much more. Uncertainty is measured in bits, so a leak of 3 bits means, roughly, that the attacker's set of likely secrets got 8 times smaller. A program that reveals nothing leaks 0 bits. A program that prints the secret leaks all of it. Everything in between is a matter of degree, and the right measure depends on what the attacker wants: one correct guess, several tries, or a value close enough to the truth.

## The idea

**Secrets, priors and channels.** The secret $X$ takes values in a finite set $\mathcal X$. The attacker's knowledge before the run is a prior distribution $\pi$ on $\mathcal X$. The system is a channel: a matrix $C$ with $C[x, y] = P(Y = y \mid X = x)$ for each observable output $y$. A deterministic program has one 1 per row. The observation $y$ turns $\pi$ into a posterior distribution $p(x \mid y)$ by [Bayes' theorem](/bayes-theorem/). The observation is whatever the model says the attacker sees: a printed value, a running time or the state of a shared resource. The guarantee covers only that observation.

**Leakage as a drop in uncertainty.** Pick an uncertainty measure $H$ on distributions and its conditional form $H(\pi, C)$, the expected uncertainty after the output. The leakage is

$$ \text{leakage} = H(\pi) - H(\pi, C). $$

The capacity of the channel is the largest leakage over all priors. It does not depend on what the attacker knows in advance, which makes it the usual worst-case figure.

**The choice of measure.** Three measures are in common use, and they can rank the same pair of programs in opposite order.
- **Shannon leakage.** With [Shannon entropy](/shannon-entropy/) and [conditional entropy](/conditional-entropy/), the leakage is the mutual information $H(X) - H(X \mid Y)$, and the capacity is the Shannon [channel capacity](/channel-capacity/). It measures the expected number of bits needed to describe the secret. Early work on covert channels and the static analysis of Clark, Hunt and Malacaria (2007) use it.
- **Min-entropy leakage.** With [min-entropy](/min-entropy/), $H_\infty(\pi) = -\log_2 \max_x \pi(x)$, the leakage measures how much the output raises the chance of guessing the secret in one try. Smith (2009) proposed it because Shannon leakage can call a program safe when it lets the attacker guess the secret often. See [min-entropy leakage](/min-entropy-leakage/).
- **g-leakage.** A gain function scores each guess against each secret, which models attackers with several tries or partial goals. Min-entropy leakage is one case. See [g-leakage](/g-leakage/).

All QIF pages on this site measure entropy and leakage in bits, with $\log_2$.

**Facts that hold for these measures.** Each is a theorem for min-entropy leakage and g-leakage, and the first two also hold for Shannon leakage.
- Leakage is never negative: an attacker can ignore the output.
- Processing the output further cannot increase leakage.
- A channel that satisfies noninterference, so that every row of $C$ is the same, leaks 0 bits. The converse fails for min-entropy leakage: a channel can leak 0 bits to a one-try attacker under a given prior while its output still depends on the secret.
- The [min-capacity bound](/min-entropy-leakage-bound/) gives the worst case in closed form, $\log_2 \sum_y \max_x C[x, y]$, and a deterministic program with $m$ outputs leaks at most $\log_2 m$ bits under every prior. The min-capacity is also at least the Shannon capacity and at least every g-capacity.

**Adversary.** Unless a page states otherwise, the attacker knows the prior and the channel, sees one output and has unbounded computing power. An adaptive attacker who chooses inputs and runs the system many times needs a model of the whole interaction; Köpf and Basin (2007) give one for side channels.

## Examples

**The last two bits.** Let $h$ be uniform on $\{0, \ldots, 7\}$ and let the program output $h \bmod 4$. Each output is equally likely and leaves two secrets. Shannon leakage and min-entropy leakage both equal 2 bits, and the one-try chance of guessing $h$ goes from $1/8$ to $1/2$.

**A password check.** Let $h$ be uniform on 8 values and let the output be whether a guess equals $h$. The Shannon leakage is the entropy of the output, $H(1/8) = 0.544$ bits. The min-entropy leakage is 1 bit: the attacker's chance goes from $1/8$ to $1/4$. The program fails noninterference, yet a single check leaks little. Repeated checks are a different system: an attacker who may test every value learns the whole secret.

**An election.** Following Smith (2009), suppose each of $k$ voters picks one of two candidates independently with probability $1/2$, and the system reveals the number of votes for the first candidate. The secret is the vector of $k$ votes, with $2^k$ equally likely values, and the output has $k + 1$ possible values. The min-entropy leakage is $\log_2(k + 1)$ bits. For $k = 10$ it is $3.459$ bits, and the chance of guessing every vote rises from $1/1024$ to $11/1024$.

**Two measures that disagree.** Let $h$ be uniform on 8-bit values. Program A outputs $h$ when $h$ is a multiple of 8 and outputs 1 otherwise. Program B outputs the last three bits of $h$. Shannon leakage rates A at 1.169 bits and B at 3 bits. But A reveals the whole secret one time in eight, and min-entropy leakage rates it at $\log_2 33 = 5.044$ bits against 3 bits for B. The numbers come from the exact calculation on the [min-entropy leakage](/min-entropy-leakage/) page.

**A noisy channel.** The [binary symmetric channel](/binary-symmetric-channel/) with crossover probability 0.1 has Shannon capacity $1 - H(0.1) = 0.531$ bits and min-capacity $\log_2 1.8 = 0.848$ bits. The two capacities answer different questions: how many bits per use can a sender and a receiver who cooperate get through with coding, and how much does one use help a one-try guesser.

## Where it is used

- **Covert channel analysis.** The bandwidth of a [covert channel](/covert-channel/) is a capacity in bits per unit time. Since few channels can be closed completely, the practical question is often whether the bandwidth is low enough, not whether it is zero.
- **Side channels.** A running time, a cache state or a power trace is an output of a channel from the key or the input. Bounding the number of distinct observations bounds the min-entropy leakage; see the [min-capacity bound](/min-entropy-leakage-bound/). Köpf and Basin (2007) model adaptive [side-channel attacks](/side-channel-attack/) in this setting.
- **Program analysis.** Static analyses bound the Shannon or min-entropy leakage of a program, for example by bounding the number of its outputs. Clark, Hunt and Malacaria (2007) give such an analysis for a small imperative language.
- **Declassification policies.** A [declassification](/declassification/) policy may allow a program to release some information, and QIF can state how much: at most $k$ bits for a stated measure and adversary.
- **Privacy of released data.** Gain functions model attackers who want to learn a property of a person's record, such as an attribute value, rather than the whole record.

## References
