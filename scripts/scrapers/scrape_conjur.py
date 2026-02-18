#!/usr/bin/env python3
"""
Scraper para Conjur - Notícias Tributárias
Busca notícias sobre CARF, planejamento tributário e Reforma Tributária
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def scrape_conjur():
    """Busca notícias tributárias no Conjur"""
    
    base_url = "https://www.conjur.com.br"
    search_terms = ["CARF", "planejamento tributário", "Reforma Tributária", "IBS", "CBS"]
    
    results = {
        "fonte": "Conjur",
        "data_busca": datetime.now().isoformat(),
        "noticias": []
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Busca por cada termo
        for term in search_terms[:2]:  # Limita para evitar muitas requisições
            try:
                url = f"{base_url}/busca/?q={term.replace(' ', '+')}"
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Busca resultados (ajustar seletores conforme estrutura real)
                articles = soup.find_all(['article', 'div'], class_=['post', 'item', 'result'], limit=10)
                
                for article in articles:
                    try:
                        # Extrai título
                        title_elem = article.find(['h2', 'h3', 'h1', 'a'])
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        # Evita duplicatas
                        if any(n['titulo'] == title for n in results['noticias']):
                            continue
                        
                        # Extrai link
                        link_elem = article.find('a', href=True)
                        link = link_elem['href'] if link_elem else None
                        if link and not link.startswith('http'):
                            link = base_url + link
                        
                        # Extrai resumo
                        desc_elem = article.find(['p', 'div'], class_=['excerpt', 'description', 'summary'])
                        description = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        # Extrai data
                        date_elem = article.find(['time', 'span'], class_=['date', 'published'])
                        pub_date = date_elem.get_text(strip=True) if date_elem else None
                        
                        noticia = {
                            "titulo": title,
                            "link": link,
                            "resumo": description[:300] if description else "",
                            "data_publicacao": pub_date,
                            "palavras_chave": [t for t in search_terms if t.lower() in title.lower()]
                        }
                        
                        results["noticias"].append(noticia)
                        
                    except Exception as e:
                        print(f"Erro ao processar artigo: {e}")
                        continue
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro ao buscar '{term}' no Conjur: {e}")
                continue
        
        print(f"✅ Conjur: {len(results['noticias'])} notícias encontradas")
        
    except Exception as e:
        print(f"❌ Erro geral no Conjur: {e}")
        results["erro"] = str(e)
    
    # Salva resultados
    os.makedirs('data/news', exist_ok=True)
    output_file = f"data/news/conjur_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Resultados salvos em: {output_file}")
    return results

if __name__ == "__main__":
    scrape_conjur()
