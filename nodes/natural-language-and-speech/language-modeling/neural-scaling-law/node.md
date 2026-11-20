---
tag: 4D8APH
kind: concept
slug: neural-scaling-law
name: Neural scaling law
aliases:
- Kaplan scaling law
- Chinchilla scaling law
area: natural-language-and-speech/language-modeling
level: research
summary: "Fitted, measured power laws for how the test loss of language models falls with parameters, data and compute. Kaplan et al. (2020) and Hoffmann et al. (2022) fitted different laws."
history:
  year: 2020
  people: [Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, Dario Amodei]
  note: "Kaplan and colleagues at OpenAI fitted power laws to the loss of transformer language models. In 2022 Hoffmann and colleagues at DeepMind fitted new laws with a different split of compute, and trained Chinchilla to test it."
prereqs: [language-model, cross-entropy-loss, transformer]
see_also: [generative-pretrained-transformer, perplexity, zipfs-law, heaps-law, overfitting, learning-rate-schedule, bfgs, in-context-learning]
sources:
  - url: https://arxiv.org/abs/2001.08361
    title: "Jared Kaplan, Sam McCandlish, Tom Henighan and others, Scaling laws for neural language models, 2020"
    locator: "Section 1.1 (summary, including D growing as N to the 0.74 and as C to the 0.27), Section 1.2 (equations 1.1 to 1.3 with alpha_N 0.076, N_c 8.8e13, alpha_D 0.095, D_c 5.4e13, alpha_C 0.050, C_c 3.1e8 PF-days, equation 1.5 and the exponents 0.73 for N), Section 2.1 (C about 6N per token)"
  - url: https://arxiv.org/abs/2203.15556
    title: "Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch and others, Training compute-optimal large language models, NeurIPS 2022"
    locator: "Section 2 (how the work differs from Kaplan et al.), Sections 3.1 to 3.4 and Table 2 (three approaches and the exponents a and b), Table 3 (tokens for each model size by Approach 1), Section 4 (Chinchilla, 70B parameters and 1.4T tokens, 67.5% on MMLU), Appendix D.2 (E = 1.69, A = 406.4, B = 410.7, alpha = 0.34, beta = 0.28)"
  - url: https://arxiv.org/abs/2404.10102
    title: "Tamay Besiroglu, Ege Erdil, Matthew Barnett and Josh You, Chinchilla scaling: A replication attempt, 2024"
    locator: "the abstract (the parametric fit of Approach 3 does not match the data read from the plots, and a refit agrees with Approaches 1 and 2)"
---

A neural scaling law is a fitted formula, usually a power law, that predicts the test loss of a model from its number of parameters $N$, the number of training tokens $D$, or the training compute $C$. For language models the loss is the [cross-entropy](/cross-entropy-loss/) per token on held-out text. These laws are measurements: curves fitted to a set of training runs, on one kind of data, one tokenizer and one family of networks. No theorem says that they hold, and they are used outside the range of the fit at the user's own risk. Two fits are widely used, by Kaplan et al. (2020) and by Hoffmann et al. (2022), and they disagree on how to split a compute budget between $N$ and $D$.

## In plain words

Train many language models of different sizes on different amounts of text, and plot their test loss on log-log axes. The points fall close to straight lines. A straight line on log-log axes is a power law: each time you multiply the model size by ten, the loss is multiplied by about the same factor.

People use such lines to plan. Before a large and expensive training run, they train many small ones, fit the lines, and read off the loss they expect and the best model size for their budget.

The lines are found by experiment, not proved. Two well-known studies drew different lines from different experiments, and so gave different advice on how big a model should be for a given budget.

## The idea

**The fit of Kaplan et al. (2020).** They trained transformer language models on WebText2 and counted $N$ without the embedding parameters. When only one of the three quantities limits the loss, they fitted (Section 1.2):

$$L(N) = (N_c / N)^{\alpha_N}, \quad \alpha_N \approx 0.076, \; N_c \approx 8.8 \times 10^{13},$$

$$L(D) = (D_c / D)^{\alpha_D}, \quad \alpha_D \approx 0.095, \; D_c \approx 5.4 \times 10^{13} \text{ tokens},$$

$$L(C_{\min}) = (C_c / C_{\min})^{\alpha_C}, \quad \alpha_C \approx 0.050, \; C_c \approx 3.1 \times 10^{8} \text{ PF-days},$$

with $L$ in nats per token. The first is for models trained to convergence on enough data, the second for large models stopped early on limited data, and the third for the best model size at each compute. They combined the first two into one law for $N$ and $D$ together (equation 1.5):

$$L(N, D) = \Big[ (N_c / N)^{\alpha_N / \alpha_D} + D_c / D \Big]^{\alpha_D}.$$

From these fits they concluded that, as compute grows, the best model size grows as $N \propto C^{0.73}$ and the data only as $D \propto C^{0.27}$. To avoid overfitting, the data needs to grow as $D \propto N^{0.74}$: a model 8 times larger needs about 5 times more data (Section 1.1).

**The fit of Hoffmann et al. (2022).** They trained more than 400 models, from 70M to over 16B parameters, on 5B to 500B tokens, and used three methods (Section 3).

1. For each model size, vary the number of tokens and take the minimum loss at each compute.
2. For each of nine compute budgets, vary the model size and find the minimum of each curve (IsoFLOP profiles).
3. Fit one formula to all final losses:

$$\hat L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}},$$

with $E = 1.69$, $A = 406.4$, $B = 410.7$, $\alpha = 0.34$ and $\beta = 0.28$ (Appendix D.2). They minimized a Huber loss on the log of the loss with [L-BFGS](/bfgs/). $E$ stands for the loss that no model can remove, the second term for the limit of a model of size $N$, and the third for training on a finite number of tokens.

With $C \approx 6ND$, the best split is $N_{\text{opt}} \propto C^{a}$ and $D_{\text{opt}} \propto C^{b}$. Table 2 gives $a = 0.50$, $b = 0.50$ for Approach 1, $0.49$ and $0.51$ for Approach 2, and $0.46$ and $0.54$ for Approach 3. All three say: grow parameters and tokens in about equal proportion, which comes to about 20 tokens per parameter (Table 3).

**Why the two fits differ.** Hoffmann et al. (Section 2) give two reasons. Kaplan et al. used one fixed number of training tokens and one cosine [learning rate schedule](/learning-rate-schedule/), set for 130B tokens, for all models. So the loss of a run that was stopped early was higher than that of a run whose schedule was set for its own length, which made more data look less useful than it is. Second, most runs of Kaplan et al. were small, many under 100M parameters, while most runs of Hoffmann et al. had more than 500M. Neither paper proves its law; each is a fit to its own runs.

**Replication.** Besiroglu et al. (2024) read the data of Approach 3 from the plots of Hoffmann et al. and report that the published parametric fit does not fit those data and does not agree with Approaches 1 and 2; their own refit does agree with them.

## Examples

**Kaplan's law in $N$.** From equation 1.1, $L(10^8) = 2.83$, $L(10^9) = 2.3756$, $L(10^{10}) = 1.9943$ and $L(10^{11}) = 1.6741$ nats per token. Each factor of 10 in $N$ multiplies the loss by $10^{-0.076} = 0.8395$. The law in $D$ gives $L(10^9) = 2.8156$, $L(10^{10}) = 2.2624$ and $L(10^{11}) = 1.8179$. These hold only in the regimes stated above, and only for WebText2 with that tokenizer.

**Hoffmann's fitted losses.** The formula of Approach 3 gives $\hat L = 1.9366$ for $N = 70\text{B}$, $D = 1.4\text{T}$ (Chinchilla), $1.9933$ for $N = 280\text{B}$, $D = 300\text{B}$ (Gopher) and $2.0023$ for $N = 175\text{B}$, $D = 300\text{B}$ (the size and data of GPT-3). These losses are on their MassiveText data and cannot be compared with Kaplan's numbers.

**Chinchilla.** Gopher has 280B parameters trained on 300B tokens. Chinchilla was trained with the same compute budget but with 70B parameters and 1.4T tokens, 4 times fewer parameters and 4 times more data. It scored 67.5% on the MMLU benchmark, which the abstract calls a gain of more than 7% over Gopher (abstract and Section 4). This is one measurement of the advice of the new fit. The paper puts the budget of Gopher at $5.76 \times 10^{23}$ operations. With the rule $C \approx 6ND$, the two runs come to $5.9 \times 10^{23}$ for Chinchilla and $5.0 \times 10^{23}$ for Gopher, so the rule is rough.

**How sensitive the split is.** Minimize $\hat L$ under $6ND = C$ with the rounded published values and $C = 5.76 \times 10^{23}$: the result is $N_{\text{opt}} = 3.22 \times 10^{10}$ and $D_{\text{opt}} = 2.98 \times 10^{12}$, about 93 tokens per parameter. The exponent is $a = \beta / (\alpha + \beta) = 0.452$. Hoffmann et al. report 40B for Approach 3 at this budget, and 67B and 63B for Approaches 1 and 2. Small changes to five fitted numbers move the best size by tens of billions of parameters, which agrees with the warning of Besiroglu et al.

**Table 3 of Hoffmann et al.** For a compute-optimal run, 1B parameters need 20.2B tokens, 10B need 205.1B, 67B need 1.5T and 175B need 3.7T (Approach 1).

**The 6N rule.** Kaplan et al. (Section 2.1) count about $2N$ operations per token for the forward pass and $6N$ for training. GPT-3 has $N \approx 1.74 \times 10^{11}$ non-embedding parameters and saw 300B tokens, so $6ND \approx 3.13 \times 10^{23}$.

## Where it is used

- **Planning a training run.** Choose $N$ and $D$ for a budget, and predict the loss before training. This is what both papers did; the Chinchilla run tests one such plan.
- **Comparing methods.** A change to the network or the data that shifts the whole curve down is worth more than one that helps only at small sizes. Kaplan et al. found that, within a broad range, the shape of the network (depth against width) mattered much less than $N$.
- **Deciding how far to train.** Kaplan et al. found that, for a fixed compute, the best runs are large models stopped well before convergence. Hoffmann et al. moved the advice towards smaller models on more data.
- **Heuristic beyond the fits.** The laws only predict test loss, not the score on a task. Abilities such as [in-context learning](/in-context-learning/) or chain-of-thought reasoning are measured separately, and some appear only above a model size, which a smooth loss curve does not show. If a model will answer many requests after training, the cost of inference also counts, and a smaller model trained on more tokens than the compute-optimal number may be cheaper overall.
- **Other measured regularities.** Scaling laws sit next to older laws of text such as [Zipf's law](/zipfs-law/) for word frequency and [Heaps' law](/heaps-law/) for vocabulary growth, which are also fits, not theorems.

## References
