---
tag: KDNB49
kind: concept
slug: in-context-learning
name: In-context learning
aliases:
- few-shot prompting
area: natural-language-and-speech/language-modeling
level: research
summary: A pretrained language model does a new task from an instruction and a few solved examples in its prompt, with no change to its weights. How well it works is measured, not proved.
history:
  year: 2020
  people: [Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Dario Amodei]
  note: "Brown and colleagues at OpenAI named the term in the GPT-3 paper and measured GPT-3 in the zero-shot, one-shot and few-shot settings. GPT-2 had shown zero-shot task behavior in 2019."
prereqs: [language-model, generative-pretrained-transformer, transformer]
see_also: [chain-of-thought-prompting, instruction-tuning, neural-scaling-law, retrieval-augmented-generation, k-nearest-neighbors, ordinary-least-squares, hidden-markov-model, bayesian-inference]
sources:
  - url: https://arxiv.org/abs/2005.14165
    title: "Tom B. Brown, Benjamin Mann, Nick Ryder and others, Language models are few-shot learners, NeurIPS 2020"
    locator: "Section 1 and footnote 1 (the term in-context learning), Figure 1.3 (aggregate of 42 benchmarks against model size), Section 2 (the zero-shot, one-shot and few-shot settings, K from 10 to 100, n_ctx = 2048), Section 3.2 and Table 3.3 (closed-book TriviaQA), Appendix H and Table H.1 (scores for every model size)"
  - url: https://arxiv.org/abs/2102.09690
    title: "Tony Z. Zhao, Eric Wallace, Shi Feng, Dan Klein and Sameer Singh, Calibrate before use: Improving few-shot performance of language models, ICML 2021"
    locator: "Section 3 (accuracy against the choice and order of the examples, 54.3% to 93.4% on SST-2), Section 4 (majority label, recency and common token bias), Section 5 and equation 1 (contextual calibration, W = diag of p_cf inverted, b = 0), abstract (gains of up to 30.0 points)"
  - url: https://arxiv.org/abs/2202.12837
    title: "Sewon Min, Xinxi Lyu, Ari Holtzman and others, Rethinking the role of demonstrations: What makes in-context learning work?, EMNLP 2022"
    locator: "abstract (random labels barely hurt, over 12 models including GPT-3; the label space, the input distribution and the format matter)"
  - url: https://arxiv.org/abs/2208.01066
    title: "Shivam Garg, Dimitris Tsipras, Percy Liang and Gregory Valiant, What can transformers learn in-context? A case study of simple function classes, 2022"
    locator: "abstract (transformers trained from scratch learn linear functions in context, with error close to least squares)"
  - url: https://arxiv.org/abs/2111.02080
    title: "Sang Michael Xie, Aditi Raghunathan, Percy Liang and Tengyu Ma, An explanation of in-context learning as implicit Bayesian inference, ICLR 2022"
    locator: "abstract (the mixture of hidden Markov models, the proof, and the GINC data set)"
---

In-context learning is what a pretrained [language model](/language-model/) does when it performs a task that is given only in its input: an instruction, and in some cases a few solved examples, followed by a new query. The weights do not change. The "learning" happens inside one forward pass. Brown et al. (2020) name three settings by the number $K$ of solved examples: zero-shot ($K = 0$, an instruction only), one-shot ($K = 1$) and few-shot ($K$ from about 10 to 100, as many as fit in the context). Do not confuse it with fine-tuning, which changes the weights with labeled examples, or with [instruction tuning](/instruction-tuning/), which is fine-tuning on many tasks written as instructions, so that zero-shot prompts work better later. [Chain-of-thought prompting](/chain-of-thought-prompting/) is a kind of in-context learning whose examples include the reasoning steps. All that is known about how well in-context learning works on real models is measured. No theorem guarantees it.

## In plain words

You give a trained text model a short task description and a few solved examples, then a new question in the same format. The model continues the text, and its continuation is the answer. Nobody retrains the model. The same model can sort reviews, translate words or answer quiz questions, depending only on what you put in front of the question.

It is not reliable in the way a trained classifier is. Studies show that the answer can change a lot with the order of the examples, with which examples you chose, and with the wording. The examples often seem to show the model what kind of task and answer you want, more than they teach it the task. Larger models do this much better than small ones.

## The idea

**The prompt and the shapes.** The prompt is the token sequence $P = (\text{instruction}, x_1, y_1, \ldots, x_K, y_K, x)$, where each $(x_i, y_i)$ is a solved example and $x$ is the query. It has $n$ tokens, with $n \le n_{\text{ctx}}$, the context length of the model ($n_{\text{ctx}} = 2048$ for GPT-3). A [generative pretrained transformer](/generative-pretrained-transformer/) with $L$ blocks of width $d$, $h$ heads and $d_k = d / h$ maps $P$ to an $n \times d$ matrix of hidden states. The last row gives a vector of $|V|$ logits, and a softmax gives the next-token distribution. For a classification task with label words $Y = \{y^{(1)}, \ldots, y^{(c)}\}$, the prediction is

$$\hat y = \arg\max_{y \in Y} p_\theta(y \mid P),$$

where for a label of several tokens $p_\theta$ is the product of the token conditionals. For a generation task, the answer is decoded, for example with [greedy decoding](/greedy-decoding/).

**Cost.** With $K$ examples of $m$ tokens each, $n \approx Km$, and one forward pass costs $O(L(n d^2 + n^2 d))$ multiply-adds: the cost of attention grows as $K^2$. The examples are a prefix shared by all queries. With a key-value cache, their keys and values (an array of $L \times 2 \times n \times d$ numbers) are computed once and reused for every query. The context length caps $K$: for GPT-3 it held 10 to 100 examples (Section 2).

**What the examples seem to supply (measurement).** Min et al. (2022) replaced the labels $y_i$ of the examples with random labels on classification and multiple-choice tasks. Over 12 models, including GPT-3, this barely lowered the scores. The parts that mattered were the set of labels, the distribution of the input texts and the format of the sequence. A reading of this result, which is a heuristic and not a theorem: on these tasks, the examples mostly tell the model which task and which output format to use, and the model already knows the input-label map from pretraining.

**Sensitivity and bias (measurement).** Zhao et al. (2021) measured GPT-3 on text classification and fact retrieval. With a fixed format and a fixed set of four examples on SST-2 (GPT-3 2.7B), the order of the examples alone moved the accuracy from 54.3% to 93.4% (Section 3). They name three biases (Section 4): the model prefers labels that are frequent in the prompt (majority label bias), labels near the end of the prompt (recency bias), and tokens that are common in its pretraining data (common token bias).

**Contextual calibration (heuristic with measured gains).** Zhao et al. (Section 5) estimate the bias with an input that has no content. Let $\hat p \in \mathbb{R}^c$ be the model's probabilities of the $c$ label words for the query. Replace the query by a content-free string and call the result $\hat p_{\text{cf}}$. They set

$$W = \mathrm{diag}(\hat p_{\text{cf}})^{-1}, \qquad b = 0,$$

and predict the argmax of $W \hat p + b$. This makes the content-free input score the same for every label. They average $\hat p_{\text{cf}}$ over three such strings: "N/A", "[MASK]" and the empty string. On their tasks it raised the average accuracy of GPT-3 and GPT-2 by up to 30.0 points and reduced the variance across prompts. Nothing guarantees a gain. The method assumes that the bias is one factor per label, the same for every input.

**Two explanations, each under its own hypotheses.**

- *A synthetic measurement.* Garg et al. (2022) trained a [transformer](/transformer/) from scratch on prompts $(x_1, f(x_1), \ldots, x_k, f(x_k), x_{\text{query}})$, where each prompt has its own random linear function $f(x) = w^\top x$. On new functions, the error of its prediction was close to that of [ordinary least squares](/ordinary-least-squares/) fitted to the $k$ examples, also under some distribution shifts. They report similar results for sparse linear functions, two-layer networks and decision trees. The comparison method has a theorem of its own: with no noise and $k \ge d$ inputs that span $\mathbb{R}^d$, least squares recovers $w$ exactly. The experiment shows that a transformer can learn a learning algorithm that it runs in context. It does not show that a pretrained language model does this.
- *A Bayesian model.* Xie et al. (2022) assume that the pretraining documents come from a mixture of [hidden Markov models](/hidden-markov-model/), each with a hidden "concept", and that the examples of a prompt share one concept. Under their assumptions they prove that in-context learning happens even though prompts do not look like pretraining documents: the model infers the shared concept, as in [Bayesian inference](/bayesian-inference/). On their synthetic data set GINC, transformers and LSTMs learned in context, larger models did better at the same pretraining loss, the order of the examples mattered, and zero-shot sometimes beat few-shot. The theorem holds for their generative model, not for natural text.

## Examples

**One model, three prompts (measurement).** On closed-book TriviaQA (questions with no retrieved documents), GPT-3 175B scored 64.3% zero-shot, 68.0% one-shot and 71.2% few-shot, with the same weights (Section 3.2, Table 3.3). The authors report the few-shot score as the best of its time in that closed-book setting, including fine-tuned models. The smallest model, with 125M parameters, scored 4.15%, 4.19% and 6.96% (Table H.1). The few-shot gain over zero-shot was 2.8 points at 125M, 15.7 points at 13B and 6.9 points at 175B, so on this task it does not grow in a straight line with size. Over 42 benchmarks, the authors report that few-shot accuracy grew faster with model size than zero-shot accuracy (Figure 1.3).

**Calibrating one prediction.** A sentiment task has the labels Positive and Negative. For the query the model gives $\hat p = (0.6, 0.4)$. With the same examples and a content-free query it gives $\hat p_{\text{cf}} = (0.7, 0.3)$. Then $W \hat p = (0.6 / 0.7, 0.4 / 0.3) = (0.8571, 1.3333)$, and the prediction changes from Positive to Negative. Scaled to sum to 1, the scores are $(0.3913, 0.6087)$. In words: the prompt makes the model say Positive 70% of the time with no input at all, and this query is less positive than that.

**The majority label bias (measurement).** Zhao et al. (Section 4) often saw accuracy fall from zero-shot to one-shot, and found that the model often repeated the label of its one example. On 4-shot LAMA with GPT-3 2.7B, 50.2% of the predictions repeated one of the four example answers, against a correct repeat rate of 24.7%.

**A toy of the Bayesian view.** Suppose there are two possible tasks, A and B, with prior probability 1/2 each, and each example is 4 times more likely under A than under B (0.8 against 0.2). After $k$ examples, $P(A \mid \text{examples}) = 0.8^k / (0.8^k + 0.2^k)$, which is 0.8, 0.9412 and 0.9846 for $k = 1, 2, 3$. A predictor that mixes the two tasks with these weights soon acts as if it knew the task. This illustrates the model of Xie et al.; it is not a model of any real network.

## Where it is used

- **Evaluating language models.** Since GPT-3, models are reported in the zero-shot, one-shot and few-shot settings. The numbers depend on the prompt, so a fair comparison fixes the prompt, the examples and their order, or averages over several.
- **Building a classifier or an extractor with no training.** A few labeled examples and a prompt replace a training run. Use balanced labels, try several orders, and consider contextual calibration, given the biases above.
- **Choosing the examples by retrieval (heuristic).** Pick the stored examples nearest to the query in an embedding space, as in [k-nearest neighbors](/k-nearest-neighbors/). This is close to [retrieval-augmented generation](/retrieval-augmented-generation/), which puts retrieved documents instead of solved examples into the prompt.
- **Reasoning tasks.** [Chain-of-thought prompting](/chain-of-thought-prompting/) writes the steps of the solution into each example. Its measured gains appear only in large models.
- **After instruction tuning.** An instruction-tuned model is often used zero-shot, with an instruction and no examples. Whether examples still help is a measurement for each model and task.
- **Planning with scale.** [Neural scaling laws](/neural-scaling-law/) predict test loss, not in-context accuracy. The accuracy on a task must be measured for each model size.

## References
