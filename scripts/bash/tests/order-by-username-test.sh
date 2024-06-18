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

# Função para executar o script e obter a saída
function run_script() {
  local input_file="$1"
  local order="$2"
  local head_arg="$3"

  local script_output=$(./../order-by-username.sh "$input_file" "$order")

  # Aplica head -n se head_arg for definido
  if [[ -n "$head_arg" ]]; then
    script_output=$(echo "$script_output" | head -n "$head_arg")
  fi

  echo "$script_output"
}

# Teste de ordenação crescente
function test_ordem_crescente() {
  local input_file="usuarios.txt"
  local expected_output="damejoxo@uol.com.br inbox 002200463 size 002142222
jane.smith@yahoo.com inbox 000987654 size 000876543
john.doe@gmail.com inbox 001234567 size 001234567"

  local actual_output=$(run_script "$input_file" "asc")
  assert_equal "$expected_output" "$actual_output" "Teste de ordenação crescente"
}

# Teste de ordenação decrescente
function test_ordem_decrescente() {
  local input_file="usuarios.txt"
  local expected_output="john.doe@gmail.com inbox 001234567 size 001234567
jane.smith@yahoo.com inbox 000987654 size 000876543
damejoxo@uol.com.br inbox 002200463 size 002142222"

  local actual_output=$(run_script "$input_file" "desc")
  assert_equal "$expected_output" "$actual_output" "Teste de ordenação decrescente"
}

# Teste para verificar a aplicação de head -n #
function test_head_n() {
  local input_file="usuarios.txt"
  local expected_output="damejoxo@uol.com.br inbox 002200463 size 002142222
jane.smith@yahoo.com inbox 000987654 size 000876543"

  local actual_output=$(run_script "$input_file" "asc" 2)
  assert_equal "$expected_output" "$actual_output" "Teste de head -n #"
}

###########################################################
#                        EXECUÇÃO                         #
###########################################################

# Execução dos testes
test_ordem_crescente
test_ordem_decrescente
test_head_n
