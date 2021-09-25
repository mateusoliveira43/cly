# Modelo de script Python

- [README file in English](README.md)

Modelo para criar scripts Python.

## Tarefas

- [ ] Opção para editar e traduzir as mensagens de erro também.
- [ ] Adicionar linter e medidas de qualidade ao código.

# Sobre o Modelo

Na pasta do projeto, execute
```
[python|python3] ./script_name
[python|python3] ./script_name -h
[python|python3] ./script_name --help
```
para mostrar a mensagem de ajuda do script.

Executar o script com o comando de Python 3 é opcional. Você pode executar o script com
```
./script_name/__main__.py
```

Se você não tem permissão para executá-lo no seu sistema Linux, execute
```
chmod +x script.py
```
para dar permissão de execução ao arquivo.

- Para trocar o **nome do script**, altere a linha 3 de `/script_name/config.py`.
- Para trocar o título de **modo de uso**, altere a linha 7 de `/script_name/config.py`.
- Para trocar a mensagem de **descrição**, altere a linha 8 de `/script_name/config.py`.
- Para trocar a mensagem de **epílogo**, altere a linha 9 de `/script_name/config.py`.
- Para trocar o título de **opções obrigatórias**, altere a linha 10 de `/script_name/config.py`.
- Para trocar o título de **opções**, altere a linha 11 de `/script_name/config.py`.
- Para trocar a mensagem de **ajuda**, altere a linha 12 de `/script_name/config.py`.

Siga os exemplos de **Required options**, **Options** e **Commands** para criar as opções obrigatórias, opções e comandos do script.

Para desabilitar mostrar a mensagem de **ajuda** quando executar o script sem argumentos, remova os argumentos da função na linha 126 de `/script_name/__main__.py`.

Comece a lógica do script na linha 127 de `/script_name/__main__.py`.

# Testes

Para rodar os testes do modelos, é necessário instalar as ferramentas de teste. Para instalá-las, execute
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Para rodar os testes, execute
```
pytest
```

# Licença

Esse repositório é licenciado sob os termos da [Licença MIT](LICENSE).
