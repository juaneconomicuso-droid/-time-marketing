#!/usr/bin/env python3
"""
Parser de RSS Feeds de fontes tributárias
Alternativa mais confiável ao scraping direto
"""

import feedparser
import json
from datetime import datetime
import os

def parse_rss_feeds():
    """Parse RSS feeds de fontes tributárias"""
    
    # Lista de feeds RSS conhecidos
    feeds = {
        "JOTA": "https://www.jota.info/feed",
        "Conjur": "https://www.conjur.com.br/feed/",
        "Tributário.com.br": "https://tributario.com.br/feed/",
        "Receita Federal": "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/RSS",
    }
    
    # Termos mais amplos para capturar mais notícias
    search_terms = ["CARF", "planejamento", "Reforma", "IBS", "CBS", "tributário", "tributo", "imposto", "fiscal", "IRPF", "IRPJ"]
    
    all_results = {
        "data_busca": datetime.now().isoformat(),
        "fontes": []
    }
    
    for fonte_nome, feed_url in feeds.items():
        try:
            print(f"📡 Buscando feed: {fonte_nome}")
            feed = feedparser.parse(feed_url)
            
            fonte_results = {
                "fonte": fonte_nome,
                "feed_url": feed_url,
                "noticias": []
            }
            
            for entry in feed.entries[:20]:  # Limita a 20 mais recentes
                try:
                    title = entry.get('title', '')
                    
                    # Verifica relevância
                    if not any(term.lower() in title.lower() for term in search_terms):
                        continue
                    
                    # Extrai dados
                    link = entry.get('link', '')
                    summary = entry.get('summary', entry.get('description', ''))
                    
                    # Remove HTML do summary se houver
                    from html import unescape
                    import re
                    summary = unescape(summary)
                    summary = re.sub('<[^<]+?>', '', summary)  # Remove tags HTML
                    
                    # Data de publicação
                    pub_date = entry.get('published', entry.get('updated', ''))
                    
                    noticia = {
                        "titulo": title,
                        "link": link,
                        "resumo": summary[:300] if summary else "",
                        "data_publicacao": pub_date,
                        "palavras_chave": [t for t in search_terms if t.lower() in title.lower()]
                    }
                    
                    fonte_results["noticias"].append(noticia)
                    
                except Exception as e:
                    print(f"  ⚠️ Erro ao processar entrada: {e}")
                    continue
            
            print(f"  ✅ {fonte_nome}: {len(fonte_results['noticias'])} notícias encontradas")
            all_results["fontes"].append(fonte_results)
            
        except Exception as e:
            print(f"  ❌ Erro ao acessar feed {fonte_nome}: {e}")
            continue
    
    # Salva resultados
    os.makedirs('data/news', exist_ok=True)
    output_file = f"data/news/rss_feeds_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    total_noticias = sum(len(f['noticias']) for f in all_results['fontes'])
    print(f"\n📁 Total: {total_noticias} notícias de {len(all_results['fontes'])} fontes")
    print(f"📁 Resultados salvos em: {output_file}")
    
    return all_results

if __name__ == "__main__":
    parse_rss_feeds()
