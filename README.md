# Grande Floresta

Portal colaborativo em Django para organizar projetos audiovisuais, com cadastro, categorias e anexos de mídia em posts e comentários.

## Requisitos locais

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Deploy no Render

O repositório já contém `render.yaml`, `Procfile` e `requirements.txt`, então o Render consegue provisionar tudo automaticamente.

1. Faça login em [render.com](https://render.com) e conecte o repositório do GitHub.
2. Ao importar o repo, o Render detectará o `render.yaml` (com `rootDir: .`, garantindo que o serviço execute a partir de `/opt/render/project/src`) e criará:
   - Um banco Postgres gratuito (`grande-floresta-db`).
   - Um serviço web Python com build `pip install -r requirements.txt && python manage.py collectstatic --noinput` e start `gunicorn grande_floresta.wsgi:application`.
   - Um disco persistente de 1 GB montado em `/opt/render/project/src/media` para armazenar uploads.
3. Aplique as variáveis já declaradas no `render.yaml` (o Render gera `DJANGO_SECRET_KEY` automaticamente). Ajuste `DJANGO_ALLOWED_HOSTS` se renomear o serviço.
4. O `postDeployCommand` executa `python manage.py migrate` após cada deploy. Se precisar popular dados (categorias, superusuário), use o botão **Shell** no dashboard.
5. A primeira subida leva alguns minutos. Quando terminar, acesse `https://<nome-do-servico>.onrender.com`. Se precisar forçar um novo deploy após alterar o repo, clique em **Manual Deploy → Deploy latest commit** no dashboard do serviço.

### Variáveis importantes

| Variável | Função |
| --- | --- |
| `DJANGO_SECRET_KEY` | Assinatura criptográfica — gerada pelo Render. |
| `DJANGO_DEBUG` | Mantido como `False` em produção. |
| `DJANGO_ALLOWED_HOSTS` | Host permitido (ex.: `grande-floresta-app.onrender.com`). |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Inclui `https://<host>` para liberar o painel admin/forms. |
| `DATABASE_URL` | String automática apontando para o Postgres provisionado. |

### Dicas pós-deploy

- Rode `python manage.py createsuperuser` via shell para acessar `/admin`.
- Arquivos estáticos são servidos pelo WhiteNoise após `collectstatic`.
- Uploads ficam no disco persistente; monitore o uso pelo dashboard do Render.
