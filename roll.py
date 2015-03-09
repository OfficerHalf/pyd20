#!/usr/bin/env python
"""DnD Roller Nathan Smith 2013/06/26"""
import random
import argparse
import cmd
import re

class Roll_Console(cmd.Cmd):
	def default(self, line):
		try:
			roll_dice(line)
		except:
			print("Invalid dice! Dice should be in the format d10, 2d20, etc. Do not comma separate dice!")

	def do_EOF(self, line):
		return True

	def do_q(self, line):
		return True

def main():
	random.seed()
	parser = argparse.ArgumentParser(description="DnD Roller")
	parser.add_argument('dice', nargs='*', help="Dice to roll. Examples: [d10, 2d5 1d8, 4d12, d27].")
	parser.add_argument('-m', '--multiple', action='store_true', dest='multiple', default=False, help="Enter interactive roll mode.")
	args = parser.parse_args()

	if args.multiple == True:
		console = Roll_Console()
		console.prompt = ">>> "
		console.cmdloop()
	elif not args.dice:
		parser.print_help()
	else:
		roll_dice(args.dice[0])

def tokenize(expr):
	def maprepl(matchobj):
		token_map = {',':'SEP', ' ':''}
		return token_map[matchobj.group(0)]
	expr = re.sub('[ ,]', maprepl, expr)
	return expr

def roll_dice(dice):
	if not dice:
		return None
	elif dice:
		dice_expr = tokenize(dice)
		dice_result = roller(dice_expr)
		for result in dice_result:
			print(result)

def roller(expr):
	dice = expr.split('SEP')
	results = []
	for die in dice:
		results.append(deval(die))
	return results


def roll(expr):
	expr = str(expr.group(0))
	die = expr.split("d")
	formatted = '['+expr+':'
	sum = 0
	for i in range(int(die[0])):
		num = random.randint(1,int(die[1]))
		sum += num
		formatted += str(num)+','
	formatted = formatted[:-1]+'='+str(sum)+']'
	return formatted

def digitize(expr):
	expr = str(expr.group(0))
	a = expr.find("=")
	b = expr.find("]")
	return expr[a+1:b]

def deval(expr):
	expr = re.sub(r'\d+d\d+', roll, expr)
	numerical = re.sub(r'\[\d+d\d+:(\d,?)+=\d+\]', digitize, expr)
	total = eval(numerical)
	expr += " = "+str(total)
	return expr


if __name__ == "__main__":
    main()