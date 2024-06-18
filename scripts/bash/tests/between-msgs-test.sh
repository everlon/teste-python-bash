#!/bin/bash

###########################################################
#         Everlon Passos <everlon@protonmail.com>         #
###########################################################


###########################################################
#               TESTES DE UNIDADE / TDD                   #
###########################################################

# Função para comparar saídas esperadas com a saída real
function assert_equal() {
  local expected="$1"
  local actual="$2"
  local message="$3"

  if [[ "$expected" == "$actual" ]]; then
    echo -e "PASSED: $message"
  else
    echo -e "FAILED: $message"
    echo "Expected: $expected"
    echo "Actual  : $actual"
  fi
}

# Teste de uso incorreto
function test_usage() {
  local expected="Como usar: ./../between-msgs.sh <arquivo> <limite_inferior> <limite_superior>"
  local actual=$(./../between-msgs.sh 2>&1 | head -n 1)
  assert_equal "$expected" "$actual" "Teste de uso incorreto"
}

# Teste de arquivo inexistente
function test_file_not_found() {
  local expected="Arquivo teste.txt não encontrado!"
  local actual=$(./../between-msgs.sh teste.txt 50 200 2>&1 | head -n 1)
  assert_equal "$expected" "$actual" "Teste de arquivo inexistente"
}

# Teste de filtragem de usuários por faixa de mensagens
function test_filter_users_by_msg_count() {
  # Criando um arquivo temporário com dados de teste
  cat << EOF > test_input.txt
user1@example.com inbox 100 size 500
user2@example.com inbox 150 size 600
user3@example.com inbox 200 size 700
user4@example.com inbox 250 size 800
EOF

  local expected="user1@example.com inbox 100 size 500
user2@example.com inbox 150 size 600
user3@example.com inbox 200 size 700"

  local actual=$(./../between-msgs.sh test_input.txt 100 200)
  assert_equal "$expected" "$actual" "Teste de filtragem por faixa de mensagens"

  # Removendo o arquivo temporário após os testes
  rm test_input.txt
}

###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Executar os testes
test_file_not_found
test_usage
test_filter_users_by_msg_count
