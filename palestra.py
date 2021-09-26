#!/usr/bin/env python3

import argparse
import sys
from typing import List


class FormatadorCustomizado(argparse.HelpFormatter):
    """Formatador customizado para interpretador de argumentos do argparse.

    Métodos
    -------
    _format_usage(self, usage, actions, groups, prefix)
        Formata o prefixo da seção modo de uso.
    _format_action(self, action)
        Remove variável de ajuda do sub-interpretador ao listar na ajuda.
    _format_action_invocation(self, action)
        Adiciona variável de ajuda apenas uma vez ao listar opções na ajuda.
    """
    def __init__(self, *args, **kwargs):
        super(FormatadorCustomizado, self).__init__(*args, **kwargs)

    def _format_usage(self, usage, actions, groups, prefix):
        return super(FormatadorCustomizado, self)._format_usage(
            usage, actions, groups, 'Modo de uso:\n\t[python|python3] '
        )

    def _format_action(self, action):
        parts = super(FormatadorCustomizado, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            line_break = '\n'
            parts = line_break.join(parts.split(line_break)[1:])
        return parts

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        metavar = self._format_args(
            action, self._get_default_metavar_for_optional(action)
        )
        comma = ', '
        return f'{comma.join(action.option_strings)} {metavar}'


interpretador = argparse.ArgumentParser(
    add_help=False,
    allow_abbrev=False,
    description='Baleiador: controle de contêineres em português.',
    epilog='Python Floripa',
    prog=sys.argv[0],
    formatter_class=FormatadorCustomizado,
)
interpretador._optionals.title = 'Opções'
interpretador._positionals.title = 'Opções obrigatórias'


def inteiro_positivo(entrada: str) -> int:
    """Checa se a entrada do usuário foi um número inteiro positivo.

    Parâmetros
    ----------
    entrada : str
        Entrada do usuário a ser analisada.

    Retorna
    -------
    int
        Valor convertido para inteiro.

    Levanta
    -------
    ArgumentTypeError
        Se a entrada não pode ser convertida em um número inteiro ou não é
        positiva.
    """
    try:
        valor = int(entrada)
        if valor <= 0:
            raise argparse.ArgumentTypeError(
                'deve ser um número inteiro positivo.'
            )
        return valor
    except ValueError:
        raise argparse.ArgumentTypeError('deve ser um número inteiro.')


# Opções ######################################################################
interpretador.add_argument(
    '-a', '--ajuda',
    action='help',
    help='Mostra a ajuda de uso do script.'
)

interpretador.add_argument(
    '-v', '--versao',
    action='version',
    version='Baleidor versão 1.0.0',
    help='Mostra a versão do script.'
)

interpretador.add_argument(
    '-d', '--depuracao',
    action='store_true', default=False,
    help='Executa Baleiador em modo de depuração.'
)


# Opções obrigatórias #########################################################
# interpretador.add_argument(
#     'idade',
#     type=inteiro_positivo,
#     help='Idade do usuário, em anos.'
# )

# Comandos ####################################################################


def iniciar():
    print('Iniciando contêiner...')


def inspecionar():
    print('Inspecionado contêiner...')


def destruir():
    print('Destruindo contêiner...')


sub_interpretador = interpretador.add_subparsers(
    dest='comando',
    metavar='[COMANDOS]',
    title='Comandos',
    prog=sys.argv[0],
)
comandos = dict(
    iniciar=dict(
        ajuda='Inicia um contêiner a partir de um arquivo Dockerfile.',
        comando=iniciar
    ),
    inspecionar=dict(
        ajuda='Retorna informações de um contêiner.',
        comando=inspecionar
    ),
    destruir=dict(
        ajuda='Destrói um contêiner.',
        comando=destruir
    ),
)
# orderna os comandos em ordem alfabética automaticamente
comandos = dict(sorted(comandos.items()))

for nome_comando in comandos:
    comando = sub_interpretador.add_parser(
        nome_comando, help=comandos[nome_comando].get('ajuda')
    )
    comando.allow_abbrev = False
    comando.formatter_class = FormatadorCustomizado
    comando._positionals.title = 'Opções obrigatórias'
    comando._optionals.title = 'Opções'
    comando.description = str(comandos[nome_comando].get('ajuda'))
    comando.epilog = 'Python Floripa'

    comando.add_argument(
        '-n', '--nome',
        metavar='<texto>', type=str,
        help='Nome do contêiner.'
    )


def iniciar_interpretador(argumentos: List[str]):
    """Inicia a interface de linha de comando (CLI) do interpretador.

    Parâmetros
    ----------
    argumentos : List[str]
        Lista de argumentos a serem analisados.

    Retorna
    -------
    Namespace
        Argumentos usados e não usados.
    """
    return interpretador.parse_args(argumentos)


def principal():
    """Função principal do script, adicone a lógica aqui."""
    argumentos = iniciar_interpretador(sys.argv[1:] or ['--ajuda'])
    print(argumentos)
    comando = comandos.get(argumentos.comando)
    if comando:
        comando.get('comando')()


if __name__ == '__main__':
    principal()
