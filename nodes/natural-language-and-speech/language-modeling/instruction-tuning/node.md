---
tag: 18EH1N
kind: technique
slug: instruction-tuning
name: Instruction tuning
aliases:
- supervised fine-tuning on instructions
area: natural-language-and-speech/language-modeling
level: research
summary: Fine-tune a pretrained language model on tasks written as instructions with answers. Measured gains on unseen tasks appear in large models; FLAN models of 8B and below got worse.
history:
  year: 2021
  people: [Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, Quoc V. Le]
  note: "Wei and colleagues at Google named the method with FLAN and showed zero-shot gains on held-out task clusters at ICLR 2022. In 2022 Ouyang and colleagues at OpenAI used the same loss on human-written demonstrations as the first step of InstructGPT."
prereqs: [generative-pretrained-transformer, cross-entropy-loss, in-context-learning]
see_also: [reinforcement-learning-from-human-feedback, preference-reward-model, direct-preference-optimization, low-rank-adaptation, chain-of-thought-prompting, teacher-forcing, kullback-leibler-divergence, knowledge-distillation]
sources:
  - url: https://arxiv.org/abs/2109.01652
    title: "Jason Wei, Maarten Bosma, Vincent Y. Zhao and others, Finetuned language models are zero-shot learners, ICLR 2022"
    locator: "Section 2 (62 data sets in 12 task clusters, 10 templates for each data set, evaluation on held-out clusters), Section 3 and the abstract (20 of 25 data sets against zero-shot GPT-3 175B), Section 4 (ablations on the number of clusters, model scale and instructions), Section 4.2 (models of 8B and below got worse on held-out tasks)"
  - url: https://arxiv.org/abs/2210.11416
    title: "Hyung Won Chung, Le Hou, Shayne Longpre and others, Scaling instruction-finetuned language models, 2022"
    locator: "abstract (1.8K tasks, chain-of-thought data, Flan-PaLM 540B 9.4% above PaLM 540B on average, 75.2% on five-shot MMLU)"
  - url: https://arxiv.org/abs/2203.02155
    title: "Long Ouyang, Jeff Wu, Xu Jiang and others, Training language models to follow instructions with human feedback, NeurIPS 2022"
    locator: "Section 3.2 (about 13k prompts for supervised fine-tuning), Section 3.5 (16 epochs, overfitting of the validation loss after 1 epoch), Section 5.1 (4.9 petaflop/s-days for the 175B model), Appendix C.1 (learning rates and batch sizes), Appendix C.3 (2 epochs with 10% pretraining data for the RLHF initialization)"
  - url: https://arxiv.org/abs/2305.11206
    title: "Chunting Zhou, Pengfei Liu, Puxin Xu and others, LIMA: Less is more for alignment, 2023"
    locator: "abstract (a 65B model tuned on 1,000 examples; equal to or preferred over GPT-4 in 43% of cases, Bard 58%, DaVinci003 65%)"
---

Instruction tuning is supervised fine-tuning of a pretrained [language model](/language-model/) on pairs (instruction, response), with the [cross-entropy loss](/cross-entropy-loss/) on the response tokens only. The aim is a model that does what a new instruction asks, without examples in the prompt. It sits next to three methods that use human preferences, and it is easy to mix them up. Instruction tuning needs demonstrations: one good response per prompt. A [preference reward model](/preference-reward-model/) is a separate network trained on comparisons between two responses, and it gives a score, not text. [Reinforcement learning from human feedback](/reinforcement-learning-from-human-feedback/) trains the policy to get a high score from such a reward model, with a penalty for moving far from a reference model. [Direct preference optimization](/direct-preference-optimization/) trains the policy on the comparisons directly, with no reward model. In the pipeline of Ouyang et al. (2022), instruction tuning is step 1 and gives the starting point and the reference for the other steps. Its gains are measurements on particular models and task sets. No theorem says that a tuned model will follow an instruction that it has not seen.

## In plain words

A model trained only to continue web text does not always answer a request. Asked a question, it may write more questions. Instruction tuning trains it a little more on many examples of a request followed by a good answer. The model learns to give the answer.

There are two common sources of examples. One is existing data sets, such as translation or question answering, each rewritten as plain instructions in several wordings. The other is people writing good answers to real requests.

The training only grades the answer part, not the request. In the measurements, large models got better at tasks they had never seen, while some small models got worse. The model also copies the style and the mistakes of its examples, because it learns to imitate them.

## When it applies

- You have a pretrained model and want it to follow instructions zero-shot, with no solved examples in the prompt.
- You have demonstrations: data sets that can be written as instructions with answers, or responses written by people. If you only have comparisons between responses, use a reward model with RLHF, or DPO.
- The model is large enough. In the FLAN measurements the gains on held-out tasks appeared at large sizes, and models of 8B parameters and below got worse.
- As the first stage before preference training, which needs a model that already answers in the right format.

## The template

**Sizes.** A training example is a token sequence $x_1, \ldots, x_n$ with $n = n_p + n_r$: $n_p$ tokens of prompt (instruction and input) and then $n_r$ tokens of response. The model is a [generative pretrained transformer](/generative-pretrained-transformer/) with $L$ blocks of width $d$, $h$ heads and $d_k = d / h$. It gives an $n \times |V|$ matrix of logits, one row for each next-token prediction, with [teacher forcing](/teacher-forcing/). Let $m_t = 1$ if token $t$ is in the response and $0$ otherwise.

1. **Collect tasks.** Take many data sets, and group them into task clusters (for example: translation, natural language inference, summarization). Keep some clusters out of training for evaluation. Wei et al. used 62 data sets in 12 clusters.
2. **Write templates.** For each data set, write several instruction templates that turn an example into a prompt and a target. Wei et al. wrote 10 for each data set. Human-written demonstrations need no template.
3. **Format.** Use one fixed format that marks where the response begins, and use the same format at inference time.
4. **Train with a masked loss.** Minimize

$$\mathcal{L}(\theta) = \frac{\sum_{t=2}^{n} m_t \, \big(-\log p_\theta(x_t \mid x_{<t})\big)}{\sum_{t=2}^{n} m_t},$$

   averaged over a mixture of the data sets. Limit how much any one large data set contributes, so that it does not fill the mixture.
5. **Select and evaluate.** Pick the checkpoint by a measure you care about, and evaluate zero-shot on the held-out clusters.

**What the loss does (theorem).** For one prompt $x$ with responses drawn from the data distribution $q(\cdot \mid x)$, the expected loss is $\mathbb{E}_{y \sim q}[-\log p_\theta(y \mid x)] = H(q(\cdot \mid x)) + \mathrm{KL}(q(\cdot \mid x) \,\|\, p_\theta(\cdot \mid x))$. The entropy term does not depend on $\theta$, so the loss is smallest when $p_\theta$ matches $q$, the [Kullback-Leibler divergence](/kullback-leibler-divergence/) being zero only then. This holds for any model and any data. It means the tuned model is pushed to imitate the demonstrations, including their errors. The loss has no term that prefers a better response over a worse one; that is what comparison data adds.

**Example.** A prompt of 3 tokens is followed by a response of 3 tokens. The model gives the response tokens the probabilities 0.5, 0.25 and 0.8. Their losses are $0.693147$, $1.386294$ and $0.223144$, and the masked loss is their mean, $0.767528$. The prompt tokens do not count. If the model gave the second and third prompt tokens the probabilities 0.1 and 0.2 (the first token is never predicted) and these were counted as well, the mean over the five predicted tokens would be $1.242922$: the loss would then also train the model to predict the instructions.

## Classic examples

All results are measurements by the papers cited.

- **FLAN (Wei et al., 2022).** A 137B pretrained model was tuned on 62 data sets in 12 clusters, with 10 templates each. To evaluate one cluster, they tuned on the other clusters only. Zero-shot, it beat zero-shot GPT-3 175B on 20 of 25 data sets, and it beat few-shot GPT-3 by a large margin on ANLI, RTE, BoolQ, AI2-ARC, OpenbookQA and StoryCloze (abstract). The ablations found that more task clusters, larger models and natural language instructions all mattered (Section 4). At 8B parameters and below, instruction tuning made the held-out tasks worse (Section 4.2). The authors' guess is that small models use their capacity on the training tasks.
- **Flan-PaLM (Chung et al., 2022).** Tuning on 1.8K tasks, including data with chains of thought, raised PaLM 540B by 9.4% on average over their evaluations, and reached 75.2% on five-shot MMLU (abstract).
- **InstructGPT step 1 (Ouyang et al., 2022).** GPT-3 was tuned on human-written demonstrations for about 13k prompts (Section 3.2). The final supervised model was trained for 16 epochs. Its validation loss started to overfit after 1 epoch, but more epochs improved the reward model score and human ratings (Section 3.5). Tuning the 175B model took 4.9 petaflop/s-days, about 0.13% of the 3,640 for pretraining GPT-3 (Section 5.1). The model used to start RLHF was trained differently: 2 epochs, with 10% pretraining data in the mix (Appendix C.3).
- **LIMA (Zhou et al., 2023).** A 65B model was tuned on only 1,000 chosen examples, with no preference training. In a human study, its answers were equal to or preferred over those of GPT-4 in 43% of cases, of Bard in 58% and of DaVinci003 in 65% (abstract). The authors read this as evidence that almost all knowledge comes from pretraining. That is a hypothesis, not a result of the study.

## Variations

- **Data from existing sets or from people.** FLAN rewrites existing data sets with templates. InstructGPT and LIMA use responses written by people for real or realistic prompts. Using the responses of a stronger model as targets is a form of [knowledge distillation](/knowledge-distillation/).
- **Chains of thought in the data.** Chung et al. mixed in examples with written reasoning steps, so that the model can write steps with no exemplars, as in [chain-of-thought prompting](/chain-of-thought-prompting/).
- **Fewer trained weights.** The same loss can train only a [low-rank adaptation](/low-rank-adaptation/) of the weight matrices, which saves memory.
- **Followed by preference training.** RLHF or DPO usually starts from the instruction-tuned model and uses it as the reference policy.
- **Loss on the whole sequence.** Some setups also train on the prompt tokens. The example above shows how this changes the loss.

## Pitfalls

- **Small models can get worse.** FLAN models of 8B and below lost accuracy on held-out tasks. Measure on your model size.
- **Leaks between training and evaluation.** If a task similar to a held-out task is in the training mix, "unseen" is not true. FLAN held out whole clusters for this reason.
- **Validation loss is a weak guide.** In InstructGPT, the loss started to overfit after 1 epoch while human ratings still improved. Select checkpoints by the measure you care about, with [early stopping](/early-stopping/) on that measure.
- **Imitation of errors.** By the KL identity above, the model learns to copy its demonstrations, mistakes and style included. Clean the data.
- **Format mismatch.** A model tuned with one prompt format can do worse with another. Use the training format at inference.
- **One large data set fills the mix.** Without a limit for each data set, the largest sets dominate the gradient.

## Exercises

1. Recompute the masked loss of the example. Then change the probability of the second response token from 0.25 to 0.5 and give the new mean.
2. Prove the identity $\mathbb{E}_{y \sim q}[-\log p_\theta(y \mid x)] = H(q) + \mathrm{KL}(q \,\|\, p_\theta)$ for a finite set of responses. What does it say about a data set in which half the responses to a prompt are wrong?
3. FLAN has 62 data sets with 10 templates each. How many templates is that? To evaluate the natural language inference cluster, which data sets must be left out of training, and why is leaving out only the test split of one data set not enough?
4. For one prompt you have a demonstration, and also a comparison saying that response A is better than response B. Which of instruction tuning, a preference reward model, RLHF and DPO can use each kind of data?
5. Tuning the 175B model took 4.9 petaflop/s-days and the PPO stage 60, against 3,640 for pretraining. Compute each as a percentage of pretraining. Why does this not mean that the data was cheap?

## References
