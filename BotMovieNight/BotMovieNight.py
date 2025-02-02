import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import re
import time
import string
import urllib.request
import json
import objectpath
import math
from youtubesearchpython import VideosSearch
from datetime import datetime

lock = False

load_dotenv()

score_emote = [":tomato:", "<:imdb:1326272649504100454>", "<:metacritic:1326272970137534566>"]
genre_customs = {
    "Action": ":bomb:",
    "Adventure": ":kite:",
    "Animation": ":clown:",
    "Anime": ":ogre:",
    "Comedy": ":rofl:",
    "Crime": ":spy:",
    "Documentary": ":exploding_head:",
    "Drama": ":performing_arts:",
    "Family": ":breast_feeding:",
    "Fantasy": ":man_mage:",
    "Game Show": ":slot_machine:",
    "Horror": ":skull_crossbones:",
    "Lifestyle": ":man_in_lotus_position:",
    "Music": ":guitar:",
    "Musical": ":shit:",
    "Mystery": ":face_with_monocle:",
    "Reality TV": ":face_with_symbols_over_mouth:",
    "Romance": ":couple_ww:",
    "Sci-Fi": ":alien:",
    "Seasonal": ":jack_o_lantern:",
    "Short": ":pushpin:",
    "Sport": ":football:",
    "Thriller": ":fearful:",
    "Western": ":cowboy:",
}

genre_emote = {
    "Action": ":bomb:",
    "Adventure": ":kite:",
    "Animation": ":clown:",
    "Anime": ":ogre:",
    "Comedy": ":rofl:",
    "Crime": ":spy:",
    "Documentary": ":exploding_head:",
    "Drama": ":performing_arts:",
    "Family": ":breast_feeding:",
    "Fantasy": ":man_mage:",
    "Game Show": ":slot_machine:",
    "Horror": ":skull_crossbones:",
    "Lifestyle": ":man_in_lotus_position:",
    "Music": ":guitar:",
    "Musical": ":shit:",
    "Mystery": ":face_with_monocle:",
    "Reality TV": ":face_with_symbols_over_mouth:",
    "Romance": ":couple_ww:",
    "Sci-Fi": ":alien:",
    "Seasonal": ":jack_o_lantern:",
    "Short": ":pushpin:",
    "Sport": ":football:",
    "Thriller": ":fearful:",
    "Western": ":cowboy:",
}
char_length = {
    3.5 : ["W","M","m"],
    3.25 : ["w"],
    3 : ["A","G","H","N","O","Q","U","D","C"],
    2.75 : ["K","R","P","B","V","X","Y",],
    2.5 : ["L","Z","E","F","S","T","b","q","p"],
    2.25 : ["J","n","o","c","u","h","d","a","e","g","k","u"],
    2.1 : ["v","x","y","s"],
    2 : ["z"],
    1.8 : ["t","r"],
    1.5 : ["f"],
    1 : ["I","i","j","l"," ",":"]
}

genre_weight = {
    "Action": 5,
    "Adventure": 2,
    "Animation": 9,
    "Anime": 10,
    "Comedy": 5,
    "Crime": 5,
    "Documentary": 8,
    "Drama": 4,
    "Family": 4,
    "Fantasy": 3,
    "GameShow":9,
    "Horror": 7,
    "Lifestyle": 7,
    "Music": 8,
    "Musical": 10,
    "Mystery": 3,
    "RealityTV": 10,
    "Romance": 7,
    "Sci-Fi": 2,
    "Seasonal": 1,
    "Short": 1,
    "Sport": 3,
    "Thriller": 5,
    "Western": 1
}

def score_it(movie):
    score = int("0")
    for i in movie:
        for points, char in char_length.items():
             if i in char:
                score = score + points
    score = math.ceil(score)
    return score

def genre_ranking(genres_feed):
    numgenres = []
    for genre in genres_feed:
        for k, v in genre_weight.items():
            if k == genre:
                numgenre = f"{v}{genre}"
                numgenres.append(numgenre)
    genres_feed = []
    numgenres.sort()
    for i in numgenres:
        genres_feed.append(re.sub(r'\d+', '', i))
    print(genres_feed)
    return genres_feed

def convert_to_text(text):
  table = str.maketrans('', '', string.punctuation)
  return text.translate(table)

def retrieve_ratings(movie):
    title_search = movie.replace(" ", "_")
    ##YOU NEED TO POPULATE YOUR OWN APIKEY. Please go to omdbapi.com for details
    live_out = urllib.request.urlopen(f"http://www.omdbapi.com/?apikey=KEY-GOES-HERE&t={title_search}").read()
    json_out = json.loads(live_out)
    jsonnn_tree = objectpath.Tree(json_out["Ratings"])
    result_tuple = tuple(jsonnn_tree.execute('$..Value')) 
    for rating in result_tuple:
        if "%" in rating:
            rt_rating = rating
        if "/100" in rating:
            meta_rating = rating
        if "/10" in rating and not "100" in rating:
            imdb_rating = rating
    if 'imdb_rating' in locals():
        print(f"IMDB Rating: {imdb_rating}")
    else:
        imdb_rating = "NULL"
    if 'rt_rating' in locals():
        print(f"Rottem Tomatoes Rating: {rt_rating}")
    else:
        rt_rating = "NULL"
    if 'meta_rating' in locals():
        print(f"Metacritic Rating: {meta_rating}")
    else:
        meta_rating = "NULL"
    if json_out["Genre"]:
        genres_feed = json_out["Genre"]
    if "Genre" in json_out:
        genres_feed = json_out["Genre"].split(",")
        print(genres_feed)
        genres = [genre.strip() for genre in genres_feed]
        genres_feed = genre_ranking(genres_feed)
        genre_list = ""
        for genre in genres:
            if genre in genre_emote.keys():
                print(genre_emote[genre])
                genre_list = genre_list + genre_emote[genre]
            else:
                genre_list = genre_list + ":bucket:"
        print(genre_list)
    else:
        genre_list = "NULL"
    return rt_rating, meta_rating, imdb_rating, genre_list

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} READY TO MOVIE!')

@bot.command(name='shutdown')
async def shutdown(ctx):
    #in this case, you want an admin user-id here
    if ctx.message.author.id == ADMIN-USER-ID-HERE:
        reaction = "✅"
        await ctx.message.add_reaction(reaction)
        exit()
    else:
        fail = "❌"
        await ctx.message.add_reaction(fail)

@bot.command(name='backup')
async def backup(ctx):
    #in this case, you want an admin user-id here
    if ctx.message.author.id == ADMIN-USER-ID-HERE:
        backup_files = ["BotMovieNight.py", "bad_movies.txt", "good_movies.txt"]
        now = datetime.now()
        bu_time = now.strftime("backup-%Y-%m-%d")
        os.system(f'mkdir {bu_time}')
        for file in backup_files:
            os.system(f'cp {file} {bu_time}')
        print(f"Backed up to {bu_time}")
        reaction = "✅"
        await ctx.message.add_reaction(reaction)
    else:
        fail = "❌"
        await ctx.message.add_reaction(fail)


@bot.command(name='guide')
async def guide(ctx):
    response_string = """
**Misc Commands**
**Details**
!details $movie
Example: !details Men In Black

**Guide**
!guide

**Movie Management**
First, pick which direction you want to go - bad or good:
bad = Bad movies
good = Good movies
(duh)

For each selection, you have 4 choices:
1. add
2. list
3. remove
4. vote

Structure:
!type call movie

**Adding**
Example: !bad add Thankskilling 2: Electric Boogaloo

☑️ = Movie's in the list already
⏳ = Ratings in-progress (Removed when done)
✅ = Moved added

**Removing**
Example: !bad remove Joker: Folie A Deux

✅ = Movie removed
❌ = Movie was not in the list

**Listing**
Example: !bad list

This just spits out a text file. Expand it to see everything :)

**Voting**
Examples: 
!good vote
!bad vote 4


If a number is passed with 'vote', that's the number of people voting. Each person is expected to vote twice, with two finalist movies. Without a number, the number of people in #bad-movie-night is selected to determine the movie count.

Movies are randomly grabbed from their list and assigned numbers. Reacting with a movie's number votes it out. Voted-out movies are spoiler tagged, so if you reveal one, you just need to click a different channel and come back.

Movies have 3 potential ratings:
Rotten Tomatoes
IMDB Score
Metacritic Rating

Genre's are listed by emojis (:yay:):
:bomb:Action             :kite:Adventure
:clown:Animation      :ogre:Anime
:rofl:Comedy          :spy:Crime
:exploding_head:Documentary:performing_arts:Drama
:breast_feeding:Family             :man_mage:Fantasy
:slot_machine:GameShow    :skull_crossbones:Horror
:man_in_lotus_position:Lifestyle         :guitar:Music
:shit:Musical          :face_with_monocle:Mystery
:face_with_symbols_over_mouth:RealityTV      :couple_ww:Romance
:alien:Sci-Fi             :jack_o_lantern:Seasonal
:pushpin:Short             :football:Sport
:fearful:Thriller          :cowboy:Western

Once there are two movies left, voting is locked 🔒. Once locked, no more votes can be cast.
"""
    reaction = "✅"
    await ctx.message.add_reaction(reaction)
    user = ctx.author
    await user.send(response_string)


def get_first_youtube_result(search_query):
    videos_search = VideosSearch(search_query, limit=1)
    result = videos_search.result()
    return result['result'][0]


@bot.command(name='details')
async def shutdown(ctx, *extra):
    extra = str(extra)
    title_search = extra.replace(" ", "_")
    live_out = urllib.request.urlopen(f"http://www.omdbapi.com/?apikey=YOUR-API-KEY-HERE&t={title_search}&plot=full").read()
    json_out = json.loads(live_out)
    reaction = "✅"
    await ctx.message.add_reaction(reaction)
    json_parse = objectpath.Tree(json_out)
    title = json_parse.execute('$.Title')
    year = json_parse.execute('$.Year')
    rating = json_parse.execute('$.Rated')
    runtime = json_parse.execute('$.Runtime')
    genres = json_parse.execute('$.Genre')
    plot = json_parse.execute('$.Plot')
    language = json_parse.execute('$.Language')
    search_query = "trailer " + title + year
    try:
        trailer_get = get_first_youtube_result(search_query)
        trailer = trailer_get['link']
    except Exception as e:
        print("An error occurred:", e)
        trailer = "Not Available"
    response = f"""
**Title**: {title}
**Year**: {year}
**Language**: {language}
**Rated**: {rating}
**Runtime**: {runtime}
**Genre**: {genres}
**Trailer** {trailer}

**Plot**:
{plot}
    """
    await ctx.send(response)
@bot.command(name='bad')
async def bad_choices(ctx, option, *extra):
    option_index = ["add", "list", "remove", "vote"]
    selector = option_index.index(option)
    if lock == True:i
        #implement channel-based restricted access
        if ctx.channel.id != CHANNEL-ID-RAW
            await ctx.send("Sorry boss, I don't work here. Go to LINK-YOUR-CHANNEL-HERE")
            return
    ##Tree for decisions
    if selector == 0:
        extra = str(extra)
        extra = convert_to_text(extra.title())
        with open("bad_movies.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if extra.replace(":", " ") in line:
                    reaction_done = ["☑️"]
                    await ctx.message.add_reaction(reaction_done)
                    return
        pending = "⏳"
        await ctx.message.add_reaction(pending)
        try:
            rt_rating, meta_rating, imdb_rating, genre_list = retrieve_ratings(movie=extra)
            print("Ratings retrieved")
            extra = extra + " --- "
            if "NULL" not in rt_rating:
                extra = extra + score_emote[0] + rt_rating
            if "NULL" not in imdb_rating:
                extra = extra + score_emote[1] + imdb_rating
            if "NULL" not in meta_rating:
                extra = extra + score_emote[2] + meta_rating
            if "NULL" not in genre_list:
                extra = extra + " Genre:" + genre_list
            print(extra)
        except Exception as e:
            print("An error occurred:", e)
        await ctx.message.remove_reaction(pending, bot.user)
        with open("bad_movies.txt", "r+") as file:
            lines = [line.rstrip("\n") for line in file]
            file.write(extra + "\n")
            reaction_done = "✅"
            await ctx.message.add_reaction(reaction_done)
            file.close()
    elif selector == 1:
        with open("bad_movies.txt", "rb") as file:
            await ctx.send("Bad Movie List:", file=discord.File(file, "bad_movies.txt"))
        file.close()
    elif selector == 2:
        #Remove
        extra = str(extra)
        extra = convert_to_text(extra.title())
        try:
            with open("bad_movies.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if extra not in line.strip('\n'):
                        file.write(line)
                    if extra in line.strip('\n'):
                        call_fail = False
                file.truncate()
                file.close()
                reaction_done = "✅"
                await ctx.message.add_reaction(reaction_done)
        except:
            failed = "❌"
            await ctx.message.add_reaction(failed)
    elif selector == 3:
        #Vote process
        extra = str(extra)
        extra = convert_to_text(extra)
        movies_list_bad = []
        with open("bad_movies.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                movies_list_bad.append(line)
            file.close
        movie_count = len(movies_list_bad)
        print(f"Total Movies =")
        bad_list = movies_list_bad
        #Determine how many movies to list in vote
        #Extra is the user count, so 4x users would mean 8x movies + 2,
        #OR 2 votes per person, and a final 50:50
        if extra:
            print(f"Detected {extra} for users")
            if movie_count >= 8:
                to_watch = int(extra.strip("',")) * 2 + 2
                if movie_count < to_watch:
                    to_watch = 8
            list_method = "User-Defined"
        elif not extra:
            #User didn't define member count, retrieve
            #Define your channel ID here
            bad_movie_night = bot.get_channel(CHANNEL-ID-RAW)
            to_watch = len(bad_movie_night.members) * 2 + 2
            list_method = "Member-Determined"
        else:
            if len(movies_list_bad) >= 8:
                to_watch = 8
            else:
                to_watch = len(movies_list_bad)
            list_method = "Default"
        if to_watch > 10:
            to_watch = 10
        print(f"To-Watch determined: {to_watch}")
        movies_grabbed = random.sample(bad_list, k=to_watch)
        preamble = f""" \n
**Calculated {to_watch} movies tonight!**
List Generation Method: {list_method}\n\n
**Commence Voting:**
"""
        list_compiled = ""
        #Indexer just starts a count at 0 to enumerate options
        indexer = 0
        max_spacer = []
        spacer_diff = 0
        for movie in movies_grabbed:
            spacer = str(re.search(r"(.*) ---", movie).group(0).rstrip("---"))
            movie_ass = str(re.search(r" ---(.*)", movie).group(0).strip(" ---"))
            spacer_length = int(len(spacer))
            if spacer_length > spacer_diff:
                spacer_diff = spacer_length
                if spacer not in max_spacer:
                    max_spacer.clear()
                    max_spacer.append(spacer)
        max_spacer = str(max_spacer[0])
        max_score = int("0")
        for i in max_spacer[0]:
            for points, char in char_length.items():
                 if i in char:
                    max_score = max_score + points
        max_score = score_it(max_spacer)
        for movie in movies_grabbed:
            spacer = str(re.search(r"(.*) ---", movie).group(0).rstrip("---"))
            movie_ass = str(re.search(r" ---(.*)", movie).group(0))
            if spacer in max_spacer:
                movies_grabbed.insert(0, movies_grabbed.pop(movies_grabbed.index(movie)))
            score = score_it(spacer)
            score_diff = max_score - score
            for i in range(0, score_diff):
                spacer = spacer + " "
            indexer = indexer + 1
            movie = f"{indexer} - {spacer}{movie_ass} \n"
            #movie = f"{indexer} - {movie}\n"
            list_compiled = str(list_compiled) + movie

        ##THIS IS THE BACKUP for movie in movies_grabbed:
        ##THIS IS THE BACKUP     indexer = indexer + 1
        ##THIS IS THE BACKUP     movie = f"{indexer} - {movie}"
        ##THIS IS THE BACKUP     list_compiled = str(list_compiled) + movie
        output = preamble + str(list_compiled)
        #output = output + str("\n")
        response = output

        vote_window = await ctx.send(response)
        vote_num = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        for i in range(to_watch):
            time.sleep(0.25)
            await vote_window.add_reaction(vote_num[i])
        while True:
            def check(reaction, user):
                return user != vote_window.author
            reaction = await bot.wait_for("reaction_add", check=check)
            parser = re.search(r".*<Reaction emoji='(.*)' me.*", str(reaction))
            reaction = parser.group(1)
            striker = vote_num.index(reaction) + 1
            regex = striker
            aggregator = ""
            match = re.search(f".*{regex} - .*", list_compiled)
            for line in list_compiled.split("\n"):
                if match.group(0) in line:
                    if "||" in line:
                        line = line.strip("||").strip("     ") + "\n"
                    else:
                        line = "||     " + line + "||\n"
                    aggregator = aggregator + line
                else:
                    line = line + "\n"
                    aggregator = aggregator + line
                list_compiled = aggregator
            output = preamble + str(aggregator)
            await vote_window.edit(content=output)
            time.sleep(1)
            if list_compiled.count("\n||") == (list_compiled.count(' - ') - 3):
                print("Stopping here, final 2 determined")
                final_react = "🔒"
                await vote_window.add_reaction(final_react)
                return False
    else:
        debugger_output = """
        You've passed a command that I don't know, or can't understand.
        Available Commands:
        Start with **!bad** or **!good**
        1. add $movie
        2. remove
        3. list
        4. vote
        """
        await ctx.send(debugger_output)

@bot.command(name='good')
async def good_choices(ctx, option, *extra):
    option_index = ["add", "list", "remove", "vote"]
    selector = option_index.index(option)
    if lock == True:
        #Restricted channel access
        if ctx.channel.id != CHANNEL-ID-HERE:
            await ctx.send("Sorry boss, I don't work here. Go to CHANNEL-LINK-HERE")
            return
    ##Tree for decisions
    if selector == 0:
        extra = str(extra)
        extra = convert_to_text(extra.title())
        with open("good_movies.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if extra.replace(":", " ") in line:
                    reaction_done = ["☑️"]
                    await ctx.message.add_reaction(reaction_done)
                    return
        pending = "⏳"
        await ctx.message.add_reaction(pending)
        try:
            rt_rating, meta_rating, imdb_rating, genre_list = retrieve_ratings(movie=extra)
            print("Ratings retrieved")
            extra = extra + " --- "
            if "NULL" not in rt_rating:
                extra = extra + score_emote[0] + rt_rating
            if "NULL" not in imdb_rating:
                extra = extra + score_emote[1] + imdb_rating
            if "NULL" not in meta_rating:
                extra = extra + score_emote[2] + meta_rating
            if "NULL" not in genre_list:
                extra = extra + " Genre:" + genre_list
            print(extra)
        except Exception as e:
            # code to handle the exception
            print("An error occurred:", e)
        await ctx.message.remove_reaction(pending, bot.user)
        with open("good_movies.txt", "r+") as file:
            lines = [line.rstrip("\n") for line in file]
            file.write(extra + "\n")
            reaction_done = "✅"
            await ctx.message.add_reaction(reaction_done)
            file.close()
    elif selector == 1:
        #List
        #preamble = """**BEHOLD! SHITTY. MOVIES.
        #```"""
        with open("good_movies.txt", "rb") as file:
            await ctx.send("good Movie List:", file=discord.File(file, "good_movies.txt"))
        file.close()
        #output = str("")
        #for movie in movies_list_good:
        #    output = output + str(movie.title()) + "\n"
        #outstring = str(f"{preamble} \n {output} \n ```")
        #await ctx.send(output)
    elif selector == 2:
        #Remove
        extra = str(extra)
        extra = convert_to_text(extra.title())
        try:
            with open("good_movies.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    #if line.strip('\n') != extra:
                    if extra not in line.strip('\n'):
                        file.write(line)
                    #if line.strip('\n') == extra:
                    if extra in line.strip('\n'):
                        call_fail = False
                file.truncate()
                file.close()
                reaction_done = "✅"
                await ctx.message.add_reaction(reaction_done)
                #await ctx.send(f"Removed {extra.title()} from good movie list")
        #if extra in lines:
        #    movies_list_good.remove(extra.title())
        except:
            failed = "❌"
            await ctx.message.add_reaction(failed)
    elif selector == 3:
        #Vote process
        extra = str(extra)
        extra = convert_to_text(extra)
        movies_list_good = []
        with open("good_movies.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                movies_list_good.append(line)
            file.close
        movie_count = len(movies_list_good)
        print(f"Total Movies =")
        good_list = movies_list_good
        #Determine how many movies to list in vote
        #Extra is the user count, so 4x users would mean 8x movies + 2,
        #OR 2 votes per person, and a final 50:50
        if extra:
            print(f"Detected {extra} for users")
            if movie_count >= 8:
                to_watch = int(extra.strip("',")) * 2 + 2
                if movie_count < to_watch:
                    to_watch = 8
            list_method = "User-Defined"
        elif not extra:
            #User didn't define member count, retrieve
            #Define your channel ID here.
            good_movie_night = bot.get_channel(CHANNEL-ID-RAW)
            to_watch = len(good_movie_night.members) * 2 + 2
            list_method = "Member-Determined"
        else:
            if len(movies_list_good) >= 8:
                to_watch = 8
            else:
                to_watch = len(movies_list_good)
            list_method = "Default"
        if to_watch > 10:
            to_watch = 10
        print(f"To-Watch determined: {to_watch}")
        movies_grabbed = random.sample(good_list, k=to_watch)
        preamble = f""" \n
**Calculated {to_watch} movies tonight!**
List Generation Method: {list_method}\n\n
**Commence Voting:**
"""
        list_compiled = ""
        #Indexer just starts a count at 0 to enumerate options
        indexer = 0
        max_spacer = []
        spacer_diff = 0
        for movie in movies_grabbed:
            spacer = str(re.search(r"(.*) ---", movie).group(0).rstrip("---"))
            movie_ass = str(re.search(r" ---(.*)", movie).group(0).strip(" ---"))
            spacer_length = int(len(spacer))
            if spacer_length > spacer_diff:
                spacer_diff = spacer_length
                if spacer not in max_spacer:
                    max_spacer.clear()
                    max_spacer.append(spacer)
        max_spacer = str(max_spacer[0])
        max_score = int("0")
        for i in max_spacer[0]:
            for points, char in char_length.items():
                 if i in char:
                    max_score = max_score + points
        max_score = score_it(max_spacer)
        for movie in movies_grabbed:
            spacer = str(re.search(r"(.*) ---", movie).group(0).rstrip("---"))
            movie_ass = str(re.search(r" ---(.*)", movie).group(0))
            if spacer in max_spacer:
                movies_grabbed.insert(0, movies_grabbed.pop(movies_grabbed.index(movie)))
            score = score_it(spacer)
            score_diff = max_score - score
            for i in range(0, score_diff):
                spacer = spacer + " "
            indexer = indexer + 1
            movie = f"{indexer} - {spacer}{movie_ass} \n"
            #movie = f"{indexer} - {movie}\n"
            list_compiled = str(list_compiled) + movie
        output = preamble + str(list_compiled)
        response = output
        vote_window = await ctx.send(response)
        vote_num = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        for i in range(to_watch):
            time.sleep(0.25)
            await vote_window.add_reaction(vote_num[i])
        while True:
            def check(reaction, user):
                return user != vote_window.author
            reaction = await bot.wait_for("reaction_add", check=check)
            parser = re.search(r".*<Reaction emoji='(.*)' me.*", str(reaction))
            reaction = parser.group(1)
            striker = vote_num.index(reaction) + 1
            regex = striker
            aggregator = ""
            match = re.search(f".*{regex} - .*", list_compiled)
            for line in list_compiled.split("\n"):
                if match.group(0) in line:
                    if "||" in line:
                        line = line.strip("||").strip("     ") + "\n"
                    else:
                        line = "||     " + line + "||\n"
                    aggregator = aggregator + line
                else:
                    line = line + "\n"
                    aggregator = aggregator + line
                list_compiled = aggregator
            output = preamble + str(aggregator)
            await vote_window.edit(content=output)
            time.sleep(1)
            if list_compiled.count("\n||") == (list_compiled.count(' - ') - 3):
                print("Stopping here, final 2 determined")
                final_react = "🔒"
                await vote_window.add_reaction(final_react)
                return False
    else:
        debugger_output = """
        You've passed a command that I don't know, or can't understand.
        Available Commands:
        Start with **!bad** or **!good**
        1. add $movie
        2. remove
        3. list
        4. vote
        """
        await ctx.send(debugger_output)

bot.run(TOKEN)
