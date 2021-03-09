# Modelo de script Python

- [README file in English](README.md)

Modelo para criar scripts Python.

## Tasks

- [ ] Opção para traduzir as mensagens de erro também.
- [ ] Resolver *shebang* do Python no Linux Mint.

# Sobre o Modelo

Na pasta do projeto, execute
```
python3 ./script.py
python3 ./script.py -h
python3 ./script.py --help
```
para mostrar a mensagem de ajuda do script.

Para trocar o título de **modo de uso**, altere a linha 14 de `script.py`.
Para trocar a mensagem de **modo de uso**, altere a linha 84 de `script.py`.
Para trocar a mensagem de **descrição**, altere a linha 85 de `script.py`.
Para trocar a mensagem de **epílogo**, altere a linha 86 de `script.py`.
Para trocar o título de **opções obrigatórias**, altere a linha 90 de `script.py`.
Para trocar o título de **opções**, altere a linha 91 de `script.py`.
Para trocar a mensagem de **ajuda**, altere a linha 92 de `script.py`.
Siga os exemplos de **Required options**, **Options** e **Commands** para criar as opções obrigatórias, opções e comandos do script.
Para desabilitar mostrar a mensagem de **ajuda** quando executar o script sem argumentos, remova os argumentos da função na linha 128 de `script.py`.
Comece a lógica do script na linha 130 de `script.py`.

# Licença

Esse repositório é licenciado sob os termos da [Licença MIT](LICENSE).
