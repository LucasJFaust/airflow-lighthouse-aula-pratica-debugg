# airflow-lighthouse-aula-pratica-debugg
# 🛠️ Astro CLI + Airflow: Debugging e Solução de Problemas em Orquestração

## 1. Visão Geral

Bem-vindos ao repositório de suporte à aula prática de "Lidando com problemas de Orquestração | Airflow, debugging, logs"! Este projeto foi cuidadosamente elaborado para simular **cinco cenários comuns de falhas** em pipelines de dados orquestrados pelo Apache Airflow.

Aqui, você terá a oportunidade de aplicar os conceitos teóricos aprendidos na aula, utilizando o **Astro CLI** para agilizar o desenvolvimento e depuração local, e a **Airflow UI** para monitoramento e análise detalhada. Nosso objetivo é transformar você em um verdadeiro "detetive" de dados, capaz de navegar pela complexidade e garantir a resiliência dos seus pipelines, mesmo **sem depender exclusivamente da interface gráfica**.

## 2. Pré-requisitos - Preparando seu Ambiente

Para que você possa executar este projeto e aproveitar a experiência prática, certifique-se de ter os seguintes softwares e ferramentas instalados e configurados em sua máquina. **É crucial seguir estas etapas para garantir que o Astro CLI funcione corretamente.**

1.  **[VS Code](https://code.visualstudio.com/):** Nosso ambiente de desenvolvimento integrado (IDE) preferido. Ele oferece excelentes recursos para Python e Docker. Instale-o se ainda não tiver.
2.  **[Docker Desktop](https://www.docker.com/products/docker-desktop/):** O Astro CLI utiliza Docker para criar e gerenciar seu ambiente Airflow local. **Certifique-se de que o Docker Desktop esteja em execução** antes de iniciar o ambiente Astro. Faça o download e a instalação para o seu sistema operacional.
3.  **[Astro CLI](https://docs.astronomer.io/astro/cli/install-cli):** A ferramenta de linha de comando essencial para interagir com o Airflow, tanto localmente quanto com o Astronomer Cloud.

    ### Instalação do Astro CLI (Escolha uma opção):

    *   **macOS (Homebrew):**
        ```bash
        brew install astro
        ```
    *   **Linux (apt):**
        ```bash
        curl -sL 'https://raw.githubusercontent.com/astronomer/astro-cli/main/install.sh' | sudo bash -s -- -b /usr/local/bin
        ```
    *   **Windows (Chocolatey ou WSL):** A forma mais recomendada para Windows é usar o [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/pt-br/windows/wsl/) e instalar o Astro CLI dentro dele, seguindo as instruções do Linux. Alternativamente, você pode usar o Chocolatey.
        ```powershell
        # No PowerShell (como Administrador)
        choco install astro-cli
        ```
        (Verifique a documentação oficial para a instalação mais atualizada para Windows). 

    ### Verificação da Instalação do Astro CLI:

    Após a instalação, abra seu terminal (ou o terminal integrado do VS Code) e execute:
    ```bash
    astro version
    ```
    Você deverá ver a versão do Astro CLI instalada. Se você receber um erro, revise as etapas de instalação.

## 3. Configuração e Inicialização do Ambiente

Siga estes passos para configurar e iniciar seu ambiente Airflow local. **Leia com atenção para entender o fluxo de trabalho local com o Astro CLI.**

1.  **Clone o Repositório e crie um arquivo de requirements.txt:**
    Abra seu terminal e execute:
    ```bash
    git clone https://github.com/LucasJFaust/airflow-lighthouse-aula-pratica-debugg # Substitua pela URL real do seu repositório
    cd seu-repositorio-de-aula # Navegue até a pasta do projeto
    ```
     **Verifique e prepare o `requirements.txt`:**
    O Astro CLI utiliza o arquivo `requirements.txt` (localizado na raiz do seu projeto) para instalar as dependências Python necessárias dentro do ambiente Airflow. **Certifique-se de que este arquivo existe e contenha todas as bibliotecas que suas DAGs irão utilizar (como `requests`, `apache-airflow` na versão desejada, etc.) ANTES de iniciar o ambiente.**

    Exemplo de `requirements.txt` para este projeto:
    ```
    requests
    ```
    *   **Importante:** Se você modificar o `requirements.txt` após o `astro dev start` inicial, será necessário executar `astro dev restart` (ou `astro dev kill` e `astro dev start`) para que as novas dependências sejam instaladas nos contêineres do Airflow.
    No terminal execute:
    ```bash
    touch requirements.txt
    ```


2.  **Inicie o Ambiente Airflow Local com Astro CLI:**
     Este comando cria a estrutura de projeto que o Astro CLI espera (`.astro/` folder, `Dockerfile` e `packages.txt`).
    ```bash
    astro dev init
    ```
    *   Se for perguntado sobre sobrescrever arquivos como `Dockerfile` ou `packages.txt`, pode aceitar as opções padrão ou pular se já tiverem customizações que você queira manter (neste caso, para a aula, os padrões são suficientes).
    *   **Opcional:** Se você tem customizações em um `Dockerfile` ou `packages.txt` que não foram criados pelo `astro dev init`, você pode movê-los para dentro da pasta `.astro/` após a inicialização. Para este laboratório, o `astro dev init` já cria o básico necessário.
    Dentro da pasta do projeto (`seu-repositorio-de-aula`), execute o comando para iniciar o ambiente Airflow local. **Este é o comando chave para começar a trabalhar. Verifique que está executando ele no diretório correto.**
    ```bash
    astro dev start
    ```
    *   Este comando irá:
        *   Ler o arquivo `requirements.txt` e instalar as dependências Python no ambiente Airflow.
        *   Baixar as imagens Docker necessárias (Airflow Scheduler, Webserver, PostgreSQL, Redis).
        *   Construir os contêineres e iniciá-los, configurando as redes e volumes necessários.
        *   Sincronizar seus arquivos de DAGs (na pasta `dags/`) com o contêiner do Airflow.
    *   Este processo pode levar **vários minutos na primeira vez** (especialmente o download das imagens). Tenha paciência.

    ### Solução de Problemas Comuns `astro dev start`:

    *   **Docker Desktop não iniciado:** Verifique se o Docker Desktop está rodando. O `astro dev start` *depende* dele.
    *   **Porta 8080 em uso:** Se você tiver outro serviço usando a porta `8080`, o Astro CLI pode falhar. Você pode parar o outro serviço ou, para ambientes mais avançados, configurar o `docker-compose.yaml` gerado pelo Astro CLI em `.astro/` para usar outra porta.
    *   **Erros de `requirements.txt`:** Se houver erros na instalação de pacotes Python, verifique a sintaxe do seu `requirements.txt`.

3.  **Acesse a UI do Airflow:**
    Após o `astro dev start` concluir, o terminal exibirá a URL da interface do usuário do Airflow. Geralmente, é:
    [http://localhost:8080/](http://localhost:8080/) 
    Abra essa URL em seu navegador. As credenciais padrão são `admin`/`admin`.

## 4. Estrutura do Projeto

Entender a estrutura do projeto é crucial para a navegação e o debugging:
seu-repositorio-de-aula/ ├── dags/ # Contém os arquivos Python das DAGs │ ├── problem_config_and_logic_dag.py # Problema 1: Variável e Lógica │ ├── problem_stuck_sensor_dag.py # Problema 2: Sensor que trava │ ├── problem_dag_parsing_error.py # Problema 3: Erro de Parsing/Sintaxe (DAG não aparece!) │ ├── problem_resource_intensive_dag.py # Problema 4: Consumo de Recursos (OOMKilled/Lento) │ └── problem_external_connection_dag.py # Problema 5: Erro de Conexão Externa ├── data/ # Contém arquivos de dados de exemplo utilizados pelas DAGs │ └── initial_data.txt ├── .astro/ # Diretório oculto gerado pelo Astro CLI com configurações ├── .env # Arquivo de variáveis de ambiente (se usado) ├── requirements.txt # Lista de pacotes Python para o ambiente Airflow ├── docker-compose.yaml # Arquivo Docker Compose gerado pelo Astro CLI └── README.md # Este arquivo!


## 5. O Case Técnico - Cenários de Problemas (e como diagnosticá-los!)

Este projeto contém **cinco DAGs intencionalmente problemáticas**, cada uma demonstrando um tipo diferente de falha comum em pipelines de dados Airflow, conforme discutido no **Slide 13: Fontes de Problemas**.

Para cada problema, você deverá usar as ferramentas visuais da Airflow UI e os poderosos comandos do Astro CLI para identificar e diagnosticar a causa raiz.

### Guia Geral de Debugging e Análise de Logs (Sua Caixa Preta!)

Antes de mergulhar nos problemas específicos, familiarize-se com a abordagem geral de depuração, que integra os conceitos dos **Slides 05, 06, 11 e 12** da apresentação:

1.  **Identificação Visual (Airflow UI - Grid View / Graph View):**
    *   Vá para a `Grid View` do DAG problemático. Observe o status geral.
    *   **Pergunte-se (Slide 05 - Grid View):** "Qual tarefa está em vermelho (falha) ou em um estado inesperado (`up_for_retry`, `running` indefinidamente)? Quais são as cores das outras tarefas? Há algum padrão de falha?"
    *   Navegue para a `Graph View` do DAG.
    *   **Pergunte-se (Slide 06 - Graph View):** "Qual é a sequência de execução? Qual tarefa falhou e quais tarefas são `downstream` dela? Elas foram `skipped`? Isso faz sentido com as dependências?"

2.  **Análise de Logs (Airflow UI - Task Instance Logs / Astro CLI Logs):**
    *   **Primeira Leitura (UI):** Na `Grid View` ou `Graph View`, clique na tarefa falha (ou na que está travada) e selecione "View Log" ou "Logs".
    *   **Pergunte-se (Slide 11 - Anatomia dos Logs):**
        *   "Qual é o `Timestamp` do erro? Houve algum evento anterior relevante?"
        *   "Qual é o `Level` da mensagem? Estou vendo `ERROR` ou `CRITICAL`?"
        *   "Qual a `Message` do erro? Há alguma mensagem `print()` minha que pode dar uma pista?"
        *   "Há um `StackTrace`? Se sim, lembre-se: **leia de baixo para cima**! Qual o `Exception Type` e onde está o número da linha no código da minha DAG?"
    *   **Leitura Detalhada (Astro CLI) - SEMPRE QUE POSSÍVEL, USE ESTES COMANDOS!**
        Abra um novo terminal no VS Code (sem parar o `astro dev start`).
        *   Para ver logs de uma tarefa específica diretamente no terminal (mais rápido e fácil para copiar):
            ```bash
            astro dev logs --dag-id <dag_id> --task-id <task_id> --follow
            # Exemplo: astro dev logs --dag-id problem_config_and_logic_dag --task-id process_data_with_config_and_logic_error --follow
            ```
        *   Para seguir os logs de todos os componentes do Airflow (útil para `Scheduler` e `Webserver` logs):
            ```bash
            astro dev logs --follow
            ```
        *   **Pergunte-se (Slide 12 - Estratégias de Busca):** "Com quais `Keywords` posso procurar? `ERROR`, `Exception`, `Failed`, `Traceback`? Posso filtrar por `task_id` ou `Timestamp`?"

3.  **Diagnóstico e Raciocínio Lógico (Aplicando o Slide 13 - Fontes de Problemas):**
    *   Com base nos logs, qual é a **causa raiz** do problema?
    *   **Pergunte-se:** "Qual categoria de problema (do Slide 13) se encaixa melhor aqui? Isso me ajuda a pensar na solução?"
    *   **Pergunte-se:** "Como eu poderia simular esse erro rapidamente localmente para testar uma possível correção, antes de mudar o DAG completo, **sem precisar da UI do Airflow**?" (Pense nos comandos `astro dev run airflow tasks test` ou `astro dev run airflow dags parse` - **Slide 10**).

---

### Detalhes de Cada Problema e Passos para Reprodução

#### Problema 1: Variável de Configuração Ausente e Erro de Lógica (`problem_config_and_logic_dag`)

*   **Descrição:** Este DAG falha porque espera uma `Airflow Variable` (`processing_chunk_size`) que não está definida na UI do Airflow. Além disso, se a variável fosse definida, há um erro lógico que pode ocorrer em um caso de borda.
*   **Categorias de Problema (Slide 13):** Permissões/Variáveis (principal), Lógica da Task (secundário).
*   **Passos para Reproduzir:**
    1.  Na Airflow UI, ative o DAG `problem_config_and_logic_dag`.
    2.  Clique em `Trigger DAG`.
    3.  Observe a falha na `Grid View`.
*   **Diagnóstico e Pistas:**
    *   A tarefa `process_data_with_config_and_logic_error` falhará.
    *   Os logs (UI ou `astro dev logs`) mostrarão um `KeyError` ou `ValueError` relacionado à `Variable.get("processing_chunk_size")`.
*   **Solução:**
    1.  **Corrija a Variável:** Na Airflow UI, vá em `Admin` -> `Variables`. Crie uma nova variável com **Key:** `processing_chunk_size` e **Value:** `10` (ou qualquer número inteiro).
    2.  Dispare o DAG novamente. Observe que ele passará pela primeira falha.
    3.  *(Opcional/Discussão em aula):* Se o `IndexError` surgir (dependendo da manipulação de `initial_data.txt`), mostre como o `astro dev run airflow tasks test` para a função `_process_data_with_config_and_logic_error` poderia ter ajudado a isolar o erro de lógica.

#### Problema 2: Sensor Travado (`problem_stuck_sensor_dag`)

*   **Descrição:** Este DAG tem um `FileSensor` que aguarda a criação de um arquivo específico (`/tmp/data_notification_file.txt`). No entanto, a tarefa anterior que deveria criar este arquivo (`_generate_data_but_fail_to_create_notification_file`) *intencionalmente não o faz*, fazendo com que o sensor fique travado até atingir seu `timeout`.
*   **Categorias de Problema (Slide 13):** Lógica da Task (a tarefa anterior falha em sua lógica de notificação), Conexão Externa (do ponto de vista do sensor, o evento externo não ocorreu).
*   **Passos para Reproduzir:**
    1.  Na Airflow UI, ative o DAG `problem_stuck_sensor_dag`.
    2.  Clique em `Trigger DAG`.
    3.  Observe que a tarefa `wait_for_data_notification` permanecerá em estado `running` (ou `up_for_retry`) por um tempo, eventualmente falhando por `timeout`.
*   **Diagnóstico e Pistas:**
    *   Os logs da tarefa `wait_for_data_notification` mostrarão repetições de "Poking for file..." e, eventualmente, um `AirflowSensorTimeout`.
    *   Os logs da tarefa `generate_data_but_fail_to_create_notification_file` (a `upstream`) são cruciais: eles indicarão que o arquivo *não* foi criado intencionalmente. Use `astro dev logs` para vê-los em detalhe.
*   **Solução:**
    1.  **Edite o DAG:** No VS Code, abra `dags/problem_stuck_sensor_dag.py`.
    2.  Na função `_generate_data_but_fail_to_create_notification_file`, **descomente as linhas** que criam o arquivo `/tmp/data_notification_file.txt`.
    3.  Salve o arquivo. O Airflow recarregará a DAG.
    4.  Dispare o DAG novamente na UI. O sensor deverá passar rapidamente.

#### Problema 3: Erro de Parsing/Sintaxe (`problem_dag_parsing_error`)

*   **Descrição:** Este arquivo de DAG (`problem_dag_parsing_error.py`) contém um erro de sintaxe Python intencional. Isso impedirá que o `Airflow Scheduler` consiga carregá-lo, resultando na DAG **não aparecendo na UI** ou gerando um `Dag Import Error` no log do Scheduler.
*   **Categorias de Problema (Slide 13):** Parsing da DAG.
*   **Passos para Reproduzir:**
    1.  **Inicialmente, esta DAG NÃO APARECERÁ na UI do Airflow.** Este é o primeiro sinal.
    2.  Se você tentar corrigir, mas o erro persistir, o Scheduler pode reclamar.
*   **Diagnóstico e Pistas (SEM A UI!):**
    *   **Primeira pista:** A DAG simplesmente não está na lista de DAGs da Airflow UI.
    *   **Astro CLI para diagnosticar parsing (Slide 10):**
        Abra um terminal e execute:
        ```bash
        astro dev run airflow dags parse /usr/local/airflow/dags/problem_dag_parsing_error.py
        ```
        *Este comando irá simular o processo de parsing do Airflow e reportar o erro de sintaxe diretamente no seu terminal, indicando a linha exata!*
    *   Verifique os logs do Scheduler via `astro dev logs --follow`. Você verá mensagens de `DagFileProcessor` falhando ao carregar o arquivo.
*   **Solução:**
    1.  **Edite o DAG:** No VS Code, abra `dags/problem_dag_parsing_error.py`.
    2.  **Corrija o erro de sintaxe:** Por exemplo, adicione o parêntese `)` que falta na linha do `print()`.
    3.  Salve o arquivo. O Scheduler detectará a mudança e tentará recarregar.
    4.  Verifique a Airflow UI; a DAG `problem_dag_parsing_error` agora deverá aparecer.

#### Problema 4: Uso Intenso de Recursos (`problem_resource_intensive_dag`)

*   **Descrição:** A tarefa `consume_memory_and_cpu_task` tenta alocar uma grande quantidade de memória e/ou executa um loop pesado. Dependendo da configuração de recursos do seu ambiente Docker, isso pode levar a:
    *   Uma falha `OOMKilled` (Out Of Memory Killed), onde o sistema operacional encerra a tarefa.
    *   Uma execução extremamente lenta que eventualmente atinge um timeout do Airflow, ou apenas demora muito.
*   **Categorias de Problema (Slide 13):** Recursos.
*   **Passos para Reproduzir:**
    1.  Na Airflow UI, ative o DAG `problem_resource_intensive_dag`.
    2.  Clique em `Trigger DAG`.
    3.  Observe o status da tarefa. Ela pode ficar `running` por muito tempo e, em seguida, falhar.
*   **Diagnóstico e Pistas:**
    *   **Logs da tarefa (UI ou `astro dev logs`):** Procure por mensagens como `Killed`, `SIGKILL`, ou informações sobre uso de memória excessivo. Muitas vezes, não há um `Traceback` Python claro, apenas uma indicação de que o processo foi encerrado pelo sistema.
    *   **Observação de recursos do Docker Desktop:** Monitore o uso de memória/CPU do Docker Desktop enquanto a tarefa roda.
*   **Solução (Discussão):**
    *   Este problema não tem uma "correção de código" simples, mas sim uma discussão sobre:
        *   **Otimização do Código:** A tarefa está processando dados de forma ineficiente? Há maneiras de reduzir o consumo de memória (ex: processar em chunks)?
        *   **Configuração de Recursos:** O worker do Airflow tem memória e CPU suficientes para a carga de trabalho? Isso envolve ajustar limites no Docker/Kubernetes.
        *   **Escala:** Usar operadores mais eficientes para grandes volumes de dados (ex: operadores Spark, ferramentas específicas para cloud).

#### Problema 5: Erro de Conexão Externa (`problem_external_connection_dag`)

*   **Descrição:** Este DAG tenta conectar a uma API e a um banco de dados usando endereços que *não existem* ou portas erradas. Isso simula falhas comuns de conectividade de rede ou credenciais/configurações incorretas.
*   **Categorias de Problema (Slide 13):** Conexão Externa.
*   **Passos para Reproduzir:**
    1.  Na Airflow UI, ative o DAG `problem_external_connection_dag`.
    2.  Clique em `Trigger DAG`.
    3.  Ambas as tarefas (`test_non_existent_api_connection` e `test_non_existent_db_connection`) falharão.
*   **Diagnóstico e Pistas:**
    *   **Logs da tarefa (UI ou `astro dev logs`):** Procure por `requests.exceptions.ConnectionError`, `socket.timeout`, `ConnectionRefusedError` ou `requests.exceptions.Timeout`. As mensagens de erro serão bem explícitas sobre o problema de rede/conexão.
    *   A mensagem de erro dirá o host/IP e a porta que estão sendo tentados.
*   **Solução (Discussão):**
    *   Assim como os problemas de recursos, este não é um erro para ser corrigido no código da DAG, a menos que as credenciais estivessem embutidas (o que não é uma boa prática!). **O que deveríamos investigar para resolver problemas de conexão externa?**
        *   Verificar Conectividade de Rede: Pingar o host, verificar firewalls.
        *   Configuração de Airflow Connections: As credenciais e o hostname/porta estão corretos na `Airflow Connection` (se a tarefa usasse uma)?
        *   Variáveis de Ambiente: Se o endpoint/credenciais vêm de variáveis de ambiente, elas estão corretas?

## 6. Comandos Úteis do Astro CLI

Aqui estão alguns comandos do Astro CLI que serão seus melhores amigos durante o desenvolvimento e o debugging:

*   **`astro dev start`**: Inicia seu ambiente Airflow local.
*   **`astro dev stop`**: Para seu ambiente Airflow local.
*   **`astro dev restart`**: Reinicia todos os componentes do seu ambiente.
*   **`astro dev kill`**: Força a parada e remoção de todos os contêineres do seu ambiente local. Use com cautela.
*   **`astro dev logs [--follow]`**: Exibe os logs de todos os serviços do seu ambiente Airflow. Use `--follow` para ver os logs em tempo real.
*   **`astro dev bash`**: Abre um shell Bash dentro do contêiner do `scheduler` do Airflow, permitindo que você execute comandos como se estivesse dentro do ambiente Airflow.
*   **`astro dev run airflow dags test <dag_id> <execution_date>` (Slide 09)**: Simula a execução de uma DAG para uma data específica, exibindo os logs e saídas no seu terminal. Ótimo para testes rápidos.
    *   Exemplo: `astro dev run airflow dags test problem_config_and_logic_dag 2023-01-01`
*   **`astro dev run airflow tasks test <dag_id> <task_id> <execution_date>` (Slide 10)**: Simula a execução de uma única tarefa de uma DAG de forma isolada, sem o scheduler. Essencial para depurar o código de uma tarefa específica.
    *   Exemplo: `astro dev run airflow tasks test problem_config_and_logic_dag fetch_initial_data 2023-01-01`
*   **`astro dev run airflow dags parse /usr/local/airflow/dags/<nome_do_arquivo_dag>.py` (Slide 10)**: Valida a sintaxe e o processo de importação de uma DAG, identificando erros antes que o scheduler tente carregá-la.
    *   Exemplo: `astro dev run airflow dags parse /usr/local/airflow/dags/problem_dag_parsing_error.py`

## 7. Recursos Adicionais

*   **Documentação Oficial do Apache Airflow:** [https://airflow.apache.org/docs/apache-airflow/stable/](https://airflow.apache.org/docs/apache-airflow/stable/) 
*   **Documentação Oficial do Astro CLI:** [https://docs.astronomer.io/astro/cli/overview](https://docs.astronomer.io/astro/cli/overview) 
*   **Artigos sobre Debugging Airflow:** Procure por "Airflow debugging best practices" ou "troubleshooting Airflow DAGs" em blogs como Astronomer, DataCamp, ou Medium.

## 8. Contribuição (Opcional)

Sinta-se à vontade para sugerir melhorias neste case, adicionar novos cenários de problemas ou aprimorar as explicações. Abra uma `Iss