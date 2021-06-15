import os
import discord
import random
import gspread
import string
import json
import asyncio
import DiscordUtils

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from discord.ext import commands
from fuzzywuzzy import process
from dotenv import load_dotenv

from transcripts import load_story
from transcripts import count_lines
from operators import load_archives

load_dotenv()

FAQ = 0
DOCS = 1
COMMANDS = 2
CUTIES = 3
TRUSTED = 4

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'json_files/project_file.json'
SPREADSHEET_ID = '1qnCoJSO5-0a63X-HaZ_3L_p7y6WM0EPWl3v61-Gjn8s'

creds = None
creds = ServiceAccountCredentials.from_json_keyfile_name('json_files/project_file.json', scopes = SCOPES)

sh = gspread.authorize(creds)
sheet = sh.open("Lore")

with open('json_files/operator_table.json', encoding="utf8") as f:
	table = json.load(f)


#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


bot = commands.Bot(command_prefix = '%')
	

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)
    await asyncio.sleep(3)
    await ctx.channel.purge(limit = 2)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command(name = 'commands')
async def commands_list(ctx, *, arg = 'None'):
	worksheet = sheet.get_worksheet(COMMANDS)
	command_string = str(worksheet.col_values(1)).strip('[]')
	command_string = command_string.replace('\'', '')
	command_string = command_string.replace(', ', '\n')
	embedVar = discord.Embed(title = 'Command Documentation', description = command_string, color = 0xe3e3e3)

	if arg == '%stay':
		await ctx.send(embed = embedVar)

	else:
		await ctx.send(embed = embedVar, delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command()
async def doc(ctx, *, arg):
	document = arg
	worksheet = sheet.get_worksheet(DOCS)
	document_list = worksheet.col_values(2)
	stay = False

	if document.endswith(' %stay'):
		document = document.replace(' %stay', '')
		stay = True

	if document.startswith('list'):
		del document_list[0]
		document_string = str(document_list).strip('[]')
		document_string = document_string.replace('\'', '')
		embedVar = discord.Embed(title = 'Use `%doc [document name]` to retrieve the corresponding link.', description = document_string, color = 0xe3e3e3)
		await ctx.send(embed = embedVar, delete_after = 15)

	elif document.lower() in document_list:
		answer = worksheet.row_values(worksheet.find(document.lower()).row)

		if stay == True:
			await ctx.send('<{}>'.format(answer[2]))
		else:
			await ctx.send('<{}>'.format(answer[2]), delete_after = 15)

	else:
		embedVar = discord.Embed(title = 'Document not found.', description = 'Use `%doc list` for a list of all documents.', color = 0xe3e3e3)
		await ctx.send(embed = embedVar, delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command(name = 'q')
async def questions(ctx, *, arg):
	question = arg
	question = question.lower()
	worksheet = sheet.get_worksheet(FAQ)
	questions_list = worksheet.col_values(2)
	stay = False
	in_list = 0

	if question.endswith(' %stay'):
		question = question.replace(' %stay', '')
		stay = True
	
	question_keywords = question.split()

	for i in question_keywords:
		for j in questions_list:
			if i in j.split():
				in_list += 1
				break

	highest_match = process.extractOne(question, questions_list)

	if highest_match[0] in questions_list and highest_match[1] >= 80 and in_list == len(question_keywords):
		answer = worksheet.row_values(worksheet.find(highest_match[0]).row)
		embedVar = discord.Embed(description = answer[2], color = 0xe3e3e3)
		
		if stay == True:
			await ctx.send(embed = embedVar)

		else:
			await ctx.send(embed = embedVar, delete_after = 15)

	else:
		embedVar = discord.Embed(title = 'Question not found.', description = 'Please be more specific.', color = 0xe3e3e3)
		await ctx.send(embed = embedVar, delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command(name = 'operator')
async def op_file(ctx, *, arg):
	stay = False

	if arg.endswith(' %stay'):
		arg = arg.replace(' %stay', '')
		stay = True

	if arg == 'archive list':
		embedVar = discord.Embed(title = 'Archive commands:', description = '`basic`, `clinical`, `profile`, `archive1`, `archive2`, `archive3`, `archive4`, `promotion`', color = 0xe3e3e3)

		if stay == True:
			await ctx.send(embed = embedVar)
		else:
			await ctx.send(embed = embedVar, delete_after = 15)

	else:
		arg = arg.split()

		if len(arg) == 3:
			if arg[1] in ['corne', 'red', '3', '2', 'poison', 'fu']:
				arg[0] = arg[0] + ' ' + arg[1]
				arg[1] = arg[2]
				del arg[2]

		arg = load_archives(arg)

		if arg[0] == 'None':
			embedVar = discord.Embed(title = 'Operator not found.', color = 0xe3e3e3)
			await ctx.send(embed = embedVar, delete_after = 15)

		elif arg[1] == 'None':
			embedVar = discord.Embed(title = 'Archive not found.', color = 0xe3e3e3)
			await ctx.send(embed = embedVar, delete_after = 15)

		elif len(arg) != 2:
			embedVar = discord.Embed(title = 'Archive not found.', color = 0xe3e3e3)
			await ctx.send(embed = embedVar, delete_after = 15)

		else:
			try:
				table['handbookDict'][arg[0]]['storyTextAudio'][int(arg[1])]['storyTitle']
			except IndexError:
				embedVar = discord.Embed(title = 'Archive not found.', color = 0xe3e3e3)
				await ctx.send(embed = embedVar, delete_after = 15)
				return

			story_title = table['handbookDict'][arg[0]]['storyTextAudio'][int(arg[1])]['storyTitle']
			story_string = table['handbookDict'][arg[0]]['storyTextAudio'][int(arg[1])]['stories'][0]['storyText']

			if len(story_string) > 2000:
				story_string = story_string.split('\n')
				story_section = []
				embeds = []
				temp_string = story_string[0]
				index = 0

				for i in story_string[1:]:
					if (len(temp_string) + len(i)) < 2000:
						temp_string = temp_string + '\n' + i

					else:
						story_section.append(temp_string)
						temp_string = i
						index += 1

				story_section.append(temp_string)

				for i in range(index + 1):
					embeds.append(discord.Embed(title = story_title, description = story_section[i], color = 0xe3e3e3))

				paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
				await paginator.run(embeds)

			else:
				embedVar = discord.Embed(title = story_title, description = story_string, color = 0xe3e3e3)
				
				if stay == True:
					await ctx.send(embed = embedVar)

				else:
					await ctx.send(embed = embedVar, delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command()
async def lines(ctx, *, arg):
	stay = False

	if arg.endswith(' %stay'):
		arg = arg.replace(' %stay', '')
		stay = True

	if count_lines(arg) == 'None':
		embedVar = discord.Embed(title = 'Document not found.', description = 'Use `%doc list` for a list of all documents.', color = 0xe3e3e3)
		await ctx.send(embed = embedVar, delete_after = 15)

	else:
		embedVar = discord.Embed(title = 'Number of lines: {}'.format(count_lines(arg)), color = 0xe3e3e3)

		if stay == True:
			await ctx.send(embed = embedVar)
		else:
			await ctx.send(embed = embedVar, delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command()
async def search(ctx, *, arg):
	stay = False

	if arg.endswith(' %stay'):
		arg = arg.replace(' %stay', '')
		stay = True

	if arg.startswith('%operator '):
		arg = arg.replace('%operator ', '')
		arg = arg.split()

		if len(arg) == 3:
			if arg[1] in ['corne', 'red', '3', '2', 'poison', 'fu']:
				arg[0] = arg[0] + ' ' + arg[1]
				arg[1] = arg[2]
				del arg[2]

		elif len(arg) > 2:
			embedVar = discord.Embed(title = 'Please enter only one keyword.', color = 0xe3e3e3)
			await ctx.send(embed = embedVar, delete_after = 15)
			return

		temp = arg[1]
		op_search = load_archives(arg)
		op_search[1] = temp
		has_data = False
		title = 0
		embeds = []

		if op_search[0] == 'None':
			embedVar = discord.Embed(title = 'Operator not found.', description = 'Please spell the Operator name correctly.', color = 0xe3e3e3)
			await ctx.send(embed = embedVar, delete_after = 15)
			return

		for i in table['handbookDict'][op_search[0]]['storyTextAudio']:
			story_string = i['stories'][0]['storyText']
			split_story = story_string.split()

			for j in split_story:
				if op_search[1].lower() in j.lower():
					has_data = True

					if len(story_string) > 2000:
						story_string = story_string.split('\n')
						story_section = []
						temp_string = story_string[0]
						index = 0

						for i in story_string[1:]:
							if (len(temp_string) + len(i)) < 2000:
								temp_string = temp_string + '\n' + i

							else:
								story_section.append(temp_string)
								temp_string = i
								index += 1

						story_section.append(temp_string)

						for i in range(index + 1):
							embeds.append(discord.Embed(title = table['handbookDict'][op_search[0]]['storyTextAudio'][title]['storyTitle'], description = story_section[i], color = 0xe3e3e3))

					else:
						embeds.append(discord.Embed(title = table['handbookDict'][op_search[0]]['storyTextAudio'][title]['storyTitle'], description = story_string, color = 0xe3e3e3))

					break

			title += 1
		
		paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
		await paginator.run(embeds)	

		if has_data == True:
			return

		embedVar = discord.Embed(title = 'Keyword not found.', color = 0xe3e3e3)
		await ctx.send(embed = embedVar, delete_after = 15)
		return				

	else:
		matches = load_story(arg)
		search_string = str(matches).strip('[]')
		search_string = search_string.replace('\', \'', '\n\n')
		search_string = search_string.replace('\', \"', '\n\n')
		search_string = search_string.replace('\", \'', '\n\n')
		search_string = search_string.replace('\", \"', '\n\n')
		search_string = search_string[:0] + search_string[1:]
		search_string = search_string[:len(search_string) - 1] + search_string[len(search_string):]

		if len(matches) == 1:
			embedVar = discord.Embed(title = 'Matching line:', description = search_string, color = 0xe3e3e3)

		elif len(matches) == 0:
			embedVar = discord.Embed(title = 'File or keyword not found.', color = 0xe3e3e3)

		else:	
			embedVar = discord.Embed(title = 'Matching lines:', description = search_string, color = 0xe3e3e3)
			
		if stay == True:
			await ctx.send(embed = embedVar)

		else:
			await ctx.send(embed = embedVar, delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command(name = 'add', pass_context = True)
async def append(ctx, *, arg):
	worksheet = sheet.get_worksheet(TRUSTED)
	id_list = worksheet.col_values(1)

	if str(ctx.author.id) in id_list:
		if arg.startswith('question '):
			add_question = arg
			add_question = add_question.replace('question ', '')
			split_question = add_question.split('|')
			worksheet = sheet.get_worksheet(FAQ)
			questions_list = worksheet.col_values(2)

			if split_question[0] in questions_list:
				await ctx.send('This question is already added.', delete_after = 15)

			else:
				first_row = len(questions_list)
				add_row = first_row + 1	
				worksheet.update_cell(add_row, 1, first_row)
				worksheet.update_cell(add_row, 2, split_question[0])
				worksheet.update_cell(add_row, 3, split_question[1])
				message = await ctx.send('Question added.', delete_after = 15)

		elif arg.startswith('doc '):
			new_doc = arg
			new_doc = new_doc.replace('doc ', '')
			split_doc = new_doc.split('|')
			worksheet = sheet.get_worksheet(DOCS)
			document_list = worksheet.col_values(2)

			if new_doc in document_list:
				await ctx.send('{} already exists.'.format(new_doc), delete_after = 15)

			else:
				first_row = len(document_list)
				add_row = first_row + 1	
				worksheet.update_cell(add_row, 1, first_row)
				worksheet.update_cell(add_row, 2, split_doc[0])
				worksheet.update_cell(add_row, 3, split_doc[1])
				await ctx.send('Document added.', delete_after = 15)

		elif arg.startswith('cutie ') and ctx.author.id == 221724337902845954:
			cutie_name = arg
			cutie_name = cutie_name.replace('cutie ', '')
			worksheet = sheet.get_worksheet(CUTIES)
			cuties = worksheet.col_values(1)

			if cutie_name in cuties:
				await ctx.send('{} is already a cutie.'.format(cutie_name), delete_after = 15)
				
			else:
				first_row = len(worksheet.col_values(1))
				add_row = first_row + 1
				worksheet.update_cell(add_row, 1, cutie_name)
				await ctx.send('{} added to cuties.'.format(cutie_name), delete_after = 15)

		elif arg.startswith('trusted ') and ctx.author.id == 221724337902845954:
			trusted_name = arg
			trusted_name = trusted_name.replace('trusted ', '')
			worksheet = sheet.get_worksheet(TRUSTED)
			trusted_list = worksheet.col_values(1)

			if trusted_name in trusted_list:
				await ctx.send('{} is already a member.'.format(trusted_name), delete_after = 15)
			
			elif trusted_name.isdigit() == False:
				await ctx.send('Invalid input.', delete_after = 15)

			else:
				first_row = len(worksheet.col_values(1))
				add_row = first_row + 1
				worksheet.update_cell(add_row, 1, trusted_name)
				await ctx.send('{} added to member list.'.format(trusted_name), delete_after = 15)

		else:
			await ctx.send('Command not found.', delete_after = 15)
	
	else:
		await ctx.send('You do not have permission to use this command.', delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.command()
async def remove(ctx, *, arg):
	if ctx.author.id == 221724337902845954:
		if arg == 'question':
			worksheet = sheet.get_worksheet(FAQ)
			questions_list = worksheet.col_values(2)
			first_row = len(questions_list)
			worksheet.delete_rows(first_row)
			await ctx.send('Last question removed.', delete_after = 15)
		
		elif arg == 'doc':
			worksheet = sheet.get_worksheet(DOCS)
			document_list = worksheet.col_values(2)
			first_row = len(document_list)
			worksheet.delete_rows(first_row)
			await ctx.send('Last document removed.', delete_after = 15)

	else:
		await ctx.send('You do not have permission to use this command.', delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
		
@bot.command()
async def share(ctx, arg):
	email = arg

	if ctx.author.id == 221724337902845954:
		if email:
			sheet.share(email, perm_type = 'user', role = 'writer')
			await ctx.send('Shared with {}.'.format(email), delete_after = 15)

		else:
			await ctx.send('Email not found.', delete_after = 15)
			
	else:
		await ctx.send('You do not have permission to use this command.', delete_after = 15)

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# @bot.event
# async def on_command_error(error, ctx):
# 	if isinstance(error, commands.CommandNotFound):
# 		await error.send("No such command")



@bot.command()
async def paginate(ctx):
	embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
	embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
	embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
	paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
	embeds = [embed1, embed2, embed3]
	await paginator.run(embeds)


#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@bot.event
async def on_message(ctx):
	await bot.process_commands(ctx)

	if ctx.author.id == 221724337902845954:

		if ctx.content == 'who\'s a cutie':
			worksheet = sheet.get_worksheet(CUTIES)
			cuties = worksheet.col_values(1)
			await ctx.channel.send('{}!'.format(random.choice(cuties)))

		elif ctx.content == 'good bot':
			await ctx.channel.send(file=discord.File('images/horny.png'))

		elif ctx.content == '.lauli':
			await ctx.channel.send(file=discord.File('images/amiyathighs1.png'))
			await ctx.channel.send(file=discord.File('images/amiyathighs2.png'))

		elif ctx.content == 'stfu':
			await ctx.channel.send(file=discord.File('images/stfu.png'))

		else:
			return

#————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

print('\n\nOnline.')
bot.run(os.getenv('TOKEN'))

# cd C:\Users\pop22\OneDrive\Desktop\PRTS
# git add .
# git commit -am "update"
# git push heroku master
# heroku logs -a prts-bot