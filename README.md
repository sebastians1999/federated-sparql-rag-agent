# Federated SPARQL Query Generation using LLM Prompting Strategies

## Overview

This repository contains the implementation and evaluation framework for generating federated SPARQL queries from natural language questions using LLMs. The research evaluates different prompting methodologies including Chain-of-Thought (CoT) and Least-to-Most (LtM) prompting strategies over biomedical knowledge graphs.

## Research Objectives
The project addresses three key research questions:
How effective is Chain-of-Thought prompting in generating accurate federated SPARQL queries across biomedical knowledge graphs?
Can Least-to-Most prompting outperform Chain-of-Thought in federated SPARQL query generation?
Does the accuracy improvement of LtM justify its higher computational cost compared to CoT?

## System Architecture
The system implements a modular Retrieval-Augmented Generation (RAG) architecture designed to generate federated SPARQL queries from natural language questions. At its core, the architecture consists of two primary RAG components: entity URI retrieval and example query retrieval, both leveraging a vector database wiht distinct collections. The system processes user input through a standardized pipeline that first extracts key terms, retrieves relevant URIs and examples, then applies one of five interchangeable prompting methodologies - Baseline, Construction Prompt (CP), Augmented Construction Prompt (CP-A), Chain-of-Thought (CoT), or Least-to-Most (LtM). Each methodology receives the same contextual inputs but differs in how it structures the generation process, from simple task descriptions to sophisticated multi-stage decomposition strategies. This plug-and-play design allows to easily swap between methodologies while maintaining consistent preprocessing and evaluation, facilitating direct performance comparisons. The generated queries undergo comprehensive evaluation through execution-based, content-based, and structural similarity metrics, providing a holistic assessment of each methodology's effectiveness in handling the complexities of federated biomedical SPARQL generation


## 📁 Repository Structure

├── src/
│   ├── methodologies/          # Implementation of all prompting strategies
│   ├── evaluation/            # Evaluation framework and metrics
│   ├── rag/                   # RAG components for entity and example retrieval
│   └── utils/                 # Utility functions and helpers
├── data/
│   ├── evaluation_set/        # 32 federated SPARQL queries for evaluation
│   ├── entity_index/          # Vector database indices
│   └── example_queries/       # Question-SPARQL pair examples
├── prompts/                   # All prompt templates used in the study
├── results/                   # Experimental results and analysis
└── requirements.txt           # Python dependencies






## 🚀 Getting Started


