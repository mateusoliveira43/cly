# CLY?! Construa CLIs sem dependências!

[![Integração Contínua](https://github.com/mateusoliveira43/cly/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/cly/actions)
[![Entrega Contínua](https://github.com/mateusoliveira43/cly/actions/workflows/cd.yml/badge.svg)](https://github.com/mateusoliveira43/cly/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mateusoliveira43_python-cli-script-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mateusoliveira43_python-cli-script-template)
[![Importações: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Estilo de código: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![segurança: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

- [README file in English](../README.md)

Um framework para criar interfaces de linha de comando em Python, usando apenas bibliotecas padrão do Python, como a [argparse](https://docs.python.org/3/library/argparse.html).

Confira a documentação do projeto [aqui](https://mateusoliveira43.github.io/cly/).

## Requirements

Para usar (ou contribuir com) o framework, são necessárias as seguintes ferramentas:

- [Python](https://wiki.python.org/moin/BeginnersGuide/Download) 3.7 ou maior

## Desenvolvimento

Escolha uma das seguintes seções para configurar seu ambiente de desenvolvimento.

### Python

Para criar um ambiente virtual, execute
```
virtualenv .venv
```

Para ativar o ambiente virtual, execute
```
source .venv/bin/activate
```

Para instalar as dependências de desenvolvimento do framework no ambiente virtual, execute
```
pip install -r requirements/dev.txt
```
Para desativar o ambiente virtual, execute `deactivate`.

Execute os comandos das seções seguintes com o ambiente virtual ativo.

### Poetry

Para instalar as dependências de desenvolvimento do framework em um ambiente virtual, execute
```
poetry install
```

Para ativar o ambiente virtual, execute
```
poetry shell
```
Para desativar o ambiente virtual, execute `CTRL+D` ou `exit`.

Para atualizar o arquivo de dependências, execute
```
poetry export --format requirements.txt --output requirements/dev.txt --dev
```

Execute os comandos das seções seguintes com o ambiente virtual ativo.

### Docker

Para se conectar na shell do container Docker do projeto, execute
```
docker/run.sh
```
Para sair da shell do container, execute `CTRL+D` ou `exit`.

Para rodar o linter de arquivos Dockerfile, execute
```
docker/lint.sh
```

Para rodar a varredura de vulnerabilidades de segurança na imagem Docker, execute
```
docker/scan.sh
```
É necessário ter uma conta no [Docker Hub](https://hub.docker.com/).

Para remover os containers, imagens, volumes e redes do projeto, execute
```
docker/down.sh
```

Para mudar a configuração do Docker, altere as variáveis no arquivo `.env`.

Execute os comandos das seções seguintes na shell do container.

## Qualidade

As métricas de qualidade do framework são reproduzidas pelas etapas de integração contínua do projeto. Configurações das etapas de integração contínua descritas no arquivo `.github/workflows/ci.yml`.

### Testes

Para rodar os testes e relatório de cobertura, execute
```
pytest
```

Para ver o relatório html, confira `tests/coverage-results/htmlcov/index.html`.

Configurações dos testes e relatório de cobertura descritas no arquivo `pyproject.toml`.

### Checagem de tipo

Para rodar o checador de tipo do Python, execute
```
mypy .
```

Configurações do checador de tipo do Python descritas no arquivo `pyproject.toml`.

### Linter

Para rodar o linter de código Python, execute
```
prospector
prospector --profile tests/.prospector.yaml tests
```

Configurações do linter de Python descritas nos arquivos `.prospector.yaml` e `tests/.prospector.yaml`.

### Formatadores de código

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

### Varredura de vulnerabilidades de segurança

Para checar problemas de segurança comuns no código Python, execute
```
bandit --recursive cly
```

Para checar vulnerabilidades de segurança conhecidas nas dependências Python, execute
```
safety check --file requirements/dev.txt --full-report
```

### Documentação

Para verificar a geração de documentação do código Python, execute
```
sphinx-apidoc --module-first --private --output-dir docs/modules cly
sphinx-build -W -T -v -n -a docs public
```

Para gerar a documentação do código Python, execute
```
sphinx-apidoc --module-first --private --output-dir docs/modules cly
sphinx-build -v -n -a docs public
```
Para ver a documentação, confira `public/index.html`.

Configuração do Sphinx no arquivo [`docs/conf.py`](docs/conf.py).

A documentação é atualizada automaticamente pelas etapas de entrega contínua (CD) do projeto. Configuração das etapas de entrega contínua no arquivo [`.github/workflows/cd.yml`](.github/workflows/cd.yml).

### Análise de código com SonarCloud

[SonarCloud](https://sonarcloud.io/) analisa o código fonte do repositório através das etapas de integração contínua.

## Pre-commit

Para configurar o pre-commit automaticamente ao clonar o repositório, execute
```
pip install pre-commit
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir --hook-type commit-msg --hook-type pre-commit ~/.git-template
```
Precisa ser instalado de forma global. Mais informações [aqui](https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories).

Para configurar o pre-commit localmente, execute
```
pip install pre-commit
pre-commit install --hook-type commit-msg --hook-type pre-commit
```
com seu ambiente virtual ativo.

Para testá-lo, execute
```
pre-commit run --all-files
```

## Licença

Esse repositório é licenciado sob os termos da [Licença MIT](LICENSE).
