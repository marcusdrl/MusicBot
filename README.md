# MusicBot (para DISCORD)
Este é o código de um BOT para trocar URLs do Youtube diretamente do seu canal de voz do discord:
**Atenção! Se for utilizar o código fonte para criar seu bot, fique atento ao path do arquivo 'FFMPEG.exe' (utilizado no arquivo bot_config.py) que é o arquivo utilizado para reproduzir o conteúdo obtido da URL fornecida... então se você não possuir o arquivo, primeiramente terá que fazer o download e depois adicionar o path no código.**
<br>
<br>
**COMANDOS**
<br>
**!play:** toca a url inserida, caso alguma música já esteja tocando, será criada uma playlist com as novas músicas que forem sendo adicionadas

**!pause:** pausa a música atual, se houver música tocando

**!resume:** retorna a música atual, se houver música tocando

**!skip:** troca para a próxima música da playlist, se houver playlist criada

**!stop:** **ATENÇÃO** exclui a playlist que está tocando(se o objetivo não for perder toda a playlist utilize o comando !pause) e kicka o bot da sua sala

<br><br>
PS: não se esqueça de criar seu arquivo .env para adicionar a variável TOKEN (é a senha do seu bot)
