# Sistema de Locação de Veículos

## Tecnologias

### Backend:

- Django Ninja

- FastAPI
### Frontend

- React

## Ambiente Python

1 - Criar ambiente

```bash
python -m venv {nome-do-ambiente}
```
2 - Rodar ambiente

```bash
.\{nome-do-ambiente}\Scripts\activate
```
## Instalar Dependências

1 - No ambiente python

```bash
pip install -r requirements.txt
```

2 - No frontend

```bash
npm install
```

## Colocar em Funcionamento

1 - Rodar api veículos

```bash
python manage.py runserver 8001
```

2 - Rodar api locação

```bash
python manage.py runserver 8002
```

3 - Rodar api gateway

```bash
uvicorn gateway:app --port 8000 --reload 
```

4 - Rodar frontend

```bash
npm start
```

---

> Criado por [Pedro Ricardo](https://github.com/Ppedrocoder) e [Eduardo Medeiros](https://github.com/DuduPOG)
