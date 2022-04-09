# Modelo de script com CLI em Python

[![Integração Contínua](https://github.com/mateusoliveira43/python-cli-script-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/python-cli-script-template/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mateusoliveira43_python-cli-script-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mateusoliveira43_python-cli-script-template)
[![Importações: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Estilo de código: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![segurança: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

- [README file in English](../README.md)

Modelo para criar scripts com interfaces de linha de comando em Python, usando a biblioteca padrão do Python [argparse](https://docs.python.org/3/library/argparse.html).

Confira a [Wiki](https://github.com/mateusoliveira43/python-cli-script-template/wiki) do repositório para mais detalhes.

# Exemplo de uso

Na pasta script, o pacote Python `example` e o módulo Python `run_example` são exemplos de uso do modelo.

Para rodar o exemplo, execute
```
[python|python3] scripts/run_example.py
[python|python3] scripts/run_example.py -h
[python|python3] scripts/run_example.py --help
```
para mostrar a mensagem de ajuda do script de exemplo. Executar o script com o comando de Python 3 é opcional.

# Qualidade

Para rodar as métricas de qualidade do modelo, é necessário instalar seus requisitos de desenvolvimento. Para instalá-los, execute
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```
ou
```
poetry install --no-root
poetry shell
```

As métricas de qualidade do modelo são reproduzidas pelas etapas de integração contínua do projeto. Configurações das etapas de integração contínua descritas no arquivo `.github/workflows/ci.yml`.

## Testes

Para rodar os testes e relatório de cobertura, execute
```
pytest
```

Para ver o relatório html, confira `tests/coverage-results/htmlcov/index.html`.

Configurações dos testes e relatório de cobertura descritas no arquivo `pyproject.toml`.

## Linter

Para rodar o linter de código Python, execute
```
prospector .
```

Configurações do linter de Python descritas no arquivo `.prospector.yaml`.

## Formatadores de código

Para checar o formato das importações no código Python, execute
```
isort --check --diff .
```

Para formatar as importações no código Python, execute
```
isort .
```

Para checar o formato do código Python, execute
```
black --check --diff .
```

Para formatar o código Python, execute
```
black .
```

Configurações do isort e black descritas no arquivo `pyproject.toml`.

Para checar o formato de todos os arquivos do repositório, execute
```
ec -verbose
```

Configurações do formato dos arquivos descritas no arquivo `.editorconfig`.

## Varredura de vulnerabilidades de segurança

Para checar problemas de segurança comuns no código Python, execute
```
bandit --recursive scripts
```

Para checar vulnerabilidades de segurança conhecidas nas dependências Python, execute
```
safety check --file requirements/dev.txt --full-report
```

## Análise de código com SonarCloud

[SonarCloud](https://sonarcloud.io/) analisa o código fonte do repositório através das etapas de integração contínua.

# Docker

Para rodar um único comando do projeto no Docker, execute
```
docker/run.sh <COMMAND>
```
Por exemplo, `docker/run.sh .venv/bin/pytest` ou `docker/run.sh poetry run pytest`.

Para rodar múltiplos comandos do projeto no Docker, execute
```
docker/exec.sh
```
e execute os comandos na shell do container, por exemplo `source .venv/bin/activate` ou `poetry shell`.

Para sair da shell do container, execute `CTRL+D`.

Para remover os containers, imagens, volumes e redes do projeto, execute
```
docker/down.sh
```

# Pre-commit

Para configurar o pre-commit automaticamente ao clonar o repositório, execute
```
pip install pre-commit
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir --hook-type commit-msg ~/.git-template
```
Precisa ser instalado de forma global. Mais informações em https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories

Para configurar o pre-commit localmente, execute
```
pip install pre-commit
pre-commit install --hook-type commit-msg
```
com seu ambiente virtual ativo.

Para testá-lo, execute
```
pre-commit run --all-files
```

# Licença

Esse repositório é licenciado sob os termos da [Licença MIT](LICENSE).
