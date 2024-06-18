#!/bin/bash

###########################################################
#         Everlon Passos <everlon@protonmail.com>         #
###########################################################


###########################################################
#                        FUNÇÕES                          #
###########################################################

# Funções para saídas em cores.
# Pequena brincadeira com cores no terminal.
_color()     { tput -Txterm setaf ${1}; echo -ne ${2}; tput -Txterm sgr0; }
in_red()     { _color 1 "${1}"; } # use for failures
in_green()   { _color 2 "${1}"; } # use for successes
in_yellow()  { _color 3 "${1}"; } # use for warnings / attention
in_magenta() { _color 5 "${1}"; } # use for debug messages
in_cyan()    { _color 6 "${1}"; } # use for main actions / progress

# Função de como usar de forma correta o script.
function use_correct() {
  in_cyan "Como usar: $0 <arquivo> [-min]\n"
  in_cyan "  <arquivo>  Arquivo de entrada no formato 'email inbox NNNNNNNN size NNNNNNNN' por linha\n"
  in_cyan "  -min       Encontrar o usuário com o menor 'size' (opcional)\n"
  exit 1
}

# Função para verificar se o arquivo existe.
function check_file() {
  local arquivo="$1"
  if [[ ! -f "$arquivo" ]]; then
    in_red "Arquivo $arquivo não encontrado!\n"
    exit 1
  fi
}

# Função para determinar o comando de ordenação com base no parâmetro.
function set_order() {
  local parametro="$1"
  if [[ "$parametro" == "-min" || "$parametro" == "min" ]]; then
    echo "sort -k5n"  # Ordena pelo quinto campo numericamente (campo size).
  else
    echo "sort -k5nr"  # Ordena pelo quinto campo numericamente reverso (campo size).
  fi
}

# Função principal para encontrar o usuário com maior ou menor "size".
function get_user_max_min_size() {
  local arquivo="$1"
  local comando_de_ordenacao="$2"

  awk '{print $0}' "$arquivo" | $comando_de_ordenacao | head -n 1
}


###########################################################
#                        VARIÁVEIS                        #
###########################################################

ARQUIVO="$1"

###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Verifica o número de parâmetros
if [[ $# -lt 1 || $# -gt 2 ]]; then
  use_correct
fi

# Verifica se o arquivo existe
check_file "$ARQUIVO"

# Determina o comando de ordenação com base no parâmetro
SORT_CMD=$(set_order "${2:-}")

# Encontra o usuário com maior ou menor size
get_user_max_min_size "$ARQUIVO" "$SORT_CMD"
