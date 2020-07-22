# icm-list-appender
Python tool that can append multiple icheckmovies.com lists to create "all editions" type movies lists. It can also trim lists to only include the first x entries of each list (given different versions of a single list), e.g. for creating lists like "top 10 of each year/user" (given different list submissions for a common subject).)

Example uses:

```python -m icm-list-appender -d yearbyyear -e 10```

Have yearly top list files in yearbyyear directory, create an ascending list of all yearly top 10s

```python -m icm-list-appender -d hiddengems -a```

Have multiple editions of a Hidden Gems list in hiddengems directory,
create 'all editions' list that shows current editions, extra movies for previous editions
(and gives info about which list edition a movie is on)
