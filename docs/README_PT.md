# Modelo de script com CLI em Python

[![Integração Contínua](https://github.com/mateusoliveira43/python-cli-script-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/python-cli-script-template/actions)
[![Importações: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![segurança: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=mateusoliveira43_python-cli-script-template)](https://sonarcloud.io/summary/new_code?id=mateusoliveira43_python-cli-script-template)

- [README file in English](../README.md)

Modelo para criar scripts com interfaces de linha de comando em Python, usando a biblioteca padrão do Python [argparse](https://docs.python.org/3/library/argparse.html).

Confira a [Wiki](https://github.com/mateusoliveira43/python-cli-script-template/wiki) do repositório para mais detalhes.

# Exemplo de uso

Na pasta script, o pacote Python `example` e o módulo Python `run_example` são exemplos de uso do modelo.

Na rodar o exemplo, execute
```
[python|python3] scripts/run_example.py
[python|python3] scripts/run_example.py -h
[python|python3] scripts/run_example.py --help
```
para mostrar a mensagem de ajuda do script de exemplo. Executar o script com o comando de Python 3 é opcional.

# Qualidade

Para rodar as métricas de qualidade do modelo, é necessário instalar seus requisitos. Para instalá-los, execute
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

## Formatadores de código

Para formatar as importações, execute
```
isort -vm 3 --tc --gitignore .
```

## Varredura de vulnerabilidades de segurança

Para checar problemas de segurança comuns no código fonte, execute
```
bandit -r scripts
```

Para checar vulnerabilidades de segurança conhecidas nas dependências instaladas, execute
```
safety check
```

# Licença

Esse repositório é licenciado sob os termos da [Licença MIT](LICENSE).
