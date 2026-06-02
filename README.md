# TO DO List

---

## 🛠️ Tecnologias utilizadas 
 
* **Orquestração de Ambiente:** `Docker Compose` unificando infraestrutura, persistência e serviços em rede local isolada.
* **Frontend SPA:** `React (v19.2.6)`, `Vite (v8.0.12)`, `React Router (v7.16.0)`, `Tailwind CSS (v4.3.0)` e `ESLint (v10.3.0)`.
* **Backend & API:** `Flask (v3.1.0)`, `Flask-CORS (v3.0.10)` e `Flask-JWT-Extended (v4.7.1)`.
* **Banco de Dados:** `PostgreSQL (v16)` via imagem oficial Docker, mapeado com ORM `SQLAlchemy (v2.0.41)`.

---

## 🚀 Como executar o projeto 
1. ### 🛠️ Pré-requisitos
   
- No Windows / macOS:
Instale e abra o **Docker Desktop**
(https://docs.docker.com/get-started/get-docker/)

- No Linux:
Instale o **Docker Engine** e o **Docker Compose Plugin**
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
   
2. ### 🚀 Inicialização Unificada do Ecossistema 

Para colocar toda a aplicação em execução com a infraestrutura completa integrada, basta executar o comando abaixo na raiz do projeto:

```bash
docker compose up --build
```

---

## 📂 Arquitetura e Mapeamento de Ficheiros 

O ecossistema está distribuído de forma limpa entre as pastas de contexto do Backend (`back/`) e do Frontend (`front/`), centralizando a orquestração de infraestrutura na raiz do projeto através do Docker Compose:

```text
├── docker-compose.yml      # Manifesto de orquestração unificada de múltiplos containers
├── back/                   # Diretório do servidor de API (Flask)
│   ├── Dockerfile          # Imagem de produção do servidor (Python 3.12-slim na porta 5000)
│   ├── requirements.txt    # Lista de dependências (incluindo Flask-CORS e Pytest)
│   ├── .env                # Ficheiro local com segredos e strings de conexão do banco
│   └── app/
│       ├── run.py          # Ponto de entrada que inicializa o servidor na porta 5000
│       ├── __init__.py     # Configuração da App Factory, CORS global e registo de Blueprints (/api)
│       ├── config.py       # Mapeamento seguro das variáveis de ambiente (.env)
│       ├── extensions.py   # Instanciação global e partilhada do SQLAlchemy e do JWTManager
│       ├── models.py       # Modelos e mapeamento das tabelas relacionais ('users' e 'tasks') 
│       ├── pytest.ini      # Configuração do pythonpath de testes para o módulo 'app'
│       ├── tests/
│       │   └── test_api.py # Suite completa de testes automatizados de integração
│       └── routes/
│           ├── auth.py     # Rotas de autenticação, validação de credenciais e geração de tokens JWT
│           ├── users.py    # Rotas de gestão, cadastro, perfil e remoção de utilizadores
│           ├── tasks.py    # Rotas de CRUD completo, filtros e controle de estado das tarefas
│           └── web.py      # Rota base/padrão para verificação de integridade (Healthcheck)
└── front/                  # Diretório do cliente web (React/Vite)
    ├── index.html          # Ponto de ancoragem do DOM e injeção do script principal
    ├── vite.config.js      # Configuração de plugins compiladores (React + Tailwind v4)
    ├── eslint.config.js    # Definição de regras estáticas e boas práticas de código JavaScript/React
    ├── package.json        # Manifesto de dependências do ecossistema Node e scripts npm
    ├── package-lock.json   # Árvore de resolução exata e hashes de integridade dos pacotes
    ├── Dockerfile          # Imagem de isolamento do Frontend (Node 22 rodando em ambiente dev)
    ├── public/
    │   ├── favicon.svg     # Identidade visual / Ícone do separador do navegador
    │   └── icons.svg       # Sprite consolidado de assets vetoriais de interface     
    └── src/
        ├── main.jsx        # Inicializador do React e montagem do ciclo virtual
        ├── App.jsx         # Orquestrador central de caminhos e rotas (React Router 7)
        ├── index.css       # Compilação e diretivas de importação do Tailwind CSS v4
        ├── App.css         # Customização de variáveis visuais, temas e responsividade
        ├── assets/
        │   ├── hero.png    # Imagem de demonstração / Banner principal do ecossistema (README)
        │   ├── react.svg   # Logótipo do ecossistema React
        │   └── vite.svg    # Logótipo do ecossistema Vite
        └── modules/
            ├── auth/
            │   └── pages/
            │       └── LoginPage.jsx    # Ecrã de Autenticação assíncrono (Login/Registro)
            └── todos/
                ├── components/
                │   └── TodoItem.jsx     # Card atómico de tarefa (Edição inline, colapso e toggle)
                └── pages/
                    └── TodoListPage.jsx # Painel To-Do (CRUD completo, pesquisa e filtros)
```

---

## ⚙️ Orquestração Multi-Container com Docker Compose

O arquivo central **`docker-compose.yml`** permite subir toda a infraestrutura da aplicação (Banco de Dados, API e Frontend) com um único comando, gerenciando dependências de inicialização, healthchecks e volumes persistentes.

### 🐳 Serviços Mapeados

1. **`db` (Banco de Dados PostgreSQL v16):**
   * **Persistência:** Utiliza um volume nomeado (`postgres_data`) acoplado ao diretório interno `/var/lib/postgresql/data` para garantir que as tarefas e usuários não sejam perdidos ao reiniciar o container.
   * **Mecanismo de Healthcheck:** Implementa uma verificação ativa utilizando o utilitário `pg_isready -U postgres` a cada 5 segundos. Isso garante que os serviços dependentes só iniciem quando o banco estiver totalmente pronto para receber conexões.
   * **Porta:** Exposta localmente em `5432:5432`.

2. **`flask-app` (Servidor de API Backend):**
   * **Construção:** Compila a imagem a partir do contexto do diretório `./back`.
   * **Resolução de Dependências:** Possui a diretiva `condition: service_healthy` atrelada ao serviço `db`, evitando falhas de conexão de banco durante o bootstrap.
   * **Injeção de Credenciais:** Carrega as chaves criptográficas e strings de conexão diretamente do arquivo de ambiente local `./back/.env`.
   * **Porta:** Exposta localmente em `5000:5000`.

3. **`frontend` (Interface de Usuário React/Vite):**
   * **Construção:** Compila a imagem a partir do contexto do diretório `./front`.
   * **Sincronização Reativa (Hot-Reloading):** Mapeia o volume local `./front:/app` para refletir alterações de código em tempo real no navegador sem necessidade de rebuilding da imagem, preservando a pasta isolada `/app/node_modules`.
   * **Ordem de Inicialização:** Depende diretamente do container `flask-app`.
   * **Porta:** Exposta localmente em `5173:5173`.

---

## 🌐 Documentação Detalhada da API

> ⚠️ **Nota de Prefixos:** As rotas internas de recursos exigem o prefixo genérico `/api` para todas as chamadas estruturais.

### 🏠 Endpoints Públicos Base

| Método | Endpoint | Payload (JSON) | Comportamento / Resposta bem-sucedida |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | *Nenhum* | Retorna a string `"API funcionando!"` (Healthcheck). |
| `POST` | `/api/users` | `{"nome", "email", "password"}` | Cria um utilizador e devolve `{"id", "message"}` (Status 201). |
| `POST` | `/api/login` | `{"email", "password"}` | Valida credenciais e retorna o `access_token` (Status 200). |

<details>
<summary>🔑 Ver Endpoints Privados de Utilizador (Requer Header: Authorization: Bearer )</summary>

| Método | Endpoint | Payload (JSON) | Descrição do Fluxo |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/users/me` | *Nenhum* | Obtém o perfil atual filtrado com as chaves: `id`, `nome` e `email`. |
| `DELETE` | `/api/users/me` | *Nenhum* | Remove permanentemente o perfil do utilizador autenticado do banco. |
| `POST` | `/api/tasks/me` | `{"title", "description"}` | Cria uma tarefa atribuída automaticamente ao utilizador logado. |
| `GET` | `/api/tasks/me` | *Query string opcional* `?status=` | Lista todas as tarefas do utilizador (permite filtrar por `pendente` ou `concluido`). |
| `PUT` | `/api/tasks/me/<id>` | `{"title", "description"}` | Modifica por completo os dados estruturais de uma tarefa existente. |
| `PATCH` | `/api/tasks/me/<id>/status` | `{"status": "concluido"}` | Atualiza pontualmente o estado de uma meta ativa (apenas suporta `"concluido"`). |
| `DELETE` | `/api/tasks/me/<id>` | *Nenhum* | Elimina uma tarefa associada à conta do utilizador corrente. |

</details>

<details>
<summary>🛡️ Ver Endpoints Administrativos (Uso de Gestão Global/Admin)</summary>

| Método | Endpoint | Payload (JSON) | Descrição do Fluxo |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/users/admin/<int:user_id>` | *Nenhum* | Obtém os dados estruturais completos de qualquer utilizador através do ID fornecido, incluindo o hash da `password` (Status 200). |
| `DELETE` | `/api/users/admin/<int:user_id>` | *Nenhum* | Remove e elimina permanentemente a conta de qualquer utilizador do banco de dados através do ID fornecido (Status 200). |
| `POST` | `/api/tasks/admin/<int:id_user>` | `{"title", "description"}` | Permite a um administrador criar uma tarefa diretamente para um utilizador específico pelo ID (Status 201). |
| `GET` | `/api/tasks/admin/<int:user_id>` | *Query string opcional* `?status=` | Lista todas as tarefas de um utilizador específico do sistema, com filtros opcionais (Status 200). |
| `PUT` | `/api/tasks/admin/<int:user_id>/<int:task_id>` | `{"title", "description"}` | Modifica completamente os dados estruturais de uma tarefa de um utilizador específico (Status 200). |
| `PATCH` | `/api/tasks/admin/<int:user_id>/<int:task_id>/status` | `{"status": "concluido"}` | Permite a um administrador alterar forçadamente o estado de uma tarefa específica pertencente a um utilizador específico (Status 200). |
| `DELETE` | `/api/tasks/admin/<int:user_id>/<int:task_id>` | *Nenhum* | Remove e elimina permanentemente uma tarefa específica de um utilizador do banco de dados (Status 200). |

</details>

---

## 💻 Fluxo e Configuração do Frontend

### 🕸️ 1. Ciclo de Inicialização e Injeção no DOM (`index.html` e `main.jsx`)
O ciclo de vida da interface SPA inicia-se no ficheiro estático `index.html`:
* **Ponto de Ancoragem:** Contém a tag estrutural `<div id="root"></div>`, elemento para onde o algoritmo do React converge a árvore de componentes.
* **Carregamento Modular:** Dispara a tag nativa `<script type="module" src="/src/main.jsx"></script>` para dar início à execução assíncrona do JavaScript compatível com o navegador.

O ficheiro `main.jsx` consome esta referência, acionando o método `createRoot(document.getElementById('root'))` para instanciar a aplicação dentro do `<StrictMode>`, assegurando a identificação antecipada de bugs em fase de desenvolvimento.

### 🧭 2. Orquestração e Roteamento Virtual (`App.jsx`)
O componente central mapeia de forma declarativa e limpa os fluxos de permissão e visualização de caminhos da aplicação:
* **`<BrowserRouter>`**: Monitoriza a barra de navegação capturando eventos de modificação da URL.
* **`<Routes>` e `<Route>`**: Realizam a comutação rápida sem requisições adicionais à rede. O caminho `/` expõe o ecrã de autenticação (`LoginPage.jsx`), enquanto a rota protegida `/todos` direciona o utilizador logado para o painel de controlo principal (`TodoListPage.jsx`).

### 📦 3. Ferramentas de Build e Compilação (`vite.config.js` e `package.json`)
O empacotamento do código adota a nova especificação do **Vite 8** e do **Tailwind CSS v4**:
* **Integração do Compilador (`vite.config.js`):** O pipeline de transformação do código foi simplificado drasticamente com a inclusão unificada dos plugins nativos:
    ```javascript
    import { defineConfig } from 'vite'
    import react from '@vitejs/plugin-react'
    import tailwindcss from '@tailwindcss/vite'

    export default defineConfig({
      plugins: [react(), tailwindcss()],
    })
    ```
* **Automação de Scripts (`package.json`):** Centraliza os gatilhos industriais do projeto, mapeando comandos como `npm run dev` (servidor local), `npm run build` (compilação estática otimizada para a pasta `dist/`) e `npm run lint` (validação com regras do `eslint.config.js`).

---

## 🧪 Testes de Integração Automatizados

O sistema conta com um ciclo de testes de integração ponta a ponta estruturado no ficheiro `test_api.py` sob as diretivas do arquivo `pytest.ini`.

### 🔄 Fluxo de Execução da Suite de Testes
1. **Criação de Utilizador (`test_criar_usuario`)** $
ightarrow$ Status 201.
2. **Autenticação (`test_login`)** $
ightarrow$ Captura o Bearer Token.
3. **Criação de Duas Tarefas (`test_criar_task_1` e `test_criar_task_2`)**.
4. **Listagem e Filtros (`test_listar_tasks_pendentes`)** com query parameters.
5. **Atualização Parcial e Total (`test_atualizar_task_1` e `test_concluir_task_2`)** via `PUT` e `PATCH`.
6. **Limpeza Estrutural (`test_deletar_task_1`, `test_deletar_task_2`, `test_deletar_usuario`)**.

---

## 🛡️ Regras de Validação e Integridade

1.  **Sanitização de Identity (`users.py`):** Bloqueia nomes com dígitos e exige passwords com no mínimo 8 caracteres.
2.  **Limitação de Texto (`tasks.py`):** Título limitado a 100 caracteres e descrição a 300 caracteres.
3.  **Restrição Única por Utilizador (`models.py`):** Enforça a constraint `UniqueConstraint("id_user", "title")` na base de dados, garantindo que o mesmo utilizador não possua títulos duplicados em sua grade de tarefas.
