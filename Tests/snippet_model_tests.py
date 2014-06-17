from snippets.models import Snippet
import mock

class ModelTests():
	def setUp(self):
		super(ModelTests, self).setUp()
		self.snippet = Snippet
	def model_creation(self):
		self.snippet = mock.MagicMock()
		self.snippet.created = 132456798
		self.snippet.name = 'John Doe'

