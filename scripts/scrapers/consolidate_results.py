#!/usr/bin/env python3
"""
Consolidador de resultados de scraping
Unifica todos os JSONs gerados em um único arquivo consolidado
"""

import json
import os
from datetime import datetime
from pathlib import Path

def consolidate_results():
    """Consolida todos os resultados de scraping em um único arquivo"""
    
    data_dir = Path('data/news')
    today = datetime.now().strftime('%Y%m%d')
    
    # Busca todos os arquivos JSON do dia
    json_files = list(data_dir.glob(f'*_{today}.json'))
    
    if not json_files:
        print("⚠️ Nenhum arquivo de notícias encontrado para hoje")
        return
    
    consolidated = {
        "data_consolidacao": datetime.now().isoformat(),
        "total_fontes": 0,
        "total_noticias": 0,
        "fontes": []
    }
    
    print(f"📦 Consolidando {len(json_files)} arquivos...")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Processa diferentes formatos
            if 'fontes' in data:  # Formato RSS feeds
                for fonte in data['fontes']:
                    consolidated['fontes'].append(fonte)
                    consolidated['total_noticias'] += len(fonte.get('noticias', []))
            elif 'noticias' in data:  # Formato scraper individual
                consolidated['fontes'].append({
                    "fonte": data.get('fonte', 'Desconhecida'),
                    "noticias": data['noticias']
                })
                consolidated['total_noticias'] += len(data['noticias'])
            
            print(f"  ✅ {json_file.name}")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {json_file.name}: {e}")
            continue
    
    consolidated['total_fontes'] = len(consolidated['fontes'])
    
    # Remove duplicatas baseado no título
    seen_titles = set()
    for fonte in consolidated['fontes']:
        noticias_unicas = []
        for noticia in fonte.get('noticias', []):
            titulo = noticia.get('titulo', '').lower().strip()
            if titulo and titulo not in seen_titles:
                seen_titles.add(titulo)
                noticias_unicas.append(noticia)
        fonte['noticias'] = noticias_unicas
    
    # Recalcula total após remoção de duplicatas
    consolidated['total_noticias'] = sum(len(f['noticias']) for f in consolidated['fontes'])
    
    # Salva consolidado
    output_file = data_dir / f'consolidado_{today}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(consolidated, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Consolidação concluída!")
    print(f"📊 Total: {consolidated['total_noticias']} notícias únicas de {consolidated['total_fontes']} fontes")
    print(f"📁 Arquivo: {output_file}")
    
    # Cria também um arquivo markdown legível
    create_markdown_report(consolidated, data_dir / f'relatorio_{today}.md')
    
    return consolidated

def create_markdown_report(data, output_file):
    """Cria relatório em Markdown para fácil leitura"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Relatório de Notícias Tributárias\n\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        f.write(f"**Total de notícias:** {data['total_noticias']}\n")
        f.write(f"**Total de fontes:** {data['total_fontes']}\n\n")
        f.write("---\n\n")
        
        for fonte in data['fontes']:
            fonte_nome = fonte.get('fonte', 'Desconhecida')
            noticias = fonte.get('noticias', [])
            
            f.write(f"## {fonte_nome} ({len(noticias)} notícias)\n\n")
            
            for i, noticia in enumerate(noticias, 1):
                titulo = noticia.get('titulo', 'Sem título')
                link = noticia.get('link', '#')
                resumo = noticia.get('resumo', '')
                data_pub = noticia.get('data_publicacao', 'Data não disponível')
                palavras_chave = ', '.join(noticia.get('palavras_chave', []))
                
                f.write(f"### {i}. {titulo}\n\n")
                f.write(f"**Link:** {link}\n\n")
                f.write(f"**Data:** {data_pub}\n\n")
                if palavras_chave:
                    f.write(f"**Palavras-chave:** {palavras_chave}\n\n")
                if resumo:
                    f.write(f"**Resumo:** {resumo}\n\n")
                f.write("---\n\n")
    
    print(f"📄 Relatório Markdown: {output_file}")

if __name__ == "__main__":
    consolidate_results()
