#!/usr/bin/env python3
"""
Report Generator for Protein AI Literature Analysis

This script generates comprehensive markdown reports from analyzed papers:
- Includes executive summary, methodology, and detailed paper analysis
- Organizes papers by research category
- Provides importance scores and evaluations
- Includes direct links to original papers

Usage:
    python report_generator.py --input data/analyzed_papers.json --output reports/latest_literature_analysis.md
"""

import argparse
import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
    
    def generate_markdown_report(self, input_data, output_file):
        """Generate markdown report from analyzed papers"""
        print(f"Generating report...")
        
        # Extract data
        papers = input_data['papers']
        category_counts = input_data['category_counts']
        total_papers = input_data['total_papers']
        average_score = input_data['average_importance_score']
        
        # Group papers by category
        papers_by_category = {}
        for paper in papers:
            for category in paper['classifications']:
                if category not in papers_by_category:
                    papers_by_category[category] = []
                papers_by_category[category].append(paper)
        
        # Sort categories by number of papers (descending)
        sorted_categories = sorted(papers_by_category.items(), 
                                  key=lambda x: len(x[1]), 
                                  reverse=True)
        
        # Start building markdown
        markdown = []
        
        # Add HTML style for Times New Roman font
        markdown.append(f"<style>")
        markdown.append(f"body {{ font-family: 'Times New Roman', Times, serif; }}")
        markdown.append(f"h1, h2, h3, h4, h5, h6 {{ font-family: 'Times New Roman', Times, serif; }}")
        markdown.append(f"p, li, td, th {{ font-family: 'Times New Roman', Times, serif; }}")
        markdown.append(f"</style>")
        markdown.append(f"")
        
        # Header
        markdown.append(f"# AI & Protein Design Literature Analysis Report")
        markdown.append(f"")
        markdown.append(f"> Generated on: {self.current_date}")
        markdown.append(f"> Timeframe: Last 3 months")
        markdown.append(f"> Total papers analyzed: {total_papers}")
        markdown.append(f"> Average importance score: {average_score:.2f}/10")
        markdown.append(f"")
        markdown.append(f"---")
        markdown.append(f"")
        
        # Executive Summary
        markdown.append(f"## Executive Summary")
        markdown.append(f"")
        markdown.append(f"This report provides a comprehensive analysis of the latest literature on AI-driven protein design. The analysis covers both peer-reviewed papers from SCI journals and preprints from leading repositories.")
        markdown.append(f"")
        markdown.append(f"### Key Findings")
        markdown.append(f"")
        
        # Top categories
        if sorted_categories:
            markdown.append(f"**Top Research Categories:**")
            for i, (category, cat_papers) in enumerate(sorted_categories[:5], 1):
                markdown.append(f"{i}. {category}: {len(cat_papers)} papers")
            markdown.append(f"")
        
        # Top papers by importance score
        top_papers = sorted(papers, key=lambda x: x['importance_score'], reverse=True)[:5]
        if top_papers:
            markdown.append(f"**Highest-Rated Papers:**")
            for i, paper in enumerate(top_papers, 1):
                title = paper['title']
                score = paper['importance_score']
                url = paper.get('url', '#')
                markdown.append(f"{i}. [{title}]({url}) - Score: {score}/10")
            markdown.append(f"")
        
        markdown.append(f"### Research Trends")
        markdown.append(f"")
        markdown.append(f"- **Generative AI** continues to dominate protein design research, with diffusion models and transformers showing promising results")
        markdown.append(f"- **Multi-objective optimization** approaches are gaining traction for balancing competing protein properties")
        markdown.append(f"- **Transfer learning** from pre-trained models is becoming standard practice")
        markdown.append(f"- **Therapeutic applications** remain a key focus area for practical implementation")
        markdown.append(f"")
        
        # Methodology
        markdown.append(f"## Methodology")
        markdown.append(f"")
        markdown.append(f"### Literature Retrieval")
        markdown.append(f"")
        markdown.append(f"- **PubMed:** Peer-reviewed papers from SCI journals")
        markdown.append(f"- **bioRxiv:** Biological sciences preprints")
        markdown.append(f"- **arXiv:** Computer science and quantitative biology preprints")
        markdown.append(f"")
        markdown.append(f"### Analysis Process")
        markdown.append(f"")
        markdown.append(f"1. **Classification:** Papers categorized by research area based on keyword analysis")
        markdown.append(f"2. **Importance Scoring:** Multi-criteria evaluation (1-10 scale):")
        markdown.append(f"   - Novelty (30%)")
        markdown.append(f"   - Potential Impact (25%)")
        markdown.append(f"   - Technical Innovation (25%)")
        markdown.append(f"   - Practical Applicability (20%)")
        markdown.append(f"3. **Evaluation:** Brief assessment of each paper's contributions")
        markdown.append(f"")
        
        # Literature Overview
        markdown.append(f"## Literature Overview")
        markdown.append(f"")
        
        # Category distribution
        markdown.append(f"### Research Category Distribution")
        markdown.append(f"")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_papers) * 100 if total_papers > 0 else 0
            markdown.append(f"- **{category}:** {count} papers ({percentage:.1f}%)")
        markdown.append(f"")
        
        # Publication type distribution
        pub_types = {}
        for paper in papers:
            pub_type = paper.get('type', 'Unknown')
            pub_types[pub_type] = pub_types.get(pub_type, 0) + 1
        
        markdown.append(f"### Publication Type Distribution")
        markdown.append(f"")
        for pub_type, count in pub_types.items():
            percentage = (count / total_papers) * 100 if total_papers > 0 else 0
            markdown.append(f"- **{pub_type.capitalize()}:** {count} papers ({percentage:.1f}%)")
        markdown.append(f"")
        
        # Detailed Paper Analysis
        markdown.append(f"## Detailed Paper Analysis")
        markdown.append(f"")
        markdown.append(f"Papers are organized by research category and sorted by importance score within each category.")
        markdown.append(f"")
        
        # Papers by category
        for category, cat_papers in sorted_categories:
            # Sort papers in category by importance score (descending)
            sorted_papers = sorted(cat_papers, 
                                   key=lambda x: x['importance_score'], 
                                   reverse=True)
            
            markdown.append(f"### {category}")
            markdown.append(f"")
            markdown.append(f"**Total papers:** {len(sorted_papers)}")
            markdown.append(f"")
            
            # Papers in category
            for paper in sorted_papers:
                markdown.append(f"#### [{paper['title']}]({paper.get('url', '#')})")
                markdown.append(f"")
                
                # Authors
                authors = paper.get('authors', [])
                if authors:
                    authors_str = ', '.join(authors[:5])
                    if len(authors) > 5:
                        authors_str += f" et al. ({len(authors)} total)"
                    markdown.append(f"> **Authors:** {authors_str}")
                
                # Journal/Source
                journal = paper.get('journal', '')
                source = paper.get('source', '')
                if journal:
                    markdown.append(f"> **Publication:** {journal}")
                elif source:
                    markdown.append(f"> **Source:** {source}")
                
                # Publication date
                pub_date = paper.get('publication_date', '')
                if pub_date:
                    markdown.append(f"> **Date:** {pub_date}")
                
                # Importance score
                score = paper.get('importance_score', 'N/A')
                markdown.append(f"> **Importance Score:** {score}/10")
                
                # Evaluation
                evaluation = paper.get('evaluation', '')
                if evaluation:
                    markdown.append(f"> **Evaluation:** {evaluation}")
                
                # Abstract (truncated)
                abstract = paper.get('abstract', '')
                if abstract:
                    truncated_abstract = abstract[:300] + '...' if len(abstract) > 300 else abstract
                    markdown.append(f"")
                    markdown.append(f"> **Abstract:** {truncated_abstract}")
                
                # DOI
                doi = paper.get('doi', '')
                if doi:
                    markdown.append(f"> **DOI:** [{doi}](https://doi.org/{doi})")
                
                markdown.append(f"")
                markdown.append(f"---")
                markdown.append(f"")
        
        # Future Directions
        markdown.append(f"## Future Directions")
        markdown.append(f"")
        markdown.append(f"Based on the analyzed literature, the following areas show promising potential for future research:")
        markdown.append(f"")
        markdown.append(f"1. **Integration of multimodal AI models** that combine sequence, structure, and functional data")
        markdown.append(f"2. **Scalable protein design platforms** that can handle larger and more complex protein systems")
        markdown.append(f"3. **AI-guided experimental design** for accelerating the protein engineering pipeline")
        markdown.append(f"4. **Explainable AI models** that provide insights into the protein design process")
        markdown.append(f"5. **Cross-disciplinary approaches** combining AI with synthetic biology and materials science")
        markdown.append(f"")
        
        # References
        markdown.append(f"## References")
        markdown.append(f"")
        markdown.append(f"### Data Sources")
        markdown.append(f"")
        markdown.append(f"- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) - National Library of Medicine")
        markdown.append(f"- [bioRxiv](https://www.biorxiv.org/) - Cold Spring Harbor Laboratory")
        markdown.append(f"- [arXiv](https://arxiv.org/) - Cornell University")
        markdown.append(f"")
        
        # Appendices
        markdown.append(f"## Appendices")
        markdown.append(f"")
        markdown.append(f"### Importance Scoring Methodology")
        markdown.append(f"")
        markdown.append(f"The importance score (1-10) is calculated based on a weighted sum of four criteria:")
        markdown.append(f"")
        markdown.append(f"| Criterion | Weight | Description |")
        markdown.append(f"|-----------|--------|-------------|")
        markdown.append(f"| Novelty | 30% | Originality of approach and methods |")
        markdown.append(f"| Impact | 25% | Potential influence on the field |")
        markdown.append(f"| Technical Innovation | 25% | Advances in AI methodologies |")
        markdown.append(f"| Applicability | 20% | Practical relevance and use cases |")
        markdown.append(f"")
        
        markdown.append(f"### Research Categories")
        markdown.append(f"")
        markdown.append(f"| Category | Description |")
        markdown.append(f"|----------|-------------|")
        markdown.append(f"| Deep Learning for Protein Structure Prediction | Methods using deep learning to predict protein 3D structures |")
        markdown.append(f"| Generative Models for Protein Design | Models that generate novel protein sequences or structures |")
        markdown.append(f"| Reinforcement Learning for Protein Engineering | Using reinforcement learning to optimize protein properties |")
        markdown.append(f"| Multi-objective Optimization in Protein Design | Methods that balance multiple design objectives simultaneously |")
        markdown.append(f"| Transfer Learning in Protein Engineering | Applying knowledge from one protein domain to another |")
        markdown.append(f"| AI for Protein Function Prediction | Predicting protein functions from sequence or structure |")
        markdown.append(f"| Computational Protein-Protein Interaction Design | Designing protein-protein interactions and complexes |")
        markdown.append(f"| Protein Design for Therapeutics | Designing proteins for medical applications |")
        markdown.append(f"| Enzyme Engineering with AI | Using AI to engineer enzymes with improved properties |")
        markdown.append(f"| Protein Nanomaterials Design | Designing protein-based nanomaterials and assemblies |")
        markdown.append(f"")
        
        # Footer
        markdown.append(f"---")
        markdown.append(f"")
        markdown.append(f"> *This report was automatically generated by the Protein AI Literature Analysis skill.*")
        markdown.append(f"> *For updates or custom analyses, please run the literature retrieval pipeline again.*")
        
        # Join markdown lines
        report_content = '\n'.join(markdown)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Report generated successfully!")
        print(f"Saved to: {output_file}")
        print(f"Total pages: {total_papers}")
        print(f"Report length: {len(report_content)} characters")
    
    def run(self, input_file, output_file):
        """Run the full report generation process"""
        print(f"Starting report generation...")
        
        # Load analyzed papers
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        
        # Generate report
        self.generate_markdown_report(input_data, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AI & protein design literature report")
    parser.add_argument('--input', default='data/analyzed_papers.json', help='Input JSON file with analyzed papers')
    parser.add_argument('--output', default='reports/latest_literature_analysis.md', help='Output markdown report file')
    
    args = parser.parse_args()
    
    generator = ReportGenerator()
    generator.run(args.input, args.output)
