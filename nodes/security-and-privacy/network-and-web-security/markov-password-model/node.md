---
tag: Q34M2V
kind: algorithm
slug: markov-password-model
name: Markov password model
aliases:
- n-gram password model
area: security-and-privacy/network-and-web-security
level: advanced
summary: "Estimates password strength with a character n-gram model trained on a password list. A password scores -log2 of its probability, and its guess number is its rank under the model."
model: word-ram
complexity:
  vars: {n: the length of the password, k: the order of the model (characters of context), T: the number of symbols in the padded training list}
  time: {worst: Θ(n k), average: Θ(n k), best: Θ(n k)}
  space: {extra: O(k)}
properties: {deterministic: true, online: true}
history:
  year: 2005
  people: [Arvind Narayanan, Vitaly Shmatikov, Claude Castelluccia, Markus Duermuth, Daniele Perito, Matteo Dell'Amico, Maurizio Filippone]
  note: "Narayanan and Shmatikov modeled passwords with character Markov chains in 2005. Castelluccia, Duermuth and Perito built adaptive strength meters on them in 2012, and Dell'Amico and Filippone gave a Monte Carlo estimate of guess numbers in 2015."
prereqs: [n-gram-language-model, markov-chain, laplace-smoothing]
see_also: [pcfg-password-model, honeywords, password-hashing, kneser-ney-smoothing, good-turing-estimation, shannon-entropy, min-entropy]
sources:
  - paper: "Arvind Narayanan and Vitaly Shmatikov, Fast dictionary attacks on passwords using time-space tradeoff, ACM CCS 2005, pages 364 to 372"
    locator: the Markov models of passwords and the threshold on the probability of a string
  - paper: "Claude Castelluccia, Markus Duermuth and Daniele Perito, Adaptive password-strength meters from Markov models, NDSS 2012"
    locator: "the n-gram model of the meter, its training on the password list of the service, and the score as minus the log of the probability"
  - paper: "Jerry Ma, Weining Yang, Min Luo and Ninghui Li, A study of probabilistic password models, IEEE Symposium on Security and Privacy 2014, pages 689 to 704, doi:10.1109/SP.2014.50"
    locator: "the comparison of Markov and PCFG models, smoothing, the end symbol and normalization, and probability threshold graphs"
  - paper: "Matteo Dell'Amico and Maurizio Filippone, Monte Carlo strength evaluation, fast and reliable password checking, ACM CCS 2015, pages 158 to 169, doi:10.1145/2810103.2813631"
    locator: the estimator of the guess number from a sample of the model and its unbiasedness
---

A Markov password model estimates how strong a password is. It is a character [n-gram model](/n-gram-language-model/) trained on a password list: each character is predicted from the $k$ characters before it, and an end symbol closes the string. The trained model gives each password $w$ a probability $P(w)$. The strength is $-\log_2 P(w)$ bits, and the guess number is the rank of $w$ when all strings are sorted by decreasing probability, which is the number of guesses that a guesser who knows the model would need. Scoring is one pass over the password, $\Theta(nk)$ time for a password of $n$ characters. Both numbers are estimates under the model and its training list: they say how a password compares with the habits seen in the list, not how hard it is to guess for every attacker. The model is a [Markov chain](/markov-chain/) on contexts, and its counts are smoothed, here with [additive smoothing](/laplace-smoothing/), so that a string not seen in training still has a probability.

## In plain words

People choose passwords in patterns. Some letters often follow others, many passwords end in a digit, and short words are common. A model that has read a long list of passwords learns how often each character comes after the few characters before it.

To judge a new password, the model reads it one character at a time and asks how likely each next character was. It multiplies these chances. A password made of common steps gets a high chance and is weak. A password with rare steps gets a tiny chance and is strong. A strength meter turns the chance into a score, and it can also estimate how many more likely passwords exist, which says how many guesses a careful guesser would need.

## The problem

The input is a training list of passwords over an alphabet $\Sigma$, an order $k \ge 0$, a smoothing constant $\delta \ge 0$, and a password $w$. Let $\sigma = |\Sigma| + 1$, counting the end symbol $\dashv$. Each password in the list is padded with $k$ start symbols $\triangleright$ in front and $\dashv$ at the end. For each context $c$ of $k$ symbols and each next symbol $a$, training counts $N(c, a)$, the number of times $a$ follows $c$, and $N(c) = \sum_a N(c, a)$. The model is

$$ P(a \mid c) = \frac{N(c, a) + \delta}{N(c) + \delta\sigma}, \qquad P(w) = \prod_{i=1}^{|w|+1} P(w_i \mid c_i), $$

where $w_{|w|+1} = \dashv$ and $c_i$ is the last $k$ symbols before position $i$. The outputs are the strength $-\log_2 P(w)$ and the guess number $1 + |\{v : P(v) > P(w)\}|$.

## The algorithm

```pseudo id=main
MARKOV-SCORE(w, N, k, δ, σ)
L1  c ← ▷^k ; p ← 1                    ▷ k start symbols
L2  for i ← 1 to |w| + 1 do
L3      a ← w[i] if i ≤ |w|, else ⊣     ▷ the end symbol
L4      p ← p · (N(c, a) + δ) / (N(c) + δσ)
L5      c ← the last k symbols of c·a
L6  return -log2 p
```

Training is one pass over the padded list that adds 1 to $N(c, a)$ and $N(c)$ for each symbol. Line L4 is the smoothed probability of the next symbol; with $\delta = 0$ it is the maximum likelihood estimate, and an unseen step gives probability 0 and strength $+\infty$. The end symbol of line L3 makes $P$ a distribution over strings of all lengths, so that a long password is not scored as if it were a prefix of a longer one. The code keeps $p$ as an exact fraction and computes the logarithm from its numerator and denominator.

**Guess numbers.** The exact guess number counts the strings with a higher probability. A prefix has a probability at least as large as each string that extends it, so a search over prefixes can skip each prefix whose probability is already at most $P(w)$. This is exact but can take time proportional to the guess number. Dell'Amico and Filippone (2015) estimate it instead from $m$ strings $S_1, \ldots, S_m$ drawn from the model: each $S_j$ with $P(S_j) > P(w)$ stands for $1/(m P(S_j))$ strings, and the sum is an unbiased estimate of the count. The code returns only the probabilities of the drawn strings, not the strings.

## Example

The training list is made up: `ab1`, `ab11`, `abab`, `b1`, `ba1`, `a1`, `ab` and `bb1`, over the alphabet $\{a, b, 1\}$. With $k = 1$ there are four contexts: the start, with $N = 8$; `a`, with $N = 7$; `b`, with $N = 9$; and `1`, with $N = 7$. With $\delta = 1$ and $\sigma = 4$, scoring $w =$ `ab1` goes as follows.

| $i$ | context $c$ | symbol $a$ | $N(c, a)$ | $N(c)$ | $P(a \mid c)$ | $p$ after line L4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | start | `a` | 5 | 8 | 6/12 | 1/2 |
| 2 | `a` | `b` | 5 | 7 | 6/11 | 3/11 |
| 3 | `b` | `1` | 4 | 9 | 5/13 | 15/143 |
| 4 | `1` | end | 6 | 7 | 7/11 | 105/1573 |

So $P(\texttt{ab1}) = 105/1573$ and the strength is $-\log_2(105/1573) \approx 3.91$ bits. Only 4 strings have a higher probability, so the guess number is 5. The other strings score as follows.

| password | $P(w)$ | strength in bits | guess number |
| --- | --- | --- | --- |
| `ab1` | 105/1573 | 3.91 | 5 |
| `ba` | 1/143 | 7.16 | 24 |
| `1b` | 1/572 | 9.16 | 50 |
| `b1a` | 5/4719 | 9.88 | 80 |

The password `1b` is short, but it starts with a digit and puts a letter after a digit, which no password of the list does, so it scores higher than the longer `ab1`. On a real list the numbers are much larger, but the ordering logic is the same.

## Correctness

Line L2 keeps the invariant that before step $i$, $c$ is the context $c_i$ and $p$ is the product of the first $i - 1$ factors, so line L6 returns $-\log_2 P(w)$. For $\delta > 0$ the probabilities of all finite strings sum to 1: the mass of the strings of length at most $L$ plus the mass of the prefixes of length $L + 1$ is exactly 1 for each $L$, and the second part shrinks geometrically because each context gives the end symbol a probability of at least $\delta / (N(c) + \delta\sigma)$. With $\delta = 0$ the counts are the maximum likelihood model of the list. The exact guess number search is correct because a prefix is at least as probable as each of its extensions, and the Monte Carlo estimate is unbiased because each string $v$ is drawn with probability $P(v)$ and weighted by $1/P(v)$. The full proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Scoring.** Line L4 runs $n + 1$ times, each with a hash table lookup of a context of $k$ symbols, so the time is $\Theta(nk)$ on the word-RAM, or $\Theta(n)$ for a fixed order. The extra space is $O(k)$ for the context.
- **Training.** One lookup for each of the $T$ symbols of the padded list, so $O(Tk)$ time. The model stores at most $T$ contexts, and in the worst case $|\Sigma|^k$ of them can appear, which is why orders above 4 or 5 need much data and strong smoothing.
- **Exact guess numbers.** The pruned search visits each string it counts and the prefixes on the way, so its time grows with the guess number. It is only for small models, as in the test.
- **Monte Carlo guess numbers.** Drawing $m$ strings costs $O(m \ell |\Sigma|)$ for strings of length at most $\ell$. After sorting the $m$ probabilities and taking suffix sums of $1/(mP)$, each estimate is a binary search, $O(\log m)$.

## Properties

- **An estimate, not a measure.** The score depends on the training list, the order and the smoothing. A password that is rare in the list can still be common elsewhere, and a model trained on one population can misjudge another.
- **A proper distribution.** With an end symbol and $\delta > 0$, the probabilities of all strings sum to 1, so probabilities of different lengths can be compared.
- **Exact arithmetic.** The code multiplies fractions, so equal probabilities are equal and ties in the guess number are well defined.
- **Online.** A meter can update $p$ after each typed character with one step of line L4.

## Variants and improvements

- **Order and backoff.** Orders between 2 and 5 are common. When a context is rare, backoff or interpolation with lower orders, or [Kneser-Ney smoothing](/kneser-ney-smoothing/) and [Good-Turing estimation](/good-turing-estimation/), give better probabilities than a single additive $\delta$. Ma et al. (2014) found that the choice of smoothing and normalization has a large effect on the results.
- **Normalization by length.** Instead of an end symbol, a model can generate the length first and then the characters; the end symbol is the simpler way to get a distribution over all lengths.
- **Adaptive meters.** Castelluccia, Duermuth and Perito (2012) trained the model on the passwords of the service itself, so the meter follows the habits of its own users.
- **Comparison with grammars.** The [PCFG password model](/pcfg-password-model/) splits a password into segments of letters, digits and symbols. The two models can be compared by their guess numbers on a held-out list.

## When to use it

Use a Markov model to estimate strength in a meter or to compare password policies on a test list. It needs only a training list and counts, it scores in one pass, and its probabilities are well defined for any string. A PCFG model is closer to how people build passwords from words and digits, and a dictionary-based meter catches known words better; Ma et al. (2014) found that well-smoothed Markov models did at least as well as PCFG models in their study. Neither model gives a security guarantee: for stored passwords, use slow [password hashing](/password-hashing/), and to detect a stolen password file, use [honeywords](/honeywords/).

## Pitfalls

- **No end symbol.** If line L3 stops at $i = |w|$, the product is the probability of $w$ as a prefix. A password then never has a higher probability than its own prefixes, the probabilities of strings of different lengths do not sum to 1, and they cannot be compared. Line L3 must include the end symbol.
- **No smoothing.** With $\delta = 0$ in line L4, any step not seen in training gives probability 0 and an infinite strength, even for a weak password with one unusual character. Use $\delta > 0$ or a backoff to a lower order.
- **Floating point underflow.** A product of many small factors in line L4 can round to 0 in floating point. Add logarithms instead, or keep exact fractions, as the code does.
- **A wrong context update.** If line L5 keeps the first $k$ symbols instead of the last $k$, each step uses a stale context. The context is the last $k$ symbols of $c \cdot a$.
- **Reading the score as a guarantee.** A high score means that the password is unlike the training list, not that it is safe against an attacker with another list.

## Implementations

## History

Shannon used n-gram models of text in 1951 to estimate the entropy of English. Narayanan and Shmatikov (2005) applied character Markov models to passwords. Castelluccia, Duermuth and Perito (NDSS 2012) used n-gram models for adaptive strength meters. Ma, Yang, Luo and Li (2014) compared Markov and PCFG models with probability threshold graphs and showed the effect of smoothing and normalization. Dell'Amico and Filippone (2015) gave the Monte Carlo estimate of the guess number, which makes the comparison of models on large lists practical.

## References
