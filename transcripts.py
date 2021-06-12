import os
import gspread
import string

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

PROLOGUE = 0
CHAPTER0 = 1
CHAPTER1 = 2
CHAPTER2 = 3
CHAPTER3 = 4
CHAPTER4 = 5
CHAPTER5 = 6
CHAPTER6 = 7
CHAPTER7 = 8
CHAPTER8 = 9
GKT = 10
HOSF = 11
COB = 12
AF = 13
SOA = 14
CCB = 15
COU = 16
TOW = 17
DM = 18
GCR = 19
RB = 20
MN = 21

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'json_files/transcript_file.json'
SPREADSHEET_ID = '1DOB5jHmPvGBjIFxYRnFZ2yQXtkhLxTBYZAj5pCFwXrI'

creds = None
creds = ServiceAccountCredentials.from_json_keyfile_name('json_files/transcript_file.json', scopes = SCOPES)

sh = gspread.authorize(creds)
sheet = sh.open("Transcripts")

def load_story(arg):
	search_key = arg

	if arg.startswith('prologue '):
		search_key = search_key.replace('prologue ', '')
		worksheet = sheet.get_worksheet(PROLOGUE)

	elif arg.startswith('chapter 0 '):
		search_key = search_key.replace('chapter 0 ', '')
		worksheet = sheet.get_worksheet(CHAPTER0)

	elif arg.startswith('chapter 1 '):
		search_key = search_key.replace('chapter 1 ', '')
		worksheet = sheet.get_worksheet(CHAPTER1)

	elif arg.startswith('chapter 2 '):
		search_key = search_key.replace('chapter 2 ', '')
		worksheet = sheet.get_worksheet(CHAPTER2)

	elif arg.startswith('chapter 3 '):
		search_key = search_key.replace('chapter 3 ', '')
		worksheet = sheet.get_worksheet(CHAPTER3)

	elif arg.startswith('chapter 4 '):
		search_key = search_key.replace('chapter 4 ', '')
		worksheet = sheet.get_worksheet(CHAPTER4)

	elif arg.startswith('chapter 5 '):
		search_key = search_key.replace('chapter 5 ', '')
		worksheet = sheet.get_worksheet(CHAPTER5)

	elif arg.startswith('chapter 6 '):
		search_key = search_key.replace('chapter 6 ', '')
		worksheet = sheet.get_worksheet(CHAPTER6)

	elif arg.startswith('chapter 7 '):
		search_key = search_key.replace('chapter 7 ', '')
		worksheet = sheet.get_worksheet(CHAPTER7)

	elif arg.startswith('chapter 8 '):
		search_key = search_key.replace('chapter 8 ', '')
		worksheet = sheet.get_worksheet(CHAPTER8)

	elif arg.startswith('gkt '):
		search_key = search_key.replace('gkt ', '')
		worksheet = sheet.get_worksheet(GKT)

	elif arg.startswith('hosf '):
		search_key = search_key.replace('hosf ', '')
		worksheet = sheet.get_worksheet(HOSF)

	elif arg.startswith('cob '):
		search_key = search_key.replace('cob ', '')
		worksheet = sheet.get_worksheet(COB)

	elif arg.startswith('af '):
		search_key = search_key.replace('af ', '')
		worksheet = sheet.get_worksheet(AF)

	elif arg.startswith('soa '):
		search_key = search_key.replace('soa ', '')
		worksheet = sheet.get_worksheet(SOA)
	
	elif arg.startswith('ccb '):
		search_key = search_key.replace('ccb ', '')
		worksheet = sheet.get_worksheet(CCB)

	elif arg.startswith('cou '):
		search_key = search_key.replace('cou ', '')
		worksheet = sheet.get_worksheet(COU)

	elif arg.startswith('tow '):
		search_key = search_key.replace('tow ', '')
		worksheet = sheet.get_worksheet(TOW)

	elif arg.startswith('dm '):
		search_key = search_key.replace('dm ', '')
		worksheet = sheet.get_worksheet(DM)

	elif arg.startswith('gcr '):
		search_key = search_key.replace('gcr ', '')
		worksheet = sheet.get_worksheet(GCR)

	elif arg.startswith('rb '):
		search_key = search_key.replace('rb ', '')
		worksheet = sheet.get_worksheet(RB)
	
	elif arg.startswith('mn '):
		search_key = search_key.replace('mn ', '')
		worksheet = sheet.get_worksheet(MN)

	else:
		matches = list()
		return matches

	search_list = worksheet.col_values(2)
	matches = list()

	if search_key.startswith('last '):
		search_key = search_key.replace('last ', '')
		keywords = search_key.lower()
		keywords = keywords.split()

		for i in reversed(search_list):
			lower_case = i.lower()

			if any(substring in lower_case.split() for substring in keywords) == True:
				matches.append(i)

			if len(matches) > 5:
				break

	else:
		keywords = search_key.lower()
		keywords = keywords.split()

		if keywords[0].isdigit() == True:
			index = int(keywords[0])
			del keywords[0]

			if index > len(search_list):
				return matches

			else:
				for i in search_list[index - 1:]:
					lower_case = i.lower()
					
					if any(substring in lower_case.split() for substring in keywords) == True:
						matches.append(i)

					if len(matches) > 5:
						break

		else:
			for i in search_list:
				lower_case = i.lower()
				if any(substring in lower_case.split() for substring in keywords) == True:
					matches.append(i)

				if len(matches) > 5:
					break
	
	return matches


def count_lines(arg):
	if arg.startswith('prologue'):
		worksheet = sheet.get_worksheet(PROLOGUE)

	elif arg.startswith('chapter 0'):
		worksheet = sheet.get_worksheet(CHAPTER0)

	elif arg.startswith('chapter 1'):
		worksheet = sheet.get_worksheet(CHAPTER1)

	elif arg.startswith('chapter 2'):
		worksheet = sheet.get_worksheet(CHAPTER2)

	elif arg.startswith('chapter 3'):
		worksheet = sheet.get_worksheet(CHAPTER3)

	elif arg.startswith('chapter 4'):
		worksheet = sheet.get_worksheet(CHAPTER4)

	elif arg.startswith('chapter 5'):
		worksheet = sheet.get_worksheet(CHAPTER5)

	elif arg.startswith('chapter 6'):
		worksheet = sheet.get_worksheet(CHAPTER6)

	elif arg.startswith('chapter 7'):
		worksheet = sheet.get_worksheet(CHAPTER7)

	elif arg.startswith('chapter 8'):
		worksheet = sheet.get_worksheet(CHAPTER8)

	elif arg.startswith('gkt'):
		worksheet = sheet.get_worksheet(GKT)

	elif arg.startswith('hosf'):
		worksheet = sheet.get_worksheet(HOSF)

	elif arg.startswith('cob'):
		worksheet = sheet.get_worksheet(COB)

	elif arg.startswith('af'):
		worksheet = sheet.get_worksheet(AF)

	elif arg.startswith('soa'):
		worksheet = sheet.get_worksheet(SOA)
	
	elif arg.startswith('ccb'):
		worksheet = sheet.get_worksheet(CCB)

	elif arg.startswith('cou'):
		worksheet = sheet.get_worksheet(COU)

	elif arg.startswith('tow'):
		worksheet = sheet.get_worksheet(TOW)

	elif arg.startswith('dm'):
		worksheet = sheet.get_worksheet(DM)

	elif arg.startswith('gcr'):
		worksheet = sheet.get_worksheet(GCR)

	elif arg.startswith('rb'):
		worksheet = sheet.get_worksheet(RB)
	
	elif arg.startswith('mn'):
		worksheet = sheet.get_worksheet(MN)

	search_list = worksheet.col_values(2)
	return len(search_list)