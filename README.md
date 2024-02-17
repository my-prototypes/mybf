# MY_BF_Image

My Basic Flask

Exemplo de Protótipo de Aplicação Web (Prova de Conceito) de CRUD de usuários e imagens

# A. Ambiente de Desenvolvimento

Existe uma estrutura base que vamos seguir para a construção de nossas aplicações em [Flask](https://flask.palletsprojects.com/en/2.3.x/): 

## 1. Virtual Environment

Vamos usar o esquema de [virtual environment](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv venv
```

Mais detalhes em [python venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

### 1.1 Para ativar o venv (Linux e MacOS)

```bash
source venv/bin/activate
```

### 1.2 Para desativar o venv 

```bash
deactivate
```

## 2. Uma vez criado e ativado o venv precisamos instalar os módulos, pacotes e bibliotecas usadas pela aplicação

```bash
pip3 install -r requirements.txt
```

## 3. Para executar a aplicação principal

```bash
flask --app principal run --host=0.0.0.0 --port=5000
```

Abra o browser: http://localhost:5000


# B. Descrição da estrutura da aplicação 

Segue uma breve descrição dos diretórios e arquivos:

**app/**: O diretório principal da aplicação.

**app/tests/**: diretório contendo a implementação dos casos de testes da aplicação

**app/controllers/**: diretório que contém os controladores ou [blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/) da aplicação. Os arquivos authentication.py, usuarios.py e dashboard.py definem as rotas e a lógica associada a cada uma delas.

**app/static/**: diretório que contem os arquivos e recursos estáticos da aplicação

**app/templates/**: O diretório que contém os templates HTML usados para renderizar as páginas da sua aplicação. Os templates estão organizados em subdiretórios, como auth/,  usuarios/ e dashboard/ correspondendo aos controladores aos quais eles pertencem.

**app/models.py**: O arquivo que contém as definições das classes de modelo da sua aplicação. A classe Usuario está definida neste arquivo.

**app/utils**: Corresponde ao pacote de utilidades da aplicação.

**app/dao.py**: Padrão Data Access Object (DAO) pattern, que é bom para separar interações de banco de dados de outras lógicas.

**app/extensions.py**: Inicialização do banco de dados e configurações do Login Manager.

**app/forms.py**: Classe para facilitar a manipulação de forms html e validação de dados.

**app/models.py**: Representa as classes de modelo da aplicação.

**app/instance/users.db**: O arquivo de banco de dados [SQLite](https://www.sqlite.org/docs.html) onde os dados dos usuários e as informações de imagens são armazenadas.

**principal.py**: O ponto de entrada da aplicação Flask, onde você cria a instância do aplicativo e registra os blueprints.

**exec.sh**: Script bash para executar a aplicação

**requirements.txt**: Um arquivo que lista as dependências do projeto.

**README.md**: Um arquivo de documentação contendo informações sobre o projeto.


