# Cadastro automático de histórias no Jira (via YAML + Streamlit)

Este projeto implementa uma pequena aplicação interna para facilitar o **cadastro em massa de histórias/tarefas no Jira**, usando:

- Arquivos de configuração em **YAML** (backlog como código)
- Uma interface em **Streamlit** para edição e disparo das histórias
- Um backend em Python com boas práticas de **Engenharia de Software, SOLID e Clean Architecture**
- Registro de histórico em um banco **SQLite** local

---

## 🚀 Motivação – Por que essa solução existe?

Criar várias histórias manualmente pela UI do Jira é:

- Repetitivo  
- Propenso a erros  
- Difícil de versionar (não há histórico de “como” as histórias foram definidas)

Este projeto foi criado para resolver isso:

- Permitir definir histórias como **configuração em arquivo** (`stories_example.yaml`)
- Editar esse arquivo de forma amigável via uma **tela simples em Streamlit**
- Enviar tudo para o Jira de uma vez, com **registro de histórico local** (SQLite)
- Reaproveitar o mesmo mecanismo em **cursos, treinamentos e projetos Sirius**

Em resumo:

> **Menos clique manual, mais automação, rastreabilidade e reprodutibilidade.**

---

## 🧩 O que a aplicação faz (visão geral)

- Lê histórias definidas em YAML (modo “**backlog as code**”)
- Permite editar esse YAML diretamente em uma tela Streamlit
- Converte cada história em issues no Jira, via **API oficial** (`/rest/api/3/issue`)
- Converte a descrição texto para o formato exigido pelo Jira Cloud (**Atlassian Document Format – ADF**)
- Guarda em `SQLite`:
  - Histórico de issues criadas (`issue_history`)
  - Logs operacionais (`app_log`)

Você pode usar a aplicação de duas formas:

1. **UI (recomendado)**
   - `run_ui.bat` (Windows) → abre a tela em `http://localhost:8501`
   - Aba **“Modo YAML”** para edição e envio em lote
   - Aba **“Modo simples”** para uma história rápida

2. **CLI**
   - `python -m src.main --mode single`
   - `python -m src.main --mode test-two`
   - `python -m src.main --mode bulk --input-file data/stories_example.yaml`

---

## 📁 Estrutura do repositório

Pensando no diretório `apps/cadastro-jira`:

```text
apps/
  cadastro-jira/
    data/
      stories_example.yaml   # Arquivo de configuração YAML das histórias
      app_logs.db            # Banco SQLite com logs e histórico (criado em runtime)

    src/
      __init__.py
      config.py              # Lê variáveis de ambiente (.env) e centraliza configuração Jira
      jira_client.py         # Cliente HTTP para Jira REST API (inclui conversão p/ ADF)
      models.py              # Modelos de domínio (ex.: Story)

      loaders/
        __init__.py
        yaml_loader.py       # Parser do YAML (inclui suporte a separador ';' entre blocos)

      use_cases/
        __init__.py
        create_single_issue.py  # Caso de uso: criar 1 história
        create_bulk_issues.py   # Caso de uso: criar várias histórias

      ui/
        __init__.py
        streamlit_app.py     # Interface web (Streamlit): abas Modo YAML + Modo simples

      logging_db.py          # Integração com SQLite: issue_history + app_log

    .env.example             # Exemplo de configuração de ambiente
    requirements.txt         # Dependências com faixas de versões
    requirements-lock.txt    # (opcional) Dependências travadas por pip freeze
    run_ui.bat               # Script para abrir a UI no Windows
    README.md                # Este arquivo
```

### 🔍 O que cada diretório e arquivo faz

- **`data/stories_example.yaml`**
  - Onde você define as histórias em YAML.
  - Suporta:
    - uma única história
    - várias histórias em lista
    - **vários blocos** separados por linhas com apenas `;`.

- **`data/app_logs.db`**
  - Banco SQLite com duas tabelas:
    - `issue_history` → cada issue criada (UI ou CLI) gera um registro.
    - `app_log` → logs de erros/avisos de uso da aplicação.
  - **Não deve ser commitado** se contiver dados sensíveis.

- **`src/config.py`**
  - Lê `.env` usando `python-dotenv`.
  - Centraliza a configuração Jira:
    - `JIRA_BASE_URL`
    - `JIRA_EMAIL`
    - `JIRA_API_TOKEN`
    - `JIRA_PROJECT_KEY`
    - `JIRA_ISSUE_TYPE`.

- **`src/jira_client.py`**
  - Cuida de falar com a API do Jira (`/rest/api/3/issue`).
  - Constrói o header de autenticação (`Basic <base64(email:token)>`).
  - Converte a descrição texto para **ADF** (documento Atlassian).

- **`src/models.py`**
  - Define a classe `Story` (título, descrição, tasks).
  - Método `full_description()` monta a descrição formatada para envio ao Jira.

- **`src/loaders/yaml_loader.py`**
  - Converte o texto YAML (incluindo múltiplos blocos separados por `;`) em uma lista de `Story`.
  - Interpreta o campo `tasks` como:
    - lista YAML normal (`- tarefa 1`, `- tarefa 2`); e/ou
    - string com `;` (ex.: `"Tarefa 1; Tarefa 2"`).

- **`src/use_cases/create_single_issue.py`**
  - Caso de uso que orquestra a criação de uma história (1 issue) via `JiraClient`.

- **`src/use_cases/create_bulk_issues.py`**
  - Caso de uso para criar várias histórias em sequência.

- **`src/ui/streamlit_app.py`**
  - UI principal:
    - Aba **“Modo YAML”**: edição de `stories_example.yaml`, preview e criação em massa.
    - Aba **“Modo simples (1 história)”**: criação rápida de uma única história.

- **`src/logging_db.py`**
  - Funções para:
    - inicializar o SQLite (`init_db`)
    - registrar histórico de issues (`log_issue_creation`)
    - registrar logs de eventos (`log_app_event`).

- **`run_ui.bat`**
  - Ativa o ambiente virtual `.venv` (Windows).
  - Executa `streamlit run src\ui\streamlit_app.py`.
  - Pode precisar de ajustes conforme o seu ambiente (detalhado mais abaixo).

---

## 🧪 Por que usar um ambiente virtual (`.venv`)?

Um **ambiente virtual** isola as dependências do seu projeto:

- Evita conflito entre versões de bibliotecas usadas por outros projetos.
- Permite congelar versões e ter **reprodutibilidade** (todo mundo usa as mesmas libs).
- Facilita o uso em treinamentos e ambientes corporativos:
  - cada projeto traz **apenas o que precisa**.

Sem `venv`, você pode:

- quebrar outro projeto ao atualizar uma lib aqui; ou
- quebrar esta aplicação ao atualizar uma lib em outro lugar.

Por isso, este projeto **assume e recomenda fortemente** o uso de um ambiente virtual.

---

## 🛠️ Como criar e ativar o ambiente virtual

### Pré-requisitos

- Python 3.x instalado e acessível via `python` ou `py` no terminal.
- Estar dentro de `apps/cadastro-jira` ao rodar os comandos.

---

### 🪟 Windows (CMD / PowerShell)

#### CMD (Prompt de Comando)

```bat
cd apps\cadastro-jira

REM Criar ambiente virtual
python -m venv .venv

REM Ativar ambiente virtual
.\.venv\Scripts\activate

REM (Você verá algo como) (.venv) C:\Users\...\apps\cadastro-jira>
```

#### PowerShell

```powershell
cd apps\cadastro-jira

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie scripts (`ExecutionPolicy`), você pode (com cuidado):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

> ⚠️ Ajuste de `ExecutionPolicy` deve respeitar as políticas de segurança da sua empresa.

---

### 🐧 Linux / WSL / Git Bash

No terminal (Bash, WSL ou Git Bash):

```bash
cd apps/cadastro-jira

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

Após ativar, o prompt geralmente muda para algo como:

```bash
(.venv) user@host:~/Desktop/github/apps/cadastro-jira$
```

---

## 📦 Gerenciando dependências com `requirements.txt` e lock

### Instalar dependências com `requirements.txt`

Depois de ativar o `.venv`, rode:

```bash
pip install -r requirements.txt
```

- O arquivo `requirements.txt` contém as bibliotecas necessárias com faixas de versões estáveis (por exemplo `>=x,<y`).
- Se você tentar rodar a aplicação sem esse passo, verá erros como:
  - `ModuleNotFoundError: No module named 'streamlit'`
  - `ModuleNotFoundError: No module named 'yaml'`
  - `ModuleNotFoundError: No module named 'requests'`

> ✅ **Sempre** ative o `.venv` e rode `pip install -r requirements.txt` ao configurar o projeto em uma máquina nova.

---

### Congelar versões exatas com `pip freeze > requirements-lock.txt`

Para congelar as versões exatas instaladas no seu ambiente (útil para produção e treinamentos):

```bash
pip freeze > requirements-lock.txt
```

- Isso gera um arquivo com todas as dependências utilizadas **com versões específicas**.
- No futuro, você pode recriar exatamente o mesmo ambiente com:

```bash
pip install -r requirements-lock.txt
```

---

## 🔐 Arquivo `.env` – configuração do Jira

Crie o arquivo `.env` na raiz de `apps/cadastro-jira` a partir do modelo:

```bash
cp .env.example .env
```

Edite `.env` com os valores reais:

```env
JIRA_BASE_URL=https://suaorg.atlassian.net
JIRA_EMAIL=seu.email@empresa.com
JIRA_API_TOKEN=seu_token_de_api_jira
JIRA_PROJECT_KEY=SUAKEY
JIRA_ISSUE_TYPE=Task   # ou Story, História etc. (de acordo com o projeto)
```

> ⚠️ **Nunca** commit o `.env` no Git.  
> Ele contém token e e-mail do seu usuário Jira.

---

## ▶️ Como usar a solução – passo a passo

### 0. Checklist obrigatório

Antes de qualquer coisa, verifique:

1. ✅ Python 3.x instalado  
2. ✅ Ambiente virtual `.venv` criado  
3. ✅ Ambiente virtual `.venv` ativado  
4. ✅ Dependências instaladas: `pip install -r requirements.txt`  
5. ✅ Arquivo `.env` criado e configurado corretamente  
6. ✅ Arquivo YAML preenchido (ou uso do modo simples na UI)

Se **qualquer** desses passos não for feito, a aplicação pode:

- nem iniciar; ou
- falhar ao falar com o Jira (erros 400/401/403); ou
- interromper com erros de módulo não encontrado.

---

### 1. Executar a UI (recomendado) – Windows via `run_ui.bat`

1. Garanta que `.venv` existe e tem as dependências instaladas.
2. No Windows, dentro de `apps\cadastro-jira`, execute:

   ```bat
   run_ui.bat
   ```

   ou dê **duplo clique** no arquivo `run_ui.bat`.

3. O script faz automaticamente:
   - entra no diretório do projeto
   - ativa `.venv`
   - executa: `streamlit run src\ui\streamlit_app.py`

4. Acesse o app em:

   ```text
   http://localhost:8501
   ```

#### Sobre o `run_ui.bat` (ajustes possíveis)

O `.bat` assume que:

- o ambiente virtual está em `.venv`
- o script de ativação está em `.venv\Scripts\activate.bat`
- o comando `streamlit` está disponível **dentro** do `.venv`

Se no seu ambiente:

- você criou o venv com outro nome (`.venv_jira`, por exemplo), ajuste o caminho:

  ```bat
  call ".venv_jira\Scripts\activate.bat"
  ```

- o Python só é acessível via `py` e você for criar o venv manualmente:

  ```bat
  py -m venv .venv
  ```

  (Isso não muda o `.bat`, que apenas ativa o venv já existente.)

> 💡 Em Linux/macOS, o `.bat` não funciona. Veja a seguir uma alternativa de script `.sh`.

---

### 2. Executar a UI em Linux/macOS (sem `.bat`)

No terminal (com `.venv` ativado):

```bash
cd apps/cadastro-jira
streamlit run src/ui/streamlit_app.py
```

Se quiser um script simples, crie `run_ui.sh`:

```bash
#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "Ambiente .venv não encontrado. Crie com:"
  echo "  python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# Ativar venv
# shellcheck disable=SC1091
source .venv/bin/activate

streamlit run src/ui/streamlit_app.py
```

Dê permissão de execução:

```bash
chmod +x run_ui.sh
./run_ui.sh
```

---

### 3. Modo CLI (opcional, avançado)

Além da UI, você pode rodar pelo terminal:

```bash
cd apps/cadastro-jira
# Ativar venv antes!
# Windows: .\.venv\Scripts\activate
# Linux/WSL: source .venv/bin/activate

# Criar 1 história de teste
python -m src.main --mode single

# Criar 2 histórias de teste
python -m src.main --mode test-two

# Criar histórias em massa a partir de YAML
python -m src.main --mode bulk --input-file data/stories_example.yaml
```

---

## ✍️ Como escrever o YAML de histórias

### 1. Uma única história (lista com 1 item)

```yaml
- title: "[Usuário Sirius] - Criar usuário dedicado no notebook para o curso de Docker"
  description: >
    Criar um novo usuário no notebook exclusivo para a Sirius, usado nos cursos de Docker,
    separando o ambiente de estudos do ambiente pessoal.
  tasks:
    - Criar usuário dedicado no sistema operacional.
    - Configurar permissões mínimas (docker, git, editor).
    - Organizar diretórios padrão de projetos da Sirius.
    - Documentar o passo a passo para os alunos.
```

Também funciona como **dict único**:

```yaml
title: "[Usuário Sirius] - Criar usuário dedicado no notebook para o curso de Docker"
description: >
  Criar um novo usuário no notebook exclusivo para a Sirius.
tasks:
  - Criar usuário dedicado no sistema operacional.
  - Configurar permissões mínimas (docker, git, editor).
  - Organizar diretórios padrão de projetos da Sirius.
  - Documentar o passo a passo para os alunos.
```

---

### 2. Várias histórias, separadas com `;` (múltiplos blocos)

Você pode escrever vários blocos de YAML separados por linhas com apenas `;`:

```yaml
- title: "[Usuário Sirius] - Criar usuário dedicado..."
  description: >
    Criar um novo usuário no notebook exclusivo para a Sirius.
  tasks:
    - Criar usuário dedicado no sistema operacional.
    - Configurar permissões mínimas (docker, git, editor).

;
- title: "[Jornada Docker] - Estruturar curso com Dockerfiles e Composes manuais"
  description: >
    Definir e documentar a jornada didática em que os alunos criam Dockerfiles
    e docker-compose manualmente, para só depois evoluir para scripts automatizados.
  tasks:
    - Mapear módulos com Dockerfile/Compose.
    - Definir sequência didática.
    - Criar exemplos práticos focados no uso de CLI.

;
- title: "[Segurança] - Padronizar .env, .gitignore e .dockerignore"
  description: >
    Revisar e padronizar arquivos de configuração e ignore em todos os repositórios.
  tasks:
    - Mapear arquivos sensíveis (.env, chaves, logs).
    - Atualizar .gitignore e .dockerignore.
    - Validar que arquivos sensíveis não vão para o Git nem para imagens Docker.
```

O parser:

- quebra o texto pelos `;`
- faz `yaml.safe_load()` em cada bloco
- converte tudo em uma lista de `Story`.

---

### 3. `tasks` em linha única com `;` (opcional)

Opcionalmente, você pode escrever as tarefas como uma única string:

```yaml
- title: "[Usuário Sirius] - Criar usuário dedicado..."
  description: >
    Criar um novo usuário no notebook exclusivo para a Sirius.
  tasks: "Criar usuário dedicado; Configurar permissões mínimas; Documentar passo a passo"
```

O parser divide por `;` e cria uma lista de tasks.

---

## 📚 Logs e histórico – SQLite

A aplicação registra automaticamente:

### Tabela `issue_history`

Campos principais:

- `created_at` – data/hora em UTC (ISO8601)
- `source` – origem da criação:
  - `cli_single`
  - `cli_test_two`
  - `cli_bulk`
  - `ui_yaml`
  - `ui_single`
- `issue_key` – chave da issue no Jira (ex.: `DOCKER-123`)
- `title`
- `description`
- `n_tasks`
- `project_key`
- `issue_type`

### Tabela `app_log`

Campos principais:

- `created_at` – data/hora em UTC
- `level` – nível (`INFO`, `ERROR`, etc.)
- `context` – contexto do log (ex.: `ui_yaml_create`, `ui_yaml_parse`, `ui_single_create`)
- `message`
- `details` – detalhes do erro (stacktrace, mensagens, etc.)

O arquivo fica em: `data/app_logs.db`.

Você pode inspecionar com:

```bash
sqlite3 data/app_logs.db
```

ou ferramentas gráficas (DBeaver, SQLite Browser etc.).

> ⚠️ Se as histórias contiverem dados sensíveis (PII), este arquivo também passa a ser sensível.  
> Evite comitar ou compartilhar `app_logs.db` com dados reais.

---

## 🧠 Pontos críticos – o que pode quebrar a aplicação

Algumas causas comuns de erro:

- `.venv` não criado ou não ativado  
  → erros de `ModuleNotFoundError`.

- `pip install -r requirements.txt` não executado  
  → bibliotecas ausentes (`streamlit`, `yaml`, `requests`, `python-dotenv`, `pandas`…).

- `.env` inexistente ou mal configurado  
  → erros de autenticação no Jira (401) ou erros 400 (“project cannot be found”, “Issue type is invalid”).

- `JIRA_PROJECT_KEY` errado  
  → Jira responde 400/404 para criação de issues.

- `JIRA_ISSUE_TYPE` que não existe no projeto  
  → Jira responde 400 com mensagem “Issue type is invalid”.

- YAML mal formatado na aba “Modo YAML”  
  → erro de parsing (a aplicação mostra o erro na tela).

Quando algo não funcionar, revise:

1. Ambiente virtual `.venv` está ativo?  
2. Dependências foram instaladas (`pip install -r requirements.txt`)?  
3. `.env` está preenchido corretamente (base URL, e-mail, token, projeto e issue type)?  
4. O YAML está bem formatado e sem erros de indentação?

---

## ✅ Resumo e próximos passos

Este projeto é uma ferramenta prática para:

- **Automatizar** criação de histórias no Jira via YAML
- **Ensinar** boas práticas de:
  - Ambientes virtuais (`venv`)
  - Organização de projeto (`src/`, `use_cases/`, `ui/`, `loaders/`, `infra`)
  - Integração com APIs externas (Jira REST)
  - Persistência leve com SQLite para logs/histórico

Ele é ideal para:

- Uso interno da Sirius em trilhas/cursos de Engenharia de Software, DevOps e Gestão de Projetos
- Automação de backlogs recorrentes em times de dados, engenharia e governança

Possíveis evoluções futuras:

- Autenticação na UI (ex.: login interno)
- Aba para consulta dos logs/histórico (`issue_history`, `app_log`)
- Exposição de uma API (FastAPI) e integração com front-ends como Docusaurus/React
- Integração com outros sistemas além do Jira

---
