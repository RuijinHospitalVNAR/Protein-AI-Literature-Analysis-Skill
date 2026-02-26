#!/usr/bin/env python3
"""
Paper Analyzer for Protein AI Literature Analysis

This script analyzes retrieved papers on AI-driven protein design:
- Classifies papers into research categories
- Scores importance based on multiple criteria
- Generates detailed evaluations

Usage:
    python paper_analyzer.py --input data/papers.json --output data/analyzed_papers.json
"""

import argparse
import json
import re
from collections import defaultdict

class PaperAnalyzer:
    def __init__(self):
        # Define classification categories and keywords
        self.categories = {
            'Deep Learning for Protein Structure Prediction': {
                'keywords': ['structure prediction', 'AlphaFold', 'RoseTTAFold', 'protein structure', 'fold prediction'],
                'description': 'Methods using deep learning to predict protein 3D structures'
            },
            'Generative Models for Protein Design': {
                'keywords': ['generative model', 'GPT', 'diffusion', 'VAE', 'GAN', 'protein generation', 'de novo design'],
                'description': 'Models that generate novel protein sequences or structures'
            },
            'Reinforcement Learning for Protein Engineering': {
                'keywords': ['reinforcement learning', 'RL', 'policy gradient', 'Q-learning', 'protein engineering'],
                'description': 'Using reinforcement learning to optimize protein properties'
            },
            'Multi-objective Optimization in Protein Design': {
                'keywords': ['multi-objective', 'Pareto', 'optimization', 'trade-off', 'multi-criteria'],
                'description': 'Methods that balance multiple design objectives simultaneously'
            },
            'Transfer Learning in Protein Engineering': {
                'keywords': ['transfer learning', 'fine-tuning', 'pre-trained', 'domain adaptation'],
                'description': 'Applying knowledge from one protein domain to another'
            },
            'AI for Protein Function Prediction': {
                'keywords': ['function prediction', 'annotation', 'protein function', 'activity prediction'],
                'description': 'Predicting protein functions from sequence or structure'
            },
            'Computational Protein-Protein Interaction Design': {
                'keywords': ['protein-protein interaction', 'PPI', 'interaction design', 'binding interface'],
                'description': 'Designing protein-protein interactions and complexes'
            },
            'Protein Design for Therapeutics': {
                'keywords': ['therapeutic', 'drug design', 'biologic', 'pharmaceutical', 'medicine'],
                'description': 'Designing proteins for medical applications'
            },
            'Enzyme Engineering with AI': {
                'keywords': ['enzyme', 'catalysis', 'biocatalyst', 'enzyme engineering'],
                'description': 'Using AI to engineer enzymes with improved properties'
            },
            'Protein Nanomaterials Design': {
                'keywords': ['nanomaterial', 'self-assembly', 'nanoparticle', 'protein material'],
                'description': 'Designing protein-based nanomaterials and assemblies'
            }
        }
    
    def classify_paper(self, paper):
        """Classify a paper into one or more research categories"""
        text = f"{paper['title']} {paper['abstract']}".lower()
        classifications = []
        
        for category, info in self.categories.items():
            if any(keyword in text for keyword in info['keywords']):
                classifications.append(category)
        
        # Handle papers that don't fit any category
        if not classifications:
            classifications.append('Other')
        
        return classifications
    
    def score_importance(self, paper):
        """Score paper importance on a 1-10 scale"""
        score = 0
        
        # Novelty (30%)
        novelty_score = self._score_novelty(paper)
        score += novelty_score * 0.3
        
        # Impact (25%)
        impact_score = self._score_impact(paper)
        score += impact_score * 0.25
        
        # Technical Innovation (25%)
        tech_score = self._score_technical_innovation(paper)
        score += tech_score * 0.25
        
        # Applicability (20%)
        app_score = self._score_applicability(paper)
        score += app_score * 0.2
        
        return min(10, round(score, 1))
    
    def _score_novelty(self, paper):
        """Score novelty (1-10)"""
        text = f"{paper['title']} {paper['abstract']}".lower()
        
        # Look for novelty indicators
        novelty_indicators = [
            'novel', 'new approach', 'first', 'innovative', 'breakthrough',
            'unprecedented', 'original', 'state-of-the-art', 'advance'
        ]
        
        score = 5  # Base score
        
        # Add points for novelty indicators
        for indicator in novelty_indicators:
            if indicator in text:
                score += 0.5
        
        # Add points for recent publications (within last month)
        import datetime
        try:
            pub_date = paper['publication_date']
            if pub_date:
                # Parse date
                if '-' in pub_date:
                    date_parts = pub_date.split('-')
                    if len(date_parts) >= 3:
                        year, month, day = map(int, date_parts)
                        pub_datetime = datetime.datetime(year, month, day)
                        days_since_pub = (datetime.datetime.now() - pub_datetime).days
                        if days_since_pub <= 30:
                            score += 1
        except:
            pass
        
        return min(10, score)
    
    def _score_impact(self, paper):
        """Score potential impact (1-10)"""
        text = f"{paper['title']} {paper['abstract']}".lower()
        
        # Look for impact indicators
        impact_indicators = [
            'significant', 'important', 'impact', 'broad application',
            'transformative', 'revolutionary', 'game-changer', 'paradigm shift'
        ]
        
        score = 5  # Base score
        
        # Add points for impact indicators
        for indicator in impact_indicators:
            if indicator in text:
                score += 0.5
        
        # Add points for papers in high-impact journals
        high_impact_journals = [
            'nature', 'science', 'cell', 'nature biotechnology', 'science advances',
            'nature methods', 'proceedings of the national academy of sciences', 'pnas'
        ]
        
        journal = paper.get('journal', '').lower()
        for high_impact in high_impact_journals:
            if high_impact in journal:
                score += 2
                break
        
        return min(10, score)
    
    def _score_technical_innovation(self, paper):
        """Score technical innovation (1-10)"""
        text = f"{paper['title']} {paper['abstract']}".lower()
        
        # Look for technical innovation indicators
        tech_indicators = [
            'deep learning', 'machine learning', 'artificial intelligence',
            'neural network', 'algorithm', 'methodology', 'technique',
            'framework', 'architecture', 'model'
        ]
        
        score = 5  # Base score
        
        # Add points for technical indicators
        for indicator in tech_indicators:
            if indicator in text:
                score += 0.3
        
        # Add points for specific advanced techniques
        advanced_techniques = [
            'transformer', 'diffusion model', 'reinforcement learning',
            'graph neural network', 'attention mechanism', 'generative model'
        ]
        
        for technique in advanced_techniques:
            if technique in text:
                score += 0.5
        
        return min(10, score)
    
    def _score_applicability(self, paper):
        """Score practical applicability (1-10)"""
        text = f"{paper['title']} {paper['abstract']}".lower()
        
        # Look for applicability indicators
        app_indicators = [
            'application', 'practical', 'useful', 'implement',
            'deploy', 'real-world', 'industry', 'commercial',
            'therapeutic', 'medical', 'diagnostic', 'biotechnological'
        ]
        
        score = 5  # Base score
        
        # Add points for applicability indicators
        for indicator in app_indicators:
            if indicator in text:
                score += 0.4
        
        return min(10, score)
    
    def generate_evaluation(self, paper):
        """Generate a brief evaluation of the paper"""
        text = f"{paper['title']} {paper['abstract']}".lower()
        evaluation = []
        
        # Evaluate novelty
        if any(word in text for word in ['novel', 'new approach', 'first', 'innovative']):
            evaluation.append('Presents novel approach')
        
        # Evaluate technical quality
        if any(word in text for word in ['deep learning', 'machine learning', 'algorithm']):
            evaluation.append('Utilizes advanced AI techniques')
        
        # Evaluate impact potential
        if any(word in text for word in ['significant', 'important', 'impact']):
            evaluation.append('Has potential for significant impact')
        
        # Evaluate practical applications
        if any(word in text for word in ['application', 'practical', 'therapeutic']):
            evaluation.append('Shows practical applicability')
        
        # Add default if no specific evaluations
        if not evaluation:
            evaluation.append('Contributes to the field of AI-driven protein design')
        
        return '; '.join(evaluation)
    
    def analyze_papers(self, papers):
        """Analyze all papers in the dataset"""
        analyzed_papers = []
        category_counts = defaultdict(int)
        
        for paper in papers:
            # Classify paper
            classifications = self.classify_paper(paper)
            paper['classifications'] = classifications
            
            # Score importance
            importance_score = self.score_importance(paper)
            paper['importance_score'] = importance_score
            
            # Generate evaluation
            evaluation = self.generate_evaluation(paper)
            paper['evaluation'] = evaluation
            
            # Add to analyzed papers
            analyzed_papers.append(paper)
            
            # Update category counts
            for category in classifications:
                category_counts[category] += 1
        
        # Sort papers by importance score (descending)
        analyzed_papers.sort(key=lambda x: x['importance_score'], reverse=True)
        
        return analyzed_papers, dict(category_counts)
    
    def run(self, input_file, output_file):
        """Run the full analysis process"""
        print(f"Starting paper analysis...")
        
        # Load papers
        with open(input_file, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        print(f"Analyzing {len(papers)} papers...")
        
        # Analyze papers
        analyzed_papers, category_counts = self.analyze_papers(papers)
        
        # Save results
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        output_data = {
            'papers': analyzed_papers,
            'category_counts': category_counts,
            'total_papers': len(analyzed_papers),
            'average_importance_score': sum(p['importance_score'] for p in analyzed_papers) / len(analyzed_papers) if analyzed_papers else 0
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print(f"\nAnalysis complete!")
        print(f"Total papers analyzed: {len(analyzed_papers)}")
        print(f"Average importance score: {output_data['average_importance_score']:.2f}")
        print(f"\nCategory distribution:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}")
        
        print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze AI & protein design papers")
    parser.add_argument('--input', default='data/papers.json', help='Input JSON file with papers')
    parser.add_argument('--output', default='data/analyzed_papers.json', help='Output JSON file with analysis')
    
    args = parser.parse_args()
    
    analyzer = PaperAnalyzer()
    analyzer.run(args.input, args.output)
