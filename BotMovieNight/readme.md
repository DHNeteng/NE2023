I built this bot for a single purpose:

I needed a way to track multiple lists of movies to watch with friends. Typically, we watch a
bad movie and a good movie one night a week. Those movies used to be just be a series of
discord messages, which I would aggregate throughout the week, then push the list, and
we would vote movies out. Once we got to two movies, we would vote for which we wanted to watch.

As this is now on GH, it's public - so anyone can use this. I don't know of anyone that
goes through this same process as I do, but maybe the methods used to get these lists managed
could be helpful for someone else.

I'm making an assumption that if you're retrieving and using this bot, you have some working knowledge of python, so you can tinker with this as-needed. My code is sloppy, some is very rudamentary or basic, but it works. There's some unused/planned features included within this (like stack-ranked genre emojis to trim output size).

**Functionality:**
* !guide - Bot DM's user a usage guide
* !$type [add|remove|list|vote] - Movie management, inventory, and voting
* !details - Lookup a movie. Provides language, runtime, plot, year, attempts to retrieve a trailer via YT
* !backup (admin only) - Backs up the movie lists into a new (unix-based) directory
* !shutdown (admin only) - Shuts the bot down via discord command. Niche use for sure.

**Requirements (Lines approximated as doc changes made):**
* omdbapi key [BotMovieNight.py#L316,L144]- Follow the guide to get your own key here https://www.omdbapi.com
* Discord bot token [.env#L2- 
* File structure - In the published state, this bot only needs good_movies.txt and bad_movies.txt - they follow the same args and structure. Creating the empty file may/may not be required, but it'll probably same some troubleshooting if you create the file itself.
* Personal Discord user ID [BotMoveNight.py#L198,L209] - This is effectively your 'admin', I could have made this a list, but I'm lazy, this was fast, and I don't care about optimization as this is a very personal bot to me :P
* Dedicated Movie Night Channel [BotMovieNight.py#L354,L556] - This is specific to generating a pre-determined list size to vote against, and nothing else. Add your discord channel ID here. You can also remove these if you want to just do the defaulted user-count, or manually define it.
* IMDB/MetaCritic Emojis [BotMovieNight.py#L20] - Emojis needed to actually show IMDB and MetaCritic emojis, else you'll fail to retrieve the emoji ID's. You can also just change this to an emoji you prefer

**Hey, wtf does char_length actually do?**
The discord font's weird. It's got awkward spacing, and I couldn't render these in python to measure pixel-width of each character (thanks Discord for making it impossible to download the font :P). So I went through every character and determined how many "spaces" wide each character is. As PrettyTable or some other formatting mechanism would very quickly exceeed the 2000 character limit of an individual discord message, alignment by manually adding spaces was the only viable means of ensuring a "pretty" vote window would be provided.