import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from discord.utils import get
import requests


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ydl = YoutubeDL(ytdlopts)


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []

    @commands.command()
    async def play(self, ctx, argument):
        r = requests.get(argument)
        if ' ' not in argument and "Vídeo indisponível" not in r.text:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            # channel = get(ctx.guild.voice_channels, name=ctx.author.voice)
            channel_voice = ctx.author.voice

            def checar_lista(lista):
                if lista:
                    url_musica = lista[0]
                    audio_2 = discord.FFmpegPCMAudio(
                        executable="C:\\Users\\Marcus Vinicius\\Desktop\\ffmpeg\\bin\\ffmpeg.exe",
                        source=url_musica, **ffmpeg_options)
                    lista.pop(0)
                    voice.play(audio_2, after=lambda e: checar_lista(lista))
                    voice.is_playing()
                else:
                    pass

            if not voice:
                await channel_voice.channel.connect()
            elif voice.is_playing() or voice.is_paused():
                # quando o bot já estiver tocando uma música, insere a nova url na playlist do bot e notifica o usuário
                info = ydl.extract_info(argument, download=False)
                url = info['formats'][0]['url']
                self.players.append(url)
                await ctx.channel.send(f"```Uma música já está sendo tocada. {info['title']} será adicionada à lista```")

            # Declarar voice novamente para que o python reconheca que é VoiceClient, se não fica dando error
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if not voice.is_playing() and not voice.is_paused():
                # conecta ao canal e extrai os dados da url inserida
                # voice = get(self.bot.voice_clients, guild=ctx.guild)
                info = ydl.extract_info(argument, download=False)

                # extrai o valor da url e inicia o player
                url = info['formats'][0]['url']
                self.players.append(url)
                await ctx.channel.send(f"```Tocando agora: {info['title']}```")
                self.players.pop(0)
                audio = discord.FFmpegPCMAudio(
                    executable="C:\\Users\\Marcus Vinicius\\Desktop\\ffmpeg\\bin\\ffmpeg.exe",
                    source=url, **ffmpeg_options)
                voice.play(audio, after=lambda e: checar_lista(self.players))
                voice.is_playing()
        else:
            await ctx.channel.send(f"```\nFormato e/ou URL do youtube inválidos!"
                                   f"\nFormato correto: !play <YOUTUBE URL>"
                                   f"\nOu verificar se o link não está corrompido\n```")

    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.channel.send(f"```A playlist foi pausada```")
            voice.pause()
        else:
            await ctx.channel.send(f"```Não existem músicas sendo tocadas no momento```")

    @commands.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            await ctx.channel.send(f"```A playlist voltou a tocar```")
            voice.resume()
        else:
            await ctx.channel.send(f"```Não existem músicas sendo tocadas no momento```")

    @commands.command()
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        def checar_lista(lista):
            if lista:
                url_musica_skip = self.players[0]
                audio_skip = discord.FFmpegPCMAudio(
                    executable="C:\\Users\\Marcus Vinicius\\Desktop\\ffmpeg\\bin\\ffmpeg.exe",
                    source=url_musica_skip, **ffmpeg_options)
                lista.pop(0)
                voice.play(audio_skip, after=lambda e: checar_lista(lista))
                voice.is_playing()
            else:
                pass

        if self.players and voice.is_playing():
            voice.pause()
            url_musica = self.players[0]
            audio_2 = discord.FFmpegPCMAudio(
                executable="C:\\Users\\Marcus Vinicius\\Desktop\\ffmpeg\\bin\\ffmpeg.exe",
                source=url_musica, **ffmpeg_options)
            self.players.pop(0)
            voice.play(audio_2, after=lambda e: checar_lista(self.players))
            voice.is_playing()
        elif voice.is_playing and not self.players:
            await ctx.channel.send(f"```Não existem próximas músicas na fila para serem tocadas. "
                                   f"Adicione músicas com o comando !play```")
        elif voice.is_paused() and self.players:
            url_musica = self.players[0]
            audio_2 = discord.FFmpegPCMAudio(
                executable="C:\\Users\\Marcus Vinicius\\Desktop\\ffmpeg\\bin\\ffmpeg.exe",
                source=url_musica, **ffmpeg_options)
            self.players.pop(0)
            voice.play(audio_2, after=lambda e: checar_lista(self.players))
            voice.is_playing()
        elif voice.is_paused() and not self.players:
            await ctx.channel.send(f"```Não existem próximas músicas na fila para serem tocadas. "
                                   f"Adicione músicas com o comando !play```")
        else:
            await ctx.channel.send(f"```Não existem próximas músicas na fila para serem tocadas. ")

    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        voice.pause()
        self.players.clear()
        await ctx.guild.voice_client.disconnect()

    @commands.command()
    async def comandos(self, ctx):
        await ctx.channel.send(f"``` ** COMANDOS WOLHAIKSONG BOT (SOMENTE PARA URL's do YOUTUBE)** "
                               f"\n\n!play: toca a url inserida, caso alguma música já esteja tocando, "
                               f"será criada uma playlist com as novas músicas que forem sendo adicionadas"
                               f"\n\n!pause: pausa a música atual, se houver música tocando"
                               f"\n\n!resume: retorna a música atual, se houver música tocando"
                               f"\n\n!skip: troca para a próxima música da playlist, se houver playlist criada"
                               f"\n\n!stop: **ATENÇÃO** exclui a playlist que está tocando(se o objetivo não for perder "
                               f"toda a playlist utilize o comando !pause) e kicka o bot da sua sala\n\n```")


def setup(bot):
    bot.add_cog(MainCog(bot))
