class UserRegistry:
	def __init__(self):
		self.__user = {} # user -> ip
		self.__ip = {}   # ip -> user

	def register(self, new_user: str, new_ip: str):
		self.__user[new_user] = new_ip
		self.__ip[new_ip] = new_user

	def name_taken(self, username: str) -> bool:
		return username in self.__user

	def ip_known(self, ip: str) -> bool:
		return ip in self.__ip

	def get_user(self, ip: str) -> str:
		return self.__ip[ip]

	def get_ip(self, user: str) -> str:
		return self.__user[user]

	def ip(self):
		for ip in self.__ip.keys():
			yield ip

	def delete_user(self, key: str):
		ip_to_del = self.__user[key]
		del self.__user[key]
		del self.__ip[ip_to_del]

	def delete_ip(self, key: str):
		user_to_del = self.__ip[key]
		del self.__ip[key]
		del self.__user[user_to_del]

	def rename_user(self, ip_addr: str, new_user: str):
		if not self.name_taken(new_user):
			old_user = self.__ip[ip_addr]
			self.__ip[ip_addr] = new_user

			del self.__user[old_user]
			self.__user[new_user] = ip_addr