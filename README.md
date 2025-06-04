# Sistema de Gerenciamento de Agendamentos de Salão de Beleza

Este é um protótipo funcional de um sistema de gerenciamento de agendamentos para um salão de beleza. Desenvolvido em Python, utiliza Tkinter para a interface gráfica e SQLite para o banco de dados local, com foco na arquitetura MVC.

## Funcionalidades Principais

* **Cadastro do Primeiro Usuário Administrador**:
    * Na primeira execução da aplicação (se nenhum usuário existir), uma tela especial permite o cadastro do primeiro usuário administrador com nome de usuário e senha.
* **Login**:
    * Autenticação de usuário com nome de usuário e senha.
    * As senhas são armazenadas de forma segura no banco de dados utilizando hash e salt.
* **Gerenciamento Completo de Agendamentos (CRUD)**:
    * **Cadastro**: Permite registrar novos agendamentos detalhando cliente, data, horário, tipo de serviço e valor.
    * **Listagem**: Exibe todos os agendamentos de forma organizada.
    * **Edição**: Permite a alteração dos dados de agendamentos existentes.
    * **Remoção**: Permite excluir agendamentos do sistema após confirmação.
* **Geração de Relatórios**:
    * Apresenta um relatório básico listando todos os agendamentos cadastrados.
* **Interface Gráfica**:
    * Desenvolvida com Tkinter, com janelas dedicadas para o cadastro inicial, login, gerenciamento principal e relatórios.

## Requisitos

* **Python**: Versão 3.6 ou superior.
    * **Tkinter**: Geralmente incluído na instalação padrão do Python.
    * **SQLite 3**: Geralmente incluído na instalação padrão do Python.
    * **Módulos padrão**: `hashlib` e `os` (utilizados para o sistema de senhas).

## Como Rodar a Aplicação

1.  **Preparar o Ambiente**:
    * Certifique-se de ter o Python 3.6 (ou mais recente) instalado.
    * Clone ou baixe todos os arquivos do projeto para um diretório em seu computador:
      ```bash
       git clone https://github.com/jorgemdt/gerenciamento-de-salao.git
      ```



2.  **Executar a Aplicação**:
    * Abra um terminal ou prompt de comando.
    * Navegue até o diretório raiz do projeto (a pasta que contém o arquivo `main.py`).
    * Execute o comando:
        ```bash
        python main.py
        ```

3.  **Primeira Execução**:
    * Ao rodar a aplicação pela primeira vez (ou após deletar o `database.db`), você será apresentado a uma tela de "Cadastro do Primeiro Usuário".
    * Crie um nome de usuário e uma senha para o administrador do sistema. Confirme a senha.
    * Após o cadastro bem-sucedido, a tela de login normal será exibida.

4.  **Execuções Subsequentes**:
    * A tela de login será exibida diretamente.
    * Utilize o nome de usuário e a senha que você cadastrou para acessar o sistema.

Após o login, a tela principal de gerenciamento de agendamentos estará disponível.
