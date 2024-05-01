<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body> 
  <h1>Internet das Coisas</h1>
  <h2>Como Executar o Projeto</h2> 
    <p>Siga os seguintes passos para a execução do projeto:</p>
    <ul>
      <li>baixe o repositório: </li>
      <li>abra os arquivos <strong>'cliente.py'</strong> e <strong>'dispositivo.py'</strong> e subtitua o endereço ip pelo da sua máquina</li>
      <li>execute o seguinte comando com o terminal nas pastas Cliente, Dispositivo e Broker: <strong>'docker build -t nome_do_arquivo .'</strong></li>
      <li>digite <strong>'docker images'</strong> para ver se as imagens docker foram criadas com sucesso</li>
      <li>por fim, execute o programa usando o comando <strong>'docker run --network='host' -it nome_da_imagem'</strong> para executar as três imagens criadas</li>
   </ul>
  <p>tendo feito isso, é possível fazer solicitações por meio do cliente via CLI pedindo para que forneça a temperatura, desligue ou ligue um determinado dispositivo.</p>
</body>
</html>
