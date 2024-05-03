<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body> 
  <h1>Internet das Coisas</h1>
    <p>Devido aos avanços tecnológicos nas áreas de sitemas embarcados, microeletrônica, comunicação e sensoriamento, o termo Internet das Coisas (<em>Internet of things</em>, IoT) criado por Kevin Ashton, vem sendo muito discutido nos dias atuais frente as possíveis aplicações as mais diversas áreas como saúde, energia, cidades inteligentes, etc.</p>
    <p></p>
    <p>Mediante a isso, esse projeto tem o intuito de realizar a conexão de dispositivos simulados via script em python com uma interface cliente por meio de um sistema de mensageria chamado de broker, sendo utilizados para isso os protocolos de comunicação TCP e UDP para a comunicação dispositivo-broker e uma API em python para realizar a comunicação broker-cliente.</p>
    <h2>Arquiterura do Projeto</h2>
    O projeto funciona da seguinte forma:
        <ol>
            <li>O broker inicializa o servidor TCP, o servidor UDP e a API para poder trocar mensagens com os dispositivos e com os clientes.</li>
            <li>O dispositivo tenta se conectar ao servidor para poder receber mensagens TCP e envia dados UDP ao broker.</li>
            <li>O cliente comunica com a API as solicitações que ela deseja fazer ao broker.</li>
            <br>
            <div align="center">
                <figure>
                    <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/docs/Captura%20de%20tela%202024-04-24%20210107.png" alt="Descrição da Imagem">
                    <br>
                    <figcaption>Arquitetura do Projeto</figcaption>
                </figure>
            </div>
        </ol>
    <h2>Sobre o Projeto</h2>
    <h3>Cliente</h3>
    <p>Segue as funções contidas no <strong>'cliente.py'</strong></p></p>
    <ul>
        <li><strong>obter_lista_de_sensores()</strong>, responsável por consumir a rota da API que guarda dados sobre os dispositivos conectados.</li>
        <li><strong>limpar_terminal()</strong>, responsável por limpar o terminal da interface CLI do cliente.</li>
        <li><strong>menu()</strong>, responsável por mostrar as opções ao usuário e repassar os comandos realizados por ele ao broker.</li>
        <li><strong>main()</strong>, responsável por chamar tudo que vai ser realizado na execução.</li>
    </ul>
    <h3>Dispositivo</h3>
    <p>Segue as funções contidas no <strong>'dispositivo.py'</strong></p>
    <ul>
        <li><strong>gerar_temperatura()</strong>, responsável por gerar temperaturas aleatórias entre 20° e 30°.</li>
        <li><strong>receber_mensagem_tcp()</strong>, responsável por fazer a conexão do dispositivo com o broker para que ele possa receber as mensagens TCP.</li>
        <li><strong>enviar_mensagem_udp()</strong>, responsável por enviar os dados ao broker em UDP.</li>
        <li><strong>entrada()</strong>, responsável por esperar por uma solicitação do usuário via CLI no dispositivo.</li>
        <li><strong>limpar_terminal()</strong>, responsável por limpar a interface CLI do dispositivo.</li>
        <li><strong>main()</strong>, responsável por criar threads para que o dispositivo consiga receber mensagens TCP, enviar mensagens UDP e esperar uma solicitação do usuário via CLI constantemente.</li>
    </ul>
    <h3>Broker</h3>
    <p>Diferente dos demais, o <strong>'broker.py'</strong> guarda a parte referente ao Servidor para lidar com a comunicação com os dispositivos e a parte da API para poder pegar requisições dos clientes e subir dados para que o cliente possa acessá-los</p>
    <ul>
    <h3>Servidor</h3>
            <p>Segue as funções referentes a parte do servidor no <strong>'broker.py'</strong></p>
            <ul>
                <li><strong>broker()</strong>, responsável por iniciar o servidor TCP e aceitar conexões dos dispositivos.</li>
                <li><strong>receber_udp()</strong>, responsável por receber os dados dos dispositivos e manter eles atualizados no dicionário da API.</li>
                <li><strong>tratamento_mensagens()</strong>, responsável por verificar se tem alguma solicitação pendente de um cliente para um dispositivo para repassá-lo ao dispositivo.</li>
                <li><strong>remover_solicitação()</strong>, responsável por remover uma solicitação no dicionário da API.</li>
                <li><strong>obter_lista_solicitações()</strong>, responsável por pegar a lista de dicionários da API.</li>
                <li><strong>enviar_tcp()</strong>, responsável por enviar a mensagem tcp ao dispositivo escolhido.</li>
                <li><strong>delete_cliente()</strong>, responsável por deletar um cliente da lista de clientes.</li>
            </ul>
    <h3>API</h3>
        <p>Segue as funções referentes a parte da API no <strong>'api.py'</strong></p>
        <ul>
            <li><strong>get_sensores()</strong>, responsável por retornar os dados e todos os sensores registrados na sua aplicação.</li>
            <li><strong>get_sensor()</strong>, responsável por retornar os dados de um sensor expecífico registrado na aplicação.</li>
            <li><strong>criar_sensor()</strong>, responsável por criar e registrar um sensor na aplicação.</li>
            <li><strong>atualizar_sensor()</strong>, responsável por atualizar dados de um sensor na aplicação.</li>
            <li><strong>excluir_sensor()</strong>, responsável por remover um sensor da aplicação.</li>
            <li><strong>get_solicitacoes()</strong>, responsável por retornar os dados e todas as solicitações registradas na sua aplicação.</li>
            <li><strong>get_solicitacao()</strong>, responsável por retornar os dados de uma solicitação expecífica registrada na aplicação.</li>
            <li><strong>criar_solicitacao()</strong>, responsável por criar e registrar uma solicitação na aplicação.</li>
            <li><strong>atualizar_solicitacao()</strong>, responsável por atualizar dados de uma solicitação na aplicação.</li>
            <li><strong>excluir_solicitacao()</strong>, responsável por remover uma solicitação da aplicação.</li>
        </ul>
    </ul>
  <h2>Como Executar o Projeto</h2> 
    <p>Siga os seguintes passos para a execução do projeto:</p>
    <ul>
      <li>baixe o repositório: 
          <a href="https://github.com/emersonrlp/MI-de-Redes.git">https://github.com/emersonrlp/MI-de-Redes.git</a>
      </li>
      <li>abra os arquivos <strong>'cliente.py'</strong> e <strong>'dispositivo.py'</strong> em um editor de texto/terminal e subtitua o endereço ip pelo da máquina que vai hospedar o servidor.</li>
      <li>execute o seguinte comando com o terminal nas pastas Cliente, Dispositivo e Broker: <strong>'docker build -t nome_do_arquivo .'</strong></li>
      <li>digite <strong>'docker images'</strong> para ver se as imagens docker foram criadas com sucesso</li>
      <li>por fim, execute o programa usando o comando <strong>'docker run --network='host' -it nome_da_imagem'</strong> para executar as três imagens criadas</li>
   </ul>
  <p>tendo feito isso, é possível fazer solicitações por meio do cliente via CLI pedindo para que forneça a temperatura, desligue ou ligue um determinado dispositivo.</p>    
    <p><strong>Obs.:</strong> é necessário ter o docker instalado na máquina que deseja executar o código.</p>
</body>
</html>
