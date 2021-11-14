import bitarray
from bitstring import BitArray

def bitEncode(text):
  ba = bitarray.bitarray()
  ba.frombytes(text.encode("utf-8"))
  return ba.to01()

def bitDecode(bitcode):
  b = BitArray(bin=bitcode)
  return b.bytes.decode("utf-8")

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

  keys.append([C, D])

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

  



def main():
  text = "Hello World!"
  bitcode = bitEncode(text)
  blocks = toBlocks(bitcode)
  key = "abcdefg"

  permutatedBlocks = []

  for block in blocks:
    permutatedBlock = initialPermutation(block)
    permutatedBlocks.append(permutatedBlock)
  
  print(generateKeys(key))

if __name__ == "__main__":
  main()
