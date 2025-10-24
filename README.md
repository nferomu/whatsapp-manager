# WhatsApp Manager

Um sistema completo de gerenciamento de instâncias do WhatsApp usando Evolution API, com interface web moderna e autenticação segura.

## 🚀 Funcionalidades

### ✨ Gerenciamento de Instâncias
- **Criação de Instâncias**: Crie novas instâncias do WhatsApp com diferentes integrações
- **Listagem Personalizada**: Visualize apenas suas instâncias (filtradas por usuário)
- **Status em Tempo Real**: Acompanhe o status de conexão das suas instâncias
- **QR Code**: Visualize e escaneie QR codes para conectar instâncias
- **Exclusão Segura**: Remova instâncias com confirmação e validação de propriedade

### 🔐 Autenticação e Segurança
- **Login Seguro**: Autenticação via Supabase Auth
- **Controle de Acesso**: Cada usuário vê apenas suas próprias instâncias
- **Validação de Propriedade**: Todas as operações verificam se a instância pertence ao usuário

### 🔄 Sincronização Automática
- **Atualização Automática**: Status das instâncias atualizado a cada 30 segundos
- **Sincronização Manual**: Botão para atualizar status sob demanda
- **Integração Evolution API**: Comunicação direta com a API do Evolution

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido para Python
- **Supabase**: Banco de dados PostgreSQL com autenticação integrada
- **Evolution API**: API para gerenciamento de instâncias WhatsApp
- **Python 3.13**: Linguagem de programação
- **HTTPX**: Cliente HTTP assíncrono para comunicação com APIs

### Frontend
- **Vue.js 3**: Framework JavaScript reativo
- **Tailwind CSS**: Framework CSS utilitário
- **Axios**: Cliente HTTP para comunicação com o backend
- **Vite**: Build tool moderno e rápido

## 📋 Pré-requisitos

- Python 3.13+
- Node.js 18+
- Conta no Supabase
- Evolution API configurada

## 🚀 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd whatsapp-manager
```

### 2. Configuração do Backend

```bash
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração do Frontend

```bash
cd frontend

# Instale as dependências
npm install
```

### 4. Configuração das Variáveis de Ambiente

#### Backend (`.env`)
```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_SERVICE_ROLE_KEY=sua_service_role_key
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_api_key_evolution
```

#### Frontend (`.env`)
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=sua_url_do_supabase
VITE_SUPABASE_ANON_KEY=sua_anon_key_do_supabase
```

### 5. Configuração do Banco de Dados

No Supabase, crie a tabela `instances`:

```sql
CREATE TABLE instances (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    integration VARCHAR(50) NOT NULL DEFAULT 'WHATSAPP-BAILEYS',
    instance_id VARCHAR(255) UNIQUE NOT NULL,
    instance_hash VARCHAR(255),
    qrcode TEXT,
    status VARCHAR(50) DEFAULT 'disconnected',
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para melhor performance
CREATE INDEX idx_instances_user_id ON instances(user_id);
CREATE INDEX idx_instances_instance_id ON instances(instance_id);
CREATE INDEX idx_instances_status ON instances(status);
```

## 🏃‍♂️ Executando o Projeto

### Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

O sistema estará disponível em:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## 📱 Como Usar

### 1. Login
- Acesse o frontend e faça login com suas credenciais do Supabase

### 2. Criar Instância
- Clique em "Criar Nova Instância"
- Preencha o nome, número do WhatsApp e escolha a integração
- A instância será criada no Evolution API e salva no Supabase

### 3. Conectar WhatsApp
- Clique no botão "QR" na instância criada
- Escaneie o QR Code com seu WhatsApp
- O status será atualizado automaticamente

### 4. Gerenciar Instâncias
- Visualize o status de todas suas instâncias
- Use o botão "Atualizar Status" para sincronizar manualmente
- Exclua instâncias que não precisar mais

## 🔧 API Endpoints

### Instâncias
- `POST /instances/create` - Criar nova instância
- `GET /instances` - Listar instâncias do usuário
- `GET /instances/status/{instance_key}` - Obter status de uma instância
- `POST /instances/refresh-status` - Atualizar status de todas as instâncias
- `DELETE /instances/{instance_key}` - Excluir instância

### Autenticação
- `POST /login/auth` - Autenticar usuário
- `POST /login/register` - Registrar novo usuário

## 🎨 Interface

A interface foi desenvolvida com foco na experiência do usuário:

- **Design Moderno**: Interface dark theme com Tailwind CSS
- **Responsiva**: Funciona perfeitamente em desktop e mobile
- **Intuitiva**: Navegação simples e clara
- **Feedback Visual**: Estados de loading, sucesso e erro bem definidos
- **Modais**: QR Code em modal dedicado para melhor visualização

## 🔒 Segurança

- **Autenticação JWT**: Tokens seguros para todas as requisições
- **Validação de Propriedade**: Usuários só podem gerenciar suas próprias instâncias
- **CORS Configurado**: Política de CORS restritiva
- **Validação de Dados**: Validação rigorosa de entrada com Pydantic

## 🐛 Solução de Problemas

### Erro de Conexão com Evolution API
- Verifique se a Evolution API está rodando
- Confirme as variáveis de ambiente `EVOLUTION_API_URL` e `EVOLUTION_API_KEY`

### Problemas de Autenticação
- Verifique se as chaves do Supabase estão corretas
- Confirme se o usuário está logado no frontend

### Instâncias não aparecem
- Verifique se o usuário está autenticado
- Confirme se as instâncias foram criadas com sucesso no Evolution API

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato através do email: [seu-email@exemplo.com]

---

**Desenvolvido com ❤️ para facilitar o gerenciamento de instâncias WhatsApp**