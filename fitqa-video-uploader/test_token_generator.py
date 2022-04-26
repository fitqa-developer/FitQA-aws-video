import unittest
import token_generator


class TestTokenGenerator(unittest.TestCase):
  def test_length(self):
    self.assertEqual(token_generator._TOKEN_LENGTH, len(token_generator.random_character_with_prefix("123")))
    self.assertEqual(token_generator._TOKEN_LENGTH, len(token_generator.random_character_with_prefix("")))
    self.assertEqual(token_generator._TOKEN_LENGTH, len(token_generator.random_character_with_prefix("abc")))
    self.assertEqual(token_generator._TOKEN_LENGTH, len(token_generator.random_character_with_prefix("1a2s3d")))

  def test_prefix(self):
    self.assertEqual(True, token_generator.random_character_with_prefix("123").startswith("123"))
    self.assertEqual(True, token_generator.random_character_with_prefix("abc").startswith("abc"))
    self.assertEqual(False, token_generator.random_character_with_prefix("123").startswith("abc"))
    self.assertEqual(True, token_generator.random_character_with_prefix("1").startswith("1"))
    self.assertEqual(True, token_generator.random_character_with_prefix("").startswith(""))


if __name__ == '__main__':
  unittest.main()
