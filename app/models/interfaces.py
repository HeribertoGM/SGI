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