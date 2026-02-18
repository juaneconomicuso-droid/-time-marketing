#!/usr/bin/env python3
"""
Scraper para JOTA - Notícias Tributárias
Busca notícias sobre CARF, planejamento tributário e Reforma Tributária
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def scrape_jota():
    """Busca notícias tributárias no JOTA"""
    
    base_url = "https://www.jota.info"
    search_terms = ["CARF", "planejamento tributário", "Reforma Tributária", "IBS", "CBS"]
    
    results = {
        "fonte": "JOTA",
        "data_busca": datetime.now().isoformat(),
        "noticias": []
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Tenta acessar a seção de tributos
        url = f"{base_url}/tributos-e-empresas"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Busca artigos (ajustar seletores conforme estrutura real do site)
        articles = soup.find_all('article', limit=20)
        
        for article in articles:
            try:
                # Extrai título
                title_elem = article.find(['h2', 'h3', 'h1'])
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                
                # Verifica se contém palavras-chave relevantes
                if not any(term.lower() in title.lower() for term in search_terms):
                    continue
                
                # Extrai link
                link_elem = article.find('a', href=True)
                link = link_elem['href'] if link_elem else None
                if link and not link.startswith('http'):
                    link = base_url + link
                
                # Extrai resumo/descrição
                desc_elem = article.find(['p', 'div'], class_=['excerpt', 'description', 'summary'])
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extrai data (se disponível)
                date_elem = article.find(['time', 'span'], class_=['date', 'published'])
                pub_date = date_elem.get_text(strip=True) if date_elem else None
                
                noticia = {
                    "titulo": title,
                    "link": link,
                    "resumo": description[:300] if description else "",
                    "data_publicacao": pub_date,
                    "palavras_chave": [term for term in search_terms if term.lower() in title.lower()]
                }
                
                results["noticias"].append(noticia)
                
            except Exception as e:
                print(f"Erro ao processar artigo: {e}")
                continue
        
        print(f"✅ JOTA: {len(results['noticias'])} notícias encontradas")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar JOTA: {e}")
        results["erro"] = str(e)
    
    # Salva resultados
    os.makedirs('data/news', exist_ok=True)
    output_file = f"data/news/jota_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Resultados salvos em: {output_file}")
    return results

if __name__ == "__main__":
    scrape_jota()
