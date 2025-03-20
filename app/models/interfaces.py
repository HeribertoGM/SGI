from config import ma

# CustomSchema made to add 'include' option to Schema
class CustomSchema(ma.Schema):
	class Meta:
		ordered = True

	def __init__(self, *args, **kwargs):
		if 'include' in kwargs:
			include = kwargs.pop('include')
			self.opts.fields.extend(include)

		super(ma.Schema, self).__init__(*args, **kwargs)

# JoinedSchema made to manage joint queries
class JoinedSchema(CustomSchema):
	joins = None
	join_keys = None
	def __init__(self, *args, **kwargs):
		if 'joins' in kwargs:
			self.joins = kwargs.pop('joins')
			self.join_keys = list(self.joins.keys())

		super(CustomSchema, self).__init__(*args, **kwargs)

	def dump(self, rows):
		result = []
		if self.join_keys != None:
			schema_lst = []
			for key in self.join_keys:
				schema_lst.append(self.joins[key]())

			for row in rows:
				row_res = {}
				for i in range(len(row)):
					res = schema_lst[i].dump(row[i])
					res[f'{self.join_keys[i]}_id'] = res['id']

					row_res = dict(row_res, **res)
				
				del row_res['id']
				result.append(row_res)
		
		return result