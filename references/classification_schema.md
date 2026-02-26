# Classification Schema

This document defines the research categories used for classifying AI & protein design literature.

## Primary Categories

### 1. Deep Learning for Protein Structure Prediction
**Description:** Methods using deep learning to predict protein 3D structures

**Keywords:**
- structure prediction
- AlphaFold
- RoseTTAFold
- protein structure
- fold prediction
- tertiary structure
- conformational prediction

**Examples:**
- Papers describing improvements to AlphaFold or similar models
- Methods for predicting protein dynamics
- Techniques for refining predicted structures

### 2. Generative Models for Protein Design
**Description:** Models that generate novel protein sequences or structures

**Keywords:**
- generative model
- GPT
- diffusion
- VAE
- GAN
- protein generation
- de novo design
- sequence generation
- structure generation

**Examples:**
- Diffusion models for protein sequence design
- Transformer-based protein generators
- Methods for generating diverse protein libraries

### 3. Reinforcement Learning for Protein Engineering
**Description:** Using reinforcement learning to optimize protein properties

**Keywords:**
- reinforcement learning
- RL
- policy gradient
- Q-learning
- protein engineering
- optimization
- sequential decision making

**Examples:**
- RL agents for optimizing protein stability
- Policy gradient methods for enzyme engineering
- Reward function design for protein optimization

### 4. Multi-objective Optimization in Protein Design
**Description:** Methods that balance multiple design objectives simultaneously

**Keywords:**
- multi-objective
- Pareto
- optimization
- trade-off
- multi-criteria
- conflicting objectives

**Examples:**
- Methods balancing protein stability and activity
- Pareto optimization for protein therapeutics
- Multi-objective frameworks for enzyme design

### 5. Transfer Learning in Protein Engineering
**Description:** Applying knowledge from one protein domain to another

**Keywords:**
- transfer learning
- fine-tuning
- pre-trained
- domain adaptation
- knowledge transfer
- cross-domain learning

**Examples:**
- Pre-trained models for protein family-specific design
- Transferring knowledge from natural to designed proteins
- Domain adaptation techniques for protein engineering

### 6. AI for Protein Function Prediction
**Description:** Predicting protein functions from sequence or structure

**Keywords:**
- function prediction
- annotation
- protein function
- activity prediction
- functional annotation
- property prediction

**Examples:**
- Methods for predicting enzyme substrate specificity
- Function prediction from protein-protein interactions
- Techniques for annotating protein function at scale

### 7. Computational Protein-Protein Interaction Design
**Description:** Designing protein-protein interactions and complexes

**Keywords:**
- protein-protein interaction
- PPI
- interaction design
- binding interface
- complex design
- dimer design

**Examples:**
- Methods for designing high-affinity protein binders
- Computational design of protein complexes
- Techniques for optimizing binding interfaces

### 8. Protein Design for Therapeutics
**Description:** Designing proteins for medical applications

**Keywords:**
- therapeutic
- drug design
- biologic
- pharmaceutical
- medicine
- therapy
- drug development

**Examples:**
- Designed protein therapeutics
- AI for antibody design
- Protein-based drug delivery systems

### 9. Enzyme Engineering with AI
**Description:** Using AI to engineer enzymes with improved properties

**Keywords:**
- enzyme
- catalysis
- biocatalyst
- enzyme engineering
- activity improvement
- substrate specificity

**Examples:**
- AI methods for improving enzyme activity
- Techniques for designing enzymes with new functions
- Computational approaches for enzyme stabilization

### 10. Protein Nanomaterials Design
**Description:** Designing protein-based nanomaterials and assemblies

**Keywords:**
- nanomaterial
- self-assembly
- nanoparticle
- protein material
- nanofiber
- protein assembly

**Examples:**
- Methods for designing self-assembling protein nanoparticles
- Protein-based materials with specific properties
- Computational design of protein nanostructures

## Classification Methodology

### Keyword Matching
Papers are classified based on the presence of category-specific keywords in their title and abstract.

### Hierarchical Classification
Papers can belong to multiple categories if they cover multiple research areas.

### Edge Cases
- **Review papers:** Classified based on the primary research areas they cover
- **Methodology papers:** Classified based on their intended application
- **Interdisciplinary papers:** Assigned to all relevant categories

### Confidence Scoring
For each paper, a confidence score is calculated for each category based on:
1. Number of matching keywords
2. Position of keywords (title vs. abstract)
3. Contextual relevance

## Usage Guidelines

### When to Use This Schema
- For organizing literature reviews
- For identifying research trends
- For categorizing papers in the analysis pipeline
- For comparing different research areas

### How to Extend This Schema
1. **Adding new categories:** When a new research area emerges
2. **Updating keywords:** When new terminology becomes common
3. **Refining descriptions:** When research areas evolve

### Validation
- Regularly validate classification results against expert annotations
- Adjust keywords and categories based on misclassifications
- Maintain consistency with field-specific terminology
