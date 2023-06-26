"""
This cog holds and handles all the minor "fun" commands
Generally, they do silly things and can be bulked together.
"""
import json
from random import choice
from io import BytesIO
from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands


requests.packages.urllib3.disable_warnings()


class Fun(commands.Cog):
    """
    # TODO: Refactor this messy shit. Put each one into it's own cog.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def hello(self, ctx):
        """
        A simple hello.
        """
        await ctx.respond("Don't talk to me, I am being developed!")

    @commands.slash_command()
    async def taunt(self, ctx, person):
        """
        Scrapes a webpage for shakespearean taunts.
        """
        taunt = BeautifulSoup(
            requests.get(
                "https://fungenerators.com/random/insult/shakespeare/"
                , timeout=5
            ).content,
            "html.parser",
        ).find("h2")
        await ctx.respond(f"{person}, {taunt.text}")

    @commands.slash_command()
    async def catfact(self, ctx):
        """
        Sends a cat fact using an API
        """
        await ctx.respond(
            json.loads(
                requests.get(
                    "https://catfact.ninja/fact"
                    , timeout=5).text)["fact"]
        )

    @commands.slash_command()
    async def dogfact(self, ctx):
        """
        Sends a dog fact using an API
        """
        await ctx.respond(
            json.loads(
                requests.get(
                    "https://dog-api.kinduff.com/api/facts"
                    , timeout=5).text)["facts"][0]
        )

    @commands.slash_command()
    async def pugfact(self, ctx):
        """
        Sends a pug fact using an API
        """
        await ctx.respond(
            BeautifulSoup(
                requests.get(
                    "https://fungenerators.com/random/facts/dogs/pug"
                    , timeout=5).content
                , "html.parser")
            .find("h2")
            .text[:-15]
        )

    @commands.slash_command()
    async def catpic(self, ctx):
        """
        Sends a cat pic using an API
        """
        await ctx.respond(
            file=discord.File(
                fp=BytesIO(
                    requests.get(
                        "https://cataas.com/cat"
                        , timeout=5).content),
                filename="cat.png",
            )
        )

    @commands.slash_command()
    async def dogpic(self, ctx, *, breed=None):
        """
        Sends a dog pic using an API
        """
        embed = discord.Embed(
            title="Dog Pic!", description="A lovely dog pic just for you."
        )
        if breed is None:
            link = requests.get(
                "https://dog.ceo/api/breeds/image/random"
                , timeout=5).json()["message"]
        elif breed is not None:
            link = requests.get(
                f"https://dog.ceo/api/breed/{breed}/images/random"
                , timeout=5).json()["message"]
        embed.set_image(url=link)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def joke(self, ctx):
        """
        Sends a joke using an API
        """
        await ctx.respond(
            json.loads(
                requests.get(
                    "https://geek-jokes.sameerkumar.website/api?format=json"
                    , timeout=5).text)["joke"])

    @commands.slash_command()
    async def quote(self, ctx):
        """
        Sends a quote using an API
        """
        quote = json.loads(
            requests.get(
                "https://zenquotes.io/api/random"
                , timeout=5).text)[0]
        await ctx.respond((quote["q"] + "\n- " + quote["a"]))

    @commands.slash_command()
    async def fakeperson(self, ctx):
        """
        Sends a fake person using an API
        """
        person = json.loads(
            requests.get(
                "https://randomuser.me/api/"
                , timeout=5).text)["results"]
        name = f'Name: {person[0]["name"]["title"]}' \
               f' {person[0]["name"]["first"]}' \
               f' {person[0]["name"]["last"]}'

        hometown = f'Hometown:' \
                   f' {person[0]["location"]["city"]},' \
                   f' {person[0]["location"]["country"]}'
        age = f'Age: {person[0]["dob"]["age"]} Years old'
        await ctx.respond(
            "You have requested a fake person:\n\n"
            + name
            + "\n"
            + hometown
            + "\n"
            + age
        )

    @commands.slash_command()
    async def google(self, ctx, question):
        """
        sarcastically googles a question.
        """
        await ctx.respond(
            f"Here, allow me to google that one for you:"
            f"\nhttps://letmegooglethat.com/?q={question.replace(' ', '+')}"
        )

    @commands.slash_command()
    async def pokedex(self, ctx, pokemon):
        """
        Sends pokemon information using an API
        """
        data = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
            , timeout=5)
        if data.status_code == 200:
            data = data.json()
            embed = discord.Embed(
                title=data["name"].title(), color=discord.Color.blue()
            )
            embed.set_thumbnail(url=data["sprites"]["front_default"])
            embed.add_field(name="Stats", value=data["name"].title())
            embed.add_field(name="Weight", value=data["weight"])
            embed.add_field(name="Type", value=data["types"][0]["type"]["name"].title())
            embed.add_field(
                name="Abilities", value=data["abilities"][0]["ability"]["name"]
            )
            await ctx.respond(embed=embed)
        elif data.status_code == 404:
            embed = discord.Embed(title="Uhh oh...", color=discord.Color.blue())
            embed.set_thumbnail(
                url="https://assets.pokemon.com/assets/cms2/img/misc/gus/buttons"
                    "/logo-pokemon-79x45.png"
            )
            embed.add_field(name="Error", value=pokemon.title() + " does not exist!")
            await ctx.respond(embed=embed)

    @commands.slash_command()
    async def rolldice(self, ctx):
        """
        rolls a die.
        """
        await ctx.respond(f"**{ctx.author.name}** rolled a **{choice(range(1, 7))}**")

    @commands.slash_command(aliases=["8ball"])
    async def eightball(self, ctx, question):
        """
        Asks a question to a magic 8-ball
        """
        answer = choice(
            [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs points to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not to tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good",
                "Very doubtful.",
                "Be more polite.",
                "How would i know",
                "100%",
                "Think harder",
                "Sure",
                "In what world will that ever happen",
                "As i see it no.",
                "No doubt about it",
                "Focus",
                "Unfortunately yes",
                "Unfortunately no,",
                "Signs point to no",
            ]
        )
        await ctx.respond(f"Question: {question}\n🎱 - {answer}")

    @commands.slash_command(description="Generates an AI-made image from a prompt.")
    async def drawme(self, ctx, prompt, seed):
        """
        Sends a computer generated image based on a prompt.
        """
        sanetized = prompt.replace(" ", "-")
        gen_url = f"https://api.computerender.com/generate/{sanetized}"
        if seed:
            gen_url = gen_url + f"?seed={seed}"
        embed = embed = discord.Embed.from_dict(
            {"title": prompt, "color": 10848322, "image": {"url": gen_url}}
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.respond(embed=embed)

    @commands.slash_command(description="Gives you something to do.")
    async def imbored(self, ctx):
        """
        Sends a "thing-to-do using an API
        """
        data = requests.get(
            "https://www.boredapi.com/api/activity/"
            , timeout=5).json()
        if data["price"] < 0.5:
            price = "and is not too expensive"
        else:
            price = "and is a bit expensive"
        await ctx.respond(
            f'Im bored too...\nLets do this: {data["activity"]}.'
            f'\nIts {data["type"]} and you could involve '
            f'{str(data["participants"])} people {price}'
        )


def setup(bot):
    """
    Required.
    """
    bot.add_cog(Fun(bot))
