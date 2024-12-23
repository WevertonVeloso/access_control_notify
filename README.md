# access_control_notify
# README

## Descrição do Projeto
Este projeto é um script Python desenvolvido para:

1. Alertar os pais quando seus filhos entram e saem da escola, com base no acesso liberado pelo controlador de acesso.
2. Obter o ID do último acesso liberado por um controlador de acesso Intelbras.
3. Verificar se esse ID é diferente do último processado, evitando duplicatas.
4. Consultar um banco de dados MySQL para obter informações do usuário associado ao ID.
5. Enviar os dados do usuário para uma API AWS em formato JSON.
6. Repetir o processo em intervalos definidos.

## Funcionalidades
- Consulta ao controlador de acesso via requisição HTTP GET com autenticação Digest.
- Manipulação de arquivos para armazenar o último ID processado.
- Conexão segura com o banco de dados MySQL para consultas de usuários.
- Envio de dados para um endpoint AWS em formato JSON.
- Execução em loop infinito com intervalos configuráveis.

## Requisitos

### Dependências
Certifique-se de instalar as seguintes bibliotecas antes de executar o script e de ter o MySQL instalado:

```bash
pip install requests mysql-connector-python
```

### Configurações de Ambiente
Defina as seguintes variáveis de ambiente para configurar o script:

- **URL_CONTROLADOR**: URL do controlador de acesso Intelbras.
- **USER_API**: Nome de usuário para autenticação no controlador.
- **PASSWD_API**: Senha para autenticação no controlador.
- **HOST_DB**: Endereço do host do banco de dados MySQL.
- **USER_DB**: Nome de usuário para conexão ao banco de dados.
- **PASSWD_DB**: Senha para conexão ao banco de dados.
- **DATABASE**: Nome do banco de dados.
- **URL_AWS**: URL do endpoint AWS para envio dos dados.

Exemplo de configuração em um arquivo `.env`:
```env
URL_CONTROLADOR=http://192.168.1.123:80/cgi-bin/recordFinder.cgi
USER_API=admin
PASSWD_API=admin12345
HOST_DB=localhost
USER_DB=ever
PASSWD_DB=1234
DATABASE=cadastro
URL_AWS=https://api-gateway-url
```

## Como Usar

1. **Configure as variáveis de ambiente:** Certifique-se de que todas as variáveis necessárias estão definidas corretamente.

2. **Execute o script:**
   ```bash
   python access_alert.py
   ```

3. O script irá executar em loop infinito, consultando o controlador de acesso, verificando o banco de dados e enviando os dados para a AWS.

## Estrutura do Código

### Funções Principais

#### `get_id(url, params, user_api, passwd_api)`
Realiza uma requisição HTTP GET ao controlador de acesso para obter o último ID registrado.

#### `get_last_id()`
Lê o último ID processado a partir do arquivo `idprevio`.

#### `get_user_db(get_id, get_last_id)`
Consulta o banco de dados MySQL para obter informações do usuário com base no ID obtido.

#### `send_data(user_db, url_aws)`
Envia os dados do usuário para a API AWS em formato JSON.

### Estrutura do Loop Principal
1. Calcula o intervalo de tempo para consulta.
2. Obtém o ID do controlador de acesso.
3. Verifica se o ID é novo.
4. Consulta o banco de dados.
5. Envia os dados para a AWS.
6. Aguarda 3 segundos antes de repetir o processo.

## Licença
Este projeto está licenciado sob a [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.html).

