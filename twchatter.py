from twitchio.ext import commands
import json
from aioconsole import ainput

class Chatter(commands.Bot):
	def __init__(self, botconffile):
		with open(botconffile, "r") as read_file: self.confdict = json.load(read_file)

		tempchannel = input(f'Channel to connect to(hit enter for {self.confdict["channel"]}): ')
		if tempchannel != "":
			self.confdict["channel"] = tempchannel
			with open(botconffile, "w") as outfile: json.dump(self.confdict, outfile, indent = 4)

		super().__init__(token=self.confdict["token"], prefix='!', initial_channels=["#" + self.confdict["channel"]])

	async def event_ready(self):
		print(f'Logged in as - {self.nick} at channel: {self.confdict["channel"]}')
		print(f'User id is: {self.user_id}')
		print("-" * 80)
		while True: await self.connected_channels[0].send(await ainput())

	async def event_message(self, message): #bug in twitcho? message.content seem to lose the first character if it is a ':'
		if message.echo: print(self.confdict["username"] + ": " + message.content)
		else: print(message.author.display_name + ": " + message.content)

def main():
	chttr = Chatter("twchatter.json")
	chttr.run()

if __name__ == "__main__":
	main()