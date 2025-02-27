> create prod branch: prod
> create dev branch: dev
> do change on dev, push it  and raise PR against prod
> merge PR if no conflicts, and changes will be available on prod branch
> connect to EC2 server, pull prod changes: git pull origin prod
> run migrations, collectstatics and restart gunicorn and nginx
    - sudo systemctl restart gunicorn nginx
