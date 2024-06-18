#!/bin/bash

###########################################################
#         Everlon Passos <everlon@protonmail.com>         #
###########################################################


###########################################################
#                        FUNÇÕES                          #
###########################################################

# Função para exibir o uso correto do script
function usage() {
  echo "Como usar: $0 <arquivo> <limite_inferior> <limite_superior>"
  echo "  <arquivo>         Arquivo de entrada no formato 'email inbox NNNNNNNN size NNNNNNNN' por linha"
  echo "  <limite_inferior> Limite inferior de quantidade de mensagens na INBOX"
  echo "  <limite_superior> Limite superior de quantidade de mensagens na INBOX"
  exit 1
}

# Função para verificar se o arquivo existe
function check_file_exists() {
  local arquivo="$1"
  if [[ ! -f "$arquivo" ]]; then
    echo "Arquivo $arquivo não encontrado!"
    exit 1
  fi
}

# Função principal para filtrar e exibir usuários na faixa especificada de mensagens na INBOX
function filter_users_by_msg_count() {
  local arquivo="$1"
  local limite_inferior="$2"
  local limite_superior="$3"

  awk -v li="$limite_inferior" -v ls="$limite_superior" '$2 == "inbox" && $3 >= li && $3 <= ls' "$arquivo"
}

###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Verifica o número de parâmetros
if [[ $# -ne 3 ]]; then
  usage
fi

###########################################################
#                        VARIÁVEIS                        #
###########################################################

# Determinando as variáveis com os Parâmetros de entrada
ARQUIVO="$1"
LIMITE_INFERIOR="$2"
LIMITE_SUPERIOR="$3"

###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Verifica se o arquivo existe
check_file_exists "$ARQUIVO"

# Filtra e exibe os usuários na faixa solicitada de mensagens na INBOX
filter_users_by_msg_count "$ARQUIVO" "$LIMITE_INFERIOR" "$LIMITE_SUPERIOR"
