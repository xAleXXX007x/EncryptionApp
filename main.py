import bitarray
from bitstring import BitArray
import unittest

def bitEncode(text):
  ba = bitarray.bitarray()
  ba.frombytes(text.encode("utf-8"))
  return ba.to01()

def bitDecode(bitcode):
  b = BitArray(bin=bitcode)
  return b.bytes.decode("utf-8")

def toPattern(block, pattern):
  output = ""

  for i in pattern:
    output += block[i - 1]
  
  return output

def toBlocks(bitcode):
  output = []
  mod = len(bitcode) % 64

  if (mod != 0):
    for i in range(0, int(mod / 8)):
      bitcode += "00000000"

  while (len(bitcode) >= 64):
    block = bitcode[:64]
    output.append(block)
    bitcode = bitcode[64:]

  return output

def bitcodeFromBlocks(blocks):
  output = ""

  for block in blocks:
    output += block

  while (output.endswith("00000000")):
    output = output[:-8]
  
  return output

def initialPermutation(block):
  output = ""
  pattern = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
  ]

  for i in pattern:
    output += block[i - 1]
  
  return output

def endingPermutation(block):
  output = ""
  pattern = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9,  49, 17, 57, 25
  ]

  for i in pattern:
    output += block[i - 1]
  
  return output

def E(block):
  output = ""
  pattern = [
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
  ]

  for i in pattern:
    output += block[i - 1]

  return output

def generateKeys(key):
  if (len(key) != 7):
    raise Exception("Key length must be exactly 7 characters")

  bitcode = bitEncode(key)
  key64 = ""

  for i in range(0, 7):
    byte = bitcode[i * 8:(i + 1) * 8]

    if (byte.count("1") % 2 == 0):
      byte += "1"
    else:
      byte += "0"
    
    key64 += byte
  
  pattern = [
    57, 49, 41, 33, 25, 17, 9,  1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4
  ]

  key56 = ""

  for i in pattern:
    key56 += key64[i - 1]
  
  keys = []

  C, D = key56[:28], key56[28:]

  shiftOffset = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

  for i in range(0, 16):
    offset = shiftOffset[i]
    C, D = leftShift(C, offset), leftShift(D, offset)
    keys.append([C, D])
  
  pattern = [
    14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10, 23, 19, 12, 4,
    26, 8,  16, 7,  27, 20, 13, 2,  41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
  ]

  output = []

  for keyPair in keys:
    key56 = keyPair[0] + keyPair[1]
    key = ""

    for i in pattern:
      key += key56[i - 1]

    output.append(key)

  return output
  
def leftShift(key, offset):
  chars = key[:offset]
  return key[offset:] + chars

def xor(a, b):
  if (len(a) != len(b)):
    raise Exception("A length not equal to B length")

  output = ""

  for i in range(0, len(a)):
    if (a[i] != b[i]):
      output += "1"
    else:
      output += "0"
  
  return output

def F(block, key):
  bitcode = E(block)
  bitcode = xor(bitcode, key)

  bits = ""

  for i in range(0, 8):
    bits += S(i, bitcode[i * 6:i * 6 + 6])

  pattern = [
    16, 7,  20, 21, 29, 12, 28, 17,
    1,  15, 23, 26, 5,  18, 31, 10,
    2,  8,  24, 14, 32, 27, 3,  9,
    19, 13, 30, 6,  22, 11, 4,  25
  ]

  output = ""

  for i in pattern:
    output += bits[i - 1]

  return output

SPatterns = [
  [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
  ],
  [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
  ],
  [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
  ],
  [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
  ],
  [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
  ],
  [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
  ],
  [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
  ],
  [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
  ]
]

def S(i, block):
  pattern = SPatterns[i]

  row = int(block[0] + block[5], 2)
  column = int(block[1:5], 2)

  return "{0:04b}".format(pattern[row][column])

def feistel(block, keys):
  block = initialPermutation(block)

  output = ""

  L, R = block[:32], block[32:]

  for i in range(0, 16):
    L = xor(L, F(R, keys[i]))
    L, R = R, L

  output = L + R

  return endingPermutation(output)

def fromFeistel(block, keys):
  block = initialPermutation(block)

  output = ""

  L, R = block[:32], block[32:]

  for i in range(15, -1, -1):
    L, R = R, L
    L = xor(L, F(R, keys[i]))
  
  output = L + R

  return endingPermutation(output)

def encodeDES(text, key):
  encoded = bitEncode(text)
  blocks = toBlocks(encoded)
  keys = generateKeys(key)

  encodedBlocks = []
  
  for block in blocks:
    encodedBlocks.append(feistel(block, keys))
  
  return ''.join(encodedBlocks)

def decodeDes(bitcode, key):
  keys = generateKeys(key)
  blocks = toBlocks(bitcode)
  decodedBlocks = []

  for block in blocks:
    decodedBlocks.append(fromFeistel(block, keys))

  bitcode = bitcodeFromBlocks(decodedBlocks)

  return bitDecode(bitcode)

class TestEncoding(unittest.TestCase):

  def test_bit_ecoding(self):
    self.assertEqual("Hello World!", bitDecode(bitEncode("Hello World!")))
  
  def test_blocks(self):
    encoded = bitEncode("Hello World!")
    blocks = toBlocks(encoded)
    self.assertEqual("Hello World!", bitDecode(bitcodeFromBlocks(blocks)))
  
  def test_permutation(self):
    encoded = bitEncode("Hello World!")
    blocks = toBlocks(encoded)
    permutatedBlocks = []

    for block in blocks:
      permutatedBlocks.append(initialPermutation(block))
    
    restoredBlocks = []

    for block in permutatedBlocks:
      restoredBlocks.append(endingPermutation(block))

    self.assertEqual("Hello World!", bitDecode(bitcodeFromBlocks(restoredBlocks)))

  def test_xor(self):
    a = "1101101"
    b = "1010110"
    
    self.assertEqual(xor(a, b), "0111011")

  def test_f(self):
    keys = generateKeys("abcdefg")
    block = '1101111101000000110111101101001000000000101111101001110111010000'
    L, R = block[:32], block[32:]

    L1, R1 = L, R

    for i in range(0, 16):
      L = xor(L, F(R, keys[i]))
      L, R = R, L

    for i in range(15, -1, -1):
      L, R = R, L
      L = xor(L, F(R, keys[i]))

    self.assertEqual(L1, L)
    self.assertEqual(R1, R)

  def test_s(self):
    self.assertEqual("0101", S(0, "011011"))

  def test_feistel(self):
    encoded = bitEncode("Hello World!")
    blocks = toBlocks(encoded)
    keys = generateKeys("abcdefg")

    encodedBlocks = []
    
    for block in blocks:
      encodedBlocks.append(feistel(block, keys))

    decodedBlocks = []

    for block in encodedBlocks:
      decodedBlocks.append(fromFeistel(block, keys))

    bitcode = bitcodeFromBlocks(decodedBlocks)

    self.assertEqual("Hello World!", bitDecode(bitcode))

  def test_des(self):
    self.assertEqual("Hello World!", decodeDes(encodeDES("Hello World!", "abcdefg"), "abcdefg"))

if __name__ == "__main__":
  unittest.main()
