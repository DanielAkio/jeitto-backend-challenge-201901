# Jeitto ( jeitto-backend-challenge-201901 )
Gostaria antes de tudo, agradecer pela oportunidade.

A aplicação está hospedada na plataforma Heroku, para ter acesso <a href="https://jeitto.herokuapp.com/" target="_blank">clique aqui</a>.

Para visualizar a documentação dos métodos da API <a href="https://documenter.getpostman.com/view/11794083/SzzobGC7" target="_blank">clique aqui</a>.

# Índice
1. [Perguntas](#perguntas)
2. [Como Utilizar](#como_utilizar)
3. [Estrutura](#estrutura)

<a id="perguntas"></a>

# Perguntas

## Quais foram os principais desafios durante o desenvolvimento?
- Acreito que o maior desafio foi me acostumar com uma __linguagem nova__ e ao mesmo tempo criar um software __conciso e seguro__, sendo fácil de ser compreendido e utilizado

## O que você escolheu como arquitetura/framework/banco e por que?
- Framework: utilizei o __Flask__, foi minha escolha pois é um framework muito simples de ser utilizado e por ter muito conteúdo sobre o mesmo em sites de ensino, facilitando assim o desenvolvimento e melhorando também a legibilidade do software.

- Arquitetura: utilizei o padrão de rotas, views, models e templates. Nas minhas pesquisas sobre projetos em flask, me familiarizei bastante com o estilo de pastas utilizado pelo exemplo e resolvi aplicar o mesmo.

- Banco: utilizei o __Mysql__, foi escolhido pois me senti bastante familiarizado com o __SQLAlchemy__, facilitando assim o progresso com o desenvolvimento.

## O que falta desenvolver / como poderiamos melhorar o que você entregou?
- Gostaria de ter me aprofundado mais nas relações entre usuários, companhias e produtos.
- Acredito que uma grande melhoria seria criar um front consumindo essa API

## Python é a melhor escolha para esta atividade? Por que?
- Dentre as linguagens que eu conheço, sim. 
- O python possui uma __legibilidade__ fora do comum, chega a ser algo intuitivo programar utilizando o mesmo, acarretando assim em uma linguagem com uma manutenção mais ágil e uma excelente escalabilidade

<a id="como_utilizar"></a>

# Como Utilizar

- clonar o repositório
- pip install -r requirements.txt


<a id="estrutura"></a>

# Estrutura
```
jeitto
├── app
│   ├── routes
│   ├── views
│   ├── models
│   ├── templates
│   └── test
├── config.py
├── Procfile
├── README.md
├── requirements.txt
├── run_dev.py
└── run.py
```