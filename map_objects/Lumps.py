from random import randint


def Make_lumps(self, x, y):
		for r in range(max_lumps):
			if randint(1,10) == 1:
				self.tile[x][y].blocked = False
				self.tile[x][y].block_sight = False