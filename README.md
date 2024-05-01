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
  <h2>Como Executar o Projeto</h2> 
    <p>Siga os seguintes passos para a execução do projeto:</p>
    <ul>
      <li>baixe o repositório: 
          <a href="https://github.com/emersonrlp/MI-de-Redes.git">https://github.com/emersonrlp/MI-de-Redes.git</a>
      </li>
      <li>abra os arquivos <strong>'cliente.py'</strong> e <strong>'dispositivo.py'</strong> em um editor de texto/terminal e subtitua o endereço ip pelo da sua máquina</li>
      <li>execute o seguinte comando com o terminal nas pastas Cliente, Dispositivo e Broker: <strong>'docker build -t nome_do_arquivo .'</strong></li>
      <li>digite <strong>'docker images'</strong> para ver se as imagens docker foram criadas com sucesso</li>
      <li>por fim, execute o programa usando o comando <strong>'docker run --network='host' -it nome_da_imagem'</strong> para executar as três imagens criadas</li>
   </ul>
  <p>tendo feito isso, é possível fazer solicitações por meio do cliente via CLI pedindo para que forneça a temperatura, desligue ou ligue um determinado dispositivo.</p>
</body>
</html>
