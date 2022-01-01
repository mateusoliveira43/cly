# Modelo de script Python

- [README file in English](../README.md)

Modelo para criar scripts Python.

## Tarefas

- [ ] Opção para editar e traduzir as mensagens de erro também.
- [ ] Adicionar mais medidas de qualidade ao código e às etapas de integração contínua.
- [ ] Remover regra de docstring para arquivos de testes.
- [ ] Adicionar poetry ao modelo.

TODO atualizar README
# Sobre o Modelo

Na pasta do projeto, execute
```
[python|python3] ./scripts
[python|python3] ./scripts -h
[python|python3] ./scripts --help
```
para mostrar a mensagem de ajuda do script.

Executar o script com o comando de Python 3 é opcional. Você pode executar o script com
```
./scripts/__main__.py
```

Se você não tem permissão para executá-lo no seu sistema Linux, execute
```
chmod +x ./scripts/__main__.py
```
para dar permissão de execução ao arquivo.

- Para trocar o **nome do script**, altere a linha 11 de `/scripts/__main__.py`.
- Para trocar a mensagem de **descrição**, altere a linha 12 de `/scripts/__main__.py`.
- Para trocar o título de **modo de uso**, altere a linha 4 de `/scripts/config.py`.
- Para trocar a mensagem de **epílogo**, altere a linha 5 de `/scripts/config.py`.
- Para trocar o título de **opções obrigatórias**, altere a linha 6 de `/scripts/config.py`.
- Para trocar o título de **opções**, altere a linha 7 de `/scripts/config.py`.

Para desabilitar mostrar a mensagem de **ajuda** quando executar o script sem argumentos, remova o argumento `--help` da função na linha 163 de `/scripts/config.py`.

Comece a lógica do script na função `main` (linha 59) de `/scripts/__main__.py`.

# Qualidade

Para rodar as métricas de qualidade do modelo, é necessário instalar os requisitos. Para instalá-los, execute
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

As métricas de qualidade do modelo são reproduzidas pelas etapas de integração contínua do projeto. Configurações das etapas de integração contínua descritas no arquivo `.github/workflows/ci.yml`.

## Testes

Para rodar os testes e relatório de cobertura, execute
```
pytest
```

Para ver o relatório html, confira `tests/coverage-results/htmlcov/index.html`.

Configurações dos testes e relatório de cobertura descritas no arquivo `pytest.ini`.

## Linter

Para rodar o linter, execute
```
prospector .
```

Configurações do Linter descritas no arquivo `.prospector.yml`.

# Licença

Esse repositório é licenciado sob os termos da [Licença MIT](LICENSE).
