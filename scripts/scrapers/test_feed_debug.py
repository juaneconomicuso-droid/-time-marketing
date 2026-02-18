#!/usr/bin/env python3
"""
Script de debug para testar feeds RSS
Mostra TODAS as notícias sem filtro para verificar se o feed está funcionando
"""

import feedparser

feeds = {
    "Tributário.com.br": "https://tributario.com.br/feed/",
    "JOTA": "https://www.jota.info/feed",
    "Conjur": "https://www.conjur.com.br/feed/",
}

for nome, url in feeds.items():
    print(f"\n{'='*60}")
    print(f"Feed: {nome}")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    try:
        feed = feedparser.parse(url)
        
        print(f"Status: {feed.get('status', 'N/A')}")
        print(f"Total de entradas: {len(feed.entries)}")
        
        if len(feed.entries) == 0:
            print("⚠️ Feed vazio ou inacessível")
            print(f"Bozo: {feed.get('bozo', False)}")
            if feed.get('bozo'):
                print(f"Erro: {feed.get('bozo_exception', 'N/A')}")
        else:
            print(f"\n📰 Primeiras 5 notícias:\n")
            for i, entry in enumerate(feed.entries[:5], 1):
                title = entry.get('title', 'Sem título')
                link = entry.get('link', 'Sem link')
                pub_date = entry.get('published', entry.get('updated', 'Sem data'))
                
                print(f"{i}. {title}")
                print(f"   Link: {link}")
                print(f"   Data: {pub_date}")
                print()
    
    except Exception as e:
        print(f"❌ Erro ao acessar feed: {e}")

print("\n" + "="*60)
print("Debug concluído")
