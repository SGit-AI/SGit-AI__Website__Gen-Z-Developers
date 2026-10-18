---
title: Generative AI, not AI: the technology this book is about is the one that generates, how I understand it works, from next-word prediction to the image that made it click, and where I was corrected
date: 2026-10-18
author: Dinis Cruz
summary: AI has become a huge bucket, and the word gets abused. The technology that is changing the world, and the one driving my imagination and my capabilities, is generative AI, so the book should say so, and explain the difference between AI, machine learning and generative AI. My understanding is this: the data goes into a model, the model builds its own interpretation of it, and then it recreates an output from that interpretation, an abstraction layer between what goes in and what comes out. A language model predicts the next word, but it predicts it from an incredibly rich picture of how everything connects, which is why a better prompt gives a better answer, and why hallucinations happen: inside the model everything is connected to everything, and it is hard to know where the lines are, so the text you give it acts as a short-term memory of what the connections actually are. What made it click for me was an image: the early tools that extended a photo, where the new parts matched the old, which only works if the model has learned the mountains, the light, the shadows and the palette. Then I realised that is what happens with text. I think the models have found patterns in our language we never put into words, and we are still discovering what they can do. I asked to be corrected, and I was, on several points: classic machine learning learns too; inside a model there are vectors, not a stored graph, so my graph is a metaphor; most image models work by removing noise, not by predicting the next piece; hallucinations also come from training that rewards guessing; and emergent abilities are debated. And a note on the name: Gen Z, Gen AI, and after them Gen Alpha, already born.
version: v0.2.8
tags: generative-ai, machine-learning, llm, hallucinations, images, naming, gen-z-book, article
status: published
---

## In short {#in-short}

- **This book is about generative AI, not AI in general.** AI is now a huge bucket, and the word gets abused.
- **Generative AI generates.** Data goes in, the model builds its own representation, and it recreates an output from it.
- **A language model predicts the next word, from a very rich picture of how things connect.** Which is why a better prompt gives a better answer.
- **Hallucinations come partly from that richness.** Everything is connected; the text you give it says which connections matter.
- **An image made it click for me.** Extending a photo coherently needs mountains, light and shadows learned; text is the same.
- **We are still discovering what these models can do.** That is the sense of wonder again.
- **I asked to be corrected, and I was.** On machine learning, on the graph, on images, on hallucinations and on emergence.
- **A note on the name.** Gen Z, Gen AI, and Gen Alpha after them.

## AI is a huge bucket {#bucket}

I want to be exact about this. The technology that is changing the world, and the technology that is really driving my imagination and my capabilities right now, is generative AI. AI has become a huge bucket, and to be honest the word gets abused a lot. So the book should have a section that explains the difference between AI, machine learning and generative AI, and then say plainly that it is about the generative kind.

There will be very few examples in this book of AI in the wider sense, out in the field, recognising faces or scoring loans or recommending films. That AI is huge and has a lot of interesting applications. What this book is about is the generative one: the AI that creates something based on the input it is given.

## How I understand it {#understand}

The interesting property of generative AI, which I have talked about before, is in the name: it generates the output. There are the transformers and all that jazz, but for me the interesting part is that the data goes into a model, and the model recreates the output from its own interpretation of it. There is an abstraction layer between the input and the output: the input becomes an intermediate representation inside the model, and the output, an image or a text, is generated from that representation.

Inside a language model, what happens is that it predicts the next word. But it predicts the next word from an incredibly rich picture of the world, of how things connect, which it narrows down based on your prompt. That is why the better your prompt, the better the output, as I am doing here by talking for ten minutes: the model knows better which concepts you are talking about. I wrote in [who owns the words](https://newsroom.sgit.ai/articles/who-owns-the-words.html) that "predicting the next word" is accurate and demeaning at the same time, and that a prompt pulls the model towards the part of what it knows that you mean.

## Where hallucinations come from {#hallucinations}

I think that is also where hallucinations come from. Just about everything is connected to everything, and from inside the model they are all just connections; it is very hard for a model to know where the lines are. That is why giving it text helps so much: the text in your prompt is like a short-term memory that says, these are the connections that actually hold here.

In a talk I gave in Lisbon in June 2024, which the newsroom wrote up as [GenAI in Portuguese](https://newsroom.sgit.ai/articles/portugal-2024-genai-in-portuguese.html), I said hallucinations "Are a FEATURE when creating content and when we want creativity, But are a BUG and PROBLEM when we want facts, evident and trust". I still think so.

## The image that made it click {#image}

Ironically, it was an image, in one of my presentations, that made me understand generative AI at this level. It is slide 70 of *Deterministic GenAI Output With Provenance*, the keynote I gave at OWASP Global AppSec EU in Lisbon on 28 June 2024, and its title says it: "The image that caused my 'GenAI Paradigm Shift'". The image is a post by Lee Brimelow, who used Photoshop's Generative Fill and Adobe Firefly to extend Van Gogh's *The Starry Night* on every side, with the original shown in a frame at the centre. Outside the frame, the swirls, the stars, the hills and the brushwork carry on as if Van Gogh had painted a bigger canvas. The tools for this were new then: OpenAI announced outpainting for DALL-E in August 2022, and Adobe put Generative Fill into Photoshop in May 2023.

I remember thinking: for that to work, the model has to have learned all those concepts: in that case, how Van Gogh paints. The patterns, the structure, the positions, the palette; what we are actually looking at, the landscape, the sky, a character. If there is a mountain here, there will be a mountain there, and the new mountains have to be coherent with every other mountain it has seen. If the sun is there, the light falls a certain way, and so do the shadows. Once you see all the variables it has to hold, extending the image makes sense.

And then I took that to text, and thought: that is exactly what happens with text. Nine slides later, the same talk has the picture I still use: "Input", "Intermediate Representation", "Output", with "GenAI" in the middle. And the slide after it says what matters about that black box is not the black box: it is the human verification and the human ownership of the answer, which is where provenance comes in. A large language model is a model built on language, and generative AI is the wider family of models that generate, but I believe the language models are doing the same thing with words.

## What the models found in our language {#language}

As I have written before, I think the models have discovered things about our language that we never found ourselves, because we were never able to rationalise them. We do not know what is happening in a child's head as they learn to speak, because they cannot put it into words; and we are too close to our own language to see it. With many layers, and as they get bigger, the models found connections and relationships in it.

We are still discovering what they can do. In the early days of ChatGPT there were all these stories: it can count, it can do chemistry, it speaks all these languages. A model trained mostly on English turns out to work in a language it saw very little of. How does that work? That is the same sense of wonder the book starts with.

## Where I was corrected {#corrected}

I asked Claude, which is helping me write this book, to correct me where I was wrong. It did, and the corrections belong in the book, because they are the kind of thing a reader should learn to ask for.

- **Classic machine learning learns too.** My memo said traditional AI was more like a sequence of steps or a formula, and generative AI learns. The older, rule-based AI was like that; but machine learning in general learns from data, and generative AI is one branch of it. The real difference is what comes out: most machine learning predicts a label or a number (is this spam, what will this cost), while a generative model produces new content of the kind it was trained on.
- **Inside the model there are vectors, not a graph.** A language model represents words and their contexts as long lists of numbers, and passes them through many layers; its attention mechanism connects every word in the text to every other word, with learned strengths. You can picture that as a graph, and I find the picture useful, but there is no stored graph of nodes and edges inside. My graph is a metaphor, and the book should say so.
- **The prompt does not change the model.** It conditions what the model computes. My "real-time fine-tuning" is also a metaphor: the model's weights stay the same, and the prompt steers what it draws on.
- **It predicts the next token, then it is trained to be useful.** Tokens are pieces of words. The prediction is the start; further training, including on human feedback, is what makes a model into an assistant that follows instructions.
- **Hallucinations have a second cause.** Besides the one in my picture, a study published by OpenAI researchers in September 2025, [Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/), argues that training and evaluation reward guessing over saying "I don't know": a guess is sometimes right, while an honest "I don't know" scores nothing.
- **Most image models work differently.** The common kind are diffusion models: they start from noise and remove it step by step, guided by the text, rather than predicting the next piece. My intuition, that they have learned the structure of images, still holds; but they learned statistical patterns, and they still get light, shadows and hands wrong in ways a person would not.
- **"Emergent abilities" are debated.** The term comes from a 2022 paper by Jason Wei and others: abilities that appear only in larger models. A 2023 paper by Rylan Schaeffer and others, [Are emergent abilities of large language models a mirage?](https://arxiv.org/abs/2304.15004), argues that many of those jumps come from how they were measured. Models working across languages is real and studied; the specific stories of near-zero data and full fluency are anecdotes.
- **Whether models have a "world model" is an open question.** There is research showing they form internal representations of things like positions, places and dates; how far that goes is argued about.

## A note on the name {#name}

Most of what this book says should say generative AI, not AI. And the edition has been described as the AI edition; maybe it should be the Gen AI edition, because there is a play in it: Gen Z, Gen AI. And after Gen Z comes Gen Alpha: Mark McCrindle, who named them, puts them as born from 2010 to 2024, so the oldest are sixteen in 2026, and after them Gen Beta, from 2025. The boundaries are not official. I am only leaving a note here; the title is a question for the editor's interview.

## The brief {#brief}

For the editor. Read `team/editor/role.md` and this article first.

1. **Plan a short section, early, on what generative AI is**: the bucket (AI, machine learning, deep learning, generative AI), how a language model works in plain words, why a better prompt helps, where hallucinations come from, and the corrections above. Done when the chapter map places it and the storyboard draws it.
2. **Use "generative AI" across the book**, and "AI" only where the wider field is meant. Done when the style notes for the drafts say so.
3. **Add the name to the title interview** (`002__the-title-the-subtitle-and-the-language.md`): Gen AI edition, or not; and whether Gen Alpha is a future reader. Done when the question is in the script.
4. **Ask for the image, or remake it.** The slide is Lee Brimelow's post; the book can only reproduce it with his permission. The painting itself is in the public domain, so the alternative is to extend *The Starry Night* ourselves, with a named tool, and show that. Done when one of the two is decided with me.

Questions for me, kept apart:

- The Gen AI edition: yes, no, or a subtitle?
- Ask Lee Brimelow for his image, or remake the demonstration ourselves?

## What this does not claim {#limits}

- **My picture of how models work is a working picture.** The corrections say where it is a metaphor, and the book should keep both: the picture, and what is actually inside.
- **"The models discovered things about our language we had not" is my hypothesis.** Interpretability research is finding structures inside models; what they mean is still being worked out.
- **The hallucination study is one explanation**, from researchers at one model maker; it is not the only one.
- **The dates of the image tools are the announced ones.** Outpainting on 31 August 2022; Generative Fill in beta on 23 May 2023.
- **Generation boundaries are conventions.** No official body sets them.

If you can explain generative AI more simply than this, without losing what is true, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice, with the corrections I asked for. The argument and the editorial responsibility are mine.

The quotes from my June 2024 talk are as the newsroom recorded them in [GenAI in Portuguese](https://newsroom.sgit.ai/articles/portugal-2024-genai-in-portuguese.html); the next-word passage is from [who owns the words](https://newsroom.sgit.ai/articles/who-owns-the-words.html). Sources for the corrections: Adam Tauman Kalai, Ofir Nachum, Santosh Vempala and Edwin Zhang, [Why Language Models Hallucinate](https://arxiv.org/abs/2509.04664), 4 September 2025, and OpenAI's [post](https://openai.com/index/why-language-models-hallucinate/) of 5 September; Rylan Schaeffer, Brando Miranda and Sanmi Koyejo, [Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004), 2023; Jason Wei and others, *Emergent Abilities of Large Language Models*, 2022. Outpainting: OpenAI's announcement of 31 August 2022, reported by [Dataconomy](https://dataconomy.com/2022/09/02/dall-e-2-launched-outpainting/); Generative Fill: [PetaPixel, 23 May 2023](https://petapixel.com/2023/05/23/photoshops-new-generative-fill-uses-ai-to-expand-or-change-photos). The image slide: slide 70 of the 117-page PDF of *Deterministic GenAI Output With Provenance*, v1.0, 28 June 2024, which I shared afterwards; slides 79 to 81 are the intermediate representation and human ownership. Generations: Mark McCrindle's ranges, as summarised by [Wikipedia on Generation Beta](https://en.wikipedia.org/wiki/Generation_Beta).
