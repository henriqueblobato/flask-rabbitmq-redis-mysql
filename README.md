# flask-rabbitmq-redis-mysql

## Running the project

`docker-compose up`

## Endpoint POST /credit-request

- Example:
- `{"age":20, "value":100000}`
```
curl -s "localhost:8000/credit-request" -XPOST \
-d '{"age":20, "value":100000}' \
-H "Content-Type: application/json" | jq .
```

## Endpoint GET /credit-validation
`GET /credit-validation`
- Example:
```
curl -s "localhost:8000/credit-validation?ticket=6826e88b-dc6d-4c27-b480-eb529511357c" | jq .
```

## Architecture

![diagram](https://user-images.githubusercontent.com/18133417/125178614-2faf0580-e1bd-11eb-89ef-26606c9225fa.png)
- A arquitetura escolhida para estudo foi a de um sistema distribuído assíncrono, na qual usando o serviço de mensageria RabbitMQ comunica-se entre diferentes tasks de um mesmo sistema.
- Temos dois workers totalmente desacoplados e independentes entre si, um para cada tópico. Um dos workers é responsável pela regra de idades, e outro pelas verificações de quantidades monetárias

## Escalabilidade
- Separando-se em tópicos organizam-se as responsabilidades e desacoplamentos de cada routing-key
- As lambdas por sua vez tem a responsabilidade única de fazerem uma verificação da regra de negócio, nesse primeiro momento temos somente uma regra simples de um 'if-else', mas em um futuro poderemos ter integrações e cálculos de machine learning ou engenharia de dados, aumentando a complexidade, cada lambda é reponsável por sua própria regra de negócio
- O redis tem papel duplo entre performance e escalabilidade, que por sua vez acumulam-se resultados rápidos que podem ser armazenados em quandes quantidades

## Análise das interações
- Enviando uma request solicitando um pedido de crédito
<img width="891" alt="Screen Shot 2021-07-10 at 20 34 07" src="https://user-images.githubusercontent.com/18133417/125178845-d5af3f80-e1be-11eb-9204-0934d9ad6317.png">

- O pedido de crédito é recebido e quebrado em duas partes, idade e valor
- A task de 'age' é enviada para o tópico de 'age', no qual será processada por sua respectiva tarefa assíncrona, o mesmoa contece com a task 'value'
- Caso passem nas condições, seus valores são adicionados no banco de dados
<img width="902" alt="Screen Shot 2021-07-10 at 20 34 18" src="https://user-images.githubusercontent.com/18133417/125178855-e95aa600-e1be-11eb-9597-f1e5879be878.png">

## Resultados
<img width="689" alt="Screen Shot 2021-07-10 at 20 41 34" src="https://user-images.githubusercontent.com/18133417/125178888-3e96b780-e1bf-11eb-8dfe-40da0534ebd9.png">
- Se as duas condições forem aceitas o status de APPROVED será adicionado ao ticket, caso não seja, ele será NOT approved, como vemos no exemplo de age=17,value=500000
<img width="883" alt="Screen Shot 2021-07-10 at 20 44 19" src="https://user-images.githubusercontent.com/18133417/125178927-a6e59900-e1bf-11eb-93a2-8972bcbb494a.png">
- Novamente o servidor quebra a resposta e manda seus valores para seus respectivos tópicos que serão tratados pelos workers, nesse caso, um exemplo não autorizado, no qual um valor monetário acima da condição
<img width="1004" alt="Screen Shot 2021-07-10 at 20 56 16" src="https://user-images.githubusercontent.com/18133417/125179102-874f7000-e1c1-11eb-8db4-837048414732.png">
