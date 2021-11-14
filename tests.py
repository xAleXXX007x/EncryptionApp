import unittest
import encoding

# Класс для проведения unit-тестов
class TestEncoding(unittest.TestCase):

  # Тест кодирования и расшифровки в битовое представление
  def test_bit_encoding(self):
    self.assertEqual("Hello World!", encoding.bitDecode(encoding.bitEncode("Hello World!".encode("utf-8"))).decode("utf-8"))
  
  # Тест разбиения множества бит на блоки
  def test_blocks(self):
    encoded = encoding.bitEncode("Hello World!".encode("utf-8"))
    blocks = encoding.toBlocks(encoded)
    self.assertEqual("Hello World!", encoding.bitDecode(encoding.bitcodeFromBlocks(blocks)).decode("utf-8"))
  
  # Тест начальной и конечной перестановки
  def test_permutation(self):
    encoded = encoding.bitEncode("Hello World!".encode("utf-8"))
    blocks = encoding.toBlocks(encoded)
    permutatedBlocks = []

    for block in blocks:
      permutatedBlocks.append(encoding.initialPermutation(block))
    
    restoredBlocks = []

    for block in permutatedBlocks:
      restoredBlocks.append(encoding.endingPermutation(block))

    self.assertEqual("Hello World!", encoding.bitDecode(encoding.bitcodeFromBlocks(restoredBlocks)).decode("utf-8"))

  # Тест работы XOR
  def test_xor(self):
    a = "1101101"
    b = "1010110"
    
    self.assertEqual(encoding.xor(a, b), "0111011")

  # Тест работы функции F
  def test_f(self):
    keys = encoding.generateKeys("abcdefg")
    block = '1101111101000000110111101101001000000000101111101001110111010000'
    L, R = block[:32], block[32:]

    L1, R1 = L, R

    for i in range(0, 16):
      L = encoding.xor(L, encoding.F(R, keys[i]))
      L, R = R, L

    for i in range(15, -1, -1):
      L, R = R, L
      L = encoding.xor(L, encoding.F(R, keys[i]))

    self.assertEqual(L1, L)
    self.assertEqual(R1, R)

  # Тест работы функции S-box'ов
  def test_s(self):
    self.assertEqual("0101", encoding.S(0, "011011"))

  # Тест работы функции Фейстеля
  def test_feistel(self):
    encoded = encoding.bitEncode("Hello World!".encode("utf-8"))
    blocks = encoding.toBlocks(encoded)
    keys = encoding.generateKeys("abcdefg")

    encodedBlocks = []
    
    for block in blocks:
      encodedBlocks.append(encoding.feistel(block, keys))

    decodedBlocks = []

    for block in encodedBlocks:
      decodedBlocks.append(encoding.fromFeistel(block, keys))

    bitcode = encoding.bitcodeFromBlocks(decodedBlocks)

    self.assertEqual("Hello World!", encoding.bitDecode(bitcode).decode("utf-8"))

  # Тест работы основных функций шифрования и расшифрования
  def test_des(self):
    self.assertEqual("Hello World!", encoding.decodeDES(encoding.encodeDES("Hello World!".encode("utf-8"), "abcdefg", "foobar"), "abcdefg", "foobar").decode("utf-8"))

if __name__ == "__main__":
  unittest.main()
