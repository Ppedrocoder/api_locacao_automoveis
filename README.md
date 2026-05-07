# Sistema de Locação de Veículos

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
