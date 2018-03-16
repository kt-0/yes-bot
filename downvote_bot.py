
import praw, re, pdb, time, datetime, os
import pandas as pd
import numpy as np
from time import sleep

df1 = pd.read_excel("assets/excel/comment_data.xlsx", "Sheet1")
df2 = pd.read_excel("assets/excel/comment_data.xlsx", "Sheet2")


has_question = re.compile(r"^.(?=(?:.+?\?)).*$", re.M).search
is_bot = re.compile(r"^(\bI\sam\sa\sbot\.)$", re.M).search
has_or = re.compile(r"^.(?=(?:.*\sor\s)).*$", re.I | re.M).search
and_which = re.compile(r"^.* and (?=.* which ).*$", re.I | re.M).search
how_and = re.compile(r"^.(?=(?:.*\show\s.*\sand\s)).*$", re.I | re.M).search
has_yes = re.compile(r"^(Yes|Yes\.)$").search


def main():

	print("df1.shape: ", df1.shape[0])
	start_time = datetime.datetime.now()
	print(start_time)

	try:
		df1.drop_duplicates("Comment_ID", inplace=True)
		df1.dropna(axis=0, how="any", inplace=True)
		df1.reset_index(drop=True, inplace=True)

		df2.reset_index(drop=True, inplace=True)
		df2.drop_duplicates('Comment_ID', inplace=True)

	except Exception as e:
		time_stamp = time.strftime("%m/%d/%y %H:%M:%S", time.localtime())
		print("Time:{} Exception near top of main: {}".format(time_stamp, e))
		with open("assets/logging/errors.txt", "a") as f:
			time_stamp = time.strftime("%m/%d/%y %H:%M:%S", time.localtime())
			f.write("Time Stamp: {}    || Exception dropping duplicates or NaN: {}  \n\n".format(time_stamp, e))



	initial_shape = df1.shape[0]
	print("df1.shape: ", initial_shape)

	comments_voted = df2["Comment_ID"].tolist()
	actual = "TBD"

	loc_has_yes = has_yes

	print("starting reddit loop")
	print(datetime.datetime.now())

	reddit = praw.Reddit("bot1")
	subreddit = reddit.subreddit("all")

	period = datetime.timedelta(minutes=10)
	max_runtime = datetime.timedelta(minutes=30)
	timer = datetime.datetime.now()


	for comment in subreddit.stream.comments(pause_after=4):


		users_voted = df2["Username"].tolist()
		print(len(users_voted))

		curr_time = datetime.datetime.now()
		curr_interval = (curr_time - timer)
		time_elapsed = (curr_time - start_time)

		try:
			if (comment is None):
				print("Comment is None. Sleeping it off")
				time.sleep(10)
				continue

			if (loc_has_yes(comment.body) and comment.id not in comments_voted):
				comment.downvote()
				author = str(comment.author)
				subR = comment.subreddit_name_prefixed[2:]
				parent = comment.parent()
				parent_id = str(parent.id)
				parent_author = "deleted" if (parent.author == None) else str(parent.author)
				parent_body = parent.body if not comment.is_root else ("Title: "+parent.title+"| selftext: "+parent.selftext)
				proposed = str(check_format(parent_body)).upper()
				parent_created = time.strftime("%m/%d/%y %H:%M:%S", time.localtime(parent.created))

				df1.loc[df1.shape[0]]=[parent_created, parent_author, subR, author, parent_id, proposed, actual, parent_body]

				#converted from epoch time
				comm_created = time.strftime("%m/%d/%y %H:%M:%S", time.localtime(comment.created))

				if author not in users_voted:

					#add a new row to Sheet2
					df2.loc[df2.shape[0]]=[comm_created, author, subR, [str(comment.id)], 1]

				else:
					i = users_voted.index(author)
					cur_score = df2.get_value(i, "num_votes")
					new_score = int(cur_score)+1

					df2['Comment_ID'] = df2['Comment_ID'].astype(list)
					print("Repeat offender found: ", author)

					comment_list = [df2.get_value(i, "Comment_ID"), comment.id]

					df2.loc[i,'num_votes'] = new_score
					x = df2.set_value(i, "Comment_ID", comment_list)



			if (time_elapsed > max_runtime):
				print("df1.shape[0]", df1.shape[0])
				num_new_matches = (int(df1.shape[0]) - initial_shape)
				print("Approx. {} minutes have elapsed. Number of new matches found:{} ".format(max_runtime, num_new_matches))
				write_xlsx()
				break

			if (curr_interval > period):
				print("df1.shape[0]", df1.shape[0])

				num_new_matches = (int(df1.shape[0]) - initial_shape)
				print("Approx. {} minutes have elapsed. Number of new matches found:{} ".format(period, num_new_matches))
				write_xlsx()
				# restart the timer
				timer = datetime.datetime.now()
				continue

		except Exception as e:
			time_stamp = time.strftime("%m/%d/%y %H:%M:%S", time.localtime())

			print("Time:{} ,Exception in reddit loop: {}".format(time_stamp, e))
			with open("assets/logging/errors.txt", "a") as f:
				f.write("Time Stamp: {}    || Exception in main loop: {}  \n\n".format(time_stamp, e))
			print("Sleeping 20 seconds")
			time.sleep(20)
			continue


	print("finished reddit loop. End time: ", datetime.datetime.now())


# This function checks whether a comment poses a question in a manner that would
# allow another user to erroneously respond with "Yes" (hurr hurr, circlejerk)
def check_format(comment):

	found_match = False

	if (has_or(comment) or and_which(comment) or how_and(comment)):
		found_match = True

	return found_match


def write_xlsx():
	# Create a Pandas Excel writer using XlsxWriter as the engine.
	writer = pd.ExcelWriter("assets/excel/comment_data.xlsx", engine="xlsxwriter")
	df1.to_excel(writer, sheet_name="Sheet1")
	df2.to_excel(writer, sheet_name="Sheet2")

	workbook  = writer.book
	worksheet1 = writer.sheets["Sheet1"]
	worksheet2 = writer.sheets["Sheet2"]

	bold = workbook.add_format({"bold": 1})

	# Add a format. Green fill with dark green text. GREEN = GOOD
	format_true = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})

	number_rows = len(df1.index)
	worksheet1.conditional_format("G2:G{}".format(number_rows), {"type": "cell", "criteria":"==", "value": "True", "format": format_true})

	# Format the columns by width

	# general info columns
	worksheet1.set_column("A:A", 3)
	worksheet1.set_column("B:E", 20)
	worksheet1.set_column("F:F", 15)

	# Boolean columns
	worksheet1.set_column("G:H", 8)
	worksheet1.set_column("I:I", 35)

	# general info columns
	worksheet2.set_column("A:A", 3)
	worksheet2.set_column("B:D", 20)
	worksheet2.set_column("E:E", 15)
	worksheet2.set_column("F:F", 8)

	# Close the Pandas Excel writer and output the Excel file.
	writer.save()



main()
