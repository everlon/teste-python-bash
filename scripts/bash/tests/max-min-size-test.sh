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
    echo "PASSED: $message"
  else
    echo "FAILED: $message"
    echo "Expected: $expected"
    echo "Actual  : $actual"
  fi
}

# Teste para verificar se o script encontra o usuário com maior size
function test_max_size() {
  local input_file="usuarios.txt"
  local expected_output="damejoxo@uol.com.br inbox 002200463 size 002142222"

  local actual_output=$(./../max-min-size.sh "$input_file")
  assert_equal "$expected_output" "$actual_output" "Teste de maior size"
}

# Teste para verificar se o script encontra o usuário com menor size
function test_min_size() {
  local input_file="usuarios.txt"
  local expected_output="jane.smith@yahoo.com inbox 000987654 size 000876543"

  local actual_output=$(./../max-min-size.sh "$input_file" -min)
  assert_equal "$expected_output" "$actual_output" "Teste de menor size"
}

###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Execução dos testes
test_max_size
test_min_size
