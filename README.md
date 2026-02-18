# Time Marketing - Economic Consultoria

Sistema automatizado de busca, análise e produção de conteúdo tributário para a Economic Consultoria.

## 📋 Visão Geral

Este projeto resolve o problema de **acesso à internet limitado** no ambiente local, usando **GitHub Actions** para executar scrapers automaticamente na nuvem e armazenar os resultados no repositório.

### Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│              GITHUB ACTIONS (Cloud)                      │
│  Scrapers executam diariamente com acesso à internet    │
│  Resultados salvos em data/news/*.json                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AMBIENTE LOCAL (Sem internet)               │
│  Consome dados já coletados do repositório              │
│  @monitor analisa → Squad Marketing produz conteúdo     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Como Funciona

### 1. Busca Automática de Notícias (GitHub Actions)

**Quando:** Todo dia às 8h (horário de Brasília)  
**Onde:** GitHub Actions (runners na nuvem com acesso à internet)  
**O que faz:**
- Busca notícias em JOTA, Conjur, Tributário nos Bastidores
- Parse de RSS feeds (Receita Federal, etc.)
- Filtra por palavras-chave: CARF, Reforma Tributária, IBS, CBS, planejamento tributário
- Salva resultados em `data/news/consolidado_YYYYMMDD.json`
- Faz commit automático no repositório

### 2. Consumo Local dos Dados

No ambiente local (sem internet), você:
1. Faz `git pull` para baixar as notícias coletadas
2. Lê o arquivo `data/news/consolidado_YYYYMMDD.json`
3. Escolhe uma notícia relevante
4. Aciona `@qa-marketing *produzir [notícia]`
5. O sistema produz todos os formatos automaticamente

---

## 📁 Estrutura do Projeto

```
time-marketing/
├── .github/
│   └── workflows/
│       └── scrape-carf-news.yml          # Workflow automático
├── squads/
│   ├── economic-marketing/               # Squad de marketing
│   │   ├── monitor.md
│   │   ├── newsletter.md
│   │   ├── reels.md
│   │   ├── carrossel.md
│   │   ├── linkedin.md
│   │   ├── comercial.md
│   │   └── qa-marketing.md
│   └── dev-squad/                        # Squad de devs
│       ├── web-scraper.md
│       ├── api-integrator.md
│       ├── automation-engineer.md
│       ├── devops.md
│       └── tech-lead.md
├── scripts/
│   └── scrapers/
│       ├── scrape_jota.py                # Scraper JOTA
│       ├── scrape_conjur.py              # Scraper Conjur
│       ├── scrape_tributario.py          # Scraper Tributário nos Bastidores
│       ├── parse_rss_feeds.py            # Parser de RSS feeds
│       ├── consolidate_results.py        # Consolidador de resultados
│       └── requirements.txt              # Dependências Python
├── data/
│   └── news/                             # Notícias coletadas (JSON)
└── output/                               # Conteúdos produzidos
```

---

## ⚙️ Configuração Inicial

### 1. Ativar GitHub Actions

1. Vá em **Settings** → **Actions** → **General**
2. Marque **"Allow all actions and reusable workflows"**
3. Em **Workflow permissions**, marque **"Read and write permissions"**
4. Salve as configurações

### 2. Executar Manualmente (Primeira Vez)

1. Vá em **Actions** → **Buscar Notícias CARF e Tributárias**
2. Clique em **Run workflow** → **Run workflow**
3. Aguarde ~2-3 minutos
4. Verifique se os arquivos foram criados em `data/news/`

### 3. Baixar Notícias no Ambiente Local

```bash
git pull origin main
```

Agora você tem acesso às notícias coletadas automaticamente!

---

## 📖 Como Usar

### Opção 1: Usar notícias já coletadas

```bash
# 1. Baixar últimas notícias
git pull

# 2. Ver notícias disponíveis
cat data/news/relatorio_YYYYMMDD.md

# 3. Escolher uma notícia e produzir conteúdo
# (copiar texto da notícia e colar no chat)
@qa-marketing *produzir [texto da notícia]
```

### Opção 2: Executar scrapers localmente (se tiver internet)

```bash
cd scripts/scrapers

# Instalar dependências
pip install -r requirements.txt

# Executar scrapers individuais
python scrape_jota.py
python scrape_conjur.py
python parse_rss_feeds.py

# Consolidar resultados
python consolidate_results.py
```

---

## 🤖 Squads Disponíveis

### Squad de Marketing (@economic-marketing)
- **@monitor** — analisa notícias e identifica relevância
- **@newsletter** — produz newsletter premium
- **@reels** — cria roteiros de vídeo para Instagram
- **@carrossel** — produz carrosséis e stories
- **@linkedin** — escreve artigos técnicos
- **@comercial** — gera PDF e mensagens WhatsApp
- **@qa-marketing** — revisa tudo antes de publicar

### Squad de Devs (@dev-squad)
- **@web-scraper** — especialista em scraping e busca
- **@api-integrator** — integração com APIs externas
- **@automation-engineer** — automação de workflows
- **@devops** — infraestrutura e deploy
- **@tech-lead** — orquestrador técnico

---

## 🔧 Troubleshooting

### Problema: GitHub Actions não está executando

**Solução:**
1. Verificar se Actions está habilitado (Settings → Actions)
2. Verificar se há permissões de escrita (Workflow permissions)
3. Executar manualmente: Actions → Run workflow

### Problema: Scrapers falhando

**Solução:**
- Os scrapers têm `continue-on-error: true`, então falhas individuais não param o workflow
- Verificar logs em Actions → última execução
- RSS feeds são mais confiáveis que scraping direto

### Problema: Notícias não aparecem no repositório

**Solução:**
1. Verificar se o commit foi feito: Actions → última execução → logs
2. Fazer `git pull` para baixar
3. Verificar se `data/news/` existe

---

## 📊 Monitoramento

### Ver últimas execuções
1. Ir em **Actions**
2. Clicar em **Buscar Notícias CARF e Tributárias**
3. Ver histórico de execuções

### Ver notícias coletadas
```bash
# JSON consolidado
cat data/news/consolidado_YYYYMMDD.json

# Relatório legível
cat data/news/relatorio_YYYYMMDD.md
```

---

## 🎯 Próximos Passos

- [ ] Adicionar mais fontes (Valor Econômico, Estadão, etc.)
- [ ] Implementar notificações por email/Slack quando houver notícias importantes
- [ ] Criar dashboard web para visualizar notícias
- [ ] Integrar com APIs de publicação (Instagram, LinkedIn, WhatsApp Business)
- [ ] Implementar análise de sentimento e relevância com IA

---

## 📝 Licença

Uso interno - Economic Consultoria

---

## 👥 Contato

Para dúvidas ou sugestões, falar com o time de desenvolvimento.
