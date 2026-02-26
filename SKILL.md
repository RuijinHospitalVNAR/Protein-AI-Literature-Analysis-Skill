---
name: protein-ai-literature-analysis
description: Retrieves and analyzes the latest AI & protein design literature from SCI journals and preprints. Classifies papers by research area, provides brief evaluations, scores importance, and generates comprehensive reports with links. Use when users need to stay updated on cutting-edge developments in AI-driven protein design research.
---

# Protein AI Literature Analysis

## Overview

This skill enables comprehensive retrieval and analysis of the latest scientific literature on AI-driven protein design. It automates the process of searching reputable sources, classifying research areas, evaluating significance, and generating structured reports with direct links to original papers.

## Workflow Decision Tree

1. **Initialization**
   - User requests literature analysis on AI & protein design
   - Determine time range (default: last 3 months)
   - Confirm output format (markdown report)

2. **Literature Retrieval**
   - Query PubMed for SCI journal papers
   - Query bioRxiv and arXiv for preprints
   - Filter results by relevance

3. **Data Processing**
   - Extract metadata (title, authors, journal, date, abstract, DOI)
   - Download full texts when available
   - Process and store results

4. **Analysis and Classification**
   - Classify papers by research area
   - Evaluate scientific significance
   - Score importance (1-10 scale)

5. **Report Generation**
   - Generate structured markdown report
   - Include paper details with links
   - Add summary statistics and insights
   - Save report to specified location

## Core Capabilities

### 1. Literature Retrieval

**PubMed Integration**
- Uses PubMed API to search for peer-reviewed papers
- Search terms: "artificial intelligence"[Title/Abstract] AND "protein design"[Title/Abstract]
- Filters: Recent publications, English language, full text available

**Preprint Sources**
- bioRxiv: Biological sciences preprints
- arXiv: Computer science and quantitative biology preprints
- Comprehensive coverage of cutting-edge research

**Google Scholar Integration**
- Provides broader coverage across multiple publishers
- Includes citations and related papers
- Requires external library (scholarly) or API (SerpAPI)

**X (Twitter) Integration**
- Captures latest discussions and preprint announcements
- Identifies trending research topics
- Requires Twitter Developer API authentication

### 2. Research Classification

**Primary Categories**
- Deep Learning for Protein Structure Prediction
- Generative Models for Protein Design
- Reinforcement Learning for Protein Engineering
- Multi-objective Optimization in Protein Design
- Transfer Learning in Protein Engineering
- AI for Protein Function Prediction
- Computational Protein-Protein Interaction Design
- Protein Design for Therapeutics
- Enzyme Engineering with AI
- Protein Nanomaterials Design

**Classification Method**
- Keyword extraction from title and abstract
- Topic modeling for content analysis
- Hierarchical classification system

### 3. Importance Scoring

**Scoring Criteria**
- **Novelty (30%)**: Originality of approach and methods
- **Impact (25%)**: Potential influence on the field
- **Technical Innovation (25%)**: Advances in AI methodologies
- **Applicability (20%)**: Practical relevance and use cases

**Scoring Process**
- Automated initial scoring based on content analysis
- Contextual adjustment for field-specific significance
- Final scoring validated against citation potential

### 4. Report Generation

**Report Structure**
- Executive Summary
- Methodology
- Literature Overview
- Detailed Paper Analysis (by category)
- Summary Statistics
- Future Directions
- References with Direct Links

**Output Format**
- Markdown file with structured sections
- Interactive table of contents
- DOI links for direct paper access
- Visual summaries of classification and scoring

## Implementation Details

### Required Scripts

**literature_retriever.py**
- Handles API calls to PubMed, bioRxiv, and arXiv
- Manages pagination and rate limiting
- Parses and normalizes metadata

**paper_analyzer.py**
- Performs text analysis and classification
- Computes importance scores
- Generates detailed paper evaluations

**report_generator.py**
- Creates structured markdown reports
- Formats citations and links
- Adds visualizations and summaries

### API Configuration

**PubMed API**
- Base URL: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- Required parameters: db, term, retmax, retmode, sort
- Rate limit: 3 requests per second

**bioRxiv API**
- Base URL: https://api.biorxiv.org/
- Endpoints: /papers, /detail
- Rate limit: 10 requests per second

**arXiv API**
- Base URL: http://export.arxiv.org/api/
- Endpoints: /query
- Rate limit: 1 request per 3 seconds

**Google Scholar**
- No official API
- Recommended libraries: scholarly (Python)
- Alternative: SerpAPI (paid service)
- Rate limit: Varies by method

**X (Twitter) API**
- Base URL: https://api.twitter.com/2/
- Endpoints: /tweets/search/recent
- Requires: Bearer token authentication
- Rate limit: 450 requests per 15-minute window

### Usage Examples

**Basic Usage**
```python
# Example: Retrieve and analyze recent literature
python scripts/literature_retriever.py --timeframe 3months --output data/papers.json
python scripts/paper_analyzer.py --input data/papers.json --output data/analyzed_papers.json
python scripts/report_generator.py --input data/analyzed_papers.json --output reports/latest_literature_analysis.md
```

**Custom Parameters**
```python
# Example: Focus on specific research areas
python scripts/literature_retriever.py --timeframe 6months --categories "generative models" "reinforcement learning" --output data/custom_papers.json
```

## References

### API Documentation
- [PubMed E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [bioRxiv API Documentation](https://api.biorxiv.org/)
- [arXiv API Documentation](https://info.arxiv.org/help/api/index.html)

### Classification Schema
- Detailed category definitions and keywords
- Hierarchical classification tree
- Example papers for each category

### Scoring Guidelines
- Detailed scoring rubrics
- Examples of high-scoring papers
- Contextual adjustment factors

## Troubleshooting

### Common Issues
- **API Rate Limiting**: Implement exponential backoff
- **Full Text Access**: Handle paywalled papers gracefully
- **Classification Ambiguity**: Use probabilistic classification
- **Scoring Inconsistency**: Regular calibration against expert reviews

### Error Handling
- Robust error handling for API failures
- Graceful degradation when data is incomplete
- Comprehensive logging for debugging

## Future Enhancements

- Integration with Google Scholar for broader coverage
- Automated citation network analysis
- Interactive visualization dashboard
- Custom alert system for new publications
- Integration with lab management systems

## Resources

### scripts/
- `literature_retriever.py` - Retrieves papers from multiple sources (PubMed, bioRxiv, arXiv, Google Scholar, X)
- `paper_analyzer.py` - Analyzes and scores papers
- `report_generator.py` - Generates comprehensive reports
- `utils.py` - Common utilities and helper functions

### references/
- `api_documentation.md` - API usage guides and examples
- `classification_schema.md` - Detailed classification system
- `scoring_guidelines.md` - Comprehensive scoring criteria

### assets/
- `report_template.md` - Markdown report template
- `visualization_templates/` - Templates for data visualization
- `example_reports/` - Sample output reports
