from discord.ext import commands
import time

class cooldowns:
	def cooldown(self, seconds):
	       async def cooldown_predicate(ctx):
	           if not ctx.guild:
	           
	           	raise commands.NoPrivateMessage('Guild only')
	           if not (cd := await ctx.bot.db.fetchrow(f'SELECT * FROM cooldown WHERE id={ctx.author.id} AND command=$1', str(ctx.command))):
	           	await ctx.bot.db.execute(f'INSERT INTO cooldown VALUES ({ctx.author.id}, $1, {int(time.time()+seconds)})', str(ctx.command))
	           	return True
	           else:
	           	ends_at = cd[0]['ends_at'] or 0
	           	if ends_at > time.time():
	           		raise commands.CommandOnCooldown(f'Command {ctx.command} is on cooldown', retry_after=ends_at - time.time())
	           	else:
	           	   await ctx.bot.db.execute(f'UPDATE cooldown SET ends_at={int(time.time()+seconds)} WHERE id={ctx.author.id} AND command=$1', str(ctx.command))
	           	   return True
	           return commands.check(cooldown_predicate)