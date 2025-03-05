import os
import pdfplumber
from datetime import datetime

def pdf_to_md(input_dir="articles", output_file="articles.md"):
    """Конвертирует все PDF-файлы в папке в структурированный Markdown"""
    
    md_content = "# Анализ научных статей\n\n"
    
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith('.pdf'):
            continue
            
        filepath = os.path.join(input_dir, filename)
        article_data = {
            'title': filename[:-4],
            'authors': 'Не указаны',
            'year': 'Не указан',
            'content': ''
        }

        try:
            with pdfplumber.open(filepath) as pdf:
                # Извлечение метаданных
                meta = pdf.metadata
                article_data['title'] = meta.get('Title', article_data['title'])
                article_data['authors'] = meta.get('Author', article_data['authors'])
                
                # Попытка извлечь год из даты создания
                if 'CreationDate' in meta:
                    year = meta['CreationDate'][2:6]
                    if year.isdigit():
                        article_data['year'] = year
                
                # Извлечение текста
                full_text = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text = text.replace('\n', ' ')  # Чистка переносов
                        full_text.append(text)
                
                article_data['content'] = ' '.join(full_text)
                
        except Exception as e:
            print(f"Ошибка обработки {filename}: {str(e)}")
            continue
            
        # Формирование Markdown
        md_content += f"## {article_data['title']}\n\n"
        md_content += f"- **Авторы**: {article_data['authors']}\n"
        md_content += f"- **Год**: {article_data['year']}\n\n"
        md_content += f"```\n{article_data['content']}\n```\n\n"
        md_content += "---\n\n"
    
    # Сохранение в файл
    with open(output_file, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)
    
    print(f"Создан файл: {output_file}")

if __name__ == "__main__":
    pdf_to_md()