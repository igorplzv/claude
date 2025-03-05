import PyPDF2
from typing import Dict, List
import re
import os
import json

class ArticleExtractor:
    def detect_publisher(self, text: str) -> str:
        publishers = {
            'elsevier': r'elsevier',
            'springer': r'springer',
            'mdpi': r'mdpi'
        }
        for publisher, pattern in publishers.items():
            if re.search(pattern, text, re.IGNORECASE):
                return publisher
        return 'other'

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return ' '.join(page.extract_text() for page in reader.pages)
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {str(e)}")
            return ''

    def extract_metadata(self, text: str) -> Dict:
        metadata = {
            'title': '',
            'authors': [],
            'abstract': '',
            'keywords': [],
            'doi': ''
        }

        # Title
        title_match = re.search(r'(?:Title|Original Article)[:\s]*\n*([^\n]+)', text)
        if title_match:
            metadata['title'] = title_match.group(1).strip()

        # Authors
        authors_match = re.search(r'(?:Authors?|Contributors?)[:\s]*([^*\n]+?)(?:\n|$)', text)
        if authors_match:
            authors = [a.strip() for a in authors_match.group(1).split(',')]
            metadata['authors'] = [a for a in authors if a]

        # Abstract
        abstract_match = re.search(r'Abstract[:\s]*\n*(.*?)(?=(?:Introduction|Keywords|1\.|$))', 
                                 text, re.IGNORECASE | re.DOTALL)
        if abstract_match:
            metadata['abstract'] = abstract_match.group(1).strip()

        # DOI
        doi_match = re.search(r'(?:DOI|doi)[:\s]*(10\.\d{4,}/[-._;()/:\w]+)', text)
        if doi_match:
            metadata['doi'] = doi_match.group(1)

        # Keywords
        keywords_match = re.search(r'Keywords?[:\s]*(.*?)(?:\n\n|\.|$)', text, re.IGNORECASE)
        if keywords_match:
            metadata['keywords'] = [k.strip() for k in keywords_match.group(1).split(';')]

        return metadata

    def extract_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        headers = ['Introduction', 'Methods', 'Results', 'Discussion', 'Conclusion']
        
        for i, header in enumerate(headers):
            next_header = headers[i+1] if i < len(headers)-1 else None
            pattern = fr'{header}[:\s]*\n*(.*?)(?={next_header}|\n\n\n|$)' if next_header else fr'{header}[:\s]*\n*(.*?)(?:\n\n\n|$)'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[header] = match.group(1).strip()

        return sections

    def process_article(self, pdf_path: str) -> Dict:
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {}

        publisher = self.detect_publisher(text)
        metadata = self.extract_metadata(text)
        sections = self.extract_sections(text)

        return {
            'metadata': metadata,
            'sections': sections,
            'publisher': publisher
        }

    def process_directory(self, input_dir: str, output_file: str):
        results = []
        for filename in os.listdir(input_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(input_dir, filename)
                result = self.process_article(pdf_path)
                result['filename'] = filename
                results.append(result)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    extractor = ArticleExtractor()
    extractor.process_directory('articles', 'output.json')

if __name__ == '__main__':
    main()