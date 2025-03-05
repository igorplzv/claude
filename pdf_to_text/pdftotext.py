import PyPDF2
import re
import os
import json
from typing import Dict, List

class ArticleExtractor:
   def __init__(self):
       self.required_fields = ['title', 'authors', 'journal', 'doi']

   def extract_text_from_pdf(self, pdf_path: str) -> str:
       try:
           with open(pdf_path, 'rb') as file:
               reader = PyPDF2.PdfReader(file)
               return ' '.join(page.extract_text() for page in reader.pages[:2])
       except Exception as e:
           print(f"Error extracting text from {pdf_path}: {str(e)}")
           return ''

   def extract_metadata(self, text: str) -> Dict:
       metadata = {
           'title': '',
           'authors': [],
           'abstract': '',
           'keywords': [],
           'doi': '',
           'journal': '',
       }

       # Extract title
       text_lines = text.split('\n')
       for line in text_lines[:10]:
           stripped = line.strip()
           if len(stripped) > 20 and stripped[0].isupper() and not stripped.startswith('Authors'):
               metadata['title'] = stripped
               break

       # Extract authors
       authors_pattern = r'(?:Authors?:|Contributors:)([^*\n]+?)(?=\n\s*[a-z]|Division|Department|School)'
       authors_match = re.search(authors_pattern, text, re.IGNORECASE | re.DOTALL)
       if authors_match:
           authors_text = authors_match.group(1)
           authors_text = re.sub(r'[,*†‡§]+', ',', authors_text)
           authors = [a.strip() for a in re.split(r',\s*|\s+and\s+', authors_text)]
           metadata['authors'] = [a for a in authors if a and len(a) > 1]

       # Extract journal
       journal_patterns = [
           r'journal homepage: www\.([^/\s]+)\.com',
           r'Available online at ScienceDirect\n+([\w\s&]+)',
           r'(?:Journal|Materials|Acta)[^(\n]{5,}',
           r'(?i)^((?:Journal|Materials|Acta)[^\d\n]{10,})'
       ]
       
       for pattern in journal_patterns:
           journal_match = re.search(pattern, text, re.IGNORECASE)
           if journal_match:
               try:
                   journal = journal_match.group(1).strip()
               except IndexError:
                   journal = journal_match.group(0).strip()
               metadata['journal'] = journal.replace('www.', '').replace('.com', '')
               break

       # Extract DOI
       doi_patterns = [
           r'doi\.org/(10\.\d{4,}/[-._;()/:\w]+)',
           r'DOI:\s*(10\.\d{4,}/[-._;()/:\w]+)',
           r'https?://doi\.org/(10\.\d{4,}/[-._;()/:\w]+)'
       ]
       
       for pattern in doi_patterns:
           doi_match = re.search(pattern, text, re.IGNORECASE)
           if doi_match:
               metadata['doi'] = doi_match.group(1)
               break

       # Extract abstract
       abstract_match = re.search(r'Abstract[:\s]*\n*(.*?)(?=Introduction|Keywords|1\.|$)', 
                                text, re.IGNORECASE | re.DOTALL)
       if abstract_match:
           metadata['abstract'] = abstract_match.group(1).strip()

       # Extract keywords
       keywords_match = re.search(r'Keywords?[:\s]*(.*?)(?:\n\n|\.|$)', text, re.IGNORECASE)
       if keywords_match:
           metadata['keywords'] = [k.strip() for k in keywords_match.group(1).split(';')]

       return metadata

   def verify_metadata(self, metadata: Dict) -> Dict:
       missing_fields = []
       for field in self.required_fields:
           if not metadata.get(field):
               missing_fields.append(field)
       return {
           'complete': len(missing_fields) == 0,
           'missing_fields': missing_fields
       }

   def process_article(self, pdf_path: str) -> Dict:
       text = self.extract_text_from_pdf(pdf_path)
       if not text:
           return {}

       metadata = self.extract_metadata(text)
       verification = self.verify_metadata(metadata)
       
       return {
           'metadata': metadata,
           'verification': verification,
           'filename': os.path.basename(pdf_path)
       }

   def process_directory(self, input_dir: str, output_file: str):
       results = []
       pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
       
       print(f"\nProcessing {len(pdf_files)} PDF files...")
       
       for filename in pdf_files:
           pdf_path = os.path.join(input_dir, filename)
           result = self.process_article(pdf_path)
           if result:
               results.append(result)

       with open(output_file, 'w', encoding='utf-8') as f:
           json.dump(results, f, indent=2, ensure_ascii=False)
           
       print(f"\nResults saved to {output_file}")
       
       complete = sum(1 for r in results if r.get('verification', {}).get('complete', False))
       print(f"\nExtraction summary:")
       print(f"Successfully processed: {complete}/{len(results)} articles")

def main():
   extractor = ArticleExtractor()
   extractor.process_directory('articles', 'output.json')

if __name__ == '__main__':
   main()