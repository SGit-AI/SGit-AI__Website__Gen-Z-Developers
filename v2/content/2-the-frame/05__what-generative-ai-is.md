---
title: What generative AI is
slug: what-generative-ai-is
part: the-frame
number: 5
ideas: [generative-ai-not-ai, better-prompt-richer-picture]
answers_2018: [3.technologies/content/ml-ai.md]
sources: [art:generative-ai-not-ai, book:3.technologies/content/ml-ai.md]
character: zara
gravity: all
status: draft
---

In 2018 I wrote that one of the most important areas you needed to understand in the next five years was machine learning and artificial intelligence. I said it was not a Skynet scenario, and that the question was "whether you are going to be a player or a pawn in what is happening next". Then I pointed you at the machine learning services the cloud providers had started to offer, and at three books. That was the whole chapter.

I was right about the five years and wrong about where to look. What arrived was not the AI I was describing. So before this book says anything else about what you can do, I want to be exact about what it is talking about.

## AI is a huge bucket

AI has become a huge bucket, and to be honest the word gets abused a lot. Inside the bucket there is AI in the wider sense, there is machine learning, there is deep learning, and there is generative AI. They are not the same thing, and most of what you read online does not say which one it means.

The technology that is changing the world, and the technology that is driving my imagination and my capabilities right now, is the generative kind. So this book says "generative AI" when it means that, and "AI" only when it means the wider field.

There will be very few examples here of AI out in the field recognising faces, scoring loans or recommending films. That AI is huge and has a lot of interesting applications. It is not what this book is about. This book is about the AI that creates something from the input it is given.

## How I understand it

The interesting property of generative AI is in the name: it generates the output. There are the transformers and all that jazz, but for me the interesting part is simpler. The data goes into a model. The model builds its own interpretation of it. Then it recreates an output from that interpretation. There is an abstraction layer between what goes in and what comes out: the input becomes an intermediate representation inside the model, and the output, an image or a text, is generated from that representation.

Inside a language model, what happens is that it predicts the next word. That sounds small. I wrote in the newsroom, in *Who owns the words*, that "predicting the next word" is accurate and demeaning at the same time. It is accurate because that is the mechanism. It is demeaning because of what the prediction is made from: an incredibly rich picture of the world, of how things connect, which the model narrows down based on your prompt.

That is why the better your prompt, the better the output. When I talk to a model for ten minutes before I ask it for anything, as I did for the article this chapter comes from, it is not politeness. The model knows better which concepts I am talking about. The prompt pulls it towards the part of what it knows that I mean.

## Where hallucinations come from

I think that is also where hallucinations come from. Just about everything is connected to everything, and from inside the model they are all just connections. It is very hard for a model to know where the lines are. Giving it text helps so much because the text in your prompt is like a short-term memory that says: these are the connections that actually hold here.

In a talk I gave in Lisbon in June 2024 I said hallucinations "Are a FEATURE when creating content and when we want creativity, But are a BUG and PROBLEM when we want facts, evident and trust". I still think so. If you want a story, you want the model to wander across those connections. If you want a fact, you want it held to the ones you gave it. Most of the trouble people have comes from asking for the second while set up for the first.

## The image that made it click

Ironically, it was an image, in one of my presentations, that made me understand generative AI at this level. The keynote was *Deterministic GenAI Output With Provenance*, at OWASP Global AppSec EU in Lisbon on 28 June 2024, and slide 70 has the title "The image that caused my 'GenAI Paradigm Shift'". The image is a post by Lee Brimelow. He used Photoshop's Generative Fill and Adobe Firefly to extend Van Gogh's *The Starry Night* on every side, with the original shown in a frame at the centre. Outside the frame, the swirls, the stars, the hills and the brushwork carry on as if Van Gogh had painted a bigger canvas. The tools for this were new then: outpainting was announced in August 2022, and Generative Fill went into Photoshop in May 2023.

I remember thinking: for that to work, the model has to have learned all those concepts. How Van Gogh paints. The patterns, the structure, the positions, the palette. What we are actually looking at: the landscape, the sky, a character. If there is a mountain here, there will be a mountain there, and the new mountains have to be coherent with every other mountain it has seen. If the sun is there, the light falls a certain way, and so do the shadows. Once you see all the variables it has to hold, extending the image makes sense.

And then I took that to text, and thought: that is exactly what happens with text. Nine slides later, the same talk has the picture I still use: "Input", "Intermediate Representation", "Output", with "GenAI" in the middle. The slide after it says what matters about that black box is not the black box. It is the human verification and the human ownership of the answer. That is where provenance comes in, and *Facts, evidence and the record* picks it up.

> **For Dinis:** the book can only reproduce Lee Brimelow's image with his permission. The alternative the article names is to extend *The Starry Night* ourselves, with a named tool, and show that. Which one?

## What the models found in our language

I think the models have discovered things about our language that we never found ourselves, because we were never able to rationalise them. We do not know what is happening in a child's head as they learn to speak, because they cannot put it into words. We are too close to our own language to see it. With many layers, and as they got bigger, the models found connections and relationships in it. That is my hypothesis, not a finding; the people who study the insides of these models are still working out what the structures they find mean.

We are still discovering what the models can do. In the early days of the chat assistants there were all these stories: it can count, it can do chemistry, it speaks all these languages. A model trained mostly on English turns out to work in a language it saw very little of. How does that work? That is the same sense of wonder this book started with.

## Where I was corrected

I asked the agent that is helping me write this book to correct me where I was wrong. It did. The corrections belong here, because they are the kind of thing you should learn to ask for, and because my picture above is a working picture, not the inside of the machine.

- **Classic machine learning learns too.** I had said the older AI was a sequence of steps or a formula, and generative AI learns. The rule-based AI was like that; machine learning in general learns from data, and generative AI is one branch of it. The real difference is what comes out. Most machine learning predicts a label or a number (is this spam, what will this cost). A generative model produces new content of the kind it was trained on.
- **Inside the model there are vectors, not a graph.** A language model represents words and their contexts as long lists of numbers, and passes them through many layers; its attention mechanism connects every word in the text to every other word, with learned strengths. You can picture that as a graph, and I find the picture useful. But there is no stored graph of nodes and edges inside. My graph is a metaphor.
- **The prompt does not change the model.** It conditions what the model computes. The weights stay the same; the prompt steers what it draws on. My "real-time fine-tuning" was also a metaphor.
- **It predicts the next token, then it is trained to be useful.** Tokens are pieces of words. The prediction is the start; further training, including on human feedback, is what turns a model into an assistant that follows instructions.
- **Hallucinations have a second cause.** A study published by OpenAI researchers in September 2025, *Why language models hallucinate*, argues that training and evaluation reward guessing over saying "I don't know": a guess is sometimes right, and an honest "I don't know" scores nothing. One explanation, from one model maker; not the only one.
- **Most image models work differently.** The common kind are diffusion models: they start from noise and remove it step by step, guided by the text. My intuition that they learned the structure of images holds; but they learned statistical patterns, and they still get light, shadows and hands wrong in ways a person would not.
- **"Emergent abilities" are debated.** The term comes from a 2022 paper by Jason Wei and others; a 2023 paper by Rylan Schaeffer and others argues that many of those jumps come from how they were measured. Models working across languages is real and studied; the stories of near-zero data and full fluency are anecdotes.
- **Whether models have a "world model" is an open question.** Research shows they form internal representations of things like positions, places and dates; how far that goes is argued about.

Keep both halves. The picture is how I work with these models every day, and it has not let me down. The corrections are what is actually inside. You will need the first to be fast and the second to be honest, and asking for the second is a habit this book will keep coming back to.

## A note on the name

Most of what this book says should say generative AI, not AI. This edition has been described as the AI edition; maybe it should be the Gen AI edition, because there is a play in it: Gen Z, Gen AI. And after Gen Z comes Gen Alpha. Mark McCrindle, who named them, puts them as born from 2010 to 2024, so the oldest are sixteen in 2026, and after them Gen Beta, from 2025. The boundaries are not official; no body sets them. If you are reading this and you are sixteen, the book is for you too.

> **For Dinis:** the Gen AI edition: yes, no, or a subtitle? The article leaves it to the title interview.
