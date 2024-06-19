#!/bin/bash

###########################################################
#         Everlon Passos <everlon@protonmail.com>         #
###########################################################

#
# Este script é somente um teste para retornar JSON no próprio ShellScript/BASH
#

function check_file_exists() {
  local arquivo="$1"
  if [[ ! -f "$arquivo" ]]; then
    echo "Arquivo $arquivo não encontrado!"
    exit 1
  fi
}

function filter_users_by_msg_count() {
  local arquivo="$1"
  local limite_inferior="$2"
  local limite_superior="$3"

  awk -v li="$limite_inferior" -v ls="$limite_superior" '
  BEGIN {
    print "["
    first = 1
  }
  $2 == "inbox" && $3 >= li && $3 <= ls {
    if (!first) print ","
    printf "  {\"username\":\"%s\",\"folder\":\"%s\",\"numberMessages\":%d,\"size\":%d}", $1, $2, $3, $5
    first = 0
  }
  END {
    print "\n]"
  }' "$arquivo"
}

ARQUIVO="$1"
LIMITE_INFERIOR="$2"
LIMITE_SUPERIOR="$3"

check_file_exists "$ARQUIVO"

filter_users_by_msg_count "$ARQUIVO" "$LIMITE_INFERIOR" "$LIMITE_SUPERIOR"
