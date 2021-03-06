# Jeitto ( jeitto-backend-challenge-201901 )

Gostaria antes de tudo, mencionar que eu não tinha experiências com o Python e a construção dessa API foi sem sombra de dúvidas muito proveitosa no sentido de aprendizado, pois praticamente a maioria das soluções que acabei por utilizar, eu nunca tinha utilizado antes.

A aplicação está hospedada na plataforma Heroku, para ter acesso <a href="https://jeitto.herokuapp.com/" target="_blank">clique aqui</a>.

O banco de dados Mysql está hospedado na plataforma Clever Cloud.

Para visualizar a documentação dos métodos da API <a href="https://documenter.getpostman.com/view/11794083/SzzobGC7" target="_blank">clique aqui</a>.

Obrigado pela oportunidade.



# Índice
1. [Perguntas](#perguntas)
2. [Pré Requisitos](#prerequisitos)
3. [Como Utilizar](#comoutilizar)
4. [Estrutura](#estrutura)



<a id="perguntas"></a>
# Perguntas

### Quais foram os principais desafios durante o desenvolvimento?
- Acreito que o maior desafio foi me acostumar com uma __linguagem nova__ e ao mesmo tempo criar um software __conciso e seguro__, sendo fácil de ser compreendido e utilizado.

### O que você escolheu como arquitetura/framework/banco e por que?
- Framework: utilizei o __Flask__, foi minha escolha pois é um framework muito simples de ser utilizado, por ter muito conteúdo sobre o mesmo em sites de ensino e por ser um microframework, que não traz consigo ferramentas que não seriam utilizadas para a construção de uma API, facilitando assim o desenvolvimento e melhorando também a legibilidade do software.

- Arquitetura: utilizei o padrão de rotas, views, models e templates. Nas minhas pesquisas sobre projetos em flask, me familiarizei bastante com o estilo de pastas utilizado pelo exemplo e resolvi aplicar o mesmo.

- Banco: utilizei o __Mysql__, foi escolhido pois me senti bastante familiarizado com o __SQLAlchemy__, facilitando assim o progresso com o desenvolvimento.

### O que falta desenvolver / como poderiamos melhorar o que você entregou?
- Gostaria de ter me aprofundado mais nas relações entre usuários, companhias e produtos.
- Acredito que uma grande melhoria seria criar um front consumindo essa API

### Python é a melhor escolha para esta atividade? Por que?
- Dentre as linguagens que eu conheço, sim.
- O python possui uma __legibilidade__ fora do comum, chega a ser algo intuitivo programar utilizando o mesmo, acarretando assim em uma linguagem com uma manutenção mais ágil e uma excelente escalabilidade

<a id="prerequisitos"></a>
# Pré Requisitos

- Docker
- Mysql (Deve possuir uma database que será utilizada pela aplicação)



<a id="comoutilizar"></a>
# Como Utilizar

- Clonar este repositório

    ```
    git clone https://github.com/DanielAkio/jeitto-backend-challenge-201901.git
    ```

- Entrar no repositório

    ```
    cd jeitto-backend-challenge-201901
    ```

- Criar um arquivo .env, com as variáveis de ambiente MYSQL_URI e SECRET_KEY

    ```
    touch .env & echo MYSQL_URI="sua_mysql_uri" > .env & echo SECRET_KEY="sua_secret_key" >> .env
    ```

- Utilizar o comando bash

    ```
    bash start.sh
    ```



<a id="estrutura"></a>
# Estrutura

    jeitto
    ├── app
    │   ├── __init__.py
    │   ├── models
    │   ├── routes
    │   ├── templates
    │   ├── test
    │   └── views
    ├── config.py
    ├── Dockerfile
    ├── Procfile
    ├── README.md
    ├── requirements.txt
    ├── run_dev.py
    ├── run.py
    └── start.sh

- __app__:
    - __init__: local onde são declarados todos os módulos a serem utilizados pela applicação.
    - __models__: local onde são definidos os medelos de tabelas e suas relações com a orm.
    - __routes__: local onde são definidas as rotas e as mesmas realizam as chamadas para as views.
    - __templates__: local onde são encontrados os templates html utilizados pela aplicação
    - __test__: local onde são definidos os teste unitários
    - __views__: local onde são definidas todas as lógicas e procedimentos a serem feitos

- __fora do app__: são encontradas as configurações das plataformas utilizadas, do sqlalchemy, dos modos de execução da aplicação e os requisitos do projeto