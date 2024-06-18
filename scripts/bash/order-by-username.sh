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


# Função de use para exibir a forma correta de usar o script
function use() {
  in_cyan "Como usar: $0 <nome_do_arquivo> [ordem] [quantidade]\n"
  in_cyan "  <nome_do_arquivo>  Nome do arquivo de entrada\n"
  in_cyan "  [ordem]            Ordem de classificação: 'asc' (padrão) ou 'desc'\n"
  exit 1
}

# Função para verificar se o arquivo existe
function check_file() {
  local arquivo="$1"
  if [[ ! -f "$arquivo" ]]; then
    in_red "Arquivo $arquivo não encontrado!\n"
    exit 1
  fi
}

# Função para determinar a ordem de classificação
function set_order() {
  local ordem="$1"
  if [[ "$ordem" == "-desc" || "$ordem" == "desc" ]]; then
    echo "sort -r"
  else
    echo "sort"
  fi
}

# Função para listar usuários
function list_users() {
  local arquivo="$1"
  local sort_cmd="$2"
  awk '{print $0}' "$arquivo" | $sort_cmd
}


###########################################################
#                        VARIÁVEIS                        #
###########################################################

# Nome do arquivo de entrada
ARQUIVO="$1"

# Ordem de classificação (padrão: ascendente)
ORDEM="${2:-asc}"


###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Verifica se o nome do arquivo foi passado como parâmetro
if [[ $# -lt 1 ]]; then
  use
fi

# Verifica se o arquivo existe
check_file "$ARQUIVO"

# Determina a ordem de classificação
SORT_CMD=$(set_order "$ORDEM")

# Lista os usuários ordenados
list_users "$ARQUIVO" "$SORT_CMD"
