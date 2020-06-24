# Jeitto ( jeitto-backend-challenge-201901 )
Gostaria antes de tudo, agradecer pela oportunidade.

A aplicação está hospedada na plataforma Heroku, para ter acesso <a href="https://jeitto.herokuapp.com/" target="_blank">clique aqui</a>.

Para visualizar a documentação dos métodos da API <a href="https://documenter.getpostman.com/view/11794083/SzzobGC7" target="_blank">clique aqui</a>.

# Índice
1. [Estrutura](#estrutura)

<a id="estrutura"></a>
# Estrutura
```
jeitto
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── company.py
│   │   ├── log.py
│   │   ├── product.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── company.py
│   │   ├── database.py
│   │   ├── helper.py
│   │   ├── product.py
│   │   ├── recharge.py
│   │   └── user.py
│   ├── views
│   │   ├── __init__.py
│   │   ├── company.py
│   │   ├── database.py
│   │   ├── helper.py
│   │   ├── log.py
│   │   ├── product.py
│   │   └── user.py
│   └── templates
│       └── template.html
├── config.py
├── Procfile
├── README.md
├── requirements.txt
├── run_dev.py
└── run.py
```